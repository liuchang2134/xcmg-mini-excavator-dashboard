import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STYLE_FILES = (
    ROOT / "assets" / "dashboard.css",
    ROOT / "assets" / "crane-dashboard.css",
    ROOT / "assets" / "crane-insights.css",
    ROOT / "assets" / "excavator-market-overview-source.css",
    ROOT / "assets" / "site-credits.css",
)


def test_shared_styles_use_rem_type_scale_instead_of_pixel_font_sizes():
    for path in STYLE_FILES:
        css = path.read_text(encoding="utf-8")
        assert not re.search(r"font-size\s*:\s*\d+(?:\.\d+)?px", css), path


def test_dashboard_defines_and_enforces_readable_type_floor():
    css = (ROOT / "assets" / "dashboard.css").read_text(encoding="utf-8")
    for token in (
        "--font-min:.6875rem",
        "--font-xs:.75rem",
        "--font-sm:.8125rem",
        "--font-body:.875rem",
        "--font-base:1rem",
    ):
        assert token in css
    assert "main p{font-size:var(--font-body)!important}" in css
    assert "table :is(th,td){font-size:var(--font-xs)!important}" in css


def test_narrative_measure_is_constrained_without_narrowing_data_surfaces():
    css = (ROOT / "assets" / "dashboard.css").read_text(encoding="utf-8")
    assert "main p{max-inline-size:34em;text-wrap:pretty}" in css
    assert ":is(table,.tableScroll,.detailMatrix,.rawTable,.conditionHeatmap,.sourceVisualGrid) p{max-inline-size:none}" in css


def test_shared_font_stack_covers_cjk_system_fonts():
    expected = 'system-ui,-apple-system,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC","Source Han Sans SC",sans-serif'
    css = (ROOT / "assets" / "dashboard.css").read_text(encoding="utf-8")
    assert expected in css
    assert css.count(expected) >= 2


def test_390px_breakpoint_preserves_readable_text_and_tables():
    css = (ROOT / "assets" / "dashboard.css").read_text(encoding="utf-8")
    assert "@media(max-width:390px){body,main p{font-size:var(--font-body)}" in css
    assert "table,table :is(th,td){font-size:var(--font-xs)!important}" in css
