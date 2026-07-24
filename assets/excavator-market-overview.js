(function () {
  const groupSelectors = [
    '.cycleChart',
    '.mixRows',
    '.tonnageHeatmap',
    '.brandBars',
    '.portfolioCards',
    '.issueBars',
    '.modelTargetBars',
    '.targetColumns'
  ];

  const itemSelector = ':scope > *';

  function clearGroup(group) {
    group.classList.remove('has-focus');
    group.querySelectorAll(':scope > .is-focused').forEach((item) => {
      item.classList.remove('is-focused');
    });
  }

  function focusItem(group, item) {
    clearGroup(group);
    group.classList.add('has-focus');
    item.classList.add('is-focused');
  }

  function setupInteractions() {
    groupSelectors.forEach((selector) => {
      document.querySelectorAll(selector).forEach((group) => {
        group.querySelectorAll(itemSelector).forEach((item) => {
          if (item.dataset.overviewInteractive === 'true') return;
          item.dataset.overviewInteractive = 'true';
          item.classList.add('interactiveDatum');
          if (!item.hasAttribute('tabindex')) item.tabIndex = 0;

          item.addEventListener('pointerenter', () => focusItem(group, item));
          item.addEventListener('focus', () => focusItem(group, item));
          item.addEventListener('pointerleave', () => {
            if (!item.matches(':focus')) clearGroup(group);
          });
          item.addEventListener('blur', () => clearGroup(group));
        });
      });
    });
  }

  setupInteractions();
  const main = document.querySelector('main');
  if (main) {
    const observer = new MutationObserver(setupInteractions);
    observer.observe(main, { childList: true, subtree: true });
  }

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    document.querySelectorAll('.has-focus').forEach(clearGroup);
    if (document.activeElement instanceof HTMLElement) document.activeElement.blur();
  });
})();
