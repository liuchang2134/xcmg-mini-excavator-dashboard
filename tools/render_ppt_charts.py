"""Render extracted PowerPoint chart data as responsive, accessible SVG."""

from __future__ import annotations

import html
import math
import re


COLORS = [
    "#075da8",
    "#4f86b5",
    "#8ba3ba",
    "#128152",
    "#f5b400",
    "#d95757",
    "#6f58b6",
    "#1aa3a8",
    "#a76f25",
    "#405c75",
    "#91a35c",
]

BRAND_COLORS = {
    "XCMG": "#f5b400",
    "徐工": "#f5b400",
    "KUBOTA": "#e56f21",
    "久保田": "#e56f21",
    "DEERE": "#2f7d32",
    "迪尔": "#2f7d32",
    "JOHN DEERE": "#2f7d32",
    "BOBCAT": "#6f8294",
    "山猫": "#6f8294",
    "CAT": "#252b31",
    "CATERPILLAR": "#252b31",
    "卡特": "#252b31",
    "SANY": "#d64c4c",
    "三一": "#d64c4c",
    "KOMATSU": "#2c72b8",
    "小松": "#2c72b8",
    "VOLVO": "#557c9f",
    "沃尔沃": "#557c9f",
    "HYUNDAI": "#cf7c27",
    "现代": "#cf7c27",
    "DOOSAN": "#d45a3a",
    "斗山": "#d45a3a",
}

TEXT_EN = {
    "微挖": "Micro",
    "小挖": "Small",
    "中挖": "Medium",
    "大挖": "Large",
    "整机参数": "Machine package",
    "性能配置": "Performance and equipment",
    "安全性": "Safety",
    "环境适应性": "Environmental adaptability",
    "操控性": "Controllability",
    "维修性": "Serviceability",
    "经济性": "Operating economy",
    "外观细节": "Fit and finish",
    "软文资料": "Documentation",
    "单价 万美元": "Unit price (USD 10k)",
    "占有率": "Market share",
    "经销商售价": "Dealer price (USD)",
    "竞争力": "Competitiveness",
    "同比增长": "Year-over-year change",
    "2026预测": "2026 forecast",
    "2025E": "2025 estimate",
}


def esc(value):
    return html.escape(str(value or ""), quote=True)


def clean_series(chart):
    return [
        item
        for item in (chart.get("series") or [])
        if item.get("name") or any(value is not None for value in (item.get("values") or []))
    ]


def english_text(value):
    value = str(value or "").strip()
    if value in TEXT_EN:
        return TEXT_EN[value]
    match = re.fullmatch(r">?(\d+)-(\d+)", value)
    if match:
        return f"{match.group(1)}-{match.group(2)} t"
    if value.endswith("预测"):
        return value[:-2] + " forecast"
    return value


def english_title(value):
    value = str(value or "").strip()
    tonnage = re.search(r"(\d+(?:~|-)\d+吨(?:级)?)", value)
    tonnage_en = tonnage.group(1).replace("~", "-").replace("吨级", " t").replace("吨", " t") if tonnage else ""
    year = re.search(r"(20\d{2})年", value)
    if "行业趋势" in value:
        return "Industry Analysis - Market Trend"
    if "竞争格局" in value:
        prefix = f"{year.group(1)} " if year else ""
        return f"{prefix}Industry Analysis - Competitive Landscape".strip()
    if "市场规模" in value:
        return "Excavator market volume"
    if "履带液压挖掘机" in value and "同比" in value:
        return "Crawler excavator volume and year-over-year change"
    if "产品近年销量" in value or "产品销量" in value:
        return f"{tonnage_en} product volume trend and forecast".strip()
    if "市场竞争格局" in value or "产品竞争格局" in value:
        prefix = f"{year.group(1)} " if year else ""
        return f"{prefix}{tonnage_en} market landscape".strip()
    if "产品竞争力分析" in value:
        return f"{tonnage_en} product competitiveness".strip()
    if "定位" in value:
        return f"{tonnage_en} product positioning".strip()
    if "产品结构" in value:
        return "Excavator size-class structure"
    return value


