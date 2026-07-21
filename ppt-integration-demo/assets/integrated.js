(function () {
  'use strict';

  const STORAGE_KEY = 'xcmg-benchmark-language';
  const params = new URLSearchParams(window.location.search);
  let storedLanguage = '';
  try { storedLanguage = window.localStorage.getItem(STORAGE_KEY) || ''; } catch (_) { storedLanguage = ''; }
  const language = params.get('lang') === 'en' || (params.get('lang') !== 'zh' && storedLanguage === 'en') ? 'en' : 'zh';
  const expanded = window.XCMGExpandedContent || {
    marketPortfolio: [], transportRules: [], scenarioAssessments: {}, paperGroups: [], fieldGroups: [],
    competitionDimensions: [], positioning: [], translations: {}
  };

  const copy = {
    zh: {
      internal: 'XCMG ARC内部分析',
      marketTitle: '市场、客户与运输适配',
      marketSubtitle: '先看该吨级为什么被购买，再判断产品参数和配置是否覆盖真实使用边界。',
      scoringBoundary: '本节解释市场适配背景，不改变现有参数分、配置分、总体分和工况分。',
      volumeTitle: '3-4吨市场规模变化', historical: '历史实绩', estimate: '源文件滚动估计', forecast: '源文件预测', units: '台', basePeriod: '基期', yearOverYear: '同比',
      shareTitle: '四个领先品牌合计份额', shareNote: '久保田、约翰迪尔、山猫、卡特',
      customerTitle: '主要客户结构', purchaseLogic: '购买判断重点', transportTitle: '典型运输组合重量',
      portfolioTitle: '同吨级产品型谱覆盖', portfolioBrand: '品牌', portfolioCount: '主力机型数', portfolioArchitecture: '型谱结构', portfolioImplication: '竞争含义',
      transportRuleTitle: '运输与驾照边界', licenceClass: '许可类型', generalThreshold: '通用门槛', applicationImpact: '对3-4吨产品的影响', transportRuleCaveat: '以下为历史材料中的通用判断。州法规、商业用途、车辆额定值及组合总质量必须按实际运输方案复核。',
      baseMass: '基础机', equippedMass: '典型配置后', marketRead: '市场判断',
      marketRole: '吨级角色', marketRoleText: '3-4吨是微小挖销量核心，也是租赁市场的高频规格。成熟品牌通常用短尾、常规尾和不同配置层级覆盖运输、狭窄施工与重载稳定需求。',
      competition: '竞争结构', competitionText: '历史样本中，久保田、约翰迪尔、山猫和卡特合计约占74%。竞争优势来自产品型谱、附件体系、渠道服务和残值，而不只是单项参数。',
      xcmgEntry: 'XCMG切入点', xcmgEntryText: 'XE35U需要优先处理整备后运输重量、行走速度、AUX流量、回填配置和驾驶舒适性，同时保留AUX2、斗杆力和起吊能力等可验证优势。',
      transportStoryTitle: '运输边界直接影响成交和跨工地周转',
      transportStoryText: '现款基础机记录重量为4,200 kg；加副配重、快换、拇指钳和标准斗后约4,579 kg。该组合会明显压缩皮卡与14K拖车的有效载荷余量，选车、拖车额定值、组合总质量和驾驶许可必须按具体方案核验。',
      transportPayloadWindow: '14K拖车常见有效载荷', transportCurrentPackage: 'XE35U常用配置后', transportHistoricalPackage: 'XE35U PRO历史方案', transportMargin: '相对载荷下限余量',
      transportMarginNote: '负值表示设备组合已超过源文件所述常见有效载荷区间下限。', transportDecisionTitle: '运输判断', transportDecisionText: '现款常用组合已越过常见载荷区间下限，历史PRO方案能够恢复一定余量。实际运输仍须复核拖车铭牌、牵引车额定值、组合总质量和驾驶许可。',
      transportCaptionA: '轻型皮卡与14K拖车是该吨级常见转运组合', transportCaptionB: '竞品35G装车状态：整机与附件共同占用有效载荷',
      scenarioTitle: '真实作业场景', scenarioSubtitle: '把现场任务、客户要求和产品差距直接连接到现有量化工况。',
      customer: '主要客户', needs: '作业要求', steps: '任务链', finding: '当前判断', scenarioIndex: '八类场景快速对照',
      workCondition: '作业场景', keyFinding: '关键差距', status: '判断', parameterImpact: '关键参数差距', configurationImpact: '关键配置作用', engineeringAction: '产品动作',
      scenarioRequirement: '客户任务', currentFit: '当前产品适配', productAction: '产品动作', covered: '已覆盖', mixed: '部分覆盖', linkedConditions: '关联量化工况',
      paperTitle: '纸面竞争力复核', paperSubtitle: '把尺寸、作业能力、液压和属具配置放回具体应用中解释。',
      paperBoundary: '该矩阵补充现有Excel评分，不重复计分；不同版本数据冲突时，以当前机型实测和最新配置清单为准。',
      fullPaper: '关键参数对比矩阵', metric: '指标', findingColumn: '对工况的影响', configurationTitle: '关键配置差异',
      paperRead: '参数与配置结论', xcmgState: 'XCMG状态', comparison: '竞品差异与工况影响',
      dataConflictTitle: '当前数据与历史口径差异', currentDataset: '当前 Excel', historicalReference: '历史研究口径', handlingRule: '处理方式', conflictRule: '评分继续使用当前 Excel；历史值仅用于追溯，完成版本和测试条件核验后再统一。',
      completePaperData: '完整参数与配置明细', sourceCategory: '类别', sourceSystem: '系统', sourcePriority: '关注度', sourceUnit: '单位',
      fieldTitle: '实机评价', fieldSubtitle: '将操控、舒适性、可靠性和维修性与纸面参数分开呈现。',
      fieldBoundary: '没有统一工况下的当前量化试验时，只标记优势、差距或待验证，不生成新分数。',
      fullField: '实机评价矩阵', dimension: '维度', conclusion: '工程判断', validation: '验证要求',
      advantage: '优势', gap: '差距', pending: '待验证', missing: '未覆盖', fieldRead: '实机评价重点',
      completeFieldData: '历史实机评价明细', historicalRatingNote: '表内1-5级为历史样机评价，仅用于定位差异，不并入现有评分；当前量产机状态仍需按统一工况复测。',
      actionTitle: 'XCMG产品改进路径', actionSubtitle: '把市场、参数和实机差距转化为系统级工程任务。',
      actionBoundary: '以下为建议动作和验证任务，不代表已经立项、完成或承诺时间。',
      priority: '优先级', topic: '改进主题', action: '工程动作', validationState: '验证状态',
      verifyRequired: '需工程、试验与市场共同验证', portfolio: '型谱差距', historicalPositioning: '市场定位复核',
      competitionDetail: '九个维度的具体差距与动作', strengthColumn: '已有基础', gapColumn: '具体差距', actionColumn: '弥补动作',
      positioningTitle: '历史价格与市场份额定位', positioningBrand: '品牌', positioningModels: '代表机型', positioningPrice: '历史参考价', positioningShare: '历史份额', positioningCaveat: '价格、份额和产品状态均为历史快照，只用于理解当时定位；对外使用前必须更新当前市场数据。',
      navMarket: '市场与客户', navScenarios: '真实作业场景', navPaper: '参数与配置', navField: '实机评价', navActions: '改进路线',
      phaseNow: '优先验证', phaseNext: '系统改进', phasePlatform: '平台规划', validationOutput: '应形成的验证输出',
      sourcePpt: '研究资料', historicalBasis: '历史口径', currentUnverified: '当前状态待核验',
      year: '年份', total: '合计', dataStatus: '数据属性', sourceEstimate: '源文件滚动估计', sourceForecast: '源文件预测',
      brandSalesTable: '品牌销量明细', modelDemandTitle: '主销机型排名', priceShareTitle: '价格与份额分布',
      priceAxis: '历史单价（万美元）', shareAxis: '历史份额（%）', sourceVolume: '源文件销量口径',
      transportBreakdownTitle: '整机与附件重量构成', packageName: '运输组合', component: '构成项', weight: '重量', packageTotal: '组合总重', optionalAttachments: '可追加属具',
      performanceVisualTitle: '关键性能分项对比', performanceScaleNote: '每个指标按本组最大值显示条长，右侧保留原始单位。', noSourceValue: '源页未给值',
      fieldHeatmapTitle: '历史实机评价热力矩阵', ratingLegend: '1级较弱，5级较强；颜色只表达源文件历史等级。',
      profileTitle: '历史竞争力维度画像', profileKey: '维度索引',
      ledgerTitle: 'XE35U历史问题与升级台账', ledgerCaveat: '这是源文件记录的历史计划，不表示已批准、已完成或已量产；当前状态必须逐项复核。',
      itemNo: '序号', system: '系统', problem: '源文件问题', sourceAction: '源文件升级方案', historicalUpgradeDate: '历史升级日期', historicalProductionDate: '历史量产日期',
      loadError: '扩展分析数据未能载入，请通过本地预览地址打开。'
    },
    en: {
      internal: 'XCMG ARC INTERNAL ANALYSIS',
      marketTitle: 'Market, Customer and Transport Fit',
      marketSubtitle: 'Start with why the class is purchased, then test whether the product covers real operating constraints.',
      scoringBoundary: 'This section explains market fit and does not change the existing specification, equipment, overall or application scores.',
      volumeTitle: '3-4 t market volume trend', historical: 'Historical actual', estimate: 'Source rolling estimate', forecast: 'Source forecast', units: 'units', basePeriod: 'Base period', yearOverYear: 'YoY',
      shareTitle: 'Combined share of four leading brands', shareNote: 'Kubota, John Deere, Bobcat and Caterpillar',
      customerTitle: 'Primary customer mix', purchaseLogic: 'Purchase priorities', transportTitle: 'Representative transport mass',
      portfolioTitle: 'Portfolio coverage within the class', portfolioBrand: 'Brand', portfolioCount: 'Core models', portfolioArchitecture: 'Portfolio structure', portfolioImplication: 'Competitive implication',
      transportRuleTitle: 'Transport and licence boundaries', licenceClass: 'Licence class', generalThreshold: 'General threshold', applicationImpact: 'Impact on the 3-4 t product', transportRuleCaveat: 'These are general boundaries from the historical material. State law, commercial use, vehicle ratings and gross combination mass must be checked for the actual transport setup.',
      baseMass: 'Base machine', equippedMass: 'Representative equipped mass', marketRead: 'Market interpretation',
      marketRole: 'Role of the class', marketRoleText: 'The 3-4 t class is a compact-excavator volume center and a high-frequency rental size. Established brands use short-tail, conventional-tail and multiple trim levels to span transport, confined work and stability needs.',
      competition: 'Competitive structure', competitionText: 'In the historical sample, Kubota, John Deere, Bobcat and Caterpillar account for about 74% combined. Advantage comes from portfolio breadth, attachments, channel support and residual value, not one specification.',
      xcmgEntry: 'XCMG opportunity', xcmgEntryText: 'XE35U priorities are equipped transport mass, travel speed, auxiliary flow, backfill equipment and cab comfort, while retaining validated strengths in AUX2 provision, arm force and lifting capability.',
      transportStoryTitle: 'Transport limits directly affect purchase and jobsite mobility',
      transportStoryText: 'Recorded base-machine mass is 4,200 kg; counterweight, coupler, thumb and standard bucket bring a representative combination to about 4,579 kg. This compresses useful payload margin on a pickup and 14K trailer, so tow rating, trailer rating, gross combination mass and licence requirements must be checked for each setup.',
      transportPayloadWindow: 'Typical effective payload of a 14K trailer', transportCurrentPackage: 'XE35U with common equipment', transportHistoricalPackage: 'Historical XE35U PRO proposal', transportMargin: 'Margin to lower payload bound',
      transportMarginNote: 'A negative value means the machine package exceeds the lower end of the common effective-payload range stated in the source.', transportDecisionTitle: 'Transport assessment', transportDecisionText: 'The current common package exceeds the lower end of the typical payload window, while the historical PRO proposal restores some margin. Verify the trailer data plate, tow-vehicle ratings, gross combination mass and licence requirement for the actual setup.',
      transportCaptionA: 'A light-duty pickup and 14K trailer are a common transport combination in this class', transportCaptionB: 'Competitor 35G loaded for transport: machine and equipment consume the same payload allowance',
      scenarioTitle: 'Real Job Applications', scenarioSubtitle: 'Connect field tasks and customer requirements directly to the existing quantified applications.',
      customer: 'Primary users', needs: 'Operating requirements', steps: 'Task sequence', finding: 'Current assessment', scenarioIndex: 'Eight-application comparison',
      workCondition: 'Application', keyFinding: 'Principal gap', status: 'Assessment', parameterImpact: 'Relevant specification gap', configurationImpact: 'Equipment effect', engineeringAction: 'Product action',
      scenarioRequirement: 'Customer task', currentFit: 'Current product fit', productAction: 'Product action', covered: 'Covered', mixed: 'Partly covered', linkedConditions: 'Linked quantified applications',
      paperTitle: 'Paper Competitiveness Review', paperSubtitle: 'Interpret dimensions, working capability, hydraulics and equipment in the applications they affect.',
      paperBoundary: 'This matrix supplements the existing Excel score and is not scored again. Where versions conflict, use current-machine testing and the latest equipment list.',
      fullPaper: 'Key specification comparison', metric: 'Metric', findingColumn: 'Application effect', configurationTitle: 'Key equipment differences',
      paperRead: 'Specification and equipment conclusions', xcmgState: 'XCMG status', comparison: 'Competitive difference and application effect',
      dataConflictTitle: 'Current data versus historical basis', currentDataset: 'Current Excel', historicalReference: 'Historical research basis', handlingRule: 'Treatment', conflictRule: 'Scores continue to use the current Excel. Historical values remain traceable until version and test-condition checks are complete.',
      completePaperData: 'Complete specification and equipment detail', sourceCategory: 'Category', sourceSystem: 'System', sourcePriority: 'Priority', sourceUnit: 'Unit',
      fieldTitle: 'Field Evaluation', fieldSubtitle: 'Keep control, comfort, reliability and serviceability separate from paper specifications.',
      fieldBoundary: 'Where no current quantified common-condition test exists, use Advantage, Gap or Pending Validation rather than creating a score.',
      fullField: 'Field-evaluation matrix', dimension: 'Dimension', conclusion: 'Engineering assessment', validation: 'Validation requirement',
      advantage: 'Advantage', gap: 'Gap', pending: 'Pending validation', missing: 'Not covered', fieldRead: 'Field-evaluation priorities',
      completeFieldData: 'Historical field-evaluation detail', historicalRatingNote: 'The 1-5 ratings below are historical prototype evaluations used only to locate differences. They do not enter the existing score and require common-condition retesting on the current production machine.',
      actionTitle: 'XCMG Product Improvement Path', actionSubtitle: 'Translate market, specification and field gaps into system-level engineering work.',
      actionBoundary: 'The items below are recommendations and validation tasks, not evidence of approval, completion or committed timing.',
      priority: 'Priority', topic: 'Improvement topic', action: 'Engineering action', validationState: 'Validation status',
      verifyRequired: 'Joint engineering, test and market validation required', portfolio: 'Portfolio gap', historicalPositioning: 'Market-position review',
      competitionDetail: 'Concrete gaps and actions across nine dimensions', strengthColumn: 'Existing foundation', gapColumn: 'Specific gap', actionColumn: 'Closing action',
      positioningTitle: 'Historical price and market-share position', positioningBrand: 'Brand', positioningModels: 'Representative models', positioningPrice: 'Historical reference price', positioningShare: 'Historical share', positioningCaveat: 'Prices, shares and product status are a historical snapshot used only to explain the position at that time. Refresh current market data before external use.',
      navMarket: 'Market and customers', navScenarios: 'Real job applications', navPaper: 'Specifications and equipment', navField: 'Field evaluation', navActions: 'Improvement path',
      phaseNow: 'Validate first', phaseNext: 'System improvements', phasePlatform: 'Platform planning', validationOutput: 'Required validation output',
      sourcePpt: 'Source file', historicalBasis: 'Historical basis', currentUnverified: 'Current status unverified',
      year: 'Year', total: 'Total', dataStatus: 'Data status', sourceEstimate: 'Source rolling estimate', sourceForecast: 'Source forecast',
      brandSalesTable: 'Brand-volume detail', modelDemandTitle: 'Leading-model ranking', priceShareTitle: 'Price and share distribution',
      priceAxis: 'Historical price (USD 10k)', shareAxis: 'Historical share (%)', sourceVolume: 'Source volume basis',
      transportBreakdownTitle: 'Machine and attachment mass build-up', packageName: 'Transport package', component: 'Component', weight: 'Mass', packageTotal: 'Package total', optionalAttachments: 'Additional attachments',
      performanceVisualTitle: 'Key performance comparisons', performanceScaleNote: 'Bar length is normalized to the maximum within each metric; original units remain at right.', noSourceValue: 'No source value',
      fieldHeatmapTitle: 'Historical field-evaluation heatmap', ratingLegend: '1 is weaker and 5 is stronger; color represents source historical ratings only.',
      profileTitle: 'Historical competitiveness profile', profileKey: 'Dimension key',
      ledgerTitle: 'Historical XE35U issue and upgrade ledger', ledgerCaveat: 'This is a historical source-file plan and does not prove approval, completion or production release. Verify every current status.',
      itemNo: 'No.', system: 'System', problem: 'Source issue', sourceAction: 'Source upgrade action', historicalUpgradeDate: 'Historical upgrade date', historicalProductionDate: 'Historical production date',
      loadError: 'The extended analysis could not be loaded. Open this page through the local preview address.'
    }
  }[language];

  const fieldMetricNames = {
    safety_systems: {zh: '安全系统', en: 'Safety systems'},
    corrosion_coating_rubber_durability: {zh: '防锈、涂层与橡胶耐久', en: 'Corrosion, coating and rubber durability'},
    temperature_humidity_altitude: {zh: '温湿度与海拔适应性', en: 'Temperature, humidity and altitude capability'},
    travel_control: {zh: '行走启停与转向', en: 'Travel start/stop and steering'},
    inching_precision_smoothness: {zh: '微动、精度与平顺性', en: 'Inching, precision and smoothness'},
    grading_coordination: {zh: '平地复合动作协调性', en: 'Grading coordination'},
    seat_hvac_space_hmi: {zh: '座椅、空调、空间与HMI', en: 'Seat, HVAC, space and HMI'},
    service_access_and_fluid_fill: {zh: '维修可达性与液压油加注', en: 'Service access and hydraulic-oil filling'},
    fuel_economy: {zh: '燃油经济性', en: 'Fuel economy'},
    coating_and_line_identification: {zh: '涂装与管线识别', en: 'Coating and line identification'},
    sales_service_documentation: {zh: '销售与售后资料', en: 'Sales and service documentation'}
  };

  const roadmapTopics = {
    'roadmap-transport-mass': {zh: '运输重量与拖车余量', en: 'Transport mass and trailer margin'},
    'roadmap-travel-speed': {zh: '行走速度系统匹配', en: 'Travel-speed system matching'},
    'roadmap-aux-flow': {zh: '高流量属具系统', en: 'High-flow attachment system'},
    'roadmap-backfill-package': {zh: '回填效率配置包', en: 'Backfill-productivity package'},
    'roadmap-control-tuning': {zh: '液压与操控标定', en: 'Hydraulic and control calibration'},
    'roadmap-cab-hmi': {zh: '驾驶室与人机工程', en: 'Cab and ergonomics'},
    'roadmap-service-quality': {zh: '维修与细节质量', en: 'Serviceability and detail quality'},
    'roadmap-portfolio': {zh: '短尾 / 常规尾型谱', en: 'Short-tail / conventional-tail portfolio'}
  };

  const validationLabels = {
    requires_current_machine_configuration_audit: {zh: '核验当前安全配置清单', en: 'Audit the current safety-equipment list'},
    current_quantified_test_report_not_in_scope: {zh: '补充耐久与防腐试验报告', en: 'Add durability and corrosion test reports'},
    altitude_and_current_environmental_test_required: {zh: '补充环境与高海拔试验', en: 'Add environmental and altitude testing'},
    requires_current_machine_control_test: {zh: '复核软件与液压标定版本', en: 'Verify software and hydraulic calibration'},
    requires_instrumented_and_operator_validation: {zh: '开展仪器测试与机手盲评', en: 'Run instrumented testing and operator blind evaluation'},
    quantified_current_test_required: {zh: '补充循环时间和平整精度', en: 'Add cycle-time and grading-accuracy data'},
    current_pro_configuration_and_user_clinic_required: {zh: '核验配置并开展北美用户诊断', en: 'Verify configuration and run a North American user clinic'},
    requires_current_service_task_time_study: {zh: '测量典型保养任务工时', en: 'Measure representative service-task time'},
    quantified_duty_cycle_test_required: {zh: '统一工况实测油耗', en: 'Measure fuel use under a common duty cycle'},
    requires_current_coating_audit_and_field_return_review: {zh: '涂层审计并复盘市场故障件', en: 'Audit coatings and review field-return parts'},
    requires_current_document_control_audit: {zh: '校核手册完整性与准确性', en: 'Audit manual completeness and accuracy'}
  };

  const scenarioAssets = {
    'scenario-transport': ['s049-photo-01.jpg', 's049-photo-02.jpg'],
    'scenario-municipal-roadwork': ['s050-photo-01.jpg', 's050-photo-02.jpg'],
    'scenario-light-demolition': ['s052-photo-01.jpg', 's052-photo-02.jpg', 's052-photo-03.jpg'],
    'scenario-foundation': ['s053-photo-01.jpg', 's053-photo-02.jpg', 's053-photo-03.jpg'],
    'scenario-landscape': ['s054-photo-01.jpg', 's054-photo-02.jpg', 's054-photo-03.jpg', 's055-photo-01.jpg', 's055-photo-02.jpg', 's055-photo-03.jpg'],
    'scenario-road-bridge': ['s056-photo-01.jpg', 's056-photo-02.jpg'],
    'scenario-agriculture-clearing': ['s057-photo-01.jpg', 's057-photo-02.jpg', 's057-photo-03.jpg'],
    'scenario-agriculture-drainage': ['s058-photo-01.jpg', 's058-photo-02.jpg', 's058-photo-03.jpg']
  };

  const scenarioImageCaptions = {
    's049-photo-01.jpg': {zh: '轻型皮卡牵引双轴拖车转运设备', en: 'Pickup towing a tandem-axle equipment trailer'},
    's049-photo-02.jpg': {zh: '设备装载后的拖车空间与载荷边界', en: 'Trailer space and payload boundary with the machine loaded'},
    's050-photo-01.jpg': {zh: '市政沟槽开挖与底部找平', en: 'Municipal trench excavation and bottom grading'},
    's050-photo-02.jpg': {zh: '道路破碎与管线施工', en: 'Pavement breaking and utility work'},
    's052-photo-01.jpg': {zh: '拆除构件抓取与装车', en: 'Grabbing and loading demolition material'},
    's052-photo-02.jpg': {zh: '小型构筑物拆除与分拣', en: 'Small-structure demolition and sorting'},
    's052-photo-03.jpg': {zh: '拆除物料吊装转运', en: 'Lifting and transferring demolition debris'},
    's053-photo-01.jpg': {zh: '地基施工前的混凝土破碎', en: 'Concrete breaking before foundation work'},
    's053-photo-02.jpg': {zh: '地基区域土方开挖', en: 'Earth excavation within a foundation footprint'},
    's053-photo-03.jpg': {zh: '建筑边界贴墙沟槽施工', en: 'Close-to-wall trenching beside a structure'},
    's054-photo-01.jpg': {zh: '场地清表与地形整理', en: 'Site clearing and terrain shaping'},
    's054-photo-02.jpg': {zh: '景观区域土方开挖', en: 'Landscape earthwork excavation'},
    's054-photo-03.jpg': {zh: '排水管沟开挖与铺设', en: 'Drainage trench excavation and pipe placement'},
    's055-photo-01.jpg': {zh: '挡墙与景观基坑施工', en: 'Retaining-wall and landscape excavation'},
    's055-photo-02.jpg': {zh: '完工后的草坪与景观地形', en: 'Completed lawn and shaped landscape'},
    's055-photo-03.jpg': {zh: '植被修剪与边界清理', en: 'Vegetation cutting and boundary clearing'},
    's056-photo-01.jpg': {zh: '预制管件吊装与定位', en: 'Lifting and positioning a precast pipe section'},
    's056-photo-02.jpg': {zh: '道路沟槽与地下管线施工', en: 'Road trench and underground utility work'},
    's057-photo-01.jpg': {zh: '林地清理与通道开辟', en: 'Woodland clearing and access preparation'},
    's057-photo-02.jpg': {zh: '树桩挖除与根系处理', en: 'Stump extraction and root removal'},
    's057-photo-03.jpg': {zh: '液压割草属具清理植被', en: 'Vegetation clearing with a hydraulic mower'},
    's058-photo-01.jpg': {zh: '农田排水沟连续开挖', en: 'Continuous agricultural drainage trenching'},
    's058-photo-02.jpg': {zh: '沟渠成形与坡面整理', en: 'Ditch shaping and bank finishing'},
    's058-photo-03.jpg': {zh: '波纹管吊装与铺设', en: 'Lifting and placing corrugated drainage pipe'}
  };

  const scenarioConditionLinks = {
    'scenario-transport': [{id: 'cond6', zh: '租赁 / 快速转场', en: 'Rental / rapid relocation'}],
    'scenario-municipal-roadwork': [{id: 'cond1', zh: '狭窄空间', en: 'Confined space'}, {id: 'cond2', zh: '沟槽深挖', en: 'Trenching'}, {id: 'cond3', zh: '土方短循环', en: 'Short-cycle loading'}],
    'scenario-light-demolition': [{id: 'cond4', zh: '破碎 / 多属具', en: 'Breaking / attachments'}, {id: 'cond1', zh: '狭窄空间', en: 'Confined space'}],
    'scenario-foundation': [{id: 'cond2', zh: '沟槽深挖', en: 'Trenching'}, {id: 'cond1', zh: '狭窄空间', en: 'Confined space'}],
    'scenario-landscape': [{id: 'cond1', zh: '狭窄空间', en: 'Confined space'}, {id: 'cond2', zh: '沟槽深挖', en: 'Trenching'}, {id: 'cond5', zh: '坡地稳定', en: 'Slope stability'}],
    'scenario-road-bridge': [{id: 'cond2', zh: '沟槽深挖', en: 'Trenching'}, {id: 'cond5', zh: '吊装稳定', en: 'Lifting stability'}],
    'scenario-agriculture-clearing': [{id: 'cond4', zh: '破碎 / 多属具', en: 'Breaking / attachments'}, {id: 'cond5', zh: '坡地软土', en: 'Slope / soft ground'}],
    'scenario-agriculture-drainage': [{id: 'cond2', zh: '沟槽深挖', en: 'Trenching'}, {id: 'cond5', zh: '吊装稳定', en: 'Lifting stability'}]
  };

  const scenarioEngineering = {
    'scenario-transport': {
      parameter: {zh: '典型整备组合约4,579 kg，明显压缩皮卡与14K拖车的载荷余量。', en: 'A representative equipped combination is about 4,579 kg, materially compressing pickup and 14K-trailer payload margin.'},
      configuration: {zh: '副配重、快换、拇指钳和铲斗必须按组合称重，不能只看基础机重量。', en: 'Counterweight, coupler, thumb and buckets must be weighed as a complete combination, not treated as isolated options.'},
      action: {zh: '建立车型、属具、拖车和牵引车辆的配置化运输边界表，并核验现量产版本。', en: 'Create a configuration-based transport envelope covering machine, attachments, trailer and tow vehicle, then verify the current production version.'}
    },
    'scenario-municipal-roadwork': {
      parameter: {zh: '高速行走3.6 km/h低于久保田4.6 km/h；铲斗力28.6 kN低于KX033-4的36.2 kN。', en: 'High travel speed is 3.6 km/h versus Kubota at 4.6 km/h; bucket force is 28.6 kN versus 36.2 kN on KX033-4.'},
      configuration: {zh: 'AUX2与快换形成附件基础，但推土铲浮动、回转回填和报警消音仍影响效率与扰民控制。', en: 'AUX2 and coupler provision support attachments, while blade float, swing-assisted backfill and alarm muting still affect productivity and disturbance control.'},
      action: {zh: '把回转力矩、制动线性、推土铲浮动和偏摆作为一个回填效率包验证。', en: 'Validate swing torque, braking linearity, blade float and blade angling as one backfill-productivity package.'}
    },
    'scenario-light-demolition': {
      parameter: {zh: 'AUX1最大流量40 L/min低于久保田60 L/min，限制部分高流量属具；基础破碎作业仍需核对压力和背压。', en: 'Maximum AUX1 flow is 40 L/min versus Kubota at 60 L/min, limiting some high-flow attachments; breaker pressure and back pressure still require verification.'},
      configuration: {zh: '双辅助管路和快换是基础优势，但卸油管路、驾驶室密封和报警消音需要补齐或核验。', en: 'Dual auxiliary plumbing and coupler provision are useful foundations, while case drain, cab sealing and alarm muting require confirmation or improvement.'},
      action: {zh: '按破碎锤、拇指钳和剪切属具建立流量、压力、背压、冷却与回油匹配表。', en: 'Build a flow, pressure, back-pressure, cooling and return-line match table for breakers, thumbs and demolition attachments.'}
    },
    'scenario-foundation': {
      parameter: {zh: '最大挖掘深度3,060 mm，比KX033-4少150 mm；短尾和75°/50°动臂偏摆有利于贴墙作业。', en: 'Maximum digging depth is 3,060 mm, 150 mm below KX033-4; short-tail packaging and 75°/50° boom swing support close-to-wall work.'},
      configuration: {zh: '缺少推土铲浮动会增加回填与找平操作量；坡度辅助和地下设施保护能力需结合实际配置判断。', en: 'The absence of blade float adds work during backfill and trimming; grade-assist and utility-protection capability depend on actual equipment.'},
      action: {zh: '用深度精度、贴墙开挖、回填循环和地下设施避让四项实测验证完整地基工况。', en: 'Validate the foundation workflow through depth accuracy, close-to-wall digging, backfill cycle and utility-avoidance tests.'}
    },
    'scenario-landscape': {
      parameter: {zh: '长斗杆扩大范围，但微动、平顺性和回转制动线性决定精整质量，不能只看最大作业范围。', en: 'A long arm extends reach, but inching, smoothness and swing-braking linearity determine finish quality beyond maximum working range.'},
      configuration: {zh: '多铲斗、拇指钳和破碎锤覆盖较好；推土铲浮动、偏摆和坡度辅助更直接影响修坡与草坪基底整平。', en: 'Bucket, thumb and breaker coverage is useful; blade float, blade angling and grade assistance more directly affect slope shaping and lawn-base grading.'},
      action: {zh: '用同一机手、同一场地对比修坡精度、平整循环时间和回填油耗。', en: 'Compare slope accuracy, grading cycle time and backfill fuel use with the same operator and site.'}
    },
    'scenario-road-bridge': {
      parameter: {zh: '记录的3 m起吊能力为1,145 kg，具备纸面优势，但必须统一推土铲位置、回转方向和额定口径。', en: 'Recorded lift at 3 m is 1,145 kg, a paper advantage that requires a common blade position, slew direction and rating basis.'},
      configuration: {zh: '液压夯、吊装点、行走报警和副配重决定施工覆盖；推土铲功能影响路缘石周边回填与收面。', en: 'Compactor compatibility, certified lift point, travel alarm and counterweight define coverage; blade functions affect curb backfill and finishing.'},
      action: {zh: '补齐起吊曲线口径，并用吊装、压实、回填三个循环验证稳定性和效率。', en: 'Normalize lift-chart conditions and validate stability and productivity across lifting, compaction and backfill cycles.'}
    },
    'scenario-agriculture-clearing': {
      parameter: {zh: 'AUX1最大流量40 L/min低于久保田60 L/min和三一70 L/min，高流量割草或开带属具适配受限。', en: 'Maximum AUX1 flow is 40 L/min versus Kubota at 60 L/min and SANY at 70 L/min, constraining high-flow mowing and clearing attachments.'},
      configuration: {zh: '拇指钳、割草机、螺旋钻和防护配置决定场景覆盖；非专业机手更依赖直观模式和低冲击启停。', en: 'Thumb, mower, auger and guarding provision define coverage; non-professional operators depend more on intuitive modes and low-shock travel.'},
      action: {zh: '优先定义北美农业属具清单，再反推辅助流量、冷却、防护和控制模式。', en: 'Define the North American agricultural attachment set first, then derive auxiliary flow, cooling, guarding and control-mode requirements.'}
    },
    'scenario-agriculture-drainage': {
      parameter: {zh: '行走速度偏低会拉长沟渠间转场；深度控制、回转回填和起吊稳定性共同决定铺管效率。', en: 'Low travel speed extends relocation time between trenches; depth control, swing-assisted backfill and lifting stability jointly determine pipe-installation productivity.'},
      configuration: {zh: '窄斗、拇指钳、吊装点、推土铲浮动和报警消音直接影响开沟、铺管、回填和早晚作业。', en: 'Narrow bucket, thumb, lift point, blade float and alarm muting directly affect trenching, pipe placement, backfill and early/late operation.'},
      action: {zh: '按每百米沟渠记录开挖、吊装、回填、整平和转场时间，形成完整工况效率基线。', en: 'Record excavation, lifting, backfill, finishing and relocation time per 100 m of trench to establish a full-cycle productivity baseline.'}
    }
  };

  const paperInsights = [
    {tone: 'gap', title: {zh: '运输与尺寸', en: 'Transport and package'}, metric: {zh: '4,200 kg基础机；1,740 mm宽', en: '4,200 kg base; 1,740 mm wide'}, detail: {zh: '较KX033-4的重量区间高436-835 kg，宽190 mm。对皮卡拖挂和狭小进场不利。', en: '436-835 kg above the KX033-4 mass range and 190 mm wider, reducing pickup-trailer and confined-access flexibility.'}},
    {tone: 'gap', title: {zh: '挖掘与短循环', en: 'Digging and short cycle'}, metric: {zh: '深度-150 mm；铲斗力-7.6 kN', en: 'Depth -150 mm; bucket force -7.6 kN'}, detail: {zh: '相对KX033-4，深挖余量和重挖前端能力偏弱；斗杆力20.3 kN是可保留优势。', en: 'Versus KX033-4, deep-dig margin and front-end breakout are lower; 20.3 kN arm force is a retained strength.'}},
    {tone: 'gap', title: {zh: '转场与属具', en: 'Mobility and attachments'}, metric: {zh: '高速3.6 km/h；AUX1 40 L/min', en: 'High speed 3.6 km/h; AUX1 40 L/min'}, detail: {zh: '分别比久保田低1.0 km/h和20 L/min，直接影响场内转场及高流量属具覆盖。', en: 'Respectively 1.0 km/h and 20 L/min below Kubota, directly affecting jobsite mobility and high-flow attachment coverage.'}},
    {tone: 'advantage', title: {zh: '起吊与管路基础', en: 'Lifting and plumbing foundation'}, metric: {zh: '3 m起吊1,145 kg；AUX2标配', en: '1,145 kg lift at 3 m; AUX2 standard'}, detail: {zh: '具备纸面优势，但起吊数据需统一工况复核；AUX2有利于旋转类属具。', en: 'Paper advantages that need a common lifting basis; standard AUX2 supports rotating attachments.'}}
  ];

  const paperConflicts = [
    {metric: {zh: '整机运输长度', en: 'Transport length'}, current: '4,960 mm', historical: '4,970 mm'},
    {metric: {zh: '整机运输高度', en: 'Transport height'}, current: '2,535 mm', historical: '2,550 mm'},
    {metric: {zh: '尾部回转半径', en: 'Tail-swing radius'}, current: '870 mm', historical: '850 mm'},
    {metric: {zh: 'AUX1最大流量', en: 'Maximum AUX1 flow'}, current: '50 L/min', historical: '40 L/min'}
  ];

  const fieldThemes = [
    {tone: 'pending', title: {zh: '安全与环境', en: 'Safety and environment'}, detail: {zh: '安全配置被记录为与竞品接近；常规温度范围为-20至40°C。当前实装清单、高海拔和耐久证据仍需核验。', en: 'Safety provision is recorded as comparable, with a normal temperature range of -20 to 40°C. Current installed equipment, altitude and durability evidence still need verification.'}},
    {tone: 'gap', title: {zh: '操控精度', en: 'Control precision'}, detail: {zh: '微动、作业精准性和平顺性为3分，久保田为4分；回转制动冲击导致工作装置回摆，是首要标定问题。', en: 'Inching, task precision and smoothness are rated 3 versus Kubota at 4; implement rebound from swing-braking shock is the first calibration issue.'}},
    {tone: 'gap', title: {zh: '驾驶环境', en: 'Operator environment'}, detail: {zh: '空调、座椅和界面友好性为3分，竞品为4分；脚踏距离、扶手箱内宽、屏幕和侧门操作均需目标用户验证。', en: 'HVAC, seat and interface usability are rated 3 versus 4; pedal reach, console width, display and door operation need target-user validation.'}},
    {tone: 'gap', title: {zh: '耐久与维修', en: 'Durability and service'}, detail: {zh: '防锈、薄板涂层和橡胶耐久为4分，竞品为5分；维修可达性4分对5分，并缺少独立液压油加注口。', en: 'Corrosion, sheet-metal coating and rubber durability are rated 4 versus 5; service access is 4 versus 5 and a dedicated hydraulic-oil fill point is absent.'}},
    {tone: 'advantage', title: {zh: '经济性潜力', en: 'Operating-economy potential'}, detail: {zh: '历史评价将燃油经济性列为优势，但必须在统一属具、负载和循环下实测，才能用于销售论证。', en: 'Historical evaluation identifies fuel economy as a strength, but common attachment, load and duty-cycle testing is required before using it in sales claims.'}}
  ];

  const actionPhases = [
    {title: {zh: '先建立事实基线', en: 'Establish the facts first'}, items: {zh: ['整备组合称重与拖车余量', '行走速度、循环时间与油耗', 'AUX流量、压力、背压和热平衡', '机手盲评与操控数据'], en: ['Equipped-combination mass and trailer margin', 'Travel speed, cycle time and fuel use', 'Auxiliary flow, pressure, back pressure and thermal balance', 'Operator blind evaluation and control data']}},
    {title: {zh: '再做系统级改进', en: 'Then improve systems'}, items: {zh: ['行走系统匹配', '回转与工作装置标定', '推土铲浮动与偏摆', '驾驶室、人机与维修可达性'], en: ['Travel-system matching', 'Swing and implement calibration', 'Blade float and angling', 'Cab, ergonomics and service access']}},
    {title: {zh: '最后形成平台方案', en: 'Finish with a platform decision'}, items: {zh: ['短尾与常规尾组合', '北美属具与配置包', '耐久、涂层和资料标准', '价格、渠道和残值闭环'], en: ['Short-tail and conventional-tail portfolio', 'North American attachment packages', 'Durability, coating and documentation standards', 'Price, channel and residual-value loop']}}
  ];

  let state = null;

  function text(value) {
    if (value == null) return '';
    if (typeof value === 'object' && ('zh' in value || 'en' in value)) return value[language] || value.zh || value.en || '';
    return String(value);
  }

  function narrative(value) {
    let output = text(value);
    const replacements = language === 'en'
      ? [[/The PPT/gi, 'The historical evaluation'], [/the PPT/gi, 'the historical evaluation'], [/PPT basis/gi, 'historical basis'], [/PPT/gi, 'historical record'], [/The source/gi, 'The historical evaluation'], [/the source/gi, 'the historical evaluation'], [/historical source material/gi, 'historical proposal']]
      : [[/PPT口径/g, '历史口径'], [/PPT显示/g, '历史记录显示'], [/PPT/g, '历史记录'], [/资料认为/g, '历史评价认为'], [/资料称/g, '历史记录显示'], [/资料将/g, '历史评价将'], [/资料中/g, '历史记录中'], [/资料/g, '历史记录']];
    replacements.forEach(([pattern, replacement]) => { output = output.replace(pattern, replacement); });
    return output;
  }

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }

  function findingKey(value) {
    if (value === '优势') return 'advantage';
    if (value === '差距') return 'gap';
    if (value === '资料未覆盖') return 'missing';
    return 'pending';
  }

  function findingLabel(value) { return copy[findingKey(value)]; }

  function assessmentKey(value) {
    if (value === 'covered') return 'advantage';
    if (value === 'mixed') return 'pending';
    return value === 'gap' || value === 'pending' ? value : 'pending';
  }

  function assessmentLabel(value) {
    if (value === 'covered') return copy.covered;
    if (value === 'mixed') return copy.mixed;
    return copy[assessmentKey(value)];
  }

  function technicalText(value) {
    const raw = String(value == null ? '' : value).trim();
    if (language !== 'en' || !/[\u3400-\u9fff]/.test(raw)) return raw;
    if (expanded.translations[raw]) return expanded.translations[raw];
    let translated = raw;
    Object.keys(expanded.translations)
      .sort((a, b) => b.length - a.length)
      .forEach((term) => { translated = translated.split(term).join(expanded.translations[term]); });
    return translated
      .replace(/标配/g, 'Standard')
      .replace(/选配/g, 'Optional')
      .replace(/无配置/g, 'Not equipped')
      .replace(/^有$/g, 'Yes')
      .replace(/^无$/g, 'No')
      .replace(/——/g, '-');
  }

  function sourceTable(slideNumber, tableId) {
    const slide = state?.visualAssets?.slides?.find((item) => Number(item.slide) === Number(slideNumber));
    return slide?.tables?.find((item) => item.id === tableId) || null;
  }

  function normalizedSourceRows(table, kind) {
    if (!table?.rows?.length) return {headers: [], rows: []};
    const isPaper = kind === 'paper';
    const header = isPaper ? table.rows[1].map((value, index) => value || table.rows[0][index] || '') : [...table.rows[0]];
    if (isPaper) {
      header[0] = copy.sourceCategory;
      header[1] = copy.metric;
      header[2] = copy.sourcePriority;
      header[3] = copy.sourceUnit;
    } else {
      header[0] = copy.dimension;
      header[1] = copy.sourceSystem;
      header[2] = copy.metric;
      header[3] = copy.sourcePriority;
      header[4] = copy.sourceUnit;
    }
    const keep = isPaper ? 9 : 8;
    const body = table.rows.slice(isPaper ? 2 : 1).map((row) => row.slice(0, keep));
    const carryColumns = isPaper ? [0] : [0, 1];
    const carry = {};
    body.forEach((row) => {
      carryColumns.forEach((index) => {
        if (row[index]) carry[index] = row[index];
        else row[index] = carry[index] || '';
      });
    });
    return {headers: header.slice(0, keep), rows: body};
  }

  function renderSourceDataGroup(group, kind) {
    const table = sourceTable(group.slide, group.table);
    if (!table) return '';
    const normalized = normalizedSourceRows(table, kind);
    const header = normalized.headers.map((value) => {
      const label = technicalText(value);
      const xcmgClass = /XE35U|XCMG/.test(label) ? ' class="xcmgSourceColumn"' : '';
      return `<th scope="col"${xcmgClass}>${escapeHtml(label)}</th>`;
    }).join('');
    const rowHeaderIndex = kind === 'paper' ? 1 : 2;
    const rows = normalized.rows.map((row) => `<tr>${row.map((value, index) => {
      const tag = index === rowHeaderIndex ? 'th' : 'td';
      const scope = index === rowHeaderIndex ? ' scope="row"' : '';
      const xcmgClass = /XE35U|XCMG/.test(normalized.headers[index]) ? ' class="xcmgSourceColumn"' : '';
      return `<${tag}${scope}${xcmgClass}>${escapeHtml(technicalText(value))}</${tag}>`;
    }).join('')}</tr>`).join('');
    return `<article class="sourceDataGroup" data-source-slide="${group.slide}">
      <div class="sourceDataHeading"><div><span>${kind === 'paper' ? escapeHtml(copy.completePaperData) : escapeHtml(copy.completeFieldData)}</span><h3>${escapeHtml(text(group.title))}</h3></div><div class="sourceDataMeta"><p>${escapeHtml(text(group.description))}</p>${sourceBadge(group.slide)}</div></div>
      <div class="sourceDataScroll"><table><caption class="srOnly">${escapeHtml(text(group.title))}</caption><thead><tr>${header}</tr></thead><tbody>${rows}</tbody></table></div>
    </article>`;
  }

  function fieldGroup(metric) {
    if (/safety/.test(metric)) return language === 'en' ? 'Safety' : '安全性';
    if (/corrosion|temperature/.test(metric)) return language === 'en' ? 'Reliability' : '可靠性';
    if (/travel|inching|grading/.test(metric)) return language === 'en' ? 'Control' : '操控性';
    if (/seat|hvac|space|hmi/.test(metric)) return language === 'en' ? 'Comfort' : '舒适性';
    return language === 'en' ? 'Service and economy' : '维修与经济性';
  }

  function makeSection(id, title, subtitle) {
    const section = document.createElement('section');
    section.id = id;
    section.className = 'pptSection';
    section.innerHTML = `<h2>${escapeHtml(title)}</h2><p class="sectionLead">${escapeHtml(subtitle)}</p>`;
    return section;
  }

  function renderInsightPoints(items, className = '') {
    return `<div class="decisionNarrative ${className}">${items.map((item) => `<article><span>${escapeHtml(text(item.label))}</span><h3>${escapeHtml(text(item.title))}</h3><p>${escapeHtml(text(item.detail))}</p></article>`).join('')}</div>`;
  }

  function sourcePageText(value) {
    const pages = (Array.isArray(value) ? value : [value]).map(Number).filter(Number.isFinite).sort((a, b) => a - b);
    if (!pages.length) return copy.sourcePpt;
    const ranges = [];
    let start = pages[0];
    let end = pages[0];
    pages.slice(1).forEach((page) => {
      if (page === end + 1) end = page;
      else { ranges.push(start === end ? `${start}` : `${start}-${end}`); start = page; end = page; }
    });
    ranges.push(start === end ? `${start}` : `${start}-${end}`);
    return language === 'en' ? `${copy.sourcePpt} · pp. ${ranges.join(', ')}` : `${copy.sourcePpt} · 第${ranges.join('、')}页`;
  }

  function sourceBadge(source, statusLabel = copy.historicalBasis) {
    const pages = typeof source === 'object' && source !== null ? source.source_slide : source;
    const label = sourcePageText(pages);
    return `<span class="sourceBadge" data-source-slide="${escapeHtml(Array.isArray(pages) ? pages.join(',') : pages)}"><b>${escapeHtml(label)}</b><em>${escapeHtml(statusLabel)}</em></span>`;
  }

  function dataStatusLabel(status) {
    if (status === 'source_forecast') return copy.sourceForecast;
    if (status === 'source_estimate') return copy.sourceEstimate;
    return copy.historical;
  }

  function formatNumber(value, digits = 0) {
    return Number(value).toLocaleString(language === 'en' ? 'en-US' : 'zh-CN', {maximumFractionDigits: digits});
  }

  function renderBrandSales(data) {
    if (!data) return '';
    const maxTotal = Math.max(...data.years.map((year) => year.total));
    const volumeColumns = data.years.map((year, yearIndex) => {
      const previous = data.years[yearIndex - 1]?.total;
      const delta = previous ? (year.total - previous) / previous * 100 : null;
      const deltaLabel = delta === null ? copy.basePeriod : `${copy.yearOverYear} ${delta > 0 ? '+' : ''}${formatNumber(delta, 1)}%`;
      const statusClass = year.status === 'source_estimate' ? 'estimate' : year.status === 'source_forecast' ? 'forecast' : 'historical';
      return `<div class="volumeColumn ${statusClass}">
        <div class="volumeBarArea"><i style="height:${(year.total / maxTotal * 100).toFixed(1)}%"></i></div>
        <b>${formatNumber(year.total)} ${escapeHtml(copy.units)}</b>
        <strong>${escapeHtml(year.year)}</strong>
        <span>${escapeHtml(dataStatusLabel(year.status))}</span>
        <small class="${delta !== null && delta < 0 ? 'negative' : ''}">${escapeHtml(deltaLabel)}</small>
      </div>`;
    }).join('');
    const volumeLegend = [
      {className: 'historical', label: copy.historical},
      {className: 'estimate', label: copy.estimate},
      {className: 'forecast', label: copy.forecast}
    ].map((item) => `<span class="${item.className}"><i></i>${escapeHtml(item.label)}</span>`).join('');
    const rows = data.years.map((year, yearIndex) => {
      const segments = data.series.map((series) => {
        const value = series.values[yearIndex];
        const width = year.total ? value / year.total * 100 : 0;
        return `<span style="width:${width.toFixed(3)}%;background:${escapeHtml(series.color)}" title="${escapeHtml(series.brand)} · ${formatNumber(value)} ${copy.units}"></span>`;
      }).join('');
      return `<div class="brandStackRow"><b>${escapeHtml(year.year)}</b><div class="brandStackTrack">${segments}</div><strong>${formatNumber(year.total)}</strong><small>${escapeHtml(dataStatusLabel(year.status))}</small></div>`;
    }).join('');
    const legend = data.series.map((series) => `<span><i style="background:${escapeHtml(series.color)}"></i>${escapeHtml(series.brand)}</span>`).join('');
    const tableHeader = data.series.map((series) => `<th scope="col">${escapeHtml(series.brand)}</th>`).join('');
    const tableRows = data.years.map((year, yearIndex) => `<tr><th scope="row">${escapeHtml(year.year)}</th>${data.series.map((series) => `<td>${formatNumber(series.values[yearIndex])}</td>`).join('')}<td><b>${formatNumber(year.total)}</b></td><td>${escapeHtml(dataStatusLabel(year.status))}</td></tr>`).join('');
    return `<article class="evidenceVisual brandSalesVisual">
      <header><div><h3>${escapeHtml(text(data.title))}</h3><p>${escapeHtml(text(data.subtitle))}</p></div>${sourceBadge(data)}</header>
      <div class="volumeStatusLegend" aria-label="${escapeHtml(copy.dataStatus)}">${volumeLegend}</div>
      <div class="volumeSeries" role="img" aria-label="${escapeHtml(copy.volumeTitle)}">${volumeColumns}</div>
      <div class="brandStackChart" role="img" aria-label="${escapeHtml(text(data.title))}">${rows}</div>
      <div class="chartLegend">${legend}</div>
      <div class="evidenceTableScroll compactEvidenceTable"><table><caption class="srOnly">${escapeHtml(copy.brandSalesTable)}</caption><thead><tr><th>${escapeHtml(copy.year)}</th>${tableHeader}<th>${escapeHtml(copy.total)}</th><th>${escapeHtml(copy.dataStatus)}</th></tr></thead><tbody>${tableRows}</tbody></table></div>
    </article>`;
  }

  function renderModelDemand(data) {
    if (!data) return '';
    const max = Math.max(...data.models.map((item) => item.units));
    const rows = data.models.map((item, index) => `<div class="modelDemandRow"><span>${index + 1}</span><div><b>${escapeHtml(item.model)}</b><small>${escapeHtml(item.brand)}</small></div><i><em style="width:${(item.units / max * 100).toFixed(1)}%"></em></i><strong>${formatNumber(item.units)}</strong></div>`).join('');
    return `<article class="evidenceVisual modelDemandVisual"><header><div><h3>${escapeHtml(text(data.title))}</h3><p>${escapeHtml(text(data.subtitle))}</p></div>${sourceBadge(data)}</header><div class="modelDemandChart">${rows}</div></article>`;
  }

  function renderPriceShare(data) {
    if (!data) return '';
    const xMin = 50000;
    const xMax = 75000;
    const yMax = 25;
    const plot = {left: 68, top: 24, width: 570, height: 228};
    const x = (value) => plot.left + (value - xMin) / (xMax - xMin) * plot.width;
    const y = (value) => plot.top + plot.height - value / yMax * plot.height;
    const maxVolume = Math.max(...data.points.map((item) => item.volume));
    const offsets = {DEERE: [10, -10], KUBOTA: [-62, -9], BOBCAT: [10, 18], CAT: [10, -8], SANY: [10, -8], XCMG: [10, -8]};
    const yGrid = [0, 5, 10, 15, 20, 25].map((tick) => `<g><line x1="${plot.left}" x2="${plot.left + plot.width}" y1="${y(tick)}" y2="${y(tick)}"></line><text x="${plot.left - 10}" y="${y(tick) + 4}" text-anchor="end">${tick}</text></g>`).join('');
    const xGrid = [50000, 60000, 70000].map((tick) => `<g><line x1="${x(tick)}" x2="${x(tick)}" y1="${plot.top}" y2="${plot.top + plot.height}"></line><text x="${x(tick)}" y="${plot.top + plot.height + 20}" text-anchor="middle">${(tick / 10000).toFixed(1)}</text></g>`).join('');
    const points = data.points.map((item) => {
      const radius = 6 + Math.sqrt(item.volume / maxVolume) * 14;
      const offset = offsets[item.brand] || [10, -8];
      const fill = item.brand === 'XCMG' ? '#f5b400' : '#005aa7';
      return `<g class="scatterPoint ${item.brand === 'XCMG' ? 'isXcmg' : ''}" tabindex="0"><title>${escapeHtml(item.brand)} · $${formatNumber(item.price_usd)} · ${item.share_pct.toFixed(1)}% · ${formatNumber(item.volume, 1)}</title><circle cx="${x(item.price_usd)}" cy="${y(item.share_pct)}" r="${radius.toFixed(1)}" fill="${fill}"></circle><text x="${x(item.price_usd) + offset[0]}" y="${y(item.share_pct) + offset[1]}">${escapeHtml(item.brand)}</text></g>`;
    }).join('');
    return `<article class="evidenceVisual priceShareVisual"><header><div><h3>${escapeHtml(text(data.title))}</h3><p>${escapeHtml(text(data.subtitle))}</p></div>${sourceBadge(data)}</header><svg viewBox="0 0 700 300" role="img" aria-label="${escapeHtml(text(data.title))}" class="priceShareSvg"><g class="chartGrid">${yGrid}${xGrid}</g><line class="chartAxis" x1="${plot.left}" x2="${plot.left + plot.width}" y1="${plot.top + plot.height}" y2="${plot.top + plot.height}"></line><line class="chartAxis" x1="${plot.left}" x2="${plot.left}" y1="${plot.top}" y2="${plot.top + plot.height}"></line>${points}<text class="axisTitle" x="${plot.left + plot.width / 2}" y="294" text-anchor="middle">${escapeHtml(copy.priceAxis)}</text><text class="axisTitle" transform="translate(14 ${plot.top + plot.height / 2}) rotate(-90)" text-anchor="middle">${escapeHtml(copy.shareAxis)}</text></svg></article>`;
  }

  function renderTransportBreakdown(data) {
    if (!data) return '';
    const max = 5000;
    const colors = ['#005aa7', '#f5b400', '#829bb2', '#0f7b45'];
    const packageRows = data.packages.map((item) => {
      const segments = item.components.map((component, index) => `<span style="width:${(component.kg / max * 100).toFixed(2)}%;background:${colors[index]}" title="${escapeHtml(text(component.label))} · ${formatNumber(component.kg)} kg"></span>`).join('');
      return `<div class="massPackageRow"><div><b>${escapeHtml(text(item.label))}</b><small>${item.status === 'historical_plan_unverified' ? escapeHtml(copy.currentUnverified) : escapeHtml(copy.historicalBasis)}</small></div><div class="massTrack">${segments}</div><strong>${formatNumber(item.equipped_total_kg)} kg</strong></div>`;
    }).join('');
    const componentRows = data.packages.map((item) => `<tr><th scope="row">${escapeHtml(text(item.label))}</th><td>${item.components.map((component) => `${escapeHtml(text(component.label))} ${formatNumber(component.kg)} kg`).join(' + ')}</td><td><b>${formatNumber(item.equipped_total_kg)} kg</b></td></tr>`).join('');
    const optional = data.additional_attachments.map((item) => `<li><span>${escapeHtml(text(item.label))}</span><b>${formatNumber(item.kg)} kg</b></li>`).join('');
    return `<article class="evidenceVisual transportBreakdownVisual"><header><div><h3>${escapeHtml(text(data.title))}</h3><p>${escapeHtml(text(data.subtitle))}</p></div>${sourceBadge(data)}</header><div class="massPackageChart">${packageRows}</div><div class="massDetailGrid"><div class="evidenceTableScroll"><table><thead><tr><th>${escapeHtml(copy.packageName)}</th><th>${escapeHtml(copy.component)}</th><th>${escapeHtml(copy.packageTotal)}</th></tr></thead><tbody>${componentRows}</tbody></table></div><div class="optionalAttachmentList"><h4>${escapeHtml(copy.optionalAttachments)}</h4><ul>${optional}</ul></div></div></article>`;
  }

  function renderPerformanceVisual(data) {
    if (!data) return '';
    const cards = data.metrics.map((metric) => {
      const finite = metric.values.filter((value) => Number.isFinite(value));
      const max = Math.max(...finite);
      const rows = data.models.map((model, index) => {
        const value = metric.values[index];
        const hasValue = Number.isFinite(value);
        return `<div class="performanceBarRow ${index === 0 ? 'isXcmg' : ''}"><span>${escapeHtml(model)}</span><i>${hasValue ? `<em style="width:${Math.max(2, value / max * 100).toFixed(1)}%"></em>` : ''}</i><b>${hasValue ? `${formatNumber(value, 1)} ${escapeHtml(metric.unit)}` : escapeHtml(copy.noSourceValue)}</b></div>`;
      }).join('');
      const basis = metric.basis ? `<p>${escapeHtml(text(metric.basis))}</p>` : '';
      return `<article class="performanceFacet"><h4>${escapeHtml(text(metric.label))}<small>${escapeHtml(metric.unit)}</small></h4>${rows}${basis}</article>`;
    }).join('');
    return `<article class="evidenceVisual performanceEvidence"><header><div><h3>${escapeHtml(text(data.title))}</h3><p>${escapeHtml(copy.performanceScaleNote)}</p></div>${sourceBadge(data)}</header><div class="performanceFacetGrid">${cards}</div></article>`;
  }

  function renderFieldHeatmap(data) {
    if (!data) return '';
    let lastGroup = '';
    const rows = data.rows.map((item) => {
      const group = text(item.group);
      const groupCell = group === lastGroup ? '' : group;
      lastGroup = group;
      return `<tr><th scope="row">${escapeHtml(groupCell)}</th><td>${escapeHtml(text(item.metric))}<small>${sourcePageText(item.source_slide)}</small></td>${item.ratings.map((rating) => `<td class="ratingCell" data-rating="${rating}" title="${escapeHtml(text(item.metric))}: ${rating}/5"><b>${rating}</b></td>`).join('')}</tr>`;
    }).join('');
    return `<article class="evidenceVisual fieldHeatmapVisual"><header><div><h3>${escapeHtml(text(data.title))}</h3><p>${escapeHtml(text(data.subtitle))}</p></div>${sourceBadge(data)}</header><div class="heatmapLegend"><span>1</span><i data-rating="1"></i><i data-rating="2"></i><i data-rating="3"></i><i data-rating="4"></i><i data-rating="5"></i><span>5</span><b>${escapeHtml(copy.ratingLegend)}</b></div><div class="evidenceTableScroll"><table class="ratingHeatmap"><thead><tr><th>${escapeHtml(copy.dimension)}</th><th>${escapeHtml(copy.metric)}</th>${data.models.map((model, index) => `<th class="${index === 0 ? 'xcmgHeatHeader' : ''}">${escapeHtml(model)}</th>`).join('')}</tr></thead><tbody>${rows}</tbody></table></div></article>`;
  }

  function radarPoints(values, cx, cy, radius) {
    return values.map((value, index) => {
      const angle = -Math.PI / 2 + index * Math.PI * 2 / values.length;
      const r = radius * Number(value) / 5;
      return `${(cx + Math.cos(angle) * r).toFixed(1)},${(cy + Math.sin(angle) * r).toFixed(1)}`;
    }).join(' ');
  }

  function renderCompetitivenessProfile(data) {
    if (!data) return '';
    const cx = 250;
    const cy = 176;
    const radius = 126;
    const levels = [1, 2, 3, 4, 5].map((level) => `<polygon points="${radarPoints(Array(data.dimensions.length).fill(level), cx, cy, radius)}"></polygon>`).join('');
    const axes = data.dimensions.map((_, index) => {
      const angle = -Math.PI / 2 + index * Math.PI * 2 / data.dimensions.length;
      return `<line x1="${cx}" y1="${cy}" x2="${(cx + Math.cos(angle) * radius).toFixed(1)}" y2="${(cy + Math.sin(angle) * radius).toFixed(1)}"></line><text x="${(cx + Math.cos(angle) * (radius + 22)).toFixed(1)}" y="${(cy + Math.sin(angle) * (radius + 22) + 4).toFixed(1)}" text-anchor="middle">${index + 1}</text>`;
    }).join('');
    const series = data.series.map((item) => `<polygon class="radarSeries" points="${radarPoints(item.values, cx, cy, radius)}" style="--series:${escapeHtml(item.color)}"><title>${escapeHtml(item.model)}: ${item.values.join(' / ')}</title></polygon>`).join('');
    const legend = data.series.map((item) => `<span><i style="background:${escapeHtml(item.color)}"></i>${escapeHtml(item.model)}</span>`).join('');
    const keys = data.dimensions.map((item, index) => `<li><b>${index + 1}</b>${escapeHtml(text(item))}</li>`).join('');
    return `<article class="evidenceVisual competitivenessProfile"><header><div><h3>${escapeHtml(text(data.title))}</h3><p>${escapeHtml(text(data.subtitle))}</p></div>${sourceBadge(data)}</header><div class="radarLayout"><div><svg viewBox="0 0 500 340" role="img" aria-label="${escapeHtml(text(data.title))}" class="competitivenessRadar"><g class="radarGrid">${levels}${axes}</g>${series}</svg><div class="chartLegend radarLegend">${legend}</div></div><div class="radarKey"><h4>${escapeHtml(copy.profileKey)}</h4><ol>${keys}</ol></div></div></article>`;
  }

  function renderImprovementLedger(data) {
    if (!data) return '';
    const rows = data.items.map((item) => `<tr><td>${item.id}</td><th scope="row">${escapeHtml(text(item.system))}</th><td>${escapeHtml(text(item.problem))}</td><td>${escapeHtml(text(item.source_action))}</td><td>${escapeHtml(item.upgrade_date)}</td><td>${escapeHtml(item.production_date)}</td><td><span class="scenarioStatus status-pending">${escapeHtml(copy.currentUnverified)}</span></td></tr>`).join('');
    return `<article class="evidenceVisual improvementLedger"><header><div><h3>${escapeHtml(text(data.title))}</h3><p>${escapeHtml(text(data.subtitle))}</p></div>${sourceBadge(data, copy.currentUnverified)}</header><p class="ledgerCaveat">${escapeHtml(copy.ledgerCaveat)}</p><div class="evidenceTableScroll"><table><thead><tr><th>${escapeHtml(copy.itemNo)}</th><th>${escapeHtml(copy.system)}</th><th>${escapeHtml(copy.problem)}</th><th>${escapeHtml(copy.sourceAction)}</th><th>${escapeHtml(copy.historicalUpgradeDate)}</th><th>${escapeHtml(copy.historicalProductionDate)}</th><th>${escapeHtml(copy.status)}</th></tr></thead><tbody>${rows}</tbody></table></div></article>`;
  }

  function renderMarket(view, sourceVisuals) {
    const section = makeSection('ppt-market', copy.marketTitle, copy.marketSubtitle);
    const customers = view.market.customer_mix.map((item) => `<span style="width:${item.value}%" title="${escapeHtml(text(item.label))} ${item.value}%"></span>`).join('');
    const customerLegend = view.market.customer_mix.map((item) => `<li><i></i><span>${escapeHtml(text(item.label))}</span><b>${item.value}%</b></li>`).join('');
    const logic = view.market.purchase_logic.map((item) => `<li>${escapeHtml(text(item))}</li>`).join('');
    const marketPoints = [
      {label: copy.marketRead, title: copy.marketRole, detail: copy.marketRoleText},
      {label: copy.marketRead, title: copy.competition, detail: copy.competitionText},
      {label: copy.marketRead, title: copy.xcmgEntry, detail: copy.xcmgEntryText}
    ];
    const portfolioRows = expanded.marketPortfolio.map((item) => `<tr class="${item.brand === 'XCMG' ? 'xcmgPortfolioRow' : ''}"><th scope="row">${escapeHtml(item.brand)}</th><td>${escapeHtml(item.models)}</td><td>${escapeHtml(text(item.architecture))}</td><td>${escapeHtml(text(item.implication))}</td></tr>`).join('');
    const transportRuleRows = expanded.transportRules.map((item) => `<tr><th scope="row">${escapeHtml(item.level)}</th><td>${escapeHtml(text(item.threshold))}</td><td>${escapeHtml(text(item.implication))}</td></tr>`).join('');
    const positionData = sourceVisuals?.historical_positioning;
    const positionRows = (positionData?.rows || expanded.positioning).map((item) => `<tr class="${item.brand === 'XCMG' ? 'xcmgPositionRow' : ''}"><th scope="row">${escapeHtml(item.brand)}</th><td>${escapeHtml(item.models)}</td><td>${escapeHtml(item.price || `$${formatNumber(item.price_usd)}`)}</td><td>${escapeHtml(item.share)}</td></tr>`).join('');
    const transportSource = sourceVisuals?.transport;
    const currentPackage = transportSource?.packages?.find((item) => item.id === 'xe35u-current');
    const historicalPackage = transportSource?.packages?.find((item) => item.id === 'xe35u-pro-historical');
    const trailerContext = transportSource?.trailer_context;
    const lowerPayload = trailerContext?.effective_payload_kg?.[0];
    const signedMass = (value) => `${value > 0 ? '+' : ''}${formatNumber(value)} kg`;
    const transportFacts = currentPackage && historicalPackage && trailerContext ? `
      <dl class="transportBoundaryFacts">
        <div><dt>${escapeHtml(copy.transportPayloadWindow)}</dt><dd>${formatNumber(trailerContext.effective_payload_kg[0])}-${formatNumber(trailerContext.effective_payload_kg[1])} kg</dd><small>${formatNumber(trailerContext.effective_payload_lb[0])}-${formatNumber(trailerContext.effective_payload_lb[1])} lb</small></div>
        <div><dt>${escapeHtml(copy.transportCurrentPackage)}</dt><dd>${formatNumber(currentPackage.equipped_total_kg)} kg</dd><small class="negative">${escapeHtml(copy.transportMargin)} ${signedMass(lowerPayload - currentPackage.equipped_total_kg)}</small></div>
        <div><dt>${escapeHtml(copy.transportHistoricalPackage)}</dt><dd>${formatNumber(historicalPackage.equipped_total_kg)} kg</dd><small class="positive">${escapeHtml(copy.transportMargin)} ${signedMass(lowerPayload - historicalPackage.equipped_total_kg)}</small></div>
      </dl>
      <p class="transportMarginNote">${escapeHtml(copy.transportMarginNote)}</p>` : '';

    section.insertAdjacentHTML('beforeend', `
      <p class="analysisScope">${escapeHtml(copy.scoringBoundary)}</p>
      <div class="marketDecisionGrid">
        ${renderBrandSales(sourceVisuals?.market?.annual_brand_sales)}
        <div class="pptModule customerEvidence"><div class="pptModuleTitle"><span>${escapeHtml(copy.customerTitle)}</span>${sourceBadge(49)}</div><div class="shareStrip"><div class="shareStripHead"><span>${escapeHtml(copy.shareTitle)}</span><b>${view.market.leading_share.value}%</b></div><div class="shareBar"><span></span></div><div class="brandNames"><span>${escapeHtml(copy.shareNote)}</span>${sourceBadge(48)}</div></div><div class="customerMix" aria-label="${escapeHtml(copy.customerTitle)}">${customers}</div><ul class="customerLegend">${customerLegend}</ul><p class="sourceCaveat">${escapeHtml(narrative(view.market.customer_mix_note))}</p><h3 class="pptModuleTitle"><span>${escapeHtml(copy.purchaseLogic)}</span></h3><ul class="purchaseLogic">${logic}</ul></div>
      </div>
      <div class="sourceVisualPair">${renderModelDemand(sourceVisuals?.market?.model_demand_2025)}${renderPriceShare(sourceVisuals?.market?.brand_position_2025)}</div>
      ${renderTransportBreakdown(sourceVisuals?.transport)}
      ${renderInsightPoints(marketPoints, 'marketNarrative')}
      <article class="transportStory">
        <header class="transportStoryHeader"><div><span>${escapeHtml(copy.marketRead)}</span><h3>${escapeHtml(copy.transportStoryTitle)}</h3></div>${sourceBadge(transportSource || 49)}</header>
        <div class="transportStoryGrid">
          <div class="transportStoryCopy"><p>${escapeHtml(copy.transportStoryText)}</p>${transportFacts}<div class="transportDecision"><b>${escapeHtml(copy.transportDecisionTitle)}</b><span>${escapeHtml(copy.transportDecisionText)}</span></div></div>
          <div class="transportPhotoPair"><figure><img src="ppt-integration-demo/assets/extracted/s049-photo-01.jpg" alt="${escapeHtml(copy.transportCaptionA)}"><figcaption>${escapeHtml(copy.transportCaptionA)}</figcaption></figure><figure><img src="ppt-integration-demo/assets/extracted/s049-photo-02.jpg" alt="${escapeHtml(copy.transportCaptionB)}"><figcaption>${escapeHtml(copy.transportCaptionB)}</figcaption></figure></div>
        </div>
      </article>
      <div class="marketDetailGrid">
        <article class="marketDetailBlock"><div class="pptModuleTitle"><span>${escapeHtml(copy.portfolioTitle)}</span></div><div class="marketTableScroll"><table class="marketPortfolioMatrix"><thead><tr><th>${escapeHtml(copy.portfolioBrand)}</th><th>${escapeHtml(copy.portfolioCount)}</th><th>${escapeHtml(copy.portfolioArchitecture)}</th><th>${escapeHtml(copy.portfolioImplication)}</th></tr></thead><tbody>${portfolioRows}</tbody></table></div></article>
        <article class="marketDetailBlock"><div class="pptModuleTitle"><span>${escapeHtml(copy.transportRuleTitle)}</span></div><p class="marketTableCaveat">${escapeHtml(copy.transportRuleCaveat)}</p><div class="marketTableScroll"><table class="transportRuleTable"><thead><tr><th>${escapeHtml(copy.licenceClass)}</th><th>${escapeHtml(copy.generalThreshold)}</th><th>${escapeHtml(copy.applicationImpact)}</th></tr></thead><tbody>${transportRuleRows}</tbody></table></div></article>
      </div>
      <div class="positioningBlock marketPositioning"><div class="pptModuleTitle"><span>${escapeHtml(copy.positioningTitle)}</span>${sourceBadge(positionData || 68)}</div><p>${escapeHtml(copy.positioningCaveat)}</p><div class="positioningScroll"><table><thead><tr><th>${escapeHtml(copy.positioningBrand)}</th><th>${escapeHtml(copy.positioningModels)}</th><th>${escapeHtml(copy.positioningPrice)}</th><th>${escapeHtml(copy.positioningShare)}</th></tr></thead><tbody>${positionRows}</tbody></table></div></div>`);
    return section;
  }

  function renderScenarioGallery(record) {
    const assets = scenarioAssets[record.id] || [];
    const countClass = `photoCount-${Math.min(assets.length, 6)}`;
    return `<div class="scenarioPhotoGrid ${countClass}">${assets.map((asset) => {
      const caption = text(scenarioImageCaptions[asset]) || text(record.title);
      return `<figure><img src="ppt-integration-demo/assets/extracted/${asset}" alt="${escapeHtml(caption)}"><figcaption>${escapeHtml(caption)}</figcaption></figure>`;
    }).join('')}</div>`;
  }

  function renderScenarioBody(record, index) {
    const needs = record.needs?.[language] || record.needs?.zh || [];
    const steps = record.steps?.[language] || record.steps?.zh || [];
    const key = findingKey(record.finding_status);
    const engineering = scenarioEngineering[record.id];
    const links = (scenarioConditionLinks[record.id] || []).map((item) => `<a href="#${escapeHtml(item.id)}">${escapeHtml(language === 'en' ? item.en : item.zh)}</a>`).join('');
    const assessments = (expanded.scenarioAssessments[record.id] || []).map((item) => {
      const statusKey = assessmentKey(item.status);
      return `<tr><th scope="row" data-label="${escapeHtml(copy.scenarioRequirement)}">${escapeHtml(text(item.need))}</th><td data-label="${escapeHtml(copy.currentFit)}">${escapeHtml(text(item.current))}</td><td data-label="${escapeHtml(copy.status)}"><span class="scenarioStatus status-${statusKey}">${escapeHtml(assessmentLabel(item.status))}</span></td><td data-label="${escapeHtml(copy.productAction)}">${escapeHtml(text(item.action))}</td></tr>`;
    }).join('');
    return `
      <article class="scenarioBand" id="job-${escapeHtml(record.id)}" data-scenario-id="${escapeHtml(record.id)}">
        <header class="scenarioBandHeader">
          <span class="scenarioNumber">${String(index + 1).padStart(2, '0')}</span>
          <div class="scenarioBandTitle"><h3>${escapeHtml(text(record.title))}</h3><div class="scenarioConditionLinks"><span>${escapeHtml(copy.linkedConditions)}</span>${links}</div><div class="scenarioSource">${sourceBadge(record)}</div></div>
          <span class="scenarioStatus status-${key}">${escapeHtml(findingLabel(record.finding_status))}</span>
        </header>
        <div class="scenarioBandMain">
          ${renderScenarioGallery(record)}
          <div class="scenarioBody">
            <dl class="scenarioFacts">
              <div class="scenarioFact"><dt>${escapeHtml(copy.customer)}</dt><dd>${escapeHtml(text(record.customer))}</dd></div>
              <div class="scenarioFact"><dt>${escapeHtml(copy.needs)}</dt><dd><ul>${needs.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul></dd></div>
              <div class="scenarioFact"><dt>${escapeHtml(copy.steps)}</dt><dd><ol>${steps.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ol></dd></div>
              <div class="scenarioFact"><dt>${escapeHtml(copy.finding)}</dt><dd class="scenarioFinding">${escapeHtml(narrative(record.conclusion))}</dd></div>
            </dl>
          </div>
        </div>
        <div class="scenarioEngineering">
          <article><span>${escapeHtml(copy.parameterImpact)}</span><p>${escapeHtml(text(engineering?.parameter))}</p></article>
          <article><span>${escapeHtml(copy.configurationImpact)}</span><p>${escapeHtml(text(engineering?.configuration))}</p></article>
          <article><span>${escapeHtml(copy.engineeringAction)}</span><p>${escapeHtml(text(engineering?.action))}</p></article>
        </div>
        <div class="scenarioAssessment"><table><caption class="srOnly">${escapeHtml(text(record.title))}</caption><thead><tr><th>${escapeHtml(copy.scenarioRequirement)}</th><th>${escapeHtml(copy.currentFit)}</th><th>${escapeHtml(copy.status)}</th><th>${escapeHtml(copy.productAction)}</th></tr></thead><tbody>${assessments}</tbody></table></div>
      </article>`;
  }

  function renderScenarios(records) {
    const section = makeSection('ppt-scenarios', copy.scenarioTitle, copy.scenarioSubtitle);
    section.insertAdjacentHTML('beforeend', `<div class="scenarioSequence">${records.map((record, index) => renderScenarioBody(record, index)).join('')}</div>`);
    return section;
  }

  function renderPaper(view, sourceVisuals) {
    const section = makeSection('ppt-paper', copy.paperTitle, copy.paperSubtitle);
    const headerModels = view.paper_comparison.models.map((model, index) => `<th class="${index === 0 ? 'xcmgColumn' : ''}">${escapeHtml(model)}</th>`).join('');
    const rows = view.paper_comparison.metrics.map((metric) => {
      const values = metric.values.map((value, index) => `<td class="${index === 0 ? 'xcmgColumn' : ''}">${escapeHtml(value)}${value !== '/' ? ` <small>${escapeHtml(metric.unit)}</small>` : ''}</td>`).join('');
      return `<tr class="metric-${escapeHtml(metric.status)}"><th>${escapeHtml(text(metric.name))}</th>${values}<td class="metricFinding">${escapeHtml(narrative(metric.finding))}</td></tr>`;
    }).join('');
    const configRows = view.paper_comparison.configuration_findings.map((item) => `<div class="configRow"><b>${escapeHtml(text(item.label))}</b><strong>${escapeHtml(narrative(item.xcmg))}</strong><span>${escapeHtml(narrative(item.comparison))}</span></div>`).join('');
    const insights = `<div class="paperInsightGrid">${paperInsights.map((item) => `<article class="tone-${item.tone}"><span>${escapeHtml(text(item.title))}</span><b>${escapeHtml(text(item.metric))}</b><p>${escapeHtml(text(item.detail))}</p></article>`).join('')}</div>`;
    const conflictRows = paperConflicts.map((item) => `<tr><th scope="row">${escapeHtml(text(item.metric))}</th><td>${escapeHtml(item.current)}</td><td>${escapeHtml(item.historical)}</td><td>${escapeHtml(copy.conflictRule)}</td></tr>`).join('');
    const completeGroups = expanded.paperGroups.map((group) => renderSourceDataGroup(group, 'paper')).join('');
    section.insertAdjacentHTML('beforeend', `<p class="analysisScope">${escapeHtml(copy.paperBoundary)}</p>${renderPerformanceVisual(sourceVisuals?.performance)}<div class="pptModuleTitle"><span>${escapeHtml(copy.paperRead)}</span>${sourceBadge([59, 60, 61])}</div>${insights}<div class="dataConflictBlock"><div class="pptModuleTitle"><span>${escapeHtml(copy.dataConflictTitle)}</span></div><div class="dataConflictScroll"><table><thead><tr><th>${escapeHtml(copy.metric)}</th><th>${escapeHtml(copy.currentDataset)}</th><th>${escapeHtml(copy.historicalReference)}</th><th>${escapeHtml(copy.handlingRule)}</th></tr></thead><tbody>${conflictRows}</tbody></table></div></div><div class="pptModuleTitle directDataTitle"><span>${escapeHtml(copy.fullPaper)}</span>${sourceBadge([59, 60, 61])}</div><div class="comparisonMatrix"><table><thead><tr><th>${escapeHtml(copy.metric)}</th>${headerModels}<th>${escapeHtml(copy.findingColumn)}</th></tr></thead><tbody>${rows}</tbody></table></div><div class="pptModuleTitle configTitle"><span>${escapeHtml(copy.configurationTitle)}</span>${sourceBadge(60)}</div><div class="configMatrix">${configRows}</div><div class="sourceDataGroups paperSourceGroups">${completeGroups}</div>`);
    return section;
  }

  function renderField(records, sourceVisuals) {
    const section = makeSection('ppt-field', copy.fieldTitle, copy.fieldSubtitle);
    const counts = records.reduce((result, record) => { const key = findingKey(record.finding_status); result[key] = (result[key] || 0) + 1; return result; }, {});
    const summary = ['advantage', 'gap', 'pending', 'missing'].map((key) => `<span class="status-${key}"><b>${counts[key] || 0}</b>${escapeHtml(copy[key])}</span>`).join('');
    const rows = records.map((record) => {
      const key = findingKey(record.finding_status);
      return `<tr><td>${escapeHtml(fieldGroup(record.metric))}</td><td><b>${escapeHtml(text(fieldMetricNames[record.metric]) || record.metric)}</b></td><td>${escapeHtml(narrative(record.conclusion))}</td><td><span class="scenarioStatus status-${key}">${escapeHtml(copy[key])}</span></td><td><span class="validationText">${escapeHtml(text(validationLabels[record.validation_status]))}</span></td></tr>`;
    }).join('');
    const themes = `<div class="fieldThemeGrid">${fieldThemes.map((item) => `<article class="tone-${item.tone}"><span>${escapeHtml(text(item.title))}</span><p>${escapeHtml(text(item.detail))}</p></article>`).join('')}</div>`;
    const completeGroups = expanded.fieldGroups.map((group) => renderSourceDataGroup(group, 'field')).join('');
    section.insertAdjacentHTML('beforeend', `<p class="analysisScope">${escapeHtml(copy.fieldBoundary)}</p><div class="fieldSummary">${summary}</div><div class="pptModuleTitle"><span>${escapeHtml(copy.fieldRead)}</span>${sourceBadge([62, 63, 64, 65, 66])}</div>${themes}${renderCompetitivenessProfile(sourceVisuals?.competitiveness_profile)}${renderFieldHeatmap(sourceVisuals?.field_rating_heatmap)}<div class="pptModuleTitle directDataTitle"><span>${escapeHtml(copy.fullField)}</span>${sourceBadge([62, 63, 64, 65, 66])}</div><div class="fieldMatrix"><table><thead><tr><th>${escapeHtml(copy.dimension)}</th><th>${escapeHtml(copy.metric)}</th><th>${escapeHtml(copy.conclusion)}</th><th>${escapeHtml(copy.status)}</th><th>${escapeHtml(copy.validation)}</th></tr></thead><tbody>${rows}</tbody></table></div><p class="historicalRatingNote">${escapeHtml(copy.historicalRatingNote)}</p><div class="sourceDataGroups fieldSourceGroups">${completeGroups}</div>`);
    return section;
  }

  function renderActions(roadmap, portfolio, sourceVisuals) {
    const section = makeSection('ppt-actions', copy.actionTitle, copy.actionSubtitle);
    const rows = roadmap.map((record) => `<div class="roadmapRow" data-priority="${escapeHtml(record.priority)}"><span class="roadmapPriority">${escapeHtml(record.priority)}</span><span class="roadmapTopic">${escapeHtml(text(roadmapTopics[record.id]) || record.id)}</span><span class="roadmapAction">${escapeHtml(narrative(record.action))}</span><span class="roadmapValidation">${escapeHtml(copy.verifyRequired)}</span></div>`).join('');
    const portfolioGap = portfolio.find((record) => record.id === 'portfolio-current-gap');
    const phases = `<div class="actionPhaseGrid">${actionPhases.map((phase, index) => `<article><span>${escapeHtml([copy.phaseNow, copy.phaseNext, copy.phasePlatform][index])}</span><h3>${escapeHtml(text(phase.title))}</h3><ul>${(phase.items[language] || phase.items.zh).map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul></article>`).join('')}</div>`;
    const dimensionRows = expanded.competitionDimensions.map((item) => `<tr><th scope="row">${escapeHtml(text(item.dimension))}</th><td>${escapeHtml(text(item.strength))}</td><td>${escapeHtml(text(item.gap))}</td><td>${escapeHtml(text(item.action))}</td></tr>`).join('');
    section.insertAdjacentHTML('beforeend', `<p class="analysisScope">${escapeHtml(copy.actionBoundary)}</p><div class="pptModuleTitle"><span>${escapeHtml(copy.competitionDetail)}</span>${sourceBadge(67)}</div><div class="competitionGapMatrix"><table><thead><tr><th>${escapeHtml(copy.dimension)}</th><th>${escapeHtml(copy.strengthColumn)}</th><th>${escapeHtml(copy.gapColumn)}</th><th>${escapeHtml(copy.actionColumn)}</th></tr></thead><tbody>${dimensionRows}</tbody></table></div>${renderImprovementLedger(sourceVisuals?.historical_improvement_ledger)}${phases}<div class="roadmapTable">${rows}</div><div class="portfolioNote"><div><b>${escapeHtml(copy.portfolio)}</b><p>${escapeHtml(narrative(portfolioGap?.conclusion))}</p></div><div><b>${escapeHtml(copy.historicalPositioning)}</b><p>${language === 'en' ? 'Revalidate target price, channel support, residual value and current product status before using the historical value-positioning claim.' : '历史材料中的价值型定位、价格主张和产品状态必须结合当前售价、渠道支持、残值与量产配置重新评估。'}</p></div></div>`);
    return section;
  }

  async function loadData() {
    const names = ['tonnage-3-4t-view', 'tonnage', 'field-evaluation', 'roadmap', 'portfolio', 'visual-assets', 'source-visuals-3-4t'];
    const values = await Promise.all(names.map(async (name) => {
      const response = await fetch(`data/ppt-insights/${name}.json`);
      if (!response.ok) throw new Error(`${name}: ${response.status}`);
      return response.json();
    }));
    return {tonnage34tView: values[0], tonnage: values[1], fieldEvaluation: values[2], roadmap: values[3], portfolio: values[4], visualAssets: values[5], sourceVisuals: values[6]};
  }

  async function init() {
    if (!document.body.classList.contains('pptIntegratedDemo')) return;
    const navLabels = {market: copy.navMarket, scenarios: copy.navScenarios, paper: copy.navPaper, field: copy.navField, actions: copy.navActions};
    document.querySelectorAll('[data-ppt-nav]').forEach((link) => { link.textContent = navLabels[link.dataset.pptNav] || link.textContent; });
    try {
      state = await loadData();
      const eyebrow = document.querySelector('.hero .eyebrow');
      if (eyebrow) eyebrow.textContent = copy.internal;
      document.querySelector('#summary')?.after(renderMarket(state.tonnage34tView, state.sourceVisuals));
      const scenarios = renderScenarios(state.tonnage.records.filter((record) => record.id.startsWith('scenario-')));
      const paper = renderPaper(state.tonnage34tView, state.sourceVisuals);
      document.querySelector('#conditions')?.after(scenarios, paper);
      document.querySelector('#cond6')?.after(renderField(state.fieldEvaluation.records, state.sourceVisuals), renderActions(state.roadmap.records, state.portfolio.records, state.sourceVisuals));
      window.XCMGPPTIntegration = {language, data: state};
    } catch (error) {
      const section = makeSection('ppt-load-error', copy.marketTitle, '');
      section.innerHTML += `<p class="scopeBoundary">${escapeHtml(copy.loadError)}</p>`;
      document.querySelector('#summary')?.after(section);
      console.error(error);
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once: true}); else init();
})();
