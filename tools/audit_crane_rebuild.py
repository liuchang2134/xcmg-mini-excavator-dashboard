from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SLIDES_PATH = ROOT / "data" / "crane-ppt-insights" / "slides.json"
SEGMENTS_PATH = ROOT / "data" / "crane-ppt-insights" / "segment-map.json"
PPT_SOURCE_PATH = ROOT / "data" / "crane-ppt-insights" / "source.json"
WORKBOOK_PATH = ROOT / "data" / "generated" / "cranes" / "crane-benchmark.json"
OUTPUT_PATH = ROOT / "data" / "generated" / "cranes" / "crane-rebuild-audit.json"

CLASS_PAGES = {
    "RT-60t": "crane-rt-60t.html",
    "RT-75t": "crane-rt-75t.html",
    "RT-100t": "crane-rt-100t.html",
    "RT-130t": "crane-rt-130t.html",
    "RT-160t": "crane-rt-160t.html",
    "AT-150t": "crane-at-150t.html",
}


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _slide_payload(slides: list[dict[str, Any]]) -> dict[str, Any]:
    sections = Counter(item["section"] for item in slides)
    statuses = Counter(item["status"] for item in slides)
    return {
        "slides": len(slides),
        "text_blocks": sum(len(item.get("text_blocks") or []) for item in slides),
        "text_characters": sum(
            len(block.get("text") or "")
            for item in slides
            for block in item.get("text_blocks") or []
        ),
        "native_tables": sum(len(item.get("tables") or []) for item in slides),
        "native_table_cells": sum(
            sum(len(row) for row in table.get("rows") or [])
            for item in slides
            for table in item.get("tables") or []
        ),
        "native_charts": sum(len(item.get("charts") or []) for item in slides),
        "images": sum(len(item.get("images") or []) for item in slides),
        "sections": dict(sorted(sections.items())),
        "statuses": dict(sorted(statuses.items())),
    }


def _html_profile(path: Path) -> dict[str, Any]:
    source = path.read_text(encoding="utf-8")
    slide_refs = sorted(
        {int(value) for value in re.findall(r'data-source-slide=["\'](\d+)', source)}
    )
    section_ids = re.findall(r'<section[^>]+id=["\']([^"\']+)', source)
    return {
        "file": path.name,
        "bytes": len(source.encode("utf-8")),
        "sections": section_ids,
        "tables": source.count("<table"),
        "images": source.count("<img"),
        "source_slide_refs": slide_refs,
        "source_slide_ref_count": len(slide_refs),
    }


def _model_coverage(model: dict[str, Any]) -> dict[str, Any]:
    metrics = model.get("metrics") or []
    configurations = model.get("configurations") or []
    numeric_metrics = sum(item.get("numeric_value") is not None for item in metrics)
    recorded_configurations = sum(
        item.get("normalized_status") != "unrecorded" for item in configurations
    )
    return {
        "product": model["display_name"],
        "is_xcmg": model["is_xcmg"],
        "numeric_parameter_values": numeric_metrics,
        "parameter_value_slots": len(metrics),
        "parameter_coverage": round(numeric_metrics / len(metrics), 4) if metrics else 0,
        "recorded_configuration_values": recorded_configurations,
        "configuration_value_slots": len(configurations),
        "configuration_coverage": (
            round(recorded_configurations / len(configurations), 4)
            if configurations
            else 0
        ),
        "anomalies": model.get("anomalies") or [],
    }


