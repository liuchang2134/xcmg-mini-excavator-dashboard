const fs = require('fs');
const path = require('path');
const { chromium } = require('../ppt-integration-demo/node_modules/playwright-core');

const base = process.argv[2] || 'http://127.0.0.1:4174';
const pages = [
  'arc.html',
  'excavator-market-overview.html',
  'excavator-1-2t.html',
  'excavator-2-3t.html',
  'index.html',
  'excavator-4-5t.html',
  'excavator-5-6t.html',
  'excavator-7-8t.html',
  'excavator-8-10t.html',
  'excavator-12-14t.html',
  'excavator-14-16t-short-tail.html',
  'excavator-21-24t.html',
  'excavator-24-28t.html',
  'excavator-24-28t-short-tail.html',
  'excavator-28-33t.html',
  'excavator-33-40t.html',
  'excavator-40-60t.html'
];

function browserExecutable() {
  return [
    process.env.XCMG_QA_BROWSER,
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
  ].filter(Boolean).find((candidate) => fs.existsSync(candidate));
}

async function loadLazyImages(page) {
  await page.evaluate(() => {
    for (const image of document.images) image.loading = 'eager';
  });
  await page.waitForFunction(
    () => [...document.images].every((image) => image.complete),
    null,
    { timeout: 20000 }
  ).catch(() => null);
  await page.evaluate(() =>
    Promise.all([...document.images].map((image) => image.decode().catch(() => null)))
  );
}

(async () => {
  const executablePath = browserExecutable();
  if (!executablePath) throw new Error('No local Edge or Chrome executable found');
  const browser = await chromium.launch({ headless: true, executablePath });
  const results = [];
  try {
    for (const file of pages) {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/${file}`, { waitUntil: 'networkidle' });
      await loadLazyImages(page);
      const state = await page.evaluate(() => ({
        pageOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        images: [...document.images].map((image) => {
          const rect = image.getBoundingClientRect();
          const style = getComputedStyle(image);
          const widthScale = image.naturalWidth ? rect.width / image.naturalWidth : 0;
          const heightScale = image.naturalHeight ? rect.height / image.naturalHeight : 0;
          const nativeRatio = image.naturalHeight ? image.naturalWidth / image.naturalHeight : 0;
          const displayRatio = rect.height ? rect.width / rect.height : 0;
          const hasPadding = ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft']
            .some((property) => parseFloat(style[property]) > 0);
          return {
            src: new URL(image.currentSrc || image.src).pathname,
            className: image.closest('figure')?.className || image.className || '',
            natural: `${image.naturalWidth}x${image.naturalHeight}`,
            rendered: `${Math.round(rect.width)}x${Math.round(rect.height)}`,
            widthScale: Number(widthScale.toFixed(2)),
            heightScale: Number(heightScale.toFixed(2)),
            objectFit: style.objectFit,
            broken: image.complete && image.naturalWidth === 0,
            distorted: style.objectFit === 'fill' && !hasPadding
              && nativeRatio > 0
              && Math.abs(displayRatio / nativeRatio - 1) > 0.05
          };
        })
      }));
      const broken = state.images.filter((image) => image.broken);
      const distorted = state.images.filter((image) => image.distorted);
      const rasterCharts = state.images.filter((image) => /-chart-\d+\./i.test(image.src));
      const upscaled = state.images
        .filter((image) => Math.max(image.widthScale, image.heightScale) > 1.15)
        .sort((a, b) => Math.max(b.widthScale, b.heightScale) - Math.max(a.widthScale, a.heightScale));
      if (state.pageOverflow > 1 || broken.length || distorted.length || rasterCharts.length) {
        throw new Error(
          `${file}: overflow=${state.pageOverflow}, broken=${broken.length}, ` +
          `distorted=${JSON.stringify(distorted)}, rasterCharts=${rasterCharts.length}`
        );
      }
      results.push({
        file,
        imageCount: state.images.length,
        upscaled: upscaled.slice(0, 8)
      });
      await page.close();
    }
  } finally {
    await browser.close();
  }

  console.log(JSON.stringify({
    checked: results.length,
    totalImages: results.reduce((sum, item) => sum + item.imageCount, 0),
    pagesWithUpscaledImages: results.filter((item) => item.upscaled.length)
  }, null, 2));
})().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
