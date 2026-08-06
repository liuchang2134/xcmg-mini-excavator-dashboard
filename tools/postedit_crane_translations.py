from __future__ import annotations

import argparse
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "crane-ppt-insights" / "translations.en.json"
OUTPUT = ROOT / "data" / "crane-ppt-insights" / "translations.en.reviewed.json"
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen3:1.7b"
FALLBACK_MODEL = "qwen3:4b"
LAST_RESORT_MODEL = "qwen3:8b"
HAN = re.compile(r"[\u3400-\u9fff]")
NUMBER = re.compile(r"\d+(?:\.\d+)?")
HIGH_RISK = re.compile(
    r"boom trick|boom trock|competor|competator|competent\b|i'm sorry|"
    r"i don.?t know|nothing wrong with you|outsider|replay goldbox|call the police|"
    r"counterwater|counterlight|driver.?s room|muddled|unrigger|\btort\b|appetizer|"
    r"relibr|telecop|wirre|xcmg[a-z]|tadano[a-z]|upperstrut|\bhanger\b|hang\.$",
    re.IGNORECASE,
)

SOURCE_TERMS = {
    "通用底盘起重机": "boom truck",
    "越野轮胎起重机": "rough-terrain crane",
    "全地面起重机": "all-terrain crane",
    "履带起重机": "crawler crane",
    "主臂": "main boom",
    "基本臂": "base boom",
    "副臂": "jib",
    "支腿": "outrigger",
    "配重": "counterweight",
    "卷扬": "winch",
    "钢丝绳": "wire rope",
    "行走减速机": "travel reduction gearbox",
}

TEXT_REPLACEMENTS = {
    "boom trick": "boom truck",
    "boom trock": "boom truck",
    "boomtt": "boom truck",
    "general-purpose undercarriage crane": "boom truck",
    "general chassis crane": "boom truck",
    "generic chassis crane": "boom truck",
    "universal chassis crane": "boom truck",
    "general chassis": "boom-truck chassis",
    "generic chassis": "boom-truck chassis",
    "universal chassis": "boom-truck chassis",
    "cross-country tyre crane": "rough-terrain crane",
    "cross-country tire crane": "rough-terrain crane",
    "ground-wide crane": "all-terrain crane",
    "ground-wide": "all-terrain",
    "full-truck crane": "all-terrain crane",
    "main arm": "main boom",
    "secondary arm": "jib",
    "walking reducer": "travel reduction gearbox",
    "replay goldbox": "reduction gearbox",
    "driver's room": "operator cab",
    "driver ’ s room": "operator cab",
    "counterwater": "counterweight",
    "counterlight": "counterweight",
    "book block": "hook block",
    "unrigger": "outrigger",
    "humanization": "operator ergonomics",
    "humanized": "ergonomic",
    "relibrity": "reliability",
    "relibility": "reliability",
    "telecoping": "telescoping",
    "wirre rope": "wire rope",
    "value of sex": "value for money",
    "compitor": "competitor",
    "competor": "competitor",
    "competator": "competitor",
    "competitorss": "competitors",
}


