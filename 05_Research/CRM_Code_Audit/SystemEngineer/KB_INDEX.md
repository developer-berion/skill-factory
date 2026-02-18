\# KB\_INDEX — Auditoría técnica de CRM a nivel de código (System Engineer / Enterprise)



\## Propósito

Este Knowledge Base (KB) sirve como \*\*fuente de verdad\*\* para un agente/skill que audita un CRM construido por IA (o humanos) y entrega:

\- Barrido total del repositorio (dead code, dependencias inútiles, entrypoints reales).

\- Auditoría de base de datos (conexiones, queries, índices, migraciones, costos).

\- Auditoría de integraciones (p. ej. Brevo webhooks, retries, idempotencia, seguridad).

\- QA analítico end-to-end (golden sets, flaky tests, contract tests, CI).

\- Seguridad enterprise (RBAC/ABAC, multi-tenancy, audit logs, secrets).

\- Observabilidad (SLOs, trazas, logging estructurado, runbooks).

\- Performance y escalabilidad (patrones, colas/workers, caché, paginación).

\- FinOps: infra + LLM/tokens (detección de gasto inútil, control por tenant/feature).

\- Informe final con severidad, evidencia mínima, remediación y plan 30/60/90.



\## Cómo usar este KB (flujo recomendado)

1\) \*\*Fase 0 — Runbook\*\*: define alcance, entornos, evidencia mínima y criterios de “needs\_clarification”.

2\) \*\*Fase 1 — Repo Sweep\*\*: identifica entrypoints, rutas, jobs, workers, flags; detecta dead code y deps inútiles.

3\) \*\*Fase 2 — DB Audit\*\*: conexiones activas, pool, queries top, N+1, índices, migraciones seguras (expand/contract).

4\) \*\*Fase 3 — Integraciones\*\*: contratos, idempotencia, webhooks (ACK rápido + cola), retries/backoff, DLQ, firma/headers.

5\) \*\*Fase 4 — QA Strategy\*\*: pirámide, golden sets determinísticos, cuarentena de flaky, contract tests, seeds reproducibles.

6\) \*\*Fase 5 — Seguridad\*\*: multi-tenancy como control de seguridad, anti-BOLA, logs sin PII, secrets operables.

7\) \*\*Fase 6 — Performance + Observabilidad + FinOps\*\*: SLOs, burn-rate, tracing, costos infra/colas/logs y tokens LLM.

8\) \*\*Salida — Reporte final\*\*: hallazgos con severidad, evidencia, impacto, recomendación, owner, retest y 30/60/90.



\## Mapa de archivos (Source of Truth)

\### 00. Runbook y salida

\- `KB\_00\_Audit\_Runbook\_CRM\_EndToEnd.md` — Runbook de auditoría por fases, gates y evidencia mínima.  

&nbsp; Referencias base a SSDF/ASVS/SRE/DORA/tokens. 【ver fuentes internas del doc】:contentReference\[oaicite:0]{index=0}

\- `Plantilla de informe final de auditoría técnica (h.md` — Plantilla del informe final + preguntas diagnósticas + 30/60/90. :contentReference\[oaicite:1]{index=1}



\### 01. Dominio CRM (modelo a nivel de código)

\- `KB\_01\_CRM\_Domain\_Model\_At\_Code\_Level.md.md` — Entidades, invariantes, eventos de dominio, multitenancy, workflows (pipeline). :contentReference\[oaicite:2]{index=2}



\### 02. Barrido de repo (análisis estático / dead code)

\- `KB\_02\_Repo\_Sweep\_Static\_Analysis\_DeadCode.md` — call graph, reachability, CodeQL/Semgrep/ts-prune/Vulture/depcheck/staticcheck. :contentReference\[oaicite:3]{index=3}



\### 03. Auditoría DB

\- `KB\_03\_DB\_Audit\_Connections\_Queries\_Indexes\_Migrati.md` — EXPLAIN/ANALYZE, N+1, pool leaks, índices concurrentes, expand/contract, logging seguro. :contentReference\[oaicite:4]{index=4}



\### 04. Integraciones (Brevo / Webhooks / Confiabilidad)

\- `KB\_04\_Integrations\_Brevo\_Webhooks\_Reliability.md` — diseño webhook “verify → enqueue → ACK”, idempotencia, retries, DLQ, rate limits, auth. :contentReference\[oaicite:5]{index=5}



\### 05. Seguridad enterprise (RBAC/ABAC + multitenancy + audit logs)

\- `KB\_05\_Security\_RBAC\_Multitenancy\_AuditLogs — Segur.md` — anti-BOLA, aislamiento tenant, ABAC, logging, secrets. :contentReference\[oaicite:6]{index=6}



\### 06. QA Strategy (Golden Sets)

\- `KB\_06\_QA\_Strategy\_CRM\_Testing\_GoldenSets — Estrate.md` — pirámide, flaky quarantine, data seeding, snapshot testing/golden masters. :contentReference\[oaicite:7]{index=7}



\### 07. Observabilidad (SaaS CRM + integraciones)

\- `KB\_07 — Observabilidad en SaaS (CRM + Integracione.md` — trace context, OTel propagation, RED/USE, SLO + burn rate, runbooks. :contentReference\[oaicite:8]{index=8}



\### 08. Performance y escalabilidad

\- `Performance y escalabilidad en CRMs\_ patrones prác.md` — paginación keyset, índices, caching anti-stampede, colas/workers, export incremental. :contentReference\[oaicite:9]{index=9}



\### 09. FinOps + tokens LLM

\- `KB\_09 — FinOps + optimización de tokens (LLM).md` — unit economics por feature/tenant, caching/dedupe, routing de modelos, telemetría de tokens. :contentReference\[oaicite:10]{index=10}



\### 10. Template de hallazgos / severidad (si aplica)

\- `KB\_10\_Audit\_Report\_Template\_Findings\_Severity..md` — (si está en la carpeta final) criterios de severidad, estructura de hallazgo.



\### 11–13. Complementarios (gobernanza y costos infra)

\- `KB\_11 — Secure SDLC\_ SAST, Secrets \& Dependency Sc.md` — Secure SDLC, escaneo, secretos, dependencias.

\- `KB\_12 — Data Governance\_ PII, Retention \& Audit Tr.md` — PII, retención, audit trail tamper-evident, compliance. :contentReference\[oaicite:11]{index=11}

\- `KB\_13\_FinOps\_CRM\_Infrastructure\_DB\_Queue\_Costs.md` — costos infra (DB, colas, logs/retención), showback/chargeback. :contentReference\[oaicite:12]{index=12}



\## Convenciones (para el skill)

\- \*\*No inventar\*\*: si falta evidencia → `needs\_clarification`.

\- \*\*Facts vs Inferences\*\*: separar explícitamente.

\- \*\*Cada hallazgo\*\* debe traer: evidencia mínima, impacto, recomendación, owner sugerido, retest.

\- \*\*Multi-tenant\*\*: todo análisis debe poder segmentar por `tenant\_id` (o explicar por qué no).



\## Qué falta (gap checklist rápido)

\- Falta estandarizar una sección única “\*\*Inventory of Entry Points\*\*” (API/routes/cron/queue/flags) como artefacto obligatorio del repo sweep.

\- Falta un KB explícito de \*\*arquitectura de referencia CRM\*\* (capas, límites de contexto, módulos) si tu CRM es grande.

\- Falta “\*\*Data migration playbooks\*\*” (rollback, backfill, dual-write, verificación) si haces cambios frecuentes de esquema.



\## Referencias

\- Ver `SOURCES.md`.



