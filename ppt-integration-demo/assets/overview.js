(function () {
  'use strict';

  const query = new URLSearchParams(window.location.search);
  let stored = '';
  try { stored = window.localStorage.getItem('xcmg-benchmark-language') || ''; } catch (_) { stored = ''; }
  const language = query.get('lang') === 'en' || (query.get('lang') !== 'zh' && stored === 'en') ? 'en' : 'zh';
  let records = [];
  let lastFocus = null;

  const ui = {
    zh: {
      evidence: '查看依据', slide: '第', slideSuffix: '页', drawer: '结论依据', close: '关闭',
      sourceType: '来源类型', date: '数据时间', temporal: '时间属性', validation: '验证状态', raw: 'PPT原始文字',
      verify: '需按当前市场、政策或产品版本复核'
    },
    en: {
      evidence: 'View evidence', slide: 'Slide ', slideSuffix: '', drawer: 'Evidence', close: 'Close',
      sourceType: 'Source type', date: 'Data date', temporal: 'Temporal status', validation: 'Validation status', raw: 'Original PPT wording',
      verify: 'Current market, policy or product-version validation required'
    }
  }[language];

  const englishStatic = new Map([
    ['挖掘机整体分析', 'Excavator Overall Analysis'],
    ['页面导航', 'Page Navigation'],
    ['顶部', 'Top'],
    ['返回3–4吨集成原型', 'Return to the 3–4 t Integrated Prototype'],
    ['行业周期与竞争格局', 'Industry Cycle and Competitive Landscape'],
    ['宏观约束与机会', 'Macro Constraints and Opportunities'],
    ['战略标杆', 'Strategic Benchmarks'],
    ['核心吨级结构', 'Core Tonnage Structure'],
    ['原始依据', 'Source Evidence'],
    ['查看依据', 'View evidence'],
    ['XCMG ARC内部资料', 'XCMG ARC INTERNAL'],
    ['用于承接不能归入单一吨级的挖掘机产品线内容；所有市场数字均保留PPT时间属性。', 'This page holds excavator product-line content that cannot be assigned to one tonnage class. Every market figure retains its PPT time basis.'],
    ['北美挖掘机整体分析', 'North American Excavator Overall Analysis'],
    ['把宏观环境、行业周期、竞争集中度、主销吨级和战略标杆放在产品线层级阅读；各吨级的参数、配置和具体工况仍回到对应对标页面。', 'Read the macro environment, industry cycle, competitive concentration, core tonnage classes and strategic benchmarks at product-line level. Specifications, equipment and individual applications remain in each tonnage benchmark.'],
    ['2025市场规模历史预测 / 台', 'Historical 2025 market forecast / units'],
    ['0–10吨前十品牌合计', 'Top-ten share, 0–10 t'],
    ['10吨以上前十品牌合计', 'Top-ten share, above 10 t'],
    ['XCMG历史排名：0–10吨 / 10吨以上', 'Historical XCMG rank: 0–10 t / above 10 t'],
    ['需求调整、品牌集中度和吨级结构共同决定产品对标优先级。', 'Demand adjustment, brand concentration and tonnage mix jointly determine benchmarking priority.'],
    ['PPT来源', 'PPT source'],
    ['第9–12页', 'Slides 9–12'],
    ['竞争集中度与市场格局', 'Competitive concentration and market structure'],
    ['品牌份额与XCMG位置', 'Brand share and XCMG position'],
    ['只保留会影响产品规划、区域投入和市场准入的因素。', 'Retain only factors that affect product planning, regional investment and market access.'],
    ['第3–8页', 'Slides 3–8'],
    ['微小挖与中大挖采用不同标杆，不把一个品牌的优势机械复制到所有吨级。', 'Use different benchmarks for mini/compact and mid/large excavators rather than copying one brand across every tonnage class.'],
    ['第13–14页', 'Slides 13–14'],
    ['用于决定对标资产建设顺序，销量与降幅需按最新AEM/EDA数据复核。', 'Use this structure to prioritize benchmark assets. Volumes and declines require the latest AEM/EDA validation.'],
    ['第15页', 'Slide 15'],
    ['微挖 0–4吨', 'Mini excavators, 0–4 t'],
    ['核心：3–4、1–2、2–3吨', 'Core: 3–4, 1–2 and 2–3 t'],
    ['小挖 4–10吨', 'Compact excavators, 4–10 t'],
    ['核心：5–6、4–5吨', 'Core: 5–6 and 4–5 t'],
    ['中挖 10–33吨', 'Mid-size excavators, 10–33 t'],
    ['核心：21–24、14–16、24–28吨', 'Core: 21–24, 14–16 and 24–28 t'],
    ['大挖 33吨以上', 'Large excavators, above 33 t'],
    ['核心：33–40、40–50吨', 'Core: 33–40 and 40–50 t'],
    ['点击页码查看PPT原页、原始文字、时间属性和验证状态。', 'Select a slide to inspect the original page, source wording, temporal status and validation state.'],
    ['范围', 'Range'],
    ['第3–15页', 'Slides 3–15'],
    ['回到页面顶部', 'Return to page top'],
    ['回到顶部', 'Back to top']
  ]);

  function text(value) {
    if (value == null) return '';
    if (typeof value === 'object' && ('zh' in value || 'en' in value)) return value[language] || value.zh || value.en || '';
    return String(value);
  }

  function esc(value) {
    return String(value == null ? '' : value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }

  function page(value) { return `${ui.slide}${value}${ui.slideSuffix}`; }

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
    document.querySelector('.overviewVisual img[src*="slide-10"]')?.setAttribute('alt', 'PPT slide 10 competitive-concentration chart');
    document.querySelector('.overviewVisual img[src*="slide-12"]')?.setAttribute('alt', 'PPT slide 12 brand-share chart');
  }

  function row(record) {
    return `<div class="overviewDecisionRow"><h3>${esc(text(record.title))}</h3><p>${esc(text(record.conclusion))}</p><button type="button" class="evidenceTrigger" data-overview-slide="${record.source_slide}">${esc(ui.evidence)}</button></div>`;
  }

  function render() {
    const byTopic = Object.fromEntries(records.map((record) => [record.metric, record]));
    const industryTopics = ['industry_cycle', 'competition_concentration', 'product_structure', 'brand_share'];
    const macroTopics = ['macro_social', 'technology', 'economy_rental', 'emissions', 'trade_policy', 'macro_summary'];
    document.querySelector('#industry-rows').innerHTML = industryTopics.map((topic) => row(byTopic[topic])).join('');
    document.querySelector('#macro-rows').innerHTML = macroTopics.map((topic) => row(byTopic[topic])).join('');
    document.querySelector('#benchmark-bands').innerHTML = ['benchmark_kubota', 'benchmark_caterpillar'].map((topic) => {
      const record = byTopic[topic];
      return `<div class="benchmarkBand"><h3>${esc(text(record.title))}</h3><p>${esc(text(record.conclusion))}</p><button type="button" class="evidenceTrigger" data-overview-slide="${record.source_slide}">${esc(ui.evidence)}</button></div>`;
    }).join('');
    document.querySelector('#tonnage-row').innerHTML = row(byTopic.core_tonnages);
    document.querySelector('#overview-evidence-buttons').innerHTML = records.map((record) => `<button type="button" data-overview-slide="${record.source_slide}"><b>${esc(page(record.source_slide))}</b>${esc(text(record.title))}</button>`).join('');
  }

  function installDrawer() {
    document.body.insertAdjacentHTML('beforeend', `<div class="evidenceOverlay" aria-hidden="true"></div><aside class="evidenceDrawer" aria-hidden="true" aria-labelledby="overview-drawer-title"><div class="evidenceDrawerHead"><h2 id="overview-drawer-title">${esc(ui.drawer)}</h2><button type="button" class="drawerClose" aria-label="${esc(ui.close)}">×</button></div><div class="evidenceDrawerBody"></div></aside>`);
    document.querySelector('.drawerClose').addEventListener('click', closeDrawer);
    document.querySelector('.evidenceOverlay').addEventListener('click', closeDrawer);
    document.addEventListener('keydown', (event) => { if (event.key === 'Escape') closeDrawer(); });
    document.addEventListener('click', (event) => {
      const button = event.target.closest('[data-overview-slide]');
      if (button) openDrawer(Number(button.dataset.overviewSlide));
    });
  }

  function openDrawer(slideNumber) {
    const record = records.find((item) => Number(item.source_slide) === slideNumber);
    if (!record) return;
    const drawer = document.querySelector('.evidenceDrawer');
    const overlay = document.querySelector('.evidenceOverlay');
    const body = drawer.querySelector('.evidenceDrawerBody');
    body.innerHTML = `<img class="evidenceSlideImage" src="ppt-integration-demo/${esc(record.thumbnail)}" alt="${esc(text(record.title))}"><dl class="evidenceMeta"><div><dt>${esc(ui.slide.replace(/\s+$/, ''))}</dt><dd>${esc(page(slideNumber))}</dd></div><div><dt>${esc(ui.sourceType)}</dt><dd>${language === 'en' ? 'XCMG ARC internal presentation' : 'XCMG ARC内部PPT'}</dd></div><div><dt>${esc(ui.date)}</dt><dd>${esc(record.as_of_date)}</dd></div><div><dt>${esc(ui.temporal)}</dt><dd>${esc(status(record.status))}</dd></div><div><dt>${esc(ui.validation)}</dt><dd>${esc(ui.verify)}</dd></div></dl><div class="evidenceConclusion"><b>${esc(text(record.title))}</b><br>${esc(text(record.conclusion))}</div><label class="evidenceRawLabel" for="overview-evidence-raw">${esc(ui.raw)}</label><textarea id="overview-evidence-raw" class="evidenceRaw" readonly></textarea>`;
    body.querySelector('.evidenceRaw').value = record.zh?.raw_text || (record.zh?.paragraphs || []).join('\n');
    lastFocus = document.activeElement;
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
    lastFocus?.focus?.();
  }

  async function init() {
    localizeStatic();
    installDrawer();
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
