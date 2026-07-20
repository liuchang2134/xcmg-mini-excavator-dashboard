(function () {
  'use strict';

  const STORAGE_KEY = 'xcmg-benchmark-language';
  const params = new URLSearchParams(window.location.search);
  let storedLanguage = '';
  try { storedLanguage = window.localStorage.getItem(STORAGE_KEY) || ''; } catch (_) { storedLanguage = ''; }
  const language = params.get('lang') === 'en' || (params.get('lang') !== 'zh' && storedLanguage === 'en') ? 'en' : 'zh';

  const copy = {
    zh: {
      internal: 'XCMG ARC内部分析',
      marketTitle: '市场与客户适配',
      marketSubtitle: '销量结构、客户决策与运输边界共同定义3–4吨产品的实际适用性。',
      scoringBoundary: '该部分用于解释产品适配背景，不参与现有参数、配置、总体及工况评分。',
      volumeTitle: '3–4吨市场销量变化',
      historical: '历史值',
      estimate: '历史估计',
      forecast: '历史预测',
      units: '台',
      shareTitle: '领先品牌合计份额',
      shareNote: '久保田、约翰迪尔、山猫、卡特',
      customerTitle: '客户结构与购买逻辑',
      purchaseLogic: '购买决策重点',
      transportTitle: '皮卡 + 14K拖车运输边界',
      baseMass: '基础机',
      equippedMass: '典型配置后',
      historicalPlan: '方案状态需结合当前量产配置复核。',
      scenarioTitle: '扩展作业场景',
      scenarioSubtitle: '补充运输、进场、挖掘、回填和精整等连续作业环节。',
      customer: '客户群',
      needs: '关键需求',
      steps: '典型作业步骤',
      finding: 'XCMG判断',
      scenarioIndex: '作业场景与主要差距',
      workCondition: '工况',
      keyFinding: '关键判断',
      status: '状态',
      paperTitle: '关键参数与配置复核',
      paperSubtitle: '围绕市场适配和现场作业，对五款代表机型进行直接复核。',
      paperBoundary: '本矩阵作为现有Excel评分的补充证据，不重复计分；如不同版本存在差异，以最新核验数据为准。',
      fullPaper: '展开关键参数矩阵',
      metric: '指标',
      findingColumn: '对工况的具体影响',
      configurationTitle: '关键配置差异',
      xcmgState: 'XCMG状态',
      comparison: '竞品差异与工况影响',
      fieldTitle: '实机评价',
      fieldSubtitle: '操控、舒适性、可靠性和维修性单独呈现',
      fieldBoundary: '实机评价不生成新分数。无当前量化试验数据时，只使用“优势、差距、待验证、未覆盖”。',
      fullField: '展开实机评价矩阵',
      dimension: '评价维度',
      conclusion: '评价结论',
      validation: '当前验证要求',
      advantage: '优势',
      gap: '差距',
      pending: '待验证',
      missing: '未覆盖',
      actionTitle: 'XCMG产品改进建议',
      actionSubtitle: '将市场、参数与实机差距转化为可验证的工程动作。',
      actionBoundary: '以下均为建议动作或验证任务，不代表已立项、已完成或承诺日期。',
      priority: '优先级',
      topic: '改进主题',
      action: '工程动作',
      validationState: '验证状态',
      verifyRequired: '需工程、试验与市场共同验证',
      portfolio: '型谱差距',
      historicalPositioning: '历史定位与目标',
      inlineMaterials: '模块资料',
      researchSummary: '研究结论',
      rawText: '原始记录',
      safety: '安全性',
      reliability: '可靠性与环境',
      control: '操控性能',
      comfort: '驾驶舒适性',
      service: '维修性、经济性与细节',
      loadError: '扩展分析数据未能载入，请通过本地预览地址打开。'
    },
    en: {
      internal: 'XCMG ARC INTERNAL ANALYSIS',
      marketTitle: 'Market and Customer Fit',
      marketSubtitle: 'Volume structure, customer decisions and transport constraints jointly define practical fit in the 3–4 t class.',
      scoringBoundary: 'This section explains product-fit context and does not participate in existing specification, equipment, overall or application scores.',
      volumeTitle: '3–4 t market volume trend',
      historical: 'Historical',
      estimate: 'Historical estimate',
      forecast: 'Historical forecast',
      units: 'units',
      shareTitle: 'Combined leading-brand share',
      shareNote: 'Kubota, John Deere, Bobcat and Caterpillar',
      customerTitle: 'Customer mix and purchase logic',
      purchaseLogic: 'Purchase-decision priorities',
      transportTitle: 'Pickup + 14K trailer transport envelope',
      baseMass: 'Base machine',
      equippedMass: 'With representative equipment',
      historicalPlan: 'Confirm the proposal against the current production configuration.',
      scenarioTitle: 'Extended Job Applications',
      scenarioSubtitle: 'Covers connected transport, site-entry, excavation, backfill and finish-work sequences.',
      customer: 'Customer group',
      needs: 'Critical requirements',
      steps: 'Representative work sequence',
      finding: 'XCMG finding',
      scenarioIndex: 'Application index and principal gaps',
      workCondition: 'Application',
      keyFinding: 'Key finding',
      status: 'Status',
      paperTitle: 'Key Specification and Equipment Review',
      paperSubtitle: 'Directly reviews five representative models against market fit and field applications.',
      paperBoundary: 'This matrix supplements the existing Excel-based scoring and is not scored again. Where versions differ, use the latest validated dataset.',
      fullPaper: 'Open key-specification matrix',
      metric: 'Metric',
      findingColumn: 'Specific application impact',
      configurationTitle: 'Key equipment differences',
      xcmgState: 'XCMG status',
      comparison: 'Competitive difference and application impact',
      fieldTitle: 'Field Evaluation',
      fieldSubtitle: 'Control, comfort, reliability and serviceability remain separate from paper scores',
      fieldBoundary: 'No new field-test score is created. Without current quantified test data, only Advantage, Gap, Pending Validation or Not Covered is used.',
      fullField: 'Open field-evaluation matrix',
      dimension: 'Evaluation dimension',
      conclusion: 'Source finding',
      validation: 'Current validation requirement',
      advantage: 'Advantage',
      gap: 'Gap',
      pending: 'Pending validation',
      missing: 'Not covered',
      actionTitle: 'XCMG Improvement Priorities and Evidence',
      actionSubtitle: 'Translate gaps into system-level actions without treating historical plans as completed work',
      actionBoundary: 'The items below are recommendations or validation tasks. They do not indicate approval, completion or committed timing.',
      priority: 'Priority',
      topic: 'Improvement topic',
      action: 'Engineering action',
      validationState: 'Validation status',
      verifyRequired: 'Engineering, test and market validation required',
      portfolio: 'Portfolio gap',
      historicalPositioning: 'Historical positioning and target',
      inlineMaterials: 'Module research material',
      researchSummary: 'Research finding',
      rawText: 'Original record',
      safety: 'Safety',
      reliability: 'Reliability and environment',
      control: 'Controllability',
      comfort: 'Operator comfort',
      service: 'Serviceability, economy and detail quality',
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
    current_quantified_test_report_not_in_scope: {zh: '补充当前耐久与防腐试验报告', en: 'Add current durability and corrosion test reports'},
    altitude_and_current_environmental_test_required: {zh: '补充环境与高海拔试验', en: 'Add environmental and altitude testing'},
    requires_current_machine_control_test: {zh: '复核当前软件与液压标定版本', en: 'Verify current software and hydraulic calibration'},
    requires_instrumented_and_operator_validation: {zh: '开展仪器测试与机手盲评', en: 'Run instrumented testing and operator blind evaluation'},
    quantified_current_test_required: {zh: '补充循环时间和平整精度数据', en: 'Add cycle-time and grading-accuracy data'},
    current_pro_configuration_and_user_clinic_required: {zh: '核验PRO配置并开展北美用户诊断', en: 'Verify PRO configuration and run a North American user clinic'},
    requires_current_service_task_time_study: {zh: '开展典型保养任务工时测量', en: 'Measure representative service-task time'},
    quantified_duty_cycle_test_required: {zh: '统一工况实测油耗', en: 'Measure fuel use under a common duty cycle'},
    requires_current_coating_audit_and_field_return_review: {zh: '开展涂层审计并复盘市场故障件', en: 'Audit coatings and review field-return parts'},
    requires_current_document_control_audit: {zh: '校核手册完整性与准确性', en: 'Audit manual completeness and accuracy'}
  };

  const statusLabels = {
    historical_fact: {zh: '历史事实', en: 'Historical fact'},
    historical_fact_and_forecast: {zh: '历史事实与预测', en: 'Historical fact and forecast'},
    historical_assessment: {zh: '历史判断', en: 'Historical assessment'},
    historical_assessment_and_plan: {zh: '历史判断与计划', en: 'Historical assessment and plan'},
    historical_internal_evaluation: {zh: '历史内部评价', en: 'Historical internal evaluation'},
    historical_internal_evaluation_and_plan: {zh: '历史评价与计划', en: 'Historical evaluation and plan'},
    historical_specification_comparison: {zh: '历史参数对比', en: 'Historical specification comparison'},
    historical_summary: {zh: '历史总结', en: 'Historical summary'},
    historical_positioning_and_target: {zh: '历史定位与目标', en: 'Historical positioning and target'},
    historical_portfolio_gap: {zh: '历史型谱差距', en: 'Historical portfolio gap'},
    historical_positioning: {zh: '历史定位', en: 'Historical positioning'},
    historical_target: {zh: '历史目标', en: 'Historical target'},
    future_recommendation: {zh: '建议动作', en: 'Recommended action'}
  };

  const state = {data: null};

  function text(value) {
    if (value == null) return '';
    if (typeof value === 'object' && ('zh' in value || 'en' in value)) return value[language] || value.zh || value.en || '';
    return String(value);
  }

  function narrative(value) {
    let output = text(value);
    const replacements = language === 'en' ? [
      [/The PPT/gi, 'The historical analysis'],
      [/the PPT/gi, 'the historical analysis'],
      [/The source/gi, 'The historical assessment'],
      [/the source/gi, 'the historical assessment'],
      [/historical source material/gi, 'historical proposal'],
      [/\(PPT basis\)/gi, '']
    ] : [
      [/PPT历史方案/g, '历史方案'],
      [/PPT记录的/g, '历史记录中的'],
      [/PPT记录/g, '历史记录显示'],
      [/PPT明确列出的/g, '当前记录明确列出的'],
      [/PPT列出的/g, '对标记录中的'],
      [/PPT未列出/g, '当前记录未列出'],
      [/PPT未给出/g, '当前记录未给出'],
      [/PPT提及/g, '历史方案提及'],
      [/PPT建议/g, '历史方案建议'],
      [/PPT显示/g, '对标记录显示'],
      [/PPT评价/g, '历史评价认为'],
      [/PPT将/g, '历史评价将'],
      [/资料认为/g, '行业分析认为'],
      [/资料判断/g, '行业分析判断'],
      [/资料显示/g, '历史数据表明'],
      [/资料称/g, '历史评价显示'],
      [/资料将/g, '历史评价将'],
      [/在资料中/g, '在历史评价中'],
      [/历史资料/g, '历史方案'],
      [/（PPT口径）/g, '']
    ];
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

  function findingLabel(value) {
    return copy[findingKey(value)];
  }

  function statusLabel(value) {
    return text(statusLabels[value]) || String(value || '').replace(/_/g, ' ');
  }

  function validationLabel(value) {
    const exact = text(validationLabels[value]);
    if (exact) return exact;
    if (!value) return copy.verifyRequired;
    if (/legal|compliance|regulation/.test(value)) return language === 'en' ? 'Current legal and compliance review required' : '需当前法务与合规复核';
    if (/current|unverified|revalidated|confirmation|requires/.test(value)) return language === 'en' ? 'Current product or dataset verification required' : '需按当前产品或数据版本复核';
    if (/not_started|not_in_scope|business_case/.test(value)) return language === 'en' ? 'Validation has not been completed in this prototype' : '本原型尚未完成验证';
    return copy.verifyRequired;
  }

  function fieldGroup(metric) {
    if (metric === 'safety_systems') return copy.safety;
    if (/corrosion|temperature/.test(metric)) return copy.reliability;
    if (/travel|inching|grading/.test(metric)) return copy.control;
    if (/seat|hvac|space|hmi/.test(metric)) return copy.comfort;
    return copy.service;
  }

  function makeSection(id, title, subtitle) {
    const section = document.createElement('section');
    section.id = id;
    section.className = 'pptSection';
    section.innerHTML = `<h2>${escapeHtml(title)}</h2><p class="methodNote">${escapeHtml(subtitle)}</p>`;
    return section;
  }

  function slideNumbers(value) {
    return (Array.isArray(value) ? value : [value]).map(Number).filter(Boolean);
  }

  function displayDate(value) {
    const source = String(value || '');
    if (language === 'en') {
      return source
        .replace(/PPT version/gi, 'Internal record version')
        .replace(/PPT 11\.14 version/gi, 'Internal record version 11.14')
        .replace(/on slide/gi, 'in the record');
    }
    const translations = {
      '2025 market snapshot; 2026 forecast': '2025市场快照 / 2026预测',
      '2025 snapshot; 2026 forecast': '2025市场快照 / 2026预测',
      '2025 historical target; current outcome not provided': '2025历史目标 / 当前结果未提供',
      'PPT version 11.14; year not stated on slide': '内部资料版本11.14 / 原记录未注明年份',
      'PPT 11.14 version; year not stated on slide': '内部资料版本11.14 / 原记录未注明年份'
    };
    return translations[source] || source
      .replace(/PPT/gi, '内部资料')
      .replace(/on slide/gi, '在原记录中');
  }

  function inlineEvidenceCard(slide, evidenceId) {
    const slideNumber = slideNumbers(slide)[0];
    const slideRecord = state.data.slides.records.find((record) => Number(record.source_slide) === slideNumber);
    if (!slideRecord) return '';
    const evidence = state.data.evidence.records.find((record) => record.id === evidenceId)
      || state.data.evidence.records.find((record) => slideNumbers(record.source_slide).includes(slideNumber));
    const title = text(slideRecord[language]?.title || slideRecord.zh?.title || slideRecord.conclusion);
    const conclusion = narrative(evidence?.conclusion || slideRecord.conclusion);
    const raw = language === 'en'
      ? narrative(slideRecord.en?.summary || evidence?.conclusion || slideRecord.conclusion)
      : narrative(slideRecord.zh?.raw_text || (slideRecord.zh?.paragraphs || []).join('\n'));
    const asOf = displayDate(evidence?.as_of_date || slideRecord.as_of_date);
    const temporal = statusLabel(evidence?.status || slideRecord.status);
    const validation = validationLabel(evidence?.validation_status || slideRecord.validation_status);
    return `
      <article class="inlineEvidenceCard" data-source-slide="${slideNumber}">
        <figure class="inlineEvidenceVisual"><img src="ppt-integration-demo/${escapeHtml(slideRecord.thumbnail)}" alt="${escapeHtml(title)}"></figure>
        <div class="inlineEvidenceContent">
          <div class="inlineEvidenceTop"><b>${escapeHtml(copy.inlineMaterials)}</b><span>${escapeHtml(asOf)}</span></div>
          <h4>${escapeHtml(title)}</h4>
          <p class="inlineEvidenceConclusion"><strong>${escapeHtml(copy.researchSummary)}：</strong>${escapeHtml(conclusion)}</p>
          <div class="inlineEvidenceRaw"><b>${escapeHtml(copy.rawText)}</b><pre>${escapeHtml(raw)}</pre></div>
          <div class="inlineEvidenceMeta"><span>${escapeHtml(temporal)}</span><span>${escapeHtml(validation)}</span></div>
        </div>
      </article>`;
  }

  function inlineEvidenceGallery(items) {
    const seen = new Set();
    const cards = items.map((item) => typeof item === 'object' ? item : {slide: item})
      .filter((item) => {
        const slide = slideNumbers(item.slide)[0];
        if (!slide || seen.has(slide)) return false;
        seen.add(slide);
        return true;
      })
      .map((item) => inlineEvidenceCard(item.slide, item.evidenceId))
      .join('');
    return cards ? `<div class="inlineEvidenceSection"><h3>${escapeHtml(copy.inlineMaterials)}</h3><div class="inlineEvidenceGrid${seen.size > 1 ? ' multi' : ''}">${cards}</div></div>` : '';
  }

  function renderMarket(view) {
    const section = makeSection('ppt-market', copy.marketTitle, copy.marketSubtitle, copy.slides4849);
    const max = Math.max(...view.market.volume.map((item) => item.units));
    const volumes = view.market.volume.map((item) => {
      const typeLabel = item.type === 'source_forecast' ? copy.forecast : item.type === 'source_estimate' ? copy.estimate : copy.historical;
      const forecastClass = item.type === 'historical' ? '' : ' forecast';
      return `<div class="volumeColumn${forecastClass}"><i style="height:${Math.max(8, item.units / max * 100).toFixed(1)}%"></i><b>${item.units.toLocaleString(language === 'en' ? 'en-US' : 'zh-CN')} ${copy.units}</b><span>${item.year} · ${escapeHtml(typeLabel)}</span></div>`;
    }).join('');
    const customers = view.market.customer_mix.map((item) => `<span style="width:${item.value}%" title="${escapeHtml(text(item.label))} ${item.value}%"></span>`).join('');
    const customerLegend = view.market.customer_mix.map((item) => `<li><i></i><span>${escapeHtml(text(item.label))}</span><b>${item.value}%</b></li>`).join('');
    const logic = view.market.purchase_logic.map((item) => `<li>${escapeHtml(text(item))}</li>`).join('');
    const transports = view.market.transport.map((item) => {
      const width = Math.min(100, item.equipped_kg / 5000 * 100);
      return `<div class="transportRow${item.id === 'historical_pro' ? ' historical' : ''}"><strong>${escapeHtml(narrative(item.label))}</strong><div class="transportTrack"><span style="width:${width.toFixed(1)}%"></span></div><div class="transportNumbers"><b>${item.equipped_kg.toLocaleString()} kg</b>${copy.baseMass} ${item.base_kg.toLocaleString()} kg</div></div>`;
    }).join('');
    section.insertAdjacentHTML('beforeend', `
      <p class="scopeBoundary">${escapeHtml(copy.scoringBoundary)}</p>
      <div class="marketDecisionGrid">
        <div class="pptModule">
          <div class="pptModuleTitle"><span>${escapeHtml(copy.volumeTitle)}</span></div>
          <div class="volumeSeries" role="img" aria-label="${escapeHtml(copy.volumeTitle)}">${volumes}</div>
          <div class="shareStrip"><div class="shareStripHead"><span>${escapeHtml(copy.shareTitle)}</span><b>${view.market.leading_share.value}%</b></div><div class="shareBar"><span></span></div><div class="brandNames"><span>${escapeHtml(copy.shareNote)}</span></div></div>
        </div>
        <div class="pptModule">
          <div class="pptModuleTitle"><span>${escapeHtml(copy.customerTitle)}</span></div>
          <div class="customerMix" aria-label="${escapeHtml(copy.customerTitle)}">${customers}</div>
          <ul class="customerLegend">${customerLegend}</ul>
          <p class="sourceCaveat">${escapeHtml(narrative(view.market.customer_mix_note))}</p>
          <h3 class="pptModuleTitle"><span>${escapeHtml(copy.purchaseLogic)}</span></h3>
          <ul class="purchaseLogic">${logic}</ul>
        </div>
      </div>
      <div class="transportCompare">
        <div class="pptModuleTitle"><span>${escapeHtml(copy.transportTitle)}</span></div>
        <div class="transportRows">${transports}</div>
        <p class="sourceCaveat">${escapeHtml(copy.historicalPlan)}</p>
      </div>
      ${inlineEvidenceGallery([{slide: 48, evidenceId: 'ev-market-volume'}, {slide: 49, evidenceId: 'ev-customer-mix'}])}`);
    return section;
  }

  function renderScenarioBody(record) {
    const needs = text(record.needs);
    const steps = text(record.steps);
    const needsList = (Array.isArray(needs) ? needs : record.needs[language] || record.needs.zh || []).map((item) => `<li>${escapeHtml(item)}</li>`).join('');
    const stepsList = (Array.isArray(steps) ? steps : record.steps[language] || record.steps.zh || []).map((item) => `<li>${escapeHtml(item)}</li>`).join('');
    const key = findingKey(record.finding_status);
    return `
      <figure class="scenarioMedia"><img src="ppt-integration-demo/${escapeHtml(record.image)}" alt="${escapeHtml(text(record.title))}"><figcaption>${escapeHtml(text(record.title))}</figcaption></figure>
      <div class="scenarioBody">
        <div class="scenarioHead"><h3>${escapeHtml(text(record.title))}</h3><span class="scenarioStatus status-${key}">${escapeHtml(findingLabel(record.finding_status))}</span></div>
        <dl class="scenarioFacts">
          <div class="scenarioFact"><dt>${escapeHtml(copy.customer)}</dt><dd>${escapeHtml(text(record.customer))}</dd></div>
          <div class="scenarioFact"><dt>${escapeHtml(copy.needs)}</dt><dd><ul>${needsList}</ul></dd></div>
          <div class="scenarioFact"><dt>${escapeHtml(copy.steps)}</dt><dd><ol>${stepsList}</ol></dd></div>
          <div class="scenarioFact"><dt>${escapeHtml(copy.finding)}</dt><dd class="scenarioFinding">${escapeHtml(narrative(record.conclusion))}</dd></div>
        </dl>
      </div>
      <div class="scenarioEvidence">${inlineEvidenceCard(record.source_slide, record.evidence_id)}</div>`;
  }

  function renderScenarios(records) {
    const section = makeSection('ppt-scenarios', copy.scenarioTitle, copy.scenarioSubtitle, copy.sourcePages);
    const tabs = records.map((record, index) => `<button type="button" role="tab" id="scenario-tab-${index}" aria-controls="scenario-stage" aria-selected="${index === 0}" data-scenario-index="${index}">${escapeHtml(text(record.title))}</button>`).join('');
    const indexRows = records.map((record) => `<tr><td>${escapeHtml(text(record.title))}</td><td><span class="scenarioStatus status-${findingKey(record.finding_status)}">${escapeHtml(findingLabel(record.finding_status))}</span></td><td>${escapeHtml(narrative(record.conclusion))}</td></tr>`).join('');
    section.insertAdjacentHTML('beforeend', `
      <div class="scenarioTabs" role="tablist" aria-label="${escapeHtml(copy.scenarioTitle)}">${tabs}</div>
      <div class="scenarioStage" id="scenario-stage" role="tabpanel" aria-live="polite">${renderScenarioBody(records[0])}</div>
      <details class="mobileDisclosure pptDisclosure" open data-mobile-open="false"><summary>${escapeHtml(copy.scenarioIndex)}</summary><div class="scenarioIndex"><table><thead><tr><th>${escapeHtml(copy.workCondition)}</th><th>${escapeHtml(copy.status)}</th><th>${escapeHtml(copy.keyFinding)}</th></tr></thead><tbody>${indexRows}</tbody></table></div></details>`);
    section.querySelectorAll('[data-scenario-index]').forEach((button) => {
      button.addEventListener('click', () => {
        section.querySelectorAll('[data-scenario-index]').forEach((item) => item.setAttribute('aria-selected', 'false'));
        button.setAttribute('aria-selected', 'true');
        const record = records[Number(button.dataset.scenarioIndex)];
        const stage = section.querySelector('#scenario-stage');
        stage.innerHTML = renderScenarioBody(record);
        stage.setAttribute('aria-labelledby', button.id);
      });
    });
    return section;
  }

  function renderPaper(view) {
    const section = makeSection('ppt-paper', copy.paperTitle, copy.paperSubtitle, copy.source5961);
    const headerModels = view.paper_comparison.models.map((model, index) => `<th class="${index === 0 ? 'xcmgColumn' : ''}">${escapeHtml(model)}</th>`).join('');
    const rows = view.paper_comparison.metrics.map((metric) => {
      const values = metric.values.map((value, index) => `<td class="${index === 0 ? 'xcmgColumn' : ''}">${escapeHtml(value)}${value !== '/' ? ` <small>${escapeHtml(metric.unit)}</small>` : ''}</td>`).join('');
      return `<tr class="metric-${escapeHtml(metric.status)}"><th>${escapeHtml(text(metric.name))}</th>${values}<td class="metricFinding">${escapeHtml(narrative(metric.finding))}</td></tr>`;
    }).join('');
    const configRows = view.paper_comparison.configuration_findings.map((item) => `<div class="configRow"><b>${escapeHtml(text(item.label))}</b><strong>${escapeHtml(narrative(item.xcmg))}</strong><span>${escapeHtml(narrative(item.comparison))}</span></div>`).join('');
    const paperSlides = view.paper_comparison.metrics.flatMap((metric) => slideNumbers(metric.source_slide))
      .concat(view.paper_comparison.configuration_findings.flatMap((item) => slideNumbers(item.source_slide)));
    section.insertAdjacentHTML('beforeend', `
      <p class="scopeBoundary">${escapeHtml(copy.paperBoundary)}</p>
      <details class="mobileDisclosure pptDisclosure" open data-mobile-open="false"><summary>${escapeHtml(copy.fullPaper)}</summary><div class="comparisonMatrix"><table><thead><tr><th>${escapeHtml(copy.metric)}</th>${headerModels}<th>${escapeHtml(copy.findingColumn)}</th></tr></thead><tbody>${rows}</tbody></table></div></details>
      <div class="pptModuleTitle"><span>${escapeHtml(copy.configurationTitle)}</span></div>
      <div class="configMatrix">${configRows}</div>
      ${inlineEvidenceGallery(paperSlides)}`);
    return section;
  }

  function renderField(records) {
    const section = makeSection('ppt-field', copy.fieldTitle, copy.fieldSubtitle, copy.source6266);
    const counts = records.reduce((result, record) => { const key = findingKey(record.finding_status); result[key] = (result[key] || 0) + 1; return result; }, {});
    const summary = ['advantage', 'gap', 'pending', 'missing'].map((key) => `<span class="status-${key}"><b>${counts[key] || 0}</b>${escapeHtml(copy[key])}</span>`).join('');
    const rows = records.map((record) => {
      const key = findingKey(record.finding_status);
      const metricName = text(fieldMetricNames[record.metric]) || record.metric;
      const validation = validationLabel(record.validation_status);
      return `<tr><td>${escapeHtml(fieldGroup(record.metric))}</td><td><b>${escapeHtml(metricName)}</b></td><td>${escapeHtml(narrative(record.conclusion))}</td><td><span class="scenarioStatus status-${key}">${escapeHtml(copy[key])}</span></td><td><span class="validationText">${escapeHtml(validation)}</span></td></tr>`;
    }).join('');
    const fieldSlides = records.flatMap((record) => slideNumbers(record.source_slide));
    section.insertAdjacentHTML('beforeend', `
      <p class="scopeBoundary">${escapeHtml(copy.fieldBoundary)}</p>
      <div class="fieldSummary">${summary}</div>
      <details class="mobileDisclosure pptDisclosure" open data-mobile-open="false"><summary>${escapeHtml(copy.fullField)}</summary><div class="fieldMatrix"><table><thead><tr><th>${escapeHtml(copy.dimension)}</th><th>${escapeHtml(copy.metric)}</th><th>${escapeHtml(copy.conclusion)}</th><th>${escapeHtml(copy.status)}</th><th>${escapeHtml(copy.validation)}</th></tr></thead><tbody>${rows}</tbody></table></div></details>
      ${inlineEvidenceGallery(fieldSlides)}`);
    return section;
  }

  function renderActions(roadmap, portfolio) {
    const section = makeSection('ppt-actions', copy.actionTitle, copy.actionSubtitle, copy.source6768);
    const rows = roadmap.map((record) => `<div class="roadmapRow" data-priority="${escapeHtml(record.priority)}"><span class="roadmapPriority">${escapeHtml(record.priority)}</span><span class="roadmapTopic">${escapeHtml(text(roadmapTopics[record.id]) || record.id)}</span><span class="roadmapAction">${escapeHtml(narrative(record.action))}</span><span class="roadmapValidation">${escapeHtml(copy.verifyRequired)}</span></div>`).join('');
    const portfolioGap = portfolio.find((record) => record.id === 'portfolio-current-gap');
    const positioning = portfolio.find((record) => record.id === 'portfolio-positioning');
    const target = portfolio.find((record) => record.id === 'portfolio-historical-target');
    section.insertAdjacentHTML('beforeend', `
      <p class="scopeBoundary">${escapeHtml(copy.actionBoundary)}</p>
      <div class="roadmapTable">${rows}</div>
      <div class="portfolioNote">
        <div><b>${escapeHtml(copy.portfolio)}</b><p>${escapeHtml(narrative(portfolioGap?.conclusion))}</p></div>
        <div><b>${escapeHtml(copy.historicalPositioning)}</b><p>${escapeHtml([narrative(positioning?.conclusion), narrative(target?.conclusion)].filter(Boolean).join(' '))}</p></div>
      </div>
      ${inlineEvidenceGallery([{slide: 67, evidenceId: portfolioGap?.evidence_id}, {slide: 68, evidenceId: 'ev-positioning-target'}])}`);
    return section;
  }

  function setupSupplementDisclosures() {
    const media = window.matchMedia('(max-width:720px)');
    const apply = () => document.querySelectorAll('.pptDisclosure').forEach((item) => { item.open = media.matches ? item.dataset.mobileOpen === 'true' : true; });
    apply();
    if (media.addEventListener) media.addEventListener('change', apply);
    else media.addListener(apply);
  }

  async function loadData() {
    const names = ['tonnage-3-4t-view', 'tonnage', 'field-evaluation', 'roadmap', 'portfolio', 'evidence', 'slides'];
    const values = await Promise.all(names.map(async (name) => {
      const response = await fetch(`data/ppt-insights/${name}.json`);
      if (!response.ok) throw new Error(`${name}: ${response.status}`);
      return response.json();
    }));
    return {
      tonnage34tView: values[0],
      tonnage: values[1],
      fieldEvaluation: values[2],
      roadmap: values[3],
      portfolio: values[4],
      evidence: values[5],
      slides: values[6]
    };
  }

  async function init() {
    if (!document.body.classList.contains('pptIntegratedDemo')) return;
    try {
      state.data = await loadData();
      const view = state.data.tonnage34tView;
      const eyebrow = document.querySelector('.hero .eyebrow');
      if (eyebrow) eyebrow.textContent = copy.internal;

      const market = renderMarket(view);
      document.querySelector('#summary')?.after(market);

      const scenarios = renderScenarios(state.data.tonnage.records.filter((record) => record.id.startsWith('scenario-')));
      const paper = renderPaper(view);
      document.querySelector('#conditions')?.after(scenarios, paper);

      const field = renderField(state.data.fieldEvaluation.records);
      const actions = renderActions(state.data.roadmap.records, state.data.portfolio.records);
      document.querySelector('#cond6')?.after(field, actions);

      setupSupplementDisclosures();
      window.XCMGPPTIntegration = {language, data: state.data};
    } catch (error) {
      const section = makeSection('ppt-load-error', copy.marketTitle, '', copy.sourcePages);
      section.innerHTML += `<p class="scopeBoundary">${escapeHtml(copy.loadError)}</p>`;
      document.querySelector('#summary')?.after(section);
      console.error(error);
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once: true});
  else init();
})();
