import html
import json
import math
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

try:
    from .render_ppt_charts import render_chart_figure
except ImportError:
    from render_ppt_charts import render_chart_figure


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "source-excel"
ASSET_DIR = ROOT / "assets" / "arc"
TONNAGE_INSIGHT_PATH = ROOT / "data" / "ppt-insights" / "tonnage-insights.json"
PPT_BUSINESS_TABLE_PATH = ROOT / "data" / "ppt-insights" / "ppt-business-tables.json"
PPT_SOURCE_CONTENT_PATH = ROOT / "data" / "ppt-insights" / "ppt-source-content.json"


def load_tonnage_insights():
    if not TONNAGE_INSIGHT_PATH.exists():
        return {}
    payload = json.loads(TONNAGE_INSIGHT_PATH.read_text(encoding="utf-8"))
    return {record["slug"]: record for record in payload.get("records", [])}


def load_ppt_business_tables():
    if not PPT_BUSINESS_TABLE_PATH.exists():
        return {"records": {}, "by_slug": {}, "summary": {}}
    payload = json.loads(PPT_BUSINESS_TABLE_PATH.read_text(encoding="utf-8"))
    records = {record["id"]: record for record in payload.get("records", [])}
    return {
        "records": records,
        "by_slug": payload.get("by_slug", {}),
        "summary": payload.get("summary", {}),
    }


def load_ppt_source_content():
    if not PPT_SOURCE_CONTENT_PATH.exists():
        return {"slides": {}, "by_slug": {}, "overview": [], "summary": {}}
    payload = json.loads(PPT_SOURCE_CONTENT_PATH.read_text(encoding="utf-8"))
    slides = {record["id"]: record for record in payload.get("slides", [])}
    return {
        "slides": slides,
        "by_slug": payload.get("by_slug", {}),
        "overview": payload.get("overview", []),
        "summary": payload.get("summary", {}),
    }


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
    {
        "slug": "excavator-24-28t",
        "output": "excavator-24-28t.html",
        "label": "24-28 吨级",
        "title": "XCMG XE250U 24-28 吨级挖掘机竞品对标看板",
        "xcmg": "XCMG XE250U",
        "source": DATA_DIR / "XCMG_24-28t_excavator_competitor_source.xlsx",
        "download": "XCMG_24-28t_excavator_competitor_source.xlsx",
        "image": "assets/arc/xe250u-official-cropped.webp",
        "image_source": "XCMG USA XE250U",
    },
    {
        "slug": "excavator-24-28t-short-tail",
        "output": "excavator-24-28t-short-tail.html",
        "label": "24-28 吨级短尾",
        "title": "XCMG XE235UCR 24-28 吨级短尾挖掘机竞品对标看板",
        "xcmg": "XCMG XE235UCR",
        "source": DATA_DIR / "XCMG_24-28t_short_tail_excavator_competitor_source.xlsx",
        "download": "XCMG_24-28t_short_tail_excavator_competitor_source.xlsx",
        "image": "assets/arc/xe235ucr-official-cropped.webp",
        "image_source": "XCMG USA XE235UCR",
    },
    {
        "slug": "excavator-28-33t",
        "output": "excavator-28-33t.html",
        "label": "28-33 吨级",
        "title": "XCMG XE300U 28-33 吨级挖掘机竞品对标看板",
        "xcmg": "XCMG XE300U",
        "source": DATA_DIR / "XCMG_28-33t_excavator_competitor_source.xlsx",
        "download": "XCMG_28-33t_excavator_competitor_source.xlsx",
        "image": "assets/arc/xe300u-official-cropped.webp",
        "image_source": "XCMG USA XE300U",
    },
    {
        "slug": "excavator-33-40t",
        "output": "excavator-33-40t.html",
        "label": "33-40 吨级",
        "title": "XCMG XE360U 33-40 吨级挖掘机竞品对标看板",
        "xcmg": "XCMG XE360U",
        "source": DATA_DIR / "XCMG_33-40t_excavator_competitor_source.xlsx",
        "download": "XCMG_33-40t_excavator_competitor_source.xlsx",
        "image": "assets/arc/xe360u-official-cropped.webp",
        "image_source": "XCMG USA XE360U",
    },
    {
        "slug": "excavator-40-60t",
        "output": "excavator-40-60t.html",
        "label": "40-60 吨级",
        "title": "XCMG XE490U 40-60 吨级挖掘机竞品对标看板",
        "xcmg": "XCMG XE490U",
        "source": DATA_DIR / "XCMG_40-60t_excavator_competitor_source.xlsx",
        "download": "XCMG_40-60t_excavator_competitor_source.xlsx",
        "image": "assets/arc/xe490u-official.jpg",
        "image_source": "XCMG USA XE490U",
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
        "image": "assets/conditions/narrow-urban.jpg",
        "image_alt": "徐工挖掘机在受限道路边施工的工况示意",
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
        "image": "assets/conditions/trench-foundation.jpg",
        "image_alt": "徐工挖掘机进行基础施工的工况示意",
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
        "image": "assets/conditions/loading-cycle.jpg",
        "image_alt": "徐工挖掘机进行土方装车的工况示意",
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
        "image": "assets/conditions/breaker-attachments.jpg",
        "image_alt": "徐工挖掘机在岩石施工现场作业的工况示意",
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
        "image": "assets/conditions/slope-soft-ground.jpg",
        "image_alt": "徐工挖掘机在坡地和松软地面施工的工况示意",
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
        "image": "assets/conditions/rental-fleet.jpg",
        "image_alt": "多台徐工挖掘机协同施工的工况示意",
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
    clean_product = lambda value: re.sub(r"\s+", " ", clean(value)).strip()
    products = [clean_product(x) for x in param.iloc[0, 3:].tolist() if clean_product(x)]

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
    opt_products = [clean_product(x) for x in option.iloc[0, 2:].tolist() if clean_product(x)]
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
    normalize_cell = lambda value: re.sub(r"\s+", " ", clean(value)).strip()
    out = []
    for row in rows[: limit or len(rows)]:
        cells = "".join(f"<td>{esc(normalize_cell(row['values'].get(p, ''))) or '-'}</td>" for p in products)
        out.append(f"<tr><th scope=\"row\">{esc(normalize_cell(row['category']))}</th><td>{esc(normalize_cell(row['item']))}</td><td>{esc(normalize_cell(row.get('unit','')))}</td>{cells}</tr>")
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


def render_product_gap_spotlight(model, xcmg, leader):
    param_gaps = [
        (*gap, "参数")
        for row in model["rawParamRows"]
        if (gap := raw_param_gap_text(row, model, xcmg))
    ]
    option_gaps = [
        (*gap, "配置")
        for row in model["rawOptionRows"]
        if (gap := raw_option_gap_text(row, model, xcmg))
    ]
    gaps = sorted(param_gaps + option_gaps, reverse=True, key=lambda item: item[0])[:4]
    if gaps:
        items = "、".join(gap[2] for gap in gaps)
        rows = "".join(
            '<li>'
            f'<span>{idx:02d}</span><div><small>{esc(gap[3])}</small><b>{esc(gap[2])}</b><p>{esc(gap[1])}</p></div>'
            '</li>'
            for idx, gap in enumerate(gaps, start=1)
        )
        title = f"与 {leader['product']} 的具体差距"
        summary = f"当前可核验差距集中在 {items}。以下均为原始参数或标选配状态，不用综合分替代实际差异。"
    else:
        title = "当前资料未显示明确落后项"
        summary = "继续复核缺失字段、配置口径和来源版本，避免把未披露信息误判为无配置。"
        rows = '<li class="gapEmpty"><span>01</span><div><small>数据复核</small><b>来源与口径</b><p>补齐缺失字段并核验同版本、同配置条件后再形成产品目标。</p></div></li>'
    return (
        '<div class="productGapSpotlight">'
        '<div class="productGapMedia">'
        '<span>Product Gap Focus</span>'
        f'<img src="{esc(model["meta"]["image"])}" alt="{esc(xcmg)} 产品图">'
        f'<div><b>{esc(xcmg)}</b><small>当前对标产品</small></div>'
        '</div>'
        '<div class="productGapContent">'
        '<span>参数与配置实差</span>'
        f'<h3>{esc(title)}</h3><p>{esc(summary)}</p><ol>{rows}</ol>'
        '</div>'
        '</div>'
    )


def render_condition_visual_nav(model):
    cards = []
    for idx, condition in enumerate(model["conditions"], start=1):
        focus = "、".join(item[1] for item in condition["items"][:3])
        cards.append(
            f'<a class="conditionVisualCard" href="#cond{idx}">'
            f'<img src="{esc(condition["image"])}" alt="{esc(condition["image_alt"])}">'
            '<div>'
            f'<span>典型工况 {idx:02d}</span><strong>{esc(condition["name"])}</strong>'
            f'<small>关键项：{esc(focus)}</small>'
            '</div></a>'
        )
    return (
        '<div class="conditionVisualNav">'
        + "".join(cards)
        + '</div><p class="conditionVisualSource">图片来源：徐工官方施工案例，仅用于工况示意；本页参数、配置和排名仍以对应吨级原始数据为准。</p>'
    )


def render_overall_section(model):
    xcmg = model["meta"]["xcmg"]
    rank, xscore, rows = xcmg_rank(model["overall"], xcmg)
    leader = rows[0] if rows else {"product": "-", "score": 0}
    gap_notes = render_overall_gap_notes(model, xcmg, leader)
    gap_spotlight = render_product_gap_spotlight(model, xcmg, leader)
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
        + gap_spotlight
        + '<div class="split">'
        f'<div class="panel"><h3>总体评分排名</h3><div class="bars">{render_bar_ranking(model["overall"], xcmg, coverage=model["overallCoverage"])}</div><p class="coverageNote">覆盖率低于 {int(MIN_SCORE_COVERAGE*100)}% 的产品不进入排名，仍在右侧表格中保留并标记为“数据不足”。</p></div>'
        '<div class="panel"><h3>XCMG 总体差距分析</h3>'
        + gap_notes
        + '<details class="mobileDisclosure overallTableDisclosure" open data-mobile-open="false"><summary>完整评分明细</summary><div class="tableScroll compact"><table><caption class="srOnly">总体评分、参数评分、配置评分及数据覆盖率</caption><thead><tr><th scope="col">产品</th><th scope="col">总体</th><th scope="col">参数</th><th scope="col">配置</th><th scope="col">数据覆盖</th><th scope="col">完整度等级</th></tr></thead><tbody>'
        + overall_table
        + '</tbody></table></div></details></div></div></section>'
    )


def bilingual_leaf(value, tag="span", class_name=""):
    if isinstance(value, dict):
        zh = value.get("zh", "")
        en = value.get("en") or zh
    else:
        zh = en = str(value or "")
    class_attr = f' class="{esc(class_name)}"' if class_name else ""
    return f'<{tag}{class_attr} data-en="{esc(en)}">{esc(zh)}</{tag}>'


def clean_ppt_table_title(value):
    value = str(value or "")
    prefixes = (
        "二、大区产业板块洞察 | ",
        "二、细分市场洞察 | ",
        "2、核心产品线—履带式挖掘机 ",
        "2、核心产品线—挖掘机 ",
    )
    for prefix in prefixes:
        if value.startswith(prefix):
            value = value[len(prefix):]
    return re.sub(r"\s+", " ", value).strip()


def render_ppt_business_table(record):
    matrix = record.get("matrix_zh") or []
    if not matrix:
        return ""
    width = max((len(row) for row in matrix), default=1)
    rows = [
        list(row) + [""] * max(0, width - len(row))
        for row in matrix
    ]
    header = "".join(
        f'<th scope="col">{esc(cell) if cell else "&nbsp;"}</th>'
        for cell in rows[0]
    )
    body = []
    for row in rows[1:]:
        cells = []
        for index, cell in enumerate(row):
            tag = "th" if index == 0 else "td"
            scope = ' scope="row"' if index == 0 else ""
            cells.append(
                f'<{tag}{scope}>{esc(cell) if cell else "&nbsp;"}</{tag}>'
            )
        body.append(f'<tr>{"".join(cells)}</tr>')
    title = clean_ppt_table_title(record.get("title"))
    english_titles = {
        "market": "Complete market-data table",
        "application": "Complete application-fit table",
        "product_comparison": "Complete specification, equipment and field-evaluation table",
        "positioning": "Complete product-positioning and historical-target table",
    }
    english_title = english_titles.get(
        record.get("role"),
        "Complete business-data table",
    )
    return (
        f'<details class="pptBusinessTable" open data-source-slide="{record.get("slide")}" '
        f'data-table-role="{esc(record.get("role"))}">'
        '<summary>'
        f'<h3 data-en="{esc(english_title)}">{esc(title)}</h3>'
        f'<span data-en="{record.get("rows", len(rows))} rows × {record.get("columns", width)} columns">'
        f'{record.get("rows", len(rows))} 行 × {record.get("columns", width)} 列</span>'
        '</summary>'
        '<div class="pptBusinessTableScroll">'
        '<table lang="zh-CN">'
        f'<caption class="srOnly">{esc(title)}</caption>'
        f'<thead><tr>{header}</tr></thead>'
        f'<tbody>{"".join(body)}</tbody>'
        '</table></div></details>'
    )


def render_ppt_table_group(records, roles, title, title_en, lead, lead_en):
    selected = [record for record in records if record.get("role") in roles]
    if not selected:
        return ""
    return (
        '<div class="pptBusinessGroup">'
        '<div class="pptBusinessGroupHead">'
        f'<h3 data-en="{esc(title_en)}">{esc(title)}</h3>'
        f'<p data-en="{esc(lead_en)}">{esc(lead)}</p>'
        '</div>'
        f'<div class="pptBusinessTableStack">{"".join(render_ppt_business_table(record) for record in selected)}</div>'
        '</div>'
    )


def market_status_label(status):
    labels = {
        "historical_actual": {"zh": "历史实际", "en": "Historical actual"},
        "historical_estimate": {"zh": "历史估计", "en": "Historical estimate"},
        "historical_forecast": {"zh": "原资料预测", "en": "Original forecast"},
    }
    return labels.get(status, {"zh": "历史口径", "en": "Historical basis"})


def market_color(brand, index):
    if "XCMG" in str(brand).upper():
        return "#f5b400"
    palette = ["#005ca9", "#397fb8", "#829db6", "#137a47", "#6b5aa6", "#9b5b37"]
    return palette[index % len(palette)]


