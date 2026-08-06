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
from tools.crane_condition_context import CONDITION_EXECUTION, OFFICIAL_REFERENCES, field_observation
from tools.crane_data import load_crane_workbook
from tools.crane_ppt_insights import CLASS_SLIDES
from tools.crane_scoring import (
    CONDITIONS,
    condition_applicable,
    condition_config_weights,
    condition_metric_weights,
    score_sheet,
)


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


def test_rt160_uses_an_official_same_series_reference_without_claiming_model_specific_evidence():
    build_all()
    definition = PAGE_DEFINITIONS["RT-160t"]
    image_path = ROOT / definition["image"]
    rt160 = (ROOT / definition["output"]).read_text(encoding="utf-8")
    homepage = (ROOT / "arc.html").read_text(encoding="utf-8")

    assert definition["image"] == "assets/arc/cranes/xcr130u-product-official.jpeg"
    assert image_path.exists()
    with Image.open(image_path) as image:
        assert image.width >= 1600
        assert image.height >= 1000
    assert "仅用于 XCR165U 规划参考，不作为该型号实机证据" in rt160
    assert "XCR130U 官方同系列示意" in homepage
    assert "assets/arc/category-cranes.webp" not in homepage.split('data-tonnage="rt-160"', 1)[1].split("</a>", 1)[0]


def test_crane_pages_are_bilingual_and_mobile_bounded():
    build_all()
    page = (ROOT / "crane-rt-100t.html").read_text(encoding="utf-8")
    css = (ROOT / "assets" / "crane-dashboard.css").read_text(encoding="utf-8")
    assert 'data-en="Road Transport and Axle-Load Compliance"' in page
    assert 'name="viewport"' in page
    assert "@media(max-width:720px)" in css
    assert "html,body{max-width:100%;overflow-x:clip}" in css


def test_crane_work_conditions_use_explicit_engineering_mappings():
    workbook = load_crane_workbook()
    rt60 = next(sheet for sheet in workbook.sheets if sheet.label == "RT-60t")
    mobility = next(item for item in CONDITIONS if item["id"] == "site-mobility")
    stability = next(item for item in CONDITIONS if item["id"] == "outrigger-stability")

    mobility_names = condition_metric_weights(rt60, mobility)
    stability_names = condition_metric_weights(rt60, stability)

    assert len(CONDITIONS) >= 10
    assert "Speed" in mobility_names
    assert "Main winch max speed" not in mobility_names
    assert "Aux winch max speed" not in mobility_names
    assert "Outrigger penetration" not in stability_names


def test_crane_work_condition_scores_publish_component_coverage_and_contributions():
    workbook = load_crane_workbook()
    rt75 = next(sheet for sheet in workbook.sheets if sheet.label == "RT-75t")
    rt130 = next(sheet for sheet in workbook.sheets if sheet.label == "RT-130t")
    scoring = score_sheet(rt75)
    xcmg = next(item for item in scoring["products"] if item["is_xcmg"])

    detail = xcmg["condition_details"]["near-heavy-lift"]
    assert detail["parameter_coverage"] >= 0
    assert detail["configuration_coverage"] >= 0
    assert detail["components"]
    assert all("effective_weight" in item for item in detail["components"])


def test_crane_condition_sections_include_interactive_radar_contributions_and_simulator():
    build_all()
    page = (ROOT / "crane-rt-75t.html").read_text(encoding="utf-8")
    assert page.count('class="conditionSection"') == len(CONDITIONS)
    assert page.count('class="radarBox craneConditionRadar"') >= 8
    assert 'class="conditionContribution"' in page
    assert 'class="simulator craneConditionSimulator"' in page
    assert "作业执行与工程验证" in page
    assert "有益配置与设计特征" in page
    assert "贡献分仅表示该指标在当前工况权重下的作用" in page


def test_every_crane_condition_has_a_complete_job_chain_and_validation_record():
    assert set(CONDITION_EXECUTION) == {condition["id"] for condition in CONDITIONS}
    for condition_id, context in CONDITION_EXECUTION.items():
        assert len(context["workflow"]) >= 5, condition_id
        assert len(context["constraints"]) >= 3, condition_id
        assert len(context["checks"]) >= 3, condition_id
        assert context["customer"]["zh"] and context["customer"]["en"]
        assert context["load"]["zh"] and context["load"]["en"]
        assert context["boundary"]["zh"] and context["boundary"]["en"]
        assert all(reference in OFFICIAL_REFERENCES for reference in context["refs"])


