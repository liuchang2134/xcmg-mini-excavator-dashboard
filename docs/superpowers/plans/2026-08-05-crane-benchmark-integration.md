# Crane Benchmark Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add six source-backed crane benchmark assets and a crane overview to the formal XCMG ARC platform without changing excavator results.

**Architecture:** A product-line-specific crane parser and builder reads the governed workbook, emits normalized JSON, and renders pages with the existing shared dashboard assets. Homepage integration is limited to activating the crane card and registering the seven new crane routes.

**Tech Stack:** Python 3.11, pandas/openpyxl, static HTML/CSS/JavaScript, pytest, Playwright/browser smoke checks.

---

### Task 1: Govern and validate the source workbook

**Files:**
- Create: `data/source-excel/XCMG_crane_benchmark_data_pool.xlsx`
- Modify: `data/source-register.csv`
- Create: `tests/test_crane_source.py`

- [ ] Write tests that assert the six allowed sheet names, five excluded sheets, workbook hash metadata, and known incomplete `RT-160t` / `AT-150t` records.
- [ ] Run `pytest tests/test_crane_source.py -q` and verify it fails before the source adapter exists.
- [ ] Copy the source workbook without modifying its content and add governed register rows with market, update date, validation state, and source path.
- [ ] Run `pytest tests/test_crane_source.py -q` and verify the source-boundary tests pass.

### Task 2: Build the normalized crane data adapter

**Files:**
- Create: `tools/crane_data.py`
- Create: `tests/test_crane_data.py`
- Create: `data/generated/cranes/crane-benchmark.json`

- [ ] Write parser tests for model headers, eight parameter subcategories, configuration states, missing-value semantics, coverage, source dates, and anomaly codes.
- [ ] Run `pytest tests/test_crane_data.py -q` and verify the tests fail with the adapter missing.
- [ ] Implement `CraneWorkbook`, `CraneSheet`, `CraneModel`, `CraneMetric`, and `CraneConfiguration` records plus `load_crane_workbook()` and `write_crane_json()`.
- [ ] Encode `std=100`, `opt=60`, explicit absence `=0`, and blank `=None`; calculate coverage before scores.
- [ ] Run `pytest tests/test_crane_data.py -q` and verify all parser and anomaly tests pass.

### Task 3: Implement crane scoring and work-condition mapping

**Files:**
- Create: `tools/crane_scoring.py`
- Create: `tests/test_crane_scoring.py`

- [ ] Write tests for higher/lower direction, equal-value handling, unrecorded exclusion, 60% eligibility, 65/35 overall score, and all six condition mappings.
- [ ] Run `pytest tests/test_crane_scoring.py -q` and verify it fails before implementation.
- [ ] Implement direction-aware normalization, weighted category/condition aggregation, configuration scoring, coverage gates, rank assignment, and `not_ranked_reason`.
- [ ] Assert `RT-160t` and `AT-150t` cannot receive an XCMG overall rank from the current workbook.
- [ ] Run `pytest tests/test_crane_scoring.py -q` and verify all scoring tests pass.

### Task 4: Generate the crane overview and tonnage pages

**Files:**
- Create: `tools/build_crane_dashboards.py`
- Create: `crane-overview.html`
- Create: `crane-rt-60t.html`
- Create: `crane-rt-75t.html`
- Create: `crane-rt-100t.html`
- Create: `crane-rt-130t.html`
- Create: `crane-rt-160t.html`
- Create: `crane-at-150t.html`
- Modify: `assets/dashboard.css`
- Modify: `assets/dashboard.js`
- Modify: `assets/i18n.js`
- Create: `tests/test_crane_pages.py`

- [ ] Write page tests for required sections, bilingual labels, score eligibility messaging, all-model radar defaults, source link, stable sidebar, footer, and mobile disclosure markup.
- [ ] Run `pytest tests/test_crane_pages.py -q` and verify it fails before generation.
- [ ] Implement overview and tonnage renderers using the normalized JSON and shared dashboard components.
- [ ] Add only scoped crane CSS/JS where existing components do not cover the required matrix or coverage states.
- [ ] Run the builder twice and verify deterministic output with `git diff --exit-code` after the second run.
- [ ] Run `pytest tests/test_crane_pages.py -q` and verify all page tests pass.

### Task 5: Activate the crane product line on the platform homepage

**Files:**
- Modify: `arc.html`
- Modify: `data/project-manifest.json`
- Modify: `tests/test_arc_homepage.py`
- Modify: `README.md`

- [ ] Update homepage tests to expect excavators and cranes as live product lines while the remaining five lines stay disabled.
- [ ] Run `pytest tests/test_arc_homepage.py -q` and verify the changed expectation fails.
- [ ] Link the whole crane card to `crane-overview.html`, update quick selection and asset counts, and register the six crane analysis routes.
- [ ] Update the manifest and README with governed crane assets and formal routes.
- [ ] Run `pytest tests/test_arc_homepage.py -q` and verify the homepage tests pass.

### Task 6: Regression, responsive, and visual verification

**Files:**
- Modify: `tests/test_dashboard_browser.py`
- Create: `tests/test_crane_browser.py`
- Create: `artifacts/crane-desktop.png`
- Create: `artifacts/crane-mobile.png`

- [ ] Add browser assertions for Chinese/English rendering, 390 px body overflow, sidebar/drawer behavior, radar selection, table containment, and valid internal links.
- [ ] Run the complete Python test suite and fix only failures caused by the crane integration.
- [ ] Start the local server on an available port and run desktop plus 390 px browser checks.
- [ ] Capture desktop and mobile screenshots and visually inspect for clipping, overlap, excessive whitespace, and unreadable tables.
- [ ] Run `git diff --check`, `git status --short`, and a generated-page link scan before reporting completion.

