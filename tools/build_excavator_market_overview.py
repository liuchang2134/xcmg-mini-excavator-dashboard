"""Build the source-faithful excavator category overview.

The page renders original presentation text, native visual objects and rebuilt
HTML tables. It intentionally avoids editorial summary data maintained outside
the presentation source.
"""

import re
from pathlib import Path

from build_excavator_dashboards import (
    ROOT,
    bilingual_leaf,
    esc,
    load_ppt_business_tables,
    load_ppt_source_content,
    render_source_slide,
    render_source_table,
    render_source_visuals,
)


SECTION_META = [
    ("environment", "environment", "宏观环境与北美市场基础", "External Environment and North American Market"),
    ("industry", "industry", "行业趋势与竞争格局", "Industry Trend and Competitive Landscape"),
    ("competition", "competition", "品牌占有率与标杆锁定", "Brand Share and Benchmark Selection"),
    ("class_structure", "class-structure", "吨级结构与核心规格", "Tonnage Structure and Core Classes"),
    ("portfolio", "portfolio", "产品型谱与覆盖能力", "Product Portfolio and Coverage"),
    ("roadmap", "roadmap", "产品竞争力提升举措", "Product Competitiveness Roadmap"),
    ("sales_plan", "sales-plan", "销售目标与市场推进", "Sales Targets and Market Development"),
    ("intelligence", "intelligence", "市场洞察资源与信息渠道", "Market Intelligence Resources"),
]

CHART_COLORS = [
    "#7f91a6",
    "#9bcf78",
    "#f4c542",
    "#df8c72",
    "#21a5a5",
    "#e15a64",
    "#7762bb",
    "#c98943",
    "#5d84ad",
    "#2d8c69",
    "#a6afb9",
]

DONUT_COLORS = [
    "#4472c4",
    "#ed7d31",
    "#ffc000",
    "#70ad47",
    "#2bb3b1",
    "#e75b67",
    "#2f5597",
    "#a35d18",
    "#9b7214",
    "#2e8b57",
    "#b7c0ca",
]

ENVIRONMENT_CONTEXT_MEDIA = [
    {
        "file": "assets/ppt-insights/overview-1-2t-landscape-handling.png",
        "alt_zh": "北美住宅景观维护中的小型挖掘机作业",
        "alt_en": "Compact excavator working in North American residential landscaping",
        "title_zh": "住宅与景观维护",
        "title_en": "Residential and landscape work",
        "caption_zh": "人口迁移、住宅建设与庭院改造共同形成微小挖的持续需求。",
        "caption_en": "Population migration, housing construction and landscape renovation sustain compact-excavator demand.",
    },
    {
        "file": "assets/ppt-source/s049-picture-01.webp",
        "alt_zh": "挖掘机采用皮卡和14K拖车转运",
        "alt_en": "Excavator transported by pickup and 14K trailer",
        "title_zh": "皮卡与拖车转运",
        "title_en": "Pickup and trailer transport",
        "caption_zh": "整机重量、附件组合和拖车额定载荷直接影响交付与跨工地周转。",
        "caption_en": "Machine weight, attachment package and trailer rating directly affect delivery and jobsite mobility.",
    },
    {
        "file": "assets/ppt-source/s050-picture-01.webp",
        "alt_zh": "北美市政基础施工中的小型挖掘机",
        "alt_en": "Compact excavator on a North American municipal jobsite",
        "title_zh": "市政与基础施工",
        "title_en": "Municipal and infrastructure work",
        "caption_zh": "成熟市场更关注效率、操控、安全配置以及附件适配的综合表现。",
        "caption_en": "Mature markets emphasize the combined performance of productivity, control, safety equipment and attachment fit.",
    },
]

