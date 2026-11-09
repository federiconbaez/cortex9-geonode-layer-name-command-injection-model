# Limitations

- **Options fragment only.** Only the three fields in
  `create_ogr2ogr_command` (1408290c:L17-22) and the tokenize / `shell=` choice
  (1408290c:L41, 1408290c:L52-53, 1408290c:L65) are modelled. The `OGR2OGR_COPY_WITH_DUMP` pipe
  branch (1408290c:L45-62) and datastore credentials are out of scope.
- **Not ogr2ogr.** Nothing is executed. `SHELL_METACHAR` means "pre would
  have passed this string to a shell", not that a command ran.
- **o01** (quoted path with spaces still splits pre) is a **model
  observation**, not verified as a separate advisory finding.
- **DEFAULT_PK_COLUMN_NAME** is modelled as the stand-in `fid`.
- This is not a finding and not an exploit. The only command name in
  fixtures is the inert marker `id`.
