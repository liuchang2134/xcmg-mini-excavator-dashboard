const fs = require('fs');
const os = require('os');
const path = require('path');
const { chromium } = require('../ppt-integration-demo/node_modules/playwright-core');

const base = process.argv[2] || 'http://127.0.0.1:4174';
const expected = {
  sections: 8,
  slides: 26,
  tables: 19,
  visuals: 7
};

function browserExecutable() {
  return [
    process.env.XCMG_QA_BROWSER,
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
  ].filter(Boolean).find((candidate) => fs.existsSync(candidate));
}

async function assertHomepageEntry(page, language, viewportName) {
  const query = language === 'en' ? '?lang=en' : '';
  await page.goto(`${base}/arc.html${query}`, { waitUntil: 'networkidle' });

  const navEntry = page.locator('#arc-nav a[href^="excavator-market-overview.html"]');
  if ((await navEntry.count()) !== 0) {
    throw new Error(
      `${viewportName}/${language}: product-specific market entry leaked into the global navigation`
    );
  }

  const productLineEntry = page.locator('#line-excavators[href="#live"]');
  if ((await productLineEntry.count()) !== 1) {
    throw new Error(
      `${viewportName}/${language}: excavator product-line card does not target the excavator section`
    );
  }
  await productLineEntry.click();
  await page.waitForTimeout(700);
  const productLineTarget = await page.evaluate(() => ({
    pathname: window.location.pathname,
    hash: window.location.hash,
    sectionTop: document.querySelector('#live')?.getBoundingClientRect().top
  }));
  if (!/arc\.html$/.test(productLineTarget.pathname) || productLineTarget.hash !== '#live') {
    throw new Error(`${viewportName}/${language}: product-line card left the homepage`);
  }
  if (productLineTarget.sectionTop === undefined || Math.abs(productLineTarget.sectionTop) > 180) {
    throw new Error(
      `${viewportName}/${language}: excavator section was not brought into view (${productLineTarget.sectionTop})`
    );
  }

  const entry = page.locator(
    '#excavator-overview-gateway[href^="excavator-market-overview.html"]'
  );
  await entry.scrollIntoViewIfNeeded();
  if (!(await entry.isVisible())) {
    throw new Error(`${viewportName}/${language}: market-overview gateway is not visible`);
  }

  const screenshot = path.join(
    os.tmpdir(),
    `xcmg-market-overview-home-entry-${viewportName}-${language}.png`
  );
  await entry.screenshot({ path: screenshot });
  return screenshot;
}

