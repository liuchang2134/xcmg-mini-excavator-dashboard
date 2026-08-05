from __future__ import annotations

import html
import json
import math
import re
from pathlib import Path
from typing import Any, Iterable

try:
    from .crane_ppt_insights import CLASS_SLIDES, OUTPUT_DIR, SOURCE_DATE
except ImportError:
    from crane_ppt_insights import CLASS_SLIDES, OUTPUT_DIR, SOURCE_DATE


ROOT = Path(__file__).resolve().parents[1]

STATUS_COPY = {
    "historical": ("历史数据", "Historical data"),
    "current-at-source-date": ("截至2025-07判断", "Assessment as of 2025-07"),
    "plan": ("规划 / 待验证", "Plan / validation pending"),
}

SECTION_LABELS = {
    "macro": "市场环境",
    "market-volume": "市场规模",
    "competition": "品牌格局",
    "regional-demand": "区域需求",
    "boom-truck": "通用底盘",
    "all-terrain": "全地面",
    "rough-terrain": "越野轮胎",
    "crawler": "履带起重机",
    "portfolio": "产品型谱",
    "roadmap": "改进路线",
    "go-to-market": "市场与服务",
}

SLIDE_TITLE_OVERRIDES = {
    2: "北美宏观环境及其对起重机业务的影响",
    3: "北美起重机销量与产品类别结构",
    4: "通用底盘与越野轮胎起重机品牌份额",
    5: "全地面与履带起重机品牌份额",
    6: "各产品类别主要竞争标杆与市场定位",
    7: "北美起重机区域需求分布",
    8: "北美区域差异与产品适应性",
    9: "北美区域需求与配置策略",
}

IMAGE_CAPTION_OVERRIDES = {
    7: (
        "2024年加拿大越野轮胎起重机销量分布",
        "2024年美国越野轮胎起重机销量分布",
        "2024年美国全地面起重机销量分布",
        "2024年美国履带起重机销量分布",
        "2024年美国通用底盘起重机销量分布",
    ),
}

CLASS_INTRO = {
    "RT-60t": (
        "60-75吨级越野吊集中服务住宅施工、电力检修、油气与工业设施、道路桥梁等场景。材料同时覆盖区域工况、参配对比、客户口碑及可靠性、安全性、操控性、舒适性和维修性评价。",
        "The 60-75 t rough-terrain segment serves residential construction, utility maintenance, oil and gas, industrial facilities, roads and bridges. The evidence covers regional applications, specifications, customer feedback, reliability, safety, controllability, comfort and serviceability.",
    ),
    "RT-75t": (
        "60-75吨级越野吊集中服务住宅施工、电力检修、油气与工业设施、道路桥梁等场景。材料同时覆盖区域工况、参配对比、客户口碑及可靠性、安全性、操控性、舒适性和维修性评价。",
        "The 60-75 t rough-terrain segment serves residential construction, utility maintenance, oil and gas, industrial facilities, roads and bridges. The evidence covers regional applications, specifications, customer feedback, reliability, safety, controllability, comfort and serviceability.",
    ),
    "RT-100t": (
        "90-110吨级越野吊面向城市更新、工业厂房、电力和通信维护、自然灾害救援及大型工程。对标重点从单一吊重参数扩展到长臂覆盖、低温和高温适应、微动性、故障诊断与维保便利性。",
        "The 90-110 t rough-terrain segment supports urban renewal, industrial plants, utility and communications work, disaster response and large projects. Benchmarking extends beyond lift capacity to long-boom coverage, climate adaptation, fine control, diagnostics and serviceability.",
    ),
    "RT-130t": (
        "120-130吨级越野吊对应大型工业、能源、港口及重型基础设施吊装。页面保留区域与工况矩阵、XCR130_U参数配置对比、客户使用评价以及当时的产品定位和市场目标。",
        "The 120-130 t rough-terrain segment targets large industrial, energy, port and heavy-infrastructure lifts. The page retains the regional application matrix, XCR130_U comparison, customer-use evaluation, and the product positioning and market targets stated at the source date.",
    ),
    "RT-160t": (
        "该吨级材料属于165美吨越野吊产品规划，不是当前实机验证结论。页面用于说明北美大吨位需求、初步技术方案、型谱位置和计划节点，并与现有Excel数据缺口分开呈现。",
        "This class is represented by the planned 165-US-ton rough-terrain crane, not a verified current machine evaluation. The page shows demand, the initial technical concept, portfolio position and planned milestones separately from Excel data gaps.",
    ),
    "AT-150t": (
        "150吨级全地面起重机聚焦风电、能源、工业安装和大型基础设施。材料覆盖重点区域、客户任务、XCA150_U参配对比，以及安全、人性化、配重适应性、可靠性和伸缩效率的实机评价。",
        "The 150 t all-terrain segment focuses on wind, energy, industrial installation and major infrastructure. Evidence covers priority regions, customer tasks, XCA150_U comparisons, safety, ergonomics, counterweight flexibility, reliability and telescoping efficiency.",
    ),
}

