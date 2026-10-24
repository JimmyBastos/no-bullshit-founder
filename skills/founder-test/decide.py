#!/usr/bin/env python3
"""Test decisions for founder-test. Standard library only, no network.

Reads one test file (founder/tests/NNN.json), written before the test started,
and applies its rule to the data collected so far. The model never decides a
test by reading numbers by eye: it runs this script.

    python3 decide.py founder/tests/001.json
    python3 decide.py founder/tests/001.json --out founder/tests/001.md
    python3 decide.py founder/tests/001.json --json --today 2026-11-20

The file (see test.example.json in this folder):

    id, hypothesis, channel   what is being tested, for the report
    started                   the date the test went live (YYYY-MM-DD)
    rule                      written before launch, never edited after:
      target_cold_sales       cold sales needed after the refund window
      max_cac                 the most one customer may cost (from founder-numbers)
      cap_spend               the total budget; never extended
      deadline                the last day of the test (YYYY-MM-DD)
      min_visitors            people who must see the offer for a no to count
      refund_days             legal cancel window (default 7)
      kill_multiple           pause a variant after spending this many times
                              max_cac with no cold sale (default 2)
      p_best                  probability needed to call a variant the leader
                              (default 0.95)
    prediction                optional {conversion, source}: the model's guess
                              from founder-idea, to compare with reality
    arms                      one per variant (angle, channel or price):
      name, spend, visitors
      sales                   [{date, warm, refunded}]

How sales count:

    warm       a buyer who knows the founder. Shown, never counted for the gate.
    pending    a cold sale still inside the refund window.
    confirmed  a cold sale past the refund window and not refunded.

The gate:

    PASS          confirmed cold sales >= target, and spend per confirmed
                  sale <= max_cac
    FAIL          deadline passed or budget spent, enough people saw it, and
                  the gate is not met
    INCONCLUSIVE  deadline passed or budget spent, but fewer than
                  min_visitors saw it: the test, not the idea, failed
    WAITING       enough sales, but some are still inside the refund window
    RUNNING       none of the above yet
"""

import argparse
import datetime
import json
import random
import sys


class TestError(Exception):
    pass


def _date(v, field):
    try:
        return datetime.date.fromisoformat(str(v))
    except ValueError:
        raise TestError("%s is not a date (YYYY-MM-DD): %r" % (field, v))


def _num(v, field):
    try:
        x = float(v)
    except (TypeError, ValueError):
        raise TestError("%s is not a number: %r" % (field, v))
    if x < 0:
        raise TestError("%s cannot be negative" % field)
    return x


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise TestError("no such file: %s" % path)
    except json.JSONDecodeError as e:
        raise TestError("%s is not valid JSON: %s" % (path, e))


def p_best(arms, draws=20000, seed=0):
    """Chance each arm has the best cold conversion rate (Beta-Binomial, flat prior)."""
    rng = random.Random(seed)
    wins = [0] * len(arms)
    for _ in range(draws):
        samples = [rng.betavariate(1 + a["cold"], 1 + max(a["visitors"] - a["cold"], 0)) for a in arms]
        wins[samples.index(max(samples))] += 1
    return [w / float(draws) for w in wins]


