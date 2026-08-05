from __future__ import annotations

import html
import math
from pathlib import Path
from typing import Any

try:
    from .crane_data import load_crane_workbook
    from .crane_scoring import CATEGORY_WEIGHTS, CONDITIONS, metric_direction, score_sheet
except ImportError:
    from crane_data import load_crane_workbook
    from crane_scoring import CATEGORY_WEIGHTS, CONDITIONS, metric_direction, score_sheet


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DOWNLOAD = "data/source-excel/XCMG_crane_benchmark_data_pool.xlsx"

PAGE_DEFINITIONS = {
    "RT-60t": {
        "output": "crane-rt-60t.html",
        "image": "assets/arc/cranes/xcr60u-official.jpg",
        "image_alt": "XCMG XCR60U rough-terrain crane",
        "official": True,
    },
    "RT-75t": {
        "output": "crane-rt-75t.html",
        "image": "assets/arc/cranes/xcr75u-official.jpg",
        "image_alt": "XCMG XCR75U rough-terrain crane",
        "official": True,
    },
    "RT-100t": {
        "output": "crane-rt-100t.html",
        "image": "assets/arc/cranes/xcr100u-official.jpg",
        "image_alt": "XCMG XCR100U rough-terrain crane",
        "official": True,
    },
    "RT-130t": {
        "output": "crane-rt-130t.html",
        "image": "assets/arc/cranes/xcr130u-official.jpg",
        "image_alt": "XCMG XCR130U rough-terrain crane",
        "official": True,
    },
    "RT-160t": {
        "output": "crane-rt-160t.html",
        "image": "assets/arc/category-cranes.webp",
        "image_alt": "XCMG crane product-line image",
        "official": False,
    },
    "AT-150t": {
        "output": "crane-at-150t.html",
        "image": "assets/arc/cranes/xca150u-official.jpg",
        "image_alt": "XCMG XCA150U all-terrain crane",
        "official": True,
    },
}

CATEGORY_NAMES = {
    "Transport Parameters": ("运输参数", "Transport Parameters"),
    "Ground Parameters": ("底盘与机动参数", "Chassis and Mobility"),
    "Boom and jib": ("主臂与副臂", "Boom and Jib"),
    "Outriggers": ("支腿系统", "Outriggers"),
    "Power": ("动力系统", "Powertrain"),
    "Winches": ("卷扬系统", "Winches"),
    "Lifting performance": ("起重性能", "Lifting Performance"),
    "Speeds": ("作业速度", "Operating Speeds"),
}

METRIC_ZH = {
    "Minimum transport weight": "最小运输重量",
    "Transport Width": "运输宽度",
    "Transport Height": "运输高度",
    "Transport Length": "运输长度",
    "Removable CWT": "可拆卸配重",
    "Number of CWT configurations": "配重组合数量",
    "Speed": "最高行驶速度",
    "Speed with max CWT": "最大配重行驶速度",
    "Wheelbase": "轴距",
    "Tire size": "轮胎规格",
    "Number of steering modes": "转向模式数量",
    "Minimum turning radius": "最小转弯半径",
    "Gradability": "最大爬坡度",
    "Front approach angle": "前接近角",
    "Rear approach angle": "后离去角",
    "Retracted Boom Length": "主臂基本臂长度",
    "Extended Boom Length": "主臂全伸长度",
    "Max jib carried on crane": "随车携带最大副臂长度",
    "Jib extensions": "副臂延伸节数量",
    "Jib offset angles": "副臂变角范围",
    "Luffing jib": "塔式副臂",
    "Tail swing radius": "尾部回转半径",
    "Cab tilt": "驾驶室俯仰角",
    "Outrigger penetration": "支腿穿透量",
    "Full outrigger extension": "支腿全伸跨度",
    "Number of outrigger extensions": "支腿伸缩档位数量",
    "Asymmetric outrigger operation": "非对称支腿作业",
    "Engine": "发动机型号",
    "Engine Power": "发动机功率",
    "Engine Torque": "发动机扭矩",
    "Fuel tank": "燃油箱容量",
    "Transmission": "变速箱",
    "Forward speeds": "前进挡位数量",
    "Reverse speeds": "倒退挡位数量",
    "Interaxle lock": "轴间差速锁",
    "Number of axles": "车轴数量",
    "Number of drive axles": "驱动桥数量",
    "Number of steering axles": "转向桥数量",
    "Axle diff locks": "桥间差速锁",
    "Main winch max line pull": "主卷扬最大单绳拉力",
    "Aux winch max line pull": "副卷扬最大单绳拉力",
    "Main winch max speed": "主卷扬最大绳速",
    "Aux winch max speed": "副卷扬最大绳速",
    "Maximum capacity W/O special equipment": "无专用附件最大起重量",
    "Main boom @ 5m": "主臂 5m 幅度起重量",
    "Main boom @ 10m": "主臂 10m 幅度起重量",
    "Main boom @ 15m": "主臂 15m 幅度起重量",
    "Main boom @ 20m": "主臂 20m 幅度起重量",
    "Main boom @ 25m": "主臂 25m 幅度起重量",
    "Main boom @ 30m": "主臂 30m 幅度起重量",
    "Main boom @ 40m": "主臂 40m 幅度起重量",
    "Main boom @ 50m": "主臂 50m 幅度起重量",
    "Main boom max rated radius": "主臂最大额定幅度",
    "Main boom @ max radius": "主臂最大幅度起重量",
    "Jib W/O inserts @ 20m": "基本副臂 20m 幅度起重量",
    "Jib W/O inserts @ 25m": "基本副臂 25m 幅度起重量",
    "Jib W/O inserts @ 30m": "基本副臂 30m 幅度起重量",
    "Jib W/O inserts @ 40m": "基本副臂 40m 幅度起重量",
    "Jib W/O inserts @ 50m": "基本副臂 50m 幅度起重量",
    "Jib W/O inserts max radius": "基本副臂最大幅度",
    "On tires @ 3m over front": "轮胎支撑前方 3m 起重量",
    "On tires @ 5m over front": "轮胎支撑前方 5m 起重量",
    "On tires @ 7m over front": "轮胎支撑前方 7m 起重量",
    "On tires @ 10m over front": "轮胎支撑前方 10m 起重量",
    "Pick and carry @ 5m": "带载行驶 5m 幅度起重量",
    "Swing Speed": "回转速度",
    "Boom raise speed": "起臂时间",
    "Boom extend speed": "伸臂时间",
    "Weight per axle": "单轴载荷",
    "CWT on crane @12 mt per axle": "12t 轴荷条件随车配重",
    "CWT on crane @ 10mt per axle": "10t 轴荷条件随车配重",
    "Minimum transport with dolly": "带辅助小车最小运输重量",
    "Weight per axle with dolly": "带辅助小车单轴载荷",
    "Wheel travel up": "车轮上跳行程",
    "Wheel travel down": "车轮下跳行程",
}

