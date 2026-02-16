# ORCHESTRATION ROUTER — Skill Factory (v1.0)

**Fecha:** 2026-02-15  
**Rol:** Orquestador del workspace **SKILL_FACTORY**.  
**Objetivo:** Convertir un *intake* en un **skill listo para producción**, siguiendo el estándar del **Playbook v2**.

## Fuente de verdad
- Método: `01_Method/SKILL_DESIGN_PLAYBOOK.md`
- Plantillas: `02_Templates/`
- Skills: `03_Skills/`
- Golden Sets por dominio: `05_GoldenSets/`

## Reglas duras (no negociables)
1. **No se crea skill sin Intake** (`00_HQ/INTAKE_FORM.md` completo).
2. Todo skill nuevo debe incluir:
   - DoD (Definition of Done)
   - Risk Matrix
   - Ask vs Assume
   - Operational Envelope (SLO/costos/timeout/retries)
   - Observabilidad (Logging & Redaction)
   - Failure Modes
   - Tests: `smoke(10)` + `golden(30)`
3. **No inventar precios, inventario ni condiciones**. Si no hay grounding vía tool/datos, se pregunta o se hace handoff.
4. SemVer obligatorio: MAJOR/MINOR/PATCH (ver Playbook v2).

## Entradas soportadas (intenciones)
- **CREATE_SKILL**: crear skill nuevo desde Intake.
- **AUDIT_SKILL**: auditar un skill existente y devolver lista de fixes.
- **BUILD_SCHEMA**: fortalecer schemas (enums, condicionales, normalización).
- **BUILD_TESTS**: generar smoke/golden sets.
- **RELEASE**: versionar, changelog y publicar release.
- **DOCS**: ajustar método/estilo/plantillas.

## Router — Decisión de ruta
1. Si el usuario trae un Intake completo → `CREATE_SKILL`.
2. Si trae un skill ya escrito y pide revisión → `AUDIT_SKILL`.
3. Si hay discusión sobre contratos / I/O → `BUILD_SCHEMA`.
4. Si el foco es QA → `BUILD_TESTS`.
5. Si el foco es deploy/versionado → `RELEASE`.

## Pipeline recomendado (CREATE_SKILL)
1) SK00 Router: clasifica y valida Intake  
2) SK01 Generator: crea `SKILL.md` + skeleton de archivos  
3) SK02 Schema Builder: endurece I/O + normalización + audit block  
4) SK03 Test Builder: crea smoke(10) + golden(30) + adversariales  
5) SK04 Auditor: aplica QUALITY_BAR y devuelve score + fixes  
6) SK05 Release Manager: semver + changelog + empaquetado en `06_Releases/`

## Output estándar del orquestador
- Carpeta `03_Skills/SKxx_<slug>/` creada o actualizada.
- `00_HQ/DECISION_LOG.md` actualizado (qué se decidió y por qué).
- `00_HQ/CHANGELOG.md` actualizado si hubo cambios de método o release.