MACRO_FACTS = {
    3: [
        ("3.35亿", "335M", "2023年美国人口", "U.S. population in 2023"),
        ("1.2%", "1.2%", "加拿大人口增速", "Canadian population growth"),
        ("20亿+", "2B+", "YouTube月活跃用户", "YouTube monthly active users"),
    ],
    4: [
        ("本地研发", "Local R&D", "理解客户使用习惯", "Understand operator habits"),
        ("高端化", "Premium", "产品技术演进方向", "Product technology direction"),
        ("智能化 / 绿色化", "Smart / Green", "未来三年技术主线", "Three-year technology direction"),
    ],
    5: [
        ("约2%", "About 2%", "宏观经济长期趋势", "Long-term macro trend"),
        ("58万台", "580K units", "2023年美国工程机械市场", "2023 U.S. equipment market"),
        ("120.64亿美元", "$12.064B", "2023年设备租赁收入", "2023 equipment rental revenue"),
    ],
    6: [
        ("CORE", "CORE", "加州清洁非道路设备激励", "California clean off-road incentive"),
        ("RCRA / CERCLA", "RCRA / CERCLA", "危害材料合规边界", "Hazardous-material compliance"),
        ("高热 / 高寒", "Hot / Cold", "极端气候选装需求", "Extreme-climate package need"),
    ],
    7: [
        ("55%", "55%", "文中关税水平", "Tariff level stated in the analysis"),
        ("TCF", "TCF", "技术文件完整性要求", "Technical-file completeness"),
        ("准入与保供", "Access / Supply", "配置和供应链前置规划", "Forward product and supply planning"),
    ],
}

MACRO_FACTOR_LABELS = {
    3: ("01", "社会因素", "Social"),
    4: ("02", "技术因素", "Technology"),
    5: ("03", "经济因素", "Economy"),
    6: ("04", "环境因素", "Environment"),
    7: ("05", "政策因素", "Policy"),
}

TREND_HEADING_RE = re.compile(r"^现象\s*/?\s*趋势\d+\s*[：:]")
NUMBERED_LINE_RE = re.compile(r"^\d+\s*[、.]")
INLINE_LABEL_RE = re.compile(r"^([^：:]{1,28}[：:])(.*)$")


def format_percent(value, digits=0):
    if value is None:
        return "—"
    return f"{float(value) * 100:.{digits}f}%"


def chart_legend(series):
    items = []
    for index, item in enumerate(series):
        color = CHART_COLORS[index % len(CHART_COLORS)]
        items.append(
            f'<span class="nativeChartLegendItem" data-series-index="{index}" '
            'role="button" tabindex="0">'
            f'<i style="background:{color}"></i>{esc(item.get("name") or "—")}'
            "</span>"
        )
    return f'<div class="nativeChartLegend">{"".join(items)}</div>'


def render_stacked_area_chart(chart):
    categories = chart.get("categories") or []
    series = chart.get("series") or []
    width, height = 760, 330
    left, right, top, bottom = 58, 18, 18, 44
    plot_width = width - left - right
    plot_height = height - top - bottom
    step = plot_width / max(1, len(categories) - 1)
    xs = [left + index * step for index in range(len(categories))]
    grid = []
    for tick in range(0, 101, 20):
        y = top + (1 - tick / 100) * plot_height
        grid.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}"></line>'
            f'<text x="{left - 10}" y="{y + 4:.1f}" text-anchor="end">{tick}%</text>'
        )
    for index, category in enumerate(categories):
        grid.append(
            f'<text x="{xs[index]:.1f}" y="{height - 13}" text-anchor="middle">{esc(category)}</text>'
        )

    polygons = []
    labels = []
    cumulative = [0.0 for _ in categories]
    for series_index, item in enumerate(series):
        values = [float(value or 0) for value in (item.get("values") or [])]
        values += [0.0] * max(0, len(categories) - len(values))
        lower = list(cumulative)
        upper = [min(1.0, lower[index] + values[index]) for index in range(len(categories))]
        top_points = [
            f"{xs[index]:.1f},{top + (1 - upper[index]) * plot_height:.1f}"
            for index in range(len(categories))
        ]
        bottom_points = [
            f"{xs[index]:.1f},{top + (1 - lower[index]) * plot_height:.1f}"
            for index in reversed(range(len(categories)))
        ]
        color = CHART_COLORS[series_index % len(CHART_COLORS)]
        title = "；".join(
            f"{categories[index]} {format_percent(values[index])}"
            for index in range(len(categories))
        )
        polygons.append(
            f'<polygon class="nativeChartSeries nativeChartMark" data-series-index="{series_index}" '
            f'points="{" ".join(top_points + bottom_points)}" fill="{color}">'
            f"<title>{esc(item.get('name') or '—')}：{esc(title)}</title>"
            "</polygon>"
        )
        if series_index < 2:
            for index, value in enumerate(values[: len(categories)]):
                if value < 0.08:
                    continue
                middle = lower[index] + value / 2
                y = top + (1 - middle) * plot_height
                label_x = max(left + 16, min(width - right - 16, xs[index]))
                labels.append(
                    f'<text class="nativeChartValue" x="{label_x:.1f}" y="{y + 4:.1f}" '
                    f'text-anchor="middle">{format_percent(value)}</text>'
                )
        cumulative = upper

    return (
        f'<svg class="nativeChartSvg" viewBox="0 0 {width} {height}" '
        'role="img" aria-label="历年北美挖掘机品牌来源结构变化">'
        '<g class="nativeChartGrid">'
        + "".join(grid)
        + "</g>"
        + "".join(polygons)
        + "".join(labels)
        + "</svg>"
        + chart_legend(series)
    )