def bilingual_text(x, y, zh, en=None, **attrs):
    attributes = " ".join(
        f'{"class" if key == "class_" else key.replace("_", "-")}="{esc(value)}"'
        for key, value in attrs.items()
    )
    if attributes:
        attributes = " " + attributes
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" data-en="{esc(en or english_text(zh))}"'
        f"{attributes}>{esc(zh)}</text>"
    )


def fmt_number(value):
    if value is None:
        return "—"
    value = float(value)
    if abs(value) >= 1000:
        return f"{value:,.0f}"
    if abs(value) >= 100:
        return f"{value:.0f}"
    if abs(value) >= 10:
        return f"{value:.1f}".rstrip("0").rstrip(".")
    return f"{value:.2f}".rstrip("0").rstrip(".")


def fmt_percent(value, digits=1):
    if value is None:
        return "—"
    return f"{float(value) * 100:.{digits}f}%"


def nice_ceiling(value):
    value = max(1.0, float(value))
    magnitude = 10 ** math.floor(math.log10(value))
    normalized = value / magnitude
    step = 1 if normalized <= 1 else 2 if normalized <= 2 else 5 if normalized <= 5 else 10
    return step * magnitude


def series_color(name, index):
    normalized = str(name or "").strip().upper()
    for brand, color in BRAND_COLORS.items():
        if brand.upper() in normalized:
            return color
    return COLORS[index % len(COLORS)]


def legend(series, line_name=None):
    only_name = str(series[0].get("name") or "").strip().lower() if len(series) == 1 else ""
    if (
        len(series) == 1
        and only_name in {"", "series 1", "series1", "系列1", "系列 1"}
    ):
        return ""
    items = []
    for index, item in enumerate(series):
        name = str(item.get("name") or f"Series {index + 1}")
        line_class = " sourceChartLegendLine" if name == line_name else ""
        items.append(
            f'<span class="sourceChartLegendItem{line_class}">'
            f'<i style="--series-color:{series_color(name, index)}"></i>'
            f'<b data-en="{esc(english_text(name))}">{esc(name)}</b>'
            "</span>"
        )
    return f'<div class="sourceChartLegend">{"".join(items)}</div>'


def chart_shell(chart, svg, *, dense=False, legend_html=""):
    title = chart.get("title") or "数据图表"
    density = "dense" if dense else "standard"
    return (
        f'<figure class="sourceVisual sourceVisual-chart sourceDataChart" '
        f'data-chart-density="{density}" data-chart-type="{esc(chart.get("type"))}">'
        f'<figcaption data-en="{esc(english_title(title))}">{esc(title)}</figcaption>'
        f'<div class="sourceChartViewport">{svg}</div>'
        f"{legend_html}"
        "</figure>"
    )


