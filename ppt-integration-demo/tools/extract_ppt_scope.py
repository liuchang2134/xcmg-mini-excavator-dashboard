"""Extract the approved 3-4 t PPT scope into a traceable slide registry."""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}

SLIDE_META = {
    48: (
        "市场销量与竞争格局",
        "Market volume and competitive landscape",
        "market",
        "market_volume_brand_mix",
        "3-4吨是北美挖机核心销量区间；PPT称微小挖四强近三年合计约占74%，并给出2023-2026预测销量结构。",
        "The 3-4 t class is presented as a core North American volume segment. The source states that the four leading compact-excavator brands held about 74% combined share and provides a 2023-2026 forecast mix.",
        "historical_fact_and_forecast",
        "2025 market snapshot; 2026 forecast",
    ),
    49: (
        "运输方式、驾照约束与客户结构",
        "Transport method, licence constraints and customer mix",
        "transport",
        "transport_payload_regulation",
        "北美客户常用轻型皮卡与14K拖车转运3.5吨挖机及附件；现款XE35U带典型附件后运输灵活性不足，PPT中的法规表述需由合规部门复核。",
        "North American users commonly move a 3.5 t excavator and attachments with a light-duty pickup and 14K trailer. The current XE35U is described as transport-constrained once typical attachments are added; regulatory statements require compliance revalidation.",
        "historical_assessment",
        "PPT version 11.14; year not stated on slide",
    ),
    50: (
        "市政与道路维修：施工流程（上）",
        "Municipal and road maintenance workflow, part 1",
        "municipal_roadwork",
        "workflow_customer_needs",
        "沟槽开挖、预制件吊装、回填和平整要求精准操控、稳定性、回转力矩、推土铲浮动及多属具适配。",
        "Trenching, lifting precast components, backfilling and grading require precise control, stability, swing torque, blade float and attachment versatility.",
        "historical_assessment_and_plan",
        "PPT version 11.14; year not stated on slide",
    ),
    51: (
        "市政与道路维修：施工流程（下）",
        "Municipal and road maintenance workflow, part 2",
        "municipal_roadwork",
        "workflow_customer_needs",
        "地面整理、设施安装和景观石吊装进一步强调小空间精准作业、行走启停稳定性和驾驶舒适性。",
        "Finishing, utility installation and landscape-stone handling reinforce the need for confined-space precision, travel start-stop stability and operator comfort.",
        "historical_assessment_and_plan",
        "PPT version 11.14; year not stated on slide",
    ),
    52: (
        "小型拆除",
        "Light demolition",
        "light_demolition",
        "workflow_customer_needs",
        "小型拆除依赖铲斗与拇指钳、封闭驾驶室、足够作业范围及精细操控；资料称附件管路基本满足，但蜂鸣器消音未满足。",
        "Light demolition depends on bucket-and-thumb handling, an enclosed cab, sufficient reach and fine control. The source considers attachment plumbing broadly adequate but reports no alarm mute function.",
        "historical_assessment_and_plan",
        "PPT version 11.14; year not stated on slide",
    ),
    53: (
        "地基挖掘",
        "Foundation excavation",
        "foundation_excavation",
        "workflow_customer_needs",
        "受限空间地基施工要求短尾、动臂偏摆、深度精度、回填效率和附件兼容；资料重点指出回转力矩与推土铲功能缺口。",
        "Confined foundation work requires short-tail packaging, boom swing, depth accuracy, backfill productivity and attachment compatibility. The source highlights swing-torque and blade-function gaps.",
        "historical_assessment_and_plan",
        "PPT version 11.14; year not stated on slide",
    ),
    54: (
        "花园改造：土方与排水",
        "Landscape renovation: earthwork and drainage",
        "landscape_renovation",
        "workflow_customer_needs",
        "花园改造前半流程包括清表、地形修整、沟槽、管道安装与回填，核心需求是精细控制、稳定起吊和高效回填。",
        "The first half of the landscape-renovation workflow covers clearing, shaping, trenching, pipe installation and backfill, with emphasis on fine control, stable lifting and productive backfilling.",
        "historical_assessment_and_plan",
        "PPT version 11.14; year not stated on slide",
    ),
    55: (
        "花园改造：整平与绿化",
        "Landscape renovation: grading and planting",
        "landscape_renovation",
        "workflow_customer_needs",
        "后半流程覆盖场地平整、绿化布局与收尾，强调坡度和深度控制、地下设施保护、狭小场地操作与环境影响。",
        "The second half covers grading, planting and finishing, emphasizing slope/depth control, utility protection, confined-site operation and environmental impact.",
        "historical_assessment_and_plan",
        "PPT version 11.14; year not stated on slide",
    ),
    56: (
        "道路与桥梁建设",
        "Road and bridge construction",
        "road_bridge",
        "workflow_customer_needs",
        "道路和桥梁辅助施工涉及沟渠、基础、回填、压实及路缘设施安装；对稳定性、回转回填、舒适性和多属具支持要求较高。",
        "Road and bridge support work covers trenches, foundations, backfill, compaction and curb installation, with strong requirements for stability, swing-assisted backfill, comfort and attachment support.",
        "historical_assessment_and_plan",
        "PPT version 11.14; year not stated on slide",
    ),
    57: (
        "农业：土地清理",
        "Agriculture: land clearing",
        "agricultural_clearing",
        "workflow_customer_needs",
        "土地清理需要拇指钳、割草机或开带机等附件，并要求非专业机手易操作、不平地面稳定、行走效率高。",
        "Land clearing needs attachments such as a thumb, mower or brush cutter, plus intuitive controls for non-professional operators, rough-ground stability and efficient travel.",
        "historical_assessment_and_plan",
        "PPT version 11.14; year not stated on slide",
    ),
    58: (
        "农业：排水系统",
        "Agriculture: drainage systems",
        "agricultural_drainage",
        "workflow_customer_needs",
        "农田排水覆盖沟渠开挖、管道吊装、回填与表面整理；资料总结行走速度、回转力矩、推土铲功能、报警消音和行走稳定性仍需提升。",
        "Agricultural drainage covers trenching, pipe handling, backfill and finishing. The source identifies travel speed, swing torque, blade functions, alarm mute and travel stability as improvement needs.",
        "historical_assessment_and_plan",
        "PPT version 11.14; year not stated on slide",
    ),
    59: (
        "运输、接地与工作范围参数",
        "Transport, undercarriage and working-range parameters",
        "paper_competitiveness",
        "dimensions_working_range",
        "XE35U操作重量4200 kg且运输尺寸偏大；最大挖掘深度3060 mm，弱于久保田KX033-4和三一SY35U；当前型谱缺少常规尾机型。",
        "The XE35U is listed at 4,200 kg with comparatively large transport dimensions. Its 3,060 mm digging depth trails the Kubota KX033-4 and SANY SY35U, while the range lacks a conventional-tail model.",
        "historical_specification_comparison",
        "PPT version 11.14; year not stated on slide",
    ),
    60: (
        "动力、工作装置、属具与液压配置",
        "Powertrain, work equipment, attachments and hydraulics",
        "paper_competitiveness",
        "configuration_comparison",
        "发动机功率与竞品接近；XE35U标配AUX2并可选长斗杆，但缺少久保田卸油管路，负载敏感系统的复合动作表现仍需验证和优化。",
        "Engine power is comparable. The XE35U includes AUX2 and offers a long arm, but lacks the Kubota case-drain line; combined-operation performance of the load-sensing system still requires validation and tuning.",
        "historical_specification_comparison",
        "PPT version 11.14; year not stated on slide",
    ),
    61: (
        "力学性能、速度与辅助流量",
        "Forces, speeds and auxiliary flow",
        "paper_competitiveness",
        "performance_comparison",
        "斗杆挖掘力20.3 kN和地面3 m起吊力1145 kg为资料中的优势；铲斗挖掘力28.6 kN、行驶速度2.2/3.6 km/h及AUX1流量40 L/min落后主要竞品。",
        "The source presents 20.3 kN arm force and 1,145 kg lifting capacity at 3 m ground level as strengths. Bucket force at 28.6 kN, travel speed at 2.2/3.6 km/h and AUX1 flow at 40 L/min trail key competitors.",
        "historical_specification_comparison",
        "PPT version 11.14; year not stated on slide",
    ),
    62: (
        "安全性评价",
        "Safety evaluation",
        "field_evaluation",
        "safety",
        "资料认为XE35U直接安全、间接安全和指导性安全配置与久保田基本相当；该评价为内部历史判断，当前机型需复核。",
        "The source assesses direct, indirect and instructional safety provisions as broadly comparable with Kubota. This is a historical internal judgement and requires current-model verification.",
        "historical_internal_evaluation",
        "PPT version 11.14; year not stated on slide",
    ),
    63: (
        "可靠性与环境适应性评价",
        "Reliability and environmental adaptability evaluation",
        "field_evaluation",
        "reliability_environment",
        "资料称常规环境适应性与竞品相当，但紧固件防锈、薄板件涂层耐久和橡胶件耐久弱于久保田；可靠性结论缺少当前量化试验附件。",
        "The source considers normal environmental capability comparable, but rates fastener corrosion protection, sheet-metal coating durability and rubber durability below Kubota. Current quantified validation evidence is not included.",
        "historical_internal_evaluation",
        "PPT version 11.14; year not stated on slide",
    ),
    64: (
        "行走、单动作与复合动作操控评价",
        "Travel, single-function and combined-function control evaluation",
        "field_evaluation",
        "controllability",
        "行走操控经优化后被评为与竞品相当；微动性、作业精准性和平顺性仍有差距，回转制动线性不足会引起工作装置回摆。",
        "Travel control is rated comparable after tuning. Inching, precision and smoothness remain gaps, and insufficient swing-braking linearity is reported to induce implement rebound.",
        "historical_internal_evaluation",
        "PPT version 11.14; year not stated on slide",
    ),
    65: (
        "驾驶环境与人机舒适性评价",
        "Cab environment and ergonomic comfort evaluation",
        "field_evaluation",
        "comfort_hmi",
        "座椅减震、空调、空间匹配及现款小屏交互被列为差距；资料对XE35U PRO 7英寸屏和新驾驶室的表述属于历史方案/状态，需确认。",
        "Seat suspension, HVAC, packaging for larger operators and the current small display are listed as gaps. Statements about the XE35U PRO 7-inch display and revised cab describe a historical plan/status and require confirmation.",
        "historical_internal_evaluation_and_plan",
        "PPT version 11.14; year not stated on slide",
    ),
    66: (
        "维修性、经济性、细节品质与资料评价",
        "Serviceability, operating economy, detail quality and documentation",
        "field_evaluation",
        "serviceability_quality",
        "资料认为燃油经济性有优势，但维修可达性、液压油加注、外观涂装、管线标识及售后资料准确性存在差距。",
        "The source identifies a fuel-economy advantage, while service access, hydraulic-oil filling, coating quality, line identification and after-sales documentation accuracy remain gaps.",
        "historical_internal_evaluation",
        "PPT version 11.14; year not stated on slide",
    ),
    67: (
        "竞争力综合结论",
        "Integrated competitiveness conclusion",
        "portfolio",
        "gap_summary",
        "资料总结XE35U的主要差距为整机重量、行走速度、AUX流量、作业效率、微操控、驾驶空间、维修可达性、涂层耐久和资料准确性，并指出型谱缺少常规尾。",
        "The source summarises gaps in machine mass, travel speed, auxiliary flow, productivity, fine control, cab space, service access, coating durability and documentation accuracy, and notes the absence of a conventional-tail model.",
        "historical_summary",
        "PPT version 11.14; year not stated on slide",
    ),
    68: (
        "产品定位与历史目标",
        "Product positioning and historical target",
        "portfolio",
        "positioning_target",
        "PPT将XE35U定位为“中质低价”，并记录较久保田标杆低15%的历史定价主张及2025年194台销售目标；这些均不得视为当前结果。",
        "The PPT positions the XE35U as a mid-quality, value-priced product and records a historical pricing claim of 15% below the Kubota benchmark plus a 2025 sales target of 194 units. Neither is treated as a current result.",
        "historical_positioning_and_target",
        "2025 historical target; current outcome not provided",
    ),
}

