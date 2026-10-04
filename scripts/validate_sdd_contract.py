#!/usr/bin/env python3
"""Validate deterministic minimum fields for active OpenSpec changes."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = (
    "Status and human approval",
    "Plan objective",
    "Objective",
    "Scope",
    "Acceptance criteria",
    "Rubric",
    "Tests and verification",
    "Open questions and blockers",
    "Approval",
)
PLACEHOLDER_PATTERN = re.compile(r"\b(TODO|TBD)\b|<[^>]+>|\[insert[^\]]*\]", re.IGNORECASE)
TASK_DONE_PATTERN = re.compile(r"^- \[[xX]\]", re.MULTILINE)
STATUS_PATTERN = re.compile(r"^- Status:\s*(Pending|Approved|Rejected)\s*$", re.MULTILINE)
ISSUE_PATTERN = re.compile(r"#\d+")


def section_body(text: str, heading: str) -> str:
    match = re.search(r"^## " + re.escape(heading) + r"\s*$", text, re.MULTILINE)
    if not match:
        return ""
    next_heading = re.search(r"^## ", text[match.end():], re.MULTILINE)
    end = match.end() + next_heading.start() if next_heading else len(text)
    return text[match.end():end].strip()


def validate_change(change_dir: Path) -> list[str]:
    errors: list[str] = []
    proposal_path = change_dir / "proposal.md"
    design_path = change_dir / "design.md"
    tasks_path = change_dir / "tasks.md"

    for path in (proposal_path, design_path, tasks_path):
        if not path.is_file():
            errors.append(change_dir.name + ": missing " + path.name)

    if not proposal_path.is_file():
        return errors

    proposal = proposal_path.read_text(encoding="utf-8")
    for heading in REQUIRED_SECTIONS:
        body = section_body(proposal, heading)
        if not body:
            errors.append(change_dir.name + ": missing or empty section " + heading)
        elif PLACEHOLDER_PATTERN.search(body):
            errors.append(change_dir.name + ": unresolved placeholder in " + heading)

    status_match = STATUS_PATTERN.search(section_body(proposal, "Status and human approval"))
    if not status_match:
        errors.append(change_dir.name + ": status must be Pending, Approved or Rejected")
        status = ""
    else:
        status = status_match.group(1)

    if not ISSUE_PATTERN.search(section_body(proposal, "Status and human approval")):
        errors.append(change_dir.name + ": missing Issue reference")

    rubric = section_body(proposal, "Rubric")
    if rubric and "No aplica" not in rubric and len(rubric.split()) < 3:
        errors.append(change_dir.name + ": rubric must name a criterion or state No aplica with a reason")

    specs_root = change_dir / "specs"
    spec_files = list(specs_root.glob("*/spec.md")) if specs_root.is_dir() else []
    if not spec_files:
        errors.append(change_dir.name + ": missing canonical delta spec at specs/<capability>/spec.md")
    for spec_path in spec_files:
        spec = spec_path.read_text(encoding="utf-8")
        if not re.search(r"^## (ADDED|MODIFIED|REMOVED) Requirements", spec, re.MULTILINE):
            errors.append(change_dir.name + ": " + str(spec_path.relative_to(change_dir)) + " lacks delta classification")
        for token in ("SHALL", "MUST", "GIVEN", "WHEN", "THEN"):
            if token not in spec:
                errors.append(change_dir.name + ": " + str(spec_path.relative_to(change_dir)) + " lacks " + token)

    if tasks_path.is_file() and status != "Approved":
        tasks = tasks_path.read_text(encoding="utf-8")
        if TASK_DONE_PATTERN.search(tasks):
            errors.append(change_dir.name + ": completed task requires Approved status")

    return errors


def validate_root(changes_root: Path) -> list[str]:
    if not changes_root.is_dir():
        return ["changes directory does not exist: " + str(changes_root)]
    errors: list[str] = []
    for change_dir in sorted(changes_root.iterdir()):
        if not change_dir.is_dir() or change_dir.name.startswith("."):
            continue
        if change_dir.name == "archive":
            continue
        if change_dir.name == "README.md":
            continue
        errors.extend(validate_change(change_dir))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--changes-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "openspec" / "changes",
    )
    args = parser.parse_args()
    errors = validate_root(args.changes_dir)
    if errors:
        for error in errors:
            print("ERROR: " + error)
        return 1
    print("SDD contract validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
