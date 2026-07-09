import html
import json
import math
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
ASSET_DIR = ROOT / "assets" / "arc"


SOURCE_FILES = [
    {
        "slug": "excavator-1-2t",
        "label": "1-2 吨级",
        "title": "XCMG XE19U 1-2 吨级小挖竞品分析看板",
        "xcmg": "XCMG XE19U",
        "source": Path(r"C:\Users\xcmgusa\Downloads\1-2.xlsx"),
        "download": "1-2.xlsx",
        "image": "assets/arc/xe19u-official-cropped.png",
        "image_source": "XCMG Australia XE19U",
    },
    {
        "slug": "excavator-2-3t",
        "label": "2-3 吨级",
        "title": "XCMG XE27U 2-3 吨级小挖竞品分析看板",
        "xcmg": "XCMG XE27U",
        "source": Path(r"C:\Users\xcmgusa\Downloads\2-3.xlsx"),
        "download": "2-3.xlsx",
        "image": "assets/arc/xe27u-official-cropped.jpg",
        "image_source": "XCMG USA XE27U",
    },
]


CONDITIONS = [
    {
        "id": "narrow",
        "name": "狭窄空间 / 市政庭院",
        "weight": 0.18,
        "feature": "看重窄机身、短尾回转、低运输尺寸和边角贴墙作业能力。",
        "benefit": "可伸缩底盘、动臂偏摆、推土铲偏摆、后视安全配置对庭院和市政抢修更有价值。",
        "items": [
            ("参数", "整机运输宽度", 0.18, "low", "越窄越适合入户、园林和人行道受限空间。"),
            ("参数", "整机运输长度", 0.12, "low", "短车身转场和狭小现场调头更灵活。"),
            ("参数", "尾部回转半径", 0.24, "low", "尾扫越小越不容易碰墙、碰车和碰围挡。"),
            ("参数", "动臂偏摆（左/右）", 0.18, "swing", "越能贴边开沟、贴墙清底，狭窄空间收益越高。"),
            ("配置", "可伸缩底盘", 0.08, "option", "窄处收窄、开阔处展开，兼顾通过性和稳定性。"),
            ("配置", "推土铲偏摆", 0.07, "option", "角落回填和边沟修整时减少重复调车。"),
            ("配置", "后视摄像头", 0.06, "option", "城市巷道和庭院倒车安全配置。"),
            ("配置", "行走报警", 0.04, "option", "人车混行环境降低安全风险。"),
            ("配置", "报警灯", 0.03, "option", "市政施工和租赁场景提高周边可感知性。"),
        ],
    },
    {
        "id": "trench",
        "name": "沟槽 / 基础深挖",
        "weight": 0.20,
        "feature": "核心是下挖深度、挖掘半径、斗杆挖掘力和长斗杆覆盖能力。",
        "benefit": "长斗杆、AUX 管路和动臂斗杆防爆阀有助于深沟、管线和基础作业。",
        "items": [
            ("参数", "最大挖掘深度", 0.28, "high", "深度决定基础沟槽和管线施工覆盖范围。"),
            ("参数", "最大挖掘半径", 0.14, "high", "半径越大，站位不变时覆盖面越宽。"),
            ("参数", "最大地面挖掘半径", 0.12, "high", "平面沟槽连续开挖效率更高。"),
            ("参数", "斗杆挖掘力", 0.12, "high", "深挖末端破土和清底能力。"),
            ("参数", "标配斗杆", 0.08, "high", "斗杆长度影响天然深挖覆盖。"),
            ("参数", "选配斗杆", 0.06, "high", "选配斗杆说明是否可向深挖场景扩展。"),
            ("配置", "长斗杆", 0.08, "option", "深沟和管线施工直接增益配置。"),
            ("配置", "动臂斗杆防爆阀", 0.06, "option", "基础施工和吊装附近作业的安全配置。"),
            ("配置", "AUX1管路", 0.04, "option", "便于搭配夯实、破碎和清沟属具。"),
            ("配置", "AUX2管路", 0.02, "option", "旋转类属具扩展能力。"),
        ],
    },
    {
        "id": "loading",
        "name": "土方装车 / 短循环效率",
        "weight": 0.18,
        "feature": "看卸载高度、挖掘力、液压流量、回转和行走响应。",
        "benefit": "经济模式、自动怠速、推土铲浮动和快换管路影响短循环油耗与辅助动作效率。",
        "items": [
            ("参数", "最大卸载高度", 0.18, "high", "影响能否顺利装车和越过车厢。"),
            ("参数", "铲斗挖掘力", 0.13, "high", "装料、切土和短循环满斗能力。"),
            ("参数", "斗杆挖掘力", 0.08, "high", "连续挖装时保持切入力。"),
            ("参数", "系统流量", 0.14, "high", "复合动作速度与液压响应。"),
            ("参数", "发动机净功率", 0.10, "high", "连续循环中的动力储备。"),
            ("参数", "发动机总功率", 0.08, "high", "动力系统基础能力。"),
            ("参数", "行走速度（低速/高速）", 0.07, "high", "场内短距离转场效率。"),
            ("参数", "回转速度", 0.07, "high", "短循环挖装回转效率。"),
            ("配置", "经济模式", 0.05, "option", "轻载和市政土方循环中控制油耗。"),
            ("配置", "自动怠速", 0.04, "option", "等待装车和短暂停顿时降低怠速油耗。"),
            ("配置", "推土铲浮动", 0.03, "option", "回填、整平、清底动作效率更高。"),
            ("配置", "快换管路", 0.03, "option", "多属具切换减少停机时间。"),
        ],
    },
    {
        "id": "attachment",
        "name": "破碎 / 多属具作业",
        "weight": 0.16,
        "feature": "重点是液压系统流量、压力和 AUX 管路覆盖。",
        "benefit": "AUX1/AUX2、卸油管路、流量保持和快换管路决定破碎锤、拇指夹、螺旋钻等属具适配效率。",
        "items": [
            ("参数", "系统流量", 0.14, "high", "液压属具连续工作基础。"),
            ("参数", "工作压力", 0.12, "high", "破碎、夹持和钻孔属具输出能力。"),
            ("参数", "AUX1流量", 0.14, "high", "主属具回路供油能力。"),
            ("参数", "AUX1压力", 0.10, "high", "主属具负载能力。"),
            ("参数", "AUX2流量", 0.08, "high", "旋转/夹持类辅回路能力。"),
            ("参数", "AUX2压力", 0.08, "high", "辅回路属具稳定性。"),
            ("配置", "AUX1管路", 0.10, "option", "破碎锤和常规属具基础配置。"),
            ("配置", "AUX2管路", 0.08, "option", "旋转夹、拇指夹等复合属具更友好。"),
            ("配置", "卸油管路", 0.06, "option", "破碎锤回油保护和热管理。"),
            ("配置", "流量保持", 0.05, "option", "连续属具输出更稳定。"),
            ("配置", "快换管路", 0.05, "option", "多属具场景减少切换时间。"),
        ],
    },
    {
        "id": "slope",
        "name": "坡地 / 软土 / 吊装稳定",
        "weight": 0.14,
        "feature": "关注接地比压、履带宽度、牵引、爬坡和起吊能力。",
        "benefit": "副配重、推土铲浮动、驾驶室安全和行走报警可以增强坡地和吊装边界。",
        "items": [
            ("参数", "履带宽度", 0.09, "high", "宽履带降低陷车风险并提升侧向稳定性。"),
            ("参数", "接地比压", 0.14, "low", "越低越适合软土、草地和回填土表面。"),
            ("参数", "最大牵引力", 0.13, "high", "坡地转场和湿软场地脱困能力。"),
            ("参数", "爬坡能力", 0.13, "high", "坡地作业和上下车能力。"),
            ("参数", "地面正前方3m远处起吊能力（放下推土铲）", 0.18, "high", "放铲吊装代表稳定边界。"),
            ("参数", "地面正前方3m远处起吊能力（抬起推土铲）", 0.12, "high", "无支撑状态下的保守吊装能力。"),
            ("参数", "地面侧方3m远处起吊能力", 0.12, "high", "侧方吊装稳定性。"),
            ("配置", "副配重", 0.05, "option", "提升尾部稳定性和吊装边界。"),
            ("配置", "推土铲浮动", 0.04, "option", "整平和坡面贴合更容易。"),
        ],
    },
    {
        "id": "rental",
        "name": "租赁 / 快速转场 / 多客户通用",
        "weight": 0.14,
        "feature": "看运输尺寸、油耗管理、易用性、安全提醒和远程管理。",
        "benefit": "自动怠速、自动停机、远程信息处理、报警灯、行走报警和驾驶舒适配置直接影响租赁周转。",
        "items": [
            ("参数", "整机运输宽度", 0.12, "low", "拖车、仓库和门洞通过性。"),
            ("参数", "整机运输长度", 0.10, "low", "拖车装载和仓储占地。"),
            ("参数", "整机运输高度", 0.08, "low", "低矮通道和运输合规性。"),
            ("参数", "操作重量", 0.08, "low", "拖车级别和租赁客户自提门槛。"),
            ("参数", "行走速度（低速/高速）", 0.08, "high", "场内转场效率。"),
            ("配置", "自动怠速", 0.08, "option", "降低怠速油耗和新手误操作成本。"),
            ("配置", "自动停机", 0.09, "option", "降低无效怠速、油耗和租赁客户使用成本。"),
            ("配置", "远程信息处理系统", 0.09, "option", "定位、工时、维保和资产管理。"),
            ("配置", "密码防盗", 0.05, "option", "租赁资产防盗。"),
            ("配置", "密码启动", 0.05, "option", "租赁资产防盗。"),
            ("配置", "一键启动", 0.04, "option", "多客户使用更方便。"),
            ("配置", "USB电源", 0.03, "option", "基础便利配置。"),
            ("配置", "蓝牙收音机", 0.03, "option", "驾驶舒适性。"),
            ("配置", "手机托", 0.03, "option", "租赁客户通用便利性。"),
            ("配置", "报警灯", 0.04, "option", "工地安全可视化。"),
            ("配置", "行走报警", 0.04, "option", "人员密集场景安全提醒。"),
            ("配置", "驾驶室冷暖空调", 0.04, "option", "租赁客户跨季节适用。"),
            ("配置", "驾驶室版本制热", 0.02, "option", "低温地区租赁适配。"),
            ("配置", "驾驶室版本制冷", 0.02, "option", "高温地区租赁适配。"),
        ],
    },
]


