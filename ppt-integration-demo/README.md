# XCMG ARC 3-4 t Market and Product Prototype

This is an isolated, local-only prototype. It keeps the formal 3-4 t benchmark as the page foundation and converts the source presentation into web-native market, customer, transport, application, field-evaluation and improvement analysis.

The interface does not render full presentation pages. Individual field photographs are extracted from the source, while charts, tables and narrative are rebuilt for the dashboard. One additional page provides cross-tonnage excavator analysis.

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

The first URL is the stable 3-4 t demo entry. Do not add commit IDs, section hashes or
cache-busting parameters to the shared address; the page normalizes legacy preview URLs
automatically and keeps the address unchanged during in-page navigation.

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
