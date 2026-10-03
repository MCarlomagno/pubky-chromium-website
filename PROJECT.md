# Pubky Chromium download website

Repository: https://github.com/MCarlomagno/pubky-chromium-website
Browser source: https://github.com/MCarlomagno/pubky-chromium

This repository contains the experimental Pubky Chromium download page. The current package targets macOS on Apple Silicon, extending the original Linux draft at the owner's request. Use plain HTML/CSS and local Pubky artwork. Keep distributable packages in browser-repository prereleases; do not commit binaries here.

A download must name its browser version, exact source revision, architecture, minimum deployment target, macOS version actually tested, package SHA-256, and signing/notarization status. Validate the unpacked package and fetch the published asset to verify its digest before enabling a link. Disclose untested platforms and first-launch requirements. Preserve normal sandbox, TLS and DNS protections and do not ask users to disable Gatekeeper globally. If no verified package exists, show a pending state without a download link.

Keep scope to the download page. Exclude catalog, key gateway, DNS service, login, trackers, backend, updater, paid hosting, and claims of Google endorsement or automatic security updates. Only genuine browser screenshots may be shown as screenshots. Preserve source and artwork attribution.

Run `python3 scripts/check_site.py`, preview locally, and check desktop/mobile layout and keyboard focus in a real browser. Update the existing feature PR; independent review and passing checks precede merge or deployment. Do not self-approve or self-merge.

Hosting is planned through GitHub Pages from `main` → `/docs`, after review. This PR does not configure Pages. Roll back a deployed change by reverting its commit on `main`, checking the Pages build and fetching the public page.