COMPETITORS = [
    "Kubota U35-4",
    "Kubota KX033-4",
    "Kubota KX030-4",
    "SANY SY35U",
    "John Deere 35P",
    "Caterpillar 303/303.5 CR",
    "Bobcat E32/E35",
]


def slide_paragraphs(archive: zipfile.ZipFile, slide: int) -> list[str]:
    root = ET.fromstring(archive.read(f"ppt/slides/slide{slide}.xml"))
    paragraphs: list[str] = []
    for paragraph in root.findall(".//a:p", NS):
        value = "".join(
            node.text or "" for node in paragraph.findall(".//a:t", NS)
        ).strip()
        value = re.sub(r"\s+", " ", value)
        if value:
            paragraphs.append(value)
    return paragraphs


def build_registry(source: Path) -> dict:
    records = []
    with zipfile.ZipFile(source) as archive:
        for slide in range(48, 69):
            title_zh, title_en, scenario, metric, summary_zh, summary_en, status, date = (
                SLIDE_META[slide]
            )
            paragraphs = slide_paragraphs(archive, slide)
            records.append(
                {
                    "id": f"ppt-3-4t-s{slide}",
                    "tonnage": "3-4t",
                    "model": ["XCMG XE35U", "XCMG XE35U PRO"],
                    "competitor": COMPETITORS,
                    "scenario": scenario,
                    "metric": metric,
                    "conclusion": {"zh": summary_zh, "en": summary_en},
                    "source_slide": slide,
                    "source_type": "XCMG ARC internal presentation",
                    "as_of_date": date,
                    "status": status,
                    "validation_status": "source_mapped_current_product_status_unverified",
                    "thumbnail": f"assets/slides/slide-{slide}.png",
                    "zh": {
                        "title": title_zh,
                        "summary": summary_zh,
                        "paragraphs": paragraphs,
                        "raw_text": "\n".join(paragraphs),
                    },
                    "en": {
                        "title": title_en,
                        "summary": summary_en,
                        "source_note": "The original Chinese wording is preserved in the evidence drawer for auditability.",
                    },
                }
            )
    return {
        "meta": {
            "scope": "3-4t prototype",
            "source_file": source.name,
            "source_slides": [48, 68],
            "slide_count": len(records),
            "classification": "XCMG ARC INTERNAL",
            "mapping_rule": "Every source slide is retained as an image and verbatim text record.",
        },
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    registry = build_registry(args.source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Wrote {len(registry['records'])} slide records to {args.output}")


if __name__ == "__main__":
    main()
