const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright-core");

const base = process.argv[2] || "http://127.0.0.1:4174/ppt-integration-demo/";
const artifactDir = path.resolve(__dirname, "..", "artifacts");
fs.mkdirSync(artifactDir, { recursive: true });

const routes = ["index.html", "excavator-overview.html"];

function browserExecutable() {
  return [
    process.env.XCMG_QA_BROWSER,
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  ].filter(Boolean).find((candidate) => fs.existsSync(candidate));
}

async function assertPage(page, label, language, route) {
  const state = await page.evaluate(() => ({
    lang: document.documentElement.lang,
    text: document.querySelector("main")?.innerText || "",
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
    brokenImages: [...document.images].filter((image) => image.complete && image.naturalWidth === 0).map((image) => image.src),
  }));
  if (state.lang !== (language === "en" ? "en-US" : "zh-CN")) throw new Error(`${label}: lang=${state.lang}`);
  if (state.text.trim().length < 1500) throw new Error(`${label}: insufficient content`);
  if (state.scrollWidth > state.clientWidth + 1) throw new Error(`${label}: horizontal overflow ${state.scrollWidth}/${state.clientWidth}`);
  if (state.brokenImages.length) throw new Error(`${label}: broken images ${state.brokenImages.join(", ")}`);
  if (/source_mapped_|requires_current_|historical_internal_/.test(state.text)) throw new Error(`${label}: exposes internal data key`);
  if (/\bPPT\b/i.test(state.text)) throw new Error(`${label}: exposes source-presentation language in the main reading flow`);
  if (language === "en" && route === "excavator-overview.html" && /[\u3400-\u9fff]/.test(state.text)) throw new Error(`${label}: contains mixed Chinese/English body text`);
}

(async () => {
  const executablePath = browserExecutable();
  if (!executablePath) throw new Error("Set XCMG_QA_BROWSER to a local Edge or Chrome executable");
  const browser = await chromium.launch({ headless: true, executablePath });
  const consoleErrors = [];
  try {
    for (const viewport of [
      { name: "desktop", width: 1440, height: 1000 },
      { name: "mobile", width: 390, height: 844 },
    ]) {
      for (const language of ["zh", "en"]) {
        for (const route of routes) {
          const page = await browser.newPage({ viewport, deviceScaleFactor: 1 });
          const label = `${route} ${viewport.name} ${language}`;
          page.on("console", (message) => { if (message.type() === "error") consoleErrors.push(`${label}: ${message.text()}`); });
          page.on("pageerror", (error) => consoleErrors.push(`${label}: ${error.message}`));
          const url = new URL(route, base);
          if (language === "en") url.searchParams.set("lang", "en");
          const response = await page.goto(url.href, { waitUntil: "networkidle" });
          if (!response?.ok()) throw new Error(`${label}: status=${response?.status()}`);
          await assertPage(page, label, language, route);
          await page.close();
        }
      }
    }

    const desktop = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
    await desktop.goto(new URL("index.html", base).href, { waitUntil: "networkidle" });
    if ((await desktop.locator("#page-nav a").count()) !== 12 || (await desktop.locator(".navPptLink,.navCategoryLink").count()) !== 0) throw new Error("Integrated page must retain the formal sidebar navigation only");
    if ((await desktop.locator(".conditionBlock").count()) !== 6) throw new Error("Formal six-condition content changed");
    if ((await desktop.locator(".scenarioTabs button").count()) !== 8) throw new Error("Expected eight PPT application tabs");
    if ((await desktop.locator(".comparisonMatrix tbody tr").count()) < 9) throw new Error("Paper comparison is incomplete");
    if ((await desktop.locator(".fieldMatrix tbody tr").count()) !== 11) throw new Error("Field evaluation is incomplete");
    if ((await desktop.locator(".roadmapRow").count()) !== 8) throw new Error("Roadmap is incomplete");
    const firstTitle = await desktop.locator(".scenarioStage h3").innerText();
    await desktop.locator(".scenarioTabs button").nth(7).click();
    const lastTitle = await desktop.locator(".scenarioStage h3").innerText();
    if (firstTitle === lastTitle) throw new Error("Scenario tabs do not update the workspace");
    await desktop.locator("#ppt-market .evidenceTrigger").first().click();
    await desktop.locator(".evidenceDrawer.open").waitFor();
    if (!(await desktop.locator(".evidenceSlideImage").isVisible())) throw new Error("Evidence image is not visible");
    await desktop.locator(".drawerClose").click();
    await desktop.waitForTimeout(300);
    await desktop.locator("#ppt-market").scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-integrated-3-4t.png"), fullPage: false });
    await desktop.close();

    const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
    await mobile.goto(new URL("index.html", base).href, { waitUntil: "networkidle" });
    await mobile.locator("#ppt-scenarios").scrollIntoViewIfNeeded();
    await mobile.screenshot({ path: path.join(artifactDir, "mobile-integrated-3-4t.png"), fullPage: false });
    await mobile.close();

    const overview = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
    await overview.goto(new URL("excavator-overview.html", base).href, { waitUntil: "networkidle" });
    await overview.waitForTimeout(400);
    if ((await overview.locator("#page-nav a").count()) !== 1) throw new Error("Overview sidebar must contain only one return link");
    if ((await overview.locator(".hero").count()) !== 1 || (await overview.locator(".categoryHero").count()) !== 0) throw new Error("Overview must reuse the formal dashboard hero");
    if ((await overview.locator('main img[src*="assets/slides/slide-"]').count()) !== 0) throw new Error("Overview main flow must use native web visuals rather than slide screenshots");
    await overview.screenshot({ path: path.join(artifactDir, "desktop-excavator-overview.png"), fullPage: false });
    await overview.setViewportSize({ width: 390, height: 844 });
    await overview.waitForTimeout(200);
    await overview.screenshot({ path: path.join(artifactDir, "mobile-excavator-overview.png"), fullPage: false });
    await overview.close();

    const zoomedOverview = await browser.newPage({ viewport: { width: 1000, height: 800 }, deviceScaleFactor: 1 });
    await zoomedOverview.goto(new URL("excavator-overview.html", base).href, { waitUntil: "networkidle" });
    const zoomedLayout = await zoomedOverview.evaluate(() => {
      const sidebar = document.querySelector("aside.nav");
      const menu = document.querySelector("#page-nav");
      return {
        layout: getComputedStyle(document.querySelector(".layout")).display,
        sidebarPosition: getComputedStyle(sidebar).position,
        sidebarWidth: sidebar.getBoundingClientRect().width,
        menuDisplay: getComputedStyle(menu).display,
        overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      };
    });
    if (zoomedLayout.layout !== "grid" || zoomedLayout.sidebarPosition !== "sticky" || zoomedLayout.sidebarWidth < 200 || zoomedLayout.menuDisplay === "none") throw new Error(`Zoomed overview lost its sidebar: ${JSON.stringify(zoomedLayout)}`);
    if (zoomedLayout.overflow) throw new Error("Zoomed overview has horizontal overflow");
    await zoomedOverview.close();

    if (consoleErrors.length) throw new Error(`Browser console errors:\n${consoleErrors.join("\n")}`);
    console.log("Browser QA passed: integrated 3-4 t and excavator overview in both languages at desktop and 390px.");
  } finally {
    await browser.close();
  }
})().catch((error) => { console.error(error.stack || error); process.exit(1); });
