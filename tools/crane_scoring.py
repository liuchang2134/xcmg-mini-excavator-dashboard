from __future__ import annotations

import math
import re
from dataclasses import asdict, dataclass
from typing import Any

try:
    from .crane_data import CraneSheet, load_crane_workbook
except ImportError:
    from crane_data import CraneSheet, load_crane_workbook


MIN_SCORE_COVERAGE = 0.60
OVERALL_WEIGHTS = {"parameter": 0.65, "configuration": 0.35}
CATEGORY_WEIGHTS = {
    "Transport Parameters": 0.10,
    "Ground Parameters": 0.12,
    "Boom and jib": 0.18,
    "Outriggers": 0.12,
    "Power": 0.08,
    "Winches": 0.10,
    "Lifting performance": 0.25,
    "Speeds": 0.05,
}


CONDITIONS = [
    {
        "id": "road-transport",
        "title_zh": "道路运输 / 轴荷与外廓合规",
        "title_en": "Road Transport and Axle-Load Compliance",
        "metric_rules": [
            ("Minimum transport weight", 22),
            ("Weight per axle", 18),
            ("CWT on crane @12 mt per axle", 8),
            ("CWT on crane @ 10mt per axle", 8),
            ("Minimum transport with dolly", 10),
            ("Weight per axle with dolly", 8),
            ("Transport Width", 10),
            ("Transport Height", 8),
            ("Transport Length", 8),
            ("Removable CWT", 8),
            ("Number of CWT configurations", 6),
            ("Speed with max CWT", 8),
        ],
        "config_rules": [("Tow hooks", 65), ("Cribbing rack", 35)],
        "parameter_share": 0.85,
        "configuration_share": 0.15,
        "minimum_metric_items": 3,
    },
    {
        "id": "rapid-mobilization",
        "title_zh": "快速拆装 / 多工地转场",
        "title_en": "Rapid Setup and Multi-Site Mobilization",
        "metric_rules": [
            ("Removable CWT", 22),
            ("Number of CWT configurations", 18),
            ("CWT on crane @12 mt per axle", 12),
            ("CWT on crane @ 10mt per axle", 10),
            ("Minimum transport with dolly", 10),
            ("Weight per axle with dolly", 8),
            ("Speed with max CWT", 12),
            ("Transport Length", 8),
        ],
        "config_rules": [
            ("Tow hooks", 40),
            ("Cribbing rack", 35),
            ("Auto Lubrication system", 25),
        ],
        "parameter_share": 0.78,
        "configuration_share": 0.22,
        "minimum_metric_items": 3,
    },
    {
        "id": "site-mobility",
        "title_zh": "场地进出 / 越野机动",
        "title_en": "Site Access and Rough-Terrain Mobility",
        "metric_rules": [
            ("Speed", 20),
            ("Minimum turning radius", 20),
            ("Number of steering modes", 15),
            ("Gradability", 15),
            ("Front approach angle", 10),
            ("Rear approach angle", 10),
            ("Number of drive axles", 5),
            ("Number of steering axles", 5),
            ("Wheel travel up", 5),
            ("Wheel travel down", 5),
        ],
        "config_rules": [("Tires", 60), ("Tires options", 40)],
        "parameter_share": 0.90,
        "configuration_share": 0.10,
        "minimum_metric_items": 3,
    },
    {
        "id": "confined-positioning",
        "title_zh": "狭窄场地 / 精细调位",
        "title_en": "Confined-Site Maneuvering and Precision Positioning",
        "metric_rules": [
            ("Minimum turning radius", 28),
            ("Tail swing radius", 28),
            ("Retracted Boom Length", 18),
            ("Number of steering modes", 16),
            ("Swing Speed", 10),
        ],
        "config_rules": [
            ("360deg house lock", 40),
            ("Auto winch and boom control", 60),
        ],
        "parameter_share": 0.82,
        "configuration_share": 0.18,
        "minimum_metric_items": 3,
    },
    {
        "id": "near-heavy-lift",
        "title_zh": "近幅度 / 重载吊装",
        "title_en": "Near-Radius Heavy Lifting",
        "metric_rules": [
            ("Maximum capacity W/O special equipment", 22),
            ("role:main-boom-near", 34),
            ("Main winch max line pull", 18),
            ("Main winch max speed", 12),
            ("Boom raise speed", 14),
        ],
        "config_rules": [
            ("heavy CWT", 50),
            ("Short heavy lift Jib", 20),
            ("Auto winch and boom control", 30),
        ],
        "parameter_share": 0.88,
        "configuration_share": 0.12,
        "minimum_metric_items": 3,
    },
    {
        "id": "mid-radius-installation",
        "title_zh": "中幅度 / 结构安装",
        "title_en": "Mid-Radius Structural Installation",
        "metric_rules": [
            ("role:main-boom-mid", 42),
            ("Main winch max line pull", 18),
            ("Main winch max speed", 14),
            ("Boom raise speed", 13),
            ("Swing Speed", 13),
        ],
        "config_rules": [("Auto winch and boom control", 100)],
        "parameter_share": 0.90,
        "configuration_share": 0.10,
        "minimum_metric_items": 3,
    },
    {
        "id": "long-boom-high-lift",
        "title_zh": "长臂大幅度 / 高空安装",
        "title_en": "Long-Boom, Long-Radius High-Elevation Installation",
        "metric_rules": [
            ("Extended Boom Length", 16),
            ("Main boom max rated radius", 14),
            ("role:main-boom-far", 30),
            ("Main boom @ max radius", 22),
            ("Boom extend speed", 12),
            ("Cab tilt", 6),
        ],
        "config_rules": [
            ("Auto winch and boom control", 60),
            ("heavy CWT", 40),
        ],
        "parameter_share": 0.88,
        "configuration_share": 0.12,
        "minimum_metric_items": 3,
    },
    {
        "id": "jib-long-radius",
        "title_zh": "副臂组合 / 远幅度作业",
        "title_en": "Jib Configuration and Long-Radius Work",
        "metric_rules": [
            ("Max jib carried on crane", 15),
            ("Jib extensions", 12),
            ("role:jib-near", 28),
            ("role:jib-far", 28),
            ("Jib W/O inserts max radius", 17),
        ],
        "context_metrics": ["Jib offset angles", "Luffing jib"],
        "config_rules": [
            ("Short Jib", 45),
            ("Short heavy lift Jib", 35),
            ("Auto winch and boom control", 20),
        ],
        "parameter_share": 0.82,
        "configuration_share": 0.18,
        "minimum_metric_items": 3,
    },
    {
        "id": "outrigger-stability",
        "title_zh": "支腿展开 / 不平地面稳定",
        "title_en": "Outrigger Setup and Uneven-Ground Stability",
        "metric_rules": [
            ("Full outrigger extension", 58),
            ("Number of outrigger extensions", 42),
        ],
        "context_metrics": ["Outrigger penetration", "Asymmetric outrigger operation"],
        "config_rules": [
            ("2deg out of level load charts", 35),
            ("Cribbing rack", 25),
            ("360deg house lock", 20),
            ("Auto winch and boom control", 20),
        ],
        "parameter_share": 0.65,
        "configuration_share": 0.35,
        "minimum_metric_items": 2,
    },
    {
        "id": "partial-outrigger-confined",
        "title_zh": "部分支腿 / 受限支撑",
        "title_en": "Partial-Outrigger and Constrained-Support Operation",
        "metric_rules": [
            ("Full outrigger extension", 34),
            ("Number of outrigger extensions", 34),
            ("Tail swing radius", 16),
            ("role:main-boom-mid", 16),
        ],
        "context_metrics": ["Asymmetric outrigger operation", "Outrigger penetration"],
        "config_rules": [
            ("2deg out of level load charts", 45),
            ("Cribbing rack", 30),
            ("360deg house lock", 25),
        ],
        "parameter_share": 0.62,
        "configuration_share": 0.38,
        "minimum_metric_items": 2,
    },
    {
        "id": "on-tire-pick-carry",
        "title_zh": "轮胎吊装 / 带载行驶",
        "title_en": "On-Tire Lifting and Pick-and-Carry",
        "families": ["RT"],
        "metric_rules": [
            ("role:on-tire-near", 36),
            ("role:on-tire-far", 32),
            ("Pick and carry @ 5m", 24),
            ("Speed", 8),
        ],
        "config_rules": [("Tires", 60), ("360deg house lock", 40)],
        "parameter_share": 0.90,
        "configuration_share": 0.10,
        "minimum_metric_items": 2,
    },
    {
        "id": "cycle-productivity",
        "title_zh": "连续循环 / 双卷扬协同",
        "title_en": "Continuous Cycles and Dual-Winch Coordination",
        "metric_rules": [
            ("Main winch max line pull", 14),
            ("Aux winch max line pull", 14),
            ("Main winch max speed", 16),
            ("Aux winch max speed", 16),
            ("Swing Speed", 14),
            ("Boom raise speed", 13),
            ("Boom extend speed", 13),
        ],
        "config_rules": [
            ("Auto winch and boom control", 70),
            ("Auto Lubrication system", 30),
        ],
        "parameter_share": 0.86,
        "configuration_share": 0.14,
        "minimum_metric_items": 4,
    },
    {
        "id": "precision-maintenance-lift",
        "title_zh": "精密落钩 / 高空维保",
        "title_en": "Precision Placement and Elevated Maintenance",
        "metric_rules": [
            ("Main winch max speed", 18),
            ("Aux winch max speed", 20),
            ("Swing Speed", 22),
            ("Boom raise speed", 15),
            ("Boom extend speed", 15),
            ("Cab tilt", 10),
        ],
        "config_rules": [
            ("Auto winch and boom control", 70),
            ("360deg house lock", 30),
        ],
        "parameter_share": 0.76,
        "configuration_share": 0.24,
        "minimum_metric_items": 4,
    },
    {
        "id": "all-weather-duty",
        "title_zh": "低温环境 / 全天候连续作业",
        "title_en": "Cold-Weather and All-Weather Continuous Duty",
        "metric_rules": [
            ("Engine Power", 38),
            ("Engine Torque", 38),
            ("Fuel tank", 24),
        ],
        "config_rules": [
            ("Auto Lubrication system", 20),
            ("Fuel engine heater", 25),
            ("Cold weather package", 35),
            ("Greasless boom", 20),
        ],
        "parameter_share": 0.45,
        "configuration_share": 0.55,
        "minimum_metric_items": 2,
    },
    {
        "id": "urban-utility-installation",
        "group": "application",
        "title_zh": "城市更新 / 公用设施高空作业",
        "title_en": "Urban Renewal and Utility Installation",
        "metric_rules": [
            ("Minimum turning radius", 16),
            ("Tail swing radius", 16),
            ("Retracted Boom Length", 12),
            ("role:main-boom-mid", 20),
            ("role:main-boom-far", 16),
            ("Swing Speed", 10),
            ("Boom extend speed", 10),
        ],
        "config_rules": [
            ("360deg house lock", 30),
            ("Auto winch and boom control", 45),
            ("2deg out of level load charts", 25),
        ],
        "parameter_share": 0.82,
        "configuration_share": 0.18,
        "minimum_metric_items": 4,
    },
    {
        "id": "industrial-shutdown-maintenance",
        "group": "application",
        "title_zh": "油气装置 / 工业停机检修",
        "title_en": "Oil, Gas and Industrial Shutdown Maintenance",
        "metric_rules": [
            ("role:main-boom-mid", 22),
            ("role:main-boom-far", 14),
            ("Aux winch max line pull", 12),
            ("Aux winch max speed", 14),
            ("Swing Speed", 12),
            ("Boom raise speed", 12),
            ("Boom extend speed", 14),
        ],
        "config_rules": [
            ("Auto winch and boom control", 45),
            ("Greasless boom", 25),
            ("Auto Lubrication system", 30),
        ],
        "parameter_share": 0.80,
        "configuration_share": 0.20,
        "minimum_metric_items": 4,
    },
    {
        "id": "bridge-infrastructure-placement",
        "group": "application",
        "title_zh": "道路桥梁 / 基础设施构件安装",
        "title_en": "Road, Bridge and Infrastructure Placement",
        "metric_rules": [
            ("Minimum turning radius", 8),
            ("Gradability", 8),
            ("Full outrigger extension", 14),
            ("Number of outrigger extensions", 8),
            ("role:main-boom-mid", 24),
            ("role:main-boom-far", 22),
            ("Swing Speed", 8),
            ("Boom raise speed", 8),
        ],
        "context_metrics": ["Asymmetric outrigger operation", "Outrigger penetration"],
        "config_rules": [
            ("2deg out of level load charts", 35),
            ("Cribbing rack", 25),
            ("Auto winch and boom control", 25),
            ("360deg house lock", 15),
        ],
        "parameter_share": 0.82,
        "configuration_share": 0.18,
        "minimum_metric_items": 5,
    },
    {
        "id": "emergency-response",
        "group": "application",
        "title_zh": "应急抢险 / 快速响应吊装",
        "title_en": "Emergency Response and Rapid-Recovery Lifting",
        "metric_rules": [
            ("Speed", 12),
            ("Minimum turning radius", 14),
            ("Gradability", 12),
            ("Front approach angle", 8),
            ("Rear approach angle", 8),
            ("role:main-boom-near", 12),
            ("role:main-boom-mid", 12),
            ("Boom raise speed", 10),
            ("Swing Speed", 12),
        ],
        "context_metrics": ["Tire size", "Axle diff locks", "Interaxle lock"],
        "config_rules": [
            ("Tow hooks", 30),
            ("Tires", 20),
            ("Auto winch and boom control", 30),
            ("360deg house lock", 20),
        ],
        "parameter_share": 0.84,
        "configuration_share": 0.16,
        "minimum_metric_items": 5,
    },
    {
        "id": "port-yard-handling",
        "group": "application",
        "title_zh": "港口堆场 / 高频装卸",
        "title_en": "Port and Yard High-Cycle Handling",
        "metric_rules": [
            ("Speed", 8),
            ("Minimum turning radius", 8),
            ("Main winch max line pull", 10),
            ("Aux winch max line pull", 10),
            ("Main winch max speed", 17),
            ("Aux winch max speed", 17),
            ("Swing Speed", 15),
            ("Boom raise speed", 15),
        ],
        "config_rules": [
            ("Auto winch and boom control", 60),
            ("Auto Lubrication system", 25),
            ("360deg house lock", 15),
        ],
        "parameter_share": 0.84,
        "configuration_share": 0.16,
        "minimum_metric_items": 5,
    },
]