async function inspectOverview(page, language, viewportName) {
  const query = language === 'en' ? '?lang=en' : '';
  await page.goto(`${base}/excavator-market-overview.html${query}`, {
    waitUntil: 'networkidle'
  });
  await page.locator('#environment').scrollIntoViewIfNeeded();

  const state = await page.evaluate(() => ({
    lang: document.documentElement.lang,
    textLength: (document.querySelector('main')?.innerText || '').length,
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
    brokenImages: [...document.images]
      .filter((image) => image.complete && image.naturalWidth === 0)
      .map((image) => image.src),
    sourceSections: document.querySelectorAll('.overviewSourceSection').length,
    sourceSlides: document.querySelectorAll('[data-source-slide]').length,
    sourceTables: document.querySelectorAll('.sourceTableBlock').length,
    sourceTableCaptions: document.querySelectorAll('.sourceTableBlock caption').length,
    sourceVisuals: document.querySelectorAll('.sourceVisual img').length,
    sourceDataCharts: document.querySelectorAll('.sourceDataChart').length,
    rasterChartImages: document.querySelectorAll('.sourceVisual-chart img').length,
    nativeCharts: document.querySelectorAll('.nativeChartPanel').length,
    productStructureChart: (() => {
      const slide = document.querySelector('[data-source-slide="11"]');
      const figure = slide?.querySelector('.sourceDataChart');
      const viewport = figure?.querySelector('.sourceChartViewport');
      const svg = figure?.querySelector('.sourceChartSvg');
      if (!slide || !figure || !viewport || !svg) return null;
      const viewportRect = viewport.getBoundingClientRect();
      const svgRect = svg.getBoundingClientRect();
      return {
        images: slide.querySelectorAll('img').length,
        caption: figure.querySelector('figcaption')?.textContent.trim(),
        captionEn: figure.querySelector('figcaption')?.getAttribute('data-en'),
        svgTop: Math.round(svgRect.top),
        viewportTop: Math.round(viewportRect.top),
        svgBottom: Math.round(svgRect.bottom),
        viewportBottom: Math.round(viewportRect.bottom)
      };
    })(),
    sourceParagraphs: document.querySelectorAll(
      '.sourceParagraph, .macroBodyLine, .macroActionLine'
    ).length,
    macroLayout: (() => {
      const slides = [...document.querySelectorAll('.sourceMacroSlide')];
      const images = [...document.querySelectorAll('.environmentContextImage img')];
      return {
        slides: slides.length,
        facts: document.querySelectorAll('.macroFact').length,
        trends: document.querySelectorAll('.macroTrendItem').length,
        actions: document.querySelectorAll('.macroActionItem').length,
        contextImages: images.map((image) => {
          const imageRect = image.getBoundingClientRect();
          const containerRect = image.parentElement.getBoundingClientRect();
          return {
            naturalWidth: image.naturalWidth,
            naturalHeight: image.naturalHeight,
            imageWidth: Math.round(imageRect.width),
            imageHeight: Math.round(imageRect.height),
            containerWidth: Math.round(containerRect.width),
            containerHeight: Math.round(containerRect.height),
            objectFit: getComputedStyle(image).objectFit
          };
        })
      };
    })(),
    oldExpandedScript: [...document.scripts].some((script) =>
      script.src.includes('excavator-market-overview-expanded.js')
    ),
    navLinks: [...document.querySelectorAll('#page-nav a')].map((link) =>
      link.getAttribute('href')
    ),
    heroLayout: (() => {
      const hero = document.querySelector('.sourceOverviewHero');
      const media = hero?.querySelector('.heroMedia');
      const image = media?.querySelector('img');
      if (!hero || !media || !image) return null;
      const mediaRect = media.getBoundingClientRect();
      const imageRect = image.getBoundingClientRect();
      return {
        columns: getComputedStyle(hero).gridTemplateColumns
          .split(' ')
          .filter(Boolean).length,
        mediaWidth: Math.round(mediaRect.width),
        imageWidth: Math.round(imageRect.width),
        mediaHeight: Math.round(mediaRect.height),
        imageHeight: Math.round(imageRect.height)
      };
    })(),
    extractionArtifacts: {
      standaloneClassLabels: [...document.querySelectorAll(
        '#class-structure .sourceNarrative > .sourceParagraph'
      )].filter((item) => ['微挖', '小挖', '中挖', '大挖'].includes(item.textContent.trim())).length,
      punctuatedHeadings: [...document.querySelectorAll('.sourceSlideHeader h3')]
        .filter((item) => /^[、，,]/.test(item.textContent.trim())).length
    },
    nativeChartLayout: (() => {
      const grid = document.querySelector(
        '.sourceNativeChartSlide > .nativeChartGrid'
      );
      if (!grid) return null;
      const gridRect = grid.getBoundingClientRect();
      const panels = [...grid.querySelectorAll(':scope > .nativeChartPanel')];
      return {
        columns: getComputedStyle(grid).gridTemplateColumns
          .split(' ')
          .filter(Boolean).length,
        gridWidth: Math.round(gridRect.width),
        panels: panels.map((panel) => {
          const panelRect = panel.getBoundingClientRect();
          const canvasRect = panel
            .querySelector('.nativeChartCanvas')
            ?.getBoundingClientRect();
          const svgRect = panel
            .querySelector('.nativeChartSvg')
            ?.getBoundingClientRect();
          return {
            panelWidth: Math.round(panelRect.width),
            canvasWidth: Math.round(canvasRect?.width || 0),
            svgWidth: Math.round(svgRect?.width || 0),
            rightOverflow: Math.max(0, Math.round(panelRect.right - gridRect.right))
          };
        })
      };
    })()
  }));

  const expectedLanguage = language === 'en' ? 'en-US' : 'zh-CN';
  if (state.lang !== expectedLanguage) {
    throw new Error(`${viewportName}/${language}: incorrect lang ${state.lang}`);
  }
  if (state.scrollWidth > state.clientWidth + 1) {
    throw new Error(
      `${viewportName}/${language}: horizontal overflow ${state.scrollWidth}/${state.clientWidth}`
    );
  }
  if (state.brokenImages.length) {
    throw new Error(
      `${viewportName}/${language}: broken images ${state.brokenImages.join(', ')}`
    );
  }
  const expectedHeroColumns = viewportName === 'mobile' ? 1 : 2;
  if (!state.heroLayout || state.heroLayout.columns !== expectedHeroColumns) {
    throw new Error(
      `${viewportName}/${language}: hero columns ` +
      `${state.heroLayout?.columns || 0}/${expectedHeroColumns}`
    );
  }
  if (
    state.heroLayout.imageWidth < state.heroLayout.mediaWidth - 2
    || state.heroLayout.imageHeight < state.heroLayout.mediaHeight - 2
  ) {
    throw new Error(
      `${viewportName}/${language}: hero image leaves unused media space ` +
      JSON.stringify(state.heroLayout)
    );
  }
  if (
    state.extractionArtifacts.standaloneClassLabels
    || state.extractionArtifacts.punctuatedHeadings
  ) {
    throw new Error(
      `${viewportName}/${language}: presentation extraction artifacts remain ` +
      JSON.stringify(state.extractionArtifacts)
    );
  }
  for (const key of ['sections', 'slides', 'tables']) {
    const actual = state[`source${key[0].toUpperCase()}${key.slice(1)}`];
    if (actual !== expected[key]) {
      throw new Error(`${viewportName}/${language}: ${key} ${actual}/${expected[key]}`);
    }
  }
  if (
    state.sourceVisuals + state.sourceDataCharts + state.nativeCharts !== expected.visuals
    || state.nativeCharts !== 4
    || state.sourceDataCharts !== 3
    || state.rasterChartImages !== 0
  ) {
    throw new Error(
      `${viewportName}/${language}: visual units ` +
      `${state.sourceVisuals}+${state.sourceDataCharts}+${state.nativeCharts}/` +
      `${expected.visuals}; raster charts ${state.rasterChartImages}`
    );
  }
  if (
    !state.productStructureChart
    || state.productStructureChart.images !== 0
    || state.productStructureChart.captionEn !== 'Excavator size-class structure'
    || state.productStructureChart.svgTop < state.productStructureChart.viewportTop - 1
    || state.productStructureChart.svgBottom > state.productStructureChart.viewportBottom + 1
  ) {
    throw new Error(
      `${viewportName}/${language}: product-structure chart is cropped or rasterized ` +
      JSON.stringify(state.productStructureChart)
    );
  }
  if (!state.nativeChartLayout || state.nativeChartLayout.panels.length !== 4) {
    throw new Error(`${viewportName}/${language}: responsive chart layout is missing`);
  }
  const expectedColumns = viewportName === 'desktop' ? 2 : 1;
  if (state.nativeChartLayout.columns !== expectedColumns) {
    throw new Error(
      `${viewportName}/${language}: chart columns ` +
      `${state.nativeChartLayout.columns}/${expectedColumns}`
    );
  }
  for (const [index, panel] of state.nativeChartLayout.panels.entries()) {
    if (
      panel.rightOverflow > 1
      || panel.svgWidth > panel.canvasWidth + 1
      || panel.panelWidth > state.nativeChartLayout.gridWidth + 1
    ) {
      throw new Error(
        `${viewportName}/${language}: chart ${index + 1} does not follow its container ` +
        JSON.stringify(panel)
      );
    }
  }
  if (state.sourceTableCaptions !== expected.tables) {
    throw new Error(
      `${viewportName}/${language}: table captions ${state.sourceTableCaptions}/${expected.tables}`
    );
  }
  if (state.sourceParagraphs < 40 || state.textLength < 10000) {
    throw new Error(
      `${viewportName}/${language}: source narrative unexpectedly short ` +
      `${state.sourceParagraphs}/${state.textLength}`
    );
  }
  if (
    !state.macroLayout
    || state.macroLayout.slides !== 5
    || state.macroLayout.facts !== 15
    || state.macroLayout.trends < 15
    || state.macroLayout.actions < 15
    || state.macroLayout.contextImages.length !== 3
  ) {
    throw new Error(
      `${viewportName}/${language}: macro report structure is incomplete ` +
      JSON.stringify(state.macroLayout)
    );
  }
  for (const [index, image] of state.macroLayout.contextImages.entries()) {
    if (
      image.naturalWidth < 900
      || image.naturalHeight < 480
      || image.imageWidth > image.containerWidth + 1
      || image.imageHeight > image.containerHeight + 1
      || image.objectFit !== 'contain'
    ) {
      throw new Error(
        `${viewportName}/${language}: context image ${index + 1} is low-resolution or cropped ` +
        JSON.stringify(image)
      );
    }
  }
  if (state.oldExpandedScript) {
    throw new Error(`${viewportName}/${language}: obsolete hand-written overview is still loaded`);
  }

  const expectedAnchors = [
    '#environment',
    '#industry',
    '#competition',
    '#class-structure',
    '#portfolio',
    '#roadmap',
    '#sales-plan',
    '#intelligence'
  ];
  for (const anchor of expectedAnchors) {
    if (!state.navLinks.includes(anchor)) {
      throw new Error(`${viewportName}/${language}: navigation anchor ${anchor} is missing`);
    }
  }

  const fullScreenshot = path.join(
    os.tmpdir(),
    `xcmg-market-overview-${viewportName}-${language}.png`
  );
  await page.screenshot({ path: fullScreenshot, fullPage: true });

  const selectedScreenshots = [];
  if (language === 'zh') {
    for (const id of viewportName === 'desktop'
      ? ['environment', 'industry', 'competition', 'roadmap']
      : ['environment', 'industry', 'competition']) {
      const target = page.locator(`#${id}`);
      await target.scrollIntoViewIfNeeded();
      const screenshot = path.join(
        os.tmpdir(),
        `xcmg-market-overview-${id}-${viewportName}.png`
      );
      await target.screenshot({ path: screenshot });
      selectedScreenshots.push(screenshot);
    }

    const nativeCharts = page.locator('.sourceNativeChartSlide');
    await nativeCharts.scrollIntoViewIfNeeded();
    const chartScreenshot = path.join(
      os.tmpdir(),
      `xcmg-market-overview-native-charts-${viewportName}.png`
    );
    await nativeCharts.screenshot({ path: chartScreenshot });
    selectedScreenshots.push(chartScreenshot);
  }

  return {
    viewportName,
    language,
    width: `${state.scrollWidth}/${state.clientWidth}`,
    textLength: state.textLength,
    sourceParagraphs: state.sourceParagraphs,
    sourceSlides: state.sourceSlides,
    sourceTables: state.sourceTables,
    sourceVisuals: state.sourceVisuals + state.sourceDataCharts + state.nativeCharts,
    chartColumns: state.nativeChartLayout.columns,
    screenshots: [fullScreenshot, ...selectedScreenshots]
  };
}