def render_bar_chart(chart):
    categories = chart.get("categories") or []
    series = (chart.get("series") or [{}])[0]
    values = [float(value or 0) for value in (series.get("values") or [])]
    width, height = 700, 330
    left, right, top, bottom = 58, 20, 22, 44
    plot_width = width - left - right
    plot_height = height - top - bottom
    slot = plot_width / max(1, len(categories))
    bar_width = min(68, slot * 0.52)
    elements = []
    for tick in range(0, 101, 20):
        y = top + (1 - tick / 100) * plot_height
        elements.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}"></line>'
            f'<text x="{left - 10}" y="{y + 4:.1f}" text-anchor="end">{tick}%</text>'
        )
    bars = []
    for index, category in enumerate(categories):
        value = values[index] if index < len(values) else 0
        x = left + index * slot + (slot - bar_width) / 2
        y = top + (1 - value) * plot_height
        bar_height = value * plot_height
        bars.append(
            f'<rect class="nativeChartBar nativeChartMark" data-point-index="{index}" '
            f'x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{bar_height:.1f}" '
            'rx="2" fill="#1766ae">'
            f"<title>{esc(category)}：{format_percent(value)}</title>"
            "</rect>"
            f'<text class="nativeChartBarValue" x="{x + bar_width / 2:.1f}" y="{max(16, y - 8):.1f}" '
            f'text-anchor="middle">{format_percent(value)}</text>'
            f'<text x="{x + bar_width / 2:.1f}" y="{height - 13}" '
            f'text-anchor="middle">{esc(category)}</text>'
        )
    return (
        f'<svg class="nativeChartSvg" viewBox="0 0 {width} {height}" '
        'role="img" aria-label="历年北美挖掘机行业CR4集中度变化">'
        f'<g class="nativeChartGrid">{"".join(elements)}</g>'
        + "".join(bars)
        + "</svg>"
    )


