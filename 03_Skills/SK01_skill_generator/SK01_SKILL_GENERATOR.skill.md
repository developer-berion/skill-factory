---
name: sk01_generate_skill
title: Generar skill desde Intake
version: 0.1.0
owner: UNKNOWN
status: draft
last_reviewed: 2026-02-15
domain: general
dependencies:
  tools: []
  schemas: []
---

# 1) Propósito
Genera un skill completo desde INTAKE_FORM y plantillas oficiales.

# 2) Definition of Done (DoD)
- Golden set pass rate: >= 27/30
- 0 fallas críticas (alucinación de precio/inventario/condiciones)
- p95 latency <= 6s, timeout <= 12s
- Salida válida contra schema en 100% de ejecuciones

# 3) Interface — Contrato
- Input: ver `schema.input.json`
- Output: ver `schema.output.json`

# 4) Política “Ask vs Assume”
Never assume: fechas, pax, moneda, cancelación, documentación.  
Thresholds: confidence < 0.75 => pregunta; < 0.55 => handoff.

# 5) Procedure
1) Validar intent + inputs mínimos
2) Normalizar señales
3) Ejecutar ruta
4) Verificar consistencia
5) Responder con status + audit

# 6) Guardrails
- No inventar datos no soportados por evidencia.
- Si faltan datos críticos: `needs_clarification`.

# 7) Risk Matrix
| Riesgo | Trigger | Mitigación | Acción |
|---|---|---|---|
| Reputacional | responder sin contexto | pedir clarificación | needs_clarification |

# 8) Operational Envelope
- max_tool_calls: 0
- max_tokens: 1200
- timeout_seconds: 12
- retry_policy: {max_retries: 0, backoff: "none"}
- p95_latency_target: 6

# 9) Observabilidad (Logging & Redaction)
- Log: request_id, skill_version, status, handoff_reason
- Redact: PII si aparece en raw_text

# 10) Failure Modes
- Ambigüedad → preguntar.
- Loop → handoff.

# 11) Tests
- `tests.smoke.json`
- `tests.golden.json`

# 12) Changelog
- 0.1.0: skeleton
