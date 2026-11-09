#!/usr/bin/env python3
"""Regenerate results/ deterministically: python scripts/gen_results.py OUT."""
import csv
import hashlib
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from c9geonode import cases


def main(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(("id", "class", "version", "outcome", "argc", "extra", "shell",
                "rule", "argv_json"))
    summary = {}
    for c in cases.load():
        for ver in ("pre", "post"):
            r = cases.run(c, ver)
            w.writerow((c["id"], c["class"], ver, r["outcome"], r["argc"],
                        r["extra"], r["shell"], r["rule"],
                        json.dumps(r["argv"])))
            key = (c["class"], ver, r["outcome"])
            summary[key] = summary.get(key, 0) + 1
    (out / "cases.csv").write_text(buf.getvalue(), encoding="utf-8")
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(("class", "version", "outcome", "n"))
    for key in sorted(summary):
        w.writerow((*key, summary[key]))
    (out / "summary.csv").write_text(buf.getvalue(), encoding="utf-8")
    sums = [f"{hashlib.sha256((out / n).read_bytes()).hexdigest()}  {n}"
            for n in ("cases.csv", "summary.csv")]
    (out / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: gen_results.py OUTDIR")
    main(Path(sys.argv[1]))
