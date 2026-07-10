import html
import json
import math
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "source-excel"
ASSET_DIR = ROOT / "assets" / "arc"


SOURCE_FILES = [
    {
        "slug": "excavator-1-2t",
        "output": "excavator-1-2t.html",
        "label": "1-2 吨级",
        "title": "XCMG XE19U 1-2 吨级挖掘机竞品对标看板",
        "xcmg": "XCMG XE19U",
        "source": DATA_DIR / "XCMG_1-2t_mini_excavator_competitor_source.xlsx",
        "download": "XCMG_1-2t_mini_excavator_competitor_source.xlsx",
        "image": "assets/arc/xe19u-official-cropped.png",
        "image_source": "XCMG Australia XE19U",
    },
    {
        "slug": "excavator-2-3t",
        "output": "excavator-2-3t.html",
        "label": "2-3 吨级",
        "title": "XCMG XE27U 2-3 吨级挖掘机竞品对标看板",
        "xcmg": "XCMG XE27U",
        "source": DATA_DIR / "XCMG_2-3t_mini_excavator_competitor_source.xlsx",
        "download": "XCMG_2-3t_mini_excavator_competitor_source.xlsx",
        "image": "assets/arc/xe27u-official-cropped.jpg",
        "image_source": "XCMG USA XE27U",
    },
    {
        "slug": "excavator-35t",
        "output": "index.html",
        "label": "3-4 吨级",
        "title": "XCMG XE35U 3-4 吨级挖掘机竞品对标看板",
        "xcmg": "XCMG XE35U",
        "source": DATA_DIR / "XCMG_3.5t_mini_excavator_competitor_source.xlsx",
        "download": "XCMG_3.5t_mini_excavator_competitor_source.xlsx",
        "image": "assets/arc/xe35u-official-cropped.jpg",
        "image_source": "XCMG USA XE35U",
    },
    {
        "slug": "excavator-4-5t",
        "output": "excavator-4-5t.html",
        "label": "4-5 吨级",
        "title": "XCMG XE45U 4-5 吨级挖掘机竞品对标看板",
        "xcmg": "XCMG XE45U",
        "source": DATA_DIR / "XCMG_4-5t_mini_excavator_competitor_source.xlsx",
        "download": "XCMG_4-5t_mini_excavator_competitor_source.xlsx",
        "image": "assets/arc/xe45u-official-cropped.png",
        "image_source": "XCMG USA XE45U",
    },
    {
        "slug": "excavator-5-6t",
        "output": "excavator-5-6t.html",
        "label": "5-6 吨级",
        "title": "XCMG XE55U 5-6 吨级挖掘机竞品对标看板",
        "xcmg": "XCMG XE55U",
        "source": DATA_DIR / "XCMG_5-6t_mini_excavator_competitor_source.xlsx",
        "download": "XCMG_5-6t_mini_excavator_competitor_source.xlsx",
        "image": "assets/arc/xe55u-official-cropped.jpg",
        "image_source": "XCMG USA XE55U",
    },
    {
        "slug": "excavator-7-8t",
        "output": "excavator-7-8t.html",
        "label": "7-8 吨级",
        "title": "XCMG XE75U 7-8 吨级挖掘机竞品对标看板",
        "xcmg": "XCMG XE75U",
        "source": DATA_DIR / "XCMG_7-8t_mini_excavator_competitor_source.xlsx",
        "download": "XCMG_7-8t_mini_excavator_competitor_source.xlsx",
        "image": "assets/arc/xe75u-official-cropped.jpg",
        "image_source": "XCMG USA XE75U",
    },
    {
        "slug": "excavator-8-10t",
        "output": "excavator-8-10t.html",
        "label": "8-10 吨级",
        "title": "XCMG XE80U 8-10 吨级挖掘机竞品对标看板",
        "xcmg": "XCMG XE80U",
        "source": DATA_DIR / "XCMG_8-10t_mini_excavator_competitor_source.xlsx",
        "download": "XCMG_8-10t_mini_excavator_competitor_source.xlsx",
        "image": "assets/arc/xe80u-official-cropped.jpg",
        "image_source": "XCMG USA XE80U",
    },
    {
        "slug": "excavator-12-14t",
        "output": "excavator-12-14t.html",
        "label": "12-14 吨级",
        "title": "XCMG XE135U 12-14 吨级挖掘机竞品对标看板",
        "xcmg": "XCMG XE135U",
        "source": DATA_DIR / "XCMG_12-14t_excavator_competitor_source.xlsx",
        "download": "XCMG_12-14t_excavator_competitor_source.xlsx",
        "image": "assets/arc/xe135u-official-cropped.webp",
        "image_source": "XCMG USA XE135U",
    },
    {
        "slug": "excavator-14-16t-short-tail",
        "output": "excavator-14-16t-short-tail.html",
        "label": "14-16 吨级短尾",
        "title": "XCMG XE155UCR 14-16 吨级短尾挖掘机竞品对标看板",
        "xcmg": "XCMG XE155UCR",
        "source": DATA_DIR / "XCMG_14-16t_short_tail_excavator_competitor_source.xlsx",
        "download": "XCMG_14-16t_short_tail_excavator_competitor_source.xlsx",
        "image": "assets/arc/xe155ucr-official-cropped.jpg",
        "image_source": "XCMG USA XE155UCR",
    },
    {
        "slug": "excavator-21-24t",
        "output": "excavator-21-24t.html",
        "label": "21-24 吨级",
        "title": "XCMG XE225U 21-24 吨级挖掘机竞品对标看板",
        "xcmg": "XCMG XE225U",
        "source": DATA_DIR / "XCMG_21-24t_excavator_competitor_source.xlsx",
        "download": "XCMG_21-24t_excavator_competitor_source.xlsx",
        "image": "assets/arc/xe225u-official-cropped.png",
        "image_source": "XCMG USA XE225U",
    },
]


MIN_SCORE_COVERAGE = 0.60
OVERALL_WEIGHTS = {"parameter": 0.65, "option": 0.35}

UNIT_ALIASES = {
    "mpa": "MPa",
    "kpa": "kPa",
    "kw": "kW",
    "kn": "kN",
    "l/min": "L/min",
}

ENGINEERING_GUIDANCE = {
    "运输参数": "需评估整机布置、结构尺寸和运输合规性",
    "接地参数": "需评估底盘尺寸、接地比压和整机稳定性",
    "工作参数": "需评估动臂、斗杆、铰点和整机稳定性",
    "动力": "需评估发动机匹配、冷却能力和油耗表现",
    "工作装置": "需评估动臂斗杆结构、油缸规格和工作范围",
    "液压系统": "需评估泵阀匹配、压力设定、流量分配和热平衡",
    "行走": "需评估行走马达、减速机构、系统压力和操控标定",
    "回转": "需评估回转液压匹配、减速机构和操控标定",
    "挖掘力": "需评估油缸规格、系统压力和机构传动比",
    "起吊能力": "需评估结构强度、整机稳定性和载荷表验证",
}

ITEM_ENGINEERING_GUIDANCE = {
    "尾部回转半径": "需评估上车回转包络、配重和发动机舱布置",
    "动臂偏摆（左/右）": "需评估偏摆机构、油缸行程、管路布置和结构干涉",
    "接地比压": "需评估操作重量、履带接地长度和履带宽度",
    "操作重量": "需评估结构减重、配重方案和拖车级别",
    "爬坡能力": "需评估行走驱动、牵引、制动和安全边界",
}

# Virtual labels keep cross-tonnage terminology consistent without rewriting the source files.
PARAM_ALIASES = {
    "行走速度（高速）": ("行走速度（低速/高速）",),
    "行走速度（低速）": ("行走速度（低速/高速）",),
}

OPTION_ALIASES = {
    "安全摄像头": ("后视摄像头", "270°摄像头", "270°视摄像头"),
    "密码启动/防盗": ("密码启动", "密码防盗"),
    "驾驶室温控": ("驾驶室冷暖空调", "驾驶室版本制热", "驾驶室版本制冷"),
    "电子围栏": ("电子围栏", "电子栅栏"),
}

OPTION_ALIAS_STRATEGY = {
    "驾驶室温控": "all",
}