def render_donut_chart(chart, center_zh, center_en):
    categories = chart.get("categories") or []
    series = (chart.get("series") or [{}])[0]
    values = [max(0.0, float(value or 0)) for value in (series.get("values") or [])]
    total = sum(values) or 1.0
    segments = []
    legends = []
    current = 0.0
    for index, category in enumerate(categories):
        value = values[index] if index < len(values) else 0
        normalized = value / total
        start = min(100, current * 100)
        length = 100 - start if index == len(categories) - 1 else min(100 - start, normalized * 100)
        color = DONUT_COLORS[index % len(DONUT_COLORS)]
        segments.append(
            f'<circle class="nativeDonutSegment nativeChartMark" data-series-index="{index}" '
            'cx="120" cy="120" r="84" pathLength="100" fill="none" '
            f'stroke="{color}" stroke-width="52" stroke-dasharray="{length:.3f} {100 - length:.3f}" '
            f'stroke-dashoffset="{-start:.3f}">'
            f"<title>{esc(category)}：{format_percent(value, 1)}</title>"
            "</circle>"
        )
        current += normalized
        legends.append(
            f'<li data-series-index="{index}" role="button" tabindex="0">'
            f'<i style="background:{color}"></i><span>{esc(category)}</span>'
            f"<strong>{format_percent(value, 1)}</strong>"
            "</li>"
        )
    return (
        '<div class="nativeDonutLayout">'
        f'<div class="nativeDonut" role="img" aria-label="{esc(center_zh)}">'
        '<svg class="nativeDonutSvg" viewBox="0 0 240 240" aria-hidden="true">'
        '<circle class="nativeDonutTrack" cx="120" cy="120" r="84" pathLength="100" '
        'fill="none" stroke="#e4ebf1" stroke-width="52"></circle>'
        '<g transform="rotate(-90 120 120)">'
        f'{"".join(segments)}</g></svg>'
        '<div class="nativeDonutCenter">'
        f'<b data-en="{esc(center_en)}">{esc(center_zh)}</b><span>2021–2024</span>'
        "</div></div>"
        f'<ol class="nativeDonutLegend">{"".join(legends)}</ol>'
        "</div>"
    )


def render_competition_chart_slide(record, table_records):
    charts = [
        visual.get("chart_data")
        for visual in record.get("visuals", [])
        if visual.get("chart_data")
    ]
    if len(charts) != 4:
        return render_source_slide(record, table_records)
    tables = "".join(
        render_source_table(table_records[table_id])
        for table_id in record.get("table_ids", [])
        if table_id in table_records
    )
    notes = "".join(
        bilingual_leaf(item, "p", "sourceDataNote")
        for item in record.get("notes", [])
    )
    panels = [
        (
            "历年北美行业竞争格局",
            "Brand-origin Share Trend",
            render_stacked_area_chart(charts[0]),
            "本土品牌占比由2019年的63%降至2023年的55%，日系品牌由32%升至37%；欧美、韩系和中系品牌合计占比较低。",
            "North American brands declined from 63% in 2019 to 55% in 2023, while Japanese brands rose from 32% to 37%.",
        ),
        (
            "历年北美挖机行业CR4集中度变化",
            "Top-four Brand Concentration (CR4)",
            render_bar_chart(charts[1]),
            "前四大品牌合计份额从2019年的87%降至2022年的80%，2023年回升至82%，市场仍保持较高集中度。",
            "The combined share of the four largest brands moved from 87% in 2019 to 80% in 2022, then recovered to 82% in 2023.",
        ),
        (
            "2021-2024微小挖市场份额占比",
            "2021–2024 Compact Excavator Brand Share",
            render_donut_chart(charts[2], "微小挖", "Compact"),
            "久保田31.0%、卡特19.5%、迪尔16.2%、Bobcat 15.6%，前四品牌合计约82.4%。",
            "Kubota, CAT, Deere and Bobcat account for approximately 82.4% of the compact-excavator segment.",
        ),
        (
            "2021-2024中大挖市场份额占比",
            "2021–2024 Medium and Large Excavator Brand Share",
            render_donut_chart(charts[3], "中大挖", "Medium/Large"),
            "卡特36.6%、迪尔18.9%、小松17.9%，前三品牌合计约73.4%。",
            "CAT, Deere and Komatsu account for approximately 73.4% of the medium- and large-excavator segment.",
        ),
    ]
    panel_html = []
    for title_zh, title_en, chart_html, reading_zh, reading_en in panels:
        panel_html.append(
            '<section class="nativeChartPanel">'
            f'<h4 data-en="{esc(title_en)}">{esc(title_zh)}</h4>'
            f'<div class="nativeChartCanvas">{chart_html}</div>'
            f'<p class="nativeChartReading" data-en="{esc(reading_en)}">{esc(reading_zh)}</p>'
            "</section>"
        )
    return (
        f'<article class="sourceSlide sourceNativeChartSlide" data-source-slide="{record.get("slide")}">'
        '<header class="sourceSlideHeader">'
        f'{bilingual_leaf(record.get("title"), "h3")}'
        "</header>"
        + tables
        + f'<div class="nativeChartGrid">{"".join(panel_html)}</div>'
        + (f'<div class="sourceNotes">{notes}</div>' if notes else "")
        + "</article>"
    )


