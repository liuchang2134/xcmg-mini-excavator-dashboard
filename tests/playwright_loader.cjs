const path = require('path');

function loadPlaywrightCore() {
  const candidates = [
    process.env.XCMG_PLAYWRIGHT_CORE,
    path.resolve(__dirname, '..', 'ppt-integration-demo', 'node_modules', 'playwright-core'),
    'playwright-core'
  ].filter(Boolean);

  let lastError;
  for (const candidate of candidates) {
    try {
      return require(candidate);
    } catch (error) {
      lastError = error;
    }
  }

  throw new Error(
    `Playwright Core is unavailable. Set XCMG_PLAYWRIGHT_CORE to its module directory. ${lastError?.message || ''}`
  );
}

module.exports = loadPlaywrightCore();
