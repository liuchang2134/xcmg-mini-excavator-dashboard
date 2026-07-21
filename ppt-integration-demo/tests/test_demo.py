from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
DEMO = REPO / "ppt-integration-demo"
DATA = REPO / "data" / "ppt-insights"
CORE_DATA = {
    "slides.json",
    "market.json",
    "tonnage.json",
    "field-evaluation.json",
    "portfolio.json",
    "roadmap.json",
    "evidence.json",
}
NEW_DATA = {"tonnage-3-4t-view.json", "excavator-overview.json"}
TRACE_FIELDS = {
    "id",
    "tonnage",
    "model",
    "competitor",
    "scenario",
    "metric",
    "conclusion",
    "source_slide",
    "source_type",
    "as_of_date",
    "status",
    "validation_status",
}
PROTECTED = {
    "arc.html",
    "index.html",
    "assets/dashboard.css",
    "assets/dashboard.js",
    "assets/i18n.js",
}


def load_json(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def evidence_ids(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            if key == "evidence_id":
                yield from nested if isinstance(nested, list) else [nested]
            else:
                yield from evidence_ids(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from evidence_ids(nested)


class PptIntegrationDemoTests(unittest.TestCase):
    def test_required_data_files_exist(self):
        names = {path.name for path in DATA.glob("*.json")}
        self.assertTrue(CORE_DATA | NEW_DATA <= names)

    def test_core_records_are_traceable_and_bilingual(self):
        for name in CORE_DATA:
            for record in load_json(name)["records"]:
                missing = TRACE_FIELDS - record.keys()
                self.assertFalse(missing, f"{name}:{record.get('id')} missing {missing}")
                self.assertEqual("3-4t", record["tonnage"])
                self.assertTrue(record["conclusion"].get("zh"))
                self.assertTrue(record["conclusion"].get("en"))

    def test_3_4t_slide_scope_is_complete(self):
        slides = load_json("slides.json")["records"]
        self.assertEqual(list(range(48, 69)), [int(item["source_slide"]) for item in slides])
        for record in slides:
            self.assertTrue(record["zh"]["raw_text"].strip())
            self.assertTrue((DEMO / record["thumbnail"]).is_file())

    def test_excavator_overview_scope_is_complete(self):
        overview = load_json("excavator-overview.json")["records"]
        self.assertEqual(list(range(3, 16)), [int(item["source_slide"]) for item in overview])
        for record in overview:
            self.assertTrue(TRACE_FIELDS <= record.keys())
            self.assertEqual("all", record["tonnage"])
            self.assertTrue(record["zh"]["raw_text"].strip())
            self.assertTrue((DEMO / record["thumbnail"]).is_file())

    def test_view_model_keeps_scoring_boundary_and_quantitative_data(self):
        view = load_json("tonnage-3-4t-view.json")
        self.assertIn("不改变", view["meta"]["scoring_boundary"]["zh"])
        self.assertEqual(4, len(view["market"]["volume"]))
        tonnage_records = load_json("tonnage.json")["records"]
        self.assertEqual(9, len(tonnage_records))
        self.assertEqual(8, len([item for item in tonnage_records if item["id"].startswith("scenario-")]))
        self.assertGreaterEqual(len(view["paper_comparison"]["metrics"]), 9)
        self.assertGreaterEqual(len(view["paper_comparison"]["configuration_findings"]), 4)

    def test_full_3_4t_analysis_is_rendered_as_native_content(self):
        html = (DEMO / "index.html").read_text(encoding="utf-8")
        script = (DEMO / "assets" / "integrated.js").read_text(encoding="utf-8")
        expanded = (DEMO / "assets" / "expanded-content.js").read_text(encoding="utf-8")
        visuals = load_json("visual-assets.json")
        self.assertEqual(5, html.count("data-ppt-nav="))
        self.assertIn("expanded-content.js", html)
        self.assertIn("visual-assets", script)
        self.assertIn("expanded.paperGroups", script)
        self.assertIn("expanded.fieldGroups", script)
        self.assertIn("scenarioAssessments", expanded)
        self.assertIn("competitionDimensions", expanded)
        self.assertIn("scenarioSequence", script)
        self.assertIn("scenarioImageCaptions", script)
        self.assertNotIn("scenarioTabs", script)
        scenario_assets = {
            name
            for name in __import__("re").findall(r"s0(?:49|50|52|53|54|55|56|57|58)-photo-\d{2}\.jpg", script)
        }
        self.assertEqual(24, len(scenario_assets))
        tables = {
            table["id"]
            for slide in visuals["slides"]
            if 59 <= int(slide["slide"]) <= 66
            for table in slide["tables"]
        }
        self.assertTrue({f"s{slide:03d}-table-02" for slide in range(59, 67)} <= tables)
        self.assertNotIn("slide-thumb", script)

    def test_evidence_references_resolve_and_cover_every_slide(self):
        evidence = load_json("evidence.json")["records"]
        valid_ids = {item["id"] for item in evidence}
        for name in CORE_DATA - {"evidence.json", "slides.json"}:
            for item in evidence_ids(load_json(name)):
                self.assertIn(item, valid_ids, f"{name} references {item}")
        covered = {
            int(page)
            for item in evidence
            for page in (item["source_slide"] if isinstance(item["source_slide"], list) else [item["source_slide"]])
        }
        self.assertEqual(set(range(48, 69)), covered)

    def test_field_evaluation_has_no_generated_score(self):
        allowed = {"优势", "差距", "待验证", "资料未覆盖"}
        for record in load_json("field-evaluation.json")["records"]:
            self.assertIn(record["finding_status"], allowed)
            self.assertNotIn("score", record)
            self.assertNotIn("rating_score", record)

    def test_only_integrated_and_overview_pages_remain(self):
        self.assertEqual(
            {"index.html", "excavator-overview.html"},
            {path.name for path in DEMO.glob("*.html")},
        )
        for name in ("index.html", "excavator-overview.html"):
            html = (DEMO / name).read_text(encoding="utf-8")
            self.assertIn('meta name="robots" content="noindex,nofollow"', html)
            self.assertIn('base href="../"', html)
            self.assertIn("integrated.css", html)
        integrated = (DEMO / "index.html").read_text(encoding="utf-8")
        formal = (REPO / "index.html").read_text(encoding="utf-8")
        for marker in ("44.3", 'id="cond1"', 'id="cond6"', 'id="raw"'):
            self.assertIn(marker, formal)
            self.assertIn(marker, integrated)

    def test_formal_site_files_match_main(self):
        protected = set(PROTECTED)
        protected.update(path.name for path in REPO.glob("excavator-*.html"))
        for relative in sorted(protected):
            result = subprocess.run(
                ["git", "diff", "--quiet", "main", "--", relative],
                cwd=REPO,
                check=False,
            )
            self.assertEqual(0, result.returncode, f"Protected file changed: {relative}")


if __name__ == "__main__":
    unittest.main()
