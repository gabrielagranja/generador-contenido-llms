from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_sdd_contract import validate_change


class ContractValidatorTests(unittest.TestCase):
    def test_valid_fixture_passes(self) -> None:
        errors = validate_change(ROOT / "tests" / "fixtures" / "contracts" / "valid-contract")
        self.assertEqual(errors, [])

    def test_invalid_fixture_fails(self) -> None:
        errors = validate_change(ROOT / "tests" / "fixtures" / "contracts" / "invalid-contract")
        self.assertTrue(errors)
        self.assertTrue(any("missing Issue reference" in error for error in errors))
        self.assertTrue(any("completed task requires Approved status" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
