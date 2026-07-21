import json
import math
import unittest
from collections import Counter
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
        self.assertEqual(len(SOURCE_FILES), 14)
        expected_outputs = {
            "excavator-8-10t.html",
            "excavator-12-14t.html",
            "excavator-14-16t-short-tail.html",
            "excavator-21-24t.html",
            "excavator-24-28t.html",
            "excavator-24-28t-short-tail.html",
            "excavator-28-33t.html",
            "excavator-33-40t.html",
        }
        self.assertTrue(expected_outputs.issubset({meta["output"] for meta in SOURCE_FILES}))
        for meta in SOURCE_FILES:
            self.assertTrue((ROOT / meta["output"]).exists(), meta["output"])
            self.assertTrue(meta["source"].exists(), meta["source"])
        arc_html = (ROOT / "arc.html").read_text(encoding="utf-8")
        self.assertEqual(arc_html.count('class="projectRow"'), len(SOURCE_FILES))
        self.assertIn("十四个吨级统一覆盖狭窄空间、沟槽、土方装车、破碎、坡地和租赁六类典型工况", arc_html)

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
                self.assertIn('src="assets/dashboard.js"', html)
                self.assertNotIn('class="summaryGrid" style="margin-top:12px"', html)

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
                self.assertIn("XCMG ARC 独立开发", html)
                self.assertIn("返回对标平台主页", html)
                self.assertNotIn("返回 ARC 主页", html)

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
        pages = [ROOT / "arc.html", ROOT / "data-downloads.html"] + [
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

    def test_generated_pages_strip_source_cell_edge_whitespace(self):
        for meta in SOURCE_FILES:
            html = (ROOT / meta["output"]).read_text(encoding="utf-8")
            with self.subTest(page=meta["output"]):
                self.assertFalse(any(line.endswith((" ", "\t")) for line in html.splitlines()))

    def test_manifest_matches_generated_models(self):
        manifest = json.loads((ROOT / "data" / "project-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["excavatorTonnageCount"], len(self.models))
        self.assertEqual(manifest["benchmarkProductCount"], sum(len(model["products"]) for model in self.models))
        self.assertEqual(manifest["sourceWorkbookCount"], len(SOURCE_FILES))
        self.assertEqual(manifest["minimumScoreCoverage"], MIN_SCORE_COVERAGE)


if __name__ == "__main__":
    unittest.main()
