from pathlib import Path
import json
import re

from PIL import Image

from tools.build_crane_dashboards import (
    CONFIG_ZH,
    METRIC_ZH,
    PAGE_DEFINITIONS,
    build_all,
)
from tools.crane_data import load_crane_workbook


ROOT = Path(__file__).resolve().parents[1]


def test_crane_builder_generates_overview_and_six_tonnage_pages():
    outputs = build_all()
    expected = {"crane-overview.html", "crane-market-overview.html"} | {
        page["output"] for page in PAGE_DEFINITIONS.values()
    }
    assert {path.name for path in outputs} == expected
    for output in expected:
        assert (ROOT / output).exists()


def test_crane_pages_preserve_unknowns_and_exclude_stale_excavator_scoring():
    build_all()
    rt60 = (ROOT / "crane-rt-60t.html").read_text(encoding="utf-8")
    assert "资料未记录" in rt60
    assert "Data not recorded" in rt60
    assert "XE19U" not in rt60
    assert "301.7 CR" not in rt60


def test_crane_pages_render_semantic_source_values_without_unit_garble():
    build_all()
    rt60 = (ROOT / "crane-rt-60t.html").read_text(encoding="utf-8")
    assert "none kg" not in rt60
    assert "none m" not in rt60
    assert "N Y/N" not in rt60
    assert 'data-source-value="none">无<' in rt60
    assert 'data-source-value="N">否<' in rt60


def test_incomplete_crane_sheets_are_not_forced_into_rankings():
    build_all()
    rt160 = (ROOT / "crane-rt-160t.html").read_text(encoding="utf-8")
    at150 = (ROOT / "crane-at-150t.html").read_text(encoding="utf-8")
    assert "参数有效覆盖率不足60%" in rt160
    assert "竞品表头与数据范围待核验" in at150
    assert "第 0" not in rt160 + at150
    assert "0.0 分" not in rt160 + at150


def test_crane_pages_are_bilingual_and_mobile_bounded():
    build_all()
    page = (ROOT / "crane-rt-100t.html").read_text(encoding="utf-8")
    css = (ROOT / "assets" / "crane-dashboard.css").read_text(encoding="utf-8")
    assert 'data-en="Road Transport / Compliance"' in page
    assert 'name="viewport"' in page
    assert "@media(max-width:720px)" in css
    assert "overflow-x:hidden" in css


def test_crane_pages_separate_publication_status_and_add_measurable_actions():
    build_all()
    page = (ROOT / "crane-rt-60t.html").read_text(encoding="utf-8")
    assert 'id="actions"' in page
    assert "XCMG 量化补强清单" in page
    assert "首要量化差距" in page
    assert "参数排名资格" in page
    assert "配置评价资格" in page
    assert "综合排名" in page
    assert "逐项把工况竞争位置" in page


def test_crane_pages_expose_all_normalized_parameters_and_configurations():
    build_all()
    workbook = load_crane_workbook()
    for sheet in workbook.sheets:
        page_name = PAGE_DEFINITIONS[sheet.label]["output"]
        page = (ROOT / page_name).read_text(encoding="utf-8")
        for name in sheet.parameter_names:
            assert METRIC_ZH.get(name, name) in page, (page_name, name)
        for name in sheet.configuration_names:
            assert CONFIG_ZH.get(name, name) in page, (page_name, name)


def test_crane_radar_defaults_to_all_products_and_supports_multi_select_controls():
    build_all()
    page = (ROOT / "crane-rt-60t.html").read_text(encoding="utf-8")
    script = (ROOT / "assets" / "dashboard.js").read_text(encoding="utf-8")
    assert page.count('class="radar-series selected"') == page.count('class="selected" data-product=')
    assert 'aria-pressed="true"' in page
    assert "btn.addEventListener('click'" in script


def test_crane_homepage_entry_and_quick_selector_are_live():
    build_all()
    homepage = (ROOT / "arc.html").read_text(encoding="utf-8")
    assert '<option value="cranes">' in homepage
    assert 'href="crane-overview.html"' not in homepage
    assert 'href="crane-market-overview.html"' in homepage
    assert 'data-crane-asset-panel' in homepage
    assert "crane-rt-60t.html" in homepage
    assert "crane-at-150t.html" in homepage


def test_crane_class_pages_include_mapped_ppt_analysis_without_changing_scores():
    build_all()
    rt60 = (ROOT / "crane-rt-60t.html").read_text(encoding="utf-8")
    rt100 = (ROOT / "crane-rt-100t.html").read_text(encoding="utf-8")
    rt130 = (ROOT / "crane-rt-130t.html").read_text(encoding="utf-8")
    rt160 = (ROOT / "crane-rt-160t.html").read_text(encoding="utf-8")
    at150 = (ROOT / "crane-at-150t.html").read_text(encoding="utf-8")
    assert 'data-source-slide="81"' in rt60
    assert 'data-source-slide="96"' in rt100
    assert 'data-source-slide="108"' in rt130
    assert 'data-source-slide="58"' in at150
    assert 'data-source-slide="147"' in rt160
    assert 'data-source-status="plan"' in rt160
    assert "XCMG 量化补强清单" in rt60
    assert 'assets/crane-insights.css' in rt60


