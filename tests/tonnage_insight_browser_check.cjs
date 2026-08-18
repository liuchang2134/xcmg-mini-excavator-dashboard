const fs = require('fs');
const os = require('os');
const path = require('path');
const { chromium } = require('./playwright_loader.cjs');

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
  const publishedSlides = sourceSlides.filter(
    (slideId) => slides.get(slideId)?.section !== 'comparison'
  );
  return {
    file,
    slug,
    sourceSlides,
    publishedSlides,
    excludedComparisonSlides: sourceSlides.filter(
      (slideId) => slides.get(slideId)?.section === 'comparison'
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
  const target = '#market-insight';
  await page.locator(target).scrollIntoViewIfNeeded();

  const state = await page.evaluate(() => ({
    lang: document.documentElement.lang,
    textLength: (document.querySelector('main')?.innerText || '').length,
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
    brokenImages: [...document.images]
      .filter((image) => image.complete && image.naturalWidth === 0)
      .map((image) => image.src),
    sourceSlideIds: [...document.querySelectorAll('[data-source-slide]')]
      .map((element) => `slide-${String(element.dataset.sourceSlide).padStart(3, '0')}`),
    requiredSections: [
      'summary', 'market-insight', 'product-positioning', 'overall',
      'condition-overview', 'cond1', 'cond2', 'cond3', 'cond4', 'cond5', 'cond6',
      'upgrade-roadmap', 'raw'
    ].filter((id) => document.getElementById(id)).length,
    obsoleteSections: ['job-applications', 'engineering-insight', 'source-analysis']
      .filter((id) => document.getElementById(id)),
    conditionBlocks: document.querySelectorAll('.conditionSection[id^="cond"]').length,
    roadmapRows: document.querySelectorAll('#upgrade-roadmap tbody tr').length,
    rawTables: document.querySelectorAll('#raw table').length,
    conditionImages: document.querySelectorAll('.conditionContextCard img').length,
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
    sourceParagraphs: document.querySelectorAll('.decisionSourceArticle p, .conditionContextCard p').length
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
  const actualSlides = [...new Set(state.sourceSlideIds)].sort();
  const expectedSlides = [...spec.publishedSlides].sort();
  if (JSON.stringify(actualSlides) !== JSON.stringify(expectedSlides)) {
    throw new Error(
      `${spec.file}/${viewportName}/${language}: published source slides ` +
      `${JSON.stringify(actualSlides)}/${JSON.stringify(expectedSlides)}`
    );
  }
  if (spec.excludedComparisonSlides.some((slideId) => actualSlides.includes(slideId))) {
    throw new Error(
      `${spec.file}/${viewportName}/${language}: obsolete PPT comparison slide was published`
    );
  }
  if (state.requiredSections !== 13 || state.obsoleteSections.length) {
    throw new Error(
      `${spec.file}/${viewportName}/${language}: information architecture ` +
      `${state.requiredSections}/13; obsolete ${state.obsoleteSections.join(', ') || 'none'}`
    );
  }
  if (state.conditionBlocks !== 6 || state.roadmapRows < 1 || state.rawTables < 1) {
    throw new Error(
      `${spec.file}/${viewportName}/${language}: condition/roadmap/raw coverage ` +
      `${state.conditionBlocks}/${state.roadmapRows}/${state.rawTables}`
    );
  }
  if (state.rasterChartImages !== 0) {
    throw new Error(`${spec.file}/${viewportName}/${language}: raster chart image remains`);
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
  if (spec.publishedSlides.length && state.sourceParagraphs < 1) {
    throw new Error(
      `${spec.file}/${viewportName}/${language}: PPT narrative is missing from integrated sections`
    );
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
    sourceSlides: actualSlides.length,
    conditionImages: state.conditionImages,
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
