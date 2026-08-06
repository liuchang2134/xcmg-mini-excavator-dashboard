from __future__ import annotations


def bi(zh: str, en: str) -> dict[str, str]:
    return {"zh": zh, "en": en}


OFFICIAL_REFERENCES = {
    "ground": {
        "label": bi("地基与支撑条件", "Ground and support conditions"),
        "url": "https://www.osha.gov/laws-regs/regulations/standardnumber/1926/1926.1402",
    },
    "operation": {
        "label": bi("载荷表与操作程序", "Load charts and operating procedures"),
        "url": "https://www.osha.gov/laws-regs/regulations/standardnumber/1926/1926.1417",
    },
    "inspection": {
        "label": bi("班前与周期检查", "Shift and periodic inspections"),
        "url": "https://www.osha.gov/laws-regs/regulations/standardnumber/1926/1926.1412/",
    },
    "powerline": {
        "label": bi("临近电力线路作业", "Operations near power lines"),
        "url": "https://www.osha.gov/laws-regs/regulations/standardnumber/1926/1926.1408",
    },
    "tadano-smart-chart": {
        "label": bi("行业参照：非对称支腿控制", "Industry reference: asymmetric outrigger control"),
        "url": "https://mediahub.tadano.com/m/dad9efadc1f44f9/original/doc_tadano_GR-range_en_view.pdf",
    },
    "grove-maxbase": {
        "label": bi("行业参照：可变支腿载荷图", "Industry reference: variable-outrigger charts"),
        "url": "https://www.manitowoc.com/media/17361/download",
    },
    "linkbelt-vcalc": {
        "label": bi("行业参照：实时360度能力预览", "Industry reference: real-time 360-degree capacity preview"),
        "url": "https://cdn.linkbelt.com/wp-content/uploads/2024/01/75RT-b.pdf",
    },
}


def check(item_zh: str, item_en: str, method_zh: str, method_en: str, record_zh: str, record_en: str) -> dict:
    return {
        "item": bi(item_zh, item_en),
        "method": bi(method_zh, method_en),
        "record": bi(record_zh, record_en),
    }


