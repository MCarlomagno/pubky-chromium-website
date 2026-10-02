# Pubky Chromium download website

Repository: https://github.com/MCarlomagno/pubky-chromium-website
Browser source: https://github.com/MCarlomagno/pubky-chromium

This repository is for the experimental Linux x86_64 download page. Use plain HTML/CSS and local Pubky artwork. The distributable browser package belongs in a prerelease of the browser-source repository, not in this repository. Until a tested package, version, SHA-256 and install instructions are available, the page must say that no build is available.

Exclude the catalog, key gateway, DNS, login, trackers, backend, updater, paid hosting, and claims of Google endorsement or automatic security updates. Only genuine browser screenshots may be shown as screenshots. Preserve source and artwork attribution.

Run `python3 scripts/check_site.py` before review. Preview locally with `python3 -m http.server 8000 --bind 127.0.0.1 --directory docs`. Check desktop/mobile layout and keyboard focus in a real browser. Open a draft pull request from a feature branch; review and passing checks precede merge or production deployment. Do not self-approve.

Hosting: GitHub Pages from the main branch's `/docs` folder, once independently reviewed. Do not publish a feature branch as the production Pages source. Roll back by reverting the bad commit on main and letting Pages publish the previous content; check the Pages build and fetched site afterward.