def render_clustered(chart):
    categories = chart.get("categories") or []
    series = clean_series(chart)
    if not categories or not series:
        return ""
    line_series = next(
        (item for item in series if "同比" in str(item.get("name") or "") or "growth" in str(item.get("name") or "").lower()),
        None,
    )
    bars = [item for item in series if item is not line_series]
    count = len(categories)
    dense = count > 10
    width = max(920, count * (76 if dense else 120))
    height = 500
    left, right, top, bottom = 78, (86 if line_series else 26), 30, 82
    plot_width = width - left - right
    plot_height = height - top - bottom
    max_value = max(
        (float(value or 0) for item in bars for value in (item.get("values") or [])),
        default=1,
    )
    y_max = nice_ceiling(max_value * 1.08)
    grid = []
    for index in range(6):
        value = y_max * index / 5
        y = top + plot_height - (value / y_max) * plot_height
        grid.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}"></line>')
        grid.append(bilingual_text(left - 10, y + 4, fmt_number(value), text_anchor="end"))
    slot = plot_width / max(1, count)
    group_width = min(slot * 0.72, 78)
    bar_width = group_width / max(1, len(bars))
    marks = []
    labels = []
    direct_values = count <= 8 and len(bars) <= 2
    for category_index, category in enumerate(categories):
        center = left + slot * (category_index + 0.5)
        category_zh = re.sub(r"^>", "", str(category)).replace("-", "–")
        if re.fullmatch(r"\d+–\d+", category_zh):
            category_zh += "吨"
        labels.append(
            bilingual_text(
                center,
                height - 30,
                category_zh,
                english_text(str(category)),
                text_anchor="middle",
                class_="sourceChartCategory",
            )
        )
        for series_index, item in enumerate(bars):
            values = item.get("values") or []
            value = float(values[category_index] or 0) if category_index < len(values) else 0
            x = center - group_width / 2 + series_index * bar_width
            y = top + plot_height - (value / y_max) * plot_height
            bar_height = max(0, top + plot_height - y)
            color = series_color(item.get("name"), series_index)
            tooltip = f"{item.get('name') or ''} {category}: {fmt_number(value)}"
            marks.append(
                f'<rect class="sourceChartMark" data-series-index="{series.index(item)}" '
                f'data-point-index="{category_index}" x="{x:.1f}" y="{y:.1f}" '
                f'width="{max(3, bar_width - 3):.1f}" height="{bar_height:.1f}" '
                f'fill="{color}"><title>{esc(tooltip)}</title></rect>'
            )
            if direct_values and value:
                marks.append(
                    bilingual_text(
                        x + max(3, bar_width - 3) / 2,
                        max(16, y - 7),
                        fmt_number(value),
                        text_anchor="middle",
                        class_="sourceChartValue",
                    )
                )
    if line_series:
        values = [float(value or 0) for value in (line_series.get("values") or [])]
        values += [0.0] * max(0, count - len(values))
        line_min = min(-0.1, math.floor(min(values[:count]) * 10) / 10)
        line_max = max(0.0, math.ceil(max(values[:count]) * 10) / 10)
        line_span = max(0.1, line_max - line_min)
        points = []
        line_color = series_color(line_series.get("name"), len(bars))
        for index, value in enumerate(values[:count]):
            x = left + slot * (index + 0.5)
            y = top + (line_max - value) / line_span * plot_height
            points.append(f"{x:.1f},{y:.1f}")
            marks.append(
                f'<circle class="sourceChartPoint" data-series-index="{series.index(line_series)}" '
                f'data-point-index="{index}" cx="{x:.1f}" cy="{y:.1f}" r="5" '
                f'fill="{line_color}"><title>{esc(categories[index])}: {fmt_percent(value)}</title></circle>'
            )
            marks.append(
                bilingual_text(
                    x,
                    min(height - bottom + 18, max(top + 12, y - 9)),
                    fmt_percent(value, 0),
                    text_anchor="middle",
                    class_="sourceChartGrowthValue",
                )
            )
        marks.insert(
            0,
            f'<polyline class="sourceChartLine" points="{" ".join(points)}" '
            f'stroke="{line_color}"></polyline>',
        )
        for tick_index in range(4):
            value = line_max - line_span * tick_index / 3
            y = top + tick_index / 3 * plot_height
            grid.append(
                bilingual_text(
                    width - right + 10,
                    y + 4,
                    fmt_percent(value, 0),
                    text_anchor="start",
                    class_="sourceChartSecondaryAxis",
                )
            )
    svg = (
        f'<svg class="sourceChartSvg" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="{esc(chart.get("title") or "数据图表")}">'
        f'<g class="sourceChartGrid">{"".join(grid)}</g>'
        f'<g class="sourceChartMarks">{"".join(marks)}</g>'
        f'<g class="sourceChartLabels">{"".join(labels)}</g>'
        "</svg>"
    )
    return chart_shell(
        chart,
        svg,
        dense=dense,
        legend_html=legend(series, line_series.get("name") if line_series else None),
    )