MANUAL_OVERRIDES = {
    "否": "No",
    "是": "Yes",
    "宽": "Width",
    "长": "Length",
    "高": "Height",
    "无": "None",
    "主臂": "Main boom",
    "主臂+副臂": "Main boom + jib",
    "副臂": "Jib",
    "基本臂": "Base boom",
    "支腿": "Outriggers",
    "配重": "Counterweight",
    "钢丝绳": "Wire rope",
    "舒适性": "Operator comfort",
    "操控性": "Controllability",
    "维修性": "Serviceability",
    "可靠性": "Reliability",
    "安全性": "Safety",
    "经济性": "Economy",
    "液控": "Hydraulic controls",
    "电控": "Electronic controls",
    "转速": "Rotational speed",
    "轴荷": "Axle load",
    "配置": "Configuration",
    "板块": "Product segment",
    "论证": "Validation",
    "全地面": "All-terrain",
    "操纵室": "Operator cab",
    "自拆装": "Self-assembly",
    "人机交互": "Human-machine interface",
    "软文资料": "Sales literature",
    "主臂旁弯": "Main boom lateral deflection",
    "工况满足性分析": "Work-condition fit assessment",
    "是否通用场景": "Common application",
    "施工场景": "Jobsite application",
    "施工场景工况描述": "Application details",
    "施工场景工况描述\n(波士顿、普罗维登斯等)": "Application details\n(Boston, Providence, etc.)",
    "施工场景工况描述\n(纽约、费城、新泽西)": "Application details\n(New York City, Philadelphia, New Jersey)",
    "12*8驱动": "12x8 drive",
    "8*6驱动": "8x6 drive",
    "2种驱动模式": "Two drive modes",
    "1.1m宽体司机室，集作业工况自动规划、故障自诊断等功能于一体": (
        "1.1 m wide operator cab integrating automated lift planning, fault self-diagnostics and related functions"
    ),
    "G1平台\n5节绳排主臂\n美康Tier 4F发动机\n4种转向模式\n2种驱动模式\nH型支腿": (
        "G1 platform\n5-section synchronized main boom\nCummins Tier 4 Final engine\n"
        "Four steering modes\nTwo drive modes\nH-pattern outriggers"
    ),
    "G2平台\n6节50m主臂\n康明斯发动机\n液压单发\n全轮转向\n8*6驱动\nH型支腿": (
        "G2 platform\n6-section, 50 m main boom\nCummins engine\nSingle-engine hydraulic system\n"
        "All-wheel steering\n8x6 drive\nH-pattern outriggers"
    ),
    "G2平台\n6节主臂\n奔驰发动机\n液压单发\n全轮转向\n8*6驱动\nH型支腿": (
        "G2 platform\n6-section main boom\nMercedes-Benz engine\nSingle-engine hydraulic system\n"
        "All-wheel steering\n8x6 drive\nH-pattern outriggers"
    ),
    "G2平台\n7节主臂\n奔驰发动机\n液压单发\n全轮转向\n12*8驱动\nH型支腿": (
        "G2 platform\n7-section main boom\nMercedes-Benz engine\nSingle-engine hydraulic system\n"
        "All-wheel steering\n12x8 drive\nH-pattern outriggers"
    ),
    "① 吊装精度高，控制细腻\n② 作业环境严苛，设备耐久性要求强": (
        "1. High lifting accuracy and precise control\n2. Severe operating environments require strong equipment durability"
    ),
    "① 环境复杂，需支腿灵活布置\n② 吊装跨度大、设备稳定性要求高": (
        "1. Complex jobsites require flexible outrigger configurations\n"
        "2. Long-radius lifts require high machine stability"
    ),
    "① 空间受限，对整车尺寸要求高；\n② 要求高空吊装稳定；\n③ 操作简单便于非职业司机操作。": (
        "1. Confined jobsites place strict limits on machine dimensions\n"
        "2. Stable lifting performance is required at height\n"
        "3. Controls must be straightforward for occasional operators"
    ),
    "① 高温高尘环境适应性强\n② 吊装周期集中，对转场便捷性要求高。": (
        "1. Strong adaptability to hot, dusty environments\n"
        "2. Concentrated lifting schedules require efficient jobsite relocation"
    ),
    "①在树木吊装工况中，需求无线遥控功能、要求臂外无测长电缆等容易被树木刮坏的部件；\n②在进行树干吊装时，经常需要回转对枝干进行转移作业，要求回转操控平顺性，此外作业空间经常受限。": (
        "1. Tree-service work requires wireless remote control and protection of exposed components, "
        "such as external boom-length cables, from branches\n"
        "2. Moving trunks and limbs requires smooth swing control, often within restricted operating space"
    ),
    "①在树木吊装工况中，需求无线遥控功能、要求臂外无测长电缆等容易被树木刮坏的部件；\n②进行树干吊装时，经常需要回转对枝干进行转移作业，要求回转操控精准。": (
        "1. Tree-service work requires wireless remote control and protection of exposed components, "
        "such as external boom-length cables, from branches\n"
        "2. Moving trunks and limbs requires precise swing control"
    ),
    "①路面条件差，需要车辆有良好的越野能力和爬坡能力。\n②要求高空吊装稳定；\n③操作简单便于非职业司机操作。": (
        "1. Poor road conditions require strong off-road mobility and gradeability\n"
        "2. Stable lifting performance is required at height\n"
        "3. Controls must be straightforward for occasional operators"
    ),
    "【机会】起重机客户对智能化、互联化设备的需求是未来市场的关键驱动力，在未来作业场景下3D模拟重机吊装工况、远程监控和诊断是必然。\n【机会】物联网促进服务升级：远程监测、预测性维护等功能提高设备运营效率，增强客户粘性。": (
        "Opportunity: Demand for intelligent, connected cranes is a major market driver. 3D lift simulation, "
        "remote monitoring and remote diagnostics are expected to become standard capabilities.\n"
        "Opportunity: IoT-enabled remote monitoring and predictive maintenance can improve fleet uptime "
        "and strengthen long-term customer relationships."
    ),
    "作业工况可以覆盖，已完成重点提升项：陡坡路况的轮胎离地间隙。": (
        "The application is covered. Tire ground clearance on steep approaches has been improved."
    ),
    "作业工况可满足，但可以增加可变支撑功能满足部分客户需求\n①部分场地环境复杂，如有可变支撑，可进一步拓展工况适应性，建议选配。\n②中短臂性能领先。\n③支脚盘0.55m×0.55m，支撑面积大，接地比压小。": (
        "The application is supported, while variable outrigger positioning would address additional customer needs.\n"
        "1. Variable outrigger spans are recommended as an option for constrained or irregular jobsites.\n"
        "2. Short- and mid-boom lifting performance is competitive.\n"
        "3. The 0.55 m x 0.55 m outrigger pads provide a large bearing area and low ground pressure."
    ),
    "作业工况可满足：\n①空调安装作业幅度15-18m,吊重3-3.5吨左右40吨起重机可满足，但到达4吨及以上需求更强的稳定性和更大吨位45吨产品。\n②适应不平整地面布置与作业。": (
        "The application is supported.\n1. A 40 t crane can cover typical HVAC lifts of 3-3.5 t at a "
        "15-18 m radius. Loads of 4 t or more require greater stability and favor a 45 t model.\n"
        "2. The crane must support setup and operation on uneven ground."
    ),
    "具有司机室于配重操控盒互锁\n力限器精度3%": (
        "Interlock between the operator cab and counterweight control station\nRated-capacity limiter accuracy: 3%"
    ),
    "具有平衡重识别功能\n无司机室与配重操控盒互锁力限器精度5%": (
        "Counterweight recognition\nNo interlock between the operator cab and counterweight control station\n"
        "Rated-capacity limiter accuracy: 5%"
    ),
    "具有平衡重识别功能\n无司机室于配重操控盒互锁\n力限器精度5%": (
        "Counterweight recognition\nNo interlock between the operator cab and counterweight control station\n"
        "Rated-capacity limiter accuracy: 5%"
    ),
    "无平衡重识别功能\n具有司机室与配重操控盒互锁力限器精度3%": (
        "No counterweight recognition\nInterlock between the operator cab and counterweight control station\n"
        "Rated-capacity limiter accuracy: 3%"
    ),
    "无平衡重识别功能\n具有司机室于配重操控盒互锁\n力限器精度3%": (
        "No counterweight recognition\nInterlock between the operator cab and counterweight control station\n"
        "Rated-capacity limiter accuracy: 3%"
    ),
    "司机室耳旁噪音在75.8dB左右，辐射噪音107.5dB": (
        "Sound pressure level at the operator's ear: approximately 75.8 dB\nRadiated sound level: 107.5 dB"
    ),
    "司机室耳旁噪音较我司产品低1-2dB\n辐射噪音高于我司3dB左右": (
        "Sound pressure level at the operator's ear is 1-2 dB lower than the XCMG product\n"
        "Radiated sound level is approximately 3 dB higher than the XCMG product"
    ),
    "司机耳旁噪音72db左右\n辐射噪音在105-108db": (
        "Sound pressure level at the operator's ear: approximately 72 dB\nRadiated sound level: 105-108 dB"
    ),
    "司机耳旁噪音74db左右\n辐射噪音在108db": (
        "Sound pressure level at the operator's ear: approximately 74 dB\nRadiated sound level: 108 dB"
    ),
    "60USt：司机室耳旁噪音在73.3dB左右，辐射噪音106dB\n75USt：司机室耳旁噪音在74.6dB左右，辐射噪音107.2dB": (
        "60 USt: sound pressure level at the operator's ear is approximately 73.3 dB; radiated sound level is 106 dB\n"
        "75 USt: sound pressure level at the operator's ear is approximately 74.6 dB; radiated sound level is 107.2 dB"
    ),
    "吊装作业工况可以满足\n①整机臂长及幅度满足使用要求;\n②双变量泵系统，单泵作业微动性好，双泵作业效率高;\n③整机操作简单，用户提出增加座椅先导,进一步简化操作。": (
        "The lifting application is supported.\n1. Boom length and working radius meet the application requirements.\n"
        "2. The dual-variable-pump system provides precise single-pump control and efficient dual-pump operation.\n"
        "3. Controls are straightforward; the customer requested seat-mounted pilot controls for further simplification."
    ),
    "吊装作业工况可以满足，①徐工起重能力更高，\n②整机产品微动性较好,吊装平稳。\n③产品的伸缩效率/变幅效率及整机综合效率优于竞品,整体效率较高。": (
        "The lifting application is supported.\n1. XCMG provides higher lifting capacity.\n"
        "2. Fine-control performance is good and lifts remain stable.\n"
        "3. Telescoping, luffing and overall operating efficiency exceed the benchmark product."
    ),
    "吊装作业工况可以满足，①微动性好，整体尺寸适合大臂长,大载荷作业。": (
        "The lifting application is supported. Fine-control performance is good, and the machine dimensions "
        "suit long-boom, high-capacity work."
    ),
    "吊装作业工况可以满足，但需提升大幅度作业性能①具有0度性能；\n②双变量泵系统，单泵作业微动性好，双泵作业效率高。": (
        "The application is supported, but long-radius lifting performance requires improvement.\n"
        "1. Provide a 0-degree boom-angle load chart.\n"
        "2. The dual-variable-pump system provides precise single-pump control and efficient dual-pump operation."
    ),
    "吊装作业工况可以满足，徐工起重能力更高，\n①U型起重臂相比竞品4边型吊装更平稳，晃动小。\n②整机重量和轴荷＜9t,总重小于24吨，满足当地道路许可限制。": (
        "The lifting application is supported, and XCMG provides higher lifting capacity.\n"
        "1. The U-shaped boom is more stable and exhibits less lateral movement than the benchmark four-plate boom.\n"
        "2. Axle loads are below 9 t and gross vehicle weight is below 24 t, meeting local road-permit limits."
    ),
    "吊装作业工况可以满足，徐工起重能力更高，\n①起重性能领先行业竞品②四种转向模式，行业最小转弯半径，一键转向模式切换，机动灵活。": (
        "The lifting application is supported, and XCMG provides higher lifting capacity.\n"
        "1. Lifting performance exceeds the benchmark product.\n"
        "2. Four steering modes, a class-leading minimum turning radius and one-touch mode selection improve mobility."
    ),
    "吊装钢箱梁、桥面模块或预制构件，单件重40–70吨，吊高20–30米，常见于铁路、公路或城市立交桥改建项目中。": (
        "Steel box girders, bridge-deck modules and precast components typically weigh 40-70 t and are lifted "
        "20-30 m during railway, highway and urban interchange reconstruction."
    ),
    "城市商业区、工厂园区屋顶设备吊装，需道路封闭与高空精准定位，常见操作高度20–30米": (
        "Rooftop-equipment lifts in commercial districts and industrial parks typically require road closures "
        "and precise placement at working heights of 20-30 m."
    ),
    "基础设施改造（电力、暖通：用于城市架设电缆或暖通设备更新等施工场景，常见吊高25–35米，吊重10–15吨，狭窄街道作业比较多。": (
        "Infrastructure renewal includes urban cable installation and HVAC replacement. Typical lifts are "
        "10-15 t at heights of 25-35 m, often on narrow streets."
    ),
    "基础设施维护：很多基础设施老旧，有较多的历史建筑，需要对各类建筑外立面、基础设施进行吊装、维护保养作业。\n典型工况：作业高度25m以内，吊重很轻1吨以内。": (
        "Aging infrastructure and historic buildings create demand for facade and infrastructure maintenance.\n"
        "Typical application: working height below 25 m and load below 1 t."
    ),
    "工况可满足，但需提升项：\n①配置臂内测长+无线高度限位器，满足树木吊装工况需求，但应提升无高限抗干扰能力。配置回转比例制动功能满足吊装树木操控平顺性要求。\n②支腿允许不同跨距组合，适配空间受限区域作业。": (
        "The application is supported, with the following improvements required.\n"
        "1. Use internal boom-length sensing and a wireless anti-two-block device for tree-service work; improve "
        "wireless signal immunity and add proportional swing braking for smoother load control.\n"
        "2. Provide multiple outrigger-span combinations for confined jobsites."
    ),
    "平衡重前位，转弯半径更小，平衡重后位，起重性能更高。智能适应各种工况需求，尤其满足狭小空间作业需求。": (
        "A forward counterweight position reduces turning radius, while a rearward position increases lifting "
        "performance. Automatic positioning supports different applications, particularly confined jobsites."
    ),
    "建筑施工包括城市高层建筑、以及农场等、城市高层主要是空调吊装、屋顶外立面修整等；农场主要是粮仓、仓库施工等，\n在农场或者高层建筑作业时，需求250英尺以上高度，需要300吨以上产品": (
        "Construction applications include high-rise HVAC installation and rooftop facade work, plus farm grain-silo "
        "and warehouse construction. Work above 250 ft on farms or high-rise buildings requires cranes above 300 t."
    ),
    "臂头连接：通过螺纹丝杠轴连接，使用电动扳手转动丝杠轴，实现销轴插拔。": (
        "Boom-head connection: a threaded lead screw is rotated with an electric wrench to insert or remove the pin."
    ),
    "现有产品": "Current products",
    "新品": "New products",
    "高层建筑维护：通常为载人作业，进行高层外立面维护、设备安装等。": (
        "High-rise building maintenance typically involves personnel lifting for facade work and equipment installation."
    ),
    "高空空调设备安装与更换：\n适用于商场屋顶的大型HVAC系统吊装与更换，吊重5–15吨，作业高度一般为20–35米，常在城市商业区、空间受限区域作业": (
        "Installation and replacement of rooftop HVAC equipment:\nLarge HVAC systems on shopping-center roofs typically "
        "involve 5-15 t loads at working heights of 20-35 m in urban, space-constrained locations."
    ),
    "支车收车": "Outrigger setup and retraction",
    "通用底盘": "Boom truck",
    "通用底盘起重机": "Boom truck",
    "越野轮胎起重机": "Rough-terrain crane",
    "全地面起重机": "All-terrain crane",
    "履带起重机": "Crawler crane",
    "16万N.m行走减速机": "160,000 N.m travel reduction gearbox",
    "人性化及外观": "Operator ergonomics and exterior quality",
    "徐工越野轮胎起重机与标杆竞品相比，市场主销机型4款，市场覆盖率到75%；": (
        "Compared with the benchmark competitor, XCMG has four major rough-terrain crane models "
        "on the market, covering 75% of the target range."
    ),
    "徐工口碑：\n徐工越野轮胎起重机性能很高，功能配置很多用着不错，但是小毛病有点多，有时候我很无语。\n品牌2口碑：格鲁夫产品整体可靠性较好。": (
        "XCMG customer feedback: XCMG rough-terrain cranes deliver strong performance and a useful "
        "feature set, but recurring minor faults can be frustrating.\nBenchmark brand feedback: Grove "
        "products generally provide good overall reliability."
    ),
    "对比结论：\n1、结合对适应性和核心竞争力对比分析，徐工越野轮胎起重机在整机作业性能、功能配置等方面相较竞品有优势，但考虑徐工起重机在高端市场突破初期，同时考虑中小吨位产品利润空间，确定产品定位为低于行业标杆5%以内；\n2、结合竞争力优势分析，2025年该产品段的市场目标为产品销量突破。": (
        "Comparison conclusion:\n1. XCMG rough-terrain cranes have advantages in machine performance and "
        "equipment content. Considering the early stage of XCMG's entry into the premium market and "
        "the margin available in small and mid-size classes, the proposed price position was within "
        "5% below the industry benchmark.\n2. Based on these competitive strengths, the 2025 plan called "
        "for a sales breakthrough in this product segment."
    ),
    "对比结论：\n1、结合对适应性和核心竞争力对比分析，徐工越野轮胎起重机在整机作业性能、功能配置等方面相较竞品有优势，但考虑徐工起重机在高端市场突破初期，同时考虑中小吨位产品利润空间，确定产品定位为低于行业标杆5%以内；\n2、结合竞争力优势分析，2025年该产品段的市场目标为销量达到4台以上，相比2024年销售收入翻倍。": (
        "Comparison conclusion:\n1. XCMG rough-terrain cranes have advantages in machine performance and "
        "equipment content. Considering the early stage of XCMG's entry into the premium market and "
        "the margin available in small and mid-size classes, the proposed price position was within "
        "5% below the industry benchmark.\n2. Based on these competitive strengths, the 2025 plan targeted "
        "sales of more than four units and twice the 2024 sales revenue."
    ),
    "对比结论：\n1、结合对适应性和核心竞争力对比分析，徐工越野轮胎起重机在整机作业性能、功能配置等方面相较竞品有优势，但考虑徐工起重机在高端市场突破初期，产品在适应性、可靠性与标杆竞争上还需一定提升周期，确定产品定位为低于行业标杆10%；\n2、结合竞争力优势分析，2025年该产品段的市场目标为销量达到4台以上，相比2024年销售收入翻倍。": (
        "Comparison conclusion:\n1. XCMG rough-terrain cranes have advantages in machine performance and "
        "equipment content. Because XCMG remains in the early stage of entering the premium market, "
        "additional development time is required to close benchmark gaps in adaptability and reliability. "
        "The proposed price position was 10% below the industry benchmark.\n2. Based on these competitive "
        "strengths, the 2025 plan targeted sales of more than four units and twice the 2024 sales revenue."
    ),
    "主系统采用电控系统，速度精准，操作灵敏，微动性好，可实现多动作的复合操作。": (
        "The main hydraulic system uses electro-hydraulic controls for precise speeds, "
        "responsive operation, fine metering and smooth combined functions."
    ),
}


