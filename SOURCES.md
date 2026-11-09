# Sources

Local copies under `security-research-45/sources/cve2026/`. SHA-256
re-verified against `sources/cve2026/SHA256SUMS`. Line citations: see
"Line citations" below.

| Source | URL | Used for | SHA-256 |
|---|---|---|---|
| Commit 1408290c0bb54872924a9b334a516db9758a2180 (2026-02-27) as `diffs/CVE-2026-33050_geonode_1408290c0bb5.diff` | https://github.com/GeoNode/geonode/commit/1408290c0bb54872924a9b334a516db9758a2180 | pre 1408290c:L17-19, 1408290c:L52-53; post 1408290c:L20-22, 1408290c:L41, 1408290c:L65; pipe branch 1408290c:L45-62 (out of scope) | e5fd1609d53c12daecad10d6729acaf4fe477a6a2ed808eccf2e1fafb018ebed |
| GHSA-9fpx-fr6j-2vh6 | https://github.com/GeoNode/geonode/security/advisories/GHSA-9fpx-fr6j-2vh6 | affected <5.1.0, patched 5.1.0, CWE-78 | 7591816809aafa357bbcfba073b8dbc58564f888de1718f45b65f6c3bd9214f5 |
| NVD CVE-2026-33050 (Awaiting Analysis) | https://nvd.nist.gov/vuln/detail/CVE-2026-33050 | CVE exists; fixed in 5.1.0 | 0baf23c6753bed92ed0f514657eab0189a60c60cc6342e47783c7843c30d6c30 |
| cve.org (PUBLISHED) | https://www.cve.org/CVERecord?id=CVE-2026-33050 | PUBLISHED; <5.1.0 | 5212d4c731a005eefd2ec596b54080a380831ae1d361b7c43202b99c12e8a5a2 |
| Compare API, 2026-11-09 | see evidence/fix-in-5.1.0.md | fix in 5.1.0 | see that file |

## Line citations (diff not in this repo)

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

