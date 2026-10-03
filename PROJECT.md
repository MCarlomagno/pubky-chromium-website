# Pubky Chromium download website

Repository: https://github.com/MCarlomagno/pubky-chromium-website
Browser source: https://github.com/MCarlomagno/pubky-chromium

This repository contains the Pubky Chromium download page for macOS on Apple Silicon and Ubuntu Linux x86_64. Use plain HTML/CSS and local artwork. Keep distributable packages in browser-repository prereleases; do not commit binaries here.

A download must use the exact published asset URL and show its exact source revision and SHA-256. Validate the package and fetch the published asset to verify its digest before enabling a link. Preserve normal sandbox, TLS and DNS protections. If no verified package exists, do not show a download link.

Keep scope to the download page. Exclude catalog, key gateway, DNS service, login, trackers, backend, updater, paid hosting, and claims of Google endorsement or automatic security updates. Only genuine browser screenshots may be shown as screenshots. Preserve source and artwork attribution.

Run `python3 scripts/check_site.py`, the Pages assembly tests, and desktop/mobile layout and keyboard focus checks. Update the existing feature PR. The owner authorized automatic PR preview deployments; independent review and passing checks still precede merge. Do not self-approve or self-merge.

GitHub Actions deploys `main`'s `/docs` as production and open same-repository PRs under `/pr-N/`. PR updates refresh previews; closing a PR removes it. Forks receive CI checks without deployment permissions. Keep production pinned to `main`, never to a feature branch. Read preview Git blobs as static data; do not run preview scripts in the publisher. Roll back production by reverting its commit on `main`, checking the Pages workflow and fetching the public page.
