---
name: <snake_case>
title: <Verbo + Objeto>
version: 1.0.0
owner: <email o team>
status: draft | active | deprecated
last_reviewed: YYYY-MM-DD
domain: <tourism|insurance|ecommerce|...>
dependencies:
  tools:
    - <tool_name>
  schemas:
    - <schema_name>
---

# 1) Propósito
Qué hace y qué NO hace.

# 2) Definition of Done (DoD)
- Golden set pass rate: >= __/30
- 0 fallas críticas (alucinación de precio/inventario/condiciones)
- p95 latency <= __s, timeout <= __s
- Salida válida contra schema en 100% de ejecuciones

# 3) Interface — Contrato
## 3.1 Input Schema
Ver `schema.input.json`

## 3.2 Output Schema
Ver `schema.output.json`

## 3.3 Artifact Skeletons
(Define esqueletos base para archivos generados: YAML, Rego, SQL, MD)
*   **[filename]**: `content_skeleton`

# 4) Política “Ask vs Assume”
Never assume: fechas, pax, moneda, cancelación, documentación.  
Thresholds: confidence < 0.75 => pregunta; < 0.55 => handoff.

# 5) Procedure
1) Validar inputs
2) **Check Tech Radar** (Validar contra lista de adopt/hold/retire)
3) Normalizar
4) Ejecutar tools
5) Verificar (consistencia + riesgo)
6) Responder

# 6) Guardrails
## 6.1 Tech Radar & Lifecycle
- (Define aquí qué tecnologías están obsoletas y deben bloquearse)
## 6.2 Constraints
- Prohibiciones absolutas
- Disclaimers obligatorios
- Reglas por riesgo (ver Risk Matrix)

# 7) Risk Matrix
(Ver `risk_matrix.md` o incluir tabla aquí)

# 8) Operational Envelope
- max_tool_calls:
- max_tokens:
- timeout_seconds:
- retry_policy:
- p95_latency_target:

# 9) Observabilidad (Logging & Redaction)
Log sin PII + redacción obligatoria.

# 10) Failure Modes
Señales + mitigación + fallback.

# 11) Tests
- `tests.smoke.json` (10)
- `tests.golden.json` (30)

# 12) Changelog
- 1.0.0: initial
