import json
import math
import re
import unittest
from collections import Counter
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

from tools.build_excavator_dashboards import (
    CONDITIONS,
    MIN_SCORE_COVERAGE,
    OPTION_CATEGORY_WEIGHTS,
    OVERALL_WEIGHTS,
    PARAM_CATEGORY_WEIGHTS,
    ROOT,
    SOURCE_FILES,
    build_model,
    load_workbook,
    option_score,
    parse_metric_value,
)
from tools.render_ppt_charts import nice_ceiling


class StructureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.h1_count = 0
        self.table_count = 0
        self.caption_count = 0
        self.references = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "table":
            self.table_count += 1
        if tag == "caption":
            self.caption_count += 1
        if tag in {"a", "img", "script", "link"}:
            ref = values.get("href") or values.get("src")
            if ref:
                self.references.append(ref)


class TextContentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


class DashboardModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.models = [build_model(load_workbook(meta["source"]), meta) for meta in SOURCE_FILES]

    def test_weight_groups_sum_to_one(self):
        self.assertTrue(math.isclose(sum(c["weight"] for c in CONDITIONS), 1.0, abs_tol=1e-9))
        self.assertTrue(math.isclose(sum(PARAM_CATEGORY_WEIGHTS.values()), 1.0, abs_tol=1e-9))
        self.assertTrue(math.isclose(sum(OPTION_CATEGORY_WEIGHTS.values()), 1.0, abs_tol=1e-9))
        for condition in CONDITIONS:
            with self.subTest(condition=condition["id"]):
                self.assertTrue(
                    math.isclose(sum(item[2] for item in condition["items"]), 1.0, abs_tol=1e-9),
                    f'{condition["id"]} item weights must total 100%',
                )

    def test_overall_score_uses_parameter_and_option_only(self):
        self.assertEqual(OVERALL_WEIGHTS, {"parameter": 0.65, "option": 0.35})
        for model in self.models:
            for product in model["products"]:
                actual = model["overall"].get(product)
                param = model["paramScore"].get(product)
                option = model["optionScore"].get(product)
                if param is None or option is None:
                    self.assertIsNone(actual)
                else:
                    expected = param * 0.65 + option * 0.35
                    self.assertAlmostEqual(actual, expected, places=8)

    def test_blank_option_is_unknown_not_no_configuration(self):
        self.assertIsNone(option_score(""))
        self.assertEqual(option_score("/"), 0)
        self.assertEqual(option_score("无配置"), 0)
        self.assertEqual(option_score("选配"), 60)
        self.assertEqual(option_score("标配"), 100)

    def test_metric_specific_parsers(self):
        self.assertAlmostEqual(parse_metric_value("2x38.4+22.8", "flow_sum"), 99.6)
        self.assertAlmostEqual(parse_metric_value("2×37", "flow_sum"), 74.0)
        self.assertAlmostEqual(parse_metric_value("2.2/3.6", "speed_low"), 2.2)
        self.assertAlmostEqual(parse_metric_value("2.2/3.6", "speed_high"), 3.6)
        self.assertIsNone(parse_metric_value("/5.7", "speed_low"))
        self.assertAlmostEqual(parse_metric_value("/5.7", "speed_high"), 5.7)
        self.assertAlmostEqual(parse_metric_value("3.5/", "speed_low"), 3.5)
        self.assertIsNone(parse_metric_value("3.5/", "speed_high"))
        self.assertAlmostEqual(parse_metric_value("3480-4190", "low"), 3835.0)

    def test_low_coverage_products_do_not_receive_formal_scores(self):
        for model in self.models:
            for condition in CONDITIONS:
                coverage = model["conditionCoverage"][condition["id"]]
                scores = model["conditionScores"][condition["id"]]
                for product in model["products"]:
                    if coverage[product] + 1e-9 < MIN_SCORE_COVERAGE:
                        self.assertIsNone(scores[product])

    def test_all_tonnage_pages_remain_published(self):
        self.assertEqual(len(SOURCE_FILES), 15)
        expected_outputs = {
            "excavator-8-10t.html",
            "excavator-12-14t.html",
            "excavator-14-16t-short-tail.html",
            "excavator-21-24t.html",
            "excavator-24-28t.html",
            "excavator-24-28t-short-tail.html",
            "excavator-28-33t.html",
            "excavator-33-40t.html",
            "excavator-40-60t.html",
        }
        self.assertTrue(expected_outputs.issubset({meta["output"] for meta in SOURCE_FILES}))
        for meta in SOURCE_FILES:
            self.assertTrue((ROOT / meta["output"]).exists(), meta["output"])
            self.assertTrue(meta["source"].exists(), meta["source"])
        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        self.assertEqual(arc_html.count('class="projectRow"'), len(SOURCE_FILES))
        self.assertIn("十五个吨级统一覆盖狭窄空间、沟槽、土方装车、破碎、坡地和租赁六类典型工况", arc_html)

    def test_new_tonnage_sources_and_models_are_bound_correctly(self):
        by_output = {model["meta"]["output"]: model for model in self.models}
        self.assertEqual(by_output["excavator-12-14t.html"]["meta"]["xcmg"], "XCMG XE135U")
        self.assertEqual(
            by_output["excavator-14-16t-short-tail.html"]["meta"]["xcmg"],
            "XCMG XE155UCR",
        )
        self.assertEqual(
            by_output["excavator-21-24t.html"]["meta"]["xcmg"],
            "XCMG XE225U",
        )
        expected_new_models = {
            "excavator-24-28t.html": "XCMG XE250U",
            "excavator-24-28t-short-tail.html": "XCMG XE235UCR",
            "excavator-28-33t.html": "XCMG XE300U",
            "excavator-33-40t.html": "XCMG XE360U",
            "excavator-40-60t.html": "XCMG XE490U",
        }
        for output, xcmg_model in expected_new_models.items():
            with self.subTest(output=output):
                self.assertEqual(by_output[output]["meta"]["xcmg"], xcmg_model)
        replacement = by_output["excavator-8-10t.html"]
        weight_row = next(row for row in replacement["rawParamRows"] if row["item"] == "操作重量")
        self.assertEqual(weight_row["values"]["XCMG XE80U"], "9250/9500")
        revised_33_40 = by_output["excavator-33-40t.html"]
        delayed_lights = next(
            row for row in revised_33_40["rawOptionRows"] if row["item"] == "工作灯延迟关闭"
        )
        long_stick = next(
            row for row in revised_33_40["rawOptionRows"] if row["item"] == "长斗杆 m"
        )
        self.assertEqual(delayed_lights["values"]["XCMG XE360U"], "/")
        self.assertEqual(long_stick["values"]["XCMG XE360U"], "选配4")

        large_excavator = by_output["excavator-40-60t.html"]
        self.assertEqual(large_excavator["meta"]["label"], "40-60 吨级")
        operating_weight = next(
            row for row in large_excavator["rawParamRows"] if row["item"] == "操作重量"
        )
        reverse_fan = next(
            row for row in large_excavator["rawOptionRows"] if row["item"] == "风扇反向"
        )
        self.assertEqual(operating_weight["values"]["XCMG XE490U"], "51090")
        self.assertEqual(reverse_fan["values"]["XCMG XE490U"], "/")

        short_tail = by_output["excavator-24-28t-short-tail.html"]
        self.assertNotIn("\n", "".join(short_tail["products"]))

    def test_xe35u_is_presented_as_3_to_4_tonnes_without_breaking_legacy_urls(self):
        meta = next(item for item in SOURCE_FILES if item["xcmg"] == "XCMG XE35U")
        self.assertEqual(meta["label"], "3-4 吨级")
        self.assertEqual(meta["title"], "XCMG XE35U 3-4 吨级挖掘机竞品对标看板")
        self.assertEqual(meta["output"], "index.html")
        self.assertEqual(meta["source"].name, "XCMG_3.5t_mini_excavator_competitor_source.xlsx")

        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        self.assertIn('<option value="3.5">3-4 吨级</option>', arc_html)
        self.assertIn("XE35U 3-4 吨级小型挖掘机", arc_html)

        downloads_html = (ROOT / "data-downloads.html").read_text(encoding="utf-8")
        self.assertIn('<div class="dataCell tonnage">3-4 吨级</div>', downloads_html)

    def test_generated_pages_have_single_h1_and_table_captions(self):
        for meta in SOURCE_FILES:
            path = ROOT / meta["output"]
            parser = StructureParser()
            parser.feed(path.read_text(encoding="utf-8"))
            with self.subTest(page=meta["output"]):
                self.assertEqual(parser.h1_count, 1)
                self.assertGreater(parser.table_count, 0)
                self.assertEqual(parser.caption_count, parser.table_count)
                duplicates = [item for item, count in Counter(parser.ids).items() if count > 1]
                self.assertEqual(duplicates, [])

    def test_generated_pages_have_mobile_progressive_disclosure(self):
        dashboard_js = (ROOT / "assets" / "dashboard.js").read_text(encoding="utf-8")
        self.assertIn("setupMobileDisclosures();", dashboard_js)
        for meta in SOURCE_FILES:
            html = (ROOT / meta["output"]).read_text(encoding="utf-8")
            with self.subTest(page=meta["output"]):
                self.assertEqual(html.count('class="mobileDisclosure factorDisclosure"'), 6)
                self.assertEqual(html.count('class="mobileDisclosure matrixDisclosure"'), 6)
                self.assertEqual(html.count('class="mobileDisclosure simulatorDisclosure"'), 6)
                self.assertIn('class="mobileDisclosure rawDisclosure"', html)
                self.assertIn('src="assets/dashboard.js?v=', html)
                self.assertNotIn('class="summaryGrid" style="margin-top:12px"', html)

    def test_chart_scale_and_sidebar_are_responsive(self):
        dashboard_css = (ROOT / "assets" / "dashboard.css").read_text(encoding="utf-8")
        dashboard_js = (ROOT / "assets" / "dashboard.js").read_text(encoding="utf-8")

        self.assertEqual(nice_ceiling(2138 * 1.08), 2500)
        self.assertEqual(nice_ceiling(718 * 1.08), 800)
        self.assertIn(
            "grid-template-columns:clamp(216px,16vw,252px) minmax(0,1fr)",
            dashboard_css,
        )
        self.assertIn(".layout.sidebarCollapsed", dashboard_css)
        self.assertIn("width:min(100%,72rem);min-width:0", dashboard_css)
        self.assertIn("@media(max-width:900px)", dashboard_css)
        self.assertIn("@media(min-width:901px)", dashboard_css)
        self.assertIn("document.createElement('button')", dashboard_js)
        self.assertIn("window.matchMedia('(min-width:901px)')", dashboard_js)
        self.assertIn("setupSidebarCollapse();", dashboard_js)

        shared_layout_pages = [
            *[ROOT / meta["output"] for meta in SOURCE_FILES],
            ROOT / "excavator-market-overview.html",
            ROOT / "ppt-integration-demo" / "index.html",
            ROOT / "ppt-integration-demo" / "excavator-overview.html",
        ]
        for page in shared_layout_pages:
            with self.subTest(page=page.name):
                html = page.read_text(encoding="utf-8")
                self.assertIn("assets/dashboard.css?v=20260724k", html)
                self.assertIn('class="sidebarToggle"', html)

        market_html = (ROOT / "excavator-market-overview.html").read_text(encoding="utf-8")
        self.assertIn('data-en="150,000"', market_html)
        self.assertNotIn('data-en="200,000"', market_html)

        for meta in SOURCE_FILES:
            html = (ROOT / meta["output"]).read_text(encoding="utf-8")
            sales_chart = re.search(
                r'<figure class="[^"]*sourceDataChart[^"]*"[^>]*>'
                r'.*?<figcaption[^>]*>.*?产品近年销量.*?</figcaption>'
                r'.*?</figure>',
                html,
                flags=re.DOTALL,
            )
            if sales_chart is None:
                continue
            chart_html = sales_chart.group(0)
            grid = re.search(
                r'<g class="sourceChartGrid">(.*?)</g>',
                chart_html,
                flags=re.DOTALL,
            )
            self.assertIsNotNone(grid, meta["output"])
            axis_values = [
                int(value.replace(",", ""))
                for value in re.findall(r"<text[^>]*>\s*([\d,]+)\s*</text>", grid.group(1))
            ]
            totals = [
                int(value.replace(",", ""))
                for value in re.findall(
                    r'<text[^>]*class="sourceChartTotal"[^>]*>\s*([\d,]+)\s*</text>',
                    chart_html,
                )
            ]
            self.assertTrue(axis_values, meta["output"])
            self.assertTrue(totals, meta["output"])
            y_max = max(axis_values)
            max_total = max(totals)
            with self.subTest(page=meta["output"]):
                self.assertGreaterEqual(y_max, max_total)
                self.assertLessEqual(y_max, max_total * 1.40)

    def test_every_tonnage_page_uses_its_own_source_chapter(self):
        source_path = ROOT / "data" / "ppt-insights" / "ppt-source-content.json"
        payload = json.loads(source_path.read_text(encoding="utf-8"))
        mapped_slugs = set(payload["by_slug"])
        expected_slugs = {meta["slug"] for meta in SOURCE_FILES} - {"excavator-7-8t"}
        self.assertEqual(mapped_slugs, expected_slugs)

        for meta in SOURCE_FILES:
            html = (ROOT / meta["output"]).read_text(encoding="utf-8")
            with self.subTest(page=meta["output"]):
                if meta["slug"] == "excavator-7-8t":
                    self.assertNotIn('class="sourceContentSection"', html)
                    self.assertNotIn('data-source-slide="', html)
                    self.assertNotIn("8-10 吨是小挖向中挖过渡", html)
                    continue
                self.assertIn('id="market-insight"', html)
                self.assertIn('id="job-applications"', html)
                self.assertIn('id="engineering-insight"', html)
                self.assertIn('id="product-positioning"', html)
                self.assertIn('class="navGroup"', html)
                self.assertEqual(
                    html.count('data-source-slide="'),
                    len(payload["by_slug"][meta["slug"]]),
                )

    def test_all_ppt_business_tables_are_mapped_without_personnel_or_navigation_tables(self):
        table_path = ROOT / "data" / "ppt-insights" / "ppt-business-tables.json"
        self.assertTrue(table_path.exists())
        payload = json.loads(table_path.read_text(encoding="utf-8"))
        summary = payload["summary"]
        self.assertEqual(summary["included_table_count"], 220)
        self.assertEqual(summary["overview_table_count"], 19)
        self.assertEqual(summary["excluded"]["navigation_table"], 208)
        self.assertEqual(summary["excluded"]["personnel_table"], 1)
        self.assertEqual(
            summary["included_table_count"],
            summary["overview_table_count"] + sum(
                1 for record in payload["records"] if not record["overview"]
            ),
        )
        self.assertEqual(
            set(payload["by_slug"]),
            {meta["slug"] for meta in SOURCE_FILES if meta["slug"] != "excavator-7-8t"},
        )

        expected_counts = {slug: len(records) for slug, records in payload["by_slug"].items()}
        for meta in SOURCE_FILES:
            html = (ROOT / meta["output"]).read_text(encoding="utf-8")
            with self.subTest(page=meta["output"]):
                self.assertEqual(
                    html.count('class="sourceTableBlock"'),
                    expected_counts.get(meta["slug"], 0),
                )

    def test_ppt_business_tables_are_responsive_and_language_aware(self):
        dashboard_css = (ROOT / "assets" / "dashboard.css").read_text(encoding="utf-8")
        self.assertIn(".sourceTableScroll", dashboard_css)
        self.assertIn("overflow-x:auto", dashboard_css)
        self.assertIn("position:sticky", dashboard_css)
        self.assertIn("white-space:pre-line", dashboard_css)

    def test_generated_pages_use_an_inclusive_summary_label(self):
        builder_source = (ROOT / "tools" / "build_excavator_dashboards.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("对标概览", builder_source)
        self.assertNotIn("管理层摘要", builder_source)
        for meta in SOURCE_FILES:
            html = (ROOT / meta["output"]).read_text(encoding="utf-8")
            with self.subTest(page=meta["output"]):
                self.assertIn('<a href="#summary">对标概览</a>', html)
                self.assertIn("<h2>对标概览</h2>", html)
                self.assertNotIn("管理层摘要", html)

    def test_subpage_logos_link_back_to_the_platform_homepage(self):
        expected = (
            '<a class="navBrand" href="arc.html" '
            'aria-label="返回全产品线竞品对标平台主页">'
        )
        builder_source = (ROOT / "tools" / "build_excavator_dashboards.py").read_text(
            encoding="utf-8"
        )
        self.assertIn(expected, builder_source)
        for meta in SOURCE_FILES:
            html = (ROOT / meta["output"]).read_text(encoding="utf-8")
            with self.subTest(page=meta["output"]):
                self.assertEqual(html.count(expected), 1)

    def test_all_radars_start_with_every_product_selected(self):
        dashboard_js = (ROOT / "assets" / "dashboard.js").read_text(encoding="utf-8")
        builder_source = (ROOT / "tools" / "build_excavator_dashboards.py").read_text(
            encoding="utf-8"
        )
        for source in (dashboard_js, builder_source):
            self.assertIn(
                "const selected=new Set(controls.map(btn=>btn.dataset.product));",
                source,
            )
            self.assertIn("const allSelected=selected.size===controls.length;", source)
            self.assertIn("box.classList.toggle('compare',!allSelected);", source)
            self.assertIn("current.textContent='当前：未选择品牌';", source)
            self.assertNotIn("controls.filter(btn=>btn.dataset.default", source)

    def test_leadership_copy_avoids_overclaiming(self):
        banned_phrases = {
            "置信度",
            "用户提供 Excel",
            "不用纯主观判断",
            "工程目标",
            "竞品高水平目标",
            "平台和尺寸优化",
            "完整竞品数据",
            "完整对标数据",
        }
        pages = [ROOT / "arc.html", ROOT / "data-downloads.html"] + [
            ROOT / meta["output"] for meta in SOURCE_FILES
        ]
        for page in pages:
            html = page.read_text(encoding="utf-8")
            with self.subTest(page=page.name):
                for phrase in banned_phrases:
                    self.assertNotIn(phrase, html)

    def test_brand_and_project_names_are_not_mixed(self):
        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        self.assertIn("全产品线竞品对标平台｜XCMG ARC", arc_html)
        self.assertIn("由 XCMG ARC 独立开发", arc_html)
        self.assertNotIn("ARC 产品对标平台", arc_html)
        self.assertNotIn("ARC 不是参数表汇总", arc_html)
        for meta in SOURCE_FILES:
            html = (ROOT / meta["output"]).read_text(encoding="utf-8")
            with self.subTest(page=meta["output"]):
                self.assertIn("返回对标平台主页", html)
                self.assertNotIn("返回 ARC 主页", html)
                self.assertNotIn("XCMG ARC 独立开发", html)

    def test_arc_homepage_has_three_level_quick_selector(self):
        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        for control_id in ("quick-line", "quick-tonnage", "quick-model", "quick-open"):
            self.assertIn(f'id="{control_id}"', arc_html)
        self.assertIn('id="quick-selection-summary"', arc_html)

    def test_arc_homepage_has_three_status_metrics(self):
        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        self.assertEqual(arc_html.count('class="platformMetric"'), 3)
        self.assertNotIn('data-kpi-target=', arc_html)
        self.assertNotIn('<div class="heroActions">', arc_html)
        self.assertNotIn('class="heroModel"', arc_html)

    def test_arc_homepage_uses_the_approved_five_section_structure(self):
        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        self.assertIn('<header class="topbar">', arc_html)
        self.assertIn('class="hero"', arc_html)
        self.assertIn('id="products"', arc_html)
        self.assertIn('id="live"', arc_html)
        self.assertIn('id="method"', arc_html)
        self.assertIn("平台应用价值", arc_html)
        self.assertNotIn("管理层决策价值", arc_html)
        self.assertNotIn("项目价值", arc_html)

    def test_raw_data_downloads_are_centralized_on_a_secondary_page(self):
        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        download_path = ROOT / "data-downloads.html"
        self.assertTrue(download_path.exists())
        download_html = download_path.read_text(encoding="utf-8")
        self.assertEqual(arc_html.count('href="data-downloads.html"'), 1)
        self.assertNotIn('id="sources"', arc_html)
        self.assertNotIn("data/source-excel/", arc_html)
        self.assertNotIn("<b>Excel</b><span>原始数据</span>", arc_html)
        self.assertEqual(download_html.count('data-source-file="'), len(SOURCE_FILES))
        for meta in SOURCE_FILES:
            with self.subTest(page=meta["output"]):
                self.assertIn(f'href="{meta["output"]}"', download_html)
                self.assertIn(
                    f'href="data/source-excel/{meta["download"]}"',
                    download_html,
                )

    def test_arc_product_lines_have_one_direct_action_or_pending_state(self):
        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        self.assertEqual(arc_html.count('data-product-line="'), 7)
        self.assertNotIn('id="product-line-detail"', arc_html)
        self.assertNotIn("renderProductLineDetail", arc_html)
        self.assertEqual(arc_html.count('class="lineCard is-live"'), 1)
        self.assertEqual(arc_html.count('class="lineCard is-disabled"'), 6)
        self.assertEqual(arc_html.count('aria-disabled="true"'), 6)

    def test_arc_excavator_projects_are_filterable_and_clickable(self):
        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        self.assertIn('id="excavator-tonnage-filter"', arc_html)
        self.assertIn('id="excavator-model-search"', arc_html)
        self.assertIn('id="project-filter-empty"', arc_html)
        self.assertEqual(arc_html.count('<a class="projectRow"'), len(SOURCE_FILES))
        self.assertNotIn('class="projectActions"', arc_html)
        self.assertNotIn("典型工况</span>", arc_html)
        self.assertIn("filterProjectRows", arc_html)

    def test_every_public_page_has_a_persistent_bilingual_switch(self):
        i18n_path = ROOT / "assets" / "i18n.js"
        self.assertTrue(i18n_path.exists())
        i18n_js = i18n_path.read_text(encoding="utf-8")
        for term in (
            "Boom Swing",
            "Stick Digging Force",
            "Bucket Digging Force",
            "Auxiliary Circuit 1 Flow",
            "Operating Pressure - Travel",
            "Ground Pressure",
            "Operating Weight",
            "Overall Shipping Width",
        ):
            self.assertIn(term, i18n_js)
        self.assertIn("MutationObserver", i18n_js)
        self.assertIn("localStorage", i18n_js)

        pages = [ROOT / "arc.html", ROOT / "data-downloads.html"] + [
            ROOT / meta["output"] for meta in SOURCE_FILES
        ]
        for page in pages:
            html = page.read_text(encoding="utf-8")
            with self.subTest(page=page.name):
                self.assertIn('class="languageToggle"', html)
                self.assertIn('src="assets/i18n.js?v=', html)

    def test_arc_model_search_supports_typo_tolerant_matching(self):
        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        self.assertIn("function normalizeSearchValue", arc_html)
        self.assertIn("function levenshteinDistance", arc_html)
        self.assertIn("function fuzzyMatchesProject", arc_html)
        self.assertIn("fuzzyMatchesProject(row, query)", arc_html)
        self.assertNotIn(".toLowerCase().includes(query)", arc_html)

    def test_arc_navigation_and_mobile_drawer_have_persistent_state(self):
        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        self.assertIn('class="navBackdrop"', arc_html)
        self.assertIn("function updateActiveNav()", arc_html)
        self.assertIn("const marker = window.scrollY + (topbar?.offsetHeight ?? 0) + 32;", arc_html)
        self.assertIn("window.addEventListener('scroll', scheduleActiveNav, {passive: true});", arc_html)
        self.assertIn("const atPageBottom = window.innerHeight + window.scrollY", arc_html)
        self.assertNotIn("IntersectionObserver", arc_html)
        self.assertIn("aria-current", arc_html)
        self.assertIn("Escape", arc_html)
        self.assertIn("overflow-x:hidden", arc_html)

    def test_arc_top_links_scroll_to_the_absolute_page_top(self):
        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        self.assertIn("document.querySelectorAll('a[href=\"#top\"]')", arc_html)
        self.assertIn("event.preventDefault();", arc_html)
        self.assertIn("window.scrollTo(0, 0);", arc_html)
        self.assertIn("location.pathname + location.search", arc_html)

    def test_arc_filters_round_trip_through_url(self):
        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        self.assertIn("URLSearchParams", arc_html)
        self.assertIn("history.replaceState", arc_html)
        for key in ("line", "tonnage", "model"):
            self.assertIn(f"params.set('{key}'", arc_html)

    def test_arc_tonnage_change_clears_stale_model_query(self):
        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        self.assertIn("modelSearch.value = '';", arc_html)

    def test_arc_exact_model_search_updates_shared_product_state(self):
        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        self.assertIn("visibleRows.length === 1", arc_html)
        self.assertIn("visibleRows[0].dataset.tonnage", arc_html)

    def test_arc_mobile_drawer_does_not_expand_page_width(self):
        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        self.assertIn("clip-path:inset(0 0 0 100%)", arc_html)
        self.assertNotIn("transform:translateX(105%)", arc_html)

    def test_arc_mobile_drawer_stays_above_its_backdrop(self):
        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        self.assertIn("z-index:40;", arc_html)
        self.assertIn("height:calc(100dvh - 60px)", arc_html)
        self.assertIn("height:calc(100dvh - 56px)", arc_html)

    def test_ppt_demo_fragment_links_stay_inside_demo_pages(self):
        navigation = (ROOT / "ppt-integration-demo" / "assets" / "demo-navigation.js").read_text(
            encoding="utf-8"
        )
        self.assertIn("a[href^=\"#\"]", navigation)
        self.assertIn("event.preventDefault();", navigation)
        self.assertIn("new URL(window.location.href)", navigation)
        self.assertIn("window.history.replaceState", navigation)
        for filename in ("index.html", "excavator-overview.html"):
            html = (ROOT / "ppt-integration-demo" / filename).read_text(encoding="utf-8")
            with self.subTest(page=filename):
                self.assertIn("ppt-integration-demo/assets/demo-navigation.js", html)

    def test_condition_summary_is_concise_and_quantified(self):
        for meta in SOURCE_FILES:
            html = (ROOT / meta["output"]).read_text(encoding="utf-8")
            with self.subTest(page=meta["output"]):
                for condition in CONDITIONS:
                    self.assertEqual(html.count(condition["feature"]), 1)
                    self.assertEqual(html.count(condition["benefit"]), 1)
                self.assertLessEqual(html.count("覆盖率低于 60%"), 2)
                self.assertIn("配置项累计贡献", html)
                self.assertNotIn("XCMG - 分", html)

    def test_low_coverage_condition_has_no_zero_based_simulation(self):
        html = (ROOT / "excavator-14-16t-short-tail.html").read_text(encoding="utf-8")
        self.assertIn("暂不进入正式排名", html)
        self.assertIn("暂不生成模拟排名", html)
        self.assertNotIn("XCMG - 分，第 -", html)

    def test_parameter_units_are_normalized(self):
        for model in self.models:
            units = {row["unit"] for row in model["rawParamRows"]}
            self.assertNotIn("Mpa", units)
            self.assertIn("MPa", units)

    def test_local_page_references_exist(self):
        pages = [
            ROOT / "arc.html",
            ROOT / "data-downloads.html",
            ROOT / "excavator-market-overview.html",
        ] + [
            ROOT / meta["output"] for meta in SOURCE_FILES
        ]
        for page in pages:
            parser = StructureParser()
            parser.feed(page.read_text(encoding="utf-8"))
            for ref in parser.references:
                parsed = urlparse(ref)
                if parsed.scheme in {"http", "https", "mailto", "tel", "data"} or ref.startswith("#"):
                    continue
                target_text = unquote(parsed.path)
                target = (page.parent / target_text).resolve()
                with self.subTest(page=page.name, reference=ref):
                    self.assertTrue(target.exists(), f"Missing local reference: {ref}")

    def test_excavator_market_overview_is_separate_traceable_and_internal(self):
        page = ROOT / "excavator-market-overview.html"
        data_file = ROOT / "data" / "ppt-insights" / "excavator-market-overview.json"
        source_file = ROOT / "data" / "ppt-insights" / "ppt-source-content.json"
        self.assertTrue(page.exists())
        self.assertTrue(data_file.exists())
        self.assertTrue(source_file.exists())

        html = page.read_text(encoding="utf-8")
        data = json.loads(data_file.read_text(encoding="utf-8"))
        source = json.loads(source_file.read_text(encoding="utf-8"))
        parser = StructureParser()
        parser.feed(html)

        required_sections = {
            "environment",
            "industry",
            "competition",
            "class-structure",
            "portfolio",
            "roadmap",
            "sales-plan",
            "intelligence",
        }
        self.assertTrue(required_sections.issubset(set(parser.ids)))
        self.assertIn("XCMG ARC INTERNAL", html)
        self.assertNotIn("ppt-integration-demo", html)
        self.assertNotIn("fetch(", html)
        self.assertNotIn("assets/excavator-market-overview-expanded.js", html)
        self.assertIn("assets/excavator-market-overview-source.css", html)
        self.assertEqual(html.count('data-source-slide="'), len(source["overview"]))
        self.assertEqual(html.count('class="sourceTableBlock"'), 19)
        self.assertEqual(html.count('class="sourceVisual '), 3)
        self.assertEqual(html.count('class="nativeChartPanel"'), 4)
        self.assertIn('class="nativeChartSvg"', html)
        self.assertIn('class="nativeDonut"', html)
        self.assertEqual(data["meta"]["scope"], "excavator-category-overview")
        self.assertIn("245", data["meta"]["excluded_slides"])
        self.assertEqual(
            data["market_cycle"][-1]["status"],
            "historical_forecast_not_current_actual",
        )

        for name in ["杜冬洋", "李梦琪", "Felix", "Terrian", "Michael Wolf", "Chris"]:
            with self.subTest(name=name):
                self.assertNotIn(name, html)
                self.assertNotIn(name, data_file.read_text(encoding="utf-8"))

        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        self.assertIn('href="excavator-market-overview.html"', arc_html)
        self.assertIn("北美挖掘机市场总体洞察", arc_html)

    def test_ppt_source_content_is_fully_mapped_to_formal_pages(self):
        source_path = ROOT / "data" / "ppt-insights" / "ppt-source-content.json"
        payload = json.loads(source_path.read_text(encoding="utf-8"))
        slides = {record["id"]: record for record in payload["slides"]}
        page_by_slug = {meta["slug"]: meta["output"] for meta in SOURCE_FILES}

        actual_slide_ids = set()
        actual_visuals = set()
        expected_table_placements = 0
        actual_table_placements = 0

        page_specs = [("overview", "excavator-market-overview.html", payload["overview"])]
        page_specs.extend(
            (slug, page_by_slug[slug], slide_ids)
            for slug, slide_ids in payload["by_slug"].items()
        )

        for scope, output, slide_ids in page_specs:
            page_html = (ROOT / output).read_text(encoding="utf-8")
            text_parser = TextContentParser()
            text_parser.feed(page_html)
            normalized_page_text = re.sub(r"\s+", "", "".join(text_parser.parts))
            page_slide_ids = {
                f"slide-{int(match):03d}"
                for match in re.findall(r'data-source-slide="(\d+)"', page_html)
            }
            with self.subTest(scope=scope, page=output):
                self.assertEqual(page_slide_ids, set(slide_ids))

            expected_tables = sum(len(slides[slide_id]["table_ids"]) for slide_id in slide_ids)
            actual_tables = page_html.count('class="sourceTableBlock"')
            self.assertEqual(actual_tables, expected_tables, output)
            expected_table_placements += expected_tables
            actual_table_placements += actual_tables

            for slide_id in slide_ids:
                record = slides[slide_id]
                actual_slide_ids.add(slide_id)
                for item in record.get("body", []):
                    source_text = item.get("zh", "").strip()
                    if source_text:
                        normalized_source_text = re.sub(r"\s+", "", source_text)
                        self.assertIn(
                            normalized_source_text,
                            normalized_page_text,
                            f"{output}: {slide_id}",
                        )
                for item in record.get("notes", []):
                    source_text = item.get("zh", "").strip()
                    if source_text:
                        normalized_source_text = re.sub(r"\s+", "", source_text)
                        self.assertIn(
                            normalized_source_text,
                            normalized_page_text,
                            f"{output}: {slide_id}",
                        )
                slide_match = re.search(
                    rf'<article class="sourceSlide[^"]*" data-source-slide="{int(record["slide"])}">.*?</article>',
                    page_html,
                    re.DOTALL,
                )
                self.assertIsNotNone(slide_match, f"{output}: {slide_id}")
                slide_html = slide_match.group(0)
                chart_visuals = [
                    visual
                    for visual in record.get("visuals", [])
                    if visual.get("chart_data")
                ]
                if slide_id == "slide-010":
                    self.assertEqual(slide_html.count('class="nativeChartPanel"'), 4)
                else:
                    self.assertEqual(
                        slide_html.count("sourceDataChart"),
                        len(chart_visuals),
                        f"{output}: {slide_id}",
                    )
                for visual in record.get("visuals", []):
                    if not visual.get("chart_data"):
                        self.assertIn(f'src="{visual["file"]}"', slide_html)
                    actual_visuals.add(visual["file"])

        expected_slide_ids = {record["id"] for record in payload["slides"]}
        expected_visuals = {
            visual["file"]
            for record in payload["slides"]
            for visual in record.get("visuals", [])
        }
        self.assertEqual(actual_slide_ids, expected_slide_ids)
        self.assertEqual(actual_visuals, expected_visuals)
        self.assertEqual(actual_table_placements, expected_table_placements)
        self.assertEqual(expected_table_placements, 265)
        self.assertEqual(len(expected_visuals), 207)

    def test_generated_pages_strip_source_cell_edge_whitespace(self):
        table_payload = json.loads(
            (ROOT / "data" / "ppt-insights" / "ppt-business-tables.json").read_text(
                encoding="utf-8"
            )
        )
        for record in table_payload["records"]:
            for row in record["matrix_zh"]:
                for cell in row:
                    self.assertEqual(cell, cell.strip())
        for meta in SOURCE_FILES:
            html = (ROOT / meta["output"]).read_text(encoding="utf-8")
            with self.subTest(page=meta["output"]):
                self.assertFalse(any(line.endswith((" ", "\t")) for line in html.splitlines()))

    def test_all_formal_pages_include_project_credits(self):
        formal_pages = [
            "arc.html",
            "data-downloads.html",
            "excavator-market-overview.html",
            *(meta["output"] for meta in SOURCE_FILES),
        ]
        self.assertEqual(len(formal_pages), 18)
        for output in formal_pages:
            html = (ROOT / output).read_text(encoding="utf-8")
            with self.subTest(page=output):
                self.assertEqual(
                    len(re.findall(r'class="[^"]*\bsiteCredits\b[^"]*"', html)),
                    1,
                )
                self.assertIn('href="assets/site-credits.css?v=20260724a"', html)
                self.assertIn("指导领导：张盛楠", html)
                self.assertIn("数据可视化：刘畅", html)
                self.assertIn("数据来源：ARC产品小组", html)
                self.assertIn("问题提报：", html)
                self.assertIn('href="mailto:changl@xcmgarc.com"', html)
                self.assertIn("Executive Sponsor: Zhang Shengnan", html)
                self.assertIn("Data Visualization: Liu Chang", html)
                self.assertIn("Data Source: ARC Product Team", html)
                self.assertIn("Issue Reporting:", html)

    def test_manifest_matches_generated_models(self):
        manifest = json.loads((ROOT / "data" / "project-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["excavatorTonnageCount"], len(self.models))
        self.assertEqual(manifest["benchmarkProductCount"], sum(len(model["products"]) for model in self.models))
        self.assertEqual(manifest["sourceWorkbookCount"], len(SOURCE_FILES))
        self.assertEqual(manifest["minimumScoreCoverage"], MIN_SCORE_COVERAGE)
        self.assertEqual(
            manifest["marketOverview"],
            {
                "output": "excavator-market-overview.html",
                "data": "data/ppt-insights/excavator-market-overview.json",
                "classification": "XCMG ARC INTERNAL",
            },
        )


if __name__ == "__main__":
    unittest.main()