def render_stacked(chart, normalized=False, area=False):
    categories = chart.get("categories") or []
    series = clean_series(chart)
    if not categories or not series:
        return ""
    count = len(categories)
    width, height = max(920, count * 130), 500
    left, right, top, bottom = 72, 28, 30, 72
    plot_width = width - left - right
    plot_height = height - top - bottom
    raw_totals = []
    for index in range(count):
        total = 0.0
        for item in series:
            values = item.get("values") or []
            total += float(values[index] or 0) if index < len(values) else 0.0
        raw_totals.append(total)
    y_max = 1.0 if normalized else nice_ceiling(max(raw_totals, default=1) * 1.08)
    grid = []
    for index in range(6):
        value = y_max * index / 5
        y = top + plot_height - index / 5 * plot_height
        label = fmt_percent(value, 0) if normalized else fmt_number(value)
        grid.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}"></line>')
        grid.append(bilingual_text(left - 10, y + 4, label, text_anchor="end"))
    slot = plot_width / max(1, count)
    marks = []
    labels = []
    if area:
        xs = [left + slot * (index + 0.5) for index in range(count)]
        cumulative = [0.0] * count
        for series_index, item in enumerate(series):
            values = [
                float(value or 0)
                for value in (item.get("values") or [])
            ] + [0.0] * count
            lower = list(cumulative)
            upper = [
                lower[index] + values[index] / max(raw_totals[index], 1e-9)
                for index in range(count)
            ]
            top_points = [
                f"{xs[index]:.1f},{top + (1 - upper[index]) * plot_height:.1f}"
                for index in range(count)
            ]
            bottom_points = [
                f"{xs[index]:.1f},{top + (1 - lower[index]) * plot_height:.1f}"
                for index in reversed(range(count))
            ]
            marks.append(
                f'<polygon class="sourceChartArea sourceChartSeries" '
                f'data-series-index="{series_index}" '
                f'points="{" ".join(top_points + bottom_points)}" '
                f'fill="{series_color(item.get("name"), series_index)}">'
                f'<title>{esc(item.get("name") or "")}</title></polygon>'
            )
            cumulative = upper
    else:
        bar_width = min(82, slot * 0.64)
        for category_index, category in enumerate(categories):
            center = left + slot * (category_index + 0.5)
            cumulative = 0.0
            total = raw_totals[category_index]
            for series_index, item in enumerate(series):
                values = item.get("values") or []
                raw_value = float(values[category_index] or 0) if category_index < len(values) else 0
                value = raw_value / max(total, 1e-9) if normalized else raw_value
                segment_height = value / y_max * plot_height
                y = top + plot_height - (cumulative + value) / y_max * plot_height
                color = series_color(item.get("name"), series_index)
                marks.append(
                    f'<rect class="sourceChartMark sourceChartSeries" '
                    f'data-series-index="{series_index}" data-point-index="{category_index}" '
                    f'x="{center - bar_width / 2:.1f}" y="{y:.1f}" width="{bar_width:.1f}" '
                    f'height="{max(0, segment_height):.1f}" fill="{color}">'
                    f'<title>{esc(item.get("name") or "")} {esc(category)}: '
                    f'{esc(fmt_percent(raw_value) if normalized else fmt_number(raw_value))}</title></rect>'
                )
                if value / y_max >= 0.085:
                    label = fmt_percent(raw_value, 0) if normalized else fmt_number(raw_value)
                    marks.append(
                        bilingual_text(
                            center,
                            y + segment_height / 2 + 4,
                            label,
                            text_anchor="middle",
                            class_="sourceChartSegmentValue",
                        )
                    )
                cumulative += value
            if not normalized:
                marks.append(
                    bilingual_text(
                        center,
                        max(18, top + plot_height - total / y_max * plot_height - 9),
                        fmt_number(total),
                        text_anchor="middle",
                        class_="sourceChartTotal",
                    )
                )
    for index, category in enumerate(categories):
        x = left + slot * (index + 0.5)
        labels.append(
            bilingual_text(
                x,
                height - 28,
                str(category),
                english_text(category),
                text_anchor="middle",
                class_="sourceChartCategory",
            )
        )
    svg = (
        f'<svg class="sourceChartSvg" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="{esc(chart.get("title") or "数据图表")}">'
        f'<g class="sourceChartGrid">{"".join(grid)}</g>'
        f'<g class="sourceChartMarks">{"".join(marks)}</g>'
        f'<g class="sourceChartLabels">{"".join(labels)}</g>'
        "</svg>"
    )
    return chart_shell(chart, svg, legend_html=legend(series))


