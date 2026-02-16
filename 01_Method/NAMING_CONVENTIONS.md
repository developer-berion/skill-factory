# Naming Conventions — Skill Factory

## Directorios
- Skills: `03_Skills/SK##_<slug>/`
- Releases: `06_Releases/vX.Y.Z/`
- Golden sets: `05_GoldenSets/<domain>/`

## Archivos por skill (estándar)
- Principal: `SK##_XXXX.skill.md`
- Schemas: `schema.input.json`, `schema.output.json`
- Tests: `tests.smoke.json`, `tests.golden.json`
- (Opcional) `README.md` del skill, ejemplos y fixtures.

## Slug rules
- snake_case, sin acentos, sin espacios.
- Verbos en infinitivo para títulos: “Consultar disponibilidad”, “Normalizar pasajeros”.

## Versionado (SemVer)
- MAJOR: cambia schema/contrato
- MINOR: agrega capacidades compatibles
- PATCH: copy/bugfix sin contrato
