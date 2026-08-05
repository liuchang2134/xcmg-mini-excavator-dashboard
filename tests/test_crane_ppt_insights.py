import json
from pathlib import Path

from tools.crane_ppt_insights import (
    CLASS_SLIDES,
    DEFAULT_SOURCE,
    OUTPUT_DIR,
    build_crane_ppt_insights,
)


ROOT = Path(__file__).resolve().parents[1]


def load_json(name: str):
    return json.loads((OUTPUT_DIR / name).read_text(encoding="utf-8"))


def test_crane_source_presentation_is_available_locally():
    assert DEFAULT_SOURCE.exists()
    assert DEFAULT_SOURCE.stat().st_size > 100_000_000


def test_crane_slide_map_covers_all_163_slides():
    result = build_crane_ppt_insights()
    assert result["slide_count"] == 163
    slides = load_json("slides.json")
    assert len(slides) == 163
    assert {item["slide"] for item in slides} == set(range(1, 164))
    assert all(item["source_date"] == "2025-07-01" for item in slides)


def test_crane_segment_map_assigns_formal_class_ranges():
    build_crane_ppt_insights()
    mapping = load_json("segment-map.json")
    assert mapping["RT-60t"]["slides"] == list(range(81, 96))
    assert mapping["RT-75t"]["slides"] == list(range(81, 96))
    assert mapping["RT-100t"]["slides"] == list(range(96, 108))
    assert mapping["RT-130t"]["slides"] == list(range(108, 120))
    assert mapping["AT-150t"]["slides"] == list(range(58, 69))
    assert mapping["RT-160t"]["slides"] == [132, 147, 152]
    assert CLASS_SLIDES == {key: value["slides"] for key, value in mapping.items()}


def test_crane_plans_are_not_marked_current():
    build_crane_ppt_insights()
    slides = load_json("slides.json")
    planned = [item for item in slides if item["slide"] in range(143, 164)]
    assert planned
    assert all(item["status"] == "plan" for item in planned)


def test_slide_records_preserve_text_tables_images_and_evidence():
    build_crane_ppt_insights()
    slides = load_json("slides.json")
    assert any(item["tables"] for item in slides)
    assert any(item["images"] for item in slides)
    assert any(item["charts"] for item in slides)
    evidence = load_json("evidence.json")
    assert len(evidence) == 163
    assert evidence[0]["source_slide"] == 1
    assert evidence[-1]["source_slide"] == 163


def test_extracted_assets_are_not_whole_slide_screenshots():
    build_crane_ppt_insights()
    slides = load_json("slides.json")
    asset_paths = [ROOT / path for item in slides for path in item["images"]]
    assert asset_paths
    assert all(path.exists() for path in asset_paths)
    assert all("slide-screenshot" not in path.name for path in asset_paths)
