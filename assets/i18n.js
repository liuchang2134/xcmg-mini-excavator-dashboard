(function () {
  'use strict';

  const STORAGE_KEY = 'xcmg-benchmark-language';
  const HAN = /[\u3400-\u9fff]/;
  const queryLanguage = new URLSearchParams(window.location.search).get('lang');
  let storedLanguage = '';
  try {
    storedLanguage = window.localStorage.getItem(STORAGE_KEY) || '';
  } catch (_) {
    storedLanguage = '';
  }
  const language = queryLanguage === 'en' || queryLanguage === 'zh'
    ? queryLanguage
    : (storedLanguage === 'en' ? 'en' : 'zh');

  const exactTranslations = {
    '全产品线竞品对标平台｜XCMG ARC': 'All-Product Competitive Benchmarking Platform | XCMG ARC',
    '全产品线竞品对标平台': 'All-Product Competitive Benchmarking Platform',
    '全产品线竞品': 'All-Product Competitive ',
    '对标平台': 'Benchmarking Platform',
    '全产品线竞品对标平台总览': 'All-Product Competitive Benchmarking Platform Overview',
    '由 XCMG ARC 独立开发，将竞品参数、配置差异和典型工况统一为可追溯的产品对标资产。': 'Developed independently by XCMG ARC, the platform consolidates competitor specifications, configuration differences, and representative work conditions into traceable benchmarking assets.',
    '平台总览': 'Platform Overview',
    '产品线入口': 'Product Lines',
    '挖掘机对标': 'Excavator Benchmarking',
    '挖掘机市场总览': 'Excavator Market Overview',
    '挖掘机分析中心': 'Excavator Analysis Center',
    '挖掘机吨级资产': 'Excavator Class Assets',
    '原始数据中心': 'Source Data Center',
    '平台应用价值': 'Platform Application Value',
    '页面导航': 'Page Navigation',
    '收起导航': 'Close Navigation',
    '关闭页面导航': 'Close Page Navigation',
    '快速进入产品分析': 'Quick Product Analysis',
    '产品线': 'Product Line',
    '吨级 / 类别': 'Tonnage / Category',
    'XCMG 型号': 'XCMG Model',
    '进入分析': 'Open Analysis',
    '产品线规划': 'Product Lines Planned',
    '已建吨级资产': 'Tonnage Assets Available',
    '对标产品型号': 'Benchmark Models',
    '平台关键状态': 'Platform Status',
    '市场画像': 'Market Snapshot',
    '北美挖掘机市场画像': 'North American Excavator Market Snapshot',
    '用市场份额确定重点竞品，用产品谱系连接到已建吨级资产。市场数据来自内部洞察材料，产品对标结论仍以各吨级原始数据为准。': 'Use market share to identify priority competitors and connect the XCMG portfolio to available tonnage-class assets. Market figures come from the internal insight deck; product benchmark findings remain governed by each class source workbook.',
    '2025 北美挖掘机品牌份额': '2025 North American Excavator Brand Share',
    '重点竞品集中度': 'Priority Competitor Concentration',
    '北美市场': 'North American Market',
    '0-10 吨市场份额': '0-10 t Market Share',
    '10 吨以上市场份额': 'Above 10 t Market Share',
    '0-10 吨': '0-10 t',
    '10 吨以上': 'Above 10 t',
    '前四品牌合计 74%': 'Top four brands: 74% combined',
    '前三品牌合计 69%': 'Top three brands: 69% combined',
    '数据来源：北美挖机产品线洞察 11.14；份额口径与年份按原材料呈现。': 'Source: North American Excavator Product-Line Insight 11.14. Share definitions and year are reproduced from the source deck.',
    'XCMG 挖掘机已建产品谱系': 'Available XCMG Excavator Benchmark Portfolio',
    '已建产品谱系': 'Available Benchmark Portfolio',
    '14 个吨级资产': '14 Tonnage-Class Assets',
    '15 个吨级资产': '15 Tonnage-Class Assets',
    '微挖': 'Mini Excavator',
    '小挖': 'Compact Excavator',
    '中挖': 'Mid-Size Excavator',
    '核心覆盖': 'Core Coverage',
    '扩展覆盖': 'Extended Coverage',
    '1-6 吨紧凑型与通用型资产连续覆盖。': 'Continuous benchmark coverage across the 1-6 t compact and general-purpose range.',
    '7-40 吨级补齐市政、土方、基础施工和重载场景。': 'The 7-40 t range extends coverage to municipal, earthmoving, foundation, and heavy-duty applications.',
    '7-60 吨级补齐市政、土方、基础施工和重载场景。': 'The 7-60 t range extends coverage to municipal, earthmoving, foundation, and heavy-duty applications.',
    '产品线对标入口': 'Product-Line Benchmarking',
    '产品线竞争力矩阵': 'Product-Line Benchmarking Matrix',
    '进入挖掘机分析板块': 'Open the excavator analysis section',
    '已接入': 'Available',
    '进入挖掘机板块，查看市场总体洞察及按吨级组织的十五个产品对标资产。': 'Open the excavator section for the market overview and fifteen product benchmark assets organized by tonnage class.',
    '进入挖掘机板块': 'Open Excavator Section',
    '挖掘机吨级分层': 'Excavator Tonnage Classification',
    '挖掘机吨级和型号筛选': 'Excavator Tonnage and Model Filter',
    '总体洞察覆盖北美市场、客户、竞争格局与产品型谱；十五个吨级统一覆盖狭窄空间、沟槽、土方装车、破碎、坡地和租赁六类典型工况，并提供参数与配置的产品级对标。': 'The category overview covers the North American market, customers, competitive landscape, and product portfolio. Fifteen tonnage-class assets consistently cover confined sites, trenching, truck loading, attachment work, slopes, and rental use, with product-level specification and configuration benchmarking.',
    '北美挖掘机市场总体洞察': 'North American Excavator Market Overview',
    '集中查看行业周期、吨级结构、客户与运输方式、竞争格局、真实工况、标杆体系、XCMG 产品型谱和跨吨级产品行动。': 'Review the industry cycle, tonnage structure, customers and transport methods, competitive landscape, real applications, benchmark systems, the XCMG portfolio, and cross-class product actions in one report.',
    '总体洞察覆盖主题': 'Market-overview topics',
    '市场与客户': 'Market and Customers',
    '竞争格局': 'Competitive Landscape',
    '真实工况': 'Real Applications',
    '标杆与型谱': 'Benchmarks and Portfolio',
    '产品行动': 'Product Actions',
    '打开总体洞察': 'Open Market Overview',
    '打开北美挖掘机市场总体洞察': 'Open the North American excavator market overview',
    '分吨级产品对标资产': 'Product Benchmark Assets by Tonnage Class',
    '产品图': 'Product Image',
    '已接入产品线可直接进入分析资产；其余产品线保留统一入口，完成数据和评价口径后开放。': 'Available product lines open their benchmarking assets directly. Remaining product lines retain a consistent entry point until source data and evaluation criteria are ready.',
    '进入挖掘机吨级资产列表': 'Open excavator tonnage assets',
    '进入资产': 'Open Assets',
    '待接入': 'Pending',
    '按吨级和应用场景分层': 'Structured by tonnage and application',
    '挖掘机系列已建立统一的吨级、工况、参数、配置贡献、综合排名和提升模拟模型，覆盖 14 个吨级区间。': 'Excavator assets use a consistent model for tonnage classes, work conditions, specifications, configuration contribution, overall ranking, and improvement simulation across 14 tonnage ranges.',
    '挖掘机系列已建立统一的吨级、工况、参数、配置贡献、综合排名和提升模拟模型，覆盖 15 个吨级区间。': 'Excavator assets use a consistent model for tonnage classes, work conditions, specifications, configuration contribution, overall ranking, and improvement simulation across 15 tonnage ranges.',
    '1-4 吨紧凑型': '1-4 t Compact',
    '4-6 吨通用型': '4-6 t General Purpose',
    '7-10 吨级': '7-10 t Class',
    '12-40 吨级': '12-40 t Class',
    '40-60 吨级': '40-60 t Class',
    'XE490U 40-60 吨级挖掘机': 'XE490U 40-60 t Excavator',
    'XCMG XE490U 40-60 吨级挖掘机竞品对标看板': 'XCMG XE490U 40-60 t Excavator Competitive Benchmark Dashboard',
    '40-60 吨级挖掘机对标': '40-60 t Excavator Benchmarking',
    '进入 XCMG XE490U 40-60 吨级对标看板': 'Open the XCMG XE490U 40-60 t benchmark dashboard',
    '装载与堆料': 'Loading and Stockpiling',
    '重点围绕装车效率、斗容匹配、行驶效率、油耗和驾驶舒适性。': 'Benchmark scope: truck-loading productivity, bucket-capacity matching, travel efficiency, fuel consumption, and operator comfort.',
    '压实设备': 'Compaction Equipment',
    '重点围绕压实能力、振动参数、转场效率和维护便利性。': 'Benchmark scope: compaction performance, vibration parameters, travel efficiency, and serviceability.',
    '重点围绕平地精度、牵引能力、刀板控制和驾驶辅助配置。': 'Benchmark scope: grading accuracy, drawbar performance, moldboard control, and operator-assist features.',
    '起重设备': 'Cranes and Lifting Equipment',
    '重点围绕起重能力、工况表、支腿布置、转场效率和安全系统。': 'Benchmark scope: lifting capacity, load charts, outrigger arrangement, roadability, and safety systems.',
    '矿用运输': 'Mining Haulage',
    '重点围绕载重、动力、矿区循环效率、制动性能和维护成本。': 'Benchmark scope: payload, powertrain, mine-cycle productivity, braking performance, and maintenance cost.',
    '高空作业平台': 'Mobile Elevating Work Platforms',
    '重点围绕作业高度、平台载荷、越野能力、电池系统和租赁适配。': 'Benchmark scope: working height, platform capacity, rough-terrain capability, battery system, and rental suitability.',
    '十四个吨级统一覆盖狭窄空间、沟槽、土方装车、破碎、坡地和租赁六类典型工况；卡片仅突出各吨级的差异化应用。': 'All 14 tonnage classes use six representative work conditions: confined sites, trenching, truck loading, attachment work, slopes, and rental use. Each asset row highlights only the applications that differentiate its class.',
    '十五个吨级统一覆盖狭窄空间、沟槽、土方装车、破碎、坡地和租赁六类典型工况；卡片仅突出各吨级的差异化应用。': 'All 15 tonnage classes use six representative work conditions: confined sites, trenching, truck loading, attachment work, slopes, and rental use. Each asset row highlights only the applications that differentiate its class.',
    '吨级筛选': 'Tonnage Filter',
    '全部吨级': 'All Tonnage Classes',
    '型号搜索': 'Model Search',
    '输入型号、吨级或近似拼写': 'Enter a model, tonnage class, or approximate spelling',
    '没有匹配的吨级或型号，请调整筛选条件。': 'No matching tonnage class or model. Adjust the filters.',
    '对标产品': 'Benchmark Models',
    '平台把竞品数据转化为统一、可追溯的产品对标资产，服务产品规划、工程评审、市场验证和数据治理。': 'The platform converts competitor data into consistent, traceable benchmarking assets for product planning, engineering review, market validation, and data governance.',
    '产品规划': 'Product Planning',
    '明确产品目标': 'Define Product Targets',
    '按吨级和工况识别运输尺寸、工作范围、液压性能和配置包的优先改进项。': 'Prioritize improvements to shipping dimensions, working range, hydraulic performance, and configuration packages by tonnage class and work condition.',
    '工程评审': 'Engineering Review',
    '量化竞品差距': 'Quantify Competitive Gaps',
    '将结论落实到具体参数、配置状态和数据来源，便于跨专业复核与方案评估。': 'Tie each conclusion to a specific specification, configuration status, and source for cross-functional review and concept evaluation.',
    '市场与销售': 'Market and Sales',
    '形成场景化论证': 'Build Application-Based Evidence',
    '把参数差异转化为客户工况、应用收益和配置建议，支持渠道与重点客户沟通。': 'Translate specification differences into customer work conditions, application benefits, and configuration recommendations for dealer and key-account discussions.',
    '数据治理': 'Data Governance',
    '保持口径可追溯': 'Maintain Traceable Criteria',
    '集中管理原始源表、评分规则和版本状态，确保不同产品线沿用一致的对标结构。': 'Centrally manage source workbooks, scoring rules, and revision status so each product line follows a consistent benchmarking structure.',
    '工程数据集中管理': 'Centralized Engineering Data Management',
    '原始数据中心｜XCMG ARC': 'Source Data Center | XCMG ARC',
    '返回 XCMG ARC 竞品对标平台主页': 'Return to the XCMG ARC benchmarking platform',
    '返回平台主页': 'Return to Platform Home',
    '按吨级集中管理竞品参数与标选配源表。可先进入对应对标页面查看分析，也可下载数据文件进行工程复核和版本更新。': 'Manage competitor specifications and standard/optional equipment source workbooks by tonnage class. Open the corresponding benchmark for analysis or download the workbook for engineering review and revision control.',
    '吨级数据集': 'Tonnage Datasets',
    '原始数据目录': 'Source Data Directory',
    '查找吨级或 XCMG 型号': 'Find a Tonnage Class or XCMG Model',
    '例如：3-4、XE225U、短尾': 'Example: 3-4, XE225U, short-tail',
    '数据内容': 'Dataset Contents',
    '对标页面': 'Benchmark Page',
    '数据文件': 'Data File',
    '竞品参数、标配/选配状态与数据来源': 'Competitor specifications, standard/optional equipment status, and sources',
    '查看对标': 'Open Benchmark',
    '下载数据': 'Download Data',
    '没有匹配的数据集，请调整关键词。': 'No matching dataset. Adjust the search terms.',
    '对标概览': 'Benchmark Overview',
    '总体评分': 'Overall Evaluation',
    '总体评分（不分细分工况）': 'Overall Evaluation (All Work Conditions)',
    '工况竞争格局': 'Competitive Position by Work Condition',
    '工况总览': 'Work-Condition Overview',
    '原始数据': 'Source Data',
    '返回对标平台主页': 'Return to Benchmarking Platform',
    '返回全产品线竞品对标平台主页': 'Return to the All-Product Benchmarking Platform',
    '回到页面顶部': 'Return to Page Top',
    '回到顶部': 'Back to Top',
    '顶部': 'Top',
    'XCMG ARC 独立开发': 'Developed Independently by XCMG ARC',
    '本页按照统一口径展示参数、标选配、典型工况、配置贡献、差距来源和提升模拟。全部结论可追溯至原始数据表和来源登记。': 'This page applies consistent criteria to specifications, standard/optional equipment, representative work conditions, configuration contribution, gap drivers, and improvement simulations. Every conclusion is traceable to the source workbook and source register.',
    '查看工况对标': 'View Work-Condition Benchmarking',
    '导出原始 Excel': 'Export Source Excel',
    '对标产品数': 'Benchmark Model Count',
    '含 XCMG 与主流竞品': 'Includes XCMG and key competitors',
    'XCMG 总体排名': 'XCMG Overall Rank',
    '参数与配置综合': 'Specifications and equipment combined',
    'XCMG 总体得分': 'XCMG Overall Score',
    '参数 65% / 配置 35%': 'Specifications 65% / Equipment 35%',
    'XCMG 数据覆盖': 'XCMG Data Coverage',
    '完整度等级：高': 'Completeness: High',
    '完整度等级：中': 'Completeness: Medium',
    '完整度等级：有限': 'Completeness: Limited',
    '评分口径：参数综合分 65% + 标选配综合分 35%；工况评分单独展示，不重复计入总体分。': 'Evaluation basis: specification score 65% + equipment score 35%. Work-condition scores are reported separately and are not counted twice.',
    '总体评分排名': 'Overall Evaluation Ranking',
    'XCMG 总体差距分析': 'XCMG Overall Gap Analysis',
    '完整评分明细': 'Complete Evaluation Detail',
    '产品': 'Product',
    '总体': 'Overall',
    '参数': 'Specification',
    '配置': 'Equipment',
    '数据覆盖': 'Data Coverage',
    '数据覆盖率': 'Data Coverage',
    '模拟标配': 'Simulate as Standard',
    '地面正前方3m远': 'Front Lift at 3 m',
    '地面侧方3m远处': 'Side Lift at 3 m',
    '左/右': 'Left / Right',
    '轴距': 'Wheelbase',
    '完整度等级': 'Completeness',
    '工况雷达图': 'Work-Condition Radar Chart',
    '当前：全部品牌': 'Current: All Brands',
    '当前：未选择品牌': 'Current: No Brand Selected',
    '选择对比品牌': 'Select Brands to Compare',
    '工况综合排名（按 6 类工况）': 'Overall Work-Condition Ranking (6 Conditions)',
    '默认显示 XCMG 与工况领先产品；点击图例可增加或取消品牌，全部取消后恢复全品牌展示。': 'All brands are shown by default. Select legend items to add or remove brands; clearing the selection restores all brands.',
    '排名口径：工况字段覆盖率低于 60% 的产品不进入正式排名；缺失项仍保留在指标明细中。': 'Ranking basis: products with less than 60% field coverage for a work condition are excluded from the formal ranking. Missing fields remain visible in the detailed matrix.',
    '覆盖率低于 60% 的产品不进入排名，仍在右侧表格中保留并标记为“数据不足”。': 'Products with less than 60% data coverage are excluded from the ranking and remain listed in the table as “Insufficient Data.”',
    '总体评分、参数评分、配置评分及数据覆盖': 'Overall, specification, and equipment evaluations with data coverage',
    '总体评分、参数评分、配置评分及数据覆盖率': 'Overall, specification, and equipment evaluations with data coverage',
    '典型工况': 'Representative Work Condition',
    '工况特点：': 'Work-condition requirements:',
    '有益配置：': 'Beneficial equipment:',
    '工况评分排名': 'Work-Condition Ranking',
    '关键参数 / 配置雷达图': 'Key Specification / Equipment Radar',
    'XCMG关键项': 'XCMG Key Items',
    '类型': 'Type',
    '关键项': 'Key Item',
    '当前对标产品': 'Current XCMG Benchmark Model',
    '参数与配置实差': 'Documented Specification and Equipment Gaps',
    '当前资料未显示明确落后项': 'No Explicit Disadvantage in the Current Dataset',
    '继续复核缺失字段、配置口径和来源版本，避免把未披露信息误判为无配置。': 'Continue validating missing fields, equipment definitions, and source revisions so undisclosed information is not misclassified as unavailable equipment.',
    '数据复核': 'Data Validation',
    '来源与口径': 'Sources and Definitions',
    '补齐缺失字段并核验同版本、同配置条件后再形成产品目标。': 'Complete missing fields and verify like-for-like revisions and configurations before setting product targets.',
    '图片来源：徐工官方施工案例，仅用于工况示意；本页参数、配置和排名仍以对应吨级原始数据为准。': 'Image source: official XCMG construction cases, used only to illustrate work conditions. Specifications, equipment status, and rankings remain based on the source workbook for this tonnage class.',
    '徐工挖掘机在受限道路边施工的工况示意': 'XCMG excavator illustrating work beside a constrained roadway',
    '徐工挖掘机进行基础施工的工况示意': 'XCMG excavator illustrating foundation work',
    '徐工挖掘机进行土方装车的工况示意': 'XCMG excavator illustrating earthmoving and truck loading',
    '徐工挖掘机在岩石施工现场作业的工况示意': 'XCMG excavator illustrating work on a rocky jobsite',
    '徐工挖掘机在坡地和松软地面施工的工况示意': 'XCMG excavator illustrating slope and soft-ground work',
    '多台徐工挖掘机协同施工的工况示意': 'Multiple XCMG excavators illustrating fleet operation',
    '得分': 'Score',
    '权重': 'Weight',
    '工况相关项：': 'Work-condition inputs:',
    '全部指标贡献明细': 'Complete Item Contribution Detail',
    '指标/配置': 'Specification / Equipment',
    '对工况影响': 'Effect on Work Condition',
    '数据状态': 'Data Status',
    '指标得分': 'Item Score',
    '贡献分': 'Contribution',
    '相关性说明': 'Relevance',
    'XCMG 与竞品差距及建议动作': 'XCMG Competitive Gaps and Recommended Actions',
    '1. 对标参照': '1. Benchmark Reference',
    '2. 硬参数差距': '2. Specification Gaps',
    '3. 配置缺口': '3. Equipment Gaps',
    '4. 建议动作': '4. Recommended Actions',
    '提升模拟方案': 'Improvement Simulation',
    'XCMG 提升模拟器': 'XCMG Improvement Simulator',
    '清除选择': 'Clear Selection',
    '模拟结果仅反映当前评分模型，不替代工程验证、成本评审和市场需求判断。': 'Simulation results reflect the current evaluation model only and do not replace engineering validation, cost review, or market-demand assessment.',
    '模拟工况分': 'Simulated Work-Condition Score',
    '排名计算中': 'Calculating Rank',
    '数据口径': 'Data Basis',
    '本页评分基于对应原始 Excel；空白项标记为“待核验”，不等同于无配置。数值范围按区间中值计算，系统流量按泵组流量合计，行走速度拆分高、低速档。数据来源及核验状态详见来源登记表。': 'This evaluation uses the corresponding source Excel workbook. Blank fields are marked “Verification Pending” and do not mean “Not Available.” Numeric ranges use the interval midpoint; main pump flow is summed by pump group; travel speed is separated into low and high ranges. See the source register for provenance and verification status.',
    '下载来源登记表': 'Download Source Register',
    '全量参数与配置': 'All Specifications and Equipment',
    '标选配': 'Standard / Optional Equipment',
    '全部原始参数数据': 'All Source Specification Data',
    '全部原始标选配数据': 'All Source Standard / Optional Equipment Data',
    '类别': 'Category',
    '指标': 'Specification',
    '单位': 'Unit',
    '展开': 'Expand',
    '收起': 'Collapse',
    '狭窄空间 / 市政庭院': 'Confined Sites / Municipal and Residential',
    '沟槽 / 基础深挖': 'Trenching / Foundation Excavation',
    '土方装车 / 短循环效率': 'Truck Loading / Short-Cycle Productivity',
    '破碎 / 多属具作业': 'Breaker / Multi-Attachment Work',
    '坡地 / 软土 / 吊装稳定': 'Slopes / Soft Ground / Lifting Stability',
    '租赁 / 快速转场 / 多客户通用': 'Rental / Fast Relocation / Multi-Operator Use',
    '狭窄空间': 'Confined Sites',
    '沟槽': 'Trenching',
    '土方装车': 'Truck Loading',
    '破碎': 'Breaker Work',
    '坡地': 'Slopes and Soft Ground',
    '租赁': 'Rental Use',
    '看重窄机身、短尾回转、较小运输尺寸和贴边作业能力。': 'Prioritizes a narrow machine envelope, reduced tail swing, compact transport dimensions, and close-to-wall operation.',
    '可伸缩底盘、动臂偏摆、推土铲偏摆和安全摄像头有助于庭院、市政和受限空间作业。': 'A variable-width undercarriage, boom swing, angle blade, and safety camera support yard, municipal, and confined-site work.',
    '核心是下挖深度、挖掘半径、斗杆挖掘力和长斗杆覆盖能力。': 'Key requirements are digging depth, digging reach, stick digging force, and long-stick coverage.',
    '长斗杆、AUX 管路和动臂斗杆防爆阀有助于深沟、管线和基础作业。': 'A long stick, auxiliary hydraulic lines, and boom/stick hose-burst protection valves support deep trenching, utility, and foundation work.',
    '看卸载高度、挖掘力、液压流量、回转和行走响应。': 'Prioritizes dump clearance, digging forces, hydraulic flow, swing response, and travel response.',
    '经济模式、自动怠速、推土铲浮动和快换管路影响短循环油耗与辅助动作效率。': 'Economy mode, auto idle, blade float, and quick-coupler lines affect short-cycle fuel consumption and auxiliary-function productivity.',
    '重点是液压系统流量、压力和 AUX 管路覆盖。': 'Prioritizes hydraulic flow, pressure, and auxiliary-circuit availability.',
    'AUX1/AUX2 管路、卸油管路、流量保持和快换管路影响破碎锤、拇指夹、螺旋钻等属具适配。': 'Auxiliary Circuit 1/2 lines, a case-drain line, continuous-flow control, and quick-coupler lines determine compatibility with breakers, thumbs, augers, and other attachments.',
    '关注接地比压、履带宽度、牵引、爬坡和起吊能力。': 'Prioritizes ground pressure, track shoe width, traction, gradeability, and lift capacity.',
    '副配重和推土铲浮动有助于改善稳定性与整平效率；起吊边界仍应以载荷表和作业规范为准。': 'A counterweight and blade float can improve stability and grading productivity; lifting limits remain governed by the load chart and operating procedures.',
    '看运输尺寸、油耗管理、易用性、安全提醒和远程管理。': 'Prioritizes transport dimensions, fuel management, ease of operation, safety alerts, and remote fleet management.',
    '自动怠速、自动停机、远程信息处理、防盗、摄像头和报警配置会影响油耗管理、资产管理和多客户使用便利性。': 'Auto idle, auto engine shutdown, telematics, anti-theft protection, cameras, and warning systems affect fuel management, asset control, and multi-operator usability.',
    '越窄越适合入户、园林和人行道受限空间。': 'A narrower machine is better suited to residential access, landscaping, and confined sidewalk work.',
    '短车身转场和狭小现场调头更灵活。': 'A shorter machine improves relocation and turning in confined sites.',
    '尾扫越小越不容易碰墙、碰车和碰围挡。': 'Less tail overhang reduces the risk of striking walls, vehicles, and barriers.',
    '越能贴边开沟、贴墙清底，狭窄空间收益越高。': 'Greater boom swing improves close-to-wall trenching and cleanout in confined spaces.',
    '窄处收窄、开阔处展开，兼顾通过性和稳定性。': 'Retracts for narrow access and extends on open ground to balance access and stability.',
    '角落回填和边沟修整时减少重复调车。': 'Reduces machine repositioning during corner backfill and roadside-ditch finishing.',
    '后视或环视能力可以降低城市巷道和庭院倒车风险。': 'Rear or surround visibility can reduce reversing risk in urban alleys and yards.',
    '人车混行环境降低安全风险。': 'Reduces risk where personnel and machines share the work area.',
    '市政施工和租赁场景提高周边可感知性。': 'Improves machine conspicuity in municipal and rental applications.',
    '深度决定基础沟槽和管线施工覆盖范围。': 'Digging depth determines coverage for foundation trenches and utility installation.',
    '半径越大，站位不变时覆盖面越宽。': 'Greater reach expands the work envelope without repositioning the machine.',
    '平面沟槽连续开挖效率更高。': 'Greater ground-level reach improves continuous trenching productivity.',
    '深挖末端破土和清底能力。': 'Supports breakout and cleanout at the far end of a deep trench.',
    '斗杆长度影响标配状态下的深挖覆盖。': 'Standard stick length affects deep-excavation coverage in base configuration.',
    '选配斗杆说明是否可向深挖场景扩展。': 'Optional stick availability indicates whether the machine can extend into deeper excavation applications.',
    '深沟和管线施工直接增益配置。': 'Directly benefits deep-trench and utility work.',
    '基础施工和吊装附近作业的安全配置。': 'A safety provision for foundation work and operations near lifting activities.',
    '便于搭配夯实、破碎和清沟属具。': 'Supports compactors, breakers, and ditch-cleaning attachments.',
    '旋转类属具扩展能力。': 'Expands compatibility with rotating attachments.',
    '影响能否顺利装车和越过车厢。': 'Determines whether the machine can load a truck cleanly and clear the body side.',
    '装料、切土和短循环满斗能力。': 'Supports bucket fill, cutting performance, and full-bucket short cycles.',
    '连续挖装时保持切入力。': 'Maintains penetration force during continuous excavating and loading.',
    '复合动作速度与液压响应。': 'Drives combined-function speed and hydraulic response.',
    '连续循环中的动力储备。': 'Provides power reserve during continuous cycles.',
    '动力系统基础能力。': 'Indicates the base capability of the powertrain.',
    '场内短距离转场效率。': 'Improves short-distance travel productivity within the site.',
    '接近卡车和料堆时的精细行走控制。': 'Supports precise low-speed travel near trucks and stockpiles.',
    '短循环挖装回转效率。': 'Affects swing productivity during short loading cycles.',
    '轻载和市政土方循环中控制油耗。': 'Helps control fuel consumption in light-duty and municipal earthmoving cycles.',
    '等待装车和短暂停顿时降低怠速油耗。': 'Reduces idle fuel consumption while waiting to load or during brief pauses.',
    '回填、整平、清底动作效率更高。': 'Improves backfilling, grading, and cleanup productivity.',
    '多属具切换减少停机时间。': 'Reduces downtime when changing attachments.',
    '决定液压属具连续工作的供油基础。': 'Defines the oil-flow foundation for continuous hydraulic-attachment operation.',
    '破碎、夹持和钻孔属具输出能力。': 'Supports breaker, grapple, and auger output capability.',
    '主属具回路供油能力。': 'Indicates available flow for the primary attachment circuit.',
    '主属具负载能力。': 'Indicates load capability of the primary attachment circuit.',
    '旋转/夹持类辅回路能力。': 'Indicates secondary-circuit capability for rotating or clamping attachments.',
    '决定辅回路可匹配属具的压力范围。': 'Determines the attachment pressure range supported by the secondary circuit.',
    '破碎锤和常规属具基础配置。': 'Base provision for breakers and conventional hydraulic attachments.',
    '旋转夹、拇指夹等复合属具更友好。': 'Improves compatibility with rotating grapples, hydraulic thumbs, and other multi-function attachments.',
    '破碎锤回油保护和热管理。': 'Supports breaker return-oil protection and thermal management.',
    '连续属具输出更稳定。': 'Stabilizes continuous attachment output.',
    '多属具场景减少切换时间。': 'Reduces changeover time in multi-attachment applications.',
    '较宽履带通常有助于降低接地比压并改善稳定性，但会增加运输宽度。': 'Wider track shoes generally reduce ground pressure and improve stability, but increase transport width.',
    '越低越适合软土、草地和回填土表面。': 'Lower ground pressure is better suited to soft soil, turf, and backfilled surfaces.',
    '坡地转场和湿软场地脱困能力。': 'Supports relocation on slopes and recovery in wet or soft ground.',
    '反映设备上下坡和转场能力，不等同于允许作业坡度。': 'Indicates uphill/downhill travel capability; it is not the allowable working slope.',
    '放铲吊装代表稳定边界。': 'Blade-down lifting indicates the supported stability boundary.',
    '无支撑状态下的保守吊装能力。': 'Indicates conservative lift capability without blade support.',
    '侧方吊装稳定性。': 'Indicates side-lift stability.',
    '可改善稳定性和额定起吊能力，具体以载荷表为准。': 'Can improve stability and rated lift capacity; use the applicable load chart for limits.',
    '可提升整平效率，不能替代坡地稳定性验证。': 'Can improve grading productivity but does not replace slope-stability validation.',
    '拖车、仓库和门洞通过性。': 'Affects trailer, warehouse, and doorway access.',
    '拖车装载和仓储占地。': 'Affects trailer loading and storage footprint.',
    '低矮通道和运输合规性。': 'Affects low-clearance access and transport compliance.',
    '拖车级别和租赁客户自提门槛。': 'Determines trailer class and customer pickup requirements.',
    '场内快速转场效率。': 'Improves rapid relocation within the site.',
    '多客户使用时的低速操控友好性。': 'Improves low-speed controllability for multiple operators.',
    '减少等待和停顿阶段的怠速油耗。': 'Reduces idle fuel consumption during waiting and pauses.',
    '降低无效怠速、油耗和租赁客户使用成本。': 'Reduces unnecessary idling, fuel consumption, and rental-customer operating cost.',
    '定位、工时、维保和资产管理。': 'Supports location, operating-hours, maintenance, and asset management.',
    '租赁资产防盗和授权使用。': 'Supports theft prevention and authorized use of rental assets.',
    '多客户使用更方便。': 'Improves ease of use across multiple customers and operators.',
    '基础便利配置。': 'Provides basic operator convenience.',
    '租赁客户通用便利性。': 'Provides broadly useful convenience for rental customers.',
    '提高设备在市政和工地环境中的可见性。': 'Improves machine visibility in municipal and construction-site environments.',
    '人员密集场景安全提醒。': 'Provides a safety warning in personnel-dense work areas.',
    '跨季节租赁适用性。': 'Improves rental suitability across seasons.',
    '多客户倒车和近机作业安全。': 'Improves reversing and near-machine safety for multiple operators.',
    '租赁资产区域管理。': 'Supports geofenced management of rental assets.',
    '夜间停机和离场便利性。': 'Improves convenience when shutting down and leaving the site at night.',
    '配置项暂未发现明确弱项，建议继续核验竞品配置资料并维护现有标配口径。': 'No clear equipment disadvantage is currently documented. Continue verifying competitor equipment data and maintain the present standard-equipment basis.',
    '-分': '—',
    '无': 'No',
    '是': 'Yes',
    '否': 'No',
    '运输参数': 'Transport Dimensions',
    '接地参数': 'Undercarriage / Ground Contact',
    '工作参数': 'Working Range',
    '动力': 'Engine / Power',
    '工作装置': 'Front Attachment',
    '液压系统': 'Hydraulic System',
    '行走': 'Travel System',
    '回转': 'Swing System',
    '挖掘力': 'Digging Forces',
    '起吊能力': 'Lift Capacity',
    '发动机': 'Engine',
    '驾驶环境': 'Operator Environment',
    '电器系统': 'Electrical System',
    '电气系统': 'Electrical System',
    '工装底盘': 'Attachments / Undercarriage',
    '整机运输宽度': 'Overall Shipping Width',
    '整机运输长度': 'Overall Shipping Length',
    '整机运输高度': 'Overall Shipping Height',
    '操作重量': 'Operating Weight',
    '尾部回转半径': 'Tail Swing Radius',
    '履带宽度': 'Track Shoe Width',
    '履带长度': 'Track Length',
    '轨距': 'Track Gauge',
    '接地比压': 'Ground Pressure',
    '最大挖掘高度': 'Maximum Digging Height',
    '最大卸载高度': 'Maximum Dump Clearance',
    '最大挖掘深度': 'Maximum Digging Depth',
    '最大挖掘半径': 'Maximum Digging Reach',
    '最大地面挖掘半径': 'Maximum Reach at Ground Level',
    '发动机总功率': 'Gross Engine Power',
    '发动机净功率': 'Net Engine Power',
    '标配动臂': 'Standard Boom Length',
    '标配斗杆': 'Standard Stick Length',
    '选配斗杆': 'Optional Stick Length',
    '系统流量': 'Main Pump Flow',
    '工作压力': 'Operating Pressure - Equipment',
    '行走压力': 'Operating Pressure - Travel',
    '回转压力': 'Operating Pressure - Swing',
    'AUX1流量': 'Auxiliary Circuit 1 Flow',
    'AUX1压力': 'Auxiliary Circuit 1 Pressure',
    'AUX2流量': 'Auxiliary Circuit 2 Flow',
    'AUX2压力': 'Auxiliary Circuit 2 Pressure',
    '行走速度（低速/高速）': 'Travel Speed (Low / High)',
    '行走速度（低速）': 'Travel Speed - Low',
    '行走速度（高速）': 'Travel Speed - High',
    '最大牵引力': 'Maximum Drawbar Pull',
    '爬坡能力': 'Gradeability',
    '回转速度': 'Machine Swing Speed',
    '动臂偏摆（左/右）': 'Boom Swing (Left / Right)',
    '铲斗挖掘力': 'Bucket Digging Force',
    '斗杆挖掘力': 'Stick Digging Force',
    '地面正前方3m远处起吊能力（放下推土铲）': 'Front Lift Capacity at 3 m, Ground Level (Blade Down)',
    '地面正前方3m远处起吊能力（抬起推土铲）': 'Front Lift Capacity at 3 m, Ground Level (Blade Up)',
    '地面侧方3m远处起吊能力': 'Side Lift Capacity at 3 m, Ground Level',
    '地面正前方4.5m远处起吊能力（放下推土铲）': 'Front Lift Capacity at 4.5 m, Ground Level (Blade Down)',
    '地面正前方4.5m远处起吊能力（抬起推土铲）': 'Front Lift Capacity at 4.5 m, Ground Level (Blade Up)',
    '地面正前方4.5m远处起吊能力': 'Front Lift Capacity at 4.5 m, Ground Level',
    '地面侧方4.5m远处起吊能力': 'Side Lift Capacity at 4.5 m, Ground Level',
    '地面正前方6m远处起吊能力': 'Front Lift Capacity at 6 m, Ground Level',
    '地面侧方6m远处起吊能力': 'Side Lift Capacity at 6 m, Ground Level',
    '全产品线竞品对标平台｜挖掘机 14 个吨级区间': 'All-Product Competitive Benchmarking Platform | 14 Excavator Tonnage Classes',
    '全产品线竞品对标平台｜挖掘机 15 个吨级区间': 'All-Product Competitive Benchmarking Platform | 15 Excavator Tonnage Classes',
    '已建立统一的吨级、工况、参数、配置贡献、综合排名和提升模拟模型，可直接进入十四个吨级看板。': 'A consistent model now covers tonnage classes, work conditions, specifications, configuration contribution, overall ranking, and improvement simulation across 14 dashboards.',
    '已建立统一的吨级、工况、参数、配置贡献、综合排名和提升模拟模型，可直接进入十五个吨级看板。': 'A consistent model now covers tonnage classes, work conditions, specifications, configuration contribution, overall ranking, and improvement simulation across 15 dashboards.',
    '是否有Cab版本': 'Cab Availability',
    '密码防盗': 'PIN-Code Anti-Theft',
    'Optional8英寸触屏': 'Optional 8-in Touchscreen Display',
    'Optional8英寸Touchscreen Display': 'Optional 8-in Touchscreen Display',
    'Optional7英寸Touchscreen Display': 'Optional 7-in Touchscreen Display',
    'Cab版Optional 2D/3D': 'Cab Version: Optional 2D/3D Grade Control',
    'Cab版Standard 2D/3D': 'Cab Version: Standard 2D/3D Grade Control',
    'Optional缸体加热': 'Optional Engine Block Heater',
    'Optional缸体加热器': 'Optional Engine Block Heater',
    '270°摄像头': '270° Camera System',
    '270°视摄像头': '270° Surround-View Camera System',
    '360°/270°视摄像头': '360° / 270° Surround-View Camera System',
    'Optional2D/3D+ 激光捕捉': 'Optional 2D/3D Grade Control with Laser Catcher',
    'Standard2D Optional3D及激光捕捉': 'Standard 2D; Optional 3D Grade Control and Laser Catcher',
    'Standard2D及激光捕捉': 'Standard 2D Grade Control and Laser Catcher',
    'Standard 动臂/铲斗/Swing System/平地/Lift Assist': 'Standard Boom Assist / Bucket Assist / Swing Assist / Grade Assist / Lift Assist',
    'Standard 动臂/Bucket/Swing System/平地/Lift Assist': 'Standard Boom Assist / Bucket Assist / Swing Assist / Grade Assist / Lift Assist',
    'Standard: 平地 动臂 铲斗 Swing 起吊': 'Standard: Grade Assist / Boom Assist / Bucket Assist / Swing Assist / Lift Assist',
    'Standard: 平地 动臂 Bucket Swing 起吊': 'Standard: Grade Assist / Boom Assist / Bucket Assist / Swing Assist / Lift Assist',
    'Standard: 平地 动臂 铲斗 Swing System 起吊': 'Standard: Grade Assist / Boom Assist / Bucket Assist / Swing Assist / Lift Assist',
    'Standard: 平地 动臂 Bucket Swing System 起吊': 'Standard: Grade Assist / Boom Assist / Bucket Assist / Swing Assist / Lift Assist',
    'Standard: 平地 铲斗 Swing System 起吊': 'Standard: Grade Assist / Bucket Assist / Swing Assist / Lift Assist',
    'Standard: 平地 Bucket Swing System 起吊': 'Standard: Grade Assist / Bucket Assist / Swing Assist / Lift Assist',
    'Standard: Swing System Truck Loading 平地 修破 Bucket Assist': 'Standard: Swing Assist / Truck Loading Assist / Grade Assist / Trenching and Breaker Assist / Bucket Assist',
    'Standard前窗天窗 Optional后窗': 'Standard Front Windshield and Skylight; Optional Rear Window',
    'Swing Systemvs动臂, 优先级可调': 'Adjustable Swing / Boom Priority',
    '动臂上升及Swing, 优先级可调': 'Adjustable Boom-Raise / Swing Priority',
    'Swing System报警': 'Swing Alarm',
    '动臂浮动': 'Boom Float',
    '动作优先': 'Work-Function Priority',
    '斗杆快收阀': 'Arm Regeneration Valve',
    'Breaker Work锤回油过滤': 'Breaker Return-Line Filter',
    'Breaker Work锤自动停止': 'Automatic Breaker Stop',
    '电风扇': 'Electric Cooling Fan',
    '三种': 'Three Modes',
    '强力/智能/经济': 'Power / Intelligent / Economy',
    '强力/经济/起吊/Breaker Work': 'Power / Economy / Lifting / Breaker',
    '偏置动臂 Offset Boom': 'Offset Boom',
    '偏置动臂 offset boom': 'Offset Boom',
    '辅助动作': 'Auxiliary Function',
    '过载报警': 'Overload Warning',
    '远程操控': 'Remote Control',
    '遮阳': 'Sunshade',
    '遮雨棚': 'Rain Guard',
    '超长工装': 'Super Long-Reach Front',
    '4300kg 5490kg 超长臂用': '4,300 kg / 5,490 kg for Super Long-Reach Front',
    '4600kg 5400kg 超长臂用': '4,600 kg / 5,400 kg for Super Long-Reach Front',
    '配重': 'Counterweight',
    '铲斗': 'Bucket',
    '铲斗 m³': 'Bucket Capacity (m³)',
    'GP: 0.2-0.76 HD: 0.31-0.53 清理斗: 0.57/0.74': 'GP: 0.2-0.76; HD: 0.31-0.53; Ditch-Cleaning: 0.57/0.74',
    'GP: 0.55-1.59 HD: 0.46-1.38 SD: 0.46-1.19 清理斗: 1.01-1.76': 'GP: 0.55-1.59; HD: 0.46-1.38; SD: 0.46-1.19; Ditch-Cleaning: 1.01-1.76',
    '吨级': 'Tonnage Class',
    '标配': 'Standard',
    '选配': 'Optional',
    '无配置': 'Not Available',
    '待核验': 'Verification Pending',
    '有效数据': 'Valid Data',
    '数据不足': 'Insufficient Data',
    '高': 'High',
    '中': 'Medium',
    '有限': 'Limited'
  };

  const technicalTerms = {
    'Cab顶': 'Cab Roof',
    '四角式': 'Four-Corner Type',
    '不带': 'without ',
    '竞品对标看板': 'Competitive Benchmark Dashboard',
    '总体评分、参数评分、配置评分及数据覆盖': 'Overall, specification, and equipment evaluations with data coverage',
    '全部指标与配置贡献明细': 'Complete Specification and Equipment Contribution Detail',
    '关键项及权重': 'Key Items and Weights',
    '关键参数 / 配置对比': 'Key Specification / Equipment Comparison',
    '配置项累计贡献': 'Cumulative Equipment Contribution',
    '主要差距项': 'Primary Gap Items',
    '硬参数差距': 'Specification Gaps',
    '配置差距': 'Equipment Gaps',
    '对标参照': 'Benchmark Reference',
    '工况表现': 'Work-Condition Performance',
    '数据覆盖': 'Data Coverage',
    '距领先产品': 'behind the leader by',
    '不进入排名': 'excluded from the ranking',
    '数据不足': 'Insufficient Data',
    '动臂偏摆': 'Boom Swing',
    'AUX 管路': 'auxiliary hydraulic lines',
    '远程信息处理': 'Telematics',
    'USB电源': 'USB Power Outlet',
    '密码启动': 'PIN Start',
    '左偏摆少': 'left swing is lower by',
    '左偏摆多': 'left swing is greater by',
    '右偏摆少': 'right swing is lower by',
    '搭配选配仪表': 'paired with the optional display',
    '驾驶室版本制热': 'Cab Heating',
    '驾驶室版本制冷': 'Cab Air Conditioning',
    '兼容拇指钳': 'Thumb-Ready',
    '600mm履带': '600 mm Track Shoes',
    '六向铲': 'Six-Way Blade',
    '6向铲': 'Six-Way Blade',
    '选配动臂': 'Optional Boom',
    '偏摆动臂': 'Swing Boom',
    '二节臂': 'Two-Piece Boom',
    '增压压力': 'Boost Pressure',
    '回转力矩': 'Swing Torque',
    '副配重影响': 'counterweight dependent',
    'Counterweight影响': 'counterweight dependent',
    '可伸缩': 'Extendable',
    '合流': 'combined flow',
    '需确认': 'Verification Pending',
    '配置': 'Equipment',
    '对标': 'Benchmark',
    '可直接进入完整竞品对标看板': 'Full benchmark dashboard available',
    '全产品线竞品': 'All-Product Competitive',
    '小型挖掘机': 'Compact Excavator',
    '高空作业平台': 'Mobile Elevating Work Platforms',
    '装载机': 'Wheel Loaders',
    '压路机': 'Rollers',
    '平地机': 'Motor Graders',
    '挖掘机': 'Excavator',
    '装载效率': 'Loading Productivity',
    '燃油消耗': 'Fuel Consumption',
    '油耗': 'Fuel Consumption',
    '驾驶舒适性': 'Operator Comfort',
    '舒适性': 'Operator Comfort',
    '平地精度': 'Grading Accuracy',
    '载荷曲线': 'Load Charts',
    '安全系统': 'Safety Systems',
    '作业高度': 'Working Height',
    '平台载荷': 'Platform Capacity',
    '租赁适配': 'Rental Suitability',
    '属具适配': 'Attachment Compatibility',
    '运输边界': 'Transport Envelope',
    '液压属具': 'Hydraulic Attachments',
    '驾驶安全': 'Operator Safety',
    '沟槽深挖': 'Deep Trenching',
    '吊装稳定': 'Lifting Stability',
    '基础深挖': 'Foundation Excavation',
    '重载挖掘': 'Heavy-Duty Excavation',
    '短尾回转': 'Reduced Tail Swing',
    '受限空间': 'Confined Sites',
    '受限场地': 'Confined Worksites',
    '重载土方': 'Heavy Earthmoving',
    '入户 / 庭院': 'Residential Access / Yard Work',
    '市政施工': 'Municipal Work',
    '窄场地': 'Confined Sites',
    '短循环': 'Short-Cycle Work',
    '压实': 'Compaction',
    '振动': 'Vibration',
    '转场': 'Relocation',
    '牵引': 'Traction',
    '控制': 'Control Systems',
    '支腿': 'Outriggers',
    '载重': 'Payload',
    '吊装': 'Lifting',
    '装车': 'Truck Loading',
    '深挖': 'Deep Excavation',
    '道路施工': 'Road Construction',
    '多属具': 'Multi-Attachment Work',
    '大挖': 'Large Excavator',
    '大型土方': 'Large-Scale Earthmoving',
    '矿山剥离': 'Mine Stripping',
    '重载装车': 'Heavy-Duty Truck Loading',
    '高产能': 'High Productivity',
    '重载': 'Heavy Duty',
    '待接入': 'Pending',
    '远程信息处理系统模拟标配': 'Simulate Telematics as Standard',
    '动臂斗杆防爆阀模拟标配': 'Simulate Boom / Stick Hose-Burst Protection Valves as Standard',
    '工作灯延迟关闭模拟标配': 'Simulate Delayed Work-Light Shutdown as Standard',
    '可伸缩底盘模拟标配': 'Simulate Variable-Width Undercarriage as Standard',
    '安全摄像头模拟标配': 'Simulate Safety Camera as Standard',
    '推土铲偏摆模拟标配': 'Simulate Angle Blade as Standard',
    '推土铲浮动模拟标配': 'Simulate Blade Float as Standard',
    '自动停机模拟标配': 'Simulate Auto Engine Shutdown as Standard',
    '自动怠速模拟标配': 'Simulate Auto Idle as Standard',
    '卸油管路模拟标配': 'Simulate Case-Drain Line as Standard',
    '行走报警模拟标配': 'Simulate Travel Alarm as Standard',
    '电子围栏模拟标配': 'Simulate Geofencing as Standard',
    '驾驶室温控模拟标配': 'Simulate Cab Climate Control as Standard',
    '长斗杆模拟标配': 'Simulate Long Stick as Standard',
    '副配重模拟标配': 'Simulate Counterweight as Standard',
    '一键启动模拟标配': 'Simulate Push-Button Start as Standard',
    '手机托模拟标配': 'Simulate Phone Holder as Standard',
    '经济模式模拟标配': 'Simulate Economy Mode as Standard',
    '快换管路模拟标配': 'Simulate Quick-Coupler Lines as Standard',
    '流量保持模拟标配': 'Simulate Continuous-Flow Control as Standard',
    '密码启动/防盗模拟标配': 'Simulate PIN Start / Anti-Theft as Standard',
    '尾部回转半径对标': 'Benchmark Tail Swing Radius',
    '整机运输宽度对标': 'Benchmark Overall Shipping Width',
    '整机运输长度对标': 'Benchmark Overall Shipping Length',
    '整机运输高度对标': 'Benchmark Overall Shipping Height',
    '操作重量对标': 'Benchmark Operating Weight',
    '最大挖掘高度对标': 'Benchmark Maximum Digging Height',
    '最大卸载高度对标': 'Benchmark Maximum Dump Clearance',
    '最大挖掘深度对标': 'Benchmark Maximum Digging Depth',
    '最大挖掘半径对标': 'Benchmark Maximum Digging Reach',
    '最大地面挖掘半径对标': 'Benchmark Maximum Reach at Ground Level',
    '发动机总功率对标': 'Benchmark Gross Engine Power',
    '发动机净功率对标': 'Benchmark Net Engine Power',
    '系统流量对标': 'Benchmark Main Pump Flow',
    '工作压力对标': 'Benchmark Operating Pressure - Equipment',
    'AUX1流量对标': 'Benchmark Auxiliary Circuit 1 Flow',
    'AUX1压力对标': 'Benchmark Auxiliary Circuit 1 Pressure',
    'AUX2流量对标': 'Benchmark Auxiliary Circuit 2 Flow',
    'AUX2压力对标': 'Benchmark Auxiliary Circuit 2 Pressure',
    '最大牵引力对标': 'Benchmark Maximum Drawbar Pull',
    '爬坡能力对标': 'Benchmark Gradeability',
    '回转速度对标': 'Benchmark Machine Swing Speed',
    '铲斗挖掘力对标': 'Benchmark Bucket Digging Force',
    '斗杆挖掘力对标': 'Benchmark Stick Digging Force',
    '标配斗杆对标': 'Benchmark Standard Stick Length',
    '选配斗杆对标': 'Benchmark Optional Stick Length',
    '远处起吊能力对标': 'Benchmark Lift Capacity at Reach',
    '自动怠速': 'Auto Idle',
    '自动停机': 'Auto Engine Shutdown',
    '经济模式': 'Economy Mode',
    '功率模式': 'Power Mode',
    '一键启动': 'Push-Button Start',
    '冷启动': 'Cold-Start Package',
    '燃油泵': 'Fuel Transfer Pump',
    '风扇反向': 'Reversing Fan',
    '自动润滑': 'Automatic Lubrication',
    'AUX1换向阀': 'Auxiliary Circuit 1 Selector Valve',
    'AUX1管路': 'Auxiliary Circuit 1 Lines',
    'AUX2管路': 'Auxiliary Circuit 2 Lines',
    'AUX3管路': 'Auxiliary Circuit 3 Lines',
    '卸油管路': 'Case-Drain Line',
    '流量保持': 'Continuous-Flow Control',
    '快换管路': 'Quick-Coupler Lines',
    '液压油自动预热': 'Automatic Hydraulic-Oil Warm-Up',
    '液压油采样口': 'Hydraulic-Oil Sampling Port',
    '机油采样口': 'Engine-Oil Sampling Port',
    '动臂斗杆缓冲阀': 'Boom / Stick Cushion Valves',
    '动臂斗杆防爆阀': 'Boom / Stick Hose-Burst Protection Valves',
    '密码启动/防盗': 'PIN Start / Anti-Theft',
    '远程信息处理系统': 'Telematics System',
    '电子围栏': 'Geofencing',
    '电子栅栏': 'Geofencing',
    '报警灯': 'Warning Beacon',
    '行走报警': 'Travel Alarm',
    '带消音': 'with Mute Switch',
    '后视摄像头': 'Rearview Camera',
    '安全摄像头': 'Safety Camera',
    '坡度系统': 'Grade Control System',
    '手机托': 'Phone Holder',
    '无线充电': 'Wireless Charging',
    '蓝牙收音机': 'Bluetooth Radio',
    '触屏显示器': 'Touchscreen Display',
    '驾驶室温控': 'Cab Climate Control',
    '驾驶室冷暖空调': 'Heating and Air-Conditioned Cab',
    '气悬浮座椅': 'Air-Suspension Seat',
    '悬浮座椅': 'Suspension Seat',
    '后视镜加热': 'Heated Mirrors',
    '工作灯延迟关闭': 'Delayed Work-Light Shutdown',
    '推土铲浮动': 'Blade Float',
    '推土铲偏摆': 'Angle Blade',
    '六向推土铲': 'Six-Way Blade',
    '可伸缩底盘': 'Variable-Width Undercarriage',
    '履带橡胶垫': 'Rubber Track Pads',
    '橡胶垫': 'Rubber Track Pads',
    '副配重': 'Counterweight',
    '长斗杆': 'Long Stick',
    '可伸长斗杆': 'Extendable Stick',
    '机械快换': 'Mechanical Quick Coupler',
    '楔式快换': 'Wedge-Type Quick Coupler',
    '液压手腕': 'Hydraulic Tiltrotator',
    '回转助手': 'Swing Assist',
    '起吊助手': 'Lift Assist',
    '铲斗助手': 'Bucket Assist',
    '智能称重': 'Payload Weighing',
    '障碍物检测': 'Object Detection',
    '精准回转': 'Precision Swing',
    '手柄行走': 'Joystick Travel',
    '单脚踏行驶': 'Single-Pedal Travel',
    '自动双速': 'Automatic Two-Speed Travel',
    '蠕行模式': 'Creep Mode',
    '三泵': 'Three-Pump System',
    '全电控': 'Fully Electronic Control',
    '正流量': 'Positive Flow Control',
    '电控正流量': 'Electronic Positive Flow Control',
    '负流量': 'Negative Flow Control',
    '负载敏感': 'Load Sensing',
    '闭式主阀': 'Closed-Center Main Control Valve',
    '闭式': 'Closed Center',
    '卡特': 'Caterpillar',
    '迪尔': 'John Deere',
    '山猫': 'Bobcat',
    '久保田': 'Kubota',
    '沃尔沃': 'Volvo',
    '现代': 'Hyundai',
    '斗山': 'DEVELON',
    '三一': 'SANY',
    '小松': 'Komatsu',
    '神钢': 'Kobelco',
    '洋马': 'Yanmar',
    '驾驶棚': 'Canopy',
    '驾驶室': 'Cab',
    '副配重影响': 'counterweight dependent',
    '包括推土铲': 'including blade',
    '越高越好': 'higher is better',
    '越低越好': 'lower is better',
    '总流量越高越好': 'higher total flow is better',
    '低速档能力': 'low-speed capability',
    '高速档能力': 'high-speed capability',
    '配置项累计贡献最高': 'highest cumulative equipment contribution',
    '配置字段覆盖不足，暂不比较': 'insufficient equipment-field coverage; comparison withheld',
    '暂不进入正式排名': 'excluded from the formal ranking',
    '暂不生成模拟排名': 'simulation ranking not generated',
    '已达到该工况第一名': 'Ranked first for this work condition',
    '排名计算中': 'Calculating rank',
    '模拟状态为标配': 'Simulated as standard equipment',
    '建议纳入标配或选配方案评估': 'Evaluate as standard or optional equipment',
    '并核算客户价值、成本和法规要求': 'and assess customer value, cost, and regulatory requirements',
    '是否转为产品目标需通过工程与试验评审': 'Adoption as a product target requires engineering and validation review',
    '需评估整机布置、结构尺寸和运输合规性': 'Assess machine packaging, structural dimensions, and transport compliance',
    '需评估底盘尺寸、接地比压和整机稳定性': 'Assess undercarriage dimensions, ground pressure, and machine stability',
    '需评估动臂、斗杆、铰点和整机稳定性': 'Assess boom/stick geometry, pin locations, and machine stability',
    '需评估泵阀匹配、压力设定、流量分配和热平衡': 'Assess pump/valve matching, pressure settings, flow allocation, and thermal balance',
    '需评估行走马达、减速机构、系统压力和操控标定': 'Assess travel motors, final drives, system pressure, and control calibration',
    '需评估油缸规格、系统压力和机构传动比': 'Assess cylinder sizing, system pressure, and linkage ratio',
    '需评估结构强度、整机稳定性和载荷表验证': 'Assess structural strength, machine stability, and load-chart validation',
    '需评估上车回转包络、配重和发动机舱布置': 'Assess upperstructure swing envelope, counterweight, and engine-compartment packaging',
    '需评估偏摆机构、油缸行程、管路布置和结构干涉': 'Assess boom-swing linkage, cylinder stroke, hose routing, and structural interference',
    '需评估操作重量、履带接地长度和履带宽度': 'Assess operating weight, track contact length, and track shoe width',
    '需评估结构减重、配重方案和拖车级别': 'Assess structural mass reduction, counterweight strategy, and trailer class',
    '需评估行走驱动、牵引、制动和安全边界': 'Assess travel drive, traction, braking, and safe operating limits',
    '需评估发动机匹配、冷却能力和油耗表现': 'Assess engine matching, cooling capacity, and fuel consumption',
    '需评估动臂斗杆结构、油缸规格和工作范围': 'Assess boom/stick structure, cylinder sizing, and working range',
    '需评估回转液压匹配、减速机构和操控标定': 'Assess swing-hydraulic matching, swing drive, and control calibration',
    '可拆卸配重 kg': 'Removable Counterweight kg',
    '可拆卸': 'Removable',
    '当前': 'Current',
    '参考': 'Reference',
    '差': 'gap',
    '高于参考值': 'above the reference by',
    '低于参考值': 'below the reference by',
    '该指标越低越有利': 'lower values are preferable for this metric',
    '对标参考': 'benchmark reference',
    '竞品参考': 'competitor reference',
    '贡献': 'Contribution',
    '排名': 'Rank',
    '覆盖率': 'Coverage',
    '缺失': 'Missing',
    '无': 'None',
    '是': 'Yes',
    '否': 'No'
  };

  const termEntries = [
    ...Object.entries(exactTranslations),
    ...Object.entries(technicalTerms)
  ].filter(([source]) => source.length >= 2).sort((a, b) => b[0].length - a[0].length);

  const sentenceRules = [
    [/^XCMG\s+(.+?)\s+(\d+(?:-\d+)?)\s*吨级(短尾)?挖掘机竞品对标看板$/, (model, range, shortTail) => `XCMG ${model} ${range} t${shortTail ? ' Short-Tail' : ''} Excavator Competitive Benchmark Dashboard`],
    [/^(\d+(?:-\d+)?)\s*吨级(短尾)?挖掘机对标$/, (range, shortTail) => `${range} t${shortTail ? ' Short-Tail' : ''} Excavator Benchmark`],
    [/^工况表现：(.+?)\s+([\d.]+)\s*分；XCMG\s+([\d.]+)\s*分，第\s*([\d-]+)，距领先产品\s*([\d.]+)\s*分。$/, (leader, leaderScore, xcmgScore, rank, gap) => `Work-condition performance: ${translateCore(leader)} ${leaderScore} pts; XCMG ${xcmgScore} pts, ranked No. ${rank}, ${gap} pts behind the leader.`],
    [/^主要差距项：(.+?)。$/, (items) => `Primary gap items: ${translateCore(items)}.`],
    [/^配置项累计贡献：(.+)$/, (detail) => `Cumulative equipment contribution: ${translateCore(detail)}`],
    [/^XCMG 有效字段覆盖率为 ([\d.]+%)，(?:暂)?不进入正式排名；当前资料中领先产品为 (.+?)，已知差距项为 (.+?)。$/, (coverage, leader, items) => `XCMG valid-field coverage is ${coverage}, below the formal ranking threshold. The current documented leader is ${translateCore(leader)}; known gap items: ${translateCore(items)}.`],
    [/^硬参数未显示明显短板，当前差距主要来自配置完整度或数据缺失。$/, () => 'No clear specification disadvantage is documented; the current gap is driven primarily by equipment completeness or missing data.'],
    [/^XCMG 有效字段覆盖率为 ([\d.]+%)，低于正式排名门槛，暂不生成模拟排名。请先补齐该工况缺失参数或配置，再开展提升方案评估。$/, (coverage) => `XCMG valid-field coverage is ${coverage}, below the formal ranking threshold, so no simulated rank is generated. Complete the missing specification or equipment fields before evaluating an improvement package.`],
    [/^(.+?)关键项及权重$/, (condition) => `${translateCore(condition)} — Key Items and Weights`],
    [/^典型工况\s*(\d+)$/, (number) => `Representative Work Condition ${number}`],
    [/^关键项：(.+)$/, (items) => `Key inputs: ${translateCore(items)}`],
    [/^与 (.+?) 的具体差距$/, (product) => `Specific Gaps vs ${translateCore(product)}`],
    [/^当前可核验差距集中在 (.+?)。以下均为原始参数或标选配状态，不用综合分替代实际差异。$/, (items) => `Documented gaps are concentrated in ${translateCore(items)}. Each point below is tied to a source specification or equipment status rather than being represented only by a composite score.`],
    [/^(.+?)全部指标与配置贡献明细$/, (condition) => `${translateCore(condition)} — Complete Specification and Equipment Contribution Detail`],
    [/^进入\s*(.+?)看板$/, (label) => `Open ${translateCore(label)} dashboard`],
    [/^(.+?)关键参数与配置雷达图$/, (condition) => `${translateCore(condition)} Key Specification and Equipment Radar Chart`],
    [/^显示 (\d+) 个吨级项目$/, (count) => `Showing ${count} tonnage assets`],
    [/^显示 (\d+) 个数据集$/, (count) => `Showing ${count} datasets`],
    [/^第\s*([\d-]+)$/, (rank) => `No. ${rank}`],
    [/^模拟第([\d-]+)$/, (rank) => `Simulated Rank ${rank}`],
    [/^距前一名 (.+?) 还差 ([\d.]+) 分$/, (product, gap) => `${translateCore(gapProduct(product))} is ${gap} pts ahead`],
    [/^当前：(.+?)$/, (value) => `Current: ${translateCore(value)}`],
    [/^(\d+) 个品牌对比$/, (count) => `${count} Brands Selected`],
    [/^权重\s*([\d.]+)%$/, (value) => `Weight ${value}%`],
    [/^覆盖\s*([\d.]+)%$/, (value) => `Coverage ${value}%`],
    [/^([+-]?[\d.]+)\s*工况分$/, (value) => `${value} work-condition pts`],
    [/^([+-]?[\d.]+)分$/, (value) => `${value} pts`],
    [/^贡献\s*([\d.-]+)\s*·\s*(.+)$/, (value, status) => `Contribution ${value} · ${translateCore(status)}`],
    [/^XCMG\s+([\d.-]+)\s*分，排名第\s*([\d-]+)。$/, (score, rank) => `XCMG ${score} pts, ranked No. ${rank}.`],
    [/^XCMG\s+([\d.-]+)\s*分，第\s*([\d-]+)，距领先产品\s*([\d.-]+)\s*分。$/, (score, rank, gap) => `XCMG ${score} pts, ranked No. ${rank}, ${gap} pts behind the leader.`],
    [/^(.+?)\s+([\d.-]+)\s*分；XCMG\s+([\d.-]+)\s*分，差\s*([\d.-]+)\s*分。$/, (leader, leaderScore, xScore, gap) => `${translateCore(leader)} ${leaderScore} pts; XCMG ${xScore} pts, a ${gap}-pt gap.`],
    [/^XCMG\s+([\d.-]+)\s*分，配置项累计贡献最高。$/, (score) => `XCMG ${score} pts, the highest cumulative equipment contribution.`],
    [/^(.+?)：当前 (.+?)，对标参考 (.+?) (.+?)。需评估(.+?)；是否转为产品目标需通过工程与试验评审。$/, (item, current, product, reference, guidance) => `${translateCore(item)}: XCMG ${translateCore(current)}; benchmark ${translateCore(product)} ${translateCore(reference)}. ${translateCore(`需评估${guidance}`)}. Adoption as a product target requires engineering and validation review.`],
    [/^(.+?)：XCMG (.+?)，(.+?) (.+?)；XCMG (高于|低于)参考值 (.+?)(，该指标越低越有利)?。$/, (item, current, product, reference, direction, gap, lower) => `${translateCore(item)}: XCMG ${translateCore(current)}; ${translateCore(product)} ${translateCore(reference)}. XCMG is ${direction === '高于' ? 'above' : 'below'} the reference by ${translateCore(gap)}${lower ? '; lower values are preferable for this metric' : ''}.`],
    [/^(.+?)：XCMG 当前为(.+?)，(.+?) 为(.+?)。建议纳入标配或选配方案评估，并核算客户价值、成本和法规要求。$/, (item, current, product, reference) => `${translateCore(item)}: XCMG is ${translateCore(current)}; ${translateCore(product)} is ${translateCore(reference)}. Evaluate standard/optional availability, customer value, cost, and regulatory requirements.`],
    [/^模拟状态为标配；当前为(.+?)，参考 (.+?) 为(.+?)。$/, (current, product, reference) => `Simulated as standard equipment; current status is ${translateCore(current)}, while ${translateCore(product)} is ${translateCore(reference)}.`],
    [/^同工况排名第一的参考产品为 (.+?)；XCMG 的主要差距项为 (.+?)。$/, (product, items) => `The work-condition leader is ${translateCore(product)}. XCMG's primary gap items are ${translateCore(items)}.`],
    [/^总体排名第一的参考产品为 (.+?)；单项差距主要集中在 (.+?) 等具体指标。$/, (product, items) => `The overall benchmark leader is ${translateCore(product)}. Item-level gaps are concentrated in ${translateCore(items)}.`],
    [/^XCMG 有效字段覆盖率(?:为)? ([\d.]+%)，暂不进入正式排名；当前资料领先产品为 (.+?) ([\d.-]+) 分。$/, (coverage, product, score) => `XCMG valid-field coverage is ${coverage}, below the formal ranking threshold. The current data leader is ${translateCore(product)} at ${score} pts.`],
    [/^XCMG 配置字段覆盖不足，暂不比较；当前资料最高为 (.+?) ([\d.-]+) 分。$/, (product, score) => `XCMG equipment-field coverage is insufficient for comparison. The highest documented result is ${translateCore(product)} at ${score} pts.`],
    [/^(.+?)：XCMG (.+?)，(.+?) (.+?)，已接近对标参考。$/, (item, current, product, reference) => `${translateCore(item)}: XCMG ${translateCore(current)}; ${translateCore(product)} ${translateCore(reference)}. XCMG is close to the benchmark reference.`],
    [/^(\d+(?:-\d+)?) 吨级短尾$/, (range) => `${range} t Short-Tail Class`],
    [/^(\d+(?:-\d+)?) 吨级$/, (range) => `${range} t Class`]
  ];

  function gapProduct(value) {
    return String(value || '').trim();
  }

  function translateCore(value) {
    const original = String(value || '').trim().replace(/\s+/g, ' ');
    let text = original;
    if (!HAN.test(text)) return text;
    if (Object.prototype.hasOwnProperty.call(exactTranslations, text)) {
      return exactTranslations[text];
    }
    for (const [pattern, handler] of sentenceRules) {
      const match = text.match(pattern);
      if (match) {
        const translated = handler(...match.slice(1));
        return HAN.test(translated) ? original : translated;
      }
    }
    text = text
      .replace(/^无(?=[、，,])/, 'None')
      .replace(/第\s*([\d-]+)/g, 'No. $1')
      .replace(/([+-]?[\d.]+)\s*工况分/g, '$1 work-condition pts')
      .replace(/([+-]?[\d.]+)\s*分/g, '$1 pts')
      .replace(/覆盖\s*([\d.]+)%/g, 'Coverage $1%')
      .replace(/权重\s*([\d.]+)%/g, 'Weight $1%')
      .replace(/(\d+(?:-\d+)?)\s*吨级短尾/g, '$1 t short-tail class')
      .replace(/(\d+(?:-\d+)?)\s*吨级/g, '$1 t class')
      .replace(/(\d+(?:-\d+)?)\s*吨/g, '$1 t');
    for (const [source, target] of termEntries) {
      text = text.split(source).join(target);
    }
    const translated = text
      .replace(/，/g, ', ')
      .replace(/；/g, '; ')
      .replace(/：/g, ': ')
      .replace(/。/g, '.')
      .replace(/、/g, ', ')
      .replace(/（/g, ' (')
      .replace(/）/g, ')')
      .replace(/｜/g, ' | ')
      .replace(/(class|Class)(Excavator)/g, '$1 $2')
      .replace(/ExcavatorCompetitive/g, 'Excavator Competitive')
      .replace(/\s+,/g, ',')
      .replace(/\s+\./g, '.')
      .replace(/\s{2,}/g, ' ')
      .trim();
    return HAN.test(translated) ? original : translated;
  }

  function translateValue(value) {
    const text = String(value || '');
    if (!HAN.test(text)) return text;
    const leading = text.match(/^\s*/)[0];
    const trailing = text.match(/\s*$/)[0];
    return leading + translateCore(text.trim()) + trailing;
  }

  function translateFully(value) {
    let current = String(value || '');
    for (let pass = 0; pass < 4 && HAN.test(current); pass += 1) {
      const next = translateValue(current);
      if (next === current) break;
      current = next;
    }
    return current;
  }

  function shouldSkip(node) {
    const parent = node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement;
    return !parent || Boolean(parent.closest('script, style, noscript, textarea, .languageToggle'));
  }

  function translateElement(root) {
    if (language !== 'en' || !root || shouldSkip(root)) return;
    const elements = root.nodeType === Node.ELEMENT_NODE ? [root, ...root.querySelectorAll('*')] : [];
    for (const element of elements) {
      if (shouldSkip(element)) continue;
      const explicitEnglish = element.getAttribute('data-en');
      if (explicitEnglish !== null && !HAN.test(explicitEnglish)) {
        if (element.textContent !== explicitEnglish) element.textContent = explicitEnglish;
        continue;
      }
      for (const attribute of ['aria-label', 'placeholder', 'title', 'alt']) {
        const value = element.getAttribute(attribute);
        if (value && HAN.test(value)) {
          element.setAttribute(attribute, translateFully(value));
        }
      }
    }
    const nodes = [];
    const collectTextNodes = (parent) => {
      parent.childNodes.forEach((child) => {
        if (child.nodeType === 3) nodes.push(child);
        else if (child.nodeType === 1 && !shouldSkip(child)) collectTextNodes(child);
      });
    };
    collectTextNodes(root);
    for (const node of nodes) {
      if (!shouldSkip(node) && HAN.test(node.nodeValue || '')) {
        const translated = translateFully(node.nodeValue);
        if (translated !== node.nodeValue) node.nodeValue = translated;
      }
    }
  }

  function decorateInternalLinks() {
    if (language !== 'en') return;
    document.querySelectorAll('a[href]').forEach((link) => {
      if (link.hasAttribute('download')) return;
      const href = link.getAttribute('href');
      if (!href || href.startsWith('#') || /^(mailto:|tel:|javascript:)/i.test(href)) return;
      const url = new URL(href, window.location.href);
      if (url.origin !== window.location.origin || !/\.html$|\/$/.test(url.pathname)) return;
      url.searchParams.set('lang', 'en');
      link.setAttribute('href', url.pathname.split('/').pop() + url.search + url.hash);
    });
  }

  function updateToggle() {
    document.querySelectorAll('.languageToggle').forEach((button) => {
      button.textContent = language === 'en' ? '中文' : 'EN';
      button.setAttribute('aria-label', language === 'en' ? 'Switch to Chinese' : 'Switch to English');
      button.addEventListener('click', () => {
        const nextLanguage = language === 'en' ? 'zh' : 'en';
        try {
          window.localStorage.setItem(STORAGE_KEY, nextLanguage);
        } catch (_) {
          // The URL parameter remains the fallback when storage is unavailable.
        }
        const url = new URL(window.location.href);
        if (nextLanguage === 'zh') url.searchParams.delete('lang');
        else url.searchParams.set('lang', 'en');
        window.location.href = url.toString();
      });
    });
  }

  function installEnglishDisclosureLabels() {
    if (language !== 'en') return;
    const style = document.createElement('style');
    style.textContent = `
      html[lang^="en"] .mobileDisclosure>summary:after,
      html[lang^="en"] .radarPicker>summary:after{content:"Expand"}
      html[lang^="en"] .mobileDisclosure[open]>summary:after,
      html[lang^="en"] .radarPicker[open]>summary:after{content:"Collapse"}`;
    document.head.appendChild(style);
  }

  function normalizeEnglishRadarLabels(root = document) {
    if (language !== 'en') return;
    const shortLabels = new Map([
      ['Boom Swing (Left / Right)', 'Boom Swing L/R'],
      ['Front Lift Capacity at 3 m, Ground Level (Blade Down)', 'Front Lift 3 m, Blade Down'],
      ['Front Lift Capacity at 3 m, Ground Level (Blade Up)', 'Front Lift 3 m, Blade Up'],
      ['Side Lift Capacity at 3 m, Ground Level', 'Side Lift 3 m']
    ]);
    root.querySelectorAll?.('.radar-label').forEach((label) => {
      const fullLabel = label.querySelector('title')?.textContent.trim();
      const shortLabel = shortLabels.get(fullLabel);
      if (!shortLabel) return;
      const visibleLabel = [...label.childNodes]
        .filter((node) => node.nodeType === Node.TEXT_NODE)
        .map((node) => node.nodeValue)
        .join('')
        .trim();
      if (visibleLabel === shortLabel) return;
      [...label.childNodes].forEach((node) => {
        if (node.nodeType === Node.TEXT_NODE) node.remove();
      });
      label.appendChild(document.createTextNode(shortLabel));
    });
  }

  function finalizeEnglishRendering() {
    if (language !== 'en') return;
    translateElement(document.body);
    normalizeEnglishRadarLabels(document);
    decorateInternalLinks();
    scheduleRenderingSettled();
  }

  let renderingSettledTimer = 0;
  function scheduleRenderingSettled() {
    window.clearTimeout(renderingSettledTimer);
    renderingSettledTimer = window.setTimeout(() => {
      document.dispatchEvent(new CustomEvent('xcmg:i18n-rendered', {
        detail: {language}
      }));
    }, 60);
  }

  document.documentElement.lang = language === 'en' ? 'en-US' : 'zh-CN';
  document.documentElement.dataset.language = language;
  updateToggle();
  if (language === 'en') {
    document.title = translateFully(document.title);
    translateElement(document.body);
    normalizeEnglishRadarLabels(document);
    decorateInternalLinks();
    installEnglishDisclosureLabels();
    scheduleRenderingSettled();
    window.addEventListener('load', finalizeEnglishRendering, {once: true});
    requestAnimationFrame(() => requestAnimationFrame(finalizeEnglishRendering));
    if (typeof MutationObserver === 'function') {
      let translating = false;
      const observer = new MutationObserver((mutations) => {
        if (translating) return;
        translating = true;
        for (const mutation of mutations) {
          if (mutation.type === 'characterData' && HAN.test(mutation.target.nodeValue || '')) {
            const translated = translateFully(mutation.target.nodeValue);
            if (translated !== mutation.target.nodeValue) mutation.target.nodeValue = translated;
          }
          mutation.addedNodes.forEach((node) => {
            if (node.nodeType === 1) {
              translateElement(node);
              normalizeEnglishRadarLabels(node);
            }
            else if (node.nodeType === 3 && HAN.test(node.nodeValue || '')) {
              const translated = translateFully(node.nodeValue);
              if (translated !== node.nodeValue) node.nodeValue = translated;
            }
          });
        }
        decorateInternalLinks();
        scheduleRenderingSettled();
        translating = false;
      });
      observer.observe(document.body, {childList: true, characterData: true, subtree: true});
    }
  }

  window.XCMGI18n = {language, translateText: translateCore};
})();