MANUAL_OVERRIDES.update({
    "对手主推130吨级\n布局1款\nXCR130_U\n覆盖竞品120-130吨": (
        "Benchmark focus: 130-USt class\nOne model planned\nXCR130_U\nCovers the 120-130 USt benchmark range"
    ),
    "布局110USt履带吊，2026年二季度完成先导样机发运，2027年具备批量上市条件\n其他产品包括300吨级桁架臂履带吊、160吨级伸缩臂履带吊根据论证情况开展，暂不列入型谱。": (
        "Plan a 110-USt crawler crane, with pilot-unit shipment scheduled for Q2 2026 and volume-market readiness targeted for 2027.\nA 300-USt lattice-boom crawler crane and a 160-USt telescopic crawler crane remain subject to business-case validation and are not yet included in the formal portfolio."
    ),
    "布局1款\n论证开发165美吨": "One model planned\n165-USt development under evaluation",
    "徐工布局1款\n350吨换代": "One XCMG model planned\n350-USt replacement generation",
    "布局165吨级越野吊\n研发目的：覆盖日益增长的大吨位越野吊需求，与XCR130_U组合抢占大吨位越野吊市场；\n初步方案：3桥6节臂，最大臂长64m，在现有XCR150基础上，根据北美标准、环境特点、客户偏好等进行适应性设计；\n售价目标：徐工销售当地建议价格94万美元；\n完成时间：2027年完成市场导入，具备上市状态。": (
        "Plan one 165-USt rough-terrain crane.\nDevelopment objective: address growing demand for high-capacity rough-terrain cranes and pair with XCR130_U in the upper-capacity segment.\nPreliminary concept: three-axle carrier, six-section boom and 64 m maximum boom length, adapted from XCR150 for North American standards, environmental conditions and customer preferences.\nTarget local suggested price: USD 940,000.\nTiming: target market introduction and commercial readiness in 2027."
    ),
    "越野轮胎起重机。": "Rough-terrain crane segment.",
    "0-16.9吨占比4.2%，17-24.9吨市场占比3.6%，25-34.9吨市场占比7.6%，35-39.9吨占比2.3%，40-49.9占比0.7%。": (
        "The 0-16.9 USt class represents 4.2% of the market; 17-24.9 USt, 3.6%; 25-34.9 USt, 7.6%; 35-39.9 USt, 2.3%; and 40-49.9 USt, 0.7%."
    ),
    "XCR60_U；占12.2%；布局1款；XCR130_U；占比18.0%；XCR75_U；占28%；XCR100_U；占5.1%；论证165美吨。": (
        "Current portfolio positions: XCR60_U at 12.2% share; XCR75_U at 18.0%; XCR100_U at 28%; XCR130_U at 5.1%. A 165-USt model remains under evaluation."
    ),
    "越野轮胎起重机占起重机产品线销量34.1%，主流吨级包括60吨、75吨、100吨、130吨，主需求吨级主要集中在50吨以上。": (
        "Rough-terrain cranes account for 34.1% of crane product-line sales. The primary classes are 60, 75, 100 and 130 USt, with most demand concentrated above 50 USt."
    ),
    "0-16.9吨占比4.2%，17-24.9吨市场占比3.6%，25-34.9吨市场占比7.6%，35-39.9吨占比2.3%，40-49.9占比0.7%。\n50吨以下市场整体占比在18.4%，但需求分散，各吨级占比小，储备50美吨，根据市场需求推进。": (
        "The 0-16.9 USt class represents 4.2% of the market; 17-24.9 USt, 3.6%; 25-34.9 USt, 7.6%; 35-39.9 USt, 2.3%; and 40-49.9 USt, 0.7%.\nClasses below 50 USt account for 18.4% in total, but demand is fragmented. Retain a 50-USt concept and advance it only as market demand develops."
    ),
    "50吨以下市场整体占比在18.4%，但需求分散，各吨级占比小，储备50美吨，根据市场需求推进。": (
        "Classes below 50 USt account for 18.4% in total, but demand is fragmented. Retain a 50-USt concept and advance it only as market demand develops."
    ),
    "全地面起重机占起重机产品线销量19.2%，主流吨级包括60吨、110吨、150吨、275吨、300吨，主需求110吨以上产品，400吨及以上大吨位产品专项分析(专项报告)，重点论证美国中部风电市场、大型基建等施工需求。": (
        "All-terrain cranes account for 19.2% of crane product-line sales. Primary classes are 60, 110, 150, 275 and 300 USt, with most demand above 110 USt. Cranes at 400 USt and above require a separate business case focused on central U.S. wind-energy and major-infrastructure demand."
    ),
    "占12.2%\n布局1款\nXCR130_U": "12.2% share\nOne model planned\nXCR130_U",
    "占28%\n布局1款\nXCR100_U": "28% share\nOne model planned\nXCR100_U",
    "占比18.0%\n布局1款\nXCR75_U": "18.0% share\nOne model planned\nXCR75_U",
    "占比27.3%\n布局1款\nXGC110U": "27.3% share\nOne model planned\nXGC110U",
    "占比7.9%\n布局1款\nXCA350_U": "7.9% share\nOne model planned\nXCA350_U",
    "布局1款": "One model planned",
    "布局1款机型": "One model planned",
    "布局165吨级越野吊": "Plan one 165-USt rough-terrain crane",
    "覆盖竞品主推LTM1130-5.1\n徐工布局1款\nXCA150_U": (
        "Covers the competitor's core LTM1130-5.1 position\nOne XCMG model planned\nXCA150_U"
    ),
    "作业工况可部分满足：\n①根据住宅吊装工况适配设计，提升大幅度吊装能力，性能覆盖竞品15%；\n②作业幅度30-32m时，40吨可满足，超过32m不再满足，需求更高稳定性能或45吨及以上产品。\n②首创无线臂头影像装置，运用无线信号传输，解决客户跨建筑吊装痛点需求。": (
        "The application is partially supported.\n1. Residential-lifting optimization improves long-radius capacity, with stated performance 15% above the benchmark.\n2. A 40 t crane can cover working radii of 30-32 m; beyond 32 m, greater stability or a 45 t-and-above model is required.\n3. A wireless boom-tip camera supports blind lifts over buildings without an exposed signal cable."
    ),
    "增加平衡重安装回转指示器，方便在操纵室挂接平衡重时确定配重挂接位置。": (
        "Add a counterweight-installation swing indicator so the operator can align the counterweight attachment point from the cab."
    ),
    "徐工型号XCA275_U客户使用评价对标：竞品可靠性上总体优于徐工产品，竞品优势主要在无故障工作时长优于徐工，其它稳定性等设计参数相当。\n劣势主要包括全伸臂缩臂晃动、全伸臂旁弯、力限器重量显示不准，回转比例制动效果不佳": (
        "XCA275_U customer evaluation: the benchmark product provides better overall reliability, principally longer fault-free operating time; stability and other design parameters are comparable.\nPrimary XCMG gaps are boom oscillation during retraction from full extension, lateral boom deflection at full extension, inaccurate displayed load and inadequate proportional swing braking."
    ),
    "徐工型号XCR130_U客户使用评价对标：竞品整体表现稳定，相比徐工优势包括回转平顺性好、场地适应性强。劣势主要包括全伸臂缩臂晃动、全伸臂旁弯、力限器重量显示不准。": (
        "XCR130_U customer evaluation: the benchmark product is stable overall and leads XCMG in swing smoothness and jobsite adaptability. XCMG gaps are boom oscillation during retraction from full extension, lateral boom deflection at full extension and inaccurate displayed load."
    ),
    "徐工型号XCR130_U客户使用评价对标：竞品整体表现稳定，相比徐工优势包括驾乘空间大、回转平顺性好、支车速度快、场地适应性强。": (
        "XCR130_U customer evaluation: the benchmark product is stable overall and leads XCMG in cab space, swing smoothness, outrigger setup speed and jobsite adaptability."
    ),
    "徐工型号XCR130_U客户使用评价对标：竞品整体表现稳定，相比徐工优势包括驾乘空间大、回转平顺性好、支车速度快、场地适应性强。\n劣势主要包括全伸臂缩臂晃动、全伸臂旁弯、力限器重量显示不准，回转比例制动效果不佳。": (
        "XCR130_U customer evaluation: the benchmark product is stable overall and leads XCMG in cab space, swing smoothness, outrigger setup speed and jobsite adaptability.\nXCMG gaps are boom oscillation during retraction from full extension, lateral boom deflection at full extension, inaccurate displayed load and inadequate proportional swing braking."
    ),
    "徐工型号XCT35_U客户使用评价对标：竞品整体表现稳定，相比徐工优势包括驾乘空间大、回转平顺性好、支车速度快、场地适应性强。": (
        "XCT35_U customer evaluation: the benchmark product is stable overall and leads XCMG in cab space, swing smoothness, outrigger setup speed and jobsite adaptability."
    ),
    "徐工型号XCT35_U客户使用评价对标：竞品整体表现稳定，相比徐工优势包括驾乘空间大、回转平顺性好、支车速度快、场地适应性强。\n劣势主要包括全伸臂缩臂晃动、全伸臂旁弯、力限器重量显示不准，回转比例制动效果不佳": (
        "XCT35_U customer evaluation: the benchmark product is stable overall and leads XCMG in cab space, swing smoothness, outrigger setup speed and jobsite adaptability.\nXCMG gaps are boom oscillation during retraction from full extension, lateral boom deflection at full extension, inaccurate displayed load and inadequate proportional swing braking."
    ),
    "徐工型号XCT35_U客户使用评价对标：竞品整体表现稳定，相比徐工优势包括驾乘空间大、回转平顺性好、支车速度快、场地适应性强。\n劣势主要包括全伸臂缩臂晃动、全伸臂旁弯、力限器重量显示不准，回转比例制动效果不佳。": (
        "XCT35_U customer evaluation: the benchmark product is stable overall and leads XCMG in cab space, swing smoothness, outrigger setup speed and jobsite adaptability.\nXCMG gaps are boom oscillation during retraction from full extension, lateral boom deflection at full extension, inaccurate displayed load and inadequate proportional swing braking."
    ),
    "徐工型号XCT40_U客户使用评价对标：竞品整体表现稳定，相比徐工优势包括驾乘空间大、回转平顺性好、支车速度快、场地适应性强。": (
        "XCT40_U customer evaluation: the benchmark product is stable overall and leads XCMG in cab space, swing smoothness, outrigger setup speed and jobsite adaptability."
    ),
    "徐工型号XCT40_U客户使用评价对标：竞品整体表现稳定，相比徐工优势包括驾乘空间大、回转平顺性好、支车速度快、场地适应性强。\n劣势主要包括全伸臂缩臂晃动、全伸臂旁弯、力限器重量显示不准，回转比例制动效果不佳.": (
        "XCT40_U customer evaluation: the benchmark product is stable overall and leads XCMG in cab space, swing smoothness, outrigger setup speed and jobsite adaptability.\nXCMG gaps are boom oscillation during retraction from full extension, lateral boom deflection at full extension, inaccurate displayed load and inadequate proportional swing braking."
    ),
    "徐工型号XCT60_U客户使用评价对标：竞品整体表现稳定，相比徐工优势包括驾乘空间大、回转平顺性好、支车速度快、场地适应性强。\n劣势主要包括全伸臂缩臂晃动、全伸臂旁弯、力限器重量显示不准，回转比例制动效果不佳": (
        "XCT60_U customer evaluation: the benchmark product is stable overall and leads XCMG in cab space, swing smoothness, outrigger setup speed and jobsite adaptability.\nXCMG gaps are boom oscillation during retraction from full extension, lateral boom deflection at full extension, inaccurate displayed load and inadequate proportional swing braking."
    ),
    "桥梁铺设：在高架或匝道建设中，吊装桥梁和各类建设材料，在远距离吊装时，特别是支车位置受限时，XCR75_U更具备优势。": (
        "Bridge construction: lift bridge components and building materials for elevated structures and ramps. XCR75_U is advantageous for long-radius lifts, particularly where crane setup is constrained."
    ),
    "起重性能强、设备稳定性高、支腿布置灵活，满足苛刻能源作业场地和吊装精度要求。": (
        "Strong lifting performance, high machine stability and flexible outrigger configurations meet demanding energy-sector jobsite and load-placement requirements."
    ),
    "4种支腿跨距组合，工况适应性更好": "Four outrigger-span combinations improve application flexibility",
    "XCT35_U和XCT40_U更改控制程序，允许在操纵室内通过支腿遥控进行调平。\nXCT60_U更改控制程序，在显示器界面增加支腿调平，通过触摸操作调节支腿。": (
        "For XCT35_U and XCT40_U, revise the control software to permit outrigger leveling from the cab using the remote control.\nFor XCT60_U, add touch-screen outrigger leveling to the display interface."
    ),
    "伸缩过程较为平顺，但2节臂或3-4-5到达全伸臂时无缓冲，得分3.4分": (
        "Boom telescoping is generally smooth, but no end-of-stroke cushioning is provided when section 2 or sections 3-4-5 reach full extension. Score: 3.4/5."
    ),
    "作业工况可以覆盖，\n①起重性能领先；\n②双变量泵系统，单泵作业微动性好，双泵作业效率高。": (
        "The application is covered.\n1. Lifting performance leads the benchmark.\n2. The dual-variable-pump system provides precise single-pump control and efficient dual-pump operation."
    ),
    "作业工况可以覆盖，但有需提升项次\n①具备可变位平衡重，支腿可变支撑，满足不同作业空间需求。\n②具备主臂低角度吊装能力，但是带载伸缩性能缺失；\n③ 中长臂性能覆盖安装需求。": (
        "The application is covered, with improvement items.\n1. Movable counterweight and variable outrigger positions support different setup envelopes.\n2. Low-boom-angle lifting is available, but telescoping under load is not.\n3. Mid- and long-boom performance covers installation requirements."
    ),
    "作业工况可以覆盖：\n① 底盘上路便捷，支车收车快，双泵分合流效率高，可满足多频转场。\n② 轻载高频吊装，作业工况可覆盖，同时作业高效能满足快速施工需求。": (
        "The application is covered.\n1. Road travel is convenient, outrigger setup and retraction are fast, and pump-combining efficiency supports frequent jobsite moves.\n2. High operating efficiency supports frequent light-load lifts and rapid construction cycles."
    ),
    "作业工况可满足\n①受限区域支车时，支腿允许不同跨距组合，适配空间受限区域作业。\n②双泵分合流技术，单泵作业微动性更好，双泵作业更加高效。": (
        "The application is supported.\n1. Multiple outrigger-span combinations support setup in confined areas.\n2. Pump-combining technology provides precise single-pump control and efficient dual-pump operation."
    ),
    "作业工况可满足\n①受限区域支车时，支腿允许不同跨距组合，适配空间受限区域作业。\n②在空调安装作业时，双泵分合流技术，单泵作业微动性更好，双泵作业更加高效。": (
        "The application is supported.\n1. Multiple outrigger-span combinations support setup in confined areas.\n2. For HVAC installation, pump-combining technology provides precise single-pump control and efficient dual-pump operation."
    ),
    "作业工况可满足\n①受限区域支车时，支腿支持50%跨距作业，满足一定需求，但建议增加支腿0%、75%伸出组合。\n②空调安装作业幅度15-18m,吊重3-3.5吨左右40吨起重机可满足，但到达4吨及以上需求更强的稳定性和更大吨位45吨产品。": (
        "The application is supported.\n1. A 50% outrigger span covers part of the confined-site demand; add 0% and 75% extension combinations.\n2. A 40 t crane can cover typical HVAC lifts of 3-3.5 t at a 15-18 m radius. Loads of 4 t or more require greater stability and favor a 45 t model."
    ),
    "作业工况可覆盖\n整车布局紧凑，支持多级支腿展开、狭小场地布置能力强，具备360°全覆盖吊装能力。": (
        "The application is covered. Compact dimensions, multiple outrigger-extension positions and 360-degree load charts support confined jobsites."
    ),
    "作业工况可覆盖，应提升：\n①支腿可50%跨距作业，满足一定需求，但建议增加支腿0%、75%伸出组合，以适应野外通信设施维护工况。\n②载人作业工况，操作精准性满足要求": (
        "The application is covered, with improvements required.\n1. The 50% outrigger span covers part of the demand; add 0% and 75% extension combinations for remote communications-site maintenance.\n2. Control precision meets personnel-lifting requirements."
    ),
    "作业工况覆盖广，具备下列优势：\n①整机配备可变位平衡重、支腿可变支撑，满足车间内狭窄区域作业；\n②复合动作满足工况需求，作业精准，设备就位效率高。": (
        "The crane covers a broad application range.\n1. A movable counterweight and variable outrigger positions support confined workshop operation.\n2. Smooth combined functions support precise, efficient equipment placement."
    ),
    "全伸臂主臂仰角60°，主臂位于车辆后方时，缩臂晃动较轻，约3-4下，晃动距离约1m左右": (
        "With the boom fully extended at a 60-degree angle over the rear, retracting the boom produced approximately three to four oscillations with about 1 m of movement."
    ),
    "制造厂房设备吊装与搬迁，空压机、注塑机、模具等设备频繁更换，作业环境为厂房内部或厂房门前狭小空间，对整车通过性、吊重性能、支腿展开空间要求较高。": (
        "Manufacturing-plant lifts and relocations include air compressors, injection-molding machines and dies. Work inside plants or at narrow entrances places high demands on machine access, lifting capacity and outrigger setup envelope."
    ),
    "劣势主要包括全伸臂缩臂晃动、全伸臂旁弯、力限器重量显示不准，回转比例制动效果不佳": (
        "Primary gaps are boom oscillation during retraction from full extension, lateral boom deflection at full extension, inaccurate displayed load and inadequate proportional swing braking."
    ),
    "回转制动踏板没有比例制动功能，回转停止时制动过快，造成晃动。\n建议更改控制程序，通过液压回转比例控制阀调节回转制动效果。": (
        "The swing-brake pedal does not provide proportional braking; abrupt deceleration at swing stop causes load oscillation.\nRevise the control software and tune the hydraulic proportional swing-brake valve."
    ),
    "城市道路狭窄，项目位于历史城区，常需更换屋顶结构、HVAC系统、电梯井道组件等，作业空间有限，需非对称支腿布置、精准操控。": (
        "Historic urban districts have narrow roads and confined work zones. Roof structures, HVAC systems and elevator-shaft components require asymmetric outrigger setup and precise control."
    ),
    "工程建设：包括各类厂房建设、机场等大型施工工程，用于吊装构件、建筑材料等。在远距离吊装时，特别是支车位置受限时，XCR75_U更具备优势。": (
        "Construction applications include industrial plants, airports and other large projects involving structural components and building materials. XCR75_U is advantageous for long-radius lifts, particularly where crane setup is constrained."
    ),
    "工况可满足：\n① 研发主副卷同步作业功能满足油田吊装；\n② 回转比例制动，解决客户在管路吊装时回转操控需求；\n③ 配置电动空调，空调可持续工况4小时，\n满足需求。": (
        "The application is supported.\n1. Add synchronized main- and auxiliary-winch control for oilfield lifting.\n2. Add proportional swing braking for controlled pipe handling.\n3. Provide electric air conditioning capable of four hours of continuous operation."
    ),
    "工况可满足：\n①中长臂性能优化提升，性能覆盖竞争对手5%以上。\n②275全地面配置三轴Dolly小车，满足当地上路行驶要求。": (
        "The application is supported.\n1. Optimized mid- and long-boom performance is stated to exceed the benchmark by more than 5%.\n2. The 275-USt all-terrain crane uses a three-axle boom dolly to meet local road requirements."
    ),
    "强化现有经销商管理和赋能，稳扎稳打，逐步扩大突破，寻求目标适配经销商，优先枢纽州、重点经济州进行渠道布局": (
        "Strengthen dealer management and support, expand coverage in stages and recruit dealers that fit the product line, prioritizing logistics hubs and economically important states."
    ),
    "徐工XCR100_U客户使用评价对标：徐工低温启动功能齐全，与竞品TD相当，空调制冷制热效果略优与TD。": (
        "XCR100_U customer evaluation: cold-start capability is comparable with the Tadano benchmark, while HVAC heating and cooling performance is slightly better."
    ),
    "徐工型号XCA150_U客户使用评价对标：徐工150吨全地面的安全性、人性化配置、可变位平衡重工况适应性方面上优于竞争对手，但在可靠性上、伸缩效率等方面和对手相比存在一定劣势。": (
        "XCA150_U customer evaluation: the 150-USt all-terrain crane leads the benchmark in safety, operator-oriented equipment and application flexibility from the movable counterweight, but trails in reliability and boom-telescoping efficiency."
    ),
    "徐工型号XCA275_U客户使用评价对标：竞品可靠性上总体优于徐工产品，竞品优势主要在无故障工作时长优于徐工，其它稳定性等设计参数相当。": (
        "XCA275_U customer evaluation: the benchmark product provides better overall reliability, principally longer fault-free operating time; stability and other design parameters are comparable."
    ),
    "徐工型号XCT60_U客户使用评价对标：竞品整体表现稳定，相比徐工优势包括驾乘空间大、回转平顺性好、支车速度快、场地适应性强。": (
        "XCT60_U customer evaluation: the benchmark product is stable overall and leads XCMG in cab space, swing smoothness, outrigger setup speed and jobsite adaptability."
    ),
    "徐工型号XGC110U客户使用评价对标：竞品整体表现稳定，相比徐工优势包括驾乘视野空间大、吊装作业安全性更高、主动作启停平顺性、微动性好、拆装更便利。劣势主要包括主臂作业性能及使用经济性。": (
        "XGC110U customer evaluation: the benchmark product is stable overall and leads XCMG in cab visibility and space, lifting safety, smooth main-function starts and stops, fine control and ease of assembly. Its disadvantages are main-boom lifting performance and operating economy."
    ),
    "空调与屋顶设备安装或更换：住宅、小型商业区域安装空调，吊装 3吨以内 HVAC 设备至单层或两层建筑屋顶。": (
        "HVAC and rooftop-equipment installation or replacement: lift HVAC units up to 3 t onto one- or two-story residential and small-commercial buildings."
    ),
    "空调安装：住宅、小型商业区域安装空调，吊装 3吨 以内HVAC 设备至单层或两层建筑屋顶。": (
        "HVAC installation: lift HVAC units up to 3 t onto one- or two-story residential and small-commercial buildings."
    ),
    "空调安装：住宅、小型商业区域安装空调，吊装 3吨以内 HVAC 设备至单层或两层建筑屋顶。": (
        "HVAC installation: lift HVAC units up to 3 t onto one- or two-story residential and small-commercial buildings."
    ),
    "车辆两侧各配有爬梯，同时后方布置有扶梯，配置高扶手，三点支撑相比竞品更人性化，方便爬上趴下。此外踏步错开设计，方便爬下时观察下方踏步位置。": (
        "Access ladders are provided on both sides and at the rear. High handrails maintain three points of contact and improve access compared with the benchmark. Staggered steps remain visible during descent."
    ),
    "车辆两侧各配有爬梯，后方有扶梯，高扶手配置，同时在吊臂支架处设计有长扶手，满足三点支撑，方便爬上趴下。踏步错开设计，方便爬下时观察下方踏步位置。": (
        "Access ladders are provided on both sides and at the rear. High handrails and a long handrail at the boom rest maintain three points of contact. Staggered steps remain visible during descent."
    ),
    "1轴转向，3-4驱动，2轴浮动": "First-axle steering, third- and fourth-axle drive, second floating axle",
    "4/5节绳排主臂": "4/5-section synchronized main boom",
    "6/7节单缸插销主臂": "6/7-section single-cylinder pinned main boom",
    "作业工况可以满足\n3轴底盘机动性强，4节单缸主臂能在短时间完成部署，适应路边/软土地带施工，支持多种支腿跨距组合。": (
        "The application is supported.\nThe three-axle carrier is highly maneuverable, and the four-section single-cylinder boom deploys quickly. Multiple outrigger-span combinations support roadside and soft-ground jobsites."
    ),
    "作业工况可以满足\n①受限区域支车时，支腿允许不同跨距组合，适配空间受限区域作业。\n②在空调安装作业时，双泵分合流技术，单泵作业微动性更好，双泵作业更加高效。": (
        "The application is supported.\n1. Multiple outrigger-span combinations support setup in confined areas.\n2. For HVAC installation, pump-combining technology provides precise single-pump control and efficient dual-pump operation."
    ),
    "作业工况可以满足\n①对操控精准性要求比较高，包括微动性、平顺县，重点提升操控平顺性；\n②增加全工况无线遥控，操作人员可在吊篮处遥控车辆，同时能监测车辆工况，确保作业安全。": (
        "The application is supported.\n1. The work demands precise, smooth fine control; control consistency remains the priority improvement.\n2. Full-function wireless remote control would let the operator control and monitor the crane from the personnel basket, improving operating safety."
    ),
    "作业工况可以满足\n①微动性好，整体尺寸适合主干道两侧停车位内作业。\n②具有高空操作可视性（无线臂头监控），提升广告施工能力。": (
        "The application is supported.\n1. Fine-control performance is good, and overall dimensions support work from curbside parking spaces.\n2. A wireless boom-tip camera improves visibility for elevated sign installation."
    ),
    "作业工况可以满足\n①根据住宅吊装工况进行优化和适配设计，优化提升大幅度远距离吊装能力，性能覆盖竞品15%以上；\n②首创无线臂头影像装置，运用无线信号传输，解决客户跨建筑吊装痛点需求。": (
        "The application is supported.\n1. Residential-lifting optimization improves long-radius capacity, with stated performance more than 15% above the benchmark.\n2. A wireless boom-tip camera supports blind lifts over buildings without an exposed signal cable."
    ),
    "作业工况可以满足\n可完成常规油田轻载吊装任务，整机稳定性佳。\n可选装附加平衡重，提升整机作业稳定性能，适应较大设备更远幅度吊装需求。\n整机操作简便，具有支腿无线遥控、上车操纵支腿水平等功能。": (
        "The application is supported.\nThe crane covers routine light-duty oilfield lifts with good overall stability. Optional additional counterweight increases stability for larger equipment at longer radii. Controls are straightforward and include wireless outrigger control and upper-cab outrigger leveling."
    ),
    "作业工况可以满足\n起重机臂长覆盖典型作业需求，布置紧凑适配城区狭小工位,配置臂头影像辅助吊装功能。": (
        "The application is supported.\nBoom length covers the typical work envelope, compact dimensions suit confined urban sites, and the boom-tip camera supports load placement."
    ),
    "作业工况可以满足\n适应当地环境，空调前后风道制冷、还配有风扇，适应早、中、晚班不同时段操作人员需求。": (
        "The application is supported.\nThe HVAC system provides front and rear airflow, supplemented by a fan, to support operators across day, evening and night shifts."
    ),
    "作业工况可以满足，但需提升大幅度作业性能。\n①具有0度性能。\n②双变量泵系统，单泵作业微动性好，双泵作业效率高。": (
        "The application is supported, but long-radius lifting performance requires improvement.\n1. Provide a 0-degree boom-angle load chart.\n2. The dual-variable-pump system provides precise single-pump control and efficient dual-pump operation."
    ),
    "作业工况可满足\n满足快速部署需求，设备出勤高。同时液控系统稳定可靠，频繁和连续作业能力强。": (
        "The application is supported. Rapid setup supports high utilization, while the stable hydraulic-control system supports frequent and continuous operation."
    ),
    "作业工况可满足，但需要加强盐雾环境下的耐腐蚀性能。": (
        "The application is supported, but corrosion protection requires improvement for salt-spray environments."
    ),
    "作业工况可满足：\n①整机作业稳定性能高，支腿支持50%伸出作业，满足一定需求，建议增加支腿0%、75%伸出组合；\n②适应西海岸干热环境；\n支车/收车迅速，作业效率快 。": (
        "The application is supported.\n1. Stability is strong and 50% outrigger extension covers part of the demand; add 0% and 75% extension combinations.\n2. The machine is adapted to dry, hot West Coast conditions.\n3. Fast outrigger setup and retraction improve jobsite efficiency."
    ),
    "作业工况可满足：\n①车辆通过性好，转场便捷，能快速进入老旧街区；\n②整机作业稳定性同吨位产品最强，3-4-5单独伸出作业稳定性可覆盖大部分工况。": (
        "The application is supported.\n1. Good roadability and maneuverability provide quick access to older urban neighborhoods.\n2. Class-leading stability and independent extension of outrigger beams 3, 4 and 5 cover most setup conditions."
    ),
    "作业工况可覆盖\n60吨级性能可覆盖、吊臂强度高，适合中等规模工业装配施工任务": (
        "The application is covered. The 60-USt class provides the required capacity and boom strength for medium-scale industrial assembly work."
    ),
    "作业工况可覆盖\n整机通过性强，支持快拆快装，吊臂强度高、微动性好，满足精细设备作业需求。": (
        "The application is covered. Strong jobsite mobility, rapid assembly, high boom strength and precise fine control support sensitive equipment handling."
    ),
    "作业工况可覆盖，但应从以下方面进行提升：\n①支持码头区域不规则地形部署，支腿跨距可50%伸出，但不具备0%、75%等组合工况。": (
        "The application is covered, but setup flexibility requires improvement. A 50% outrigger extension supports some irregular port terrain; 0% and 75% extension combinations are not currently available."
    ),
    "全钢结构操纵室，可调节座椅，安装有单轴操纵手柄，配有前挡风玻璃、雨刮、可开启天窗、侧面门窗防护，制冷空调和柴油加热除霜装置，内置风扇，灭火器等配置": (
        "All-steel operator cab with adjustable seat, single-axis control levers, windshield and wiper, opening roof window, guarded side windows, air conditioning, diesel heater/defroster, circulation fan and fire extinguisher"
    ),
    "具有完备的配重、臂架、履带梁自拆装功能": (
        "Complete self-assembly functions for counterweights, boom sections and crawler side frames"
    ),
    "定量/液控无级变量马达": "Fixed-displacement pump / hydraulically controlled continuously variable motor",
    "臂架长度": "Boom-system length",
    "竞品不具备副臂角度调整功能": "The benchmark product does not provide jib-offset adjustment",
    "竞品不具备副臂角度调整功能。": "The benchmark product does not provide jib-offset adjustment.",
    "高精力限器系统，重载误差在5%以内，具有系统故障提示，但整体安全性设计的完备性略低于竞品": (
        "High-accuracy rated-capacity limiter with heavy-load error within 5% and system-fault alerts; the overall safety-system implementation is slightly less comprehensive than the benchmark product"
    ),
    "1.经销商渠道开发：依托现有通用底盘起重机渠道，稳扎稳打，主攻Manitex和Grove竞品经销商、设备改装厂、中小租赁公司。\n2.现有经销商赋能：建立徐工北美经销商评价体系，定期评价优胜劣汰。以数字化手段对经销商赋能，从营销宣传、技术培训、服务支持、备件响应方面赋能强化粘性，将现有经销商培养成市场旗帜标杆。": (
        "1. Distributor development: build on the existing boom-truck channel and target Manitex and Grove dealers, equipment upfitters and small-to-mid-size rental companies.\n"
        "2. Distributor capability: establish a North American dealer evaluation system and use digital tools, marketing support, technical training, service support and parts responsiveness to improve dealer performance and retention."
    ),
    "1、徐工力限器系统满足北美ASME.B30.5同时兼顾CE安全性要求，增加多方向限动限速；\n2、力限器精度：幅度误差1-3%；吊重量误差5-6%；\n3、风速仪仅报警，不限动\n4、徐工配重盒与司机室有配重操作互锁功能\n5、有支腿跨距检测功能\n6、有回转锁止状态检测": (
        "1. The XCMG rated-capacity-limiter system addresses ASME B30.5 and CE safety requirements and adds multi-direction motion and speed limits.\n"
        "2. Limiter accuracy: radius error 1-3%; displayed-load error 5-6%.\n"
        "3. The anemometer provides a warning only and does not inhibit motion.\n"
        "4. Counterweight controls are interlocked with the operator cab.\n"
        "5. Outrigger-span detection is provided.\n"
        "6. Swing-lock status is monitored."
    ),
    "1.2025年经销商渠道州覆盖度40%，打通重点突破美东区域全地面和履带吊，美西区域越野吊\n2.2027年经销商渠道州覆盖率70%，重点发展加东等区域\n3.2030年经销商渠道州实现90%全覆盖。": (
        "1. The 2025 plan targeted distributor coverage in 40% of U.S. states, prioritizing all-terrain and crawler cranes in the East and rough-terrain cranes in the West.\n"
        "2. The 2027 plan targeted 70% state coverage, with additional focus on Eastern Canada.\n"
        "3. The 2030 plan targeted 90% state coverage."
    ),
    "1.副臂展开，穿销轴时应具有定位装置，避免反复人工调节副臂对孔\n2.副臂回收时，应具有辅助回缩装置，减少人工。": (
        "1. Provide a locating device to align the jib pin holes during deployment and eliminate repeated manual adjustment.\n"
        "2. Provide assisted jib retraction to reduce manual handling."
    ),
    "12V电气系统和底盘适配，具备工况查询，臂头影像等功能配置，智能化程度高。": (
        "The 12 V electrical architecture is integrated with the chassis and supports lift-condition lookup, boom-tip camera monitoring and related intelligent functions."
    ),
    "作业工况可以覆盖，并且优势如下：\n①目前产品可以覆盖住宅吊装工况,满足用户需求；\n②可以根据用户需求增加无线对讲机,便于视野不佳时辅助操作。": (
        "The application is covered, with the following advantages.\n"
        "1. The current product supports residential lifting requirements.\n"
        "2. A wireless intercom can be added to support spotter-to-operator communication when visibility is restricted."
    ),
    "力限器吊重时，现场吊重1800lb重物，实际总重约2200lb左右，在测试不同工况下，力限器显示值在2200lb到2600lb之间，可以看出力限器吊重显示重量同样存在一定偏差。": (
        "With an 1,800 lb test load and an actual suspended weight of approximately 2,200 lb, the rated-capacity limiter displayed 2,200-2,600 lb across the tested configurations, indicating a measurement deviation."
    ),
    "力限器吊重时，现场吊重1800lb重物，实际总重约2800lb左右，在测试不同工况下，力限器显示值在2800lb到3620lb之间，可以看出力限器吊重显示重量同样存在一定偏差。": (
        "With an 1,800 lb test load and an actual suspended weight of approximately 2,800 lb, the rated-capacity limiter displayed 2,800-3,620 lb across the tested configurations, indicating a measurement deviation."
    ),
    "力限器工况：设置有拆装工况按键，可以通过拆装工况按键进行爬臂操作。": (
        "Rated-capacity-limiter mode: a dedicated assembly/disassembly mode permits boom-climbing procedures during crane setup."
    ),
    "徐工XCR100_U客户使用评价对标：在安全性方面。相比竞品，徐工耳旁噪音略高，辐射噪音低于竞品3dB左右；徐工力限器精度高，整体安全控制逻辑优于竞品，行驶制动能力优于竞品。": (
        "XCR100_U customer evaluation - safety: operator-ear noise is slightly higher than the benchmark, while radiated noise is approximately 3 dB lower. The XCMG rated-capacity limiter is more accurate, the overall safety-control logic is stronger and road-braking performance is better than the benchmark product."
    ),
    "徐工产品可实时进行轴荷监测，实施优化车辆行驶状态，保证车辆行驶安全。且设计支腿侧长与压力检测，保证吊装作业过程中支腿安全性。": (
        "XCMG provides real-time axle-load monitoring to optimize the roading condition and support safe travel. Outrigger extension-length and pressure monitoring also support safe setup throughout lifting operations."
    ),
    "车辆处于水平状态，倾角在±0.5°以内，现场测试当力限器吊重显示达到额定起重机的98%时，车辆限动。吊臂在后方作业时，前方支腿未松动。吊臂侧方作业时，后方支腿松动。": (
        "The crane was level within +/-0.5 degrees. During the field test, motion cutout occurred when the rated-capacity limiter reached 98% of rated load. With the boom over the rear, the front outriggers remained loaded; with the boom over the side, the rear outrigger unloaded."
    ),
    "锁定机构：副臂展开后，自动锁定在主臂臂头，配合调节顶丝，实现轴孔对齐，方便丝杠轴连接。": (
        "Locking mechanism: after deployment, the jib locks automatically at the main-boom head. An adjusting screw aligns the pin holes to simplify lead-screw pin installation."
    ),
    "降低固定支腿高度，同时增加高支脚盘，提升离地间隙。": (
        "Reduce the fixed outrigger-beam height and use taller outrigger pads to increase ground clearance."
    ),
    "零散吊装，商业或厂房：各种商业、厂房、基础电力设施升级、杆塔通信设备吊装。典型工况：吊重量较轻，一般在1-2吨以内；": (
        "General lifting for commercial and industrial facilities includes power-infrastructure upgrades and utility-pole or communications-equipment installation. Typical loads are light, generally below 1-2 t."
    ),
    "要求起重机具备强爬坡能力，适应泥泞/碎石路面。": (
        "The crane requires strong gradeability and must remain mobile on muddy or gravel surfaces."
    ),
    "1.要求起重机具备强爬坡能力，适应泥泞/碎石路面。\n2.恶劣路面适应性；\n3.连续工作≥8小时不过热。": (
        "1. Strong gradeability and mobility on muddy or gravel surfaces.\n"
        "2. Adaptability to rough road conditions.\n"
        "3. At least eight hours of continuous operation without overheating."
    ),
    "①紧凑车身+多种转向模式，适应狭窄工地。\n②高精度液压控制，确保平稳落梁。": (
        "1. A compact carrier and multiple steering modes support confined jobsites.\n"
        "2. Precise hydraulic control supports smooth beam placement."
    ),
    "①紧凑车身+多种转向模式，适应狭窄，空间。\n②高精度液压控制，确保平稳吊装货物。": (
        "1. A compact carrier and multiple steering modes support confined jobsites.\n"
        "2. Precise hydraulic control supports smooth load placement."
    ),
    "①街道狭窄，需要车辆外形紧凑、多种组合跨距。\n②小幅度起重性能高，③接地比压小": (
        "1. Narrow streets require compact carrier dimensions and multiple outrigger-span combinations.\n"
        "2. Short-radius lifting performance is strong.\n"
        "3. Low ground-bearing pressure reduces jobsite impact."
    ),
    "吊装作业工况可以满足，①微动性好，安装整体安装需求。\n②中短臂起重性能领先。\n③支脚盘0.55m×0.55m，支撑面积大，接地比压小。": (
        "The lifting application is supported.\n"
        "1. Fine-control performance supports precise installation.\n"
        "2. Short- and mid-boom lifting performance is competitive.\n"
        "3. The 0.55 m x 0.55 m outrigger pads provide a large bearing area and low ground pressure."
    ),
    "徐工优于多田野共8项，劣于多田野5项，但整体均满足客户使用需求。具体如下：\n优势项：发动机、变速箱、油泵检修方便性好；空调燃油加注、空滤器滤芯更换方便好；具有压力检测口，测压方便。\n劣势项：蓄电池、传动轴检修方便性略低；发动机机油滤芯更换、变速箱机油检查、洗涤液加注方便性略低。": (
        "XCMG leads Tadano on eight serviceability items and trails on five; both products meet customer requirements overall.\n"
        "Advantages: convenient access for engine, transmission and hydraulic-pump service; convenient HVAC refrigerant filling and air-filter replacement; pressure test ports simplify diagnostics.\n"
        "Gaps: battery and driveshaft access is less convenient; engine-oil-filter replacement, transmission-oil inspection and washer-fluid filling are also less convenient."
    ),
    "G1平台\n4/5节绳排主臂\n液压先导\n肯沃斯/彼特/福莱纳底盘\nH型支腿": (
        "G1 platform\n4/5-section synchronized main boom\nHydraulic pilot controls\n"
        "Kenworth / Peterbilt / Freightliner chassis\nH-pattern outriggers"
    ),
    "G1平台\n5节主臂\n4轴底盘\n1轴转向，3-4驱动，2轴浮动\nH型支腿": (
        "G1 platform\n5-section main boom\n4-axle carrier\nFirst-axle steering, third- and fourth-axle drive, second floating axle\nH-pattern outriggers"
    ),
    "G1平台\n6/7节单缸插销主臂\n双电控变量柱塞泵+阀前补偿\n奔驰Tier 4F发动机\n全轮转向\nH型支腿": (
        "G1 platform\n6/7-section single-cylinder pinned main boom\nDual electronically controlled variable-displacement piston pumps with pre-compensated valves\n"
        "Mercedes-Benz Tier 4 Final engine\nAll-wheel steering\nH-pattern outriggers"
    ),
    "G2平台\n全新外观\n6节主臂\n康明斯发动机": (
        "G2 platform\nNew exterior design\n6-section main boom\nCummins engine"
    ),
    "奔驰发动机": "Mercedes-Benz engine",
    "康明斯发动机": "Cummins engine",
    "美康Tier 4F发动机": "Cummins Tier 4 Final engine",
    "2.5 可售型谱分析——越野轮胎起重机对标多田野": (
        "2.5 Market-ready portfolio analysis - rough-terrain crane benchmark against Tadano"
    ),
    "2、核心产品线—起重机\n2.5 可售型谱分析——越野轮胎起重机对标多田野": (
        "Core product line - cranes\n2.5 Market-ready portfolio analysis - rough-terrain crane benchmark against Tadano"
    ),
    "2、核心产品线—起重机\n2.5 可售型谱分析——通用底盘起重机对标National": (
        "Core product line - cranes\n2.5 Market-ready portfolio analysis - boom-truck benchmark against National Crane"
    ),
    "2.11 当地化保供举措—美国施维英合作组装Boom truck": (
        "2.11 Local supply initiative - boom-truck assembly partnership with Schwing America"
    ),
    "当地化保供举措—美国施维英合作组装Boom truck": (
        "Local supply initiative - boom-truck assembly partnership with Schwing America"
    ),
    "2、核心产品线—起重机\n2.11 当地化保供举措—美国施维英合作组装Boom truck": (
        "Core product line - cranes\n2.11 Local supply initiative - boom-truck assembly partnership with Schwing America"
    ),
    "① 对多频转场效率要求高；\n② 零散吊装对作业效率要求高；\n③ 安全标准严。": (
        "1. Frequent jobsite moves require high roading efficiency.\n"
        "2. General pick-and-carry work requires high operating efficiency.\n"
        "3. Safety requirements are stringent."
    ),
    "① 能够吊臂在很小仰角吊重；\n② 狭小空间适应能力强，具有多种支腿跨距、四种转向模式。\n③吊装精度高，操作平稳、安全可靠。": (
        "1. The crane can lift at very low boom angles.\n"
        "2. Multiple outrigger spans and four steering modes support confined jobsites.\n"
        "3. Load placement is precise, smooth and safe."
    ),
    "①设备常集成于标准集装箱内，需精准对位就位；②场地空间小，支腿展开受限；③作业频率高，设备需调度灵活；④部分项目与建筑结构相连，要求吊装安全等级高": (
        "1. Equipment is often housed in standard containers and requires precise placement.\n"
        "2. Confined sites restrict outrigger deployment.\n"
        "3. High work frequency requires flexible dispatching.\n"
        "4. Interfaces with building structures require a high level of lifting safety."
    ),
    "①风大地区作业、吊装高度中等、防风性能好。\n②工况全覆盖，吊装稳定，平稳性好。": (
        "1. Operations in windy areas require stable lifting at moderate heights and good wind resistance.\n"
        "2. The application range is fully covered, with stable and smooth lifting performance."
    ),
    "作业工况可覆盖\nXCT60_U中短臂长吊装性能优化，吊装精度高，液控系统稳定可靠，连续作业能力强。": (
        "The application is covered.\nXCT60_U provides optimized short- and mid-boom lifting performance, precise load placement, a stable hydraulic-control system and strong continuous-duty capability."
    ),
    "力限器吊重时，实际总重约2000-2500lb左右，在测试不同工况下，力限器显示值最大达到在3400lb，存在一定误差。": (
        "With an actual suspended load of approximately 2,000-2,500 lb, the rated-capacity limiter displayed up to 3,400 lb under the tested configurations, indicating a measurement deviation."
    ),
    "力限器空钩、吊重重量": "Rated-capacity-limiter readings with empty hook and suspended load",
    "加州山火/地震、华盛顿泥石流等自然载荷，需要清理倒塌建筑、架设临时桥梁等。": (
        "Disaster-response work following California wildfires or earthquakes and Washington landslides includes clearing collapsed structures and erecting temporary bridges."
    ),
    "吊装作业工况可以满足，①整机臂长及幅度满足使用要求。\n②双变量泵系统，单泵作业微动性好，双泵作业效率高。\n③整机操作简单，具有虚拟墙功能,但用户提出增加座椅先导,进一步简化操作.": (
        "The lifting application is supported.\n"
        "1. Boom length and working radius meet the application requirements.\n"
        "2. The dual-variable-pump system provides precise single-pump control and efficient dual-pump operation.\n"
        "3. Controls are straightforward and include a virtual-wall function; users requested seat-mounted pilot controls to simplify operation further."
    ),
    "智能臂架、新型电控负载敏感液压系统，操控性、使用方便性、作业效率行业领先": (
        "The intelligent boom system and electro-hydraulic load-sensing system provide class-leading controllability, ease of use and operating efficiency."
    ),
    "暂不布局": "Not currently planned",
    "销量较低\n暂不布局": "Low sales volume\nNot currently planned",
    "桥梁下方更换预制桥面板（单块重12-15吨），作业面为河岸滩涂软泥地，空间受桥墩限制。": (
        "Replace precast bridge-deck panels weighing 12-15 t beneath a bridge, working from soft riverbank ground with clearance constrained by bridge piers."
    ),
    "泥泞、坑洼等恶劣路面，周围环境复杂，吊装工况多，有时需34m以上大幅度作业": (
        "Muddy, rutted access roads and complex surroundings require broad application coverage, including occasional long-radius work beyond 34 m."
    ),
    "零散吊装，商业或厂房": "General lifting for commercial and industrial facilities",
    "零散吊装，商业或厂房：各种商业、厂房、基础电力设施升级、杆塔通信设备吊装": (
        "General lifting for commercial and industrial facilities, including power-infrastructure upgrades and utility-pole or communications-equipment installation"
    ),
    "高精力限器系统，重载误差在3%以内，具有系统故障提示": (
        "High-accuracy rated-capacity limiter with heavy-load error within 3% and system-fault alerts"
    ),
    "高精力限器系统，重载误差在5%以内，具有故障提示功能，整体安全性设计的完备性高于徐工": (
        "High-accuracy rated-capacity limiter with heavy-load error within 5% and fault alerts; the overall safety-system implementation is more comprehensive than XCMG's current product"
    ),
    "高精力限器系统，重载误差在5%以内，具有系统故障提示": (
        "High-accuracy rated-capacity limiter with heavy-load error within 5% and system-fault alerts"
    ),
})


