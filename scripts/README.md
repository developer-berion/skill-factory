# Skill Factory Tools
Esta carpeta contiene herramientas para automatizar el ciclo de vida de un Skill en producción.

## 1. Skill Factory (`skill_factory.py`)
Genera la estructura de carpetas y archivos para un nuevo skill de manera interactiva.
Automatiza el **Intake**.

### Uso:
```bash
python scripts/skill_factory.py create
```

Esto lanzará un wizard que preguntará:
- Nombre del skill
- Dominio
- Descripción
- Parámetros operativos

Y creará:
- Carpeta `SKxx_<name>`
- `*.skill.md` con los datos llenos
- `schema.input.json` y `schema.output.json`
- `tests.smoke.json` y `tests.golden.json` (vacíos pero listos)
- `risk_matrix.md`

## 2. Validator (`validate_skill.py`)
Valida que un skill cumpla con el estándar de calidad (Quality Bar).

### Uso:
```bash
# Validar todos los skills
python scripts/validate_skill.py

# Validar un skill específico
python scripts/validate_skill.py SK05_release_manager
```

Chequeos que realiza:
- Exisencia de schemas JSON válidos.
- Existencia de tests mínimos (Smoke >= 10, Golden >= 30 casos - *configurable*).
- Estructura correcta del Markdown (secciones obligatorias: DoD, Risk Matrix, etc).

## Próximos pasos (Roadmap)
- `run_tests.py`: Ejecutor de tests contra LLMs reales (requiere API key).
- `generate_schema.py`: Generador de JSON Schema a partir de descripción en lenguaje natural.
