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
  if (/查看依据|View evidence/.test(state.text)) throw new Error(`${label}: still exposes a secondary evidence action`);
  if (/模块资料|原始记录|Module research material|Original record/.test(state.text)) throw new Error(`${label}: exposes production or source-record wording`);
  if (language === "en" && /[\u3400-\u9fff]/.test(state.text)) throw new Error(`${label}: contains mixed Chinese/English body text`);
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
    if ((await desktop.locator("#page-nav a").count()) !== 17 || (await desktop.locator("[data-ppt-nav]").count()) !== 5 || (await desktop.locator(".navPptLink,.navCategoryLink").count()) !== 0) throw new Error("Integrated page must expose the five integrated analysis sections as first-level navigation");
    if ((await desktop.locator(".conditionBlock").count()) !== 6) throw new Error("Formal six-condition content changed");
    if ((await desktop.locator(".scenarioBand").count()) !== 8) throw new Error("Expected eight directly displayed job applications");
    if ((await desktop.locator(".comparisonMatrix tbody tr").count()) < 9) throw new Error("Paper comparison is incomplete");
    if ((await desktop.locator(".fieldMatrix tbody tr").count()) !== 11) throw new Error("Field evaluation is incomplete");
    if ((await desktop.locator(".roadmapRow").count()) !== 8) throw new Error("Roadmap is incomplete");
    if ((await desktop.locator(".evidenceTrigger,.evidenceDrawer,.evidenceButtons,.inlineEvidenceCard").count()) !== 0) throw new Error("Source-presentation controls or cards remain in the reading flow");
    if ((await desktop.locator(".pptSection details").count()) !== 0) throw new Error("Integrated modules must display their analysis directly without secondary disclosure menus");
    if ((await desktop.locator('main img[src*="assets/slides/slide-"]').count()) !== 0) throw new Error("Full-slide images must not appear in the web narrative");
    if ((await desktop.locator("#ppt-market .marketNarrative article").count()) !== 3) throw new Error("Market interpretation is incomplete");
    if ((await desktop.locator("#ppt-market .brandStackRow").count()) !== 4 || (await desktop.locator("#ppt-market .brandSalesVisual tbody tr").count()) !== 4) throw new Error("Brand-volume chart or table is incomplete");
    if ((await desktop.locator("#ppt-market .volumeColumn.historical").count()) !== 2 || (await desktop.locator("#ppt-market .volumeColumn.estimate").count()) !== 1 || (await desktop.locator("#ppt-market .volumeColumn.forecast").count()) !== 1) throw new Error("Market-volume data statuses are not explicit");
    if ((await desktop.locator("#ppt-market .modelDemandRow").count()) !== 10) throw new Error("Leading-model ranking is incomplete");
    if ((await desktop.locator("#ppt-market .scatterPoint").count()) !== 6) throw new Error("Historical price-share chart is incomplete");
    if ((await desktop.locator("#ppt-market .massPackageRow").count()) !== 2) throw new Error("Transport mass build-up is incomplete");
    if ((await desktop.locator("#ppt-market .transportPhotoPair img").count()) !== 2) throw new Error("Transport field photography is incomplete");
    if ((await desktop.locator("#ppt-market .transportBoundaryFacts>div").count()) !== 3) throw new Error("Transport payload boundary is incomplete");
    const transportPhotoHeights = await desktop.locator("#ppt-market .transportPhotoPair img").evaluateAll((images) => images.map((image) => ({rendered: image.getBoundingClientRect().height, natural: image.naturalHeight})));
    if (transportPhotoHeights.some((image) => image.rendered < 200 || image.natural < 400)) throw new Error("Transport photography is too small or failed to load");
    if ((await desktop.locator("#ppt-paper .performanceFacet").count()) !== 8) throw new Error("Core performance small multiples are incomplete");
    if ((await desktop.locator("#ppt-paper .paperInsightGrid article").count()) !== 4) throw new Error("Specification conclusions are incomplete");
    if ((await desktop.locator("#ppt-paper .dataConflictBlock tbody tr").count()) !== 4) throw new Error("Current-versus-historical data reconciliation is incomplete");
    if ((await desktop.locator("#ppt-field .fieldThemeGrid article").count()) !== 5) throw new Error("Field-evaluation themes are incomplete");
    if ((await desktop.locator("#ppt-field .radarSeries").count()) !== 3) throw new Error("Historical competitiveness profile is incomplete");
    if ((await desktop.locator("#ppt-field .ratingHeatmap tbody tr").count()) !== 18) throw new Error("Historical field-evaluation heatmap is incomplete");
    if ((await desktop.locator("#ppt-actions .actionPhaseGrid article").count()) !== 3) throw new Error("Improvement phases are incomplete");
    if ((await desktop.locator("#ppt-actions .improvementLedger tbody tr").count()) !== 13) throw new Error("Historical improvement ledger is incomplete");
    if ((await desktop.locator(".sourceBadge").count()) < 25) throw new Error("Source-page references are incomplete");
    const scenarioImages = desktop.locator(".scenarioBand .scenarioPhotoGrid img");
    if ((await scenarioImages.count()) !== 24 || (await desktop.locator(".scenarioBand .scenarioPhotoGrid figcaption").count()) !== 24) throw new Error("All 24 unique field photos must be displayed with captions");
    for (let index = 0; index < 24; index += 1) await scenarioImages.nth(index).scrollIntoViewIfNeeded();
    await desktop.waitForFunction(() => [...document.querySelectorAll(".scenarioBand .scenarioPhotoGrid img")].every((image) => image.complete && image.naturalWidth > 0));
    const imageAudit = await scenarioImages.evaluateAll((images) => ({
      unique: new Set(images.map((image) => image.getAttribute("src"))).size,
      loaded: images.every((image) => image.complete && image.naturalWidth > 0 && image.naturalHeight > 0),
      sized: images.every((image) => { const rect = image.getBoundingClientRect(); return rect.width > 0 && rect.height > 0; }),
      uncropped: images.every((image) => getComputedStyle(image).objectFit === "contain"),
    }));
    if (imageAudit.unique !== 24 || !imageAudit.loaded || !imageAudit.sized || !imageAudit.uncropped) throw new Error(`Scenario image audit failed: ${JSON.stringify(imageAudit)}`);
    if ((await desktop.locator(".scenarioBand .scenarioEngineering article").count()) !== 24) throw new Error("Every application must include parameter, equipment and action analysis");
    if ((await desktop.locator(".scenarioBand .scenarioSourceContext").count()) !== 8 || (await desktop.locator(".scenarioBand .scenarioSourceContext section").count()) !== 24) throw new Error("PPT-derived application context is incomplete");
    if ((await desktop.locator(".scenarioFacts ul,.scenarioFacts ol,.scenarioSourceContext ul,.scenarioSourceContext ol").count()) !== 0) throw new Error("Scenario prose has regressed into fragmented lists");
    const proseAudit = await desktop.locator(".scenarioBand .scenarioNarrative").evaluateAll((nodes) => ({
      count: nodes.length,
      historicalItems: nodes.filter((node) => node.classList.contains("historicalNarrative")).reduce((sum, node) => sum + Number(node.dataset.itemCount || 0), 0),
      shortBlocks: nodes.filter((node) => (node.textContent || '').trim().length < 28).length,
    }));
    if (proseAudit.count !== 40 || proseAudit.historicalItems !== 42 || proseAudit.shortBlocks !== 0) throw new Error(`Scenario prose audit failed: ${JSON.stringify(proseAudit)}`);
    if ((await desktop.locator(".scenarioBand .scenarioAssessment tbody tr").count()) !== 32) throw new Error("Every application must include direct requirement-to-action analysis");
    if ((await desktop.locator(".scenarioConditionLinks a").count()) < 16) throw new Error("Applications are not linked to the existing quantified conditions");
    if ((await desktop.locator("#ppt-paper .sourceDataGroup").count()) !== 3 || (await desktop.locator("#ppt-paper .sourceDataGroup tbody tr").count()) !== 38) throw new Error("Complete specification and equipment tables are missing");
    if ((await desktop.locator("#ppt-field .sourceDataGroup").count()) !== 5 || (await desktop.locator("#ppt-field .sourceDataGroup tbody tr").count()) !== 68) throw new Error("Complete historical field-evaluation tables are missing");
    if ((await desktop.locator(".competitionGapMatrix tbody tr").count()) !== 9 || (await desktop.locator(".positioningScroll tbody tr").count()) !== 6) throw new Error("Concrete competitive-gap or positioning analysis is incomplete");
    await desktop.locator("#ppt-market").scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-integrated-3-4t.png"), fullPage: false });
    await desktop.locator(".brandSalesVisual").scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-source-market.png"), fullPage: false });
    await desktop.locator(".transportStory").scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-source-transport.png"), fullPage: false });
    await desktop.locator(".performanceEvidence").scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-source-performance.png"), fullPage: false });
    await desktop.locator(".fieldHeatmapVisual").scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-source-field.png"), fullPage: false });
    await desktop.locator(".improvementLedger").scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-source-ledger.png"), fullPage: false });
    await desktop.locator(".scenarioBandHeader").first().scrollIntoViewIfNeeded();
    await desktop.waitForTimeout(500);
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-integrated-scenarios.png"), fullPage: false });
    await desktop.locator(".scenarioSourceContext").first().scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-scenario-detail.png"), fullPage: false });
    await desktop.close();

    const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
    await mobile.goto(new URL("index.html", base).href, { waitUntil: "networkidle" });
    await mobile.locator(".scenarioBandHeader").first().scrollIntoViewIfNeeded();
    await mobile.waitForFunction(() => [...document.querySelectorAll(".scenarioBand:first-of-type img")].every((image) => image.complete && image.naturalWidth > 0));
    await mobile.waitForTimeout(500);
    await mobile.screenshot({ path: path.join(artifactDir, "mobile-integrated-3-4t.png"), fullPage: false });
    await mobile.locator(".scenarioSourceContext").first().scrollIntoViewIfNeeded();
    await mobile.waitForTimeout(300);
    await mobile.screenshot({ path: path.join(artifactDir, "mobile-scenario-detail.png"), fullPage: false });
    await mobile.locator(".transportStory").scrollIntoViewIfNeeded();
    await mobile.waitForFunction(() => [...document.querySelectorAll(".transportPhotoPair img")].every((image) => image.complete && image.naturalWidth > 0));
    await mobile.screenshot({ path: path.join(artifactDir, "mobile-source-transport.png"), fullPage: false });
    await mobile.close();

    const overview = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
    await overview.goto(new URL("excavator-overview.html", base).href, { waitUntil: "networkidle" });
    await overview.waitForTimeout(400);
    if ((await overview.locator("#page-nav a").count()) !== 1) throw new Error("Overview sidebar must contain only one return link");
    if ((await overview.locator(".hero").count()) !== 1 || (await overview.locator(".categoryHero").count()) !== 0) throw new Error("Overview must reuse the formal dashboard hero");
    if ((await overview.locator(".evidenceTrigger,.evidenceDrawer,.evidenceButtons,.inlineEvidenceCard").count()) !== 0) throw new Error("Overview still contains source-presentation controls or cards");
    if ((await overview.locator('main img[src*="assets/slides/slide-"]').count()) !== 0) throw new Error("Overview must not display full-slide images");
    if ((await overview.locator(".cycleBar").count()) !== 5) throw new Error("Market-cycle chart is incomplete");
    if ((await overview.locator(".overviewDecisionRow").count()) !== 8) throw new Error("Decision analysis is incomplete");
    if ((await overview.locator(".benchmarkBand").count()) !== 2) throw new Error("Benchmark systems are incomplete");
    if ((await overview.locator(".tonnagePriorityGrid article").count()) !== 4) throw new Error("Tonnage priorities are incomplete");
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
