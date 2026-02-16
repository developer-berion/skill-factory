# QUALITY BAR — Skill Factory (v1.0)

Esta barra define el **mínimo aceptable** para marcar un skill como `active`.

## A) Criterios “Stop the line” (cero tolerancia)
Si ocurre cualquiera, el skill NO pasa:
- Alucinación de precio/inventario/condiciones.
- Output inválido contra schema.
- Filtración de datos sensibles (PII) en logs o output_public.
- Promesas prohibidas (“garantizado”, “100% seguro”) en dominios de riesgo.

## B) Definition of Done (DoD) mínima
- DoD explícito dentro del skill.
- Risk Matrix completa.
- Ask vs Assume definida (never assume + thresholds).
- Operational Envelope definido.
- Observabilidad: logging & redaction.
- Failure modes con mitigación + fallback.
- Tests: smoke(10) + golden(30).
- Golden set pass rate: **>= 27/30**.
- Rúbrica promedio: **>= 4.0** y **0 casos score 0**.

## C) Rúbrica 0–5 (resumen)
- 0: crítico (inventó algo de alto riesgo)
- 1: inválido/no usable
- 2: operativo pero frágil
- 3: pasable
- 4: bueno (auditables, claro)
- 5: golden (maneja edge cases sin humo)

## D) Señales de robustez
- Pregunta lo mínimo necesario (1–2 preguntas bien diseñadas).
- Registra trace_id y audit.normalization_report.
- Se degrada con gracia cuando tools fallan (no se queda “pensando”).
