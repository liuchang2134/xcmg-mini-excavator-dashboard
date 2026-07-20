from __future__ import annotations

import json
import subprocess
import unittest
from html.parser import HTMLParser
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
DEMO = REPO / "ppt-integration-demo"
DATA = REPO / "data" / "ppt-insights"
REQUIRED_DATA = {
    "slides.json",
    "market.json",
    "tonnage.json",
    "field-evaluation.json",
    "portfolio.json",
    "roadmap.json",
    "evidence.json",
}
REQUIRED_FIELDS = {
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


def iter_evidence_ids(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            if key == "evidence_id":
                yield from nested if isinstance(nested, list) else [nested]
            else:
                yield from iter_evidence_ids(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from iter_evidence_ids(nested)


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag in {"a", "link"} and values.get("href"):
            self.links.append(values["href"])
        if tag in {"img", "script"} and values.get("src"):
            self.links.append(values["src"])


class PptIntegrationDemoTests(unittest.TestCase):
    def test_required_data_files_exist(self):
        self.assertEqual(REQUIRED_DATA, {path.name for path in DATA.glob("*.json")})

    def test_all_records_have_traceability_fields(self):
        for name in REQUIRED_DATA:
            data = load_json(name)
            for record in data["records"]:
                missing = REQUIRED_FIELDS - record.keys()
                self.assertFalse(missing, f"{name}:{record.get('id')} missing {missing}")
                self.assertEqual("3-4t", record["tonnage"])
                self.assertTrue(record["conclusion"].get("zh"))
                self.assertTrue(record["conclusion"].get("en"))

    def test_slide_scope_is_complete_and_contiguous(self):
        slides = load_json("slides.json")["records"]
        numbers = [int(record["source_slide"]) for record in slides]
        self.assertEqual(list(range(48, 69)), numbers)
        self.assertEqual(21, len(slides))
        for record in slides:
            self.assertTrue(record["zh"]["raw_text"].strip())
            self.assertTrue(record["en"]["summary"].strip())
            self.assertTrue((DEMO / record["thumbnail"]).is_file())

    def test_every_evidence_reference_resolves(self):
        evidence = load_json("evidence.json")["records"]
        valid = {record["id"] for record in evidence}
        for name in REQUIRED_DATA - {"evidence.json", "slides.json"}:
            data = load_json(name)
            for evidence_id in iter_evidence_ids(data):
                self.assertIn(evidence_id, valid, f"{name} references {evidence_id}")
        covered_slides = {
            int(slide)
            for record in evidence
            for slide in (
                record["source_slide"]
                if isinstance(record["source_slide"], list)
                else [record["source_slide"]]
            )
        }
        self.assertEqual(set(range(48, 69)), covered_slides)

    def test_field_evaluation_has_no_generated_score(self):
        field = load_json("field-evaluation.json")
        allowed = {"优势", "差距", "待验证", "资料未覆盖"}
        for record in field["records"]:
            self.assertIn(record["finding_status"], allowed)
            self.assertNotIn("score", record)
            self.assertNotIn("rating_score", record)

    def test_field_images_exist(self):
        tonnage = load_json("tonnage.json")
        for record in tonnage["records"]:
            if record.get("image"):
                self.assertTrue((DEMO / record["image"]).is_file(), record["image"])

    def test_demo_pages_and_local_links_exist(self):
        pages = {
            "index.html",
            "market-insights.html",
            "tonnage-insight.html",
            "product-portfolio.html",
            "improvement-roadmap.html",
            "evidence-center.html",
        }
        self.assertEqual(pages, {path.name for path in DEMO.glob("*.html")})
        for name in pages:
            path = DEMO / name
            html = path.read_text(encoding="utf-8")
            self.assertIn("XCMG ARC内部资料", html)
            self.assertIn('meta name="robots" content="noindex,nofollow"', html)
            parser = LinkParser()
            parser.feed(html)
            for link in parser.links:
                if link.startswith(("http:", "https:", "mailto:", "#", "data:")):
                    continue
                clean = link.split("#", 1)[0].split("?", 1)[0]
                if not clean:
                    continue
                target = (path.parent / clean).resolve()
                self.assertTrue(target.exists(), f"{name} -> {link}")

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
