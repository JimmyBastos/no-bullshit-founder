import datetime
import json
import unittest

from _load import load, example

dc = load("founder-test", "decide")


def spec():
    with open(example("founder-test", "test.example.json"), encoding="utf-8") as fh:
        return json.load(fh)


def day(s):
    return datetime.date.fromisoformat(s)


def sale(date, warm=False, refunded=False):
    return {"date": date, "warm": warm, "refunded": refunded}


class Decide(unittest.TestCase):
    def test_example_while_running(self):
        a = dc.analyse(spec(), day("2026-11-12"))
        self.assertEqual(a["gate"][0], "RUNNING")
        pain, outcome = a["arms"]
        self.assertEqual((pain["cold"], pain["confirmed"], pain["pending"], pain["warm"], pain["refunds"]),
                         (2, 1, 1, 1, 1))
        self.assertEqual(outcome["action"], "PAUSE")
        self.assertEqual(pain["action"], "KEEP")

    def test_warm_sales_never_count(self):
        s = spec()
        s["arms"] = [{"name": "network", "spend": 0, "visitors": 400,
                      "sales": [sale("2026-11-02", warm=True)] * 10}]
        a = dc.analyse(s, day("2026-11-30"))
        self.assertEqual(a["total"]["confirmed"], 0)
        self.assertEqual(a["gate"][0], "FAIL")

    def test_pass_needs_confirmed_sales_within_max_cac(self):
        s = spec()
        s["arms"] = [{"name": "a", "spend": 200, "visitors": 500, "sales": [sale("2026-11-03")] * 4}]
        self.assertEqual(dc.analyse(s, day("2026-11-12"))["gate"][0], "PASS")
        s["arms"][0]["spend"] = 399
        self.assertEqual(dc.analyse(s, day("2026-11-17"))["gate"][0], "FAIL")

    def test_sales_inside_refund_window_wait(self):
        s = spec()
        s["arms"] = [{"name": "a", "spend": 100, "visitors": 500, "sales": [sale("2026-11-10")] * 4}]
        self.assertEqual(dc.analyse(s, day("2026-11-12"))["gate"][0], "WAITING")
        self.assertEqual(dc.analyse(s, day("2026-11-17"))["gate"][0], "PASS")

    def test_too_few_visitors_is_inconclusive_not_a_no(self):
        s = spec()
        s["arms"] = [{"name": "a", "spend": 50, "visitors": 40, "sales": []}]
        self.assertEqual(dc.analyse(s, day("2026-11-17"))["gate"][0], "INCONCLUSIVE")

    def test_budget_cap_stops_spending(self):
        s = spec()
        s["arms"][0]["spend"] = 300
        a = dc.analyse(s, day("2026-11-12"))
        self.assertTrue(a["stop_spending"])
        self.assertIn("Stop all spending", dc.report(a))

    def test_clear_leader(self):
        s = spec()
        s["arms"] = [{"name": "a", "spend": 50, "visitors": 300, "sales": [sale("2026-11-03")] * 15},
                     {"name": "b", "spend": 50, "visitors": 300, "sales": [sale("2026-11-03")]}]
        a = dc.analyse(s, day("2026-11-12"))
        self.assertEqual(a["arms"][0]["action"], "LEADER")
        self.assertGreater(a["arms"][0]["p_best"], 0.99)

    def test_prediction_is_compared_with_reality(self):
        a = dc.analyse(spec(), day("2026-11-12"))
        self.assertEqual(a["prediction"], 0.04)
        self.assertAlmostEqual(a["real_conversion"], 2 / 450.0)
        self.assertIn("Prediction against reality", dc.report(a))

    def test_missing_rule_is_refused(self):
        s = spec()
        del s["rule"]
        with self.assertRaises(dc.TestError):
            dc.analyse(s)
        s = spec()
        del s["rule"]["min_visitors"]
        with self.assertRaises(dc.TestError):
            dc.analyse(s)
        s = spec()
        s["arms"][0]["sales"][0]["date"] = "soon"
        with self.assertRaises(dc.TestError):
            dc.analyse(s)


if __name__ == "__main__":
    unittest.main()
