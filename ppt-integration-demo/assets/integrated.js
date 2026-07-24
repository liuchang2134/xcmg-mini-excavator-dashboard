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
      internal: 'XCMG ARC 产品对标',
      marketTitle: '市场、客户与运输适配',
      marketSubtitle: '',
      scoringBoundary: '',
      volumeTitle: '3-4吨五品牌EDA样本变化', historical: '历史实绩', estimate: '报告原估计', forecast: '报告原预测', units: '台', basePeriod: '基期', yearOverYear: '同比',
      shareTitle: '四个领先品牌合计份额', shareNote: '久保田、约翰迪尔、山猫、卡特',
      customerTitle: '主要客户结构', purchaseLogic: '购买判断重点', transportTitle: '典型运输组合重量',
      portfolioTitle: '同吨级产品型谱覆盖', portfolioBrand: '品牌', portfolioCount: '主力机型数', portfolioArchitecture: '型谱结构', portfolioImplication: '竞争含义',
      transportRuleTitle: '运输与驾照边界', licenceClass: '许可类型', generalThreshold: '通用门槛', applicationImpact: '对3-4吨产品的影响', transportRuleCaveat: '州法规、商业用途、车辆额定值及组合总质量应按实际运输方案复核。',
      baseMass: '基础机', equippedMass: '典型配置后', marketRead: '市场判断',
      marketRole: '吨级角色', marketRoleText: '3-4吨是微小挖销量核心，也是租赁市场的高频规格。成熟品牌通常用短尾、常规尾和不同配置层级覆盖运输、狭窄施工与重载稳定需求。',
      competition: '竞争结构', competitionText: '久保田、约翰迪尔、山猫和卡特合计约占74%。竞争优势来自产品型谱、附件体系、渠道服务和残值，而不只是单项参数。',
      xcmgEntry: 'XCMG切入点', xcmgEntryText: 'XE35U需要优先处理整备后运输重量、行走速度、AUX流量、回填配置和驾驶舒适性，同时保留AUX2、斗杆力和起吊能力等可验证优势。',
      rightInsightTitle: '该吨级的购买逻辑',
      leadingModelsTitle: '主销机型锚点',
      leadingModelsText: '2025 年 3-4 吨主销机型集中在 Deere 35P、Bobcat E35、Kubota U35、CAT 303.5 CR 与 Kubota KX033。客户并非只买低价，而是在短尾、租赁保有量、属具适配、服务网络和残值之间做综合判断。',
      transportFitTitle: '运输约束不是附属条件',
      transportFitText: '该吨级常被皮卡和14K拖车跨工地转运。基础机重量、快换、拇指钳、副配重和铲斗必须按整备组合核算；一旦压缩有效载荷余量，客户会转向更轻或配置分层更清晰的竞品。',
      productFitTitle: '对 XCMG 的产品含义',
      productFitText: 'XE35U 的切入点应放在“短尾+多属具+可运输”的组合价值上。优先验证运输重量、AUX1流量、行走速度、推土铲浮动和驾驶室舒适性，避免只用挖掘深度或单项力值解释竞争力。',
      transportStoryTitle: '运输边界直接影响成交和跨工地周转',
      transportStoryText: '现款基础机重量为4,200 kg；加副配重、快换、拇指钳和标准斗后约4,579 kg。该组合会明显压缩皮卡与14K拖车的有效载荷余量，牵引车、拖车额定值、组合总质量和驾驶许可必须按具体方案核验。',
      transportPayloadWindow: '14K拖车常见有效载荷', transportCurrentPackage: 'XE35U常用配置后', transportHistoricalPackage: 'XE35U PRO方案', transportMargin: '相对载荷下限余量',
      transportMarginNote: '负值表示设备组合已超过常见有效载荷区间下限。', transportDecisionTitle: '运输判断', transportDecisionText: '现款常用组合已越过常见载荷区间下限，PRO方案可恢复一定余量。实际运输仍须复核拖车铭牌、牵引车额定值、组合总质量和驾驶许可。',
      transportCaptionA: '轻型皮卡与14K拖车是该吨级常见转运组合', transportCaptionB: '竞品35G装车状态：整机与附件共同占用有效载荷',
      scenarioTitle: '真实作业场景', scenarioSubtitle: '把现场任务、客户要求和产品差距直接连接到现有量化工况。',
      customer: '主要客户', needs: '作业要求', steps: '任务链', finding: '当前判断', scenarioIndex: '八类场景快速对照', workObjects: '作业对象', operatingCharacteristics: '作业特点', historicalAssessment: '产品适应性判断', historicalAssessmentNote: '',
      workCondition: '作业场景', keyFinding: '关键差距', status: '工程判断', parameterImpact: '关键参数差距', configurationImpact: '关键配置作用', engineeringAction: '产品动作',
      scenarioRequirement: '客户任务', currentFit: '当前产品适配', productAction: '验证与产品动作', covered: '已具备基础', mixed: '部分满足，仍有缺口', linkedConditions: '关联量化工况',
      paperTitle: '纸面竞争力复核', paperSubtitle: '把尺寸、作业能力、液压和属具配置放回具体应用中解释。',
      paperBoundary: '该矩阵补充现有Excel评分，不重复计分；不同版本数据冲突时，以当前机型实测和最新配置清单为准。',
      fullPaper: '关键参数对比矩阵', metric: '指标', findingColumn: '对工况的影响', configurationTitle: '关键配置差异',
      paperRead: '参数与配置结论', xcmgState: 'XCMG状态', comparison: '竞品差异与工况影响',
      dataConflictTitle: '当前数据与历史口径差异', currentDataset: '当前 Excel', historicalReference: '历史研究口径', handlingRule: '处理方式', conflictRule: '评分继续使用当前 Excel；历史值仅用于追溯，完成版本和测试条件核验后再统一。',
      completePaperData: '完整参数与配置明细', sourceCategory: '类别', sourceSystem: '系统', sourcePriority: '关注度', sourceUnit: '单位',
      fieldTitle: '实机评价', fieldSubtitle: '将操控、舒适性、可靠性和维修性与纸面参数分开呈现。',
      fieldBoundary: '没有统一工况下的当前量化试验时，只标记优势、差距或待验证，不生成新分数。',
      fullField: '实机评价矩阵', dimension: '维度', conclusion: '工程判断', validation: '验证要求',
      advantage: '优势', gap: '已识别具体差距', pending: '待实机验证', missing: '暂无评价', fieldRead: '实机评价重点',
      completeFieldData: '实机评价明细', historicalRatingNote: '',
      ratingRuleTitle: '评分口径', ratingScaleTitle: '等级方向', ratingScaleText: '采用1–5级，数值越高表示该项评价越强；2–4级尚无统一量化阈值。',
      ratingAverageTitle: '分组算法', ratingAverageText: '同一维度内各指标等权平均，保留1位小数，不增加额外主观权重。',
      ratingVisualTitle: '图形与状态', ratingVisualText: '数字为分组均值；条形相对本行最高值；优势、差距和待验证为记录条数。',
      ratingBoundaryTitle: '使用边界', ratingBoundaryText: '仅用于定位实机差异，不并入参数分、配置分、工况分或综合评分。',
      actionTitle: 'XCMG产品改进路径', actionSubtitle: '把市场、参数和实机差距转化为系统级工程任务。',
      actionBoundary: '以下为建议动作和验证任务，不代表已经立项、完成或承诺时间。',
      priority: '优先级', topic: '改进主题', action: '工程动作', validationState: '验证状态',
      verifyRequired: '需工程、试验与市场共同验证', portfolio: '型谱差距', historicalPositioning: '市场定位',
      competitionDetail: '九个维度的具体差距与动作', strengthColumn: '已有基础', gapColumn: '具体差距', actionColumn: '弥补动作',
      actionRuleTitle: '判断口径', actionRuleValue: '不设置总分', actionRuleText: '依据可核验参数、配置状态和实机评价逐项判断；已有基础、具体差距与弥补动作之间一一对应，建议动作不代表已经立项或完成。',
      positioningTitle: '价格与市场份额定位', positioningBrand: '品牌', positioningModels: '代表机型', positioningPrice: '参考价格', positioningShare: '市场份额', positioningCaveat: '价格与份额按同一市场口径对比，并随渠道和产品状态更新。',
      positionSectionTitle: '产品定位与竞争主张', positionSectionSubtitle: '',
      positionHeadline: '低价切入尚未转化为市场份额，产品价值必须由运输适配、属具能力、操控品质和渠道支持共同支撑。',
      positionHistory: '历史定位', positionHistoryValue: '中质低价', positionPrice: '参考价格', positionPriceValue: '$54,000', positionPriceDetail: '较久保田 $60,000 参考价低 $6,000，按表内价格计算约低 10%。',
      positionShare: '历史份额记录', positionShareValue: '<1%', positionShareDetail: '低价并未自动形成份额，需同步补齐产品适应性、渠道和服务能力。',
      positionTarget: '2025历史目标', positionTargetValue: '194 台', positionTargetDetail: '属于历史销售目标，现有材料未提供实际完成结果。',
      positionPortfolio: '型谱缺口', positionPortfolioValue: '缺常规尾', positionPortfolioDetail: '当前以短尾机型切入，尚未形成与标杆同等的短尾、常规尾组合覆盖。',
      positionBoundary: '历史价格、份额和销售目标用于定位复盘，不与当前 Excel 综合评分合并；“低15%”的历史表述与表内 $54,000 对 $60,000 的约10%价差存在口径差异，正式决策前应统一报价时间、配置和渠道条件。',
      positionArchitectureTitle: '品牌型谱策略', positionDecisionTitle: '定位结论', profileBoundary: '维度画像沿用历史1–5级评价，只用于说明竞争结构，不并入当前参数分、配置分或总体评分。',
      navMarket: '市场与客户', navScenarios: '真实作业场景', navPaper: '参数与配置', navField: '实机评价', navPositioning: '产品定位', navActions: '改进路线',
      phaseNow: '优先验证', phaseNext: '系统改进', phasePlatform: '平台规划', validationOutput: '应形成的验证输出',
      sourcePpt: '', historicalBasis: '产品配置', currentUnverified: '状态待确认',
      year: '年份', total: '五品牌合计', dataStatus: '数据属性', sourceEstimate: '报告原估计（待实绩回填）', sourceForecast: '报告原预测（待实绩回填）',
      brandSalesTable: '品牌销量明细', modelDemandTitle: '主销机型排名', priceShareTitle: '价格与份额分布',
      priceAxis: '参考单价（万美元）', shareAxis: '市场份额（%）', sourceVolume: '销量',
      marketEvidenceTitle: '本吨级四个关键事实', topSellingModel: '主销机型', xcmgVolumeSignal: 'XCMG销量变化', xcmgPricePosition: '价格位置', transportRiskSignal: '运输余量',
      marketEvidenceNote: '',
      scenarioMatrixTitle: '八类真实工况矩阵', scenarioCustomerColumn: '客户与场景', scenarioEvidenceColumn: '作业内容', scenarioLinkColumn: '关联工况',
      fieldGroupTitle: '实机评价分组', fieldGroupNote: '',
      transportBreakdownTitle: '整机与附件重量构成', packageName: '运输组合', component: '构成项', weight: '重量', packageTotal: '组合总重', optionalAttachments: '可追加属具',
      performanceVisualTitle: '关键性能分项对比', performanceScaleNote: '', noSourceValue: '暂无数据',
      fieldHeatmapTitle: '实机评价热力矩阵', ratingLegend: '1级较弱，5级较强。',
      profileTitle: '竞争力维度画像', profileKey: '维度索引',
      ledgerTitle: 'XE35U问题与升级台账', ledgerCaveat: '',
      itemNo: '序号', system: '系统', problem: '现存问题', sourceAction: '升级方案', historicalUpgradeDate: '计划升级节点', historicalProductionDate: '计划量产节点',
      loadError: '分析数据载入失败。'
    },
    en: {
      internal: 'XCMG ARC PRODUCT BENCHMARKING',
      marketTitle: 'Market, Customer and Transport Fit',
      marketSubtitle: '',
      scoringBoundary: '',
      volumeTitle: '3-4 t five-brand EDA sample trend', historical: 'Historical actuals', estimate: 'Original report estimate', forecast: 'Original report forecast', units: 'units', basePeriod: 'Base period', yearOverYear: 'YoY',
      shareTitle: 'Combined share of four leading brands', shareNote: 'Kubota, John Deere, Bobcat and Caterpillar',
      customerTitle: 'Primary customer mix', purchaseLogic: 'Purchase priorities', transportTitle: 'Representative transport mass',
      portfolioTitle: 'Portfolio coverage within the class', portfolioBrand: 'Brand', portfolioCount: 'Core models', portfolioArchitecture: 'Portfolio structure', portfolioImplication: 'Competitive implication',
      transportRuleTitle: 'Transport and licence boundaries', licenceClass: 'Licence class', generalThreshold: 'General threshold', applicationImpact: 'Impact on the 3-4 t product', transportRuleCaveat: 'Check state law, commercial use, vehicle ratings and gross combination mass for the actual transport setup.',
      baseMass: 'Base machine', equippedMass: 'Representative equipped mass', marketRead: 'Market interpretation',
      marketRole: 'Role of the class', marketRoleText: 'The 3-4 t class is a compact-excavator volume center and a high-frequency rental size. Established brands use short-tail, conventional-tail and multiple trim levels to span transport, confined work and stability needs.',
      competition: 'Competitive structure', competitionText: 'Kubota, John Deere, Bobcat and Caterpillar account for about 74% combined. Advantage comes from portfolio breadth, attachments, channel support and residual value, not one specification.',
      xcmgEntry: 'XCMG opportunity', xcmgEntryText: 'XE35U priorities are equipped transport mass, travel speed, auxiliary flow, backfill equipment and cab comfort, while retaining validated strengths in AUX2 provision, arm force and lifting capability.',
      rightInsightTitle: 'How this class is purchased',
      leadingModelsTitle: 'Leading-model anchors',
      leadingModelsText: 'In 2025, demand in the 3-4 t class clusters around Deere 35P, Bobcat E35, Kubota U35, CAT 303.5 CR and Kubota KX033. Customers are not buying on price alone; they weigh tail architecture, rental availability, attachment fit, dealer support and residual value.',
      transportFitTitle: 'Transport is not a secondary issue',
      transportFitText: 'This class is frequently moved between jobsites by pickup and 14K trailer. Base machine, coupler, thumb, counterweight and buckets must be assessed as one transport package; once useful payload margin is compressed, customers shift toward lighter or better-tiered competitor offerings.',
      productFitTitle: 'Product implication for XCMG',
      productFitText: 'XE35U should be positioned around a “short-tail + multi-attachment + transportable” value proposition. Priorities are equipped mass, AUX1 flow, travel speed, blade float and cab comfort, rather than explaining competitiveness through digging depth or one force value alone.',
      transportStoryTitle: 'Transport limits directly affect purchase and jobsite mobility',
      transportStoryText: 'Base-machine mass is 4,200 kg; counterweight, coupler, thumb and standard bucket bring a representative combination to about 4,579 kg. This compresses useful payload margin on a pickup and 14K trailer, so tow rating, trailer rating, gross combination mass and licence requirements must be checked for each setup.',
      transportPayloadWindow: 'Typical effective payload of a 14K trailer', transportCurrentPackage: 'XE35U with common equipment', transportHistoricalPackage: 'XE35U PRO package', transportMargin: 'Margin to lower payload bound',
      transportMarginNote: 'A negative value means the machine package exceeds the lower end of the common effective-payload range.', transportDecisionTitle: 'Transport assessment', transportDecisionText: 'The current common package exceeds the lower end of the typical payload window, while the PRO package restores some margin. Verify the trailer data plate, tow-vehicle ratings, gross combination mass and licence requirement for the actual setup.',
      transportCaptionA: 'A light-duty pickup and 14K trailer are a common transport combination in this class', transportCaptionB: 'Competitor 35G loaded for transport: machine and equipment consume the same payload allowance',
      scenarioTitle: 'Real Job Applications', scenarioSubtitle: 'Connect field tasks and customer requirements directly to the existing quantified applications.',
      customer: 'Primary users', needs: 'Operating requirements', steps: 'Task sequence', finding: 'Current assessment', scenarioIndex: 'Eight-application comparison', workObjects: 'Work objects', operatingCharacteristics: 'Operating characteristics', historicalAssessment: 'Product application-fit assessment', historicalAssessmentNote: '',
      workCondition: 'Application', keyFinding: 'Principal gap', status: 'Engineering assessment', parameterImpact: 'Relevant specification gap', configurationImpact: 'Equipment effect', engineeringAction: 'Product action',
      scenarioRequirement: 'Customer task', currentFit: 'Current product fit', productAction: 'Validation and product action', covered: 'Baseline capability present', mixed: 'Partly met; gap remains', linkedConditions: 'Linked quantified applications',
      paperTitle: 'Paper Competitiveness Review', paperSubtitle: 'Interpret dimensions, working capability, hydraulics and equipment in the applications they affect.',
      paperBoundary: 'This matrix supplements the existing Excel score and is not scored again. Where versions conflict, use current-machine testing and the latest equipment list.',
      fullPaper: 'Key specification comparison', metric: 'Metric', findingColumn: 'Application effect', configurationTitle: 'Key equipment differences',
      paperRead: 'Specification and equipment conclusions', xcmgState: 'XCMG status', comparison: 'Competitive difference and application effect',
      dataConflictTitle: 'Current data versus historical basis', currentDataset: 'Current Excel', historicalReference: 'Historical research basis', handlingRule: 'Treatment', conflictRule: 'Scores continue to use the current Excel. Historical values remain traceable until version and test-condition checks are complete.',
      completePaperData: 'Complete specification and equipment detail', sourceCategory: 'Category', sourceSystem: 'System', sourcePriority: 'Priority', sourceUnit: 'Unit',
      fieldTitle: 'Field Evaluation', fieldSubtitle: 'Keep control, comfort, reliability and serviceability separate from paper specifications.',
      fieldBoundary: 'Where no current quantified common-condition test exists, use Advantage, Gap or Pending Validation rather than creating a score.',
      fullField: 'Field-evaluation matrix', dimension: 'Dimension', conclusion: 'Engineering assessment', validation: 'Validation requirement',
      advantage: 'Advantage', gap: 'Specific gap identified', pending: 'Field validation required', missing: 'No evaluation', fieldRead: 'Field-evaluation priorities',
      completeFieldData: 'Field-evaluation detail', historicalRatingNote: '',
      ratingRuleTitle: 'Rating Method', ratingScaleTitle: 'Scale direction', ratingScaleText: 'Uses a 1–5 scale; higher values indicate stronger performance. Levels 2–4 do not yet have uniform quantitative thresholds.',
      ratingAverageTitle: 'Group calculation', ratingAverageText: 'Metrics within each dimension receive equal weight and are averaged to one decimal place, with no added subjective weighting.',
      ratingVisualTitle: 'Bars and status', ratingVisualText: 'Numbers are group means; bars are relative to the row leader; Advantage, Gap and Pending are record counts.',
      ratingBoundaryTitle: 'Use boundary', ratingBoundaryText: 'Used only to locate field-performance differences; excluded from specification, equipment, work-condition and overall scores.',
      actionTitle: 'XCMG Product Improvement Path', actionSubtitle: 'Translate market, specification and field gaps into system-level engineering work.',
      actionBoundary: 'The items below are recommendations and validation tasks, not evidence of approval, completion or committed timing.',
      priority: 'Priority', topic: 'Improvement topic', action: 'Engineering action', validationState: 'Validation status',
      verifyRequired: 'Joint engineering, test and market validation required', portfolio: 'Portfolio gap', historicalPositioning: 'Market position',
      competitionDetail: 'Concrete gaps and actions across nine dimensions', strengthColumn: 'Existing foundation', gapColumn: 'Specific gap', actionColumn: 'Closing action',
      actionRuleTitle: 'Assessment Method', actionRuleValue: 'No aggregate score', actionRuleText: 'Each item is assessed from verifiable specifications, equipment status and field evaluation. Existing foundation, specific gap and closing action map one to one; recommendations do not imply approval or completion.',
      positioningTitle: 'Price and market-share position', positioningBrand: 'Brand', positioningModels: 'Representative models', positioningPrice: 'Reference price', positioningShare: 'Market share', positioningCaveat: 'Compare price and share on a consistent market basis and update them as channel and product status changes.',
      positionSectionTitle: 'Product Positioning and Competitive Proposition', positionSectionSubtitle: '',
      positionHeadline: 'A lower entry price has not yet translated into share; transport fit, attachment capability, control quality and channel support must carry the value proposition together.',
      positionHistory: 'Historical position', positionHistoryValue: 'Mid-quality, value price', positionPrice: 'Reference price', positionPriceValue: '$54,000', positionPriceDetail: '$6,000 below the $60,000 Kubota reference, or about 10% on the table values.',
      positionShare: 'Historical share record', positionShareValue: '<1%', positionShareDetail: 'A lower price did not automatically create share; product fit, channel and service capability must improve together.',
      positionTarget: 'Historical 2025 target', positionTargetValue: '194 units', positionTargetDetail: 'This is a historical sales target; the available material does not provide the actual result.',
      positionPortfolio: 'Portfolio gap', positionPortfolioValue: 'No conventional-tail model', positionPortfolioDetail: 'The current offer enters with a short-tail model without the short-tail and conventional-tail coverage of the benchmark portfolio.',
      positionBoundary: 'Historical price, share and sales targets are used for positioning review and are not merged into the current Excel overall score. The historical “15% lower” statement conflicts with the roughly 10% difference between $54,000 and $60,000; align quote date, equipment and channel conditions before a decision.',
      positionArchitectureTitle: 'Brand portfolio strategy', positionDecisionTitle: 'Positioning conclusion', profileBoundary: 'The profile retains the historical 1–5 assessment and is used only to explain competitive structure. It is excluded from the current specification, equipment and overall scores.',
      navMarket: 'Market and customers', navScenarios: 'Real job applications', navPaper: 'Specifications and equipment', navField: 'Field evaluation', navPositioning: 'Product positioning', navActions: 'Improvement path',
      phaseNow: 'Validate first', phaseNext: 'System improvements', phasePlatform: 'Platform planning', validationOutput: 'Required validation output',
      sourcePpt: '', historicalBasis: 'Product configuration', currentUnverified: 'Status to be confirmed',
      year: 'Year', total: 'Five-brand total', dataStatus: 'Data status', sourceEstimate: 'Original estimate (actual pending)', sourceForecast: 'Original forecast (actual pending)',
      brandSalesTable: 'Brand-volume detail', modelDemandTitle: 'Leading-model ranking', priceShareTitle: 'Price and share distribution',
      priceAxis: 'Reference price (USD 10k)', shareAxis: 'Market share (%)', sourceVolume: 'Sales volume',
      marketEvidenceTitle: 'Four facts to read first', topSellingModel: 'Top-selling model', xcmgVolumeSignal: 'XCMG volume trend', xcmgPricePosition: 'Price position', transportRiskSignal: 'Transport margin',
      marketEvidenceNote: '',
      scenarioMatrixTitle: 'Eight real-application matrix', scenarioCustomerColumn: 'Customer and application', scenarioEvidenceColumn: 'Application detail', scenarioLinkColumn: 'Related conditions',
      fieldGroupTitle: 'Field-evaluation groups', fieldGroupNote: '',
      transportBreakdownTitle: 'Machine and attachment mass build-up', packageName: 'Transport package', component: 'Component', weight: 'Mass', packageTotal: 'Package total', optionalAttachments: 'Additional attachments',
      performanceVisualTitle: 'Key performance comparisons', performanceScaleNote: '', noSourceValue: 'No data',
      fieldHeatmapTitle: 'Field-evaluation heatmap', ratingLegend: '1 is weaker and 5 is stronger.',
      profileTitle: 'Competitiveness profile', profileKey: 'Dimension key',
      ledgerTitle: 'XE35U issue and upgrade ledger', ledgerCaveat: '',
      itemNo: 'No.', system: 'System', problem: 'Current issue', sourceAction: 'Upgrade action', historicalUpgradeDate: 'Planned upgrade milestone', historicalProductionDate: 'Planned production milestone',
      loadError: 'Analysis data failed to load.'
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
    sales_service_documentation: {zh: '销售与售后文档', en: 'Sales and service documentation'}
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
    {tone: 'advantage', title: {zh: '经济性潜力', en: 'Operating-economy potential'}, detail: {zh: '燃油经济性具备优势潜力；销售论证前仍需在统一属具、负载和循环条件下完成实测。', en: 'Fuel economy shows advantage potential; a common attachment, load and duty-cycle test is still required before a sales claim is made.'}}
  ];

  const actionPhases = [
    {title: {zh: '验证基线', en: 'Validation baseline'}, items: {zh: ['整备组合称重与拖车余量', '行走速度、循环时间与油耗', 'AUX流量、压力、背压和热平衡', '机手盲评与操控数据'], en: ['Equipped-combination mass and trailer margin', 'Travel speed, cycle time and fuel use', 'Auxiliary flow, pressure, back pressure and thermal balance', 'Operator blind evaluation and control data']}},
    {title: {zh: '系统改进', en: 'System improvements'}, items: {zh: ['行走系统匹配', '回转与工作装置标定', '推土铲浮动与偏摆', '驾驶室、人机与维修可达性'], en: ['Travel-system matching', 'Swing and implement calibration', 'Blade float and angling', 'Cab, ergonomics and service access']}},
    {title: {zh: '平台规划', en: 'Platform planning'}, items: {zh: ['短尾与常规尾组合', '北美属具与配置包', '耐久、涂层和资料标准', '价格、渠道和残值闭环'], en: ['Short-tail and conventional-tail portfolio', 'North American attachment packages', 'Durability, coating and documentation standards', 'Price, channel and residual-value loop']}}
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
      ? [
          [/Slides?\s+\d+(?:\s*[–—-]\s*\d+)?\s+(?:describe|states?|records?|shows?)/gi, ''],
          [/The PPT rates (.+?) as (.+)/gi, '$1 is $2'], [/The PPT positions (.+?) as (.+)/gi, '$1 is positioned as $2'],
          [/The PPT shows one XCMG short-tail model in the class/gi, 'XCMG has one short-tail model in the class'],
          [/The PPT provides no /gi, 'No '], [/The PPT mentions /gi, 'The product plan includes '],
          [/The PPT/gi, ''], [/the PPT/gi, ''], [/PPT basis/gi, ''], [/PPT/gi, ''],
          [/The source explicitly assesses (.+?) as (.+)/gi, '$1 is $2'], [/The source assesses (.+?) as (.+)/gi, '$1 is $2'],
          [/The source considers (.+?) (broadly .+)/gi, '$1 is $2'], [/The source explicitly identifies /gi, ''],
          [/The source-level conclusion also identifies /gi, ''], [/The source states that /gi, ''], [/The source calls for /gi, 'The product requires '],
          [/The source records no /gi, 'The current configuration has no '], [/The source records missing /gi, 'The current configuration has no '],
          [/the source records only /gi, 'only '], [/the source records /gi, ''], [/The source lists /gi, ''], [/The source rates /gi, ''],
          [/Market feedback in the source identifies /gi, 'Market feedback identifies '],
          [/The source file/gi, ''], [/the source file/gi, ''], [/The source/gi, ''], [/the source/gi, ''],
          [/source basis/gi, ''], [/source-presentation/gi, ''], [/source-period/gi, ''], [/source estimate/gi, 'estimate'], [/source forecast/gi, 'forecast'], [/source target/gi, 'target'],
          [/historical XE35U PRO proposal/gi, 'XE35U PRO package'], [/historical PRO proposal/gi, 'PRO package'],
          [/historical source material/gi, ''], [/historical material/gi, ''], [/historical evaluation/gi, 'field performance'], [/historical proposal/gi, 'proposal'],
          [/historical plan/gi, 'plan'], [/historical record/gi, ''], [/historical sample/gi, 'sample'],
          [/recorded base-machine mass/gi, 'base-machine mass'], [/the material requires/gi, 'the product requires'], [/the material recommends/gi, 'the recommended action is'],
          [/the material explicitly concludes/gi, ''], [/the material concludes/gi, ''], [/according to the material/gi, ''],
          [/These transport and licence statements reflect the\s+basis\.?/gi, ''],
          [/and records that alarm muting was not equipped at that time/gi, '; alarm muting is not equipped'],
          [/and records missing alarm muting/gi, '; alarm muting is not equipped']
        ]
      : [
          [/第\d+(?:\s*[–—-]\s*\d+)?页(?:又)?(?:称|显示|记录|指出)?/g, ''],
          [/PPT口径/g, ''], [/PPT显示/g, ''], [/PPT列出的/g, ''], [/PPT未列出/g, '尚未配置'], [/PPT未给出/g, '尚无'],
          [/PPT提及/g, '方案包含'], [/PPT建议/g, '建议'], [/PPT将/g, ''], [/PPT/g, ''],
          [/源文件口径/g, ''], [/源文件中/g, ''], [/源文件记录/g, ''], [/源文件给出的/g, ''], [/源文件所述/g, ''], [/源文件估计/g, '估计'], [/源文件预测/g, '预测'], [/源文件/g, '数据'],
          [/以上运输和驾照判断为资料形成时口径[；;]?/g, ''], [/资料形成时口径/g, ''],
          [/历史材料未给出([^。；]+)[。；]?/g, '$1尚未明确。'], [/历史材料提供通用门槛/g, '通用门槛已经明确'], [/历史材料/g, ''], [/历史资料/g, ''],
          [/资料总体结论还指出/g, ''], [/资料明确判断/g, ''], [/资料建议/g, '建议'], [/资料要求/g, '需要'], [/资料指出/g, ''], [/资料表明/g, ''],
          [/资料认为/g, ''], [/资料称/g, ''], [/资料将/g, ''], [/资料记录/g, ''], [/资料中/g, ''], [/资料未配置/g, '未配置'], [/资料未覆盖/g, '暂无评价'],
          [/历史XE35U PRO方案/g, 'XE35U PRO方案'], [/历史PRO方案/g, 'PRO方案'], [/历史PRO驾驶(?:室)?空间改进/g, 'XE35U PRO驾驶室空间方案'], [/历史方案/g, '方案'], [/历史计划/g, '计划'],
          [/历史样机/g, '样机'], [/历史评价/g, '实机表现'], [/历史反馈/g, '反馈'], [/历史优势/g, '优势'], [/历史差距/g, '差距'],
          [/历史记录显示/g, ''], [/历史记录中/g, ''], [/历史记录/g, ''], [/历史口径/g, ''],
          [/PRO方案记录基础机/g, 'PRO方案基础机'], [/记录的地面3\s*m起吊力/g, '地面3 m起吊力'], [/记录的3\s*m起吊能力/g, '3 m起吊能力'],
          [/有优势记录/g, '表现较好'], [/被记录为/g, ''], [/记录较完整/g, '较完整'], [/在源页可比数据中/g, '在当前可比数据中'],
          [/XCMG为源页五款产品最高/g, 'XCMG在当前五款产品中最高'], [/优于源页久保田与三一配置/g, '优于久保田与三一的当前配置'],
          [/当时未配置蜂鸣器消音，后续仪表报警逻辑属于计划，当前状态待核/g, '蜂鸣器消音与仪表报警逻辑的当前状态待核'],
          [/当时蜂鸣器不具备消音功能，后续报警逻辑属于计划/g, '蜂鸣器消音与报警逻辑的当前状态待核'],
          [/蜂鸣器消音缺失，后续报警逻辑属于计划/g, '蜂鸣器消音与报警逻辑的当前状态待核'],
          [/并指出蜂鸣器消音当时未配置/g, '；蜂鸣器消音功能尚未确认'], [/并记录蜂鸣器消音缺失/g, '；蜂鸣器消音功能尚未确认'],
          [/资料与交付/g, '文档与交付'], [/销售与售后资料/g, '销售与售后文档'], [/售前售后资料/g, '售前售后文档'], [/资料种类/g, '文档种类'], [/资料标准/g, '文档标准']
        ];
    replacements.forEach(([pattern, replacement]) => { output = output.replace(pattern, replacement); });
    output = output
      .replace(/；\s*；/g, '；')
      .replace(/。\s*。/g, '。')
      .replace(/[（(]\s*[）)]/g, '')
      .replace(/\s{2,}/g, ' ')
      .replace(/^\s*[，,；;:：]\s*/u, '')
      .trim();
    if (language === 'en' && /^[a-z]/.test(output)) output = output.charAt(0).toUpperCase() + output.slice(1);
    return output;
  }

  function trimSentence(value) {
    return String(value || '').trim().replace(/[。；，、.!?;,:\s]+$/u, '');
  }

  function statementFromItems(items, separator) {
    const values = (items || []).map((item) => trimSentence(narrative(item))).filter(Boolean);
    if (!values.length) return '';
    const joiner = separator || (language === 'en' ? '; ' : '；');
    return `${values.join(joiner)}${language === 'en' ? '.' : '。'}`;
  }

  function workflowFromItems(items) {
    const values = (items || []).map((item) => trimSentence(narrative(item))).filter(Boolean);
    if (!values.length) return '';
    if (values.length === 1) return `${values[0]}${language === 'en' ? '.' : '。'}`;
    const first = values[0];
    const last = values[values.length - 1];
    const middle = values.slice(1, -1);
    if (language === 'en') {
      const middleText = middle.length ? `; then ${middle.join('; ')}` : '';
      return `First, ${first}${middleText}; finally, ${last}.`;
    }
    const middleText = middle.length ? `，随后依次完成${middle.join('、')}` : '';
    return `作业通常先进行${first}${middleText}，最后${last}。`;
  }

  function workObjectNarrative(items) {
    const values = (items || []).map((item) => trimSentence(narrative(item))).filter(Boolean);
    if (!values.length) return '';
    if (language === 'en') return `The primary work scope covers ${values.map((item) => item.charAt(0).toLowerCase() + item.slice(1)).join(', ')}.`;
    return `主要作业对象包括${values.join('、')}。`;
  }

  function historicalNarrative(items) {
    return (items || []).map((item) => {
      const value = narrative(item).trim();
      if (!value) return '';
      return /[。.!?]$/u.test(value) ? value : `${value}${language === 'en' ? '.' : '。'}`;
    }).filter(Boolean).join(language === 'en' ? ' ' : '');
  }

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }

  function findingKey(value) {
    if (value === '优势') return 'advantage';
    if (value === '差距') return 'gap';
    if (value === '资料未覆盖' || value === '暂无评价') return 'missing';
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
    const normalized = raw === '资料未配置'
      ? '未配置'
      : raw === '软文资料'
        ? '产品文档'
        : raw === '资料'
          ? '文档交付'
          : raw;
    if (language !== 'en' || !/[\u3400-\u9fff]/.test(normalized)) return narrative(normalized);
    if (normalized === '产品文档') return 'Product documentation';
    if (normalized === '文档交付') return 'Documentation delivery';
    if (expanded.translations[normalized]) return expanded.translations[normalized];
    let translated = normalized;
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
      const label = technicalText(narrative(value));
      const xcmgClass = /XE35U|XCMG/.test(label) ? ' class="xcmgSourceColumn"' : '';
      return `<th scope="col"${xcmgClass}>${escapeHtml(label)}</th>`;
    }).join('');
    const rowHeaderIndex = kind === 'paper' ? 1 : 2;
    const rows = normalized.rows.map((row) => `<tr>${row.map((value, index) => {
      const tag = index === rowHeaderIndex ? 'th' : 'td';
      const scope = index === rowHeaderIndex ? ' scope="row"' : '';
      const xcmgClass = /XE35U|XCMG/.test(normalized.headers[index]) ? ' class="xcmgSourceColumn"' : '';
      return `<${tag}${scope}${xcmgClass}>${escapeHtml(technicalText(narrative(value)))}</${tag}>`;
    }).join('')}</tr>`).join('');
    return `<article class="sourceDataGroup">
      <div class="sourceDataHeading"><h3>${escapeHtml(narrative(group.title))}</h3></div>
      <div class="sourceDataScroll"><table><caption class="srOnly">${escapeHtml(narrative(group.title))}</caption><thead><tr>${header}</tr></thead><tbody>${rows}</tbody></table></div>
    </article>`;
  }

  function fieldGroup(metric) {
    if (/safety/.test(metric)) return language === 'en' ? 'Safety' : '安全性';
    if (/corrosion|temperature/.test(metric)) return language === 'en' ? 'Reliability' : '可靠性';
    if (/travel|inching|grading/.test(metric)) return language === 'en' ? 'Control' : '操控性';
    if (/seat|hvac|space|hmi/.test(metric)) return language === 'en' ? 'Comfort' : '舒适性';
    return language === 'en' ? 'Service and economy' : '维修与经济性';
  }

  function makeSection(id, title, subtitle, sourceSlides = []) {
    const section = document.createElement('section');
    section.id = id;
    section.className = 'pptSection';
    if (sourceSlides.length) section.dataset.sourceSlides = sourceSlides.join(' ');
    section.innerHTML = `<h2>${escapeHtml(title)}</h2>`;
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
    return '';
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
      <header><div><h3>${escapeHtml(text(data.title))}</h3><p>${escapeHtml(text(data.subtitle))}</p></div></header>
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
    return `<article class="evidenceVisual modelDemandVisual"><header><div><h3>${escapeHtml(text(data.title))}</h3></div></header><div class="modelDemandChart">${rows}</div></article>`;
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
    const title = text(data.title);
    return `<article class="evidenceVisual priceShareVisual"><header><div><h3>${escapeHtml(title)}</h3></div></header><svg viewBox="0 0 700 300" role="img" aria-label="${escapeHtml(title)}" class="priceShareSvg"><g class="chartGrid">${yGrid}${xGrid}</g><line class="chartAxis" x1="${plot.left}" x2="${plot.left + plot.width}" y1="${plot.top + plot.height}" y2="${plot.top + plot.height}"></line><line class="chartAxis" x1="${plot.left}" x2="${plot.left}" y1="${plot.top}" y2="${plot.top + plot.height}"></line>${points}<text class="axisTitle" x="${plot.left + plot.width / 2}" y="294" text-anchor="middle">${escapeHtml(copy.priceAxis)}</text><text class="axisTitle" transform="translate(14 ${plot.top + plot.height / 2}) rotate(-90)" text-anchor="middle">${escapeHtml(copy.shareAxis)}</text></svg></article>`;
  }

  function renderMarketEvidenceSummary(sourceVisuals) {
    const market = sourceVisuals?.market;
    const modelDemand = market?.model_demand_2025;
    const brandSales = market?.annual_brand_sales;
    const priceShare = market?.brand_position_2025;
    if (!modelDemand || !brandSales || !priceShare) return '';
    const topModel = modelDemand.models[0];
    const xcmgSeries = brandSales.series.find((item) => item.brand === 'XCMG');
    const xcmg2025 = xcmgSeries?.values?.[2];
    const xcmg2026 = xcmgSeries?.values?.[3];
    const xcmgPoint = priceShare.points.find((item) => item.brand === 'XCMG');
    const kubotaPoint = priceShare.points.find((item) => item.brand === 'KUBOTA');
    const currentPackage = sourceVisuals?.transport?.packages?.find((item) => item.id === 'xe35u-current');
    const lowerPayload = sourceVisuals?.transport?.trailer_context?.effective_payload_kg?.[0];
    const margin = Number.isFinite(lowerPayload) && currentPackage ? lowerPayload - currentPackage.equipped_total_kg : null;
    const cards = [
      {
        label: language === 'en' ? '2025 demand anchor in the study' : '研究口径的2025主销锚点',
        value: `${topModel.brand} ${topModel.model}`,
        detail: language === 'en' ? `${formatNumber(topModel.units)} units in the study dataset; used to identify the mainstream package.` : `研究样本销量${formatNumber(topModel.units)}台，用于识别主流产品组合。`
      },
      {
        label: language === 'en' ? 'XCMG planning signal, not actual sales' : 'XCMG规划信号，并非实绩',
        value: `${formatNumber(xcmg2025)} → ${formatNumber(xcmg2026)} ${copy.units}`,
        detail: language === 'en' ? 'Original 2025 estimate to 2026 forecast; current actuals still require backfill.' : '报告原2025估计到2026预测，当前实绩仍需回填。'
      },
      {
        label: language === 'en' ? 'Reference price position' : '参考价格位置',
        value: `$${formatNumber(xcmgPoint.price_usd)}`,
        detail: kubotaPoint ? (language === 'en' ? `About $${formatNumber(kubotaPoint.price_usd - xcmgPoint.price_usd)} below the Kubota reference; align quote date and equipment.` : `较久保田参考低约$${formatNumber(kubotaPoint.price_usd - xcmgPoint.price_usd)}，需统一报价时间与配置。`) : ''
      },
      {
        label: language === 'en' ? '14K trailer lower-bound fit' : '14K拖车常见载荷下限适配',
        value: margin == null ? '-' : `${margin > 0 ? '+' : ''}${formatNumber(margin)} kg`,
        detail: margin == null ? '' : (language === 'en' ? 'Representative equipped package versus the lower end of the common payload range; verify the actual combination.' : '常用配置组合相对常见有效载荷区间下限，实际组合仍须复核。')
      }
    ];
    return `<div class="marketEvidenceSummary"><div class="pptModuleTitle"><span>${escapeHtml(copy.marketEvidenceTitle)}</span></div><div class="marketEvidenceCards">${cards.map((item) => `<article><span>${escapeHtml(item.label)}</span><b>${escapeHtml(item.value)}</b><small>${escapeHtml(item.detail)}</small></article>`).join('')}</div></div>`;
  }

  function renderTransportBreakdown(data) {
    if (!data) return '';
    const max = 5000;
    const colors = ['#005aa7', '#f5b400', '#829bb2', '#0f7b45'];
    const packageRows = data.packages.map((item) => {
      const segments = item.components.map((component, index) => `<span style="width:${(component.kg / max * 100).toFixed(2)}%;background:${colors[index]}" title="${escapeHtml(text(component.label))} · ${formatNumber(component.kg)} kg"></span>`).join('');
      return `<div class="massPackageRow"><div><b>${escapeHtml(narrative(item.label))}</b><small>${item.status === 'historical_plan_unverified' ? escapeHtml(copy.currentUnverified) : escapeHtml(copy.historicalBasis)}</small></div><div class="massTrack">${segments}</div><strong>${formatNumber(item.equipped_total_kg)} kg</strong></div>`;
    }).join('');
    const componentRows = data.packages.map((item) => `<tr><th scope="row">${escapeHtml(narrative(item.label))}</th><td>${item.components.map((component) => `${escapeHtml(text(component.label))} ${formatNumber(component.kg)} kg`).join(' + ')}</td><td><b>${formatNumber(item.equipped_total_kg)} kg</b></td></tr>`).join('');
    const optional = data.additional_attachments.map((item) => `<li><span>${escapeHtml(text(item.label))}</span><b>${formatNumber(item.kg)} kg</b></li>`).join('');
    const subtitle = narrative(data.subtitle);
    return `<article class="evidenceVisual transportBreakdownVisual"><header><div><h3>${escapeHtml(narrative(data.title))}</h3>${subtitle ? `<p>${escapeHtml(subtitle)}</p>` : ''}</div></header><div class="massPackageChart">${packageRows}</div><div class="massDetailGrid"><div class="evidenceTableScroll"><table><thead><tr><th>${escapeHtml(copy.packageName)}</th><th>${escapeHtml(copy.component)}</th><th>${escapeHtml(copy.packageTotal)}</th></tr></thead><tbody>${componentRows}</tbody></table></div><div class="optionalAttachmentList"><h4>${escapeHtml(copy.optionalAttachments)}</h4><ul>${optional}</ul></div></div></article>`;
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
      const basis = metric.basis ? `<p>${escapeHtml(narrative(metric.basis))}</p>` : '';
      return `<article class="performanceFacet"><h4>${escapeHtml(text(metric.label))}<small>${escapeHtml(metric.unit)}</small></h4>${rows}${basis}</article>`;
    }).join('');
    return `<article class="evidenceVisual performanceEvidence"><header><div><h3>${escapeHtml(narrative(data.title))}</h3></div></header><div class="performanceFacetGrid">${cards}</div></article>`;
  }

  function renderFieldHeatmap(data) {
    if (!data) return '';
    let lastGroup = '';
    const rows = data.rows.map((item) => {
      const group = technicalText(text(item.group));
      const groupCell = group === lastGroup ? '' : group;
      lastGroup = group;
      return `<tr><th scope="row">${escapeHtml(groupCell)}</th><td>${escapeHtml(text(item.metric))}</td>${item.ratings.map((rating) => `<td class="ratingCell" data-rating="${rating}" title="${escapeHtml(text(item.metric))}: ${rating}/5"><b>${rating}</b></td>`).join('')}</tr>`;
    }).join('');
    return `<article class="evidenceVisual fieldHeatmapVisual"><header><div><h3>${escapeHtml(copy.fieldHeatmapTitle)}</h3></div></header><div class="heatmapLegend"><span>1</span><i data-rating="1"></i><i data-rating="2"></i><i data-rating="3"></i><i data-rating="4"></i><i data-rating="5"></i><span>5</span><b>${escapeHtml(copy.ratingLegend)}</b></div><div class="evidenceTableScroll"><table class="ratingHeatmap"><thead><tr><th>${escapeHtml(copy.dimension)}</th><th>${escapeHtml(copy.metric)}</th>${data.models.map((model, index) => `<th class="${index === 0 ? 'xcmgHeatHeader' : ''}">${escapeHtml(model)}</th>`).join('')}</tr></thead><tbody>${rows}</tbody></table></div></article>`;
  }

  function renderFieldGroupSummary(data) {
    if (!data?.rows?.length) return '';
    const groups = new Map();
    data.rows.forEach((row) => {
      const group = technicalText(text(row.group));
      if (!groups.has(group)) groups.set(group, {count: 0, sums: Array(data.models.length).fill(0)});
      const entry = groups.get(group);
      entry.count += 1;
      row.ratings.forEach((rating, index) => { entry.sums[index] += Number(rating) || 0; });
    });
    const rows = [...groups.entries()].map(([group, entry]) => {
      const averages = entry.sums.map((sum) => sum / entry.count);
      const best = Math.max(...averages);
      return `<tr><th scope="row">${escapeHtml(group)}</th>${averages.map((avg, index) => `<td class="${index === 0 ? 'xcmgFieldAvg' : ''}"><b>${avg.toFixed(1)}</b><i><em style="width:${(avg / best * 100).toFixed(1)}%"></em></i></td>`).join('')}</tr>`;
    }).join('');
    return `<article class="fieldGroupSummary"><div class="pptModuleTitle"><span>${escapeHtml(copy.fieldGroupTitle)}</span></div><div class="evidenceTableScroll"><table><thead><tr><th>${escapeHtml(copy.dimension)}</th>${data.models.map((model, index) => `<th class="${index === 0 ? 'xcmgHeatHeader' : ''}">${escapeHtml(model)}</th>`).join('')}</tr></thead><tbody>${rows}</tbody></table></div></article>`;
  }

  function renderScenarioMatrix(records) {
    if (!records?.length) return '';
    const sourceLine = (label, items, separator = language === 'en' ? '; ' : '；') => {
      const localized = items?.[language] || items?.zh || [];
      const values = Array.isArray(localized) ? localized : [localized];
      if (!values.length) return '';
      const content = values.map((item) => trimSentence(narrative(item))).filter(Boolean);
      if (!content.length) return '';
      return `<div class="sourceContentLine"><span>${escapeHtml(label)}</span><p>${content.map((item) => escapeHtml(item)).join(separator)}</p></div>`;
    };
    const rows = records.map((record) => {
      const links = (scenarioConditionLinks[record.id] || []).map((item) => `<a href="#${escapeHtml(item.id)}">${escapeHtml(language === 'en' ? item.en : item.zh)}</a>`).join('');
      const sourceContent = [
        sourceLine(copy.needs, record.needs),
        sourceLine(copy.steps, record.steps, language === 'en' ? ' -> ' : ' → '),
        sourceLine(copy.historicalAssessment, record.historical_assessment)
      ].filter(Boolean).join('');
      return `<tr>
        <th scope="row"><b>${escapeHtml(text(record.title))}</b><small>${escapeHtml(text(record.customer))}</small></th>
        <td class="scenarioSourceOriginal">${sourceContent}</td>
        <td><div class="scenarioConditionLinks matrixLinks">${links}</div></td>
      </tr>`;
    }).join('');
    return `<article class="scenarioMatrix">
      <header class="scenarioMatrixHeader"><h3>${escapeHtml(copy.scenarioMatrixTitle)}</h3></header>
      <div class="scenarioMatrixTable"><table><colgroup><col class="scenarioMatrixScenario"><col class="scenarioMatrixSourceContent"><col class="scenarioMatrixMapping"></colgroup><thead><tr><th>${escapeHtml(copy.scenarioCustomerColumn)}</th><th>${escapeHtml(copy.scenarioEvidenceColumn)}</th><th>${escapeHtml(copy.scenarioLinkColumn)}</th></tr></thead><tbody>${rows}</tbody></table></div>
    </article>`;
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
    return `<article class="evidenceVisual competitivenessProfile"><header><div><h3>${escapeHtml(copy.profileTitle)}</h3></div></header><div class="radarLayout"><div><svg viewBox="0 0 500 340" role="img" aria-label="${escapeHtml(copy.profileTitle)}" class="competitivenessRadar"><g class="radarGrid">${levels}${axes}</g>${series}</svg><div class="chartLegend radarLegend">${legend}</div></div><div class="radarKey"><h4>${escapeHtml(copy.profileKey)}</h4><ol>${keys}</ol></div></div></article>`;
  }

  function renderImprovementLedger(data) {
    if (!data) return '';
    const rows = data.items.map((item) => `<tr><td>${item.id}</td><th scope="row">${escapeHtml(text(item.system))}</th><td>${escapeHtml(text(item.problem))}</td><td>${escapeHtml(narrative(item.source_action))}</td><td>${escapeHtml(item.upgrade_date)}</td><td>${escapeHtml(item.production_date)}</td><td><span class="scenarioStatus status-pending">${escapeHtml(copy.currentUnverified)}</span></td></tr>`).join('');
    return `<article class="evidenceVisual improvementLedger"><header><div><h3>${escapeHtml(copy.ledgerTitle)}</h3></div></header><div class="evidenceTableScroll"><table><thead><tr><th>${escapeHtml(copy.itemNo)}</th><th>${escapeHtml(copy.system)}</th><th>${escapeHtml(copy.problem)}</th><th>${escapeHtml(copy.sourceAction)}</th><th>${escapeHtml(copy.historicalUpgradeDate)}</th><th>${escapeHtml(copy.historicalProductionDate)}</th><th>${escapeHtml(copy.status)}</th></tr></thead><tbody>${rows}</tbody></table></div></article>`;
  }

  function visualParagraphs(data) {
    const paragraphs = data?.paragraphs?.[language] || data?.paragraphs?.zh || [];
    return paragraphs.map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`).join('');
  }

  function renderVisualStory(data, visual, className = '') {
    if (!data) return '';
    return `<article class="decisionVisual ${escapeHtml(className)}">
      <header class="decisionVisualHeader"><span>${escapeHtml(text(data.title))}</span><h3>${escapeHtml(text(data.conclusion))}</h3></header>
      <div class="decisionVisualLayout">
        <div class="decisionVisualStage">${visual}</div>
        <div class="decisionVisualAnalysis">${visualParagraphs(data)}<div class="decisionAction"><b>${language === 'en' ? 'Product action' : '产品动作'}</b><p>${escapeHtml(text(data.action))}</p></div></div>
      </div>
    </article>`;
  }

  function renderCategoryContext(data) {
    if (!data) return '';
    const focus = `<div class="classFocusBanner"><span>${escapeHtml(text(data.focus.label))}</span><strong>${escapeHtml(data.focus.range)}</strong><b>${escapeHtml(text(data.focus.statement))}</b></div>`;
    const blocks = data.decision_blocks.map((item) => `<article class="classDecisionCard">
      <span>${escapeHtml(text(item.label))}</span>
      <h4>${escapeHtml(text(item.headline))}</h4>
      <p>${escapeHtml(text(item.detail))}</p>
    </article>`).join('');
    const benchmarks = data.benchmark_roles.map((item) => `<div class="benchmarkRole"><span>${escapeHtml(text(item.class))}</span><strong>${escapeHtml(text(item.brand))}</strong><p>${escapeHtml(text(item.reason))}</p></div>`).join('');
    return renderVisualStory(data, `${focus}<div class="classDecisionGrid">${blocks}</div><div class="benchmarkRoles">${benchmarks}</div>`, 'categoryContextVisual');
  }

  function renderPortfolioCoverage(data) {
    if (!data) return '';
    const headers = data.slots.map((slot) => `<th>${escapeHtml(text(slot.label))}</th>`).join('');
    const rows = data.rows.map((row) => {
      const cells = data.slots.map((slot) => {
        const model = row.coverage[slot.id];
        const missing = !model;
        return `<td class="${missing ? 'portfolioMissing' : 'portfolioCovered'}"><span>${missing ? (language === 'en' ? 'No dedicated product' : '无专属产品') : escapeHtml(text(model))}</span></td>`;
      }).join('');
      return `<tr class="${row.xcmg ? 'portfolioXcmg' : ''}"><th scope="row">${escapeHtml(row.brand)}</th>${cells}</tr>`;
    }).join('');
    const visual = `<div class="portfolioCoverageScroll"><table class="portfolioCoverageTable"><thead><tr><th>${language === 'en' ? 'Brand' : '品牌'}</th>${headers}</tr></thead><tbody>${rows}</tbody></table></div>`;
    return renderVisualStory(data, visual, 'portfolioCoverageVisual');
  }

  function renderTaskCapability(data, scenarioRecords) {
    if (!data) return '';
    const scenarioMap = new Map(scenarioRecords.map((record) => [record.id, record]));
    const tabs = data.records.map((record, index) => {
      const scenario = scenarioMap.get(record.scenario_id);
      return `<button type="button" class="capabilityTab${index === 0 ? ' is-active' : ''}" data-capability-target="capability-${escapeHtml(record.scenario_id)}" aria-pressed="${index === 0 ? 'true' : 'false'}">${escapeHtml(text(scenario?.title) || record.scenario_id)}</button>`;
    }).join('');
    const panels = data.records.map((record, index) => {
      const stages = [
        {label: language === 'en' ? 'Customer objective' : '客户目标', value: text(record.customer)},
        {label: language === 'en' ? 'Task sequence' : '任务步骤', value: text(record.task)},
        {label: language === 'en' ? 'Critical capability' : '关键能力', value: text(record.capability)},
        {label: language === 'en' ? 'Validation metric' : '验证指标', value: text(record.measure)}
      ];
      return `<div class="capabilityPanel${index === 0 ? ' is-active' : ''}" id="capability-${escapeHtml(record.scenario_id)}" ${index === 0 ? '' : 'hidden'}>${stages.map((stage, stageIndex) => `<article><span>${String(stageIndex + 1).padStart(2, '0')} · ${escapeHtml(stage.label)}</span><p>${escapeHtml(stage.value)}</p></article>`).join('')}</div>`;
    }).join('');
    return renderVisualStory(data, `<div class="capabilityExplorer"><div class="capabilityTabs" role="group">${tabs}</div>${panels}</div>`, 'taskCapabilityVisual');
  }

  function renderAttachmentHeatmap(data, scenarioRecords) {
    if (!data) return '';
    const scenarioMap = new Map(scenarioRecords.map((record) => [record.id, record]));
    const levelMap = new Map(data.legend.map((item) => [item.value, text(item.label)]));
    const legend = data.legend.map((item) => `<span><i class="attachmentHeat heat-${item.value}"></i>${escapeHtml(text(item.label))}</span>`).join('');
    const headers = data.attachments.map((item) => `<th><span>${escapeHtml(text(item.label))}</span></th>`).join('');
    const rows = data.rows.map((row) => {
      const scenario = scenarioMap.get(row.scenario_id);
      const cells = row.values.map((value) => `<td class="attachmentHeat heat-${value}" title="${escapeHtml(levelMap.get(value))}"><span>${value}</span><small>${escapeHtml(levelMap.get(value))}</small></td>`).join('');
      return `<tr><th scope="row">${escapeHtml(text(scenario?.title) || row.scenario_id)}</th>${cells}</tr>`;
    }).join('');
    const visual = `<div class="attachmentLegend">${legend}</div><div class="attachmentHeatmapScroll"><table class="attachmentHeatmap"><thead><tr><th>${language === 'en' ? 'Application' : '作业场景'}</th>${headers}</tr></thead><tbody>${rows}</tbody></table></div>`;
    return renderVisualStory(data, visual, 'attachmentMatrixVisual');
  }

  function formatDelta(metric) {
    const sign = metric.delta > 0 ? '+' : '';
    return `${sign}${formatMetricValue(metric.delta)} ${metric.unit}`;
  }

  function formatMetricValue(value) {
    const number = Number(value);
    if (!Number.isFinite(number)) return String(value);
    return number.toLocaleString(language === 'en' ? 'en-US' : 'zh-CN', {
      minimumFractionDigits: Number.isInteger(number) ? 0 : 1,
      maximumFractionDigits: 1
    });
  }

  function renderAbsoluteGaps(data) {
    if (!data) return '';
    const rows = data.metrics.map((metric) => {
      const ratio = Math.min(42, Math.max(4, Math.abs(metric.delta / metric.benchmark) * 130));
      const benchmarkDisplay = metric.benchmark_display || formatNumber(metric.benchmark);
      const side = metric.status === 'advantage' ? 'positive' : 'negative';
      return `<article class="gapMetricRow status-${escapeHtml(metric.status)}">
        <div class="gapMetricIdentity"><b>${escapeHtml(text(metric.label))}</b><span>${escapeHtml(metric.benchmark_model)}</span></div>
        <div class="gapMetricValues"><span><i>XCMG</i><b>${formatMetricValue(metric.xcmg)} ${escapeHtml(metric.unit)}</b></span><span><i>${language === 'en' ? 'Benchmark' : '标杆'}</i><b>${escapeHtml(metric.benchmark_display ? String(benchmarkDisplay) : formatMetricValue(metric.benchmark))} ${escapeHtml(metric.unit)}</b></span></div>
        <div class="gapDeltaChart"><div class="gapZero"></div><span class="gapDeltaBar ${side}" style="--gap-width:${ratio}%"></span><strong>${escapeHtml(formatDelta(metric))}</strong></div>
        <p>${escapeHtml(text(metric.impact))}</p>
      </article>`;
    }).join('');
    return renderVisualStory(data, `<div class="absoluteGapChart"><div class="gapAxis"><span>${language === 'en' ? 'Gap' : '短板'}</span><b>0</b><span>${language === 'en' ? 'Advantage' : '优势'}</span></div>${rows}</div>`, 'absoluteGapVisual');
  }

  function renderFieldEvidence(data) {
    if (!data) return '';
    const levelMap = new Map(data.levels.map((item) => [item.value, text(item.label)]));
    const legend = data.levels.map((item) => `<span><i class="evidenceLevel level-${item.value}"></i>${escapeHtml(text(item.label))}</span>`).join('');
    const headers = data.axes.map((axis) => `<th>${escapeHtml(text(axis.label))}</th>`).join('');
    const rows = data.rows.map((row) => `<tr><th scope="row">${escapeHtml(text(row.label))}</th>${row.values.map((value) => `<td class="evidenceLevel level-${value}"><b>${value}</b><span>${escapeHtml(levelMap.get(value))}</span></td>`).join('')}<td class="evidenceFinding">${escapeHtml(text(row.finding))}</td></tr>`).join('');
    const visual = `<div class="evidenceLevelLegend">${legend}</div><div class="fieldEvidenceScroll"><table class="fieldEvidenceTable"><thead><tr><th>${language === 'en' ? 'Dimension' : '维度'}</th>${headers}<th>${language === 'en' ? 'Current reading' : '当前判断'}</th></tr></thead><tbody>${rows}</tbody></table></div>`;
    return renderVisualStory(data, visual, 'fieldEvidenceVisual');
  }

  function renderClosureTimeline(data, ledger) {
    if (!data || !ledger) return '';
    const rows = ledger.items.map((item) => `<div class="closureRow">
      <div class="closureIdentity"><b>${item.id}. ${escapeHtml(text(item.system))}</b><span>${escapeHtml(text(item.problem))}</span></div>
      <div class="closureMilestone"><i class="milestoneDot historical"></i><span>${escapeHtml(item.upgrade_date)}</span></div>
      <div class="closureMilestone"><i class="milestoneDot historical"></i><span>${escapeHtml(item.production_date)}</span></div>
      <div class="closureMilestone current"><i class="milestoneDot pending"></i><span>${escapeHtml(copy.currentUnverified)}</span></div>
      <p>${escapeHtml(text(data.close_criteria[String(item.id)]))}</p>
    </div>`).join('');
    const phaseHeaders = data.phase_labels.map((phase) => `<span>${escapeHtml(text(phase.label))}</span>`).join('');
    const visual = `<div class="closureTimeline"><div class="closureTimelineHead"><span>${language === 'en' ? 'Issue / system' : '问题 / 系统'}</span>${phaseHeaders}<span>${language === 'en' ? 'Closure evidence' : '关闭证据'}</span></div>${rows}</div>`;
    return renderVisualStory(data, visual, 'closureTimelineVisual');
  }

  function initCapabilityExplorer(root = document) {
    root.querySelectorAll('.capabilityExplorer').forEach((explorer) => {
      explorer.querySelectorAll('.capabilityTab').forEach((button) => {
        button.addEventListener('click', () => {
          const target = button.dataset.capabilityTarget;
          explorer.querySelectorAll('.capabilityTab').forEach((item) => {
            const active = item === button;
            item.classList.toggle('is-active', active);
            item.setAttribute('aria-pressed', String(active));
          });
          explorer.querySelectorAll('.capabilityPanel').forEach((panel) => {
            const active = panel.id === target;
            panel.classList.toggle('is-active', active);
            panel.hidden = !active;
          });
        });
      });
    });
  }

  function renderMarket(view, sourceVisuals, visualExpansion) {
    const section = makeSection('ppt-market', copy.marketTitle, copy.marketSubtitle, [48, 49]);
    const customers = view.market.customer_mix.map((item) => `<span style="width:${item.value}%" title="${escapeHtml(text(item.label))} ${item.value}%"></span>`).join('');
    const customerLegend = view.market.customer_mix.map((item) => `<li><i></i><span>${escapeHtml(text(item.label))}</span><b>${item.value}%</b></li>`).join('');
    const logic = view.market.purchase_logic.map((item) => `<li>${escapeHtml(text(item))}</li>`).join('');
    const marketPoints = [
      {label: copy.marketRead, title: copy.marketRole, detail: copy.marketRoleText},
      {label: copy.marketRead, title: copy.competition, detail: copy.competitionText},
      {label: copy.marketRead, title: copy.xcmgEntry, detail: copy.xcmgEntryText}
    ];
    const transportRuleRows = expanded.transportRules.map((item) => `<tr><th scope="row">${escapeHtml(item.level)}</th><td>${escapeHtml(narrative(item.threshold))}</td><td>${escapeHtml(narrative(item.implication))}</td></tr>`).join('');
    const rightInsightCards = [
      {title: copy.leadingModelsTitle, detail: copy.leadingModelsText, source: 48},
      {title: copy.transportFitTitle, detail: copy.transportFitText, source: 49}
    ].map((item) => `<article><header><b>${escapeHtml(item.title)}</b></header><p>${escapeHtml(narrative(item.detail))}</p></article>`).join('');
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
      ${renderMarketEvidenceSummary(sourceVisuals)}
      ${renderCategoryContext(visualExpansion?.category_context)}
      <div class="marketDecisionGrid">
        ${renderBrandSales(sourceVisuals?.market?.annual_brand_sales)}
        <div class="pptModule customerEvidence">
          <div class="customerEvidenceTop">
            <div class="pptModuleTitle"><span>${escapeHtml(copy.customerTitle)}</span>${sourceBadge(49)}</div>
            <div class="shareStrip"><div class="shareStripHead"><span>${escapeHtml(copy.shareTitle)}</span><b>${view.market.leading_share.value}%</b></div><div class="shareBar"><span></span></div><div class="brandNames"><span>${escapeHtml(copy.shareNote)}</span>${sourceBadge(48)}</div></div>
            <div class="customerMix" aria-label="${escapeHtml(copy.customerTitle)}">${customers}</div><ul class="customerLegend">${customerLegend}</ul><p class="sourceCaveat">${escapeHtml(language === 'en' ? 'The four listed customer groups account for 90%; the remaining 10% is grouped as other customers.' : '四类客户占比合计90%，其余10%归入其他客户。')}</p>
          </div>
          <div class="marketRightInsights"><h3>${escapeHtml(copy.rightInsightTitle)}</h3>${rightInsightCards}</div>
          <div class="purchaseLogicBlock"><h3 class="pptModuleTitle"><span>${escapeHtml(copy.purchaseLogic)}</span></h3><ul class="purchaseLogic">${logic}</ul></div>
        </div>
      </div>
      <div class="marketModelDemand">${renderModelDemand(sourceVisuals?.market?.model_demand_2025)}</div>
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
        <article class="marketDetailBlock transportRuleBlock"><div class="pptModuleTitle"><span>${escapeHtml(copy.transportRuleTitle)}</span></div><p class="marketTableCaveat">${escapeHtml(copy.transportRuleCaveat)}</p><div class="marketTableScroll"><table class="transportRuleTable"><thead><tr><th>${escapeHtml(copy.licenceClass)}</th><th>${escapeHtml(copy.generalThreshold)}</th><th>${escapeHtml(copy.applicationImpact)}</th></tr></thead><tbody>${transportRuleRows}</tbody></table></div></article>
      </div>`);
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
    const workObjects = record.work_objects?.[language] || record.work_objects?.zh || [];
    const operatingCharacteristics = record.operating_characteristics?.[language] || record.operating_characteristics?.zh || [];
    const historicalAssessment = record.historical_assessment?.[language] || record.historical_assessment?.zh || [];
    const key = findingKey(record.finding_status);
    const engineering = scenarioEngineering[record.id];
    const links = (scenarioConditionLinks[record.id] || []).map((item) => `<a href="#${escapeHtml(item.id)}">${escapeHtml(language === 'en' ? item.en : item.zh)}</a>`).join('');
    const assessments = (expanded.scenarioAssessments[record.id] || []).map((item) => {
      const statusKey = assessmentKey(item.status);
      return `<tr><th scope="row" data-label="${escapeHtml(copy.scenarioRequirement)}">${escapeHtml(text(item.need))}</th><td data-label="${escapeHtml(copy.status)}"><div class="assessmentJudgment"><span class="scenarioStatus status-${statusKey}">${escapeHtml(assessmentLabel(item.status))}</span><p>${escapeHtml(narrative(item.current))}</p></div></td><td data-label="${escapeHtml(copy.productAction)}">${escapeHtml(narrative(item.action))}</td></tr>`;
    }).join('');
    return `
      <article class="scenarioBand" id="job-${escapeHtml(record.id)}" data-scenario-id="${escapeHtml(record.id)}">
        <header class="scenarioBandHeader">
          <span class="scenarioNumber">${String(index + 1).padStart(2, '0')}</span>
          <div class="scenarioBandTitle"><h3>${escapeHtml(text(record.title))}</h3><div class="scenarioConditionLinks"><span>${escapeHtml(copy.linkedConditions)}</span>${links}</div><div class="scenarioSource">${sourceBadge(record)}</div></div>
        </header>
        <div class="scenarioBandMain">
          ${renderScenarioGallery(record)}
          <div class="scenarioBody">
            <dl class="scenarioFacts">
              <div class="scenarioFact"><dt>${escapeHtml(copy.customer)}</dt><dd>${escapeHtml(text(record.customer))}</dd></div>
              <div class="scenarioFact"><dt>${escapeHtml(copy.needs)}</dt><dd><p class="scenarioNarrative">${escapeHtml(statementFromItems(needs))}</p></dd></div>
              <div class="scenarioFact"><dt>${escapeHtml(copy.steps)}</dt><dd><p class="scenarioNarrative">${escapeHtml(workflowFromItems(steps))}</p></dd></div>
              <div class="scenarioFact scenarioFindingFact"><dt>${escapeHtml(copy.finding)}</dt><dd class="scenarioFinding"><span class="scenarioStatus status-${key}">${escapeHtml(findingLabel(record.finding_status))}</span><p>${escapeHtml(narrative(record.conclusion))}</p></dd></div>
            </dl>
          </div>
        </div>
        <div class="scenarioSourceContext">
          <section class="workObjects"><h4>${escapeHtml(copy.workObjects)}</h4><p class="scenarioNarrative" data-item-count="${workObjects.length}">${escapeHtml(workObjectNarrative(workObjects))}</p></section>
          <section class="operatingCharacteristics"><h4>${escapeHtml(copy.operatingCharacteristics)}</h4><p class="scenarioNarrative" data-item-count="${operatingCharacteristics.length}">${escapeHtml(statementFromItems(operatingCharacteristics))}</p></section>
          <section class="historicalAssessment"><h4>${escapeHtml(copy.historicalAssessment)}</h4><p class="scenarioNarrative historicalNarrative" data-item-count="${historicalAssessment.length}">${escapeHtml(historicalNarrative(historicalAssessment))}</p></section>
        </div>
        <div class="scenarioEngineering">
          <article><span>${escapeHtml(copy.parameterImpact)}</span><p>${escapeHtml(text(engineering?.parameter))}</p></article>
          <article><span>${escapeHtml(copy.configurationImpact)}</span><p>${escapeHtml(text(engineering?.configuration))}</p></article>
          <article><span>${escapeHtml(copy.engineeringAction)}</span><p>${escapeHtml(text(engineering?.action))}</p></article>
        </div>
        <div class="scenarioAssessment"><table><caption class="srOnly">${escapeHtml(text(record.title))}</caption><thead><tr><th>${escapeHtml(copy.scenarioRequirement)}</th><th>${escapeHtml(copy.status)}</th><th>${escapeHtml(copy.productAction)}</th></tr></thead><tbody>${assessments}</tbody></table></div>
      </article>`;
  }

  function renderScenarios(records, visualExpansion) {
    const section = makeSection('ppt-scenarios', copy.scenarioTitle, copy.scenarioSubtitle, [50, 51, 52, 53, 54, 55, 56, 57, 58]);
    section.insertAdjacentHTML('beforeend', `${renderTaskCapability(visualExpansion?.task_capability, records)}${renderAttachmentHeatmap(visualExpansion?.attachment_matrix, records)}${renderScenarioMatrix(records)}<div class="scenarioSequence">${records.map((record, index) => renderScenarioBody(record, index)).join('')}</div>`);
    return section;
  }

  function renderPaper(view, sourceVisuals, visualExpansion) {
    const section = makeSection('ppt-paper', copy.paperTitle, copy.paperSubtitle, [59, 60, 61]);
    const headerModels = view.paper_comparison.models.map((model, index) => `<th class="${index === 0 ? 'xcmgColumn' : ''}">${escapeHtml(model)}</th>`).join('');
    const rows = view.paper_comparison.metrics.map((metric) => {
      const values = metric.values.map((value, index) => `<td class="${index === 0 ? 'xcmgColumn' : ''}">${escapeHtml(value)}${value !== '/' ? ` <small>${escapeHtml(metric.unit)}</small>` : ''}</td>`).join('');
      return `<tr class="metric-${escapeHtml(metric.status)}"><th>${escapeHtml(text(metric.name))}</th>${values}<td class="metricFinding">${escapeHtml(narrative(metric.finding))}</td></tr>`;
    }).join('');
    const configRows = view.paper_comparison.configuration_findings.map((item) => `<div class="configRow"><b>${escapeHtml(text(item.label))}</b><strong>${escapeHtml(narrative(item.xcmg))}</strong><span>${escapeHtml(narrative(item.comparison))}</span></div>`).join('');
    const insights = `<div class="paperInsightGrid">${paperInsights.map((item) => `<article class="tone-${item.tone}"><span>${escapeHtml(text(item.title))}</span><b>${escapeHtml(text(item.metric))}</b><p>${escapeHtml(text(item.detail))}</p></article>`).join('')}</div>`;
    const completeGroups = expanded.paperGroups.map((group) => renderSourceDataGroup(group, 'paper')).join('');
    section.insertAdjacentHTML('beforeend', `${renderPerformanceVisual(sourceVisuals?.performance)}${renderAbsoluteGaps(visualExpansion?.absolute_gaps)}<div class="pptModuleTitle"><span>${escapeHtml(copy.paperRead)}</span></div>${insights}<div class="pptModuleTitle directDataTitle"><span>${escapeHtml(copy.fullPaper)}</span></div><div class="comparisonMatrix"><table><thead><tr><th>${escapeHtml(copy.metric)}</th>${headerModels}<th>${escapeHtml(copy.findingColumn)}</th></tr></thead><tbody>${rows}</tbody></table></div><div class="pptModuleTitle configTitle"><span>${escapeHtml(copy.configurationTitle)}</span></div><div class="configMatrix">${configRows}</div><div class="sourceDataGroups paperSourceGroups">${completeGroups}</div>`);
    return section;
  }

  function renderField(records, sourceVisuals, visualExpansion) {
    const section = makeSection('ppt-field', copy.fieldTitle, copy.fieldSubtitle, [62, 63, 64, 65, 66]);
    const counts = records.reduce((result, record) => { const key = findingKey(record.finding_status); result[key] = (result[key] || 0) + 1; return result; }, {});
    const summary = ['advantage', 'gap', 'pending', 'missing'].map((key) => `<span class="status-${key}"><b>${counts[key] || 0}</b>${escapeHtml(copy[key])}</span>`).join('');
    const rows = records.map((record) => {
      const key = findingKey(record.finding_status);
      return `<tr><td>${escapeHtml(fieldGroup(record.metric))}</td><td><b>${escapeHtml(text(fieldMetricNames[record.metric]) || record.metric)}</b></td><td>${escapeHtml(narrative(record.conclusion))}</td><td><span class="scenarioStatus status-${key}">${escapeHtml(copy[key])}</span></td><td><span class="validationText">${escapeHtml(text(validationLabels[record.validation_status]))}</span></td></tr>`;
    }).join('');
    const ratingMethod = `<div class="scoringMethod fieldScoringMethod"><div class="scoringMethodLead"><span>${escapeHtml(copy.ratingRuleTitle)}</span><strong>1–5</strong></div><dl><div><dt>${escapeHtml(copy.ratingScaleTitle)}</dt><dd>${escapeHtml(copy.ratingScaleText)}</dd></div><div><dt>${escapeHtml(copy.ratingAverageTitle)}</dt><dd>${escapeHtml(copy.ratingAverageText)}</dd></div><div><dt>${escapeHtml(copy.ratingVisualTitle)}</dt><dd>${escapeHtml(copy.ratingVisualText)}</dd></div><div><dt>${escapeHtml(copy.ratingBoundaryTitle)}</dt><dd>${escapeHtml(copy.ratingBoundaryText)}</dd></div></dl></div>`;
    const themes = `<div class="fieldThemeGrid">${fieldThemes.map((item) => `<article class="tone-${item.tone}"><span>${escapeHtml(text(item.title))}</span><p>${escapeHtml(narrative(item.detail))}</p></article>`).join('')}</div>`;
    const completeGroups = expanded.fieldGroups.map((group) => renderSourceDataGroup(group, 'field')).join('');
    section.insertAdjacentHTML('beforeend', `${ratingMethod}<div class="fieldSummary">${summary}</div>${renderFieldEvidence(visualExpansion?.field_evidence)}<div class="pptModuleTitle"><span>${escapeHtml(copy.fieldRead)}</span></div>${themes}${renderFieldGroupSummary(sourceVisuals?.field_rating_heatmap)}${renderFieldHeatmap(sourceVisuals?.field_rating_heatmap)}<div class="pptModuleTitle directDataTitle"><span>${escapeHtml(copy.fullField)}</span></div><div class="fieldMatrix"><table><thead><tr><th>${escapeHtml(copy.dimension)}</th><th>${escapeHtml(copy.metric)}</th><th>${escapeHtml(copy.conclusion)}</th><th>${escapeHtml(copy.status)}</th><th>${escapeHtml(copy.validation)}</th></tr></thead><tbody>${rows}</tbody></table></div><div class="sourceDataGroups fieldSourceGroups">${completeGroups}</div>`);
    return section;
  }

  function renderPositioning(sourceVisuals, visualExpansion) {
    const section = makeSection('ppt-positioning', copy.positionSectionTitle, copy.positionSectionSubtitle, [67, 68]);
    const positionData = sourceVisuals?.historical_positioning;
    const positionRows = (positionData?.rows || expanded.positioning).map((item) => {
      const price = item.price || (Number.isFinite(item.price_usd) ? `$${formatNumber(item.price_usd)}` : '-');
      return `<tr class="${item.brand === 'XCMG' ? 'xcmgPositionRow' : ''}"><th scope="row">${escapeHtml(item.brand)}</th><td>${escapeHtml(item.models)}</td><td>${escapeHtml(price)}</td><td>${escapeHtml(item.share)}</td></tr>`;
    }).join('');
    const portfolioRows = expanded.marketPortfolio.map((item) => `<tr class="${item.brand === 'XCMG' ? 'xcmgPortfolioRow' : ''}"><th scope="row">${escapeHtml(item.brand)}</th><td>${escapeHtml(item.models)}</td><td>${escapeHtml(narrative(item.architecture))}</td><td>${escapeHtml(narrative(item.implication))}</td></tr>`).join('');
    const metrics = [
      {label: copy.positionHistory, value: copy.positionHistoryValue, detail: copy.positionHeadline},
      {label: copy.positionPrice, value: copy.positionPriceValue, detail: copy.positionPriceDetail},
      {label: copy.positionShare, value: copy.positionShareValue, detail: copy.positionShareDetail},
      {label: copy.positionTarget, value: copy.positionTargetValue, detail: copy.positionTargetDetail},
      {label: copy.positionPortfolio, value: copy.positionPortfolioValue, detail: copy.positionPortfolioDetail}
    ].map((item) => `<article><span>${escapeHtml(item.label)}</span><b>${escapeHtml(item.value)}</b><p>${escapeHtml(item.detail)}</p></article>`).join('');
    const positioningTable = `<article class="positioningBlock"><div class="pptModuleTitle"><span>${escapeHtml(copy.positioningTitle)}</span></div><div class="positioningScroll"><table><thead><tr><th>${escapeHtml(copy.positioningBrand)}</th><th>${escapeHtml(copy.positioningModels)}</th><th>${escapeHtml(copy.positioningPrice)}</th><th>${escapeHtml(copy.positioningShare)}</th></tr></thead><tbody>${positionRows}</tbody></table></div></article>`;
    const portfolioTable = `<article class="marketDetailBlock positionPortfolioTable"><div class="pptModuleTitle"><span>${escapeHtml(copy.positionArchitectureTitle)}</span></div><div class="marketTableScroll"><table class="marketPortfolioMatrix"><thead><tr><th>${escapeHtml(copy.portfolioBrand)}</th><th>${escapeHtml(copy.portfolioCount)}</th><th>${escapeHtml(copy.portfolioArchitecture)}</th><th>${escapeHtml(copy.portfolioImplication)}</th></tr></thead><tbody>${portfolioRows}</tbody></table></div></article>`;
    section.insertAdjacentHTML('beforeend', `
      <div class="positionDecision">
        <div class="positionDecisionLead"><span>${escapeHtml(copy.positionDecisionTitle)}</span><h3>${escapeHtml(copy.positionHeadline)}</h3><p>${escapeHtml(copy.positionBoundary)}</p></div>
        <div class="positionMetricStrip">${metrics}</div>
      </div>
      <div class="positionVisualGrid">
        ${renderPriceShare(sourceVisuals?.market?.brand_position_2025)}
        ${positioningTable}
      </div>
      ${renderPortfolioCoverage(visualExpansion?.portfolio_matrix)}
      ${portfolioTable}
      <div class="profileBoundary">${escapeHtml(copy.profileBoundary)}</div>
      ${renderCompetitivenessProfile(sourceVisuals?.competitiveness_profile)}`);
    return section;
  }

  function renderActions(roadmap, portfolio, sourceVisuals, visualExpansion) {
    const section = makeSection('ppt-actions', copy.actionTitle, copy.actionSubtitle, [67]);
    const rows = roadmap.map((record) => `<div class="roadmapRow" data-priority="${escapeHtml(record.priority)}"><span class="roadmapPriority">${escapeHtml(record.priority)}</span><span class="roadmapTopic">${escapeHtml(text(roadmapTopics[record.id]) || record.id)}</span><span class="roadmapAction">${escapeHtml(narrative(record.action))}</span><span class="roadmapValidation">${escapeHtml(copy.verifyRequired)}</span></div>`).join('');
    const portfolioGap = portfolio.find((record) => record.id === 'portfolio-current-gap');
    const phases = `<div class="actionPhaseGrid">${actionPhases.map((phase, index) => `<article><span>${escapeHtml([copy.phaseNow, copy.phaseNext, copy.phasePlatform][index])}</span><h3>${escapeHtml(text(phase.title))}</h3><ul>${(phase.items[language] || phase.items.zh).map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul></article>`).join('')}</div>`;
    const dimensionRows = expanded.competitionDimensions.map((item) => `<tr><th scope="row">${escapeHtml(text(item.dimension))}</th><td>${escapeHtml(narrative(item.strength))}</td><td>${escapeHtml(narrative(item.gap))}</td><td>${escapeHtml(narrative(item.action))}</td></tr>`).join('');
    const actionMethod = `<div class="scoringMethod actionMethod"><div class="scoringMethodLead"><span>${escapeHtml(copy.actionRuleTitle)}</span><strong>${escapeHtml(copy.actionRuleValue)}</strong></div><p>${escapeHtml(copy.actionRuleText)}</p></div>`;
    section.insertAdjacentHTML('beforeend', `${actionMethod}<div class="pptModuleTitle"><span>${escapeHtml(copy.competitionDetail)}</span></div><div class="competitionGapMatrix"><table><colgroup><col class="gapDimensionCol"><col class="gapFoundationCol"><col class="gapDetailCol"><col class="gapActionCol"></colgroup><thead><tr><th>${escapeHtml(copy.dimension)}</th><th>${escapeHtml(copy.strengthColumn)}</th><th>${escapeHtml(copy.gapColumn)}</th><th>${escapeHtml(copy.actionColumn)}</th></tr></thead><tbody>${dimensionRows}</tbody></table></div>${renderClosureTimeline(visualExpansion?.closure_timeline, sourceVisuals?.historical_improvement_ledger)}${renderImprovementLedger(sourceVisuals?.historical_improvement_ledger)}${phases}<div class="roadmapTable">${rows}</div><div class="portfolioNote"><div><b>${escapeHtml(copy.portfolio)}</b><p>${escapeHtml(narrative(portfolioGap?.conclusion))}</p></div><div><b>${escapeHtml(copy.historicalPositioning)}</b><p>${language === 'en' ? 'Align target price, channel support, residual value and production equipment into one market position.' : '目标价格、渠道支持、残值与量产配置应形成一致的市场定位。'}</p></div></div>`);
    return section;
  }

  function applyStaticDemoCopy() {
    const labels = language === 'en'
      ? {
          fullData: 'Complete Data',
          exportData: 'Export Complete Data',
          allData: 'All Specifications and Equipment',
          parameterCaption: 'Complete Specification Data',
          equipmentCaption: 'Complete Equipment Data',
          gapLead: 'Verified gaps currently center on blade float, joystick travel, the AUX1 selector valve and the case-drain line. The list below shows the underlying specifications and equipment status.'
        }
      : {
          fullData: '完整数据',
          exportData: '导出完整数据',
          allData: '全量参数与配置',
          parameterCaption: '全部参数数据',
          equipmentCaption: '全部标选配数据',
          gapLead: '当前可核验差距集中在推土铲浮动、手柄行走、AUX1换向阀和卸油管路。下列均为具体参数或标选配状态。'
        };
    document.documentElement.lang = language === 'en' ? 'en-US' : 'zh-CN';
    document.querySelectorAll('a[href="#raw"]').forEach((link) => { link.textContent = labels.fullData; });
    const heading = document.querySelector('#raw > h2');
    if (heading) heading.textContent = labels.fullData;
    document.querySelectorAll('a[download][href*="XCMG_3.5t_mini_excavator_competitor_source.xlsx"]').forEach((link) => { link.textContent = labels.exportData; });
    const summary = document.querySelector('#raw .rawDisclosure > summary');
    if (summary) summary.textContent = labels.allData;
    const captions = document.querySelectorAll('#raw .rawTable caption');
    if (captions[0]) captions[0].textContent = labels.parameterCaption;
    if (captions[1]) captions[1].textContent = labels.equipmentCaption;
    const gapLead = document.querySelector('.productGapContent > p');
    if (gapLead) gapLead.textContent = labels.gapLead;
  }

  async function loadJson(name, {optional = false} = {}) {
    let lastError;
    for (let attempt = 0; attempt < 2; attempt += 1) {
      try {
        const url = new URL(`data/ppt-insights/${name}.json`, document.baseURI);
        if (attempt) url.searchParams.set('retry', String(Date.now()));
        const response = await fetch(url, {cache: 'no-store'});
        if (!response.ok) throw new Error(`${name}: ${response.status}`);
        return await response.json();
      } catch (error) {
        lastError = error;
        if (!attempt) await new Promise((resolve) => window.setTimeout(resolve, 180));
      }
    }
    if (optional) {
      console.warn(`Optional analysis data unavailable: ${name}`, lastError);
      return null;
    }
    throw lastError;
  }

  async function loadDemoJson(name) {
    let lastError;
    for (let attempt = 0; attempt < 2; attempt += 1) {
      try {
        const url = new URL(`ppt-integration-demo/data/${name}.json`, document.baseURI);
        if (attempt) url.searchParams.set('retry', String(Date.now()));
        const response = await fetch(url, {cache: 'no-store'});
        if (!response.ok) throw new Error(`${name}: ${response.status}`);
        return await response.json();
      } catch (error) {
        lastError = error;
        if (!attempt) await new Promise((resolve) => window.setTimeout(resolve, 180));
      }
    }
    throw lastError;
  }

  async function loadData() {
    const requiredNames = ['tonnage-3-4t-view', 'tonnage', 'field-evaluation', 'roadmap', 'portfolio'];
    const optionalNames = ['visual-assets', 'source-visuals-3-4t', 'visual-expansion-3-4t'];
    const [required, optional, coverage] = await Promise.all([
      Promise.all(requiredNames.map((name) => loadJson(name))),
      Promise.all(optionalNames.map((name) => loadJson(name, {optional: true}))),
      loadDemoJson('coverage-3-4t')
    ]);
    return {
      tonnage34tView: required[0],
      tonnage: required[1],
      fieldEvaluation: required[2],
      roadmap: required[3],
      portfolio: required[4],
      visualAssets: optional[0],
      sourceVisuals: optional[1],
      visualExpansion: optional[2],
      coverage
    };
  }

  async function init() {
    if (!document.body.classList.contains('pptIntegratedDemo')) return;
    const navLabels = {market: copy.navMarket, scenarios: copy.navScenarios, paper: copy.navPaper, field: copy.navField, positioning: copy.navPositioning, actions: copy.navActions};
    document.querySelectorAll('[data-ppt-nav]').forEach((link) => { link.textContent = navLabels[link.dataset.pptNav] || link.textContent; });
    try {
      state = await loadData();
      const coveredSlides = [...new Set(state.coverage.records.map((record) => record.slide))].sort((a, b) => a - b);
      if (coveredSlides.length !== state.coverage.meta.expected_slide_count || coveredSlides[0] !== state.coverage.meta.first_slide || coveredSlides.at(-1) !== state.coverage.meta.last_slide) throw new Error('3-4 t content coverage manifest is incomplete');
      document.body.dataset.coveredSlides = coveredSlides.join(' ');
      const eyebrow = document.querySelector('.hero .eyebrow');
      if (eyebrow) eyebrow.textContent = copy.internal;
      document.querySelector('#summary')?.after(renderMarket(state.tonnage34tView, state.sourceVisuals, state.visualExpansion));
      const scenarios = renderScenarios(state.tonnage.records.filter((record) => record.id.startsWith('scenario-')), state.visualExpansion);
      const paper = renderPaper(state.tonnage34tView, state.sourceVisuals, state.visualExpansion);
      document.querySelector('#conditions')?.after(scenarios, paper);
      document.querySelector('#cond6')?.after(
        renderField(state.fieldEvaluation.records, state.sourceVisuals, state.visualExpansion),
        renderPositioning(state.sourceVisuals, state.visualExpansion),
        renderActions(state.roadmap.records, state.portfolio.records, state.sourceVisuals, state.visualExpansion)
      );
      initCapabilityExplorer(document);
      window.XCMGPPTIntegration = {language, data: state, coveredSlides};
    } catch (error) {
      const section = makeSection('ppt-load-error', copy.marketTitle, '');
      section.innerHTML += `<p class="scopeBoundary">${escapeHtml(copy.loadError)}</p>`;
      document.querySelector('#summary')?.after(section);
      console.error(error);
    } finally {
      applyStaticDemoCopy();
      window.setTimeout(applyStaticDemoCopy, 0);
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once: true}); else init();
})();
