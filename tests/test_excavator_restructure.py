import json
import re
import unittest
from pathlib import Path

from tools.build_excavator_dashboards import ROOT, SOURCE_FILES
from tools.ppt_scope import OVERVIEW_SLIDES, SLUG_SLIDE_RANGES


class ExcavatorRestructureTests(unittest.TestCase):
    def test_updated_presentation_scope_matches_the_247_slide_deck(self):
        self.assertIn(16, OVERVIEW_SLIDES)
        self.assertIn(245, OVERVIEW_SLIDES)
        self.assertNotIn(246, OVERVIEW_SLIDES)
        self.assertIn(247, OVERVIEW_SLIDES)
        expected_starts = {
            "excavator-1-2t": 19,
            "excavator-2-3t": 38,
            "excavator-35t": 51,
            "excavator-4-5t": 72,
            "excavator-5-6t": 93,
            "excavator-8-10t": 111,
            "excavator-12-14t": 129,
            "excavator-14-16t-short-tail": 130,
            "excavator-21-24t": 155,
            "excavator-24-28t": 172,
            "excavator-28-33t": 173,
            "excavator-33-40t": 202,
            "excavator-40-60t": 219,
        }
        for slug, start in expected_starts.items():
            with self.subTest(slug=slug):
                self.assertEqual(SLUG_SLIDE_RANGES[slug][0][0], start)

    def test_updated_source_manifest_is_traceable_without_publishing_the_deck(self):
        manifest = json.loads(
            (ROOT / "data/source-presentations/source-manifest.json").read_text(
                encoding="utf-8"
            )
        )
        current = manifest["current_excavator_market_deck"]
        self.assertEqual(current["slide_count"], 247)
        self.assertEqual(
            current["sha256"],
            "B819F0AA0496CBB39835376BDE16E134C0FCCDFA8209639613890C6B6AB98A58",
        )
        self.assertEqual(current["classification"], "XCMG ARC INTERNAL")
        self.assertFalse(current["publish_binary"])

    def test_tonnage_pages_use_the_eight_section_reading_order(self):
        section_order = [
            "summary",
            "market-insight",
            "product-positioning",
            "overall",
            "condition-overview",
            "upgrade-roadmap",
            "raw",
        ]
        for meta in SOURCE_FILES:
            html = (ROOT / meta["output"]).read_text(encoding="utf-8")
            with self.subTest(page=meta["output"]):
                positions = [html.index(f'id="{section_id}"') for section_id in section_order]
                self.assertEqual(positions, sorted(positions))
                self.assertNotIn('id="job-applications"', html)
                self.assertNotIn('id="engineering-insight"', html)
                self.assertNotIn("核心规格产品参数及配置对比", html)
                self.assertNotRegex(html, r"徐工VS(?:久保田|卡特|卡特彼勒|三一)")

    def test_application_analysis_is_integrated_into_scored_conditions(self):
        for meta in SOURCE_FILES:
            html = (ROOT / meta["output"]).read_text(encoding="utf-8")
            if meta["slug"] == "excavator-7-8t":
                continue
            with self.subTest(page=meta["output"]):
                overview = html.split('id="condition-overview"', 1)[1].split(
                    'class="conditionSection"', 1
                )[0]
                self.assertIn("主要客户", overview)
                self.assertIn("客户需求", overview)
                condition_blocks = re.findall(
                    r'<section id="cond\d+" class="conditionSection".*?</section>',
                    html,
                    flags=re.DOTALL,
                )
                self.assertGreaterEqual(len(condition_blocks), 6)
                self.assertTrue(
                    any("作业任务" in block and "客户需求" in block for block in condition_blocks)
                )

    def test_upgrade_summary_combines_score_gaps_with_current_ppt_actions(self):
        for meta in SOURCE_FILES:
            html = (ROOT / meta["output"]).read_text(encoding="utf-8")
            with self.subTest(page=meta["output"]):
                roadmap = html.split('id="upgrade-roadmap"', 1)[1].split('id="raw"', 1)[0]
                self.assertIn("评分差距", roadmap)
                self.assertIn("升级动作", roadmap)
                self.assertIn("验证状态", roadmap)
                self.assertNotIn("已经完成", roadmap)


if __name__ == "__main__":
    unittest.main()
