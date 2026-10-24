#!/usr/bin/env python3
"""Price sensitivity (Van Westendorp) for founder-numbers. Standard library only.

Every respondent answers four questions: at what price would it be too
cheap to trust, a bargain, getting expensive, and too expensive to buy. Plotted
together, those four answers give you an acceptable price range and the price
that leaves the fewest people unhappy.

    python3 van_westendorp.py survey.csv
    python3 van_westendorp.py survey.csv --price 6.50 --out founder/price-range.md
    python3 van_westendorp.py survey.csv --json

Input is a CSV from a survey of real people, with the columns too_cheap, cheap,
expensive, too_expensive (one row per respondent; extra columns are ignored).
Never feed it answers written by a model. A respondent
missing any of the four numbers, or giving them out of order (too cheap must be
the lowest, too expensive the highest), is dropped and counted.

The four points it reports:

    PMC  point of marginal cheapness   below this, too many think it's too cheap
    PME  point of marginal expensiveness above this, too many think it's too expensive
    OPP  optimal price point            as many say "too cheap" as "too expensive"
    IPP  indifference price point       as many say "a bargain" as "expensive"

PMC to PME is the acceptable range. With few respondents, use it to choose
which prices to test with real sales, not as the final price.

When two curves touch along a flat stretch (common when answers cluster on
round numbers), the crossing is reported at the middle of that stretch.
"""

import argparse
import csv
import json
import sys

KEYS = ("too_cheap", "cheap", "expensive", "too_expensive")


class PricingError(Exception):
    pass


def _f(v):
    try:
        x = float(str(v).replace("$", "").replace(",", "").strip())
    except (TypeError, ValueError):
        return None
    return x if x > 0 else None


def read(path):
    """Return (rows, dropped) where rows are (too_cheap, cheap, expensive, too_expensive)."""
    if not path.endswith(".csv"):
        raise PricingError("give a .csv from a survey of real people")
    raw = []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            raw.append(tuple(_f(r.get(k)) for k in KEYS))
    rows, dropped = [], 0
    for r in raw:
        if any(v is None for v in r) or not (r[0] <= r[1] <= r[2] <= r[3]):
            dropped += 1
            continue
        rows.append(r)
    return rows, dropped


def curves(rows, grid):
    n = float(len(rows))
    tc = [sum(1 for r in rows if r[0] >= p) / n for p in grid]          # too cheap at p (falls)
    ch = [sum(1 for r in rows if r[1] >= p) / n for p in grid]          # a bargain at p (falls)
    ex = [sum(1 for r in rows if r[2] <= p) / n for p in grid]          # expensive at p (rises)
    te = [sum(1 for r in rows if r[3] <= p) / n for p in grid]          # too expensive at p (rises)
    return tc, ch, ex, te


def cross(grid, falling, rising):
    """First price where the rising curve meets the falling one.

    A clean crossing is found by linear interpolation. If the curves are equal
    along a flat stretch, the middle of that stretch is returned.
    """
    for i in range(1, len(grid)):
        d0 = rising[i - 1] - falling[i - 1]
        d1 = rising[i] - falling[i]
        if d0 == 0:
            j = i - 1
            while j + 1 < len(grid) and rising[j + 1] - falling[j + 1] == 0:
                j += 1
            return (grid[i - 1] + grid[j]) / 2.0
        if d0 < 0 < d1:
            t = -d0 / (d1 - d0)
            return grid[i - 1] + t * (grid[i] - grid[i - 1])
    return None


def analyse(rows, step=None):
    if len(rows) < 5:
        raise PricingError("need at least 5 complete answers (got %d)" % len(rows))
    lo = min(r[0] for r in rows)
    hi = max(r[3] for r in rows)
    step = step or max(0.01, round((hi - lo) / 400, 2))
    grid, p = [], lo
    while p <= hi + 1e-9:
        grid.append(round(p, 4))
        p += step
    tc, ch, ex, te = curves(rows, grid)
    not_cheap = [1 - v for v in ch]
    not_exp = [1 - v for v in ex]
    pts = {
        "PMC": cross(grid, tc, not_cheap),
        "PME": cross(grid, not_exp, te),
        "OPP": cross(grid, tc, te),
        "IPP": cross(grid, ch, ex),
    }
    return {"n": len(rows), "points": pts, "range": [pts["PMC"], pts["PME"]],
            "median": {k: sorted(r[i] for r in rows)[len(rows) // 2] for i, k in enumerate(KEYS)}}


def report(res, dropped, price=None):
    m = lambda v: "n/a" if v is None else "$%.2f" % v
    p = res["points"]
    L = ["# Price sensitivity", "",
         "%d complete answers%s. Use the range to pick prices to test with real sales." % (
             res["n"], (", %d dropped (incomplete or out of order)" % dropped) if dropped else ""), "",
         "| point | price | what it means |", "| --- | ---: | --- |",
         "| PMC | %s | below this, too many think it is too cheap to be good |" % m(p["PMC"]),
         "| OPP | %s | as many say too cheap as too expensive: the least resistance |" % m(p["OPP"]),
         "| IPP | %s | as many call it a bargain as call it expensive |" % m(p["IPP"]),
         "| PME | %s | above this, too many say it is too expensive to buy |" % m(p["PME"]), "",
         "**Acceptable range: %s to %s.**" % (m(p["PMC"]), m(p["PME"])), ""]
    md = res["median"]
    L.append("Median answers: too cheap %s, a bargain %s, getting expensive %s, too expensive %s." % (
        m(md["too_cheap"]), m(md["cheap"]), m(md["expensive"]), m(md["too_expensive"])))
    if price is not None and p["PMC"] is not None and p["PME"] is not None:
        where = "inside" if p["PMC"] <= price <= p["PME"] else ("below" if price < p["PMC"] else "above")
        L += ["", "Your current price, %s, is **%s** the acceptable range." % (m(price), where)]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("source", help="a CSV from a survey of real people")
    ap.add_argument("--price", type=float, help="your current price, to place it on the range")
    ap.add_argument("--out", help="write the report here (markdown)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        rows, dropped = read(a.source)
        res = analyse(rows)
    except (PricingError, FileNotFoundError) as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(dict(res, dropped=dropped), indent=1))
        return 0
    text = report(res, dropped, a.price)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("wrote %s" % a.out)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