def render_market_chart(insight):
    chart = insight.get("market_chart") or {}
    years = chart.get("years") or []
    series = chart.get("series") or []
    statuses = chart.get("status") or []
    if not years or not series:
        return (
            '<div class="marketSeriesEmpty">'
            + bilingual_leaf({
                "zh": "本吨级在现有市场资料中未单独拆分销量序列。页面只呈现该吨级能够独立核验的客户、运输、应用和工程判断，不借用相邻吨级数据。",
                "en": "The available market material does not separate a sales series for this class. This page uses only class-specific customer, transport, application and engineering evidence rather than borrowing adjacent-class data.",
            }, "p")
            + "</div>"
        )

    totals = [sum(item.get("values", [0] * len(years))[i] for item in series) for i in range(len(years))]
    max_total = max(totals) or 1
    columns = []
    for year_index, year in enumerate(years):
        year_match = re.search(r"\d{4}", str(year))
        year_label = year_match.group(0) if year_match else str(year)
        total = totals[year_index]
        segments = []
        for brand_index, item in enumerate(series):
            values = item.get("values") or []
            value = values[year_index] if year_index < len(values) else 0
            if value <= 0 or total <= 0:
                continue
            height = value / total * 100
            color = market_color(item.get("brand"), brand_index)
            segments.append(
                f'<span style="height:{height:.3f}%;background:{color}" title="{esc(item.get("brand"))}: {value:,}"></span>'
            )
        overall_height = max(10, total / max_total * 100)
        status = statuses[year_index] if year_index < len(statuses) else ""
        columns.append(
            '<div class="marketColumn">'
            f'<div class="marketBarShell"><div class="marketBar" style="height:{overall_height:.2f}%">{"".join(segments)}</div></div>'
            f'<b>{esc(year_label)}</b><strong>{total:,} {bilingual_leaf({"zh": "台", "en": "units"})}</strong>'
            + bilingual_leaf(market_status_label(status), "small")
            + "</div>"
        )
    legend = "".join(
        f'<span><i style="background:{market_color(item.get("brand"), index)}"></i>{esc(item.get("brand"))}</span>'
        for index, item in enumerate(series)
    )
    return (
        '<div class="marketChart" role="img" aria-label="按品牌展示历史销量、估计值与原预测值">'
        f'<div class="marketColumns">{"".join(columns)}</div>'
        f'<div class="marketLegend">{legend}</div>'
        "</div>"
    )


def render_market_detail(insight):
    chart = insight.get("market_chart") or {}
    years = chart.get("years") or []
    series = chart.get("series") or []
    statuses = chart.get("status") or []
    if not years or not series:
        return (
            '<div class="marketEvidenceBoundary">'
            + bilingual_leaf({
                "zh": "本吨级没有独立拆分的品牌销量明细，因此不生成市场份额、增长率或品牌排名。客户、运输、作业场景和工程判断仍按本吨级已有记录呈现。",
                "en": "No class-specific brand-volume series is available, so this page does not calculate market share, growth or brand rank. Customer, transport, application and engineering findings remain limited to the evidence recorded for this class.",
            }, "p")
            + "</div>"
        )

    totals = [
        sum((item.get("values") or [0] * len(years))[index] for item in series)
        for index in range(len(years))
    ]
    actual_indices = [
        index for index, status in enumerate(statuses)
        if status == "historical_actual"
    ]
    latest_actual_index = actual_indices[-1] if actual_indices else min(1, len(years) - 1)
    previous_actual_index = actual_indices[-2] if len(actual_indices) > 1 else None
    latest_total = totals[latest_actual_index]

    latest_values = [
        ((item.get("values") or [0] * len(years))[latest_actual_index], item)
        for item in series
    ]
    leader_value, leader = max(latest_values, key=lambda entry: entry[0])
    leader_share = leader_value / latest_total * 100 if latest_total else 0
    xcmg = next(
        (item for item in series if "XCMG" in str(item.get("brand", "")).upper()),
        None,
    )
    xcmg_value = (
        (xcmg.get("values") or [0] * len(years))[latest_actual_index]
        if xcmg else 0
    )
    xcmg_share = xcmg_value / latest_total * 100 if latest_total else 0

    if previous_actual_index is not None and totals[previous_actual_index]:
        change = (
            (latest_total - totals[previous_actual_index])
            / totals[previous_actual_index]
            * 100
        )
        change_zh = f"{change:+.1f}%"
        change_en = f"{change:+.1f}%"
        comparison_zh = (
            f"{years[latest_actual_index]} 合计 {latest_total:,} 台，"
            f"较 {years[previous_actual_index]} 的 {totals[previous_actual_index]:,} 台"
            f"变化 {change_zh}。"
        )
        comparison_en = (
            f"{years[latest_actual_index]} totals {latest_total:,} units, "
            f"{change_en} versus {totals[previous_actual_index]:,} units in "
            f"{years[previous_actual_index]}."
        )
    else:
        comparison_zh = f"{years[latest_actual_index]} 可核验市场规模为 {latest_total:,} 台。"
        comparison_en = f"The verifiable {years[latest_actual_index]} market volume is {latest_total:,} units."

    gap_value = max(0, leader_value - xcmg_value)
    facts = [
        {
            "label": {"zh": "市场变化", "en": "Market movement"},
            "value": comparison_zh,
            "value_en": comparison_en,
        },
        {
            "label": {"zh": "领先品牌", "en": "Leading brand"},
            "value": (
                f"{leader.get('brand')} 在 {years[latest_actual_index]} 为 {leader_value:,} 台，"
                f"占本表合计约 {leader_share:.1f}%。"
            ),
            "value_en": (
                f"{leader.get('brand')} records {leader_value:,} units in "
                f"{years[latest_actual_index]}, about {leader_share:.1f}% of the displayed total."
            ),
        },
        {
            "label": {"zh": "XCMG 位置", "en": "XCMG position"},
            "value": (
                f"{years[latest_actual_index]} 记录 {xcmg_value:,} 台，约占 {xcmg_share:.1f}%；"
                f"与表内领先品牌相差 {gap_value:,} 台。"
            ),
            "value_en": (
                f"XCMG records {xcmg_value:,} units in {years[latest_actual_index]}, "
                f"about {xcmg_share:.1f}%, with a {gap_value:,}-unit gap to the displayed leader."
            ),
        },
    ]
    fact_html = "".join(
        '<article>'
        + bilingual_leaf(fact["label"], "b")
        + bilingual_leaf({"zh": fact["value"], "en": fact["value_en"]}, "p")
        + "</article>"
        for fact in facts
    )

    header_cells = []
    for index, year in enumerate(years):
        year_match = re.search(r"\d{4}", str(year))
        year_label = year_match.group(0) if year_match else str(year)
        header_cells.append(
            f'<th scope="col"><span>{esc(year_label)}</span>'
            + bilingual_leaf(
                market_status_label(statuses[index] if index < len(statuses) else ""),
                "small",
            )
            + "</th>"
        )
    header_cells = "".join(header_cells)
    body_rows = []
    for item in series:
        values = item.get("values") or []
        cells = "".join(
            f"<td>{(values[index] if index < len(values) else 0):,}</td>"
            for index in range(len(years))
        )
        row_class = " xcmgMarketRow" if "XCMG" in str(item.get("brand", "")).upper() else ""
        body_rows.append(
            f'<tr class="{row_class.strip()}"><th scope="row">{esc(item.get("brand"))}</th>{cells}</tr>'
        )
    total_cells = "".join(f"<td>{value:,}</td>" for value in totals)
    body_rows.append(
        '<tr class="marketTotalRow"><th scope="row" data-en="Displayed total">表内合计</th>'
        f"{total_cells}</tr>"
    )
    return (
        '<div class="marketEvidenceGrid">'
        '<article class="marketDataPanel"><div class="insightPanelTitle"><span data-en="Brand volume detail">品牌销量明细</span></div>'
        '<div class="marketDataTableWrap"><table class="marketDataTable"><caption class="srOnly" data-en="Brand volume by year and data status">分品牌、年份与数据状态的销量明细</caption>'
        f'<thead><tr><th scope="col" data-en="Brand">品牌</th>{header_cells}</tr></thead>'
        f'<tbody>{"".join(body_rows)}</tbody></table></div></article>'
        '<article class="marketFactPanel"><div class="insightPanelTitle"><span data-en="Quantified reading">量化结论</span></div>'
        f'<div class="marketFactList">{fact_html}</div></article>'
        "</div>"
    )


def render_market_insight(insight, business_tables=None):
    business_tables = business_tables or []
    chart = insight.get("market_chart") or {}
    years = chart.get("years") or []
    series = chart.get("series") or []
    totals = [sum(item.get("values", [0] * len(years))[i] for item in series) for i in range(len(years))] if years else []
    actual_index = 1 if len(years) > 1 else 0
    actual_value = f"{totals[actual_index]:,}" if totals else "--"
    actual_label_zh = f"{years[actual_index]} 实际规模" if years else "独立销量序列"
    actual_label_en = f"{years[actual_index]} actual market" if years else "Class sales series"
    xcmg_series = next((item for item in series if "XCMG" in str(item.get("brand", "")).upper()), None)
    if xcmg_series and xcmg_series.get("values"):
        values = xcmg_series["values"]
        xcmg_zh = f"{values[0]:,} → {values[-1]:,} 台"
        xcmg_en = f"{values[0]:,} → {values[-1]:,} units"
    else:
        xcmg_zh = "暂无独立序列"
        xcmg_en = "No separate series"
    source_slides = insight.get("source_slides") or []
    source_attr = f' data-source-slides="{esc("-".join(str(value) for value in source_slides))}"'
    return (
        f'<section id="market-insight" class="insightSection"{source_attr}>'
        f'<h2>{bilingual_leaf({"zh": "市场、客户与运输适配", "en": "Market, Customer and Transport Fit"})}</h2>'
        '<div class="marketKpis">'
        f'<div><span data-en="{esc(actual_label_en)}">{esc(actual_label_zh)}</span><b>{actual_value}</b>{bilingual_leaf({"zh": "台", "en": "units"}, "small") if totals else ""}</div>'
        f'<div><span data-en="XCMG volume path">XCMG 销量路径</span>{bilingual_leaf({"zh": xcmg_zh, "en": xcmg_en}, "b")}</div>'
        f'<div><span data-en="Competitive concentration">竞争集中度</span>{bilingual_leaf(insight.get("concentration"), "b")}</div>'
        f'<div><span data-en="Primary benchmark">主要标杆</span>{bilingual_leaf(insight.get("benchmark"), "b")}</div>'
        "</div>"
        '<div class="marketInsightGrid">'
        '<article class="marketTrendPanel"><div class="insightPanelTitle"><span data-en="Historical market structure">历史市场结构</span></div>'
        + render_market_chart(insight)
        + bilingual_leaf({
            "zh": "时间口径：2023-2024 为历史实际，2025 为原资料中的历史估计，2026 为原预测值；2026 实际销量需在最新数据到位后回填。",
            "en": "Time basis: 2023-2024 are historical actuals, 2025 is the historical estimate in the source material, and 2026 is the original forecast. Replace it with 2026 actuals when current data is available.",
        }, "p", "marketTimeBasis")
        + "</article>"
        '<article class="marketReading"><div class="insightPanelTitle"><span data-en="Class decision view">吨级判断</span></div>'
        + bilingual_leaf(insight.get("role"), "p", "marketRole")
        + '<dl class="marketDecisionList">'
        f'<div><dt data-en="Primary customers">主要客户</dt><dd>{bilingual_leaf(insight.get("customers"))}</dd></div>'
        f'<div><dt data-en="Typical jobs">典型任务</dt><dd>{bilingual_leaf(insight.get("jobs"))}</dd></div>'
        f'<div><dt data-en="Purchase priorities">购买重点</dt><dd>{bilingual_leaf(insight.get("purchase"))}</dd></div>'
        f'<div class="transportDecision"><dt data-en="Transport boundary">运输边界</dt><dd>{bilingual_leaf(insight.get("transport"))}</dd></div>'
        "</dl></article></div>"
        + render_market_detail(insight)
        + render_ppt_table_group(
            business_tables,
            {"market"},
            "完整市场数据表",
            "Complete market data tables",
            "按品牌、年份和机型保留该吨级市场表中的全部业务数据。",
            "All business data from the class market tables are retained by brand, year and model.",
        )
        + "</section>"
    )


def render_application_insight(insight, business_tables=None):
    business_tables = business_tables or []
    cards = []
    matrix_rows = []
    for item in insight.get("applications", []):
        cards.append(
            f'<article class="applicationCard" data-source-slide="{esc(item.get("source_slide"))}">'
            '<figure>'
            f'<img src="{esc(item.get("image"))}" alt="{esc(item.get("title", {}).get("zh", "作业场景"))}" loading="lazy">'
            f'<figcaption>{bilingual_leaf(item.get("title"), "strong")}</figcaption>'
            "</figure>"
            f'{bilingual_leaf(item.get("body"), "p")}'
            '<div class="applicationRequirement"><span data-en="Capability requirements">能力要求</span>'
            f'{bilingual_leaf(item.get("requirements"), "b")}</div></article>'
        )
        matrix_rows.append(
            "<tr>"
            f'<th scope="row">{bilingual_leaf(item.get("title"), "b")}</th>'
            f"<td>{bilingual_leaf(item.get('body'))}</td>"
            f'<td class="applicationCapabilityCell">{bilingual_leaf(item.get("requirements"))}</td>'
            "</tr>"
        )
    return (
        '<section id="job-applications" class="insightSection">'
        f'<h2>{bilingual_leaf({"zh": "真实作业场景", "en": "Real Job Applications"})}</h2>'
        + bilingual_leaf({
            "zh": "以下场景按本吨级客户的实际任务链展开，直接说明机器需要完成什么工作，以及参数、配置和操控应满足哪些边界。",
            "en": "These applications follow the actual task chain for this class and show what the machine must accomplish and which specification, equipment and control boundaries matter.",
        }, "p", "insightLead")
        + f'<div class="applicationGrid">{"".join(cards)}</div>'
        '<div class="applicationMatrixWrap"><div class="insightPanelTitle"><span data-en="Job-to-capability comparison">任务与能力对照</span></div>'
        '<table class="applicationMatrix"><caption class="srOnly" data-en="Application task and capability comparison">作业任务与关键能力对照</caption>'
        '<thead><tr><th scope="col" data-en="Application">作业场景</th><th scope="col" data-en="Customer task">客户任务</th><th scope="col" data-en="Critical machine capability">关键整机能力</th></tr></thead>'
        f'<tbody>{"".join(matrix_rows)}</tbody></table></div>'
        + render_ppt_table_group(
            business_tables,
            {"application"},
            "完整工况适应性表",
            "Complete application-fit tables",
            "保留客户、任务链、运输边界、关键能力和产品适配判断的全部表格内容。",
            "Retains the complete customer, task-chain, transport-boundary, capability and product-fit table content.",
        )
        + "</section>"
    )