SYSTEM_PROMPT = """You are a senior North American mobile-crane product engineer and technical editor.
Translate and edit every item into clear, natural US English for an internal engineering benchmark website.

Requirements:
- Use the Chinese source as authoritative. The draft is only a reference and may be wrong or misaligned.
- Translate every fact completely. Do not summarize, add, omit or invent information.
- Preserve numbers, dates, percentages, units, model codes, list numbering, line breaks and uncertainty.
- Mandatory glossary: 通用底盘起重机 = boom truck; 越野轮胎起重机 = rough-terrain crane;
  全地面起重机 = all-terrain crane; 履带起重机 = crawler crane; 主臂 = main boom;
  基本臂 = base boom; 副臂 = jib; 支腿 = outrigger; 配重 = counterweight;
  卷扬 = winch; 钢丝绳 = wire rope; 行走减速机 = travel reduction gearbox.
- Use professional mobile-crane terminology: rough-terrain crane, all-terrain crane, boom truck,
  crawler crane, main boom, base boom, jib, outrigger, counterweight, hook block, winch, wire rope,
  travel reduction gearbox, load chart, rated-capacity limiter, pick-and-carry, fine-control performance,
  operator ergonomics, operator comfort, serviceability, jobsite travel and product portfolio.
- Use XCMG, Caterpillar, Komatsu, John Deere, SANY, LiuGong, Bobcat, Tadano, Liebherr, Grove,
  Terex and Manitowoc for brand names.
- Avoid literal Chinese syntax, vague pronouns, sales language and sentence fragments.
- Use sentence case for body copy. Do not capitalize every word.
- Return a JSON object with a translations array of exactly the same length and order.
"""