REPORT_SECTIONS = [
    (
        "macro",
        "宏观环境与市场规模",
        "Macro Environment and Market Size",
        "从政策、经济、社会、技术、环境和法规六个维度解释北美起重机市场的约束与机会，并连接到销量、产品结构和经营风险。",
        "Explains the constraints and opportunities in the North American crane market across policy, economic, social, technological, environmental and legal dimensions, linked to volume, product mix and operating risk.",
        list(range(1, 4)),
    ),
    (
        "competition",
        "竞争格局与区域需求",
        "Competitive Landscape and Regional Demand",
        "按通用底盘、越野吊、全地面和履带吊拆分品牌份额，并结合美国和加拿大主要区域的产业结构、气候和法规差异。",
        "Breaks down share by boom truck, rough-terrain, all-terrain and crawler crane, then connects United States and Canada regional demand to industry structure, climate and regulation.",
        list(range(4, 10)),
    ),
    (
        "boom-truck",
        "通用底盘起重机产品线",
        "Boom-Truck Product Line",
        "完整保留35吨及以下、40-45吨和50吨以上产品段的区域场景、参数配置、客户评价、产品定位和当时目标。",
        "Retains regional applications, specification and equipment comparisons, customer evaluations, positioning and source-date targets for the up-to-35 t, 40-45 t and 50 t-plus segments.",
        list(range(10, 58)),
    ),
    (
        "all-terrain",
        "全地面起重机扩展分析",
        "All-Terrain Crane Expansion",
        "补充XCA275_U等未建立正式Excel吨级页的市场、区域、产品和客户评价；XCA150_U细节在对应吨级页展示。",
        "Adds the market, regional, product and customer evaluation for XCA275_U and other segments without a formal Excel class page. XCA150_U detail remains on its class page.",
        list(range(69, 81)),
    ),
    (
        "crawler",
        "履带起重机市场与产品评价",
        "Crawler-Crane Market and Product Evaluation",
        "覆盖履带吊销量结构、100吨级产品方案、核心参数、六性评价、客户反馈、价格定位和样机验证目标。",
        "Covers crawler-crane volume mix, the 100 t concept, specifications, six-characteristic evaluation, customer feedback, price positioning and prototype-validation targets.",
        list(range(120, 130)),
    ),
    (
        "portfolio",
        "产品型谱与竞争力提升",
        "Portfolio and Competitiveness Improvement",
        "把通用底盘、全地面、越野吊和履带吊的型谱覆盖、空白吨级、现有产品问题及跨产品线提升重点放在同一张路线图中。",
        "Brings portfolio coverage, missing classes, current-product issues and cross-line improvement priorities for boom trucks, all-terrain, rough-terrain and crawler cranes into one roadmap.",
        list(range(130, 143)),
    ),
    (
        "roadmap",
        "2025-2027产品路线图",
        "2025-2027 Product Roadmap",
        "按原资料保留新品定义、关键技术方案、售价目标和计划节点；这些内容全部标为规划，不能视为已经上市或完成验证。",
        "Retains new-product definitions, technical concepts, price targets and planned milestones. Every item is labelled as a plan and must not be read as launched or validated.",
        list(range(143, 153)),
    ),
    (
        "go-to-market",
        "市场、渠道、服务与本地化",
        "Market, Channel, Service and Localization",
        "展示市场机会、销售目标、产品进攻策略、经销网络、租赁客户、服务备件和美国本地组装规划，形成从产品到交付的闭环。",
        "Shows market opportunity, sales targets, product strategy, dealer network, rental accounts, service and parts, and U.S. assembly plans to connect product decisions to delivery.",
        list(range(153, 164)),
    ),
]


def esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def load_crane_insights() -> dict[str, Any]:
    slides = json.loads((OUTPUT_DIR / "slides.json").read_text(encoding="utf-8"))
    segments = json.loads((OUTPUT_DIR / "segment-map.json").read_text(encoding="utf-8"))
    evidence = json.loads((OUTPUT_DIR / "evidence.json").read_text(encoding="utf-8"))
    return {
        "slides": slides,
        "by_slide": {item["slide"]: item for item in slides},
        "segments": segments,
        "evidence": evidence,
    }


