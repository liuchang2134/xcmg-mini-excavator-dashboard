# Internal Deployment Gate

The source presentation contains product gaps, targets, future portfolio plans, timing and other internal information. `noindex` metadata and an unlinked URL do not provide access control.

## Recommended production route

1. Host the static prototype in the XCMG North America SharePoint tenant or Azure Static Web Apps.
2. Require Microsoft Entra ID authentication before any page or asset is returned.
3. Authorize a dedicated security group for XCMG ARC product, engineering, sales and management users. Do not grant tenant-wide anonymous or external access.
4. Apply Conditional Access for managed devices and approved locations where corporate policy requires it.
5. Keep the PPT, slide images, JSON evidence and downloaded exports behind the same authorization boundary as the HTML pages.
6. Enable access logging and periodic membership review; define an owner for removing access when roles change.
7. Separate current validated specifications from historical facts and future plans at publication time. Require product, compliance and program-owner review before release.

## SharePoint option

Use a private communication site or document-library application page with inheritance disabled only where approved. Grant access through an Entra security group, block anonymous sharing, and keep download permissions aligned with the source library.

## Azure option

Use Azure Static Web Apps with Entra ID authentication and route rules that require an authenticated authorized role for every HTML, JSON, image and presentation path. Store deployment credentials in the approved CI secret store, not in the repository.

## Prohibited production setup

- Public GitHub Pages
- Public object-storage links for slide thumbnails or JSON
- Security based only on obscured URLs, `robots.txt` or `noindex`
- Employee names or unnecessary personal information in the rendered evidence

Formal deployment remains blocked until the user explicitly approves the prototype and the access-control owner confirms the chosen internal hosting route.
