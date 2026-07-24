const fs = require('fs');
const os = require('os');
const path = require('path');
const { chromium } = require('../ppt-integration-demo/node_modules/playwright-core');

const repo = path.resolve(__dirname, '..');
const base = process.argv[2] || 'http://127.0.0.1:4174';
const source = JSON.parse(
  fs.readFileSync(path.join(repo, 'data', 'ppt-insights', 'ppt-source-content.json'), 'utf8')
);
const slides = new Map(source.slides.map((record) => [record.id, record]));
const pages = [
  ['excavator-1-2t.html', 'excavator-1-2t'],
  ['excavator-2-3t.html', 'excavator-2-3t'],
  ['index.html', 'excavator-35t'],
  ['excavator-4-5t.html', 'excavator-4-5t'],
  ['excavator-5-6t.html', 'excavator-5-6t'],
  ['excavator-7-8t.html', 'excavator-7-8t'],
  ['excavator-8-10t.html', 'excavator-8-10t'],
  ['excavator-12-14t.html', 'excavator-12-14t'],
  ['excavator-14-16t-short-tail.html', 'excavator-14-16t-short-tail'],
  ['excavator-21-24t.html', 'excavator-21-24t'],
  ['excavator-24-28t.html', 'excavator-24-28t'],
  ['excavator-24-28t-short-tail.html', 'excavator-24-28t-short-tail'],
  ['excavator-28-33t.html', 'excavator-28-33t'],
  ['excavator-33-40t.html', 'excavator-33-40t'],
  ['excavator-40-60t.html', 'excavator-40-60t']
].map(([file, slug]) => {
  const sourceSlides = source.by_slug[slug] || [];
  return {
    file,
    slug,
    sourceSlides,
    expectedTables: sourceSlides.reduce(
      (total, slideId) => total + (slides.get(slideId)?.table_ids?.length || 0),
      0
    ),
    expectedVisuals: sourceSlides.reduce(
      (total, slideId) => total + (slides.get(slideId)?.visuals?.length || 0),
      0
    ),
    expectedDataCharts: sourceSlides.reduce(
      (total, slideId) => total + (slides.get(slideId)?.visuals || [])
        .filter((visual) => visual.kind === 'chart' && visual.chart_data).length,
      0
    )
  };
});

function browserExecutable() {
  return [
    process.env.XCMG_QA_BROWSER,
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
  ].filter(Boolean).find((candidate) => fs.existsSync(candidate));
}