CONDITIONS = [
    {
        "id": "narrow",
        "name": "狭窄空间 / 市政庭院",
        "weight": 0.18,
        "feature": "看重窄机身、短尾回转、较小运输尺寸和贴边作业能力。",
        "benefit": "可伸缩底盘、动臂偏摆、推土铲偏摆和安全摄像头有助于庭院、市政和受限空间作业。",
        "items": [
            ("参数", "整机运输宽度", 0.18, "low", "越窄越适合入户、园林和人行道受限空间。"),
            ("参数", "整机运输长度", 0.12, "low", "短车身转场和狭小现场调头更灵活。"),
            ("参数", "尾部回转半径", 0.24, "low", "尾扫越小越不容易碰墙、碰车和碰围挡。"),
            ("参数", "动臂偏摆（左/右）", 0.18, "swing", "越能贴边开沟、贴墙清底，狭窄空间收益越高。"),
            ("配置", "可伸缩底盘", 0.08, "option", "窄处收窄、开阔处展开，兼顾通过性和稳定性。"),
            ("配置", "推土铲偏摆", 0.07, "option", "角落回填和边沟修整时减少重复调车。"),
            ("配置", "安全摄像头", 0.06, "option", "后视或环视能力可以降低城市巷道和庭院倒车风险。"),
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
            ("参数", "标配斗杆", 0.08, "high", "斗杆长度影响标配状态下的深挖覆盖。"),
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
            ("参数", "系统流量", 0.14, "flow_sum", "复合动作速度与液压响应。"),
            ("参数", "发动机净功率", 0.10, "high", "连续循环中的动力储备。"),
            ("参数", "发动机总功率", 0.08, "high", "动力系统基础能力。"),
            ("参数", "行走速度（高速）", 0.05, "speed_high", "场内短距离转场效率。"),
            ("参数", "行走速度（低速）", 0.02, "speed_low", "接近卡车和料堆时的精细行走控制。"),
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
        "benefit": "AUX1/AUX2 管路、卸油管路、流量保持和快换管路影响破碎锤、拇指夹、螺旋钻等属具适配。",
        "items": [
            ("参数", "系统流量", 0.14, "flow_sum", "决定液压属具连续工作的供油基础。"),
            ("参数", "工作压力", 0.12, "high", "破碎、夹持和钻孔属具输出能力。"),
            ("参数", "AUX1流量", 0.14, "high", "主属具回路供油能力。"),
            ("参数", "AUX1压力", 0.10, "high", "主属具负载能力。"),
            ("参数", "AUX2流量", 0.08, "high", "旋转/夹持类辅回路能力。"),
            ("参数", "AUX2压力", 0.08, "high", "决定辅回路可匹配属具的压力范围。"),
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
        "benefit": "副配重和推土铲浮动有助于改善稳定性与整平效率；起吊边界仍应以载荷表和作业规范为准。",
        "items": [
            ("参数", "履带宽度", 0.09, "high", "较宽履带通常有助于降低接地比压并改善稳定性，但会增加运输宽度。"),
            ("参数", "接地比压", 0.14, "low", "越低越适合软土、草地和回填土表面。"),
            ("参数", "最大牵引力", 0.13, "high", "坡地转场和湿软场地脱困能力。"),
            ("参数", "爬坡能力", 0.13, "high", "反映设备上下坡和转场能力，不等同于允许作业坡度。"),
            ("参数", "地面正前方3m远处起吊能力（放下推土铲）", 0.18, "high", "放铲吊装代表稳定边界。"),
            ("参数", "地面正前方3m远处起吊能力（抬起推土铲）", 0.12, "high", "无支撑状态下的保守吊装能力。"),
            ("参数", "地面侧方3m远处起吊能力", 0.12, "high", "侧方吊装稳定性。"),
            ("配置", "副配重", 0.05, "option", "可改善稳定性和额定起吊能力，具体以载荷表为准。"),
            ("配置", "推土铲浮动", 0.04, "option", "可提升整平效率，不能替代坡地稳定性验证。"),
        ],
    },
    {
        "id": "rental",
        "name": "租赁 / 快速转场 / 多客户通用",
        "weight": 0.14,
        "feature": "看运输尺寸、油耗管理、易用性、安全提醒和远程管理。",
        "benefit": "自动怠速、自动停机、远程信息处理、防盗、摄像头和报警配置会影响油耗管理、资产管理和多客户使用便利性。",
        "items": [
            ("参数", "整机运输宽度", 0.10, "low", "拖车、仓库和门洞通过性。"),
            ("参数", "整机运输长度", 0.08, "low", "拖车装载和仓储占地。"),
            ("参数", "整机运输高度", 0.07, "low", "低矮通道和运输合规性。"),
            ("参数", "操作重量", 0.08, "low", "拖车级别和租赁客户自提门槛。"),
            ("参数", "行走速度（高速）", 0.05, "speed_high", "场内快速转场效率。"),
            ("参数", "行走速度（低速）", 0.02, "speed_low", "多客户使用时的低速操控友好性。"),
            ("配置", "自动怠速", 0.06, "option", "减少等待和停顿阶段的怠速油耗。"),
            ("配置", "自动停机", 0.08, "option", "降低无效怠速、油耗和租赁客户使用成本。"),
            ("配置", "远程信息处理系统", 0.09, "option", "定位、工时、维保和资产管理。"),
            ("配置", "密码启动/防盗", 0.05, "option", "租赁资产防盗和授权使用。"),
            ("配置", "一键启动", 0.03, "option", "多客户使用更方便。"),
            ("配置", "USB电源", 0.02, "option", "基础便利配置。"),
            ("配置", "蓝牙收音机", 0.02, "option", "驾驶舒适性。"),
            ("配置", "手机托", 0.02, "option", "租赁客户通用便利性。"),
            ("配置", "报警灯", 0.04, "option", "提高设备在市政和工地环境中的可见性。"),
            ("配置", "行走报警", 0.05, "option", "人员密集场景安全提醒。"),
            ("配置", "驾驶室温控", 0.05, "option", "跨季节租赁适用性。"),
            ("配置", "安全摄像头", 0.04, "option", "多客户倒车和近机作业安全。"),
            ("配置", "电子围栏", 0.03, "option", "租赁资产区域管理。"),
            ("配置", "工作灯延迟关闭", 0.02, "option", "夜间停机和离场便利性。"),
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


def display_value(value):
    text = clean(value)
    if not text:
        return "/"
    text = re.sub(r"\s*[\r\n]+\s*", "；", text)
    text = re.sub(r"\s+", " ", text)
    return text


def fmt_score(value):
    if value is None or math.isnan(value):
        return "-"
    return f"{value:.1f}".rstrip("0").rstrip(".")


def fmt_percent(value):
    if value is None:
        return "-"
    return f"{value * 100:.0f}%"


def completeness_label(coverage):
    if coverage is None or coverage < MIN_SCORE_COVERAGE:
        return "数据不足"
    if coverage >= 0.90:
        return "高"
    if coverage >= 0.75:
        return "中"
    return "有限"


def normalize_unit(unit):
    text = clean(unit)
    return UNIT_ALIASES.get(text.lower(), text)


def value_with_unit(value, unit):
    text = display_value(value)
    normalized = normalize_unit(unit)
    if text == "/" or not normalized or normalized in {"配置", "类别"}:
        return text
    if normalized.lower() in text.lower():
        return text
    return f"{text} {normalized}"


def engineering_guidance(detail):
    return ITEM_ENGINEERING_GUIDANCE.get(
        detail.get("item"),
        ENGINEERING_GUIDANCE.get(detail.get("category"), "需结合整机约束、客户需求和试验结果评估"),
    )


def reference_action_text(detail, xcmg, best_product):
    current = value_with_unit(detail["values"].get(xcmg), detail.get("unit"))
    reference = value_with_unit(detail["values"].get(best_product), detail.get("unit"))
    return (
        f"{detail['item']}：当前 {current}，对标参考 {best_product} {reference}。"
        f"{engineering_guidance(detail)}；是否转为产品目标需通过工程与试验评审。"
    )


def extract_numbers(value):
    text = clean(value)
    if not text or text in {"/", "-", "—"}:
        return []
    text = text.replace("，", ",")
    # A hyphen between two numbers is a range separator, not a negative sign.
    return [float(x) for x in re.findall(r"(?<!\d)-?\d+(?:\.\d+)?", text)]


def parse_flow_total(value):
    text = clean(value).lower().replace("×", "x").replace("*", "x")
    if not text:
        return None
    if "+" not in text and "x" not in text:
        nums = extract_numbers(text)
        return max(nums) if nums else None
    total = 0.0
    matched = False
    for part in re.split(r"\s*\+\s*", text):
        product = re.search(r"(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)", part)
        if product:
            total += float(product.group(1)) * float(product.group(2))
            matched = True
            continue
        nums = extract_numbers(part)
        if nums:
            total += nums[0]
            matched = True
    return total if matched else None


def parse_metric_value(value, direction):
    text = clean(value)
    nums = extract_numbers(text)
    if not nums:
        return None
    if direction == "flow_sum":
        return parse_flow_total(text)
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
    if direction in {"speed_low", "speed_high"}:
        speed_parts = re.split(r"[/／]", text, maxsplit=1)
        if len(speed_parts) == 2:
            part = speed_parts[0] if direction == "speed_low" else speed_parts[1]
            part_nums = extract_numbers(part)
            if not part_nums:
                return None
            positives = [x for x in part_nums if x >= 0]
            return (min if direction == "speed_low" else max)(positives or part_nums)
        positives = [x for x in nums if x >= 0]
        values = positives or nums
        return (min if direction == "speed_low" else max)(values)
    if direction == "low":
        positives = [x for x in nums if x >= 0]
        if len(positives) > 1 and re.search(r"\d\s*[-~/]\s*\d", text):
            return sum(positives) / len(positives)
        return positives[0] if positives else nums[0]
    positives = [x for x in nums if x >= 0]
    if len(positives) > 1 and re.search(r"\d\s*[-~/]\s*\d", text):
        return sum(positives) / len(positives)
    return positives[0] if positives else nums[0]


def best_swing_pair(value):
    text = clean(value)
    if not text:
        return None
    groups = re.split(r"[;；\n]+", text)
    pairs = []
    for group in groups:
        nums = [abs(x) for x in extract_numbers(group) if abs(x) <= 180]
        if len(nums) >= 2:
            pairs.append((nums[0], nums[1]))
    if not pairs:
        return None
    return max(pairs, key=lambda pair: pair[0] + pair[1])


def swing_gap_sentence(item, xraw_original, braw_original, best_product, suffix):
    xpair = best_swing_pair(xraw_original)
    bpair = best_swing_pair(braw_original)
    if not xpair or not bpair:
        return None
    parts = []
    for label, xv, bv in [("左", xpair[0], bpair[0]), ("右", xpair[1], bpair[1])]:
        diff = bv - xv
        if diff > 0:
            parts.append(f"{label}偏摆少 {fmt_score(diff)}{suffix}")
        elif diff < 0:
            parts.append(f"{label}偏摆多 {fmt_score(abs(diff))}{suffix}")
        else:
            parts.append(f"{label}偏摆相同")
    return f"{item}：XCMG {display_value(xraw_original)}{suffix}，{best_product} {display_value(braw_original)}{suffix}；XCMG {'，'.join(parts)}。"


def option_score(value):
    text = clean(value)
    if not text:
        return None
    if text in {"/", "-", "—", "nan"} or text.startswith("无") or "未配置" in text:
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


def option_status(value, score=None):
    score = option_score(value) if score is None else score
    if score is None:
        return "待核验"
    if score >= 100:
        return "标配"
    if score >= 60:
        return "选配"
    if score > 0:
        return "需确认"
    return "无配置"


def resolve_parameter_record(wb, item):
    for source_item in PARAM_ALIASES.get(item, (item,)):
        rec = wb.param_map.get(source_item)
        if rec:
            resolved = dict(rec)
            resolved["item"] = item
            return resolved
    return None


def resolve_option_record(wb, item):
    source_items = OPTION_ALIASES.get(item, (item,))
    records = [wb.option_map[name] for name in source_items if name in wb.option_map]
    if not records:
        return None

    strategy = OPTION_ALIAS_STRATEGY.get(item, "max")
    values = {}
    scores = {}
    for product in wb.products:
        raw_parts = []
        product_scores = []
        for rec in records:
            raw = clean(rec["values"].get(product))
            raw_parts.append((rec["item"], raw))
            product_scores.append(option_score(raw))

        if len(raw_parts) == 1:
            values[product] = raw_parts[0][1]
        else:
            values[product] = "；".join(f"{name}：{raw or '待核验'}" for name, raw in raw_parts)

        known_scores = [score for score in product_scores if score is not None]
        if not known_scores:
            scores[product] = None
        elif strategy == "all" and len(product_scores) > 1:
            scores[product] = None if len(known_scores) != len(product_scores) else min(known_scores)
        else:
            scores[product] = max(known_scores)

    return {
        "category": records[0]["category"],
        "item": item,
        "unit": "配置",
        "values": values,
        "scores": scores,
    }


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
        unit = normalize_unit(row.iloc[2])
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


def coverage_ratio(parts):
    weighted = [(score, weight) for score, weight in parts if weight > 0]
    total_weight = sum(weight for _, weight in weighted)
    if total_weight <= 0:
        return 0.0
    known_weight = sum(weight for score, weight in weighted if score is not None)
    return known_weight / total_weight


def weighted_average(parts, min_coverage=0.0):
    weighted = [(score, weight) for score, weight in parts if weight > 0]
    if coverage_ratio(weighted) + 1e-9 < min_coverage:
        return None
    valid = [(score, weight) for score, weight in weighted if score is not None]
    if not valid:
        return None
    total_weight = sum(weight for _, weight in valid)
    return sum(score * weight for score, weight in valid) / total_weight


def condition_scores(wb):
    result = {}
    details = {}
    coverage = {}
    for condition in CONDITIONS:
        raw_details = []
        product_parts = {p: [] for p in wb.products}
        for typ, item, weight, direction, note in condition["items"]:
            if typ == "参数":
                rec = resolve_parameter_record(wb, item)
                if not rec:
                    continue
                metric_values = {p: parse_metric_value(rec["values"].get(p), direction) for p in wb.products}
                norm = normalize(metric_values, "low" if direction == "low" else "high")
                for p in wb.products:
                    score = norm.get(p)
                    product_parts[p].append((score, weight))
                if direction == "low":
                    direction_label = "越低越好"
                elif direction == "speed_low":
                    direction_label = "低速档能力"
                elif direction == "speed_high":
                    direction_label = "高速档能力"
                elif direction == "flow_sum":
                    direction_label = "总流量越高越好"
                else:
                    direction_label = "越高越好"
                raw_details.append({
                    "type": typ,
                    "category": rec["category"],
                    "item": item,
                    "unit": rec["unit"],
                    "direction": direction_label,
                    "parser": direction,
                    "weight": weight,
                    "note": note,
                    "values": rec["values"],
                    "scores": {p: norm.get(p) for p in wb.products},
                })
            else:
                rec = resolve_option_record(wb, item)
                if not rec:
                    continue
                scores = rec.get("scores") or {p: option_score(rec["values"].get(p)) for p in wb.products}
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
        scores = {p: weighted_average(product_parts[p], MIN_SCORE_COVERAGE) for p in wb.products}
        result[condition["id"]] = scores
        details[condition["id"]] = raw_details
        coverage[condition["id"]] = {p: coverage_ratio(product_parts[p]) for p in wb.products}
    return result, details, coverage


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
            entries = [(item, scores)]
        else:
            variants = []
            if item == "行走速度（低速/高速）":
                variants = [("行走速度（低速）", "speed_low"), ("行走速度（高速）", "speed_high")]
            elif item == "系统流量":
                variants = [(item, "flow_sum")]
            else:
                direction = "low" if item in LOWER_BETTER else ("swing" if item == "动臂偏摆（左/右）" else "high")
                variants = [(item, direction)]
            entries = []
            for display_item, direction in variants:
                vals = {p: parse_metric_value(row["values"].get(p), direction) for p in wb.products}
                scores = normalize(vals, "low" if direction == "low" else "high")
                entries.append((display_item, scores))
        for display_item, scores in entries:
            by_cat[cat].append((display_item, scores))
            metric_detail.append((cat, display_item, scores))

    product_category_scores = {p: {} for p in wb.products}
    for cat, items in by_cat.items():
        for p in wb.products:
            vals = [(scores.get(p), 1) for _, scores in items]
            product_category_scores[p][cat] = weighted_average(vals)

    coverage = {
        p: coverage_ratio([(scores.get(p), 1) for _, _, scores in metric_detail])
        for p in wb.products
    }
    product_scores = {}
    for p in wb.products:
        score = weighted_average([(product_category_scores[p].get(cat), w) for cat, w in weights.items()])
        product_scores[p] = score if coverage[p] + 1e-9 >= MIN_SCORE_COVERAGE else None
    return product_scores, product_category_scores, coverage


def build_model(wb, meta):
    cond_scores, cond_details, cond_coverage = condition_scores(wb)
    param_score, param_categories, param_coverage = category_scores(wb, wb.param_rows, PARAM_CATEGORY_WEIGHTS, is_option=False)
    option_score_map, option_categories, option_coverage = category_scores(wb, wb.option_rows, OPTION_CATEGORY_WEIGHTS, is_option=True)
    condition_total = {}
    condition_total_coverage = {}
    for p in wb.products:
        parts = [(cond_scores[c["id"]].get(p), c["weight"]) for c in CONDITIONS]
        condition_total[p] = weighted_average(parts, MIN_SCORE_COVERAGE)
        condition_total_coverage[p] = coverage_ratio(parts)
    overall_coverage = {
        p: param_coverage[p] * OVERALL_WEIGHTS["parameter"] + option_coverage[p] * OVERALL_WEIGHTS["option"]
        for p in wb.products
    }
    overall = {
        p: weighted_average([
            (param_score.get(p), OVERALL_WEIGHTS["parameter"]),
            (option_score_map.get(p), OVERALL_WEIGHTS["option"]),
        ], min_coverage=1.0)
        for p in wb.products
    }
    return {
        "meta": meta,
        "products": wb.products,
        "colors": {p: COLORS[i % len(COLORS)] for i, p in enumerate(wb.products)},
        "conditions": CONDITIONS,
        "conditionScores": cond_scores,
        "conditionDetails": cond_details,
        "conditionCoverage": cond_coverage,
        "conditionTotal": condition_total,
        "conditionTotalCoverage": condition_total_coverage,
        "paramScore": param_score,
        "paramCoverage": param_coverage,
        "optionScore": option_score_map,
        "optionCoverage": option_coverage,
        "overall": overall,
        "overallCoverage": overall_coverage,
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
        out.append(f"<tr><th scope=\"row\">{esc(row['category'])}</th><td>{esc(row['item'])}</td><td>{esc(row.get('unit',''))}</td>{cells}</tr>")
    return "\n".join(out)


def render_bar_ranking(scores, xcmg, max_rows=None, coverage=None):
    rows = ranking(scores)[: max_rows or 99]
    max_score = max([r["score"] for r in rows] + [1])
    html_rows = []
    for idx, row in enumerate(rows, start=1):
        cls = "bar xcmg" if row["product"] == xcmg else "bar"
        width = max(2, row["score"] / max_score * 100)
        html_rows.append(
            f'<div class="{cls}"><span>{idx}</span><b>{esc(row["product"])}</b>'
            f'<i><em style="width:{width:.1f}%"></em></i><strong>{fmt_score(row["score"])}</strong>'
            + (f'<small class="barCoverage" title="数据覆盖率">覆盖 {fmt_percent(coverage.get(row["product"]))}</small>' if coverage else "")
            + '</div>'
        )
    return "".join(html_rows)


def default_radar_products(model, ranking_map):
    xcmg = model["meta"]["xcmg"]
    rows = ranking(ranking_map)
    leader = rows[0]["product"] if rows else None
    defaults = [xcmg]
    if leader and leader != xcmg:
        defaults.append(leader)
    return defaults


def render_radar(model, score_map, title, small=False, ranking_map=None):
    products = model["products"]
    conditions = model["conditions"]
    colors = model["colors"]
    defaults = default_radar_products(model, ranking_map or model["conditionTotal"])
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
        labels.append(f'<text x="{lx:.1f}" y="{ly:.1f}" class="radar-label"><title>{esc(conditions[i]["name"])}</title>{esc(label)}</text>')

    series = []
    for p in products:
        values = [score_map[c["id"]].get(p) or 0 for c in conditions]
        pts = [point(i, v) for i, v in enumerate(values)]
        path = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        series.append(
            f'<polygon class="radar-series" data-product="{esc(p)}" points="{path}" '
            f'style="--series-color:{colors[p]}"/>'
        )
    legend = "".join(
        f'<button type="button" data-product="{esc(p)}" data-default="{str(p in defaults).lower()}"><i style="background:{colors[p]}"></i>{esc(p)}</button>'
        for p in products
    )
    return (
        f'<div class="radarBox"><div class="radarHead"><h3>{esc(title)}</h3><span class="radarCurrent">当前：全部品牌</span></div>'
        f'<svg class="radarSvg" viewBox="0 0 {size} {size}" role="img" aria-label="{esc(title)}">'
        + "".join(grid)
        + "".join(axis_lines)
        + "".join(labels)
        + "".join(series)
        + "</svg>"
        '<details class="radarPicker" open data-mobile-open="false"><summary>选择对比品牌</summary>'
        f'<div class="radarLegend">{legend}</div></details></div>'
    )


def render_condition_factor_radar(model, condition):
    details = model["conditionDetails"][condition["id"]][:8]
    products = model["products"]
    colors = model["colors"]
    defaults = default_radar_products(model, model["conditionScores"][condition["id"]])
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
        labels.append(f'<text x="{lx:.1f}" y="{ly:.1f}" class="radar-label"><title>{esc(detail["item"])}</title>{esc(short(detail["item"]))}</text>')
    series = []
    for p in products:
        pts = [point(i, detail["scores"].get(p) or 0) for i, detail in enumerate(details)]
        path = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        series.append(f'<polygon class="radar-series" data-product="{esc(p)}" points="{path}" style="--series-color:{colors[p]}"/>')
    legend = "".join(
        f'<button type="button" data-product="{esc(p)}" data-default="{str(p in defaults).lower()}"><i style="background:{colors[p]}"></i>{esc(p)}</button>'
        for p in products
    )
    key_rows = "".join(
        f'<tr><td>{esc(d["type"])}</td><td>{esc(d["item"])}</td><td>{int(d["weight"]*100)}%</td></tr>' for d in details
    )
    return (
        '<div class="factorRadar">'
        '<div class="radarHead factorRadarHead"><h3>关键参数 / 配置对比</h3><span class="radarCurrent"></span></div>'
        '<div class="factorRadarGrid"><div>'
        f'<svg class="radarSvg small" viewBox="0 0 {size} {size}" role="img" aria-label="{esc(condition["name"])}关键参数与配置雷达图">' + "".join(grid + lines + labels + series) + "</svg>"
        '<details class="radarPicker" open data-mobile-open="false"><summary>选择对比品牌</summary>'
        f'<div class="radarLegend compact">{legend}</div></details>'
        "</div>"
        f'<table class="keyTable"><caption class="srOnly">{esc(condition["name"])}关键项及权重</caption><thead><tr><th scope="col">类型</th><th scope="col">关键项</th><th scope="col">权重</th></tr></thead><tbody>{key_rows}</tbody></table>'
        "</div></div>"
    )


def render_detail_matrix(model, condition):
    products = model["products"]
    details = model["conditionDetails"][condition["id"]]
    known_weight = {
        p: sum(d["weight"] for d in details if d["scores"].get(p) is not None)
        for p in products
    }
    rows = []
    for d in details:
        cells = []
        for p in products:
            value = d["values"].get(p, "")
            score = d["scores"].get(p)
            cls = score_class(score)
            if d["type"] == "配置":
                status = option_status(value, score)
            else:
                status = "有效数据" if score is not None else "待核验"
            contribution = "" if score is None or known_weight[p] <= 0 else fmt_score(score * d["weight"] / known_weight[p])
            cells.append(
                f'<td class="scoreCell {cls}"><b>{esc(value) if value else "-"}</b>'
                f'<span>{fmt_score(score)}分</span><small>贡献 {contribution or "-"} · {esc(status)}</small></td>'
            )
        rows.append(
            f'<tr><th scope="row">{esc(d["item"])}</th><td>{esc(d["type"])}</td><td>{int(d["weight"]*100)}%</td>'
            f'<td>{esc(d["note"])}</td>{"".join(cells)}</tr>'
        )
    head = "".join(f'<th scope="col">{esc(p)}</th>' for p in products)
    return (
        f'<div class="tableScroll detailMatrix"><table><caption class="srOnly">{esc(condition["name"])}全部指标与配置贡献明细</caption><thead><tr><th scope="col">指标/配置</th><th scope="col">类型</th><th scope="col">权重</th><th scope="col">对工况影响</th>'
        + head
        + "</tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></div>"
    )


def direction_key(detail):
    if detail.get("parser"):
        return detail["parser"]
    if detail["item"] == "动臂偏摆（左/右）":
        return "swing"
    if detail["direction"] == "越低越好":
        return "low"
    return "high"


def best_reference(detail, xcmg):
    xs = detail["scores"].get(xcmg)
    candidates = [(p, s) for p, s in detail["scores"].items() if p != xcmg and s is not None]
    if xs is None or not candidates:
        return None
    best_product, best_score = max(candidates, key=lambda item: item[1])
    delta = max(0, best_score - xs) * detail["weight"]
    if delta <= 0.05:
        return None
    return best_product, best_score, delta


def metric_gap_text(detail, xcmg, best_product):
    xraw_original = detail["values"].get(xcmg, "") or "-"
    braw_original = detail["values"].get(best_product, "") or "-"
    xraw = display_value(xraw_original)
    braw = display_value(braw_original)
    unit = detail.get("unit", "")
    key = direction_key(detail)
    xv = parse_metric_value(xraw_original, key)
    bv = parse_metric_value(braw_original, key)
    suffix = f" {unit}" if unit and unit != "配置" else ""
    if key == "swing":
        swing_text = swing_gap_sentence(detail["item"], xraw_original, braw_original, best_product, suffix)
        if swing_text:
            return swing_text
    if xv is None or bv is None:
        return f"{detail['item']}：XCMG {xraw}，{best_product} {braw}。"
    if key == "low":
        diff = max(0, xv - bv)
        if diff > 0:
            return f"{detail['item']}：XCMG {xraw}{suffix}，{best_product} {braw}{suffix}；XCMG 高于参考值 {fmt_score(diff)}{suffix}，该指标越低越有利。"
        return f"{detail['item']}：XCMG {xraw}{suffix}，{best_product} {braw}{suffix}，已接近对标参考。"
    diff = max(0, bv - xv)
    if diff > 0:
        return f"{detail['item']}：XCMG {xraw}{suffix}，{best_product} {braw}{suffix}；XCMG 低于参考值 {fmt_score(diff)}{suffix}。"
    return f"{detail['item']}：XCMG {xraw}{suffix}，{best_product} {braw}{suffix}，已接近对标参考。"


def option_gap_text(detail, xcmg, best_product):
    xraw = display_value(detail["values"].get(xcmg, "") or "/")
    braw = display_value(detail["values"].get(best_product, "") or "/")
    xstatus = option_status(xraw, detail["scores"].get(xcmg))
    bstatus = option_status(braw, detail["scores"].get(best_product))
    return f"{detail['item']}：XCMG {xstatus}（{xraw}），{best_product} {bstatus}（{braw}）。"


def as_list(items, fallback):
    if not items:
        return f"<p>{esc(fallback)}</p>"
    return '<ul class="gapList">' + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def render_gap_cards(model, condition):
    xcmg = model["meta"]["xcmg"]
    scores = model["conditionScores"][condition["id"]]
    _, xscore, rows = xcmg_rank(scores, xcmg)
    leader = rows[0] if rows else {"product": "-", "score": 0}
    details = model["conditionDetails"][condition["id"]]
    param_gaps = []
    option_gaps = []
    for d in details:
        ref = best_reference(d, xcmg)
        if not ref:
            continue
        best_product, _, delta = ref
        if d["type"] == "配置":
            option_gaps.append((delta, option_gap_text(d, xcmg, best_product), d))
        else:
            param_gaps.append((delta, metric_gap_text(d, xcmg, best_product), d))
    param_gaps.sort(reverse=True, key=lambda x: x[0])
    option_gaps.sort(reverse=True, key=lambda x: x[0])

    param_text = [x[1] for x in param_gaps[:4]]
    option_text = [x[1] for x in option_gaps[:4]]
    combined_gaps = sorted(param_gaps + option_gaps, reverse=True, key=lambda x: x[0])
    major_items = [x[2]["item"] for x in combined_gaps[:3]]
    major_text = ("、".join(major_items)) if major_items else "已列关键项"
    if xscore is None:
        coverage = model["conditionCoverage"][condition["id"]].get(xcmg)
        leader_text = (
            f"XCMG 有效字段覆盖率为 {fmt_percent(coverage)}，暂不进入正式排名；"
            f"当前资料中领先产品为 {leader['product']}，已知差距项为 {major_text}。"
        )
    else:
        leader_text = f"同工况排名第一的参考产品为 {leader['product']}；XCMG 的主要差距项为 {major_text}。"
    actions = []
    for _, _, d in option_gaps[:3]:
        raw = display_value(d["values"].get(xcmg, "") or "/")
        ref = best_reference(d, xcmg)
        if ref:
            best_product, _, _ = ref
            best_raw = display_value(d["values"].get(best_product, "") or "/")
            actions.append(
                f"{d['item']}：XCMG 当前为{option_status(raw)}，{best_product} 为{option_status(best_raw)}。"
                "建议纳入标配或选配方案评估，并核算客户价值、成本和法规要求。"
            )
    for _, _, d in param_gaps[:3]:
        ref = best_reference(d, xcmg)
        if ref:
            best_product, _, _ = ref
            actions.append(reference_action_text(d, xcmg, best_product))
    if not actions:
        actions.append("当前数据未显示单项明显短板。建议先复核缺失值和配置口径，再决定是否开展工程方案评估。")
    return (
        '<div class="gapPanel"><h3>XCMG 与竞品差距及建议动作</h3><div class="gapGrid">'
        f'<article><b>1. 对标参照</b><p>{esc(leader_text)}</p></article>'
        f'<article><b>2. 硬参数差距</b>{as_list(param_text, "硬参数未显示明显短板，当前差距主要来自配置完整度或数据缺失。")}</article>'
        f'<article><b>3. 配置缺口</b>{as_list(option_text, "配置项暂未发现明确弱项，建议继续核验竞品配置资料并维护现有标配口径。")}</article>'
        f'<article><b>4. 建议动作</b>{as_list(actions[:5], "复核缺失数据后再确认工程动作。")}</article>'
        "</div></div>"
    )


def render_simulator(model, condition):
    xcmg = model["meta"]["xcmg"]
    scores = model["conditionScores"][condition["id"]]
    base = scores.get(xcmg)
    if base is None:
        coverage = model["conditionCoverage"][condition["id"]].get(xcmg)
        return (
            '<div class="simulator simulatorUnavailable">'
            '<div class="simHead"><h3>XCMG 提升模拟器</h3></div>'
            f'<p class="simDisclaimer">XCMG 有效字段覆盖率为 {fmt_percent(coverage)}，低于正式排名门槛，'
            "暂不生成模拟排名。请先补齐该工况缺失参数或配置，再开展提升方案评估。</p></div>"
        )
    rivals = "|".join(f"{p}:{scores[p]:.3f}" for p in model["products"] if p != xcmg and scores.get(p) is not None)
    options = []
    for d in model["conditionDetails"][condition["id"]]:
        raw = d["values"].get(xcmg, "")
        xs = d["scores"].get(xcmg)
        if d["type"] == "配置":
            current = xs
            if current is None:
                continue
            delta = (100 - current) * d["weight"]
            candidates = [(p, score) for p, score in d["scores"].items() if p != xcmg and score is not None]
            best_product, _ = max(candidates, key=lambda item: item[1], default=("竞品参考", 0))
            best_raw = display_value(d["values"].get(best_product, "") or "/")
            label = f"{d['item']}模拟标配"
            desc = f"模拟状态为标配；当前为{option_status(raw)}，参考 {best_product} 为{option_status(best_raw)}。"
        else:
            candidates = [(p, score) for p, score in d["scores"].items() if p != xcmg and score is not None]
            if xs is None or not candidates:
                continue
            best_product, best = max(candidates, key=lambda item: item[1])
            delta = max(0, best - xs) * d["weight"]
            label = f"{d['item']}对标"
            desc = (
                f"当前 {value_with_unit(raw, d.get('unit'))}；"
                f"参考 {best_product} {value_with_unit(d['values'].get(best_product), d.get('unit'))}。"
                f"{engineering_guidance(d)}。"
            )
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
        option_html = '<p class="muted">当前没有可量化的参数或配置提升项。建议先复核缺失数据，再开展方案评估。</p>'
    return (
        f'<div class="simulator" data-base="{base:.3f}" data-xcmg="{esc(xcmg)}" data-rivals="{esc(rivals)}">'
        '<div class="simHead"><h3>XCMG 提升模拟器</h3><button type="button" class="resetSim">清除选择</button></div>'
        '<p class="simDisclaimer">模拟结果仅反映当前评分模型，不替代工程验证、成本评审和市场需求判断。</p>'
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
        condition_coverage = model["conditionCoverage"][c["id"]].get(xcmg)
        config_details = [d for d in model["conditionDetails"][c["id"]] if d["type"] == "配置"]
        best_cfg = None
        xcmg_cfg = None
        if config_details:
            cfg_scores = {}
            for p in model["products"]:
                parts = [(d["scores"].get(p), d["weight"]) for d in config_details]
                cfg_scores[p] = (
                    sum(score * weight for score, weight in parts if score is not None)
                    if coverage_ratio(parts) + 1e-9 >= MIN_SCORE_COVERAGE
                    else None
                )
            cfg_rows = ranking(cfg_scores)
            best_cfg = cfg_rows[0] if cfg_rows else None
            xcmg_cfg = cfg_scores.get(xcmg)
        score_gap = max(0, leader["score"] - xscore) if xscore is not None else None
        cfg_gap = max(0, best_cfg["score"] - xcmg_cfg) if best_cfg and xcmg_cfg is not None else None
        gap_candidates = []
        for detail in model["conditionDetails"][c["id"]]:
            ref = best_reference(detail, xcmg)
            if ref:
                _, _, delta = ref
                gap_candidates.append((delta, detail["item"]))
        gap_candidates.sort(reverse=True)
        focus_text = "、".join(item for _, item in gap_candidates[:3]) or "暂无单项明显短板"
        if xscore is None:
            performance_text = (
                f"XCMG 有效字段覆盖率 {fmt_percent(condition_coverage)}，暂不进入正式排名；"
                f"当前资料领先产品为 {leader['product']} {fmt_score(leader['score'])} 分。"
            )
        elif leader["product"] == xcmg:
            performance_text = f"XCMG {fmt_score(xscore)} 分，排名第 1。"
        else:
            performance_text = (
                f"{leader['product']} {fmt_score(leader['score'])} 分；"
                f"XCMG {fmt_score(xscore)} 分，第 {rank or '-'}，距领先产品 {fmt_score(score_gap)} 分。"
            )
        if xcmg_cfg is None:
            config_text = (
                f"XCMG 配置字段覆盖不足，暂不比较；当前资料最高为 {best_cfg['product']} {fmt_score(best_cfg['score'])} 分。"
                if best_cfg
                else "配置字段覆盖不足，暂不比较。"
            )
        elif best_cfg and best_cfg["product"] == xcmg:
            config_text = f"XCMG {fmt_score(xcmg_cfg)} 分，配置项累计贡献最高。"
        else:
            config_text = (
                f"{best_cfg['product'] if best_cfg else '-'} {fmt_score(best_cfg['score']) if best_cfg else '-'} 分；"
                f"XCMG {fmt_score(xcmg_cfg)} 分，差 {fmt_score(cfg_gap)} 分。"
            )
        cards.append(
            f'<article class="summaryCard"><h3>{esc(c["name"])}</h3>'
            f'<p><b>工况表现：</b>{esc(performance_text)}</p>'
            f'<p><b>主要差距项：</b>{esc(focus_text)}。</p>'
            f'<p><b>配置项累计贡献：</b>{esc(config_text)}</p>'
            "</article>"
        )
    return "".join(cards)


def raw_param_gap_text(row, model, xcmg):
    item = row["item"]
    if item in LOWER_BETTER:
        direction = "low"
    elif item == "动臂偏摆（左/右）":
        direction = "swing"
    elif item == "系统流量":
        direction = "flow_sum"
    else:
        direction = "high"
    values = {p: parse_metric_value(row["values"].get(p), direction) for p in model["products"]}
    scores = normalize(values, "low" if direction == "low" else "high")
    xscore = scores.get(xcmg)
    candidates = [(p, s) for p, s in scores.items() if p != xcmg and s is not None]
    if xscore is None or not candidates:
        return None
    best_product, best_score = max(candidates, key=lambda item: item[1])
    delta = max(0, best_score - xscore)
    if delta <= 3:
        return None
    xv = values.get(xcmg)
    bv = values.get(best_product)
    if xv is None or bv is None:
        return None
    unit = row.get("unit", "")
    suffix = f" {unit}" if unit and unit != "配置" else ""
    xraw = display_value(row["values"].get(xcmg))
    braw = display_value(row["values"].get(best_product))
    if direction == "swing":
        text = swing_gap_sentence(item, row["values"].get(xcmg), row["values"].get(best_product), best_product, suffix)
        if text:
            return delta * PARAM_CATEGORY_WEIGHTS.get(row["category"], 0.05), text, item
    if direction == "low":
        diff = max(0, xv - bv)
        if diff <= 0:
            return None
        text = f"{item}：XCMG {xraw}{suffix}，{best_product} {braw}{suffix}；XCMG 高于参考值 {fmt_score(diff)}{suffix}，该指标越低越有利。"
    else:
        diff = max(0, bv - xv)
        if diff <= 0:
            return None
        text = f"{item}：XCMG {xraw}{suffix}，{best_product} {braw}{suffix}；XCMG 低于参考值 {fmt_score(diff)}{suffix}。"
    return delta * PARAM_CATEGORY_WEIGHTS.get(row["category"], 0.05), text, item


def raw_option_gap_text(row, model, xcmg):
    xraw_original = row["values"].get(xcmg)
    xscore = option_score(xraw_original)
    if xscore is None:
        return None
    xraw = display_value(xraw_original)
    candidates = []
    for p in model["products"]:
        if p == xcmg:
            continue
        raw_original = row["values"].get(p)
        raw = display_value(raw_original)
        candidates.append((p, option_score(raw_original), raw))
    candidates = [c for c in candidates if c[1] is not None]
    if not candidates:
        return None
    best_product, best_score, braw = max(candidates, key=lambda item: item[1])
    delta = best_score - xscore
    if delta <= 0:
        return None
    text = f"{row['item']}：XCMG {option_status(xraw)}（{xraw}），{best_product} {option_status(braw)}（{braw}）。"
    return delta * OPTION_CATEGORY_WEIGHTS.get(row["category"], 0.05), text, row["item"]


def render_overall_gap_notes(model, xcmg, leader):
    param_gaps = [x for row in model["rawParamRows"] if (x := raw_param_gap_text(row, model, xcmg))]
    option_gaps = [x for row in model["rawOptionRows"] if (x := raw_option_gap_text(row, model, xcmg))]
    param_gaps.sort(reverse=True, key=lambda item: item[0])
    option_gaps.sort(reverse=True, key=lambda item: item[0])
    focus_items = [x[2] for x in (param_gaps + option_gaps)[:4]]
    focus_text = "、".join(focus_items) if focus_items else "已列核心指标"
    return (
        '<div class="overallNotes">'
        f'<p><b>对标参照：</b>总体排名第一的参考产品为 {esc(leader["product"])}；单项差距主要集中在 {esc(focus_text)} 等具体指标。</p>'
        f'<p><b>硬参数差距：</b></p>{as_list([x[1] for x in param_gaps[:4]], "当前原始参数没有显示明显落后项，重点复核缺失值和口径一致性。")}'
        f'<p><b>配置差距：</b></p>{as_list([x[1] for x in option_gaps[:4]], "标选配口径下暂无明显配置短板，后续以客户场景验证配置价值。")}'
        '</div>'
    )


def render_overall_section(model):
    xcmg = model["meta"]["xcmg"]
    rank, xscore, rows = xcmg_rank(model["overall"], xcmg)
    leader = rows[0] if rows else {"product": "-", "score": 0}
    gap_notes = render_overall_gap_notes(model, xcmg, leader)
    ranked_products = [row["product"] for row in rows]
    ordered_products = ranked_products + [p for p in model["products"] if p not in ranked_products]
    overall_table = "".join(
        f'<tr class="{ "xcmg-row" if p == xcmg else ""}"><th scope="row">{esc(p)}</th><td class="{score_class(model["overall"].get(p))}">{fmt_score(model["overall"].get(p))}</td>'
        f'<td>{fmt_score(model["paramScore"].get(p))}</td><td>{fmt_score(model["optionScore"].get(p))}</td>'
        f'<td>{fmt_percent(model["overallCoverage"].get(p))}</td><td>{completeness_label(model["overallCoverage"].get(p))}</td></tr>'
        for p in ordered_products
    )
    return (
        '<section id="overall"><h2>总体评分（不分细分工况）</h2>'
        f'<p class="methodNote">评分口径：参数综合分 {int(OVERALL_WEIGHTS["parameter"]*100)}% + 标选配综合分 {int(OVERALL_WEIGHTS["option"]*100)}%；工况评分单独展示，不重复计入总体分。</p>'
        '<div class="split">'
        f'<div class="panel"><h3>总体评分排名</h3><div class="bars">{render_bar_ranking(model["overall"], xcmg, coverage=model["overallCoverage"])}</div><p class="coverageNote">覆盖率低于 {int(MIN_SCORE_COVERAGE*100)}% 的产品不进入排名，仍在右侧表格中保留并标记为“数据不足”。</p></div>'
        '<div class="panel"><h3>XCMG 总体差距分析</h3>'
        + gap_notes
        + '<details class="mobileDisclosure overallTableDisclosure" open data-mobile-open="false"><summary>完整评分明细</summary><div class="tableScroll compact"><table><caption class="srOnly">总体评分、参数评分、配置评分及数据覆盖率</caption><thead><tr><th scope="col">产品</th><th scope="col">总体</th><th scope="col">参数</th><th scope="col">配置</th><th scope="col">数据覆盖</th><th scope="col">完整度等级</th></tr></thead><tbody>'
        + overall_table
        + '</tbody></table></div></details></div></div></section>'
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
            f'<section id="cond{idx}" class="conditionBlock"><div class="conditionTitle"><div><span>典型工况</span><h2>{esc(c["name"])}</h2></div><em>权重 {int(c["weight"]*100)}%</em></div>'
            '<div class="conditionIntro">'
            f'<p><b>工况特点：</b>{esc(c["feature"])}</p><p><b>有益配置：</b>{esc(c["benefit"])}</p>'
            "</div>"
            '<div class="conditionTop">'
            f'<details class="mobileDisclosure factorDisclosure" open data-mobile-open="false"><summary>关键参数 / 配置雷达图</summary><div class="panel">{render_condition_factor_radar(model, c)}</div></details>'
            f'<div class="panel conditionRanking"><h3>工况评分排名</h3><div class="bars">{render_bar_ranking(cond_scores[c["id"]], xcmg, coverage=model["conditionCoverage"][c["id"]])}</div></div>'
            "</div>"
            + '<details class="mobileDisclosure matrixDisclosure" open data-mobile-open="false"><summary>全部指标贡献明细</summary>'
            + render_detail_matrix(model, c)
            + '</details>'
            + render_gap_cards(model, c)
            + '<details class="mobileDisclosure simulatorDisclosure" open data-mobile-open="false"><summary>提升模拟方案</summary>'
            + render_simulator(model, c)
            + '</details>'
            + "</section>"
        )
    param_head = "".join(f'<th scope="col">{esc(p)}</th>' for p in model["products"])
    param_rows = table_rows(model["rawParamRows"], model["products"])
    option_rows = table_rows(model["rawOptionRows"], model["products"])
    radar = render_radar(model, cond_scores, "工况雷达图", ranking_map=cond_total)
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
  <title>{esc(meta["title"])}｜XCMG ARC</title>
  <style>
    :root{{--blue:#004c97;--blue-dark:#003765;--ink:#0a2d4f;--muted:#5f7285;--line:#cfdae6;--bg:#f3f7fa;--paper:#fff;--yellow:#f5b400;--green:#0f7b45;--red:#ba1f1f;--shadow:0 8px 24px rgba(0,58,112,.07)}}
    *{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--bg);color:#102a43;font-family:"Segoe UI",Arial,"Microsoft YaHei",sans-serif;line-height:1.55}}a{{color:inherit;text-decoration:none}}button,input{{font-family:inherit}}
    .layout{{display:grid;grid-template-columns:260px minmax(0,1fr);min-height:100vh}}aside.nav{{position:sticky;top:0;height:100vh;overflow:auto;background:linear-gradient(180deg,var(--blue-dark),#001e3d);color:white;border-right:5px solid var(--yellow);padding:18px 14px;z-index:20}}.navBrand{{display:inline-block;width:max-content}}.navBrand:focus-visible{{outline:3px solid var(--yellow);outline-offset:3px}}.navTitle{{font-size:18px;margin:10px 0 6px;color:#fff;font-weight:900}}.nav img{{width:118px;background:#fff;padding:6px;border-radius:2px}}.nav small{{display:block;color:#bcd3e8;font-weight:800;letter-spacing:.08em;text-transform:uppercase}}.navMenu a{{display:block;padding:8px 10px;border-left:3px solid transparent;border-radius:3px;margin:2px 0;color:#eef7ff;font-size:13px;font-weight:700}}.navMenu a:hover{{background:rgba(255,255,255,.10);border-left-color:var(--yellow)}}.navMenu .home{{background:var(--yellow);color:#08213d;font-weight:900;margin:12px 0}}.navToggle,.mobileTop{{display:none}}
    main{{padding:22px;min-width:0}}.hero{{background:#fff;border:1px solid var(--line);box-shadow:var(--shadow);display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:18px;align-items:center;border-left:6px solid var(--blue);margin-bottom:16px}}.heroText{{padding:28px 28px 24px}}.eyebrow{{color:var(--blue);font-size:12px;font-weight:900;letter-spacing:.14em;text-transform:uppercase}}h1{{font-size:38px;line-height:1.1;color:#082b4d;margin:8px 0 12px}}h2{{font-size:22px;color:#082b4d;margin:0 0 14px}}h2:after{{content:"";display:block;width:46px;height:3px;background:var(--yellow);margin-top:8px}}h3{{color:#0b3155;margin:0 0 8px;font-size:16px}}.hero p{{max-width:980px}}.heroMedia{{height:260px;position:relative;background:#f7fafc;border-left:1px solid var(--line);padding:18px;overflow:hidden}}.heroMedia img{{position:absolute;inset:18px;width:calc(100% - 36px);height:calc(100% - 36px);object-fit:contain}}.actions{{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}}.btn{{display:inline-flex;align-items:center;justify-content:center;border:1px solid #b9cadb;border-radius:4px;padding:9px 13px;font-weight:900;font-size:13px;background:#f7fbff}}.btn.blue{{background:var(--blue);color:#fff;border-color:var(--blue)}}.btn.yellow{{background:var(--yellow);border-color:var(--yellow);color:#08213d}}
    section{{background:#fff;border:1px solid var(--line);box-shadow:var(--shadow);border-radius:5px;padding:18px;margin:14px 0}}.kpis{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}}.kpi{{border:1px solid #c9d8e7;border-left:5px solid var(--blue);padding:12px;background:#fbfdff}}.kpi:nth-child(2){{border-left-color:var(--yellow)}}.kpi b{{display:block;font-size:30px;color:var(--blue)}}.kpi span{{font-size:12px;color:var(--muted)}}.split{{display:grid;grid-template-columns:minmax(0,1fr) minmax(420px,.9fr);gap:14px}}.panel{{border:1px solid #c8d7e6;border-radius:5px;background:#fff;padding:14px;min-width:0}}.summaryGrid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}.summaryCard{{border:1px solid #c8d7e6;border-top:4px solid var(--blue);padding:12px;background:#fbfdff}}.summaryCard p{{margin:7px 0;font-size:13px}}.conditionTitle{{display:flex;align-items:flex-start;justify-content:space-between;border-bottom:1px solid #e2ebf3;padding-bottom:12px;margin-bottom:12px}}.conditionTitle span{{display:block;color:var(--blue);font-size:12px;font-weight:900;letter-spacing:.14em}}.conditionTitle em{{font-style:normal;font-weight:900;color:#4f6172}}.conditionIntro{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px}}.conditionIntro p{{margin:0;background:#f7fafc;border-left:4px solid var(--yellow);padding:10px 12px}}.conditionTop{{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(390px,.8fr);gap:12px;margin-bottom:12px}}.conditionTop>.mobileDisclosure{{min-width:0}}.conditionTop>.mobileDisclosure>.panel{{height:100%}}
    .bars{{display:grid;gap:7px}}.bar{{display:grid;grid-template-columns:28px minmax(100px,145px) minmax(90px,1fr) 48px 64px;gap:8px;align-items:center;min-width:0}}.bar span{{background:#e6f0fa;color:var(--blue);font-weight:900;text-align:center;border-radius:3px;padding:3px 0}}.bar b{{font-size:13px;min-width:0;overflow-wrap:anywhere}}.bar i{{height:17px;background:#e3ecf5;border-radius:3px;overflow:hidden}}.bar i em{{display:block;height:100%;background:linear-gradient(90deg,var(--blue),#2878bd)}}.bar strong{{color:#08335d}}.barCoverage{{font-size:11px;color:#65798c;white-space:nowrap}}.bar.xcmg span{{background:var(--yellow);color:#08213d}}.bar.xcmg i em{{background:linear-gradient(90deg,var(--yellow),#ffd86d)}}.bar.xcmg b,.bar.xcmg strong{{color:var(--blue);font-weight:900}}
    .radarBox{{min-width:0}}.radarHead{{display:flex;justify-content:space-between;gap:10px;align-items:center;padding-right:6px}}.radarCurrent{{font-size:12px;color:var(--blue);font-weight:900;white-space:nowrap}}.radarSvg{{display:block;margin:6px auto;max-width:100%;height:360px}}.radarSvg.small{{height:300px}}.radar-grid{{fill:none;stroke:#d9e6f2;stroke-width:1}}.radar-axis{{stroke:#d9e6f2;stroke-width:1}}.radar-label{{font-size:12px;font-weight:800;fill:#0b3155;text-anchor:middle;dominant-baseline:middle}}.radar-series{{fill:var(--series-color);fill-opacity:.08;stroke:var(--series-color);stroke-width:2.3;transition:.18s;cursor:pointer}}.radarBox.compare .radar-series,.factorRadar.compare .radar-series{{opacity:.08;fill-opacity:.03}}.radarBox.compare .radar-series.selected,.factorRadar.compare .radar-series.selected{{opacity:1;fill-opacity:.18;stroke-width:3.6}}.radarLegend{{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}}.radarLegend button{{border:1px solid #bfd0e0;background:#fff;border-radius:4px;padding:5px 7px;font-size:12px;cursor:pointer;font-weight:700}}.radarLegend i{{display:inline-block;width:10px;height:10px;margin-right:5px;border-radius:2px}}.radarLegend button:hover,.radarLegend button.selected{{border-color:var(--yellow);box-shadow:0 0 0 2px rgba(245,180,0,.18)}}.radarLegend button.selected{{background:#fff7d6;color:#08213d}}.radarLegend.compact button{{font-size:11px;padding:4px 6px}}.mobileDisclosure,.radarPicker{{border:0;padding:0;margin:0;min-width:0}}.mobileDisclosure>summary,.radarPicker>summary{{display:none}}
    .factorRadar{{min-width:0}}.factorRadarHead{{margin-bottom:4px}}.factorRadarGrid{{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:12px;align-items:center}}.keyTable{{width:100%;border-collapse:collapse;font-size:12px}}.keyTable th{{background:var(--blue);color:#fff}}.keyTable th,.keyTable td{{border-bottom:1px solid #e3edf5;padding:8px;text-align:left}}.tableScroll{{overflow:auto;border:1px solid var(--line);border-radius:4px;max-height:520px;background:white}}.tableScroll.compact{{max-height:360px}}table{{border-collapse:collapse;width:100%;font-size:12px}}th,td{{border-bottom:1px solid #e3edf5;padding:8px;text-align:left;vertical-align:top;white-space:nowrap}}th{{position:sticky;top:0;background:var(--blue);color:#fff;z-index:2}}td:first-child,th:first-child{{position:sticky;left:0;z-index:3}}td:first-child,tbody th:first-child{{background:#fff;font-weight:800;color:#0b3155;box-shadow:2px 0 0 rgba(0,76,151,.08)}}tr:nth-child(even) td,tr:nth-child(even) th:first-child{{background:#f8fbfe}}tr.xcmg-row td{{box-shadow:inset 3px 0 0 var(--yellow)}}.scoreCell{{min-width:124px;white-space:normal}}.scoreCell b{{display:block}}.scoreCell span{{display:block;font-weight:900}}.scoreCell small{{display:block;color:#51677a}}.good{{background:#e6f4ea!important;color:#0c6a36!important;font-weight:800}}.mid{{background:#fff4cc!important;color:#785700!important;font-weight:800}}.bad{{background:#fde9e9!important;color:#ad1d1d!important;font-weight:800}}.missing{{background:#eef2f6!important;color:#607080!important}}.srOnly{{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important}}
    .gapPanel{{border:1px solid #dfb650;background:#fffdf4;border-radius:5px;padding:14px;margin:12px 0}}.gapGrid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}}.gapGrid article{{background:#fff;border:1px solid #ecd991;padding:12px}}.gapGrid b{{display:block;color:#08335d}}.gapGrid p{{margin:5px 0 0;font-size:13px}}.overallNotes p{{margin:7px 0 4px}}.gapList{{margin:6px 0 0;padding-left:18px;font-size:13px;line-height:1.55}}.gapList li{{margin:4px 0}}.methodNote,.coverageNote,.sourceNote{{font-size:12px;color:#526a7f;background:#f6f9fc;border-left:4px solid var(--yellow);padding:9px 11px;margin:0 0 12px}}.coverageNote{{margin:10px 0 0}}.sourceNote{{display:flex;gap:10px;align-items:flex-start}}.sourceNote b{{color:#08335d;white-space:nowrap}}.simulator{{border:1px solid #c8d7e6;border-radius:5px;overflow:hidden;margin-top:12px}}.simHead{{display:flex;justify-content:space-between;padding:12px;background:#f7fafc;border-bottom:1px solid #e3edf5}}.simDisclaimer{{margin:0;padding:9px 12px;background:#fffdf4;border-bottom:1px solid #ecd991;color:#526a7f;font-size:12px}}.resetSim{{border:1px solid #b9cadb;border-radius:4px;background:#fff;padding:6px 10px;font-weight:900;cursor:pointer}}.simGrid{{display:grid;grid-template-columns:minmax(0,1fr) 230px;gap:12px;padding:12px}}.simOptions{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}}.simOptions label{{border:1px solid #d6e2ee;background:#fbfdff;padding:9px;display:grid;grid-template-columns:18px 1fr;gap:8px}}.simOptions b,.simOptions em,.simOptions small{{display:block}}.simOptions em{{color:var(--blue);font-style:normal;font-weight:900;font-size:12px}}.simOptions small{{color:#5d7083;font-size:11px}}.simResult{{border-left:5px solid var(--yellow);background:#f7fafc;padding:18px}}.simResult strong{{display:block;font-size:34px;color:var(--blue)}}.simResult b,.simResult span,.simResult small{{display:block}}.rankPanel{{display:none;padding:0 12px 12px}}.rankPanel.show{{display:block}}.muted{{color:var(--muted)}}.rawTabs{{display:flex;gap:8px;margin-bottom:10px}}.rawTabs button{{border:1px solid #bfd0e0;background:#fff;border-radius:4px;padding:7px 11px;font-weight:900;cursor:pointer}}.rawTabs button.active{{background:var(--yellow);border-color:var(--yellow)}}.rawTable[data-open="false"]{{display:none}}.backTop{{position:fixed;left:14px;bottom:14px;z-index:40;background:var(--yellow);border:1px solid #c89200;border-radius:18px;padding:8px 12px;font-weight:900;color:#08213d;box-shadow:0 8px 20px rgba(0,58,112,.18);opacity:0;pointer-events:none;transform:translateY(8px);transition:.18s}}.backTop.show{{opacity:1;pointer-events:auto;transform:none}}
    @media(max-width:1200px){{html{{scroll-padding-top:72px}}.layout{{display:block}}aside.nav{{height:auto;position:sticky;top:0;overflow:visible;border-right:0;border-bottom:4px solid var(--yellow);padding:8px 12px;display:grid;grid-template-columns:auto minmax(0,1fr) auto auto;gap:10px;align-items:center}}.nav img{{width:82px}}.navTitle{{font-size:14px;margin:0}}.nav small{{font-size:10px}}.navToggle,.mobileTop{{display:inline-flex;align-items:center;justify-content:center;border:1px solid rgba(255,255,255,.35);background:transparent;color:#fff;border-radius:4px;padding:7px 10px;font-weight:900}}.mobileTop{{font-size:12px}}.navMenu{{display:none;grid-column:1/-1;grid-template-columns:repeat(2,minmax(0,1fr));gap:3px;max-height:calc(100vh - 76px);overflow:auto;padding-top:8px}}.navMenu.open{{display:grid}}.navMenu .home{{grid-column:1/-1;margin:0}}main{{padding:14px}}section,.hero{{scroll-margin-top:78px}}.hero,.split,.conditionTop{{grid-template-columns:1fr}}.factorRadarGrid{{grid-template-columns:1fr}}.kpis,.summaryGrid,.gapGrid{{grid-template-columns:1fr 1fr}}.conditionIntro,.simGrid,.simOptions{{grid-template-columns:1fr}}.heroMedia{{height:220px}}.backTop{{display:none}}.detailMatrix table{{min-width:1360px}}.rawTable table{{min-width:1100px}}}}
    @media(max-width:720px){{body{{font-size:14px}}main{{padding:8px}}section{{padding:12px;margin:8px 0;border-radius:4px;box-shadow:none}}section,.hero{{scroll-margin-top:66px}}aside.nav{{grid-template-columns:72px minmax(0,1fr) auto auto;padding:6px 8px;gap:7px}}.nav img{{width:72px;padding:4px}}.navTitle{{font-size:12px;line-height:1.25}}.nav small{{font-size:9px}}.navToggle,.mobileTop{{padding:6px 8px;font-size:11px}}.navMenu{{max-height:calc(100vh - 64px);grid-template-columns:1fr 1fr}}.navMenu a{{font-size:12px;padding:7px 8px}}.hero{{margin-bottom:8px}}.heroText{{padding:16px 14px 12px}}.heroDescription{{display:none}}.heroMedia{{height:142px;border-left:0;border-top:1px solid var(--line);padding:10px}}.heroMedia img{{inset:10px;width:calc(100% - 20px);height:calc(100% - 20px)}}h1{{font-size:26px;margin:6px 0 8px}}h2{{font-size:20px;margin-bottom:10px}}h2:after{{margin-top:6px}}h3{{font-size:15px}}.actions{{gap:6px;flex-wrap:nowrap;overflow-x:auto;margin-top:10px;padding-bottom:2px}}.actions .btn{{flex:0 0 auto;padding:7px 9px;font-size:12px}}.kpis{{grid-template-columns:1fr 1fr;gap:7px}}.kpi{{padding:9px;border-left-width:4px;min-height:92px}}.kpi b{{font-size:24px;line-height:1.15;margin:3px 0}}.kpi span{{font-size:11px;line-height:1.35;display:block}}.summaryGrid{{display:grid;grid-template-columns:none;grid-auto-flow:column;grid-auto-columns:minmax(82%,1fr);gap:8px;overflow-x:auto;scroll-snap-type:x mandatory;padding:1px 13% 6px 1px}}.summaryCard{{scroll-snap-align:start;padding:10px;min-height:150px}}.summaryCard p{{font-size:12px;margin:5px 0}}.conditionBlock{{padding:11px}}.conditionTitle{{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;padding-bottom:8px;margin-bottom:8px}}.conditionTitle h2{{font-size:18px;overflow-wrap:anywhere;margin-bottom:0}}.conditionTitle span{{font-size:10px}}.conditionIntro{{display:grid;grid-template-columns:none;grid-auto-flow:column;grid-auto-columns:88%;overflow-x:auto;gap:8px;scroll-snap-type:x mandatory;margin-bottom:8px;padding-right:10%}}.conditionIntro p{{scroll-snap-align:start;padding:9px 10px;font-size:12px}}.conditionTop{{gap:8px;margin-bottom:8px}}.panel{{padding:10px}}.conditionRanking .bars{{gap:5px}}.bar{{grid-template-columns:24px minmax(82px,105px) minmax(64px,1fr) 40px;gap:5px}}.bar span{{padding:2px 0}}.bar b,.bar strong{{font-size:12px}}.bar i{{height:14px}}.barCoverage{{display:none}}.coverageNote,.methodNote,.sourceNote{{font-size:11px;padding:8px 9px;margin-bottom:8px}}th,td{{padding:7px 6px}}.sourceNote{{display:block}}.factorRadarGrid>div{{min-width:0;width:100%}}.factorRadarGrid .keyTable{{width:100%;min-width:0;table-layout:fixed}}.factorRadarGrid .keyTable th,.factorRadarGrid .keyTable td{{white-space:normal;overflow-wrap:anywhere}}.radarSvg{{height:260px;margin:2px auto}}.radarSvg.small{{width:100%;height:auto;max-height:255px}}.radarLegend{{min-width:0;padding-top:6px}}.radarLegend button{{white-space:normal;overflow-wrap:anywhere;font-size:11px;padding:4px 5px}}.mobileDisclosure>summary,.radarPicker>summary{{display:flex;align-items:center;justify-content:space-between;gap:8px;min-height:42px;padding:9px 11px;border:1px solid #c8d7e6;border-left:4px solid var(--blue);border-radius:4px;background:#f7fafc;color:#0b3155;font-weight:900;cursor:pointer;list-style:none}}.mobileDisclosure>summary::-webkit-details-marker,.radarPicker>summary::-webkit-details-marker{{display:none}}.mobileDisclosure>summary:after,.radarPicker>summary:after{{content:"展开";font-size:11px;color:var(--blue);font-weight:800}}.mobileDisclosure[open]>summary:after,.radarPicker[open]>summary:after{{content:"收起"}}.mobileDisclosure[open]>summary,.radarPicker[open]>summary{{margin-bottom:8px;border-left-color:var(--yellow)}}.conditionTop>.mobileDisclosure>.panel{{height:auto}}.factorDisclosure>.panel{{border:0;padding:0}}.matrixDisclosure,.simulatorDisclosure{{margin:8px 0}}.matrixDisclosure>.detailMatrix,.simulatorDisclosure>.simulator{{margin-top:0}}.overallTableDisclosure{{margin-top:10px}}.radarDisclosure>.panel{{border:0;padding:0}}.radarPicker{{margin-top:4px}}.radarPicker>summary{{min-height:36px;padding:7px 9px;border-left-width:3px;font-size:12px}}.gapPanel{{padding:10px;margin:8px 0}}.gapGrid{{display:grid;grid-template-columns:none;grid-auto-flow:column;grid-auto-columns:88%;gap:8px;overflow-x:auto;scroll-snap-type:x mandatory;padding-right:10%}}.gapGrid article{{scroll-snap-align:start;padding:10px}}.gapList{{font-size:12px;padding-left:17px}}.simGrid{{padding:8px}}.simOptions{{gap:6px}}.simOptions label{{padding:8px}}.simResult{{padding:12px}}.simResult strong{{font-size:28px}}.tableScroll{{max-height:62vh}}}}
  </style>
</head>
<body>
<a class="backTop" href="#top" aria-label="回到页面顶部">回到顶部</a>
<div class="layout" id="top">
  <aside class="nav">
    <a class="navBrand" href="arc.html" aria-label="返回全产品线竞品对标平台主页"><img src="assets/xcmg-logo.svg" alt="XCMG"></a>
    <div><div class="navTitle">{esc(meta["label"])}挖掘机对标</div><small>{esc(meta["xcmg"])}</small></div>
    <button class="navToggle" type="button" aria-expanded="false" aria-controls="page-nav">页面导航</button>
    <a class="mobileTop" href="#top">顶部</a>
    <div class="navMenu" id="page-nav">
      <a class="home" href="arc.html">返回对标平台主页</a>
      <a href="#summary">对标概览</a>
      <a href="#overall">总体评分</a>
      <a href="#radar">工况竞争格局</a>
      <a href="#conditions">工况总览</a>
      {''.join(f'<a href="#cond{i}">{esc(c["name"])}</a>' for i,c in enumerate(model["conditions"],1))}
      <a href="#raw">原始数据</a>
    </div>
  </aside>
  <main>
    <div class="hero">
      <div class="heroText">
        <span class="eyebrow">XCMG ARC 独立开发</span>
        <h1>{esc(meta["title"])}</h1>
        <p class="heroDescription">本页按照统一口径展示参数、标选配、典型工况、配置贡献、差距来源和提升模拟。全部结论可追溯至原始数据表和来源登记。</p>
        <div class="actions"><a class="btn blue" href="#conditions">查看工况对标</a><a class="btn yellow" href="data/source-excel/{esc(meta["download"])}" download>导出原始 Excel</a><a class="btn" href="arc.html">返回对标平台主页</a></div>
      </div>
      <div class="heroMedia"><img src="{esc(meta["image"])}" alt="{esc(meta["xcmg"])} 产品图"></div>
    </div>

    <section id="summary">
      <h2>对标概览</h2>
      <div class="kpis">
        <div class="kpi"><span>对标产品数</span><b>{product_count}</b><span>含 XCMG 与主流竞品</span></div>
        <div class="kpi"><span>XCMG 总体排名</span><b>第 {overall_rank or "-"}</b><span>参数与配置综合</span></div>
        <div class="kpi"><span>XCMG 总体得分</span><b>{fmt_score(overall_score)}</b><span>参数 65% / 配置 35%</span></div>
        <div class="kpi"><span>XCMG 数据覆盖</span><b>{fmt_percent(model["overallCoverage"].get(xcmg))}</b><span>完整度等级：{completeness_label(model["overallCoverage"].get(xcmg))}</span></div>
      </div>
    </section>

    {render_overall_section(model)}

    <section id="radar">
      <h2>工况竞争格局</h2>
      <div class="split">
        <details class="mobileDisclosure radarDisclosure" open data-mobile-open="false"><summary>工况雷达图</summary><div class="panel">{radar}</div></details>
        <div class="panel"><h3>工况综合排名（按 6 类工况）</h3><div class="bars">{render_bar_ranking(cond_total, xcmg, coverage=model["conditionTotalCoverage"])}</div><p class="muted">默认显示 XCMG 与工况领先产品；点击图例可增加或取消品牌，全部取消后恢复全品牌展示。</p></div>
      </div>
    </section>

    <section id="conditions">
      <h2>工况总览</h2>
      <p class="methodNote">排名口径：工况字段覆盖率低于 {int(MIN_SCORE_COVERAGE*100)}% 的产品不进入正式排名；缺失项仍保留在指标明细中。</p>
      <div class="summaryGrid">{summary_cards}</div>
    </section>

    {''.join(conditions_html)}

    <section id="raw">
      <h2>原始数据</h2>
      <div class="sourceNote"><b>数据口径</b><span>本页评分基于对应原始 Excel；空白项标记为“待核验”，不等同于无配置。数值范围按区间中值计算，系统流量按泵组流量合计，行走速度拆分高、低速档。数据来源及核验状态详见来源登记表。</span></div>
      <div class="actions"><a class="btn yellow" href="data/source-excel/{esc(meta["download"])}" download>导出原始 Excel</a><a class="btn" href="data/source-register.csv" download>下载来源登记表</a></div>
      <details class="mobileDisclosure rawDisclosure" open data-mobile-open="false"><summary>全量参数与配置</summary>
        <div class="rawTabs"><button type="button" class="active" data-table="param">参数</button><button type="button" data-table="option">标选配</button></div>
        <div class="tableScroll rawTable" data-name="param" data-open="true"><table><caption class="srOnly">全部原始参数数据</caption><thead><tr><th scope="col">类别</th><th scope="col">指标</th><th scope="col">单位</th>{param_head}</tr></thead><tbody>{param_rows}</tbody></table></div>
        <div class="tableScroll rawTable" data-name="option" data-open="false"><table><caption class="srOnly">全部原始标选配数据</caption><thead><tr><th scope="col">类别</th><th scope="col">配置</th><th scope="col">单位</th>{param_head}</tr></thead><tbody>{option_rows}</tbody></table></div>
      </details>
    </section>
  </main>
</div>
<script type="application/json" id="dashboard-data">{data_json}</script>
<script>
function setupRadars(){{
  document.querySelectorAll('.radarBox,.factorRadar').forEach(box=>{{
    const current=box.querySelector('.radarCurrent');
    const series=[...box.querySelectorAll('.radar-series[data-product]')];
    const controls=[...box.querySelectorAll('.radarLegend [data-product]')];
    const selected=new Set(controls.map(btn=>btn.dataset.product));
    const label=()=>{{
      if(!current) return;
      if(selected.size===controls.length) current.textContent='当前：全部品牌';
      else if(selected.size===0) current.textContent='当前：未选择品牌';
      else if(selected.size===1) current.textContent='当前：'+[...selected][0];
      else current.textContent='当前：'+selected.size+' 个品牌对比';
    }};
    const render=()=>{{
      const allSelected=selected.size===controls.length;
      box.classList.toggle('compare',!allSelected);
      series.forEach(s=>s.classList.toggle('selected',selected.has(s.dataset.product)));
      controls.forEach(btn=>{{
        const on=selected.has(btn.dataset.product);
        btn.classList.toggle('selected',on);
        btn.setAttribute('aria-pressed',String(on));
      }});
      label();
    }};
    const toggle=(product)=>{{
      if(selected.has(product)) selected.delete(product);
      else selected.add(product);
      render();
    }};
    controls.forEach(btn=>{{
      btn.setAttribute('aria-pressed','false');
      btn.addEventListener('click',()=>toggle(btn.dataset.product));
    }});
    series.forEach(shape=>{{
      shape.setAttribute('tabindex','0');
      shape.setAttribute('role','button');
      shape.addEventListener('click',()=>toggle(shape.dataset.product));
      shape.addEventListener('keydown',e=>{{
        if(e.key==='Enter'||e.key===' '){{
          e.preventDefault();
          toggle(shape.dataset.product);
        }}
      }});
    }});
    render();
  }});
}}
function setupSimulators(){{
    document.querySelectorAll('.simulator[data-base]').forEach(sim=>{{
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
function setupPageNavigation(){{
  const toggle=document.querySelector('.navToggle');
  const menu=document.querySelector('.navMenu');
  if(toggle&&menu){{
    toggle.addEventListener('click',()=>{{
      const open=menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded',String(open));
      toggle.textContent=open?'收起导航':'页面导航';
    }});
    menu.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{{
      if(window.matchMedia('(max-width:1200px)').matches){{
        menu.classList.remove('open');
        toggle.setAttribute('aria-expanded','false');
        toggle.textContent='页面导航';
      }}
    }}));
  }}
  const backTop=document.querySelector('.backTop');
  if(backTop){{
    const update=()=>backTop.classList.toggle('show',window.scrollY>640);
    window.addEventListener('scroll',update,{{passive:true}});
    update();
  }}
}}
function setupMobileDisclosures(){{
  const media=window.matchMedia('(max-width:720px)');
  const apply=()=>{{
    document.querySelectorAll('[data-mobile-open]').forEach(item=>{{
      item.open=media.matches ? item.dataset.mobileOpen==='true' : true;
    }});
  }};
  apply();
  if(media.addEventListener) media.addEventListener('change',apply);
  else if(media.addListener) media.addListener(apply);
}}
setupMobileDisclosures();
setupRadars();
setupSimulators();
setupRawTabs();
setupPageNavigation();
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
        ("https://xcmg-usa.com/wp-content/uploads/2025/08/XE45U_no-shadow-1-scaled.png", ASSET_DIR / "xe45u-official.png"),
        ("https://xcmg-usa.com/wp-content/uploads/2022/05/XE55U-1.jpg", ASSET_DIR / "xe55u-official.jpg"),
        ("https://xcmg-usa.com/wp-content/uploads/2024/03/XE75U_image.jpg", ASSET_DIR / "xe75u-official.jpg"),
        ("https://xcmg-usa.com/wp-content/uploads/2022/05/XE80U-1.jpg", ASSET_DIR / "xe80u-official.jpg"),
        ("https://xcmg-usa.com/wp-content/uploads/2022/05/XE155UCR-1.jpg", ASSET_DIR / "xe155ucr-official.jpg"),
    ]
    for url, dest in assets:
        if dest.exists() and dest.stat().st_size > 10000:
            continue
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            dest.write_bytes(response.read())
    xe135_cropped = ASSET_DIR / "xe135u-official-cropped.webp"
    if not xe135_cropped.exists() or xe135_cropped.stat().st_size <= 10000:
        xe135_source = ASSET_DIR / ".xe135u-official-source.png"
        req = urllib.request.Request(
            "https://xcmg-usa.com/wp-content/uploads/2025/04/135U_web-image.png",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            xe135_source.write_bytes(response.read())
        crop_product_image(xe135_source, xe135_cropped, max_dimension=1600)
        xe135_source.unlink(missing_ok=True)
    xe225_cropped = ASSET_DIR / "xe225u-official-cropped.png"
    if not xe225_cropped.exists() or xe225_cropped.stat().st_size <= 10000:
        xe225_source = ASSET_DIR / ".xe225u-official-source.png"
        req = urllib.request.Request(
            "https://xcmg-usa.com/wp-content/uploads/2025/04/225U_web-image.png",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            xe225_source.write_bytes(response.read())
        crop_product_image(xe225_source, xe225_cropped, max_dimension=1600)
        xe225_source.unlink(missing_ok=True)
    crop_product_image(ASSET_DIR / "xe19u-official.png", ASSET_DIR / "xe19u-official-cropped.png")
    crop_product_image(ASSET_DIR / "xe27u-official.jpg", ASSET_DIR / "xe27u-official-cropped.jpg")
    crop_product_image(ASSET_DIR / "xe45u-official.png", ASSET_DIR / "xe45u-official-cropped.png")
    crop_product_image(ASSET_DIR / "xe55u-official.jpg", ASSET_DIR / "xe55u-official-cropped.jpg")
    crop_product_image(ASSET_DIR / "xe75u-official.jpg", ASSET_DIR / "xe75u-official-cropped.jpg")
    crop_product_image(ASSET_DIR / "xe80u-official.jpg", ASSET_DIR / "xe80u-official-cropped.jpg")
    crop_product_image(ASSET_DIR / "xe155ucr-official.jpg", ASSET_DIR / "xe155ucr-official-cropped.jpg")


def crop_product_image(src, dest, max_dimension=None):
    from PIL import Image, ImageChops

    img = Image.open(src).convert("RGBA")
    alpha_bbox = img.split()[-1].getbbox()
    full_bbox = (0, 0, img.width, img.height)
    if alpha_bbox and alpha_bbox != full_bbox:
        bbox = alpha_bbox
    else:
        rgb = img.convert("RGB")
        near_white_mask = Image.new("L", img.size, 0)
        pixels = rgb.load()
        mask_pixels = near_white_mask.load()
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]
                if min(r, g, b) < 245:
                    mask_pixels[x, y] = 255
        bbox = near_white_mask.getbbox()
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
    if max_dimension and max(cropped.size) > max_dimension:
        scale = max_dimension / max(cropped.size)
        cropped = cropped.resize(
            (round(cropped.width * scale), round(cropped.height * scale)),
            Image.Resampling.LANCZOS,
        )
    if dest.suffix.lower() in {".jpg", ".jpeg"}:
        canvas = Image.new("RGB", cropped.size, "white")
        canvas.paste(cropped, mask=cropped.split()[-1])
        canvas.save(dest, quality=92)
    elif dest.suffix.lower() == ".webp":
        cropped.save(dest, format="WEBP", quality=88, method=6)
    else:
        cropped.save(dest)


def sync_data_files():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for meta in SOURCE_FILES:
        dest = DATA_DIR / meta["download"]
        if meta["source"].resolve() != dest.resolve():
            shutil.copy2(meta["source"], dest)


def _legacy_update_arc_page():
    arc_path = ROOT / "arc.html"
    text = arc_path.read_text(encoding="utf-8")
    text = text.replace("当前先上线 3.5 吨小挖项目，其他产品线保留入口，不伪造未完成结论。", "当前已上线 1-2 吨、2-3 吨、3-4 吨三个小挖吨级项目，其他产品线保留入口，不伪造未完成结论。")
    text = text.replace("<a class=\"btn yellow\" href=\"./\">进入小挖看板</a>", "<a class=\"btn yellow\" href=\"./\">进入挖掘机分析页</a>")
    text = text.replace("<div class=\"metric\"><strong>1</strong><span>已上线对标项目</span></div>", "<div class=\"metric\"><strong>3</strong><span>已上线对标项目</span></div>")
    text = text.replace("<div class=\"metric\"><strong>10</strong><span>小挖竞品型号</span></div>", "<div class=\"metric\"><strong>30</strong><span>小挖竞品型号</span></div>")
    text = text.replace("下一步建议先接入 Wheel Loaders 或 MEWP，二者更适合复用“工况 + 参数 + 配置包”的对标结构。", "小挖已形成 1-2 吨、2-3 吨、3-4 吨三个子板块；下一步建议接入 Wheel Loaders 或 MEWP。")
    text = text.replace("data/1-2.xlsx", "data/source-excel/XCMG_1-2t_mini_excavator_competitor_source.xlsx")
    text = text.replace("data/2-3.xlsx", "data/source-excel/XCMG_2-3t_mini_excavator_competitor_source.xlsx")
    text = text.replace("original-data.xlsx", "data/source-excel/XCMG_3.5t_mini_excavator_competitor_source.xlsx")
    text = text.replace("小挖、中挖、大挖；当前已上线 3.5 吨小挖竞品对标。", "小挖、中挖、大挖；当前已上线 1-2 吨、2-3 吨、3-4 吨三个小挖子板块。")
    text = text.replace('<div class="chips"><span class="chip live">3.5t 小挖</span><span class="chip">中挖预留</span></div>', '<div class="chips"><span class="chip live">1-2t</span><span class="chip live">2-3t</span><span class="chip live">3-4t</span></div>')
    text = text.replace('<div class="cardActions"><a class="btn yellow" href="./">打开小挖</a><button class="btn disabled" type="button">中挖待接入</button></div>', '<div class="cardActions"><a class="btn yellow" href="./">3-4 吨</a><a class="btn light" href="excavator-2-3t.html">2-3 吨</a><a class="btn light" href="excavator-1-2t.html">1-2 吨</a></div>')
    text = text.replace("把可用项目单独放出来，避免和预留入口混在一起。当前小挖项目仍使用原访问地址。", "把可用项目单独放出来，避免和预留入口混在一起。3-4 吨小挖项目仍使用原访问地址。")
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
            <div class="actions"><a class="btn blue" href="./">打开小挖看板</a><a class="btn light" href="data/source-excel/XCMG_3.5t_mini_excavator_competitor_source.xlsx" download>下载原始数据</a></div>
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
            <div class="actions"><a class="btn blue" href="excavator-1-2t.html">打开 1-2 吨</a><a class="btn light" href="data/source-excel/XCMG_1-2t_mini_excavator_competitor_source.xlsx" download>下载原始数据</a></div>
          </div>
        </article>

        <article class="panel project">
          <div class="projectImage"><img src="assets/arc/xe27u-official-cropped.jpg" alt="XCMG XE27U"></div>
          <div class="projectBody">
            <h3>2-3 吨级小型挖掘机竞品对标</h3>
            <p>XCMG XE27U 对比卡特、迪尔、山猫、久保田、沃尔沃、现代、斗山、三一等竞品，复用统一工况、参数和配置逻辑。</p>
            <div class="factRow">
              <div class="fact"><b>6</b><span>典型工况</span></div>
              <div class="fact"><b>9</b><span>对标产品</span></div>
              <div class="fact"><b>可交互</b><span>雷达 / 排名 / 模拟</span></div>
            </div>
            <div class="actions"><a class="btn blue" href="excavator-2-3t.html">打开 2-3 吨</a><a class="btn light" href="data/source-excel/XCMG_2-3t_mini_excavator_competitor_source.xlsx" download>下载原始数据</a></div>
          </div>
        </article>

        <article class="panel project">
          <div class="projectImage"><img src="assets/arc/xe35u-official-cropped.jpg" alt="XCMG XE35U"></div>
          <div class="projectBody">
            <h3>3-4 吨级小型挖掘机竞品对标</h3>
            <p>XCMG XE35U 对比沃尔沃、现代、迪尔、卡特、山猫、斗山、久保田、三一等竞品，原访问地址保持不变。</p>
            <div class="factRow">
              <div class="fact"><b>6</b><span>典型工况</span></div>
              <div class="fact"><b>10</b><span>对标产品</span></div>
              <div class="fact"><b>可交互</b><span>雷达 / 排名 / 模拟</span></div>
            </div>
            <div class="actions"><a class="btn blue" href="./">打开 3-4 吨</a><a class="btn light" href="data/source-excel/XCMG_3.5t_mini_excavator_competitor_source.xlsx" download>下载原始数据</a></div>
          </div>
        </article>
      </section>'''
    if old in text:
        text = text.replace(old, new)
    else:
        text = text.replace("assets/arc/xe19u-official.png", "assets/arc/xe19u-official-cropped.png")
        text = text.replace("assets/arc/xe27u-official.jpg", "assets/arc/xe27u-official-cropped.jpg")
    text = text.replace("小挖竞品看板原地址保持不变。", "小挖 1-2 吨、2-3 吨、3-4 吨子板块已上线；3-4 吨原地址保持不变。")
    arc_path.write_text(text, encoding="utf-8", newline="\n")


def update_arc_metrics(models):
    arc_path = ROOT / "arc.html"
    text = arc_path.read_text(encoding="utf-8")
    values = {
        "ARC_PRODUCT_LINES": 7,
        "ARC_TONNAGES": len(models),
        "ARC_PRODUCTS": sum(len(model["products"]) for model in models),
        "ARC_SOURCES": len(SOURCE_FILES),
    }
    for marker, value in values.items():
        pattern = rf"<!-- {marker} -->.*?<!-- /{marker} -->"
        replacement = f"<!-- {marker} -->{value}<!-- /{marker} -->"
        text, count = re.subn(pattern, replacement, text, flags=re.S)
        if count != 1:
            raise ValueError(f"ARC metric marker missing or duplicated: {marker}")
    arc_path.write_text(text, encoding="utf-8", newline="\n")


def write_project_manifest(models):
    manifest = {
        "productLineCount": 7,
        "excavatorTonnageCount": len(models),
        "benchmarkProductCount": sum(len(model["products"]) for model in models),
        "sourceWorkbookCount": len(SOURCE_FILES),
        "minimumScoreCoverage": MIN_SCORE_COVERAGE,
        "overallWeights": OVERALL_WEIGHTS,
        "dashboards": [
            {
                "label": model["meta"]["label"],
                "output": model["meta"]["output"],
                "xcmg": model["meta"]["xcmg"],
                "productCount": len(model["products"]),
                "source": f'data/source-excel/{model["meta"]["download"]}',
            }
            for model in models
        ],
    }
    (ROOT / "data" / "project-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def externalize_dashboard_assets(page_html):
    style_start = page_html.index("  <style>")
    style_end = page_html.index("  </style>", style_start) + len("  </style>")
    css = page_html[style_start + len("  <style>"): style_end - len("  </style>")].strip() + "\n"

    script_start = page_html.rfind("<script>")
    script_end = page_html.index("</script>", script_start) + len("</script>")
    javascript = page_html[script_start + len("<script>"): script_end - len("</script>")].strip() + "\n"

    assets_dir = ROOT / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    (assets_dir / "dashboard.css").write_text(css, encoding="utf-8", newline="\n")
    (assets_dir / "dashboard.js").write_text(javascript, encoding="utf-8", newline="\n")

    page_html = page_html[:style_start] + '  <link rel="stylesheet" href="assets/dashboard.css">' + page_html[style_end:]
    script_start = page_html.rfind("<script>")
    script_end = page_html.index("</script>", script_start) + len("</script>")
    page_html = page_html[:script_start] + '<script src="assets/dashboard.js"></script>' + page_html[script_end:]
    return page_html


def main():
    download_assets()
    sync_data_files()
    models = []
    for meta in SOURCE_FILES:
        wb = load_workbook(meta["source"])
        model = build_model(wb, meta)
        models.append(model)
        page_html = externalize_dashboard_assets(render_html(model))
        (ROOT / meta["output"]).write_text(page_html, encoding="utf-8", newline="\n")
    write_project_manifest(models)
    update_arc_metrics(models)


if __name__ == "__main__":
    main()
