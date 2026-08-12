import json
from pathlib import Path

from tools.crane_ppt_insights import (
    CLASS_SECTION_SLIDES,
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
    assert mapping["RT-60t"]["slides"] == [81, *range(82, 87), *range(88, 95)]
    assert mapping["RT-75t"]["slides"] == [81, *range(82, 86), *range(87, 94), 95]
    assert mapping["RT-100t"]["slides"] == [81, *range(96, 108)]
    assert mapping["RT-130t"]["slides"] == [81, *range(108, 120)]
    assert mapping["AT-150t"]["slides"] == list(range(58, 69))
    assert mapping["RT-160t"]["slides"] == [81, 132, 147, 152]
    assert CLASS_SLIDES == {key: value["slides"] for key, value in mapping.items()}


def test_crane_class_sections_keep_tonnage_specific_product_pages_separate():
    assert 94 in CLASS_SECTION_SLIDES["RT-60t"]["product-positioning"]
    assert 95 not in CLASS_SLIDES["RT-60t"]
    assert 95 in CLASS_SECTION_SLIDES["RT-75t"]["product-positioning"]
    assert 94 not in CLASS_SLIDES["RT-75t"]
    assert all(81 in CLASS_SLIDES[class_id] for class_id in ("RT-60t", "RT-75t", "RT-100t", "RT-130t", "RT-160t"))


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


def test_crane_ppt_extraction_counts_are_stable():
    build_crane_ppt_insights()
    slides = load_json("slides.json")
    assert sum(len(item["tables"]) for item in slides) == 354
    assert sum(len(item["charts"]) for item in slides) == 26
    assert sum(len(item["images"]) for item in slides) >= 250


def test_scatter_and_bubble_charts_preserve_all_source_dimensions():
    build_crane_ppt_insights()
    slides = {item["slide"]: item for item in load_json("slides.json")}

    scatter = slides[26]["charts"][0]["series"]
    assert scatter[0]["x_values"] == [36.9]
    assert scatter[0]["y_values"] == [0.014]
    assert scatter[1]["x_values"] == [37.1]
    assert scatter[1]["y_values"] == [0.365]

    bubble = slides[154]["charts"][0]["series"][0]
    assert bubble["x_values"] == [6.2, 4.9, 4.8, 3.6]
    assert bubble["y_values"] == [8.3, 6.0, 6.0, 5.9]
    assert bubble["bubble_sizes"] == [19.3, 45.6, 52.6, 70.2]


def test_crane_class_pages_retain_compact_field_and_diagnostic_images():
    build_crane_ppt_insights()
    slides = {item["slide"]: item for item in load_json("slides.json")}
    assert sum(len(slides[number]["images"]) for number in range(81, 96)) >= 15
    assert sum(len(slides[number]["images"]) for number in range(96, 108)) >= 14
    assert sum(len(slides[number]["images"]) for number in range(108, 120)) >= 25


def test_extracted_assets_are_not_whole_slide_screenshots():
    build_crane_ppt_insights()
    slides = load_json("slides.json")
    asset_paths = [ROOT / path for item in slides for path in item["images"]]
    assert asset_paths
    assert all(path.exists() for path in asset_paths)
    assert all("slide-screenshot" not in path.name for path in asset_paths)
