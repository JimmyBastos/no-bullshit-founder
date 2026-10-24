#!/usr/bin/env python3
"""Unit economics for founder-numbers. Standard library only, no network.

Takes one JSON file describing the business and prints the numbers a CFO would
check before a single dollar is spent: what one unit earns, the real margin at
the volume you plan, how many units a day you need to break even, what year 1
looks like month by month, and how long it takes to earn the startup money back.

    python3 unit_economics.py founder/numbers.json
    python3 unit_economics.py founder/numbers.json --out founder/cfo.md
    python3 unit_economics.py founder/numbers.json --json
    python3 unit_economics.py founder/numbers.json --price 7.00 --volume 0.8 --cost 1.15

The input (see example.json in this folder):

    business          name, for the report
    unit              what you sell one of: "cup", "order", "client-month"
    currency          symbol for the report (default "$")
    price             price per unit, before tax
    variable          [{label, cost}]  cost of ONE unit: ingredients, packaging,
                      shipping, card fees, a per-unit commission
    fixed_monthly     [{label, cost}]  costs you pay every month whatever you sell:
                      rent, salaries, software, insurance
    startup           [{label, cost}]  one-off spend before you open
    days_per_month    selling days in a month (default 30)
    capacity_per_day  the most units a day you can physically sell (optional)
    ramp_per_day      12 numbers: units a day in each month of year 1 (required:
                      month 1 is almost never the full volume)
    plan_per_day      the volume once it runs (optional; default = last ramp month)
    purchases_per_customer  times one customer buys in year 1 (default 1)
    cac_benchmark     {value, channel, source}: what one customer costs on the
                      likely channel, from a public source (optional)

Every number in the report comes from that file. Nothing is looked up or
guessed. If a field is missing the tool says so instead of filling it in.

--price, --volume and --cost run a what-if without editing the file: --price
replaces the price, --volume scales every volume (0.8 = 20 percent fewer
sales), --cost scales every unit cost (1.15 = 15 percent more).

Gate 2 passes when contribution is above zero and max CAC (contribution times
purchases per customer) is at least the CAC benchmark.
"""

import argparse
import json
import math
import sys


class NumbersError(Exception):
    pass


CURRENCY = "$"


def _money(v):
    sign = "-" if v < 0 else ""
    return "%s%s%s" % (sign, CURRENCY, "{:,.2f}".format(abs(v)))


def _whole(v):
    sign = "-" if v < 0 else ""
    return "%s%s%s" % (sign, CURRENCY, "{:,.0f}".format(abs(round(v))))


def _num(v, field):
    try:
        return float(v)
    except (TypeError, ValueError):
        raise NumbersError("%s is not a number: %r" % (field, v))


def _sum(items, field):
    total = 0.0
    for i, it in enumerate(items or []):
        if not isinstance(it, dict) or "cost" not in it:
            raise NumbersError("%s[%d] needs a 'cost'" % (field, i))
        try:
            total += float(it["cost"])
        except (TypeError, ValueError):
            raise NumbersError("%s[%d].cost is not a number: %r" % (field, i, it["cost"]))
    return total


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise NumbersError("no such file: %s" % path)
    except json.JSONDecodeError as e:
        raise NumbersError("%s is not valid JSON: %s" % (path, e))


