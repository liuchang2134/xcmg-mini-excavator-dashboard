(function () {
  'use strict';

  const NAV_LINK_SELECTOR = '#page-nav a[href^="#"]';
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let menu = null;
  let sections = [];
  let activeId = '';
  let updateFrame = 0;
  let refreshTimer = 0;
  let pulseTimer = 0;
  let scrollLock = null;
  let initialHash = '';
  let restoreHashEnabled = false;

  function canonicalizePreviewUrl() {
    const url = new URL(window.location.href);
    initialHash = url.hash;
    restoreHashEnabled = Boolean(initialHash && initialHash !== '#');
    if (!url.searchParams.has('rev')) return;
    url.searchParams.delete('rev');
    window.history.replaceState(window.history.state, '', url.pathname + url.search + url.hash);
  }

  function navigationOffset() {
    const compactNavigation = window.matchMedia('(max-width: 56.249rem)').matches;
    if (!compactNavigation) return 16;
    return (document.querySelector('aside.nav')?.getBoundingClientRect().height || 0) + 8;
  }

  function scrollToTarget(target, behavior = 'auto', updateHistory = false) {
    if (!target) return;
    const id = target.id;
    if (updateHistory && id) {
      const url = new URL(window.location.href);
      url.hash = id;
      window.history.replaceState(window.history.state, '', url.pathname + url.search + url.hash);
    }
    const top = Math.max(0, window.scrollY + target.getBoundingClientRect().top - navigationOffset());
    window.scrollTo({top, behavior});
  }

  function restoreInitialHash() {
    if (!restoreHashEnabled) return;
    const hash = initialHash || window.location.hash;
    if (!hash || hash === '#') return;
    const target = document.getElementById(decodeURIComponent(hash.slice(1)));
    if (!target) return;
    const entry = sections.find((item) => item.target === target);
    if (entry) {
      scrollLock = {id: entry.id, started: performance.now()};
      setActive(entry.id);
    }
    scrollToTarget(target, 'auto', false);
  }

  function refreshSections() {
    const seen = new Set();
    sections = [...document.querySelectorAll(NAV_LINK_SELECTOR)].flatMap((link) => {
      const hash = link.getAttribute('href') || '';
      const id = decodeURIComponent(hash.slice(1));
      const target = document.getElementById(id);
      link.classList.toggle('navSubitem', /^cond\d+$/.test(id));
      if (!id || !target || seen.has(id)) return [];
      seen.add(id);
      return [{id, link, target}];
    }).sort((a, b) => (a.target.getBoundingClientRect().top + window.scrollY) - (b.target.getBoundingClientRect().top + window.scrollY));
    document.body.dataset.navReady = sections.length ? 'true' : 'false';
    scheduleUpdate();
  }

  function keepActiveLinkVisible(link) {
    if (!link || getComputedStyle(menu).display === 'none') return;
    const menuRect = menu.getBoundingClientRect();
    const linkRect = link.getBoundingClientRect();
    const topLimit = menuRect.top + 6;
    const bottomLimit = menuRect.bottom - 8;
    let delta = 0;
    if (linkRect.top < topLimit) delta = linkRect.top - topLimit;
    else if (linkRect.bottom > bottomLimit) delta = linkRect.bottom - bottomLimit;
    if (Math.abs(delta) > 1) menu.scrollBy({top: delta, behavior: reducedMotion.matches ? 'auto' : 'smooth'});
  }

  function setActive(id) {
    const entry = sections.find((item) => item.id === id) || sections[0];
    if (!entry) return;
    const changed = activeId !== entry.id;
    activeId = entry.id;
    sections.forEach((item) => {
      const selected = item.id === activeId;
      item.link.classList.toggle('is-active', selected);
      if (selected) item.link.setAttribute('aria-current', 'location'); else item.link.removeAttribute('aria-current');
    });
    document.querySelectorAll('#page-nav .navGroup').forEach((group) => {
      const containsActiveLink = Boolean(group.querySelector('a.is-active'));
      group.classList.toggle('is-current', containsActiveLink);
      if (group.dataset.userCollapsed === 'true') group.open = false;
      else if (changed && containsActiveLink) group.open = true;
    });
    document.querySelector('aside.nav')?.setAttribute('data-current-section', activeId);
    if (changed) keepActiveLinkVisible(entry.link);
  }

  function updateNavigation() {
    updateFrame = 0;
    if (!sections.length) return;
    const compactNavigation = window.matchMedia('(max-width: 56.249rem)').matches;
    if (compactNavigation && menu.classList.contains('open')) return;
    const stickyNav = compactNavigation ? document.querySelector('aside.nav')?.getBoundingClientRect().height || 0 : 0;
    if (scrollLock) {
      const lockedEntry = sections.find((entry) => entry.id === scrollLock.id);
      const settled = lockedEntry && Math.abs(lockedEntry.target.getBoundingClientRect().top - (compactNavigation ? stickyNav : 16)) < 70;
      if (lockedEntry && !settled && performance.now() - scrollLock.started < 2600) {
        setActive(lockedEntry.id);
        return;
      }
      scrollLock = null;
    }
    const activationLine = Math.min(window.innerHeight * 0.28, 230) + stickyNav;
    let current = sections[0];
    sections.forEach((entry) => {
      if (entry.target.getBoundingClientRect().top <= activationLine) current = entry;
    });
    if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 3) current = sections[sections.length - 1];
    setActive(current.id);
  }

  function scheduleUpdate() {
    if (updateFrame) return;
    updateFrame = window.requestAnimationFrame(updateNavigation);
  }

  function pulseTarget(target) {
    window.clearTimeout(pulseTimer);
    target.classList.remove('navTargetPulse');
    void target.offsetWidth;
    target.classList.add('navTargetPulse');
    pulseTimer = window.setTimeout(() => target.classList.remove('navTargetPulse'), 850);
  }

  canonicalizePreviewUrl();
  menu = document.querySelector('#page-nav');
  if (!menu) return;
  menu.querySelectorAll('.navGroup>summary').forEach((summary) => {
    summary.addEventListener('click', (event) => {
      event.preventDefault();
      const group = summary.parentElement;
      const nextOpen = !group.open;
      group.open = nextOpen;
      group.dataset.userCollapsed = nextOpen ? 'false' : 'true';
    });
  });
  refreshSections();

  document.addEventListener('click', (event) => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const clickTarget = event.target instanceof Element ? event.target : event.target.parentElement;
    const link = clickTarget?.closest('a[href^="#"]');
    if (!link) return;
    const hash = link.getAttribute('href');
    if (!hash || hash === '#') return;
    const target = document.getElementById(decodeURIComponent(hash.slice(1)));
    event.preventDefault();
    if (!target) return;
    restoreHashEnabled = false;
    const entry = sections.find((item) => item.target === target);
    if (entry) {
      scrollLock = {id: entry.id, started: performance.now()};
      setActive(entry.id);
    } else {
      scrollLock = null;
    }
    pulseTarget(target);
    scrollToTarget(target, reducedMotion.matches ? 'auto' : 'smooth', true);
  });

  window.addEventListener('scroll', scheduleUpdate, {passive: true});
  const cancelHashRestore = () => {
    scrollLock = null;
    restoreHashEnabled = false;
  };
  window.addEventListener('wheel', cancelHashRestore, {passive: true, once: true});
  window.addEventListener('touchstart', cancelHashRestore, {passive: true, once: true});
  window.addEventListener('pointerdown', cancelHashRestore, {passive: true, once: true});
  window.addEventListener('keydown', cancelHashRestore, {once: true});
  window.addEventListener('resize', () => {
    window.clearTimeout(refreshTimer);
    refreshTimer = window.setTimeout(refreshSections, 100);
  }, {passive: true});

  const main = document.querySelector('main');
  if (main) {
    const observer = new MutationObserver(() => {
      window.clearTimeout(refreshTimer);
      refreshTimer = window.setTimeout(refreshSections, 60);
    });
    observer.observe(main, {childList: true, subtree: true});
  }
  window.addEventListener('load', restoreInitialHash, {once: true});
  document.addEventListener('xcmg:i18n-rendered', restoreInitialHash);
  [0, 250, 900, 1600, 2600].forEach((delay) => {
    window.setTimeout(() => {
      refreshSections();
      restoreInitialHash();
    }, delay);
  });
})();
