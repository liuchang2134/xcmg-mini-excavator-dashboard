from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "data" / "source-excel" / "XCMG_crane_benchmark_data_pool.xlsx"
DEFAULT_OUTPUT = ROOT / "data" / "generated" / "cranes" / "crane-benchmark.json"
EXPECTED_SHA256 = "0DF8DDC77F1F8018861204BEE4A8BAEEEDC65745302D51430CE51A7FD9005898"

CRANE_SHEETS = {
    "RT-60t": {"family": "RT", "tonnage": "60t", "xcmg": "XCMG XCR60U"},
    "RT-75t ": {"family": "RT", "tonnage": "75t", "xcmg": "XCMG XCR75U"},
    "RT-100t": {"family": "RT", "tonnage": "100t", "xcmg": "XCMG XCR100U"},
    "RT-130t": {"family": "RT", "tonnage": "130t", "xcmg": "XCMG XCR130U"},
    "RT-160t": {"family": "RT", "tonnage": "160t", "xcmg": "XCMG XCR165U"},
    "AT-150t": {"family": "AT", "tonnage": "150t", "xcmg": "XCMG XCA150U"},
}

EXCLUDED_SHEETS = {"Sheet1", "5-6", "6-7 缺", "40-60", "总结"}


@dataclass
class CraneMetric:
    category: str
    subcategory: str
    name: str
    unit: str
    raw_value: Any
    numeric_value: float | None
    source_row: int


@dataclass
class CraneConfiguration:
    name: str
    raw_status: str | None
    normalized_status: str
    score: float | None
    source_row: int


@dataclass
class CraneModel:
    brand: str
    model: str
    display_name: str
    source_column: int
    is_xcmg: bool
    metrics: list[CraneMetric] = field(default_factory=list)
    configurations: list[CraneConfiguration] = field(default_factory=list)
    parameter_coverage: float = 0.0
    configuration_coverage: float = 0.0
    anomalies: list[str] = field(default_factory=list)


@dataclass
class CraneSheet:
    source_sheet: str
    label: str
    family: str
    tonnage: str
    xcmg_model: str
    updated_at: str | None
    parameter_names: list[str]
    configuration_names: list[str]
    characteristic_names: list[str]
    models: list[CraneModel]
    anomalies: list[str]


@dataclass
class CraneWorkbook:
    source_file: str
    sha256: str
    sheets: list[CraneSheet]
    excluded_sheets: list[str]
    anomalies: list[str]


def workbook_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _clean_text(value: Any) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    return " ".join(str(value).replace("\r", " ").replace("\n", " ").split())


def _json_value(value: Any) -> Any:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def parse_numeric(value: Any) -> float | None:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = _clean_text(value).replace(",", "")
    if not text or text in {"/", "-", "--"}:
        return None
    # Avoid inventing a scalar from ranges, multiple configurations, ratios, or dimensions.
    number_tokens = re.findall(r"[-+]?\d+(?:\.\d+)?", text)
    if len(number_tokens) != 1:
        return None
    if re.search(r"\d\s*[x×/]\s*\d", text, re.IGNORECASE):
        return None
    try:
        return float(number_tokens[0])
    except ValueError:
        return None


def parse_model_header(value: Any) -> tuple[str, str, str]:
    text = _clean_text(value)
    parts = [part.strip() for part in re.split(r"\s*/\s*", text) if part.strip()]
    if len(parts) >= 2:
        brand = parts[0]
        model = " / ".join(parts[1:])
    else:
        tokens = text.split(maxsplit=1)
        brand = tokens[0] if tokens else ""
        model = tokens[1] if len(tokens) > 1 else text
    brand_aliases = {
        "Linkbelt": "Link-Belt",
        "XCMG": "XCMG",
        "Tadano": "Tadano",
        "Grove": "Grove",
        "Liebherr": "Liebherr",
        "Terex": "Terex",
        "Zoomlion": "Zoomlion",
        "Sany": "Sany",
    }
    brand = brand_aliases.get(brand, brand)
    display = f"{brand} {model}".strip()
    return brand, model, display


