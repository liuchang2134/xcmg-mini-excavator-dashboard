(function () {
  'use strict';

  const query = new URLSearchParams(window.location.search);
  let stored = '';
  try { stored = window.localStorage.getItem('xcmg-benchmark-language') || ''; } catch (_) { stored = ''; }
  const language = query.get('lang') === 'en' || (query.get('lang') !== 'zh' && stored === 'en') ? 'en' : 'zh';
  let records = [];
  const ui = {
    zh: {
      raw: '原始记录', material: '模块资料', finding: '研究结论',
      verify: '需按当前市场、政策或产品版本复核'
    },
    en: {
      raw: 'Original record', material: 'Module research material', finding: 'Research finding',
      verify: 'Current market, policy or product-version validation required'
    }
  }[language];

  const englishStatic = new Map([
    ['挖掘机整体分析', 'Excavator Overall Analysis'],
    ['页面导航', 'Page Navigation'],
    ['顶部', 'Top'],
    ['返回3–4吨对标', 'Return to the 3–4 t Benchmark'],
    ['行业周期与竞争格局', 'Industry Cycle and Competitive Landscape'],
    ['宏观约束与机会', 'Macro Constraints and Opportunities'],
    ['战略标杆', 'Strategic Benchmarks'],
    ['核心吨级结构', 'Core Tonnage Structure'],
    ['北美挖掘机整体分析', 'North American Excavator Overall Analysis'],
    ['集中呈现不能归入单一吨级的行业周期、竞争格局、战略标杆和核心吨级结构；具体参数、配置和工况仍在对应吨级看板中分析。', 'Consolidates industry-cycle, competitive-landscape, strategic-benchmark and core-tonnage content that cannot be assigned to one class. Specifications, equipment and applications remain in the corresponding tonnage benchmark.'],
    ['XCMG ARC内部资料：', 'XCMG ARC INTERNAL:'],
    ['市场数字保留PPT原有时间属性，历史判断和预测不视为当前事实。', 'Market figures retain the original PPT time basis; historical assessments and forecasts are not presented as current facts.'],
    ['数据口径：', 'Data basis:'],
    ['市场数据按形成时间展示，历史判断和预测不视为当前事实。', 'Market data is shown on its original time basis; historical assessments and forecasts are not presented as current facts.'],
    ['整体分析概览', 'Overall Analysis Overview'],
    ['2025市场规模历史预测', 'Historical 2025 market forecast'],
    ['台', 'units'],
    ['0–10吨前十品牌合计', 'Top-ten share, 0–10 t'],
    ['历史市场集中度', 'Historical market concentration'],
    ['10吨以上前十品牌合计', 'Top-ten share, above 10 t'],
    ['XCMG历史排名', 'Historical XCMG rank'],
    ['0–10吨 / 10吨以上', '0–10 t / above 10 t'],
    ['需求调整、品牌集中度和吨级结构共同决定产品对标优先级。PPT来源：第9–12页。', 'Demand adjustment, brand concentration and tonnage mix jointly determine benchmarking priority. PPT source: slides 9–12.'],
    ['需求调整、品牌集中度和吨级结构共同决定产品对标优先级。', 'Demand adjustment, brand concentration and tonnage mix jointly determine benchmarking priority.'],
    ['品牌集中度', 'Brand concentration'],
    ['前十品牌合计', 'Combined top-ten share'],
    ['10吨以上', 'Above 10 t'],
    ['成熟品牌在产品、渠道、融资、租赁和残值体系上形成综合竞争门槛。', 'Established brands create a combined competitive barrier through products, distribution, finance, rental support and residual value.'],
    ['XCMG历史市场位置', 'Historical XCMG market position'],
    ['第19', 'No. 19'],
    ['第18', 'No. 18'],
    ['历史市场快照', 'Historical market snapshot'],
    ['品牌位置需结合最新销量、经销覆盖和重点客户渗透情况持续更新。', 'Update brand position using the latest sales, dealer coverage and penetration of priority accounts.'],
    ['竞争集中度与市场格局', 'Competitive concentration and market structure'],
    ['品牌份额与XCMG位置', 'Brand share and XCMG position'],
    ['只保留会影响产品规划、区域投入和市场准入的因素。PPT来源：第3–8页。', 'Retain only factors that affect product planning, regional investment and market access. PPT source: slides 3–8.'],
    ['只保留会影响产品规划、区域投入和市场准入的因素。', 'Retain only factors that affect product planning, regional investment and market access.'],
    ['微小挖与中大挖采用不同标杆，不把一个品牌的优势机械复制到所有吨级。PPT来源：第13–14页。', 'Use different benchmarks for mini/compact and mid/large excavators rather than copying one brand across every tonnage class. PPT source: slides 13–14.'],
    ['微小挖与中大挖采用不同标杆，不把一个品牌的优势机械复制到所有吨级。', 'Use different benchmarks for mini/compact and mid/large excavators rather than copying one brand across every tonnage class.'],
    ['用于确定对标资产建设顺序，销量与降幅需按最新AEM/EDA数据复核。PPT来源：第15页。', 'Use this structure to prioritize benchmark assets. Volumes and declines require the latest AEM/EDA validation. PPT source: slide 15.'],
    ['用于确定对标资产建设顺序，销量与降幅需按最新AEM/EDA数据复核。', 'Use this structure to prioritize benchmark assets. Volumes and declines require the latest AEM/EDA validation.'],
    ['微挖', 'Mini excavators'],
    ['0–4吨', '0–4 t'],
    ['核心：3–4、1–2、2–3吨', 'Core: 3–4, 1–2 and 2–3 t'],
    ['小挖', 'Compact excavators'],
    ['4–10吨', '4–10 t'],
    ['核心：5–6、4–5吨', 'Core: 5–6 and 4–5 t'],
    ['中挖', 'Mid-size excavators'],
    ['10–33吨', '10–33 t'],
    ['核心：21–24、14–16、24–28吨', 'Core: 21–24, 14–16 and 24–28 t'],
    ['大挖', 'Large excavators'],
    ['33吨以上', 'Above 33 t'],
    ['核心：33–40、40–50吨', 'Core: 33–40 and 40–50 t'],
    ['回到页面顶部', 'Return to page top'],
    ['回到顶部', 'Back to top']
  ]);

  function text(value) {
    if (value == null) return '';
    if (typeof value === 'object' && ('zh' in value || 'en' in value)) return value[language] || value.zh || value.en || '';
    return String(value);
  }

  function narrative(value) {
    let output = text(value);
    const replacements = language === 'en' ? [
      [/The source/gi, 'The historical analysis'],
      [/the source/gi, 'the historical analysis'],
      [/The presentation/gi, 'The historical analysis'],
      [/the presentation/gi, 'the historical analysis']
    ] : [
      [/资料认为/g, '行业分析认为'],
      [/资料判断/g, '行业分析判断'],
      [/资料显示/g, '历史数据表明'],
      [/资料把/g, '历史分析把'],
      [/资料选择/g, '标杆分析选择'],
      [/资料按/g, '产品组合分析按']
    ];
    replacements.forEach(([pattern, replacement]) => { output = output.replace(pattern, replacement); });
    return output;
  }

  function esc(value) {
    return String(value == null ? '' : value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }

  function status(value) {
    const labels = {
      historical_macro_observation: {zh: '历史宏观观察', en: 'Historical macro observation'},
      historical_strategic_assessment: {zh: '历史战略判断', en: 'Historical strategic assessment'},
      historical_macro_assessment: {zh: '历史宏观判断', en: 'Historical macro assessment'},
      historical_policy_assessment: {zh: '历史政策判断', en: 'Historical policy assessment'},
      historical_strategic_summary: {zh: '历史战略总结', en: 'Historical strategic summary'},
      historical_forecast: {zh: '历史预测', en: 'Historical forecast'},
      historical_market_fact: {zh: '历史市场事实', en: 'Historical market fact'},
      historical_market_assessment: {zh: '历史市场判断', en: 'Historical market assessment'},
      historical_market_snapshot: {zh: '历史市场快照', en: 'Historical market snapshot'},
      historical_benchmark_rationale: {zh: '历史标杆选择依据', en: 'Historical benchmark rationale'},
      historical_market_structure: {zh: '历史市场结构', en: 'Historical market structure'}
    };
    return text(labels[value]) || ui.verify;
  }

  function localizeStatic() {
    if (language !== 'en') return;
    document.title = 'Excavator Overall Analysis | XCMG ARC INTERNAL';
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach((node) => {
      const trimmed = (node.nodeValue || '').trim();
      if (!englishStatic.has(trimmed)) return;
      node.nodeValue = node.nodeValue.replace(trimmed, englishStatic.get(trimmed));
    });
  }

  function displayDate(value) {
    const source = String(value || '');
    if (language === 'en') return source.replace(/PPT/gi, 'Internal record').replace(/in source/gi, 'in the historical record');
    const translations = {
      '2023 population figures in source': '2023人口数据',
      'PPT 11.14 version': '内部资料版本11.14',
      '2023-2025 figures and forecast in source': '2023–2025数据及预测',
      'PPT 11.14 version; current policy unverified': '内部资料版本11.14 / 当前政策待核验',
      '2025 forecast in source; outcome not validated': '2025历史预测 / 结果待核验',
      '2021-2024 series in source': '2021–2024历史记录序列',
      'Five-year EDA series cited in source': 'EDA五年历史序列',
      '2025 EDA snapshot in source': '2025 EDA市场快照',
      'AEM data cited in source': 'AEM历史数据'
    };
    return translations[source] || source.replace(/PPT/gi, '内部资料').replace(/in source/gi, '历史记录').replace(/cited in source/gi, '历史记录引用');
  }

  function inlineRecord(record, includeConclusion) {
    if (!record) return '';
    const title = text(record.title);
    const raw = language === 'en' ? narrative(record.conclusion) : narrative(record.zh?.raw_text || '');
    return `<article class="inlineEvidenceCard" data-source-slide="${record.source_slide}">
      <figure class="inlineEvidenceVisual"><img src="ppt-integration-demo/${esc(record.thumbnail)}" alt="${esc(title)}"></figure>
      <div class="inlineEvidenceContent">
        <div class="inlineEvidenceTop"><b>${esc(ui.material)}</b><span>${esc(displayDate(record.as_of_date))}</span></div>
        <h4>${esc(title)}</h4>
        ${includeConclusion ? `<p class="inlineEvidenceConclusion"><strong>${esc(ui.finding)}：</strong>${esc(narrative(record.conclusion))}</p>` : ''}
        <div class="inlineEvidenceRaw"><b>${esc(ui.raw)}</b><pre>${esc(raw)}</pre></div>
        <div class="inlineEvidenceMeta"><span>${esc(status(record.status))}</span><span>${esc(ui.verify)}</span></div>
      </div>
    </article>`;
  }

  function row(record) {
    return `<div class="overviewDecisionRow"><h3>${esc(text(record.title))}</h3><p>${esc(narrative(record.conclusion))}</p>${inlineRecord(record, false)}</div>`;
  }

  function render() {
    const byTopic = Object.fromEntries(records.map((record) => [record.metric, record]));
    const industryTopics = ['industry_cycle', 'product_structure'];
    const macroTopics = ['macro_social', 'technology', 'economy_rental', 'emissions', 'trade_policy', 'macro_summary'];
    document.querySelector('#industry-rows').innerHTML = industryTopics.map((topic) => row(byTopic[topic])).join('');
    document.querySelector('#overview-concentration-source').innerHTML = inlineRecord(byTopic.competition_concentration, true);
    document.querySelector('#overview-rank-source').innerHTML = inlineRecord(byTopic.brand_share, true);
    document.querySelector('#macro-rows').innerHTML = macroTopics.map((topic) => row(byTopic[topic])).join('');
    document.querySelector('#benchmark-bands').innerHTML = ['benchmark_kubota', 'benchmark_caterpillar'].map((topic) => {
      const record = byTopic[topic];
      return `<div class="panel benchmarkBand"><h3>${esc(text(record.title))}</h3><p>${esc(narrative(record.conclusion))}</p>${inlineRecord(record, false)}</div>`;
    }).join('');
    document.querySelector('#tonnage-row').innerHTML = row(byTopic.core_tonnages);
  }

  async function init() {
    localizeStatic();
    try {
      const response = await fetch('data/ppt-insights/excavator-overview.json');
      if (!response.ok) throw new Error(String(response.status));
      const data = await response.json();
      records = data.records;
      render();
    } catch (error) {
      console.error(error);
      document.querySelector('#industry-rows').innerHTML = `<p class="scopeBoundary">${language === 'en' ? 'Overview data could not be loaded. Open this page through the local HTTP preview address.' : '整体分析数据未能载入，请通过本地HTTP预览地址打开。'}</p>`;
    }
  }

  init();
})();
