(function () {
  'use strict';

  const query = new URLSearchParams(window.location.search);
  let stored = '';
  try { stored = window.localStorage.getItem('xcmg-benchmark-language') || ''; } catch (_) { stored = ''; }
  const language = query.get('lang') === 'en' || (query.get('lang') !== 'zh' && stored === 'en') ? 'en' : 'zh';
  let records = [];

  const englishStatic = new Map([
    ['北美挖掘机整体分析', 'North American Excavator Analysis'],
    ['集中呈现不能归入单一吨级的行业周期、竞争格局、战略标杆和核心吨级结构；具体参数、配置和工况仍在对应吨级看板中分析。', 'Combines the market cycle, competitive structure, strategic benchmarks and tonnage priorities that sit above any one class. Specifications, equipment and applications remain in the corresponding benchmark dashboards.'],
    ['数据口径：', 'Data basis:'],
    ['市场数据按形成时间展示，历史判断和预测不视为当前事实。', 'Market data retains its original time basis; historical assessments and forecasts are not presented as current facts.'],
    ['整体分析概览', 'Overall Analysis'],
    ['2025市场规模历史预测', 'Historical 2025 market forecast'], ['台', 'units'],
    ['0–10吨前十品牌合计', 'Top-ten share, 0-10 t'], ['10吨以上前十品牌合计', 'Top-ten share, above 10 t'],
    ['历史市场集中度', 'Historical market concentration'], ['XCMG历史排名', 'Historical XCMG rank'], ['0–10吨 / 10吨以上', '0-10 t / above 10 t'],
    ['行业周期与竞争格局', 'Industry Cycle and Competitive Structure'],
    ['需求调整、品牌集中度和吨级结构共同决定产品对标优先级。', 'Demand normalization, brand concentration and tonnage mix jointly determine benchmark priorities.'],
    ['品牌集中度', 'Brand concentration'], ['前十品牌合计', 'Combined top-ten share'], ['10吨以上', 'Above 10 t'],
    ['成熟品牌在产品、渠道、融资、租赁和残值体系上形成综合竞争门槛。', 'Established brands create a combined barrier through product depth, distribution, finance, rental support and residual value.'],
    ['XCMG历史市场位置', 'Historical XCMG market position'], ['第19', 'No. 19'], ['第18', 'No. 18'], ['历史市场快照', 'Historical market snapshot'],
    ['品牌位置需结合最新销量、经销覆盖和重点客户渗透情况持续更新。', 'Refresh brand position using current sales, dealer coverage and penetration of priority accounts.'],
    ['宏观约束与机会', 'Macro Constraints and Opportunities'],
    ['只保留会影响产品规划、区域投入和市场准入的因素。', 'Focus on factors that change product planning, regional investment or market access.'],
    ['战略标杆', 'Strategic Benchmarks'],
    ['微小挖与中大挖采用不同标杆，不把一个品牌的优势机械复制到所有吨级。', 'Use different benchmarks for compact and mid/large excavators rather than copying one brand across every class.'],
    ['核心吨级结构', 'Core Tonnage Structure'],
    ['用于确定对标资产建设顺序，销量与降幅需按最新AEM/EDA数据复核。', 'Use the structure to prioritize benchmark assets; refresh volume and decline rates with current AEM/EDA data.'],
    ['微挖', 'Mini excavators'], ['0–4吨', '0-4 t'], ['核心：3–4、1–2、2–3吨', 'Core: 3-4, 1-2 and 2-3 t'],
    ['小挖', 'Compact excavators'], ['4–10吨', '4-10 t'], ['核心：5–6、4–5吨', 'Core: 5-6 and 4-5 t'],
    ['中挖', 'Mid-size excavators'], ['10–33吨', '10-33 t'], ['核心：21–24、14–16、24–28吨', 'Core: 21-24, 14-16 and 24-28 t'],
    ['大挖', 'Large excavators'], ['33吨以上', 'Above 33 t'], ['核心：33–40、40–50吨', 'Core: 33-40 and 40-50 t']
  ]);

  const marketCycle = [
    {year: '2021', value: 83030}, {year: '2022', value: 114106}, {year: '2023', value: 132013},
    {year: '2024', value: 98632}, {year: '2025E', value: 90741}
  ];

  const implications = {
    industry_cycle: {
      zh: '市场从补库存高点转入调整后，单纯依靠低采购价更难建立优势。产品应同时证明作业效率、停机风险、维修便利性和残值。',
      en: 'As the market normalizes from the restocking peak, low acquisition price alone is less defensible. Products must also prove productivity, downtime risk, serviceability and residual value.'
    },
    product_structure: {
      zh: '2024年微挖与小挖合计约77%，应优先完善高频吨级、租赁配置包和通用属具体系，再向中大挖复制方法。',
      en: 'Mini and compact excavators represented about 77% in 2024. Prioritize high-frequency classes, rental packages and common attachments before scaling the method upward.'
    },
    macro_social: {
      zh: '南部及东南部住宅、市政和公用事业需求应成为样机投放、用户诊断和属具验证的重点区域。',
      en: 'Southern and southeastern residential, municipal and utility demand should guide prototype placement, user clinics and attachment validation.'
    },
    technology: {
      zh: '重点不是堆叠功能，而是本地工况标定、辅助施工能力、远程管理和可靠的人机交互。',
      en: 'The priority is not feature count, but local application tuning, grade-assist capability, telematics and dependable human-machine interaction.'
    },
    economy_rental: {
      zh: '租赁客户更关注周转率、非专业机手适应性、快速保养、统一附件和二手机残值。',
      en: 'Rental customers emphasize utilization, novice-operator usability, fast service, attachment commonality and residual value.'
    },
    emissions: {
      zh: '新能源产品应按州法规、客户类型、补能条件和作业周期分层导入，避免全国统一假设。',
      en: 'Electrified products should be introduced by state, customer type, charging conditions and duty cycle rather than one nationwide assumption.'
    },
    trade_policy: {
      zh: '关税、认证和本地采购变化会重塑整机成本与交付路径，应同步评估零部件本地化和合规替代方案。',
      en: 'Tariffs, certification and local-content changes can reshape landed cost and delivery paths; component localization and compliant alternatives should be evaluated together.'
    },
    macro_summary: {
      zh: '产品组合决策应把区域需求、客户结构、法规准入、产品差距和渠道能力放在同一张决策表中。',
      en: 'Portfolio decisions should combine regional demand, customer mix, market access, product gaps and channel capability in one decision model.'
    }
  };

  const benchmarkDetails = {
    benchmark_kubota: {
      zh: ['液压微操与复合动作', '短尾/常规尾型谱覆盖', '可靠性与二手机残值', '经销与客户使用路径'],
      en: ['Hydraulic inching and combined motion', 'Short-tail and conventional-tail portfolio', 'Reliability and residual value', 'Dealer and customer journey']
    },
    benchmark_caterpillar: {
      zh: ['可靠性与全生命周期成本', '经销服务与备件体系', '金融和租赁支持', '中大挖平台化能力'],
      en: ['Reliability and lifecycle cost', 'Dealer service and parts system', 'Finance and rental support', 'Mid/large platform capability']
    }
  };

  const tonnageFocus = [
    {group: {zh: '微挖', en: 'Mini'}, range: '0-4 t', share: 40, core: {zh: '3-4、1-2、2-3吨', en: '3-4, 1-2 and 2-3 t'}, focus: {zh: '运输、狭窄施工、租赁通用性', en: 'Transport, confined work and rental versatility'}},
    {group: {zh: '小挖', en: 'Compact'}, range: '4-10 t', share: 37, core: {zh: '5-6、4-5吨', en: '5-6 and 4-5 t'}, focus: {zh: '效率、属具覆盖与稳定性', en: 'Productivity, attachments and stability'}},
    {group: {zh: '中挖', en: 'Mid-size'}, range: '10-33 t', share: 16, core: {zh: '21-24、14-16、24-28吨', en: '21-24, 14-16 and 24-28 t'}, focus: {zh: '油耗、产能与可靠性', en: 'Fuel use, output and reliability'}},
    {group: {zh: '大挖', en: 'Large'}, range: '>33 t', share: 7, core: {zh: '33-40、40-50吨', en: '33-40 and 40-50 t'}, focus: {zh: '重载循环、矿山适配与TCO', en: 'Heavy cycles, quarry fit and TCO'}}
  ];

  function text(value) {
    if (value == null) return '';
    if (typeof value === 'object' && ('zh' in value || 'en' in value)) return value[language] || value.zh || value.en || '';
    return String(value);
  }

  function narrative(value) {
    let output = text(value);
    const replacements = language === 'en'
      ? [[/The source/gi, 'The historical analysis'], [/the source/gi, 'the historical analysis']]
      : [[/资料认为/g, '历史分析认为'], [/资料判断/g, '历史分析判断'], [/资料显示/g, '历史数据表明'], [/资料选择/g, '标杆分析选择'], [/资料按/g, '产品组合分析按'], [/资料/g, '历史分析']];
    replacements.forEach(([pattern, replacement]) => { output = output.replace(pattern, replacement); });
    return output;
  }

  function esc(value) {
    return String(value == null ? '' : value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }

  function localizeStatic() {
    if (language !== 'en') return;
    document.title = 'Excavator Analysis | XCMG ARC INTERNAL';
    const walker = document.createTreeWalker(document.querySelector('main'), NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach((node) => {
      const trimmed = (node.nodeValue || '').trim();
      if (englishStatic.has(trimmed)) node.nodeValue = node.nodeValue.replace(trimmed, englishStatic.get(trimmed));
    });
  }

  function forceEnglishStatic() {
    if (language !== 'en') return;
    const set = (selector, value) => { const element = document.querySelector(selector); if (element) element.textContent = value; };
    set('.navTitle', 'Excavator Overall Analysis');
    set('.navToggle', 'Page navigation');
    set('.mobileTop', 'Top');
    set('#page-nav .home', 'Return to the 3-4 t benchmark');
    set('.backTop', 'Back to top');
    set('.hero h1', 'North American Excavator Analysis');
    set('.heroDescription', 'Combines the market cycle, competitive structure, strategic benchmarks and tonnage priorities that sit above any one class. Specifications, equipment and applications remain in the corresponding benchmark dashboards.');
    const heroNote = document.querySelector('.heroText .methodNote');
    if (heroNote) heroNote.innerHTML = '<b>Data basis:</b> Market data retains its original time basis; historical assessments and forecasts are not presented as current facts.';
    set('#overview-summary h2', 'Overall Analysis');
    const summaryKpis = document.querySelectorAll('#overview-summary .kpi');
    const summaryCopy = [
      ['Historical 2025 market forecast', 'units'],
      ['Top-ten share, 0-10 t', 'Historical market concentration'],
      ['Top-ten share, above 10 t', 'Historical market concentration'],
      ['Historical XCMG rank', '0-10 t / above 10 t']
    ];
    summaryKpis.forEach((item, index) => { const spans = item.querySelectorAll('span'); if (spans[0]) spans[0].textContent = summaryCopy[index][0]; if (spans[1]) spans[1].textContent = summaryCopy[index][1]; });
    set('#industry h2', 'Industry Cycle and Competitive Structure');
    set('#industry > .methodNote', 'Demand normalization, brand concentration and tonnage mix jointly determine benchmark priorities.');
    const structurePanels = document.querySelectorAll('#industry .marketStructurePanel');
    if (structurePanels[0]) {
      set('#industry .marketStructurePanel:first-of-type .pptModuleTitle span', 'Brand concentration');
      const labels = structurePanels[0].querySelectorAll('.concentrationRow');
      if (labels[0]) { labels[0].querySelector('b').textContent = '0-10 t'; labels[0].querySelector('span').textContent = 'Combined top-ten share'; }
      if (labels[1]) { labels[1].querySelector('b').textContent = 'Above 10 t'; labels[1].querySelector('span').textContent = 'Combined top-ten share'; }
      structurePanels[0].querySelector('.sourceCaveat').textContent = 'Established brands create a combined barrier through product depth, distribution, finance, rental support and residual value.';
    }
    if (structurePanels[1]) {
      structurePanels[1].querySelector('.pptModuleTitle span').textContent = 'Historical XCMG market position';
      const snapshots = structurePanels[1].querySelectorAll('.rankSnapshots > div');
      if (snapshots[0]) { snapshots[0].querySelector('span').textContent = '0-10 t'; snapshots[0].querySelector('b').textContent = 'No. 19'; snapshots[0].querySelector('small').textContent = 'Historical market snapshot'; }
      if (snapshots[1]) { snapshots[1].querySelector('span').textContent = 'Above 10 t'; snapshots[1].querySelector('b').textContent = 'No. 18'; snapshots[1].querySelector('small').textContent = 'Historical market snapshot'; }
      structurePanels[1].querySelector('.sourceCaveat').textContent = 'Refresh brand position using current sales, dealer coverage and penetration of priority accounts.';
    }
    set('#macro h2', 'Macro Constraints and Opportunities');
    set('#macro > .methodNote', 'Focus on factors that change product planning, regional investment or market access.');
    set('#benchmarks h2', 'Strategic Benchmarks');
    set('#benchmarks > .methodNote', 'Use different benchmarks for compact and mid/large excavators rather than copying one brand across every class.');
    set('#tonnage h2', 'Core Tonnage Structure');
    set('#tonnage > .methodNote', 'Use the structure to prioritize benchmark assets; refresh volume and decline rates with current AEM/EDA data.');
    const tonnageKpis = document.querySelectorAll('#tonnage .tonnageKpis .kpi');
    const tonnageCopy = [
      ['Mini excavators', '0-4 t', 'Core: 3-4, 1-2 and 2-3 t'],
      ['Compact excavators', '4-10 t', 'Core: 5-6 and 4-5 t'],
      ['Mid-size excavators', '10-33 t', 'Core: 21-24, 14-16 and 24-28 t'],
      ['Large excavators', 'Above 33 t', 'Core: 33-40 and 40-50 t']
    ];
    tonnageKpis.forEach((item, index) => { const spans = item.querySelectorAll('span'); const bold = item.querySelector('b'); if (spans[0]) spans[0].textContent = tonnageCopy[index][0]; if (bold) bold.textContent = tonnageCopy[index][1]; if (spans[1]) spans[1].textContent = tonnageCopy[index][2]; });
  }

  function renderThesis() {
    const labels = language === 'en'
      ? [
        ['Demand center', 'Mini + compact', 'Prioritize high-frequency classes, rental duty and transport-constrained applications'],
        ['Competitive logic', 'Product + channel + residual value', 'System capability matters more than a single leading specification'],
        ['XCMG sequence', 'Validate → improve → platformize', 'Close hard application gaps first, then build repeatable product packages']
      ]
      : [
        ['需求重心', '微挖 + 小挖', '优先覆盖高频吨级、租赁任务和受运输约束的典型工况'],
        ['竞争逻辑', '产品 + 渠道 + 残值', '体系能力比单项参数领先更能形成持续竞争优势'],
        ['XCMG顺序', '验证 → 改进 → 平台化', '先补真实工况硬差距，再形成可复制的产品配置包']
      ];
    document.querySelector('#overview-thesis').innerHTML = `<div class="overviewThesis">${labels.map((item) => `<article><span>${esc(item[0])}</span><b>${esc(item[1])}</b><p>${esc(item[2])}</p></article>`).join('')}</div>`;
  }

  function renderCycleChart() {
    const max = Math.max(...marketCycle.map((item) => item.value));
    const peak = marketCycle.find((item) => item.year === '2023').value;
    const current = marketCycle[marketCycle.length - 1].value;
    const decline = ((peak - current) / peak * 100).toFixed(1);
    const bars = marketCycle.map((item) => `<div class="cycleBar${item.year.endsWith('E') ? ' estimate' : ''}"><i style="height:${(item.value / max * 100).toFixed(1)}%"></i><b>${item.value.toLocaleString(language === 'en' ? 'en-US' : 'zh-CN')}</b><span>${item.year}</span></div>`).join('');
    const title = language === 'en' ? 'US construction-equipment market cycle' : '美国工程机械市场周期';
    const detail = language === 'en'
      ? `The historical series peaks at 132,013 units in 2023 and records 90,741 units for 2025E, a ${decline}% reduction. Benchmarking should therefore emphasize lifecycle value rather than expansion-era volume assumptions.`
      : `历史序列在2023年达到132,013台高点，2025E记录为90,741台，较高点下降${decline}%。对标重点应从扩张期的销量假设转向全生命周期价值。`;
    document.querySelector('#market-cycle-chart').innerHTML = `<div class="cycleChart"><div><span class="moduleLabel">${language === 'en' ? 'Historical market series' : '历史市场序列'}</span><h3>${esc(title)}</h3><div class="cycleBars">${bars}</div></div><aside><b>${esc(decline)}%</b><span>${language === 'en' ? '2023 peak to 2025E' : '2023高点至2025E'}</span><p>${esc(detail)}</p></aside></div>`;
  }

  function decisionRow(record) {
    return `<article class="overviewDecisionRow"><div class="decisionRowTitle"><span>${language === 'en' ? 'Decision signal' : '决策信号'}</span><h3>${esc(text(record.title))}</h3></div><div class="decisionRowBody"><p>${esc(narrative(record.conclusion))}</p><div><b>${language === 'en' ? 'Product implication' : '产品含义'}</b><span>${esc(text(implications[record.metric]))}</span></div></div></article>`;
  }

  function renderBenchmark(record) {
    const points = benchmarkDetails[record.metric]?.[language] || benchmarkDetails[record.metric]?.zh || [];
    return `<article class="panel benchmarkBand"><span class="moduleLabel">${language === 'en' ? 'Benchmark system' : '标杆体系'}</span><h3>${esc(text(record.title))}</h3><p>${esc(narrative(record.conclusion))}</p><ul>${points.map((item) => `<li>${esc(item)}</li>`).join('')}</ul></article>`;
  }

  function renderTonnageStructure() {
    const title = language === 'en' ? '2024 historical mix and benchmark focus' : '2024历史结构与对标重点';
    document.querySelector('#tonnage-row').innerHTML = `<div class="tonnagePriorityHeader"><h3>${esc(title)}</h3><span>${language === 'en' ? 'Share of broad excavator groups' : '挖掘机大类结构占比'}</span></div><div class="tonnagePriorityGrid">${tonnageFocus.map((item) => `<article><div class="tonnageShare"><b>${item.share}%</b><i><em style="width:${item.share}%"></em></i></div><h3>${esc(text(item.group))} <small>${esc(item.range)}</small></h3><p><b>${language === 'en' ? 'Core classes:' : '核心吨级：'}</b>${esc(text(item.core))}</p><p><b>${language === 'en' ? 'Benchmark focus:' : '对标重点：'}</b>${esc(text(item.focus))}</p></article>`).join('')}</div>`;
  }

  function render() {
    const byTopic = Object.fromEntries(records.map((record) => [record.metric, record]));
    renderThesis();
    renderCycleChart();
    document.querySelector('#industry-rows').innerHTML = ['industry_cycle', 'product_structure'].map((topic) => decisionRow(byTopic[topic])).join('');
    document.querySelector('#macro-rows').innerHTML = ['macro_social', 'technology', 'economy_rental', 'emissions', 'trade_policy', 'macro_summary'].map((topic) => decisionRow(byTopic[topic])).join('');
    document.querySelector('#benchmark-bands').innerHTML = ['benchmark_kubota', 'benchmark_caterpillar'].map((topic) => renderBenchmark(byTopic[topic])).join('');
    renderTonnageStructure();
    forceEnglishStatic();
    window.setTimeout(forceEnglishStatic, 0);
  }

  async function init() {
    localizeStatic();
    try {
      const response = await fetch('data/ppt-insights/excavator-overview.json');
      if (!response.ok) throw new Error(String(response.status));
      records = (await response.json()).records;
      render();
    } catch (error) {
      console.error(error);
      document.querySelector('#industry-rows').innerHTML = `<p class="scopeBoundary">${language === 'en' ? 'Overview data could not be loaded. Open this page through the local preview address.' : '整体分析数据未能载入，请通过本地预览地址打开。'}</p>`;
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once: true}); else init();
})();
