(function () {
  'use strict';

  const source = window.XCMG_DEMO;
  if (!source) return;

  const copy = {
    zh: {
      brandSubtitle: '全产品线竞品对标平台', pageNavigation: '页面导航', navOverview: '平台总览', navAssets: '产品资产', navValue: '应用价值', navSource: '数据中心', navFormal: '正式平台', menu: '菜单', closeNavigation: '关闭导航',
      title: '全产品线竞品对标平台', subtitle: '统一查看竞品参数、配置差异、典型工况与原始数据来源。', quickAnalysis: '快速进入产品分析', productLine: '产品线', tonnage: '吨级 / 类别', xcmgModel: 'XCMG 型号', openAnalysis: '进入分析',
      platformMetrics: '平台数据概览', metricLines: '产品线规划', metricClasses: '吨级资产', metricModels: '对标产品型号', currentAssets: '当前可用资产', unavailableAssets: '当前产品线暂无资产',
      assetWorkspace: '产品对标资产工作台', productLines: '产品线', selectLine: '选择分析范围', excavatorAssets: '挖掘机吨级资产', assets: '个资产', modelSearch: '型号搜索', searchPlaceholder: '输入 XE75U、7-8 或应用场景', clear: '清除', tonnageFilter: '吨级筛选', all: '全部',
      benchmarkAsset: '对标资产', benchmarkProducts: '对标产品', keyApplications: '重点工况', openDashboard: '打开完整看板', noResults: '没有匹配的资产', noResultsHint: '请调整吨级或搜索条件。', noLineAssets: '暂无对标资产', noLineAssetsHint: '该产品线入口已保留。',
      valueTitle: '平台应用价值', valuePlanning: '产品规划', valuePlanningText: '按吨级与工况明确参数和配置目标。', valueEngineering: '工程评审', valueEngineeringText: '将竞品差距落实到可复核的工程指标。', valueSales: '市场与销售', valueSalesText: '把参数差异转化为客户场景与产品论据。', valueData: '数据治理', valueDataText: '集中管理源表、评价口径和版本状态。',
      footerOwner: 'XCMG ARC 独立开发', backLab: '返回 UI 风格实验室', available: '已有资产', unavailable: '暂无资产', competitors: '个对标型号'
    },
    en: {
      brandSubtitle: 'All-Product Competitive Benchmarking Platform', pageNavigation: 'Page navigation', navOverview: 'Overview', navAssets: 'Product Assets', navValue: 'Application Value', navSource: 'Data Center', navFormal: 'Production Platform', menu: 'Menu', closeNavigation: 'Close navigation',
      title: 'All-Product Competitive Benchmarking Platform', subtitle: 'Review competitor specifications, equipment differences, representative work conditions, and source data in one workspace.', quickAnalysis: 'Quick product analysis', productLine: 'Product Line', tonnage: 'Tonnage / Category', xcmgModel: 'XCMG Model', openAnalysis: 'Open Analysis',
      platformMetrics: 'Platform data overview', metricLines: 'Product Lines Planned', metricClasses: 'Tonnage Assets', metricModels: 'Benchmark Models', currentAssets: 'Assets Available', unavailableAssets: 'No Assets for This Line',
      assetWorkspace: 'Product benchmarking asset workspace', productLines: 'Product Lines', selectLine: 'Select analysis scope', excavatorAssets: 'Excavator Class Assets', assets: 'assets', modelSearch: 'Model Search', searchPlaceholder: 'Search XE75U, 7-8, or an application', clear: 'Clear', tonnageFilter: 'Tonnage filter', all: 'All',
      benchmarkAsset: 'Benchmark Asset', benchmarkProducts: 'Benchmark Models', keyApplications: 'Key Applications', openDashboard: 'Open Full Dashboard', noResults: 'No matching assets', noResultsHint: 'Adjust the tonnage or search criteria.', noLineAssets: 'No Benchmark Assets', noLineAssetsHint: 'The product-line entry is reserved.',
      valueTitle: 'Platform Application Value', valuePlanning: 'Product Planning', valuePlanningText: 'Set specification and equipment targets by class and work condition.', valueEngineering: 'Engineering Review', valueEngineeringText: 'Tie competitive gaps to reviewable engineering measures.', valueSales: 'Market and Sales', valueSalesText: 'Translate specification differences into customer applications and product evidence.', valueData: 'Data Governance', valueDataText: 'Manage source workbooks, evaluation criteria, and revisions centrally.',
      footerOwner: 'Developed Independently by XCMG ARC', backLab: 'Return to UI Direction Lab', available: 'Available', unavailable: 'No assets', competitors: 'benchmark models'
    }
  };

  const sceneEn = {
    '入户庭院': 'Residential Access', '市政施工': 'Municipal Work', '租赁周转': 'Rental Fleet', '窄场地': 'Confined Sites', '沟槽施工': 'Trenching', '属具适配': 'Attachment Compatibility',
    '狭窄空间': 'Confined Sites', '短循环': 'Short-Cycle Work', '破碎作业': 'Breaker Work', '运输边界': 'Transport Envelope', '租赁应用': 'Rental Use', '土方装车': 'Truck Loading',
    '液压属具': 'Hydraulic Attachments', '驾驶安全': 'Operator Safety', '沟槽深挖': 'Deep Trenching', '坡地作业': 'Slopes and Soft Ground', '吊装': 'Lifting', '市政土方': 'Municipal Earthmoving',
    '深挖': 'Deep Excavation', '基础深挖': 'Foundation Excavation', '重载挖掘': 'Heavy-Duty Excavation', '公路施工': 'Road Construction', '短尾回转': 'Reduced Tail Swing',
    '受限空间': 'Confined Sites', '装车': 'Truck Loading', '重载土方': 'Heavy Earthmoving'
  };
  const focusEn = {
    '紧凑机身与狭窄空间适应性': 'Compact envelope and confined-site capability', '短尾回转与运输便利性': 'Reduced tail swing and transportability', '多工况能力与配置完整度': 'Multi-application capability and equipment coverage',
    '运输边界与作业覆盖': 'Transport envelope and working coverage', '装车效率与液压属具能力': 'Truck-loading productivity and hydraulic attachment capability', '深挖、稳定性与吊装能力': 'Deep excavation, stability, and lifting capability',
    '中型施工效率与配置组合': 'Mid-size productivity and equipment package', '生产率与燃油效率平衡': 'Productivity and fuel-efficiency balance', '受限场地中的中型作业能力': 'Mid-size performance in confined sites',
    '重载生产率与耐久性': 'Heavy-duty productivity and durability'
  };
  const scopeEn = {
    '10 个吨级资产': '10 tonnage-class assets', '装载效率与油耗': 'Loading productivity and fuel consumption', '压实与振动性能': 'Compaction and vibration performance',
    '精度、牵引与控制': 'Accuracy, traction, and control', '载荷曲线与安全系统': 'Load charts and safety systems', '载重与循环效率': 'Payload and cycle productivity', '作业高度与租赁适配': 'Working height and rental suitability'
  };

  const params = new URLSearchParams(location.search);
  const state = {
    lang: params.get('lang') === 'en' ? 'en' : 'zh',
    line: source.lines.some((item) => item.id === params.get('line')) ? params.get('line') : 'excavators',
    tonnage: params.get('tonnage') || '',
    model: params.get('model') || source.models[0].model,
    query: ''
  };

  const elements = {
    lineSelect: document.querySelector('#line-select'), tonnageSelect: document.querySelector('#tonnage-select'), modelSelect: document.querySelector('#model-select'), launcher: document.querySelector('#launcher'), openAnalysis: document.querySelector('#open-analysis'),
    lineList: document.querySelector('#line-list'), assetKicker: document.querySelector('#asset-kicker'), assetHeading: document.querySelector('#asset-heading'), assetCount: document.querySelector('#asset-count'), search: document.querySelector('#asset-search'), clear: document.querySelector('#clear-filter'),
    tabs: document.querySelector('#tonnage-tabs'), list: document.querySelector('#asset-list'), inspectorImage: document.querySelector('#inspector-image'), inspectorClass: document.querySelector('#inspector-class'), inspectorModel: document.querySelector('#inspector-model'), inspectorFocus: document.querySelector('#inspector-focus'), inspectorCompetitors: document.querySelector('#inspector-competitors'), inspectorScenes: document.querySelector('#inspector-scenes'), inspectorOpen: document.querySelector('#inspector-open'),
    contextValue: document.querySelector('#metric-context-value'), contextLabel: document.querySelector('#metric-context-label'), language: document.querySelector('#language-toggle'), menu: document.querySelector('#menu-toggle'), nav: document.querySelector('#primary-nav'), scrim: document.querySelector('#nav-scrim')
  };

  function t(key) { return copy[state.lang][key] || key; }
  function lineName(line) { return state.lang === 'en' ? line.en : `${line.en} / ${line.zh}`; }
  function classLabel(model) {
    if (state.lang !== 'en') return model.label;
    return model.label.includes('短尾')
      ? `${model.tonnage} t Short-Tail Class`
      : `${model.tonnage} t Class`;
  }
  function sceneLabel(value) { return state.lang === 'en' ? (sceneEn[value] || value) : value; }
  function focusLabel(value) { return state.lang === 'en' ? (focusEn[value] || value) : value; }
  function scopeLabel(value) { return state.lang === 'en' ? (scopeEn[value] || value) : value; }
  function languageUrl(url) {
    if (state.lang !== 'en') return url;
    const separator = url.includes('?') ? '&' : '?';
    return `${url}${separator}lang=en`;
  }
  function normalize(value) { return String(value || '').toLowerCase().replace(/[^a-z0-9\u4e00-\u9fff]+/g, ''); }
  function fuzzyMatch(haystack, needle) {
    const target = normalize(haystack);
    const query = normalize(needle);
    if (!query || target.includes(query)) return true;
    let cursor = 0;
    for (const character of target) if (character === query[cursor]) cursor += 1;
    return cursor === query.length;
  }
  function selectedLine() { return source.getLine(state.line); }
  function selectedModel() { return source.models.find((item) => item.model === state.model) || source.models[0]; }
  function writeUrl() {
    const next = new URL(location.href);
    next.searchParams.set('lang', state.lang);
    next.searchParams.set('line', state.line);
    if (state.tonnage) next.searchParams.set('tonnage', state.tonnage); else next.searchParams.delete('tonnage');
    if (state.line === 'excavators') next.searchParams.set('model', state.model); else next.searchParams.delete('model');
    history.replaceState(null, '', next);
  }

  function renderStaticCopy() {
    document.documentElement.lang = state.lang === 'en' ? 'en' : 'zh-CN';
    document.title = state.lang === 'en' ? 'XCMG ARC Industrial Workspace Demo' : 'XCMG ARC 工业工作台 Demo';
    document.querySelectorAll('[data-i18n]').forEach((node) => { node.textContent = t(node.dataset.i18n); });
    document.querySelectorAll('[data-i18n-placeholder]').forEach((node) => { node.placeholder = t(node.dataset.i18nPlaceholder); });
    document.querySelectorAll('[data-i18n-aria]').forEach((node) => { node.setAttribute('aria-label', t(node.dataset.i18nAria)); });
    elements.language.textContent = state.lang === 'en' ? '中文' : 'EN';
    elements.language.setAttribute('aria-label', state.lang === 'en' ? '切换到中文' : 'Switch to English');
    document.querySelectorAll('[data-language-link]').forEach((link) => {
      const base = link.getAttribute('href').split('?')[0];
      link.setAttribute('href', state.lang === 'en' ? `${base}?lang=en` : base);
    });
  }

  function renderLauncher() {
    elements.lineSelect.innerHTML = source.lines.map((line) => `<option value="${line.id}">${lineName(line)}</option>`).join('');
    elements.lineSelect.value = state.line;
    const line = selectedLine();
    const models = line.live ? source.models : [];
    elements.tonnageSelect.disabled = !line.live;
    elements.modelSelect.disabled = !line.live;
    elements.openAnalysis.disabled = !line.live;
    elements.tonnageSelect.innerHTML = models.map((model) => `<option value="${model.tonnage}">${classLabel(model)}</option>`).join('');
    const activeModel = selectedModel();
    const launcherTonnage = models.some((model) => model.tonnage === activeModel.tonnage) ? activeModel.tonnage : (models[0]?.tonnage || '');
    elements.tonnageSelect.value = launcherTonnage;
    const inClass = models.filter((model) => model.tonnage === launcherTonnage);
    elements.modelSelect.innerHTML = inClass.map((model) => `<option value="${model.model}">${model.model}</option>`).join('');
    if (inClass.length && !inClass.some((model) => model.model === state.model)) state.model = inClass[0].model;
    elements.modelSelect.value = state.model;
  }

  function renderLineRail() {
    elements.lineList.innerHTML = source.lines.map((line) => `
      <button class="lineButton" type="button" data-line="${line.id}" aria-pressed="${line.id === state.line}">
        <span><b>${lineName(line)}</b><small>${scopeLabel(line.scope)}</small></span>
        <i class="lineState ${line.live ? 'live' : ''}" aria-hidden="true"></i>
      </button>`).join('');
  }

  function renderTabs() {
    if (!selectedLine().live) { elements.tabs.innerHTML = ''; return; }
    const values = [...new Set(source.models.map((model) => model.tonnage))];
    elements.tabs.innerHTML = [`<button type="button" data-tonnage="" aria-pressed="${state.tonnage === ''}">${t('all')}</button>`]
      .concat(values.map((value) => {
        const model = source.models.find((item) => item.tonnage === value);
        return `<button type="button" data-tonnage="${value}" aria-pressed="${state.tonnage === value}">${classLabel(model)}</button>`;
      })).join('');
  }

  function filteredModels() {
    if (!selectedLine().live) return [];
    return source.models.filter((model) => {
      const tonnageOk = !state.tonnage || model.tonnage === state.tonnage;
      const searchText = [model.model, model.label, model.tonnage, model.focus, ...model.scenes, focusLabel(model.focus), ...model.scenes.map(sceneLabel)].join(' ');
      return tonnageOk && fuzzyMatch(searchText, state.query);
    });
  }

  function renderInspector(model) {
    const line = selectedLine();
    if (!line.live || !model) {
      elements.inspectorImage.src = line.image;
      elements.inspectorImage.alt = line.en;
      elements.inspectorClass.textContent = lineName(line);
      elements.inspectorModel.textContent = t('noLineAssets');
      elements.inspectorFocus.textContent = t('noLineAssetsHint');
      elements.inspectorCompetitors.textContent = '0';
      elements.inspectorScenes.textContent = scopeLabel(line.scope);
      elements.inspectorOpen.removeAttribute('href');
      elements.inspectorOpen.setAttribute('aria-disabled', 'true');
      return;
    }
    state.model = model.model;
    elements.inspectorImage.src = model.image;
    elements.inspectorImage.alt = model.model;
    elements.inspectorClass.textContent = classLabel(model);
    elements.inspectorModel.textContent = model.model;
    elements.inspectorFocus.textContent = focusLabel(model.focus);
    elements.inspectorCompetitors.textContent = String(model.competitors);
    elements.inspectorScenes.textContent = model.scenes.map(sceneLabel).join(' · ');
    elements.inspectorOpen.href = languageUrl(model.url);
    elements.inspectorOpen.removeAttribute('aria-disabled');
  }

  function renderAssets() {
    const line = selectedLine();
    const models = filteredModels();
    elements.assetKicker.textContent = line.en;
    elements.assetHeading.textContent = line.live ? t('excavatorAssets') : lineName(line);
    elements.assetCount.textContent = line.live ? `${models.length} ${t('assets')}` : t('unavailable');
    elements.contextValue.textContent = line.live ? String(models.length) : '0';
    elements.contextLabel.textContent = line.live ? t('currentAssets') : t('unavailableAssets');

    if (!line.live) {
      elements.list.innerHTML = `<div class="emptyState"><div><img src="${line.image}" alt="${line.en}"><h3>${t('noLineAssets')}</h3><p>${t('noLineAssetsHint')}</p></div></div>`;
      renderInspector(null);
      return;
    }
    if (!models.length) {
      elements.list.innerHTML = `<div class="emptyState"><div><h3>${t('noResults')}</h3><p>${t('noResultsHint')}</p></div></div>`;
      renderInspector(selectedModel());
      return;
    }
    if (!models.some((model) => model.model === state.model)) state.model = models[0].model;
    elements.list.innerHTML = models.map((model) => `
      <button class="assetRow" type="button" data-model="${model.model}" aria-pressed="${model.model === state.model}">
        <img class="assetThumb" src="${model.image}" alt="${model.model}">
        <span class="assetMain"><h3>${model.model}</h3><p>${focusLabel(model.focus)}</p></span>
        <span class="assetMeta"><span>${classLabel(model)}</span><span>${model.competitors} ${t('competitors')}</span></span>
      </button>`).join('');
    renderInspector(selectedModel());
  }

  function renderAll() {
    renderStaticCopy();
    renderLauncher();
    renderLineRail();
    renderTabs();
    renderAssets();
    writeUrl();
  }

  elements.lineSelect.addEventListener('change', () => {
    state.line = elements.lineSelect.value;
    state.tonnage = '';
    state.model = source.models[0].model;
    state.query = '';
    elements.search.value = '';
    renderAll();
  });
  elements.tonnageSelect.addEventListener('change', () => {
    state.tonnage = elements.tonnageSelect.value;
    const match = source.models.find((model) => model.tonnage === state.tonnage);
    if (match) state.model = match.model;
    renderAll();
  });
  elements.modelSelect.addEventListener('change', () => { state.model = elements.modelSelect.value; renderAll(); });
  elements.launcher.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!selectedLine().live) return;
    location.href = languageUrl(selectedModel().url);
  });
  elements.lineList.addEventListener('click', (event) => {
    const button = event.target.closest('[data-line]');
    if (!button) return;
    state.line = button.dataset.line;
    state.tonnage = '';
    state.model = source.models[0].model;
    state.query = '';
    elements.search.value = '';
    renderAll();
  });
  elements.tabs.addEventListener('click', (event) => {
    const button = event.target.closest('[data-tonnage]');
    if (!button) return;
    state.tonnage = button.dataset.tonnage;
    const models = filteredModels();
    if (models.length) state.model = models[0].model;
    renderAll();
  });
  elements.list.addEventListener('click', (event) => {
    const button = event.target.closest('[data-model]');
    if (!button) return;
    state.model = button.dataset.model;
    renderAssets();
    writeUrl();
  });
  elements.search.addEventListener('input', () => { state.query = elements.search.value; renderAssets(); });
  elements.clear.addEventListener('click', () => { state.query = ''; state.tonnage = ''; elements.search.value = ''; renderAll(); elements.search.focus(); });
  elements.language.addEventListener('click', () => { state.lang = state.lang === 'en' ? 'zh' : 'en'; renderAll(); });
  elements.menu.addEventListener('click', () => {
    const open = !document.body.classList.contains('menuOpen');
    document.body.classList.toggle('menuOpen', open);
    elements.nav.classList.toggle('isOpen', open);
    elements.menu.setAttribute('aria-expanded', String(open));
  });
  elements.scrim.addEventListener('click', () => {
    document.body.classList.remove('menuOpen');
    elements.nav.classList.remove('isOpen');
    elements.menu.setAttribute('aria-expanded', 'false');
  });
  elements.nav.addEventListener('click', () => {
    document.body.classList.remove('menuOpen');
    elements.nav.classList.remove('isOpen');
    elements.menu.setAttribute('aria-expanded', 'false');
  });

  renderAll();
}());