def _status_badge(status: str) -> str:
    zh, en = STATUS_COPY.get(status, (status, status))
    return f'<span class="sourceStatus {esc(status)}" data-en="{esc(en)}">{esc(zh)}</span>'


def _useful_text(record: dict[str, Any]) -> list[str]:
    ignored_exact = {
        "二、大区产业板块洞察",
        "二、大区产业板块洞察—北美",
        "二、大区产业板块洞察—美国和加拿大",
        "起重机产品线",
        "数据来源: AEM",
        "数据来源：AEM",
    }
    ignored_prefixes = ("2、核心产品线—", "2、核心产品线—越野轮胎起重机")
    items = []
    seen = set()
    for block in record["text_blocks"]:
        for part in re.split(r"\n(?=\S)", block["text"]):
            text = part.strip()
            if not text or text in ignored_exact or text.startswith(ignored_prefixes):
                continue
            if text.startswith("2.4 市场洞察分析-"):
                text = text.split("-", 1)[1].strip()
            elif text.startswith("2.6 产品线竞争力提升举措-"):
                text = text.split("-", 1)[1].strip()
            if re.fullmatch(r"\d{1,3}", text):
                continue
            key = re.sub(r"\s+", "", text)
            if key in seen:
                continue
            seen.add(key)
            items.append(text)
    return items


def _display_title(record: dict[str, Any]) -> str:
    if record["slide"] in SLIDE_TITLE_OVERRIDES:
        return SLIDE_TITLE_OVERRIDES[record["slide"]]
    table_labels = []
    for table in record.get("tables", []):
        rows = table.get("rows") or []
        if len(rows) != 1 or len(rows[0]) != 1:
            continue
        label = str(rows[0][0]).strip()
        if label and len(label) <= 30 and label not in table_labels:
            table_labels.append(label)
    if table_labels:
        return _clean_business_title(" · ".join(table_labels))
    candidates = _useful_text(record)
    preferred_tokens = (
        "徐工型号",
        "客户使用评价",
        "对比结论",
        "区域范围",
        "销量趋势",
        "市场洞察",
        "可售型谱",
        "市场营销",
        "服务能力",
        "当地化",
        "布局",
    )
    for text in candidates:
        if any(token in text for token in preferred_tokens):
            return _clean_business_title(text.split("：", 1)[0][:90])
    for text in candidates:
        if 6 <= len(text) <= 90:
            return _clean_business_title(text)
    return _clean_business_title(record["title"][:90])


def _clean_business_title(value: str) -> str:
    text = re.sub(r"^\s*\d+(?:\.\d+)+\s*", "", str(value)).strip()
    region = re.fullmatch(r"\d+\s*-\s*(.+?)\s*·\s*(美国|加拿大)", text)
    if region:
        return f"{region.group(2)}{region.group(1).strip()}市场与工况"
    replacements = (
        ("占有率分析及竞争对手锁定", "品牌份额与主要竞争对手"),
        ("市场洞察分析-", ""),
        ("市场营销-", ""),
        ("产品线竞争力提升举措-", ""),
        ("可售型谱分析——", ""),
    )
    for source, target in replacements:
        text = text.replace(source, target)
    return text.strip(" -—·") or "产品与市场分析"


def _paragraphs(record: dict[str, Any], limit: int | None = None) -> str:
    items = _useful_text(record)
    title = _display_title(record)
    filtered = [item for item in items if item != title]
    if limit is not None:
        filtered = filtered[:limit]
    paragraphs = []
    short_run = []
    for item in filtered:
        compact = re.sub(r"\s+", " ", item).strip()
        compact = re.sub(r"^\d+(?:\.\d+)+\s+", "", compact)
        compact = compact.replace("市场洞察分析-", "", 1).strip(" -—·")
        if not compact or compact == title:
            continue
        is_short = len(compact) <= 45 and not re.search(r"[。！？；:]$", compact)
        if is_short:
            short_run.append(compact)
            if sum(len(value) for value in short_run) < 90:
                continue
        if short_run:
            paragraphs.append("；".join(short_run) + "。")
            short_run = []
        if not is_short:
            paragraphs.append(compact)
    if short_run:
        paragraphs.append("；".join(short_run) + "。")
    return "".join(f'<p lang="zh-CN">{esc(item)}</p>' for item in paragraphs)


