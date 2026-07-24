# XCMG ARC 3-4 t Market and Product Prototype

This is an isolated, local-only prototype. It keeps the formal 3-4 t benchmark as the page foundation and converts the source presentation into six continuous web-native sections: market and customers, real job applications, specifications and equipment, field evaluation, product positioning, and improvement path.

The interface does not render full presentation pages. Individual field photographs are extracted from the source, while charts, tables and narrative are rebuilt for the dashboard.

## Local preview

Run from the repository root:

```powershell
python -m http.server 4174 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:4174/ppt-integration-demo/index.html
```

This is the stable 3-4 t demo entry. Do not add commit IDs, section hashes or
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
- `data/coverage-3-4t.json` maps every page from 48 through 68 to its reader-facing section.
- `data/formal-site-snapshot.json` guards the formal-site working-tree state while the demo is edited.
- Field findings are qualitative only: advantage, gap, pending validation or not covered.
- Historical plans, forecasts and targets are not presented as current results.
- Do not publish this directory through the public GitHub Pages entry.