PARAM_CATEGORY_WEIGHTS = {
    "运输参数": 0.12,
    "接地参数": 0.08,
    "工作参数": 0.18,
    "动力": 0.08,
    "工作装置": 0.08,
    "液压系统": 0.16,
    "行走": 0.10,
    "回转": 0.07,
    "挖掘力": 0.08,
    "起吊能力": 0.05,
}

OPTION_CATEGORY_WEIGHTS = {
    "发动机": 0.12,
    "液压系统": 0.24,
    "驾驶环境": 0.18,
    "电器系统": 0.18,
    "工装底盘": 0.28,
}


LOWER_BETTER = {"整机运输宽度", "整机运输高度", "整机运输长度", "尾部回转半径", "接地比压"}
HIGHER_BETTER = {
    "最大挖掘高度",
    "最大卸载高度",
    "最大挖掘深度",
    "最大挖掘半径",
    "最大地面挖掘半径",
    "发动机总功率",
    "发动机净功率",
    "标配斗杆",
    "标配动臂",
    "选配斗杆",
    "系统流量",
    "工作压力",
    "行走压力",
    "回转压力",
    "AUX1流量",
    "AUX1压力",
    "AUX2流量",
    "AUX2压力",
    "行走速度（低速/高速）",
    "最大牵引力",
    "爬坡能力",
    "回转速度",
    "动臂偏摆（左/右）",
    "铲斗挖掘力",
    "斗杆挖掘力",
    "地面正前方3m远处起吊能力（放下推土铲）",
    "地面正前方3m远处起吊能力（抬起推土铲）",
    "地面侧方3m远处起吊能力",
    "轨距",
    "履带长度",
    "履带宽度",
}


COLORS = ["#f5b400", "#00529b", "#2176bd", "#009a76", "#d64f4f", "#6a55cc", "#00a6b6", "#7a8da5", "#873c71", "#2b7a4b", "#9a6a00"]


@dataclass
class WorkbookData:
    products: list
    param_rows: list
    option_rows: list
    param_map: dict
    option_map: dict


def clean(v):
    if pd.isna(v):
        return ""
    text = str(v).strip()
    if text.lower() == "nan":
        return ""
    return text


def esc(value):
    return html.escape(str(value), quote=True)


def fmt_score(value):
    if value is None or math.isnan(value):
        return "-"
    return f"{value:.1f}".rstrip("0").rstrip(".")


def extract_numbers(value):
    text = clean(value)
    if not text or text in {"/", "-", "—"}:
        return []
    text = text.replace("，", ",")
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", text)]


def parse_metric_value(value, direction):
    text = clean(value)
    nums = extract_numbers(text)
    if not nums:
        return None
    if direction == "swing":
        groups = re.split(r"[;；\n]+", text)
        best = None
        for group in groups:
            gnums = [abs(x) for x in extract_numbers(group) if abs(x) <= 180]
            if len(gnums) >= 2:
                candidate = gnums[0] + gnums[1]
            elif gnums:
                candidate = gnums[0]
            else:
                continue
            best = candidate if best is None else max(best, candidate)
        return best
    if direction == "low":
        positives = [x for x in nums if x >= 0]
        return min(positives) if positives else min(nums)
    return max(nums)


def option_score(value):
    text = clean(value)
    if not text or text in {"/", "-", "—", "nan"}:
        return 0
    if "标配" in text:
        return 100
    if "选配" in text:
        return 60
    if "可选" in text:
        return 60
    if "无" in text:
        return 0
    return 40


def option_status(value):
    score = option_score(value)
    if score >= 100:
        return "标配"
    if score >= 60:
        return "选配"
    if score > 0:
        return "需确认"
    return "无配置"


def score_class(score):
    if score is None:
        return "missing"
    if score >= 70:
        return "good"
    if score >= 45:
        return "mid"
    return "bad"


def load_workbook(path):
    param = pd.read_excel(path, sheet_name=0, header=None)
    option = pd.read_excel(path, sheet_name=1, header=None)
    products = [clean(x) for x in param.iloc[0, 3:].tolist() if clean(x)]

    param_rows, param_map = [], {}
    category = ""
    for _, row in param.iloc[1:].iterrows():
        if clean(row.iloc[0]):
            category = clean(row.iloc[0])
        item = clean(row.iloc[1])
        if not item:
            continue
        unit = clean(row.iloc[2])
        values = {p: clean(v) for p, v in zip(products, row.iloc[3:].tolist())}
        rec = {"category": category, "item": item, "unit": unit, "values": values}
        param_rows.append(rec)
        param_map[item] = rec

    option_rows, option_map = [], {}
    category = ""
    opt_products = [clean(x) for x in option.iloc[0, 2:].tolist() if clean(x)]
    if opt_products != products:
        products = opt_products
    for _, row in option.iloc[1:].iterrows():
        if clean(row.iloc[0]):
            category = clean(row.iloc[0])
        item = clean(row.iloc[1])
        if not item:
            continue
        values = {p: clean(v) for p, v in zip(products, row.iloc[2:].tolist())}
        rec = {"category": category, "item": item, "unit": "配置", "values": values}
        option_rows.append(rec)
        option_map[item] = rec

    return WorkbookData(products, param_rows, option_rows, param_map, option_map)


def normalize(values, direction):
    valid = {k: v for k, v in values.items() if v is not None and not math.isnan(v)}
    if not valid:
        return {}
    lo, hi = min(valid.values()), max(valid.values())
    if abs(hi - lo) < 1e-9:
        return {k: 100.0 for k in valid}
    if direction == "low":
        return {k: (hi - v) / (hi - lo) * 100 for k, v in valid.items()}
    return {k: (v - lo) / (hi - lo) * 100 for k, v in valid.items()}


def weighted_average(parts):
    valid = [(score, weight) for score, weight in parts if score is not None and weight > 0]
    if not valid:
        return None
    total_weight = sum(weight for _, weight in valid)
    return sum(score * weight for score, weight in valid) / total_weight


