(function () {
  'use strict';

  function canonicalizePreviewUrl() {
    const url = new URL(window.location.href);
    if (!url.searchParams.has('rev') && !url.hash) return;
    url.searchParams.delete('rev');
    url.hash = '';
    window.history.replaceState(window.history.state, '', url.pathname + url.search);
  }

  canonicalizePreviewUrl();

  document.addEventListener('click', (event) => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const clickTarget = event.target instanceof Element ? event.target : event.target.parentElement;
    const link = clickTarget?.closest('a[href^="#"]');
    if (!link) return;

    const hash = link.getAttribute('href');
    if (!hash || hash === '#') return;
    const target = document.getElementById(decodeURIComponent(hash.slice(1)));
    if (!target) return;

    event.preventDefault();
    target.scrollIntoView({
      behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
      block: 'start'
    });

  });
})();