def render_radar(chart):
    categories = chart.get("categories") or []
    series = clean_series(chart)
    if len(categories) < 3 or not series:
        return ""
    width, height = 920, 520
    cx, cy, radius = 460, 245, 174
    max_value = max(
        (float(value or 0) for item in series for value in (item.get("values") or [])),
        default=5,
    )
    scale_max = max(5, math.ceil(max_value))
    grid = []
    for ring in range(1, 6):
        current_radius = radius * ring / 5
        points = []
        for index in range(len(categories)):
            angle = -math.pi / 2 + index * 2 * math.pi / len(categories)
            points.append(
                f"{cx + math.cos(angle) * current_radius:.1f},"
                f"{cy + math.sin(angle) * current_radius:.1f}"
            )
        grid.append(f'<polygon points="{" ".join(points)}"></polygon>')
    labels = []
    for index, category in enumerate(categories):
        angle = -math.pi / 2 + index * 2 * math.pi / len(categories)
        x2, y2 = cx + math.cos(angle) * radius, cy + math.sin(angle) * radius
        grid.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}"></line>')
        label_radius = radius + 42
        lx = cx + math.cos(angle) * label_radius
        ly = cy + math.sin(angle) * label_radius
        anchor = "middle" if abs(math.cos(angle)) < 0.3 else ("start" if math.cos(angle) > 0 else "end")
        labels.append(
            bilingual_text(
                lx,
                ly + 4,
                str(category),
                english_text(category),
                text_anchor=anchor,
                class_="sourceChartRadarLabel",
            )
        )
    marks = []
    for series_index, item in enumerate(series):
        values = list(item.get("values") or []) + [0] * len(categories)
        points = []
        point_marks = []
        for index, category in enumerate(categories):
            value = float(values[index] or 0)
            angle = -math.pi / 2 + index * 2 * math.pi / len(categories)
            scaled = radius * max(0, min(scale_max, value)) / scale_max
            x = cx + math.cos(angle) * scaled
            y = cy + math.sin(angle) * scaled
            points.append(f"{x:.1f},{y:.1f}")
            point_marks.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.8">'
                f'<title>{esc(item.get("name") or "")} · {esc(category)}: {fmt_number(value)}</title>'
                "</circle>"
            )
        color = series_color(item.get("name"), series_index)
        marks.append(
            f'<g class="sourceChartSeries" data-series-index="{series_index}" '
            f'style="--series-color:{color}">'
            f'<polygon points="{" ".join(points)}"></polygon>'
            f'{"".join(point_marks)}</g>'
        )
    svg = (
        f'<svg class="sourceChartSvg sourceRadarSvg" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="{esc(chart.get("title") or "产品竞争力雷达图")}">'
        f'<g class="sourceChartRadarGrid">{"".join(grid)}</g>'
        f'<g class="sourceChartMarks">{"".join(marks)}</g>'
        f'<g class="sourceChartLabels">{"".join(labels)}</g>'
        "</svg>"
    )
    return chart_shell(chart, svg, legend_html=legend(series))