def render_environment_context_strip():
    figures = []
    for item in ENVIRONMENT_CONTEXT_MEDIA:
        figures.append(
            '<figure class="environmentContextFigure">'
            '<div class="environmentContextImage">'
            f'<img src="{esc(item["file"])}" '
            f'alt="{esc(item["alt_zh"])}" data-alt-en="{esc(item["alt_en"])}" loading="lazy">'
            "</div>"
            "<figcaption>"
            f'<strong data-en="{esc(item["title_en"])}">{esc(item["title_zh"])}</strong>'
            f'<span data-en="{esc(item["caption_en"])}">{esc(item["caption_zh"])}</span>'
            "</figcaption>"
            "</figure>"
        )
    return (
        '<section class="environmentContextStrip" aria-label="北美典型需求与使用边界">'
        '<header class="environmentContextHeader">'
        '<span data-en="Representative demand contexts">典型需求场景</span>'
        '<p data-en="Actual jobsites connect macro demand, customer expectations and machine configuration boundaries.">'
        "真实作业与运输方式把宏观需求、客户要求和产品配置边界连接起来。</p>"
        "</header>"
        f'<div class="environmentContextGrid">{"".join(figures)}</div>'
        "</section>"
    )


def split_source_lines(item):
    return [
        line.strip()
        for line in str((item or {}).get("zh") or "").splitlines()
        if line.strip()
    ]


def render_macro_line(line, class_name="macroBodyLine"):
    match = INLINE_LABEL_RE.match(line)
    if match:
        return (
            f'<p class="{class_name}">'
            f"<strong>{esc(match.group(1))}</strong>{esc(match.group(2))}"
            "</p>"
        )
    return f'<p class="{class_name}">{esc(line)}</p>'


def collect_macro_trends(items):
    groups = []
    current = None
    for item in items:
        for line in split_source_lines(item):
            if TREND_HEADING_RE.match(line):
                if current:
                    groups.append(current)
                current = {"title": line, "lines": []}
            else:
                if current is None:
                    current = {"title": "", "lines": []}
                current["lines"].append(line)
    if current:
        groups.append(current)
    return groups


def collect_macro_actions(items):
    actions = []
    current = None
    for item in items:
        for line in split_source_lines(item):
            if NUMBERED_LINE_RE.match(line):
                if current:
                    actions.append(current)
                current = [line]
            else:
                if current is None:
                    current = []
                current.append(line)
    if current:
        actions.append(current)
    return actions


def render_macro_facts(slide_number):
    facts = MACRO_FACTS.get(slide_number) or []
    if not facts:
        return ""
    items = []
    for value_zh, value_en, label_zh, label_en in facts:
        items.append(
            '<div class="macroFact">'
            f'<strong data-en="{esc(value_en)}">{esc(value_zh)}</strong>'
            f'<span data-en="{esc(label_en)}">{esc(label_zh)}</span>'
            "</div>"
        )
    return f'<div class="macroFactStrip">{"".join(items)}</div>'