def test_generated_crane_conditions_publish_workflow_constraints_validation_and_sources():
    build_all()
    page = (ROOT / "crane-rt-75t.html").read_text(encoding="utf-8")
    assert page.count('class="conditionExecution"') == len(CONDITIONS)
    assert page.count('class="conditionWorkflow"') == len(CONDITIONS)
    assert page.count('class="conditionVerification"') == len(CONDITIONS)
    assert page.count('class="conditionFieldObservation"') == 0
    assert page.count('class="classFieldEvaluation"') == 1
    assert "标准任务链" in page
    assert "建议验证记录" in page
    assert "地基与支撑条件" in page
    assert "临近电力线路作业" in page
    assert "https://www.osha.gov/" in page
    assert "https://mediahub.tadano.com/" in page


def test_crane_class_pages_surface_each_presentation_image_once_before_deep_analysis():
    build_all()
    slides = json.loads(
        (ROOT / "data" / "crane-ppt-insights" / "slides.json").read_text(
            encoding="utf-8"
        )
    )
    by_slide = {item["slide"]: item for item in slides}
    for class_id, slide_numbers in CLASS_SLIDES.items():
        page = (ROOT / PAGE_DEFINITIONS[class_id]["output"]).read_text(
            encoding="utf-8"
        )
        class_images = [
            image
            for number in slide_numbers
            for image in by_slide[number].get("images", [])
        ]

        assert class_images, class_id
        assert page.count('class="classVisualSummary"') == 1, class_id
        assert 'id="class-visuals"' in page, class_id
        assert 'href="#class-visuals"' in page, class_id
        assert page.index('class="classVisualSummary"') < page.index(
            'class="craneInsightRecords"'
        ), class_id
        for image in class_images:
            assert page.count(f'data-source-src="{image}"') == 1, (
                class_id,
                image,
            )


def test_crane_condition_method_boundaries_are_centralized_instead_of_repeated():
    build_all()
    page = (ROOT / "crane-rt-75t.html").read_text(encoding="utf-8")
    assert 'class="conditionScenarioBoundary"' not in page
    assert page.count("贡献分仅表示该指标在当前工况权重下的作用") == 1
    assert page.count("本场景将可追溯参数与配置组合为纸面适配性对比") == 1

    css = (ROOT / "assets" / "crane-dashboard.css").read_text(encoding="utf-8")
    decision_children = re.search(
        r"\.conditionDecisionGrid>\.gapPanel,\.conditionDecisionGrid>\.simulator\{([^}]*)\}",
        css,
    )
    assert decision_children
    assert "height:100%" not in decision_children.group(1).replace(" ", "")


def test_field_observations_preserve_tonnage_specific_evidence_boundaries():
    rt75 = field_observation("RT-75t", "precision-maintenance-lift")
    rt130 = field_observation("RT-130t", "precision-maintenance-lift")
    rt160 = field_observation("RT-160t", "precision-maintenance-lift")
    at150 = field_observation("AT-150t", "precision-maintenance-lift")
    assert "回转平顺性" in rt75["zh"]
    assert "全伸臂" in rt130["zh"]
    assert "未形成可核验" in rt160["zh"]
    assert "可变位平衡重" in at150["zh"]


def test_crane_pages_publish_a_work_condition_panorama_before_deep_dive_sections():
    build_all()
    rt_page = (ROOT / "crane-rt-75t.html").read_text(encoding="utf-8")
    at_page = (ROOT / "crane-at-150t.html").read_text(encoding="utf-8")

    assert 'id="condition-overview"' in rt_page
    assert 'class="radarBox craneConditionOverviewRadar"' in rt_page
    assert 'class="conditionHeatmap"' in rt_page
    assert 'class="conditionOverviewCards"' in rt_page
    assert rt_page.index('id="condition-overview"') < rt_page.index('id="cond1"')
    assert rt_page.count('class="conditionOverviewCard"') == len(CONDITIONS)

    at_sheet = next(sheet for sheet in load_crane_workbook().sheets if sheet.label == "AT-150t")
    assert at_page.count('class="conditionOverviewCard"') == sum(
        condition_applicable(at_sheet, condition) for condition in CONDITIONS
    )
    assert "资料未记录，不按0分处理" in rt_page


