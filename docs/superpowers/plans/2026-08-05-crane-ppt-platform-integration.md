# Crane PPT Platform Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate all useful content from the 163-slide North America crane insight deck into the existing XCMG ARC home, one crane market report, and six existing crane benchmark pages without changing Excel-backed scores.

**Architecture:** A dedicated PPT extraction module produces governed JSON and image assets independently from the excavator pipeline. The existing crane page generator consumes that JSON and renders report modules into each class page, while the platform home exposes the report and direct class links without an intermediate crane navigation site.

**Tech Stack:** Python 3.14, python-pptx, Pillow, static HTML/CSS/JavaScript, pytest, Playwright.

---

### Task 1: Protect the current crane implementation

**Files:**
- Create: `docs/superpowers/specs/2026-08-05-crane-ppt-platform-integration-design.md`
- Create: `docs/superpowers/plans/2026-08-05-crane-ppt-platform-integration.md`

- [ ] **Step 1: Confirm the rollback branch and clean worktree**

Run: `git status --short --branch && git branch --show-current`

Expected: branch `codex/crane-ppt-platform-integration`; no unrelated tracked changes.

- [ ] **Step 2: Record the design and implementation plan**

The design must state the home-page integration, long-form report, class mappings, evidence boundaries, and backward compatibility behavior.

- [ ] **Step 3: Commit the design checkpoint**

```powershell
git add docs/superpowers/specs/2026-08-05-crane-ppt-platform-integration-design.md docs/superpowers/plans/2026-08-05-crane-ppt-platform-integration.md
git commit -m "docs: design crane ppt platform integration"
```

### Task 2: Build the dedicated crane PPT extraction pipeline

**Files:**
- Create: `tools/crane_ppt_insights.py`
- Create: `tests/test_crane_ppt_insights.py`
- Create: `data/crane-ppt-insights/slides.json`
- Create: `data/crane-ppt-insights/segment-map.json`
- Create: `data/crane-ppt-insights/evidence.json`
- Create: `assets/crane-ppt-source/`

- [ ] **Step 1: Write parser tests**

Tests must verify:

```python
def test_crane_slide_map_covers_all_163_slides():
    slides = load_generated_slides()
    assert len(slides) == 163
    assert {item["slide"] for item in slides} == set(range(1, 164))

def test_crane_segment_map_assigns_formal_class_ranges():
    mapping = load_segment_map()
    assert mapping["RT-60t"]["slides"] == list(range(81, 96))
    assert mapping["RT-100t"]["slides"] == list(range(96, 108))
    assert mapping["RT-130t"]["slides"] == list(range(108, 120))
    assert mapping["AT-150t"]["slides"] == list(range(58, 69))

def test_crane_plans_are_not_marked_current():
    slides = load_generated_slides()
    planned = [item for item in slides if item["slide"] in range(143, 164)]
    assert all(item["status"] == "plan" for item in planned)
```

- [ ] **Step 2: Run the parser tests and confirm failure**

Run: `python -m pytest tests/test_crane_ppt_insights.py -q`

Expected: FAIL because the parser and generated files do not exist.

- [ ] **Step 3: Implement `tools/crane_ppt_insights.py`**

The module must:

```python
SOURCE_ENV = "XCMG_CRANE_PPT"
OUTPUT_DIR = ROOT / "data" / "crane-ppt-insights"
ASSET_DIR = ROOT / "assets" / "crane-ppt-source"
SOURCE_DATE = "2025-07-01"

CLASS_SLIDES = {
    "RT-60t": list(range(81, 96)),
    "RT-75t": list(range(81, 96)),
    "RT-100t": list(range(96, 108)),
    "RT-130t": list(range(108, 120)),
    "RT-160t": [132, 147, 152],
    "AT-150t": list(range(58, 69)),
}
```

It must extract ordered text blocks, native table rows, chart series and useful image blobs; attach slide number, source date, source status and class mapping; and never call the excavator PPT extractor.

- [ ] **Step 4: Generate crane PPT JSON and assets**

Run:

```powershell
$env:XCMG_CRANE_PPT='C:\Users\xcmgusa\OneDrive - XCMG North America Corporation\Documents\xwechat_files\wxid_9r97k730p5ag22_8dd1\msg\file\2026-08\北美大区重点产品线市场洞察报告 2025.07.01-V13-起重机完善版本.pptx'
python tools/crane_ppt_insights.py
```

Expected: 163 slide records, segment map, evidence register, and extracted source images.

- [ ] **Step 5: Run parser tests**

Run: `python -m pytest tests/test_crane_ppt_insights.py -q`

Expected: PASS.

### Task 3: Add reusable PPT report renderers

**Files:**
- Create: `tools/crane_ppt_render.py`
- Create: `assets/crane-insights.css`
- Create: `assets/crane-insights.js`
- Modify: `tools/build_crane_dashboards.py`
- Test: `tests/test_crane_pages.py`

- [ ] **Step 1: Add failing renderer tests**

Tests must assert that generated pages contain:

```python
assert 'data-source-slide="81"' in rt60
assert 'data-source-slide="96"' in rt100
assert 'data-source-slide="108"' in rt130
assert 'data-source-slide="58"' in at150
assert 'data-source-status="plan"' in rt160
assert 'assets/crane-insights.css' in rt60
```

- [ ] **Step 2: Run tests and confirm failure**

Run: `python -m pytest tests/test_crane_pages.py -q`

Expected: FAIL on missing PPT modules.

- [ ] **Step 3: Implement focused renderer functions**