def render_macro_slide(record, table_records):
    body = record.get("body") or []
    if len(body) < 3:
        return render_source_slide(record, table_records)
    slide_number = int(record.get("slide", 0))
    split_index = next(
        (
            index
            for index, item in enumerate(body[2:], start=2)
            if any(NUMBERED_LINE_RE.match(line) for line in split_source_lines(item))
        ),
        len(body),
    )
    trend_groups = collect_macro_trends(body[2:split_index])
    action_groups = collect_macro_actions(body[split_index:])
    trend_html = []
    for group in trend_groups:
        content_length = len(group["title"]) + sum(len(line) for line in group["lines"])
        wide_class = " macroTrendItemWide" if content_length > 360 else ""
        heading = (
            f'<h4>{esc(group["title"])}</h4>'
            if group["title"]
            else ""
        )
        paragraphs = "".join(render_macro_line(line) for line in group["lines"])
        trend_html.append(
            f'<section class="macroTrendItem{wide_class}">{heading}{paragraphs}</section>'
        )
    action_html = []
    for lines in action_groups:
        action_html.append(
            '<div class="macroActionItem">'
            + "".join(render_macro_line(line, "macroActionLine") for line in lines)
            + "</div>"
        )
    index_text, factor_zh, factor_en = MACRO_FACTOR_LABELS.get(
        slide_number,
        (f"{slide_number:02d}", "宏观因素", "Macro factor"),
    )
    notes = "".join(
        bilingual_leaf(item, "p", "sourceDataNote")
        for item in record.get("notes", [])
    )
    tables = "".join(
        render_source_table(table_records[table_id])
        for table_id in record.get("table_ids", [])
        if table_id in table_records
    )
    return (
        f'<article class="sourceSlide sourceMacroSlide" data-source-slide="{record.get("slide")}">'
        '<header class="sourceSlideHeader macroSlideHeader">'
        f'<span class="macroFactorIndex">{esc(index_text)}</span>'
        '<div>'
        f'<span class="macroFactorLabel" data-en="{esc(factor_en)}">{esc(factor_zh)}</span>'
        f'{bilingual_leaf(record.get("title"), "h3")}'
        "</div>"
        "</header>"
        + render_macro_facts(slide_number)
        + '<div class="macroNarrativeSection">'
        f'{bilingual_leaf(body[0], "h4", "macroSectionTitle")}'
        f'<div class="macroTrendGrid">{"".join(trend_html)}</div>'
        "</div>"
        + '<div class="macroImpactSection">'
        f'{bilingual_leaf(body[1], "h4", "macroSectionTitle macroImpactTitle")}'
        f'<div class="macroImpactGrid">{"".join(action_html)}</div>'
        "</div>"
        + render_source_visuals(record)
        + tables
        + (f'<div class="sourceNotes">{notes}</div>' if notes else "")
        + "</article>"
    )


def render_section(section, anchor, title_zh, title_en, records, table_records):
    selected = [record for record in records if record.get("section") == section]
    slides = []
    for record in selected:
        slide_number = int(record.get("slide", 0))
        display_record = record
        if slide_number == 11:
            display_record = {
                **record,
                "body": [
                    item
                    for item in (record.get("body") or [])
                    if str(item.get("zh") or "").strip() != "产品结构变化趋势"
                ],
                "visuals": [
                    {
                        **visual,
                        "chart_data": {
                            **(visual.get("chart_data") or {}),
                            "title": "产品结构变化趋势",
                        },
                    }
                    if visual.get("kind") == "chart"
                    else visual
                    for visual in (record.get("visuals") or [])
                ],
            }
        if slide_number == 15:
            axis_labels = {"微挖", "小挖", "中挖", "大挖"}
            display_record = {
                **record,
                "body": [
                    item
                    for item in (record.get("body") or [])
                    if str(item.get("zh") or "").strip() not in axis_labels
                ],
            }
        title = display_record.get("title") or {}
        cleaned_zh = str(title.get("zh") or "").lstrip("、，, ")
        if cleaned_zh != str(title.get("zh") or ""):
            display_record = {
                **display_record,
                "title": {**title, "zh": cleaned_zh},
            }
        if section == "environment" and 3 <= slide_number <= 7:
            slides.append(render_macro_slide(display_record, table_records))
        elif slide_number == 10:
            slides.append(render_competition_chart_slide(display_record, table_records))
        else:
            slides.append(render_source_slide(display_record, table_records))
    context_strip = render_environment_context_strip() if section == "environment" else ""
    return (
        f'<section id="{anchor}" class="sourceContentSection overviewSourceSection">'
        f'<h2 data-en="{esc(title_en)}">{esc(title_zh)}</h2>'
        f'<div class="sourceSlideStack">{context_strip}{"".join(slides)}</div>'
        "</section>"
    )


