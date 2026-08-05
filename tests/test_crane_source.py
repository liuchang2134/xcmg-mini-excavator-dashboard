import unittest
from pathlib import Path

import pandas as pd

from tools.crane_data import (
    CRANE_SHEETS,
    DEFAULT_SOURCE,
    EXCLUDED_SHEETS,
    EXPECTED_SHA256,
    workbook_sha256,
)


class CraneSourceTests(unittest.TestCase):
    def test_governed_source_exists_and_matches_fingerprint(self):
        self.assertTrue(DEFAULT_SOURCE.exists())
        self.assertEqual(workbook_sha256(DEFAULT_SOURCE), EXPECTED_SHA256)

    def test_only_six_crane_sheets_are_imported(self):
        names = pd.ExcelFile(DEFAULT_SOURCE).sheet_names
        self.assertEqual(set(CRANE_SHEETS), set(names) - EXCLUDED_SHEETS)
        self.assertEqual(len(CRANE_SHEETS), 6)

    def test_source_register_contains_each_crane_sheet(self):
        register = (DEFAULT_SOURCE.parents[1] / "source-register.csv").read_text(
            encoding="utf-8-sig"
        )
        for sheet in CRANE_SHEETS:
            with self.subTest(sheet=sheet):
                self.assertIn(f"#{sheet.strip()}", register)


if __name__ == "__main__":
    unittest.main()
