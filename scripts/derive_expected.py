"""Independent expectations for fixtures/cases.json.

Does not import src/. Rebuilds the options string and counts tokens with
str.split vs a minimal POSIX-ish splitter, and flags shell metacharacters.
Prints fixtures/expected.tsv. Python 3.10+ standard library only.
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PK = "fid"
META = set(";&|`$()<>\n")


def quote_posix(s: str) -> str:
    """Minimal single-quote form of shlex.quote."""
    return "'" + s.replace("'", "'\"'\"'") + "'"


def options(version: str, inp: str, alt: str, orig: str) -> str:
    if version == "pre":
        return f'"{inp}"' + f" -lco FID={PK} " + f'-nln {alt} "{orig}"'
    return (f" {quote_posix(inp)} -lco FID={PK} "
            + f" -nln {quote_posix(alt)} {quote_posix(orig)}")


def split_pre(s: str) -> list:
    return s.split(" ")


def split_post(s: str) -> list:
    """Minimal single-quote-aware split (no escapes beyond quote toggling)."""
    out, cur, q, i = [], [], None, 0
    while i < len(s):
        c = s[i]
        if q:
            if c == q:
                q = None
            else:
                cur.append(c)
        elif c in "'\"":
            q = c
        elif c == " ":
            out.append("".join(cur))
            cur = []
        else:
            cur.append(c)
        i += 1
    out.append("".join(cur))
    return [t for t in out if t != ""]


def safe(s: str) -> str:
    return "".join(c for c in s if c.isalnum() or c in "._/-") or "x"


def decide(case: dict, version: str) -> str:
    inp, alt, orig = case["input_file"], case["alternate"], case["original_name"]
    opts = options(version, inp, alt, orig)
    argv = split_pre(opts) if version == "pre" else split_post(opts)
    base = options(version, safe(inp), safe(alt), safe(orig))
    base_argv = split_pre(base) if version == "pre" else split_post(base)
    extra = len(argv) - len(base_argv)
    has_meta = any(c in META for c in alt + orig + inp)
    if version == "pre":
        if extra > 0:
            return "EXTRA_ARGV"
        if has_meta:
            return "SHELL_METACHAR"
        return "ONE_LAYER"
    return "EXTRA_ARGV" if extra > 0 else "ONE_LAYER"


def main() -> None:
    data = json.loads((ROOT / "fixtures/cases.json").read_text(encoding="utf-8"))
    print("id\tversion\toutcome")
    for case in data["cases"]:
        for ver in ("pre", "post"):
            print(f"{case['id']}\t{ver}\t{decide(case, ver)}")


if __name__ == "__main__":
    main()