def normalize_configuration(value: Any) -> tuple[str | None, str, float | None]:
    raw = _clean_text(value)
    if not raw or raw in {"/", "-", "--"}:
        return (raw or None, "unrecorded", None)
    lower = raw.lower()
    if re.search(r"\b(?:none|no|absent|not available|n/a)\b", lower):
        return (raw, "absent", 0.0)
    if re.search(r"\b(?:opt|option|optional)\b", lower):
        return (raw, "optional", 60.0)
    if re.search(r"\b(?:std|standard|yes|y|included)\b", lower):
        return (raw, "standard", 100.0)
    # Descriptions such as "front and rear" prove presence but not whether it is standard.
    return (raw, "present_unspecified", None)


def _find_marker(frame: pd.DataFrame, marker: str) -> int:
    for index, value in enumerate(frame.iloc[:, 0].tolist()):
        if _clean_text(value).lower() == marker.lower():
            return index
    raise ValueError(f"Required section marker not found: {marker}")


def _model_columns(frame: pd.DataFrame) -> list[tuple[int, str]]:
    columns: list[tuple[int, str]] = []
    scoring_boundary = frame.shape[1]
    for column in range(4, frame.shape[1]):
        if _clean_text(frame.iat[0, column]).lower().startswith("scoring:"):
            scoring_boundary = column
            break
    for column in range(4, scoring_boundary):
        header = _clean_text(frame.iat[0, column])
        if header and header.lower() != "score":
            columns.append((column, header))
    return columns


def _source_date(frame: pd.DataFrame) -> str | None:
    for row in range(frame.shape[0]):
        if _clean_text(frame.iat[row, 0]).lower() == "updated:":
            value = frame.iat[row, 1]
            return _json_value(value)
    return None


