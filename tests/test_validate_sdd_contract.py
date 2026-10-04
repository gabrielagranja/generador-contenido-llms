from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_sdd_contract import validate_change, validate_root


class ContractValidatorTests(unittest.TestCase):
    def test_valid_fixture_passes(self) -> None:
        errors = validate_change(ROOT / "tests" / "fixtures" / "contracts" / "valid-contract")
        self.assertEqual(errors, [])

    def test_invalid_fixture_fails(self) -> None:
        errors = validate_change(ROOT / "tests" / "fixtures" / "contracts" / "invalid-contract")
        self.assertTrue(errors)
        self.assertTrue(any("missing Issue reference" in error for error in errors))
        self.assertTrue(any("completed task requires Approved status" in error for error in errors))

    def test_archive_directory_is_ignored(self) -> None:
        fixture_root = ROOT / "tests" / "fixtures" / "contracts"
        with tempfile.TemporaryDirectory() as directory:
            changes_root = Path(directory)
            shutil.copytree(fixture_root / "valid-contract", changes_root / "active-change")
            shutil.copytree(
                fixture_root / "invalid-contract",
                changes_root / "archive" / "2026-10-04-completed-change",
            )
            self.assertEqual(validate_root(changes_root), [])

    def test_invalid_active_change_is_not_ignored_with_archive(self) -> None:
        fixture_root = ROOT / "tests" / "fixtures" / "contracts"
        with tempfile.TemporaryDirectory() as directory:
            changes_root = Path(directory)
            shutil.copytree(fixture_root / "invalid-contract", changes_root / "active-change")
            shutil.copytree(
                fixture_root / "valid-contract",
                changes_root / "archive" / "2026-10-04-completed-change",
            )
            errors = validate_root(changes_root)
            self.assertTrue(any("active-change: missing Issue reference" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