def batches(items: list[tuple[str, str]], max_items: int = 40, max_chars: int = 5200):
    current: list[tuple[str, str]] = []
    size = 0
    for item in items:
        item_size = len(item[0]) + len(item[1])
        if current and (len(current) >= max_items or size + item_size > max_chars):
            yield current
            current = []
            size = 0
        current.append(item)
        size += item_size
    if current:
        yield current


def request_review(items: list[tuple[str, str]], model: str) -> list[str]:
    payload = {
        "model": model,
        "stream": False,
        "think": False,
        "format": {
            "type": "object",
            "properties": {
                "translations": {
                    "type": "array",
                    "items": {"type": "string"},
                }
            },
            "required": ["translations"],
        },
        "options": {"temperature": 0.05, "num_ctx": 16384, "num_predict": 2048},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": json.dumps(
                    [
                        {"source_zh": source, "draft_en": draft}
                        for source, draft in items
                    ],
                    ensure_ascii=False,
                ),
            },
        ],
    }
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=900) as response:
        result = json.loads(response.read().decode("utf-8"))
    content = json.loads(result["message"]["content"])
    translations = content.get("translations") or []
    if len(items) == 1 and len(translations) > 1:
        translations = ["\n".join(str(value).strip() for value in translations if str(value).strip())]
    if len(translations) != len(items):
        raise ValueError(f"Expected {len(items)} translations, received {len(translations)}")
    return [str(value).strip() for value in translations]