def _meaningful_table(table: dict[str, Any]) -> bool:
    rows = table.get("rows") or []
    nonempty = [cell for row in rows for cell in row if str(cell).strip()]
    return len(rows) >= 2 and len(nonempty) >= 4


def _render_table(table: dict[str, Any], slide_number: int, index: int) -> str:
    rows = table["rows"]
    width = max((len(row) for row in rows), default=0)
    if width == 0:
        return ""
    rendered_rows = []
    for row_index, row in enumerate(rows):
        cells = list(row) + [""] * (width - len(row))
        tag = "th" if row_index == 0 else "td"
        rendered_rows.append(
            "<tr>" + "".join(f"<{tag}>{esc(cell)}</{tag}>" for cell in cells) + "</tr>"
        )
    return (
        f'<div class="craneSourceTable" data-table-slide="{slide_number}" data-table-index="{index}">'
        '<table>' + "".join(rendered_rows) + "</table></div>"
    )


def _chart_values(chart: dict[str, Any]) -> list[float]:
    return [
        float(value)
        for series in chart.get("series", [])
        for value in series.get("values", [])
        if isinstance(value, (int, float)) and math.isfinite(value)
    ]


def _render_pie(chart: dict[str, Any], chart_id: str) -> str:
    categories = chart.get("categories") or []
    series = (chart.get("series") or [{}])[0]
    values = [float(value or 0) for value in series.get("values", [])]
    if not categories or not values or sum(values) <= 0:
        return ""
    colors = ["#0a5ca4", "#f5b400", "#279b7d", "#e2605f", "#7656c8", "#6d8498", "#a97112", "#2d7257"]
    total = sum(values)
    cursor = 0.0
    stops = []
    legend = []
    for index, (category, value) in enumerate(zip(categories, values)):
        share = value / total * 100
        color = colors[index % len(colors)]
        stops.append(f"{color} {cursor:.3f}% {cursor + share:.3f}%")
        legend.append(
            f'<li tabindex="0" data-chart-key="{esc(category)}"><i style="background:{color}"></i>'
            f'<span>{esc(category)}</span><b>{share:.1f}%</b><small>{value:,.0f}</small></li>'
        )
        cursor += share
    return (
        f'<div class="insightDonut" data-chart-id="{esc(chart_id)}">'
        f'<div class="donutGraphic" style="--donut:{esc(",".join(stops))}"><span>{total:,.0f}</span></div>'
        f'<ul>{"".join(legend)}</ul></div>'
    )


def _render_columns(chart: dict[str, Any], chart_id: str) -> str:
    categories = chart.get("categories") or []
    series = chart.get("series") or []
    values = _chart_values(chart)
    if not categories or not series or not values:
        return ""
    maximum = max(abs(value) for value in values) or 1
    colors = ["#0a5ca4", "#f5b400", "#279b7d", "#e2605f", "#7656c8", "#6d8498"]
    groups = []
    max_categories = 18
    for category_index, category in enumerate(categories[:max_categories]):
        bars = []
        for series_index, item in enumerate(series[:6]):
            raw = item.get("values", [])
            value = raw[category_index] if category_index < len(raw) else None
            if not isinstance(value, (int, float)):
                continue
            height = max(2.0, abs(float(value)) / maximum * 100)
            color = colors[series_index % len(colors)]
            label = item.get("name") or "Series"
            bars.append(
                f'<i tabindex="0" style="height:{height:.2f}%;background:{color}" '
                f'data-label="{esc(label)}" data-value="{float(value):g}" title="{esc(label)}: {float(value):g}"></i>'
            )
        groups.append(
            f'<div class="insightColumnGroup"><div>{"".join(bars)}</div><span>{esc(category)}</span></div>'
        )
    legend = "".join(
        f'<span><i style="background:{colors[index % len(colors)]}"></i>{esc(item.get("name") or "Series")}</span>'
        for index, item in enumerate(series[:6])
    )
    return (
        f'<div class="insightColumns" data-chart-id="{esc(chart_id)}"><div class="columnPlot">'
        f'{"".join(groups)}</div><div class="chartLegend">{legend}</div></div>'
    )


def _render_chart(chart: dict[str, Any], slide_number: int, index: int) -> str:
    chart_id = f"slide-{slide_number}-chart-{index}"
    chart_type = chart.get("chart_type", "").upper()
    if "PIE" in chart_type or "DOUGHNUT" in chart_type:
        return _render_pie(chart, chart_id)
    return _render_columns(chart, chart_id)


