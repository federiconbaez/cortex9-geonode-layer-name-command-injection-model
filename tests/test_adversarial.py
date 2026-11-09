import ast
import unittest
from unittest import mock
import subprocess

from c9geonode import cases, ogr

ROOT = cases.ROOT


class Adversarial(unittest.TestCase):
    def test_src_never_calls_popen_or_system(self):
        for f in sorted((ROOT / "src/c9geonode").glob("*.py")):
            tree = ast.parse(f.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    fn = node.func
                    name = fn.attr if isinstance(fn, ast.Attribute) else getattr(
                        fn, "id", "")
                    self.assertNotIn(name, {"Popen", "run", "call", "system",
                                            "check_output", "getoutput"})

    def test_running_cases_never_touches_subprocess(self):
        boom = mock.Mock(side_effect=AssertionError("subprocess used"))
        with mock.patch.object(subprocess, "Popen", boom), \
                mock.patch.object(subprocess, "run", boom):
            for c in cases.load():
                for v in ("pre", "post"):
                    cases.run(c, v)
        boom.assert_not_called()

    def test_post_quote_keeps_metachar_in_one_slot(self):
        r = ogr.analyze("post", "/t.shp", "x;id", "layer")
        self.assertEqual(r["outcome"], "ONE_LAYER")
        self.assertIn("x;id", r["argv"])

    def test_pre_shell_true_post_false(self):
        self.assertTrue(ogr.analyze("pre", "/t.shp", "a", "b")["shell"])
        self.assertFalse(ogr.analyze("post", "/t.shp", "a", "b")["shell"])

    def test_unknown_version(self):
        with self.assertRaises(ValueError):
            ogr.build_options("v9", "a", "b", "c")

    def test_deterministic(self):
        a = [cases.run(c, "pre")["outcome"] for c in cases.load()]
        b = [cases.run(c, "pre")["outcome"] for c in cases.load()]
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
