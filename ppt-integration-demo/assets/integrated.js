(function () {
  'use strict';

  const STORAGE_KEY = 'xcmg-benchmark-language';
  const params = new URLSearchParams(window.location.search);
  let storedLanguage = '';
  try { storedLanguage = window.localStorage.getItem(STORAGE_KEY) || ''; } catch (_) { storedLanguage = ''; }
  const language = params.get('lang') === 'en' || (params.get('lang') !== 'zh' && storedLanguage === 'en') ? 'en' : 'zh';

  const copy = {
    zh: {
      internal: 'XCMG ARC内部资料',
      internalNote: '本原型把PPT第48–68页补充到3–4吨对标长页；历史判断、预测和计划均保留验证状态。',
      category: '挖掘机整体分析',
      marketNav: '市场 / 客户 / 运输',
      scenarioNav: '真实工况补充',
      paperNav: 'PPT纸面对照',
      fieldNav: '实机评价',
      actionNav: '改进重点与证据',
      marketTitle: '市场、客户与运输补充',
      marketSubtitle: '将销量、客户和转运边界放回产品对标语境',
      source: 'PPT来源',
      slides4849: '第48–49页',
      scoringBoundary: '本模块补充市场适配证据，不改变现有参数、配置、总体评分和六类工况评分。',
      volumeTitle: '3–4吨市场销量变化',
      historical: '历史值',
      estimate: '资料估计',
      forecast: '资料预测',
      units: '台',
      shareTitle: '领先品牌合计份额',
      shareNote: '久保田、约翰迪尔、山猫、卡特',
      customerTitle: '客户结构与购买逻辑',
      purchaseLogic: '购买决策重点',
      transportTitle: '皮卡 + 14K拖车运输边界',
      baseMass: '基础机',
      equippedMass: '典型配置后',
      historicalPlan: '历史方案，当前量产状态待核验',
      scenarioTitle: '真实工况补充',
      scenarioSubtitle: '在现有六类评分工况之外，补充PPT记录的运输与施工流程',
      sourcePages: 'PPT第49–58页',
      customer: '客户群',
      needs: '关键需求',
      steps: '典型作业步骤',
      finding: 'XCMG判断',
      evidence: '查看依据',
      scenarioIndex: '工况索引与主要差距',
      workCondition: '工况',
      keyFinding: '具体判断',
      status: '状态',
      page: '页码',
      paperTitle: 'PPT纸面参数与配置对照',
      paperSubtitle: '保留PPT原始五机对比，不重新计算现有评分',
      source5961: 'PPT第59–61页',
      paperBoundary: '下表是PPT中的历史纸面对照，与现有Excel评分并列展示；若数值版本不同，以正式源表核验为准。',
      fullPaper: '展开五机参数矩阵',
      metric: '指标',
      findingColumn: '对工况的具体影响',
      configurationTitle: '关键配置差异',
      xcmgState: 'XCMG状态',
      comparison: '竞品差异与工况影响',
      fieldTitle: '实机评价',
      fieldSubtitle: '操控、舒适性、可靠性和维修性单独呈现',
      source6266: 'PPT第62–66页',
      fieldBoundary: '实机评价不生成新分数。无当前量化试验数据时，只使用“优势、差距、待验证、资料未覆盖”。',
      fullField: '展开实机评价矩阵',
      dimension: '评价维度',
      conclusion: '资料结论',
      validation: '当前验证要求',
      advantage: '优势',
      gap: '差距',
      pending: '待验证',
      missing: '资料未覆盖',
      actionTitle: 'XCMG改进重点与证据',
      actionSubtitle: '把差距落到具体系统动作，不把历史计划当成完成结果',
      source6768: 'PPT第67–68页及相关工况页',
      actionBoundary: '以下均为建议动作或验证任务，不代表已立项、已完成或承诺日期。',
      priority: '优先级',
      topic: '改进主题',
      action: '工程动作',
      validationState: '验证状态',
      verifyRequired: '需工程、试验与市场共同验证',
      portfolio: '型谱差距',
      historicalPositioning: '历史定位与目标',
      evidenceIndex: 'PPT第48–68页证据索引',
      slide: '第',
      slideSuffix: '页',
      drawerTitle: '结论依据',
      close: '关闭',
      sourceType: '来源类型',
      dataDate: '数据时间',
      temporalStatus: '时间属性',
      validationStatus: '验证状态',
      rawText: 'PPT原始文字',
      safety: '安全性',
      reliability: '可靠性与环境',
      control: '操控性能',
      comfort: '驾驶舒适性',
      service: '维修性、经济性与细节',
      loadError: 'PPT补充数据未能载入，请通过本地HTTP预览地址打开。'
    },
    en: {
      internal: 'XCMG ARC INTERNAL',
      internalNote: 'This prototype integrates PPT slides 48–68 into the 3–4 t benchmark page. Historical judgements, forecasts and plans retain explicit validation status.',
      category: 'Excavator Overall Analysis',
      marketNav: 'Market / Customer / Transport',
      scenarioNav: 'Additional Field Applications',
      paperNav: 'PPT Paper Comparison',
      fieldNav: 'Field Evaluation',
      actionNav: 'Improvement Priorities and Evidence',
      marketTitle: 'Market, Customer and Transport Context',
      marketSubtitle: 'Connect volume, customer logic and transport constraints to the product benchmark',
      source: 'PPT source',
      slides4849: 'Slides 48–49',
      scoringBoundary: 'This section adds market-fit evidence only. It does not change the existing specification, equipment, overall or six-condition scores.',
      volumeTitle: '3–4 t market volume trend',
      historical: 'Historical',
      estimate: 'Source estimate',
      forecast: 'Source forecast',
      units: 'units',
      shareTitle: 'Combined leading-brand share',
      shareNote: 'Kubota, John Deere, Bobcat and Caterpillar',
      customerTitle: 'Customer mix and purchase logic',
      purchaseLogic: 'Purchase-decision priorities',
      transportTitle: 'Pickup + 14K trailer transport envelope',
      baseMass: 'Base machine',
      equippedMass: 'With representative equipment',
      historicalPlan: 'Historical proposal; current production status unverified',
      scenarioTitle: 'Additional Real-World Applications',
      scenarioSubtitle: 'Add transport and job workflows from the PPT alongside the existing six scored conditions',
      sourcePages: 'PPT slides 49–58',
      customer: 'Customer group',
      needs: 'Critical requirements',
      steps: 'Representative work sequence',
      finding: 'XCMG finding',
      evidence: 'View evidence',
      scenarioIndex: 'Application index and principal gaps',
      workCondition: 'Application',
      keyFinding: 'Documented finding',
      status: 'Status',
      page: 'Slide',
      paperTitle: 'PPT Specification and Equipment Comparison',
      paperSubtitle: 'Retain the original five-machine comparison without recalculating existing scores',
      source5961: 'PPT slides 59–61',
      paperBoundary: 'This is the historical paper comparison from the PPT and is shown alongside the current Excel-based evaluation. Where revisions differ, the formal source workbook requires validation.',
      fullPaper: 'Open five-machine comparison matrix',
      metric: 'Metric',
      findingColumn: 'Specific application impact',
      configurationTitle: 'Key equipment differences',
      xcmgState: 'XCMG status',
      comparison: 'Competitive difference and application impact',
      fieldTitle: 'Field Evaluation',
      fieldSubtitle: 'Control, comfort, reliability and serviceability remain separate from paper scores',
      source6266: 'PPT slides 62–66',
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
      source6768: 'PPT slides 67–68 and related application pages',
      actionBoundary: 'The items below are recommendations or validation tasks. They do not indicate approval, completion or committed timing.',
      priority: 'Priority',
      topic: 'Improvement topic',
      action: 'Engineering action',
      validationState: 'Validation status',
      verifyRequired: 'Engineering, test and market validation required',
      portfolio: 'Portfolio gap',
      historicalPositioning: 'Historical positioning and target',
      evidenceIndex: 'PPT slides 48–68 evidence index',
      slide: 'Slide ',
      slideSuffix: '',
      drawerTitle: 'Evidence',
      close: 'Close',
      sourceType: 'Source type',
      dataDate: 'Data date',
      temporalStatus: 'Temporal status',
      validationStatus: 'Validation status',
      rawText: 'Original PPT wording',
      safety: 'Safety',
      reliability: 'Reliability and environment',
      control: 'Controllability',
      comfort: 'Operator comfort',
      service: 'Serviceability, economy and detail quality',
      loadError: 'The PPT supplement could not be loaded. Open this page through the local HTTP preview address.'
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

  const state = {data: null, lastFocus: null};

  function text(value) {
    if (value == null) return '';
    if (typeof value === 'object' && ('zh' in value || 'en' in value)) return value[language] || value.zh || value.en || '';
    return String(value);
  }

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }

  function pageText(value) {
    const pages = Array.isArray(value) ? value : [value];
    return pages.filter(Boolean).map((page) => `${copy.slide}${page}${copy.slideSuffix}`).join(', ');
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

  function sourceTypeLabel(value) {
    if (language === 'en') return value || 'XCMG ARC internal presentation';
    if (/EDA/i.test(value || '')) return 'PPT引用的EDA数据与内部分析';
    if (/transport|regulatory/i.test(value || '')) return '内部运输测算与法规摘要';
    if (/use-case|market observation|customer/i.test(value || '')) return '内部市场与工况调研';
    if (/specification|configuration/i.test(value || '')) return '历史参数与配置对比';
    if (/internal evaluation/i.test(value || '')) return '历史内部实机评价';
    if (/presentation/i.test(value || '')) return 'XCMG ARC内部PPT';
    return 'XCMG ARC内部资料';
  }

  function fieldGroup(metric) {
    if (metric === 'safety_systems') return copy.safety;
    if (/corrosion|temperature/.test(metric)) return copy.reliability;
    if (/travel|inching|grading/.test(metric)) return copy.control;
    if (/seat|hvac|space|hmi/.test(metric)) return copy.comfort;
    return copy.service;
  }

  function makeSection(id, title, subtitle, source) {
    const section = document.createElement('section');
    section.id = id;
    section.className = 'pptSection';
    section.innerHTML = `<div class="pptSectionHeader"><div><h2>${escapeHtml(title)}</h2><p class="sourceCaveat">${escapeHtml(subtitle)}</p></div><div class="pptSourceMeta"><b>${escapeHtml(copy.source)}</b>${escapeHtml(source)}</div></div>`;
    return section;
  }

  function evidenceButton(slide, evidenceId, label) {
    const idAttr = evidenceId ? ` data-evidence-id="${escapeHtml(Array.isArray(evidenceId) ? evidenceId[0] : evidenceId)}"` : '';
    return `<button type="button" class="evidenceTrigger" data-slide="${escapeHtml(Array.isArray(slide) ? slide[0] : slide)}"${idAttr}>${escapeHtml(label || copy.evidence)}</button>`;
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
      return `<div class="transportRow${item.id === 'historical_pro' ? ' historical' : ''}"><strong>${escapeHtml(text(item.label))}</strong><div class="transportTrack"><span style="width:${width.toFixed(1)}%"></span></div><div class="transportNumbers"><b>${item.equipped_kg.toLocaleString()} kg</b>${copy.baseMass} ${item.base_kg.toLocaleString()} kg</div></div>`;
    }).join('');
    section.insertAdjacentHTML('beforeend', `
      <p class="scopeBoundary">${escapeHtml(copy.scoringBoundary)}</p>
      <div class="marketDecisionGrid">
        <div class="pptModule">
          <div class="pptModuleTitle"><span>${escapeHtml(copy.volumeTitle)}</span>${evidenceButton(48, 'ev-market-volume')}</div>
          <div class="volumeSeries" role="img" aria-label="${escapeHtml(copy.volumeTitle)}">${volumes}</div>
          <div class="shareStrip"><div class="shareStripHead"><span>${escapeHtml(copy.shareTitle)}</span><b>${view.market.leading_share.value}%</b></div><div class="shareBar"><span></span></div><div class="brandNames"><span>${escapeHtml(copy.shareNote)}</span></div></div>
        </div>
        <div class="pptModule">
          <div class="pptModuleTitle"><span>${escapeHtml(copy.customerTitle)}</span>${evidenceButton(49, 'ev-customer-mix')}</div>
          <div class="customerMix" aria-label="${escapeHtml(copy.customerTitle)}">${customers}</div>
          <ul class="customerLegend">${customerLegend}</ul>
          <p class="sourceCaveat">${escapeHtml(text(view.market.customer_mix_note))}</p>
          <h3 class="pptModuleTitle"><span>${escapeHtml(copy.purchaseLogic)}</span></h3>
          <ul class="purchaseLogic">${logic}</ul>
        </div>
      </div>
      <div class="transportCompare">
        <div class="pptModuleTitle"><span>${escapeHtml(copy.transportTitle)}</span>${evidenceButton(49, 'ev-transport-regulation')}</div>
        <div class="transportRows">${transports}</div>
        <p class="sourceCaveat">${escapeHtml(copy.historicalPlan)}</p>
      </div>`);
    return section;
  }

  function renderScenarioBody(record) {
    const needs = text(record.needs);
    const steps = text(record.steps);
    const needsList = (Array.isArray(needs) ? needs : record.needs[language] || record.needs.zh || []).map((item) => `<li>${escapeHtml(item)}</li>`).join('');
    const stepsList = (Array.isArray(steps) ? steps : record.steps[language] || record.steps.zh || []).map((item) => `<li>${escapeHtml(item)}</li>`).join('');
    const key = findingKey(record.finding_status);
    return `
      <figure class="scenarioMedia"><img src="ppt-integration-demo/${escapeHtml(record.image)}" alt="${escapeHtml(text(record.title))}"><figcaption>${escapeHtml(text(record.title))} · ${escapeHtml(pageText(record.source_slide))}</figcaption></figure>
      <div class="scenarioBody">
        <div class="scenarioHead"><h3>${escapeHtml(text(record.title))}</h3><span class="scenarioStatus status-${key}">${escapeHtml(findingLabel(record.finding_status))}</span></div>
        <dl class="scenarioFacts">
          <div class="scenarioFact"><dt>${escapeHtml(copy.customer)}</dt><dd>${escapeHtml(text(record.customer))}</dd></div>
          <div class="scenarioFact"><dt>${escapeHtml(copy.needs)}</dt><dd><ul>${needsList}</ul></dd></div>
          <div class="scenarioFact"><dt>${escapeHtml(copy.steps)}</dt><dd><ol>${stepsList}</ol></dd></div>
          <div class="scenarioFact"><dt>${escapeHtml(copy.finding)}</dt><dd class="scenarioFinding">${escapeHtml(text(record.conclusion))}</dd></div>
        </dl>
        ${evidenceButton(record.source_slide, record.evidence_id)}
      </div>`;
  }

  function renderScenarios(records) {
    const section = makeSection('ppt-scenarios', copy.scenarioTitle, copy.scenarioSubtitle, copy.sourcePages);
    const tabs = records.map((record, index) => `<button type="button" role="tab" id="scenario-tab-${index}" aria-controls="scenario-stage" aria-selected="${index === 0}" data-scenario-index="${index}">${escapeHtml(text(record.title))}</button>`).join('');
    const indexRows = records.map((record) => `<tr><td>${escapeHtml(text(record.title))}</td><td><span class="scenarioStatus status-${findingKey(record.finding_status)}">${escapeHtml(findingLabel(record.finding_status))}</span></td><td>${escapeHtml(text(record.conclusion))}</td><td>${evidenceButton(record.source_slide, record.evidence_id, pageText(record.source_slide))}</td></tr>`).join('');
    section.insertAdjacentHTML('beforeend', `
      <div class="scenarioTabs" role="tablist" aria-label="${escapeHtml(copy.scenarioTitle)}">${tabs}</div>
      <div class="scenarioStage" id="scenario-stage" role="tabpanel" aria-live="polite">${renderScenarioBody(records[0])}</div>
      <details class="mobileDisclosure pptDisclosure" open data-mobile-open="false"><summary>${escapeHtml(copy.scenarioIndex)}</summary><div class="scenarioIndex"><table><thead><tr><th>${escapeHtml(copy.workCondition)}</th><th>${escapeHtml(copy.status)}</th><th>${escapeHtml(copy.keyFinding)}</th><th>${escapeHtml(copy.page)}</th></tr></thead><tbody>${indexRows}</tbody></table></div></details>`);
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
      return `<tr class="metric-${escapeHtml(metric.status)}"><th>${escapeHtml(text(metric.name))}</th>${values}<td class="metricFinding">${escapeHtml(text(metric.finding))}</td><td>${evidenceButton(metric.source_slide, '', pageText(metric.source_slide))}</td></tr>`;
    }).join('');
    const configRows = view.paper_comparison.configuration_findings.map((item) => `<div class="configRow"><b>${escapeHtml(text(item.label))}</b><strong>${escapeHtml(text(item.xcmg))}</strong><span>${escapeHtml(text(item.comparison))}</span>${evidenceButton(item.source_slide, '', pageText(item.source_slide))}</div>`).join('');
    section.insertAdjacentHTML('beforeend', `
      <p class="scopeBoundary">${escapeHtml(copy.paperBoundary)}</p>
      <details class="mobileDisclosure pptDisclosure" open data-mobile-open="false"><summary>${escapeHtml(copy.fullPaper)}</summary><div class="comparisonMatrix"><table><thead><tr><th>${escapeHtml(copy.metric)}</th>${headerModels}<th>${escapeHtml(copy.findingColumn)}</th><th>${escapeHtml(copy.page)}</th></tr></thead><tbody>${rows}</tbody></table></div></details>
      <div class="pptModuleTitle"><span>${escapeHtml(copy.configurationTitle)}</span></div>
      <div class="configMatrix">${configRows}</div>`);
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
      return `<tr><td>${escapeHtml(fieldGroup(record.metric))}</td><td><b>${escapeHtml(metricName)}</b></td><td>${escapeHtml(text(record.conclusion))}</td><td><span class="scenarioStatus status-${key}">${escapeHtml(copy[key])}</span></td><td><span class="validationText">${escapeHtml(validation)}</span></td><td>${evidenceButton(record.source_slide, record.evidence_id, pageText(record.source_slide))}</td></tr>`;
    }).join('');
    section.insertAdjacentHTML('beforeend', `
      <p class="scopeBoundary">${escapeHtml(copy.fieldBoundary)}</p>
      <div class="fieldSummary">${summary}</div>
      <details class="mobileDisclosure pptDisclosure" open data-mobile-open="false"><summary>${escapeHtml(copy.fullField)}</summary><div class="fieldMatrix"><table><thead><tr><th>${escapeHtml(copy.dimension)}</th><th>${escapeHtml(copy.metric)}</th><th>${escapeHtml(copy.conclusion)}</th><th>${escapeHtml(copy.status)}</th><th>${escapeHtml(copy.validation)}</th><th>${escapeHtml(copy.page)}</th></tr></thead><tbody>${rows}</tbody></table></div></details>`);
    return section;
  }

  function renderActions(roadmap, portfolio, slides) {
    const section = makeSection('ppt-actions', copy.actionTitle, copy.actionSubtitle, copy.source6768);
    const rows = roadmap.map((record) => `<div class="roadmapRow" data-priority="${escapeHtml(record.priority)}"><span class="roadmapPriority">${escapeHtml(record.priority)}</span><span class="roadmapTopic">${escapeHtml(text(roadmapTopics[record.id]) || record.id)}</span><span class="roadmapAction">${escapeHtml(text(record.action))}</span><span class="roadmapValidation">${escapeHtml(copy.verifyRequired)}</span>${evidenceButton(record.source_slide, '', pageText(record.source_slide))}</div>`).join('');
    const portfolioGap = portfolio.find((record) => record.id === 'portfolio-current-gap');
    const positioning = portfolio.find((record) => record.id === 'portfolio-positioning');
    const target = portfolio.find((record) => record.id === 'portfolio-historical-target');
    const evidenceButtons = slides.map((record) => `<button type="button" data-slide="${record.source_slide}"><b>${escapeHtml(pageText(record.source_slide))}</b>${escapeHtml(text(record[language]?.title || record.zh?.title || record.conclusion))}</button>`).join('');
    section.insertAdjacentHTML('beforeend', `
      <p class="scopeBoundary">${escapeHtml(copy.actionBoundary)}</p>
      <div class="roadmapTable">${rows}</div>
      <div class="portfolioNote">
        <div><b>${escapeHtml(copy.portfolio)}</b><p>${escapeHtml(text(portfolioGap?.conclusion))}</p>${evidenceButton(portfolioGap?.source_slide || 67, portfolioGap?.evidence_id)}</div>
        <div><b>${escapeHtml(copy.historicalPositioning)}</b><p>${escapeHtml([text(positioning?.conclusion), text(target?.conclusion)].filter(Boolean).join(' '))}</p>${evidenceButton(68, 'ev-positioning-target')}</div>
      </div>
      <details class="evidenceIndex"><summary>${escapeHtml(copy.evidenceIndex)}</summary><div class="evidenceButtons">${evidenceButtons}</div></details>`);
    return section;
  }

  function installNavigation() {
    const menu = document.querySelector('.navMenu');
    const raw = menu?.querySelector('a[href="#raw"]');
    if (!menu || !raw) return;
    const links = [
      ['ppt-integration-demo/excavator-overview.html', copy.category, 'navCategoryLink'],
      ['#ppt-market', copy.marketNav, 'navPptLink'],
      ['#ppt-scenarios', copy.scenarioNav, 'navPptLink'],
      ['#ppt-paper', copy.paperNav, 'navPptLink'],
      ['#ppt-field', copy.fieldNav, 'navPptLink'],
      ['#ppt-actions', copy.actionNav, 'navPptLink']
    ];
    links.forEach(([href, label, className]) => {
      const link = document.createElement('a');
      link.href = href;
      link.className = className;
      link.textContent = label;
      raw.before(link);
      link.addEventListener('click', () => {
        if (window.matchMedia('(max-width:1200px)').matches) {
          menu.classList.remove('open');
          const toggle = document.querySelector('.navToggle');
          toggle?.setAttribute('aria-expanded', 'false');
        }
      });
    });
  }

  function installDrawer() {
    document.body.insertAdjacentHTML('beforeend', `
      <div class="evidenceOverlay" aria-hidden="true"></div>
      <aside class="evidenceDrawer" aria-hidden="true" aria-labelledby="evidence-drawer-title">
        <div class="evidenceDrawerHead"><h2 id="evidence-drawer-title">${escapeHtml(copy.drawerTitle)}</h2><button type="button" class="drawerClose" aria-label="${escapeHtml(copy.close)}">×</button></div>
        <div class="evidenceDrawerBody"></div>
      </aside>`);
    document.querySelector('.drawerClose').addEventListener('click', closeDrawer);
    document.querySelector('.evidenceOverlay').addEventListener('click', closeDrawer);
    document.addEventListener('keydown', (event) => { if (event.key === 'Escape') closeDrawer(); });
    document.addEventListener('click', (event) => {
      const button = event.target.closest('[data-slide]');
      if (!button || button.closest('.volumeColumn')) return;
      const slide = Number(button.dataset.slide);
      if (slide) openEvidence(slide, button.dataset.evidenceId || '');
    });
  }

  function openEvidence(slide, evidenceId) {
    const drawer = document.querySelector('.evidenceDrawer');
    const overlay = document.querySelector('.evidenceOverlay');
    const body = drawer.querySelector('.evidenceDrawerBody');
    const slideRecord = state.data.slides.records.find((record) => Number(record.source_slide) === Number(slide));
    const evidence = state.data.evidence.records.find((record) => record.id === evidenceId) || state.data.evidence.records.find((record) => (Array.isArray(record.source_slide) ? record.source_slide : [record.source_slide]).includes(slide));
    if (!slideRecord) return;
    const conclusion = text(evidence?.conclusion || slideRecord.conclusion);
    const title = text(slideRecord[language]?.title || slideRecord.zh?.title || slideRecord.conclusion);
    const raw = slideRecord.zh?.raw_text || (slideRecord.zh?.paragraphs || []).join('\n');
    const sourceType = evidence?.source_type || slideRecord.source_type;
    const asOf = evidence?.as_of_date || slideRecord.as_of_date;
    const temporal = statusLabel(evidence?.status || slideRecord.status);
    const validation = validationLabel(evidence?.validation_status || slideRecord.validation_status);
    body.innerHTML = `
      <img class="evidenceSlideImage" src="ppt-integration-demo/${escapeHtml(slideRecord.thumbnail)}" alt="${escapeHtml(title)}">
      <dl class="evidenceMeta">
        <div><dt>${escapeHtml(copy.page)}</dt><dd>${escapeHtml(pageText(slide))}</dd></div>
        <div><dt>${escapeHtml(copy.sourceType)}</dt><dd>${escapeHtml(sourceTypeLabel(sourceType))}</dd></div>
        <div><dt>${escapeHtml(copy.dataDate)}</dt><dd>${escapeHtml(asOf)}</dd></div>
        <div><dt>${escapeHtml(copy.temporalStatus)}</dt><dd>${escapeHtml(temporal)}</dd></div>
        <div><dt>${escapeHtml(copy.validationStatus)}</dt><dd>${escapeHtml(validation)}</dd></div>
      </dl>
      <div class="evidenceConclusion"><b>${escapeHtml(title)}</b><br>${escapeHtml(conclusion)}</div>
      <label class="evidenceRawLabel" for="evidence-raw">${escapeHtml(copy.rawText)}</label>
      <textarea id="evidence-raw" class="evidenceRaw" readonly></textarea>`;
    body.querySelector('.evidenceRaw').value = raw;
    state.lastFocus = document.activeElement;
    drawer.classList.add('open');
    overlay.classList.add('open');
    drawer.setAttribute('aria-hidden', 'false');
    overlay.setAttribute('aria-hidden', 'false');
    document.body.classList.add('evidenceOpen');
    drawer.querySelector('.drawerClose').focus();
  }

  function closeDrawer() {
    const drawer = document.querySelector('.evidenceDrawer');
    const overlay = document.querySelector('.evidenceOverlay');
    if (!drawer?.classList.contains('open')) return;
    drawer.classList.remove('open');
    overlay.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
    overlay.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('evidenceOpen');
    state.lastFocus?.focus?.();
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
      const hero = document.querySelector('.hero');
      const ribbon = document.createElement('div');
      ribbon.className = 'internalRibbon';
      ribbon.innerHTML = `<b>${escapeHtml(copy.internal)}</b><span>${escapeHtml(copy.internalNote)}</span>`;
      hero?.after(ribbon);

      const market = renderMarket(view);
      document.querySelector('#summary')?.after(market);

      const scenarios = renderScenarios(state.data.tonnage.records.filter((record) => record.id.startsWith('scenario-')));
      const paper = renderPaper(view);
      document.querySelector('#conditions')?.after(scenarios, paper);

      const field = renderField(state.data.fieldEvaluation.records);
      const actions = renderActions(state.data.roadmap.records, state.data.portfolio.records, state.data.slides.records);
      document.querySelector('#cond6')?.after(field, actions);

      installNavigation();
      installDrawer();
      setupSupplementDisclosures();
      window.XCMGPPTIntegration = {language, data: state.data, openEvidence};
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
