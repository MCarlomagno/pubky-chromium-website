"""Exercise assembly using real Git blobs and isolated commit histories."""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import build_pages


class PagesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.previous = Path.cwd()
        os.chdir(self.root)
        self.addCleanup(os.chdir, self.previous)
        self.addCleanup(self.temp.cleanup)
        self.run_git("init", "-q")
        self.run_git("config", "user.name", "Pages test")
        self.run_git("config", "user.email", "pages@example.invalid")
        self.run_git("config", "core.hooksPath", "/dev/null")
        (self.root / "docs").mkdir()

    def run_git(self, *args):
        return subprocess.check_output(["git", *args]).decode().strip()

    def commit(self):
        self.run_git("add", ".")
        self.run_git("commit", "-qm", "fixture")
        return self.run_git("rev-parse", "HEAD")

    def test_copies_only_site_blobs_and_preserves_bytes(self):
        (self.root / "docs/index.html").write_bytes(b"<html><body>site</body></html>")
        (self.root / "docs/.nojekyll").touch()
        (self.root / "private.txt").write_text("must not be deployed")
        sha = self.commit()
        output = self.root / "output"
        self.assertTrue(build_pages.copy_site(sha, output))
        self.assertEqual((output / "index.html").read_bytes(), (self.root / "docs/index.html").read_bytes())
        self.assertEqual([p.name for p in output.iterdir()], ["index.html"])

    def test_rejects_symlink_even_when_target_is_inside_site(self):
        (self.root / "docs/index.html").write_text("site")
        (self.root / "docs/link.html").symlink_to("index.html")
        sha = self.commit()
        with self.assertRaisesRegex(ValueError, "links"):
            build_pages.copy_site(sha, self.root / "output")

    def test_rejects_reserved_preview_path(self):
        (self.root / "docs/pr-1").mkdir()
        (self.root / "docs/pr-1/index.html").write_text("collision")
        sha = self.commit()
        with self.assertRaisesRegex(ValueError, "reserved"):
            build_pages.copy_site(sha, self.root / "output")

    def test_rejects_hidden_site_files(self):
        (self.root / "docs/.env").write_text("must not be deployed")
        sha = self.commit()
        with self.assertRaisesRegex(ValueError, "Unexpected"):
            build_pages.copy_site(sha, self.root / "output")

    def test_production_stays_on_main_and_closed_or_fork_previews_disappear(self):
        index = self.root / "docs/index.html"
        index.write_text("<html><head></head><body>MAIN</body></html>")
        main_sha = self.commit()
        index.write_text("<html><head></head><body>PREVIEW</body></html>")
        preview_sha = self.commit()
        pulls = [[{"number": 1, "head": {"repo": {"full_name": "owner/site"}}},
                  {"number": 2, "head": {"repo": {"full_name": "fork/site"}}}]]
        original = subprocess.check_output

        def command(args, **kwargs):
            return json.dumps(pulls).encode() if args[0] == "gh" else original(args, **kwargs)

        for name, expected in [("first", True), ("after-close", False)]:
            refs = {"refs/heads/main": main_sha, "refs/pull/1/head": preview_sha}
            with patch.dict(os.environ, {"GITHUB_REPOSITORY": "owner/site"}), \
                 patch("sys.argv", ["build_pages.py", "--output", str(self.root / name)]), \
                 patch.object(build_pages, "fetch", side_effect=lambda ref: refs[ref]), \
                 patch.object(subprocess, "check_output", side_effect=command), \
                 contextlib.redirect_stdout(io.StringIO()):
                build_pages.main()
            output = self.root / name
            self.assertIn("MAIN", (output / "index.html").read_text())
            self.assertEqual((output / "pr-1").exists(), expected)
            self.assertFalse((output / "pr-2").exists())
            if expected:
                page = (output / "pr-1/index.html").read_text()
                self.assertIn("PREVIEW", page)
                self.assertIn("noindex,nofollow", page)
                self.assertIn(preview_sha[:8], page)
            pulls = [[]]


if __name__ == "__main__":
    unittest.main()
