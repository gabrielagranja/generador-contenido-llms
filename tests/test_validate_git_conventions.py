from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_git_conventions import (
    load_policy,
    validate_branch,
    validate_commit,
    validate_commit_range,
)


class GitConventionValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = load_policy(ROOT / ".github" / "git-conventions.yml")
        cls.fixture_root = ROOT / "tests" / "fixtures" / "git-conventions"

    def test_valid_fixture_passes(self) -> None:
        fixture = json.loads((self.fixture_root / "valid.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_branch(fixture["branch"], self.policy), [])
        for commit in fixture["commits"]:
            message = commit["subject"] + "\n\n" + commit["body"]
            self.assertEqual(validate_commit(message, self.policy), [])

    def test_invalid_fixture_reports_each_violation(self) -> None:
        fixture = json.loads((self.fixture_root / "invalid.json").read_text(encoding="utf-8"))
        self.assertTrue(validate_branch(fixture["branch"], self.policy))
        errors = []
        for commit in fixture["commits"]:
            message = commit["subject"] + "\n\n" + commit["body"]
            errors.extend(validate_commit(message, self.policy))
        self.assertTrue(any("commit title must match" in error for error in errors))
        self.assertTrue(any("substantive Why:" in error for error in errors))
        self.assertTrue(any("must match the commit title" in error for error in errors))

    def test_commit_range_passes_for_valid_git_history(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=repository, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], cwd=repository, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repository, check=True)
            (repository / "sample.txt").write_text("sample\n", encoding="utf-8")
            subprocess.run(["git", "add", "sample.txt"], cwd=repository, check=True)
            subprocess.run(
                [
                    "git",
                    "commit",
                    "-m",
                    "test: validate commit range (#38)",
                    "-m",
                    "Why: exercise repository commit-range parsing.",
                    "-m",
                    "Issue: #38",
                ],
                cwd=repository,
                check=True,
            )
            errors, issues = validate_commit_range("HEAD", self.policy, cwd=repository)
            self.assertEqual(errors, [])
            self.assertEqual(issues, {"38"})


if __name__ == "__main__":
    unittest.main()
