# XCMG ARC UI Direction Lab

## Purpose

This directory is an isolated design study for the XCMG ARC product benchmarking platform. It does not replace or modify the published platform pages. The lab lets stakeholders compare complete interface directions using the same product assets and navigation tasks.

## Audience And Job

- Primary audience: XCMG ARC engineers, product managers, sales support, and leadership reviewers.
- Primary job: compare design directions quickly, understand each direction's trade-offs, and open a candidate at desktop, tablet, or phone size.
- Quality bar: flagship internal review surface, not a collection of static mockups.

## Shared Design Rules

- XCMG blue identifies the platform; XCMG yellow marks only the current selection or primary action.
- Product data and equipment imagery carry the page. Decorative graphics do not compete with the content.
- Controls use one vocabulary across the lab: clear labels, visible focus, stable sizes, and 44 px touch targets on coarse pointers.
- Motion communicates loading or state change and respects reduced-motion preferences.
- All directions use the same source data in `shared/demo-data.js` so visual comparison is not distorted by different content.

## Direction Hierarchy

### Primary candidates

1. Palantir-inspired industrial decision workspace: highest data density and strongest engineering workflow.
2. Starlink-inspired future data hub: strongest presentation impact and executive storytelling.
3. Apple-inspired product narrative: strongest product focus and lowest learning cost.

### Structural studies

- Siemens-inspired industrial asset registry
- Porsche-inspired model selector
- Linear-inspired engineering workspace
- Rivian-inspired work-condition narrative
- Heavy-equipment catalog

## Lab Interaction

- Single-preview and side-by-side comparison modes.
- Desktop, tablet, and phone viewport presets.
- URL state for the selected direction, comparison direction, mode, and device.
- Keyboard navigation with arrow keys between directions.
- Each candidate opens in a separate full-screen tab for detailed review.

## Responsive Behavior

- Desktop: persistent direction rail and full preview workspace.
- Tablet: narrower rail and responsive preview frame.
- Phone: horizontal direction picker, single preview, and touch-first controls. Side-by-side mode collapses to single preview.