LOWER_IS_BETTER = {
    "minimum transport weight",
    "transport width",
    "transport height",
    "transport length",
    "wheelbase",
    "minimum turning radius",
    "tail swing radius",
    "boom raise speed",
    "boom extend speed",
}

NON_SCORING_METRICS = {
    "tire size",
    "engine",
    "transmission",
    "luffing jib",
    "asymmetric outrigger operation",
    "interaxle lock",
    "axle diff locks",
}


@dataclass
class ProductScore:
    product: str
    brand: str
    is_xcmg: bool
    parameter_score: float | None
    parameter_coverage: float
    configuration_score: float | None
    configuration_coverage: float
    overall_score: float | None
    overall_rank: int | None
    category_scores: dict[str, float | None]
    condition_scores: dict[str, float | None]
    condition_details: dict[str, dict[str, Any]]
    not_ranked_reason: str | None


def normalize(values: dict[str, float | None], direction: str) -> dict[str, float]:
    valid = {key: value for key, value in values.items() if value is not None and math.isfinite(value)}
    if not valid:
        return {}
    low = min(valid.values())
    high = max(valid.values())
    if abs(high - low) < 1e-9:
        return {key: 100.0 for key in valid}
    if direction == "low":
        return {key: (high - value) / (high - low) * 100 for key, value in valid.items()}
    return {key: (value - low) / (high - low) * 100 for key, value in valid.items()}