def _parse_sheet(frame: pd.DataFrame, source_sheet: str, meta: dict[str, str]) -> CraneSheet:
    parameter_start = _find_marker(frame, "Parameter Comparison")
    configuration_start = _find_marker(frame, "Standard/Optional Config")
    characteristic_start = _find_marker(frame, "Six Characteristics")
    model_columns = _model_columns(frame)
    if not model_columns:
        raise ValueError(f"No crane model columns found in {source_sheet}")

    parameter_rows: list[dict[str, Any]] = []
    subcategory = ""
    for row in range(parameter_start, configuration_start):
        new_subcategory = _clean_text(frame.iat[row, 1])
        if new_subcategory:
            subcategory = new_subcategory
        name = _clean_text(frame.iat[row, 2])
        if not name:
            continue
        parameter_rows.append(
            {
                "row": row,
                "subcategory": subcategory or "Uncategorized",
                "name": name,
                "unit": _clean_text(frame.iat[row, 3]),
            }
        )

    configuration_rows: list[dict[str, Any]] = []
    for row in range(configuration_start + 1, characteristic_start):
        name = _clean_text(frame.iat[row, 2])
        if name:
            configuration_rows.append({"row": row, "name": name})

    characteristic_names = []
    for row in range(characteristic_start, min(characteristic_start + 8, frame.shape[0])):
        name = _clean_text(frame.iat[row, 1])
        if name:
            characteristic_names.append(name)

    models: list[CraneModel] = []
    for column, header in model_columns:
        brand, model_name, display = parse_model_header(header)
        model = CraneModel(
            brand=brand,
            model=model_name,
            display_name=display,
            source_column=column + 1,
            is_xcmg=brand.upper() == "XCMG",
        )
        for item in parameter_rows:
            raw = frame.iat[item["row"], column]
            model.metrics.append(
                CraneMetric(
                    category="Parameter Comparison",
                    subcategory=item["subcategory"],
                    name=item["name"],
                    unit=item["unit"],
                    raw_value=_json_value(raw),
                    numeric_value=parse_numeric(raw),
                    source_row=item["row"] + 1,
                )
            )
        for item in configuration_rows:
            raw, status, score = normalize_configuration(frame.iat[item["row"], column])
            model.configurations.append(
                CraneConfiguration(
                    name=item["name"],
                    raw_status=raw,
                    normalized_status=status,
                    score=score,
                    source_row=item["row"] + 1,
                )
            )
        model.parameter_coverage = (
            sum(metric.raw_value is not None for metric in model.metrics) / len(model.metrics)
            if model.metrics
            else 0.0
        )
        model.configuration_coverage = (
            sum(config.normalized_status != "unrecorded" for config in model.configurations)
            / len(model.configurations)
            if model.configurations
            else 0.0
        )
        if model.parameter_coverage == 0:
            model.anomalies.append("no_parameter_data")
        elif model.parameter_coverage < 0.6:
            model.anomalies.append("low_parameter_coverage")
        if model.configuration_coverage < 0.6:
            model.anomalies.append("low_configuration_coverage")
        models.append(model)

    anomalies: list[str] = []
    right_headers = " ".join(_clean_text(value) for value in frame.iloc[0].tolist())
    right_content = " ".join(
        _clean_text(frame.iat[row, column])
        for row in range(frame.shape[0])
        for column in range(max(0, frame.shape[1] - 15), frame.shape[1])
    )
    if "Scoring: Industry avg=3" in right_headers and "XE19U" in right_content:
        anomalies.append("stale_excavator_scoring_block_excluded")
    if meta["family"] == "AT" and any("GR-1300" in model.display_name for model in models):
        anomalies.append("suspected_rt130_competitor_headers")
    xcmg = next((model for model in models if model.is_xcmg), None)
    if xcmg is None:
        anomalies.append("xcmg_model_missing")
    elif xcmg.parameter_coverage == 0:
        anomalies.append("xcmg_parameter_data_missing")
    if not any(not model.is_xcmg and model.parameter_coverage >= 0.6 for model in models):
        anomalies.append("no_rankable_competitor")

    return CraneSheet(
        source_sheet=source_sheet,
        label=source_sheet.strip(),
        family=meta["family"],
        tonnage=meta["tonnage"],
        xcmg_model=meta["xcmg"],
        updated_at=_source_date(frame),
        parameter_names=[item["name"] for item in parameter_rows],
        configuration_names=[item["name"] for item in configuration_rows],
        characteristic_names=characteristic_names,
        models=models,
        anomalies=anomalies,
    )


def load_crane_workbook(path: Path = DEFAULT_SOURCE) -> CraneWorkbook:
    path = Path(path)
    excel = pd.ExcelFile(path)
    missing = sorted(set(CRANE_SHEETS) - set(excel.sheet_names))
    if missing:
        raise ValueError(f"Missing required crane sheets: {missing}")
    sheets = []
    for source_sheet, meta in CRANE_SHEETS.items():
        frame = pd.read_excel(path, sheet_name=source_sheet, header=None, dtype=object)
        sheets.append(_parse_sheet(frame, source_sheet, meta))
    excluded = sorted(set(excel.sheet_names) & EXCLUDED_SHEETS)
    anomalies = []
    digest = workbook_sha256(path)
    if digest != EXPECTED_SHA256:
        anomalies.append("source_fingerprint_changed")
    return CraneWorkbook(
        source_file=path.name,
        sha256=digest,
        sheets=sheets,
        excluded_sheets=excluded,
        anomalies=anomalies,
    )


def workbook_to_dict(workbook: CraneWorkbook) -> dict[str, Any]:
    return asdict(workbook)


def write_crane_json(
    workbook: CraneWorkbook,
    output: Path = DEFAULT_OUTPUT,
) -> Path:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = workbook_to_dict(workbook)
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return output


if __name__ == "__main__":
    write_crane_json(load_crane_workbook())
