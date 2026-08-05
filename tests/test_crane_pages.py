from pathlib import Path

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
    expected = {"crane-overview.html"} | {
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
    assert 'href="crane-overview.html"' in homepage
    assert "crane-rt-60t.html" in homepage
    assert "crane-at-150t.html" in homepage