def test_crane_condition_framework_covers_additional_source_backed_work_conditions():
    ids = {item["id"] for item in CONDITIONS}
    assert {
        "rapid-mobilization",
        "partial-outrigger-confined",
        "precision-maintenance-lift",
    } <= ids

    workbook = load_crane_workbook()
    rt75 = next(sheet for sheet in workbook.sheets if sheet.label == "RT-75t")
    rt130 = next(sheet for sheet in workbook.sheets if sheet.label == "RT-130t")
    rapid = next(item for item in CONDITIONS if item["id"] == "rapid-mobilization")
    partial = next(item for item in CONDITIONS if item["id"] == "partial-outrigger-confined")
    precision = next(item for item in CONDITIONS if item["id"] == "precision-maintenance-lift")

    assert "Removable CWT" in condition_metric_weights(rt75, rapid)
    assert "Number of outrigger extensions" in condition_metric_weights(rt75, partial)
    assert "Aux winch max speed" in condition_metric_weights(rt75, precision)
    assert "2deg out of level load charts" in condition_config_weights(rt75, partial)
    assert "Auto winch and boom control" in condition_config_weights(rt130, precision)


def test_crane_condition_framework_adds_source_backed_application_scenarios():
    scenarios = {
        item["id"]: item
        for item in CONDITIONS
        if item.get("group") == "application"
    }
    assert {
        "urban-utility-installation",
        "industrial-shutdown-maintenance",
        "bridge-infrastructure-placement",
        "emergency-response",
        "port-yard-handling",
    } <= set(scenarios)

    workbook = load_crane_workbook()
    rt75 = next(sheet for sheet in workbook.sheets if sheet.label == "RT-75t")

    urban = scenarios["urban-utility-installation"]
    industrial = scenarios["industrial-shutdown-maintenance"]
    bridge = scenarios["bridge-infrastructure-placement"]
    emergency = scenarios["emergency-response"]
    port = scenarios["port-yard-handling"]

    assert "Tail swing radius" in condition_metric_weights(rt75, urban)
    assert "Aux winch max speed" in condition_metric_weights(rt75, industrial)
    assert "Full outrigger extension" in condition_metric_weights(rt75, bridge)
    assert "Gradability" in condition_metric_weights(rt75, emergency)
    assert "Main winch max speed" in condition_metric_weights(rt75, port)
    assert "360deg house lock" in condition_config_weights(rt75, urban)
    assert "Auto Lubrication system" in condition_config_weights(rt75, port)


def test_crane_pages_visually_separate_capability_conditions_and_application_scenarios():
    build_all()
    page = (ROOT / "crane-rt-75t.html").read_text(encoding="utf-8")
    assert 'data-condition-group="capability"' in page
    assert 'data-condition-group="application"' in page
    assert "工程能力工况" in page
    assert "典型施工场景" in page
    assert "纸面适配性对比，不替代现场试吊" in page


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


def test_crane_class_image_galleries_use_balanced_count_aware_layouts():
    css = (ROOT / "assets" / "crane-insights.css").read_text(encoding="utf-8")
    assert ".classVisualGroup .craneInsightGallery.count-1{max-width:960px;grid-template-columns:minmax(0,1fr)}" in css
    assert ".classVisualGroup .craneInsightGallery.count-2{max-width:1280px;grid-template-columns:repeat(2,minmax(0,1fr))}" in css
    assert ".classVisualGroup .craneInsightGallery.count-3,.classVisualGroup .craneInsightGallery.count-6{grid-template-columns:repeat(3,minmax(0,1fr))}" in css
    assert ".classVisualGroup .craneInsightGallery.count-4{max-width:1280px;grid-template-columns:repeat(2,minmax(0,1fr))}" in css
    assert ".classVisualGroup .craneInsightGallery.count-1 .insightImageButton{aspect-ratio:auto}" in css
    assert ".classVisualGroup .craneInsightGallery.count-1 img{height:auto}" in css
    assert "repeat(auto-fit,minmax(270px,1fr))" not in css
    assert "grid-template-columns:minmax(0,760px)" not in css

    build_all()
    for definition in PAGE_DEFINITIONS.values():
        page = (ROOT / definition["output"]).read_text(encoding="utf-8")
        assert "assets/crane-insights.css?v=20260806k" in page

    rt75_page = (ROOT / "crane-rt-75t.html").read_text(encoding="utf-8")
    visual_summary = rt75_page.split('id="class-visuals"', 1)[1].split(
        'id="macro-analysis"', 1
    )[0]
    assert ">评价细节 1</figcaption>" in visual_summary
    assert "客户使用评价对标 · 评价图像" not in visual_summary