def render_bubble(chart):
    series = [
        item
        for item in clean_series(chart)
        if item.get("x_values") and item.get("values") and item.get("bubble_sizes")
    ]
    if not series:
        return ""
    points = []
    for index, item in enumerate(series):
        points.append(
            {
                "name": str(item.get("name") or f"Series {index + 1}"),
                "series_index": index,
                "x": float(item["x_values"][0]),
                "y": float(item["values"][0]),
                "size": float(item["bubble_sizes"][0]),
                "color": series_color(item.get("name"), index),
            }
        )
    axis_titles = chart.get("axis_titles") or []
    x_title = axis_titles[0] if axis_titles else "横轴"
    y_title = axis_titles[1] if len(axis_titles) > 1 else "纵轴"
    percent_y = "占有率" in y_title or max(point["y"] for point in points) <= 1
    width, height = 980, 520
    left, right, top, bottom = 86, 54, 34, 82
    plot_width = width - left - right
    plot_height = height - top - bottom
    x_values = [point["x"] for point in points]
    y_values = [point["y"] for point in points]
    x_span = max(1e-9, max(x_values) - min(x_values))
    y_span = max(1e-9, max(y_values) - min(y_values))
    x_min = max(0, min(x_values) - x_span * 0.18)
    x_max = max(x_values) + x_span * 0.18
    if percent_y:
        y_min = 0
        y_max = max(0.1, math.ceil(max(y_values) * 20) / 20)
    else:
        y_min = math.floor(min(y_values) - max(1, y_span * 0.25))
        y_max = math.ceil(max(y_values) + max(1, y_span * 0.25))
    size_values = [max(0, point["size"]) for point in points]
    min_size, max_size = min(size_values), max(size_values)
    size_span = max(1e-9, max_size - min_size)
    grid = []
    for index in range(6):
        x_value = x_min + (x_max - x_min) * index / 5
        x = left + plot_width * index / 5
        grid.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top + plot_height}"></line>')
        grid.append(
            bilingual_text(
                x,
                height - 46,
                fmt_number(x_value),
                text_anchor="middle",
                class_="sourceChartAxisValue",
            )
        )
    for index in range(6):
        y_value = y_min + (y_max - y_min) * index / 5
        y = top + plot_height - plot_height * index / 5
        grid.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_width}" y2="{y:.1f}"></line>')
        label = fmt_percent(y_value, 0) if percent_y else fmt_number(y_value)
        grid.append(
            bilingual_text(
                left - 10,
                y + 4,
                label,
                text_anchor="end",
                class_="sourceChartAxisValue",
            )
        )
    plotted = []
    for point in points:
        x = left + (point["x"] - x_min) / max(1e-9, x_max - x_min) * plot_width
        y = top + (y_max - point["y"]) / max(1e-9, y_max - y_min) * plot_height
        radius = 12 + math.sqrt((point["size"] - min_size) / size_span) * 24 if size_span else 24
        anchor = "end" if x > left + plot_width * 0.66 else "start"
        plotted.append(
            {
                **point,
                "px": x,
                "py": y,
                "radius": radius,
                "anchor": anchor,
                "label_y": max(top + 14, min(top + plot_height - 20, y - 3)),
            }
        )

    # Keep labels for nearby products apart while preserving their chart side.
    for anchor in ("start", "end"):
        side = sorted(
            (point for point in plotted if point["anchor"] == anchor),
            key=lambda point: point["label_y"],
        )
        if not side:
            continue
        minimum_y = top + 14
        maximum_y = top + plot_height - 20
        gap = 32
        for index, point in enumerate(side):
            floor = minimum_y if index == 0 else side[index - 1]["label_y"] + gap
            point["label_y"] = max(point["label_y"], floor)
        overflow = side[-1]["label_y"] - maximum_y
        if overflow > 0:
            for point in side:
                point["label_y"] -= overflow
        for index in range(len(side) - 2, -1, -1):
            side[index]["label_y"] = min(
                side[index]["label_y"],
                side[index + 1]["label_y"] - gap,
            )

    marks = []
    for point in plotted:
        x = point["px"]
        y = point["py"]
        radius = point["radius"]
        anchor = point["anchor"]
        label_x = x - radius - 12 if anchor == "end" else x + radius + 12
        label_y = point["label_y"]
        tooltip_y = fmt_percent(point["y"]) if percent_y else fmt_number(point["y"])
        line_end_x = label_x + 4 if anchor == "end" else label_x - 4
        marks.append(
            f'<g class="sourceChartSeries sourceChartBubble" '
            f'data-series-index="{point["series_index"]}" style="--series-color:{point["color"]}">'
            f'<line class="sourceChartLeader" x1="{x:.1f}" y1="{y:.1f}" '
            f'x2="{line_end_x:.1f}" y2="{label_y - 4:.1f}"></line>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}">'
            f'<title>{esc(point["name"])} · {esc(x_title)} {fmt_number(point["x"])} · '
            f'{esc(y_title)} {tooltip_y} · {fmt_number(point["size"])}</title></circle>'
            + bilingual_text(
                label_x,
                label_y,
                point["name"],
                english_text(point["name"]),
                text_anchor=anchor,
                class_="sourceChartBubbleLabel",
            )
            + bilingual_text(
                label_x,
                label_y + 15,
                tooltip_y,
                text_anchor=anchor,
                class_="sourceChartBubbleValue",
            )
            + "</g>"
        )
    axis_labels = [
        bilingual_text(
            left + plot_width / 2,
            height - 12,
            x_title,
            english_text(x_title),
            text_anchor="middle",
            class_="sourceChartAxisTitle",
        ),
        (
            f'<text class="sourceChartAxisTitle" x="18" y="{top + plot_height / 2:.1f}" '
            f'transform="rotate(-90 18 {top + plot_height / 2:.1f})" '
            f'text-anchor="middle" data-en="{esc(english_text(y_title))}">{esc(y_title)}</text>'
        ),
    ]
    svg = (
        f'<svg class="sourceChartSvg sourceBubbleSvg" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="{esc(chart.get("title") or "竞争格局气泡图")}">'
        f'<g class="sourceChartGrid">{"".join(grid)}</g>'
        f'<g class="sourceChartMarks">{"".join(marks)}</g>'
        f'<g class="sourceChartLabels">{"".join(axis_labels)}</g>'
        "</svg>"
    )
    return chart_shell(chart, svg)


