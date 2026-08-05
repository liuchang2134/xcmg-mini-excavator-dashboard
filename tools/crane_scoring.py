from __future__ import annotations

import math
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
        "id": "transport",
        "title_zh": "道路转场 / 运输合规",
        "title_en": "Road Transport / Compliance",
        "metric_patterns": [
            "minimum transport weight",
            "transport width",
            "transport height",
            "transport length",
            "removable cwt",
            "number of cwt configurations",
            "speed with max cwt",
        ],
        "config_patterns": ["tow hooks", "cribbing rack"],
    },
    {
        "id": "mobility",
        "title_zh": "场地进出 / 越野机动",
        "title_en": "Site Access / Rough-Terrain Mobility",
        "metric_patterns": [
            "speed",
            "wheelbase",
            "number of steering modes",
            "minimum turning radius",
            "gradability",
            "front approach angle",
            "rear approach angle",
            "number of drive axles",
            "number of steering axles",
        ],
        "config_patterns": ["tires"],
    },
    {
        "id": "main-lift",
        "title_zh": "主臂吊装 / 中近幅度",
        "title_en": "Main-Boom Lifting / Near-to-Mid Radius",
        "metric_patterns": [
            "maximum capacity w/o special equipment",
            "main boom @ 5m",
            "main boom @ 15m",
            "main boom @ 30m",
            "main winch max line pull",
            "main winch max speed",
            "boom raise speed",
        ],
        "config_patterns": ["auto winch and boom control"],
    },
    {
        "id": "long-reach",
        "title_zh": "长臂大幅度 / 高空吊装",
        "title_en": "Long-Reach / High-Elevation Lifting",
        "metric_patterns": [
            "extended boom length",
            "max jib carried on crane",
            "jib extensions",
            "jib offset angles",
            "main boom max rated radius",
            "main boom @ max radius",
            "jib w/o inserts @ 20m",
            "jib w/o inserts @ 30m",
            "jib w/o inserts max radius",
            "boom extend speed",
        ],
        "config_patterns": ["short jib", "short heavy lift jib"],
    },
    {
        "id": "stability",
        "title_zh": "支腿展开 / 不平地面稳定",
        "title_en": "Outrigger Setup / Uneven-Ground Stability",
        "metric_patterns": [
            "outrigger penetration",
            "full outrigger extension",
            "number of outrigger extensions",
            "asymmetric outrigger operation",
            "pick and carry @ 5m",
            "on tires @ 3m over front",
            "on tires @ 7m over front",
        ],
        "config_patterns": ["2deg out of level load charts", "360deg house lock"],
    },
    {
        "id": "continuous-duty",
        "title_zh": "连续作业 / 低温与附件适配",
        "title_en": "Continuous Duty / Cold-Weather and Attachments",
        "metric_patterns": [
            "engine power",
            "engine torque",
            "fuel tank",
            "aux winch max line pull",
            "aux winch max speed",
            "swing speed",
        ],
        "config_patterns": [
            "auto lubrication system",
            "fuel engine heater",
            "cold weather package",
            "greasless boom",
        ],
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
    "outrigger penetration",
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


def _condition_scores(
    sheet: CraneSheet,
    model,
    metric_scores: dict[str, dict[str, float]],
) -> dict[str, float | None]:
    scores = {}
    for condition in CONDITIONS:
        metric_names = [
            metric.name
            for metric in model.metrics
            if any(pattern in metric.name.lower() for pattern in condition["metric_patterns"])
            and metric_direction(metric.name) is not None
        ]
        config_items = [
            config
            for config in model.configurations
            if any(pattern in config.name.lower() for pattern in condition["config_patterns"])
        ]
        metric_weight = 0.8 / len(metric_names) if metric_names else 0.0
        config_weight = 0.2 / len(config_items) if config_items else 0.0
        parts = [
            (metric_scores.get(name, {}).get(model.display_name), metric_weight)
            for name in metric_names
        ]
        parts.extend((config.score, config_weight) for config in config_items)
        score, _ = weighted_average(parts)
        scores[condition["id"]] = score
    return scores


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
                condition_scores=_condition_scores(sheet, model, metric_scores),
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