def test_crane_ppt_reader_content_has_complete_local_english_translation():
    slides = json.loads(
        (ROOT / "data" / "crane-ppt-insights" / "slides.json").read_text(
            encoding="utf-8"
        )
    )
    translations = json.loads(
        (ROOT / "data" / "crane-ppt-insights" / "translations.en.json").read_text(
            encoding="utf-8"
        )
    )["translations"]

    source_strings = set()
    for slide in slides:
        source_strings.add(str(slide.get("title") or "").strip())
        source_strings.update(
            str(block.get("text") or "").strip()
            for block in slide.get("text_blocks", [])
        )
        for table in slide.get("tables", []):
            for row in table.get("rows", []):
                source_strings.update(str(cell).strip() for cell in row)
        for chart in slide.get("charts", []):
            source_strings.update(str(item).strip() for item in chart.get("categories", []))
            source_strings.update(
                str(series.get("name") or "").strip()
                for series in chart.get("series", [])
            )

    chinese_strings = {
        item for item in source_strings
        if item and re.search(r"[\u3400-\u9fff]", item)
    }
    missing = sorted(item for item in chinese_strings if not translations.get(item))
    assert missing == []


def test_crane_english_labels_are_professional_and_condition_counts_are_bilingual():
    build_all()
    page = (ROOT / "crane-rt-75t.html").read_text(encoding="utf-8")
    assert re.search(
        r'data-en="\d+ specifications / \d+ equipment items">\d+ 个参数 / \d+ 个配置项',
        page,
    )
    assert '<title data-en="XCMG XCR75U 75-USt Rough-Terrain Crane Competitive Benchmark | XCMG ARC">' in page
    for awkward_label in (
        "Greasless boom",
        "360deg house lock",
        "2deg out of level load charts",
        "heavy CWT",
        "Boom raise speed",
        "Boom extend speed",
    ):
        assert f'data-en="{awkward_label}"' not in page


def test_crane_english_layout_does_not_split_table_labels_letter_by_letter():
    css = (ROOT / "assets" / "crane-dashboard.css").read_text(encoding="utf-8")
    dashboard_css = (ROOT / "assets" / "dashboard.css").read_text(encoding="utf-8")
    insight_css = (ROOT / "assets" / "crane-insights.css").read_text(encoding="utf-8")
    assert 'html[data-language="en"] .compactCondition th' in css
    assert 'html[data-language="en"] .craneMatrix tr>:first-child' in css
    assert 'word-break:normal' in css
    assert '.compactCondition{max-height:none;' in css
    assert 'html[data-language="en"] .conditionTitle{grid-template-columns:1fr}' in css
    assert 'html[data-language="en"] .conditionContributionHead h3' in css
    assert 'html[data-language="en"] .conditionContributionTable tr>:nth-child(1)' in css
    assert 'html[data-language="en"] .detailMatrix tr>:nth-child(1)' in dashboard_css
    assert 'html[data-language="en"] .engineeringTableWrap' in dashboard_css
    assert 'html[data-language="en"] .craneInsightRecord>header' in insight_css
    assert 'html[data-language="en"] .craneInsightRecord>header>div{display:block}' in insight_css
    assert 'html[data-language="en"] .craneSourceTable:not(.wide){overflow-x:auto;overflow-y:visible}' in insight_css
    assert 'html[data-language="en"] .craneSourceTable:not(.wide) table{width:max-content;min-width:920px;table-layout:auto}' in insight_css
    assert 'html[data-language="en"] .craneSourceTable:not(.wide) tr>:first-child{width:190px;min-width:190px}' in insight_css
    assert 'html[data-language="en"] .craneSourceTable:not(.wide) tr>:last-child{width:320px;min-width:320px}' in insight_css


