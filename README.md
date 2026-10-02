# Site release handoff

Public site files are in `docs/`. Run `python3 scripts/check_site.py`, then serve `docs/` locally to review it. The check intentionally asserts that no download is available yet; update that assertion when a reviewed package exists.

When a Linux x86_64 package has been installed and launched, update the static page with its verified version, browser-source revision, tested distribution/library/sandbox requirements, install and uninstall steps, SHA-256, and the exact GitHub prerelease asset URL from `MCarlomagno/pubky-chromium`. Fetch the published asset and verify its digest before enabling the download link. Do not commit binaries here. Add genuine browser screenshots only after checking that they contain no private windows or profile data.

The Pubky wordmark at `docs/assets/pubky-logo.svg` was copied from https://pubky.org/images/pubky-logo.svg with permission for this browser project. Browser source and license notices remain in the browser repository.

Hosting is planned through GitHub Pages, publishing `main` → `/docs` after independent review and passing checks. No Pages source is configured for this draft. To roll back a bad release, revert the release commit on `main`, wait for the Pages build, and fetch the public URL to confirm the previous page. Do not push this feature branch as the Pages source.