(async () => {
  const executablePath = browserExecutable();
  if (!executablePath) throw new Error('No local Edge or Chrome executable found');
  const browser = await chromium.launch({ headless: true, executablePath });
  const results = [];
  const homepageScreenshots = [];
  try {
    for (const [viewportName, viewport, checkHomepage] of [
      ['desktop', { width: 1440, height: 900 }, true],
      ['zoom125', { width: 1152, height: 720 }, false],
      ['zoom150', { width: 960, height: 700 }, false],
      ['mobile', { width: 390, height: 844 }, true]
    ]) {
      for (const language of ['zh', 'en']) {
        const page = await browser.newPage({ viewport });
        const runtimeErrors = [];
        page.on('console', (message) => {
          if (
            message.type() === 'error'
            && !message.text().includes('favicon.ico')
            && !message.text().startsWith('Failed to load resource:')
          ) {
            runtimeErrors.push(message.text());
          }
        });
        page.on('pageerror', (error) => runtimeErrors.push(error.message));
        page.on('response', (response) => {
          if (response.status() >= 400 && !response.url().endsWith('/favicon.ico')) {
            runtimeErrors.push(`HTTP ${response.status()} ${response.url()}`);
          }
        });

        if (checkHomepage) {
          homepageScreenshots.push(
            await assertHomepageEntry(page, language, viewportName)
          );
        }
        const result = await inspectOverview(page, language, viewportName);
        if (runtimeErrors.length) {
          throw new Error(
            `${viewportName}/${language}: ${runtimeErrors.join(' | ')}`
          );
        }
        results.push(result);
        await page.close();
      }
    }
  } finally {
    await browser.close();
  }

  console.log(JSON.stringify({
    checked: results.length,
    combinations: '2 languages x desktop, 125%, 150% and mobile viewports',
    expected,
    desktopWidths: results
      .filter((item) => item.viewportName === 'desktop')
      .map((item) => item.width),
    mobileWidths: results
      .filter((item) => item.viewportName === 'mobile')
      .map((item) => item.width),
    chartColumns: Object.fromEntries(
      results.map((item) => [
        `${item.viewportName}/${item.language}`,
        item.chartColumns
      ])
    ),
    homepageScreenshots,
    overviewScreenshots: results.flatMap((item) => item.screenshots)
  }, null, 2));
})().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