CONDITION_EXECUTION = {
    "road-transport": {
        "customer": bi("租赁公司、经销商、大件运输承包商和跨州施工项目", "Rental fleets, dealers, heavy-haul contractors and interstate projects"),
        "load": bi("整机、配重、副臂、垫木及随车吊具", "Crane, counterweight, jib, cribbing and carried rigging"),
        "workflow": [
            bi("冻结运输配置，明确随车与拆分运输的配重、臂架和附件状态。", "Freeze the transport configuration, including carried and separately hauled counterweight, boom and attachments."),
            bi("复核整机质量、轴荷与外廓，匹配拖车、许可和限高限宽路线。", "Verify gross mass, axle loads and envelope against trailer, permit and route restrictions."),
            bi("制定配重装卸、捆扎和附件固定方案，记录需要的辅助车辆与人员。", "Plan counterweight handling, tie-downs and attachment retention, including support vehicles and labor."),
            bi("到场后按确定配置恢复整机，完成调平、功能检查和载荷表状态确认。", "Restore the approved configuration on site, level the crane, complete function checks and confirm the applicable load chart."),
            bi("记录从进场到具备首吊条件的时间，形成不同运输组合的标准节拍。", "Record gate-to-first-lift readiness time and standardize each transport combination."),
        ],
        "constraints": [
            bi("运输质量必须按实际配重和附件状态核算，不能混用空载宣传值。", "Transport mass must reflect the actual counterweight and attachment state, not an unladen brochure value."),
            bi("跨州路线受轴荷、总重、宽高和桥涵限制，车辆组合不能只按总质量选择。", "Interstate routing is constrained by axle load, gross weight, width, height and bridge limits; trailer selection cannot use gross mass alone."),
            bi("到场恢复后的载荷表、配重识别和安全装置状态必须与实际配置一致。", "After reassembly, load charts, counterweight recognition and safety-device status must match the physical configuration."),
        ],
        "checks": [
            check("运输质量与轴荷", "Transport mass and axle loads", "按每种配重组合称重或使用经验证的质量分配表。", "Weigh each counterweight combination or use a validated mass-distribution sheet.", "总重、各轴荷、质量偏差", "Gross mass, each axle load and variance"),
            check("运输外廓", "Transport envelope", "在固定行驶姿态测量长、宽、高并核对路线限制。", "Measure length, width and height in the defined travel posture and check the route.", "路线限制、许可类别、护送需求", "Route restrictions, permit class and escort needs"),
            check("到场恢复", "Site readiness", "从车辆到场计时至配重、支腿、RCL和载荷表全部可用。", "Time from arrival until counterweight, outriggers, RCL and load chart are ready.", "工时、辅助车辆数、首吊准备时间", "Labor hours, support vehicles and first-lift readiness"),
        ],
        "boundary": bi("运输合规不等于吊装可执行；首吊前仍须按实际站位、配重、支腿和臂架状态重新核对载荷表。", "Transport compliance does not prove lift feasibility; recheck the load chart for the actual setup, counterweight, outriggers and boom before the first lift."),
        "refs": ["operation", "inspection"],
    },
    "rapid-mobilization": {
        "customer": bi("租赁公司、工业检修承包商、设备安装与多工地施工团队", "Rental fleets, outage contractors, equipment installers and multi-site crews"),
        "load": bi("配重、垫木、吊钩、副臂、索具与日常维护物料", "Counterweight, cribbing, hook blocks, jib, rigging and daily service supplies"),
        "workflow": [
            bi("接收任务后锁定吊重、幅度、站位与下一工地距离，选择最少拆分的合规配置。", "Lock load, radius, setup position and next-site distance, then select the least-disassembled compliant configuration."),
            bi("按标准清单装载垫木、索具和附件，避免到场后二次调货。", "Load cribbing, rigging and attachments from a standard checklist to avoid secondary deliveries."),
            bi("完成配重转换、附件固定和道路检查，记录拆装步骤及人工。", "Complete counterweight changes, attachment retention and road checks while recording steps and labor."),
            bi("到场后调平、展开支腿、完成班前检查并加载正确工况。", "Level, deploy outriggers, complete the shift inspection and select the correct operating configuration."),
            bi("以首吊准备时间和收车时间复盘非生产停机。", "Review non-productive downtime using first-lift readiness and pack-up time."),
        ],
        "constraints": [
            bi("快速转场不能省略配置确认、班前检查和支腿地基复核。", "Rapid mobilization cannot omit configuration confirmation, shift inspection or ground review."),
            bi("随车附件越完整，运输质量和轴荷压力越大，需要同时优化而非单项追求。", "More carried equipment increases transport mass and axle-load pressure, so both must be optimized together."),
            bi("现场节拍应把等待辅助吊、配重车和垫木的时间单独记录。", "Waiting for assist cranes, counterweight trucks and cribbing should be recorded separately."),
        ],
        "checks": [
            check("拆装步骤", "Assembly steps", "逐步记录配重、附件和支腿准备动作。", "Record each counterweight, attachment and outrigger preparation step.", "步骤数、人工、工具与辅助设备", "Steps, labor, tools and support equipment"),
            check("转场准备", "Mobilization readiness", "连续执行收车、运输、到场恢复的完整演练。", "Run a complete pack-up, transport and site-restoration exercise.", "收车时间、首吊准备时间", "Pack-up and first-lift readiness time"),
            check("维护停机", "Maintenance downtime", "按班次记录润滑、加注和日检所需时间。", "Record lubrication, fluid and daily-inspection time by shift.", "分钟/班、漏项与返工", "Minutes per shift, omissions and rework"),
        ],
        "boundary": bi("节拍必须在满足制造商程序和安全检查的前提下比较，不能把省略步骤形成的时间优势计入产品能力。", "Compare cycle time only while following manufacturer procedures and safety inspections; time gained by skipping steps is not a product advantage."),
        "refs": ["inspection", "operation"],
    },
    "site-mobility": {
        "customer": bi("道路桥梁、能源、工业建设、灾后恢复和偏远工地承包商", "Road, bridge, energy, industrial, disaster-recovery and remote-site contractors"),
        "load": bi("通常为空载转场；带载移动必须使用对应轮胎载荷表和制造商程序", "Normally unloaded travel; loaded travel requires the applicable on-tire chart and manufacturer procedure"),
        "workflow": [
            bi("踏勘坡度、路宽、转弯点、软基、地下设施和顶部障碍。", "Survey slope, route width, turning points, soft ground, buried services and overhead obstructions."),
            bi("选择轮胎、驱动桥和转向模式，设定允许的行驶姿态与速度。", "Select tire, driven-axle and steering modes and define the approved travel posture and speed."),
            bi("以低速通过关键路段，观察轮胎沉陷、车身倾斜和转向余量。", "Traverse critical sections at low speed while monitoring tire sinkage, chassis inclination and steering margin."),
            bi("进入站位后复核地面承载、支腿展开空间和回转障碍。", "At the setup point, recheck bearing support, outrigger space and swing obstructions."),
            bi("记录路线用时和需人工修整的路段，形成工地准入边界。", "Record route time and sections needing preparation to define site-access limits."),
        ],
        "constraints": [
            bi("铭牌爬坡度不等于松软地面可用坡度，轮胎附着和地基强度必须单独确认。", "Nameplate gradeability is not the usable slope on soft ground; tire traction and bearing strength require separate confirmation."),
            bi("转向模式切换、差速锁和驱动桥使用必须遵循制造商限制。", "Steering-mode changes, differential locks and driven axles must follow manufacturer limits."),
            bi("行驶路线、吊臂位置、顶部障碍和速度是一个整体，不应分开评估。", "Travel route, boom position, overhead clearance and speed form one operating system and should not be assessed separately."),
        ],
        "checks": [
            check("通过与转向", "Access and steering", "按固定路线实测转弯、会车和掉头。", "Measure cornering, passing and turning around on a fixed route.", "最小通道、修正次数、路线时间", "Minimum aisle, corrections and route time"),
            check("坡道与软基", "Slope and soft ground", "在受控条件下记录坡度、沉陷和轮滑，禁止超出制造商边界。", "Record slope, sinkage and wheel slip under controlled conditions without exceeding manufacturer limits.", "坡度、沉陷量、轮滑与中止条件", "Slope, sinkage, wheel slip and stop criteria"),
            check("驾驶可视性", "Travel visibility", "评估前后左右盲区及摄像头覆盖。", "Assess front, rear and side blind areas and camera coverage.", "盲区范围、观察员需求", "Blind-zone envelope and spotter need"),
        ],
        "boundary": bi("若带载行驶，必须使用对应轮胎/带载载荷表，并由现场负责人确定载荷位置、臂架姿态、路线、障碍和安全速度。", "For loaded travel, use the applicable on-tire/pick-and-carry chart and have site supervision define load position, boom posture, route, obstructions and safe speed."),
        "refs": ["ground", "operation"],
    },
    "confined-positioning": {
        "customer": bi("城市公用事业、厂房维保、住宅施工、屋面设备和通信安装单位", "Urban utilities, plant maintenance, residential construction, rooftop-equipment and telecom contractors"),
        "load": bi("空调机组、变压器、广告牌、结构件和小型设备模块", "HVAC units, transformers, signs, structural members and equipment modules"),
        "workflow": [
            bi("用总图确定车身、支腿、尾部回转和吊臂扫掠包络。", "Use the site plan to define carrier, outrigger, tail-swing and boom-sweep envelopes."),
            bi("确认道路边线、建筑物、架空线和地下设施，选择最少移位的站位。", "Identify curbs, buildings, overhead lines and buried services, then choose the setup requiring the fewest repositioning moves."),
            bi("设置支腿档位和回转限制，完成空载干运行。", "Set outrigger positions and swing limits, then perform an unloaded dry run."),
            bi("由指挥员控制盲区和落位区，使用低速复合动作完成就位。", "Use a signal person for blind and landing areas and place the load with low-speed combined motions."),
            bi("记录调整次数、盲区和最小安全间隙。", "Record corrections, blind areas and minimum safe clearances."),
        ],
        "constraints": [
            bi("只比较尾回转半径不能代表完整站位能力，支腿、车身和臂架扫掠都必须纳入。", "Tail-swing radius alone does not represent positioning ability; outriggers, carrier and boom sweep all matter."),
            bi("部分支腿或非对称支腿只能按机器识别到的实际支腿状态使用对应载荷图。", "Partial or asymmetric outriggers require the chart recognized for the actual extension state."),
            bi("临近电线、道路交通和行人时，应把工作区边界纳入站位方案。", "Near power lines, traffic or pedestrians, the work-zone boundary must be part of the setup plan."),
        ],
        "checks": [
            check("站位包络", "Setup envelope", "以实际配重、支腿和臂架状态绘制平面包络。", "Plot the plan envelope using actual counterweight, outrigger and boom states.", "占地、尾扫、吊臂扫掠与安全间隙", "Footprint, tail sweep, boom sweep and clearance"),
            check("微动与复合动作", "Fine and combined control", "使用固定吊物和落位窗口重复执行回转、变幅与起升。", "Repeat swing, luff and hoist motions with a fixed load and landing window.", "修正次数、过冲、落位时间", "Corrections, overshoot and placement time"),
            check("驾驶员视野", "Operator visibility", "按高低仰角和左右回转位置记录吊物可见性。", "Record load visibility at high/low boom angles and left/right swing positions.", "不可见区、摄像头与指挥需求", "Blind areas, camera and signal-person needs"),
        ],
        "boundary": bi("受限空间能力必须同时满足载荷图、支腿状态、回转限位和现场工作区控制，不能仅按几何尺寸判断。", "Confined-area capability must satisfy the load chart, outrigger state, swing limits and work-zone controls; geometry alone is insufficient."),
        "refs": ["operation", "powerline", "linkbelt-vcalc"],
    },
    "near-heavy-lift": {
        "customer": bi("工业安装、预制构件、设备卸车、能源与大型检修承包商", "Industrial installers, precast contractors, equipment unloaders, energy and major-outage contractors"),
        "load": bi("反应器、变压器、预制梁、工艺设备和重型模块", "Reactors, transformers, precast beams, process equipment and heavy modules"),
        "workflow": [
            bi("确认吊物重量、重心、吊点、索具重量和动态影响。", "Confirm load mass, center of gravity, lift points, rigging mass and dynamic effects."),
            bi("按实际幅度选择主臂、倍率、吊钩、配重和支腿配置。", "Select boom, reeving, hook block, counterweight and outrigger configuration for the actual radius."),
            bi("核算支腿反力和地基承载，布置垫板并调平。", "Calculate outrigger reactions and ground bearing, install mats and level the crane."),
            bi("执行离地试吊，确认制动、RCL、载荷稳定与通信。", "Perform a trial lift clear of the ground and confirm brakes, RCL, load stability and communications."),
            bi("按规划路径起升、回转和落位，持续监控幅度与利用率。", "Hoist, slew and land along the planned path while monitoring radius and utilization."),
        ],
        "constraints": [
            bi("必须使用实际吊物总重和最大工作幅度，不能用额定吨位替代载荷图。", "Use total lifted mass and maximum working radius; nameplate tonnage cannot replace the load chart."),
            bi("配重、倍率、支腿档位和吊臂长度任何一项变化都可能改变允许载荷。", "Any change to counterweight, reeving, outrigger position or boom length can change capacity."),
            bi("重载近幅的支腿反力可能集中，地基与垫板验算是能力的一部分。", "Near-radius heavy lifts can concentrate outrigger reactions; ground and mat verification are part of capability."),
        ],
        "checks": [
            check("同幅度能力", "Like-radius capacity", "按相同配重、支腿、臂长和实际幅度读取载荷图。", "Read charts at identical counterweight, outrigger, boom and actual radius.", "允许载荷、利用率与余量", "Permitted load, utilization and margin"),
            check("卷扬与制动", "Winch and brakes", "按实际倍率试吊并记录起停、保持和低速控制。", "Trial-lift at actual reeving and record start, stop, holding and low-speed control.", "线拉力、速度、下滑与温升", "Line pull, speed, drift and temperature"),
            check("支撑系统", "Support system", "记录支腿反力、垫板面积、调平和沉降。", "Record outrigger reactions, mat area, level and settlement.", "地基压力、沉降与水平度", "Bearing pressure, settlement and level"),
        ],
        "boundary": bi("页面能力仅用于筛选方案；正式重载吊装必须形成包含重量、重心、索具、载荷图、地基和作业路径的吊装计划。", "Page results only screen concepts; a formal heavy-lift plan must cover mass, center of gravity, rigging, load charts, ground support and load path."),
        "refs": ["ground", "operation", "inspection"],
    },
    "mid-radius-installation": {
        "customer": bi("钢结构、预制构件、商业建筑、工业设备与机电安装承包商", "Steel, precast, commercial-building, industrial-equipment and MEP contractors"),
        "load": bi("钢梁、预制板、管廊、机组和一般设备模块", "Steel beams, precast panels, pipe racks, packaged units and general equipment modules"),
        "workflow": [
            bi("把构件重量、安装高度和最远回转点转换为最大实际幅度。", "Convert component mass, installation height and farthest swing point into the maximum actual radius."),
            bi("选择能覆盖完整路径的臂长、配重、支腿和倍率。", "Select boom, counterweight, outrigger and reeving states that cover the full path."),
            bi("规划卸车点、起吊区、回转通道和落位窗口。", "Plan unload point, pick zone, swing corridor and landing window."),
            bi("用稳定的起升、回转和变幅复合动作完成安装。", "Complete placement using controlled hoist, swing and luffing motions."),
            bi("以单循环时间、落位修正和最大利用率评估生产率。", "Assess productivity using cycle time, placement corrections and peak utilization."),
        ],
        "constraints": [
            bi("构件路径中的最大幅度通常比起吊点幅度更关键。", "The maximum radius along the load path is often more critical than the pick radius."),
            bi("高频安装应同时关注卷扬、回转节拍和热平衡，而非只看载荷能力。", "High-cycle installation requires winch, swing and thermal performance, not capacity alone."),
            bi("指挥通信和落位视线会直接影响精度与周期。", "Signal communication and landing visibility directly affect precision and cycle time."),
        ],
        "checks": [
            check("完整路径能力", "Full-path capacity", "按吊物路径逐点核对半径、臂长和允许载荷。", "Check radius, boom length and capacity at each point along the load path.", "峰值利用率与最小余量", "Peak utilization and minimum margin"),
            check("循环节拍", "Cycle productivity", "固定构件与路径重复完成至少多个稳定循环。", "Repeat a fixed component and path over multiple stable cycles.", "起升、回转、落位和返回分项时间", "Hoist, swing, placement and return times"),
            check("落位控制", "Placement control", "设置统一落位窗口并记录过冲和修正。", "Use a standard landing window and record overshoot and corrections.", "修正次数、落位偏差与时间", "Corrections, placement deviation and time"),
        ],
        "boundary": bi("工况比较必须使用相同吊物路径和最大幅度；只比较额定吨位或单一载荷点会高估现场适配性。", "Compare the same load path and maximum radius; nameplate tonnage or a single chart point can overstate jobsite fit."),
        "refs": ["operation", "inspection"],
    },
    "long-boom-high-lift": {
        "customer": bi("厂房屋面、塔体、风电辅助、通信、电力和大型机电安装承包商", "Roof, tower, wind-support, telecom, utility and major MEP contractors"),
        "load": bi("屋面机组、塔体附件、风电辅助件、灯杆和高位结构件", "Rooftop units, tower accessories, wind-support components, poles and elevated structures"),
        "workflow": [
            bi("建立高度、幅度和越障三维包络，识别最不利载荷点。", "Build a 3D height, radius and obstacle envelope and identify the governing point."),
            bi("按主臂或副臂方案选择臂长、配重、支腿和吊钩。", "Select main-boom or jib configuration, boom length, counterweight, outriggers and hook block."),
            bi("核对风速、吊物迎风面积、架空障碍和通信方案。", "Check wind, load sail area, overhead obstacles and communications."),
            bi("先空载验证越障与落位路径，再执行受控起升。", "Validate clearance and landing path unloaded before the controlled lift."),
            bi("记录伸臂准备、可视性、远幅余量和落位修正。", "Record extension setup, visibility, far-radius margin and placement corrections."),
        ],
        "constraints": [
            bi("最大臂长不等于有效能力，必须同时读取该长度与幅度下的允许载荷。", "Maximum boom length is not usable capacity; read the permitted load at that boom and radius."),
            bi("风、冰雪和吊物迎风面积会改变稳定性与操作边界。", "Wind, ice, snow and load sail area affect stability and operating limits."),
            bi("高仰角视野、摄像头和驾驶室俯仰影响吊钩与落位可见性。", "High-angle visibility, cameras and cab tilt affect hook and landing visibility."),
        ],
        "checks": [
            check("高度幅度包络", "Height-radius envelope", "用实际吊物尺寸建立越障、吊点和落位三维路径。", "Build a 3D path using actual load dimensions, obstacles, pick and landing points.", "最不利半径、净空与载荷余量", "Governing radius, clearance and capacity margin"),
            check("臂架响应", "Boom response", "记录全伸、回缩、变幅及组合动作。", "Record extension, retraction, luffing and combined motions.", "时间、冲击、摆动与停止精度", "Time, shock, sway and stop accuracy"),
            check("高位落钩", "Elevated placement", "在统一高度和落位窗口执行重复测试。", "Repeat tests at a fixed height and landing window.", "视野、修正次数和偏差", "Visibility, corrections and deviation"),
        ],
        "boundary": bi("风速限值、臂架组合、配重和载荷能力必须按制造商载荷图与操作手册执行，页面不生成现场允许风速。", "Wind limits, boom configuration, counterweight and capacity must follow manufacturer charts and procedures; the page does not generate a site wind limit."),
        "refs": ["operation", "inspection"],
    },
    "jib-long-radius": {
        "customer": bi("屋面设备、广告通信、工业检修、塔体和远幅越障安装承包商", "Rooftop equipment, sign/telecom, industrial maintenance, tower and long-radius clearance contractors"),
        "load": bi("轻型高位设备、塔体附件、管线、标识和越障构件", "Light elevated equipment, tower accessories, piping, signs and obstacle-clearance components"),
        "workflow": [
            bi("用高度与幅度包络判断是否必须使用副臂。", "Use the height-radius envelope to determine whether a jib is required."),
            bi("选择副臂长度、延伸节、变角、配重和倍率。", "Select jib length, inserts, offset, counterweight and reeving."),
            bi("评估副臂运输、安装空间、装拆人员和时间。", "Assess jib transport, erection space, labor and installation time."),
            bi("核对专用载荷图并空载验证越障路径。", "Check the dedicated load chart and validate clearance unloaded."),
            bi("以装拆时间、远幅余量和落位精度评估完整方案。", "Assess the solution using erection time, far-radius margin and placement accuracy."),
        ],
        "constraints": [
            bi("副臂长度与变角是离散组合，不能把不同组合的最大值拼接成一个能力。", "Jib length and offset are discrete configurations; maxima from different setups cannot be combined."),
            bi("副臂装拆所需空间和辅助设备可能抵消远幅能力优势。", "Jib erection space and support equipment can offset the benefit of long-radius capability."),
            bi("副臂载荷图、主臂角度和回转方向必须同时匹配。", "Jib chart, main-boom angle and swing sector must match simultaneously."),
        ],
        "checks": [
            check("副臂组合覆盖", "Jib configuration coverage", "逐项列出长度、延伸节、变角和对应载荷点。", "List length, inserts, offset and applicable chart points for each configuration.", "可用组合、缺失组合与任务覆盖", "Usable combinations, gaps and task coverage"),
            check("装拆效率", "Erection efficiency", "按运输状态完成副臂展开、销接、回收全过程。", "Complete jib deployment, pinning and stowage from transport state.", "时间、人员、辅助设备和高处作业", "Time, labor, support equipment and work at height"),
            check("远幅落位", "Long-radius placement", "按固定轻载和最远任务点重复落位。", "Repeat placement with a fixed light load at the farthest task point.", "摆动、偏差、修正与可见性", "Sway, deviation, corrections and visibility"),
        ],
        "boundary": bi("副臂工况只能使用对应配置的专用载荷表；资料中的多值状态只作组合边界，不自动合并评分。", "Jib work must use the dedicated chart for that configuration; multi-value source entries define combinations and are not merged into an automatic score."),
        "refs": ["operation", "inspection"],
    },
    "outrigger-stability": {
        "customer": bi("建筑、道路桥梁、能源、工业安装及场地条件不确定的施工单位", "Building, bridge, energy, industrial-installation and variable-ground contractors"),
        "load": bi("覆盖所有支腿吊装任务，重点是高利用率和不平整地面工况", "All lifts on outriggers, especially high-utilization and uneven-ground work"),
        "workflow": [
            bi("查明地面坡度、压实、排水、地下空洞和管线。", "Identify slope, compaction, drainage, voids and buried utilities."),
            bi("根据支腿反力选择垫板/垫木和支腿位置，划定不可站位区。", "Select mats/cribbing and outrigger positions from reactions and define no-setup zones."),
            bi("展开支腿、调平并确认各支腿受力与接触稳定。", "Deploy outriggers, level the crane and confirm stable contact and loading."),
            bi("选择对应支腿档位、水平度和配重的载荷图。", "Select the chart matching outrigger extension, level and counterweight."),
            bi("班中监控沉降、水平度和天气变化，必要时停机重设。", "Monitor settlement, level and weather during the shift and stop to reset if needed."),
        ],
        "constraints": [
            bi("地基必须达到制造商要求的支撑与水平度，垫板不能替代地基验算。", "Ground must meet manufacturer support and level requirements; mats do not replace a bearing assessment."),
            bi("支腿穿透量没有统一的越大越好方向，只能作为几何和地基边界记录。", "Outrigger penetration has no universal better direction and is retained only as a geometric and ground boundary."),
            bi("地面条件会随降雨、冻融、开挖和重复荷载变化，应按班次复核。", "Ground can change with rain, freeze-thaw, excavation and repeated loading and requires shift review."),
        ],
        "checks": [
            check("地基与垫板", "Ground and mats", "按最大支腿反力和允许地基压力核算接触面积。", "Calculate contact area from maximum outrigger reaction and allowable ground pressure.", "反力、面积、地压与安全余量", "Reaction, area, bearing pressure and margin"),
            check("调平与沉降", "Level and settlement", "初始调平后在试吊和最大利用率阶段复测。", "Recheck after initial leveling, trial lift and peak utilization.", "水平度、支腿沉降与变化率", "Level, settlement and rate of change"),
            check("支腿状态识别", "Outrigger-state recognition", "逐档验证传感器、显示和载荷图切换。", "Verify sensors, display and chart selection at each extension position.", "识别一致性、报警与限制动作", "Recognition consistency, alarms and limiting action"),
        ],
        "boundary": bi("OSHA要求地面达到足够的坚实、排水和整平条件，并结合必要的支撑材料满足制造商支撑与水平度要求。", "OSHA requires sufficiently firm, drained and graded ground, with supporting materials as needed, to meet manufacturer support and level requirements."),
        "refs": ["ground", "inspection", "operation"],
    },
    "partial-outrigger-confined": {
        "customer": bi("城市道路、厂区、桥边、建筑夹缝和既有设备周边施工单位", "Urban-road, plant, bridge-edge and constrained-building contractors"),
        "load": bi("受限站位中的设备、结构件、管线和屋面单元", "Equipment, structural members, piping and rooftop units in constrained setups"),
        "workflow": [
            bi("确定可用支腿空间、不可侵入边界和吊物完整路径。", "Define available outrigger space, no-encroachment boundaries and the complete load path."),
            bi("选择每条支腿的实际档位，确认机器能正确识别。", "Select the actual extension of each outrigger and confirm machine recognition."),
            bi("加载对应的分区载荷图，设置回转预警或限制。", "Load the applicable sector chart and set swing warnings or limits."),
            bi("空载回转验证允许区、禁入区和下一幅度能力。", "Dry-run the permitted sector, prohibited sector and next-radius capacity."),
            bi("吊装中监控回转方向、支腿状态、水平度和载荷利用率。", "Monitor swing sector, outrigger state, level and utilization during the lift."),
        ],
        "constraints": [
            bi("部分支腿状态下能力随回转方向变化，不能沿用360度统一能力。", "With partial outriggers, capacity changes with swing direction and cannot use a uniform 360-degree value."),
            bi("支腿传感器、RCL显示、回转限制与实体档位必须一致。", "Outrigger sensors, RCL display, swing limits and physical extension must agree."),
            bi("建筑边缘、沟槽和地下设施可能使可见地面无法承受支腿反力。", "Building edges, trenches and underground structures can make apparently solid ground unable to carry outrigger reactions."),
        ],
        "checks": [
            check("分区能力", "Sector capacity", "按每条支腿实际档位生成或读取360度能力图。", "Generate or read the 360-degree chart for actual extension of every outrigger.", "各回转区允许载荷与边界", "Permitted load and boundary by swing sector"),
            check("系统联锁", "System interlocks", "改变单条支腿档位，验证识别、预览、报警和慢停/限动。", "Change one outrigger position and verify recognition, preview, alarms and slow-stop/limit behavior.", "识别延迟、误差与保护动作", "Recognition delay, errors and protective action"),
            check("站位效率", "Setup efficiency", "用相同受限场地比较可用站位和准备过程。", "Compare feasible setups and preparation in the same constrained site.", "占地、可用回转区和准备时间", "Footprint, usable sectors and setup time"),
        ],
        "boundary": bi("非对称支腿功能只能扩展可核验的工作区，不能绕过地基、水平度、回转区和对应载荷表限制。", "Asymmetric-outrigger systems can expand a verifiable work area but cannot bypass ground, level, swing-sector or chart limits."),
        "refs": ["ground", "tadano-smart-chart", "grove-maxbase", "linkbelt-vcalc"],
    },
    "on-tire-pick-carry": {
        "customer": bi("工业厂区、预制场、港口堆场、能源设施和大型施工现场", "Industrial plants, precast yards, ports, energy facilities and major construction sites"),
        "load": bi("短距离搬运的构件、设备、吊具和模块，仅适用于有明确轮胎/带载载荷表的越野吊", "Components, equipment, rigging and modules moved short distances, only where an explicit on-tire/pick-and-carry chart exists"),
        "workflow": [
            bi("确认吊物总重、重心、行驶半径和允许的臂架姿态。", "Confirm total lifted mass, center of gravity, travel radius and permitted boom posture."),
            bi("踏勘并整备路线，消除横坡、坑洼、架空障碍和人员交叉。", "Survey and prepare the route, addressing cross-slope, potholes, overhead hazards and pedestrian conflicts."),
            bi("按对应载荷表设定轮胎压力、转向、上车锁止和行驶速度。", "Set tire pressure, steering, upperstructure lock and travel speed per the applicable chart."),
            bi("离地至规定高度后低速直线行驶，必要时由观察员引导。", "Raise the load to the specified carry height and travel slowly, using a spotter as required."),
            bi("记录摆动、制动、转向和路线时间，禁止在未批准状态下改变配置。", "Record sway, braking, steering and route time and prohibit unapproved configuration changes."),
        ],
        "constraints": [
            bi("只有明确的轮胎和带载载荷图才构成能力证据，支腿载荷图不能替代。", "Only explicit on-tire and pick-and-carry charts prove capacity; outrigger charts are not substitutes."),
            bi("横坡、急转、加减速和吊物摆动会显著改变稳定性。", "Cross-slope, sharp steering, acceleration, braking and load sway materially affect stability."),
            bi("全地面起重机页面不适用该工况，除非原厂明确提供对应能力。", "This condition does not apply to all-terrain pages unless the manufacturer explicitly provides the capability."),
        ],
        "checks": [
            check("轮胎载荷能力", "On-tire capacity", "按实际轮胎、配重、臂架、回转位置和幅度读取载荷图。", "Use the chart matching tire, counterweight, boom, upperstructure position and radius.", "允许载荷、利用率与限制条件", "Permitted load, utilization and restrictions"),
            check("带载路线", "Pick-and-carry route", "用固定吊物在受控路线记录直行、制动和转弯表现。", "Use a fixed load on a controlled route and record straight travel, braking and turning.", "摆幅、制动距离、速度与路线时间", "Sway, stopping distance, speed and route time"),
            check("驾驶控制", "Travel control", "验证上车锁止、转向模式、报警和摄像头。", "Verify upperstructure lock, steering mode, alarms and cameras.", "联锁、报警、盲区与观察员需求", "Interlocks, alarms, blind zones and spotter need"),
        ],
        "boundary": bi("带载行驶必须使用制造商程序和对应载荷图，并由现场负责人确定载荷位置、路线、障碍和安全速度。", "Pick-and-carry work requires manufacturer procedures and the applicable chart, with site supervision defining load position, route, obstructions and safe speed."),
        "refs": ["operation", "ground", "inspection"],
    },
    "cycle-productivity": {
        "customer": bi("港口堆场、预制场、材料转运、结构安装和连续吊装承包商", "Ports, precast yards, material handlers, structural installers and repetitive-lift contractors"),
        "load": bi("标准化构件、吊具、料斗、设备模块和重复装卸物料", "Standardized components, rigging, buckets, equipment modules and repetitive handled materials"),
        "workflow": [
            bi("固定吊物、路径、幅度、倍率和落位窗口，拆分完整循环。", "Fix load, path, radius, reeving and landing window and split the full cycle."),
            bi("选择主副卷扬协同方式和臂架动作顺序。", "Select main/auxiliary winch coordination and boom-motion sequence."),
            bi("完成若干稳定循环后再采集节拍，排除学习效应。", "Collect cycle data only after several stable runs to exclude learning effects."),
            bi("持续记录油温、水温、液压温度、报警和动作衰减。", "Continuously record oil, coolant and hydraulic temperature, alarms and motion degradation."),
            bi("把起升、回转、落位、返回与等待分开归因。", "Attribute hoist, swing, placement, return and waiting time separately."),
        ],
        "constraints": [
            bi("单次最快时间没有代表性，应比较稳定循环的中位数和离散度。", "One fastest cycle is not representative; compare median stable cycles and variation."),
            bi("实际生产率还受吊具、司机、指挥和路径组织影响。", "Actual productivity also depends on rigging, operator, signaling and route organization."),
            bi("连续作业必须同步观察热平衡、燃油消耗和维护需求。", "Continuous work requires simultaneous review of thermal balance, fuel use and maintenance demand."),
        ],
        "checks": [
            check("分项循环时间", "Elemental cycle time", "固定工况连续测试并拆分动作时间。", "Run repeated fixed-condition cycles and split motion times.", "中位数、P90与波动", "Median, P90 and variability"),
            check("动作协同", "Motion coordination", "记录双卷扬及回转/变幅/起升复合动作。", "Record dual-winch and combined swing/luff/hoist motions.", "动作重叠率、过冲与等待", "Motion overlap, overshoot and waiting"),
            check("持续能力", "Sustained capability", "在规定时长内持续循环并记录温度、报警和速度。", "Cycle for a defined duration while recording temperatures, alarms and speed.", "节拍衰减、温升与燃油", "Cycle degradation, temperature rise and fuel"),
        ],
        "boundary": bi("页面的纸面节拍只用于发现潜力；产品结论必须来自固定吊物、固定路径和稳定循环的对比试验。", "Paper-based cycle potential only identifies opportunities; product conclusions require matched-load, matched-path and stable-cycle testing."),
        "refs": ["operation", "inspection"],
    },
    "precision-maintenance-lift": {
        "customer": bi("石化、制造、电力、通信、HVAC和停机检修承包商", "Petrochemical, manufacturing, utility, telecom, HVAC and outage contractors"),
        "load": bi("泵、阀、换热器、电机、屋面机组和需精确对孔的设备", "Pumps, valves, heat exchangers, motors, rooftop units and equipment requiring precise alignment"),
        "workflow": [
            bi("确认停机窗口、障碍、吊点、落位公差和指挥方式。", "Confirm outage window, obstacles, lift points, placement tolerance and signaling."),
            bi("选择满足视野和微动要求的站位、臂架与卷扬组合。", "Select setup, boom and winch configuration for visibility and fine control."),
            bi("空载验证吊钩路径和复合动作，设置回转/幅度限制。", "Dry-run the hook path and combined motions and set swing/radius limits."),
            bi("以低速完成起升、回转和落位，监控过冲与载荷摆动。", "Hoist, swing and place at low speed while monitoring overshoot and sway."),
            bi("记录每次修正及对接时间，区分机器、指挥和索具原因。", "Record each correction and alignment time and separate crane, signaling and rigging causes."),
        ],
        "constraints": [
            bi("最大速度不代表微动能力，低速可控范围、响应线性和停止精度更关键。", "Maximum speed does not prove fine control; controllable low-speed range, linearity and stop accuracy matter more."),
            bi("高仰角视野和盲区会放大通信延迟与修正次数。", "High-angle visibility and blind areas amplify communication delay and corrections."),
            bi("停机检修强调可靠性、诊断和快速恢复，不能只看吊装能力。", "Outage maintenance values reliability, diagnostics and recovery, not lifting capacity alone."),
        ],
        "checks": [
            check("微动控制", "Fine control", "固定轻载和落位窗口，重复测试起升、回转与变幅。", "Repeat hoist, swing and luffing with a fixed light load and landing window.", "最低稳定速度、过冲和修正次数", "Minimum stable speed, overshoot and corrections"),
            check("复合动作", "Combined motions", "执行规定的双动作/三动作路径。", "Execute a defined two- and three-motion path.", "协调性、路径偏差与冲击", "Coordination, path deviation and shock"),
            check("故障恢复", "Fault recovery", "模拟可安全注入的常见告警并按手册诊断。", "Inject safe representative alarms and diagnose per the manual.", "识别时间、定位步骤与恢复时间", "Detection, diagnostic steps and recovery time"),
        ],
        "boundary": bi("实机操控结论必须使用统一吊物、统一路径、统一操作者熟悉度和盲测记录；纸面速度参数不能替代微动试验。", "Field control conclusions require a matched load, path, operator familiarity and blind recording; published speed values cannot replace fine-control testing."),
        "refs": ["operation", "inspection"],
    },
    "all-weather-duty": {
        "customer": bi("加拿大草原、北部能源、寒区基础设施、沿海多雨和长班次工业客户", "Canadian Prairie, northern energy, cold-region infrastructure, wet-coastal and long-shift industrial customers"),
        "load": bi("低温启动、雨雪、沙尘、高温及长班次下的常规吊装任务", "Normal lifts under cold start, rain, snow, dust, heat and long-shift conditions"),
        "workflow": [
            bi("按环境温度和停放时间执行冷浸，确认燃油、冷却液、液压油和电池状态。", "Cold-soak for the defined temperature and duration and confirm fuel, coolant, hydraulic oil and battery state."),
            bi("记录启动、预热、制热/除霜和安全装置自检时间。", "Record start, warm-up, heating/defrost and safety-system self-check times."),
            bi("完成班前检查，清除影响视野、结构和传感器的冰雪或污染。", "Complete the shift inspection and remove ice, snow or contamination affecting visibility, structure or sensors."),
            bi("在稳定工况下执行连续循环并监控温度、报警和动作响应。", "Run sustained cycles under a stable condition while monitoring temperatures, alarms and response."),
            bi("按班次记录润滑、维护、停机和故障恢复。", "Record lubrication, maintenance, downtime and recovery by shift."),
        ],
        "constraints": [
            bi("天气会影响地基、轮胎附着、风载、视野、液压响应和电气可靠性。", "Weather affects ground, tire traction, wind loading, visibility, hydraulic response and electrical reliability."),
            bi("发动机加热器或低温包有配置不等于整机通过寒区验证。", "Having engine heat or a cold-weather package does not prove full-machine cold-region validation."),
            bi("风、冰雪影响稳定性和额定能力时，应按现场条件调整或停止作业。", "Where wind, ice or snow affects stability or capacity, operations must be adjusted or stopped for site conditions."),
        ],
        "checks": [
            check("冷启动与预热", "Cold start and warm-up", "在规定冷浸条件下记录启动和系统可用过程。", "Record startup and system readiness after a defined cold soak.", "启动成功率、预热时间与告警", "Start success, warm-up time and alarms"),
            check("环境舒适性", "Cab environment", "记录制热、制冷、除霜和噪声。", "Record heating, cooling, defrost and noise.", "达到目标时间、温差、噪声与视野", "Time to target, temperature spread, noise and visibility"),
            check("连续作业", "Sustained operation", "在规定环境与循环下监控温度和动作衰减。", "Monitor temperatures and motion degradation under defined environment and cycles.", "温升、节拍衰减、故障与维护时间", "Temperature, cycle degradation, faults and maintenance time"),
        ],
        "boundary": bi("环境适应性应按温度、风、降水、沙尘和地基状态分别验证，不能用单一配置项代替整机试验。", "Environmental fit requires separate temperature, wind, precipitation, dust and ground validation; one equipment item cannot replace full-machine testing."),
        "refs": ["operation", "inspection", "ground"],
    },
    "urban-utility-installation": {
        "customer": bi("电力、公用事业、通信、广告、城市更新和屋面设备承包商", "Power, utility, telecom, sign, urban-renewal and rooftop-equipment contractors"),
        "load": bi("变压器、杆塔附件、广告牌、通信设备、HVAC与屋面机组", "Transformers, pole/tower hardware, signs, telecom equipment, HVAC and rooftop units"),
        "workflow": [
            bi("确认道路封闭、行人、建筑边线、架空线和地下管线。", "Confirm traffic closure, pedestrians, building edges, power lines and buried utilities."),
            bi("按最大工作幅度划定工作区和临电控制边界。", "Define the work zone and electrical-control boundary at maximum working radius."),
            bi("选择紧凑站位和支腿档位，设置回转/幅度限制并空载验证。", "Select a compact setup and outrigger positions, set swing/radius limits and dry-run."),
            bi("在指挥员持续通信下越障并精准落位。", "Clear obstacles and place precisely under continuous signal-person communication."),
            bi("收车前复核道路恢复、附件和现场遗留风险。", "Before pack-up, verify road restoration, attachments and residual site risks."),
        ],
        "constraints": [
            bi("任何部件、载荷线或吊物进入架空线20英尺范围时，必须按线路电压和法规采取控制措施。", "If equipment, load line or load can enter 20 ft of a power line, controls must follow line voltage and regulatory requirements."),
            bi("狭窄站位下应同时验证回转区、支腿档位和对应载荷表。", "Constrained setups require simultaneous verification of swing sector, outrigger position and applicable chart."),
            bi("交通、行人和盲区控制是任务链的一部分，不是机器配置的替代项。", "Traffic, pedestrian and blind-zone controls are part of the task chain, not substitutes for machine features."),
        ],
        "checks": [
            check("临电工作区", "Power-line work zone", "按最大工作幅度测量线路距离并确认电压、停电或最小接近距离。", "Measure line clearance at maximum radius and confirm voltage, de-energization or minimum approach distance.", "边界、隔离、观察员与限制装置", "Boundary, isolation, spotter and limiting devices"),
            check("狭窄站位", "Confined setup", "绘制车身、支腿、尾扫、吊臂和道路边界。", "Plot carrier, outriggers, tail sweep, boom and road boundary.", "占地、可用回转区与交通影响", "Footprint, usable swing sector and traffic impact"),
            check("高空落位", "Elevated placement", "固定轻载和屋面/杆塔落位窗口重复测试。", "Repeat a fixed light-load placement to a rooftop or pole/tower window.", "可见性、修正次数和落位时间", "Visibility, corrections and placement time"),
        ],
        "boundary": bi("架空线默认带电，除非电力设施所有者确认已断电并在现场可见接地；近线作业不能仅依赖接近报警器。", "Power lines are presumed energized unless the utility confirms de-energization and visible grounding; proximity alarms alone do not control near-line work."),
        "refs": ["powerline", "operation", "ground"],
    },
    "industrial-shutdown-maintenance": {
        "customer": bi("石化、油气、制造、电力、矿山和大型工业检修承包商", "Petrochemical, oil and gas, manufacturing, utility, mining and major-outage contractors"),
        "load": bi("换热器、泵阀、管段、压缩机、电机和工艺设备模块", "Heat exchangers, pumps, valves, pipe spools, compressors, motors and process modules"),
        "workflow": [
            bi("把停机窗口、并行作业、危险区和设备隔离纳入吊装计划。", "Include outage window, simultaneous operations, hazardous zones and isolation in the lift plan."),
            bi("确认吊物重心、拆装顺序、最远幅度和逃生/检修通道。", "Confirm load center of gravity, removal sequence, maximum radius and access/egress routes."),
            bi("选择主副卷扬、臂架和受限支腿方案，完成空载路径验证。", "Select main/auxiliary winch, boom and constrained-outrigger plan and complete an unloaded path check."),
            bi("按窗口连续执行拆出、转运和回装，记录等待与故障。", "Execute removal, transfer and reinstallation within the window and record waiting and faults."),
            bi("以恢复生产所需总时间而非单次吊装时间评价。", "Evaluate total return-to-service time rather than one lift time."),
        ],
        "constraints": [
            bi("厂区障碍、管廊和并行作业会限制支腿、回转与吊物路径。", "Plant obstructions, pipe racks and simultaneous operations constrain outriggers, swing and load path."),
            bi("可靠性、故障诊断和零部件可达性直接影响停机窗口风险。", "Reliability, diagnostics and service access directly affect outage-window risk."),
            bi("防爆、许可和工艺隔离要求属于现场管理边界，不能由机器评分替代。", "Hazardous-area, permit and process-isolation requirements are site controls and cannot be replaced by a machine score."),
        ],
        "checks": [
            check("窗口任务链", "Outage task chain", "用真实拆装顺序演练吊装、转运和回装。", "Rehearse removal, transfer and reinstallation in the actual sequence.", "总时长、等待、交叉作业冲突", "Total time, waiting and SIMOPS conflicts"),
            check("精密控制", "Precision control", "按设备对孔和狭小落位窗口测试复合动作。", "Test combined motions using equipment-alignment and confined landing windows.", "过冲、修正、落位偏差", "Overshoot, corrections and placement deviation"),
            check("可用率与维修", "Availability and service", "记录连续循环故障、诊断、维护和恢复。", "Record faults, diagnostics, service and recovery over sustained cycles.", "故障率、诊断时间、可达性与恢复时间", "Fault rate, diagnostic time, access and recovery time"),
        ],
        "boundary": bi("工业停机工况应把机器能力、吊装方案和厂区作业许可分开审核；页面只评估前两者中的产品证据。", "Industrial outages require separate review of machine capability, lift plan and site permits; the page assesses only product evidence within the first two."),
        "refs": ["operation", "inspection", "ground"],
    },
    "bridge-infrastructure-placement": {
        "customer": bi("道路桥梁、轨道交通、市政基础设施和大型预制构件承包商", "Road, bridge, rail, municipal-infrastructure and major-precast contractors"),
        "load": bi("预制梁、桥面板、钢构件、护栏、管涵和施工设备", "Precast beams, deck panels, steel members, barriers, culverts and construction equipment"),
        "workflow": [
            bi("确认封路窗口、吊物交付顺序、桥边站位和构件完整路径。", "Confirm closure window, delivery sequence, edge setup and complete component path."),
            bi("复核路基、桥台、沟槽、回填区和地下结构的承载边界。", "Review bearing limits at roadbed, abutment, trench, backfill and buried structures."),
            bi("选择支腿、垫板、臂长、配重和倍率并核对最大幅度。", "Select outriggers, mats, boom, counterweight and reeving and verify maximum radius."),
            bi("离地试吊后按交通与指挥方案完成回转和落位。", "After a trial lift, swing and place under the traffic and signaling plan."),
            bi("记录封路占用、支车时间、循环节拍和沉降。", "Record closure occupancy, setup time, cycle time and settlement."),
        ],
        "constraints": [
            bi("桥边、沟槽和回填区的地表外观不能证明支腿承载能力。", "Surface appearance near bridge edges, trenches and backfill does not prove outrigger support."),
            bi("构件从运输车到最终位置的最大幅度必须逐点核对。", "Maximum radius from delivery vehicle to final position must be checked along the path."),
            bi("双机抬吊需执行额外的计划、指挥和协调要求。", "Multiple-crane lifts require additional planning, signaling and coordination."),
        ],
        "checks": [
            check("边缘地基", "Edge ground support", "结合图纸、勘察和支腿反力核算边缘/地下结构承载。", "Combine drawings, investigation and reactions to assess edge and buried-structure support.", "支腿反力、边距、垫板和沉降", "Reaction, edge distance, mats and settlement"),
            check("构件路径", "Component path", "从运输车到安装点逐点记录幅度、高度和障碍。", "Record radius, height and obstacles from transporter to installation point.", "最大利用率、净空与回转区", "Peak utilization, clearance and swing sector"),
            check("封路生产率", "Closure productivity", "记录支车、试吊、单循环、收车和道路恢复。", "Record setup, trial lift, cycle, pack-up and road reopening.", "总占用时间、循环数与延误原因", "Total closure time, cycles and delay causes"),
        ],
        "boundary": bi("正式方案必须将地基、构件重量、最不利幅度、支腿状态和交通控制同时纳入；页面排名不能替代施工吊装方案。", "The final plan must integrate ground, component mass, governing radius, outrigger state and traffic control; page ranking does not replace the lift plan."),
        "refs": ["ground", "operation", "inspection"],
    },
    "emergency-response": {
        "customer": bi("消防救援、公共工程、道路抢通、灾后恢复和公用事业应急团队", "Fire/rescue, public works, route-reopening, disaster-recovery and utility emergency teams"),
        "load": bi("倒伏构件、车辆、树木、临时设备、路障和不可完全确认的受损物", "Collapsed members, vehicles, trees, temporary equipment, obstructions and damaged loads with uncertain condition"),
        "workflow": [
            bi("先识别人员、结构、火灾、电力线路、地下设施和次生坍塌风险。", "First identify personnel, structural, fire, power-line, underground-utility and secondary-collapse risks."),
            bi("建立隔离区并稳定吊物/结构，确认可接受的吊点和重量估计。", "Establish the exclusion zone, stabilize the load/structure and confirm acceptable lift points and mass estimate."),
            bi("踏勘快速进场路线与支撑位置，必要时整备地基。", "Survey the rapid-access route and support points and prepare the ground as needed."),
            bi("采用保守配置试吊，逐步确认重量和稳定性后再转运。", "Use a conservative configuration and trial lift, confirming mass and stability before transfer."),
            bi("保持通信和撤离路径，记录不确定因素与中止条件。", "Maintain communications and escape routes and record uncertainties and stop criteria."),
        ],
        "constraints": [
            bi("应急现场吊物重量、重心和结构完整性通常不确定，必须采用保守验证。", "Emergency loads often have uncertain mass, center of gravity and structural integrity and require conservative verification."),
            bi("电力线路默认带电，倒塌结构和地下设施会改变工作区。", "Power lines are presumed energized, and collapsed structures and buried services can change the work zone."),
            bi("快速响应不等于跳过班前检查、地基核验和载荷能力确认。", "Rapid response does not permit skipping shift inspection, ground review or capacity confirmation."),
        ],
        "checks": [
            check("到场能力", "Response access", "用典型受阻路线评估通行、调头和站位。", "Use a representative obstructed route to assess access, turning and setup.", "到场时间、清障需求和站位数量", "Arrival time, route preparation and setup count"),
            check("不确定载荷", "Uncertain loads", "按保守重量估计、试吊和载荷指示逐步确认。", "Use conservative estimates, trial lift and load indication to confirm progressively.", "重量估计偏差、利用率与中止条件", "Mass-estimate error, utilization and stop criteria"),
            check("安全恢复", "Safe recovery", "模拟断电、观察员、通信和撤离路径。", "Rehearse de-energization, spotter, communications and escape routes.", "响应、报警、通信与隔离有效性", "Response, alarms, communication and exclusion effectiveness"),
        ],
        "boundary": bi("本工况只比较通行、起重和控制的纸面/试验适配性，不推定任何救援认证，也不替代现场应急指挥。", "This condition compares travel, lifting and control fit only; it implies no rescue certification and does not replace incident command."),
        "refs": ["powerline", "ground", "operation", "inspection"],
    },
    "port-yard-handling": {
        "customer": bi("港口、物流堆场、预制场、钢材中心和大型设备仓储运营商", "Ports, logistics yards, precast yards, steel centers and heavy-equipment storage operators"),
        "load": bi("标准箱件、钢构、设备模块、吊具和高频重复装卸物料", "Standard packages, steel, equipment modules, rigging and high-frequency handled materials"),
        "workflow": [
            bi("标准化吊物、吊具、取放点、路径和允许回转区。", "Standardize load, rigging, pick/place points, path and permitted swing sector."),
            bi("选择能减少改倍率和移车的臂架、卷扬与站位。", "Select boom, winch and setup to minimize re-reeving and repositioning."),
            bi("组织车辆、人员和吊物节拍，减少吊机等待。", "Synchronize trucks, people and loads to reduce crane waiting."),
            bi("连续执行稳定循环，监控温升、燃油和动作衰减。", "Run stable continuous cycles while monitoring temperature, fuel and motion degradation."),
            bi("按班次复盘实际产量、等待、维护和安全中断。", "Review actual throughput, waiting, maintenance and safety interruptions by shift."),
        ],
        "constraints": [
            bi("纸面动作速度只有在吊具、路径和司机相同时才可转化为生产率比较。", "Published motion speeds translate into productivity only with matched rigging, path and operator."),
            bi("场内短距离移动必须明确空载或带载边界和对应载荷图。", "Short-distance yard travel requires a clear unloaded or pick-and-carry boundary and applicable chart."),
            bi("持续循环可能受液压温升、燃油、润滑和维护窗口约束。", "Sustained cycles can be constrained by hydraulic temperature, fuel, lubrication and maintenance windows."),
        ],
        "checks": [
            check("小时产量", "Hourly throughput", "固定吊物和路径，在稳定阶段统计完整循环。", "Count complete cycles in the stable phase using a fixed load and path.", "循环/小时、中位节拍与等待占比", "Cycles/hour, median cycle and waiting share"),
            check("持续性能", "Sustained performance", "连续运行并记录温度、速度、报警和燃油。", "Run continuously and record temperature, speed, alarms and fuel.", "节拍衰减、温升、油耗与停机", "Cycle degradation, temperature, fuel and downtime"),
            check("场内机动", "Yard mobility", "按固定通道完成调头、移位和重新站位。", "Complete turning, relocation and reset on a fixed aisle.", "通道宽度、移位时间与盲区", "Aisle width, relocation time and blind zones"),
        ],
        "boundary": bi("页面给出的是纸面循环潜力；产量承诺必须通过固定吊物、固定路径、稳定循环和班次级数据验证。", "The page shows paper-based cycle potential; throughput commitments require matched load, path, stable cycles and shift-level data."),
        "refs": ["operation", "inspection"],
    },
}


