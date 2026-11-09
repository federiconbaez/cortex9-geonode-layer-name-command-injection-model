# cortex9-geonode-layer-name-command-injection-model

Modelo offline e inerte de **CVE-2026-33050** (GHSA-9fpx-fr6j-2vh6,
CWE-78). GeoNode armaba la cadena de opciones de `ogr2ogr` sin citar
`alternate` / `original_name`, hacía `options.split(" ")` y
`Popen(..., shell=True)`. El fix, commit
`1408290c0bb54872924a9b334a516db9758a2180` (en **5.1.0**), usa
`shlex.quote`, `shlex.split` y `shell=False`. Ver
[evidence/fix-in-5.1.0.md](evidence/fix-in-5.1.0.md).

Inglés: [README.md](README.md). Ejercicios: [PRACTICE.md](PRACTICE.md).

## Citas de líneas

Cada cita tiene la forma `<tag>:L<n>` o `<tag>:L<n>-<m>`: la línea real de
`cat -n` del diff upstream del fix. El diff **no** está en este repo
(licencia upstream: GPL-2.0-or-later); `sources/diffs.tsv` lo identifica:

- `1408290c` → `CVE-2026-33050_geonode_1408290c0bb5.diff`, SHA-256 `e5fd1609d53c12daecad10d6729acaf4fe477a6a2ed808eccf2e1fafb018ebed`,
  https://github.com/GeoNode/geonode/commit/1408290c0bb54872924a9b334a516db9758a2180.diff

`citations.tsv` es la tabla única de rangos citados; para cada rango guarda
el SHA-256 del texto citado (líneas `start`..`end` del diff tal cual, unidas
con `\n`, sin salto final, UTF-8). Para verificarlo: descargar el diff de la
URL, comprobar su SHA-256 y correr
`C9_DIFF=<ruta> PYTHONPATH=src python3 -m unittest -v tests.test_citations`.
Sin `C9_DIFF` (como en CI) se comprueba el formato, que toda cita esté en la
tabla y que ninguna falte de tag, y el chequeo de contenido sale como
**skip** explícito.

## Uso

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 scripts/derive_expected.py | diff - fixtures/expected.tsv
python3 scripts/gen_results.py /tmp/r && diff -r results /tmp/r
```

Un modelo no es un hallazgo. Ver [LIMITATIONS.md](LIMITATIONS.md) y
[SOURCES.md](SOURCES.md). Licencia: Apache-2.0.