def weighted_average(
    parts: list[tuple[float | None, float]],
    minimum_coverage: float = MIN_SCORE_COVERAGE,
) -> tuple[float | None, float]:
    total_weight = sum(weight for _, weight in parts if weight > 0)
    if total_weight <= 0:
        return None, 0.0
    valid = [(score, weight) for score, weight in parts if score is not None and weight > 0]
    valid_weight = sum(weight for _, weight in valid)
    coverage = valid_weight / total_weight
    if coverage + 1e-9 < minimum_coverage or not valid:
        return None, coverage
    return sum(score * weight for score, weight in valid) / valid_weight, coverage


def metric_direction(name: str) -> str | None:
    key = name.strip().lower()
    if key in NON_SCORING_METRICS:
        return None
    if key in LOWER_IS_BETTER:
        return "low"
    return "high"


def condition_applicable(sheet: CraneSheet, condition: dict[str, Any]) -> bool:
    return sheet.family in condition.get("families", ["RT", "AT"])


def _radius_metrics(sheet: CraneSheet, prefix: str) -> list[tuple[float, str]]:
    pattern = re.compile(rf"^{re.escape(prefix)}\s*(\d+(?:\.\d+)?)m$", re.IGNORECASE)
    matches = []
    for name in sheet.parameter_names:
        match = pattern.match(name.strip())
        if match:
            matches.append((float(match.group(1)), name))
    return sorted(matches)


