"""Regression-test the real final validator gate without running KiCad."""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest

SOURCE = Path(__file__).with_name("validate_pcb.py")
GATE = compile(ast.Module(body=[ast.parse(SOURCE.read_text()).body[-1]], type_ignores=[]), str(SOURCE), "exec")

class DraftGateTests(unittest.TestCase):
    def result(self, draft=True, errs=None, viol=None, unconn=None):
        try:
            exec(GATE, {"args": SimpleNamespace(draft=draft), "errs": errs or [], "viol": viol or [], "unconn": unconn or []})
        except SystemExit as error:
            return error.code
        return 0

    def test_clean_passes(self):
        self.assertEqual(self.result(), 0)
        self.assertEqual(self.result(draft=False), 0)

    def test_only_draft_permits_unconnected(self):
        self.assertEqual(self.result(unconn=[{}]), 0)
        self.assertEqual(self.result(draft=False, unconn=[{}]), 1)

    def test_drc_always_fails(self):
        for draft in (True, False):
            for kind in ("shorting_items", "clearance"):
                with self.subTest(draft=draft, kind=kind):
                    self.assertEqual(self.result(draft=draft, viol=[{"type": kind}]), 1)

    def test_structural_error_always_fails(self):
        for draft in (True, False):
            self.assertEqual(self.result(draft=draft, errs=["net mismatch"]), 1)

if __name__ == "__main__":
    unittest.main()
