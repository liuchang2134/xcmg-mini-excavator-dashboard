from __future__ import annotations

import html
import math
from pathlib import Path
from typing import Any

try:
    from .crane_condition_context import CONDITION_EXECUTION, OFFICIAL_REFERENCES, field_observation
    from .crane_data import load_crane_workbook
    from .crane_ppt_render import _clean_crane_english, render_class_context, render_legacy_redirect, render_market_report_page
    from .crane_scoring import (
        CATEGORY_WEIGHTS,
        CONDITIONS,
        condition_applicable,
        condition_config_weights,
        condition_display_metric_names,
        condition_metric_weights,
        metric_direction,
        score_sheet,
    )
except ImportError:
    from crane_condition_context import CONDITION_EXECUTION, OFFICIAL_REFERENCES, field_observation
    from crane_data import load_crane_workbook
    from crane_ppt_render import _clean_crane_english, render_class_context, render_legacy_redirect, render_market_report_page
    from crane_scoring import (
        CATEGORY_WEIGHTS,
        CONDITIONS,
        condition_applicable,
        condition_config_weights,
        condition_display_metric_names,
        condition_metric_weights,
        metric_direction,
        score_sheet,
    )


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

METRIC_EN = {
    "Fuel tank": "Fuel Tank Capacity",
    "Main boom @ 5m": "Main-Boom Capacity at 5 m Radius",
    "Main boom @ 10m": "Main-Boom Capacity at 10 m Radius",
    "Main boom @ 15m": "Main-Boom Capacity at 15 m Radius",
    "Main boom @ 20m": "Main-Boom Capacity at 20 m Radius",
    "Main boom @ 25m": "Main-Boom Capacity at 25 m Radius",
    "Main boom @ 30m": "Main-Boom Capacity at 30 m Radius",
    "Main boom @ 40m": "Main-Boom Capacity at 40 m Radius",
    "Main boom @ 50m": "Main-Boom Capacity at 50 m Radius",
    "Main boom @ max radius": "Main-Boom Capacity at Maximum Radius",
    "Jib W/O inserts @ 20m": "Base-Jib Capacity at 20 m Radius",
    "Jib W/O inserts @ 25m": "Base-Jib Capacity at 25 m Radius",
    "Jib W/O inserts @ 30m": "Base-Jib Capacity at 30 m Radius",
    "Jib W/O inserts @ 40m": "Base-Jib Capacity at 40 m Radius",
    "Jib W/O inserts @ 50m": "Base-Jib Capacity at 50 m Radius",
    "Jib W/O inserts max radius": "Base-Jib Maximum Radius",
    "On tires @ 3m over front": "On-Tire Capacity, Over Front, at 3 m Radius",
    "On tires @ 5m over front": "On-Tire Capacity, Over Front, at 5 m Radius",
    "On tires @ 7m over front": "On-Tire Capacity, Over Front, at 7 m Radius",
    "On tires @ 10m over front": "On-Tire Capacity, Over Front, at 10 m Radius",
    "Pick and carry @ 5m": "Pick-and-Carry Capacity at 5 m Radius",
    "Boom raise speed": "Boom Raising Time",
    "Boom extend speed": "Boom Extension Time",
    "Aux winch max line pull": "Auxiliary Winch Maximum Line Pull",
    "Aux winch max speed": "Auxiliary Winch Maximum Line Speed",
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

CONFIG_EN = {
    "Auto Lubrication system": "Automatic Lubrication System",
    "Fuel engine heater": "Engine Fuel Heater",
    "Short Jib": "Short Jib",
    "Tow hooks": "Tow Hooks",
    "Greasless boom": "Grease-Free Boom",
    "360deg house lock": "360° Upperstructure Mechanical Lock",
    "2deg out of level load charts": "2° Out-of-Level Load Charts",
    "heavy CWT": "Heavy Counterweight Package",
    "Cribbing rack": "Outrigger Cribbing Rack",
    "Auto winch and boom control": "Automatic Winch and Boom Control",
    "Tires options": "Tire Options",
    "Short heavy lift Jib": "Short Heavy-Lift Jib",
}

CONDITION_COPY = {
    "road-transport": (
        "用于判断设备在州际道路运输、工地间转场和配重拆装中的合规性与组织效率。运输重量和单轴载荷决定许可与车辆组合，宽高长度决定路线限制，可拆配重、配重组合及最大配重状态行驶能力决定到场后的恢复速度。",
        "Evaluates interstate transport, job-to-job relocation and counterweight logistics. Transport mass and axle loading affect permits and trailer selection; transport envelope affects route restrictions; removable counterweight, available counterweight combinations and travel with maximum counterweight affect site-readiness time.",
    ),
    "rapid-mobilization": (
        "用于判断租赁设备在连续多工地任务中的拆装、配重转换和到场恢复效率。可拆配重、配重组合、随车配重能力和带配重行驶速度决定转场拆分方案；牵引钩、垫木架和集中润滑影响现场准备及非生产停机时间。",
        "Evaluates dismantling, counterweight changes and site-readiness efficiency during consecutive rental or multi-site assignments. Removable counterweight, available counterweight combinations, on-crane counterweight and travel speed with counterweight define the mobilization plan; tow hooks, a cribbing rack and automatic lubrication affect setup and non-productive downtime.",
    ),
    "site-mobility": (
        "用于判断设备从公路进入泥地、碎石和未铺装工地后的通过性与机动效率。最高行驶速度影响场内转场时间，最小转弯半径和转向模式影响受限通道调头，爬坡度、驱动桥及接近/离去角共同决定坡道与坑洼路面的通过边界。",
        "Evaluates mobility from paved roads into muddy, gravel or unprepared sites. Travel speed affects relocation time; turning radius and steering modes affect maneuverability in constrained access; gradeability, driven axles and approach/departure angles define the usable terrain envelope.",
    ),
    "confined-positioning": (
        "用于判断设备在厂房、设备区、住宅和障碍物密集场地内的调位能力。尾部回转半径、基本臂长度和转弯半径决定需要预留的作业包络，转向模式和回转速度影响就位次数与微动调整效率。",
        "Evaluates positioning in plants, equipment yards, residential sites and other obstacle-dense locations. Tail-swing radius, retracted boom length and turning radius define the required envelope, while steering modes and swing speed affect the number and precision of repositioning moves.",
    ),
    "near-heavy-lift": (
        "用于判断设备在近幅度完成大吨位构件卸车、设备就位和重载装配时的能力与效率。无专用附件最大起重量、最近可比幅度载荷和主卷扬拉力构成能力基础，主卷扬绳速与起臂时间影响单循环节拍。",
        "Evaluates unloading, equipment setting and heavy assembly at short radii. Maximum capacity without special equipment, the nearest comparable load-chart point and main-winch pull establish the capacity base; winch speed and boom-raising time affect cycle time.",
    ),
    "mid-radius-installation": (
        "用于判断钢结构、预制构件和一般设备在典型中等幅度下的安装能力。中幅度载荷表决定可吊构件边界，卷扬拉力、绳速、起臂时间和回转速度共同决定吊装循环效率与落钩控制。",
        "Evaluates structural steel, precast components and general equipment installation at representative mid radii. Mid-radius load-chart capacity defines the usable load envelope; winch pull, line speed, boom-raising time and swing speed determine cycle productivity and load placement control.",
    ),
    "long-boom-high-lift": (
        "用于判断厂房屋面、塔体、风电辅助和远距离越障安装的主臂覆盖能力。全伸臂长、最大额定幅度、远幅度载荷和最大幅度载荷共同定义作业边界，伸臂时间与驾驶室俯仰影响准备效率和高仰角视野。",
        "Evaluates main-boom coverage for roof, tower, wind-support and long-radius obstacle-clearance work. Full boom length, maximum rated radius, far-radius capacity and capacity at maximum radius define the operating envelope; boom-extension time and cab tilt affect setup efficiency and high-angle visibility.",
    ),
    "jib-long-radius": (
        "用于判断副臂在高空、远幅度和越障工况下的覆盖完整性。随车副臂长度、延伸节、近远幅度副臂载荷和最大幅度共同决定可承接任务；副臂变角和塔式副臂属于重要边界信息，但因源表为多值或文字状态，不参与自动优劣评分。",
        "Evaluates jib coverage for high-elevation, long-radius and obstacle-clearance work. Carried jib length, extensions, near/far jib capacities and maximum radius define the task envelope. Jib offsets and luffing-jib availability remain important boundary evidence but are not automatically scored because the source records them as multi-value or text fields.",
    ),
    "outrigger-stability": (
        "用于判断设备在不平地面、受限支腿空间和部分支腿展开条件下建立稳定作业平台的能力。支腿跨度和伸缩档位进入量化评分；支腿穿透量的工程方向在源资料中未定义，非对称支腿为文字状态，两者只展示原值并要求按载荷表复核。",
        "Evaluates stable setup on uneven ground, constrained outrigger footprints and partial-extension positions. Outrigger spread and extension positions are scored. Outrigger penetration has no verified direction in the source and asymmetric operation is text-based, so both are shown as evidence and require load-chart validation rather than automatic scoring.",
    ),
    "partial-outrigger-confined": (
        "用于判断建筑物、道路边线或设备基础限制支腿全展时的作业可执行性。支腿跨度、伸缩档位、尾部回转包络和中幅度载荷共同决定可用站位；非对称支腿状态与支腿穿透量仅作为边界证据，必须结合对应载荷表和地基承载力复核。",
        "Evaluates operation where buildings, road edges or foundations prevent full outrigger deployment. Outrigger spread, available extension positions, tail-swing envelope and mid-radius capacity define feasible setup positions. Asymmetric-outrigger status and outrigger penetration remain boundary evidence and must be verified against the applicable load chart and ground-bearing capacity.",
    ),
    "on-tire-pick-carry": (
        "用于判断越野轮胎起重机在不落支腿或带载移动时的能力边界。轮胎支撑近、远幅度载荷和 5m 带载行驶载荷是核心依据，场内行驶速度只作为作业组织效率的次要输入；该工况不用于全地面起重机页面。",
        "Evaluates rough-terrain-crane capability while lifting on tires or traveling with a suspended load. Near- and far-radius on-tire capacities and 5 m pick-and-carry capacity are the primary evidence; travel speed is a secondary productivity input. This condition does not apply to the all-terrain page.",
    ),
    "cycle-productivity": (
        "用于判断重复吊装、双钩协同和高频装卸任务中的循环效率。主副卷扬拉力与绳速决定起升能力和节拍，回转、起臂与伸臂时间决定空钩返回和下一循环准备时间；自动卷扬/臂架控制可降低操作负荷。",
        "Evaluates repetitive lifts, dual-hook coordination and high-frequency handling. Main and auxiliary winch pull and line speed determine lifting capability and pace; swing, boom raising and extension times determine return and reset time; automatic winch/boom control can reduce operator workload.",
    ),
    "precision-maintenance-lift": (
        "用于判断暖通设备、电力设施、广告与通信设备等高空维保任务中的微动控制和落位效率。主副卷扬绳速、回转速度、起臂与伸臂时间决定动作响应，驾驶室俯仰和自动卷扬/臂架控制影响高仰角视野、复合动作负荷和重复落钩一致性。",
        "Evaluates fine-motion control and placement efficiency for elevated HVAC, utility, sign and communications maintenance. Main and auxiliary line speeds, swing speed, boom-raising and extension times define motion response; cab tilt and automatic winch/boom control affect high-angle visibility, combined-motion workload and repeatable placement.",
    ),
    "all-weather-duty": (
        "用于判断低温启动、长班次连续吊装和维护受限场地的可用性。发动机功率、扭矩和燃油容量构成纸面基础，自动润滑、燃油加热、低温包和免润滑主臂对停机时间影响更直接，因此该工况提高配置侧权重。",
        "Evaluates cold starts, long-shift lifting and availability where maintenance access is limited. Engine power, torque and fuel capacity provide the specification base; automatic lubrication, fuel heating, cold-weather equipment and a grease-free boom have a more direct effect on downtime, so equipment receives the larger share.",
    ),
    "urban-utility-installation": (
        "面向老城区更新、电力、广告、通信和屋面设备等高空作业，综合判断设备能否在道路边线、建筑物和既有设施形成的狭小站位内完成进场、调位、越障和精准落位。该场景同时使用转弯与回转包络、中远幅载荷、臂架响应和控制配置，反映纸面适配性，不代替现场试吊。",
        "Covers urban renewal and elevated utility, sign, communications and rooftop-equipment work. It combines travel and swing envelope, mid/far-radius capacity, boom response and control equipment to judge paper-based fit within constrained streets and existing structures; it does not replace a site lift trial.",
    ),
    "industrial-shutdown-maintenance": (
        "面向油气装置、制造工厂和能源设施的停机检修，重点比较中远幅能力、主副卷扬协同、回转与臂架响应以及连续作业维护配置。该类任务通常受停机窗口、设备区障碍和落位精度约束，因此不能只看最大起重量。",
        "Covers shutdown maintenance in oil and gas facilities, manufacturing plants and energy sites. It emphasizes mid/far-radius capacity, auxiliary-winch coordination, swing and boom response, and uptime-related equipment because outage windows, plant obstructions and placement precision matter more than maximum capacity alone.",
    ),
    "bridge-infrastructure-placement": (
        "面向道路、桥梁和基础设施构件安装，综合比较工地通行、支腿布置、中远幅载荷和回转落位能力。支腿穿透量和非对称支腿状态保留为工程边界证据；正式方案仍需按地基承载力、支腿档位、构件重量和实际幅度复核载荷表。",
        "Covers road, bridge and infrastructure component placement by combining site access, outrigger setup, mid/far-radius capacity and controlled placement. Outrigger penetration and asymmetric-operation status remain engineering boundary evidence; the final plan still requires load-chart verification against ground bearing, outrigger position, component mass and actual radius.",
    ),
    "emergency-response": (
        "面向灾害清障、道路抢通和临时恢复任务，综合判断到场速度、未铺装路面机动、近中幅起重和快速动作能力。该场景强调响应与可达性，但不把牵引钩、轮胎或控制配置的资料空白当作无配置，也不推定任何救援认证。",
        "Covers debris clearance, route reopening and temporary recovery work by combining response speed, unprepared-site mobility, near/mid-radius lifting and fast boom motions. It emphasizes access and response without treating blank equipment fields as absence or implying any emergency-response certification.",
    ),
    "port-yard-handling": (
        "面向港口、堆场和高频装卸任务，重点比较主副卷扬拉力与绳速、回转和起臂节拍，以及场内短距离转场和调头能力。结果反映纸面循环潜力；实际生产率还取决于吊具、司机操作、路径组织、热平衡和连续循环衰减。",
        "Covers port, yard and high-cycle handling by emphasizing main/auxiliary-winch pull and line speed, swing and boom-raising pace, plus short-distance travel and maneuvering. Results indicate paper-based cycle potential; actual productivity also depends on rigging, operator technique, route planning, thermal balance and degradation over repeated cycles.",
    ),
}

CONDITION_BENEFITS = {
    "road-transport": ("牵引钩、垫木架、可拆配重和多配重组合有利于运输组织与到场恢复。", "Tow hooks, a cribbing rack, removable counterweight and multiple counterweight combinations support transport logistics and faster site preparation."),
    "rapid-mobilization": ("可拆配重、多配重组合、随车垫木架、牵引钩和集中润滑可减少拆装、等待和跨工地准备时间。", "Removable counterweight, multiple counterweight combinations, an on-crane cribbing rack, tow hooks and automatic lubrication can reduce dismantling, waiting and inter-site setup time."),
    "site-mobility": ("适配轮胎、多转向模式、驱动桥和差速锁有利于松软地面通过与受限通道调位。", "Appropriate tires, multiple steering modes, driven axles and differential locks improve soft-ground access and maneuvering in constrained routes."),
    "confined-positioning": ("360°上车锁止、自动卷扬/臂架控制、小尾部回转和短基本臂有利于精准就位。", "A 360° upperstructure lock, automatic winch/boom control, compact tail swing and short retracted boom support precise positioning."),
    "near-heavy-lift": ("重型配重、短型重载副臂和卷扬/臂架自动控制可扩展近幅重载能力并稳定循环。", "Heavy counterweight, a short heavy-lift jib and automatic winch/boom control can extend near-radius capability and stabilize cycle execution."),
    "mid-radius-installation": ("卷扬与臂架自动控制、较高卷扬绳速和稳定回转有利于结构安装节拍与落钩精度。", "Automatic winch/boom control, higher line speed and controlled swing support structural-installation productivity and placement accuracy."),
    "long-boom-high-lift": ("重型配重、自动臂架控制、驾驶室俯仰和较快伸臂动作有利于高空远幅安装。", "Heavy counterweight, automatic boom control, cab tilt and faster boom extension support high-elevation long-radius installation."),
    "jib-long-radius": ("短副臂、重载副臂、多变角组合和自动控制有利于越障与远幅度覆盖。", "Short and heavy-lift jibs, multiple offset combinations and automatic control improve obstacle clearance and long-radius coverage."),
    "outrigger-stability": ("2°倾斜载荷表、垫木架、非对称支腿作业和多档支腿伸缩有利于受限地面稳定布置。", "2° out-of-level charts, a cribbing rack, asymmetric operation and multiple outrigger positions improve setup on constrained or uneven ground."),
    "partial-outrigger-confined": ("多档支腿、非对称支腿载荷表、2°倾斜载荷表、垫木架和上车锁止有利于受限边界内建立可核验的稳定作业区。", "Multiple outrigger positions, asymmetric and 2° out-of-level load charts, a cribbing rack and upperstructure lock support a verifiable working envelope within constrained boundaries."),
    "on-tire-pick-carry": ("适配轮胎、上车锁止和明确的轮胎/带载载荷表有利于移动吊装安全边界管理。", "Appropriate tires, upperstructure lock and explicit on-tire/pick-and-carry load charts support safe mobile-lifting limits."),
    "cycle-productivity": ("双卷扬、自动卷扬/臂架控制和集中润滑有利于减少循环时间与维护停机。", "Dual winches, automatic winch/boom control and centralized lubrication reduce cycle time and maintenance interruptions."),
    "precision-maintenance-lift": ("自动卷扬/臂架控制、驾驶室俯仰、双卷扬和稳定回转可降低高空维保中的修正次数与操作负荷。", "Automatic winch/boom control, cab tilt, dual winches and controlled swing can reduce corrective motions and operator workload during elevated maintenance."),
    "all-weather-duty": ("燃油加热、低温包、集中润滑和免润滑主臂直接影响低温启动和长班次可用率。", "Fuel heating, cold-weather equipment, automatic lubrication and a grease-free boom directly affect cold-start and long-shift availability."),
    "urban-utility-installation": ("紧凑回转包络、上车锁止、自动卷扬/臂架控制和倾斜载荷表有利于在道路边线和既有设施间安全调位。", "A compact swing envelope, upperstructure lock, automatic winch/boom control and out-of-level charts support controlled positioning around street edges and existing structures."),
    "industrial-shutdown-maintenance": ("双卷扬、自动控制、集中润滑和免润滑主臂有利于缩短停机窗口内的重复动作与维护等待。", "Dual winches, automatic control, centralized lubrication and a grease-free boom support repeated work within a limited shutdown window."),
    "bridge-infrastructure-placement": ("多档支腿、倾斜载荷表、垫木架、上车锁止和稳定回转有利于道路边界与不同地基条件下的构件安装。", "Multiple outrigger positions, out-of-level charts, cribbing storage, upperstructure lock and controlled swing support component placement beside roads and on varying ground."),
    "emergency-response": ("牵引钩、适配轮胎、多模式转向、上车锁止和自动控制有利于快速进场、调位和恢复作业。", "Tow hooks, suitable tires, multiple steering modes, upperstructure lock and automatic control support rapid access, positioning and recovery work."),
    "port-yard-handling": ("双卷扬、自动卷扬/臂架控制、集中润滑和上车锁止有利于连续装卸节拍与重复落位。", "Dual winches, automatic winch/boom control, centralized lubrication and an upperstructure lock support repetitive handling and placement cycles."),
}

CONDITION_ACTIONS = {
    "road-transport": (
        "按同配重状态复核整机运输质量、外廓和轴荷，建立可拆配重与公路转场组合边界。",
        "Recheck transport mass, envelope and axle loads at matched counterweight states, then define removable-counterweight and road-transport envelopes.",
    ),
    "rapid-mobilization": (
        "按同一任务路线记录配重拆装、垫木取放、上车锁止和到场准备总时间，并分别核对随车配重、拖车及轴荷方案。",
        "Record counterweight removal, cribbing handling, upperstructure locking and total site-readiness time on the same assignment route, then verify on-crane counterweight, trailer and axle-load plans separately.",
    ),
    "site-mobility": (
        "联合底盘与控制团队复核转向模式、最小转弯半径、爬坡度和接近/离去角，并完成未铺装场地调位试验。",
        "Jointly verify steering modes, turning radius, gradability and approach/departure angles, followed by an unpaved-site maneuvering test.",
    ),
    "confined-positioning": (
        "按同一场地边界测量转弯、回转和基本臂包络，记录完成就位所需转向次数与时间，复核自动控制和上车锁止状态。",
        "Measure turning, swing and retracted-boom envelopes within the same site boundary; record steering moves and time to position; verify automatic control and upperstructure-lock status.",
    ),
    "near-heavy-lift": (
        "按相同支腿、配重、倍率和臂长复核最近幅度载荷，并实测主卷扬拉力、绳速和起臂时间。",
        "Verify nearest-radius capacity at matched outrigger, counterweight, reeving and boom length, then measure main-winch pull, line speed and boom-raising time.",
    ),
    "mid-radius-installation": (
        "在统一臂长、幅度和吊重下记录起升、回转、落钩和空钩返回时间，区分载荷表差距与动作效率差距。",
        "At matched boom length, radius and load, record hoist, swing, placement and empty-hook return times to separate load-chart gaps from motion-efficiency gaps.",
    ),
    "long-boom-high-lift": (
        "按相同主臂长度、副臂组合和配重状态复核远幅度载荷，并评估副臂覆盖与伸臂效率的产品目标。",
        "Recheck long-radius loads at matched boom length, jib combination and counterweight state, then set product targets for jib coverage and boom-extension efficiency.",
    ),
    "jib-long-radius": (
        "按相同副臂长度、变角、配重和风速复核近远幅度载荷，并验证副臂安装时间和运输随车能力。",
        "Verify near- and far-radius jib capacities at matched jib length, offset, counterweight and wind condition, then validate jib installation time and on-crane transportability.",
    ),
    "outrigger-stability": (
        "补齐非对称支腿、倾斜工况载荷表和轮胎吊装数据，按同支腿档位验证支腿跨度、带载行驶及轮胎起重量。",
        "Complete asymmetric-outrigger, out-of-level and on-tire data, then verify outrigger spread, pick-and-carry and on-tire capacities at matched extension positions.",
    ),
    "partial-outrigger-confined": (
        "在统一地基承载力、支腿档位、配重、臂长和幅度下验证部分支腿载荷，补齐非对称支腿及倾斜地面载荷表并记录上车回转安全包络。",
        "Validate partial-outrigger capacity at matched ground-bearing pressure, outrigger position, counterweight, boom length and radius; complete asymmetric and out-of-level charts and record the safe upperstructure swing envelope.",
    ),
    "on-tire-pick-carry": (
        "按统一轮胎压力、路面坡度、吊重和幅度验证轮胎吊装与带载行驶，单独核对源表中的 0 值和缺失值。",
        "Validate on-tire lifting and pick-and-carry at matched tire pressure, ground slope, load and radius, and separately verify source zeros and missing values.",
    ),
    "cycle-productivity": (
        "开展主副卷扬、回转、起臂和伸臂的连续循环测试，记录单循环时间、热衰减和操作修正次数。",
        "Run continuous main/auxiliary-winch, swing, boom-raising and extension cycles, recording cycle time, thermal degradation and operator corrections.",
    ),
    "precision-maintenance-lift": (
        "在统一吊重、臂长和目标落位区下记录主副钩微动、回转制动、复合动作和重复落钩偏差，并同步评价高仰角视野和控制修正次数。",
        "At matched load, boom length and placement zone, record main/auxiliary-hook inching, swing braking, combined motions and repeat-placement deviation, while assessing high-angle visibility and the number of control corrections.",
    ),
    "all-weather-duty": (
        "开展动力热平衡、主副卷扬连续循环和低温启动试验，同时核对自动润滑、加热器及低温包的标选配状态。",
        "Run thermal-balance, continuous main/auxiliary-winch cycling and cold-start tests, while confirming standard/optional status for lubrication, heaters and cold-weather packages.",
    ),
    "urban-utility-installation": (
        "在统一道路宽度、障碍物边界、支腿档位、臂长和目标落位区下，记录进场转向次数、回转包络、越障余量和重复落位偏差。",
        "At matched street width, obstruction boundary, outrigger position, boom length and placement zone, record steering moves, swing envelope, clearance margin and repeat-placement deviation.",
    ),
    "industrial-shutdown-maintenance": (
        "按同一停机窗口和设备区边界组织中远幅吊装循环，记录主副钩切换、复合动作、落位修正、热衰减和维护准备时间。",
        "Run matched mid/far-radius cycles within the same outage window and plant boundary, recording main/auxiliary-hook changes, combined motions, placement corrections, thermal degradation and maintenance-preparation time.",
    ),
    "bridge-infrastructure-placement": (
        "按统一地基承载力、支腿档位、构件重量、臂长和实际幅度复核载荷表，并记录从进场到稳定平台建立及完成落位的总时间。",
        "Verify the load chart at matched ground-bearing capacity, outrigger position, component mass, boom length and actual radius, then record total time from site access through stable setup and final placement.",
    ),
    "emergency-response": (
        "在统一路面、坡度和障碍条件下验证到场、调头、起臂和近中幅起吊全过程，记录响应时间、操作修正次数及牵引/恢复接口状态。",
        "Under matched surface, grade and obstruction conditions, validate arrival, maneuvering, boom raising and near/mid-radius lifting, recording response time, operator corrections and towing/recovery-interface status.",
    ),
    "port-yard-handling": (
        "在统一吊具、载荷、路径和幅度下完成不少于 20 个连续装卸循环，记录平均循环时间、主副钩切换、热衰减、制动修正和燃油消耗。",
        "Complete at least 20 handling cycles with matched rigging, load, route and radius, recording average cycle time, hook changes, thermal degradation, braking corrections and fuel consumption.",
    ),
}

CONDITION_SHORT = {
    "road-transport": ("道路运输", "Road Transport"),
    "rapid-mobilization": ("快速转场", "Mobilization"),
    "site-mobility": ("场地机动", "Site Mobility"),
    "confined-positioning": ("狭窄调位", "Confined Positioning"),
    "near-heavy-lift": ("近幅重载", "Near Heavy Lift"),
    "mid-radius-installation": ("中幅安装", "Mid-Radius Lift"),
    "long-boom-high-lift": ("长臂高空", "Long-Boom Lift"),
    "jib-long-radius": ("副臂远幅", "Jib Long Radius"),
    "outrigger-stability": ("不平地面", "Uneven Ground"),
    "partial-outrigger-confined": ("部分支腿", "Partial Outriggers"),
    "on-tire-pick-carry": ("轮胎带载", "Pick and Carry"),
    "cycle-productivity": ("循环效率", "Cycle Productivity"),
    "precision-maintenance-lift": ("精密维保", "Precision Placement"),
    "all-weather-duty": ("全天候作业", "All-Weather Duty"),
    "urban-utility-installation": ("城市公用设施", "Urban Utilities"),
    "industrial-shutdown-maintenance": ("工业停机检修", "Industrial Shutdown"),
    "bridge-infrastructure-placement": ("道路桥梁安装", "Bridge and Roadwork"),
    "emergency-response": ("应急抢险", "Emergency Response"),
    "port-yard-handling": ("港口堆场", "Port and Yard"),
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
    return bilingual(METRIC_ZH.get(name, name), METRIC_EN.get(name, name))


def config_label(name: str) -> str:
    return bilingual(CONFIG_ZH.get(name, name), CONFIG_EN.get(name, name))


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


def metric_value(value: Any, unit: str | None = None) -> tuple[str, str, str]:
    """Return readable bilingual value text while preserving source semantics."""
    unit = (unit or "").strip()
    if value is None or value == "":
        return "—", "—", unit
    raw = str(value).strip()
    lowered = raw.lower()
    if lowered in {"yes, ?", "yes, ? deg"}:
        if unit.lower() == "deg" or lowered.endswith(" deg"):
            return "是（角度未记录）", "Yes; angle not specified", ""
        return "是（数值未记录）", "Yes; value not specified", ""
    if lowered in {"none", "n/a", "na", "not available"}:
        return "无", "None", ""
    if unit.lower() == "y/n":
        if lowered in {"y", "yes", "true"}:
            return "是", "Yes", ""
        if lowered in {"n", "no", "false"}:
            return "否", "No", ""
    text = fmt_number(value)
    return text, _clean_crane_english(text), unit


def render_metric_value(value: Any, unit: str | None = None, tag: str = "span") -> str:
    zh, en, display_unit = metric_value(value, unit)
    suffix = f" {display_unit}" if display_unit else ""
    source_attr = f' data-source-value="{esc(value)}"' if value not in (None, "") else ""
    return f'<{tag} data-en="{esc(en + suffix)}"{source_attr}>{esc(zh + suffix)}</{tag}>'


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


def _condition_comparison_rows(
    sheet: Any, scoring: dict[str, Any], condition: dict[str, Any]
) -> list[dict[str, Any]]:
    return condition_ranking_rows(sheet, scoring, condition)


def render_condition_overview_radar(sheet: Any, scoring: dict[str, Any]) -> str:
    applicable = [condition for condition in CONDITIONS if condition_applicable(sheet, condition)]
    comparable = [
        condition
        for condition in applicable
        if _condition_comparison_rows(sheet, scoring, condition)
    ]
    comparable.sort(
        key=lambda condition: len(_condition_comparison_rows(sheet, scoring, condition)),
        reverse=True,
    )
    axes = comparable[:10]
    eligible_models = []
    while len(axes) >= 3:
        eligible_models = [
            model
            for model in sheet.models
            if all(
                get_score_record(scoring, model.display_name)["condition_scores"].get(
                    condition["id"]
                )
                is not None
                for condition in axes
            )
        ]
        if len(eligible_models) >= 2:
            break
        axes.pop()
    if len(axes) < 3 or len(eligible_models) < 2:
        return '<div class="rankingUnavailable">' + bilingual(
            "至少需要 3 类工况和 2 个数据完整的产品，当前仅展示下方热力矩阵。",
            "At least three work conditions and two products with complete comparable data are required; use the heatmap below for the available evidence.",
            "b",
        ) + "</div>"

    size = 560
    center = size / 2
    count = len(axes)
    rings = []
    for level in (20, 40, 60, 80, 100):
        points = [radar_point(index, level, count, size) for index in range(count)]
        rings.append(
            '<polygon class="radar-grid" points="'
            + " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
            + '"></polygon>'
        )
    axes_svg = []
    labels = []
    for index, condition in enumerate(axes):
        x, y = radar_point(index, 100, count, size)
        lx, ly = radar_point(index, 124, count, size)
        zh, en = CONDITION_SHORT[condition["id"]]
        axes_svg.append(
            f'<line class="radar-axis" x1="{center}" y1="{center}" x2="{x:.1f}" y2="{y:.1f}"></line>'
        )
        labels.append(
            f'<text class="radar-label" x="{lx:.1f}" y="{ly:.1f}" data-en="{esc(en)}">{esc(zh)}</text>'
        )

    colors = ["#f5b400", "#0060aa", "#218c74", "#d9534f", "#7656c9", "#1aa6b7", "#8799aa", "#94335b", "#2e7d4f"]
    series = []
    legend = []
    for model_index, model in enumerate(eligible_models):
        record = get_score_record(scoring, model.display_name)
        values = [record["condition_scores"][condition["id"]] for condition in axes]
        points = [radar_point(index, value, count, size) for index, value in enumerate(values)]
        color = colors[model_index % len(colors)]
        series.append(
            f'<polygon class="radar-series selected" data-product="{esc(model.display_name)}" '
            f'style="--series-color:{color}" points="'
            + " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
            + '"></polygon>'
        )
        legend.append(
            f'<button type="button" class="selected" data-product="{esc(model.display_name)}" aria-pressed="true">'
            f'<i style="background:{color}"></i>{esc(model.display_name)}</button>'
        )
    return (
        '<div class="radarBox craneConditionOverviewRadar"><div class="radarHead">'
        + bilingual("高覆盖工况雷达", "High-Coverage Work-Condition Radar", "h3")
        + bilingual("当前：全部可比品牌", "Current: All Comparable Brands", "span", "radarCurrent")
        + '</div><p class="chartScope" data-en="The radar uses only conditions with complete comparable values for every plotted product. All applicable conditions remain in the heatmap.">雷达图仅使用图中各产品均有完整可比值的工况；全部适用工况仍在热力矩阵中展示。</p>'
        + f'<svg class="radarSvg" viewBox="0 0 {size} {size}" role="img">'
        + "".join(rings + axes_svg + labels + series)
        + '</svg><div class="radarLegend">'
        + "".join(legend)
        + "</div></div>"
    )


def _heat_class(score: float | None) -> str:
    if score is None:
        return "missing"
    if score >= 75:
        return "good"
    if score >= 55:
        return "mid"
    return "low"


def render_condition_heatmap(sheet: Any, scoring: dict[str, Any]) -> str:
    applicable = [condition for condition in CONDITIONS if condition_applicable(sheet, condition)]
    ranking_by_condition = {
        condition["id"]: _condition_comparison_rows(sheet, scoring, condition)
        for condition in applicable
    }
    headers = []
    for index, condition in enumerate(applicable, 1):
        zh, en = CONDITION_SHORT[condition["id"]]
        headers.append(
            f'<a href="#cond{index}" title="{esc(condition["title_zh"])}" data-en="{esc(en)}">{esc(zh)}</a>'
        )
    rows = []
    for model in sheet.models:
        record = get_score_record(scoring, model.display_name)
        cells = []
        for condition in applicable:
            zh, en = CONDITION_SHORT[condition["id"]]
            ranked = ranking_by_condition[condition["id"]]
            rank = next(
                (index for index, item in enumerate(ranked, 1) if item["product"] == model.display_name),
                None,
            )
            score = record["condition_scores"].get(condition["id"]) if ranked else None
            detail = record["condition_details"].get(condition["id"], {})
            coverage = float(detail.get("coverage") or 0)
            if score is None:
                value = "—"
                status_zh = "不排名"
                status_en = "Not ranked"
            else:
                value = f"{score:.1f}"
                status_zh = f"第{rank}" if rank else "可比"
                status_en = f"No. {rank}" if rank else "Comparable"
            cells.append(
                f'<span class="conditionHeatCell {_heat_class(score)}" title="{esc(zh)} · 覆盖 {coverage * 100:.0f}%">'
                f'<em data-en="{esc(en)}">{esc(zh)}</em><b>{value}</b><small data-en="{esc(status_en)}">{esc(status_zh)}</small></span>'
            )
        row_class = " xcmg" if model.is_xcmg else ""
        rows.append(
            f'<div class="conditionHeatmapRow{row_class}"><strong>{esc(model.display_name)}</strong>'
            + "".join(cells)
            + "</div>"
        )
    return (
        f'<div class="conditionHeatmap" style="--condition-count:{len(applicable)}">'
        '<div class="conditionHeatmapHeader"><strong data-en="Product">产品</strong>'
        + "".join(headers)
        + "</div>"
        + "".join(rows)
        + '</div><p class="conditionHeatmapNote" data-en="Green indicates a stronger comparable result, yellow the middle band, red a weaker result, and gray means the evidence is insufficient for ranking. Unrecorded values are never treated as zero.">绿色表示可比结果较强，黄色表示中间区间，红色表示相对较弱；灰色表示证据不足，资料未记录，不按0分处理。</p>'
    )


def render_condition_overview_cards(sheet: Any, scoring: dict[str, Any]) -> str:
    applicable = [condition for condition in CONDITIONS if condition_applicable(sheet, condition)]
    xcmg = next(model for model in sheet.models if model.is_xcmg)
    xrecord = get_score_record(scoring, xcmg.display_name)
    cards: dict[str, list[str]] = {"capability": [], "application": []}
    for index, condition in enumerate(applicable, 1):
        ranked = _condition_comparison_rows(sheet, scoring, condition)
        rank = next((position for position, item in enumerate(ranked, 1) if item["is_xcmg"]), None)
        score = xrecord["condition_scores"].get(condition["id"])
        detail = xrecord["condition_details"].get(condition["id"], {})
        if rank and score is not None:
            leader = ranked[0]
            gap = max(0.0, leader["condition_scores"][condition["id"]] - score)
            position_zh = f"第 {rank} / {len(ranked)} · 距首位 {gap:.1f} 分"
            position_en = f"No. {rank} of {len(ranked)} · {gap:.1f} points behind leader"
            value = f"{score:.1f}"
        else:
            position_zh = "证据不足，暂不排名"
            position_en = "Insufficient evidence for ranking"
            value = "—"
        metric_names = list(condition_metric_weights(sheet, condition))[:3]
        config_names = list(condition_config_weights(sheet, condition))[:2]
        key_zh = "、".join(METRIC_ZH.get(name, name) for name in metric_names) or "无可比参数"
        key_en = ", ".join(METRIC_EN.get(name, name) for name in metric_names) or "No comparable specifications"
        config_zh = "、".join(CONFIG_ZH.get(name, name) for name in config_names) or "无明确配置项"
        config_en = ", ".join(CONFIG_EN.get(name, name) for name in config_names) or "No explicit equipment items"
        title_zh, title_en = CONDITION_SHORT[condition["id"]]
        group = condition.get("group", "capability")
        cards.setdefault(group, []).append(
            f'<a class="conditionOverviewCard" data-condition-group="{esc(group)}" href="#cond{index}"><header><span>{index:02d}</span>'
            f'<h3 data-en="{esc(title_en)}">{esc(title_zh)}</h3><b>{value}</b></header>'
            f'<p data-en="{esc(position_en)}">{esc(position_zh)}</p>'
            f'<dl><div><dt data-en="Key specifications">关键参数</dt><dd data-en="{esc(key_en)}">{esc(key_zh)}</dd></div>'
            f'<div><dt data-en="Beneficial equipment">有益配置</dt><dd data-en="{esc(config_en)}">{esc(config_zh)}</dd></div></dl>'
            f'<small data-en="Specification coverage {float(detail.get("parameter_coverage") or 0) * 100:.0f}% · Equipment coverage {float(detail.get("configuration_coverage") or 0) * 100:.0f}%">参数覆盖 {float(detail.get("parameter_coverage") or 0) * 100:.0f}% · 配置覆盖 {float(detail.get("configuration_coverage") or 0) * 100:.0f}%</small></a>'
        )
    groups = []
    for group, title_zh, title_en, note_zh, note_en in (
        (
            "capability",
            "工程能力工况",
            "Engineering Capability Conditions",
            "按单一作业能力拆解参数、配置、排名和差距。",
            "Decomposes specifications, equipment, ranking and gaps by engineering capability.",
        ),
        (
            "application",
            "典型施工场景",
            "Typical Application Scenarios",
            "把多个工程能力组合到真实任务中；属于纸面适配性对比，不替代现场试吊。",
            "Combines multiple engineering capabilities into real tasks; this is a paper-based fit comparison and does not replace a site lift trial.",
        ),
    ):
        if not cards.get(group):
            continue
        groups.append(
            f'<div class="conditionOverviewGroup" data-condition-group="{esc(group)}"><div class="conditionOverviewGroupHead">'
            f'<h3 data-en="{esc(title_en)}">{esc(title_zh)}</h3><p data-en="{esc(note_en)}">{esc(note_zh)}</p></div>'
            f'<div class="conditionOverviewCards">{"".join(cards[group])}</div></div>'
        )
    return "".join(groups)


def render_condition_overview(sheet: Any, scoring: dict[str, Any]) -> str:
    return (
        '<section id="condition-overview"><h2 data-en="Work-Condition Competitive Panorama">工况竞争全景</h2>'
        '<p class="sectionLead" data-en="The heatmap covers every applicable work condition and product. The radar uses only complete comparable data, followed by condition cards that expose ranking eligibility, key inputs and source coverage before the detailed sections.">热力矩阵覆盖全部适用工况和全部产品；雷达仅使用完整可比数据。工况卡片先说明排名资格、关键输入和资料覆盖，再进入逐工况参数、配置、差距与提升模拟。</p>'
        '<div class="conditionMethodology"><b data-en="Interpretation boundary">阅读边界</b><div>'
        '<p data-en="Application scenarios combine traceable specifications and equipment into a paper-based fit comparison. They do not replace a site lift plan, matched load-chart review or field trial.">本场景将可追溯参数与配置组合为纸面适配性对比，不替代现场吊装方案、同口径载荷表复核或实机验证。</p>'
        '<p data-en="Contribution points show only the input effect under the current work-condition weighting and are not a stand-alone machine-performance conclusion. Improvement simulations use only existing comparable inputs; missing evidence, engineering feasibility and cost are never assumed.">贡献分仅表示该指标在当前工况权重下的作用，不等于整机性能的独立结论；提升模拟只使用已有可比字段，不自动假设缺失数据、工程可行性或成本。</p></div></div>'
        '<div class="conditionOverviewGrid"><article class="panel">'
        + render_condition_overview_radar(sheet, scoring)
        + '</article><article class="panel conditionHeatmapPanel"><h3 data-en="Product by Work-Condition Heatmap">产品 × 工况热力矩阵</h3>'
        + render_condition_heatmap(sheet, scoring)
        + "</article></div>"
        + render_condition_overview_cards(sheet, scoring)
        + render_class_field_evaluation(sheet)
        + render_condition_gap_ledger(sheet, scoring)
        + "</section>"
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
    return condition_display_metric_names(sheet, condition)


def relevant_config_names(sheet: Any, condition: dict[str, Any]) -> list[str]:
    return list(condition_config_weights(sheet, condition))


def concrete_gaps(sheet: Any, scoring: dict[str, Any], condition: dict[str, Any]) -> list[tuple[str, str]]:
    xcmg = next(model for model in sheet.models if model.is_xcmg)
    findings = []
    for name in condition_metric_weights(sheet, condition):
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
                best_zh, best_en, best_unit = metric_value(best[2].raw_value, best[2].unit)
                best_suffix = f" {best_unit}" if best_unit else ""
                explicit_none = bool(x_metric and str(x_metric.raw_value).strip().lower() == "none")
                x_zh = "明确记录为无" if explicit_none else "资料未记录"
                x_en = "explicitly records none" if explicit_none else "is not recorded"
                zh = f"{METRIC_ZH.get(name, name)}：XCMG {x_zh}；{best[1].display_name} 为 {best_zh}{best_suffix}。"
                en = f"{METRIC_EN.get(name, name)}: XCMG {x_en}; {best[1].display_name} records {best_en}{best_suffix}."
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
        unit = (x_metric.unit or "").strip()
        x_value = f"{fmt_number(x_metric.raw_value)} {unit}".strip()
        benchmark_value = f"{fmt_number(best[2].raw_value)} {(best[2].unit or unit).strip()}".strip()
        delta_value = f"{fmt_number(delta)} {unit}".strip()
        zh = (
            f"{METRIC_ZH.get(name, name)}：XCMG {x_value}，"
            f"{best[1].display_name} {benchmark_value}，"
            f"标杆在当前评价方向上{qualifier_zh}约 {delta_value}。"
        )
        en = (
            f"{METRIC_EN.get(name, name)}: XCMG {x_value}; "
            f"{best[1].display_name} {benchmark_value}; "
            f"the benchmark is approximately {delta_value} {qualifier_en} in the evaluated direction."
        )
        findings.append((zh, en))
    return findings[:4]


def render_class_field_evaluation(sheet: Any) -> str:
    grouped: dict[str, dict[str, Any]] = {}
    for condition in CONDITIONS:
        if not condition_applicable(sheet, condition):
            continue
        observation = field_observation(sheet.label, condition["id"])
        if not observation:
            continue
        item = grouped.setdefault(
            observation["zh"],
            {"zh": observation["zh"], "en": observation["en"], "conditions": []},
        )
        item["conditions"].append((condition["title_zh"], condition["title_en"]))
    if not grouped:
        return ""

    rows = []
    for index, item in enumerate(grouped.values(), 1):
        conditions_zh = "、".join(value[0] for value in item["conditions"])
        conditions_en = ", ".join(value[1] for value in item["conditions"])
        rows.append(
            '<article><span>' + f'{index:02d}' + '</span><div>'
            f'<p data-en="{esc(item["en"])}">{esc(item["zh"])}</p>'
            f'<small data-en="Related conditions: {esc(conditions_en)}">关联工况：{esc(conditions_zh)}</small>'
            '</div></article>'
        )
    return (
        '<section class="classFieldEvaluation"><header><div>'
        '<h3 data-en="Field-Evaluation Findings for This Class">本吨级实机评价结论</h3>'
        '<p data-en="Repeated observations are consolidated here once and linked to the conditions they affect.">'
        '同一实机观察只在此汇总一次，并标明影响的工况，避免在逐工况分析中重复出现。</p></div>'
        f'<b data-en="{len(rows)} distinct findings">{len(rows)} 项独立结论</b></header>'
        f'<div class="classFieldEvaluationGrid">{"".join(rows)}</div></section>'
    )


def render_condition_gap_ledger(sheet: Any, scoring: dict[str, Any]) -> str:
    grouped: dict[str, dict[str, Any]] = {}
    for condition in CONDITIONS:
        if not condition_applicable(sheet, condition):
            continue
        for gap_zh, gap_en in concrete_gaps(sheet, scoring, condition):
            item = grouped.setdefault(
                gap_zh,
                {"zh": gap_zh, "en": gap_en, "conditions": []},
            )
            item["conditions"].append((condition["title_zh"], condition["title_en"]))
    if not grouped:
        return ""

    rows = []
    for index, item in enumerate(grouped.values(), 1):
        conditions_zh = "、".join(value[0] for value in item["conditions"])
        conditions_en = ", ".join(value[1] for value in item["conditions"])
        rows.append(
            f'<tr><td>{index:02d}</td><td data-en="{esc(item["en"])}">{esc(item["zh"])}</td>'
            f'<td data-en="{esc(conditions_en)}">{esc(conditions_zh)}</td></tr>'
        )
    return (
        '<section class="conditionGapLedger"><header><div>'
        '<h3 data-en="XCMG Verified Gap Register">XCMG 可核验差距台账</h3>'
        '<p data-en="Each distinct gap is listed once. The final column shows every work condition affected by the same engineering limitation.">'
        '每项独立差距只列一次，右侧集中标明同一工程限制影响的全部工况。</p></div>'
        f'<b data-en="{len(rows)} distinct gaps">{len(rows)} 项独立差距</b></header>'
        '<div class="tableScroll"><table><thead><tr><th>#</th>'
        '<th data-en="Verified specification gap">可核验参数差距</th>'
        '<th data-en="Affected work conditions">影响工况</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div></section>'
    )


def condition_ranking_rows(sheet: Any, scoring: dict[str, Any], condition: dict[str, Any]) -> list[dict[str, Any]]:
    if "suspected_rt130_competitor_headers" in sheet.anomalies:
        return []
    rows = [
        item for item in scoring["products"]
        if item["condition_scores"].get(condition["id"]) is not None
    ]
    rows.sort(key=lambda item: item["condition_scores"][condition["id"]], reverse=True)
    return rows if len(rows) >= 2 else []


def condition_component_effect(name: str, item_type: str) -> tuple[str, str]:
    if item_type == "configuration":
        effects = {
            "Tow hooks": ("支持牵引救援与转场组织。", "Supports recovery towing and relocation logistics."),
            "Cribbing rack": ("便于随车携带垫木并缩短支腿准备时间。", "Carries outrigger cribbing on the crane and reduces setup time."),
            "Tires": ("轮胎型式影响松软地面牵引、承载与道路适配。", "Tire selection affects soft-ground traction, load support and road suitability."),
            "Tires options": ("轮胎选项用于匹配道路、场地与轴荷要求。", "Tire options match road, site and axle-load requirements."),
            "360deg house lock": ("稳定上车运输或特定调位状态。", "Secures the upperstructure for transport or defined positioning states."),
            "Auto winch and boom control": ("降低复合动作负荷并提高重复循环一致性。", "Reduces combined-motion workload and improves repeat-cycle consistency."),
            "heavy CWT": ("扩大重载和远幅度载荷表能力。", "Extends heavy-lift and long-radius load-chart capability."),
            "Short Jib": ("补充受限高度与近中幅副臂任务覆盖。", "Adds jib coverage where height or radius is constrained."),
            "Short heavy lift Jib": ("强化近幅副臂重载与越障作业。", "Strengthens short-jib heavy lifting and obstacle-clearance work."),
            "2deg out of level load charts": ("给出倾斜地面下可执行的载荷边界。", "Provides an executable load boundary for out-of-level ground."),
            "Auto Lubrication system": ("减少班次内人工润滑和维护停机。", "Reduces manual lubrication and maintenance downtime during a shift."),
            "Fuel engine heater": ("改善低温启动与热机时间。", "Improves cold starting and warm-up time."),
            "Cold weather package": ("覆盖低温环境下的系统与操作准备。", "Provides system and operating preparation for cold-weather duty."),
            "Greasless boom": ("降低主臂维护频次和污染风险。", "Reduces boom maintenance frequency and contamination risk."),
        }
        return effects.get(name, ("影响该工况的配置完整度与执行便利性。", "Affects equipment completeness and execution convenience in this work condition."))

    lower = name.lower()
    if "transport weight" in lower or "weight per axle" in lower:
        return "决定道路许可、拖车组合和轴荷余量。", "Determines road permits, trailer selection and axle-load margin."
    if "transport width" in lower or "transport height" in lower or "transport length" in lower:
        return "决定路线限制、超限许可与运输组织难度。", "Determines route restrictions, oversize permits and transport complexity."
    if "cwt" in lower or "counterweight" in lower:
        return "影响运输拆分、到场装配和可用载荷表。", "Affects transport split, site assembly and available load charts."
    if name == "Speed" or "speed with max cwt" in lower:
        return "影响场内转场或带配重移动效率。", "Affects on-site relocation or travel efficiency with counterweight."
    if "turning radius" in lower or "steering modes" in lower:
        return "决定受限通道内调头和精准就位能力。", "Determines turning and precision positioning in constrained access."
    if "gradability" in lower or "approach angle" in lower:
        return "决定坡道、坑洼和未铺装地面的通过边界。", "Defines mobility limits on grades, breakovers and unprepared ground."
    if "tail swing" in lower or "retracted boom" in lower:
        return "决定回转与调位所需的安全包络。", "Defines the safe envelope required for swing and positioning."
    if "main boom @" in lower or "maximum capacity" in lower:
        return "直接定义对应幅度下的可吊重量。", "Directly defines liftable load at the stated radius."
    if "jib w/o inserts" in lower:
        return "定义副臂对应幅度的载荷与覆盖边界。", "Defines jib capacity and coverage at the stated radius."
    if "extended boom" in lower or "max rated radius" in lower or "max jib" in lower:
        return "决定高空、越障和远幅任务的几何覆盖。", "Defines geometric coverage for high, obstructed and long-radius work."
    if "winch" in lower and "pull" in lower:
        return "影响起升能力、倍率选择和重载启动。", "Affects hoisting capability, reeving selection and heavy-load pickup."
    if "winch" in lower and "speed" in lower:
        return "影响起升与空钩返回的循环时间。", "Affects lifting and empty-hook return cycle time."
    if "boom raise" in lower or "boom extend" in lower or "swing speed" in lower:
        return "影响臂架准备、回转和整机循环效率。", "Affects boom setup, swing and overall cycle productivity."
    if "outrigger" in lower:
        return "影响支撑包络、场地占用和支腿布置灵活性。", "Affects support envelope, site footprint and outrigger setup flexibility."
    if "tire size" in lower:
        return "影响地面接触、承载、转场速度和松软场地适配。", "Affects ground contact, load support, travel speed and soft-ground suitability."
    if "diff locks" in lower or "interaxle lock" in lower:
        return "影响低附着路面与未铺装场地的牵引通过能力。", "Affects traction and mobility on low-grip or unprepared ground."
    if "asymmetric outrigger" in lower:
        return "决定受限场地非对称支腿布置是否有明确作业边界。", "Determines whether asymmetric outrigger setup has a defined operating boundary in confined sites."
    if "outrigger penetration" in lower:
        return "用于评估支腿反力、地基承载与垫板配置风险。", "Supports assessment of outrigger reaction, ground bearing and cribbing risk."
    if "on tires" in lower or "pick and carry" in lower:
        return "定义轮胎支撑或带载行驶时的可执行载荷边界。", "Defines executable load limits for on-tire or pick-and-carry operation."
    if "engine" in lower or "fuel tank" in lower:
        return "影响动力储备、长班次续航和环境适应性。", "Affects power reserve, long-shift endurance and environmental readiness."
    return "作为当前工况的量化输入，并与同吨级竞品按同一方向比较。", "Used as a quantified input for this work condition and compared consistently within the tonnage class."


def condition_component_definitions(scoring: dict[str, Any], condition: dict[str, Any]) -> list[dict[str, Any]]:
    for product in scoring["products"]:
        detail = product["condition_details"].get(condition["id"], {})
        if detail.get("components"):
            return sorted(
                detail["components"],
                key=lambda item: (-item["effective_weight"], item["type"], item["name"]),
            )
    return []


def record_component(record: dict[str, Any], condition_id: str, item_type: str, name: str) -> dict[str, Any] | None:
    return next(
        (
            item
            for item in record["condition_details"].get(condition_id, {}).get("components", [])
            if item["type"] == item_type and item["name"] == name
        ),
        None,
    )


def render_condition_radar(sheet: Any, scoring: dict[str, Any], condition: dict[str, Any]) -> str:
    components = [
        item
        for item in condition_component_definitions(scoring, condition)
        if sum(
            record_component(record, condition["id"], item["type"], item["name"])["score"] is not None
            for record in scoring["products"]
            if record_component(record, condition["id"], item["type"], item["name"])
        ) >= 2
    ][:8]
    if len(components) < 3:
        return '<div class="rankingUnavailable">' + bilingual(
            "可比指标少于 3 项，保留原值表，不绘制雷达图。",
            "Fewer than three comparable inputs are available. Source values remain visible, but no radar is drawn.",
            "b",
        ) + "</div>"

    size = 500
    center = size / 2
    count = len(components)
    rings = []
    for level in (20, 40, 60, 80, 100):
        points = [radar_point(index, level, count, size) for index in range(count)]
        rings.append('<polygon class="radar-grid" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in points) + '"></polygon>')
    axes = []
    labels = []
    for index, component in enumerate(components):
        x, y = radar_point(index, 100, count, size)
        lx, ly = radar_point(index, 122, count, size)
        if component["type"] == "metric":
            zh, en = METRIC_ZH.get(component["name"], component["name"]), METRIC_EN.get(component["name"], component["name"])
        else:
            zh, en = CONFIG_ZH.get(component["name"], component["name"]), CONFIG_EN.get(component["name"], component["name"])
        axes.append(f'<line class="radar-axis" x1="{center}" y1="{center}" x2="{x:.1f}" y2="{y:.1f}"></line>')
        labels.append(f'<text class="radar-label" x="{lx:.1f}" y="{ly:.1f}" data-en="{esc(en)}">{esc(zh)}</text>')

    colors = ["#f5b400", "#0060aa", "#218c74", "#d9534f", "#7656c9", "#1aa6b7", "#8799aa", "#94335b", "#2e7d4f"]
    series = []
    legend = []
    for model_index, model in enumerate(sheet.models):
        record = get_score_record(scoring, model.display_name)
        values = []
        for component in components:
            item = record_component(record, condition["id"], component["type"], component["name"])
            values.append(item["score"] if item else None)
        if sum(value is not None for value in values) < 3:
            continue
        points = [radar_point(index, value or 0, count, size) for index, value in enumerate(values)]
        color = colors[model_index % len(colors)]
        series.append(
            f'<polygon class="radar-series selected" data-product="{esc(model.display_name)}" style="--series-color:{color}" points="'
            + " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
            + '"></polygon>'
        )
        legend.append(
            f'<button type="button" class="selected" data-product="{esc(model.display_name)}" aria-pressed="true"><i style="background:{color}"></i>{esc(model.display_name)}</button>'
        )
    if not series:
        return '<div class="rankingUnavailable">' + bilingual(
            "产品间有效字段不足，暂不绘制雷达图。",
            "Verified cross-product coverage is insufficient for a radar comparison.",
            "b",
        ) + "</div>"
    return (
        '<div class="radarBox craneConditionRadar"><div class="radarHead">'
        + bilingual("关键参数 / 配置对比", "Key Specification and Equipment Comparison", "h3")
        + bilingual("当前：全部品牌", "Current: All Brands", "span", "radarCurrent")
        + f'</div><svg class="radarSvg" viewBox="0 0 {size} {size}" role="img">'
        + "".join(rings + axes + labels + series)
        + '</svg><div class="radarLegend">' + "".join(legend) + "</div></div>"
    )


def render_condition_component_cell(component: dict[str, Any] | None) -> str:
    if not component:
        return '<td class="missing">—</td>'
    score = component.get("score")
    if score is None:
        cls = "missing"
    elif score >= 75:
        cls = "good"
    elif score >= 45:
        cls = "mid"
    else:
        cls = "bad"
    if component["type"] == "metric":
        raw_html = render_metric_value(component.get("raw_value"), component.get("unit"), "b")
    else:
        status_copy = {
            "standard": ("标配", "Standard"),
            "optional": ("选配", "Optional"),
            "absent": ("无配置", "Not available"),
            "present_unspecified": ("有配置，状态未注明", "Available; status unspecified"),
            "unrecorded": ("资料未记录", "Data not recorded"),
        }
        zh, en = status_copy.get(component.get("status"), ("资料未记录", "Data not recorded"))
        raw_html = f'<b data-en="{esc(en)}">{esc(zh)}</b>'
    score_text = "—" if score is None else f"{score:.1f}"
    contribution = component.get("contribution")
    contribution_text = "—" if contribution is None else f"{contribution:.1f}"
    return (
        f'<td class="{cls}">{raw_html}'
        f'<span data-en="Input score {score_text}">指标分 {score_text}</span>'
        f'<small data-en="Weighted contribution {contribution_text}">加权贡献 {contribution_text}</small></td>'
    )


def render_condition_contribution(sheet: Any, scoring: dict[str, Any], condition: dict[str, Any]) -> str:
    components = condition_component_definitions(scoring, condition)
    context_names = [name for name in relevant_metric_names(sheet, condition) if name not in {item["name"] for item in components}]
    rows = []
    for component in components:
        type_zh, type_en = ("参数", "Specification") if component["type"] == "metric" else ("配置", "Equipment")
        label = metric_label(component["name"]) if component["type"] == "metric" else config_label(component["name"])
        effect_zh, effect_en = condition_component_effect(component["name"], component["type"])
        cells = "".join(
            render_condition_component_cell(record_component(record, condition["id"], component["type"], component["name"]))
            for record in scoring["products"]
        )
        rows.append(
            f'<tr><td data-en="{type_en}">{type_zh}</td><th scope="row">{label}</th>'
            f'<td>{component["effective_weight"] * 100:.1f}%</td><td data-en="{esc(effect_en)}">{esc(effect_zh)}</td>{cells}</tr>'
        )
    for name in context_names:
        effect_zh, effect_en = condition_component_effect(name, "metric")
        cells = []
        for model in sheet.models:
            metric = model_metric(model, name)
            value = render_metric_value(metric.raw_value, metric.unit, "b") if metric else "—"
            cells.append(f'<td class="contextOnly">{value}<span data-en="Reference only">仅作参考</span></td>')
        rows.append(
            '<tr><td data-en="Reference">参考项</td><th scope="row">' + metric_label(name)
            + '</th><td>0%</td><td data-en="' + esc(effect_en) + '">' + esc(effect_zh) + '</td>' + "".join(cells) + '</tr>'
        )
    if not rows:
        return ""
    model_headers = "".join(
        f'<th class="{"xcmgHead" if model.is_xcmg else ""}">{esc(model.display_name)}</th>'
        for model in sheet.models
    )
    return (
        '<div class="conditionContribution"><div class="conditionContributionHead">'
        + bilingual("全部指标 / 配置贡献明细", "Complete Input and Equipment Contribution Detail", "h3")
        + '</div><div class="tableScroll conditionContributionTable"><table><thead><tr>'
        + bilingual("类型", "Type", "th") + bilingual("指标 / 配置", "Input / Equipment", "th")
        + bilingual("工况权重", "Work-Condition Weight", "th") + bilingual("对工况影响", "Effect on Work Condition", "th")
        + model_headers + '</tr></thead><tbody>' + "".join(rows) + '</tbody></table></div></div>'
    )


def render_condition_simulator(sheet: Any, scoring: dict[str, Any], condition: dict[str, Any]) -> str:
    xcmg = next(record for record in scoring["products"] if record["is_xcmg"])
    base = xcmg["condition_scores"].get(condition["id"])
    ranking = condition_ranking_rows(sheet, scoring, condition)
    if base is None or not ranking:
        return ""
    candidates = []
    for component in xcmg["condition_details"][condition["id"]]["components"]:
        score = component.get("score")
        if score is None:
            continue
        benchmarks = []
        for record in scoring["products"]:
            if record["is_xcmg"]:
                continue
            rival_component = record_component(record, condition["id"], component["type"], component["name"])
            if rival_component and rival_component.get("score") is not None:
                benchmarks.append((rival_component["score"], record["product"], rival_component))
        if not benchmarks:
            continue
        best_score, best_product, best_component = max(benchmarks, key=lambda item: item[0])
        delta = max(0.0, (best_score - score) * component["effective_weight"])
        if delta < 0.5:
            continue
        if component["type"] == "metric":
            label_zh = f"{METRIC_ZH.get(component['name'], component['name'])}达到标杆"
            label_en = f"Match benchmark: {METRIC_EN.get(component['name'], component['name'])}"
            best_value_zh, best_value_en, unit = metric_value(best_component.get("raw_value"), best_component.get("unit"))
            suffix = f" {unit}" if unit else ""
            current_value = f"{fmt_number(component.get('raw_value'))} {(component.get('unit') or '').strip()}".strip()
            note_zh = f"当前 {current_value}；{best_product} {best_value_zh}{suffix}"
            note_en = f"Current {current_value}; {best_product} {best_value_en}{suffix}"
        else:
            label_zh = f"{CONFIG_ZH.get(component['name'], component['name'])}提升至标配"
            label_en = f"Make standard: {CONFIG_EN.get(component['name'], component['name'])}"
            note_zh = f"按源表状态由当前配置提升至当前标杆的明确状态；标杆为 {best_product}。"
            note_en = f"Moves the recorded equipment status to the verified benchmark state represented by {best_product}."
        candidates.append((delta, label_zh, label_en, note_zh, note_en))
    candidates.sort(reverse=True, key=lambda item: item[0])
    candidates = candidates[:8]
    if not candidates:
        return ""
    options = "".join(
        f'<label><input type="checkbox" data-delta="{delta:.3f}"><span><b data-en="{esc(label_en)}">{esc(label_zh)}</b>'
        f'<em data-en="Estimated work-condition gain +{delta:.1f}">预计工况分 +{delta:.1f}</em><small data-en="{esc(note_en)}">{esc(note_zh)}</small></span></label>'
        for delta, label_zh, label_en, note_zh, note_en in candidates
    )
    rivals = "|".join(
        f"{record['product']}:{record['condition_scores'][condition['id']]:.4f}"
        for record in ranking
        if not record["is_xcmg"]
    )
    return (
        f'<div class="simulator craneConditionSimulator" data-base="{base:.4f}" data-xcmg="{esc(xcmg["product"])}" data-rivals="{esc(rivals)}">'
        '<div class="simHead">' + bilingual("XCMG 工况提升模拟", "XCMG Work-Condition Improvement Simulator", "h3")
        + '<button type="button" class="resetSim" data-en="Reset selections">恢复当前</button></div>'
        + '<div class="simGrid"><div class="simOptions">' + options
        + f'</div><div class="simResult"><strong>{base:.1f}</strong><span data-en="Simulated work-condition score">模拟工况分</span><b data-en="Current position">当前位置</b><small></small></div></div><div class="rankPanel"></div></div>'
    )


def render_action_plan(sheet: Any, scoring: dict[str, Any]) -> str:
    xcmg = next(model for model in sheet.models if model.is_xcmg)
    cards = []
    for condition in CONDITIONS:
        if not condition_applicable(sheet, condition):
            continue
        eligible = condition_ranking_rows(sheet, scoring, condition)
        rank = next((index for index, item in enumerate(eligible, 1) if item["is_xcmg"]), None)
        leader = eligible[0] if eligible else None
        xrecord = get_score_record(scoring, xcmg.display_name)
        xscore = xrecord["condition_scores"].get(condition["id"])
        if rank and leader and xscore is not None:
            gap = max(0.0, leader["condition_scores"][condition["id"]] - xscore)
            position_zh = f"第 {rank} / {len(eligible)}；距 {leader['product']} {gap:.1f} 分"
            position_en = f"No. {rank} of {len(eligible)}; {gap:.1f} points behind {leader['product']}"
        else:
            position_zh = "有效字段不足，暂不形成位置判断"
            position_en = "Insufficient verified fields for a position assessment"
        findings = concrete_gaps(sheet, scoring, condition)
        if findings:
            gap_zh, gap_en = findings[0]
        else:
            gap_zh = "未发现可量化的明显落后项；优先补齐缺失字段并复核同工况载荷口径。"
            gap_en = "No clear measurable disadvantage is visible; complete missing fields and verify like-for-like load-chart conditions first."
        action_zh, action_en = CONDITION_ACTIONS[condition["id"]]
        cards.append(
            '<article class="craneActionItem">'
            f'<header><h3 data-en="{esc(condition["title_en"])}">{esc(condition["title_zh"])}</h3>'
            f'<span data-en="{esc(position_en)}">{esc(position_zh)}</span></header>'
            '<dl><div>'
            + bilingual("首要量化差距", "Primary Measurable Gap", "dt")
            + f'<dd data-en="{esc(gap_en)}">{esc(gap_zh)}</dd></div><div>'
            + bilingual("工程验证与补强动作", "Engineering Validation and Action", "dt")
            + f'<dd data-en="{esc(action_en)}">{esc(action_zh)}</dd></div></dl></article>'
        )
    return '<div class="craneActionGrid">' + "".join(cards) + '</div>'


def render_condition_execution(sheet: Any, condition: dict[str, Any]) -> str:
    context = CONDITION_EXECUTION.get(condition["id"])
    if not context:
        return ""

    workflow = "".join(
        f'<li><span>{index:02d}</span><p data-en="{esc(item["en"])}">{esc(item["zh"])}</p></li>'
        for index, item in enumerate(context["workflow"], 1)
    )
    constraints = "".join(
        f'<li data-en="{esc(item["en"])}">{esc(item["zh"])}</li>' for item in context["constraints"]
    )
    checks = "".join(
        '<div class="conditionCheckRow">'
        f'<b data-en="{esc(item["item"]["en"])}">{esc(item["item"]["zh"])}</b>'
        f'<p data-en="{esc(item["method"]["en"])}">{esc(item["method"]["zh"])}</p>'
        f'<span data-en="Record: {esc(item["record"]["en"])}">记录：{esc(item["record"]["zh"])}</span>'
        '</div>'
        for item in context["checks"]
    )
    reference_links = []
    for reference_id in context.get("refs", []):
        reference = OFFICIAL_REFERENCES.get(reference_id)
        if not reference:
            continue
        reference_links.append(
            f'<a href="{esc(reference["url"])}" target="_blank" rel="noopener noreferrer" '
            f'data-en="{esc(reference["label"]["en"])}">{esc(reference["label"]["zh"])}</a>'
        )
    references = "".join(reference_links)
    return (
        '<section class="conditionExecution" aria-label="作业执行与工程验证">'
        '<div class="conditionExecutionHeading"><div><b data-en="Job execution and engineering validation">'
        '作业执行与工程验证</b><span data-en="Translate the paper comparison into a repeatable job process">'
        '把纸面对比还原为可复现的现场任务</span></div></div>'
        '<div class="conditionExecutionMeta"><dl><div><dt data-en="Typical customers">典型客户</dt>'
        f'<dd data-en="{esc(context["customer"]["en"])}">{esc(context["customer"]["zh"])}</dd></div>'
        '<div><dt data-en="Typical loads / work objects">典型吊物 / 工作对象</dt>'
        f'<dd data-en="{esc(context["load"]["en"])}">{esc(context["load"]["zh"])}</dd></div></dl></div>'
        '<div class="conditionExecutionGrid"><article class="conditionWorkflow"><h3 data-en="Standard task chain">标准任务链</h3>'
        f'<ol>{workflow}</ol></article><article class="conditionConstraints"><h3 data-en="Site constraints and decision boundary">'
        f'现场约束与判断边界</h3><ul>{constraints}</ul><div class="conditionBoundary"><b data-en="Engineering boundary">工程边界</b>'
        f'<p data-en="{esc(context["boundary"]["en"])}">{esc(context["boundary"]["zh"])}</p></div></article></div>'
        '<div class="conditionVerification"><div class="conditionVerificationTitle"><h3 data-en="Recommended validation record">'
        '建议验证记录</h3><span data-en="Record measured results; do not invent pass thresholds">记录实测结果，不虚构通过阈值</span></div>'
        f'<div class="conditionCheckList">{checks}</div></div>'
        f'<div class="conditionReferenceStrip"><b data-en="Engineering references">工程依据</b>{references}</div>'
        '</section>'
    )


def render_condition(sheet: Any, scoring: dict[str, Any], condition: dict[str, Any], index: int) -> str:
    if not condition_applicable(sheet, condition):
        return ""
    metric_names = relevant_metric_names(sheet, condition)
    config_names = relevant_config_names(sheet, condition)
    score_rows = condition_ranking_rows(sheet, scoring, condition)
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
    xcmg_record = get_score_record(scoring, xcmg.display_name)
    detail = xcmg_record["condition_details"][condition["id"]]

    copy_zh, copy_en = CONDITION_COPY[condition["id"]]
    benefit_zh, benefit_en = CONDITION_BENEFITS[condition["id"]]
    coverage_zh = (
        f"参数覆盖 {detail['parameter_coverage'] * 100:.0f}% / 配置覆盖 {detail['configuration_coverage'] * 100:.0f}%"
    )
    coverage_en = (
        f"Specification coverage {detail['parameter_coverage'] * 100:.0f}% / equipment coverage {detail['configuration_coverage'] * 100:.0f}%"
    )
    simulator = render_condition_simulator(sheet, scoring, condition)
    group = condition.get("group", "capability")
    group_zh = "典型施工场景" if group == "application" else "工程能力工况"
    group_en = "Typical Application Scenario" if group == "application" else "Engineering Capability Condition"
    return (
        f'<section id="cond{index}" class="conditionSection" data-condition-group="{esc(group)}">'
        f'<div class="conditionTitle"><div><span data-en="{esc(group_en)} {index:02d}">{esc(group_zh)} {index:02d}</span>'
        f'<h2 data-en="{esc(condition["title_en"])}">{esc(condition["title_zh"])}</h2></div>'
        f'<em data-en="{len(metric_names)} specifications / {len(config_names)} equipment items">{len(metric_names)} 个参数 / {len(config_names)} 个配置项</em></div>'
        f'<p class="conditionNarrative" data-en="{esc(copy_en)}">{esc(copy_zh)}</p>'
        + render_condition_execution(sheet, condition)
        + '<div class="conditionBrief"><article><b data-en="Beneficial equipment and design features">有益配置与设计特征</b>'
        f'<p data-en="{esc(benefit_en)}">{esc(benefit_zh)}</p></article><article><b data-en="Evaluation composition">评价构成</b>'
        f'<p data-en="Specification share {condition["parameter_share"] * 100:.0f}% and equipment share {condition["configuration_share"] * 100:.0f}%. {esc(coverage_en)}">参数权重 {condition["parameter_share"] * 100:.0f}%，配置权重 {condition["configuration_share"] * 100:.0f}%。{esc(coverage_zh)}</p></article></div>'
        '<div class="conditionAnalysisGrid"><article class="panel conditionRadarPanel">'
        + render_condition_radar(sheet, scoring, condition)
        + '</article><article class="panel conditionRankingPanel"><h3 data-en="Work-condition ranking">工况评分排名</h3>'
        + ranking_html
        + f'<p class="coverageNote" data-en="{esc(coverage_en)}">{esc(coverage_zh)}</p></article></div>'
        + render_condition_contribution(sheet, scoring, condition)
        + '<div class="conditionDecisionGrid">' + simulator + "</div></section>"
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
                cls = "missing" if not metric or metric.raw_value in (None, "") else ""
                value_html = render_metric_value(metric.raw_value, None) if metric else render_metric_value(None)
                cells.append(f'<td class="{cls}">{value_html}</td>')
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
    parameter_ranked = sorted(
        (item for item in scoring["products"] if item["parameter_score"] is not None),
        key=lambda item: item["parameter_score"],
        reverse=True,
    )
    parameter_ranks = {item["product"]: index for index, item in enumerate(parameter_ranked, 1)}
    rows = []
    for model in sheet.models:
        score = get_score_record(scoring, model.display_name)
        if score["parameter_score"] is not None:
            parameter_zh = f"可排名：第 {parameter_ranks[model.display_name]}，{score['parameter_score']:.1f} 分"
            parameter_en = f"Ranked: No. {parameter_ranks[model.display_name]}, {score['parameter_score']:.1f}"
        else:
            parameter_zh = "暂不纳入参数排名"
            parameter_en = "Not included in specification ranking"
        if score["configuration_score"] is not None:
            config_zh = f"可评价：{score['configuration_score']:.1f} 分"
            config_en = f"Eligible: {score['configuration_score']:.1f}"
        else:
            config_zh = "资料不足，暂不评分"
            config_en = "Insufficient source coverage; not scored"
        if score["overall_score"] is not None:
            overall_zh = f"第 {score['overall_rank']}，{score['overall_score']:.1f} 分"
            overall_en = f"No. {score['overall_rank']}, {score['overall_score']:.1f}"
        else:
            overall_zh = "暂不发布"
            overall_en = "Not published"
        rows.append(
            f'<tr class="{ "xcmg-row" if model.is_xcmg else ""}"><th scope="row">{esc(model.display_name)}</th>'
            f'<td>{fmt_percent(model.parameter_coverage)}</td><td data-en="{esc(parameter_en)}">{esc(parameter_zh)}</td>'
            f'<td>{fmt_percent(model.configuration_coverage)}</td><td data-en="{esc(config_en)}">{esc(config_zh)}</td>'
            f'<td data-en="{esc(overall_en)}">{esc(overall_zh)}</td></tr>'
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
        + bilingual("产品", "Product", "th") + bilingual("参数源数据覆盖", "Specification Source Coverage", "th")
        + bilingual("参数排名资格", "Specification Ranking Status", "th")
        + bilingual("配置源数据覆盖", "Equipment Source Coverage", "th")
        + bilingual("配置评价资格", "Equipment Evaluation Status", "th")
        + bilingual("综合排名", "Overall Ranking", "th")
        + '</tr></thead><tbody>' + "".join(rows) + "</tbody></table></div></article>"
        + '<article class="panel"><h3 data-en="Source checks">源数据核验记录</h3><ul class="qualityList">'
        + "".join(anomalies)
        + '</ul><p class="methodNote" data-en="Blank equipment cells remain unknown and are never converted to unavailable or zero. The six-characteristic section is blank in the source workbook and no score is fabricated.">配置空白保留为“资料未记录”，不转换为“无配置”或 0 分；源表“六大特性”区域为空，本页不编造实机评价分数。</p></article></div>'
    )


def render_publication_status(xscore: dict[str, Any]) -> str:
    parameter_ready = xscore["parameter_score"] is not None
    configuration_ready = xscore["configuration_score"] is not None
    overall_ready = xscore["overall_score"] is not None
    items = [
        (
            "参数竞争力",
            "Specification Position",
            "可发布" if parameter_ready else "暂不发布",
            "Published" if parameter_ready else "Not published",
            f"评分权重覆盖 {fmt_percent(xscore['parameter_coverage'])}" if parameter_ready else "XCMG 参数有效覆盖率不足60%",
            f"Evaluation-weight coverage {fmt_percent(xscore['parameter_coverage'])}" if parameter_ready else "Verified XCMG specification coverage is below 60%",
            "ready" if parameter_ready else "hold",
        ),
        (
            "配置竞争力",
            "Equipment Position",
            "可发布" if configuration_ready else "暂不发布",
            "Published" if configuration_ready else "Not published",
            f"配置状态覆盖 {fmt_percent(xscore['configuration_coverage'])}" if configuration_ready else f"配置状态覆盖仅 {fmt_percent(xscore['configuration_coverage'])}",
            f"Equipment-state coverage {fmt_percent(xscore['configuration_coverage'])}" if configuration_ready else f"Equipment-state coverage is only {fmt_percent(xscore['configuration_coverage'])}",
            "ready" if configuration_ready else "hold",
        ),
        (
            "综合总分与排名",
            "Overall Score and Ranking",
            "可发布" if overall_ready else "暂不发布",
            "Published" if overall_ready else "Not published",
            f"综合得分 {xscore['overall_score']:.1f}" if overall_ready else "参数与配置必须同时达到发布门槛",
            f"Overall score {xscore['overall_score']:.1f}" if overall_ready else "Both specification and equipment evidence must meet the publication threshold",
            "ready" if overall_ready else "hold",
        ),
    ]
    return '<div class="publicationGrid">' + "".join(
        f'<article class="publicationItem {cls}"><span data-en="{esc(title_en)}">{esc(title_zh)}</span>'
        f'<b data-en="{esc(status_en)}">{esc(status_zh)}</b><small data-en="{esc(note_en)}">{esc(note_zh)}</small></article>'
        for title_zh, title_en, status_zh, status_en, note_zh, note_en, cls in items
    ) + '</div>'


def page_nav(sheet: Any) -> str:
    applicable_conditions = [condition for condition in CONDITIONS if condition_applicable(sheet, condition)]
    indexed_conditions = list(enumerate(applicable_conditions, 1))
    capability_links = "".join(
        f'<a href="#cond{index}" data-en="{esc(condition["title_en"])}">{esc(condition["title_zh"])}</a>'
        for index, condition in indexed_conditions
        if condition.get("group", "capability") == "capability"
    )
    application_links = "".join(
        f'<a href="#cond{index}" data-en="{esc(condition["title_en"])}">{esc(condition["title_zh"])}</a>'
        for index, condition in indexed_conditions
        if condition.get("group") == "application"
    )
    return (
        '<a class="home" href="arc.html" data-en="Return to Platform Home">返回对标平台主页</a>'
        '<a href="#summary" data-en="Benchmark Overview">对标概览</a>'
        '<a href="#market-context" data-en="Market, Customer and Product Evidence">市场、客户与产品证据</a>'
        '<a href="#class-visuals" data-en="Field Images and Product Details">现场图片与产品细节</a>'
        '<a href="#condition-overview" data-en="Work-Condition Panorama">工况竞争全景</a>'
        '<a href="#position" data-en="Specification Position">参数竞争位置</a>'
        '<details class="navGroup" open><summary data-en="Engineering Conditions">工程能力工况</summary><div class="navSubmenu">'
        + capability_links + '</div></details>'
        '<details class="navGroup" open><summary data-en="Application Scenarios">典型施工场景</summary><div class="navSubmenu">'
        + application_links + '</div></details>'
        '<a href="#actions" data-en="Improvement Actions">补强清单</a>'
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
    crane_type_en = "Rough-Terrain" if sheet.label.startswith("RT-") else "All-Terrain"
    tonnage_en = sheet.tonnage.replace("t", "-USt")
    title_zh = f'{xcmg.display_name} {sheet.tonnage} 起重机竞品对标'
    title_en = f'{xcmg.display_name} {tonnage_en} {crane_type_en} Crane Competitive Benchmark'
    applicable_conditions = [condition for condition in CONDITIONS if condition_applicable(sheet, condition)]
    conditions = "".join(
        render_condition(sheet, scoring, condition, index)
        for index, condition in enumerate(applicable_conditions, 1)
    )
    return f'''<!doctype html>
<html lang="zh-CN" data-language="zh"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title data-en="{esc(title_en)} | XCMG ARC">{esc(title_zh)} | XCMG ARC</title>
<link rel="stylesheet" href="assets/dashboard.css?v=20260805e">
<link rel="stylesheet" href="assets/crane-dashboard.css?v=20260806b">
<link rel="stylesheet" href="assets/crane-insights.css?v=20260806j">
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
</div>{render_publication_status(xscore)}<div class="methodStrip"><b data-en="Evaluation boundary">评价边界</b><p data-en="Specification values use direction-aware normalization within the current tonnage class. Category weights total 100%. Equipment uses 0 for unavailable, 60 for optional and 100 for standard only when status is explicit. Overall scoring is withheld when verified equipment coverage is below 60%.">参数按当前吨级内同口径、方向归一化，八类权重合计 100%；配置仅在状态明确时按无配置 0、选配 60、标配 100 计入。当前配置有效覆盖率低于 60% 时，不生成综合总分和综合排名。</p></div></section>

{render_class_context(sheet.label)}

{render_condition_overview(sheet, scoring)}

<section id="position"><h2 data-en="Specification Position">参数竞争位置</h2><div class="positionGrid"><article class="panel"><h3 data-en="Specification ranking">参数竞争力排名</h3>{render_rank_bars(scoring, 'parameter_score', xcmg.display_name)}</article><article class="panel">{render_category_radar(sheet, scoring)}</article></div>{render_category_table(sheet, scoring)}</section>

<div id="conditions">{conditions}</div>

<section id="actions"><h2 data-en="XCMG Measurable Improvement Actions">XCMG 量化补强清单</h2><p class="sectionLead" data-en="Each row connects the current work-condition position to the largest verified specification gap and the engineering validation required before a design target is approved. These actions are not presented as completed improvements.">逐项把工况竞争位置、最大可核验参数差距和工程验证动作对应起来；以下为验证与产品决策输入，不代表改进已经完成。</p>{render_action_plan(sheet, scoring)}</section>

<section id="parameters"><h2 data-en="Complete Specification Matrix">全部参数明细</h2><p class="sectionLead" data-en="Values are grouped by eight crane engineering systems. Empty cells remain unrecorded and are not treated as zero.">按八类起重机工程系统展示全部参数；空白保留为“资料未记录”，不按 0 值处理。</p>{render_parameter_matrix(sheet)}</section>

<section id="configurations"><h2 data-en="Standard and Optional Equipment Matrix">标配 / 选配明细</h2><p class="sectionLead" data-en="Only explicit source states are classified. A blank cell means the source did not record the status.">仅对源表明确记录的状态进行分类；空白表示资料未记录，不等于无配置。</p>{render_configuration_matrix(sheet)}</section>

<section id="quality"><h2 data-en="Data Quality and Publication Boundary">数据质量与发布边界</h2>{render_quality(sheet, scoring)}</section>

<footer class="dashboardFooter"><small data-en="Executive sponsor: Zhang Shengnan · Data visualization: Liu Chang · Data source: ARC Product Team · Issue reporting: changl@xcmgarc.com">指导领导：张盛楠　数据可视化：刘畅　数据来源：ARC产品小组　问题提报：changl@xcmgarc.com</small></footer>
</main></div><script src="assets/dashboard.js?v=20260805e"></script><script src="assets/i18n.js?v=20260805e"></script><script src="assets/crane-insights.js?v=20260805e"></script>
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
    condition_groups: list[str] = []
    for group, title_zh, title_en, note_zh, note_en in (
        (
            "capability",
            "工程能力工况",
            "Engineering Capability Conditions",
            "按机动、支腿、臂架、起升和循环效率等单项能力建立统一对标口径。",
            "Benchmarks mobility, outriggers, boom geometry, lifting and cycle productivity under one engineering framework.",
        ),
        (
            "application",
            "典型施工场景",
            "Typical Application Scenarios",
            "把多项工程能力组合到城市公用工程、工业检修、桥梁施工、应急抢险和港口料场任务中；结果为纸面适配性，不替代现场试吊。",
            "Combines engineering capabilities for utility, industrial, bridge, emergency and yard tasks; results indicate paper-based fit and do not replace a site lift trial.",
        ),
    ):
        group_cards = "".join(
            f'<article data-condition-group="{esc(group)}"><span>{index:02d}</span><h3 data-en="{esc(condition["title_en"])}">{esc(condition["title_zh"])}</h3><p data-en="{esc(CONDITION_COPY[condition["id"]][1])}">{esc(CONDITION_COPY[condition["id"]][0])}</p></article>'
            for index, condition in enumerate(CONDITIONS, 1)
            if condition.get("group", "capability") == group
        )
        if group_cards:
            condition_groups.append(
                f'<div class="conditionOverviewGroup" data-condition-group="{esc(group)}"><div class="conditionOverviewGroupHead">'
                f'<h3 data-en="{esc(title_en)}">{esc(title_zh)}</h3><p data-en="{esc(note_en)}">{esc(note_zh)}</p></div>'
                f'<div class="conditionFramework">{group_cards}</div></div>'
            )
    condition_cards = "".join(condition_groups)
    return f'''<!doctype html><html lang="zh-CN" data-language="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>起重设备竞品对标总览 | XCMG ARC</title><link rel="stylesheet" href="assets/dashboard.css?v=20260805e"><link rel="stylesheet" href="assets/crane-dashboard.css?v=20260806a"></head><body>
<a class="backTop" href="#top">回到顶部</a><div class="layout" id="top"><aside class="nav"><a class="navBrand" href="arc.html"><img src="assets/xcmg-logo.svg" alt="XCMG"></a><div><div class="navTitle" data-en="Crane Benchmark Overview">起重设备对标总览</div><small>XCMG ARC</small></div><button class="languageToggle" type="button">EN</button><button class="sidebarToggle" type="button"><span>收起侧栏</span></button><button class="navToggle" type="button">页面导航</button><div class="navMenu" id="page-nav"><a class="home" href="arc.html" data-en="Return to Platform Home">返回对标平台主页</a><a href="#portfolio" data-en="Class Assets">吨级资产</a><a href="#framework" data-en="Benchmark Framework">对标框架</a><a href="#method" data-en="Evaluation Boundary">评价边界</a></div></aside><main>
<header class="hero craneOverviewHero"><div class="heroText"><p class="eyebrow">CRANES AND HOISTING</p><h1 data-en="Crane Competitive Benchmarking">起重设备竞品对标</h1><p data-en="Six rough-terrain and all-terrain classes are organized under one engineering framework covering source values, work conditions, equipment status and data-quality boundaries.">覆盖 5 个越野轮胎起重机吨级和 1 个全地面起重机吨级，统一管理参数原值、典型工况、配置状态和数据质量边界。</p><div class="actions"><a class="btn blue" href="#portfolio" data-en="Open Class Assets">查看吨级资产</a><a class="btn" href="{SOURCE_DOWNLOAD}" download data-en="Download Source Workbook">下载原始数据</a></div></div><div class="heroMedia"><img src="assets/arc/category-cranes.webp" alt="XCMG crane"></div></header>
 <section id="portfolio"><h2 data-en="Crane Class Assets">起重机吨级资产</h2><div class="kpis craneKpis"><div class="kpi"><b>6</b><span data-en="Tonnage classes">吨级 / 类别</span></div><div class="kpi"><b>{total_models}</b><span data-en="Benchmark products">对标产品</span></div><div class="kpi"><b>8</b><span data-en="Specification categories">参数类别</span></div><div class="kpi"><b>{len(CONDITIONS)}</b><span data-en="Work conditions">典型工况</span></div></div><div class="craneAssetGrid">{''.join(cards)}</div></section>
<section id="framework"><h2 data-en="Work-Condition Benchmark Framework">工况对标框架</h2><div class="conditionFramework">{condition_cards}</div></section>
<section id="method"><h2 data-en="Evaluation and Data Boundary">评分与数据边界</h2><div class="qualityGrid"><article class="panel"><h3 data-en="Specification evaluation">参数评价</h3><p data-en="Direction-aware normalization is applied within each class. Category weights are transport 10%, chassis and mobility 12%, boom and jib 18%, outriggers 12%, powertrain 8%, winches 10%, lifting performance 25% and speeds 5%.">各吨级内部按指标方向归一化；运输 10%、底盘机动 12%、主副臂 18%、支腿 12%、动力 8%、卷扬 10%、起重性能 25%、速度 5%。</p></article><article class="panel"><h3 data-en="Equipment and missing data">配置与缺失值</h3><p data-en="Explicit unavailable, optional and standard states use 0, 60 and 100. Blank cells remain unrecorded. No overall score is published below 60% verified configuration coverage, and blank six-characteristic rows are not converted into machine-test ratings.">明确的无配置、选配、标配按 0、60、100 计入；空白保留为资料未记录。配置有效覆盖率不足 60% 时不发布综合分；空白的六大特性区域不转化为实机评价。</p></article></div></section>
<footer class="dashboardFooter"><small data-en="Executive sponsor: Zhang Shengnan · Data visualization: Liu Chang · Data source: ARC Product Team · Issue reporting: changl@xcmgarc.com">指导领导：张盛楠　数据可视化：刘畅　数据来源：ARC产品小组　问题提报：changl@xcmgarc.com</small></footer>
</main></div><script src="assets/dashboard.js?v=20260805e"></script><script src="assets/i18n.js?v=20260805e"></script></body></html>'''


def build_all() -> list[Path]:
    workbook = load_crane_workbook()
    outputs = []
    market_path = ROOT / "crane-market-overview.html"
    market_path.write_text(render_market_report_page(), encoding="utf-8")
    outputs.append(market_path)
    overview_path = ROOT / "crane-overview.html"
    overview_path.write_text(render_legacy_redirect(), encoding="utf-8")
    outputs.append(overview_path)
    for sheet in workbook.sheets:
        output = ROOT / PAGE_DEFINITIONS[sheet.label]["output"]
        output.write_text(render_page(sheet), encoding="utf-8")
        outputs.append(output)
    return outputs


if __name__ == "__main__":
    for path in build_all():
        print(path.relative_to(ROOT))
