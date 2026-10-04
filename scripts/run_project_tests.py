#!/usr/bin/env python3
"""Run the explicitly configured application test command, if present."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / ".github" / "sdd-harness.yml"


def configured_command() -> str:
    if not CONFIG.is_file():
        return ""
    text = CONFIG.read_text(encoding="utf-8")
    match = re.search(r"^\s*command:\s*[\"']?(.*?)[\"']?\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def main() -> int:
    command = configured_command()
    if not command:
        print("::warning title=Application tests not configured::Set tests.command in .github/sdd-harness.yml before claiming application-test coverage.")
        print("Application tests skipped: no explicit command configured.")
        return 0
    print("Running configured application tests: " + command)
    return subprocess.run(command, cwd=ROOT, shell=True, check=False).returncode


if __name__ == "__main__":
    sys.exit(main())
