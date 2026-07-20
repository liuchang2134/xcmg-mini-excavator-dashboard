"""Extract cross-tonnage excavator insight slides into a traceable registry."""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}

SLIDE_META = {
    3: {
        "topic": "macro_social",
        "title": {"zh": "人口与区域需求迁移", "en": "Population and regional demand shifts"},
        "conclusion": {
            "zh": "资料将美国南部人口增长与迁移视为住宅、市政和公用事业施工需求的重要区域信号。",
            "en": "The source treats population growth and migration into the southern United States as an important regional signal for residential, municipal and utility work.",
        },
        "status": "historical_macro_observation",
        "as_of_date": "2023 population figures in source",
    },
    4: {
        "topic": "technology",
        "title": {"zh": "技术方向与本地化创新", "en": "Technology direction and localized innovation"},
        "conclusion": {
            "zh": "高端化、智能化和绿色化仍是资料判断的长期方向；北美本土研发与用户习惯理解是XCMG需要补强的基础能力。",
            "en": "Premiumization, intelligent functions and lower-emission products remain the long-term direction in the source; North American R&D and user-behavior knowledge are foundational capabilities XCMG needs to strengthen.",
        },
        "status": "historical_strategic_assessment",
        "as_of_date": "PPT 11.14 version",
    },
    5: {
        "topic": "economy_rental",
        "title": {"zh": "市场周期与租赁需求", "en": "Market cycle and rental demand"},
        "conclusion": {
            "zh": "资料判断北美工程机械处于高位调整期，同时租赁市场保持重要地位；产品需兼顾资产周转、残值和多客户通用性。",
            "en": "The source describes North American construction equipment as entering a high-level adjustment phase while rental remains structurally important, increasing the value of utilization, residual value and multi-operator versatility.",
        },
        "status": "historical_macro_assessment",
        "as_of_date": "2023-2025 figures and forecast in source",
    },
    6: {
        "topic": "emissions",
        "title": {"zh": "排放政策与新能源渗透", "en": "Emissions policy and electrification adoption"},
        "conclusion": {
            "zh": "加州激励与其他州推进节奏存在差异，新能源挖机不能用单一全国节奏规划，应按州、客户和应用场景分层验证。",
            "en": "The source notes different adoption rates between California incentives and other states, supporting a state-, customer- and application-specific approach rather than one national electrification assumption.",
        },
        "status": "historical_policy_assessment",
        "as_of_date": "PPT 11.14 version",
    },
    7: {
        "topic": "trade_policy",
        "title": {"zh": "贸易与准入风险", "en": "Trade and market-access risk"},
        "conclusion": {
            "zh": "资料把关税、认证和本地化采购列为进入北美市场的主要外部风险；具体税率与政策必须以当前法务和合规意见为准。",
            "en": "The source identifies tariffs, certification and local-content procurement as major external risks. Any specific rate or rule must be revalidated by current legal and compliance review.",
        },
        "status": "historical_policy_assessment",
        "as_of_date": "PPT 11.14 version; current policy unverified",
    },
    8: {
        "topic": "macro_summary",
        "title": {"zh": "宏观机会与行动框架", "en": "Macro opportunities and action framework"},
        "conclusion": {
            "zh": "宏观层面需要把区域需求、租赁客户、法规准入和本地产品改进同时纳入产品组合决策，而不是只比较采购价格。",
            "en": "At the macro level, portfolio decisions need to combine regional demand, rental users, regulatory access and localized product improvement rather than relying on acquisition price alone.",
        },
        "status": "historical_strategic_summary",
        "as_of_date": "PPT 11.14 version",
    },
    9: {
        "topic": "industry_cycle",
        "title": {"zh": "行业调整周期", "en": "Industry adjustment cycle"},
        "conclusion": {
            "zh": "资料认为补库存、通胀、利率和终端需求共同推动市场由热转冷，并给出2025年美国工程机械约9万台的历史预测。",
            "en": "The source links the market slowdown to post-pandemic restocking, inflation, interest rates and end demand, and records a historical 2025 forecast of roughly 90,000 US construction-equipment units.",
        },
        "status": "historical_forecast",
        "as_of_date": "2025 forecast in source; outcome not validated",
    },
    10: {
        "topic": "competition_concentration",
        "title": {"zh": "竞争集中度", "en": "Competitive concentration"},
        "conclusion": {
            "zh": "成熟品牌长期占据主要份额，竞争重点不只是产品参数，还包括经销网络、融资、租赁和残值体系。",
            "en": "Established brands retain the majority of the market, so competition extends beyond specifications to dealer coverage, finance, rental support and residual-value systems.",
        },
        "status": "historical_market_fact",
        "as_of_date": "2021-2024 series in source",
    },
    11: {
        "topic": "product_structure",
        "title": {"zh": "吨级结构与需求重心", "en": "Tonnage mix and demand center"},
        "conclusion": {
            "zh": "微小挖受城市更新、基础设施和租赁需求支撑，仍是北美数量主力；中挖约占特定项目需求，结构相对稳定。",
            "en": "Mini and compact excavators remain the volume center, supported by urban renewal, infrastructure and rental demand, while mid-size excavators serve more specific projects with a relatively stable share.",
        },
        "status": "historical_market_assessment",
        "as_of_date": "Five-year EDA series cited in source",
    },
    12: {
        "topic": "brand_share",
        "title": {"zh": "品牌份额与XCMG位置", "en": "Brand share and XCMG position"},
        "conclusion": {
            "zh": "资料显示2025年0-10吨前十品牌合计91%，10吨以上前十品牌合计94%；XCMG分别列第19和第18，结论应作为历史快照。",
            "en": "The source reports that the 2025 top ten held 91% of the 0-10 t segment and 94% above 10 t, with XCMG ranked 19th and 18th respectively. These figures are treated as a historical snapshot.",
        },
        "status": "historical_market_snapshot",
        "as_of_date": "2025 EDA snapshot in source",
    },
    13: {
        "topic": "benchmark_kubota",
        "title": {"zh": "微小挖战略标杆：久保田", "en": "Mini-excavator strategic benchmark: Kubota"},
        "conclusion": {
            "zh": "资料选择久保田作为微小挖标杆，重点不是复制单一参数，而是学习液压调校、可靠性、残值、客户路径和产品平台化。",
            "en": "The source selects Kubota as the mini-excavator benchmark, focusing not on one specification but on hydraulic tuning, reliability, residual value, customer journey and platform strategy.",
        },
        "status": "historical_benchmark_rationale",
        "as_of_date": "PPT 11.14 version",
    },
    14: {
        "topic": "benchmark_caterpillar",
        "title": {"zh": "中大挖战略标杆：卡特彼勒", "en": "Mid/large-excavator strategic benchmark: Caterpillar"},
        "conclusion": {
            "zh": "资料选择卡特作为中大挖标杆，评价维度延伸到可靠性、全生命周期成本、金融、服务、备件和残值闭环。",
            "en": "The source selects Caterpillar as the mid/large-excavator benchmark, extending the evaluation to reliability, lifecycle cost, finance, service, parts support and residual-value management.",
        },
        "status": "historical_benchmark_rationale",
        "as_of_date": "PPT 11.14 version",
    },
    15: {
        "topic": "core_tonnages",
        "title": {"zh": "核心吨级与产品组合", "en": "Core tonnage classes and portfolio structure"},
        "conclusion": {
            "zh": "资料按微挖、小挖、中挖和大挖识别主销吨级，并提示不同吨级降幅差异；该结构适合决定对标优先级，但销量需按最新AEM/EDA更新。",
            "en": "The source identifies core tonnage classes across mini, compact, mid-size and large excavators and highlights different decline rates. The structure can guide benchmarking priority, but volumes require current AEM/EDA refresh.",
        },
        "status": "historical_market_structure",
        "as_of_date": "AEM data cited in source",
    },
}