def deterministic_cleanup(translation: str) -> str:
    for old, new in sorted(TEXT_REPLACEMENTS.items(), key=lambda item: len(item[0]), reverse=True):
        translation = re.sub(re.escape(old), new, translation, flags=re.IGNORECASE)
    translation = re.sub(r"\bXCMG(?=[A-Za-z])", "XCMG ", translation)
    translation = re.sub(r"\bTadano(?=[A-Za-z])", "Tadano ", translation)
    translation = re.sub(r"\bUnited States(?=[A-Za-z])", "United States ", translation)
    translation = re.sub(r"\bCanada(?=[A-Za-z])", "Canada ", translation)
    translation = re.sub(r"\s+([,.;:%)])", r"\1", translation)
    translation = re.sub(r"([(])\s+", r"\1", translation)
    translation = re.sub(r"\s{2,}", " ", translation)
    return translation.strip()


def generated_manual_override(source: str) -> str | None:
    segment = source.strip().replace("。", ".")
    segment = segment.replace("二、大区产品策略—美国和加拿大；", "Regional product strategy - United States and Canada: ")
    segment = segment.replace("大区产品策略—美国和加拿大；", "Regional product strategy - United States and Canada: ")
    segment = segment.replace("对比结论：", "Comparison conclusion:")
    category_terms = {
        "越野轮胎起重机": "rough-terrain crane",
        "全地面起重机": "all-terrain crane",
        "通用底盘起重机": "boom truck",
        "履带起重机": "crawler crane",
    }
    for source_term, target_term in category_terms.items():
        segment = segment.replace(source_term, target_term)
    segment = re.sub(r"(crane|truck)(?=\d)", r"\1 ", segment)
    segment = re.sub(r"(\d+)\s*[~—–-]\s*(\d+)吨产品段", r"\1-\2 t product segment", segment)
    segment = re.sub(r"(\d+)\s*[~—–-]\s*(\d+)吨级", r"\1-\2 t class", segment)
    segment = re.sub(r"(\d+)吨及以下产品段", r"up to \1 t product segment", segment)
    segment = re.sub(r"(\d+)吨及以上产品段", r"\1 t and above product segment", segment)
    segment = re.sub(r"(\d+)吨产品段", r"\1 t product segment", segment)
    segment = re.sub(r"(\d+)吨产品", r"\1 t product", segment)
    if segment != source.strip() and not HAN.search(segment):
        return segment
    if source.startswith("作业工况可覆盖\nXCT60_U整机可靠性高"):
        return (
            "Supported work profile:\nXCT60_U provides high machine reliability, convenient transport, "
            "and rapid deployment and retraction for high-frequency construction projects."
        )
    if source.startswith("作业工况可覆盖：\n①适应当地环境"):
        return (
            "Supported work profiles:\n"
            "1. Local-climate operation: front and rear HVAC ducts plus an auxiliary fan improve operator comfort.\n"
            "2. Rapid setup: wireless outrigger controls support ground-level deployment and retraction, while "
            "the matched chassis supports efficient, regulation-compliant road travel."
        )
    if source.startswith("工况可满足：\n①根据桥梁等工地情况"):
        return (
            "Supported work conditions:\n"
            "1. For bridge and similar jobsites, ergonomic improvements simplify outrigger setup, retraction "
            "and crane deployment; jib and counterweight installation are designed for convenient handling.\n"
            "2. For jobsite relocation, a heavy pick-and-carry operating condition should cover travel with "
            "the counterweight installed."
        )
    if match := re.fullmatch(r"(\d+(?:\.\d+)?)万美(?:元|金)", source):
        return f"US${float(match.group(1)) / 100:g} million"
    if match := re.fullmatch(r"(\d+(?:\.\d+)?)亿", source):
        return f"{float(match.group(1)) / 10:g} billion"
    if match := re.fullmatch(r"(\d+(?:\.\d+)?)万", source):
        return f"{float(match.group(1)) / 100:g} million"
    if match := re.fullmatch(r"(\d{1,2})月", source):
        months = {
            "1": "January", "2": "February", "3": "March", "4": "April",
            "5": "May", "6": "June", "7": "July", "8": "August",
            "9": "September", "10": "October", "11": "November", "12": "December",
        }
        return months.get(match.group(1))
    if match := re.fullmatch(r"(\d+)节", source):
        return f"{match.group(1)}-section"
    if match := re.fullmatch(r"(\d+)节主臂", source):
        return f"{match.group(1)}-section main boom"
    if match := re.fullmatch(r"(\d+)吨", source):
        return f"{match.group(1)} t"
    if source.startswith("徐工口碑（其他高端市场）："):
        return (
            "XCMG feedback from other premium markets:\n"
            "XCMG crawler cranes are described as rugged, durable, high-performing and easy to service, "
            "with no major recurring problems. Several minor issues were reported during early ownership, "
            "but the machines became stable and satisfactory after those initial issues were resolved.\n"
            "Benchmark-brand feedback:\n"
            "1. One customer described a long-standing family preference for Liebherr cranes, citing "
            "reliability and confidence in the products.\n"
            "2. A customer working on redevelopment projects in older New York neighborhoods reported "
            "confidence in slope stability and immediate response from the safety systems."
        )
    if source.startswith("目前徐工在0-22.9吨、23-29.9吨、41-49.9"):
        return (
            "XCMG currently has portfolio gaps in the 0-22.9 USt, 23-29.9 USt and 41-49.9 USt classes. "
            "The market below 30 USt consists primarily of boom trucks. Demand in the 0-22.9 USt range "
            "is declining, and competitors have largely stopped developing products in that class; new "
            "development is therefore not recommended. The proposed portfolio action is one 30 USt boom "
            "truck, plus one 45-50 USt boom truck to address demand in the 41-49.9 USt range."
        )
    if source.startswith("徐工口碑：\n徐工通用底盘起重机"):
        return (
            "XCMG customer feedback:\n"
            "The U-shaped boom on XCMG boom trucks differs from the traditional four-sided boom used on "
            "US boom trucks. Customers described it as robust and stable, with a design similar to European "
            "all-terrain cranes.\n"
            "Benchmark-brand feedback:\n"
            "1. One customer described a long-standing family preference for National cranes, citing "
            "reliable and consistent product performance.\n"
            "2. Another customer considered the National design and equipment content dated. Although the "
            "machine was generally dependable, the customer had added features through aftermarket modifications."
        )
    if source.startswith("LB全地面主打工况适应性"):
        return (
            "Liebherr all-terrain cranes emphasize jobsite adaptability, intelligent functions and modular "
            "design for complex, demanding applications. Tadano emphasizes reliability and ease of use, "
            "supported by flexible solutions, service and long-term customer relationships.\n"
            "Compared with the benchmark portfolios, XCMG offers four mainstream all-terrain crane models "
            "covering 57% of the market. Portfolio gaps remain in the 0-65.9 t, 151-219.9 t and 400 t classes. "
            "Because demand in the 0-65.9 t and 151-219.9 t ranges is limited and outside the principal demand "
            "bands, additional standard products are not currently recommended. Products above 400 t should "
            "be developed to order, while the main priority should be improving competitiveness in the 100 t class."
        )
    if source.startswith("National和Manitex系列通用底盘起重机"):
        return (
            "National and Manitex address regional North American requirements by offering multiple chassis "
            "brands, specifications and axle configurations in each boom-truck capacity class. This approach "
            "supports differences in state and regional road regulations and jobsite-travel requirements.\n"
            "Compared with the benchmark portfolios, XCMG offers three mainstream boom-truck models covering "
            "60% of the market. Portfolio gaps remain in the 0-22.9 USt, 23-29.9 USt and 41-49.9 USt classes. "
            "The market below 30 USt consists primarily of boom trucks. Demand in the 0-22.9 USt range is "
            "declining, and competitors have largely stopped developing products in that class; new development "
            "is therefore not recommended. The proposed actions are one 30 USt boom truck and one 45-50 USt "
            "boom truck to address demand in the 41-49.9 USt range."
        )
    if source.startswith("马尼托瓦克National专注通用底盘起重机"):
        return (
            "Manitowoc National focuses on boom trucks and ranked first in North American sales in 2024. "
            "Its product quality and performance are considered industry-leading, while its core customers "
            "are small and mid-size rental companies that emphasize value. Because XCMG's intended brand "
            "position is closest to National, National is the primary boom-truck benchmark.\n"
            "Tadano leads rough-terrain crane sales and is preferred by rental customers for high reliability. "
            "Its products command first-tier pricing. XCMG should benchmark Tadano while building brand "
            "competitiveness, with proposed pricing 10-15% below the benchmark.\n"
            "Liebherr is a leading all-terrain and crawler-crane brand, with premium technology, quality, "
            "performance and pricing, serving mainly large local rental companies. XCMG should target Liebherr-level "
            "product capability, with proposed pricing 10-15% below the benchmark."
        )
    if source.startswith("多田野越野轮胎起重机在产品操控性"):
        return (
            "Tadano rough-terrain cranes are recognized in the market for controllability, operator "
            "comfort and high reliability, which align with premium North American market requirements.\n"
            "Compared with the benchmark portfolio, XCMG offers four mainstream rough-terrain crane "
            "models covering 75% of the market. XCMG currently has portfolio gaps in the 0-50 USt range; however, "
            "demand is fragmented across those capacities and each individual class is relatively small. "
            "The four planned XCMG models cover the principal North American demand bands. Future market "
            "research should evaluate development of a larger 165 USt rough-terrain crane to establish an "
            "early position in that capacity class."
        )
    if not source.startswith("对比结论："):
        return None
    category = None
    advantages = None
    gaps = None
    if "通用底盘起重机" in source:
        category = "XCMG boom trucks"
        advantages = "machine performance, equipment content, controllability and operator ergonomics"
        gaps = "Because XCMG remained in the early growth stage of the premium market"
    elif "全地面起重机" in source:
        category = "XCMG all-terrain cranes"
        advantages = "machine performance and equipment content"
        gaps = (
            "Because XCMG remained in the early stage of entering the premium market, additional "
            "development time was required to close benchmark gaps in adaptability, reliability and controllability"
        )
    if not category:
        return None

    price_match = re.search(r"低于(?:行业)?标杆(?:约)?(\d+)%", source)
    price = price_match.group(1) if price_match else ""
    first = (
        f"1. {category} were assessed as having advantages in {advantages}. {gaps}, the proposed "
        f"price position was {price}% below the industry benchmark."
    )

    if "销量达到3台，实现130吨以上越野吊产品市场突破" in source:
        target = "the 2025 plan targeted three units and a market breakthrough for rough-terrain cranes above 130 USt"
    elif "销量达到6台，市场占有率达到3%" in source:
        target = "the 2025 plan targeted six boom trucks and a 3% market share"
    elif "销量达到10台，市场占有率达到8%" in source:
        target = "the 2025 plan targeted ten boom trucks and an 8% market share"
    elif "销量达到12台，市场占有率达到5%以上" in source:
        target = "the 2025 plan targeted twelve boom trucks and a market share above 5%"
    elif "销量达到2台，相比2024年销售收入翻2倍" in source:
        target = "the 2025 plan targeted two all-terrain cranes and twice the 2024 sales revenue"
    elif "销量达到4台，相比2024年销售收入翻2倍以上" in source:
        target = "the 2025 plan targeted four all-terrain cranes and more than twice the 2024 sales revenue"
    else:
        return None
    return f"Comparison conclusion:\n{first}\n2. Based on the assessed competitive strengths, {target}."