def analyse(spec, price=None, volume=1.0):
    """Return a dict of every number in the report. Pure function, easy to test."""
    global CURRENCY
    CURRENCY = spec.get("currency", "$")
    if "price" not in spec and price is None:
        raise NumbersError("'price' is missing")
    p = _num(price if price is not None else spec["price"], "price")
    if p <= 0:
        raise NumbersError("price must be above zero")
    days = _num(spec.get("days_per_month", 30), "days_per_month")
    if days <= 0:
        raise NumbersError("days_per_month must be above zero")
    var = _sum(spec.get("variable"), "variable")
    fixed = _sum(spec.get("fixed_monthly"), "fixed_monthly")
    startup = _sum(spec.get("startup"), "startup")

    ramp = spec.get("ramp_per_day")
    if not isinstance(ramp, list) or len(ramp) != 12:
        raise NumbersError("'ramp_per_day' needs 12 numbers, one per month of year 1. "
                           "Month 1 is almost never the full volume, so it is not filled in for you.")
    ramp = [_num(v, "ramp_per_day[%d]" % i) * volume for i, v in enumerate(ramp)]
    plan = _num(spec["plan_per_day"], "plan_per_day") * volume if "plan_per_day" in spec else ramp[-1]
    purchases = _num(spec.get("purchases_per_customer", 1), "purchases_per_customer")
    if purchases <= 0:
        raise NumbersError("purchases_per_customer must be above zero")

    contribution = p - var
    contribution_pct = contribution / p
    breakeven_day = math.inf if contribution <= 0 else fixed / (contribution * days)
    plan_units_month = plan * days
    margin_at_plan = (contribution - fixed / plan_units_month) / p if plan_units_month > 0 else None
    max_cac = contribution * purchases
    bench = spec.get("cac_benchmark")
    bench_value = _num(bench["value"], "cac_benchmark.value") if isinstance(bench, dict) and "value" in bench else None

    months = []
    cumulative = -startup
    payback_month = None
    for m, per_day in enumerate(ramp, start=1):
        units = per_day * days
        revenue = units * p
        variable_cost = units * var
        profit = revenue - variable_cost - fixed
        cumulative += profit
        if payback_month is None and cumulative >= 0:
            payback_month = m
        months.append({"month": m, "per_day": per_day, "units": units, "revenue": revenue,
                       "variable": variable_cost, "fixed": fixed, "profit": profit,
                       "cumulative": cumulative})
    year_profit = sum(m["profit"] for m in months)
    year_revenue = sum(m["revenue"] for m in months)
    # the cash you need: startup plus the deepest hole the monthly losses dig
    lowest = min([-startup] + [m["cumulative"] for m in months])
    cash_needed = -lowest

    capacity = spec.get("capacity_per_day")
    flags = []
    if contribution <= 0:
        flags.append("Each unit loses money before rent and salaries: the price is below the variable cost.")
    if capacity is not None and breakeven_day > float(capacity):
        flags.append("Break-even needs %.0f %ss a day but capacity is %s." % (breakeven_day, spec.get("unit", "unit"), capacity))
    if capacity is not None and plan > float(capacity):
        flags.append("The plan (%.0f a day) is above capacity (%s)." % (plan, capacity))
    if year_profit < 0:
        flags.append("Year 1 loses money on operations (%s)." % _whole(year_profit))
    if payback_month is None:
        flags.append("The startup spend is not earned back within year 1.")
    if bench_value is not None and max_cac < bench_value:
        flags.append("Max CAC (%s) is below what customers cost on %s (%s)." % (
            _money(max_cac), bench.get("channel", "the channel"), _money(bench_value)))

    if contribution <= 0:
        gate = ("FAIL", "each sale loses money before fixed costs")
    elif bench_value is None:
        gate = ("INCOMPLETE", "add cac_benchmark with a source to check max CAC")
    elif max_cac < bench_value:
        gate = ("FAIL", "max CAC is below the channel benchmark")
    else:
        gate = ("PASS", "contribution above zero and max CAC above the channel benchmark")

    return {
        "business": spec.get("business", ""), "unit": spec.get("unit", "unit"),
        "price": p, "variable_per_unit": var, "contribution": contribution,
        "contribution_pct": contribution_pct, "fixed_monthly": fixed, "startup": startup,
        "plan_per_day": plan, "margin_at_plan": margin_at_plan, "breakeven_per_day": breakeven_day,
        "capacity_per_day": capacity, "year1_revenue": year_revenue, "year1_profit": year_profit,
        "year1_after_startup": year_profit - startup, "payback_month": payback_month,
        "cash_needed": cash_needed, "months": months, "flags": flags,
        "purchases_per_customer": purchases, "max_cac": max_cac, "cac_benchmark": bench, "gate": gate,
        "variable_items": spec.get("variable", []), "fixed_items": spec.get("fixed_monthly", []),
        "startup_items": spec.get("startup", []),
    }


def sensitivity(spec):
    """The three what-ifs every plan should survive."""
    base = analyse(spec)
    rows = [("Base plan", base)]
    rows.append(("Price -10%", analyse(spec, price=base["price"] * 0.9)))
    rows.append(("Volume -20%", analyse(spec, volume=0.8)))
    worse = json.loads(json.dumps(spec))
    for it in worse.get("variable", []):
        it["cost"] = float(it["cost"]) * 1.15
    rows.append(("Unit costs +15%", analyse(worse)))
    return rows


def _pct(v):
    return "n/a" if v is None else "%.0f%%" % (v * 100)