def _render_images(record: dict[str, Any]) -> str:
    images = record.get("images") or []
    if not images:
        return ""
    override_captions = IMAGE_CAPTION_OVERRIDES.get(record["slide"], ())
    figures = []
    for index, path in enumerate(images):
        caption = (
            override_captions[index]
            if index < len(override_captions)
            else _display_title(record)
        )
        figures.append(
            '<figure><button type="button" class="insightImageButton" '
            f'data-full-src="{esc(path)}" data-caption="{esc(caption)}" '
            f'aria-label="放大查看：{esc(caption)}" title="放大查看">'
            f'<img src="{esc(path)}" alt="{esc(caption)}" loading="lazy" decoding="async">'
            f'</button><figcaption>{esc(caption)}</figcaption></figure>'
        )
    return f'<div class="craneInsightGallery count-{len(images)}">{"".join(figures)}</div>'


def render_slide_record(record: dict[str, Any]) -> str:
    tables = [
        (index, table)
        for index, table in enumerate(record.get("tables", []), 1)
        if _meaningful_table(table)
    ]
    charts = [
        _render_chart(chart, record["slide"], index)
        for index, chart in enumerate(record.get("charts", []), 1)
    ]
    charts = [chart for chart in charts if chart]
    body = _paragraphs(record)
    media = _render_images(record)
    table_html = "".join(
        _render_table(table, record["slide"], index)
        for index, table in tables
    )
    visual_html = "".join(charts)
    content_class = " has-media" if media else ""
    if len(record.get("images") or []) >= 3:
        content_class += " many-media"
    record_label = SECTION_LABELS.get(record.get("section"), "产品分析")
    return (
        f'<article class="craneInsightRecord{content_class}" data-source-slide="{record["slide"]}" '
        f'data-source-status="{esc(record["status"])}">'
        '<header><div>'
        f'<span class="recordLabel">{esc(record_label)}</span>'
        f'<h3>{esc(_display_title(record))}</h3></div>{_status_badge(record["status"])}</header>'
        f'<div class="recordBody"><div class="recordNarrative">{body}</div>{media}</div>'
        f'{visual_html}{table_html}'
        f'<footer>资料日期 {SOURCE_DATE} · 记录号 CR-{record["slide"]:03d}</footer>'
        '</article>'
    )


def render_source_register(slide_numbers: Iterable[int]) -> str:
    numbers = sorted(set(int(number) for number in slide_numbers))
    if not numbers:
        return ""
    ranges = []
    start = previous = numbers[0]
    for number in numbers[1:]:
        if number == previous + 1:
            previous = number
            continue
        ranges.append(f"{start}" if start == previous else f"{start}-{previous}")
        start = previous = number
    ranges.append(f"{start}" if start == previous else f"{start}-{previous}")
    return (
        '<div class="craneSourceRegister"><b data-en="Source scope">资料范围</b>'
        f'<span>CR-{esc(", CR-".join(ranges))}</span>'
        f'<small data-en="Source date: {SOURCE_DATE}; historical facts, source-date assessments and future plans are labelled separately.">'
        f'资料日期：{SOURCE_DATE}；历史事实、资料日期判断和未来规划已分开标识。</small></div>'
    )


def render_class_context(class_id: str, language: str = "zh") -> str:
    data = load_crane_insights()
    if class_id not in CLASS_SLIDES:
        raise KeyError(class_id)
    records = [data["by_slide"][number] for number in CLASS_SLIDES[class_id]]
    intro_zh, intro_en = CLASS_INTRO[class_id]
    segment = data["segments"][class_id]
    status = "plan" if segment["source_scope"] == "plan" else "current-at-source-date"
    return (
        '<section id="market-context" class="craneInsightSection classContext">'
        '<div class="insightSectionHead"><div><p class="eyebrow">MARKET AND PRODUCT EVIDENCE</p>'
        f'<h2 data-en="Market, Customer and Product Evidence">市场、客户与产品证据</h2>'
        f'<p data-en="{esc(intro_en)}">{esc(intro_zh)}</p></div>{_status_badge(status)}</div>'
        f'<div class="craneInsightRecords">{"".join(render_slide_record(record) for record in records)}</div>'
        f'{render_source_register(CLASS_SLIDES[class_id])}</section>'
    )