def source_numbers(source: str) -> set[str]:
    return {value.rstrip("0").rstrip(".") for value in NUMBER.findall(source)}


def target_numbers(target: str) -> set[str]:
    values = {value.rstrip("0").rstrip(".") for value in NUMBER.findall(target.replace(",", ""))}
    number_words = {
        "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
        "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
        "eleven": "11", "twelve": "12", "thirteen": "13", "fourteen": "14",
        "fifteen": "15", "sixteen": "16", "seventeen": "17", "eighteen": "18",
        "nineteen": "19", "twenty": "20",
    }
    lower = target.lower()
    values.update(number for word, number in number_words.items() if re.search(rf"\b{word}\b", lower))
    return values


def is_valid(source: str, translation: str, *, strict: bool = True) -> bool:
    translation_lower = translation.lower()
    if not translation or HAN.search(translation):
        return False
    if "i don't know what you're talking about" in translation_lower:
        return False
    if len(source) >= 18 and len(translation) < 8:
        return False
    if strict and not source_numbers(source).issubset(target_numbers(translation)):
        return False
    if strict:
        for source_term, required_target in SOURCE_TERMS.items():
            if source_term in source and required_target not in translation_lower:
                return False
    return True


def review_batch(items: list[tuple[str, str]], *, strict: bool = True) -> list[str]:
    primary = FALLBACK_MODEL if strict and any(len(source) >= 120 for source, _ in items) else MODEL
    if strict:
        models = (primary, FALLBACK_MODEL, LAST_RESORT_MODEL) if len(items) == 1 else (primary, FALLBACK_MODEL)
    else:
        models = (MODEL,)
    for model in models:
        try:
            translations = [deterministic_cleanup(value) for value in request_review(items, model)]
            invalid = [
                index
                for index, ((source, _), value) in enumerate(zip(items, translations))
                if not is_valid(source, value, strict=strict)
            ]
            if not invalid:
                return translations
            if len(items) > 1:
                for index in invalid:
                    translations[index] = review_batch([items[index]], strict=strict)[0]
                return translations
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError, json.JSONDecodeError):
            time.sleep(1)
    if len(items) == 1:
        source, _ = items[0]
        raise RuntimeError(f"Could not review translation: {source[:100]}")
    midpoint = len(items) // 2
    return review_batch(items[:midpoint], strict=strict) + review_batch(items[midpoint:], strict=strict)


