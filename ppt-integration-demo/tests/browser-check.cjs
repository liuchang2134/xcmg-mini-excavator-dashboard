const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright-core");

const base = process.argv[2] || "http://127.0.0.1:4173/ppt-integration-demo/";
const artifactDir = path.resolve(__dirname, "..", "artifacts");
fs.mkdirSync(artifactDir, { recursive: true });

const pages = [
  "index.html",
  "market-insights.html",
  "tonnage-insight.html?range=3-4t",
  "product-portfolio.html",
  "improvement-roadmap.html",
  "evidence-center.html",
];

async function assertNoOverflow(page, label) {
  const metrics = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
  }));
  if (metrics.scrollWidth > metrics.clientWidth + 1) {
    throw new Error(`${label} horizontal overflow ${metrics.scrollWidth}/${metrics.clientWidth}`);
  }
}

function browserExecutable() {
  const candidates = [
    process.env.XCMG_QA_BROWSER,
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  ].filter(Boolean);
  return candidates.find((candidate) => fs.existsSync(candidate));
}

async function assertRendered(page, label, language) {
  const state = await page.evaluate(() => ({
    lang: document.documentElement.lang,
    text: document.querySelector("main")?.innerText || "",
    brokenImages: [...document.images].filter((image) => image.complete && image.naturalWidth === 0).length,
    loadFailure: [...document.querySelectorAll(".warning-note")].some((node) =>
      /数据加载失败|Data failed to load/.test(node.textContent || ""),
    ),
  }));
  if (state.lang !== (language === "en" ? "en" : "zh-CN")) throw new Error(`${label} language is ${state.lang}`);
  if (state.text.trim().length < 200) throw new Error(`${label} did not render enough content`);
  if (state.brokenImages) throw new Error(`${label} has ${state.brokenImages} broken image(s)`);
  if (state.loadFailure) throw new Error(`${label} shows a data-load failure`);
  const internalKey = state.text.match(/\b[a-z]+(?:_[a-z]+)+\b/);
  if (internalKey) throw new Error(`${label} exposes internal key ${internalKey[0]}`);
}

(async () => {
  const executablePath = browserExecutable();
  if (!executablePath) throw new Error("Set XCMG_QA_BROWSER to a local Edge or Chrome executable");
  const browser = await chromium.launch({ headless: true, executablePath });
  const errors = [];
  try {
    for (const viewport of [
      { name: "desktop", width: 1440, height: 1000 },
      { name: "mobile", width: 390, height: 844 },
    ]) {
      for (const language of ["zh", "en"]) {
        for (const route of pages) {
          const page = await browser.newPage({ viewport, deviceScaleFactor: 1 });
          const label = `${route} ${viewport.name} ${language}`;
          page.on("console", (message) => {
            if (message.type() === "error") errors.push(`${label}: ${message.text()}`);
          });
          page.on("pageerror", (error) => errors.push(`${label}: ${error.message}`));
          const url = new URL(route, base);
          if (language === "en") url.searchParams.set("lang", "en");
          const response = await page.goto(url.href, { waitUntil: "networkidle" });
          if (!response || !response.ok()) throw new Error(`${label} returned ${response?.status()}`);
          await assertNoOverflow(page, label);
          await assertRendered(page, label, language);
          await page.close();
        }
      }
    }

    const desktop = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
    await desktop.goto(new URL("index.html", base).href, { waitUntil: "networkidle" });
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-home.png"), fullPage: false });
    const evidenceButton = desktop.locator("[data-home-findings] [data-evidence]").first();
    await evidenceButton.click();
    await desktop.locator(".evidence-drawer.open").waitFor();
    if (!(await desktop.locator(".drawer-image").isVisible())) throw new Error("Evidence drawer image is not visible");
    await desktop.locator("[data-drawer-close]").click();
    await desktop.close();

    const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
    await mobile.goto(new URL("tonnage-insight.html?range=3-4t", base).href, { waitUntil: "networkidle" });
    await assertNoOverflow(mobile, "tonnage mobile");
    if ((await mobile.locator(".mobile-scenario").count()) !== 8) throw new Error("Mobile scenario count is not 8");
    await mobile.screenshot({ path: path.join(artifactDir, "mobile-tonnage.png"), fullPage: false });
    await mobile.close();

    const english = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
    await english.goto(new URL("index.html?lang=en", base).href, { waitUntil: "networkidle" });
    if ((await english.locator("html").getAttribute("lang")) !== "en") throw new Error("English language switch failed");
    await assertNoOverflow(english, "home English mobile");
    await english.screenshot({ path: path.join(artifactDir, "mobile-home-en.png"), fullPage: false });
    await english.close();

    if (errors.length) throw new Error(`Browser console errors:\n${errors.join("\n")}`);
    console.log("Browser QA passed: six pages in both languages at desktop and 390px, evidence drawer and screenshots.");
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error.stack || error);
  process.exit(1);
});