CONFIG_ZH = {
    "Auto Lubrication system": "集中自动润滑系统",
    "Fuel engine heater": "发动机燃油加热器",
    "Tires": "轮胎配置",
    "Short Jib": "短副臂",
    "Tow hooks": "牵引钩",
    "Cold weather package": "低温作业包",
    "Greasless boom": "免润滑主臂",
    "360deg house lock": "360° 上车机械锁止",
    "2deg out of level load charts": "2° 倾斜工况载荷表",
    "heavy CWT": "重型配重包",
    "Cribbing rack": "支腿垫木架",
    "Auto winch and boom control": "卷扬与臂架自动控制",
    "Tires options": "轮胎选项包",
    "Short heavy lift Jib": "短型重载副臂",
}

CONDITION_COPY = {
    "transport": (
        "判断整机在州际道路转场、拆装配重和轴荷管理中的适配性。重点核对运输重量、宽高尺寸、配重组合以及最大配重状态下的行驶能力。",
        "Evaluates interstate transport, counterweight handling and axle-load management through transport mass, envelope, counterweight combinations and travel capability with maximum counterweight.",
    ),
    "mobility": (
        "判断设备从道路进入未铺装场地后的通过性与转向灵活性。行驶速度、转弯半径、转向模式、驱动桥和接近/离去角共同影响现场调位效率。",
        "Evaluates access from road to unpaved sites. Travel speed, turning radius, steering modes, driven axles and approach/departure angles jointly determine repositioning efficiency.",
    ),
    "main-lift": (
        "聚焦主臂中近幅度吊装能力与单循环效率，结合无专用附件最大起重量、典型幅度载荷、主卷扬拉力和臂架动作时间判断。",
        "Focuses on near-to-mid-radius main-boom capacity and cycle efficiency using rated capacity, representative-radius loads, main-winch pull and boom-motion times.",
    ),
    "long-reach": (
        "聚焦高空安装、远幅度吊装和副臂覆盖能力。主臂全伸长度、副臂组合、最大幅度载荷及伸臂效率决定可覆盖的任务边界。",
        "Focuses on high-elevation and long-radius lifts. Full boom length, jib combinations, maximum-radius load and boom-extension time define the reachable work envelope.",
    ),
    "stability": (
        "判断不平地面支腿展开、非对称支撑和轮胎/带载工况下的稳定能力。支腿跨度、支腿档位、倾斜载荷表与轮胎载荷数据需要结合审核。",
        "Evaluates uneven-ground setup, asymmetric support and on-tire/pick-and-carry stability through outrigger geometry, extension positions, out-of-level charts and on-tire capacities.",
    ),
    "continuous-duty": (
        "判断连续吊装、低温环境和附件扩展条件下的持续作业能力。动力储备、燃油容量、主副卷扬、回转速度及低温/润滑配置共同影响停机时间。",
        "Evaluates sustained duty, cold-weather operation and attachment support through power reserve, fuel capacity, winches, swing speed and cold-weather/lubrication equipment.",
    ),
}

ANOMALY_COPY = {
    "stale_excavator_scoring_block_excluded": (
        "源表右侧存在历史挖掘机评分区，已从起重机数据和评分中排除。",
        "A legacy excavator scoring block exists on the right side of the workbook and is excluded from crane data and evaluation.",
    ),
    "suspected_rt130_competitor_headers": (
        "竞品表头与数据范围疑似沿用其他吨级，当前只展示可核验原值，不形成正式排名。",
        "Competitor headers and data ranges appear to reuse another class. Verifiable raw values are shown, but no formal ranking is produced.",
    ),
}


def esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def bilingual(zh: str, en: str, tag: str = "span", class_name: str = "") -> str:
    cls = f' class="{esc(class_name)}"' if class_name else ""
    return f'<{tag}{cls} data-en="{esc(en)}">{esc(zh)}</{tag}>'


