"""create_ogr2ogr_command / import_with_ogr2ogr of GeoNode, before and after
commit 1408290c0bb54872924a9b334a516db9758a2180 (CVE-2026-33050).

Citations ``1408290c:Lnnn`` are real `cat -n` lines of the
upstream diff CVE-2026-33050_geonode_1408290c0bb5.diff
(not in this repo; URL and sha256 in sources/diffs.tsv; range
hashes in citations.tsv; checked by tests/test_citations.py).

Nothing here runs ogr2ogr or a shell. Pre builds the options string the
old way and splits on spaces (1408290c:L52); post uses shlex.quote +
shlex.split and would pass an argv list with shell=False (1408290c:L41,
1408290c:L65).
"""
from __future__ import annotations

import shlex  # post adds it too: 1408290c:L9

DEFAULT_PK = "fid"  # DEFAULT_PK_COLUMN_NAME stand-in
PRE_RULE = "1408290c:L17-19;1408290c:L52-53"
POST_RULE = "1408290c:L20-22;1408290c:L41;1408290c:L65"


def build_options(version: str, input_file: str, alternate: str,
                  original_name: str) -> str:
    """The fragment of create_ogr2ogr_command that touches the three
    attacker-influenced strings (1408290c:L17-22)."""
    if version == "pre":
        # 1408290c:L17-19 pre
        return (f'"{input_file}"' + f" -lco FID={DEFAULT_PK} "
                + f'-nln {alternate} "{original_name}"')
    if version == "post":
        # 1408290c:L20-22 post
        return (f" {shlex.quote(input_file)} -lco FID={DEFAULT_PK} "
                + f" -nln {shlex.quote(alternate)} {shlex.quote(original_name)}")
    raise ValueError(version)


def tokenize(version: str, options: str) -> list:
    """How the options string becomes argv (1408290c:L52 vs 1408290c:L41)."""
    if version == "pre":
        return options.split(" ")  # 1408290c:L52
    if version == "post":
        return shlex.split(options)  # 1408290c:L41
    raise ValueError(version)


def analyze(version: str, input_file: str, alternate: str,
            original_name: str) -> dict:
    """Return outcome labels without running anything.

    EXTRA_ARGV: split produced more tokens than the safe baseline for the
    same inputs with metacharacters removed.
    SHELL_METACHAR: pre path would have been joined and passed to
    Popen(..., shell=True) (1408290c:L53); post uses shell=False (1408290c:L65).
    """
    options = build_options(version, input_file, alternate, original_name)
    argv = tokenize(version, options)
    # Baseline: same call with metacharacters stripped from the three fields.
    def _safe(s: str) -> str:
        return "".join(c for c in s if c.isalnum() or c in "._/-") or "x"
    base_opts = build_options(version, _safe(input_file),
                              _safe(alternate), _safe(original_name))
    base_argv = tokenize(version, base_opts)
    extra = len(argv) - len(base_argv)
    # Shell metacharacters that matter when the whole command is one string.
    meta = set(";&|`$()<>\n")
    has_meta = any(c in meta for c in alternate + original_name + input_file)
    if version == "pre":
        shell = True  # 1408290c:L53
        outcome = "EXTRA_ARGV" if extra > 0 else (
            "SHELL_METACHAR" if has_meta else "ONE_LAYER")
    else:
        shell = False  # 1408290c:L65
        # After quote+split, metacharacters stay inside a single argv slot.
        outcome = "EXTRA_ARGV" if extra > 0 else "ONE_LAYER"
    return {
        "outcome": outcome,
        "argv": argv,
        "argc": len(argv),
        "extra": extra,
        "shell": shell,
        "options": options,
        "rule": PRE_RULE if version == "pre" else POST_RULE,
    }
