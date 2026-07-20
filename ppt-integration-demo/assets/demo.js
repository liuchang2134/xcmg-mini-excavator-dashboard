(() => {
  "use strict";

  const state = {
    lang: new URLSearchParams(location.search).get("lang") === "en" ? "en" : "zh",
    data: {},
    evidenceMap: new Map(),
    slideMap: new Map(),
    activeEvidenceIds: [],
  };

  const colors = {
    Kubota: "#e87924",
    Bobcat: "#f1b80b",
    "John Deere": "#356f3d",
    Caterpillar: "#647482",
    XCMG: "#0059a7",
  };

  const configLabels = {
    standard: { zh: "标配", en: "Standard" },
    standard_wedge: { zh: "标配楔式", en: "Standard wedge" },
    optional: { zh: "选配", en: "Optional" },
    optional_1600mm: { zh: "选配 1600 mm", en: "Optional 1,600 mm" },
    telescopic_option: { zh: "可伸缩选配", en: "Telescopic option" },
    not_listed: { zh: "资料未列", en: "Not listed" },
  };

  const statusLabels = {
    优势: { zh: "优势", en: "Strength" },
    差距: { zh: "差距", en: "Gap" },
    待验证: { zh: "待验证", en: "Pending validation" },
    资料未覆盖: { zh: "资料未覆盖", en: "Not covered" },
  };

  function local(value) {
    if (value == null) return "";
    if (typeof value === "object" && !Array.isArray(value)) {
      return value[state.lang] ?? value.zh ?? value.en ?? "";
    }
    return String(value);
  }

  function recordTitle(record) {
    if (!record) return "";
    return state.lang === "en"
      ? record.en?.title || record.zh?.title || record.title?.en || record.title?.zh || record.metric
      : record.zh?.title || record.en?.title || record.title?.zh || record.title?.en || record.metric;
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function asArray(value) {
    return Array.isArray(value) ? value : value == null ? [] : [value];
  }

  function statusClass(label) {
    return label === "优势"
      ? "good"
      : label === "差距"
        ? "bad"
        : label === "待验证"
          ? "pending"
          : "warning";
  }

  function statusLabel(label) {
    return local(statusLabels[label] || { zh: label, en: label });
  }

  function temporalLabel(status) {
    const source = String(status || "");
    if (source.includes("forecast")) {
      return state.lang === "zh" ? "历史事实 / 预测" : "Historical fact / forecast";
    }
    if (source.includes("target")) {
      return state.lang === "zh" ? "历史目标" : "Historical target";
    }
    if (source.includes("plan") || source.includes("recommendation")) {
      return state.lang === "zh" ? "历史判断 / 未来计划" : "Historical finding / future plan";
    }
    if (source.includes("specification")) {
      return state.lang === "zh" ? "历史参数快照" : "Historical specification snapshot";
    }
    if (source.includes("evaluation")) {
      return state.lang === "zh" ? "历史内部评价" : "Historical internal evaluation";
    }
    return state.lang === "zh" ? "历史资料" : "Historical source";
  }

  function validationLabel(status) {
    const source = String(status || "");
    if (source.includes("requires") || source.includes("unverified") || source.includes("not_")) {
      return state.lang === "zh" ? "待当前机型验证" : "Current-model validation pending";
    }
    return state.lang === "zh" ? "已完成PPT页级映射" : "PPT page mapping complete";
  }

  async function loadData(name) {
    if (state.data[name]) return state.data[name];
    const response = await fetch(`../data/ppt-insights/${name}.json`, { cache: "no-store" });
    if (!response.ok) throw new Error(`${name}.json ${response.status}`);
    const data = await response.json();
    state.data[name] = data;
    return data;
  }

  function translateStatic() {
    document.documentElement.lang = state.lang === "zh" ? "zh-CN" : "en";
    const titleKey = state.lang === "zh" ? "titleZh" : "titleEn";
    if (document.body.dataset[titleKey]) document.title = document.body.dataset[titleKey];
    document.querySelectorAll("[data-zh][data-en]").forEach((node) => {
      node.textContent = node.dataset[state.lang];
    });
    document.querySelectorAll("[data-zh-placeholder][data-en-placeholder]").forEach((node) => {
      node.placeholder = node.dataset[`${state.lang}Placeholder`];
    });
    const langButton = document.querySelector("[data-language-toggle]");
    if (langButton) {
      langButton.textContent = state.lang === "zh" ? "EN" : "中文";
      langButton.title = state.lang === "zh" ? "Switch to English" : "切换到中文";
    }
    document.querySelectorAll("[data-route]").forEach((link) => {
      const url = new URL(link.getAttribute("href"), location.href);
      if (state.lang === "en") url.searchParams.set("lang", "en");
      else url.searchParams.delete("lang");
      link.href = url.href;
    });
  }

  function setActiveNavigation() {
    const page = document.body.dataset.page;
    document.querySelectorAll(".main-nav a[data-page-link]").forEach((link) => {
      if (link.dataset.pageLink === page) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });
  }

  function installGlobalInteractions() {
    const languageToggle = document.querySelector("[data-language-toggle]");
    languageToggle?.addEventListener("click", () => {
      const url = new URL(location.href);
      if (state.lang === "zh") url.searchParams.set("lang", "en");
      else url.searchParams.delete("lang");
      location.href = url.href;
    });

    const menuToggle = document.querySelector("[data-menu-toggle]");
    const nav = document.querySelector(".main-nav");
    menuToggle?.addEventListener("click", () => {
      const open = nav?.classList.toggle("open") || false;
      menuToggle.setAttribute("aria-expanded", String(open));
    });
    nav?.addEventListener("click", (event) => {
      if (event.target.closest("a")) {
        nav.classList.remove("open");
        menuToggle?.setAttribute("aria-expanded", "false");
      }
    });

    document.addEventListener("click", (event) => {
      const button = event.target.closest("[data-evidence]");
      if (!button) return;
      openEvidence(button.dataset.evidence.split("|").filter(Boolean), button);
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closeEvidence();
        nav?.classList.remove("open");
        menuToggle?.setAttribute("aria-expanded", "false");
      }
    });
  }

  function ensureDrawer() {
    if (document.querySelector(".evidence-drawer")) return;
    document.body.insertAdjacentHTML(
      "beforeend",
      `<div class="drawer-overlay" data-drawer-overlay></div>
       <aside class="evidence-drawer" role="dialog" aria-modal="true" aria-labelledby="drawer-title">
         <div class="drawer-head">
           <div><strong id="drawer-title"></strong><small data-drawer-subtitle></small></div>
           <button class="drawer-close" type="button" data-drawer-close aria-label="${state.lang === "zh" ? "关闭证据" : "Close evidence"}" title="${state.lang === "zh" ? "关闭" : "Close"}">×</button>
         </div>
         <div class="drawer-body" data-drawer-body></div>
       </aside>`,
    );
    document.querySelector("[data-drawer-close]").addEventListener("click", closeEvidence);
    document.querySelector("[data-drawer-overlay]").addEventListener("click", closeEvidence);
  }

  function evidenceButton(ids) {
    const list = asArray(ids).filter(Boolean);
    if (!list.length) return "";
    const label = state.lang === "zh" ? "查看依据" : "View evidence";
    const count = list.length > 1 ? ` (${list.length})` : "";
    return `<button type="button" class="evidence-button" data-evidence="${escapeHtml(list.join("|"))}">${label}${count}</button>`;
  }

  function relatedEvidenceForSlide(slideNumber) {
    const record = [...state.evidenceMap.values()].find((item) =>
      asArray(item.source_slide).map(Number).includes(Number(slideNumber)),
    );
    return record?.id || "";
  }

  async function prepareEvidence() {
    const [evidence, slides] = await Promise.all([loadData("evidence"), loadData("slides")]);
    state.evidenceMap = new Map(evidence.records.map((item) => [item.id, item]));
    state.slideMap = new Map(slides.records.map((item) => [Number(item.source_slide), item]));
    ensureDrawer();
  }

  function slideNumbersForEvidence(records) {
    return [...new Set(records.flatMap((item) => asArray(item.source_slide).map(Number)))].sort(
      (a, b) => a - b,
    );
  }

  function renderDrawerSlide(slideNumber) {
    const body = document.querySelector("[data-drawer-body]");
    const records = state.activeEvidenceIds.map((id) => state.evidenceMap.get(id)).filter(Boolean);
    const slide = state.slideMap.get(Number(slideNumber));
    if (!body || !slide || !records.length) return;
    const matchingEvidence =
      records.find((record) => asArray(record.source_slide).map(Number).includes(Number(slideNumber))) ||
      records[0];
    const numbers = slideNumbersForEvidence(records);
    const summaries = records
      .map((record) => `<li>${escapeHtml(local(record.conclusion))}</li>`)
      .join("");
    body.innerHTML = `
      <div class="drawer-summary"><strong>${state.lang === "zh" ? "结论映射" : "Mapped conclusions"}</strong><ul class="compact-list">${summaries}</ul></div>
      <div class="drawer-slides" aria-label="${state.lang === "zh" ? "证据页选择" : "Evidence slide selection"}">
        ${numbers
          .map(
            (number) =>
              `<button type="button" class="${number === Number(slideNumber) ? "active" : ""}" data-drawer-slide="${number}">${state.lang === "zh" ? "第" : "p."}${number}${state.lang === "zh" ? "页" : ""}</button>`,
          )
          .join("")}
      </div>
      <img class="drawer-image" src="${escapeHtml(slide.thumbnail)}" alt="${escapeHtml(recordTitle(slide))}">
      <div class="drawer-meta">
        <div><b>${state.lang === "zh" ? "PPT页码" : "PPT page"}</b><span>${slideNumber}</span></div>
        <div><b>${state.lang === "zh" ? "资料状态" : "Source status"}</b><span>${escapeHtml(temporalLabel(matchingEvidence.status))}</span></div>
        <div><b>${state.lang === "zh" ? "数据来源" : "Data source"}</b><span>${escapeHtml(matchingEvidence.source_type)}</span></div>
        <div><b>${state.lang === "zh" ? "数据时间" : "As-of date"}</b><span>${escapeHtml(matchingEvidence.as_of_date)}</span></div>
        <div><b>${state.lang === "zh" ? "当前验证" : "Current validation"}</b><span>${escapeHtml(validationLabel(matchingEvidence.validation_status))}</span></div>
        <div><b>${state.lang === "zh" ? "机型范围" : "Model scope"}</b><span>${escapeHtml(matchingEvidence.model)}</span></div>
      </div>
      <h3>${escapeHtml(recordTitle(slide))}</h3>
      <p class="source-note">${escapeHtml(slide.en?.source_note || "")}</p>
      <h4>${state.lang === "zh" ? "原始文字（中文源文）" : "Original wording (Chinese source)"}</h4>
      <pre class="raw-evidence">${escapeHtml(slide.zh?.raw_text || "")}</pre>`;
    body.querySelectorAll("[data-drawer-slide]").forEach((button) => {
      button.addEventListener("click", () => renderDrawerSlide(Number(button.dataset.drawerSlide)));
    });
    const subtitle = document.querySelector("[data-drawer-subtitle]");
    if (subtitle) {
      subtitle.textContent =
        state.lang === "zh"
          ? `PPT 第 ${slideNumber} 页 · XCMG ARC内部资料`
          : `PPT page ${slideNumber} · XCMG ARC internal`;
    }
  }

  let evidenceReturnFocus = null;

  async function openEvidence(ids, trigger) {
    await prepareEvidence();
    state.activeEvidenceIds = ids.filter((id) => state.evidenceMap.has(id));
    if (!state.activeEvidenceIds.length) return;
    evidenceReturnFocus = trigger || document.activeElement;
    const records = state.activeEvidenceIds.map((id) => state.evidenceMap.get(id));
    const slides = slideNumbersForEvidence(records);
    const drawer = document.querySelector(".evidence-drawer");
    const overlay = document.querySelector("[data-drawer-overlay]");
    const title = document.querySelector("#drawer-title");
    title.textContent = state.lang === "zh" ? "结论依据" : "Evidence trace";
    drawer.classList.add("open");
    overlay.classList.add("open");
    document.body.classList.add("drawer-open");
    renderDrawerSlide(slides[0]);
    document.querySelector("[data-drawer-close]").focus();
  }

  function closeEvidence() {
    const drawer = document.querySelector(".evidence-drawer");
    const overlay = document.querySelector("[data-drawer-overlay]");
    if (!drawer?.classList.contains("open")) return;
    drawer.classList.remove("open");
    overlay?.classList.remove("open");
    document.body.classList.remove("drawer-open");
    evidenceReturnFocus?.focus?.();
  }

  function renderFindingRows(container, records) {
    if (!container) return;
    container.innerHTML = records
      .map(
        (record, index) => `
        <div class="finding-row">
          <span class="finding-index">${String(index + 1).padStart(2, "0")}</span>
          <h4>${escapeHtml(findingRowTitle(record))}</h4>
          <p>${escapeHtml(local(record.conclusion))}</p>
          ${evidenceButton(record.evidence_id || relatedEvidenceForSlide(record.source_slide))}
        </div>`,
      )
      .join("");
  }

  function findingRowTitle(record) {
    if (record.metric_title) return local(record.metric_title);
    if (record.id?.startsWith("field-")) return fieldTitle(record);
    if (record.id?.startsWith("roadmap-")) return roadmapTitle(record);
    return recordTitle(record);
  }

  async function renderHome() {
    const [market, tonnage, field, roadmap, slides] = await Promise.all([
      loadData("market"),
      loadData("tonnage"),
      loadData("field-evaluation"),
      loadData("roadmap"),
      loadData("slides"),
    ]);
    const scenarios = tonnage.records.filter((record) => record.scenario !== "paper_competitiveness");
    const kpis = document.querySelector("[data-home-kpis]");
    if (kpis) {
      const items = [
        [slides.records.length, { zh: "PPT证据页", en: "PPT evidence pages" }, { zh: "第48–68页完整映射", en: "Slides 48-68 fully mapped" }],
        [scenarios.length, { zh: "真实场景", en: "Field scenarios" }, { zh: "运输与七类施工工况", en: "Transport plus seven work scenarios" }],
        [field.records.length, { zh: "实机评价项", en: "Field-evaluation findings" }, { zh: "不生成新评分", en: "No new score created" }],
        [roadmap.records.length, { zh: "验证任务", en: "Validation actions" }, { zh: "均非完成状态", en: "None treated as complete" }],
      ];
      kpis.innerHTML = items
        .map(
          ([value, label, note]) => `<article><strong>${value}</strong><span>${local(label)}</span><small>${local(note)}</small></article>`,
        )
        .join("");
    }

    const highlights = [
      market.records.find((item) => item.id === "market-sales-trend"),
      market.records.find((item) => item.id === "market-transport-envelope"),
      tonnage.records.find((item) => item.id === "paper-competitiveness"),
      field.records.find((item) => item.id === "field-fine-control"),
      field.records.find((item) => item.id === "field-serviceability"),
    ].filter(Boolean);
    highlights.forEach((record) => {
      record.metric_title = {
        zh:
          record.id === "market-sales-trend"
            ? "市场"
            : record.id === "market-transport-envelope"
              ? "运输"
              : record.id === "paper-competitiveness"
                ? "纸面竞争力"
                : record.id === "field-fine-control"
                  ? "实机操控"
                  : "全生命周期",
        en:
          record.id === "market-sales-trend"
            ? "Market"
            : record.id === "market-transport-envelope"
              ? "Transport"
              : record.id === "paper-competitiveness"
                ? "Paper competitiveness"
                : record.id === "field-fine-control"
                  ? "Field control"
                  : "Ownership lifecycle",
      };
    });
    renderFindingRows(document.querySelector("[data-home-findings]"), highlights);

    const coverage = document.querySelector("[data-home-coverage]");
    if (coverage) {
      const groups = [
        ["48", { zh: "市场规模与格局", en: "Market volume and landscape" }, "ev-market-volume"],
        ["49", { zh: "客户与运输", en: "Customer and transport" }, "ev-transport-regulation"],
        ["50–58", { zh: "真实场景与步骤", en: "Field scenarios and workflows" }, "ev-municipal-roadwork"],
        ["59–61", { zh: "纸面参数与配置", en: "Paper parameters and configurations" }, "ev-paper-dimensions"],
        ["62–66", { zh: "实机评价", en: "Field evaluation" }, "ev-field-safety"],
        ["67–68", { zh: "差距、定位与历史目标", en: "Gaps, positioning and historical targets" }, "ev-gap-summary"],
      ];
      coverage.innerHTML = groups
        .map(
          ([pages, title, evidence]) => `<div class="layer-row"><span class="layer-code">PPT ${pages}</span><div><h3>${local(title)}</h3><p>${state.lang === "zh" ? "原页图片、原文和状态均可追溯" : "Original page image, wording and status remain traceable"}</p></div><span class="layer-note">${state.lang === "zh" ? "证据层" : "Evidence layer"}</span>${evidenceButton(evidence)}</div>`,
        )
        .join("");
    }
  }

  function stackedSalesChart(record) {
    const series = record.series;
    const brands = ["Kubota", "Bobcat", "John Deere", "Caterpillar", "XCMG"];
    const maxTotal = 7000;
    const baseY = 300;
    const plotHeight = 245;
    const scale = plotHeight / maxTotal;
    const bars = series
      .map((row, index) => {
        const x = 92 + index * 160;
        let y = baseY;
        const total = brands.reduce((sum, brand) => sum + Number(row[brand] || 0), 0);
        const rects = brands
          .map((brand) => {
            const value = Number(row[brand] || 0);
            const height = value * scale;
            y -= height;
            const label = height > 22 ? `<text class="chart-label" x="${x + 43}" y="${y + height / 2 + 4}" text-anchor="middle">${value}</text>` : "";
            return `<g><rect x="${x}" y="${y.toFixed(1)}" width="86" height="${Math.max(height, 1).toFixed(1)}" fill="${colors[brand]}" ${row.forecast ? 'stroke="#163a59" stroke-dasharray="3 2"' : ""}><title>${brand}: ${value}</title></rect>${label}</g>`;
          })
          .join("");
        return `${rects}<text class="chart-value" x="${x + 43}" y="${Math.max(y - 8, 16)}" text-anchor="middle">${total}</text><text class="chart-label" x="${x + 43}" y="324" text-anchor="middle">${row.year}${row.forecast ? (state.lang === "zh" ? " 预测" : " F") : ""}</text>`;
      })
      .join("");
    const grid = [0, 2000, 4000, 6000]
      .map((value) => {
        const y = baseY - value * scale;
        return `<line class="chart-grid" x1="62" x2="718" y1="${y}" y2="${y}"></line><text class="chart-label" x="52" y="${y + 4}" text-anchor="end">${value}</text>`;
      })
      .join("");
    const legend = brands
      .map((brand) => `<span><i style="background:${colors[brand]}"></i>${brand}</span>`)
      .join("");
    return `<svg viewBox="0 0 760 342" role="img" aria-label="${state.lang === "zh" ? "3至4吨挖掘机销量结构" : "3-4 t excavator volume mix"}">${grid}<line class="chart-axis" x1="62" x2="718" y1="300" y2="300"></line>${bars}</svg><div class="chart-legend">${legend}</div>`;
  }

  async function renderMarket() {
    const market = await loadData("market");
    const trend = market.records.find((item) => item.id === "market-sales-trend");
    const brand = market.records.find((item) => item.id === "market-brand-architecture");
    const customer = market.records.find((item) => item.id === "market-customer-logic");
    const transport = market.records.find((item) => item.id === "market-transport-envelope");
    const chart = document.querySelector("[data-market-chart]");
    if (chart) chart.innerHTML = stackedSalesChart(trend);
    renderFindingRows(document.querySelector("[data-market-findings]"), [trend, brand]);

    const heat = document.querySelector("[data-brand-heat]");
    if (heat) {
      const max = Math.max(...brand.model_heat.map((item) => item.units));
      heat.innerHTML = brand.model_heat
        .map(
          (item) => `<div class="metric-bar"><strong>${escapeHtml(item.brand)} ${escapeHtml(item.model)}</strong><i><span style="width:${(item.units / max) * 100}%"></span></i><em>${item.units}</em></div>`,
        )
        .join("");
    }

    const customers = document.querySelector("[data-customer-bars]");
    if (customers) {
      customers.innerHTML = customer.segments
        .map(
          (item) => `<div class="metric-bar"><strong>${escapeHtml(local(item.name))}</strong><i><span style="width:${(item.share / 40) * 100}%"></span></i><em>${item.share}%</em></div>`,
        )
        .join("");
    }

    const pack = document.querySelector("[data-transport-pack]");
    if (pack) {
      const current = transport.mass_breakdown_kg.XE35U;
      const pro = transport.mass_breakdown_kg.XE35U_PRO_historical_proposal;
      pack.innerHTML = `<div class="transport-row"><strong>XCMG XE35U</strong><div class="transport-track"><i style="width:100%">${state.lang === "zh" ? "典型配置运输包" : "Typical equipped transport package"}</i></div><b>${current.total.toLocaleString()} kg</b></div><div class="transport-row pro"><strong>XE35U PRO*</strong><div class="transport-track"><i style="width:${(pro.total_with_two_extra_buckets / current.total) * 100}%">${state.lang === "zh" ? "PPT历史方案" : "Historical PPT proposal"}</i></div><b>${pro.total_with_two_extra_buckets.toLocaleString()} kg</b></div>`;
    }

    const customerEvidence = document.querySelector("[data-customer-evidence]");
    if (customerEvidence) customerEvidence.innerHTML = evidenceButton(customer.evidence_id);
    const transportEvidence = document.querySelector("[data-transport-evidence]");
    if (transportEvidence) transportEvidence.innerHTML = evidenceButton(transport.evidence_id);
  }

  function scenarioDetail(record) {
    const needs = local(record.needs)
      .map((item) => `<li>${escapeHtml(item)}</li>`)
      .join("");
    const steps = local(record.steps)
      .map((item) => `<li>${escapeHtml(item)}</li>`)
      .join("");
    return `<div class="scenario-hero"><img src="${escapeHtml(record.image)}" alt="${escapeHtml(local(record.title))}"><div class="scenario-summary"><div class="action-row" style="margin-top:0"><span class="status-pill ${statusClass(record.finding_status)}">${statusLabel(record.finding_status)}</span></div><h3 style="margin-top:8px">${escapeHtml(local(record.title))}</h3><p>${escapeHtml(local(record.conclusion))}</p><div class="scenario-meta"><div><b>${state.lang === "zh" ? "客户" : "Customer"}</b><span>${escapeHtml(local(record.customer))}</span></div><div><b>${state.lang === "zh" ? "验证状态" : "Validation"}</b><span>${escapeHtml(validationLabel(record.validation_status))}</span></div></div><div class="action-row">${evidenceButton(record.evidence_id)}</div></div></div><div class="scenario-columns"><div><h4>${state.lang === "zh" ? "关键购买逻辑" : "Key purchase logic"}</h4><ul class="compact-list">${needs}</ul></div><div><h4>${state.lang === "zh" ? "作业步骤" : "Work sequence"}</h4><ol class="numbered-steps">${steps}</ol></div></div>`;
  }

  function installScenarioExplorer(records) {
    const desktop = document.querySelector("[data-scenario-desktop]");
    const mobile = document.querySelector("[data-scenario-mobile]");
    if (desktop) {
      desktop.innerHTML = `<div class="scenario-tabs">${records.map((record, index) => `<button class="scenario-tab ${index === 0 ? "active" : ""}" type="button" data-scenario-id="${escapeHtml(record.id)}">${escapeHtml(local(record.title))}</button>`).join("")}</div><div class="scenario-detail" data-scenario-detail>${scenarioDetail(records[0])}</div>`;
      desktop.querySelectorAll("[data-scenario-id]").forEach((button) => {
        button.addEventListener("click", () => {
          desktop.querySelectorAll(".scenario-tab").forEach((item) => item.classList.remove("active"));
          button.classList.add("active");
          const record = records.find((item) => item.id === button.dataset.scenarioId);
          desktop.querySelector("[data-scenario-detail]").innerHTML = scenarioDetail(record);
        });
      });
    }
    if (mobile) {
      mobile.innerHTML = records
        .map(
          (record, index) => `<details class="mobile-scenario" ${index === 0 ? "open" : ""}><summary>${escapeHtml(local(record.title))}<span class="status-pill ${statusClass(record.finding_status)}">${statusLabel(record.finding_status)}</span></summary><div class="mobile-scenario-content">${scenarioDetail(record)}</div></details>`,
        )
        .join("");
    }
  }

  function labelCells(table) {
    const headers = [...table.querySelectorAll("thead th")].map((th) => th.textContent.trim());
    table.querySelectorAll("tbody tr").forEach((row) => {
      [...row.children].forEach((cell, index) => {
        cell.dataset.label = headers[index] || "";
      });
    });
  }

  function paperParameterTable(record) {
    const models = ["XE35U", "U35-4", "KX033-4", "KX030-4", "SY35U"];
    const headers = [
      state.lang === "zh" ? "类别" : "Group",
      state.lang === "zh" ? "指标" : "Metric",
      state.lang === "zh" ? "单位" : "Unit",
      ...models,
    ];
    return `<table class="responsive-table"><caption>${state.lang === "zh" ? "纸面参数原值；不改变现有产品评分" : "Paper specification values; existing product scores remain unchanged"}</caption><thead><tr>${headers.map((header) => `<th>${header}</th>`).join("")}</tr></thead><tbody>${record.parameters
      .map(
        (item) => `<tr><th>${escapeHtml(local(item.group))}</th><td>${escapeHtml(local(item.metric))}</td><td>${escapeHtml(item.unit)}</td>${models.map((model) => `<td class="${model === "XE35U" ? "xcmg-cell" : ""}">${escapeHtml(item[model])}</td>`).join("")}</tr>`,
      )
      .join("")}</tbody></table>`;
  }

  function paperConfigurationTable(record) {
    const models = ["XE35U", "U35-4", "KX033-4", "KX030-4", "SY35U"];
    return `<table class="responsive-table"><caption>${state.lang === "zh" ? "标配、选配及资料未列状态" : "Standard, optional and not-listed status"}</caption><thead><tr><th>${state.lang === "zh" ? "配置" : "Configuration"}</th>${models.map((model) => `<th>${model}</th>`).join("")}</tr></thead><tbody>${record.configurations
      .map(
        (item) => `<tr><th>${escapeHtml(local(item.metric))}</th>${models.map((model) => `<td class="${model === "XE35U" ? "xcmg-cell" : ""}">${escapeHtml(local(configLabels[item[model]] || { zh: item[model], en: item[model] }))}</td>`).join("")}</tr>`,
      )
      .join("")}</tbody></table>`;
  }

  async function renderTonnage() {
    const [tonnage, field] = await Promise.all([loadData("tonnage"), loadData("field-evaluation")]);
    const scenarios = tonnage.records.filter((record) => record.scenario !== "paper_competitiveness");
    const paper = tonnage.records.find((record) => record.id === "paper-competitiveness");
    installScenarioExplorer(scenarios);

    const params = document.querySelector("[data-paper-params]");
    if (params) {
      params.innerHTML = paperParameterTable(paper);
      labelCells(params.querySelector("table"));
    }
    const configs = document.querySelector("[data-paper-configs]");
    if (configs) {
      configs.innerHTML = paperConfigurationTable(paper);
      labelCells(configs.querySelector("table"));
    }
    const paperEvidence = document.querySelector("[data-paper-evidence]");
    if (paperEvidence) paperEvidence.innerHTML = evidenceButton(paper.evidence_id);

    const fieldMatrix = document.querySelector("[data-field-matrix]");
    if (fieldMatrix) {
      fieldMatrix.innerHTML = `<table class="responsive-table field-matrix"><caption>${state.lang === "zh" ? "仅使用优势、差距、待验证和资料未覆盖，不计算实机综合分" : "Only strength, gap, pending validation and not covered are used; no aggregate field score is calculated"}</caption><thead><tr><th>${state.lang === "zh" ? "评价维度" : "Dimension"}</th><th>${state.lang === "zh" ? "状态" : "Status"}</th><th>${state.lang === "zh" ? "具体判断" : "Specific finding"}</th><th>${state.lang === "zh" ? "验证要求" : "Validation requirement"}</th><th>${state.lang === "zh" ? "依据" : "Evidence"}</th></tr></thead><tbody>${field.records
        .map(
          (record) => `<tr><th>${escapeHtml(fieldTitle(record))}</th><td><span class="matrix-status ${statusClass(record.finding_status)}">${statusLabel(record.finding_status)}</span></td><td>${escapeHtml(local(record.conclusion))}</td><td>${escapeHtml(validationLabel(record.validation_status))}</td><td>${evidenceButton(record.evidence_id)}</td></tr>`,
        )
        .join("")}</tbody></table>`;
      labelCells(fieldMatrix.querySelector("table"));
    }

    const summary = document.querySelector("[data-tonnage-summary]");
    if (summary) {
      const selection = [
        scenarios.find((item) => item.id === "scenario-transport"),
        paper,
        field.records.find((item) => item.id === "field-fine-control"),
        field.records.find((item) => item.id === "field-cab-comfort"),
        field.records.find((item) => item.id === "field-serviceability"),
      ];
      renderFindingRows(summary, selection.filter(Boolean));
    }
  }

  function fieldTitle(record) {
    const labels = {
      "field-safety": { zh: "安全系统", en: "Safety systems" },
      "field-reliability-coating": { zh: "防锈与耐久", en: "Corrosion and durability" },
      "field-environment": { zh: "环境适应性", en: "Environmental capability" },
      "field-travel-control": { zh: "行走操控", en: "Travel control" },
      "field-fine-control": { zh: "微动与精准性", en: "Inching and precision" },
      "field-grading-control": { zh: "平地协调性", en: "Grading coordination" },
      "field-cab-comfort": { zh: "驾驶环境与人机", en: "Cab and ergonomics" },
      "field-serviceability": { zh: "维修性", en: "Serviceability" },
      "field-economy": { zh: "燃油经济性", en: "Fuel economy" },
      "field-detail-quality": { zh: "细节品质", en: "Detail quality" },
      "field-documentation": { zh: "售前售后资料", en: "Sales and service documents" },
    };
    return local(labels[record.id] || { zh: record.metric, en: record.metric });
  }

  async function renderPortfolio() {
    const portfolio = await loadData("portfolio");
    const current = portfolio.records.find((item) => item.id === "portfolio-current-gap");
    const status = portfolio.records.find((item) => item.id === "portfolio-pro-status");
    const positioning = portfolio.records.find((item) => item.id === "portfolio-positioning");
    const target = portfolio.records.find((item) => item.id === "portfolio-historical-target");
    const compare = document.querySelector("[data-portfolio-compare]");
    if (compare) {
      compare.innerHTML = `<div class="portfolio-column"><img src="../assets/arc/xe35u-official-cropped.jpg" alt="XCMG XE35U"><h3>${state.lang === "zh" ? "XCMG当前资料状态" : "XCMG source-state view"}</h3><div class="variant-list"><div><b>${state.lang === "zh" ? "短尾" : "Short tail"}</b><span>XE35U</span></div><div><b>${state.lang === "zh" ? "常规尾" : "Conventional tail"}</b><span>${state.lang === "zh" ? "资料显示缺失" : "Gap in source"}</span></div><div><b>PRO</b><span>${state.lang === "zh" ? "历史计划与实施表述并存，当前状态待验证" : "Historical plan and implementation wording coexist; current status pending"}</span></div></div>${evidenceButton(["ev-gap-summary", "ev-paper-dimensions"])}</div><div class="portfolio-arrow" aria-hidden="true">→</div><div class="portfolio-column benchmark"><h3>${state.lang === "zh" ? "久保田型谱覆盖" : "Kubota portfolio coverage"}</h3><div class="variant-list"><div><b>${state.lang === "zh" ? "短尾" : "Short tail"}</b><span>U35-4</span></div><div><b>${state.lang === "zh" ? "常规尾" : "Conventional tail"}</b><span>KX033-4</span></div><div><b>${state.lang === "zh" ? "低配常规尾" : "Value conventional tail"}</b><span>KX030-4</span></div></div><p class="status-note">${escapeHtml(local(current.conclusion))}</p>${evidenceButton(current.evidence_id)}</div>`;
    }
    const findings = [status, positioning, target].filter(Boolean);
    renderFindingRows(document.querySelector("[data-portfolio-findings]"), findings);
  }

  async function renderRoadmap() {
    const roadmap = await loadData("roadmap");
    const list = document.querySelector("[data-roadmap-list]");
    const buttons = document.querySelectorAll("[data-priority-filter]");
    let filter = "all";

    const render = () => {
      const records = roadmap.records.filter((record) => filter === "all" || record.priority === filter);
      list.innerHTML = records
        .map(
          (record) => `<div class="roadmap-row"><span class="priority ${record.priority.toLowerCase()}">${record.priority}</span><div><h4>${escapeHtml(roadmapTitle(record))}</h4><p>${escapeHtml(local(record.conclusion))}</p></div><div><h4>${state.lang === "zh" ? "建议动作" : "Recommended action"}</h4><p>${escapeHtml(local(record.action))}</p></div><div><h4>${state.lang === "zh" ? "验证方式" : "Validation"}</h4><p>${escapeHtml(local(record.verification))}</p></div>${evidenceButton(record.evidence_id)}</div>`,
        )
        .join("");
    };
    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        filter = button.dataset.priorityFilter;
        buttons.forEach((item) => item.classList.toggle("active", item === button));
        render();
      });
    });
    render();
  }

  function roadmapTitle(record) {
    const labels = {
      "roadmap-transport-mass": { zh: "运输包轻量化", en: "Transport-package weight" },
      "roadmap-travel-speed": { zh: "行走速度与系统匹配", en: "Travel speed and system matching" },
      "roadmap-aux-flow": { zh: "AUX流量与卸油回路", en: "AUX flow and case-drain circuit" },
      "roadmap-backfill-package": { zh: "回填效率功能包", en: "Backfill productivity package" },
      "roadmap-control-tuning": { zh: "微动与回转标定", en: "Inching and swing calibration" },
      "roadmap-cab-hmi": { zh: "驾驶室与人机", en: "Cab and ergonomics" },
      "roadmap-service-quality": { zh: "维修、品质与资料", en: "Service, quality and documentation" },
      "roadmap-portfolio": { zh: "短尾/常规尾双型谱论证", en: "Short/conventional-tail portfolio case" },
    };
    return local(labels[record.id] || { zh: record.metric, en: record.metric });
  }

  function evidenceCategoryLabel(record) {
    const labels = {
      market: { zh: "市场", en: "Market" },
      transport: { zh: "运输", en: "Transport" },
      municipal_roadwork: { zh: "市政道路", en: "Municipal" },
      light_demolition: { zh: "小型拆除", en: "Demolition" },
      foundation_excavation: { zh: "地基", en: "Foundation" },
      landscape_renovation: { zh: "景观", en: "Landscape" },
      road_bridge: { zh: "道路桥梁", en: "Road/bridge" },
      agricultural_clearing: { zh: "农业清理", en: "Land clearing" },
      agricultural_drainage: { zh: "农业排水", en: "Drainage" },
      paper_competitiveness: { zh: "纸面对标", en: "Paper benchmark" },
      field_evaluation: { zh: "实机评价", en: "Field evaluation" },
      portfolio: { zh: "型谱定位", en: "Portfolio" },
    };
    return local(labels[record.scenario] || { zh: record.scenario, en: record.scenario });
  }

  async function renderEvidenceCenter() {
    const slides = await loadData("slides");
    const search = document.querySelector("[data-evidence-search]");
    const category = document.querySelector("[data-evidence-category]");
    const grid = document.querySelector("[data-evidence-grid]");
    const count = document.querySelector("[data-evidence-count]");
    const categories = [...new Set(slides.records.map((item) => item.scenario))];
    category.innerHTML = `<option value="">${state.lang === "zh" ? "全部主题" : "All topics"}</option>${categories.map((value) => `<option value="${escapeHtml(value)}">${escapeHtml(evidenceCategoryLabel({ scenario: value }))}</option>`).join("")}`;

    const render = () => {
      const term = search.value.trim().toLowerCase();
      const topic = category.value;
      const records = slides.records.filter((record) => {
        const haystack = `${recordTitle(record)} ${local(record.conclusion)} ${record.zh?.raw_text || ""}`.toLowerCase();
        return (!topic || record.scenario === topic) && (!term || haystack.includes(term));
      });
      count.textContent =
        state.lang === "zh" ? `显示 ${records.length} / ${slides.records.length} 页` : `${records.length} / ${slides.records.length} pages`;
      grid.innerHTML = records.length
        ? records
            .map((record) => {
              const evidence = relatedEvidenceForSlide(record.source_slide);
              return `<article class="evidence-card"><button type="button" class="preview" data-evidence="${escapeHtml(evidence)}" aria-label="${state.lang === "zh" ? "打开第" : "Open page "}${record.source_slide}${state.lang === "zh" ? "页依据" : " evidence"}"><img loading="lazy" src="${escapeHtml(record.thumbnail)}" alt="${escapeHtml(recordTitle(record))}"></button><div class="evidence-card-content"><h3>${escapeHtml(recordTitle(record))}</h3><p>${escapeHtml(local(record.conclusion))}</p></div><div class="evidence-card-meta"><strong>PPT ${record.source_slide}</strong><span>${escapeHtml(evidenceCategoryLabel(record))}</span></div></article>`;
            })
            .join("")
        : `<div class="empty-state">${state.lang === "zh" ? "没有符合条件的证据页" : "No evidence pages match the filter"}</div>`;
    };
    search.addEventListener("input", render);
    category.addEventListener("change", render);
    render();
  }

  async function renderPage() {
    await prepareEvidence();
    const page = document.body.dataset.page;
    if (page === "home") await renderHome();
    if (page === "market") await renderMarket();
    if (page === "tonnage") await renderTonnage();
    if (page === "portfolio") await renderPortfolio();
    if (page === "roadmap") await renderRoadmap();
    if (page === "evidence") await renderEvidenceCenter();
  }

  async function init() {
    translateStatic();
    setActiveNavigation();
    installGlobalInteractions();
    try {
      await renderPage();
    } catch (error) {
      console.error(error);
      const target = document.querySelector("main") || document.body;
      target.insertAdjacentHTML(
        "afterbegin",
        `<div class="warning-note">${state.lang === "zh" ? "数据加载失败，请通过本地HTTP预览地址打开。" : "Data failed to load. Open the prototype through the local HTTP preview URL."}</div>`,
      );
    }
  }

  init();
})();
