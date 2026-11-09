import unittest
from c9geonode import cases

DATA = cases.load()
EXPECTED = {}
for line in (cases.ROOT / "fixtures/expected.tsv").read_text(
        encoding="utf-8").splitlines()[1:]:
    cid, ver, outcome = line.split("\t")
    EXPECTED[(cid, ver)] = outcome


class Fixtures(unittest.TestCase):
    def test_expected_covers_everything(self):
        self.assertEqual(len(EXPECTED), len(DATA) * 2)

    def test_model_derivation_and_hand_labels_agree(self):
        for c in DATA:
            for v in ("pre", "post"):
                with self.subTest(case=c["id"], version=v):
                    got = cases.run(c, v)["outcome"]
                    self.assertEqual(got, EXPECTED[(c["id"], v)])
                    self.assertEqual(got, c["expected"][v])

    def test_acceptance_pos_flip(self):
        for c in DATA:
            if c["class"] != "pos":
                continue
            self.assertNotEqual(cases.run(c, "pre")["outcome"], "ONE_LAYER", c["id"])
            self.assertEqual(cases.run(c, "post")["outcome"], "ONE_LAYER", c["id"])
            self.assertTrue(cases.run(c, "pre")["shell"])
            self.assertFalse(cases.run(c, "post")["shell"])

    def test_acceptance_negatives_identical(self):
        for c in DATA:
            if c["class"] != "neg":
                continue
            self.assertEqual(cases.run(c, "pre")["outcome"], "ONE_LAYER", c["id"])
            self.assertEqual(cases.run(c, "post")["outcome"], "ONE_LAYER", c["id"])


if __name__ == "__main__":
    unittest.main()
