(function () {
  'use strict';

  const source = window.XCMG_DEMO;
  const params = new URLSearchParams(location.search);
  const state = {
    lang: params.get('lang') === 'en' ? 'en' : 'zh',
    line: source.lines.some((line) => line.id === params.get('line')) ? params.get('line') : 'excavators',
    model: source.models.some((model) => model.model === params.get('model')) ? params.get('model') : source.models[0].model
  };

  const copy = {
    zh: {
      brandSubtitle: '全产品线竞品对标平台', navOverview: '平台总览', navLines: '产品线', navAssets: '对标资产', navValue: '应用价值', menu: '菜单',
      title: '全产品线竞品对标平台', subtitle: '把分散的竞品参数、配置差异和典型工况，转化为可追溯的产品决策依据。',
      productLine: '产品线', tonnage: '吨级 / 类别', model: 'XCMG 型号', openAnalysis: '进入分析', metricLines: '产品线', metricAssets: '吨级资产', metricModels: '对标型号',
      lineTitle: '产品线对标入口', lineIntro: '按产品线统一组织对标资产；当前选择只表示浏览状态，不代表重点排序。',
      assetTitle: '挖掘机吨级对标资产', assetIntro: '选择吨级后查看 XCMG 型号、竞品覆盖和典型应用，再进入完整分析看板。',
      competitors: '对标型号', applications: '典型应用', openDashboard: '打开完整分析', live: '已接入', planned: '待接入', assets: '个吨级资产',
      noAssets: '该产品线尚未接入对标资产', noAssetsHint: '入口和数据结构已经预留，接入资料后将在同一位置呈现。',
      valueTitle: '把竞品资料变成工程决策资产', valueIntro: '由 XCMG ARC 独立开发，服务产品定义、配置决策、销售论证和工程评审。',
      valueOneTitle: '同口径比较', valueOneText: '参数、配置和工况使用统一口径，减少跨资料误判。', valueTwoTitle: '差距可追溯', valueTwoText: '每项结论回到具体参数、配置状态和原始数据。',
      valueThreeTitle: '方案可模拟', valueThreeText: '量化查看配置调整对工况表现与竞争位置的影响。', valueFourTitle: '资产可扩展', valueFourText: '按产品线和吨级持续接入，不改变既有分析入口。',
      footer: 'XCMG ARC 独立开发', back: '返回 UI 风格实验室'
    },
    en: {
      brandSubtitle: 'All-Product Competitive Benchmarking Platform', navOverview: 'Overview', navLines: 'Product Lines', navAssets: 'Benchmark Assets', navValue: 'Application Value', menu: 'Menu',
      title: 'All-Product Competitive Benchmarking Platform', subtitle: 'Turn fragmented competitor specifications, equipment differences, and work-condition evidence into traceable product decisions.',
      productLine: 'Product Line', tonnage: 'Tonnage / Category', model: 'XCMG Model', openAnalysis: 'Open Analysis', metricLines: 'Product Lines', metricAssets: 'Tonnage Assets', metricModels: 'Benchmark Models',
      lineTitle: 'Product-Line Benchmarking Entry', lineIntro: 'Benchmark assets follow a common product-line structure. The current selection is a browsing state, not a priority ranking.',
      assetTitle: 'Excavator Tonnage-Class Assets', assetIntro: 'Select a class to review the XCMG model, competitor coverage, and representative applications before opening the full dashboard.',
      competitors: 'Benchmark Models', applications: 'Representative Applications', openDashboard: 'Open Full Analysis', live: 'Available', planned: 'Planned', assets: 'tonnage-class assets',
      noAssets: 'No benchmarking assets are connected for this product line', noAssetsHint: 'The entry and data structure are reserved for future source integration.',
      valueTitle: 'Turn Competitor Material into Engineering Decision Assets', valueIntro: 'Independently developed by XCMG ARC for product definition, configuration decisions, sales evidence, and engineering review.',
      valueOneTitle: 'Common Comparison Basis', valueOneText: 'Parameters, equipment, and work conditions use one consistent evaluation basis.', valueTwoTitle: 'Traceable Gaps', valueTwoText: 'Every conclusion returns to a specific parameter, configuration state, and source record.',
      valueThreeTitle: 'Scenario Simulation', valueThreeText: 'Quantify how configuration changes affect work-condition performance and competitive position.', valueFourTitle: 'Expandable Assets', valueFourText: 'Add product lines and tonnage classes without changing existing analysis entry points.',
      footer: 'Independently Developed by XCMG ARC', back: 'Return to UI Direction Lab'
    }
  };

  const focusEn = {
    '紧凑机身与狭窄空间适应性': 'Compact envelope and confined-site capability', '短尾回转与运输便利性': 'Reduced tail swing and transportability', '多工况能力与配置完整度': 'Multi-application capability and equipment coverage',
    '运输边界与作业覆盖': 'Transport envelope and working coverage', '装车效率与液压属具能力': 'Loading productivity and hydraulic attachment capability', '深挖、稳定性与吊装能力': 'Deep digging, stability, and lifting capability',
    '中型施工效率与配置组合': 'Mid-size jobsite productivity and equipment mix', '生产率与燃油效率平衡': 'Productivity and fuel-efficiency balance', '受限场地中的中型作业能力': 'Mid-size capability in restricted jobsites', '重载生产率与耐久性': 'Heavy-duty productivity and durability'
  };
  const sceneEn = {
    '入户庭院': 'Residential Access', '市政施工': 'Municipal Work', '租赁周转': 'Rental Fleet', '窄场地': 'Confined Sites', '沟槽施工': 'Trenching', '属具适配': 'Attachment Use', '狭窄空间': 'Confined Space',
    '短循环': 'Short Cycles', '破碎作业': 'Hammer Work', '运输边界': 'Transport Envelope', '租赁应用': 'Rental Use', '土方装车': 'Truck Loading', '液压属具': 'Hydraulic Attachments', '驾驶安全': 'Operator Safety',
    '沟槽深挖': 'Deep Trenching', '坡地作业': 'Slope Work', '吊装': 'Lifting', '市政土方': 'Municipal Earthwork', '深挖': 'Deep Digging', '沟槽': 'Trenching', '公路施工': 'Road Work',
    '短尾回转': 'Reduced Tail Swing', '受限空间': 'Restricted Sites', '装车': 'Loading', '重载土方': 'Heavy Earthwork'
  };
  const scopeEn = {
    '10 个吨级资产': '10 tonnage-class assets', '装载效率与油耗': 'Loading productivity and fuel consumption', '压实与振动性能': 'Compaction and vibration performance',
    '精度、牵引与控制': 'Accuracy, traction, and control', '载荷曲线与安全系统': 'Load charts and safety systems', '载重与循环效率': 'Payload and cycle efficiency', '作业高度与租赁适配': 'Working height and rental fit'
  };

  const elements = {
    language: document.querySelector('#language-switch'), menu: document.querySelector('#menu-switch'), nav: document.querySelector('#primary-nav'),
    slices: document.querySelector('#hero-slices'), lineStrip: document.querySelector('#line-strip'), lineContext: document.querySelector('#line-context'),
    command: document.querySelector('#command-bar'), lineSelect: document.querySelector('#line-select'), tonnageSelect: document.querySelector('#tonnage-select'), modelSelect: document.querySelector('#model-select'), openAnalysis: document.querySelector('#open-analysis'),
    assetTitle: document.querySelector('#asset-title'), assetIndex: document.querySelector('#asset-index'), workspace: document.querySelector('.assetWorkspace'), stage: document.querySelector('#asset-stage')
  };

  function t(key) { return copy[state.lang][key]; }
  function activeLine() { return source.getLine(state.line); }
  function activeModel() { return source.models.find((model) => model.model === state.model) || source.models[0]; }
  function lineName(line) { return state.lang === 'en' ? line.en : `${line.en} / ${line.zh}`; }
  function lineScope(line) { return state.lang === 'en' ? (scopeEn[line.scope] || line.scope) : line.scope; }
  function modelFocus(model) { return state.lang === 'en' ? (focusEn[model.focus] || model.focus) : model.focus; }
  function modelScenes(model) { return model.scenes.map((scene) => state.lang === 'en' ? (sceneEn[scene] || scene) : scene); }
  function classLabel(model) {
    if (state.lang === 'zh') return model.label;
    return model.tonnage === '14-16' ? `${model.tonnage} t Short-Tail Class` : `${model.tonnage} t Class`;
  }
  function dashboardUrl(model) { return state.lang === 'en' ? `${model.url}?lang=en` : model.url; }

  function writeUrl() {
    const next = new URL(location.href);
    next.searchParams.set('lang', state.lang);
    next.searchParams.set('line', state.line);
    if (activeLine().live) next.searchParams.set('model', state.model); else next.searchParams.delete('model');
    history.replaceState(null, '', next);
  }

  function renderCopy() {
    document.documentElement.lang = state.lang === 'en' ? 'en' : 'zh-CN';
    document.title = state.lang === 'en' ? 'XCMG ARC Industrial Platform V2 Demo' : 'XCMG ARC 工业平台 V2 Demo';
    document.querySelectorAll('[data-copy]').forEach((node) => { node.textContent = t(node.dataset.copy); });
    elements.language.textContent = state.lang === 'en' ? '中文' : 'EN';
    elements.language.setAttribute('aria-label', state.lang === 'en' ? '切换到中文' : 'Switch to English');
  }

  function renderSlices() {
    elements.slices.innerHTML = source.lines.map((line) => `
      <button class="heroSlice" type="button" data-line="${line.id}" aria-pressed="${line.id === state.line}" aria-label="${lineName(line)}">
        <img src="${line.image}" alt=""><span>${lineName(line)}</span>
      </button>`).join('');
  }

  function renderCommand() {
    const line = activeLine();
    elements.lineSelect.innerHTML = source.lines.map((item) => `<option value="${item.id}">${lineName(item)}</option>`).join('');
    elements.lineSelect.value = line.id;
    elements.tonnageSelect.disabled = !line.live;
    elements.modelSelect.disabled = !line.live;
    elements.openAnalysis.disabled = !line.live;
    if (!line.live) {
      elements.tonnageSelect.innerHTML = `<option>${t('planned')}</option>`;
      elements.modelSelect.innerHTML = `<option>${t('planned')}</option>`;
      return;
    }
    const model = activeModel();
    elements.tonnageSelect.innerHTML = source.models.map((item) => `<option value="${item.tonnage}">${classLabel(item)}</option>`).join('');
    elements.tonnageSelect.value = model.tonnage;
    const classModels = source.models.filter((item) => item.tonnage === model.tonnage);
    elements.modelSelect.innerHTML = classModels.map((item) => `<option value="${item.model}">${item.model}</option>`).join('');
    elements.modelSelect.value = model.model;
  }

  function renderLines() {
    elements.lineStrip.innerHTML = source.lines.map((line) => `
      <button class="lineTile" type="button" data-line="${line.id}" aria-pressed="${line.id === state.line}">
        <span class="lineTileMedia"><img src="${line.image}" alt="${line.en}"></span>
        <span class="lineTileBody"><b>${lineName(line)}</b><span>${lineScope(line)}</span></span>
      </button>`).join('');
    const line = activeLine();
    elements.lineContext.innerHTML = `
      <div><strong>${lineName(line)}</strong><p>${lineScope(line)}</p></div>
      <span class="contextState${line.live ? ' live' : ''}">${line.live ? `${source.models.length} ${t('assets')}` : t('planned')}</span>`;
  }

  function stageMarkup(model) {
    return `
      <div class="stageMedia"><img src="${model.image}" alt="${model.model}"></div>
      <div class="stageCopy">
        <p class="stageClass">${classLabel(model)}</p>
        <h3>${model.model}</h3>
        <p class="stageFocus">${modelFocus(model)}</p>
        <dl>
          <div><dt>${t('competitors')}</dt><dd>${model.competitors}</dd></div>
          <div><dt>${t('applications')}</dt><dd>${modelScenes(model).join(' · ')}</dd></div>
        </dl>
        <a class="stageAction" href="${dashboardUrl(model)}">${t('openDashboard')}</a>
      </div>`;
  }

  function renderAssets() {
    const line = activeLine();
    elements.workspace.classList.toggle('isEmpty', !line.live);
    elements.assetIndex.hidden = !line.live;
    elements.assetTitle.textContent = line.live ? t('assetTitle') : `${lineName(line)} ${state.lang === 'en' ? 'Benchmark Assets' : '对标资产'}`;
    if (!line.live) {
      elements.assetIndex.innerHTML = '';
      elements.stage.innerHTML = `<div class="assetEmpty"><div><img src="${line.image}" alt="${line.en}"><h3>${t('noAssets')}</h3><p>${t('noAssetsHint')}</p></div></div>`;
      return;
    }
    elements.assetIndex.innerHTML = source.models.map((model) => `
      <button class="assetRow" type="button" data-model="${model.model}" aria-pressed="${model.model === state.model}">
        <img src="${model.image}" alt="${model.model}">
        <span class="assetIdentity"><b>${model.model}</b><small>${classLabel(model)}</small></span>
        <span class="assetCount">${model.competitors} ${t('competitors')}</span>
      </button>`).join('');
    elements.stage.innerHTML = stageMarkup(activeModel());
  }

  function renderAll() {
    renderCopy();
    renderSlices();
    renderCommand();
    renderLines();
    renderAssets();
    writeUrl();
  }

  function selectLine(id) {
    state.line = id;
    if (activeLine().live && !source.models.some((model) => model.model === state.model)) state.model = source.models[0].model;
    renderAll();
  }

  elements.slices.addEventListener('click', (event) => {
    const button = event.target.closest('[data-line]');
    if (button) selectLine(button.dataset.line);
  });
  elements.lineStrip.addEventListener('click', (event) => {
    const button = event.target.closest('[data-line]');
    if (button) selectLine(button.dataset.line);
  });
  elements.lineSelect.addEventListener('change', () => selectLine(elements.lineSelect.value));
  elements.tonnageSelect.addEventListener('change', () => {
    const model = source.models.find((item) => item.tonnage === elements.tonnageSelect.value);
    if (model) state.model = model.model;
    renderAll();
  });
  elements.modelSelect.addEventListener('change', () => { state.model = elements.modelSelect.value; renderAll(); });
  elements.assetIndex.addEventListener('click', (event) => {
    const button = event.target.closest('[data-model]');
    if (!button) return;
    state.model = button.dataset.model;
    renderAll();
  });
  elements.command.addEventListener('submit', (event) => {
    event.preventDefault();
    if (activeLine().live) location.href = dashboardUrl(activeModel());
  });
  elements.language.addEventListener('click', () => { state.lang = state.lang === 'en' ? 'zh' : 'en'; renderAll(); });
  elements.menu.addEventListener('click', () => {
    const open = !elements.nav.classList.contains('isOpen');
    elements.nav.classList.toggle('isOpen', open);
    elements.menu.setAttribute('aria-expanded', String(open));
  });
  elements.nav.addEventListener('click', () => {
    elements.nav.classList.remove('isOpen');
    elements.menu.setAttribute('aria-expanded', 'false');
  });

  renderAll();
}());