def _role_metric_name(sheet: CraneSheet, role: str) -> str | None:
    role_definitions = {
        "main-boom-near": ("Main boom @", "near"),
        "main-boom-mid": ("Main boom @", "mid"),
        "main-boom-far": ("Main boom @", "far"),
        "jib-near": ("Jib W/O inserts @", "near"),
        "jib-far": ("Jib W/O inserts @", "far"),
        "on-tire-near": ("On tires @", "near"),
        "on-tire-far": ("On tires @", "far"),
    }
    definition = role_definitions.get(role)
    if not definition:
        return None
    candidates = _radius_metrics(sheet, definition[0])
    if not candidates:
        return None
    position = definition[1]
    if position == "near":
        return candidates[0][1]
    if position == "far":
        return candidates[-1][1]
    return candidates[len(candidates) // 2][1]


def condition_metric_weights(sheet: CraneSheet, condition: dict[str, Any]) -> dict[str, float]:
    """Resolve each engineering role to an exact source row for this tonnage class."""
    available = {name.lower(): name for name in sheet.parameter_names}
    resolved: dict[str, float] = {}
    if not condition_applicable(sheet, condition):
        return resolved
    for rule, weight in condition.get("metric_rules", []):
        if rule.startswith("role:"):
            name = _role_metric_name(sheet, rule.split(":", 1)[1])
        else:
            name = available.get(rule.lower())
        if name:
            resolved[name] = resolved.get(name, 0.0) + float(weight)
    return resolved


def condition_config_weights(sheet: CraneSheet, condition: dict[str, Any]) -> dict[str, float]:
    available = {name.lower(): name for name in sheet.configuration_names}
    if not condition_applicable(sheet, condition):
        return {}
    return {
        available[name.lower()]: float(weight)
        for name, weight in condition.get("config_rules", [])
        if name.lower() in available
    }


def condition_display_metric_names(sheet: CraneSheet, condition: dict[str, Any]) -> list[str]:
    names = list(condition_metric_weights(sheet, condition))
    available = {name.lower(): name for name in sheet.parameter_names}
    for name in condition.get("context_metrics", []):
        resolved = available.get(name.lower())
        if resolved and resolved not in names:
            names.append(resolved)
    return names


def _metric_score_map(sheet: CraneSheet) -> dict[str, dict[str, float]]:
    result: dict[str, dict[str, float]] = {}
    for metric_name in sheet.parameter_names:
        direction = metric_direction(metric_name)
        if direction is None:
            continue
        values = {}
        for model in sheet.models:
            metric = next((item for item in model.metrics if item.name == metric_name), None)
            values[model.display_name] = metric.numeric_value if metric else None
        result[metric_name] = normalize(values, direction)
    return result


def _category_scores(
    sheet: CraneSheet,
    model_name: str,
    metric_scores: dict[str, dict[str, float]],
) -> tuple[dict[str, float | None], float | None, float]:
    categories: dict[str, float | None] = {}
    category_parts = []
    for category, category_weight in CATEGORY_WEIGHTS.items():
        names = [
            metric.name
            for metric in sheet.models[0].metrics
            if metric.subcategory == category and metric_direction(metric.name) is not None
        ]
        parts = [(metric_scores.get(name, {}).get(model_name), 1.0) for name in names]
        score, _ = weighted_average(parts)
        categories[category] = score
        category_parts.append((score, category_weight))
    total, coverage = weighted_average(category_parts)
    return categories, total, coverage


def _configuration_score(model) -> tuple[float | None, float]:
    parts = [(config.score, 1.0) for config in model.configurations]
    return weighted_average(parts)


def _condition_score_and_detail(
    sheet: CraneSheet,
    model,
    metric_scores: dict[str, dict[str, float]],
    condition: dict[str, Any],
) -> tuple[float | None, dict[str, Any]]:
    if not condition_applicable(sheet, condition):
        return None, {
            "applicable": False,
            "score": None,
            "coverage": 0.0,
            "parameter_score": None,
            "parameter_coverage": 0.0,
            "configuration_score": None,
            "configuration_coverage": 0.0,
            "components": [],
        }

    metric_weights = condition_metric_weights(sheet, condition)
    config_weights = condition_config_weights(sheet, condition)
    metric_parts = [
        (metric_scores.get(name, {}).get(model.display_name), weight)
        for name, weight in metric_weights.items()
    ]
    parameter_score, parameter_coverage = weighted_average(metric_parts)
    valid_metric_count = sum(score is not None for score, _ in metric_parts)
    if valid_metric_count < condition.get("minimum_metric_items", 2):
        parameter_score = None

    config_lookup = {item.name: item for item in model.configurations}
    config_parts = [
        (config_lookup[name].score if name in config_lookup else None, weight)
        for name, weight in config_weights.items()
    ]
    configuration_score, configuration_coverage = weighted_average(config_parts)

    parameter_share = float(condition.get("parameter_share", 0.8)) if metric_weights else 0.0
    configuration_share = float(condition.get("configuration_share", 0.2)) if config_weights else 0.0
    score, coverage = weighted_average(
        [(parameter_score, parameter_share), (configuration_score, configuration_share)]
    )

    total_share = parameter_share + configuration_share
    metric_weight_total = sum(metric_weights.values())
    config_weight_total = sum(config_weights.values())
    components = []
    metric_lookup = {item.name: item for item in model.metrics}
    for name, weight in metric_weights.items():
        item = metric_lookup.get(name)
        component_score = metric_scores.get(name, {}).get(model.display_name)
        effective_weight = (
            parameter_share / total_share * weight / metric_weight_total
            if total_share and metric_weight_total
            else 0.0
        )
        components.append(
            {
                "type": "metric",
                "name": name,
                "source_weight": weight,
                "effective_weight": effective_weight,
                "score": component_score,
                "contribution": component_score * effective_weight if component_score is not None else None,
                "raw_value": item.raw_value if item else None,
                "unit": item.unit if item else "",
                "status": None,
            }
        )
    for name, weight in config_weights.items():
        item = config_lookup.get(name)
        component_score = item.score if item else None
        effective_weight = (
            configuration_share / total_share * weight / config_weight_total
            if total_share and config_weight_total
            else 0.0
        )
        components.append(
            {
                "type": "configuration",
                "name": name,
                "source_weight": weight,
                "effective_weight": effective_weight,
                "score": component_score,
                "contribution": component_score * effective_weight if component_score is not None else None,
                "raw_value": item.raw_status if item else None,
                "unit": "",
                "status": item.normalized_status if item else "unrecorded",
            }
        )
    return score, {
        "applicable": True,
        "score": score,
        "coverage": coverage,
        "parameter_score": parameter_score,
        "parameter_coverage": parameter_coverage,
        "configuration_score": configuration_score,
        "configuration_coverage": configuration_coverage,
        "components": components,
    }


def _condition_scores(
    sheet: CraneSheet,
    model,
    metric_scores: dict[str, dict[str, float]],
) -> tuple[dict[str, float | None], dict[str, dict[str, Any]]]:
    scores: dict[str, float | None] = {}
    details: dict[str, dict[str, Any]] = {}
    for condition in CONDITIONS:
        score, detail = _condition_score_and_detail(sheet, model, metric_scores, condition)
        scores[condition["id"]] = score
        details[condition["id"]] = detail
    return scores, details


def score_sheet(sheet: CraneSheet) -> dict[str, Any]:
    metric_scores = _metric_score_map(sheet)
    products: list[ProductScore] = []
    for model in sheet.models:
        categories, parameter_score, parameter_coverage = _category_scores(
            sheet, model.display_name, metric_scores
        )
        configuration_score, configuration_coverage = _configuration_score(model)
        overall_score = None
        reason = None
        if parameter_score is None:
            reason = "参数有效覆盖率不足60%"
        elif configuration_score is None:
            reason = "配置状态有效覆盖率不足60%"
        else:
            overall_score = (
                parameter_score * OVERALL_WEIGHTS["parameter"]
                + configuration_score * OVERALL_WEIGHTS["configuration"]
            )
        if "suspected_rt130_competitor_headers" in sheet.anomalies:
            overall_score = None
            reason = "竞品表头与数据范围待核验"
        condition_scores, condition_details = _condition_scores(sheet, model, metric_scores)
        products.append(
            ProductScore(
                product=model.display_name,
                brand=model.brand,
                is_xcmg=model.is_xcmg,
                parameter_score=parameter_score,
                parameter_coverage=parameter_coverage,
                configuration_score=configuration_score,
                configuration_coverage=configuration_coverage,
                overall_score=overall_score,
                overall_rank=None,
                category_scores=categories,
                condition_scores=condition_scores,
                condition_details=condition_details,
                not_ranked_reason=reason,
            )
        )
    ranked = sorted(
        (product for product in products if product.overall_score is not None),
        key=lambda product: product.overall_score,
        reverse=True,
    )
    for rank, product in enumerate(ranked, 1):
        product.overall_rank = rank
        product.not_ranked_reason = None
    return {
        "sheet": sheet.label,
        "minimum_score_coverage": MIN_SCORE_COVERAGE,
        "overall_weights": OVERALL_WEIGHTS,
        "category_weights": CATEGORY_WEIGHTS,
        "conditions": CONDITIONS,
        "metric_scores": metric_scores,
        "products": [asdict(product) for product in products],
    }


def score_workbook() -> dict[str, Any]:
    workbook = load_crane_workbook()
    return {sheet.label: score_sheet(sheet) for sheet in workbook.sheets}


if __name__ == "__main__":
    import json

    print(json.dumps(score_workbook(), ensure_ascii=False, indent=2))
