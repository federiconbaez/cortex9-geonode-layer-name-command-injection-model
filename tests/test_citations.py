"""Every line citation in this repo is checked against the upstream diff.

Citation form everywhere: ``<tag>:L<n>`` or ``<tag>:L<n>-<m>``, where
``<tag>`` is the 8-hex prefix of the fix commit and the numbers are real
``cat -n`` lines of that commit's diff. The diff itself is NOT in this repo
(upstream license); ``sources/diffs.tsv`` gives its URL and SHA-256, and
``citations.tsv`` gives, for every cited range, the SHA-256 of the cited
text.

Normalisation of a range's hash: take lines ``start``..``end`` of the diff
file exactly as stored (no ``cat -n`` number prefix, no stripping, any
trailing whitespace kept), join them with ``\\n``, no final newline, and hash
the UTF-8 bytes. Shell equivalent::

    sed -n "${start},${end}p" "$C9_DIFF" | head -c -1 | sha256sum

Always checked (CI): table format, every citation in src/docs/tests/results
is in the table, no untagged ``L<n>``. Content check (diff SHA-256 and every
range hash) runs only when ``C9_DIFF`` names an existing file; otherwise it is
reported as an explicit skip.
"""
import csv
import hashlib
import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAGGED = re.compile(r"\b([0-9a-f]{8}):L(\d+)(?:-(\d+))?\b")
BARE = re.compile(r"\bL\d+\b")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SKIP_DIRS = {".git", "sources", "__pycache__", "node_modules"}
SKIP_FILES = {"LICENSE", "test_citations.py", "test_citations.js"}
TEXT_EXT = {".py", ".js", ".md", ".json", ".csv", ".tsv", ".yml", ".toml",
            ".txt", ""}


def _read_tsv(path: Path) -> list:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


DIFFS = {r["tag"]: r for r in _read_tsv(ROOT / "sources/diffs.tsv")}
ROWS = _read_tsv(ROOT / "citations.tsv")
TABLE = {(r["tag"], int(r["start"]), int(r["end"])) for r in ROWS}


def range_sha256(lines: list, start: int, end: int) -> str:
    return hashlib.sha256(
        "\n".join(lines[start - 1:end]).encode("utf-8")).hexdigest()


def _tracked_text_files():
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or any(part in SKIP_DIRS for part in
                                  p.relative_to(ROOT).parts):
            continue
        if p.name in SKIP_FILES or p.suffix not in TEXT_EXT:
            continue
        yield p


class CitationTable(unittest.TestCase):
    def test_tables_are_well_formed(self):
        self.assertTrue(DIFFS)
        for tag, r in DIFFS.items():
            self.assertRegex(tag, r"^[0-9a-f]{8}$")
            self.assertRegex(r["sha256"], HEX64)
            self.assertRegex(r["url"], rf"^https://github\.com/.+/commit/{tag}[0-9a-f]{{32}}\.diff$")
            self.assertFalse((ROOT / "sources" / r["file"]).exists(),
                             "the upstream diff must not be committed")
        self.assertTrue(ROWS)
        self.assertEqual(len(TABLE), len(ROWS), "duplicate range")
        for r in ROWS:
            self.assertIn(r["tag"], DIFFS)
            self.assertTrue(1 <= int(r["start"]) <= int(r["end"]))
            self.assertRegex(r["sha256"], HEX64)
            self.assertTrue(r["what"].strip())

    def test_every_citation_in_the_repo_is_in_the_table(self):
        seen = 0
        for p in _tracked_text_files():
            text = p.read_text(encoding="utf-8")
            for m in TAGGED.finditer(text):
                tag, a = m.group(1), int(m.group(2))
                b = int(m.group(3) or a)
                seen += 1
                with self.subTest(file=str(p.relative_to(ROOT)), cite=m.group(0)):
                    self.assertIn((tag, a, b), TABLE)
            for m in BARE.finditer(TAGGED.sub("", text)):
                self.fail(f"{p.relative_to(ROOT)}: untagged citation {m.group(0)}")
        self.assertGreater(seen, 0)


class CitationContent(unittest.TestCase):
    def test_cited_ranges_match_the_upstream_diff(self):
        path = os.environ.get("C9_DIFF", "")
        if not path or not Path(path).is_file():
            self.skipTest(
                "content check SKIPPED: C9_DIFF is "
                + (f"'{path}', not an existing file" if path else "not set")
                + "; download the diff from the URL in sources/diffs.tsv and "
                "run with C9_DIFF=<path> to verify the diff SHA-256 and every "
                "cited range")
        data = Path(path).read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        tags = [t for t, r in DIFFS.items() if r["sha256"] == sha]
        self.assertEqual(len(tags), 1, f"C9_DIFF sha256 {sha} matches no diff")
        lines = data.decode("utf-8").split("\n")
        n = len(lines) - 1 if lines and lines[-1] == "" else len(lines)
        rows = [r for r in ROWS if r["tag"] == tags[0]]
        self.assertTrue(rows)
        for r in rows:
            a, b = int(r["start"]), int(r["end"])
            with self.subTest(cite=f"{r['tag']}:L{a}-{b}"):
                self.assertLessEqual(b, n, f"range past end ({n} lines)")
                self.assertEqual(range_sha256(lines, a, b), r["sha256"])


if __name__ == "__main__":
    unittest.main()
