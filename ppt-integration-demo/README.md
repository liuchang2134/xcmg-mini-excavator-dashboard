# XCMG ARC 3-4 t PPT Integration Prototype

This directory is an isolated, local-only prototype. It maps PPT pages 48-68 into a bilingual web experience without changing the formal benchmark site or its scores.

## Local preview

Run from the repository root:

```powershell
python -m http.server 4174 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:4174/ppt-integration-demo/index.html
```

## Validation

```powershell
python ppt-integration-demo/tests/test_demo.py
cd ppt-integration-demo
npm install --ignore-scripts
npm run test:browser -- http://127.0.0.1:4174/ppt-integration-demo/
```

The browser check uses an installed Microsoft Edge or Google Chrome executable. Set `XCMG_QA_BROWSER` when the browser is installed in a non-standard location.

## Boundaries

- Scope is limited to the 3-4 t prototype and PPT pages 48-68.
- Existing benchmark calculations remain in the formal 3-4 t page and are not recalculated here.
- Field findings use qualitative states only: strength, gap, pending validation or not covered.
- Historical plans are not presented as completed current-state results.
- Do not publish this directory through the public GitHub Pages entry.

