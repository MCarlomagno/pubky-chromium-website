# Pubky Chromium download page

The static site is in `docs/`. It links to the experimental macOS Apple Silicon ZIP and Ubuntu Linux x86_64 DEB in the browser repository's prereleases, with each build's source revision and SHA-256. Browser binaries and license notices are distributed from the browser repository, not committed here.

Run `python3 scripts/check_site.py`, then preview with `python3 -m http.server 8000 --bind 127.0.0.1 --directory docs`. Check desktop/mobile layout and keyboard focus in a real browser when changing the page.

For each future release, validate the package, publish the browser asset and checksum, then fetch the published asset and verify its digest before changing the download link. Update the page and the release contract in `scripts/check_site.py` together.

The Pubky wordmark at `docs/assets/pubky-logo.svg` was copied from https://pubky.org/images/pubky-logo.svg with permission for this browser project.

GitHub Actions publishes `main`'s `docs/` to [the main site](https://mcarlomagno.github.io/pubky-chromium-website/) and each open same-repository PR to `/pr-N/` (for example, [PR #1](https://mcarlomagno.github.io/pubky-chromium-website/pr-1/)). Opening, updating, reopening or closing a PR rebuilds the deployment; closed previews disappear. A push to `main` publishes production. Until the first site merge, the root lists the available previews. Draft PRs also get previews; forked PRs run checks without deployment permissions.

The Pages workflow uses GitHub's official artifact/deployment actions, a read-only assembly job, and a separate job with Pages/OIDC permissions. It reads regular files from `docs/` in pinned Git commits without running scripts from those commits. Production and previews are assembled fresh together, avoiding lost previews or a PR replacing production. `deployment.json` records their revisions. Run `python3 -m unittest discover -s scripts -p 'test_*.py'` to check assembly behavior.

Repository setup: Settings → Pages → GitHub Actions. The `github-pages` environment allows `main` and `refs/pull/*/merge`; no repository secret or external host is needed. Preview links appear in the workflow summary. This workflow does not merge PRs. Roll back production by reverting its commit on `main`; remove a preview by closing its PR, then verify the deployment and public URL.