def build_audit() -> dict[str, Any]:
    slides = _load(SLIDES_PATH)
    segments = _load(SEGMENTS_PATH)
    ppt_source = _load(PPT_SOURCE_PATH)
    workbook = _load(WORKBOOK_PATH)
    by_slide = {item["slide"]: item for item in slides}

    class_audits = []
    sheets = {item["label"].strip(): item for item in workbook["sheets"]}
    for class_id, page_name in CLASS_PAGES.items():
        slide_numbers = segments[class_id]["slides"]
        class_slides = [by_slide[number] for number in slide_numbers]
        page = _html_profile(ROOT / page_name)
        missing_refs = sorted(set(slide_numbers) - set(page["source_slide_refs"]))
        extra_refs = sorted(set(page["source_slide_refs"]) - set(slide_numbers))
        sheet = sheets[class_id]
        models = [_model_coverage(model) for model in sheet["models"]]
        class_audits.append(
            {
                "class_id": class_id,
                "page": page,
                "ppt": {
                    **_slide_payload(class_slides),
                    "slide_numbers": slide_numbers,
                    "missing_page_references": missing_refs,
                    "unexpected_page_references": extra_refs,
                },
                "excel": {
                    "source_sheet": sheet["source_sheet"],
                    "model_count": len(models),
                    "parameter_rows": len(sheet["parameter_names"]),
                    "configuration_rows": len(sheet["configuration_names"]),
                    "models": models,
                    "anomalies": sheet.get("anomalies") or [],
                },
            }
        )

    market_page = _html_profile(ROOT / "crane-market-overview.html")
    all_references = set(market_page["source_slide_refs"])
    for item in class_audits:
        all_references.update(item["page"]["source_slide_refs"])
    source_slides = set(by_slide)

    excavator_reference = _html_profile(ROOT / "excavator-4-5t.html")
    required_business_sections = [
        "summary",
        "market-insight",
        "job-applications",
        "engineering-insight",
        "product-positioning",
        "condition-overview",
        "position",
        "actions",
        "parameters",
        "configurations",
        "quality",
    ]
    class_section_gaps = {
        item["class_id"]: [
            section
            for section in required_business_sections
            if section not in item["page"]["sections"]
        ]
        for item in class_audits
    }

    findings = []
    incomplete_architecture = {
        class_id: gaps for class_id, gaps in class_section_gaps.items() if gaps
    }
    if incomplete_architecture:
        findings.append(
            {
                "severity": "high",
                "code": "BUSINESS_INFORMATION_ARCHITECTURE_INCOMPLETE",
                "finding": "One or more crane class pages are missing required business sections.",
                "impact": "The page cannot yet support the same market-to-engineering decision flow used by the excavator benchmark.",
                "details": incomplete_architecture,
            }
        )
    findings.extend([
        {
            "severity": "high",
            "code": "CONFIGURATION_COVERAGE_LIMITS_TOTAL_SCORE",
            "finding": "Configuration status is sparse in the governed workbook, especially where cells are blank or descriptive rather than explicitly standard/optional/absent.",
            "impact": "Configuration and overall rankings must remain withheld where evidence coverage is below the publication threshold.",
        },
        {
            "severity": "high",
            "code": "PLANS_REQUIRE_CURRENT_STATUS_CONFIRMATION",
            "finding": "The presentation includes future plans and target dates. These records are not current completion evidence.",
            "impact": "Roadmap items must be presented as source-date plans until a current owner confirms status.",
        },
        {
            "severity": "medium",
            "code": "RT160_AND_AT150_SOURCE_SPARSE",
            "finding": "RT-160t and AT-150t workbook parameter coverage is materially lower than the four established rough-terrain classes.",
            "impact": "These pages need evidence-first layouts and must not imitate a fully ranked product page.",
        },
    ])

    return {
        "source": {
            "ppt": ppt_source,
            "workbook": {
                "file_name": workbook["source_file"],
                "sha256": workbook["sha256"],
                "excluded_sheets": workbook["excluded_sheets"],
            },
        },
        "ppt_total": _slide_payload(slides),
        "pages": {
            "market_overview": market_page,
            "class_pages": class_audits,
            "referenced_source_slides": len(all_references),
            "unreferenced_source_slides": sorted(source_slides - all_references),
        },
        "excavator_reference": {
            "page": excavator_reference,
            "required_business_sections": required_business_sections,
            "class_section_gaps": class_section_gaps,
        },
        "findings": findings,
    }


def main() -> None:
    audit = build_audit()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(OUTPUT_PATH.relative_to(ROOT))
    print(
        json.dumps(
            {
                "ppt_slides": audit["ppt_total"]["slides"],
                "ppt_tables": audit["ppt_total"]["native_tables"],
                "ppt_charts": audit["ppt_total"]["native_charts"],
                "ppt_images": audit["ppt_total"]["images"],
                "unreferenced_source_slides": audit["pages"]["unreferenced_source_slides"],
                "findings": len(audit["findings"]),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