def render_donut(chart):
    categories = chart.get("categories") or []
    series = clean_series(chart)
    if not categories or not series:
        return ""
    values = [float(value or 0) for value in (series[0].get("values") or [])]
    total = sum(values) or 1
    cx, cy, radius, stroke_width = 280, 230, 150, 68
    circumference = 2 * math.pi * radius
    offset = 0.0
    arcs = []
    for index, category in enumerate(categories):
        value = values[index] if index < len(values) else 0
        length = circumference * value / total
        arcs.append(
            f'<circle class="sourceChartDonutArc" cx="{cx}" cy="{cy}" r="{radius}" '
            f'data-series-index="{index}" '
            f'stroke="{series_color(category, index)}" stroke-width="{stroke_width}" '
            f'stroke-dasharray="{length:.2f} {circumference - length:.2f}" '
            f'stroke-dashoffset="{-offset:.2f}">'
            f'<title>{esc(category)}: {fmt_percent(value / total)}</title></circle>'
        )
        offset += length
    svg = (
        '<svg class="sourceChartSvg sourceDonutSvg" viewBox="0 0 560 460" '
        f'role="img" aria-label="{esc(chart.get("title") or "份额结构")}">'
        '<g transform="rotate(-90 280 230)">'
        f'{"".join(arcs)}</g>'
        f'<text x="{cx}" y="{cy - 2}" text-anchor="middle" class="sourceChartDonutTotal">100%</text>'
        f'<text x="{cx}" y="{cy + 22}" text-anchor="middle" class="sourceChartDonutLabel">TOTAL</text>'
        "</svg>"
    )
    legend_series = [
        {"name": category, "values": [values[index] if index < len(values) else 0]}
        for index, category in enumerate(categories)
    ]
    return chart_shell(chart, svg, legend_html=legend(legend_series))


def render_chart_figure(visual, fallback_title=""):
    chart = dict(visual.get("chart_data") or {})
    if not str(chart.get("title") or "").strip() and fallback_title:
        chart["title"] = fallback_title
    chart_type = str(chart.get("type") or "")
    if "RADAR" in chart_type:
        return render_radar(chart)
    if "BUBBLE" in chart_type:
        return render_bubble(chart)
    if "PIE" in chart_type:
        return render_donut(chart)
    if "AREA_STACKED_100" in chart_type:
        return render_stacked(chart, normalized=True, area=True)
    if "COLUMN_STACKED_100" in chart_type:
        return render_stacked(chart, normalized=True)
    if "COLUMN_STACKED" in chart_type:
        return render_stacked(chart)
    if "COLUMN_CLUSTERED" in chart_type:
        return render_clustered(chart)
    return ""