def report(spec, a):
    u = a["unit"]
    L = []
    L.append("# Unit economics: %s" % (a["business"] or "your business"))
    L.append("")
    L.append("Every number below comes from the input file. Nothing is looked up or guessed.")
    L.append("")
    L.append("## One %s" % u)
    L.append("")
    L.append("| line | per %s |" % u)
    L.append("| --- | ---: |")
    L.append("| Price | %s |" % _money(a["price"]))
    for it in a["variable_items"]:
        L.append("| %s | -%s |" % (it.get("label", "cost"), _money(float(it["cost"]))))
    L.append("| **Contribution** (what each %s leaves to pay the fixed costs) | **%s** (%.0f%%) |"
             % (u, _money(a["contribution"]), a["contribution_pct"] * 100))
    L.append("")
    L.append("## The margin that matters")
    L.append("")
    L.append("Fixed costs: %s a month (%s)." % (_whole(a["fixed_monthly"]), ", ".join(
        "%s %s" % (it.get("label", "cost"), _whole(float(it["cost"]))) for it in a["fixed_items"]) or "none given"))
    L.append("")
    be = a["breakeven_per_day"]
    L.append("- **Break-even: %s %ss a day.** Below that you lose money every month." % (
        "never (each unit loses money)" if math.isinf(be) else "{:,.0f}".format(math.ceil(be)), u))
    L.append("- **Profit margin at your plan** (%s a day): **%s** of every sale, after every cost." % (
        "{:,.0f}".format(a["plan_per_day"]), _pct(a["margin_at_plan"])))
    if a["capacity_per_day"] is not None:
        L.append("- Capacity: %s a day." % a["capacity_per_day"])
    L.append("")
    L.append("## Year 1, month by month")
    L.append("")
    L.append("| month | %ss a day | revenue | profit | cumulative (after %s startup) |" % (u, _whole(a["startup"])))
    L.append("| ---: | ---: | ---: | ---: | ---: |")
    for m in a["months"]:
        L.append("| %d | %s | %s | %s | %s |" % (m["month"], "{:,.0f}".format(m["per_day"]), _whole(m["revenue"]),
                                             _whole(m["profit"]), _whole(m["cumulative"])))
    L.append("")
    L.append("- **Year 1 operating profit: %s** on %s of revenue." % (_whole(a["year1_profit"]), _whole(a["year1_revenue"])))
    L.append("- After the %s startup spend: %s." % (_whole(a["startup"]), _whole(a["year1_after_startup"])))
    L.append("- Startup money earned back: %s." % ("month %d" % a["payback_month"] if a["payback_month"] else "not within year 1"))
    L.append("- Cash you need before it pays for itself: **%s**." % _whole(a["cash_needed"]))
    L.append("")
    L.append("## What you can pay for a customer")
    L.append("")
    L.append("- **Max CAC: %s.** That is contribution (%s) times %s purchase(s) per customer in year 1. "
             "Spend more than this to get a customer and you lose money on them." % (
                 _money(a["max_cac"]), _money(a["contribution"]), "{:g}".format(a["purchases_per_customer"])))
    b = a["cac_benchmark"]
    if isinstance(b, dict) and "value" in b:
        L.append("- Benchmark: %s per customer on %s (source: %s)." % (
            _money(float(b["value"])), b.get("channel", "the channel"), b.get("source", "not given")))
    else:
        L.append("- No CAC benchmark given yet.")
    L.append("")
    L.append("## Gate 2: %s" % a["gate"][0])
    L.append("")
    L.append(a["gate"][1][0].upper() + a["gate"][1][1:] + ".")
    L.append("")
    L.append("## What if")
    L.append("")
    L.append("| scenario | margin at plan | break-even a day | year 1 profit |")
    L.append("| --- | ---: | ---: | ---: |")
    for name, s in sensitivity(spec):
        be = s["breakeven_per_day"]
        L.append("| %s | %s | %s | %s |" % (name, _pct(s["margin_at_plan"]),
                                              "never" if math.isinf(be) else "{:,.0f}".format(math.ceil(be)),
                                              _whole(s["year1_profit"])))
    L.append("")
    if a["flags"]:
        L.append("## Red flags")
        L.append("")
        for f in a["flags"]:
            L.append("- %s" % f)
    else:
        L.append("No red flags in these numbers. They are only as good as the inputs: check every cost against a real quote.")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("numbers", help="the business's numbers.json")
    ap.add_argument("--out", help="write the report here (markdown)")
    ap.add_argument("--json", action="store_true", help="print the numbers as JSON")
    ap.add_argument("--price", type=float, help="what-if price")
    ap.add_argument("--volume", type=float, default=1.0, help="what-if volume multiplier")
    ap.add_argument("--cost", type=float, default=1.0, help="what-if unit cost multiplier")
    args = ap.parse_args(argv)
    try:
        spec = load(args.numbers)
        if args.price is not None:
            spec = dict(spec, price=args.price)
        if args.volume != 1.0:
            spec = dict(spec)
            if "plan_per_day" in spec:
                spec["plan_per_day"] = float(spec["plan_per_day"]) * args.volume
            if isinstance(spec.get("ramp_per_day"), list):
                spec["ramp_per_day"] = [_num(v, "ramp_per_day") * args.volume for v in spec["ramp_per_day"]]
        if args.cost != 1.0:
            spec = json.loads(json.dumps(spec))
            for it in spec.get("variable", []):
                it["cost"] = _num(it.get("cost"), "variable.cost") * args.cost
        a = analyse(spec)
    except NumbersError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    if args.json:
        out = {k: v for k, v in a.items() if not k.endswith("_items")}
        out["breakeven_per_day"] = None if math.isinf(out["breakeven_per_day"]) else out["breakeven_per_day"]
        out["gate"] = {"result": a["gate"][0], "reason": a["gate"][1]}
        print(json.dumps(out, indent=1))
        return 0
    text = report(spec, a)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("wrote %s" % args.out)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