def metric_label(name: str) -> str:
    return bilingual(METRIC_ZH.get(name, name), name)


def config_label(name: str) -> str:
    return bilingual(CONFIG_ZH.get(name, name), name)


def fmt_number(value: Any) -> str:
    if value is None or value == "":
        return "—"
    if isinstance(value, bool):
        return "是" if value else "否"
    if isinstance(value, (int, float)):
        if isinstance(value, float) and not math.isfinite(value):
            return "—"
        if abs(float(value) - round(float(value))) < 1e-9:
            return f"{int(round(float(value))):,}"
        return f"{float(value):,.2f}".rstrip("0").rstrip(".")
    return str(value)


def fmt_percent(value: float | None) -> str:
    return "—" if value is None else f"{value * 100:.0f}%"


def fmt_score(value: float | None) -> str:
    return "—" if value is None else f"{value:.1f}"


def get_score_record(scoring: dict[str, Any], product: str) -> dict[str, Any]:
    return next(item for item in scoring["products"] if item["product"] == product)


def config_status(item: Any) -> tuple[str, str, str]:
    status = item.normalized_status
    if status == "standard":
        return "标配", "Standard", "good"
    if status == "optional":
        return "选配", "Optional", "mid"
    if status == "absent":
        return "无配置", "Not Available", "bad"
    if status == "present_unspecified":
        return "有配置，状态未注明", "Available; status unspecified", "mid"
    return "资料未记录", "Data not recorded", "missing"


def model_metric(model: Any, name: str) -> Any | None:
    return next((item for item in model.metrics if item.name == name), None)


def model_config(model: Any, name: str) -> Any | None:
    return next((item for item in model.configurations if item.name == name), None)


def render_rank_bars(scoring: dict[str, Any], field: str, xcmg: str) -> str:
    rows = [item for item in scoring["products"] if item[field] is not None]
    rows.sort(key=lambda item: item[field], reverse=True)
    if not rows:
        reason = get_score_record(scoring, xcmg).get("not_ranked_reason") or "参数有效覆盖率不足60%"
        return (
            '<div class="rankingUnavailable">'
            + bilingual(reason, "Insufficient verified coverage for a formal ranking.", "b")
            + bilingual("页面仍保留全部原始参数与缺失状态，待数据补齐后再计算排名。", "All source values and missing states remain visible; ranking will be enabled only after data completion.", "p")
            + "</div>"
        )
    max_score = max(item[field] for item in rows)
    rendered = []
    for rank, item in enumerate(rows, 1):
        width = max(2.0, item[field] / max_score * 100)
        cls = "bar xcmg" if item["is_xcmg"] else "bar"
        rendered.append(
            f'<div class="{cls}"><span>{rank}</span><b>{esc(item["product"])}</b>'
            f'<i><em style="width:{width:.1f}%"></em></i><strong>{item[field]:.1f}</strong>'
            f'<small class="barCoverage">{fmt_percent(item["parameter_coverage"])}</small></div>'
        )
    return '<div class="bars craneBars">' + "".join(rendered) + "</div>"


def radar_point(index: int, value: float, count: int, size: int = 440) -> tuple[float, float]:
    angle = -math.pi / 2 + index * 2 * math.pi / count
    radius = size * 0.33 * max(0, min(100, value)) / 100
    center = size / 2
    return center + math.cos(angle) * radius, center + math.sin(angle) * radius


