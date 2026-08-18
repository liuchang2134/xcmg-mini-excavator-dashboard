const fs = require('fs');
const { chromium } = require('./playwright_loader.cjs');

const base = process.argv[2] || 'http://127.0.0.1:4174';
const pages = [
  'crane-rt-60t.html',
  'crane-rt-75t.html',
  'crane-rt-100t.html',
  'crane-rt-130t.html',
  'crane-rt-160t.html',
  'crane-at-150t.html'
];

function browserExecutable() {
  return [
    process.env.XCMG_QA_BROWSER,
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
  ].filter(Boolean).find((candidate) => fs.existsSync(candidate));
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
        for (const file of pages) {
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
          await page.goto(`${base}/${file}?lang=${language}`, { waitUntil: 'networkidle' });
          const state = await page.evaluate(() => ({
            lang: document.documentElement.lang,
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth,
            textLength: (document.querySelector('main')?.innerText || '').length,
            brokenImages: [...document.images]
              .filter((image) => image.getAttribute('src') && image.complete && image.naturalWidth === 0)
              .map((image) => image.src),
            sidebar: document.querySelectorAll('aside.nav').length,
            requiredSections: [
              'summary', 'market-insight', 'product-positioning', 'overall-score',
              'condition-overview', 'upgrade-roadmap', 'raw-data'
            ].filter((id) => document.getElementById(id)).length,
            conditionSections: document.querySelectorAll('section[id^="cond"]').length,
            ambiguousFallback: (document.body.innerText || '').includes('证据不足，暂不排名')
              || (document.body.innerText || '').includes('Insufficient evidence, not ranked'),
            narrowLongLabels: [...document.querySelectorAll('th, td, .navMenu a')]
              .filter((element) => {
                const text = (element.textContent || '').trim();
                const rect = element.getBoundingClientRect();
                return text.length >= 12 && rect.width > 0 && rect.width < 44;
              })
              .map((element) => (element.textContent || '').trim().slice(0, 80))
          }));
          const expectedLanguage = language === 'en' ? 'en-US' : 'zh-CN';
          if (state.lang !== expectedLanguage) {
            throw new Error(`${file}/${viewportName}/${language}: incorrect lang ${state.lang}`);
          }
          if (state.scrollWidth > state.clientWidth + 1) {
            throw new Error(
              `${file}/${viewportName}/${language}: horizontal overflow ${state.scrollWidth}/${state.clientWidth}`
            );
          }
          if (state.brokenImages.length || runtimeErrors.length) {
            throw new Error(
              `${file}/${viewportName}/${language}: runtime or image errors ` +
              `${JSON.stringify({ brokenImages: state.brokenImages, runtimeErrors })}`
            );
          }
          if (state.sidebar !== 1 || state.requiredSections !== 7 || state.conditionSections < 6) {
            throw new Error(
              `${file}/${viewportName}/${language}: incomplete structure ` +
              `${state.sidebar}/${state.requiredSections}/${state.conditionSections}`
            );
          }
          if (state.ambiguousFallback || state.narrowLongLabels.length) {
            throw new Error(
              `${file}/${viewportName}/${language}: ambiguous or cramped copy ` +
              `${JSON.stringify(state.narrowLongLabels.slice(0, 4))}`
            );
          }
          if (state.textLength < 12000) {
            throw new Error(`${file}/${viewportName}/${language}: unexpectedly short page`);
          }
          results.push(`${file}/${viewportName}/${language}`);
          await page.close();
        }
      }
    }
  } finally {
    await browser.close();
  }
  console.log(JSON.stringify({ checked: results.length, combinations: '6 pages x 2 languages x 2 viewports' }, null, 2));
})().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
