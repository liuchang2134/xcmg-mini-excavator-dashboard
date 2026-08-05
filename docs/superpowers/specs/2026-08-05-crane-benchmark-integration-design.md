# Crane Benchmark Integration Design

## Objective

Add the supplied crane benchmark workbook to the formal XCMG ARC product benchmark platform with the same evidence, scoring, interaction, bilingual, and responsive quality bar as the excavator pages. Keep excavator calculations and generated pages unchanged.

## Source Boundary

- Governed source: `data/source-excel/XCMG_crane_benchmark_data_pool.xlsx`.
- Imported crane sheets: `RT-60t`, `RT-75t `, `RT-100t`, `RT-130t`, `RT-160t`, and `AT-150t`.
- Excluded workbook sheets: `Sheet1`, `5-6`, `6-7 缺`, `40-60`, and `总结`; these are links or excavator leftovers rather than crane benchmark inputs.
- Workbook blanks mean `资料未记录`, not `无配置` and not zero performance.
- The displayed source update date comes from each worksheet's `Updated:` row.

## Product Information Architecture

The homepage crane product-line card becomes a live entry and opens `crane-overview.html`. The overview separates rough-terrain and all-terrain cranes and links to six benchmark assets:

- `crane-rt-60t.html`
- `crane-rt-75t.html`
- `crane-rt-100t.html`
- `crane-rt-130t.html`
- `crane-rt-160t.html`
- `crane-at-150t.html`

Each tonnage page follows the existing excavator visual language and reading order:

1. Benchmark overview and data coverage.
2. Eligible overall and category rankings.
3. Six crane work-condition modules.
4. Parameter and configuration comparison matrices.
5. XCMG gap analysis and improvement simulator where evidence supports it.
6. Full raw-data table and source-quality notes.

## Crane Work Conditions

The crane modules use only workbook fields and configurations relevant to the operating condition:

1. Road transport and compliance: transport mass, axle load, width, height, length, removable counterweight, and dolly-related fields.
2. Site access and rough-terrain mobility: turning radius, travel speed, gradeability, ground clearance, tire information, and drive configuration.
3. Main-boom lifting: main-boom length, rated lifting values, line pull, winch speed, and boom operating speeds.
4. Long-reach and high-elevation lifting: boom tip height, maximum radius, jib length, jib offsets, and extension speed.
5. Outrigger setup and uneven-ground stability: outrigger spread/modes, out-of-level charts, house lock, and stability-related configuration.
6. Continuous, cold-weather, and attachment work: engine heater, cold-weather package, automatic lubrication, greaseless boom, auxiliary winch, tow hooks, and cribbing rack.

Weights are crane-specific configuration data in the builder and must sum to 100 within each module. They do not reuse excavator work-condition weights.

## Scoring and Eligibility

- Parameter metrics are normalized to 0-100 using the existing platform direction-aware comparison method.
- Configuration states are normalized as standard 100, optional 60, absent 0, and unrecorded excluded from the denominator.
- Eligible overall score keeps the platform 65% parameter / 35% configuration split.
- A product must have at least 60% valid parameter coverage and 60% valid configuration coverage for the respective component score.
- Missing values never become zero.
- The workbook's 1/3/5 legend is retained as source metadata but is not treated as populated model scoring because the inspected model score columns are blank.
- `RT-160t` has no XCR165U parameter data and therefore displays competitor/reference coverage without XCMG ranking.
- `AT-150t` has XCA150U values but no populated competitor values; repeated 130t RT competitor headers are flagged as source mismatch and excluded from ranking.
- Low-coverage competitors, including partially populated Zoomlion records, display coverage and raw values but are excluded where the threshold is not met.

## Data Model

The crane builder produces a normalized JSON artifact with:

- source sheet, crane family, tonnage, model, brand, source update date;
- parameter category, subcategory, metric, unit, value, normalized value, direction, and validity;
- configuration item, raw status, normalized status, and data state;
- condition mappings and condition weights;
- model and component coverage;
- anomaly code and user-facing explanation.

The JSON is persisted under `data/generated/cranes/` so the HTML renderer and tests consume the same authoritative normalized records.

## UI and Interaction

- Reuse `assets/dashboard.css`, `assets/dashboard.js`, logo, colors, typography, table styles, navigation behavior, and footer.
- Desktop uses a stable sidebar and paired analysis panels; mobile uses the existing drawer and disclosure patterns without horizontal page overflow.
- Radar legends are multi-select and default to all eligible models.
- Tables keep the model columns readable and use contained horizontal scrolling only where a matrix cannot reasonably collapse.
- Data coverage badges distinguish `可评分`, `参考`, `资料不足`, and `数据待核验`.
- Bilingual labels use professional crane terminology and preserve model names and source units.

## Verification

- Unit tests cover sheet selection, excluded-sheet protection, value/config parsing, score direction, coverage thresholds, and the two known incomplete sheets.
- Homepage tests prove the crane card is live while other unconnected product lines remain disabled.
- Link tests cover the overview and six tonnage pages.
- Browser checks cover desktop and 390 px mobile, English and Chinese, no body-level horizontal overflow, no overlapping text, all-model radar interaction, and source download.
- Existing excavator model, interaction, and visual tests must remain green.

