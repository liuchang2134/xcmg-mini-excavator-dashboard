import unittest

from tools.crane_data import (
    DEFAULT_SOURCE,
    load_crane_workbook,
    normalize_configuration,
    parse_numeric,
)


class CraneDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook = load_crane_workbook(DEFAULT_SOURCE)
        cls.by_label = {sheet.label: sheet for sheet in cls.workbook.sheets}

    def test_numeric_parser_avoids_compound_values(self):
        self.assertEqual(parse_numeric("41,150 kg"), 41150.0)
        self.assertIsNone(parse_numeric("15.2 / 7.6"))
        self.assertIsNone(parse_numeric("2 x 450"))
        self.assertIsNone(parse_numeric("none"))

    def test_configuration_states_keep_unknown_separate_from_absent(self):
        self.assertEqual(normalize_configuration(None), (None, "unrecorded", None))
        self.assertEqual(normalize_configuration("opt")[-2:], ("optional", 60.0))
        self.assertEqual(normalize_configuration("std")[-2:], ("standard", 100.0))
        self.assertEqual(normalize_configuration("none")[-2:], ("absent", 0.0))
        self.assertEqual(
            normalize_configuration("front and rear")[-2:],
            ("present_unspecified", None),
        )

    def test_parameter_and_configuration_sections_are_parsed(self):
        sheet = self.by_label["RT-60t"]
        self.assertEqual(len(sheet.parameter_names), 58)
        self.assertGreaterEqual(len(sheet.configuration_names), 8)
        self.assertEqual(len(sheet.models), 9)
        self.assertIn("Grove GRT765", {model.display_name for model in sheet.models})
        self.assertEqual(
            {metric.subcategory for metric in sheet.models[0].metrics},
            {
                "Transport Parameters",
                "Ground Parameters",
                "Boom and jib",
                "Outriggers",
                "Power",
                "Winches",
                "Lifting performance",
                "Speeds",
            },
        )

    def test_stale_excavator_scoring_block_is_detected_not_parsed(self):
        for sheet in self.workbook.sheets:
            with self.subTest(sheet=sheet.label):
                self.assertIn("stale_excavator_scoring_block_excluded", sheet.anomalies)
                self.assertFalse(any("XE19U" in model.display_name for model in sheet.models))

    def test_known_incomplete_sheets_are_not_rankable(self):
        rt160 = self.by_label["RT-160t"]
        xcr165 = next(model for model in rt160.models if model.is_xcmg)
        self.assertEqual(xcr165.parameter_coverage, 0)
        self.assertIn("xcmg_parameter_data_missing", rt160.anomalies)

        at150 = self.by_label["AT-150t"]
        self.assertIn("suspected_rt130_competitor_headers", at150.anomalies)
        self.assertIn("no_rankable_competitor", at150.anomalies)

    def test_partial_competitor_coverage_is_visible(self):
        rt75 = self.by_label["RT-75t"]
        zoomlion = next(model for model in rt75.models if model.brand == "Zoomlion")
        self.assertLess(zoomlion.parameter_coverage, 0.6)
        self.assertIn("low_parameter_coverage", zoomlion.anomalies)


if __name__ == "__main__":
    unittest.main()