`tools/crane_ppt_render.py` must expose `load_crane_insights()`,
`render_class_context(class_id, language)`, `render_market_overview(language)`,
and `render_source_register(slide_numbers)`. The loader returns the generated
slide and segment dictionaries; each renderer returns a complete HTML string
and raises `KeyError` for an unknown class id.

Rendered modules use source text, responsive HTML tables, extracted figures, and status labels. They must not output whole-slide screenshots or change the Excel score model.

- [ ] **Step 4: Integrate class context into the page generator**

Insert `render_class_context(sheet.label)` after the benchmark summary and before the existing specification position. Add `市场与客户`, `产品评价`, and `资料边界` navigation anchors while retaining the existing work-condition submenu.

- [ ] **Step 5: Add report styling and interaction**

`assets/crane-insights.css` must provide compact bands, two-column figure/text layouts, responsive tables, status labels, and 390 px stacking. `assets/crane-insights.js` must add chart hover/focus emphasis and source-register disclosure without creating nested pages.

- [ ] **Step 6: Regenerate pages and run tests**

Run:

```powershell
python tools/build_crane_dashboards.py
python -m pytest tests/test_crane_pages.py -q
```

Expected: PASS.

### Task 4: Replace the crane navigation hub with a full market report

**Files:**
- Create: `crane-market-overview.html`
- Modify: `tools/build_crane_dashboards.py`
- Modify: `crane-overview.html`
- Modify: `tests/test_crane_pages.py`

- [ ] **Step 1: Add failing report tests**

Tests must verify:

```python
report = (ROOT / "crane-market-overview.html").read_text(encoding="utf-8")
assert all(f'data-source-slide="{n}"' in report for n in range(1, 10))
assert 'data-source-slide="130"' in report
assert 'data-source-slide="163"' in report
assert 'craneAssetGrid' not in report
assert 'location.replace("crane-market-overview.html")' in legacy_overview
```

- [ ] **Step 2: Run tests and confirm failure**

Run: `python -m pytest tests/test_crane_pages.py -q`

Expected: FAIL because the report does not exist and the old file is still a hub.

- [ ] **Step 3: Render the long-form market report**

Generate sections for macro, market, competition, region, boom truck, all-terrain, crawler, portfolio, roadmap, marketing, service and local assembly. Each section contains the applicable source tables, images and source status.

- [ ] **Step 4: Replace the legacy overview with a redirect**

Write a minimal accessible compatibility page using:

```html
<meta http-equiv="refresh" content="0;url=crane-market-overview.html">
<script>location.replace("crane-market-overview.html" + location.search + location.hash);</script>
```

- [ ] **Step 5: Regenerate and test**

Run: `python tools/build_crane_dashboards.py && python -m pytest tests/test_crane_pages.py -q`

Expected: PASS.

### Task 5: Enrich the existing platform home

**Files:**
- Modify: `arc.html`
- Modify: `tests/test_crane_pages.py`

- [ ] **Step 1: Add failing home-page tests**

Tests must verify:

```python
assert 'href="crane-market-overview.html"' in homepage
assert 'href="crane-overview.html"' not in homepage
assert 'data-crane-asset-panel' in homepage
for page in CRANE_PAGES.values():
    assert page in homepage
```

- [ ] **Step 2: Run tests and confirm failure**

Run: `python -m pytest tests/test_crane_pages.py::test_crane_homepage_entry_and_quick_selector_are_live -q`

Expected: FAIL because the home page still points to the hub.

- [ ] **Step 3: Update the crane product-line card and selector data**

The card opens the inline crane asset panel. The panel includes one market-report row and six direct class rows. Quick selection resolves directly to a class page. No intermediate page is required.

- [ ] **Step 4: Validate keyboard and mobile behavior**

The full card uses one interactive target. The expanded asset panel is keyboard reachable and collapses on a second activation. At 390 px, the rows stack without horizontal overflow.

- [ ] **Step 5: Run home-page tests**

Run: `python -m pytest tests/test_crane_pages.py -q`

Expected: PASS.

### Task 6: Verify bilingual content, source boundaries and responsive rendering

**Files:**
- Create: `tests/crane_ppt_browser_check.cjs`
- Modify: `tests/test_crane_pages.py`
- Modify: `assets/crane-insights.css`
- Modify: `assets/crane-insights.js`

- [ ] **Step 1: Add browser checks**

The Playwright test must open the market report and all six class pages at 1440x900 and 390x844, assert no page-level horizontal overflow, switch to English, verify that headings and status labels translate, and exercise the market chart hover/focus behavior.

- [ ] **Step 2: Run the complete Python suite**

Run: `python -m pytest tests/test_crane_source.py tests/test_crane_data.py tests/test_crane_scoring.py tests/test_crane_pages.py tests/test_crane_ppt_insights.py -q`

Expected: PASS.

- [ ] **Step 3: Run browser checks**

Run: `node tests/crane_ppt_browser_check.cjs`

Expected: PASS for desktop and mobile pages with no overflow or broken links.

- [ ] **Step 4: Inspect generated pages and source coverage**

Run a link check and verify that all 163 slides appear either in the long report or the mapped class page set. Confirm that all source dates and plan/current labels are present.

- [ ] **Step 5: Commit the verified implementation**

```powershell
git add arc.html crane-*.html tools/crane_ppt_insights.py tools/crane_ppt_render.py tools/build_crane_dashboards.py assets/crane-insights.css assets/crane-insights.js assets/crane-ppt-source data/crane-ppt-insights tests/test_crane_ppt_insights.py tests/test_crane_pages.py tests/crane_ppt_browser_check.cjs docs/superpowers
git commit -m "feat: integrate crane ppt insights into arc platform"
```