def test_crane_english_copy_uses_professional_market_terms():
    build_all()
    pages = [
        ROOT / "crane-market-overview.html",
        ROOT / "crane-rt-60t.html",
        ROOT / "crane-rt-75t.html",
        ROOT / "crane-rt-100t.html",
        ROOT / "crane-rt-130t.html",
        ROOT / "crane-rt-160t.html",
        ROOT / "crane-at-150t.html",
    ]
    rendered = "\n".join(page.read_text(encoding="utf-8") for page in pages)
    for artifact in (
        "Fuck Crane",
        "Tablet distribution",
        "Possession rate",
        "Occupancy rate",
        "Sales price/$ million",
        'data-label-en="补充信息"',
    ):
        assert artifact not in rendered
    assert "Truck-mounted crane" in rendered
    assert "Market share" in rendered
    assert "Sales price (US$10,000)" in rendered


def test_crane_rendered_english_removes_known_machine_translation_artifacts():
    build_all()
    pages = [
        ROOT / "crane-market-overview.html",
        ROOT / "crane-rt-60t.html",
        ROOT / "crane-rt-75t.html",
        ROOT / "crane-rt-100t.html",
        ROOT / "crane-rt-130t.html",
        ROOT / "crane-rt-160t.html",
        ROOT / "crane-at-150t.html",
    ]
    rendered = "\n".join(page.read_text(encoding="utf-8") for page in pages)
    forbidden = (
        " ' s",
        "seller's hit product",
        "obvious parameters",
        "etc., regional characteristics",
        "well-building",
        "United East Central Markets",
        "electricity/advertising/communications high altitude",
        "The operational situation can be covered",
        "Work situation to meet needs",
        'data-en="Yes, ?',
        "Current 2 ;",
        "Current 3 ;",
        "  higher in the evaluated direction",
    )
    for artifact in forbidden:
        assert artifact not in rendered
    assert "North American homes use wood-frame construction" in rendered
    assert "US East-Central market" in rendered
    assert "XCR75_U is XCMG&#x27;s primary model in this class" in rendered


def test_crane_english_translation_table_has_no_known_corrupt_phrases():
    payload = json.loads(
        (ROOT / "data" / "crane-ppt-insights" / "translations.en.json").read_text(
            encoding="utf-8"
        )
    )
    translations = payload["translations"]
    assert len(translations) == payload["source_count"] == 2229
    assert all(value.strip() for value in translations.values())
    assert not any(re.search(r"[\u3400-\u9fff]", value) for value in translations.values())

    forbidden = re.compile(
        r"boom trick|boom trock|outsidergers?|replay goldbox|driver.?s room|"
        r"nothing wrong with you|i don.?t know what you.?re talking about|"
        r"competor|competator|compitor|humanization|main arm|secondary arm|"
        r"mudslides?/brush roads?|minority liftings?|shift patterns|"
        r"power limitr|force limitr|life operation|stop layouting|"
        r"gaza and east|schwying|type houtrigger|combinsengine|benzengine|"
        r"extrarigger|overrigger|outridges|setting the exiters|full stretcher|"
        r"computerreliability|ping-soon|cargo line sales|layout 1",
        re.IGNORECASE,
    )
    assert not [value for value in translations.values() if forbidden.search(value)]
    assert translations["舒适性"] == "Operator comfort"
    assert translations["钢丝绳"] == "Wire rope"
    assert translations["软文资料"] == "Sales literature"
    assert translations["主臂旁弯"] == "Main boom lateral deflection"
    assert translations["要求起重机具备强爬坡能力，适应泥泞/碎石路面。"] == (
        "The crane requires strong gradeability and must remain mobile on muddy or gravel surfaces."
    )
    assert translations["暂不布局"] == "Not currently planned"