def render_category_radar(sheet: Any, scoring: dict[str, Any]) -> str:
    categories = list(CATEGORY_WEIGHTS)
    size = 440
    center = size / 2
    radius = size * 0.33
    rings = []
    for level in (20, 40, 60, 80, 100):
        points = [radar_point(index, level, len(categories), size) for index in range(len(categories))]
        rings.append('<polygon class="radar-grid" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in points) + '"></polygon>')
    axes = []
    labels = []
    for index, category in enumerate(categories):
        x, y = radar_point(index, 100, len(categories), size)
        lx, ly = radar_point(index, 118, len(categories), size)
        zh, en = CATEGORY_NAMES[category]
        axes.append(f'<line class="radar-axis" x1="{center}" y1="{center}" x2="{x:.1f}" y2="{y:.1f}"></line>')
        labels.append(f'<text class="radar-label" x="{lx:.1f}" y="{ly:.1f}" data-en="{esc(en)}">{esc(zh)}</text>')
    colors = ["#f5b400", "#0060aa", "#218c74", "#d9534f", "#7656c9", "#1aa6b7", "#8799aa", "#94335b", "#2e7d4f"]
    series = []
    legend = []
    for model_index, model in enumerate(sheet.models):
        record = get_score_record(scoring, model.display_name)
        values = [record["category_scores"].get(category) for category in categories]
        if sum(value is not None for value in values) < 3:
            continue
        points = [radar_point(i, value or 0, len(categories), size) for i, value in enumerate(values)]
        color = colors[model_index % len(colors)]
        series.append(
            f'<polygon class="radar-series selected" data-product="{esc(model.display_name)}" '
            f'style="--series-color:{color}" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in points) + '"></polygon>'
        )
        legend.append(
            f'<button type="button" class="selected" data-product="{esc(model.display_name)}" aria-pressed="true">'
            f'<i style="background:{color}"></i>{esc(model.display_name)}</button>'
        )
    return (
        '<div class="radarBox craneRadar"><div class="radarHead">'
        + bilingual("八类参数竞争力", "Eight-Category Specification Position", "h3")
        + bilingual("当前：全部品牌", "Current: All Brands", "span", "radarCurrent")
        + f'</div><svg class="radarSvg" viewBox="0 0 {size} {size}" role="img">'
        + "".join(rings + axes + labels + series)
        + '</svg><div class="radarLegend">' + "".join(legend) + "</div></div>"
    )


def render_category_table(sheet: Any, scoring: dict[str, Any]) -> str:
    xcmg_record = get_score_record(
        scoring, next(model.display_name for model in sheet.models if model.is_xcmg)
    )
    rows = []
    for category, weight in CATEGORY_WEIGHTS.items():
        ranked = sorted(
            ((item["product"], item["category_scores"].get(category)) for item in scoring["products"] if item["category_scores"].get(category) is not None),
            key=lambda item: item[1], reverse=True,
        )
        leader = ranked[0] if ranked else ("—", None)
        zh, en = CATEGORY_NAMES[category]
        rows.append(
            f'<tr><th scope="row" data-en="{esc(en)}">{esc(zh)}</th><td>{weight * 100:.0f}%</td>'
            f'<td>{fmt_score(xcmg_record["category_scores"].get(category))}</td><td>{esc(leader[0])}</td><td>{fmt_score(leader[1])}</td></tr>'
        )
    return (
        '<div class="tableScroll craneCompact"><table><thead><tr>'
        + bilingual("参数类别", "Specification Category", "th")
        + bilingual("权重", "Weight", "th")
        + bilingual("XCMG 得分", "XCMG Score", "th")
        + bilingual("类别领先产品", "Category Leader", "th")
        + bilingual("领先分", "Leader Score", "th")
        + '</tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>"
    )


def relevant_metric_names(sheet: Any, condition: dict[str, Any]) -> list[str]:
    names = []
    for name in sheet.parameter_names:
        if any(pattern in name.lower() for pattern in condition["metric_patterns"]):
            names.append(name)
    return names


def relevant_config_names(sheet: Any, condition: dict[str, Any]) -> list[str]:
    return [name for name in sheet.configuration_names if any(pattern in name.lower() for pattern in condition["config_patterns"])]


def concrete_gaps(sheet: Any, scoring: dict[str, Any], condition: dict[str, Any]) -> list[tuple[str, str]]:
    xcmg = next(model for model in sheet.models if model.is_xcmg)
    findings = []
    for name in relevant_metric_names(sheet, condition):
        x_metric = model_metric(xcmg, name)
        x_score = scoring["metric_scores"].get(name, {}).get(xcmg.display_name)
        candidates = []
        for model in sheet.models:
            metric = model_metric(model, name)
            score = scoring["metric_scores"].get(name, {}).get(model.display_name)
            if not model.is_xcmg and metric and metric.numeric_value is not None and score is not None:
                candidates.append((score, model, metric))
        if not x_metric or x_metric.numeric_value is None:
            if candidates:
                best = max(candidates, key=lambda item: item[0])
                zh = f"{METRIC_ZH.get(name, name)}：XCMG 资料未记录；{best[1].display_name} 为 {fmt_number(best[2].raw_value)} {best[2].unit or ''}。"
                en = f"{name}: XCMG data not recorded; {best[1].display_name} records {fmt_number(best[2].raw_value)} {best[2].unit or ''}."
                findings.append((zh, en))
            continue
        if x_score is None or not candidates:
            continue
        best = max(candidates, key=lambda item: item[0])
        if best[0] - x_score < 12:
            continue
        delta = abs(float(x_metric.numeric_value) - float(best[2].numeric_value))
        direction = metric_direction(name)
        qualifier_zh = "高" if direction == "high" else "低"
        qualifier_en = "higher" if direction == "high" else "lower"
        zh = (
            f"{METRIC_ZH.get(name, name)}：XCMG {fmt_number(x_metric.raw_value)} {x_metric.unit or ''}，"
            f"{best[1].display_name} {fmt_number(best[2].raw_value)} {best[2].unit or ''}，"
            f"标杆在当前评价方向上{qualifier_zh}约 {fmt_number(delta)} {x_metric.unit or ''}。"
        )
        en = (
            f"{name}: XCMG {fmt_number(x_metric.raw_value)} {x_metric.unit or ''}; "
            f"{best[1].display_name} {fmt_number(best[2].raw_value)} {best[2].unit or ''}; "
            f"the benchmark is approximately {fmt_number(delta)} {x_metric.unit or ''} {qualifier_en} in the evaluated direction."
        )
        findings.append((zh, en))
    return findings[:4]


def render_condition(sheet: Any, scoring: dict[str, Any], condition: dict[str, Any], index: int) -> str:
    metric_names = relevant_metric_names(sheet, condition)
    config_names = relevant_config_names(sheet, condition)
    score_rows = [
        item for item in scoring["products"]
        if item["condition_scores"].get(condition["id"]) is not None
    ]
    score_rows.sort(key=lambda item: item["condition_scores"][condition["id"]], reverse=True)
    ranking = []
    max_score = max((item["condition_scores"][condition["id"]] for item in score_rows), default=1)
    for rank, item in enumerate(score_rows, 1):
        value = item["condition_scores"][condition["id"]]
        cls = "bar xcmg" if item["is_xcmg"] else "bar"
        ranking.append(
            f'<div class="{cls}"><span>{rank}</span><b>{esc(item["product"])}</b><i><em style="width:{value / max_score * 100:.1f}%"></em></i><strong>{value:.1f}</strong></div>'
        )
    if not ranking:
        ranking_html = '<div class="rankingUnavailable">' + bilingual("有效字段不足，暂不形成该工况排名。", "Insufficient verified fields for a work-condition ranking.", "b") + "</div>"
    else:
        ranking_html = '<div class="bars conditionBars">' + "".join(ranking) + "</div>"

    xcmg = next(model for model in sheet.models if model.is_xcmg)
    key_rows = []
    for name in metric_names[:8]:
        metric = model_metric(xcmg, name)
        value = fmt_number(metric.raw_value) if metric else "—"
        unit = metric.unit if metric else ""
        key_rows.append(f'<tr><th scope="row">{metric_label(name)}</th><td>{esc(value)} {esc(unit)}</td></tr>')
    for name in config_names:
        item = model_config(xcmg, name)
        zh, en, cls = config_status(item) if item else ("资料未记录", "Data not recorded", "missing")
        key_rows.append(f'<tr><th scope="row">{config_label(name)}</th><td class="{cls}" data-en="{esc(en)}">{esc(zh)}</td></tr>')

    gaps = concrete_gaps(sheet, scoring, condition)
    if gaps:
        gap_html = '<ol class="gapList craneGapList">' + "".join(f'<li data-en="{esc(en)}">{esc(zh)}</li>' for zh, en in gaps) + "</ol>"
    else:
        gap_html = bilingual(
            "现有可比字段未显示明显落后项；仍需优先补齐资料未记录项，并核对同配重、同支腿和同臂长条件下的载荷口径。",
            "Available comparable fields show no clear disadvantage. Complete unrecorded fields and confirm like-for-like counterweight, outrigger and boom-length conditions before setting targets.",
            "p",
        )
    copy_zh, copy_en = CONDITION_COPY[condition["id"]]
    return (
        f'<section id="cond{index}" class="conditionSection">'
        f'<div class="conditionTitle"><div><span>WORK CONDITION {index:02d}</span>'
        f'<h2 data-en="{esc(condition["title_en"])}">{esc(condition["title_zh"])}</h2></div>'
        f'<em>{len(metric_names)} 个参数 / {len(config_names)} 个配置项</em></div>'
        f'<p class="conditionNarrative" data-en="{esc(copy_en)}">{esc(copy_zh)}</p>'
        '<div class="conditionCraneGrid"><article class="panel"><h3 data-en="Work-condition position">工况竞争位置</h3>'
        + ranking_html
        + '</article><article class="panel"><h3 data-en="XCMG source values">XCMG 关键原值</h3>'
        + '<div class="tableScroll compactCondition"><table><tbody>' + "".join(key_rows) + "</tbody></table></div></article></div>"
        + '<div class="gapPanel"><h3 data-en="Documented gaps and validation points">具体差距与复核重点</h3>' + gap_html + "</div></section>"
    )


def render_parameter_matrix(sheet: Any) -> str:
    blocks = []
    for category in CATEGORY_WEIGHTS:
        names = [
            name
            for name in sheet.parameter_names
            if any(
                metric.subcategory == category and metric.name == name
                for model in sheet.models
                for metric in model.metrics
            )
        ]
        if not names:
            continue
        rows = []
        for name in names:
            unit = next((metric.unit for model in sheet.models if (metric := model_metric(model, name)) and metric.unit), "")
            cells = []
            for model in sheet.models:
                metric = model_metric(model, name)
                value = fmt_number(metric.raw_value) if metric else "—"
                cls = "missing" if not metric or metric.raw_value in (None, "") else ""
                cells.append(f'<td class="{cls}">{esc(value)}</td>')
            rows.append(f'<tr><th scope="row">{metric_label(name)}</th><td>{esc(unit)}</td>' + "".join(cells) + "</tr>")
        zh, en = CATEGORY_NAMES[category]
        header = "".join(f'<th class="{ "xcmgHead" if model.is_xcmg else ""}">{esc(model.display_name)}</th>' for model in sheet.models)
        blocks.append(
            f'<details class="dataGroup" open><summary data-en="{esc(en)}">{esc(zh)} <span>{len(rows)} 项</span></summary>'
            '<div class="tableScroll rawTable craneMatrix"><table><thead><tr>'
            + bilingual("参数", "Specification", "th") + bilingual("单位", "Unit", "th") + header
            + '</tr></thead><tbody>' + "".join(rows) + "</tbody></table></div></details>"
        )
    return "".join(blocks)


def render_configuration_matrix(sheet: Any) -> str:
    rows = []
    for name in sheet.configuration_names:
        cells = []
        for model in sheet.models:
            item = model_config(model, name)
            zh, en, cls = config_status(item) if item else ("资料未记录", "Data not recorded", "missing")
            cells.append(f'<td class="{cls}" data-en="{esc(en)}">{esc(zh)}</td>')
        rows.append(f'<tr><th scope="row">{config_label(name)}</th>' + "".join(cells) + "</tr>")
    header = "".join(f'<th class="{ "xcmgHead" if model.is_xcmg else ""}">{esc(model.display_name)}</th>' for model in sheet.models)
    return (
        '<div class="tableScroll rawTable craneMatrix"><table><thead><tr>'
        + bilingual("配置项", "Equipment Item", "th") + header
        + '</tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>"
    )


def render_quality(sheet: Any, scoring: dict[str, Any]) -> str:
    rows = []
    for model in sheet.models:
        score = get_score_record(scoring, model.display_name)
        reason = score.get("not_ranked_reason") or "—"
        reason_en = "Eligible for available evaluation" if reason == "—" else "Insufficient verified coverage or source scope"
        rows.append(
            f'<tr class="{ "xcmg-row" if model.is_xcmg else ""}"><th scope="row">{esc(model.display_name)}</th>'
            f'<td>{fmt_percent(model.parameter_coverage)}</td><td>{fmt_percent(model.configuration_coverage)}</td>'
            f'<td data-en="{esc(reason_en)}">{esc(reason)}</td></tr>'
        )
    anomalies = []
    for code in sheet.anomalies:
        zh, en = ANOMALY_COPY.get(code, (code, code))
        anomalies.append(f'<li data-en="{esc(en)}">{esc(zh)}</li>')
    if not anomalies:
        anomalies.append('<li data-en="No sheet-level source anomaly was recorded.">未记录工作表级异常。</li>')
    return (
        '<div class="qualityGrid"><article class="panel"><h3 data-en="Coverage by product">各产品数据覆盖</h3>'
        '<div class="tableScroll"><table><thead><tr>'
        + bilingual("产品", "Product", "th") + bilingual("参数覆盖", "Specification Coverage", "th")
        + bilingual("配置覆盖", "Equipment Coverage", "th") + bilingual("排名状态", "Ranking Status", "th")
        + '</tr></thead><tbody>' + "".join(rows) + "</tbody></table></div></article>"
        + '<article class="panel"><h3 data-en="Source checks">源数据核验记录</h3><ul class="qualityList">'
        + "".join(anomalies)
        + '</ul><p class="methodNote" data-en="Blank equipment cells remain unknown and are never converted to unavailable or zero. The six-characteristic section is blank in the source workbook and no score is fabricated.">配置空白保留为“资料未记录”，不转换为“无配置”或 0 分；源表“六大特性”区域为空，本页不编造实机评价分数。</p></article></div>'
    )


def page_nav(sheet: Any) -> str:
    condition_links = "".join(
        f'<a href="#cond{index}" data-en="{esc(condition["title_en"])}">{esc(condition["title_zh"])}</a>'
        for index, condition in enumerate(CONDITIONS, 1)
    )
    return (
        '<a class="home" href="arc.html" data-en="Return to Platform Home">返回对标平台主页</a>'
        '<a href="#summary" data-en="Benchmark Overview">对标概览</a>'
        '<a href="#position" data-en="Specification Position">参数竞争位置</a>'
        '<details class="navGroup" open><summary data-en="Work Conditions">典型工况</summary><div class="navSubmenu">'
        + condition_links + '</div></details>'
        '<a href="#parameters" data-en="Specification Matrix">参数明细</a>'
        '<a href="#configurations" data-en="Equipment Matrix">配置明细</a>'
        '<a href="#quality" data-en="Data Quality">数据质量</a>'
    )


def render_page(sheet: Any) -> str:
    definition = PAGE_DEFINITIONS[sheet.label]
    scoring = score_sheet(sheet)
    xcmg = next(model for model in sheet.models if model.is_xcmg)
    xscore = get_score_record(scoring, xcmg.display_name)
    ranked = sorted(
        (item for item in scoring["products"] if item["parameter_score"] is not None),
        key=lambda item: item["parameter_score"], reverse=True,
    )
    rank = next((index for index, item in enumerate(ranked, 1) if item["is_xcmg"]), None)
    rank_display = f"第 {rank}" if rank else "暂不排名"
    rank_en = f"No. {rank}" if rank else "Not ranked"
    image_note_zh = "XCMG USA 官方产品图" if definition["official"] else "XCMG 起重设备产品线示意图；XCR165U 对应官方图片待补"
    image_note_en = "Official XCMG USA product image" if definition["official"] else "XCMG crane product-line image; model-specific XCR165U image pending"
    title_zh = f'{xcmg.display_name} {sheet.tonnage} 起重机竞品对标'
    title_en = f'{xcmg.display_name} {sheet.tonnage} Crane Competitive Benchmark'
    conditions = "".join(render_condition(sheet, scoring, condition, index) for index, condition in enumerate(CONDITIONS, 1))
    return f'''<!doctype html>
<html lang="zh-CN" data-language="zh"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title_zh)} | XCMG ARC</title>
<link rel="stylesheet" href="assets/dashboard.css?v=20260805a">
<link rel="stylesheet" href="assets/crane-dashboard.css?v=20260805a">
</head><body>
<a class="backTop" href="#top" aria-label="回到页面顶部">回到顶部</a>
<div class="layout" id="top"><aside class="nav">
  <a class="navBrand" href="arc.html" aria-label="返回全产品线竞品对标平台主页"><img src="assets/xcmg-logo.svg" alt="XCMG"></a>
  <div><div class="navTitle" data-en="{esc(sheet.label)} Crane Benchmark">{esc(sheet.label)} 起重机对标</div><small>{esc(xcmg.display_name)}</small></div>
  <button class="languageToggle" type="button" aria-label="Switch to English">EN</button>
  <button class="sidebarToggle" type="button" aria-expanded="true" aria-controls="page-nav"><span>收起侧栏</span></button>
  <button class="navToggle" type="button" aria-expanded="false" aria-controls="page-nav">页面导航</button>
  <a class="mobileTop" href="#top">顶部</a><div class="navMenu" id="page-nav">{page_nav(sheet)}</div>
</aside><main>
<header class="hero craneHero"><div class="heroText"><p class="eyebrow">XCMG ARC CRANE BENCHMARK</p>
  <h1 data-en="{esc(title_en)}">{esc(title_zh)}</h1>
  <p data-en="Source-backed comparison of transport, chassis, boom and jib, outriggers, powertrain, winches, lifting performance, operating speeds and equipment status.">按同吨级比较运输、底盘机动、主副臂、支腿、动力、卷扬、起重性能、作业速度和标选配状态，所有结论保留原始值与缺失状态。</p>
  <div class="actions"><a class="btn blue" href="#position" data-en="Open Benchmark">查看对标</a><a class="btn" href="{SOURCE_DOWNLOAD}" download data-en="Download Source Workbook">下载原始数据</a></div>
</div><figure class="heroMedia craneHeroMedia"><img src="{esc(definition['image'])}" alt="{esc(definition['image_alt'])}"><figcaption data-en="{esc(image_note_en)}">{esc(image_note_zh)}</figcaption></figure></header>

<section id="summary"><h2 data-en="Benchmark Overview">对标概览</h2><div class="kpis craneKpis">
  <div class="kpi"><b>{len(sheet.models)}</b><span data-en="Benchmark products">对标产品数</span></div>
  <div class="kpi"><b>{fmt_score(xscore['parameter_score'])}</b><span data-en="XCMG specification score">XCMG 参数竞争力</span></div>
  <div class="kpi"><b data-en="{esc(rank_en)}">{esc(rank_display)}</b><span data-en="Specification rank">参数排名</span></div>
  <div class="kpi"><b>{fmt_percent(xcmg.parameter_coverage)}</b><span data-en="XCMG source coverage">XCMG 参数覆盖率</span></div>
</div><div class="methodStrip"><b data-en="Evaluation boundary">评价边界</b><p data-en="Specification values use direction-aware normalization within the current tonnage class. Category weights total 100%. Equipment uses 0 for unavailable, 60 for optional and 100 for standard only when status is explicit. Overall scoring is withheld when verified equipment coverage is below 60%.">参数按当前吨级内同口径、方向归一化，八类权重合计 100%；配置仅在状态明确时按无配置 0、选配 60、标配 100 计入。当前配置有效覆盖率低于 60% 时，不生成综合总分和综合排名。</p></div></section>

<section id="position"><h2 data-en="Specification Position">参数竞争位置</h2><div class="positionGrid"><article class="panel"><h3 data-en="Specification ranking">参数竞争力排名</h3>{render_rank_bars(scoring, 'parameter_score', xcmg.display_name)}</article><article class="panel">{render_category_radar(sheet, scoring)}</article></div>{render_category_table(sheet, scoring)}</section>

<div id="conditions">{conditions}</div>

<section id="parameters"><h2 data-en="Complete Specification Matrix">全部参数明细</h2><p class="sectionLead" data-en="Values are grouped by eight crane engineering systems. Empty cells remain unrecorded and are not treated as zero.">按八类起重机工程系统展示全部参数；空白保留为“资料未记录”，不按 0 值处理。</p>{render_parameter_matrix(sheet)}</section>

<section id="configurations"><h2 data-en="Standard and Optional Equipment Matrix">标配 / 选配明细</h2><p class="sectionLead" data-en="Only explicit source states are classified. A blank cell means the source did not record the status.">仅对源表明确记录的状态进行分类；空白表示资料未记录，不等于无配置。</p>{render_configuration_matrix(sheet)}</section>

<section id="quality"><h2 data-en="Data Quality and Publication Boundary">数据质量与发布边界</h2>{render_quality(sheet, scoring)}</section>

<footer class="dashboardFooter"><small data-en="Executive sponsor: Zhang Shengnan · Data visualization: Liu Chang · Data source: ARC Product Team · Issue reporting: changl@xcmgarc.com">指导领导：张盛楠　数据可视化：刘畅　数据来源：ARC产品小组　问题提报：changl@xcmgarc.com</small></footer>
</main></div><script src="assets/dashboard.js?v=20260805a"></script><script src="assets/i18n.js?v=20260805a"></script>
</body></html>'''


def render_overview(workbook: Any) -> str:
    cards = []
    total_models = 0
    for sheet in workbook.sheets:
        definition = PAGE_DEFINITIONS[sheet.label]
        total_models += len(sheet.models)
        scoring = score_sheet(sheet)
        xcmg = next(model for model in sheet.models if model.is_xcmg)
        xscore = get_score_record(scoring, xcmg.display_name)
        status_zh = "可形成参数对标" if xscore["parameter_score"] is not None else "数据范围待补齐"
        status_en = "Specification benchmark available" if xscore["parameter_score"] is not None else "Source scope requires completion"
        cards.append(
            f'<a class="craneAssetCard" href="{esc(definition["output"])}"><div class="craneAssetMedia"><img src="{esc(definition["image"])}" alt="{esc(definition["image_alt"])}"></div>'
            f'<div class="craneAssetBody"><span>{esc(sheet.label)}</span><h3>{esc(xcmg.display_name)}</h3>'
            f'<p>{len(sheet.models)} 个对标产品 · 参数覆盖 {fmt_percent(xcmg.parameter_coverage)}</p>'
            f'<b data-en="{esc(status_en)}">{esc(status_zh)}</b></div></a>'
        )
    condition_cards = "".join(
        f'<article><span>{index:02d}</span><h3 data-en="{esc(condition["title_en"])}">{esc(condition["title_zh"])}</h3><p data-en="{esc(CONDITION_COPY[condition["id"]][1])}">{esc(CONDITION_COPY[condition["id"]][0])}</p></article>'
        for index, condition in enumerate(CONDITIONS, 1)
    )
    return f'''<!doctype html><html lang="zh-CN" data-language="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>起重设备竞品对标总览 | XCMG ARC</title><link rel="stylesheet" href="assets/dashboard.css?v=20260805a"><link rel="stylesheet" href="assets/crane-dashboard.css?v=20260805a"></head><body>
<a class="backTop" href="#top">回到顶部</a><div class="layout" id="top"><aside class="nav"><a class="navBrand" href="arc.html"><img src="assets/xcmg-logo.svg" alt="XCMG"></a><div><div class="navTitle" data-en="Crane Benchmark Overview">起重设备对标总览</div><small>XCMG ARC</small></div><button class="languageToggle" type="button">EN</button><button class="sidebarToggle" type="button"><span>收起侧栏</span></button><button class="navToggle" type="button">页面导航</button><div class="navMenu" id="page-nav"><a class="home" href="arc.html" data-en="Return to Platform Home">返回对标平台主页</a><a href="#portfolio" data-en="Class Assets">吨级资产</a><a href="#framework" data-en="Benchmark Framework">对标框架</a><a href="#method" data-en="Evaluation Boundary">评价边界</a></div></aside><main>
<header class="hero craneOverviewHero"><div class="heroText"><p class="eyebrow">CRANES AND HOISTING</p><h1 data-en="Crane Competitive Benchmarking">起重设备竞品对标</h1><p data-en="Six rough-terrain and all-terrain classes are organized under one engineering framework covering source values, work conditions, equipment status and data-quality boundaries.">覆盖 5 个越野轮胎起重机吨级和 1 个全地面起重机吨级，统一管理参数原值、典型工况、配置状态和数据质量边界。</p><div class="actions"><a class="btn blue" href="#portfolio" data-en="Open Class Assets">查看吨级资产</a><a class="btn" href="{SOURCE_DOWNLOAD}" download data-en="Download Source Workbook">下载原始数据</a></div></div><div class="heroMedia"><img src="assets/arc/category-cranes.webp" alt="XCMG crane"></div></header>
<section id="portfolio"><h2 data-en="Crane Class Assets">起重机吨级资产</h2><div class="kpis craneKpis"><div class="kpi"><b>6</b><span data-en="Tonnage classes">吨级 / 类别</span></div><div class="kpi"><b>{total_models}</b><span data-en="Benchmark products">对标产品</span></div><div class="kpi"><b>8</b><span data-en="Specification categories">参数类别</span></div><div class="kpi"><b>6</b><span data-en="Work conditions">典型工况</span></div></div><div class="craneAssetGrid">{''.join(cards)}</div></section>
<section id="framework"><h2 data-en="Work-Condition Benchmark Framework">工况对标框架</h2><div class="conditionFramework">{condition_cards}</div></section>
<section id="method"><h2 data-en="Evaluation and Data Boundary">评分与数据边界</h2><div class="qualityGrid"><article class="panel"><h3 data-en="Specification evaluation">参数评价</h3><p data-en="Direction-aware normalization is applied within each class. Category weights are transport 10%, chassis and mobility 12%, boom and jib 18%, outriggers 12%, powertrain 8%, winches 10%, lifting performance 25% and speeds 5%.">各吨级内部按指标方向归一化；运输 10%、底盘机动 12%、主副臂 18%、支腿 12%、动力 8%、卷扬 10%、起重性能 25%、速度 5%。</p></article><article class="panel"><h3 data-en="Equipment and missing data">配置与缺失值</h3><p data-en="Explicit unavailable, optional and standard states use 0, 60 and 100. Blank cells remain unrecorded. No overall score is published below 60% verified configuration coverage, and blank six-characteristic rows are not converted into machine-test ratings.">明确的无配置、选配、标配按 0、60、100 计入；空白保留为资料未记录。配置有效覆盖率不足 60% 时不发布综合分；空白的六大特性区域不转化为实机评价。</p></article></div></section>
<footer class="dashboardFooter"><small data-en="Executive sponsor: Zhang Shengnan · Data visualization: Liu Chang · Data source: ARC Product Team · Issue reporting: changl@xcmgarc.com">指导领导：张盛楠　数据可视化：刘畅　数据来源：ARC产品小组　问题提报：changl@xcmgarc.com</small></footer>
</main></div><script src="assets/dashboard.js?v=20260805a"></script><script src="assets/i18n.js?v=20260805a"></script></body></html>'''


def build_all() -> list[Path]:
    workbook = load_crane_workbook()
    outputs = []
    overview_path = ROOT / "crane-overview.html"
    overview_path.write_text(render_overview(workbook), encoding="utf-8")
    outputs.append(overview_path)
    for sheet in workbook.sheets:
        output = ROOT / PAGE_DEFINITIONS[sheet.label]["output"]
        output.write_text(render_page(sheet), encoding="utf-8")
        outputs.append(output)
    return outputs


if __name__ == "__main__":
    for path in build_all():
        print(path.relative_to(ROOT))