FIELD_OBSERVATIONS = {
    "RT-60t": {
        "default": bi("历史实机评价显示整机稳定性与多田野相当；油漆质量和平均无故障工作时间仍是可靠性补强重点。", "Historical field evaluation found stability comparable with Tadano; paint quality and mean time between failures remain reliability priorities."),
        "control": bi("回转平顺性、变幅下落微动性和伸缩极限位置平顺性弱于多田野；空载起升平顺性、调速范围和伸缩响应较好。", "Swing smoothness, luff-down fine control and end-of-stroke telescoping smoothness trailed Tadano; unloaded hoist smoothness, speed range and telescoping response were stronger."),
        "environment": bi("低温启动功能与多田野相当，驾驶室制冷和制热效果略优；仍需按目标环境进行当前量产配置复核。", "Cold-start features were comparable with Tadano and cab heating/cooling was slightly stronger; the current production configuration still requires target-environment confirmation."),
        "service": bi("维修性表现有优有劣，传动轴维保便利性需改进；故障自诊断的智能化和易用性是已有基础。", "Serviceability was mixed, with driveline access needing improvement; intelligent and usable fault diagnostics were an existing strength."),
    },
    "RT-75t": {},
    "RT-100t": {},
    "RT-130t": {
        "default": bi("历史实机评价认可驾乘空间、支车速度和场地适应性；全伸臂缩臂晃动、旁弯及力限器重量显示准确性需重点验证。", "Historical field evaluation recognized cab space, setup speed and site adaptability; full-boom retraction sway, lateral deflection and load-indicator accuracy require focused validation."),
        "control": bi("回转平顺性是已有基础，但全伸臂缩臂晃动、旁弯和回转比例制动效果仍影响精准落位。", "Swing smoothness was a strength, while full-boom retraction sway, lateral deflection and proportional swing-brake behavior still affect precise placement."),
        "environment": bi("原资料未形成该吨级独立的高低温量化结论，环境适应性应按当前量产配置重新验证。", "The source did not provide a class-specific quantified hot/cold conclusion; environmental fit requires current-production validation."),
        "service": bi("原资料的主要信号集中在操控、臂架和力限器，维修节拍与可达性缺少独立量化记录。", "The source signals center on controls, boom behavior and the load indicator; service time and access lack separate quantified records."),
    },
    "AT-150t": {
        "default": bi("历史客户评价显示安全性、人性化配置和可变位平衡重适应性较强；可靠性和伸缩效率相对标杆仍有差距。", "Historical customer evaluation found strong safety, human-centered equipment and variable-counterweight adaptability; reliability and telescoping efficiency still trailed the benchmark."),
        "control": bi("可变位平衡重带来工况适应性，但伸缩效率和可靠性需与同配置标杆进行当前状态复核。", "Variable counterweight supports adaptability, while telescoping efficiency and reliability require current like-for-like benchmark confirmation."),
        "environment": bi("原资料未提供150吨全地面独立环境试验数据，不应由配置状态外推整机环境能力。", "The source contains no separate 150-ton all-terrain environmental test data; full-machine environmental capability cannot be inferred from equipment status."),
        "service": bi("可靠性被识别为相对差距，需用故障分布、停机时间和维修可达性数据进一步拆解。", "Reliability was identified as a relative gap and requires fault distribution, downtime and service-access data for decomposition."),
    },
    "RT-160t": {
        "default": bi("源表缺少可形成正式XCMG实机结论的完整量产数据；本吨级仅保留竞品边界和未来产品验证要求。", "The source lacks complete production data for a formal XCMG field conclusion; this class retains competitor boundaries and future product validation requirements only."),
        "control": bi("未形成可核验的XCMG操控实测结论。", "No verifiable XCMG control test conclusion is available."),
        "environment": bi("未形成可核验的XCMG环境试验结论。", "No verifiable XCMG environmental test conclusion is available."),
        "service": bi("未形成可核验的XCMG维修性实测结论。", "No verifiable XCMG serviceability test conclusion is available."),
    },
}


FIELD_OBSERVATIONS["RT-75t"] = FIELD_OBSERVATIONS["RT-60t"]
FIELD_OBSERVATIONS["RT-100t"] = FIELD_OBSERVATIONS["RT-60t"]


CONTROL_CONDITIONS = {
    "confined-positioning",
    "mid-radius-installation",
    "long-boom-high-lift",
    "jib-long-radius",
    "cycle-productivity",
    "precision-maintenance-lift",
    "urban-utility-installation",
    "industrial-shutdown-maintenance",
    "bridge-infrastructure-placement",
    "port-yard-handling",
}
SERVICE_CONDITIONS = {"rapid-mobilization", "industrial-shutdown-maintenance", "cycle-productivity"}


def field_observation(sheet_label: str, condition_id: str) -> dict[str, str] | None:
    group = FIELD_OBSERVATIONS.get(sheet_label)
    if not group:
        return None
    if condition_id == "all-weather-duty":
        return group.get("environment") or group.get("default")
    if condition_id in SERVICE_CONDITIONS:
        return group.get("service") or group.get("default")
    if condition_id in CONTROL_CONDITIONS:
        return group.get("control") or group.get("default")
    return group.get("default")