def test_crane_market_report_is_not_a_navigation_hub_and_covers_global_slides():
    build_all()
    report = (ROOT / "crane-market-overview.html").read_text(encoding="utf-8")
    legacy = (ROOT / "crane-overview.html").read_text(encoding="utf-8")
    assert all(f'data-source-slide="{number}"' in report for number in range(1, 10))
    assert 'data-source-slide="130"' in report
    assert 'data-source-slide="163"' in report
    assert "craneAssetGrid" not in report
    assert 'location.replace("crane-market-overview.html"' in legacy
    assert "市场、区域、产品与服务洞察" in report


def test_every_crane_ppt_slide_is_rendered_in_the_report_or_a_class_page():
    build_all()
    pages = [
        (ROOT / "crane-market-overview.html").read_text(encoding="utf-8"),
        *[
            (ROOT / definition["output"]).read_text(encoding="utf-8")
            for definition in PAGE_DEFINITIONS.values()
        ],
    ]
    combined = "\n".join(pages)
    missing = [
        number
        for number in range(1, 164)
        if f'data-source-slide="{number}"' not in combined
    ]
    assert missing == []


def test_every_useful_crane_ppt_visual_and_native_table_is_rendered():
    build_all()
    slides = __import__("json").loads(
        (ROOT / "data" / "crane-ppt-insights" / "slides.json").read_text(encoding="utf-8")
    )
    pages = [
        (ROOT / "crane-market-overview.html").read_text(encoding="utf-8"),
        *[
            (ROOT / definition["output"]).read_text(encoding="utf-8")
            for definition in PAGE_DEFINITIONS.values()
        ],
    ]
    combined = "\n".join(pages)
    for slide in slides:
        if slide["slide"] != 1:
            for image in slide["images"]:
                assert image in combined, (slide["slide"], image)
        for index, table in enumerate(slide["tables"], 1):
            rows = table.get("rows") or []
            nonempty = [cell for row in rows for cell in row if str(cell).strip()]
            if len(rows) >= 2 and len(nonempty) >= 4:
                assert f'data-table-slide="{slide["slide"]}" data-table-index="{index}"' in combined
        for index, chart in enumerate(slide["charts"], 1):
            if chart.get("categories") and chart.get("series"):
                assert f'data-chart-id="slide-{slide["slide"]}-chart-{index}"' in combined


def test_crane_insight_titles_and_multi_image_galleries_are_reader_facing():
    build_all()
    pages = [
        (ROOT / "crane-market-overview.html").read_text(encoding="utf-8"),
        *[
            (ROOT / definition["output"]).read_text(encoding="utf-8")
            for definition in PAGE_DEFINITIONS.values()
        ],
    ]
    combined = "\n".join(pages)
    assert not re.search(r"<h3>\s*\d+(?:\.\d+)+", combined)
    assert "2.3 市场洞察分析" not in combined
    assert "北美起重机区域需求分布" in combined
    assert "2024年加拿大越野轮胎起重机销量分布" in combined
    assert 'class="craneInsightRecord has-media many-media" data-source-slide="7"' in combined
    assert 'class="insightImageButton"' in combined
    assert "insightLightbox" in (ROOT / "assets" / "crane-insights.js").read_text(encoding="utf-8")


def test_crane_source_tables_expand_without_nested_scrolling():
    css = (ROOT / "assets" / "crane-insights.css").read_text(encoding="utf-8")
    table_wrap = re.search(r"\.craneSourceTable\{([^}]*)\}", css)
    table_rule = re.search(r"\.craneSourceTable table\{([^}]*)\}", css)
    assert table_wrap
    assert table_rule
    assert "max-height" not in table_wrap.group(1)
    assert "overflow:auto" not in table_wrap.group(1).replace(" ", "")
    assert "overflow:visible" in table_wrap.group(1).replace(" ", "")
    assert "min-width:0" in table_rule.group(1).replace(" ", "")
    assert "table-layout:fixed" in table_rule.group(1).replace(" ", "")


def test_crane_ppt_images_use_high_resolution_powerpoint_exports():
    build_all()
    manifest = json.loads(
        (ROOT / "data" / "crane-ppt-insights" / "image-display.json").read_text(
            encoding="utf-8"
        )
    )
    slides = json.loads(
        (ROOT / "data" / "crane-ppt-insights" / "slides.json").read_text(
            encoding="utf-8"
        )
    )
    source_images = {
        image
        for slide in slides
        for image in slide.get("images", [])
    }
    assert set(manifest["images"]) == source_images
    assert manifest["image_count"] == len(source_images)

    for display_path in manifest["images"].values():
        with Image.open(ROOT / display_path) as image:
            assert max(image.size) >= 1500, (display_path, image.size)
            assert image.width * image.height >= 450_000, (display_path, image.size)

    rendered_sources = set()
    for page_path in ROOT.glob("crane-*.html"):
        page = page_path.read_text(encoding="utf-8")
        rendered_sources.update(
            re.findall(r'data-source-src="([^"]+)"', page)
        )
        if 'data-source-src="assets/crane-ppt-source/' in page:
            assert 'src="assets/crane-ppt-display/' in page

    assert rendered_sources
    assert rendered_sources <= set(manifest["images"])
