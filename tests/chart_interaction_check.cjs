const fs = require('fs');
const { chromium } = require('../ppt-integration-demo/node_modules/playwright-core');

const base = process.argv[2] || 'http://127.0.0.1:4174';

function browserExecutable() {
  return [
    process.env.XCMG_QA_BROWSER,
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
  ].filter(Boolean).find((candidate) => fs.existsSync(candidate));
}

async function assertMarkInteraction(page, chart, mark, label) {
  await chart.scrollIntoViewIfNeeded();
  await mark.hover();
  await page.waitForTimeout(140);

  if (!(await page.locator('.chartInteractionTooltip.is-visible').count())) {
    throw new Error(`${label}: hover tooltip did not appear`);
  }
  if (!(await chart.locator('.is-focused').count())) {
    throw new Error(`${label}: hover did not focus a chart mark`);
  }
  if (!(await chart.locator('.is-dimmed').count())) {
    throw new Error(`${label}: hover did not dim comparison marks`);
  }

  await mark.click();
  await page.mouse.move(4, 4);
  await page.waitForTimeout(80);
  if (!(await chart.locator('.chartLockState:not([hidden])').count())) {
    throw new Error(`${label}: click did not lock the selection`);
  }
  if ((await mark.getAttribute('aria-pressed')) !== 'true') {
    throw new Error(`${label}: locked mark is missing aria-pressed`);
  }

  await chart.locator('.chartLockState').click();
  if (await chart.locator('.is-focused,.is-dimmed').count()) {
    throw new Error(`${label}: clear control did not restore all marks`);
  }
}

async function inspectOverview(page, language, viewportName) {
  const query = language === 'en' ? '?lang=en' : '';
  await page.goto(`${base}/excavator-market-overview.html${query}`, {
    waitUntil: 'networkidle'
  });

  const area = page.locator('.nativeChartPanel').first();
  await assertMarkInteraction(
    page,
    area,
    area.locator('.nativeChartMark').nth(1),
    `${viewportName}/${language}/area`
  );

  const structure = page.locator('[data-source-slide="11"] .sourceDataChart');
  await assertMarkInteraction(
    page,
    structure,
    structure.locator('.chartInteractable').first(),
    `${viewportName}/${language}/product-structure`
  );

  const donut = page.locator('.nativeChartPanel').nth(2);
  const legend = donut.locator('.nativeDonutLegend li').nth(1);
  await legend.hover();
  await page.waitForTimeout(120);
  if (
    (await donut.locator('.nativeDonutSegment.is-focused').count()) !== 1
    || (await donut.locator('.nativeDonutLegend li.is-focused').count()) !== 1
  ) {
    throw new Error(`${viewportName}/${language}/donut: legend linkage failed`);
  }
  await legend.click();
  await page.mouse.move(4, 4);
  if (!(await donut.locator('.chartLockState:not([hidden])').count())) {
    throw new Error(`${viewportName}/${language}/donut: legend click did not lock`);
  }
  await page.keyboard.press('Escape');
  if (await donut.locator('.is-focused,.is-dimmed').count()) {
    throw new Error(`${viewportName}/${language}/donut: Escape did not clear`);
  }
}

async function inspectTonnage(page, language, viewportName) {
  const query = language === 'en' ? '?lang=en' : '';
  await page.goto(`${base}/index.html${query}`, { waitUntil: 'networkidle' });
  const chart = page.locator('.sourceDataChart').first();
  await assertMarkInteraction(
    page,
    chart,
    chart.locator('.chartInteractable').first(),
    `${viewportName}/${language}/tonnage`
  );
}

(async () => {
  const executablePath = browserExecutable();
  if (!executablePath) throw new Error('No local Edge or Chrome executable found');
  const browser = await chromium.launch({ headless: true, executablePath });
  const results = [];
  try {
    for (const [viewportName, viewport, language] of [
      ['desktop', { width: 1440, height: 900 }, 'zh'],
      ['mobile', { width: 390, height: 844 }, 'en']
    ]) {
      const page = await browser.newPage({ viewport });
      const runtimeErrors = [];
      page.on('pageerror', (error) => runtimeErrors.push(error.message));
      page.on('console', (message) => {
        if (
          message.type() === 'error'
          && !message.text().includes('favicon.ico')
          && !message.text().startsWith('Failed to load resource:')
        ) {
          runtimeErrors.push(message.text());
        }
      });

      await inspectOverview(page, language, viewportName);
      await inspectTonnage(page, language, viewportName);
      if (runtimeErrors.length) {
        throw new Error(
          `${viewportName}/${language}: ${runtimeErrors.join(' | ')}`
        );
      }
      results.push(`${viewportName}/${language}`);
      await page.close();
    }
  } finally {
    await browser.close();
  }

  console.log(JSON.stringify({
    checked: results,
    behaviors: [
      'hover focus and dim',
      'tooltip',
      'click lock',
      'clear control',
      'Escape clear',
      'legend-to-mark linkage'
    ]
  }, null, 2));
})().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
