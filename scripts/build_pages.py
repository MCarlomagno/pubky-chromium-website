"""Assemble main and open same-repository PR previews without running PR code."""
import argparse
import html
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess


def git(*args):
    return subprocess.check_output(["git", *args])


def copy_site(commit, destination):
    """Read regular Git blobs only; never follow links or copy repository secrets."""
    records = git("ls-tree", "-rlz", commit, "docs").split(b"\0")
    files = []
    total = 0
    for record in filter(None, records):
        metadata, raw_path = record.split(b"\t", 1)
        mode, kind, oid, size = metadata.decode().split()
        path = PurePosixPath(raw_path.decode()).relative_to("docs")
        if mode not in {"100644", "100755"} or kind != "blob":
            raise ValueError(f"Site links and submodules are not allowed: {path}")
        if str(path) == ".nojekyll":
            continue  # The publisher creates its own marker at the deployment root.
        if any(part.startswith(".") for part in path.parts) or path.name == "CNAME":
            raise ValueError(f"Unexpected site file: {path}")
        if re.fullmatch(r"pr-\d+", path.parts[0]):
            raise ValueError("pr-N directories are reserved for previews")
        total += int(size)
        files.append((path, oid))
    if len(files) > 1000 or total > 20 * 1024 * 1024:
        raise ValueError("Static site exceeds 1,000 files or 20 MiB")
    if not any(str(path) == "index.html" for path, _ in files):
        return False
    for path, oid in files:
        target = destination.joinpath(*path.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(git("cat-file", "blob", oid))
    return True


def fetch(ref):
    subprocess.run(["git", "fetch", "--quiet", "--depth=1", "origin", ref], check=True)
    return git("rev-parse", "FETCH_HEAD").decode().strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    # Exclusive creation prevents accidentally clearing a checkout or old deployment.
    args.output.mkdir(parents=True, exist_ok=False)
    repo = os.environ["GITHUB_REPOSITORY"]
    pulls = json.loads(subprocess.check_output([
        "gh", "api", "--paginate", "--slurp",
        f"repos/{repo}/pulls?state=open&per_page=100",
    ]))
    manifest = {"main": fetch("refs/heads/main"), "previews": {}}
    production = copy_site(manifest["main"], args.output)
    links = []
    for pr in sorted((pr for page in pulls for pr in page), key=lambda pr: pr["number"]):
        if not pr["head"]["repo"] or pr["head"]["repo"]["full_name"] != repo:
            continue
        number = int(pr["number"])
        sha = fetch(f"refs/pull/{number}/head")
        destination = args.output / f"pr-{number}"
        if not copy_site(sha, destination):
            continue
        index = destination / "index.html"
        page = index.read_text()
        # Visible provenance and no indexing; the preview otherwise keeps its own assets.
        banner = (f'<aside style="padding:12px;text-align:center;background:#fff;color:#111">'
                  f'Preview of <a style="color:#174a93" href="https://github.com/{html.escape(repo)}/pull/{number}">'
                  f'PR #{number}</a> · {sha[:8]}</aside>')
        page, count = re.subn(r"(<body\b[^>]*>)", lambda m: m[0] + banner, page, count=1, flags=re.I)
        if count != 1:
            raise ValueError(f"PR #{number} needs an HTML body")
        page = re.sub(r"(<head\b[^>]*>)", r'\1<meta name="robots" content="noindex,nofollow">', page, count=1, flags=re.I)
        index.write_text(page)
        manifest["previews"][str(number)] = sha
        links.append(f'<li><a href="pr-{number}/">PR #{number}</a> · {sha[:8]}</li>')
    if not production:
        (args.output / "index.html").write_text(
            '<!doctype html><html lang="en"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Pubky Chromium previews</title><body>'
            '<h1>Pubky Chromium previews</h1><p>The main site will appear after its first merge.</p>'
            '<ul>' + "".join(links) + '</ul></body></html>'
        )
    (args.output / "deployment.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (args.output / "robots.txt").write_text("User-agent: *\nDisallow: /pubky-chromium-website/pr-\n")
    (args.output / ".nojekyll").touch()
    print(json.dumps(manifest, indent=2))
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        base = f"https://{repo.split('/')[0].lower()}.github.io/{repo.split('/')[1]}/"
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary:
            summary.write(f"Site: {base}\n\n")
            for number, sha in manifest["previews"].items():
                summary.write(f"- [PR #{number} preview]({base}pr-{number}/) (`{sha[:8]}`)\n")


if __name__ == "__main__":
    main()
