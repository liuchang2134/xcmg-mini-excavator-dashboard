# XCMG ARC 3-4 t Integrated PPT Prototype

This is an isolated, local-only prototype. It keeps the formal 3-4 t benchmark as the page foundation and adds PPT slides 48-68 as market, customer, transport, application, field-evaluation, improvement and evidence modules.

Only one additional page is retained for cross-tonnage excavator analysis using PPT slides 3-15.

## Local preview

Run from the repository root:

```powershell
python -m http.server 4174 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:4174/ppt-integration-demo/index.html
http://127.0.0.1:4174/ppt-integration-demo/excavator-overview.html
```

## Validation

```powershell
python ppt-integration-demo/tests/test_demo.py
cd ppt-integration-demo
npm run test:browser -- http://127.0.0.1:4174/ppt-integration-demo/
```

## Boundaries

- Formal site pages, formal scoring and `main` are unchanged.
- The 3-4 t PPT scope is pages 48-68; the category overview uses pages 3-15.
- Field findings are qualitative only: advantage, gap, pending validation or not covered.
- Historical plans, forecasts and targets are not presented as current results.
- Do not publish this directory through the public GitHub Pages entry.
