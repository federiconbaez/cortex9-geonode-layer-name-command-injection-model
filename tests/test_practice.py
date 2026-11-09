"""Answers to PRACTICE.md."""
import unittest
from pathlib import Path
from c9geonode import ogr


class Practice(unittest.TestCase):
    def test_level_1_plain(self):
        self.assertEqual(
            ogr.analyze("pre", "/t.shp", "roads", "roads")["outcome"], "ONE_LAYER")

    def test_level_2_semicolon(self):
        self.assertEqual(
            ogr.analyze("pre", "/t.shp", "x;id", "layer")["outcome"],
            "SHELL_METACHAR")

    def test_level_3_post_quotes(self):
        r = ogr.analyze("post", "/t.shp", "x;id", "layer")
        self.assertEqual(r["outcome"], "ONE_LAYER")
        self.assertFalse(r["shell"])

    def test_level_4_space_extra_argv(self):
        self.assertEqual(
            ogr.analyze("pre", "/t.shp", "my layer", "layer")["outcome"],
            "EXTRA_ARGV")

    def test_level_5_shell_flag(self):
        self.assertTrue(ogr.analyze("pre", "/t.shp", "a", "b")["shell"])
        self.assertFalse(ogr.analyze("post", "/t.shp", "a", "b")["shell"])

    def test_level_6_observation(self):
        text = Path("LIMITATIONS.md").read_text(encoding="utf-8")
        self.assertIn("o01", text)


if __name__ == "__main__":
    unittest.main()