def condition_scores(wb):
    result = {}
    details = {}
    for condition in CONDITIONS:
        raw_details = []
        product_parts = {p: [] for p in wb.products}
        for typ, item, weight, direction, note in condition["items"]:
            if typ == "参数":
                rec = wb.param_map.get(item)
                if not rec:
                    continue
                metric_values = {p: parse_metric_value(rec["values"].get(p), direction) for p in wb.products}
                norm = normalize(metric_values, "low" if direction == "low" else "high")
                for p in wb.products:
                    score = norm.get(p)
                    if score is not None:
                        product_parts[p].append((score, weight))
                raw_details.append({
                    "type": typ,
                    "category": rec["category"],
                    "item": item,
                    "unit": rec["unit"],
                    "direction": "越低越好" if direction == "low" else "越高越好",
                    "weight": weight,
                    "note": note,
                    "values": rec["values"],
                    "scores": {p: norm.get(p) for p in wb.products},
                })
            else:
                rec = wb.option_map.get(item)
                if not rec:
                    continue
                scores = {p: option_score(rec["values"].get(p)) for p in wb.products}
                for p in wb.products:
                    product_parts[p].append((scores[p], weight))
                raw_details.append({
                    "type": typ,
                    "category": rec["category"],
                    "item": item,
                    "unit": "配置",
                    "direction": "标配>选配>无",
                    "weight": weight,
                    "note": note,
                    "values": rec["values"],
                    "scores": scores,
                })
        scores = {p: weighted_average(product_parts[p]) for p in wb.products}
        result[condition["id"]] = scores
        details[condition["id"]] = raw_details
    return result, details


def category_scores(wb, rows, weights, is_option=False):
    by_cat = {cat: [] for cat in weights}
    metric_detail = []
    for row in rows:
        cat = row["category"]
        if cat not in by_cat:
            continue
        item = row["item"]
        if is_option:
            scores = {p: option_score(row["values"].get(p)) for p in wb.products}
        else:
            if item in LOWER_BETTER:
                direction = "low"
            else:
                direction = "swing" if item == "动臂偏摆（左/右）" else "high"
            vals = {p: parse_metric_value(row["values"].get(p), direction) for p in wb.products}
            scores = normalize(vals, "low" if direction == "low" else "high")
        by_cat[cat].append((item, scores))
        metric_detail.append((cat, item, scores))

    product_category_scores = {p: {} for p in wb.products}
    for cat, items in by_cat.items():
        for p in wb.products:
            vals = [(scores.get(p), 1) for _, scores in items if scores.get(p) is not None]
            product_category_scores[p][cat] = weighted_average(vals)

    product_scores = {}
    for p in wb.products:
        product_scores[p] = weighted_average([(product_category_scores[p].get(cat), w) for cat, w in weights.items()])
    return product_scores, product_category_scores


def build_model(wb, meta):
    cond_scores, cond_details = condition_scores(wb)
    param_score, param_categories = category_scores(wb, wb.param_rows, PARAM_CATEGORY_WEIGHTS, is_option=False)
    option_score_map, option_categories = category_scores(wb, wb.option_rows, OPTION_CATEGORY_WEIGHTS, is_option=True)
    condition_total = {}
    for p in wb.products:
        condition_total[p] = weighted_average([(cond_scores[c["id"]].get(p), c["weight"]) for c in CONDITIONS])
    overall = {
        p: weighted_average([
            (condition_total.get(p), 0.50),
            (param_score.get(p), 0.30),
            (option_score_map.get(p), 0.20),
        ])
        for p in wb.products
    }
    return {
        "meta": meta,
        "products": wb.products,
        "colors": {p: COLORS[i % len(COLORS)] for i, p in enumerate(wb.products)},
        "conditions": CONDITIONS,
        "conditionScores": cond_scores,
        "conditionDetails": cond_details,
        "conditionTotal": condition_total,
        "paramScore": param_score,
        "optionScore": option_score_map,
        "overall": overall,
        "paramCategories": param_categories,
        "optionCategories": option_categories,
        "rawParamRows": wb.param_rows,
        "rawOptionRows": wb.option_rows,
    }


def ranking(scores):
    return sorted(
        [{"product": p, "score": s} for p, s in scores.items() if s is not None],
        key=lambda x: x["score"],
        reverse=True,
    )


def xcmg_rank(scores, xcmg):
    rows = ranking(scores)
    for i, row in enumerate(rows, start=1):
        if row["product"] == xcmg:
            return i, row["score"], rows
    return None, None, rows


def table_rows(rows, products, limit=None):
    out = []
    for row in rows[: limit or len(rows)]:
        cells = "".join(f"<td>{esc(row['values'].get(p, '')) or '-'}</td>" for p in products)
        out.append(f"<tr><td>{esc(row['category'])}</td><td>{esc(row['item'])}</td><td>{esc(row.get('unit',''))}</td>{cells}</tr>")
    return "\n".join(out)


def render_bar_ranking(scores, xcmg, max_rows=None):
    rows = ranking(scores)[: max_rows or 99]
    max_score = max([r["score"] for r in rows] + [1])
    html_rows = []
    for idx, row in enumerate(rows, start=1):
        cls = "bar xcmg" if row["product"] == xcmg else "bar"
        width = max(2, row["score"] / max_score * 100)
        html_rows.append(
            f'<div class="{cls}"><span>{idx}</span><b>{esc(row["product"])}</b>'
            f'<i><em style="width:{width:.1f}%"></em></i><strong>{fmt_score(row["score"])}</strong></div>'
        )
    return "".join(html_rows)