def build_page():
    source = load_ppt_source_content()
    tables = load_ppt_business_tables()["records"]
    records = [
        source["slides"][slide_id]
        for slide_id in source["overview"]
        if slide_id in source["slides"]
    ]
    sections = "".join(
        render_section(section, anchor, title_zh, title_en, records, tables)
        for section, anchor, title_zh, title_en in SECTION_META
    )
    nav = "".join(
        f'<a href="#{anchor}" data-en="{esc(title_en)}">{esc(title_zh)}</a>'
        for _, anchor, title_zh, title_en in SECTION_META
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="robots" content="noindex,nofollow">
  <title>北美挖掘机市场与产品洞察｜XCMG ARC</title>
  <link rel="icon" href="assets/xcmg-logo.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/dashboard.css?v=20260724k">
  <link rel="stylesheet" href="assets/excavator-market-overview-source.css?v=20260724d">
  <link rel="stylesheet" href="assets/site-credits.css?v=20260724a">
</head>
<body class="marketOverviewPage sourceOverviewPage">
<a class="backTop" href="#top" aria-label="回到页面顶部" data-en="Back to top">回到顶部</a>
<div class="layout" id="top">
  <aside class="nav">
    <a class="navBrand" href="arc.html" aria-label="返回全产品线竞品对标平台主页"><img src="assets/xcmg-logo.svg" alt="XCMG"></a>
    <div>
      <div class="navTitle" data-en="Excavator Category Insight">挖掘机总体洞察</div>
      <small>XCMG ARC INTERNAL</small>
    </div>
    <button class="languageToggle" type="button" aria-label="Switch to English">EN</button>
    <button class="sidebarToggle" type="button" aria-expanded="true" aria-controls="page-nav"><span>收起侧栏</span></button>
    <button class="navToggle" type="button" aria-expanded="false" aria-controls="page-nav" data-en="Page navigation">页面导航</button>
    <a class="mobileTop" href="#top" data-en="Top">顶部</a>
    <div class="navMenu" id="page-nav">
      <a class="home" href="arc.html" data-en="Return to benchmark platform">返回对标平台主页</a>
      <a href="#overview" data-en="Excavator overview">挖掘机总览</a>
      {nav}
    </div>
  </aside>
  <main>
    <div class="hero sourceOverviewHero" id="overview">
      <div class="heroText">
        <span class="eyebrow" data-en="North America Excavator Product Line">北美挖掘机产品线</span>
        <h1 data-en="North American Excavator Market and Product Insight">北美挖掘机市场与产品洞察</h1>
        <div class="actions">
          <a class="btn blue" href="#environment" data-en="Market environment">市场环境</a>
          <a class="btn yellow" href="#competition" data-en="Competitive landscape">竞争格局</a>
          <a class="btn" href="#portfolio" data-en="Product portfolio">产品型谱</a>
        </div>
      </div>
      <div class="heroMedia"><img src="assets/arc/xe55u-official-cropped.jpg" alt="XCMG XE55U 挖掘机完整产品图"></div>
    </div>
    {sections}
    <div class="siteCredits" aria-label="项目署名">
      <span data-en="Executive Sponsor: Zhang Shengnan">指导领导：张盛楠</span>
      <span data-en="Data Visualization: Liu Chang">数据可视化：刘畅</span>
      <span data-en="Data Source: ARC Product Team">数据来源：ARC产品小组</span>
      <span><span data-en="Issue Reporting:">问题提报：</span> <a href="mailto:changl@xcmgarc.com">changl@xcmgarc.com</a></span>
    </div>
  </main>
</div>
<script src="assets/dashboard.js?v=20260724k"></script>
<script src="assets/excavator-market-overview-navigation.js?v=20260724a"></script>
<script src="assets/i18n.js?v=20260723e"></script>
</body>
</html>
"""


def main():
    output = ROOT / "excavator-market-overview.html"
    page = build_page()
    clean_page = "\n".join(line.rstrip() for line in page.splitlines()) + "\n"
    output.write_text(clean_page, encoding="utf-8", newline="\n")
    print(output)


if __name__ == "__main__":
    main()