def analyse(spec, today=None):
    """Return every number in the report. Pure function, easy to test."""
    rule = spec.get("rule")
    if not isinstance(rule, dict):
        raise TestError("'rule' is missing: write the rule before the test starts")
    for k in ("target_cold_sales", "max_cac", "cap_spend", "deadline", "min_visitors"):
        if k not in rule:
            raise TestError("rule.%s is missing" % k)
    target = _num(rule["target_cold_sales"], "rule.target_cold_sales")
    max_cac = _num(rule["max_cac"], "rule.max_cac")
    cap = _num(rule["cap_spend"], "rule.cap_spend")
    deadline = _date(rule["deadline"], "rule.deadline")
    min_visitors = _num(rule["min_visitors"], "rule.min_visitors")
    refund_days = int(_num(rule.get("refund_days", 7), "rule.refund_days"))
    kill = _num(rule.get("kill_multiple", 2), "rule.kill_multiple")
    need_p = _num(rule.get("p_best", 0.95), "rule.p_best")
    today = today or datetime.date.today()
    if not spec.get("arms"):
        raise TestError("'arms' is empty: add at least one variant")

    arms = []
    for i, a in enumerate(spec["arms"]):
        name = a.get("name", "variant %d" % (i + 1))
        spend = _num(a.get("spend", 0), "%s.spend" % name)
        visitors = _num(a.get("visitors", 0), "%s.visitors" % name)
        warm = cold = confirmed = pending = refunds = 0
        for j, s in enumerate(a.get("sales", [])):
            if s.get("refunded"):
                refunds += 1
                continue
            if s.get("warm"):
                warm += 1
                continue
            cold += 1
            if _date(s.get("date"), "%s.sales[%d].date" % (name, j)) + datetime.timedelta(days=refund_days) <= today:
                confirmed += 1
            else:
                pending += 1
        action = "PAUSE" if cold == 0 and max_cac > 0 and spend >= kill * max_cac else "KEEP"
        arms.append({"name": name, "spend": spend, "visitors": visitors, "warm": warm, "cold": cold,
                     "confirmed": confirmed, "pending": pending, "refunds": refunds,
                     "conversion": cold / visitors if visitors else None,
                     "cost_per_sale": spend / cold if cold else None, "action": action})

    if len(arms) > 1:
        for a, p in zip(arms, p_best(arms)):
            a["p_best"] = p
            if p >= need_p:
                a["action"] = "LEADER"
    total = {k: sum(a[k] for a in arms) for k in ("spend", "visitors", "warm", "cold", "confirmed", "pending", "refunds")}
    cost_per_confirmed = total["spend"] / total["confirmed"] if total["confirmed"] else None
    over = today > deadline or total["spend"] >= cap

    if total["confirmed"] >= target and cost_per_confirmed is not None and cost_per_confirmed <= max_cac:
        gate = ("PASS", "%d confirmed cold sales at %.2f each, within max CAC %.2f" % (
            total["confirmed"], cost_per_confirmed, max_cac))
    elif total["confirmed"] + total["pending"] >= target and total["pending"] and (
            total["spend"] / (total["confirmed"] + total["pending"]) <= max_cac):
        gate = ("WAITING", "%d sales are still inside the %d-day refund window" % (total["pending"], refund_days))
    elif over and total["visitors"] < min_visitors:
        gate = ("INCONCLUSIVE", "only %d people saw the offer, %d were needed for a no to count" % (
            total["visitors"], min_visitors))
    elif over:
        gate = ("FAIL", "%d confirmed cold sales of %d needed%s" % (
            total["confirmed"], target,
            "" if cost_per_confirmed is None else ", at %.2f each against max CAC %.2f" % (cost_per_confirmed, max_cac)))
    else:
        gate = ("RUNNING", "%d of %d cold sales so far, %.2f of %.2f budget spent, %d days left" % (
            total["cold"], target, total["spend"], cap, (deadline - today).days))

    pred = spec.get("prediction")
    real = total["cold"] / total["visitors"] if total["visitors"] else None
    return {"id": spec.get("id", ""), "hypothesis": spec.get("hypothesis", ""), "channel": spec.get("channel", ""),
            "today": today.isoformat(), "rule": rule, "arms": arms, "total": total,
            "cost_per_confirmed": cost_per_confirmed, "budget_left": max(cap - total["spend"], 0),
            "stop_spending": total["spend"] >= cap, "gate": gate,
            "prediction": pred.get("conversion") if isinstance(pred, dict) else None,
            "prediction_source": pred.get("source") if isinstance(pred, dict) else None,
            "real_conversion": real}


def _pct(v):
    return "n/a" if v is None else "%.1f%%" % (v * 100)


def _money(v):
    return "n/a" if v is None else "{:,.2f}".format(v)


def report(a):
    L = ["# Test %s: %s" % (a["id"], a["gate"][0]), ""]
    if a["hypothesis"]:
        L += ["Hypothesis: %s" % a["hypothesis"], ""]
    L += ["**%s.** %s." % (a["gate"][0], a["gate"][1][0].upper() + a["gate"][1][1:]), "",
          "Checked on %s against the rule written before the test." % a["today"], ""]
    if a["stop_spending"]:
        L += ["**The budget is spent. Stop all spending now; the cap is never extended.**", ""]
    L += ["## Variants", "",
          "| variant | spend | visitors | cold sales | confirmed | pending | warm | refunds | conversion | cost per sale | chance best | action |",
          "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |"]
    for v in a["arms"]:
        L.append("| %s | %s | %d | %d | %d | %d | %d | %d | %s | %s | %s | %s |" % (
            v["name"], _money(v["spend"]), v["visitors"], v["cold"], v["confirmed"], v["pending"], v["warm"],
            v["refunds"], _pct(v["conversion"]), _money(v["cost_per_sale"]),
            _pct(v.get("p_best")) if "p_best" in v else "n/a", v["action"]))
    t = a["total"]
    L += ["", "Total: %s spent, %s left, %d visitors, %d confirmed cold sales, %d pending, %d warm, %d refunds." % (
        _money(t["spend"]), _money(a["budget_left"]), t["visitors"], t["confirmed"], t["pending"], t["warm"], t["refunds"]),
        "",
        "- PAUSE: spent %sx max CAC with no cold sale. Pausing only cuts spending, so it needs no approval." %
        "{:g}".format(float(a["rule"].get("kill_multiple", 2))),
        "- LEADER: at least %s chance of the best conversion. Moving budget to it needs the user's approval." %
        _pct(float(a["rule"].get("p_best", 0.95))),
        "- Warm sales show the product works. They never count for the gate.", ""]
    L += ["## Prediction against reality", ""]
    if a["prediction"] is None:
        L.append("No prediction was logged before the test.")
    else:
        L.append("The model predicted %s conversion (%s). Real cold conversion so far: %s." % (
            _pct(a["prediction"]), a["prediction_source"] or "source not given", _pct(a["real_conversion"])))
        L.append("Log both in founder/evidence.md. Across several tests, this shows whether model predictions can be trusted.")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("test", help="the test file, founder/tests/NNN.json")
    ap.add_argument("--out", help="write the report here (markdown)")
    ap.add_argument("--json", action="store_true", help="print the numbers as JSON")
    ap.add_argument("--today", help="check as of this date (YYYY-MM-DD)")
    args = ap.parse_args(argv)
    try:
        today = _date(args.today, "--today") if args.today else None
        a = analyse(load(args.test), today)
    except TestError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(dict(a, gate={"result": a["gate"][0], "reason": a["gate"][1]}), indent=1))
        return 0
    text = report(a)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("wrote %s" % args.out)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