def write_output(source_payload: dict, cache: dict[str, str]) -> None:
    OUTPUT.write_text(
        json.dumps(
            {
                "model": f"{MODEL} post-edit with {FALLBACK_MODEL} fallback",
                "translation_scope": "crane reader-facing English; source-grounded engineering post-edit",
                "source_count": source_payload.get("source_count"),
                "translations": dict(sorted(cache.items())),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=int, default=0)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--high-risk", action="store_true")
    parser.add_argument("--non-high-risk", action="store_true")
    parser.add_argument("--skip", type=int, default=0)
    return parser.parse_args()


def high_risk(source: str, draft: str) -> bool:
    ratio = len(draft) / max(1, len(source))
    return bool(
        HIGH_RISK.search(draft)
        or (len(source) >= 12 and ratio < 0.6)
        or (len(source) <= 8 and ratio > 7)
        or (len(source) >= 20 and ratio > 5.2)
    )


def main() -> None:
    args = parse_args()
    source_payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    drafts: dict[str, str] = source_payload["translations"]
    manual_overrides = dict(MANUAL_OVERRIDES)
    manual_overrides.update(
        {
            source: value
            for source in drafts
            if (value := generated_manual_override(source)) is not None
        }
    )
    reviewed_payload = json.loads(OUTPUT.read_text(encoding="utf-8")) if OUTPUT.exists() else {}
    cache: dict[str, str] = (
        {source: deterministic_cleanup(draft) for source, draft in drafts.items()}
        if args.force
        else (reviewed_payload.get("translations") or {})
    )
    cache.update({key: value for key, value in manual_overrides.items() if key in drafts})

    if args.high_risk:
        pending = [
            (source, draft)
            for source, draft in drafts.items()
            if high_risk(source, draft) and source not in manual_overrides
        ]
        pending.sort(key=lambda item: len(item[0]))
    elif args.non_high_risk:
        pending = [
            (source, draft)
            for source, draft in drafts.items()
            if not high_risk(source, draft) and source not in manual_overrides
        ]
        pending.sort(key=lambda item: len(item[0]))
    else:
        pending = [(source, draft) for source, draft in drafts.items() if source not in cache]
    if args.skip:
        pending = pending[args.skip :]
    if args.sample:
        pending = pending[: args.sample]
    groups = list(batches(pending, max_items=20, max_chars=2400)) if args.non_high_risk else list(batches(pending))
    completed = 0
    for index, group in enumerate(groups, 1):
        values = review_batch(group, strict=not args.non_high_risk)
        cache.update(zip((source for source, _ in group), values))
        cache.update({key: value for key, value in manual_overrides.items() if key in drafts})
        write_output(source_payload, cache)
        completed += len(group)
        print(
            f"Reviewed batch {index}/{len(groups)} ({completed}/{len(pending)}); "
            f"cache {len(cache)}/{len(drafts)}",
            flush=True,
        )
    if not groups:
        write_output(source_payload, cache)
        print(f"No model review needed; cache {len(cache)}/{len(drafts)}", flush=True)


if __name__ == "__main__":
    main()
