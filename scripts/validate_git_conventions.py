#!/usr/bin/env python3
"""Validate approved branch and commit-message conventions."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / ".github" / "git-conventions.yml"
BASE_BRANCHES = {"dev", "main"}
ZERO_SHA = "0" * 40


def load_policy(path: Path) -> dict[str, Any]:
    policy = json.loads(path.read_text(encoding="utf-8"))
    for key in ("branch_types", "commit_types", "max_subject_length", "required_body_fields"):
        if key not in policy:
            raise ValueError("Missing policy field: " + key)
    return policy


def validate_branch(branch: str, policy: dict[str, Any]) -> list[str]:
    if branch in BASE_BRANCHES:
        return []
    match = re.fullmatch(
        r"(?P<type>[a-z]+)/(?P<issue>[1-9][0-9]*)-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)",
        branch,
    )
    if not match:
        return ["branch must match [type]/[issue-number]-[short-slug]"]
    if match.group("type") not in policy["branch_types"]:
        return ["branch type is not allowed: " + match.group("type")]
    return []


def issue_from_branch(branch: str) -> str | None:
    match = re.fullmatch(r"[a-z]+/([1-9][0-9]*)-[a-z0-9]+(?:-[a-z0-9]+)*", branch)
    return match.group(1) if match else None


def split_message(message: str) -> tuple[str, str]:
    normalized = message.replace("\r\n", "\n").strip()
    subject, separator, body = normalized.partition("\n")
    return subject, body.lstrip("\n") if separator else ""


def validate_commit(message: str, policy: dict[str, Any]) -> list[str]:
    subject, body = split_message(message)
    errors: list[str] = []
    if len(subject) > policy["max_subject_length"]:
        errors.append("commit title exceeds " + str(policy["max_subject_length"]) + " characters")
    title_match = re.fullmatch(
        r"(?P<type>[a-z]+)(?:\((?P<scope>[a-z0-9][a-z0-9-]*)\))?: (?P<summary>.+) \(#(?P<issue>[1-9][0-9]*)\)",
        subject,
    )
    if not title_match:
        return errors + ["commit title must match [type]([optional-scope]): [summary] (#[issue-number])"]
    if title_match.group("type") not in policy["commit_types"]:
        errors.append("commit title type is not allowed: " + title_match.group("type"))
    if not title_match.group("summary").strip():
        errors.append("commit title summary must not be empty")

    why_label, issue_label = policy["required_body_fields"]
    why_match = re.search(r"^" + re.escape(why_label) + r":\s*(\S.*)$", body, re.MULTILINE)
    issue_match = re.search(
        r"^" + re.escape(issue_label) + r":\s*#([1-9][0-9]*)\s*$",
        body,
        re.MULTILINE,
    )
    if not why_match:
        errors.append("commit description must include a substantive " + why_label + ": line")
    if not issue_match:
        errors.append("commit description must include an " + issue_label + ": #[issue-number] line")
    elif issue_match.group(1) != title_match.group("issue"):
        errors.append("Issue reference in commit description must match the commit title")
    return errors


def issue_from_commit(message: str) -> str | None:
    subject, _ = split_message(message)
    match = re.fullmatch(
        r"[a-z]+(?:\([a-z0-9][a-z0-9-]*\))?: .+ \(#([1-9][0-9]*)\)",
        subject,
    )
    return match.group(1) if match else None


def git_output(arguments: list[str], cwd: Path | None = None) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=cwd,
        check=True,
        text=True,
        capture_output=True,
    )
    return completed.stdout


def commits_in_range(commit_range: str, cwd: Path | None = None) -> list[str]:
    if ".." in commit_range:
        before, after = commit_range.split("..", 1)
        revision = after if before == ZERO_SHA else commit_range
    else:
        revision = commit_range
    output = git_output(["rev-list", "--reverse", "--no-merges", revision], cwd)
    return [line for line in output.splitlines() if line]


def validate_commit_range(
    commit_range: str,
    policy: dict[str, Any],
    cwd: Path | None = None,
) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    issue_numbers: set[str] = set()
    for commit_sha in commits_in_range(commit_range, cwd):
        message = git_output(["show", "-s", "--format=%B", commit_sha], cwd)
        issue = issue_from_commit(message)
        if issue:
            issue_numbers.add(issue)
        for error in validate_commit(message, policy):
            errors.append(commit_sha[:7] + ": " + error)
    return errors, issue_numbers


def issue_exists(repository: str, issue_number: str, token: str) -> bool:
    request = urllib.request.Request(
        "https://api.github.com/repos/" + repository + "/issues/" + issue_number,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + token,
            "User-Agent": "sdd-git-conventions-validator",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status == 200
    except urllib.error.HTTPError:
        return False
    except urllib.error.URLError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch")
    parser.add_argument("--range", dest="commit_range")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY", ""))
    parser.add_argument("--github-token", default=os.environ.get("GITHUB_TOKEN", ""))
    parser.add_argument("--verify-issues", action="store_true")
    args = parser.parse_args()

    if not args.branch and not args.commit_range:
        parser.error("Provide --branch, --range, or both.")

    policy = load_policy(args.config)
    errors: list[str] = []
    issues: set[str] = set()

    if args.branch:
        issues.add(issue_from_branch(args.branch) or "")
        errors.extend("branch " + args.branch + ": " + error for error in validate_branch(args.branch, policy))
    if args.commit_range:
        range_errors, range_issues = validate_commit_range(args.commit_range, policy)
        errors.extend(range_errors)
        issues.update(range_issues)

    issues.discard("")
    if args.verify_issues:
        if not args.repository or not args.github_token:
            errors.append("Issue verification requires repository and GitHub token.")
        else:
            for issue_number in sorted(issues, key=int):
                if not issue_exists(args.repository, issue_number, args.github_token):
                    errors.append("Issue #" + issue_number + " does not exist or cannot be read.")

    if errors:
        for error in errors:
            print("ERROR: " + error)
        return 1
    print("Git convention validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
