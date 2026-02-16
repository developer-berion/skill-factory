# SKILL_FACTORY

Workspace de Antigravity para **diseñar, auditar y versionar skills** de agentes de IA con estándar de producción.

## Inicio rápido
1) Copia y llena: `00_HQ/INTAKE_FORM.md`
2) Sigue el router: `00_HQ/ORCHESTRATION_ROUTER.md`
3) Método (fuente de verdad): `01_Method/SKILL_DESIGN_PLAYBOOK.md`
4) Plantillas: `02_Templates/skill.template.md`
5) Skills internos (pipeline): `03_Skills/SK00_router` ... `SK05_release_manager`

## Herramientas de Automatización (Nuevo)
Automatiza la creación y validación sin perder robustez:

### 1. Intake & Scaffolding
Crea un **nuevo skill completo** respondiendo preguntas en la terminal (Intake Wizard) y generando todos los archivos base automáticamente.
```bash
python scripts/skill_factory.py create
```

### 2. Validación Continua (Quality Gate)
Verifica que todos los skills cumplan con el **estándar de producción** (existencia de tests, schemas válidos y secciones obligatorias).
```bash
python scripts/validate_skill.py
```

## Calidad
Ver `00_HQ/QUALITY_BAR.md`.

**Fecha de creación:** 2026-02-15
**Última actualización:** 2026-02-16 (Automation Upgrade)
