# Crane PPT Platform Integration Design

## Objective

Integrate the 163-slide North America crane insight deck into the existing XCMG ARC platform without creating a separate crane microsite. The existing Excel benchmark remains the quantitative source for specification, configuration, work-condition, and ranking views. PPT-derived market and product analysis is added as a separate evidence layer and must not alter existing scores.

## Product structure

### Platform home (`arc.html`)

- Keep one platform-wide navigation system.
- Make the crane product-line card a live platform entry, not a link to an intermediate navigation site.
- When the crane line is selected, show an inline asset panel with:
  - one prominent crane industry-insight report entry;
  - direct links to RT-60t, RT-75t, RT-100t, RT-130t, RT-160t, and AT-150t;
  - concise coverage information and source dates.
- The quick selector must resolve directly to the selected crane class page.
- `crane-overview.html` remains only as a backward-compatible redirect; it is not exposed as a navigation destination.

### Crane industry report (`crane-market-overview.html`)

This is a long-form analysis report, not a navigation hub. It contains:

1. PESTEL and macro environment (slides 1-2).
2. Market volume and product mix (slide 3).
3. Share, benchmark brands, and competitive positioning (slides 4-6).
4. United States and Canada regional demand (slides 7-9).
5. Boom-truck segment analysis (slides 10-57).
6. All-terrain segments not represented by a formal Excel class page (slides 69-80).
7. Crawler-crane analysis (slides 120-129).
8. Portfolio gaps and product-line competitiveness (slides 130-142).
9. Product roadmap and 2025-2027 portfolio (slides 143-152).
10. Market strategy, dealer coverage, rental accounts, service, parts, and local assembly (slides 153-163).

Charts are reconstructed from source data where the source is recoverable. PPT tables are converted to responsive HTML. Useful machine and application images are extracted individually; full-slide screenshots are not used as primary content.

### Class benchmark pages

Each existing class page keeps the current Excel-backed sections and adds a source-mapped PPT analysis layer before the specification ranking:

- RT-60t and RT-75t: slides 81-95.
- RT-100t: slides 96-107.
- RT-130t: slides 108-119.
- AT-150t: slides 58-68.
- RT-160t: portfolio and planned 165-US-ton material from slides 132, 147, and 152. This content is explicitly labelled as planning and validation scope, not current verified performance.

The page order is:

1. Benchmark summary.
2. Market, customer, and regional context.
3. Application and work-condition evidence.
4. PPT product positioning and customer-use evaluation.
5. Existing Excel specification position and six work conditions.
6. Equipment and source matrices.
7. Improvement actions and validation boundaries.

## Data architecture

The crane deck is processed independently from the excavator deck.

- `data/crane-ppt-insights/slides.json`
- `data/crane-ppt-insights/segment-map.json`
- `data/crane-ppt-insights/market.json`
- `data/crane-ppt-insights/regions.json`
- `data/crane-ppt-insights/products.json`
- `data/crane-ppt-insights/portfolio.json`
- `data/crane-ppt-insights/roadmap.json`
- `data/crane-ppt-insights/evidence.json`
- `assets/crane-ppt-source/`

Every record includes slide number, source type, source date, status (`historical`, `current-at-source-date`, or `plan`), and validation status. Chinese source text is preserved; English copy uses crane and lifting terminology.

## Evidence and scoring boundaries

- Existing Excel scores and weights do not change.
- PPT product evaluations are presented as qualitative evidence unless the slide contains a directly stated measurement.
- Historical sales, 2025 targets, and 2026-2027 plans use visibly different labels.
- Plans are never presented as completed actions.
- Missing or ambiguous source content remains unverified rather than being inferred.
- Page content remains traceable through a compact source register instead of repeated “from PPT” callouts in the body.

## Visual system

- Reuse the current XCMG ARC layout, navigation, type scale, colors, tables, and mobile behavior.
- Use compact report bands, engineering tables, market charts, regional matrices, and real crane images.
- Avoid nested cards, marketing-style hero composition, full-slide screenshots, and decorative whitespace.
- Desktop and 390 px mobile layouts must avoid horizontal page overflow. Wide matrices may use a contained table scroller only where unavoidable.

## Backward compatibility

- Existing crane class URLs remain unchanged.
- Existing Excel source download remains available in the source-data center.
- `crane-overview.html` redirects to `crane-market-overview.html` for old bookmarks.
- The branch `codex/crane-benchmark-integration` is the rollback point; implementation occurs on `codex/crane-ppt-platform-integration`.