def slide_paragraphs(archive: zipfile.ZipFile, slide: int) -> list[str]:
    root = ET.fromstring(archive.read(f"ppt/slides/slide{slide}.xml"))
    paragraphs = []
    for paragraph in root.findall(".//a:p", NS):
        value = "".join(node.text or "" for node in paragraph.findall(".//a:t", NS)).strip()
        value = re.sub(r"\s+", " ", value)
        if value:
            paragraphs.append(value)
    return paragraphs


def build_registry(source: Path) -> dict:
    records = []
    with zipfile.ZipFile(source) as archive:
        for slide, meta in SLIDE_META.items():
            paragraphs = slide_paragraphs(archive, slide)
            records.append(
                {
                    "id": f"ppt-excavator-s{slide}",
                    "scope": "excavator_overview",
                    "tonnage": "all",
                    "model": None,
                    "competitor": None,
                    "scenario": "category_analysis",
                    "metric": meta["topic"],
                    "title": meta["title"],
                    "conclusion": meta["conclusion"],
                    "source_slide": slide,
                    "source_type": "XCMG ARC internal presentation",
                    "as_of_date": meta["as_of_date"],
                    "status": meta["status"],
                    "validation_status": "source_mapped_current_external_data_not_revalidated",
                    "thumbnail": f"assets/slides/slide-{slide}.png",
                    "zh": {"paragraphs": paragraphs, "raw_text": "\n".join(paragraphs)},
                    "en": {"source_note": "Original Chinese wording is retained in the evidence drawer."},
                }
            )
    return {
        "meta": {
            "classification": "XCMG ARC INTERNAL",
            "source_file": source.name,
            "scope": "cross-tonnage excavator analysis",
            "source_slides": [3, 15],
            "slide_count": len(records),
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
    args.output.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(registry['records'])} overview records to {args.output}")


if __name__ == "__main__":
    main()
