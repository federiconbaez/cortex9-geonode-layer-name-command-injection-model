# Guía práctica (6 niveles)

Ejercicios **offline**. No se ejecuta ogr2ogr ni ninguna shell. Si quieres
ver GeoNode real, hazlo en una VM tuya con un shapefile de laboratorio.
Respuestas en `tests/test_practice.py`.

Ayuda: `PYTHONPATH=src python3 -c "from c9geonode import ogr; print(ogr.analyze('pre','/t.shp','x;id','layer'))"`.

**Básico**

1. **Nombre sano.** `roads`. (`ONE_LAYER`)
2. **Punto y coma.** `x;id` en pre. (`SHELL_METACHAR` — shell=True)

**Intermedio**

3. **El fix.** Lo mismo en post. (`ONE_LAYER`, shell=False, 1408290c:L65)
4. **Espacios.** `my layer` en alternate, pre. (`EXTRA_ARGV`)

**Avanzado**

5. **`shell=True` vs `False`.** ¿Por qué `$(id)` no aumenta argc en pre
   pero igual es peligroso?
6. **Observación o01.** ¿Por qué un path entre comillas con espacios
   sigue rompiéndose en pre?

Más allá: agrega un caso a `fixtures/cases.json` y regenera expected.tsv.