def render_market_overview(language: str = "zh") -> str:
    data = load_crane_insights()
    sections = []
    all_numbers = []
    for section_id, title_zh, title_en, lead_zh, lead_en, numbers in REPORT_SECTIONS:
        records = [data["by_slide"][number] for number in numbers if number != 1]
        all_numbers.extend(numbers)
        source_attributes = ' data-source-slide="1" data-source-status="current-at-source-date"' if 1 in numbers else ""
        sections.append(
            f'<section id="{esc(section_id)}" class="craneInsightSection reportBand"{source_attributes}>'
            '<div class="insightSectionHead"><div>'
            f'<h2 data-en="{esc(title_en)}">{esc(title_zh)}</h2>'
            f'<p data-en="{esc(lead_en)}">{esc(lead_zh)}</p></div>'
            f'<span class="sectionCount">{len(numbers)} 项分析</span></div>'
            f'<div class="craneInsightRecords">{"".join(render_slide_record(record) for record in records)}</div>'
            '</section>'
        )
    return "".join(sections) + render_source_register(all_numbers)


def report_navigation() -> str:
    links = "".join(
        f'<a href="#{esc(section_id)}" data-en="{esc(title_en)}">{esc(title_zh)}</a>'
        for section_id, title_zh, title_en, _lead_zh, _lead_en, _numbers in REPORT_SECTIONS
    )
    return (
        '<a class="home" href="arc.html" data-en="Return to Platform Home">返回对标平台主页</a>'
        + links
    )


def render_market_report_page() -> str:
    return f'''<!doctype html>
<html lang="zh-CN" data-language="zh"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>北美起重机市场与产品洞察 | XCMG ARC</title>
<link rel="stylesheet" href="assets/dashboard.css?v=20260805d">
<link rel="stylesheet" href="assets/crane-dashboard.css?v=20260805d">
<link rel="stylesheet" href="assets/crane-insights.css?v=20260805d">
</head><body>
<a class="backTop" href="#top" aria-label="回到页面顶部">回到顶部</a>
<div class="layout" id="top"><aside class="nav">
<a class="navBrand" href="arc.html"><img src="assets/xcmg-logo.svg" alt="XCMG"></a>
<div><div class="navTitle" data-en="North American Crane Insight">北美起重机市场洞察</div><small>XCMG ARC</small></div>
<button class="languageToggle" type="button">EN</button>
<button class="sidebarToggle" type="button"><span>收起侧栏</span></button>
<button class="navToggle" type="button">页面导航</button>
<div class="navMenu" id="page-nav">{report_navigation()}</div></aside><main>
<header class="hero craneReportHero"><div class="heroText"><p class="eyebrow">CRANE MARKET AND PRODUCT INTELLIGENCE</p>
<h1 data-en="North American Crane Market and Product Insight">北美起重机市场与产品洞察</h1>
<p data-en="A complete view of market structure, regional demand, customer applications, product evaluation, portfolio gaps, roadmap, channels, service and localization.">覆盖市场结构、区域需求、客户工况、产品评价、型谱空白、产品路线图、渠道、服务和本地化保供，形成从市场到产品决策的完整分析。</p>
<div class="reportKpis"><span><b>163</b>项分析记录</span><span><b>4</b>类起重设备</span><span><b>9</b>个北美区域</span><span><b>2025-07</b>资料日期</span></div>
</div><figure class="heroMedia craneHeroMedia"><img src="assets/arc/category-cranes.webp" alt="XCMG crane product line"><figcaption>XCMG 起重设备产品线</figcaption></figure></header>
<section class="reportScope"><b>市场、区域、产品与服务洞察</b><p>总体报告承载跨吨级信息；已有Excel数据的越野吊与全地面吨级继续在各自正式页面中展示参数、配置、工况和排名。</p></section>
{render_market_overview()}
<footer class="dashboardFooter"><small data-en="Executive sponsor: Zhang Shengnan · Data visualization: Liu Chang · Data source: ARC Product Team · Issue reporting: changl@xcmgarc.com">指导领导：张盛楠　数据可视化：刘畅　数据来源：ARC产品小组　问题提报：changl@xcmgarc.com</small></footer>
</main></div><script src="assets/dashboard.js?v=20260805d"></script><script src="assets/i18n.js?v=20260805d"></script><script src="assets/crane-insights.js?v=20260805d"></script>
</body></html>'''


def render_legacy_redirect() -> str:
    return '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="0;url=crane-market-overview.html">
<title>正在进入北美起重机市场洞察 | XCMG ARC</title></head><body>
<p><a href="crane-market-overview.html">进入北美起重机市场洞察</a></p>
<script>location.replace("crane-market-overview.html" + location.search + location.hash);</script>
</body></html>'''
