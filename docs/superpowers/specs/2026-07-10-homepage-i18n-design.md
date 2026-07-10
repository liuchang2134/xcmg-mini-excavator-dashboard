# Homepage Simplification and Bilingual Interface Design

## Approved Scope

The homepage follows five sections only:

1. Top navigation
2. Platform positioning and three-level quick selector
3. Product-line benchmark entry points
4. Excavator tonnage asset list
5. Platform application value

The hero retains the title, one positioning sentence, the product-line / tonnage / XCMG model selector, one primary action, and three status metrics. The previous anchor-button group and the separate project-value grid are removed.

## Interaction Model

- The Excavators product-line card is one complete link to the available asset list.
- Product lines without benchmark assets are non-interactive and clearly marked as pending integration.
- The dynamic product-line detail strip is removed.
- Each excavator asset row is one complete link. It contains the XCMG model, tonnage class, competitor count, and two or three differentiated work-condition tags. There is no duplicate nested action button.
- The quick selector remains the primary entry action and persists its selection in the URL.

## Bilingual Architecture

- Every public HTML page contains one language switch control.
- Chinese remains the default. English is selected with `?lang=en` and is also stored locally for navigation between pages.
- A shared client-side translation layer changes text nodes, page titles, placeholders, tooltips, and accessibility labels without changing the HTML layout, charts, score calculations, source data, or download paths.
- A mutation observer translates text generated after interactions, including radar selections, simulator results, filter counts, and mobile navigation labels.
- English terminology follows common North American construction-equipment specification language, including `Boom Swing`, `Stick Digging Force`, `Bucket Digging Force`, `Auxiliary Circuit`, `Operating Weight`, `Ground Pressure`, and `Overall Shipping Dimensions`.

## Responsive Target

At a 390 px viewport, the first screen is targeted at approximately 700 px and contains the title, one positioning sentence, the complete selector, one primary action, and the three status metrics without horizontal overflow.

## Verification

- Structural regression tests cover the five-section homepage, three status metrics, disabled unavailable product lines, single-link project rows, and bilingual assets on every page.
- Desktop and mobile browser checks cover Chinese and English states, URL persistence, page width, selector behavior, project navigation, and representative engineering terminology.
