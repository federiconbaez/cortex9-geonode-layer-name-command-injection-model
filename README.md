# cortex9-geonode-layer-name-command-injection-model

Offline, inert model of **CVE-2026-33050** (GHSA-9fpx-fr6j-2vh6, CWE-78).
GeoNode built an `ogr2ogr` options string with unquoted `alternate` /
`original_name` (and a naively quoted `input_file`), then did
`options.split(" ")` and `Popen(..., shell=True)` (1408290c:L17-19, 1408290c:L52-53).
A crafted vector layer name could inject shell syntax. The fix, commit
`1408290c0bb54872924a9b334a516db9758a2180` (in **5.1.0** — see
[evidence/fix-in-5.1.0.md](evidence/fix-in-5.1.0.md)), wraps the three
fields with `shlex.quote`, splits with `shlex.split` and runs with
`shell=False` (1408290c:L20-22, 1408290c:L41, 1408290c:L65).

Spanish: [README.es.md](README.es.md). Exercises: [PRACTICE.md](PRACTICE.md).

## The model

- `src/c9geonode/ogr.py`: builds the options fragment pre/post, tokenizes
  it the same way the two versions do, and labels the result. **ogr2ogr
  and shells are never executed**; tests patch `subprocess.Popen`.
- Outcomes: `EXTRA_ARGV` (split produced more tokens), `SHELL_METACHAR`
  (pre: metacharacters under `shell=True` even if argc is unchanged),
  `ONE_LAYER` (safe).

## Differential evidence (`results/summary.csv`)

| Class | n | pre | post |
|---|---|---|---|
| pos | 7 | 5 `SHELL_METACHAR`, 2 `EXTRA_ARGV` | 7 `ONE_LAYER` |
| neg | 2 | `ONE_LAYER` | `ONE_LAYER` |
| observation | 1 | `EXTRA_ARGV` (quoted path with spaces) | `ONE_LAYER` |

`o01` is a **model observation**: pre puts quotes around `input_file` then
splits on spaces, so a path with spaces still breaks. Not a separate finding.

## Line citations

Every line citation has the form `<tag>:L<n>` or `<tag>:L<n>-<m>`: the real
`cat -n` line(s) of the upstream fix diff. The diff is **not** included in
this repo (upstream license: GPL-2.0-or-later); `sources/diffs.tsv` names it:

- `1408290c` → `CVE-2026-33050_geonode_1408290c0bb5.diff`, SHA-256 `e5fd1609d53c12daecad10d6729acaf4fe477a6a2ed808eccf2e1fafb018ebed`,
  https://github.com/GeoNode/geonode/commit/1408290c0bb54872924a9b334a516db9758a2180.diff

`citations.tsv` is the single table of cited ranges; for each range it
stores the SHA-256 of the cited text (lines `start`..`end` of the diff file
exactly as stored, joined with `\n`, no final newline, UTF-8; shell:
`sed -n "${start},${end}p" "$C9_DIFF" | head -c -1 | sha256sum`).

```sh
curl -fsSL -o /tmp/CVE-2026-33050_geonode_1408290c0bb5.diff https://github.com/GeoNode/geonode/commit/1408290c0bb54872924a9b334a516db9758a2180.diff
sha256sum /tmp/CVE-2026-33050_geonode_1408290c0bb5.diff   # must be e5fd1609d53c12daecad10d6729acaf4fe477a6a2ed808eccf2e1fafb018ebed
C9_DIFF=/tmp/CVE-2026-33050_geonode_1408290c0bb5.diff PYTHONPATH=src python3 -m unittest -v tests.test_citations
```

Without `C9_DIFF` (as in CI) `tests/test_citations.py` checks the table
format, that every citation in the repo is in the table and that none lacks
a tag, and reports the content check as an explicit **skip**.

## Run

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 scripts/derive_expected.py | diff - fixtures/expected.tsv
python3 scripts/gen_results.py /tmp/r && diff -r results /tmp/r
```

A model is not a finding. See [LIMITATIONS.md](LIMITATIONS.md) and
[SOURCES.md](SOURCES.md). License: Apache-2.0.