def render_radar(model, score_map, title, small=False):
    products = model["products"]
    conditions = model["conditions"]
    colors = model["colors"]
    axes = [c["name"].split(" / ")[0] for c in conditions]
    if len(axes) < 3:
        return ""
    size = 420 if not small else 340
    cx = cy = size / 2
    radius = size * 0.34
    axis_count = len(axes)

    def point(idx, value):
        angle = -math.pi / 2 + idx * 2 * math.pi / axis_count
        r = radius * max(0, min(100, value)) / 100
        return cx + math.cos(angle) * r, cy + math.sin(angle) * r

    grid = []
    for g in [20, 40, 60, 80, 100]:
        pts = [point(i, g) for i in range(axis_count)]
        grid.append('<polygon points="{}" class="radar-grid"/>'.format(" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)))
    axis_lines, labels = [], []
    for i, label in enumerate(axes):
        x, y = point(i, 100)
        axis_lines.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" class="radar-axis"/>')
        lx, ly = point(i, 118)
        labels.append(f'<text x="{lx:.1f}" y="{ly:.1f}" class="radar-label">{esc(label)}</text>')

    series = []
    for p in products:
        values = [score_map[c["id"]].get(p) or 0 for c in conditions]
        pts = [point(i, v) for i, v in enumerate(values)]
        path = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        series.append(
            f'<polygon class="radar-series" data-product="{esc(p)}" points="{path}" '
            f'style="--series-color:{colors[p]}"/>'
        )
    legend = "".join(f'<button type="button" data-product="{esc(p)}"><i style="background:{colors[p]}"></i>{esc(p)}</button>' for p in products)
    return (
        f'<div class="radarBox"><div class="radarHead"><h3>{esc(title)}</h3><span class="radarCurrent">当前：全部品牌</span></div>'
        f'<svg class="radarSvg" viewBox="0 0 {size} {size}" role="img" aria-label="{esc(title)}">'
        + "".join(grid)
        + "".join(axis_lines)
        + "".join(labels)
        + "".join(series)
        + "</svg>"
        f'<div class="radarLegend">{legend}</div></div>'
    )


def render_condition_factor_radar(model, condition):
    details = model["conditionDetails"][condition["id"]][:8]
    products = model["products"]
    colors = model["colors"]
    if len(details) < 3:
        return ""
    size = 360
    cx = cy = size / 2
    radius = 118
    n = len(details)

    def short(item):
        return item if len(item) <= 8 else item[:8] + "..."

    def point(idx, score):
        angle = -math.pi / 2 + idx * 2 * math.pi / n
        r = radius * max(0, min(100, score or 0)) / 100
        return cx + math.cos(angle) * r, cy + math.sin(angle) * r

    grid = []
    for g in [25, 50, 75, 100]:
        pts = [point(i, g) for i in range(n)]
        grid.append('<polygon points="{}" class="radar-grid"/>'.format(" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)))
    labels = []
    lines = []
    for i, detail in enumerate(details):
        x, y = point(i, 100)
        lines.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" class="radar-axis"/>')
        lx, ly = point(i, 118)
        labels.append(f'<text x="{lx:.1f}" y="{ly:.1f}" class="radar-label">{esc(short(detail["item"]))}</text>')
    series = []
    for p in products:
        pts = [point(i, detail["scores"].get(p) or 0) for i, detail in enumerate(details)]
        path = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        series.append(f'<polygon class="radar-series" data-product="{esc(p)}" points="{path}" style="--series-color:{colors[p]}"/>')
    legend = "".join(f'<button type="button" data-product="{esc(p)}"><i style="background:{colors[p]}"></i>{esc(p)}</button>' for p in products)
    key_rows = "".join(
        f'<tr><td>{esc(d["type"])}</td><td>{esc(d["item"])}</td><td>{int(d["weight"]*100)}%</td></tr>' for d in details
    )
    return (
        '<div class="factorRadar">'
        '<div>'
        f'<svg class="radarSvg small" viewBox="0 0 {size} {size}">' + "".join(grid + lines + labels + series) + "</svg>"
        f'<div class="radarLegend compact">{legend}</div>'
        "</div>"
        f'<table class="keyTable"><thead><tr><th>类型</th><th>关键项</th><th>权重</th></tr></thead><tbody>{key_rows}</tbody></table>'
        "</div>"
    )


def render_detail_matrix(model, condition):
    products = model["products"]
    details = model["conditionDetails"][condition["id"]]
    rows = []
    for d in details:
        cells = []
        for p in products:
            value = d["values"].get(p, "")
            score = d["scores"].get(p)
            cls = score_class(score)
            if d["type"] == "配置":
                status = option_status(value)
            else:
                status = "有效数据" if score is not None else "缺失"
            contribution = "" if score is None else fmt_score(score * d["weight"])
            cells.append(
                f'<td class="scoreCell {cls}"><b>{esc(value) if value else "-"}</b>'
                f'<span>{fmt_score(score)}分</span><small>贡献 {contribution or "-"} · {esc(status)}</small></td>'
            )
        rows.append(
            f'<tr><td>{esc(d["item"])}</td><td>{esc(d["type"])}</td><td>{int(d["weight"]*100)}%</td>'
            f'<td>{esc(d["note"])}</td>{"".join(cells)}</tr>'
        )
    head = "".join(f"<th>{esc(p)}</th>" for p in products)
    return (
        '<div class="tableScroll detailMatrix"><table><thead><tr><th>指标/配置</th><th>类型</th><th>权重</th><th>对工况影响</th>'
        + head
        + "</tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></div>"
    )


def render_gap_cards(model, condition):
    xcmg = model["meta"]["xcmg"]
    scores = model["conditionScores"][condition["id"]]
    rank, xscore, rows = xcmg_rank(scores, xcmg)
    leader = rows[0] if rows else {"product": "-", "score": 0}
    gap = max(0, (leader["score"] or 0) - (xscore or 0))
    details = model["conditionDetails"][condition["id"]]
    weighted_gaps = []
    improvements = []
    for d in details:
        xs = d["scores"].get(xcmg)
        best = max([v for v in d["scores"].values() if v is not None], default=None)
        if best is None or xs is None:
            continue
        delta = max(0, best - xs) * d["weight"]
        if delta > 0.05:
            weighted_gaps.append((delta, d))
        if d["type"] == "配置":
            raw = d["values"].get(xcmg, "")
            current = option_score(raw)
            if current < 100:
                improvements.append(((100 - current) * d["weight"], d, raw))
    weighted_gaps.sort(reverse=True, key=lambda x: x[0])
    improvements.sort(reverse=True, key=lambda x: x[0])
    gap_text = []
    for delta, d in weighted_gaps[:4]:
        gap_text.append(f"{d['item']} 约 {delta:.1f} 分")
    improve_text = []
    for delta, d, raw in improvements[:4]:
        improve_text.append(f"{d['item']}由“{raw or '/'}”提升为标配，理论增益约 {delta:.1f} 分")
    if not improve_text:
        improve_text.append("该工况下 XCMG 主要差距来自硬参数，需要结合结构尺寸、液压匹配或工作装置方案评估。")
    target_score = min(100, (xscore or 0) + sum(x[0] for x in improvements[:4]))
    return (
        '<div class="gapPanel"><h3>XCMG 与竞品差距及弥补路径</h3><div class="gapGrid">'
        f'<article><b>1. 对标差距</b><p>XCMG 当前约 {fmt_score(xscore)} 分，排名第 {rank or "-"}；领先产品为 {esc(leader["product"])} {fmt_score(leader["score"])} 分，差距约 {fmt_score(gap)} 分。</p></article>'
        f'<article><b>2. 差距来源</b><p>{"；".join(esc(x) for x in gap_text) if gap_text else "暂无明显可量化差距，主要看数据覆盖和配置定义。"}</p></article>'
        f'<article><b>3. 弥补动作</b><p>{"；".join(esc(x) for x in improve_text)}</p></article>'
        f'<article><b>4. 量化目标</b><p>优先补齐前述配置项后，该工况理论可提升至约 {fmt_score(target_score)} 分；若仍落后，则需要进入硬参数平台方案优化。</p></article>'
        "</div></div>"
    )


def render_simulator(model, condition):
    xcmg = model["meta"]["xcmg"]
    scores = model["conditionScores"][condition["id"]]
    base = scores.get(xcmg) or 0
    rivals = "|".join(f"{p}:{scores[p]:.3f}" for p in model["products"] if p != xcmg and scores.get(p) is not None)
    options = []
    for d in model["conditionDetails"][condition["id"]]:
        raw = d["values"].get(xcmg, "")
        xs = d["scores"].get(xcmg)
        if d["type"] == "配置":
            current = option_score(raw)
            delta = (100 - current) * d["weight"]
            label = f"{d['item']}标配"
            desc = f"当前 {raw or '/'}，按标配测算。"
        else:
            best = max([v for v in d["scores"].values() if v is not None], default=None)
            if xs is None or best is None:
                continue
            delta = max(0, best - xs) * d["weight"]
            label = f"{d['item']}优化"
            desc = "按本组竞品高水平测算，不代表立即可通过配置勾选实现。"
        if delta <= 0.25:
            continue
        options.append((delta, label, d["item"], desc))
    options.sort(reverse=True, key=lambda x: x[0])
    options = options[:8]
    option_html = "".join(
        f'<label><input type="checkbox" data-delta="{delta:.3f}"><span><b>{esc(label)}</b><em>+{delta:.1f} 工况分</em><small>{esc(desc)}</small></span></label>'
        for delta, label, _, desc in options
    )
    if not option_html:
        option_html = '<p class="muted">该工况 XCMG 当前没有可直接模拟的配置补齐项，主要差距应从硬参数和平台方案评估。</p>'
    return (
        f'<div class="simulator" data-base="{base:.3f}" data-xcmg="{esc(xcmg)}" data-rivals="{esc(rivals)}">'
        '<div class="simHead"><h3>XCMG 提升模拟器</h3><button type="button" class="resetSim">复原</button></div>'
        f'<div class="simGrid"><div class="simOptions">{option_html}</div>'
        f'<div class="simResult"><strong>{fmt_score(base)}</strong><span>模拟工况分</span><b>排名计算中</b><small></small></div></div>'
        '<div class="rankPanel"></div></div>'
    )


def render_summary_cards(model):
    xcmg = model["meta"]["xcmg"]
    cards = []
    for c in model["conditions"]:
        scores = model["conditionScores"][c["id"]]
        rank, xscore, rows = xcmg_rank(scores, xcmg)
        leader = rows[0] if rows else {"product": "-", "score": 0}
        config_details = [d for d in model["conditionDetails"][c["id"]] if d["type"] == "配置"]
        best_cfg = None
        if config_details:
            cfg_scores = {}
            for p in model["products"]:
                cfg_scores[p] = sum((d["scores"].get(p) or 0) * d["weight"] for d in config_details)
            cfg_rows = ranking(cfg_scores)
            best_cfg = cfg_rows[0] if cfg_rows else None
        cards.append(
            f'<article class="summaryCard"><h3>{esc(c["name"])}</h3>'
            f'<p><b>工况特点：</b>{esc(c["feature"])}</p>'
            f'<p><b>有益配置：</b>{esc(c["benefit"])}</p>'
            f'<p><b>领先：</b>{esc(leader["product"])} {fmt_score(leader["score"])} 分；XCMG {fmt_score(xscore)} 分，第 {rank or "-"}。</p>'
            f'<p><b>配置贡献领先：</b>{esc(best_cfg["product"]) if best_cfg else "-"} {fmt_score(best_cfg["score"]) if best_cfg else "-"} 分；XCMG 配置项按实际标选配测算。</p>'
            "</article>"
        )
    return "".join(cards)


def render_overall_section(model):
    xcmg = model["meta"]["xcmg"]
    rank, xscore, rows = xcmg_rank(model["overall"], xcmg)
    leader = rows[0] if rows else {"product": "-", "score": 0}
    overall_table = "".join(
        f'<tr class="{ "xcmg-row" if p == xcmg else ""}"><td>{esc(p)}</td><td class="{score_class(model["overall"].get(p))}">{fmt_score(model["overall"].get(p))}</td>'
        f'<td>{fmt_score(model["conditionTotal"].get(p))}</td><td>{fmt_score(model["paramScore"].get(p))}</td><td>{fmt_score(model["optionScore"].get(p))}</td></tr>'
        for p in [r["product"] for r in rows]
    )
    return (
        '<section id="overall"><h2>总体评分（不分细分工况）</h2>'
        '<div class="split">'
        f'<div class="panel"><h3>总体评分排名</h3><div class="bars">{render_bar_ranking(model["overall"], xcmg)}</div></div>'
        '<div class="panel"><h3>XCMG 总体差距判断</h3>'
        f'<p>XCMG 当前总体约 <b>{fmt_score(xscore)}</b> 分，第 {rank or "-"}；领先产品为 {esc(leader["product"])} {fmt_score(leader["score"])} 分，差距约 {fmt_score((leader["score"] or 0)-(xscore or 0))} 分。</p>'
        '<p>总体分由工况适配、参数能力和标选配完整度组合得到：工况适配 50%，参数能力 30%，标选配 20%。这部分不替代工况判断，而是用于快速判断产品基础竞争力。</p>'
        '<div class="tableScroll compact"><table><thead><tr><th>产品</th><th>总体</th><th>工况</th><th>参数</th><th>配置</th></tr></thead><tbody>'
        + overall_table
        + '</tbody></table></div></div></div></section>'
    )


def render_html(model):
    meta = model["meta"]
    xcmg = meta["xcmg"]
    cond_scores = model["conditionScores"]
    cond_total = model["conditionTotal"]
    overall_rank, overall_score, overall_rows = xcmg_rank(model["overall"], xcmg)
    condition_rank, condition_score, condition_rows = xcmg_rank(cond_total, xcmg)
    leader = condition_rows[0] if condition_rows else {"product": "-", "score": 0}
    total_detail_rows = sum(len(v) for v in model["conditionDetails"].values())
    product_count = len(model["products"])
    summary_cards = render_summary_cards(model)
    conditions_html = []
    for idx, c in enumerate(model["conditions"], start=1):
        conditions_html.append(
            f'<section id="cond{idx}" class="conditionBlock"><div class="conditionTitle"><div><span>WORK CONDITION</span><h2>{esc(c["name"])}</h2></div><em>权重 {int(c["weight"]*100)}%</em></div>'
            '<div class="conditionIntro">'
            f'<p><b>工况特点：</b>{esc(c["feature"])}</p><p><b>有益配置：</b>{esc(c["benefit"])}</p>'
            "</div>"
            '<div class="conditionTop">'
            f'<div class="panel">{render_condition_factor_radar(model, c)}</div>'
            f'<div class="panel"><h3>工况评分排名</h3><div class="bars">{render_bar_ranking(cond_scores[c["id"]], xcmg)}</div></div>'
            "</div>"
            + render_detail_matrix(model, c)
            + render_gap_cards(model, c)
            + render_simulator(model, c)
            + "</section>"
        )
    param_head = "".join(f"<th>{esc(p)}</th>" for p in model["products"])
    param_rows = table_rows(model["rawParamRows"], model["products"])
    option_rows = table_rows(model["rawOptionRows"], model["products"])
    radar = render_radar(model, cond_scores, "工况雷达图")
    data_json = json.dumps({
        "xcmg": xcmg,
        "products": model["products"],
        "colors": model["colors"],
    }, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{esc(meta["title"])}</title>
  <style>
    :root{{--blue:#004c97;--blue-dark:#003765;--ink:#0a2d4f;--muted:#5f7285;--line:#cfdae6;--bg:#f3f7fa;--paper:#fff;--yellow:#f5b400;--green:#0f7b45;--red:#ba1f1f;--shadow:0 8px 24px rgba(0,58,112,.07)}}
    *{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--bg);color:#102a43;font-family:"Segoe UI",Arial,"Microsoft YaHei",sans-serif;line-height:1.55}}a{{color:inherit;text-decoration:none}}button,input{{font-family:inherit}}
    .layout{{display:grid;grid-template-columns:260px minmax(0,1fr);min-height:100vh}}aside.nav{{position:sticky;top:0;height:100vh;overflow:auto;background:linear-gradient(180deg,var(--blue-dark),#001e3d);color:white;border-right:5px solid var(--yellow);padding:18px 14px;z-index:20}}.nav h1{{font-size:18px;margin:10px 0 6px;color:#fff!important}}.nav img{{width:118px;background:#fff;padding:6px;border-radius:2px}}.nav small{{display:block;color:#bcd3e8;font-weight:800;letter-spacing:.08em;text-transform:uppercase}}.nav a{{display:block;padding:8px 10px;border-left:3px solid transparent;border-radius:3px;margin:2px 0;color:#eef7ff;font-size:13px;font-weight:700}}.nav a:hover{{background:rgba(255,255,255,.10);border-left-color:var(--yellow)}}.nav .home{{background:var(--yellow);color:#08213d;font-weight:900;margin:12px 0}}
    main{{padding:22px;min-width:0}}.hero{{background:#fff;border:1px solid var(--line);box-shadow:var(--shadow);display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:18px;align-items:center;border-left:6px solid var(--blue);margin-bottom:16px}}.heroText{{padding:28px 28px 24px}}.eyebrow{{color:var(--blue);font-size:12px;font-weight:900;letter-spacing:.14em;text-transform:uppercase}}h1{{font-size:38px;line-height:1.1;color:#082b4d;margin:8px 0 12px}}h2{{font-size:22px;color:#082b4d;margin:0 0 14px}}h2:after{{content:"";display:block;width:46px;height:3px;background:var(--yellow);margin-top:8px}}h3{{color:#0b3155;margin:0 0 8px;font-size:16px}}.hero p{{max-width:980px}}.heroMedia{{height:260px;display:grid;place-items:center;background:#f7fafc;border-left:1px solid var(--line);padding:18px}}.heroMedia img{{max-width:100%;max-height:100%;object-fit:contain}}.actions{{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}}.btn{{display:inline-flex;align-items:center;justify-content:center;border:1px solid #b9cadb;border-radius:4px;padding:9px 13px;font-weight:900;font-size:13px;background:#f7fbff}}.btn.blue{{background:var(--blue);color:#fff;border-color:var(--blue)}}.btn.yellow{{background:var(--yellow);border-color:var(--yellow);color:#08213d}}
    section{{background:#fff;border:1px solid var(--line);box-shadow:var(--shadow);border-radius:5px;padding:18px;margin:14px 0}}.kpis{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}}.kpi{{border:1px solid #c9d8e7;border-left:5px solid var(--blue);padding:12px;background:#fbfdff}}.kpi:nth-child(2){{border-left-color:var(--yellow)}}.kpi b{{display:block;font-size:30px;color:var(--blue)}}.kpi span{{font-size:12px;color:var(--muted)}}.split{{display:grid;grid-template-columns:minmax(0,1fr) minmax(420px,.9fr);gap:14px}}.panel{{border:1px solid #c8d7e6;border-radius:5px;background:#fff;padding:14px;min-width:0}}.summaryGrid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}.summaryCard{{border:1px solid #c8d7e6;border-top:4px solid var(--blue);padding:12px;background:#fbfdff}}.summaryCard p{{margin:7px 0;font-size:13px}}.conditionTitle{{display:flex;align-items:flex-start;justify-content:space-between;border-bottom:1px solid #e2ebf3;padding-bottom:12px;margin-bottom:12px}}.conditionTitle span{{display:block;color:var(--blue);font-size:12px;font-weight:900;letter-spacing:.14em}}.conditionTitle em{{font-style:normal;font-weight:900;color:#4f6172}}.conditionIntro{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px}}.conditionIntro p{{margin:0;background:#f7fafc;border-left:4px solid var(--yellow);padding:10px 12px}}.conditionTop{{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(390px,.8fr);gap:12px;margin-bottom:12px}}
    .bars{{display:grid;gap:7px}}.bar{{display:grid;grid-template-columns:30px minmax(120px,170px) minmax(180px,1fr) 54px;gap:9px;align-items:center}}.bar span{{background:#e6f0fa;color:var(--blue);font-weight:900;text-align:center;border-radius:3px;padding:3px 0}}.bar b{{font-size:13px}}.bar i{{height:17px;background:#e3ecf5;border-radius:3px;overflow:hidden}}.bar i em{{display:block;height:100%;background:linear-gradient(90deg,var(--blue),#2878bd)}}.bar strong{{color:#08335d}}.bar.xcmg span{{background:var(--yellow);color:#08213d}}.bar.xcmg i em{{background:linear-gradient(90deg,var(--yellow),#ffd86d)}}.bar.xcmg b,.bar.xcmg strong{{color:var(--blue);font-weight:900}}
    .radarBox{{min-width:0}}.radarHead{{display:flex;justify-content:space-between;gap:10px;align-items:center}}.radarCurrent{{font-size:12px;color:var(--blue);font-weight:900}}.radarSvg{{display:block;margin:6px auto;max-width:100%;height:360px}}.radarSvg.small{{height:300px}}.radar-grid{{fill:none;stroke:#d9e6f2;stroke-width:1}}.radar-axis{{stroke:#d9e6f2;stroke-width:1}}.radar-label{{font-size:12px;font-weight:800;fill:#0b3155;text-anchor:middle;dominant-baseline:middle}}.radar-series{{fill:var(--series-color);fill-opacity:.08;stroke:var(--series-color);stroke-width:2.3;transition:.18s}}.radarBox.focus .radar-series,.factorRadar.focus .radar-series{{opacity:.08}}.radarBox.focus .radar-series.active,.factorRadar.focus .radar-series.active{{opacity:1;fill-opacity:.18;stroke-width:3.8}}.radarLegend{{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}}.radarLegend button{{border:1px solid #bfd0e0;background:#fff;border-radius:4px;padding:5px 7px;font-size:12px;cursor:pointer;font-weight:700}}.radarLegend i{{display:inline-block;width:10px;height:10px;margin-right:5px;border-radius:2px}}.radarLegend button:hover{{border-color:var(--yellow);box-shadow:0 0 0 2px rgba(245,180,0,.18)}}.radarLegend.compact button{{font-size:11px;padding:4px 6px}}
    .factorRadar{{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:12px;align-items:center}}.keyTable{{width:100%;border-collapse:collapse;font-size:12px}}.keyTable th{{background:var(--blue);color:#fff}}.keyTable th,.keyTable td{{border-bottom:1px solid #e3edf5;padding:8px;text-align:left}}.tableScroll{{overflow:auto;border:1px solid var(--line);border-radius:4px;max-height:520px;background:white}}.tableScroll.compact{{max-height:360px}}table{{border-collapse:collapse;width:100%;font-size:12px}}th,td{{border-bottom:1px solid #e3edf5;padding:8px;text-align:left;vertical-align:top;white-space:nowrap}}th{{position:sticky;top:0;background:var(--blue);color:#fff;z-index:2}}td:first-child,th:first-child{{position:sticky;left:0;z-index:3}}td:first-child{{background:#fff;font-weight:800;color:#0b3155;box-shadow:2px 0 0 rgba(0,76,151,.08)}}tr:nth-child(even) td{{background:#f8fbfe}}tr.xcmg-row td{{box-shadow:inset 3px 0 0 var(--yellow)}}.scoreCell{{min-width:124px;white-space:normal}}.scoreCell b{{display:block}}.scoreCell span{{display:block;font-weight:900}}.scoreCell small{{display:block;color:#51677a}}.good{{background:#e6f4ea!important;color:#0c6a36!important;font-weight:800}}.mid{{background:#fff4cc!important;color:#785700!important;font-weight:800}}.bad{{background:#fde9e9!important;color:#ad1d1d!important;font-weight:800}}.missing{{background:#eef2f6!important;color:#607080!important}}
    .gapPanel{{border:1px solid #dfb650;background:#fffdf4;border-radius:5px;padding:14px;margin:12px 0}}.gapGrid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}}.gapGrid article{{background:#fff;border:1px solid #ecd991;padding:12px}}.gapGrid b{{display:block;color:#08335d}}.gapGrid p{{margin:5px 0 0;font-size:13px}}.simulator{{border:1px solid #c8d7e6;border-radius:5px;overflow:hidden;margin-top:12px}}.simHead{{display:flex;justify-content:space-between;padding:12px;background:#f7fafc;border-bottom:1px solid #e3edf5}}.resetSim{{border:1px solid #b9cadb;border-radius:4px;background:#fff;padding:6px 10px;font-weight:900;cursor:pointer}}.simGrid{{display:grid;grid-template-columns:minmax(0,1fr) 230px;gap:12px;padding:12px}}.simOptions{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}}.simOptions label{{border:1px solid #d6e2ee;background:#fbfdff;padding:9px;display:grid;grid-template-columns:18px 1fr;gap:8px}}.simOptions b,.simOptions em,.simOptions small{{display:block}}.simOptions em{{color:var(--blue);font-style:normal;font-weight:900;font-size:12px}}.simOptions small{{color:#5d7083;font-size:11px}}.simResult{{border-left:5px solid var(--yellow);background:#f7fafc;padding:18px}}.simResult strong{{display:block;font-size:34px;color:var(--blue)}}.simResult b,.simResult span,.simResult small{{display:block}}.rankPanel{{display:none;padding:0 12px 12px}}.rankPanel.show{{display:block}}.muted{{color:var(--muted)}}.rawTabs{{display:flex;gap:8px;margin-bottom:10px}}.rawTabs button{{border:1px solid #bfd0e0;background:#fff;border-radius:4px;padding:7px 11px;font-weight:900;cursor:pointer}}.rawTabs button.active{{background:var(--yellow);border-color:var(--yellow)}}.rawTable[data-open="false"]{{display:none}}.backTop{{position:fixed;left:14px;bottom:14px;z-index:40;background:var(--yellow);border:1px solid #c89200;border-radius:18px;padding:8px 12px;font-weight:900;color:#08213d;box-shadow:0 8px 20px rgba(0,58,112,.18)}}
    @media(max-width:1200px){{.layout{{display:block}}aside.nav{{height:auto;position:relative}}main{{padding:14px}}.hero,.split,.conditionTop,.factorRadar{{grid-template-columns:1fr}}.kpis,.summaryGrid,.gapGrid{{grid-template-columns:1fr 1fr}}.conditionIntro,.simGrid,.simOptions{{grid-template-columns:1fr}}.heroMedia{{height:220px}}}}
    @media(max-width:720px){{.kpis,.summaryGrid,.gapGrid{{grid-template-columns:1fr}}h1{{font-size:30px}}.bar{{grid-template-columns:28px 118px 1fr 48px}}th,td{{padding:7px 6px}}}}
  </style>
</head>
<body>
<a class="backTop" href="#top">回到顶部</a>
<div class="layout" id="top">
  <aside class="nav">
    <img src="assets/xcmg-logo.svg" alt="XCMG">
    <h1>{esc(meta["label"])}小挖对标</h1>
    <small>{esc(meta["xcmg"])}</small>
    <a class="home" href="arc.html">返回 ARC 主页</a>
    <a href="./">3.5 吨看板</a>
    <a href="excavator-1-2t.html">1-2 吨看板</a>
    <a href="excavator-2-3t.html">2-3 吨看板</a>
    <a href="#summary">领导总览</a>
    <a href="#overall">总体评分</a>
    <a href="#radar">可视化驾驶舱</a>
    <a href="#conditions">工况总览</a>
    {''.join(f'<a href="#cond{i}">{esc(c["name"])}</a>' for i,c in enumerate(model["conditions"],1))}
    <a href="#raw">原始数据</a>
  </aside>
  <main>
    <div class="hero">
      <div class="heroText">
        <span class="eyebrow">XCMG Excavator Competitive Dashboard</span>
        <h1>{esc(meta["title"])}</h1>
        <p>按 3.5 吨小挖同一套方法，把参数、标选配、典型工况、配置贡献、差距来源和提升模拟拆开展示。结论均从用户提供 Excel 原始值计算，不用纯主观判断替代数据。</p>
        <div class="actions"><a class="btn blue" href="#conditions">查看工况分析</a><a class="btn yellow" href="data/{esc(meta["download"])}" download>导出原始 Excel</a><a class="btn" href="arc.html">返回 ARC</a></div>
      </div>
      <div class="heroMedia"><img src="{esc(meta["image"])}" alt="{esc(meta["xcmg"])} 产品图"></div>
    </div>

    <section id="summary">
      <h2>领导总览</h2>
      <div class="kpis">
        <div class="kpi"><span>对标产品数</span><b>{product_count}</b><span>含 XCMG 与主流竞品</span></div>
        <div class="kpi"><span>XCMG 工况综合</span><b>第 {condition_rank or "-"}</b><span>{fmt_score(condition_score)} 分</span></div>
        <div class="kpi"><span>工况领先</span><b>{esc(leader["product"])}</b><span>{fmt_score(leader["score"])} 分</span></div>
        <div class="kpi"><span>明细项</span><b>{total_detail_rows}</b><span>按工况筛选后计算</span></div>
      </div>
      <div class="summaryGrid" style="margin-top:12px">{summary_cards}</div>
    </section>

    {render_overall_section(model)}

    <section id="radar">
      <h2>可视化驾驶舱</h2>
      <div class="split">
        <div class="panel">{radar}</div>
        <div class="panel"><h3>工况综合排名（按 6 类工况）</h3><div class="bars">{render_bar_ranking(cond_total, xcmg)}</div><p class="muted">鼠标悬浮雷达图例或线条，可单独突出对应品牌；移开恢复全部。</p></div>
      </div>
    </section>

    <section id="conditions">
      <h2>工况总览</h2>
      <div class="summaryGrid">{summary_cards}</div>
    </section>

    {''.join(conditions_html)}

    <section id="raw">
      <h2>原始数据与全量展示</h2>
      <div class="actions"><a class="btn yellow" href="data/{esc(meta["download"])}" download>导出原始 Excel</a></div>
      <div class="rawTabs"><button type="button" class="active" data-table="param">参数</button><button type="button" data-table="option">标选配</button></div>
      <div class="tableScroll rawTable" data-name="param" data-open="true"><table><thead><tr><th>类别</th><th>指标</th><th>单位</th>{param_head}</tr></thead><tbody>{param_rows}</tbody></table></div>
      <div class="tableScroll rawTable" data-name="option" data-open="false"><table><thead><tr><th>类别</th><th>配置</th><th>单位</th>{param_head}</tr></thead><tbody>{option_rows}</tbody></table></div>
    </section>
  </main>
</div>
<script type="application/json" id="dashboard-data">{data_json}</script>
<script>
function setupRadars(){{
  document.querySelectorAll('.radarBox,.factorRadar').forEach(box=>{{
    const current=box.querySelector('.radarCurrent');
    const show=(product)=>{{
      box.classList.add('focus');
      box.querySelectorAll('.radar-series').forEach(s=>s.classList.toggle('active', s.dataset.product===product));
      if(current) current.textContent='当前：'+product;
    }};
    const reset=()=>{{
      box.classList.remove('focus');
      box.querySelectorAll('.radar-series').forEach(s=>s.classList.remove('active'));
      if(current) current.textContent='当前：全部品牌';
    }};
    box.querySelectorAll('[data-product]').forEach(el=>{{
      el.addEventListener('mouseenter',()=>show(el.dataset.product));
      el.addEventListener('focus',()=>show(el.dataset.product));
      el.addEventListener('mouseleave',reset);
      el.addEventListener('blur',reset);
    }});
  }});
}}
function setupSimulators(){{
  document.querySelectorAll('.simulator').forEach(sim=>{{
    const xcmg=sim.dataset.xcmg;
    const rivals=(sim.dataset.rivals||'').split('|').filter(Boolean).map(x=>{{const i=x.lastIndexOf(':');return {{product:x.slice(0,i),score:Number(x.slice(i+1))}};}});
    const base=Number(sim.dataset.base||0);
    const scoreEl=sim.querySelector('.simResult strong');
    const rankEl=sim.querySelector('.simResult b');
    const gapEl=sim.querySelector('.simResult small');
    const panel=sim.querySelector('.rankPanel');
    const inputs=[...sim.querySelectorAll('input[type="checkbox"]')];
    const render=()=>{{
      const score=Math.min(100, base + inputs.filter(i=>i.checked).reduce((s,i)=>s+Number(i.dataset.delta||0),0));
      const rows=[{{product:xcmg,score,isX:true}},...rivals].sort((a,b)=>b.score-a.score).map((r,i)=>({{...r,rank:i+1}}));
      const xrow=rows.find(r=>r.isX);
      const prev=rows[rows.findIndex(r=>r.isX)-1];
      scoreEl.textContent=score.toFixed(1).replace(/\\.0$/,'');
      rankEl.textContent='模拟第'+xrow.rank;
      gapEl.textContent=prev ? '距前一名 '+prev.product+' 还差 '+Math.max(0,prev.score-score).toFixed(1)+' 分' : '已达到该工况第一名';
      const max=Math.max(...rows.map(r=>r.score),1);
      panel.classList.add('show');
      panel.innerHTML='<div class="bars">'+rows.map(r=>'<div class="'+(r.isX?'bar xcmg':'bar')+'"><span>'+r.rank+'</span><b>'+r.product+'</b><i><em style="width:'+(r.score/max*100).toFixed(1)+'%"></em></i><strong>'+r.score.toFixed(1).replace(/\\.0$/,'')+'</strong></div>').join('')+'</div>';
    }};
    inputs.forEach(i=>i.addEventListener('change',render));
    sim.querySelector('.resetSim')?.addEventListener('click',()=>{{inputs.forEach(i=>i.checked=false);render();}});
    render();
  }});
}}
function setupRawTabs(){{
  document.querySelectorAll('.rawTabs button').forEach(btn=>btn.addEventListener('click',()=>{{
    document.querySelectorAll('.rawTabs button').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.rawTable').forEach(t=>t.dataset.open=String(t.dataset.name===btn.dataset.table));
  }}));
}}
setupRadars();
setupSimulators();
setupRawTabs();
</script>
</body>
</html>
"""


def download_assets():
    import urllib.request

    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    assets = [
        ("https://xcmg-usa.com/wp-content/uploads/2022/05/XE27U-1.jpg", ASSET_DIR / "xe27u-official.jpg"),
        ("https://xcmg.net.au/wp-content/uploads/2023/12/XE19U.png", ASSET_DIR / "xe19u-official.png"),
    ]
    for url, dest in assets:
        if dest.exists() and dest.stat().st_size > 10000:
            continue
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            dest.write_bytes(response.read())
    crop_product_image(ASSET_DIR / "xe19u-official.png", ASSET_DIR / "xe19u-official-cropped.png")
    crop_product_image(ASSET_DIR / "xe27u-official.jpg", ASSET_DIR / "xe27u-official-cropped.jpg")


def crop_product_image(src, dest):
    from PIL import Image, ImageChops

    img = Image.open(src).convert("RGBA")
    alpha_bbox = img.split()[-1].getbbox()
    rgb = img.convert("RGB")
    near_white_mask = Image.new("L", img.size, 0)
    pixels = rgb.load()
    mask_pixels = near_white_mask.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            if min(r, g, b) < 245:
                mask_pixels[x, y] = 255
    bbox = near_white_mask.getbbox() or alpha_bbox
    if not bbox:
        if dest.suffix.lower() in {".jpg", ".jpeg"}:
            canvas = Image.new("RGB", img.size, "white")
            canvas.paste(img, mask=img.split()[-1])
            canvas.save(dest, quality=92)
        else:
            img.save(dest)
        return
    pad = 28
    left = max(0, bbox[0] - pad)
    top = max(0, bbox[1] - pad)
    right = min(img.width, bbox[2] + pad)
    bottom = min(img.height, bbox[3] + pad)
    cropped = img.crop((left, top, right, bottom))
    if dest.suffix.lower() in {".jpg", ".jpeg"}:
        canvas = Image.new("RGB", cropped.size, "white")
        canvas.paste(cropped, mask=cropped.split()[-1])
        canvas.save(dest, quality=92)
    else:
        cropped.save(dest)


def sync_data_files():
    DATA_DIR.mkdir(exist_ok=True)
    for meta in SOURCE_FILES:
        shutil.copy2(meta["source"], DATA_DIR / meta["download"])


def update_arc_page():
    arc_path = ROOT / "arc.html"
    text = arc_path.read_text(encoding="utf-8")
    text = text.replace("当前先上线 3.5 吨小挖项目，其他产品线保留入口，不伪造未完成结论。", "当前已上线 1-2 吨、2-3 吨、3.5 吨三个小挖吨级项目，其他产品线保留入口，不伪造未完成结论。")
    text = text.replace("<a class=\"btn yellow\" href=\"./\">进入小挖看板</a>", "<a class=\"btn yellow\" href=\"./\">进入 3.5 吨看板</a>")
    text = text.replace("<div class=\"metric\"><strong>1</strong><span>已上线对标项目</span></div>", "<div class=\"metric\"><strong>3</strong><span>已上线对标项目</span></div>")
    text = text.replace("<div class=\"metric\"><strong>10</strong><span>小挖竞品型号</span></div>", "<div class=\"metric\"><strong>30</strong><span>小挖竞品型号</span></div>")
    text = text.replace("下一步建议先接入 Wheel Loaders 或 MEWP，二者更适合复用“工况 + 参数 + 配置包”的对标结构。", "小挖已形成 1-2 吨、2-3 吨、3.5 吨三个子板块；下一步建议接入 Wheel Loaders 或 MEWP。")
    text = text.replace("小挖、中挖、大挖；当前已上线 3.5 吨小挖竞品对标。", "小挖、中挖、大挖；当前已上线 1-2 吨、2-3 吨、3.5 吨三个小挖子板块。")
    text = text.replace('<div class="chips"><span class="chip live">3.5t 小挖</span><span class="chip">中挖预留</span></div>', '<div class="chips"><span class="chip live">1-2t</span><span class="chip live">2-3t</span><span class="chip live">3.5t</span></div>')
    text = text.replace('<div class="cardActions"><a class="btn yellow" href="./">打开小挖</a><button class="btn disabled" type="button">中挖待接入</button></div>', '<div class="cardActions"><a class="btn yellow" href="./">3.5 吨</a><a class="btn light" href="excavator-2-3t.html">2-3 吨</a><a class="btn light" href="excavator-1-2t.html">1-2 吨</a></div>')
    text = text.replace("把可用项目单独放出来，避免和预留入口混在一起。当前小挖项目仍使用原访问地址。", "把可用项目单独放出来，避免和预留入口混在一起。3.5 吨小挖项目仍使用原访问地址。")
    old = '''<section class="dashboardRow">
        <article class="panel project">
          <div class="projectImage"><img src="assets/arc/xe35u-official-cropped.jpg" alt="XCMG XE35U"></div>
          <div class="projectBody">
            <h3>3.5 吨小型挖掘机竞品对标</h3>
            <p>XCMG XE35U 对比沃尔沃、现代、迪尔、卡特、山猫、斗山、久保田、三一等竞品，按工况、参数、配置贡献和提升模拟组织。</p>
            <div class="factRow">
              <div class="fact"><b>6</b><span>典型工况</span></div>
              <div class="fact"><b>680</b><span>明细行</span></div>
              <div class="fact"><b>可交互</b><span>雷达 / 排名 / 模拟</span></div>
            </div>
            <div class="actions"><a class="btn blue" href="./">打开小挖看板</a><a class="btn light" href="original-data.xlsx" download>下载原始数据</a></div>
          </div>
        </article>

        <aside class="panel reserve">
          <h3>下一批项目位</h3>
          <div class="reserveList">
            <div class="reserveItem"><div><b>Wheel Loaders</b><span>建议先做装载效率、循环时间、铲斗、油耗和舒适性配置。</span></div><em>预留</em></div>
            <div class="reserveItem"><div><b>MEWP</b><span>建议按作业高度、平台载荷、电池、越野能力和租赁维护拆分。</span></div><em>预留</em></div>
            <div class="reserveItem"><div><b>Rollers / Motor Graders</b><span>道路机械可建立压实和平地两个工况模型。</span></div><em>预留</em></div>
          </div>
        </aside>
      </section>'''
    new = '''<section class="dashboardRow">
        <article class="panel project">
          <div class="projectImage"><img src="assets/arc/xe19u-official-cropped.png" alt="XCMG XE19U"></div>
          <div class="projectBody">
            <h3>1-2 吨级小型挖掘机竞品对标</h3>
            <p>XCMG XE19U 对比卡特、迪尔、山猫、久保田、沃尔沃、现代、斗山、三一等竞品，按同一套工况和配置贡献口径组织。</p>
            <div class="factRow">
              <div class="fact"><b>6</b><span>典型工况</span></div>
              <div class="fact"><b>11</b><span>对标产品</span></div>
              <div class="fact"><b>可交互</b><span>雷达 / 排名 / 模拟</span></div>
            </div>
            <div class="actions"><a class="btn blue" href="excavator-1-2t.html">打开 1-2 吨</a><a class="btn light" href="data/1-2.xlsx" download>下载原始数据</a></div>
          </div>
        </article>

        <article class="panel project">
          <div class="projectImage"><img src="assets/arc/xe27u-official-cropped.jpg" alt="XCMG XE27U"></div>
          <div class="projectBody">
            <h3>2-3 吨级小型挖掘机竞品对标</h3>
            <p>XCMG XE27U 对比卡特、迪尔、山猫、久保田、沃尔沃、现代、斗山、三一等竞品，复用 3.5 吨项目的工况、参数和配置逻辑。</p>
            <div class="factRow">
              <div class="fact"><b>6</b><span>典型工况</span></div>
              <div class="fact"><b>9</b><span>对标产品</span></div>
              <div class="fact"><b>可交互</b><span>雷达 / 排名 / 模拟</span></div>
            </div>
            <div class="actions"><a class="btn blue" href="excavator-2-3t.html">打开 2-3 吨</a><a class="btn light" href="data/2-3.xlsx" download>下载原始数据</a></div>
          </div>
        </article>

        <article class="panel project">
          <div class="projectImage"><img src="assets/arc/xe35u-official-cropped.jpg" alt="XCMG XE35U"></div>
          <div class="projectBody">
            <h3>3.5 吨小型挖掘机竞品对标</h3>
            <p>XCMG XE35U 对比沃尔沃、现代、迪尔、卡特、山猫、斗山、久保田、三一等竞品，原访问地址保持不变。</p>
            <div class="factRow">
              <div class="fact"><b>6</b><span>典型工况</span></div>
              <div class="fact"><b>10</b><span>对标产品</span></div>
              <div class="fact"><b>可交互</b><span>雷达 / 排名 / 模拟</span></div>
            </div>
            <div class="actions"><a class="btn blue" href="./">打开 3.5 吨</a><a class="btn light" href="original-data.xlsx" download>下载原始数据</a></div>
          </div>
        </article>
      </section>'''
    if old in text:
        text = text.replace(old, new)
    else:
        text = text.replace("assets/arc/xe19u-official.png", "assets/arc/xe19u-official-cropped.png")
        text = text.replace("assets/arc/xe27u-official.jpg", "assets/arc/xe27u-official-cropped.jpg")
    text = text.replace("小挖竞品看板原地址保持不变。", "小挖 1-2 吨、2-3 吨、3.5 吨子板块已上线；3.5 吨原地址保持不变。")
    arc_path.write_text(text, encoding="utf-8", newline="\n")


def main():
    download_assets()
    sync_data_files()
    for meta in SOURCE_FILES:
        wb = load_workbook(meta["source"])
        model = build_model(wb, meta)
        (ROOT / f"{meta['slug']}.html").write_text(render_html(model), encoding="utf-8", newline="\n")
    update_arc_page()


if __name__ == "__main__":
    main()
