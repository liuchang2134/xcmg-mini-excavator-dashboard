function setupRadars(){
  document.querySelectorAll('.radarBox,.factorRadar').forEach(box=>{
    const current=box.querySelector('.radarCurrent');
    const series=[...box.querySelectorAll('.radar-series[data-product]')];
    const controls=[...box.querySelectorAll('.radarLegend [data-product]')];
    const selected=new Set(controls.map(btn=>btn.dataset.product));
    const label=()=>{
      if(!current) return;
      if(selected.size===controls.length) current.textContent='当前：全部品牌';
      else if(selected.size===0) current.textContent='当前：未选择品牌';
      else if(selected.size===1) current.textContent='当前：'+[...selected][0];
      else current.textContent='当前：'+selected.size+' 个品牌对比';
    };
    const render=()=>{
      const allSelected=selected.size===controls.length;
      box.classList.toggle('compare',!allSelected);
      series.forEach(s=>s.classList.toggle('selected',selected.has(s.dataset.product)));
      controls.forEach(btn=>{
        const on=selected.has(btn.dataset.product);
        btn.classList.toggle('selected',on);
        btn.setAttribute('aria-pressed',String(on));
      });
      label();
    };
    const toggle=(product)=>{
      if(selected.has(product)) selected.delete(product);
      else selected.add(product);
      render();
    };
    controls.forEach(btn=>{
      btn.setAttribute('aria-pressed','false');
      btn.addEventListener('click',()=>toggle(btn.dataset.product));
    });
    series.forEach(shape=>{
      shape.setAttribute('tabindex','0');
      shape.setAttribute('role','button');
      shape.addEventListener('click',()=>toggle(shape.dataset.product));
      shape.addEventListener('keydown',e=>{
        if(e.key==='Enter'||e.key===' '){
          e.preventDefault();
          toggle(shape.dataset.product);
        }
      });
    });
    render();
  });
}
function setupSimulators(){
    document.querySelectorAll('.simulator[data-base]').forEach(sim=>{
    const xcmg=sim.dataset.xcmg;
    const rivals=(sim.dataset.rivals||'').split('|').filter(Boolean).map(x=>{const i=x.lastIndexOf(':');return {product:x.slice(0,i),score:Number(x.slice(i+1))};});
    const base=Number(sim.dataset.base||0);
    const scoreEl=sim.querySelector('.simResult strong');
    const rankEl=sim.querySelector('.simResult b');
    const gapEl=sim.querySelector('.simResult small');
    const panel=sim.querySelector('.rankPanel');
    const inputs=[...sim.querySelectorAll('input[type="checkbox"]')];
    const render=()=>{
      const score=Math.min(100, base + inputs.filter(i=>i.checked).reduce((s,i)=>s+Number(i.dataset.delta||0),0));
      const rows=[{product:xcmg,score,isX:true},...rivals].sort((a,b)=>b.score-a.score).map((r,i)=>({...r,rank:i+1}));
      const xrow=rows.find(r=>r.isX);
      const prev=rows[rows.findIndex(r=>r.isX)-1];
      scoreEl.textContent=score.toFixed(1).replace(/\.0$/,'');
      rankEl.textContent='模拟第'+xrow.rank;
      gapEl.textContent=prev ? '距前一名 '+prev.product+' 还差 '+Math.max(0,prev.score-score).toFixed(1)+' 分' : '已达到该工况第一名';
      const max=Math.max(...rows.map(r=>r.score),1);
      panel.classList.add('show');
      panel.innerHTML='<div class="bars">'+rows.map(r=>'<div class="'+(r.isX?'bar xcmg':'bar')+'"><span>'+r.rank+'</span><b>'+r.product+'</b><i><em style="width:'+(r.score/max*100).toFixed(1)+'%"></em></i><strong>'+r.score.toFixed(1).replace(/\.0$/,'')+'</strong></div>').join('')+'</div>';
    };
    inputs.forEach(i=>i.addEventListener('change',render));
    sim.querySelector('.resetSim')?.addEventListener('click',()=>{inputs.forEach(i=>i.checked=false);render();});
    render();
  });
}
function setupRawTabs(){
  document.querySelectorAll('.rawTabs button').forEach(btn=>btn.addEventListener('click',()=>{
    document.querySelectorAll('.rawTabs button').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.rawTable').forEach(t=>t.dataset.open=String(t.dataset.name===btn.dataset.table));
  }));
}
function setupPptBusinessTables(){
  const query=new URLSearchParams(window.location.search).get('lang');
  let stored='';
  try{stored=localStorage.getItem('xcmg-benchmark-language')||'';}catch(_error){}
  const language=query==='en'||(query!=='zh'&&stored==='en')?'en':'zh';
  document.querySelectorAll('.pptBusinessTable').forEach(item=>{
    item.open=language!=='en';
  });
}
function setupPageNavigation(){
  const toggle=document.querySelector('.navToggle');
  const menu=document.querySelector('.navMenu');
  if(toggle&&menu){
    toggle.addEventListener('click',()=>{
      const open=menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded',String(open));
      toggle.textContent=open?'收起导航':'页面导航';
    });
    menu.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{
      if(window.matchMedia('(max-width:900px)').matches){
        menu.classList.remove('open');
        toggle.setAttribute('aria-expanded','false');
        toggle.textContent='页面导航';
      }
    }));
  }
  const navLinks=menu?[...menu.querySelectorAll('a[href^="#"]')]:[];
  const tracked=navLinks.map(link=>({link,section:document.querySelector(link.getAttribute('href'))})).filter(item=>item.section);
  const initialHash=window.location.hash;
  let restoreHashEnabled=Boolean(initialHash&&initialHash!=='#');
  let hashRestoreTimer=0;
  let hashRestoreAttempts=0;
  let hashRestoreStableRounds=0;
  const hashRestoreStarted=window.performance.now();
  const navigationOffset=()=>window.matchMedia('(max-width:900px)').matches
    ? (document.querySelector('aside.nav')?.getBoundingClientRect().height||0)+8
    : 16;
  const scrollToSection=(section,hash,behavior='auto',updateHistory=false)=>{
    if(!section) return;
    if(updateHistory&&hash){
      const url=new URL(window.location.href);
      url.hash=hash;
      window.history.replaceState(window.history.state,'',url.pathname+url.search+url.hash);
    }
    const top=Math.max(0,window.scrollY+section.getBoundingClientRect().top-navigationOffset());
    if(behavior==='auto'){
      const scrollingElement=document.scrollingElement||document.documentElement;
      const previousBehavior=scrollingElement.style.scrollBehavior;
      scrollingElement.style.scrollBehavior='auto';
      scrollingElement.scrollTop=top;
      window.requestAnimationFrame(()=>{scrollingElement.style.scrollBehavior=previousBehavior;});
      return;
    }
    window.scrollTo({top,behavior});
  };
  navLinks.forEach(link=>link.addEventListener('click',event=>{
    if(event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey) return;
    const hash=link.getAttribute('href');
    const section=hash?document.querySelector(hash):null;
    if(!section) return;
    event.preventDefault();
    restoreHashEnabled=false;
    window.clearTimeout(hashRestoreTimer);
    navLinks.forEach(item=>item.classList.toggle('active',item===link));
    scrollToSection(section,hash,window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',true);
  }));
  let navTicking=false;
  const updateActiveNav=()=>{
    navTicking=false;
    if(!tracked.length) return;
    const offset=window.matchMedia('(max-width:900px)').matches
      ? navigationOffset()+24
      : 120;
    let active=tracked[0];
    tracked.forEach(item=>{if(item.section.getBoundingClientRect().top<=offset) active=item;});
    navLinks.forEach(link=>link.classList.toggle('active',link===active.link));
    menu?.querySelectorAll('.navGroup').forEach(group=>{
      const current=Boolean(group.querySelector('a.active'));
      group.classList.toggle('current',current);
      if(current) group.open=true;
    });
  };
  const scheduleActiveNav=()=>{
    if(navTicking) return;
    navTicking=true;
    window.requestAnimationFrame(updateActiveNav);
  };
  window.addEventListener('scroll',scheduleActiveNav,{passive:true});
  window.addEventListener('resize',scheduleActiveNav,{passive:true});
  scheduleActiveNav();
  const restoreHash=()=>{
    if(!restoreHashEnabled) return;
    const hash=initialHash;
    if(!hash||hash==='#') return;
    const section=document.querySelector(hash);
    if(!section) return;
    hashRestoreAttempts+=1;
    scrollToSection(section,hash,'auto',false);
    window.requestAnimationFrame(()=>{
      const delta=Math.abs(section.getBoundingClientRect().top-navigationOffset());
      hashRestoreStableRounds=delta<=3?hashRestoreStableRounds+1:0;
      scheduleActiveNav();
      const minimumWindowElapsed=window.performance.now()-hashRestoreStarted>=2600;
      const stable=hashRestoreStableRounds>=2&&document.readyState==='complete'&&minimumWindowElapsed;
      if(stable||hashRestoreAttempts>=32){
        restoreHashEnabled=false;
        window.clearTimeout(hashRestoreTimer);
        return;
      }
      window.clearTimeout(hashRestoreTimer);
      hashRestoreTimer=window.setTimeout(restoreHash,250);
    });
  };
  const cancelHashRestore=event=>{
    if(event?.target?.closest?.('aside.nav')) return;
    restoreHashEnabled=false;
    window.clearTimeout(hashRestoreTimer);
  };
  window.addEventListener('wheel',cancelHashRestore,{passive:true,once:true});
  window.addEventListener('touchstart',cancelHashRestore,{passive:true,once:true});
  window.addEventListener('pointerdown',cancelHashRestore,{passive:true,once:true});
  window.addEventListener('keydown',cancelHashRestore,{once:true});
  window.addEventListener('load',restoreHash,{once:true});
  document.addEventListener('xcmg:i18n-rendered',restoreHash);
  hashRestoreTimer=window.setTimeout(restoreHash,0);
  const backTop=document.querySelector('.backTop');
  if(backTop){
    const update=()=>backTop.classList.toggle('show',window.scrollY>640);
    window.addEventListener('scroll',update,{passive:true});
    update();
  }
}
function setupSidebarCollapse(){
  const layout=document.querySelector('.layout');
  const nav=layout?.querySelector('aside.nav');
  if(!layout||!nav)return;
  let toggle=nav.querySelector('.sidebarToggle');
  if(!toggle){
    toggle=document.createElement('button');
    toggle.className='sidebarToggle';
    toggle.type='button';
    toggle.setAttribute('aria-expanded','true');
    toggle.setAttribute('aria-controls',nav.querySelector('.navMenu')?.id||'page-nav');
    toggle.innerHTML='<span data-en="Collapse navigation">收起侧栏</span>';
    nav.insertBefore(toggle,nav.querySelector('.navToggle')||nav.querySelector('.navMenu'));
  }
  const desktop=window.matchMedia('(min-width:901px)');
  const storageKey='xcmg-dashboard-sidebar-collapsed';
  let stored=false;
  try{stored=localStorage.getItem(storageKey)==='1';}catch(error){stored=false;}
  const getLabel=collapsed=>{
    const isEn=document.documentElement.dataset.language==='en';
    return collapsed?(isEn?'Open navigation':'展开侧栏'):(isEn?'Collapse navigation':'收起侧栏');
  };
  const apply=(collapsed,persist)=>{
    const effective=desktop.matches&&collapsed;
    layout.classList.toggle('sidebarCollapsed',effective);
    toggle.setAttribute('aria-expanded',String(!effective));
    const text=getLabel(effective);
    const label=toggle.querySelector('span');
    if(label){
      label.dataset.en=effective?'Open navigation':'Collapse navigation';
      label.textContent=text;
    }
    toggle.setAttribute('aria-label',text);
    if(persist){
      stored=effective;
      try{localStorage.setItem(storageKey,effective?'1':'0');}catch(error){}
    }
  };
  apply(stored,false);
  toggle.addEventListener('click',()=>apply(!layout.classList.contains('sidebarCollapsed'),true));
  const sync=()=>apply(stored,false);
  if(desktop.addEventListener)desktop.addEventListener('change',sync);
  else if(desktop.addListener)desktop.addListener(sync);
  document.addEventListener('xcmg:i18n-rendered',()=>apply(layout.classList.contains('sidebarCollapsed'),false));
}
function setupMobileDisclosures(){
  const media=window.matchMedia('(max-width:720px)');
  const apply=()=>{
    document.querySelectorAll('[data-mobile-open]').forEach(item=>{
      item.open=media.matches ? item.dataset.mobileOpen==='true' : true;
    });
  };
  apply();
  if(media.addEventListener) media.addEventListener('change',apply);
  else if(media.addListener) media.addListener(apply);
}
setupPptBusinessTables();
setupMobileDisclosures();
setupRadars();
setupSimulators();
setupRawTabs();
setupSidebarCollapse();
setupPageNavigation();
(function () {
  'use strict';

  const chartSelector = '.sourceDataChart, .nativeChartPanel';
  const markSelector = [
    '.sourceChartMark',
    '.sourceChartSeries',
    '.sourceChartBubble',
    '.sourceChartPoint',
    '.sourceChartDonutArc',
    '.nativeChartMark'
  ].join(',');
  const legendSelector = [
    '.sourceChartLegendItem',
    '.nativeChartLegendItem',
    '.nativeDonutLegend li'
  ].join(',');
  let tooltip = null;

  function isEnglish() {
    return document.documentElement.lang.toLowerCase().startsWith('en');
  }

  function copy() {
    return isEnglish()
      ? {locked: 'Locked', clear: 'Clear chart selection'}
      : {locked: '已锁定', clear: '清除图表选择'};
  }

  function ensureTooltip() {
    if (tooltip) return tooltip;
    tooltip = document.createElement('div');
    tooltip.className = 'chartInteractionTooltip';
    tooltip.setAttribute('role', 'tooltip');
    tooltip.hidden = true;
    document.body.appendChild(tooltip);
    return tooltip;
  }

  function labelFor(node) {
    if (!node) return '';
    const explicit = isEnglish() ? node.dataset.tooltipEn : node.dataset.tooltip;
    if (explicit) return explicit.trim();
    const title = node.querySelector(':scope > title') || node.querySelector('title');
    if (title?.textContent?.trim()) return title.textContent.trim();
    return (node.textContent || '').replace(/\s+/g, ' ').trim();
  }

  function placeTooltip(event, node) {
    const tip = ensureTooltip();
    const rect = node.getBoundingClientRect();
    const requestedX = event?.clientX ?? rect.left + rect.width / 2;
    const requestedY = event?.clientY ?? rect.top;
    const margin = 12;
    const width = tip.offsetWidth;
    const height = tip.offsetHeight;
    const left = Math.max(margin, Math.min(window.innerWidth - width - margin, requestedX + 13));
    const above = requestedY - height - 12;
    const top = above >= margin
      ? above
      : Math.min(window.innerHeight - height - margin, requestedY + 16);
    tip.style.left = `${left}px`;
    tip.style.top = `${Math.max(margin, top)}px`;
  }

  function showTooltip(node, event) {
    const text = labelFor(node);
    if (!text) return;
    const tip = ensureTooltip();
    tip.textContent = text;
    tip.hidden = false;
    tip.classList.add('is-visible');
    window.requestAnimationFrame(() => placeTooltip(event, node));
  }

  function hideTooltip() {
    if (!tooltip) return;
    tooltip.classList.remove('is-visible');
    window.setTimeout(() => {
      if (!tooltip.classList.contains('is-visible')) tooltip.hidden = true;
    }, 130);
  }

  function renderableMark(node) {
    if (!(node instanceof SVGGraphicsElement)) return true;
    try {
      const box = node.getBBox();
      return box.width > 0.2 || box.height > 0.2;
    } catch (_) {
      return true;
    }
  }

  function seriesIndex(node) {
    const value = node?.dataset?.seriesIndex;
    return value === undefined ? '' : String(value);
  }

  function setPressed(node, pressed) {
    node.classList.toggle('is-focused', pressed);
    node.setAttribute('aria-pressed', pressed ? 'true' : 'false');
  }

  function applyFocus(chart, target) {
    const marks = [...chart.querySelectorAll(markSelector)].filter(renderableMark);
    const legends = [...chart.querySelectorAll(legendSelector)];
    const targetIsLegend = Boolean(target?.matches(legendSelector));
    const targetSeries = seriesIndex(target);
    const selectedMarks = targetIsLegend && targetSeries !== ''
      ? marks.filter((mark) => seriesIndex(mark) === targetSeries)
      : target ? [target] : [];

    chart.classList.toggle('chartHasFocus', selectedMarks.length > 0);
    marks.forEach((mark) => {
      const selected = selectedMarks.includes(mark);
      mark.classList.toggle('is-dimmed', selectedMarks.length > 0 && !selected);
      setPressed(mark, selected);
    });
    legends.forEach((legend) => {
      const selected = targetSeries !== '' && seriesIndex(legend) === targetSeries;
      legend.classList.toggle('is-dimmed', selectedMarks.length > 0 && targetSeries !== '' && !selected);
      setPressed(legend, selected);
    });
  }

  function clearFocus(chart) {
    chart.classList.remove('chartHasFocus');
    chart.querySelectorAll(`${markSelector},${legendSelector}`).forEach((node) => {
      node.classList.remove('is-focused', 'is-dimmed');
      node.setAttribute('aria-pressed', 'false');
    });
  }

  function updateLockState(chart) {
    const state = chart.querySelector(':scope > .chartLockState');
    if (!state) return;
    const language = copy();
    state.hidden = !chart.__chartLocked;
    state.querySelector('span').textContent = language.locked;
    state.setAttribute('aria-label', language.clear);
    state.title = chart.__chartLocked ? labelFor(chart.__chartLocked) : language.clear;
  }

  function clearLock(chart) {
    chart.__chartLocked = null;
    clearFocus(chart);
    updateLockState(chart);
    hideTooltip();
  }

  function lockTarget(chart, target, event) {
    if (chart.__chartLocked === target) {
      clearLock(chart);
      return;
    }
    chart.__chartLocked = target;
    applyFocus(chart, target);
    updateLockState(chart);
    showTooltip(target, event);
  }

  function eventTarget(chart, event) {
    const origin = event.target instanceof Element ? event.target : event.target?.parentElement;
    const target = origin?.closest(`${markSelector},${legendSelector}`);
    return target && chart.contains(target) ? target : null;
  }

  function prepareInteractiveNode(node, index) {
    if (!node.dataset.seriesIndex && node.matches(legendSelector)) {
      node.dataset.seriesIndex = String(index);
    }
    node.classList.add('chartInteractable');
    node.setAttribute('role', 'button');
    node.setAttribute('tabindex', '0');
    node.setAttribute('aria-pressed', 'false');
    const label = labelFor(node);
    if (label) node.setAttribute('aria-label', label);
  }

  function initializeChart(chart) {
    if (chart.dataset.chartInteractions === 'ready') return;
    chart.dataset.chartInteractions = 'ready';
    const marks = [...chart.querySelectorAll(markSelector)].filter(renderableMark);
    const legends = [...chart.querySelectorAll(legendSelector)];
    marks.forEach((node, index) => prepareInteractiveNode(node, index));
    legends.forEach((node, index) => prepareInteractiveNode(node, index));
    if (!marks.length) return;

    const lockState = document.createElement('button');
    lockState.className = 'chartLockState';
    lockState.type = 'button';
    lockState.hidden = true;
    lockState.innerHTML = '<span></span><b aria-hidden="true">×</b>';
    lockState.addEventListener('click', (event) => {
      event.stopPropagation();
      clearLock(chart);
    });
    chart.appendChild(lockState);
    updateLockState(chart);

    chart.addEventListener('pointerover', (event) => {
      const target = eventTarget(chart, event);
      if (!target || target.contains(event.relatedTarget)) return;
      if (!chart.__chartLocked) applyFocus(chart, target);
      showTooltip(target, event);
    });
    chart.addEventListener('pointermove', (event) => {
      const target = eventTarget(chart, event);
      if (target && tooltip && !tooltip.hidden) placeTooltip(event, target);
    });
    chart.addEventListener('pointerout', (event) => {
      const target = eventTarget(chart, event);
      if (!target || target.contains(event.relatedTarget)) return;
      if (chart.__chartLocked) applyFocus(chart, chart.__chartLocked);
      else clearFocus(chart);
      hideTooltip();
    });
    chart.addEventListener('focusin', (event) => {
      const target = eventTarget(chart, event);
      if (!target) return;
      if (!chart.__chartLocked) applyFocus(chart, target);
      showTooltip(target);
    });
    chart.addEventListener('focusout', (event) => {
      if (chart.contains(event.relatedTarget)) return;
      if (chart.__chartLocked) applyFocus(chart, chart.__chartLocked);
      else clearFocus(chart);
      hideTooltip();
    });
    chart.addEventListener('click', (event) => {
      const target = eventTarget(chart, event);
      if (target) {
        event.preventDefault();
        lockTarget(chart, target, event);
        return;
      }
      if (event.target.closest('.sourceChartViewport,.nativeChartCanvas,.sourceChartLegend,.nativeChartLegend,.nativeDonutLayout')) {
        clearLock(chart);
      }
    });
    chart.addEventListener('keydown', (event) => {
      const target = eventTarget(chart, event);
      if (event.key === 'Escape') {
        clearLock(chart);
      } else if (target && (event.key === 'Enter' || event.key === ' ')) {
        event.preventDefault();
        lockTarget(chart, target);
      }
    });
  }

  function initializeCharts(root) {
    root.querySelectorAll(chartSelector).forEach(initializeChart);
  }

  function init() {
    initializeCharts(document);
    const observer = new MutationObserver((records) => {
      records.forEach((record) => {
        record.addedNodes.forEach((node) => {
          if (!(node instanceof Element)) return;
          if (node.matches(chartSelector)) initializeChart(node);
          initializeCharts(node);
        });
      });
    });
    observer.observe(document.body, {childList: true, subtree: true});
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, {once: true});
  } else {
    init();
  }
})();
(function () {
  'use strict';

  let viewer = null;
  let activeItems = [];
  let activeIndex = 0;
  let lastTrigger = null;

  function isEnglish() {
    return document.documentElement.lang.toLowerCase().startsWith('en');
  }

  function copy() {
    return isEnglish()
      ? {
          eyebrow: 'Field evidence',
          close: 'Close image viewer',
          previous: 'Previous image',
          next: 'Next image'
        }
      : {
          eyebrow: '实景资料',
          close: '关闭图片查看',
          previous: '上一张图片',
          next: '下一张图片'
        };
  }

  function ensureViewer() {
    if (viewer) return viewer;
    viewer = document.createElement('dialog');
    viewer.className = 'mediaViewer';
    viewer.innerHTML = `
      <div class="mediaViewerShell">
        <header class="mediaViewerHeader">
          <div><small></small><h2></h2></div>
          <button type="button" class="mediaViewerClose" aria-label="关闭图片查看">×</button>
        </header>
        <div class="mediaViewerStage">
          <button type="button" class="mediaViewerNav mediaViewerPrevious" aria-label="上一张图片">←</button>
          <img class="mediaViewerImage" alt="">
          <button type="button" class="mediaViewerNav mediaViewerNext" aria-label="下一张图片">→</button>
        </div>
        <footer class="mediaViewerFooter">
          <span class="mediaViewerCount"></span>
          <p></p>
        </footer>
      </div>`;
    document.body.appendChild(viewer);

    viewer.querySelector('.mediaViewerClose').addEventListener('click', closeViewer);
    viewer.querySelector('.mediaViewerPrevious').addEventListener('click', () => move(-1));
    viewer.querySelector('.mediaViewerNext').addEventListener('click', () => move(1));
    viewer.addEventListener('click', (event) => {
      if (event.target === viewer) closeViewer();
    });
    viewer.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowLeft') {
        event.preventDefault();
        move(-1);
      } else if (event.key === 'ArrowRight') {
        event.preventDefault();
        move(1);
      }
    });
    viewer.addEventListener('close', () => {
      document.body.classList.remove('mediaViewerOpen');
      lastTrigger?.focus({preventScroll: true});
    });
    return viewer;
  }

  function groupFor(trigger) {
    const grid = trigger.closest('.sourceVisualGrid');
    const items = grid ? [...grid.querySelectorAll('.sourceVisualOpen')] : [trigger];
    return items.filter((item) => item.dataset.mediaSrc);
  }

  function textFor(item, key) {
    if (!item) return '';
    const englishKey = `${key}En`;
    return isEnglish()
      ? item.dataset[englishKey] || item.dataset[key] || ''
      : item.dataset[key] || '';
  }

  function renderViewer() {
    const dialog = ensureViewer();
    const item = activeItems[activeIndex];
    if (!item) return;
    const language = copy();
    const image = dialog.querySelector('.mediaViewerImage');
    const title = textFor(item, 'mediaTitle');
    const caption = textFor(item, 'mediaCaption');
    image.src = item.dataset.mediaSrc;
    image.alt = item.querySelector('img')?.alt || title;
    dialog.querySelector('.mediaViewerHeader small').textContent = language.eyebrow;
    dialog.querySelector('.mediaViewerHeader h2').textContent = title;
    dialog.querySelector('.mediaViewerFooter p').textContent = caption;
    dialog.querySelector('.mediaViewerCount').textContent =
      `${activeIndex + 1} / ${activeItems.length}`;
    const previous = dialog.querySelector('.mediaViewerPrevious');
    const next = dialog.querySelector('.mediaViewerNext');
    const multiple = activeItems.length > 1;
    previous.hidden = !multiple;
    next.hidden = !multiple;
    previous.setAttribute('aria-label', language.previous);
    next.setAttribute('aria-label', language.next);
    dialog.querySelector('.mediaViewerClose').setAttribute('aria-label', language.close);
  }

  function openViewer(trigger) {
    activeItems = groupFor(trigger);
    activeIndex = Math.max(0, activeItems.indexOf(trigger));
    lastTrigger = trigger;
    renderViewer();
    const dialog = ensureViewer();
    document.body.classList.add('mediaViewerOpen');
    if (typeof dialog.showModal === 'function') dialog.showModal();
    else dialog.setAttribute('open', '');
  }

  function closeViewer() {
    if (!viewer) return;
    if (typeof viewer.close === 'function' && viewer.open) viewer.close();
    else {
      viewer.removeAttribute('open');
      document.body.classList.remove('mediaViewerOpen');
    }
  }

  function move(step) {
    if (activeItems.length < 2) return;
    activeIndex = (activeIndex + step + activeItems.length) % activeItems.length;
    renderViewer();
  }

  function initialize(root) {
    root.querySelectorAll('.sourceVisualOpen:not([data-media-ready])').forEach((trigger) => {
      trigger.dataset.mediaReady = 'true';
      trigger.addEventListener('click', () => openViewer(trigger));
    });
  }

  function init() {
    initialize(document);
    const observer = new MutationObserver((records) => {
      records.forEach((record) => {
        record.addedNodes.forEach((node) => {
          if (node instanceof Element) initialize(node);
        });
      });
    });
    observer.observe(document.body, {childList: true, subtree: true});
    new MutationObserver(() => {
      if (viewer?.open) renderViewer();
    }).observe(document.documentElement, {attributes: true, attributeFilter: ['lang']});
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, {once: true});
  } else {
    init();
  }
})();
