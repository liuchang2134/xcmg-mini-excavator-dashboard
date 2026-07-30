"""Run release-gate checks for the formal XCMG ARC benchmark site.

The report is intentionally machine-readable. It verifies that every included
presentation slide, table and visual is reachable from a formal page, that
time-sensitive statements are guarded, and that score/ranking invariants hold.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

try:
    from tools.build_excavator_dashboards import (
        MIN_SCORE_COVERAGE,
        ROOT,
        SOURCE_FILES,
        build_model,
        load_workbook,
    )
    from tools.extract_ppt_source_content import detect_temporal_status
except ModuleNotFoundError:
    from build_excavator_dashboards import (
        MIN_SCORE_COVERAGE,
        ROOT,
        SOURCE_FILES,
        build_model,
        load_workbook,
    )
    from extract_ppt_source_content import detect_temporal_status


SOURCE_CONTENT = ROOT / "data" / "ppt-insights" / "ppt-source-content.json"
TABLE_CONTENT = ROOT / "data" / "ppt-insights" / "ppt-business-tables.json"
REPORT_PATH = ROOT / "data" / "ppt-insights" / "industrial-integrity-report.json"


class ReferenceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag in {"a", "img", "script", "link"}:
            value = values.get("href") or values.get("src")
            if value:
                self.references.append(value)


def sha256(path: Path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def formal_pages():
    return [
        ROOT / "arc.html",
        ROOT / "data-downloads.html",
        ROOT / "excavator-market-overview.html",
        *(ROOT / meta["output"] for meta in SOURCE_FILES),
    ]


def local_reference_issues(page: Path):
    parser = ReferenceParser()
    parser.feed(page.read_text(encoding="utf-8"))
    issues = []
    for reference in parser.references:
        parsed = urlparse(reference)
        if (
            parsed.scheme in {"http", "https", "mailto", "tel", "data"}
            or reference.startswith("#")
        ):
            continue
        target = (page.parent / unquote(parsed.path)).resolve()
        if not target.exists():
            issues.append({"page": page.name, "reference": reference})
    return issues


def model_issues():
    issues = []
    scored_products = 0
    for meta in SOURCE_FILES:
        model = build_model(load_workbook(meta["source"]), meta)
        products = model["products"]
        if len(products) != len(set(products)):
            issues.append({"slug": meta["slug"], "issue": "duplicate_products"})
        if meta["xcmg"] not in products:
            issues.append({"slug": meta["slug"], "issue": "xcmg_model_missing"})

        for product in products:
            score = model["overall"].get(product)
            coverage = model["overallCoverage"].get(product, 0)
            if score is not None:
                scored_products += 1
                if not math.isfinite(score) or not 0 <= score <= 100:
                    issues.append(
                        {
                            "slug": meta["slug"],
                            "product": product,
                            "issue": "invalid_score",
                            "value": score,
                        }
                    )
            if coverage < MIN_SCORE_COVERAGE and score is not None:
                issues.append(
                    {
                        "slug": meta["slug"],
                        "product": product,
                        "issue": "low_coverage_product_scored",
                        "coverage": coverage,
                    }
                )
    return scored_products, issues


def build_report():
    source = json.loads(SOURCE_CONTENT.read_text(encoding="utf-8"))
    tables = json.loads(TABLE_CONTENT.read_text(encoding="utf-8"))
    slide_by_id = {record["id"]: record for record in source["slides"]}
    table_ids = {record["id"] for record in tables["records"]}
    output_by_slug = {meta["slug"]: meta["output"] for meta in SOURCE_FILES}
    page_cache = {
        page.name: page.read_text(encoding="utf-8")
        for page in formal_pages()
        if page.exists()
    }
    issues = []
    traceability = []
    mapping_placements = 0

    for record in source["slides"]:
        slide_number = int(record["slide"])
        targets = (
            ["excavator-market-overview.html"]
            if record.get("overview")
            else [output_by_slug[slug] for slug in record.get("slugs", [])]
        )
        if not targets:
            issues.append({"slide": slide_number, "issue": "unmapped_slide"})
        mapping_placements += len(targets)

        missing_tables = [
            table_id for table_id in record.get("table_ids", []) if table_id not in table_ids
        ]
        for table_id in missing_tables:
            issues.append(
                {
                    "slide": slide_number,
                    "table": table_id,
                    "issue": "missing_table_record",
                }
            )

        missing_visuals = []
        for visual in record.get("visuals", []):
            path = ROOT / visual["file"]
            if not path.exists():
                missing_visuals.append(visual["file"])
                issues.append(
                    {
                        "slide": slide_number,
                        "visual": visual["file"],
                        "issue": "missing_visual_asset",
                    }
                )

        expected_status = detect_temporal_status(
            slide_number,
            record.get("source_title_zh") or record.get("title", {}).get("zh", ""),
            [item.get("zh", "") for item in record.get("body", [])],
            [item.get("zh", "") for item in record.get("notes", [])],
            record.get("visuals", []),
        )
        actual_status = record.get("temporal_status")
        if (expected_status or {}).get("code") != (actual_status or {}).get("code"):
            issues.append(
                {
                    "slide": slide_number,
                    "issue": "temporal_status_mismatch",
                    "expected": (expected_status or {}).get("code"),
                    "actual": (actual_status or {}).get("code"),
                }
            )

        for output in targets:
            html = page_cache.get(output, "")
            article_pattern = (
                rf'<article class="sourceSlide[^"]*" '
                rf'data-source-slide="{slide_number}">'
            )
            if not re.search(article_pattern, html):
                issues.append(
                    {
                        "slide": slide_number,
                        "page": output,
                        "issue": "slide_not_rendered",
                    }
                )
            if actual_status and f"sourceTemporalStatus-{actual_status['code']}" not in html:
                issues.append(
                    {
                        "slide": slide_number,
                        "page": output,
                        "issue": "temporal_status_not_rendered",
                    }
                )

        traceability.append(
            {
                "slide": slide_number,
                "id": record["id"],
                "reader_title": record.get("title", {}).get("zh", ""),
                "source_title": record.get("source_title_zh", ""),
                "section": record.get("section"),
                "targets": targets,
                "table_ids": record.get("table_ids", []),
                "visuals": [visual.get("file") for visual in record.get("visuals", [])],
                "temporal_status": (actual_status or {}).get("code"),
            }
        )

    pages = formal_pages()
    for page in pages:
        if not page.exists():
            issues.append({"page": page.name, "issue": "formal_page_missing"})
            continue
        issues.extend(local_reference_issues(page))

    scored_products, score_issues = model_issues()
    issues.extend(score_issues)

    unique_visuals = {
        visual["file"]
        for record in source["slides"]
        for visual in record.get("visuals", [])
    }
    temporal_counts = {}
    for record in source["slides"]:
        code = (record.get("temporal_status") or {}).get("code")
        if code:
            temporal_counts[code] = temporal_counts.get(code, 0) + 1

    report = {
        "meta": {
            "classification": "XCMG ARC INTERNAL",
            "source_file": source["meta"]["source_file"],
            "source_sha256": sha256(SOURCE_CONTENT),
            "table_sha256": sha256(TABLE_CONTENT),
            "formal_page_count": len(pages),
            "tonnage_page_count": len(SOURCE_FILES),
        },
        "metrics": {
            "included_slides": len(source["slides"]),
            "slide_mapping_placements": mapping_placements,
            "unique_tables": len(table_ids),
            "unique_visuals": len(unique_visuals),
            "scored_products": scored_products,
            "temporal_status_counts": temporal_counts,
        },
        "checks": {
            "status": "pass" if not issues else "fail",
            "issue_count": len(issues),
            "issues": issues,
        },
        "traceability": traceability,
    }
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return report


def main():
    report = build_report()
    print(
        json.dumps(
            {
                "status": report["checks"]["status"],
                "issues": report["checks"]["issue_count"],
                **report["metrics"],
                "report": str(REPORT_PATH.relative_to(ROOT)),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if report["checks"]["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
