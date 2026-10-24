import contextlib
import io
import json
import math
import unittest

from _load import load, example

ue = load("founder-numbers", "unit_economics")


def spec():
    with open(example("founder-numbers", "example.json"), encoding="utf-8") as fh:
        return json.load(fh)


class UnitEconomics(unittest.TestCase):
    def test_example_reproduces_the_plan(self):
        a = ue.analyse(spec())
        self.assertAlmostEqual(a["contribution"], 4.76, places=2)
        self.assertEqual(round(a["margin_at_plan"] * 100), 38)
        self.assertEqual(math.ceil(a["breakeven_per_day"]), 186)
        self.assertEqual(round(a["year1_profit"]), 93926)
        self.assertEqual(a["startup"], 25280)
        self.assertEqual(a["payback_month"], 8)
        self.assertEqual(round(a["cash_needed"]), 34092)
        self.assertEqual(a["flags"], [])
        self.assertAlmostEqual(a["max_cac"], 4.76 * 12, places=2)
        self.assertEqual(a["gate"][0], "PASS")

    def test_price_below_variable_cost_is_flagged(self):
        s = spec()
        s["price"] = 1.50
        a = ue.analyse(s)
        self.assertTrue(math.isinf(a["breakeven_per_day"]))
        self.assertTrue(any("loses money" in f for f in a["flags"]))

    def test_breakeven_above_capacity_is_flagged(self):
        s = spec()
        s["capacity_per_day"] = 150
        a = ue.analyse(s)
        self.assertTrue(any("capacity is 150" in f for f in a["flags"]))

    def test_what_ifs_move_the_right_way(self):
        base = ue.analyse(spec())
        cheaper = ue.analyse(spec(), price=base["price"] * 0.9)
        fewer = ue.analyse(spec(), volume=0.8)
        self.assertLess(cheaper["year1_profit"], base["year1_profit"])
        self.assertGreater(cheaper["breakeven_per_day"], base["breakeven_per_day"])
        self.assertLess(fewer["year1_profit"], base["year1_profit"])
        self.assertEqual(len(ue.sensitivity(spec())), 4)

    def test_bad_input_is_refused_not_guessed(self):
        s = spec()
        s["ramp_per_day"] = [100] * 11
        with self.assertRaises(ue.NumbersError):
            ue.analyse(s)
        s = spec()
        del s["price"]
        with self.assertRaises(ue.NumbersError):
            ue.analyse(s)
        s = spec()
        s["variable"][0]["cost"] = "lots"
        with self.assertRaises(ue.NumbersError):
            ue.analyse(s)

    def test_ramp_is_required_not_assumed(self):
        s = spec()
        del s["ramp_per_day"]
        with self.assertRaises(ue.NumbersError):
            ue.analyse(s)

    def test_bad_numbers_are_errors_not_crashes(self):
        for field, value in (("days_per_month", 0), ("plan_per_day", "abc"), ("purchases_per_customer", 0)):
            s = spec()
            s[field] = value
            with self.assertRaises(ue.NumbersError, msg=field):
                ue.analyse(s)
        s = spec()
        s["ramp_per_day"] = ["a"] * 12
        with self.assertRaises(ue.NumbersError):
            ue.analyse(s)

    def test_zero_volume_gives_no_margin_instead_of_infinity(self):
        s = spec()
        s["ramp_per_day"] = [0] * 12
        s["plan_per_day"] = 0
        self.assertIsNone(ue.analyse(s)["margin_at_plan"])

    def test_gate_two(self):
        s = spec()
        s["cac_benchmark"]["value"] = 80
        a = ue.analyse(s)
        self.assertEqual(a["gate"][0], "FAIL")
        self.assertTrue(any("Max CAC" in f for f in a["flags"]))
        del s["cac_benchmark"]
        self.assertEqual(ue.analyse(s)["gate"][0], "INCOMPLETE")
        s = spec()
        s["price"] = 1.50
        self.assertEqual(ue.analyse(s)["gate"][0], "FAIL")

    def test_cost_what_if(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(ue.main([example("founder-numbers", "example.json"), "--cost", "1.15", "--json"]), 0)
        self.assertLess(json.loads(out.getvalue())["contribution"], 4.76)

    def test_report_mentions_the_key_numbers(self):
        s = spec()
        text = ue.report(s, ue.analyse(s))
        self.assertIn("R$4.76", ue.report(dict(s, currency="R$"), ue.analyse(dict(s, currency="R$"))))
        for needle in ("$4.76", "186 cups a day", "**38%**", "$93,926", "month 8", "Max CAC: $57.12", "Gate 2: PASS"):
            self.assertIn(needle, text)


if __name__ == "__main__":
    unittest.main()
