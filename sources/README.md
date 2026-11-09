# sources/

The upstream diff behind every line citation is **not** in this repo: it
belongs to GeoNode/geonode (Copyright (C) 2014–present Open Source Geospatial Foundation; 2001-2014 OpenPlans) and is under that project's license (GPL-2.0-or-later), not this
repo's Apache-2.0. This directory only holds `diffs.tsv`: tag, file name,
SHA-256 and upstream URL of the diff.

Fetch it read-only and run the content check:

```sh
curl -fsSL -o /tmp/CVE-2026-33050_geonode_1408290c0bb5.diff https://github.com/GeoNode/geonode/commit/1408290c0bb54872924a9b334a516db9758a2180.diff
sha256sum /tmp/CVE-2026-33050_geonode_1408290c0bb5.diff   # must be e5fd1609d53c12daecad10d6729acaf4fe477a6a2ed808eccf2e1fafb018ebed
C9_DIFF=/tmp/CVE-2026-33050_geonode_1408290c0bb5.diff PYTHONPATH=src python3 -m unittest -v tests.test_citations
```

The URL above returned a byte-identical file (same SHA-256) on 2026-11-09.
Range hashes in `../citations.tsv` use this normalisation: lines
`start`..`end` of the diff exactly as stored (no `cat -n` prefix, nothing
stripped), joined with `\n`, no final newline, UTF-8 bytes, SHA-256.
