from pathlib import Path

from tools.build_crane_dashboards import PAGE_DEFINITIONS, build_all


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


def test_crane_homepage_entry_and_quick_selector_are_live():
    build_all()
    homepage = (ROOT / "arc.html").read_text(encoding="utf-8")
    assert '<option value="cranes">' in homepage
    assert 'href="crane-overview.html"' in homepage
    assert "crane-rt-60t.html" in homepage
    assert "crane-at-150t.html" in homepage