def render_engineering_insight(insight, business_tables=None):
    business_tables = business_tables or []
    rows = []
    priorities = []
    for item in insight.get("engineering", []):
        priorities.append(
            '<article>'
            f'{bilingual_leaf(item.get("dimension"), "b")}'
            f'{bilingual_leaf(item.get("gap"), "p")}'
            "</article>"
        )
        rows.append(
            f'<tr data-source-slides="{esc("-".join(str(value) for value in item.get("source_slides", [])))}">'
            f'<th scope="row"><span class="cellLabel" data-en="Dimension">维度</span>{bilingual_leaf(item.get("dimension"), "b")}</th>'
            f'<td><span class="cellLabel" data-en="Existing foundation">已有基础</span>{bilingual_leaf(item.get("basis"))}</td>'
            f'<td class="gapColumn"><span class="cellLabel" data-en="Specific gap">具体差距</span>{bilingual_leaf(item.get("gap"))}</td>'
            f'<td class="actionColumn"><span class="cellLabel" data-en="Closing action">弥补动作</span>{bilingual_leaf(item.get("action"))}</td>'
            "</tr>"
        )
    return (
        '<section id="engineering-insight" class="insightSection">'
        f'<h2>{bilingual_leaf({"zh": "实机与工程判断", "en": "Field and Engineering Assessment"})}</h2>'
        '<div class="engineeringScope"><b data-en="Assessment boundary">判断边界</b>'
        + bilingual_leaf({
            "zh": "本模块不另设总分，也不改变现有参数、配置和工况评分。已有基础、具体差距与弥补动作逐项对应；动作只有在样机、试验或市场复核完成后才能关闭。",
            "en": "This module adds no total score and does not change the existing specification, equipment or application scores. Each foundation, gap and closing action is paired; an action closes only after prototype, test or market validation.",
        })
        + "</div>"
        f'<div class="engineeringPriorityGrid">{"".join(priorities)}</div>'
        '<div class="engineeringTableWrap"><table class="engineeringTable"><caption class="srOnly" data-en="Field and engineering assessment details">实机与工程判断明细</caption>'
        '<thead><tr><th scope="col" data-en="Dimension">维度</th><th scope="col" data-en="Existing foundation">已有基础</th><th scope="col" data-en="Specific gap">具体差距</th><th scope="col" data-en="Closing action">弥补动作</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
        + render_ppt_table_group(
            business_tables,
            {"product_comparison"},
            "完整参数、配置与实机评价表",
            "Complete specification, equipment and field-evaluation tables",
            "原有参数、标选配、可靠性、操控性、舒适性、维修性和经济性表格全部保留；历史判断不自动视为当前量产状态。",
            "All specification, equipment, reliability, controllability, comfort, serviceability and economy tables are retained. Historical findings are not automatically treated as current production status.",
        )
        + render_ppt_table_group(
            business_tables,
            {"positioning"},
            "产品定位与历史目标表",
            "Product-positioning and historical-target tables",
            "定位、价格带、销量目标和时间节点按原年份保留，当前状态仍以最新业务复核为准。",
            "Positioning, price band, volume target and timing remain tied to the original year and require current business confirmation.",
        )
        + "</section>"
    )


SOURCE_SECTION_META = {
    "market": {
        "id": "market-insight",
        "zh": "市场销量与产品结构",
        "en": "Market Volume and Product Structure",
    },
    "applications": {
        "id": "job-applications",
        "zh": "客户工况与运输适应性",
        "en": "Customer Applications and Transport Fit",
    },
    "comparison": {
        "id": "engineering-insight",
        "zh": "参数、配置与实机对比",
        "en": "Specification, Equipment and Field Comparison",
    },
    "positioning": {
        "id": "product-positioning",
        "zh": "产品定位与市场目标",
        "en": "Product Positioning and Market Target",
    },
    "analysis": {
        "id": "source-analysis",
        "zh": "产品分析",
        "en": "Product Analysis",
    },
}


def render_source_table(record):
    matrix = record.get("matrix_zh") or []
    if not matrix:
        return ""
    caption = (record.get("title") or f'源表 {record.get("id", "")}').strip()
    width = max((len(row) for row in matrix), default=1)
    rows = [list(row) + [""] * max(0, width - len(row)) for row in matrix]
    populated_columns = [
        index
        for index in range(width)
        if any(str(row[index] or "").strip() for row in rows)
    ]
    rows = [[row[index] for index in populated_columns] for row in rows]
    width = len(populated_columns)
    fit_table = width <= 10
    headers = [str(cell or "").strip() for cell in rows[0]]

    column_weights = []
    for header_text in headers:
        if "吨级" in header_text or header_text in {"序号", "类型"}:
            weight = 8
        elif "场景及" in header_text or "工况描述" in header_text:
            weight = 30
        elif "施工场景" in header_text or "应用场景" in header_text:
            weight = 14
        elif "客户类型" in header_text:
            weight = 13
        elif "需求" in header_text:
            weight = 18
        elif any(token in header_text for token in ("满足性", "分析", "结论", "结果")):
            weight = 17
        else:
            weight = max(10, min(22, len(header_text) * 2 or 12))
        column_weights.append(weight)
    weight_total = sum(column_weights) or 1
    colgroup = ""
    if fit_table:
        colgroup = "<colgroup>" + "".join(
            f'<col style="width:{weight / weight_total * 100:.3f}%">'
            for weight in column_weights
        ) + "</colgroup>"

    header = "".join(
        f'<th scope="col">{esc(cell) if cell else "&nbsp;"}</th>'
        for cell in rows[0]
    )
    body = []
    for row in rows[1:]:
        cells = []
        for index, cell in enumerate(row):
            tag = "th" if index == 0 else "td"
            scope = ' scope="row"' if index == 0 else ""
            label = headers[index] if index < len(headers) else ""
            cells.append(
                f'<{tag}{scope} data-label="{esc(label)}">'
                f'{esc(cell) if cell else "&nbsp;"}</{tag}>'
            )
        body.append(f'<tr>{"".join(cells)}</tr>')
    wrapper_class = "sourceTableScroll sourceTableScrollFit" if fit_table else "sourceTableScroll"
    table_class = "sourceTableFit" if fit_table else "sourceTableWide"
    return (
        '<div class="sourceTableBlock">'
        f'<div class="{wrapper_class}">'
        f'<table class="{table_class}" lang="zh-CN">'
        f'<caption class="sourceTableCaption">{esc(caption)}</caption>'
        f"{colgroup}"
        f'<thead><tr>{header}</tr></thead>'
        f'<tbody>{"".join(body)}</tbody>'
        '</table></div></div>'
    )


def render_source_visuals(record):
    visuals = record.get("visuals") or []
    if not visuals:
        return ""
    figures = []
    title = record.get("title", {}).get("zh", "产品分析")
    for index, visual in enumerate(visuals, start=1):
        kind = visual.get("kind", "picture")
        if kind == "chart":
            fallback_title = title if len(visuals) == 1 else f"{title} · {index}"
            native_chart = render_chart_figure(visual, fallback_title)
            if native_chart:
                figures.append(native_chart)
                continue
        alt = f"{title} - {'图表' if kind == 'chart' else '实景图'} {index}"
        figures.append(
            f'<figure class="sourceVisual sourceVisual-{esc(kind)}">'
            f'<img src="{esc(visual.get("file"))}" alt="{esc(alt)}" loading="lazy">'
            "</figure>"
        )
    count_class = f" sourceVisualGrid-{min(len(figures), 4)}"
    return f'<div class="sourceVisualGrid{count_class}">{"".join(figures)}</div>'


def render_source_slide(record, table_records):
    body = "".join(
        bilingual_leaf(item, "p", "sourceParagraph")
        for item in record.get("body", [])
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
        f'<article class="sourceSlide" data-source-slide="{record.get("slide")}">'
        '<header class="sourceSlideHeader">'
        f'{bilingual_leaf(record.get("title"), "h3")}'
        "</header>"
        f'<div class="sourceNarrative">{body}</div>'
        + render_source_visuals(record)
        + tables
        + (f'<div class="sourceNotes">{notes}</div>' if notes else "")
        + "</article>"
    )


def render_source_section(section, records, table_records):
    meta = SOURCE_SECTION_META[section]
    slides = "".join(render_source_slide(record, table_records) for record in records)
    return (
        f'<section id="{meta["id"]}" class="insightSection sourceContentSection">'
        f'<h2 data-en="{esc(meta["en"])}">{esc(meta["zh"])}</h2>'
        f'<div class="sourceSlideStack">{slides}</div>'
        "</section>"
    )