async function inspect(page, spec, language, viewportName) {
  const query = language === 'en' ? '?lang=en' : '';
  await page.goto(`${base}/${spec.file}${query}`, { waitUntil: 'networkidle' });
  const target = spec.sourceSlides.length ? '#market-insight' : '#summary';
  await page.locator(target).scrollIntoViewIfNeeded();

  const state = await page.evaluate(() => ({
    lang: document.documentElement.lang,
    textLength: (document.querySelector('main')?.innerText || '').length,
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
    brokenImages: [...document.images]
      .filter((image) => image.complete && image.naturalWidth === 0)
      .map((image) => image.src),
    sourceSlides: document.querySelectorAll('[data-source-slide]').length,
    sourceSections: document.querySelectorAll('.sourceContentSection').length,
    sourceTables: document.querySelectorAll('.sourceTableBlock').length,
    sourceTableCaptions: document.querySelectorAll('.sourceTableBlock caption').length,
    fitTableOverflows: [...document.querySelectorAll('.sourceTableScrollFit')]
      .filter((wrapper) => wrapper.scrollWidth > wrapper.clientWidth + 1)
      .map((wrapper) => `${wrapper.scrollWidth}/${wrapper.clientWidth}`),
    emptyFitTableColumns: [...document.querySelectorAll('.sourceTableFit')].flatMap((table, tableIndex) => {
      const headers = [...table.querySelectorAll('thead th')];
      const bodyRows = [...table.querySelectorAll('tbody tr')];
      return headers.flatMap((header, columnIndex) => {
        const headerIsEmpty = !(header.textContent || '').trim();
        const bodyIsEmpty = bodyRows.every((row) => {
          const cell = row.children[columnIndex];
          return !cell || !(cell.textContent || '').trim();
        });
        return headerIsEmpty && bodyIsEmpty ? [`${tableIndex}:${columnIndex}`] : [];
      });
    }),
    sourceVisuals: document.querySelectorAll('.sourceVisual img').length,
    sourceDataCharts: document.querySelectorAll('.sourceDataChart').length,
    rasterChartImages: document.querySelectorAll('.sourceVisual-chart img').length,
    crampedChartLabels: [...document.querySelectorAll(
      '.sourceDataChart text:not(.sourceChartAxisTitle), .sourceDataChart .chartLegendLabel'
    )].filter((item) => {
      const text = (item.textContent || '').trim();
      const rect = item.getBoundingClientRect();
      return text.length >= 8 && rect.width > 0 && rect.width < 28;
    }).map((item) => item.textContent.trim()),
    bubbleLabelOverlaps: [...document.querySelectorAll('.sourceDataChart')].flatMap((chart) => {
      const labels = [...chart.querySelectorAll('.sourceChartBubbleLabel')]
        .map((label) => ({ text: label.textContent.trim(), rect: label.getBoundingClientRect() }));
      const overlaps = [];
      for (let left = 0; left < labels.length; left += 1) {
        for (let right = left + 1; right < labels.length; right += 1) {
          const a = labels[left].rect;
          const b = labels[right].rect;
          const intersects = a.left < b.right && a.right > b.left
            && a.top < b.bottom && a.bottom > b.top;
          if (intersects) overlaps.push(`${labels[left].text}/${labels[right].text}`);
        }
      }
      return overlaps;
    }),
    sourceParagraphs: document.querySelectorAll('.sourceParagraph').length
  }));

  const expectedLanguage = language === 'en' ? 'en-US' : 'zh-CN';
  if (state.lang !== expectedLanguage) {
    throw new Error(`${spec.file}/${viewportName}/${language}: incorrect lang ${state.lang}`);
  }
  if (state.scrollWidth > state.clientWidth + 1) {
    throw new Error(
      `${spec.file}/${viewportName}/${language}: horizontal overflow ${state.scrollWidth}/${state.clientWidth}`
    );
  }
  if (state.brokenImages.length) {
    throw new Error(
      `${spec.file}/${viewportName}/${language}: broken images ${state.brokenImages.join(', ')}`
    );
  }
  if (state.sourceSlides !== spec.sourceSlides.length) {
    throw new Error(
      `${spec.file}/${viewportName}/${language}: source slides ${state.sourceSlides}/${spec.sourceSlides.length}`
    );
  }
  if (state.sourceTables !== spec.expectedTables || state.sourceTableCaptions !== spec.expectedTables) {
    throw new Error(
      `${spec.file}/${viewportName}/${language}: source tables ${state.sourceTables}/${state.sourceTableCaptions}/${spec.expectedTables}`
    );
  }
  if (state.fitTableOverflows.length || state.emptyFitTableColumns.length) {
    throw new Error(
      `${spec.file}/${viewportName}/${language}: fit table regression ` +
      `overflow ${state.fitTableOverflows.join(', ') || 'none'}; ` +
      `empty columns ${state.emptyFitTableColumns.join(', ') || 'none'}`
    );
  }
  if (
    state.sourceVisuals + state.sourceDataCharts !== spec.expectedVisuals
    || state.sourceDataCharts !== spec.expectedDataCharts
    || state.rasterChartImages !== 0
  ) {
    throw new Error(
      `${spec.file}/${viewportName}/${language}: source visuals ` +
      `${state.sourceVisuals}+${state.sourceDataCharts}/${spec.expectedVisuals}; ` +
      `data charts ${state.sourceDataCharts}/${spec.expectedDataCharts}; ` +
      `raster charts ${state.rasterChartImages}`
    );
  }
  if (state.crampedChartLabels.length) {
    throw new Error(
      `${spec.file}/${viewportName}/${language}: cramped chart labels ` +
      state.crampedChartLabels.slice(0, 5).join(', ')
    );
  }
  if (state.bubbleLabelOverlaps.length) {
    throw new Error(
      `${spec.file}/${viewportName}/${language}: overlapping bubble labels ` +
      state.bubbleLabelOverlaps.slice(0, 5).join(', ')
    );
  }
  if (spec.sourceSlides.length && (state.sourceSections !== 4 || state.sourceParagraphs < 1)) {
    throw new Error(
      `${spec.file}/${viewportName}/${language}: incomplete source sections ${state.sourceSections}/${state.sourceParagraphs}`
    );
  }
  if (!spec.sourceSlides.length && state.sourceSections !== 0) {
    throw new Error(`${spec.file}/${viewportName}/${language}: unrelated source chapter was assigned`);
  }
  if (state.textLength < 6500) {
    throw new Error(
      `${spec.file}/${viewportName}/${language}: unexpectedly short page ${state.textLength}`
    );
  }

  let screenshot = '';
  if (
    ['index.html', 'excavator-7-8t.html', 'excavator-40-60t.html'].includes(spec.file)
    && language === 'zh'
  ) {
    screenshot = path.join(
      os.tmpdir(),
      `xcmg-source-${path.basename(spec.file, '.html')}-${viewportName}.png`
    );
    await page.locator(target).screenshot({ path: screenshot });
  }
  return {
    file: spec.file,
    viewportName,
    language,
    width: `${state.scrollWidth}/${state.clientWidth}`,
    sourceSlides: state.sourceSlides,
    sourceTables: state.sourceTables,
    sourceVisuals: state.sourceVisuals + state.sourceDataCharts,
    sourceDataCharts: state.sourceDataCharts,
    screenshot
  };
}

(async () => {
  const executablePath = browserExecutable();
  if (!executablePath) throw new Error('No local Edge or Chrome executable found');
  const browser = await chromium.launch({ headless: true, executablePath });
  const results = [];
  try {
    for (const [viewportName, viewport] of [
      ['desktop', { width: 1440, height: 900 }],
      ['mobile', { width: 390, height: 844 }]
    ]) {
      for (const language of ['zh', 'en']) {
        for (const spec of pages) {
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
          const result = await inspect(page, spec, language, viewportName);
          if (runtimeErrors.length) {
            throw new Error(
              `${spec.file}/${viewportName}/${language}: ${runtimeErrors.join(' | ')}`
            );
          }
          results.push(result);
          await page.close();
        }
      }
    }
  } finally {
    await browser.close();
  }

  console.log(JSON.stringify({
    checked: results.length,
    pages: pages.length,
    combinations: '15 pages x 2 languages x 2 viewports',
    sourceSlides: [...new Set(results.map((item) => item.sourceSlides))].sort((a, b) => a - b),
    desktopWidths: [...new Set(
      results.filter((item) => item.viewportName === 'desktop').map((item) => item.width)
    )],
    mobileWidths: [...new Set(
      results.filter((item) => item.viewportName === 'mobile').map((item) => item.width)
    )],
    screenshots: results.filter((item) => item.screenshot).map((item) => item.screenshot)
  }, null, 2));
})().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
