import math
import unittest

from tools.crane_data import load_crane_workbook
from tools.crane_scoring import (
    CATEGORY_WEIGHTS,
    CONDITIONS,
    OVERALL_WEIGHTS,
    normalize,
    score_sheet,
    weighted_average,
)


class CraneScoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = load_crane_workbook()
        cls.sheets = {sheet.label: sheet for sheet in cls.workbook.sheets}

    def test_weight_groups_and_condition_count(self):
        self.assertTrue(math.isclose(sum(CATEGORY_WEIGHTS.values()), 1.0))
        self.assertTrue(math.isclose(sum(OVERALL_WEIGHTS.values()), 1.0))
        self.assertEqual(len(CONDITIONS), 6)
        for condition in CONDITIONS:
            self.assertTrue(condition["metric_patterns"])

    def test_normalization_matches_platform_behavior(self):
        self.assertEqual(normalize({"a": 10.0, "b": 20.0}, "high"), {"a": 0.0, "b": 100.0})
        self.assertEqual(normalize({"a": 10.0, "b": 20.0}, "low"), {"a": 100.0, "b": 0.0})
        self.assertEqual(normalize({"a": 10.0, "b": 10.0}, "high"), {"a": 100.0, "b": 100.0})

    def test_weighted_average_enforces_coverage(self):
        score, coverage = weighted_average([(100.0, 0.5), (None, 0.5)])
        self.assertIsNone(score)
        self.assertEqual(coverage, 0.5)
        score, coverage = weighted_average([(100.0, 0.6), (None, 0.4)])
        self.assertEqual(score, 100.0)
        self.assertEqual(coverage, 0.6)

    def test_four_complete_rt_sheets_have_parameter_analysis(self):
        for label in ["RT-60t", "RT-75t", "RT-100t", "RT-130t"]:
            with self.subTest(label=label):
                scored = score_sheet(self.sheets[label])
                xcmg = next(product for product in scored["products"] if product["is_xcmg"])
                self.assertIsNotNone(xcmg["parameter_score"])
                self.assertEqual(set(xcmg["condition_scores"]), {item["id"] for item in CONDITIONS})

    def test_missing_configuration_does_not_become_zero(self):
        scored = score_sheet(self.sheets["RT-60t"])
        xcmg = next(product for product in scored["products"] if product["is_xcmg"])
        self.assertIsNone(xcmg["configuration_score"])
        self.assertIsNone(xcmg["overall_score"])
        self.assertIn("配置状态", xcmg["not_ranked_reason"])

    def test_known_incomplete_sheets_do_not_rank_xcmg(self):
        for label in ["RT-160t", "AT-150t"]:
            with self.subTest(label=label):
                scored = score_sheet(self.sheets[label])
                xcmg = next(product for product in scored["products"] if product["is_xcmg"])
                self.assertIsNone(xcmg["overall_score"])
                self.assertIsNone(xcmg["overall_rank"])


if __name__ == "__main__":
    unittest.main()