def render_tonnage_insights(model):
    slug = model["meta"].get("slug")
    source_payload = load_ppt_source_content()
    slide_ids = source_payload["by_slug"].get(slug, [])
    records = [
        source_payload["slides"][slide_id]
        for slide_id in slide_ids
        if slide_id in source_payload["slides"]
    ]
    if not records:
        return ""
    table_payload = load_ppt_business_tables()
    sections = []
    for section in ("market", "applications", "comparison", "positioning", "analysis"):
        selected = [record for record in records if record.get("section") == section]
        if selected:
            sections.append(
                render_source_section(
                    section,
                    selected,
                    table_payload["records"],
                )
            )
    return "".join(sections)


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
    tonnage_insights_html = render_tonnage_insights(model)
    primary_analysis_target = "#market-insight" if tonnage_insights_html else "#overall"
    primary_analysis_zh = "市场与产品分析" if tonnage_insights_html else "查看总体评分"
    primary_analysis_en = "Market and product analysis" if tonnage_insights_html else "View overall score"
    source_nav_html = (
        """
      <details class="navGroup" open>
        <summary data-en="Product and market insight">产品与市场洞察</summary>
        <div class="navSubmenu">
          <a href="#market-insight" data-en="Market volume and product structure">市场销量与产品结构</a>
          <a href="#job-applications" data-en="Customers, applications and transport">客户工况与运输适应性</a>
          <a href="#engineering-insight" data-en="Specifications, equipment and field comparison">参数、配置与实机对比</a>
          <a href="#product-positioning" data-en="Product positioning and market target">产品定位与市场目标</a>
        </div>
      </details>
        """
        if tonnage_insights_html
        else ""
    )
    condition_visual_nav = render_condition_visual_nav(model)
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
    .layout{{display:grid;grid-template-columns:260px minmax(0,1fr);min-height:100vh}}aside.nav{{position:sticky;top:0;height:100vh;overflow:auto;background:linear-gradient(180deg,var(--blue-dark),#001e3d);color:white;border-right:5px solid var(--yellow);padding:18px 14px;z-index:20}}.navBrand{{display:inline-block;width:max-content}}.navBrand:focus-visible{{outline:3px solid var(--yellow);outline-offset:3px}}.navTitle{{font-size:18px;margin:10px 0 6px;color:#fff;font-weight:900}}.nav img{{width:118px;background:#fff;padding:6px;border-radius:2px}}.nav small{{display:block;color:#bcd3e8;font-weight:800;letter-spacing:.08em;text-transform:uppercase}}.navMenu a{{display:block;padding:8px 10px;border-left:3px solid transparent;border-radius:3px;margin:2px 0;color:#eef7ff;font-size:13px;font-weight:700}}.navMenu a:hover{{background:rgba(255,255,255,.10);border-left-color:var(--yellow)}}.navMenu .home{{background:var(--yellow);color:#08213d;font-weight:900;margin:12px 0}}.languageToggle{{display:inline-flex;align-items:center;justify-content:center;min-width:52px;min-height:34px;margin:10px 0;border:1px solid rgba(255,255,255,.4);border-radius:4px;background:transparent;color:#fff;padding:0 9px;font-weight:900;cursor:pointer}}.languageToggle:hover,.languageToggle:focus-visible{{border-color:var(--yellow);color:var(--yellow);outline:none}}.navToggle,.mobileTop{{display:none}}
    main{{padding:22px;min-width:0}}.hero{{background:#fff;border:1px solid var(--line);box-shadow:var(--shadow);display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:18px;align-items:center;border-left:6px solid var(--blue);margin-bottom:16px}}.heroText{{padding:28px 28px 24px}}.eyebrow{{color:var(--blue);font-size:12px;font-weight:900;letter-spacing:.14em;text-transform:uppercase}}h1{{font-size:38px;line-height:1.1;color:#082b4d;margin:8px 0 12px}}h2{{font-size:22px;color:#082b4d;margin:0 0 14px}}h2:after{{content:"";display:block;width:46px;height:3px;background:var(--yellow);margin-top:8px}}h3{{color:#0b3155;margin:0 0 8px;font-size:16px}}.hero p{{max-width:980px}}.heroMedia{{height:260px;position:relative;background:#f7fafc;border-left:1px solid var(--line);padding:18px;overflow:hidden}}.heroMedia img{{position:absolute;inset:18px;width:calc(100% - 36px);height:calc(100% - 36px);object-fit:contain}}.actions{{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}}.btn{{display:inline-flex;align-items:center;justify-content:center;border:1px solid #b9cadb;border-radius:4px;padding:9px 13px;font-weight:900;font-size:13px;background:#f7fbff}}.btn.blue{{background:var(--blue);color:#fff;border-color:var(--blue)}}.btn.yellow{{background:var(--yellow);border-color:var(--yellow);color:#08213d}}
    section{{background:#fff;border:1px solid var(--line);box-shadow:var(--shadow);border-radius:5px;padding:18px;margin:14px 0}}.kpis{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}}.kpi{{border:1px solid #c9d8e7;border-left:5px solid var(--blue);padding:12px;background:#fbfdff}}.kpi:nth-child(2){{border-left-color:var(--yellow)}}.kpi b{{display:block;font-size:30px;color:var(--blue)}}.kpi span{{font-size:12px;color:var(--muted)}}.split{{display:grid;grid-template-columns:minmax(0,1fr) minmax(420px,.9fr);gap:14px}}.panel{{border:1px solid #c8d7e6;border-radius:5px;background:#fff;padding:14px;min-width:0}}.summaryGrid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}.summaryCard{{border:1px solid #c8d7e6;border-top:4px solid var(--blue);padding:12px;background:#fbfdff}}.summaryCard p{{margin:7px 0;font-size:13px}}.conditionTitle{{display:flex;align-items:flex-start;justify-content:space-between;border-bottom:1px solid #e2ebf3;padding-bottom:12px;margin-bottom:12px}}.conditionTitle span{{display:block;color:var(--blue);font-size:12px;font-weight:900;letter-spacing:.14em}}.conditionTitle em{{font-style:normal;font-weight:900;color:#4f6172}}.conditionIntro{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px}}.conditionIntro p{{margin:0;background:#f7fafc;border-left:4px solid var(--yellow);padding:10px 12px}}.conditionTop{{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(390px,.8fr);gap:12px;margin-bottom:12px}}.conditionTop>.mobileDisclosure{{min-width:0}}.conditionTop>.mobileDisclosure>.panel{{height:100%}}
    .bars{{display:grid;gap:7px}}.bar{{display:grid;grid-template-columns:28px minmax(100px,145px) minmax(90px,1fr) 48px 64px;gap:8px;align-items:center;min-width:0}}.bar span{{background:#e6f0fa;color:var(--blue);font-weight:900;text-align:center;border-radius:3px;padding:3px 0}}.bar b{{font-size:13px;min-width:0;overflow-wrap:anywhere}}.bar i{{height:17px;background:#e3ecf5;border-radius:3px;overflow:hidden}}.bar i em{{display:block;height:100%;background:linear-gradient(90deg,var(--blue),#2878bd)}}.bar strong{{color:#08335d}}.barCoverage{{font-size:11px;color:#65798c;white-space:nowrap}}.bar.xcmg span{{background:var(--yellow);color:#08213d}}.bar.xcmg i em{{background:linear-gradient(90deg,var(--yellow),#ffd86d)}}.bar.xcmg b,.bar.xcmg strong{{color:var(--blue);font-weight:900}}
    .radarBox{{min-width:0}}.radarHead{{display:flex;justify-content:space-between;gap:10px;align-items:center;padding-right:6px}}.radarCurrent{{font-size:12px;color:var(--blue);font-weight:900;white-space:nowrap}}.radarSvg{{display:block;margin:6px auto;max-width:100%;height:360px}}.radarSvg.small{{height:300px}}.radar-grid{{fill:none;stroke:#d9e6f2;stroke-width:1}}.radar-axis{{stroke:#d9e6f2;stroke-width:1}}.radar-label{{font-size:12px;font-weight:800;fill:#0b3155;text-anchor:middle;dominant-baseline:middle}}.radar-series{{fill:var(--series-color);fill-opacity:.08;stroke:var(--series-color);stroke-width:2.3;transition:.18s;cursor:pointer}}.radarBox.compare .radar-series,.factorRadar.compare .radar-series{{opacity:.08;fill-opacity:.03}}.radarBox.compare .radar-series.selected,.factorRadar.compare .radar-series.selected{{opacity:1;fill-opacity:.18;stroke-width:3.6}}.radarLegend{{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}}.radarLegend button{{border:1px solid #bfd0e0;background:#fff;border-radius:4px;padding:5px 7px;font-size:12px;cursor:pointer;font-weight:700}}.radarLegend i{{display:inline-block;width:10px;height:10px;margin-right:5px;border-radius:2px}}.radarLegend button:hover,.radarLegend button.selected{{border-color:var(--yellow);box-shadow:0 0 0 2px rgba(245,180,0,.18)}}.radarLegend button.selected{{background:#fff7d6;color:#08213d}}.radarLegend.compact button{{font-size:11px;padding:4px 6px}}.mobileDisclosure,.radarPicker{{border:0;padding:0;margin:0;min-width:0}}.mobileDisclosure>summary,.radarPicker>summary{{display:none}}
    .factorRadar{{min-width:0}}.factorRadarHead{{margin-bottom:4px}}.factorRadarGrid{{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:12px;align-items:center}}.keyTable{{width:100%;border-collapse:collapse;font-size:12px}}.keyTable th{{background:var(--blue);color:#fff}}.keyTable th,.keyTable td{{border-bottom:1px solid #e3edf5;padding:8px;text-align:left}}.tableScroll{{overflow:auto;border:1px solid var(--line);border-radius:4px;max-height:520px;background:white}}.tableScroll.compact{{max-height:360px}}table{{border-collapse:collapse;width:100%;font-size:12px}}th,td{{border-bottom:1px solid #e3edf5;padding:8px;text-align:left;vertical-align:top;white-space:nowrap}}th{{position:sticky;top:0;background:var(--blue);color:#fff;z-index:2}}td:first-child,th:first-child{{position:sticky;left:0;z-index:3}}td:first-child,tbody th:first-child{{background:#fff;font-weight:800;color:#0b3155;box-shadow:2px 0 0 rgba(0,76,151,.08)}}tr:nth-child(even) td,tr:nth-child(even) th:first-child{{background:#f8fbfe}}tr.xcmg-row td{{box-shadow:inset 3px 0 0 var(--yellow)}}.scoreCell{{min-width:124px;white-space:normal}}.scoreCell b{{display:block}}.scoreCell span{{display:block;font-weight:900}}.scoreCell small{{display:block;color:#51677a}}.good{{background:#e6f4ea!important;color:#0c6a36!important;font-weight:800}}.mid{{background:#fff4cc!important;color:#785700!important;font-weight:800}}.bad{{background:#fde9e9!important;color:#ad1d1d!important;font-weight:800}}.missing{{background:#eef2f6!important;color:#607080!important}}.srOnly{{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important}}
    .gapPanel{{border:1px solid #dfb650;background:#fffdf4;border-radius:5px;padding:14px;margin:12px 0}}.gapGrid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}}.gapGrid article{{background:#fff;border:1px solid #ecd991;padding:12px}}.gapGrid b{{display:block;color:#08335d}}.gapGrid p{{margin:5px 0 0;font-size:13px}}.overallNotes p{{margin:7px 0 4px}}.gapList{{margin:6px 0 0;padding-left:18px;font-size:13px;line-height:1.55}}.gapList li{{margin:4px 0}}.methodNote,.coverageNote,.sourceNote{{font-size:12px;color:#526a7f;background:#f6f9fc;border-left:4px solid var(--yellow);padding:9px 11px;margin:0 0 12px}}.coverageNote{{margin:10px 0 0}}.sourceNote{{display:flex;gap:10px;align-items:flex-start}}.sourceNote b{{color:#08335d;white-space:nowrap}}
    .productGapSpotlight{{display:grid;grid-template-columns:310px minmax(0,1fr);min-height:285px;margin:14px 0 18px;border:1px solid var(--line);border-top:4px solid var(--blue);background:#fff;overflow:hidden}}.productGapMedia{{display:grid;grid-template-rows:auto 1fr auto;min-width:0;padding:16px;background:#f4f8fb;border-right:1px solid var(--line)}}.productGapMedia>span,.productGapContent>span{{color:var(--blue);font-size:10px;font-weight:900;letter-spacing:.11em;text-transform:uppercase}}.productGapMedia img{{display:block;width:100%;height:190px;object-fit:contain;padding:10px}}.productGapMedia>div{{display:flex;justify-content:space-between;gap:8px;align-items:end;border-top:1px solid #d7e3ed;padding-top:10px}}.productGapMedia b{{color:#08335d;font-size:16px}}.productGapMedia small{{color:#65798c;font-size:10px}}.productGapContent{{min-width:0;padding:18px}}.productGapContent h3{{margin:5px 0 6px;color:#08335d;font-size:19px}}.productGapContent>p{{margin:0;color:#536b80;font-size:12px;line-height:1.6}}.productGapContent ol{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:14px 0 0;padding:0;list-style:none}}.productGapContent li{{display:grid;grid-template-columns:32px minmax(0,1fr);gap:9px;padding:10px;border:1px solid #d9e5ef;background:#f8fbfd}}.productGapContent li>span{{display:flex;align-items:center;justify-content:center;width:28px;height:28px;background:var(--blue);color:#fff;font-size:11px;font-weight:900}}.productGapContent li small,.productGapContent li b,.productGapContent li p{{display:block}}.productGapContent li small{{color:#6b7e8f;font-size:9px;font-weight:900}}.productGapContent li b{{margin-top:2px;color:#0b3155;font-size:13px}}.productGapContent li p{{margin:4px 0 0;color:#526a7f;font-size:11px;line-height:1.45;white-space:normal}}
    .conditionVisualNav{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:12px 0}}.conditionVisualCard{{position:relative;min-height:172px;overflow:hidden;border:1px solid var(--line);background:#092d50;color:#fff}}.conditionVisualCard:after{{content:"";position:absolute;inset:0;background:rgba(2,24,45,.36);transition:background .18s}}.conditionVisualCard:hover:after,.conditionVisualCard:focus-visible:after{{background:rgba(2,24,45,.20)}}.conditionVisualCard:focus-visible{{outline:3px solid rgba(245,180,0,.50);outline-offset:2px}}.conditionVisualCard img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .2s}}.conditionVisualCard:hover img{{transform:scale(1.025)}}.conditionVisualCard>div{{position:absolute;z-index:1;inset:auto 0 0;padding:13px;background:rgba(2,28,52,.82);border-top:2px solid var(--yellow)}}.conditionVisualCard span,.conditionVisualCard strong,.conditionVisualCard small{{display:block}}.conditionVisualCard span{{color:var(--yellow);font-size:9px;font-weight:900;letter-spacing:.10em}}.conditionVisualCard strong{{margin-top:3px;color:#fff;font-size:14px}}.conditionVisualCard small{{margin-top:4px;color:#d4e2ee;font-size:10px;line-height:1.4}}.conditionVisualSource{{margin:0 0 14px;color:#64798c;font-size:10px;line-height:1.5}}
    .navGroup{{margin:3px 0;border-left:3px solid rgba(255,255,255,.18)}}.navGroup>summary{{display:flex;align-items:center;justify-content:space-between;min-height:36px;padding:7px 10px;color:#fff;font-size:13px;font-weight:900;cursor:pointer;list-style:none}}.navGroup>summary::-webkit-details-marker{{display:none}}.navGroup>summary:after{{content:"+";color:var(--yellow);font-size:16px}}.navGroup[open]>summary:after{{content:"−"}}.navSubmenu{{padding:0 0 4px 7px}}.navSubmenu a{{font-size:12px!important;color:#d9e8f4!important}}.navMenu a.active{{background:rgba(255,255,255,.14);border-left-color:var(--yellow);color:#fff}}.navSubmenu a.active{{color:#fff!important}}
    .insightSection{{border-top:4px solid var(--blue)}}.insightLead{{margin:-4px 0 14px;max-width:1050px;color:#536b80;font-size:13px}}.marketKpis{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:14px}}.marketKpis>div{{min-width:0;border:1px solid #c9d8e7;border-left:4px solid var(--yellow);background:#f8fbfd;padding:11px 12px}}.marketKpis span,.marketKpis b,.marketKpis small{{display:block}}.marketKpis>div>span{{color:#557087;font-size:11px;font-weight:800}}.marketKpis b{{margin-top:4px;color:#073c70;font-size:18px;line-height:1.35;overflow-wrap:anywhere}}.marketKpis small{{color:#657a8e;font-size:10px}}.marketInsightGrid{{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(340px,.85fr);gap:14px;align-items:stretch}}.marketTrendPanel,.marketReading{{min-width:0;border:1px solid #c8d7e6;background:#fff;padding:14px}}.insightPanelTitle{{display:flex;align-items:center;min-height:30px;margin-bottom:10px;border-bottom:1px solid #dce6ef;color:#083a68;font-size:14px;font-weight:900}}.marketColumns{{display:grid;grid-template-columns:repeat(4,minmax(58px,1fr));gap:12px;height:230px;align-items:end;padding:8px 6px 0;border-bottom:1px solid #aac0d4;background:repeating-linear-gradient(to top,#fff 0,#fff 56px,#edf3f8 57px)}}.marketColumn{{display:grid;grid-template-rows:160px auto auto auto;gap:2px;align-items:end;text-align:center;min-width:0}}.marketBarShell{{height:160px;display:flex;align-items:flex-end;justify-content:center}}.marketBar{{display:flex;flex-direction:column-reverse;width:min(52px,72%);min-height:3px;border-top:1px solid rgba(0,45,85,.18);overflow:hidden}}.marketBar span{{display:block;min-height:2px}}.marketColumn>b{{color:#0a3155;font-size:12px}}.marketColumn>strong{{color:#082b4d;font-size:12px;white-space:nowrap}}.marketColumn>strong span{{display:inline}}.marketColumn>small{{min-height:16px;color:#61778b;font-size:9px;line-height:1.2}}.marketLegend{{display:flex;flex-wrap:wrap;gap:7px 13px;margin-top:10px;color:#425b70;font-size:10px}}.marketLegend span{{display:inline-flex;align-items:center;gap:5px}}.marketLegend i{{width:11px;height:11px}}.marketTimeBasis{{margin:10px 0 0;padding-top:9px;border-top:1px solid #e0e9f1;color:#5b7084;font-size:11px;line-height:1.55}}.marketSeriesEmpty{{display:flex;align-items:center;min-height:230px;padding:24px;border:1px dashed #9eb5c9;background:#f7fafc}}.marketSeriesEmpty p{{margin:0;color:#496277;line-height:1.75}}.marketRole{{margin:0 0 11px;padding:11px;border-left:4px solid var(--yellow);background:#f7fafc;color:#183d5e;line-height:1.7}}.marketDecisionList{{margin:0}}.marketDecisionList>div{{display:grid;grid-template-columns:92px minmax(0,1fr);gap:10px;padding:9px 0;border-top:1px solid #e1e9f1}}.marketDecisionList dt{{color:#0a4f8c;font-size:11px;font-weight:900}}.marketDecisionList dd{{margin:0;color:#334f67;font-size:12px;line-height:1.6}}.transportDecision{{margin-top:4px;padding:10px!important;border-left:4px solid var(--blue);background:#f5f9fc}}
    .marketEvidenceGrid{{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(300px,.65fr);gap:14px;margin-top:14px}}.marketDataPanel,.marketFactPanel{{min-width:0;border:1px solid #c8d7e6;background:#fff;padding:14px}}.marketDataTableWrap{{max-width:100%;overflow-x:auto}}.marketDataTable{{min-width:610px;table-layout:fixed;font-size:11px}}.marketDataTable th,.marketDataTable td{{position:static!important;padding:8px 9px;text-align:right;white-space:normal;box-shadow:none!important}}.marketDataTable thead th{{background:#075da8;color:#fff;text-align:center}}.marketDataTable thead th:first-child,.marketDataTable tbody th{{text-align:left}}.marketDataTable thead small{{display:block;margin-top:2px;color:#dbeaf7;font-size:8px;font-weight:600}}.marketDataTable tbody th{{width:19%;background:#f4f8fb;color:#0b3e6b}}.marketDataTable .xcmgMarketRow th,.marketDataTable .xcmgMarketRow td{{background:#fff5cf;font-weight:900}}.marketDataTable .marketTotalRow th,.marketDataTable .marketTotalRow td{{border-top:2px solid var(--blue);background:#eef5fb;font-weight:900}}.marketFactList{{display:grid;gap:9px}}.marketFactList article{{padding:10px 11px;border-left:4px solid var(--blue);background:#f5f9fc}}.marketFactList article:nth-child(2){{border-left-color:var(--green)}}.marketFactList article:nth-child(3){{border-left-color:var(--yellow)}}.marketFactList b{{display:block;color:#0a4b84;font-size:11px}}.marketFactList p{{margin:4px 0 0;color:#334f67;font-size:12px;line-height:1.65}}.marketEvidenceBoundary{{margin-top:14px;padding:14px;border:1px solid #c8d7e6;border-left:4px solid var(--yellow);background:#f7fafc}}.marketEvidenceBoundary p{{margin:0;color:#3f5a70;line-height:1.7}}
    .applicationGrid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}}.applicationCard{{display:grid;grid-template-rows:auto 1fr auto;min-width:0;border:1px solid #c8d7e6;background:#fff}}.applicationCard figure{{margin:0;border-bottom:1px solid #c8d7e6;background:#edf3f7}}.applicationCard img{{display:block;width:100%;aspect-ratio:16/10;object-fit:contain;background:#eaf0f5}}.applicationCard figcaption{{padding:9px 11px;border-top:3px solid var(--yellow);background:#f8fbfd;color:#093960}}.applicationCard>p{{margin:0;padding:11px;color:#3f5b71;font-size:12px;line-height:1.68}}.applicationRequirement{{margin:0 11px 11px;padding:9px 10px;border-left:3px solid var(--blue);background:#f4f8fb}}.applicationRequirement span,.applicationRequirement b{{display:block}}.applicationRequirement span{{color:#527087;font-size:10px;font-weight:900}}.applicationRequirement b{{margin-top:3px;color:#0a3f70;font-size:11px;line-height:1.55}}.applicationMatrixWrap{{margin-top:14px;padding:14px;border:1px solid #c8d7e6;background:#fff}}.applicationMatrix{{table-layout:fixed;font-size:12px}}.applicationMatrix th,.applicationMatrix td{{position:static!important;padding:10px 11px;white-space:normal;overflow-wrap:anywhere;line-height:1.6;box-shadow:none!important}}.applicationMatrix thead th{{background:#075da8;color:#fff}}.applicationMatrix thead th:nth-child(1){{width:20%}}.applicationMatrix thead th:nth-child(2){{width:45%}}.applicationMatrix thead th:nth-child(3){{width:35%}}.applicationMatrix tbody th{{background:#f4f8fb;color:#083b69;text-align:left}}.applicationCapabilityCell{{border-left:3px solid var(--yellow);background:#fffdf4;color:#163f63;font-weight:800}}
    .engineeringScope{{display:grid;grid-template-columns:150px minmax(0,1fr);border:1px solid #c8d7e6;background:#f5f9fc;margin-bottom:12px}}.engineeringScope>b{{display:flex;align-items:center;padding:10px 12px;border-right:1px solid #c8d7e6;color:#0a4b84}}.engineeringScope>span{{padding:10px 12px;color:#3f5a70;font-size:12px;line-height:1.6}}.engineeringPriorityGrid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px;margin-bottom:12px}}.engineeringPriorityGrid article{{min-width:0;padding:10px 11px;border:1px solid #c8d7e6;border-top:3px solid #c93434;background:#fff}}.engineeringPriorityGrid b{{display:block;color:#0a4b84;font-size:11px}}.engineeringPriorityGrid p{{margin:4px 0 0;color:#3f566b;font-size:11px;line-height:1.55}}.engineeringTableWrap{{border:1px solid #afc5d9;overflow:hidden}}.engineeringTable{{table-layout:fixed;font-size:12px}}.engineeringTable th,.engineeringTable td{{position:static!important;white-space:normal;overflow-wrap:anywhere;padding:10px 11px;line-height:1.55;box-shadow:none!important}}.engineeringTable thead th{{background:#075da8;color:#fff}}.engineeringTable thead th:nth-child(1){{width:16%}}.engineeringTable thead th:nth-child(2){{width:28%}}.engineeringTable thead th:nth-child(3){{width:30%}}.engineeringTable thead th:nth-child(4){{width:26%}}.engineeringTable tbody th{{background:#f4f8fb!important;color:#083b69;border-left:4px solid var(--green)}}.engineeringTable .gapColumn{{border-left:3px solid #c93434;background:#fffafa}}.engineeringTable .actionColumn{{border-left:3px solid var(--yellow);background:#fffdf6}}.cellLabel{{display:none}}
    .pptBusinessGroup{{margin-top:16px;padding-top:12px;border-top:3px solid var(--blue)}}.pptBusinessGroupHead{{display:flex;align-items:end;justify-content:space-between;gap:20px;margin-bottom:10px}}.pptBusinessGroupHead h3{{margin:0;color:#073c70;font-size:16px}}.pptBusinessGroupHead p{{max-width:760px;margin:0;color:#526c82;font-size:11px;line-height:1.55;text-align:right}}.pptBusinessTableStack{{display:grid;gap:12px}}.pptBusinessTable{{min-width:0;border:1px solid #b8ccdd;background:#fff}}.pptBusinessTable>summary{{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:44px;padding:9px 11px;border-bottom:1px solid #c8d7e6;background:#f3f8fb;cursor:pointer;list-style:none}}.pptBusinessTable>summary::-webkit-details-marker{{display:none}}.pptBusinessTable>summary h3{{margin:0;color:#073c70;font-size:13px;line-height:1.45}}.pptBusinessTable>summary span{{flex:0 0 auto;color:#61788c;font-size:10px;font-weight:800}}.pptBusinessTable:not([open])>summary{{border-bottom:0}}.pptBusinessTableScroll{{max-width:100%;overflow-x:auto;overscroll-behavior-inline:contain;scrollbar-color:#8299ad #edf2f6}}.pptBusinessTableScroll table{{width:max-content;min-width:100%;border-collapse:separate;border-spacing:0;table-layout:auto;font-size:11px}}.pptBusinessTableScroll th,.pptBusinessTableScroll td{{position:static;min-width:116px;max-width:420px;padding:8px 9px;border-right:1px solid #d7e2ec;border-bottom:1px solid #d7e2ec;background:#fff;box-shadow:none;line-height:1.55;text-align:left;vertical-align:top;white-space:pre-line;overflow-wrap:anywhere}}.pptBusinessTableScroll thead th{{position:sticky;top:0;z-index:3;min-width:132px;background:#075da8;color:#fff;font-weight:900}}.pptBusinessTableScroll tbody th{{position:sticky;left:0;z-index:2;min-width:145px;background:#eef5fa!important;color:#073c70;font-weight:900}}.pptBusinessTableScroll tbody tr:nth-child(even) td{{background:#f8fbfd}}.pptBusinessTableScroll tr>*:last-child{{border-right:0}}.pptBusinessTableScroll tbody tr:last-child>*{{border-bottom:0}}
    .sourceContentSection{{padding:0;border-top:4px solid var(--blue);overflow:hidden}}.sourceContentSection>h2{{padding:18px 20px 0;margin-bottom:6px}}.sourceSlideStack{{display:block}}.sourceSlide{{padding:20px;border-top:1px solid #c8d7e6;background:#fff}}.sourceSlide:first-child{{border-top:0}}.sourceSlideHeader{{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:10px}}.sourceSlideHeader h3{{margin:0;color:#073c70;font-size:18px;line-height:1.45}}.sourceNarrative{{max-width:1180px}}.sourceParagraph{{margin:0 0 10px;color:#203f5b;font-size:14px;line-height:1.82;white-space:pre-line;overflow-wrap:anywhere}}.sourceParagraph:last-child{{margin-bottom:0}}.sourceMacroGrid{{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(340px,.65fr);gap:16px;align-items:start}}.sourceMacroColumn{{min-width:0;padding:14px 16px;border-left:4px solid var(--blue);background:#f6f9fc}}.sourceMacroColumn:last-child{{border-left-color:var(--yellow)}}.sourceMacroColumn .sourceParagraph:first-child{{color:#075da8;font-weight:900}}.sourceVisualGrid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:16px 0 2px;align-items:start}}.sourceVisualGrid-1{{grid-template-columns:minmax(0,980px);justify-content:center}}.sourceVisualGrid-3{{grid-template-columns:repeat(3,minmax(0,1fr))}}.sourceVisualGrid-4{{grid-template-columns:repeat(2,minmax(0,1fr))}}.sourceVisual{{display:flex;align-items:center;justify-content:center;min-width:0;margin:0;border:1px solid #c8d7e6;background:#f7fafc;overflow:hidden}}.sourceVisual img{{display:block;width:100%;height:auto;max-height:560px;object-fit:contain;background:#fff}}.sourceVisual-picture img{{max-height:480px}}.sourceTableBlock{{margin-top:16px;border-top:3px solid var(--blue)}}.sourceTableScroll{{max-width:100%;overflow-x:auto;overscroll-behavior-inline:contain;border:1px solid #b8ccdd;border-top:0;background:#fff}}.sourceTableScroll table{{width:max-content;min-width:100%;border-collapse:separate;border-spacing:0;table-layout:auto;font-size:12px}}.sourceTableCaption{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}}.sourceTableScroll th,.sourceTableScroll td{{position:static;min-width:118px;max-width:460px;padding:9px 10px;border-right:1px solid #d7e2ec;border-bottom:1px solid #d7e2ec;background:#fff;box-shadow:none;line-height:1.65;text-align:left;vertical-align:top;white-space:pre-line;overflow-wrap:anywhere}}.sourceTableScroll thead th{{position:sticky;top:0;z-index:3;background:#075da8;color:#fff;font-weight:900}}.sourceTableScroll tbody th{{position:sticky;left:0;z-index:2;min-width:150px;background:#eef5fa!important;color:#073c70;font-weight:900}}.sourceTableScroll tbody tr:nth-child(even) td{{background:#f8fbfd}}.sourceTableScroll tr>*:last-child{{border-right:0}}.sourceTableScroll tbody tr:last-child>*{{border-bottom:0}}.sourceNotes{{margin-top:12px;padding:9px 11px;border-left:4px solid var(--blue);background:#f3f7fa}}.sourceDataNote{{margin:0;color:#526a7f;font-size:11px;line-height:1.6;white-space:pre-line}}
    .simulator{{border:1px solid #c8d7e6;border-radius:5px;overflow:hidden;margin-top:12px}}.simHead{{display:flex;justify-content:space-between;padding:12px;background:#f7fafc;border-bottom:1px solid #e3edf5}}.simDisclaimer{{margin:0;padding:9px 12px;background:#fffdf4;border-bottom:1px solid #ecd991;color:#526a7f;font-size:12px}}.resetSim{{border:1px solid #b9cadb;border-radius:4px;background:#fff;padding:6px 10px;font-weight:900;cursor:pointer}}.simGrid{{display:grid;grid-template-columns:minmax(0,1fr) 230px;gap:12px;padding:12px}}.simOptions{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}}.simOptions label{{border:1px solid #d6e2ee;background:#fbfdff;padding:9px;display:grid;grid-template-columns:18px 1fr;gap:8px}}.simOptions b,.simOptions em,.simOptions small{{display:block}}.simOptions em{{color:var(--blue);font-style:normal;font-weight:900;font-size:12px}}.simOptions small{{color:#5d7083;font-size:11px}}.simResult{{border-left:5px solid var(--yellow);background:#f7fafc;padding:18px}}.simResult strong{{display:block;font-size:34px;color:var(--blue)}}.simResult b,.simResult span,.simResult small{{display:block}}.rankPanel{{display:none;padding:0 12px 12px}}.rankPanel.show{{display:block}}.muted{{color:var(--muted)}}.rawTabs{{display:flex;gap:8px;margin-bottom:10px}}.rawTabs button{{border:1px solid #bfd0e0;background:#fff;border-radius:4px;padding:7px 11px;font-weight:900;cursor:pointer}}.rawTabs button.active{{background:var(--yellow);border-color:var(--yellow)}}.rawTable[data-open="false"]{{display:none}}.backTop{{position:fixed;left:14px;bottom:14px;z-index:40;background:var(--yellow);border:1px solid #c89200;border-radius:18px;padding:8px 12px;font-weight:900;color:#08213d;box-shadow:0 8px 20px rgba(0,58,112,.18);opacity:0;pointer-events:none;transform:translateY(8px);transition:.18s}}.backTop.show{{opacity:1;pointer-events:auto;transform:none}}
    @media(max-width:900px){{html{{scroll-padding-top:72px}}.layout{{display:block}}aside.nav{{height:auto;position:sticky;top:0;overflow:visible;border-right:0;border-bottom:4px solid var(--yellow);padding:8px 12px;display:grid;grid-template-columns:auto minmax(0,1fr) auto auto auto;gap:10px;align-items:center}}.nav img{{width:82px}}.navTitle{{font-size:14px;margin:0}}.nav small{{font-size:10px}}.languageToggle{{margin:0}}.navToggle,.mobileTop{{display:inline-flex;align-items:center;justify-content:center;border:1px solid rgba(255,255,255,.35);background:transparent;color:#fff;border-radius:4px;padding:7px 10px;font-weight:900}}.mobileTop{{font-size:12px}}.navMenu{{display:none;grid-column:1/-1;grid-template-columns:repeat(2,minmax(0,1fr));gap:3px;max-height:calc(100vh - 76px);overflow:auto;padding-top:8px}}.navMenu.open{{display:grid}}.navMenu .home,.navGroup{{grid-column:1/-1}}.navMenu .home{{margin:0}}.navSubmenu{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:3px}}main{{padding:14px}}section,.hero{{scroll-margin-top:78px}}.hero,.split,.conditionTop{{grid-template-columns:1fr}}.factorRadarGrid{{grid-template-columns:1fr}}.kpis,.summaryGrid,.gapGrid{{grid-template-columns:1fr 1fr}}.conditionIntro,.simGrid,.simOptions{{grid-template-columns:1fr}}.heroMedia{{height:220px}}.productGapSpotlight{{grid-template-columns:260px minmax(0,1fr)}}.conditionVisualNav{{grid-template-columns:repeat(2,minmax(0,1fr))}}.backTop{{display:none}}.detailMatrix table{{min-width:1360px}}.rawTable table{{min-width:1100px}}}}
    @media(max-width:720px){{body{{font-size:14px}}main{{padding:8px}}section{{padding:12px;margin:8px 0;border-radius:4px;box-shadow:none}}section,.hero{{scroll-margin-top:66px}}aside.nav{{grid-template-columns:72px minmax(0,1fr) auto auto auto;padding:6px 8px;gap:7px}}.nav img{{width:72px;padding:4px}}.navTitle{{font-size:12px;line-height:1.25}}.nav small{{font-size:9px}}.languageToggle{{min-width:40px;min-height:32px;padding:0 6px;font-size:11px}}.navToggle,.mobileTop{{padding:6px 8px;font-size:11px}}.navMenu{{max-height:calc(100vh - 64px);grid-template-columns:1fr 1fr}}.navMenu a{{font-size:12px;padding:7px 8px}}.hero{{margin-bottom:8px}}.heroText{{padding:16px 14px 12px}}.heroDescription{{display:none}}.heroMedia{{height:142px;border-left:0;border-top:1px solid var(--line);padding:10px}}.heroMedia img{{inset:10px;width:calc(100% - 20px);height:calc(100% - 20px)}}h1{{font-size:26px;margin:6px 0 8px}}h2{{font-size:20px;margin-bottom:10px}}h2:after{{margin-top:6px}}h3{{font-size:15px}}.actions{{gap:6px;flex-wrap:nowrap;overflow-x:auto;margin-top:10px;padding-bottom:2px}}.actions .btn{{flex:0 0 auto;padding:7px 9px;font-size:12px}}.kpis{{grid-template-columns:1fr 1fr;gap:7px}}.kpi{{padding:9px;border-left-width:4px;min-height:92px}}.kpi b{{font-size:24px;line-height:1.15;margin:3px 0}}.kpi span{{font-size:11px;line-height:1.35;display:block}}.summaryGrid{{display:grid;grid-template-columns:none;grid-auto-flow:column;grid-auto-columns:minmax(82%,1fr);gap:8px;overflow-x:auto;scroll-snap-type:x mandatory;padding:1px 13% 6px 1px}}.summaryCard{{scroll-snap-align:start;padding:10px;min-height:150px}}.summaryCard p{{font-size:12px;margin:5px 0}}.conditionBlock{{padding:11px}}.conditionTitle{{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;padding-bottom:8px;margin-bottom:8px}}.conditionTitle h2{{font-size:18px;overflow-wrap:anywhere;margin-bottom:0}}.conditionTitle span{{font-size:10px}}.conditionIntro{{display:grid;grid-template-columns:none;grid-auto-flow:column;grid-auto-columns:88%;overflow-x:auto;gap:8px;scroll-snap-type:x mandatory;margin-bottom:8px;padding-right:10%}}.conditionIntro p{{scroll-snap-align:start;padding:9px 10px;font-size:12px}}.conditionTop{{gap:8px;margin-bottom:8px}}.panel{{padding:10px}}.conditionRanking .bars{{gap:5px}}.bar{{grid-template-columns:24px minmax(82px,105px) minmax(64px,1fr) 40px;gap:5px}}.bar span{{padding:2px 0}}.bar b,.bar strong{{font-size:12px}}.bar i{{height:14px}}.barCoverage{{display:none}}.coverageNote,.methodNote,.sourceNote{{font-size:11px;padding:8px 9px;margin-bottom:8px}}th,td{{padding:7px 6px}}.sourceNote{{display:block}}.factorRadarGrid>div{{min-width:0;width:100%}}.factorRadarGrid .keyTable{{width:100%;min-width:0;table-layout:fixed}}.factorRadarGrid .keyTable th,.factorRadarGrid .keyTable td{{white-space:normal;overflow-wrap:anywhere}}.radarSvg{{height:260px;margin:2px auto}}.radarSvg.small{{width:100%;height:auto;max-height:255px}}.radarLegend{{min-width:0;padding-top:6px}}.radarLegend button{{white-space:normal;overflow-wrap:anywhere;font-size:11px;padding:4px 5px}}.mobileDisclosure>summary,.radarPicker>summary{{display:flex;align-items:center;justify-content:space-between;gap:8px;min-height:42px;padding:9px 11px;border:1px solid #c8d7e6;border-left:4px solid var(--blue);border-radius:4px;background:#f7fafc;color:#0b3155;font-weight:900;cursor:pointer;list-style:none}}.mobileDisclosure>summary::-webkit-details-marker,.radarPicker>summary::-webkit-details-marker{{display:none}}.mobileDisclosure>summary:after,.radarPicker>summary:after{{content:"展开";font-size:11px;color:var(--blue);font-weight:800}}.mobileDisclosure[open]>summary:after,.radarPicker[open]>summary:after{{content:"收起"}}.mobileDisclosure[open]>summary,.radarPicker[open]>summary{{margin-bottom:8px;border-left-color:var(--yellow)}}.conditionTop>.mobileDisclosure>.panel{{height:auto}}.factorDisclosure>.panel{{border:0;padding:0}}.matrixDisclosure,.simulatorDisclosure{{margin:8px 0}}.matrixDisclosure>.detailMatrix,.simulatorDisclosure>.simulator{{margin-top:0}}.overallTableDisclosure{{margin-top:10px}}.radarDisclosure>.panel{{border:0;padding:0}}.radarPicker{{margin-top:4px}}.radarPicker>summary{{min-height:36px;padding:7px 9px;border-left-width:3px;font-size:12px}}.gapPanel{{padding:10px;margin:8px 0}}.gapGrid{{display:grid;grid-template-columns:none;grid-auto-flow:column;grid-auto-columns:88%;gap:8px;overflow-x:auto;scroll-snap-type:x mandatory;padding-right:10%}}.gapGrid article{{scroll-snap-align:start;padding:10px}}.gapList{{font-size:12px;padding-left:17px}}.simGrid{{padding:8px}}.simOptions{{gap:6px}}.simOptions label{{padding:8px}}.simResult{{padding:12px}}.simResult strong{{font-size:28px}}.tableScroll{{max-height:62vh}}}}
    @media(max-width:720px){{.actions{{display:grid;grid-template-columns:1fr;gap:6px;overflow:visible;margin-top:10px;padding-bottom:0}}.actions .btn{{width:100%;min-height:38px;padding:7px 9px;font-size:12px}}}}
    @media(max-width:720px){{.productGapSpotlight{{grid-template-columns:1fr;min-height:0}}.productGapMedia{{border-right:0;border-bottom:1px solid var(--line);padding:12px}}.productGapMedia img{{height:155px;padding:4px}}.productGapContent{{padding:12px}}.productGapContent h3{{font-size:17px}}.productGapContent ol{{grid-template-columns:1fr;gap:6px}}.conditionVisualNav{{display:grid;grid-template-columns:none;grid-auto-flow:column;grid-auto-columns:84%;gap:8px;overflow-x:auto;scroll-snap-type:x mandatory;padding-right:12%;margin:9px 0}}.conditionVisualCard{{scroll-snap-align:start;min-height:178px}}.conditionVisualSource{{font-size:9px}}}}
    @media(max-width:1200px){{.marketInsightGrid,.marketEvidenceGrid{{grid-template-columns:1fr}}.applicationGrid{{grid-template-columns:repeat(2,minmax(0,1fr))}}.engineeringPriorityGrid{{grid-template-columns:1fr 1fr}}.sourceMacroGrid{{grid-template-columns:1fr}}.sourceVisualGrid-3{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
    @media(max-width:720px){{.navSubmenu{{grid-template-columns:1fr}}.marketKpis{{grid-template-columns:1fr 1fr;gap:7px}}.marketKpis>div{{padding:9px;min-height:82px}}.marketKpis b{{font-size:15px}}.marketInsightGrid,.marketEvidenceGrid{{gap:8px}}.marketTrendPanel,.marketReading,.marketDataPanel,.marketFactPanel{{padding:10px}}.marketColumns{{height:205px;grid-template-columns:repeat(4,minmax(46px,1fr));gap:4px;padding-inline:2px}}.marketColumn{{grid-template-rows:135px auto auto auto}}.marketBarShell{{height:135px}}.marketBar{{width:min(42px,78%)}}.marketColumn>strong{{font-size:10px}}.marketLegend{{gap:5px 9px}}.marketDecisionList>div{{grid-template-columns:1fr;gap:3px;padding:8px 0}}.marketDecisionList dt{{font-size:10px}}.marketSeriesEmpty{{min-height:170px;padding:14px}}.marketDataTableWrap{{overscroll-behavior-inline:contain}}.marketFactList{{gap:6px}}.applicationGrid{{grid-template-columns:1fr;gap:8px}}.applicationCard img{{aspect-ratio:16/9}}.applicationMatrixWrap{{padding:10px}}.applicationMatrix,.applicationMatrix tbody,.applicationMatrix tr,.applicationMatrix th,.applicationMatrix td{{display:block;width:100%}}.applicationMatrix thead{{display:none}}.applicationMatrix tr{{margin:0 0 9px;border:1px solid #b9ccdc;background:#fff}}.applicationMatrix th,.applicationMatrix td{{border-bottom:1px solid #dde7ef;padding:9px 10px}}.applicationMatrix tbody th{{border-left:4px solid var(--blue)}}.applicationMatrix .applicationCapabilityCell{{border-left:4px solid var(--yellow);border-bottom:0}}.engineeringScope{{grid-template-columns:1fr}}.engineeringScope>b{{border-right:0;border-bottom:1px solid #c8d7e6}}.engineeringPriorityGrid{{grid-template-columns:1fr;gap:6px}}.engineeringTableWrap{{overflow:visible;border:0}}.engineeringTable,.engineeringTable tbody,.engineeringTable tr,.engineeringTable th,.engineeringTable td{{display:block;width:100%}}.engineeringTable thead{{display:none}}.engineeringTable tr{{margin:0 0 9px;border:1px solid #b9ccdc;background:#fff}}.engineeringTable th,.engineeringTable td{{border-bottom:1px solid #dde7ef;padding:9px 10px}}.engineeringTable tbody th{{border-left:4px solid var(--green)}}.engineeringTable .gapColumn,.engineeringTable .actionColumn{{border-left:4px solid}}.engineeringTable .actionColumn{{border-bottom:0}}.cellLabel{{display:block;margin-bottom:3px;color:#5b7185;font-size:9px;font-weight:900;text-transform:uppercase;letter-spacing:.04em}}.pptBusinessGroup{{margin-top:10px;padding-top:9px}}.pptBusinessGroupHead{{display:block;margin-bottom:7px}}.pptBusinessGroupHead h3{{font-size:14px}}.pptBusinessGroupHead p{{margin-top:4px;text-align:left}}.pptBusinessTableStack{{gap:8px}}.pptBusinessTable>summary{{align-items:flex-start;min-height:40px;padding:8px 9px}}.pptBusinessTable>summary h3{{font-size:12px}}.pptBusinessTableScroll{{max-height:72vh}}.pptBusinessTableScroll table{{font-size:10px}}.pptBusinessTableScroll th,.pptBusinessTableScroll td{{min-width:106px;max-width:290px;padding:7px 8px}}.pptBusinessTableScroll tbody th{{min-width:122px}}.sourceContentSection>h2{{padding:14px 12px 0}}.sourceSlide{{padding:14px 12px}}.sourceSlideHeader h3{{font-size:16px}}.sourceParagraph{{font-size:13px;line-height:1.75}}.sourceVisualGrid,.sourceVisualGrid-1,.sourceVisualGrid-3,.sourceVisualGrid-4{{grid-template-columns:1fr;gap:8px;margin-top:12px}}.sourceVisual img,.sourceVisual-picture img{{max-height:none}}.sourceTableScroll table{{font-size:10px}}.sourceTableScroll th,.sourceTableScroll td{{min-width:112px;max-width:300px;padding:7px 8px}}.sourceTableScroll tbody th{{min-width:126px}}}}
    html[data-language="en"] .conditionIntro b:after,html[data-language="en"] .overallNotes p>b:first-child:after,html[data-language="en"] .summaryCard p>b:first-child:after{{content:" "}}html[data-language="en"] .navMenu a,html[data-language="en"] .conditionTitle h2,html[data-language="en"] .simOptions b,html[data-language="en"] .simOptions small{{overflow-wrap:anywhere}}html[data-language="en"] .sourceNote b{{white-space:normal}}html[data-language="en"] th{{white-space:normal;overflow-wrap:anywhere}}html[data-language="en"] .radar-label{{font-size:11px}}
    @media(max-width:720px){{html[data-language="en"] .navTitle{{font-size:11px;line-height:1.2}}html[data-language="en"] .nav small{{display:none}}html[data-language="en"] .summaryGrid,html[data-language="en"] .conditionIntro,html[data-language="en"] .gapGrid{{display:grid;grid-template-columns:1fr;grid-auto-flow:row;grid-auto-columns:auto;overflow:visible;scroll-snap-type:none;padding:0}}html[data-language="en"] .summaryCard{{min-height:0}}html[data-language="en"] .summaryCard,html[data-language="en"] .conditionIntro p,html[data-language="en"] .gapGrid article{{scroll-snap-align:none}}html[data-language="en"] .mobileDisclosure>summary,html[data-language="en"] .radarPicker>summary{{white-space:normal;overflow-wrap:anywhere}}html[data-language="en"] .radarHead{{align-items:flex-start;flex-wrap:wrap}}html[data-language="en"] .radarCurrent{{white-space:normal}}html[data-language="en"] .simHead{{gap:8px;align-items:flex-start}}html[data-language="en"] .resetSim{{flex:0 0 auto;white-space:normal}}}}
    .sourceTableScroll.sourceTableScrollFit{{overflow-x:hidden}}
    .sourceTableScrollFit table.sourceTableFit{{width:100%;min-width:0;table-layout:fixed;font-size:11px}}
    .sourceTableScrollFit table.sourceTableFit th,.sourceTableScrollFit table.sourceTableFit td{{position:static;min-width:0;max-width:none;padding:8px 9px;white-space:pre-line;overflow-wrap:anywhere;word-break:normal;line-height:1.55}}
    .sourceTableScrollFit table.sourceTableFit tbody th{{position:static;min-width:0}}
    @media(max-width:720px){{.sourceTableScroll.sourceTableScrollFit{{max-height:none;overflow:visible;border:0}}.sourceTableScrollFit table.sourceTableFit,.sourceTableScrollFit .sourceTableFit tbody,.sourceTableScrollFit .sourceTableFit tr,.sourceTableScrollFit .sourceTableFit th,.sourceTableScrollFit .sourceTableFit td{{display:block;width:100%}}.sourceTableScrollFit .sourceTableFit colgroup,.sourceTableScrollFit .sourceTableFit thead{{display:none}}.sourceTableScrollFit .sourceTableFit tr{{margin-bottom:10px;border:1px solid #b8ccdd;background:#fff}}.sourceTableScrollFit .sourceTableFit th,.sourceTableScrollFit .sourceTableFit td{{display:grid;grid-template-columns:minmax(88px,7rem) minmax(0,1fr);gap:8px;border-right:0;padding:8px 9px}}.sourceTableScrollFit .sourceTableFit th::before,.sourceTableScrollFit .sourceTableFit td::before{{content:attr(data-label);color:#075da8;font-size:10px;font-weight:900}}.sourceTableScrollFit .sourceTableFit tbody th{{border-left:4px solid #075da8;background:#eef5fa!important}}.sourceTableScrollFit .sourceTableFit tr>:last-child{{border-bottom:0}}}}
    /* Reader-facing copy remains comfortable without loosening dense data tables. */
    .insightLead,.marketRole,.marketDecisionList dd,.marketFactList p,.applicationCard>p,.engineeringScope>span,.engineeringPriorityGrid p,.sourceParagraph,.sourceDataNote{{font-size:14px;line-height:1.7}}
    .marketEvidenceBoundary p,.applicationRequirement b{{font-size:13px;line-height:1.65}}
    .sidebarToggle{{display:none}}
    @media(min-width:901px){{.layout{{grid-template-columns:clamp(216px,16vw,252px) minmax(0,1fr);transition:grid-template-columns .18s ease}}aside.nav{{display:flex;flex-direction:column;overflow:hidden;padding-bottom:66px}}.navMenu{{display:block;grid-column:auto;flex:1;min-height:0;max-height:none;overflow-y:auto;padding:0 3px 0 0}}.navToggle,.mobileTop{{display:none}}.backTop{{left:14px;bottom:14px;min-height:40px;border-radius:4px;padding:8px 14px}}.sourceTableScroll table:not(:has(tr > :nth-child(11))){{width:100%;min-width:100%;table-layout:fixed}}.sourceTableScroll table:not(:has(tr > :nth-child(11))) th,.sourceTableScroll table:not(:has(tr > :nth-child(11))) td{{min-width:0;max-width:none}}.sidebarToggle{{display:inline-flex;align-items:center;justify-content:center;width:100%;min-height:36px;margin:0 0 10px;border:1px solid rgba(255,255,255,.36);border-radius:4px;background:transparent;color:#fff;font-size:12px;font-weight:800;cursor:pointer}}.sidebarToggle:hover,.sidebarToggle:focus-visible{{border-color:var(--yellow);color:var(--yellow);outline:none}}.layout.sidebarCollapsed{{grid-template-columns:76px minmax(0,1fr)}}.layout.sidebarCollapsed aside.nav{{padding-left:10px;padding-right:10px;align-items:center}}.layout.sidebarCollapsed .navBrand img{{width:48px;padding:4px}}.layout.sidebarCollapsed .navTitle,.layout.sidebarCollapsed aside.nav>div>small,.layout.sidebarCollapsed .languageToggle,.layout.sidebarCollapsed .navMenu{{display:none}}.layout.sidebarCollapsed .sidebarToggle{{width:52px;margin-top:10px;padding:5px;line-height:1.25}}}}
    @media(max-width:720px){{.languageToggle,.navToggle,.mobileTop,.actions .btn,.radarLegend button,.radarPicker>summary,.resetSim,.rawTabs button{{min-height:44px}}.languageToggle{{min-width:44px}}.navToggle,.mobileTop{{padding:8px 10px}}.insightLead,.marketRole,.marketDecisionList dd,.marketFactList p,.applicationCard>p,.engineeringScope>span,.engineeringPriorityGrid p,.sourceParagraph,.sourceDataNote{{font-size:15px;line-height:1.72}}.mobileDisclosure>summary,.radarPicker>summary{{min-height:44px}}}}
  </style>
</head>
<body>
<a class="backTop" href="#top" aria-label="回到页面顶部">回到顶部</a>
<div class="layout" id="top">
  <aside class="nav">
    <a class="navBrand" href="arc.html" aria-label="返回全产品线竞品对标平台主页"><img src="assets/xcmg-logo.svg" alt="XCMG"></a>
    <div><div class="navTitle">{esc(meta["label"])}挖掘机对标</div><small>{esc(meta["xcmg"])}</small></div>
    <button class="languageToggle" type="button" aria-label="Switch to English">EN</button>
    <button class="sidebarToggle" type="button" aria-expanded="true" aria-controls="page-nav"><span>收起侧栏</span></button>
    <button class="navToggle" type="button" aria-expanded="false" aria-controls="page-nav">页面导航</button>
    <a class="mobileTop" href="#top">顶部</a>
    <div class="navMenu" id="page-nav">
      <a class="home" href="arc.html">返回对标平台主页</a>
      <a href="#summary">对标概览</a>
      {source_nav_html}
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
        <span class="eyebrow" data-en="North America Product Benchmark">北美产品竞争力分析</span>
        <h1>{esc(meta["title"])}</h1>
        <div class="actions"><a class="btn blue" href="{primary_analysis_target}" data-en="{primary_analysis_en}">{primary_analysis_zh}</a><a class="btn yellow" href="#conditions" data-en="Work-condition benchmark">工况对标</a><a class="btn" href="data-downloads.html" data-en="Data center">数据中心</a></div>
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

    {tonnage_insights_html}

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
      {condition_visual_nav}
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
    <div class="siteCredits" aria-label="项目署名">
      <span data-en="Executive Sponsor: Zhang Shengnan">指导领导：张盛楠</span>
      <span data-en="Data Visualization: Liu Chang">数据可视化：刘畅</span>
      <span data-en="Data Source: ARC Product Team">数据来源：ARC产品小组</span>
      <span><span data-en="Issue Reporting:">问题提报：</span> <a href="mailto:changl@xcmgarc.com">changl@xcmgarc.com</a></span>
    </div>
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
function setupPptBusinessTables(){{
  const query=new URLSearchParams(window.location.search).get('lang');
  let stored='';
  try{{stored=localStorage.getItem('xcmg-benchmark-language')||'';}}catch(_error){{}}
  const language=query==='en'||(query!=='zh'&&stored==='en')?'en':'zh';
  document.querySelectorAll('.pptBusinessTable').forEach(item=>{{
    item.open=language!=='en';
  }});
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
      if(window.matchMedia('(max-width:900px)').matches){{
        menu.classList.remove('open');
        toggle.setAttribute('aria-expanded','false');
        toggle.textContent='页面导航';
      }}
    }}));
  }}
  const navLinks=menu?[...menu.querySelectorAll('a[href^="#"]')]:[];
  const tracked=navLinks.map(link=>({{link,section:document.querySelector(link.getAttribute('href'))}})).filter(item=>item.section);
  const initialHash=window.location.hash;
  let restoreHashEnabled=Boolean(initialHash&&initialHash!=='#');
  const navigationOffset=()=>window.matchMedia('(max-width:900px)').matches
    ? (document.querySelector('aside.nav')?.getBoundingClientRect().height||0)+8
    : 16;
  const scrollToSection=(section,hash,behavior='auto',updateHistory=false)=>{{
    if(!section) return;
    if(updateHistory&&hash){{
      const url=new URL(window.location.href);
      url.hash=hash;
      window.history.replaceState(window.history.state,'',url.pathname+url.search+url.hash);
    }}
    const top=Math.max(0,window.scrollY+section.getBoundingClientRect().top-navigationOffset());
    window.scrollTo({{top,behavior}});
  }};
  navLinks.forEach(link=>link.addEventListener('click',event=>{{
    if(event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey) return;
    const hash=link.getAttribute('href');
    const section=hash?document.querySelector(hash):null;
    if(!section) return;
    event.preventDefault();
    restoreHashEnabled=false;
    navLinks.forEach(item=>item.classList.toggle('active',item===link));
    scrollToSection(section,hash,window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',true);
  }}));
  let navTicking=false;
  const updateActiveNav=()=>{{
    navTicking=false;
    if(!tracked.length) return;
    const offset=window.matchMedia('(max-width:900px)').matches?92:120;
    let active=tracked[0];
    tracked.forEach(item=>{{if(item.section.getBoundingClientRect().top<=offset) active=item;}});
    navLinks.forEach(link=>link.classList.toggle('active',link===active.link));
    menu?.querySelectorAll('.navGroup').forEach(group=>{{
      const current=Boolean(group.querySelector('a.active'));
      group.classList.toggle('current',current);
      if(current) group.open=true;
    }});
  }};
  const scheduleActiveNav=()=>{{
    if(navTicking) return;
    navTicking=true;
    window.requestAnimationFrame(updateActiveNav);
  }};
  window.addEventListener('scroll',scheduleActiveNav,{{passive:true}});
  window.addEventListener('resize',scheduleActiveNav,{{passive:true}});
  scheduleActiveNav();
  const restoreHash=()=>{{
    if(!restoreHashEnabled) return;
    const hash=initialHash;
    if(!hash||hash==='#') return;
    const section=document.querySelector(hash);
    if(section) scrollToSection(section,hash,'auto',false);
  }};
  const cancelHashRestore=()=>{{restoreHashEnabled=false;}};
  window.addEventListener('wheel',cancelHashRestore,{{passive:true,once:true}});
  window.addEventListener('touchstart',cancelHashRestore,{{passive:true,once:true}});
  window.addEventListener('pointerdown',cancelHashRestore,{{passive:true,once:true}});
  window.addEventListener('keydown',cancelHashRestore,{{once:true}});
  window.addEventListener('load',restoreHash,{{once:true}});
  document.addEventListener('xcmg:i18n-rendered',restoreHash);
  [0,250,900,1600,2600].forEach(delay=>window.setTimeout(restoreHash,delay));
  const backTop=document.querySelector('.backTop');
  if(backTop){{
    const update=()=>backTop.classList.toggle('show',window.scrollY>640);
    window.addEventListener('scroll',update,{{passive:true}});
    update();
  }}
}}
function setupSidebarCollapse(){{
  const layout=document.querySelector('.layout');
  const nav=layout?.querySelector('aside.nav');
  if(!layout||!nav)return;
  let toggle=nav.querySelector('.sidebarToggle');
  if(!toggle){{
    toggle=document.createElement('button');
    toggle.className='sidebarToggle';
    toggle.type='button';
    toggle.setAttribute('aria-expanded','true');
    toggle.setAttribute('aria-controls',nav.querySelector('.navMenu')?.id||'page-nav');
    toggle.innerHTML='<span>收起侧栏</span>';
    nav.insertBefore(toggle,nav.querySelector('.navToggle')||nav.querySelector('.navMenu'));
  }}
  const desktop=window.matchMedia('(min-width:901px)');
  const storageKey='xcmg-dashboard-sidebar-collapsed';
  let stored=false;
  try{{stored=localStorage.getItem(storageKey)==='1';}}catch(error){{stored=false;}}
  const getLabel=collapsed=>{{
    const isEn=document.documentElement.dataset.language==='en';
    return collapsed?(isEn?'Open navigation':'展开侧栏'):(isEn?'Collapse navigation':'收起侧栏');
  }};
  const apply=(collapsed,persist)=>{{
    const effective=desktop.matches&&collapsed;
    layout.classList.toggle('sidebarCollapsed',effective);
    toggle.setAttribute('aria-expanded',String(!effective));
    const text=getLabel(effective);
    const label=toggle.querySelector('span');
    if(label)label.textContent=text;
    toggle.setAttribute('aria-label',text);
    if(persist){{
      stored=effective;
      try{{localStorage.setItem(storageKey,effective?'1':'0');}}catch(error){{}}
    }}
  }};
  apply(stored,false);
  toggle.addEventListener('click',()=>apply(!layout.classList.contains('sidebarCollapsed'),true));
  const sync=()=>apply(stored,false);
  if(desktop.addEventListener)desktop.addEventListener('change',sync);
  else if(desktop.addListener)desktop.addListener(sync);
  document.addEventListener('xcmg:i18n-rendered',()=>apply(layout.classList.contains('sidebarCollapsed'),false));
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
setupPptBusinessTables();
setupMobileDisclosures();
setupRadars();
setupSimulators();
setupRawTabs();
setupSidebarCollapse();
setupPageNavigation();
</script>
<script src="assets/i18n.js?v=20260723c"></script>
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
    new_product_assets = [
        (
            "https://xcmg-usa.com/wp-content/uploads/2022/05/XE250U%E6%8A%A0%E5%9B%BE.png",
            ASSET_DIR / "xe250u-official-cropped.webp",
            ".png",
        ),
        (
            "https://xcmg-usa.com/wp-content/uploads/2025/04/235UCR_web-image.png",
            ASSET_DIR / "xe235ucr-official-cropped.webp",
            ".png",
        ),
        (
            "https://xcmg-usa.com/wp-content/uploads/2022/05/XE300U-1.jpg",
            ASSET_DIR / "xe300u-official-cropped.webp",
            ".jpg",
        ),
        (
            "https://xcmg-usa.com/wp-content/uploads/2022/05/XE360U.jpg",
            ASSET_DIR / "xe360u-official-cropped.webp",
            ".jpg",
        ),
    ]
    for url, cropped_dest, source_suffix in new_product_assets:
        if cropped_dest.exists() and cropped_dest.stat().st_size > 10000:
            continue
        source_path = ASSET_DIR / f".{cropped_dest.stem}-source{source_suffix}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as response:
            source_path.write_bytes(response.read())
        crop_product_image(source_path, cropped_dest, max_dimension=1600)
        source_path.unlink(missing_ok=True)
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
    }
    for marker, value in values.items():
        pattern = rf"<!-- {marker} -->.*?<!-- /{marker} -->"
        replacement = f"<!-- {marker} -->{value}<!-- /{marker} -->"
        text, count = re.subn(pattern, replacement, text, flags=re.S)
        if count != 1:
            raise ValueError(f"ARC metric marker missing or duplicated: {marker}")
    arc_path.write_text(text, encoding="utf-8", newline="\n")


def write_project_manifest(models):
    ppt_business_tables = load_ppt_business_tables()
    table_summary = ppt_business_tables.get("summary", {})
    manifest = {
        "productLineCount": 7,
        "excavatorTonnageCount": len(models),
        "benchmarkProductCount": sum(len(model["products"]) for model in models),
        "sourceWorkbookCount": len(SOURCE_FILES),
        "minimumScoreCoverage": MIN_SCORE_COVERAGE,
        "overallWeights": OVERALL_WEIGHTS,
        "marketOverview": {
            "output": "excavator-market-overview.html",
            "data": "data/ppt-insights/excavator-market-overview.json",
            "classification": "XCMG ARC INTERNAL",
        },
        "pptBusinessTables": {
            "data": "data/ppt-insights/ppt-business-tables.json",
            "includedBusinessTableCount": table_summary.get("included_table_count", 0),
            "excludedNavigationTableCount": table_summary.get("excluded", {}).get("navigation_table", 0),
            "excludedPersonnelTableCount": table_summary.get("excluded", {}).get("personnel_table", 0),
            "classification": "XCMG ARC INTERNAL",
        },
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


PPT_CHART_CSS = r"""
/* Source charts are rebuilt from the embedded workbook data. */
.sourceVisualGrid:has(.sourceDataChart){grid-template-columns:minmax(0,1fr)}
.sourceDataChart{display:block;min-width:0;padding:0;border:1px solid #b8ccdd;background:#fff;overflow:hidden}
.sourceDataChart>figcaption{display:flex;align-items:center;min-height:42px;padding:10px 14px;border-bottom:1px solid #d7e2ec;background:#f3f8fb;color:#073c70;font-size:14px;font-weight:900;line-height:1.4}
.sourceChartViewport{max-width:100%;overflow-x:auto;overflow-y:hidden;overscroll-behavior-inline:contain;scrollbar-color:#8299ad #edf2f6;background:#fff}
.sourceChartSvg{display:block;width:min(100%,72rem);min-width:0;height:auto;max-height:none;margin-inline:auto;background:#fff;font-family:"Segoe UI",Arial,"Microsoft YaHei",sans-serif}
.sourceDataChart[data-chart-density="dense"] .sourceChartSvg{width:100%;min-width:0}
.sourceChartGrid line,.sourceChartRadarGrid line,.sourceChartRadarGrid polygon{fill:none;stroke:#dbe6ef;stroke-width:1}
.sourceChartSvg text,.sourceChartGrid,.sourceChartRadarGrid,.sourceChartLabels{pointer-events:none}
.sourceChartGrid text,.sourceChartLabels text{fill:#36536d;font-size:12px}
.sourceChartCategory,.sourceChartRadarLabel,.sourceChartAxisTitle{fill:#0a355c!important;font-weight:800}
.sourceChartAxisTitle{font-size:13px!important}
.sourceChartAxisValue,.sourceChartSecondaryAxis{fill:#64798c!important;font-size:10px!important}
.sourceChartValue,.sourceChartTotal,.sourceChartGrowthValue{fill:#082f54!important;font-size:11px!important;font-weight:900}
.sourceChartSegmentValue{fill:#fff!important;font-size:10px!important;font-weight:900;paint-order:stroke;stroke:rgba(0,35,68,.38);stroke-width:2px}
.sourceChartMark,.sourceChartPoint,.sourceChartSeries,.sourceChartBubble,.sourceChartDonutArc{transition:opacity .16s ease,filter .16s ease,stroke-width .16s ease}
.sourceChartMarks:hover .sourceChartMark:not(:hover),.sourceChartMarks:hover .sourceChartSeries:not(:hover),.sourceChartMarks:hover .sourceChartBubble:not(:hover){opacity:.24}
.sourceChartMark:hover,.sourceChartSeries:hover,.sourceChartBubble:hover{opacity:1;filter:brightness(1.04) saturate(1.12)}
.sourceChartLine{fill:none;stroke-width:3}
.sourceChartSeries polygon{fill:var(--series-color);fill-opacity:.10;stroke:var(--series-color);stroke-width:2.4}
.sourceChartSeries circle{fill:var(--series-color);fill-opacity:.88;stroke:#fff;stroke-width:1.5}
.sourceChartSeries:hover polygon{fill-opacity:.20;stroke-width:3.4}
.sourceChartArea{opacity:.86;stroke:#fff;stroke-width:1}
.sourceChartBubble circle{fill:var(--series-color);fill-opacity:.74;stroke:var(--series-color);stroke-width:2}
.sourceChartLeader{stroke:var(--series-color);stroke-width:1.2;opacity:.72}
.sourceChartBubbleLabel{fill:#0a355c!important;font-size:11px!important;font-weight:900}
.sourceChartBubbleValue{fill:#60758a!important;font-size:9px!important;font-weight:800}
.sourceChartLegend{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:7px 14px;padding:10px 14px 12px;border-top:1px solid #e0e8ef;background:#fbfdff;color:#334f67;font-size:11px}
.sourceChartLegendItem{display:inline-flex;align-items:center;gap:5px;min-width:0}
.sourceChartLegendItem i{display:inline-block;width:11px;height:11px;flex:0 0 11px;background:var(--series-color)}
.sourceChartLegendLine i{height:3px}
.sourceChartLegendItem b{font-weight:800;overflow-wrap:anywhere}
.sourceChartDonutArc{fill:none}
.sourceChartDonutTotal{fill:#073c70;font-size:32px;font-weight:900}
.sourceChartDonutLabel{fill:#64798c;font-size:11px;font-weight:800;letter-spacing:.08em}
.sourceVisual-picture{min-height:0}
.sourceVisual-picture img{width:auto;max-width:100%;height:auto;max-height:480px;object-fit:contain}
.sourceDataChart,.nativeChartPanel{position:relative}
.chartInteractable{cursor:pointer;outline:none;transform-box:fill-box;transform-origin:center;transition:opacity .16s ease,filter .16s ease,transform .16s ease,stroke-width .16s ease}
.chartHasFocus .chartInteractable.is-dimmed{opacity:.16!important;filter:saturate(.24)}
.chartInteractable.is-focused{opacity:1!important;filter:drop-shadow(0 2px 3px rgba(3,52,92,.28)) brightness(1.05) saturate(1.12)}
.sourceChartMark.is-focused,.nativeChartBar.is-focused{transform:translateY(-2px)}
.sourceChartDonutArc.is-focused{stroke-width:78!important}
.nativeDonutSegment.is-focused{stroke-width:60!important}
.chartInteractable:focus-visible{stroke:#f7b500!important;stroke-width:3!important;filter:drop-shadow(0 0 3px rgba(247,181,0,.58))}
.sourceChartLegendItem,.nativeChartLegendItem,.nativeDonutLegend li{cursor:pointer;outline:none;border-radius:2px;transition:opacity .16s ease,background .16s ease,box-shadow .16s ease}
.sourceChartLegendItem.is-dimmed,.nativeChartLegendItem.is-dimmed,.nativeDonutLegend li.is-dimmed{opacity:.3}
.sourceChartLegendItem.is-focused,.nativeChartLegendItem.is-focused,.nativeDonutLegend li.is-focused{opacity:1;background:#eaf3fa;box-shadow:0 0 0 2px #a8c7df}
.sourceChartLegendItem:focus-visible,.nativeChartLegendItem:focus-visible,.nativeDonutLegend li:focus-visible{box-shadow:0 0 0 2px #f7b500}
.chartLockState{position:absolute;z-index:4;top:8px;right:10px;display:inline-flex;align-items:center;gap:7px;min-height:27px;padding:4px 8px;border:1px solid #8fb5d2;background:#fff;color:#075da8;font:800 11px/1 "Segoe UI",Arial,"Microsoft YaHei",sans-serif;box-shadow:0 2px 8px rgba(7,60,112,.12);cursor:pointer}
.chartLockState[hidden]{display:none}
.chartLockState b{font-size:15px;line-height:1}
.sourceDataChart:has(.chartLockState:not([hidden]))>figcaption,.nativeChartPanel:has(.chartLockState:not([hidden]))>h4{padding-right:92px}
.chartInteractionTooltip{position:fixed;z-index:10000;max-width:min(340px,calc(100vw - 24px));padding:8px 10px;border:1px solid #6f9cbd;background:#062f54;color:#fff;font:700 12px/1.45 "Segoe UI",Arial,"Microsoft YaHei",sans-serif;box-shadow:0 6px 20px rgba(3,32,58,.24);pointer-events:none;opacity:0;transform:translateY(4px);transition:opacity .12s ease,transform .12s ease}
.chartInteractionTooltip.is-visible{opacity:1;transform:translateY(0)}
@media(max-width:720px){
  .sourceDataChart>figcaption{min-height:38px;padding:9px 10px;font-size:12px}
  .sourceChartSvg{min-width:42rem}
  .sourceDataChart[data-chart-density="dense"] .sourceChartSvg{width:72rem;min-width:72rem}
  .sourceChartLegend{justify-content:flex-start;gap:6px 10px;padding:8px 10px 10px;font-size:10px}
  .sourceVisual-picture img{width:auto;max-width:100%;height:auto;max-height:none}
  .chartLockState{position:static;margin:8px 10px 0;box-shadow:none}
  .sourceDataChart:has(.chartLockState:not([hidden]))>figcaption,.nativeChartPanel:has(.chartLockState:not([hidden]))>h4{padding-right:10px}
}
"""


PPT_CHART_INTERACTION_JS = r"""
(function () {
  'use strict';

  const chartSelector = '.sourceDataChart, .nativeChartPanel';
  const markSelector = [
    '.sourceChartMark',
    '.sourceChartSeries',
    '.sourceChartBubble',
    '.sourceChartPoint',
    '.sourceChartDonutArc',
    '.nativeChartMark'
  ].join(',');
  const legendSelector = [
    '.sourceChartLegendItem',
    '.nativeChartLegendItem',
    '.nativeDonutLegend li'
  ].join(',');
  let tooltip = null;

  function isEnglish() {
    return document.documentElement.lang.toLowerCase().startsWith('en');
  }

  function copy() {
    return isEnglish()
      ? {locked: 'Locked', clear: 'Clear chart selection'}
      : {locked: '已锁定', clear: '清除图表选择'};
  }

  function ensureTooltip() {
    if (tooltip) return tooltip;
    tooltip = document.createElement('div');
    tooltip.className = 'chartInteractionTooltip';
    tooltip.setAttribute('role', 'tooltip');
    tooltip.hidden = true;
    document.body.appendChild(tooltip);
    return tooltip;
  }

  function labelFor(node) {
    if (!node) return '';
    const explicit = isEnglish() ? node.dataset.tooltipEn : node.dataset.tooltip;
    if (explicit) return explicit.trim();
    const title = node.querySelector(':scope > title') || node.querySelector('title');
    if (title?.textContent?.trim()) return title.textContent.trim();
    return (node.textContent || '').replace(/\s+/g, ' ').trim();
  }

  function placeTooltip(event, node) {
    const tip = ensureTooltip();
    const rect = node.getBoundingClientRect();
    const requestedX = event?.clientX ?? rect.left + rect.width / 2;
    const requestedY = event?.clientY ?? rect.top;
    const margin = 12;
    const width = tip.offsetWidth;
    const height = tip.offsetHeight;
    const left = Math.max(margin, Math.min(window.innerWidth - width - margin, requestedX + 13));
    const above = requestedY - height - 12;
    const top = above >= margin
      ? above
      : Math.min(window.innerHeight - height - margin, requestedY + 16);
    tip.style.left = `${left}px`;
    tip.style.top = `${Math.max(margin, top)}px`;
  }

  function showTooltip(node, event) {
    const text = labelFor(node);
    if (!text) return;
    const tip = ensureTooltip();
    tip.textContent = text;
    tip.hidden = false;
    tip.classList.add('is-visible');
    window.requestAnimationFrame(() => placeTooltip(event, node));
  }

  function hideTooltip() {
    if (!tooltip) return;
    tooltip.classList.remove('is-visible');
    window.setTimeout(() => {
      if (!tooltip.classList.contains('is-visible')) tooltip.hidden = true;
    }, 130);
  }

  function renderableMark(node) {
    if (!(node instanceof SVGGraphicsElement)) return true;
    try {
      const box = node.getBBox();
      return box.width > 0.2 || box.height > 0.2;
    } catch (_) {
      return true;
    }
  }

  function seriesIndex(node) {
    const value = node?.dataset?.seriesIndex;
    return value === undefined ? '' : String(value);
  }

  function setPressed(node, pressed) {
    node.classList.toggle('is-focused', pressed);
    node.setAttribute('aria-pressed', pressed ? 'true' : 'false');
  }

  function applyFocus(chart, target) {
    const marks = [...chart.querySelectorAll(markSelector)].filter(renderableMark);
    const legends = [...chart.querySelectorAll(legendSelector)];
    const targetIsLegend = Boolean(target?.matches(legendSelector));
    const targetSeries = seriesIndex(target);
    const selectedMarks = targetIsLegend && targetSeries !== ''
      ? marks.filter((mark) => seriesIndex(mark) === targetSeries)
      : target ? [target] : [];

    chart.classList.toggle('chartHasFocus', selectedMarks.length > 0);
    marks.forEach((mark) => {
      const selected = selectedMarks.includes(mark);
      mark.classList.toggle('is-dimmed', selectedMarks.length > 0 && !selected);
      setPressed(mark, selected);
    });
    legends.forEach((legend) => {
      const selected = targetSeries !== '' && seriesIndex(legend) === targetSeries;
      legend.classList.toggle('is-dimmed', selectedMarks.length > 0 && targetSeries !== '' && !selected);
      setPressed(legend, selected);
    });
  }

  function clearFocus(chart) {
    chart.classList.remove('chartHasFocus');
    chart.querySelectorAll(`${markSelector},${legendSelector}`).forEach((node) => {
      node.classList.remove('is-focused', 'is-dimmed');
      node.setAttribute('aria-pressed', 'false');
    });
  }

  function updateLockState(chart) {
    const state = chart.querySelector(':scope > .chartLockState');
    if (!state) return;
    const language = copy();
    state.hidden = !chart.__chartLocked;
    state.querySelector('span').textContent = language.locked;
    state.setAttribute('aria-label', language.clear);
    state.title = chart.__chartLocked ? labelFor(chart.__chartLocked) : language.clear;
  }

  function clearLock(chart) {
    chart.__chartLocked = null;
    clearFocus(chart);
    updateLockState(chart);
    hideTooltip();
  }

  function lockTarget(chart, target, event) {
    if (chart.__chartLocked === target) {
      clearLock(chart);
      return;
    }
    chart.__chartLocked = target;
    applyFocus(chart, target);
    updateLockState(chart);
    showTooltip(target, event);
  }

  function eventTarget(chart, event) {
    const origin = event.target instanceof Element ? event.target : event.target?.parentElement;
    const target = origin?.closest(`${markSelector},${legendSelector}`);
    return target && chart.contains(target) ? target : null;
  }

  function prepareInteractiveNode(node, index) {
    if (!node.dataset.seriesIndex && node.matches(legendSelector)) {
      node.dataset.seriesIndex = String(index);
    }
    node.classList.add('chartInteractable');
    node.setAttribute('role', 'button');
    node.setAttribute('tabindex', '0');
    node.setAttribute('aria-pressed', 'false');
    const label = labelFor(node);
    if (label) node.setAttribute('aria-label', label);
  }

  function initializeChart(chart) {
    if (chart.dataset.chartInteractions === 'ready') return;
    chart.dataset.chartInteractions = 'ready';
    const marks = [...chart.querySelectorAll(markSelector)].filter(renderableMark);
    const legends = [...chart.querySelectorAll(legendSelector)];
    marks.forEach((node, index) => prepareInteractiveNode(node, index));
    legends.forEach((node, index) => prepareInteractiveNode(node, index));
    if (!marks.length) return;

    const lockState = document.createElement('button');
    lockState.className = 'chartLockState';
    lockState.type = 'button';
    lockState.hidden = true;
    lockState.innerHTML = '<span></span><b aria-hidden="true">×</b>';
    lockState.addEventListener('click', (event) => {
      event.stopPropagation();
      clearLock(chart);
    });
    chart.appendChild(lockState);
    updateLockState(chart);

    chart.addEventListener('pointerover', (event) => {
      const target = eventTarget(chart, event);
      if (!target || target.contains(event.relatedTarget)) return;
      if (!chart.__chartLocked) applyFocus(chart, target);
      showTooltip(target, event);
    });
    chart.addEventListener('pointermove', (event) => {
      const target = eventTarget(chart, event);
      if (target && tooltip && !tooltip.hidden) placeTooltip(event, target);
    });
    chart.addEventListener('pointerout', (event) => {
      const target = eventTarget(chart, event);
      if (!target || target.contains(event.relatedTarget)) return;
      if (chart.__chartLocked) applyFocus(chart, chart.__chartLocked);
      else clearFocus(chart);
      hideTooltip();
    });
    chart.addEventListener('focusin', (event) => {
      const target = eventTarget(chart, event);
      if (!target) return;
      if (!chart.__chartLocked) applyFocus(chart, target);
      showTooltip(target);
    });
    chart.addEventListener('focusout', (event) => {
      if (chart.contains(event.relatedTarget)) return;
      if (chart.__chartLocked) applyFocus(chart, chart.__chartLocked);
      else clearFocus(chart);
      hideTooltip();
    });
    chart.addEventListener('click', (event) => {
      const target = eventTarget(chart, event);
      if (target) {
        event.preventDefault();
        lockTarget(chart, target, event);
        return;
      }
      if (event.target.closest('.sourceChartViewport,.nativeChartCanvas,.sourceChartLegend,.nativeChartLegend,.nativeDonutLayout')) {
        clearLock(chart);
      }
    });
    chart.addEventListener('keydown', (event) => {
      const target = eventTarget(chart, event);
      if (event.key === 'Escape') {
        clearLock(chart);
      } else if (target && (event.key === 'Enter' || event.key === ' ')) {
        event.preventDefault();
        lockTarget(chart, target);
      }
    });
  }

  function initializeCharts(root) {
    root.querySelectorAll(chartSelector).forEach(initializeChart);
  }

  function init() {
    initializeCharts(document);
    const observer = new MutationObserver((records) => {
      records.forEach((record) => {
        record.addedNodes.forEach((node) => {
          if (!(node instanceof Element)) return;
          if (node.matches(chartSelector)) initializeChart(node);
          initializeCharts(node);
        });
      });
    });
    observer.observe(document.body, {childList: true, subtree: true});
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, {once: true});
  } else {
    init();
  }
})();
"""


def externalize_dashboard_assets(page_html):
    style_start = page_html.index("  <style>")
    style_end = page_html.index("  </style>", style_start) + len("  </style>")
    css = (
        page_html[style_start + len("  <style>"): style_end - len("  </style>")].strip()
        + "\n"
        + PPT_CHART_CSS.strip()
        + "\n"
    )

    script_start = page_html.rfind("<script>")
    script_end = page_html.index("</script>", script_start) + len("</script>")
    javascript = (
        page_html[script_start + len("<script>"): script_end - len("</script>")].strip()
        + "\n"
        + PPT_CHART_INTERACTION_JS.strip()
        + "\n"
    )

    assets_dir = ROOT / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    (assets_dir / "dashboard.css").write_text(css, encoding="utf-8", newline="\n")
    (assets_dir / "dashboard.js").write_text(javascript, encoding="utf-8", newline="\n")

    page_html = page_html[:style_start] + (
        '  <link rel="stylesheet" href="assets/dashboard.css?v=20260724k">\n'
        '  <link rel="stylesheet" href="assets/site-credits.css?v=20260724a">'
    ) + page_html[style_end:]
    script_start = page_html.rfind("<script>")
    script_end = page_html.index("</script>", script_start) + len("</script>")
    page_html = page_html[:script_start] + '<script src="assets/dashboard.js?v=20260724k"></script>' + page_html[script_end:]
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
        page_html = "\n".join(line.rstrip() for line in page_html.splitlines()) + "\n"
        (ROOT / meta["output"]).write_text(page_html, encoding="utf-8", newline="\n")
    write_project_manifest(models)
    update_arc_metrics(models)


if __name__ == "__main__":
    main()
