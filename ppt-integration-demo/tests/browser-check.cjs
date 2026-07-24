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
    narrowEnglishCells: [...document.querySelectorAll("main table th, main table td")].map((cell) => {
      const rect = cell.getBoundingClientRect();
      return {
        text: (cell.textContent || "").trim().replace(/\s+/g, " ").slice(0, 80),
        width: Math.round(rect.width),
        height: Math.round(rect.height),
      };
    }).filter((cell) => /[A-Za-z]{4}/.test(cell.text) && cell.text.length >= 9 && cell.width < 48 && cell.height > 52).slice(0, 12),
    gapMatrix: (() => {
      const table = document.querySelector(".competitionGapMatrix table");
      const firstHeader = table?.querySelector("thead th:first-child");
      const rows = table ? [...table.querySelectorAll("tbody tr")] : [];
      return table && firstHeader ? {
        firstColumnWidth: Math.round(firstHeader.getBoundingClientRect().width),
        tableHeight: Math.round(table.getBoundingClientRect().height),
        tallestRow: Math.round(Math.max(0, ...rows.map((row) => row.getBoundingClientRect().height))),
      } : null;
    })(),
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
  if (language === "en" && state.narrowEnglishCells.length) throw new Error(`${label}: English table labels collapsed vertically ${JSON.stringify(state.narrowEnglishCells)}`);
  if (route === "index.html" && (!state.gapMatrix || state.gapMatrix.firstColumnWidth < (language === "en" ? 150 : 110) || state.gapMatrix.tallestRow > 180 || state.gapMatrix.tableHeight > 1200)) throw new Error(`${label}: improvement-path matrix is unreadable ${JSON.stringify(state.gapMatrix)}`);
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

    const retryProbe = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
    let expansionRequests = 0;
    await retryProbe.route("**/visual-expansion-3-4t.json*", async (route) => {
      expansionRequests += 1;
      if (expansionRequests === 1) await route.abort("failed"); else await route.continue();
    });
    await retryProbe.goto(new URL("index.html", base).href, { waitUntil: "networkidle" });
    if (expansionRequests < 2 || (await retryProbe.locator(".taskCapabilityVisual").count()) !== 1 || (await retryProbe.locator("#ppt-load-error").count()) !== 0) {
      throw new Error(`Transient data retry failed: requests=${expansionRequests}`);
    }
    await retryProbe.close();

    const degradedProbe = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
    await degradedProbe.route("**/visual-expansion-3-4t.json*", (route) => route.abort("failed"));
    await degradedProbe.goto(new URL("index.html", base).href, { waitUntil: "networkidle" });
    if ((await degradedProbe.locator(".marketDecisionGrid").count()) !== 1 || (await degradedProbe.locator("#ppt-load-error").count()) !== 0) {
      throw new Error("Optional visual data failure removed the core market analysis");
    }
    await degradedProbe.close();

    const desktop = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
    const canonicalProbe = new URL("index.html", base);
    canonicalProbe.searchParams.set("rev", "legacy-preview-link");
    canonicalProbe.hash = "ppt-scenarios";
    await desktop.goto(canonicalProbe.href, { waitUntil: "networkidle" });
    const canonicalState = new URL(desktop.url());
    if (canonicalState.searchParams.has("rev") || canonicalState.hash) throw new Error(`Demo URL was not canonicalized: ${desktop.url()}`);
    if ((await desktop.locator("#page-nav a").count()) !== 18 || (await desktop.locator("[data-ppt-nav]").count()) !== 6 || (await desktop.locator(".navPptLink,.navCategoryLink").count()) !== 0) throw new Error("Integrated page must expose the six integrated analysis sections as first-level navigation");
    if ((await desktop.locator("#page-nav .navGroup").count()) !== 1 || (await desktop.locator("#page-nav .navGroup .navSubmenu a").count()) !== 6 || !(await desktop.locator("#page-nav .navGroup").evaluate((group) => group.open))) throw new Error("The six work conditions must be grouped in one expanded submenu");
    await desktop.waitForFunction(() => document.body.dataset.navReady === "true" && document.querySelectorAll("#page-nav a.is-active").length === 1);
    const stableAddress = new URL(desktop.url()).pathname + new URL(desktop.url()).search;
    await desktop.locator('#page-nav a[href="#ppt-market"]').click();
    await desktop.waitForFunction(() => document.querySelector('#page-nav a[href="#ppt-market"]')?.getAttribute("aria-current") === "location");
    await desktop.waitForFunction(() => Math.abs(document.querySelector("#ppt-market").getBoundingClientRect().top - 16) < 60);
    const marketNavigation = await desktop.evaluate(() => ({
      active: document.querySelector("#page-nav a.is-active")?.getAttribute("href"),
      activeCount: document.querySelectorAll("#page-nav a.is-active").length,
      currentTitle: document.querySelector(".navLocationTitle")?.textContent.trim(),
      progress: Number(document.querySelector(".navProgressTrack")?.getAttribute("aria-valuenow")),
      hash: window.location.hash,
    }));
    if (marketNavigation.active !== "#ppt-market" || marketNavigation.activeCount !== 1 || marketNavigation.currentTitle !== "市场与客户" || marketNavigation.progress <= 0 || marketNavigation.hash) throw new Error(`Market navigation state is inconsistent: ${JSON.stringify(marketNavigation)}`);
    if (new URL(desktop.url()).pathname + new URL(desktop.url()).search !== stableAddress) throw new Error(`Sidebar navigation changed the stable demo address: ${desktop.url()}`);
    await desktop.locator("#cond4").evaluate((target) => target.scrollIntoView({block: "start"}));
    await desktop.waitForFunction(() => document.querySelector('#page-nav a[href="#cond4"]')?.getAttribute("aria-current") === "location");
    const conditionNavigation = await desktop.evaluate(() => ({
      active: document.querySelector("#page-nav a.is-active")?.getAttribute("href"),
      activeCount: document.querySelectorAll("#page-nav a.is-active").length,
      currentTitle: document.querySelector(".navLocationTitle")?.textContent.trim(),
    }));
    if (conditionNavigation.active !== "#cond4" || conditionNavigation.activeCount !== 1 || !conditionNavigation.currentTitle.includes("破碎")) throw new Error(`Scroll tracking did not follow the condition section: ${JSON.stringify(conditionNavigation)}`);
    if (!(await desktop.locator("#page-nav .navGroup").evaluate((group) => group.open && group.classList.contains("is-current")))) throw new Error("The work-condition submenu did not expose the active condition");
    await desktop.locator("#page-nav .navGroup > summary").click();
    if (await desktop.locator("#page-nav .navGroup").evaluate((group) => group.open)) throw new Error("The work-condition submenu could not be collapsed");
    await desktop.locator("#page-nav .navGroup > summary").click();
    if (!(await desktop.locator("#page-nav .navGroup").evaluate((group) => group.open))) throw new Error("The work-condition submenu could not be expanded");
    if ((await desktop.locator(".conditionBlock").count()) !== 6) throw new Error("Formal six-condition content changed");
    if ((await desktop.locator(".scenarioBand").count()) !== 8) throw new Error("Expected eight directly displayed job applications");
    if ((await desktop.locator(".comparisonMatrix tbody tr").count()) < 9) throw new Error("Paper comparison is incomplete");
    if ((await desktop.locator(".fieldMatrix tbody tr").count()) !== 11) throw new Error("Field evaluation is incomplete");
    if ((await desktop.locator(".roadmapRow").count()) !== 8) throw new Error("Roadmap is incomplete");
    const coverageAudit = await desktop.locator(".pptSection[data-source-slides]").evaluateAll((sections) => {
      const slides = sections.flatMap((section) => (section.dataset.sourceSlides || "").split(/\s+/).filter(Boolean).map(Number));
      return {
        sectionCount: sections.length,
        slides: [...new Set(slides)].sort((a, b) => a - b),
        bodySlides: (document.body.dataset.coveredSlides || "").split(/\s+/).filter(Boolean).map(Number),
      };
    });
    const expectedCoverage = Array.from({length: 21}, (_, index) => index + 48);
    if (coverageAudit.sectionCount !== 6 || JSON.stringify(coverageAudit.slides) !== JSON.stringify(expectedCoverage) || JSON.stringify(coverageAudit.bodySlides) !== JSON.stringify(expectedCoverage)) throw new Error(`Slides 48-68 are not fully mapped: ${JSON.stringify(coverageAudit)}`);
    if ((await desktop.locator(".evidenceTrigger,.evidenceDrawer,.evidenceButtons,.inlineEvidenceCard").count()) !== 0) throw new Error("Source-presentation controls or cards remain in the reading flow");
    if ((await desktop.locator(".pptSection details").count()) !== 0) throw new Error("Integrated modules must display their analysis directly without secondary disclosure menus");
    if ((await desktop.locator('main img[src*="assets/slides/slide-"]').count()) !== 0) throw new Error("Full-slide images must not appear in the web narrative");
    if ((await desktop.locator("#ppt-market .marketNarrative article").count()) !== 3) throw new Error("Market interpretation is incomplete");
    if ((await desktop.locator("#ppt-market .categoryContextVisual .classFocusBanner").count()) !== 1 || (await desktop.locator("#ppt-market .categoryContextVisual .classDecisionCard").count()) !== 4 || (await desktop.locator("#ppt-market .categoryContextVisual .benchmarkRole").count()) !== 2) throw new Error("3-4 t customer and product logic is incomplete");
    const categoryContextText = await desktop.locator("#ppt-market .categoryContextVisual").innerText();
    if (/1-3\s*t|4-6\s*t|1-3吨|4-6吨/.test(categoryContextText)) throw new Error("3-4 t context still discusses other tonnage classes");
    if ((await desktop.locator("#ppt-market .portfolioCoverageVisual,#ppt-market .priceShareVisual,#ppt-market .positioningScroll").count()) !== 0) throw new Error("Product-positioning content still duplicates the market section");
    if ((await desktop.locator("#ppt-market .brandStackRow").count()) !== 4 || (await desktop.locator("#ppt-market .brandSalesVisual tbody tr").count()) !== 4) throw new Error("Brand-volume chart or table is incomplete");
    if ((await desktop.locator("#ppt-market .volumeColumn.historical").count()) !== 2 || (await desktop.locator("#ppt-market .volumeColumn.estimate").count()) !== 1 || (await desktop.locator("#ppt-market .volumeColumn.forecast").count()) !== 1) throw new Error("Market-volume data statuses are not explicit");
    if ((await desktop.locator("#ppt-market .modelDemandRow").count()) !== 10) throw new Error("Leading-model ranking is incomplete");
    if ((await desktop.locator("#ppt-market .massPackageRow").count()) !== 2) throw new Error("Transport mass build-up is incomplete");
    if ((await desktop.locator("#ppt-market .transportPhotoPair img").count()) !== 2) throw new Error("Transport field photography is incomplete");
    if ((await desktop.locator("#ppt-market .transportBoundaryFacts>div").count()) !== 3) throw new Error("Transport payload boundary is incomplete");
    const transportPhotoHeights = await desktop.locator("#ppt-market .transportPhotoPair img").evaluateAll((images) => images.map((image) => ({rendered: image.getBoundingClientRect().height, natural: image.naturalHeight})));
    if (transportPhotoHeights.some((image) => image.rendered < 200 || image.natural < 400)) throw new Error("Transport photography is too small or failed to load");
    if ((await desktop.locator("#ppt-paper .performanceFacet").count()) !== 8) throw new Error("Core performance small multiples are incomplete");
    if ((await desktop.locator("#ppt-paper .absoluteGapVisual .gapMetricRow").count()) !== 8 || (await desktop.locator("#ppt-paper .absoluteGapVisual .status-advantage").count()) !== 1) throw new Error("Absolute specification-gap chart is incomplete");
    const absoluteGapText = await desktop.locator("#ppt-paper .absoluteGapVisual").innerText();
    if (!absoluteGapText.includes("28.6 kN") || !absoluteGapText.includes("3.6 km/h") || !absoluteGapText.includes("-7.6 kN")) throw new Error("Absolute specification values lost source precision");
    if ((await desktop.locator("#ppt-paper .paperInsightGrid article").count()) !== 4) throw new Error("Specification conclusions are incomplete");
    if ((await desktop.locator("#ppt-paper .dataConflictBlock").count()) !== 0) throw new Error("Source-reconciliation content must not appear in the product narrative");
    if ((await desktop.locator("#ppt-field .fieldThemeGrid article").count()) !== 5) throw new Error("Field-evaluation themes are incomplete");
    if ((await desktop.locator("#ppt-field .fieldEvidenceVisual tbody tr").count()) !== 8 || (await desktop.locator("#ppt-field .fieldEvidenceVisual .evidenceLevel").count()) < 36) throw new Error("Field-evidence maturity matrix is incomplete");
    if ((await desktop.locator("#ppt-field .fieldScoringMethod").count()) !== 1 || !(await desktop.locator("#ppt-field .fieldScoringMethod").innerText()).includes("等权平均") || !(await desktop.locator("#ppt-field .fieldScoringMethod").innerText()).includes("不并入参数分")) throw new Error("Field-evaluation scoring method is missing or incomplete");
    if ((await desktop.locator("#ppt-field .ratingHeatmap tbody tr").count()) !== 18) throw new Error("Historical field-evaluation heatmap is incomplete");
    if ((await desktop.locator("#ppt-positioning .positionMetricStrip article").count()) !== 5) throw new Error("Product-positioning facts are incomplete");
    if ((await desktop.locator("#ppt-positioning .scatterPoint").count()) !== 6) throw new Error("Historical price-share chart is incomplete");
    if ((await desktop.locator("#ppt-positioning .portfolioCoverageVisual tbody tr").count()) !== 6 || (await desktop.locator("#ppt-positioning .portfolioCoverageVisual .portfolioMissing").count()) < 3) throw new Error("Portfolio coverage matrix is incomplete");
    if ((await desktop.locator("#ppt-positioning .marketPortfolioMatrix tbody tr").count()) < 5 || (await desktop.locator("#ppt-positioning .positioningScroll tbody tr").count()) !== 6) throw new Error("Portfolio strategy or historical positioning detail is incomplete");
    if ((await desktop.locator("#ppt-positioning .radarSeries").count()) !== 3) throw new Error("Historical competitiveness profile is incomplete");
    const positioningText = await desktop.locator("#ppt-positioning").innerText();
    if (!positioningText.includes("194 台") || !positioningText.includes("约低 10%") || !positioningText.includes("历史销售目标") || !positioningText.includes("不与当前 Excel 综合评分合并")) throw new Error("Product-positioning boundaries or historical target are incomplete");
    if ((await desktop.locator("#ppt-actions .actionPhaseGrid article").count()) !== 3) throw new Error("Improvement phases are incomplete");
    if ((await desktop.locator("#ppt-actions .actionMethod").count()) !== 1 || !(await desktop.locator("#ppt-actions .actionMethod").innerText()).includes("不设置总分")) throw new Error("Improvement-path assessment method is missing");
    if ((await desktop.locator("#ppt-actions .improvementLedger tbody tr").count()) !== 13) throw new Error("Historical improvement ledger is incomplete");
    if ((await desktop.locator("#ppt-actions .closureTimelineVisual .closureRow").count()) !== 13) throw new Error("Improvement closure timeline is incomplete");
    if ((await desktop.locator(".sourceBadge").count()) !== 0) throw new Error("Source-page references must not appear in the product narrative");
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
    if ((await desktop.locator("#ppt-scenarios .taskCapabilityVisual .capabilityTab").count()) !== 8 || (await desktop.locator("#ppt-scenarios .taskCapabilityVisual .capabilityPanel").count()) !== 8) throw new Error("Customer-task capability explorer is incomplete");
    if ((await desktop.locator("#ppt-scenarios .taskCapabilityVisual .capabilityTabs").innerText()).includes("scenario-")) throw new Error("Customer-task explorer exposes internal scenario identifiers");
    if ((await desktop.locator("#ppt-scenarios .attachmentMatrixVisual tbody tr").count()) !== 8 || (await desktop.locator("#ppt-scenarios .attachmentMatrixVisual tbody td").count()) !== 80) throw new Error("Application-attachment heatmap is incomplete");
    await desktop.locator("#ppt-scenarios .capabilityTab").nth(1).click();
    if ((await desktop.locator("#ppt-scenarios .capabilityTab.is-active").count()) !== 1 || (await desktop.locator("#ppt-scenarios .capabilityPanel.is-active:not([hidden])").count()) !== 1 || (await desktop.locator("#ppt-scenarios .capabilityTab").nth(1).getAttribute("aria-pressed")) !== "true") throw new Error("Customer-task capability explorer interaction failed");
    const judgmentAudit = await desktop.locator(".scenarioAssessment .assessmentJudgment").evaluateAll((nodes) => ({
      count: nodes.length,
      vagueOnly: nodes.filter((node) => !node.querySelector("p") || (node.querySelector("p").textContent || "").trim().length < 16).length,
      standaloneLabels: nodes.filter((node) => (node.textContent || "").trim() === (node.querySelector(".scenarioStatus")?.textContent || "").trim()).length,
    }));
    if (judgmentAudit.count !== 32 || judgmentAudit.vagueOnly !== 0 || judgmentAudit.standaloneLabels !== 0) throw new Error(`Scenario engineering judgments are not explicit: ${JSON.stringify(judgmentAudit)}`);
    if ((await desktop.locator(".scenarioConditionLinks a").count()) < 16) throw new Error("Applications are not linked to the existing quantified conditions");
    if ((await desktop.locator("#ppt-paper .sourceDataGroup").count()) !== 3 || (await desktop.locator("#ppt-paper .sourceDataGroup tbody tr").count()) !== 38) throw new Error("Complete specification and equipment tables are missing");
    if ((await desktop.locator("#ppt-field .sourceDataGroup").count()) !== 5 || (await desktop.locator("#ppt-field .sourceDataGroup tbody tr").count()) !== 68) throw new Error("Complete historical field-evaluation tables are missing");
    if ((await desktop.locator(".competitionGapMatrix tbody tr").count()) !== 9) throw new Error("Concrete competitive-gap analysis is incomplete");
    await desktop.locator("#ppt-market").scrollIntoViewIfNeeded();
    await desktop.waitForTimeout(250);
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-integrated-3-4t.png"), fullPage: false });
    await desktop.locator(".categoryContextVisual").scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-class-choice.png"), fullPage: false });
    await desktop.locator(".brandSalesVisual").scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-source-market.png"), fullPage: false });
    await desktop.locator("#ppt-positioning .portfolioCoverageVisual").scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-portfolio-coverage.png"), fullPage: false });
    await desktop.locator("#ppt-positioning .positionDecision").scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-positioning.png"), fullPage: false });
    await desktop.locator(".transportStory").scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-source-transport.png"), fullPage: false });
    await desktop.locator(".performanceEvidence").scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-source-performance.png"), fullPage: false });
    await desktop.locator(".absoluteGapVisual").scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-absolute-gaps.png"), fullPage: false });
    await desktop.locator(".taskCapabilityVisual").scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-task-capability.png"), fullPage: false });
    await desktop.locator(".attachmentMatrixVisual").scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-attachment-heatmap.png"), fullPage: false });
    await desktop.locator(".fieldHeatmapVisual").scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-source-field.png"), fullPage: false });
    await desktop.locator(".fieldEvidenceVisual").scrollIntoViewIfNeeded();
    await desktop.screenshot({ path: path.join(artifactDir, "desktop-field-evidence.png"), fullPage: false });
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
    await mobile.waitForFunction(() => document.body.dataset.navReady === "true");
    await mobile.locator(".navToggle").click();
    await mobile.locator('#page-nav a[href="#ppt-scenarios"]').click();
    await mobile.waitForFunction(() => document.querySelector('#page-nav a[href="#ppt-scenarios"]')?.getAttribute("aria-current") === "location");
    await mobile.waitForFunction(() => {
      const top = document.querySelector("#ppt-scenarios")?.getBoundingClientRect().top;
      return Number.isFinite(top) && top >= 0 && top < 150;
    });
    const mobileNavigation = await mobile.evaluate(() => ({
      active: document.querySelector("#page-nav a.is-active")?.getAttribute("href"),
      currentTitle: document.querySelector(".navLocationTitle")?.textContent.trim(),
      menuOpen: document.querySelector("#page-nav")?.classList.contains("open"),
      hash: window.location.hash,
    }));
    if (mobileNavigation.active !== "#ppt-scenarios" || mobileNavigation.currentTitle !== "真实作业场景" || mobileNavigation.menuOpen || mobileNavigation.hash) throw new Error(`Mobile navigation interaction failed: ${JSON.stringify(mobileNavigation)}`);
    await mobile.locator(".navToggle").click();
    await mobile.waitForTimeout(150);
    if ((await mobile.locator('#page-nav a[href="#ppt-scenarios"]').getAttribute("aria-current")) !== "location") throw new Error("Opening the mobile navigation changed the current section");
    await mobile.screenshot({ path: path.join(artifactDir, "mobile-navigation-open.png"), fullPage: false });
    await mobile.locator(".navToggle").click();
    await mobile.locator(".scenarioBandHeader").first().scrollIntoViewIfNeeded();
    await mobile.waitForFunction(() => [...document.querySelectorAll(".scenarioBand:first-of-type img")].every((image) => image.complete && image.naturalWidth > 0));
    await mobile.waitForTimeout(500);
    await mobile.screenshot({ path: path.join(artifactDir, "mobile-integrated-3-4t.png"), fullPage: false });
    await mobile.locator(".categoryContextVisual").scrollIntoViewIfNeeded();
    await mobile.screenshot({ path: path.join(artifactDir, "mobile-class-choice.png"), fullPage: false });
    await mobile.locator(".taskCapabilityVisual").scrollIntoViewIfNeeded();
    await mobile.screenshot({ path: path.join(artifactDir, "mobile-visual-expansion.png"), fullPage: false });
    await mobile.locator(".scenarioSourceContext").first().scrollIntoViewIfNeeded();
    await mobile.waitForTimeout(300);
    await mobile.screenshot({ path: path.join(artifactDir, "mobile-scenario-detail.png"), fullPage: false });
    await mobile.locator(".transportStory").scrollIntoViewIfNeeded();
    await mobile.waitForFunction(() => [...document.querySelectorAll(".transportPhotoPair img")].every((image) => image.complete && image.naturalWidth > 0));
    await mobile.screenshot({ path: path.join(artifactDir, "mobile-source-transport.png"), fullPage: false });
    await mobile.locator("#ppt-positioning .positionDecision").scrollIntoViewIfNeeded();
    await mobile.screenshot({ path: path.join(artifactDir, "mobile-positioning.png"), fullPage: false });
    await mobile.close();

    const zoomedIntegrated = await browser.newPage({ viewport: { width: 1000, height: 800 }, deviceScaleFactor: 1 });
    await zoomedIntegrated.goto(new URL("index.html", base).href, { waitUntil: "networkidle" });
    await zoomedIntegrated.waitForFunction(() => document.body.dataset.navReady === "true");
    const zoomedIntegratedLayout = await zoomedIntegrated.evaluate(() => {
      const sidebar = document.querySelector("aside.nav");
      const menu = document.querySelector("#page-nav");
      return {
        layout: getComputedStyle(document.querySelector(".layout")).display,
        sidebarPosition: getComputedStyle(sidebar).position,
        sidebarWidth: sidebar.getBoundingClientRect().width,
        menuDisplay: getComputedStyle(menu).display,
        activeCount: menu.querySelectorAll("a.is-active").length,
        overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      };
    });
    if (zoomedIntegratedLayout.layout !== "grid" || zoomedIntegratedLayout.sidebarPosition !== "sticky" || zoomedIntegratedLayout.sidebarWidth < 200 || zoomedIntegratedLayout.menuDisplay === "none" || zoomedIntegratedLayout.activeCount !== 1) throw new Error(`Zoomed integrated page lost interactive sidebar state: ${JSON.stringify(zoomedIntegratedLayout)}`);
    if (zoomedIntegratedLayout.overflow) throw new Error("Zoomed integrated page has horizontal overflow");
    await zoomedIntegrated.screenshot({ path: path.join(artifactDir, "desktop-zoomed-navigation.png"), fullPage: false });
    await zoomedIntegrated.close();

    const overview = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
    await overview.goto(new URL("excavator-overview.html", base).href, { waitUntil: "networkidle" });
    await overview.waitForFunction(() => document.body.dataset.overviewReady === "true");
    if ((await overview.locator('#page-nav a[href^="#"]').count()) !== 7) throw new Error("Overview sidebar must expose seven first-level sections");
    if ((await overview.locator(".hero").count()) !== 1 || (await overview.locator(".categoryHero").count()) !== 0) throw new Error("Overview must reuse the formal dashboard shell");
    if ((await overview.locator(".evidenceTrigger,.evidenceDrawer,.evidenceButtons,.inlineEvidenceCard").count()) !== 0) throw new Error("Overview still contains source-presentation controls or cards");
    if ((await overview.locator('main img[src*="assets/slides/slide-"]').count()) !== 0) throw new Error("Overview must not display full-slide images");
    const overviewInventory = {
      cycle: await overview.locator(".cycleColumn").count(),
      regions: await overview.locator(".regionRow").count(),
      customers: await overview.locator(".customerRow").count(),
      macro: await overview.locator(".macroRow").count(),
      tonnage: await overview.locator(".heatCell").count(),
      shares: await overview.locator(".expandedSharePanel").count(),
      applications: await overview.locator(".applicationFigure").count(),
      machines: await overview.locator(".portfolioMachine").count(),
      portfolioRows: await overview.locator(".portfolioRow").count(),
      issueModels: await overview.locator(".issueHeatRow").count(),
      ledgerRows: await overview.locator(".ledgerRow").count(),
      pageHeight: await overview.evaluate(() => document.documentElement.scrollHeight),
    };
    const requiredOverviewInventory = {
      cycle: 5,
      regions: 3,
      customers: 4,
      macro: 5,
      tonnage: 20,
      shares: 2,
      applications: 8,
      machines: 7,
      portfolioRows: 17,
      issueModels: 14,
      ledgerRows: 7,
    };
    for (const [key, expected] of Object.entries(requiredOverviewInventory)) {
      if (overviewInventory[key] !== expected) throw new Error(`Overview ${key} inventory mismatch: ${overviewInventory[key]} !== ${expected}`);
    }
    if (overviewInventory.pageHeight < 9000) throw new Error(`Overview is not a long-form analysis page: ${overviewInventory.pageHeight}px`);
    const overviewLayout = await overview.evaluate(() => ({
      overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      activeCount: document.querySelectorAll("#page-nav a.is-active").length,
    }));
    if (overviewLayout.overflow) throw new Error("Desktop overview has horizontal overflow");
    if (overviewLayout.activeCount !== 1) throw new Error(`Desktop overview must highlight one current section, found ${overviewLayout.activeCount}`);
    await overview.screenshot({ path: path.join(artifactDir, "desktop-excavator-overview.png"), fullPage: false });
    await overview.setViewportSize({ width: 390, height: 844 });
    await overview.waitForTimeout(300);
    const mobileOverviewLayout = await overview.evaluate(() => ({
      overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      bodyWidth: document.body.getBoundingClientRect().width,
      viewport: document.documentElement.clientWidth,
    }));
    if (mobileOverviewLayout.overflow || mobileOverviewLayout.bodyWidth > mobileOverviewLayout.viewport + 1) throw new Error(`Mobile overview has horizontal overflow: ${JSON.stringify(mobileOverviewLayout)}`);
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
