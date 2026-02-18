<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_00_Audit_Runbook_CRM_EndToEnd

## Executive summary (10–15 líneas)

**Facts:** NIST SSDF (SP 800-218) define un set de prácticas recomendadas para reducir vulnerabilidades a lo largo del SDLC.[^1]
**Facts:** OWASP ASVS provee una base para verificar controles técnicos de seguridad en aplicaciones web.[^2]
**Facts:** En SRE, los SLOs y el “error budget” habilitan políticas claras (p.ej., frenar releases si se excede el presupuesto de error).[^3][^4]
**Facts:** DORA identifica cuatro métricas clave para performance de entrega de software (Four Keys).[^5]
**Facts:** OpenAI documenta cómo contar tokens con `tiktoken` usando `len(encoding.encode(text))`.[^6]
**Inferences:** Este runbook estandariza una auditoría end-to-end de un CRM (repo sweep + DB + integraciones + QA + seguridad + performance + costos + tokens LLM) en **7 fases (0–6)** con entradas, evidencia mínima y gates de “needs_clarification”.
**Inferences:** La salida esperada es un **informe final** accionable (riesgo + impacto + evidencia + validación + decisión safe/aggressive + plan de remediación).
**Inferences:** Diseñado para equipos enterprise: múltiples repos, entornos (dev/stage/prod), integraciones con terceros, y flujos críticos (ventas, pipeline, comisiones, cobranza, soporte).
**Inferences:** Priorización por riesgo: seguridad + continuidad operativa, luego performance, luego costos/eficiencia, sin perder trazabilidad.
**Inferences:** “Sin evidencia” no es “cumple”: cualquier control sin prueba verificable queda como **needs_clarification** hasta que exista evidencia mínima.
**Inferences:** Incluye 3 templates reutilizables: inventario auditado, ficha de hallazgo, y mapeo hallazgo→evidencia→validación.

***

## Definitions and why it matters

**Facts:** SSDF busca mitigar el riesgo de vulnerabilidades mediante prácticas de desarrollo seguro aplicables a diferentes formas de software.[^1]
**Facts:** ASVS sirve como base para probar controles técnicos de seguridad en aplicaciones web.[^2]
**Facts:** En el enfoque SRE, SLOs + error budgets se usan para tomar decisiones operativas (incluyendo frenar releases cuando el budget se agota).[^4][^3]
**Facts:** DORA Four Keys son métricas para medir desempeño de entrega (enfoque DevOps).[^5]
**Facts:** Contar tokens antes de llamar a un LLM ayuda a controlar límites y costos, y puede hacerse con `tiktoken`.[^6]

**Inferences (por qué importa en CRM enterprise):**

- Un CRM es “sistema de verdad” para revenue: un hallazgo en permisos, integraciones o datos puede traducirse en fuga de información, fraude interno, comisiones erróneas o caída de ventas.
- Auditoría end-to-end evita “puntos ciegos”: el repo puede verse bien, pero el problema real estar en DB, secretos, jobs, pipelines, o un webhook sin validación.
- Tener evidencia mínima por fase reduce discusiones subjetivas y acelera decisiones (remediar vs aceptar riesgo vs monitorear).

***

## Principles and best practices (con citas por sección + fecha)

### 1) Secure SDLC como columna vertebral (NIST SSDF) — Consultado: 2026-02-17

**Facts:** NIST SP 800-218 (SSDF) recomienda un “core set” de prácticas de desarrollo seguro para mitigar riesgo de vulnerabilidades.[^1]
**Inferences (aplicación práctica al audit):**

- Mapea cada fase del audit a prácticas SSDF: ambiente de desarrollo, code review, pruebas, gestión de vulnerabilidades, y respuesta.
- Requisitos mínimos: trazabilidad (ticket→commit→deploy), manejo de vulnerabilidades (SLA, severidad), y evidencia verificable.


### 2) Verificación técnica de seguridad (OWASP ASVS) — Consultado: 2026-02-17

**Facts:** OWASP ASVS “provides a basis for testing web application technical security controls”.[^2]
**Facts:** OWASP describe niveles de verificación (y recomienda que la mayoría apunte a un nivel intermedio para apps con datos sensibles).[^7]
**Inferences:**

- Usa ASVS como checklist “control-by-control” para CRM: auth, session, access control, input validation, API security, configuración, logging.
- Output esperado: “cumple/no cumple/needs_clarification” por control + evidencia (logs, configs, pruebas, screenshots, queries, reports).


### 3) Confiabilidad operativa gobernada por SLO/Error Budget (Google SRE) — Consultado: 2026-02-17

**Facts:** El workbook de Google SRE explica que el error budget se deriva del SLO y requiere una política para actuar cuando se agota.[^3]
**Facts:** Un ejemplo de política: si se excede el error budget en una ventana (p.ej. 4 semanas), se **detienen cambios/releases** excepto P0 o fixes de seguridad hasta volver al SLO.[^4]
**Inferences:**

- En auditoría, performance y confiabilidad no son “opinión”: define SLOs por journeys (crear lead, cotizar, emitir, cobrar, postventa).
- El informe final debe incluir: SLOs actuales (si existen), gaps, y una política operativa mínima (qué se congela, quién aprueba, cuándo se reanuda).


### 4) Métricas de entrega para detectar fricción sistémica (DORA / Four Keys) — Consultado: 2026-02-17

**Facts:** Google Cloud explica que DORA identifica cuatro métricas clave (Four Keys) para indicar performance de equipos de software.[^5]
**Inferences:**

- Incluye baseline y tendencia (si hay histórico) para: frecuencia de despliegue, lead time de cambios, change failure rate, y MTTR.
- Si el CRM es core revenue, usa estas métricas como señales de riesgo: baja frecuencia + alto lead time suele correlacionar con releases “grandes” y más incidentes.


### 5) Control de costos y límites en LLM por token accounting (OpenAI/tiktoken) — Consultado: 2026-02-17

**Facts:** OpenAI Cookbook muestra cómo contar tokens con `tiktoken` usando `len(encoding.encode(string))`.[^6]
**Inferences:**

- Toda feature LLM del CRM debe auditar: input tokens, output tokens, retries, fallback, caching, y “token spikes” por prompts grandes o adjuntos.
- Estándar mínimo: logging de tokens por request (anonimizado), presupuestos por workflow (p.ej., “resumen de cuenta”), y alertas.

***

## Examples (paso a paso) — aplicado a CRM enterprise

### Example A: Auditoría de “Creación de Lead + Enriquecimiento + Asignación”

**Inferences (pasos):**

1) Identifica el journey: UI/Front → API CRM → DB → webhook enrichment (tercero) → reglas de asignación → notificación (email/WhatsApp/Slack).
2) Recolecta evidencia: diagrama actual, contratos API, config de webhook, logs de auditoría, y 3 casos reales (éxito, error, retry).
3) Seguridad: verifica control de acceso por rol (quién puede crear/editar/ver), validación de payload entrante, protección contra replay, y secrets management.
4) Confiabilidad: define SLI “lead creado end-to-end”, mide tasa de fallas y latencia p95/p99, identifica dependencias duras.
5) Costos/tokens (si LLM): cuantifica tokens por enriquecimiento/resumen y define budget mensual por agencia/tenant.
6) Hallazgos: crea fichas con severidad y recomendación safe vs aggressive; marca needs_clarification donde falte evidencia.

### Example B: Auditoría de “Cotización + Emisión + Facturación” (flujo crítico revenue)

**Inferences (pasos):**

1) Mapea estados y transiciones: cotización→reserva→emisión→factura→pago→anulación/refund.
2) DB audit: constraints (unicidad), integridad referencial, idempotencia (reintentos), y auditoría de cambios (quién cambió qué y cuándo).
3) Integraciones: GDS/bedbanks/PSP/ERP; verifica timeouts, retries, DLQ (si aplica), y reconciliación.
4) QA: crea un set mínimo de pruebas E2E y regresión para “emisión” y “pago”, con datos sintéticos y masking.
5) Reporta gaps como riesgos operativos (dinero + reputación + contracargos).

***

## Metrics / success signals

**Facts:** DORA Four Keys son un set de métricas para performance de entrega.[^5]
**Facts:** SLO/error budgets guían decisiones cuando se agota el presupuesto de error.[^3][^4]
**Facts:** Token counting puede implementarse con `tiktoken` y ayuda a anticipar límites/costos.[^6]

**Inferences (señales de éxito del audit):**

- Cobertura: % de repos/servicios/endpoints/integraciones inventariadas con dueño asignado.
- Evidencia: % de controles críticos con evidencia verificable (no “de palabra”); 0 controles “core” en needs_clarification al cierre.
- Riesgo: reducción del “Top 10” interno (p.ej., authz gaps, secrets expuestos, integraciones sin firma, queries lentas).
- Operación: SLOs definidos para 3–5 journeys críticos + política básica de error budget aprobada.
- Entrega: baseline DORA y plan para instrumentación si no existe.
- Costos: top drivers identificados (infra, terceros, LLM) + presupuestos + alertas.

***

## Operational checklist (por fase)

### Fase 0 — Kickoff, alcance y accesos (Gate de inicio)

**Entradas requeridas (mínimas):**

- Acceso a repos (GitHub/GitLab/Bitbucket) read + ability to run CI logs (si aplica).
- Acceso a entornos: dev/stage/prod (al menos read en configs, logs, métricas).
- Acceso a DB(s): schema read-only, EXPLAIN/ANALYZE (ideal) o snapshots sanitizados.
- Inventario preliminar: dominios funcionales del CRM y lista de integraciones.
- Contactos: owner técnico, owner producto, owner seguridad, owner data/BI, owner operaciones.

**Evidencia mínima:**

- Documento de alcance (in-scope/out-of-scope), lista de entornos, y responsables.
- Lista de repos + ramas principales + pipeline(s) existentes.

**Decisiones (safe vs aggressive):**

- Safe: read-only en todo; sin cambios; se audita con evidencia existente.
- Aggressive: habilitar feature flags/telemetría temporal, correr pruebas de carga controladas, y escaneo automatizado ampliado.

**Criterio needs_clarification:**

- Si no hay lista completa de repos/servicios o no se confirma qué es “source of truth” de datos → needs_clarification (no iniciar Fase 1).

***

### Fase 1 — Inventario y mapa end-to-end (sistemas + data flows)

**Objetivo:** “qué existe, dónde corre, quién lo dueña, cómo se conecta”.

**Checklist:**

- Identificar componentes: frontend(s), backend(s), workers/jobs, ETL/ELT, BI, auth/SSO, gateway, colas, cache, storage.
- Mapear integraciones: proveedores, webhooks, batch, APIs internas, PSP/ERP/Email/SMS/WhatsApp.
- Clasificar datos: PII, PCI, credenciales, contratos, tarifas, comisiones.

**Evidencia mínima:**

- Diagrama (C4 o equivalente) + tabla de inventario auditado completa al 80% (template abajo).
- Lista de “journeys críticos” (3–5) con owners.

**Decisiones (safe vs aggressive):**

- Safe: inventario basado en docs + repos + configs.
- Aggressive: descubrimiento activo (tracing, service map, enumeración de endpoints en runtime).

**needs_clarification:**

- Si no se puede trazar un journey crítico end-to-end (UI→API→DB→integración) con evidencia → needs_clarification.

***

### Fase 2 — Repo sweep (código + CI/CD + dependencias)

**Objetivo:** “lo que está en el repo coincide con lo que corre” + detectar riesgo en supply chain.

**Checklist:**

- Repos: estructura, ownership, ramas, políticas de merge, code owners.
- CI/CD: pipelines, secrets, approvals, ambientes, promoción de artefactos.
- Dependencias: lockfiles, actualización, librerías críticas, licencias (si aplica).
- Seguridad en código: patrones de authz, validación de input, manejo de errores, logging sensible.

**Evidencia mínima:**

- Lista de repos auditados + commit hash/branch auditada por repo.
- Export de configuración de pipeline (o screenshots verificables) + política de releases.

**Decisiones (safe vs aggressive):**

- Safe: revisión estática + políticas + muestreo dirigido en módulos críticos.
- Aggressive: SAST/secret scanning/dep scanning ampliado + ejecución en CI con reglas “fail on high”.

**needs_clarification:**

- Si no hay trazabilidad mínima ticket→commit→deploy para un módulo crítico → needs_clarification.

***

### Fase 3 — Data layer audit (DB + modelos + privacidad + retención)

**Objetivo:** exactitud, integridad, confidencialidad, y performance de datos.

**Checklist:**

- Esquema: claves, constraints, índices, particionado, migrations.
- Accesos: roles DB, least privilege, cuentas de servicio, rotación.
- Data quality: duplicados, “orphan records”, consistencia de estados.
- Privacidad: masking, retención, borrado, auditoría de cambios.

**Evidencia mínima:**

- ERD (o schema dump), lista de tablas PII, y 5 queries “más costosas” con plan de ejecución (si se puede).
- Política de backups/restore test (evidencia de último restore probado).

**Decisiones (safe vs aggressive):**

- Safe: análisis con read replicas/snapshots sanitizados.
- Aggressive: habilitar pg_stat_statements/slow query log temporal, correr EXPLAIN ANALYZE en horarios controlados.

**needs_clarification:**

- Si no existe prueba verificable de restore (RTO/RPO real) → needs_clarification.

***

### Fase 4 — Integraciones (contratos, resiliencia, seguridad, reconciliación)

**Objetivo:** que integraciones no sean “puntos únicos de falla” ni “puertas abiertas”.

**Checklist:**

- Contratos: versionado, idempotencia, validación de esquema, compatibilidad hacia atrás.
- Seguridad: firmas HMAC/mTLS donde aplique, allowlists, anti-replay, rotación de keys.
- Resiliencia: timeouts, retries con backoff, circuit breakers, DLQ/colas, re-procesamiento.
- Reconciliación: jobs de conciliación, dashboards, alertas por desbalance.

**Evidencia mínima:**

- Lista de integraciones + método auth + SLA esperado + evidencia de logs/monitoring.
- 3 incidentes pasados (si existen) o simulaciones controladas con resultados.

**Decisiones (safe vs aggressive):**

- Safe: revisión de contratos + configuración + logs.
- Aggressive: tests de caos controlados en stage, pruebas de reintento/idempotencia con replay.

**needs_clarification:**

- Si no se puede demostrar idempotencia o reconciliación en flujos de dinero → needs_clarification.

***

### Fase 5 — QA, seguridad, performance y confiabilidad (validación)

**Objetivo:** comprobar con pruebas, no solo con revisión.

**Checklist:**

- QA: suite mínima (smoke + regresión) para journeys críticos; datos sintéticos.
- Seguridad: verificación de controles (ASVS) y pruebas focalizadas (authn/authz, session, input, SSRF, etc.).[^2]
- Performance: p95/p99, saturación, cold starts, DB contention, colas, cache hit rate.
- Confiabilidad: SLOs/SLIs, error budgets, runbooks de incidentes.[^4][^3]

**Evidencia mínima:**

- Report de ejecución de pruebas (con fecha), resultados de performance (p95/p99), y definición de SLOs para 3–5 journeys.
- Política de error budget (aunque sea v0) y criterio de congelamiento de releases.[^4]

**Decisiones (safe vs aggressive):**

- Safe: pruebas en stage, carga baja, ventanas controladas.
- Aggressive: carga realista, fault injection limitada, y “release freeze” si se excede budget (en servicios críticos).[^4]

**needs_clarification:**

- Si no hay ambiente representativo para pruebas E2E o no se puede correr un smoke test confiable → needs_clarification.

***

### Fase 6 — Costos + LLM tokens + informe final (cierre)

**Objetivo:** convertir hallazgos en decisiones y plan.

**Checklist (costos):**

- Infra: top servicios por costo, entornos zombis, egress, storage, observabilidad.
- Terceros: costos por transacción (PSP, mensajería, enrichment), y reconciliación contra uso real.
- Performance/costo: queries caras, jobs ineficientes, overprovisioning.

**Checklist (LLM tokens):**

- Instrumentar conteo: input/output tokens por endpoint/workflow; usar `tiktoken` para conteo consistente en preflight.[^6]
- Presupuestos: tokens por tenant/agencia, límites por usuario, caching, y fallback sin LLM.
- Alertas: anomalías (spikes), retries, prompts demasiado largos.

**Evidencia mínima:**

- “Cost baseline” (últimos 30–90 días si existe) + top 10 drivers.
- Log/tabla de tokens por workflow (o plan implementable) con fórmula de conteo.[^6]
- Informe final firmado por stakeholders (o acta de entrega).

**Decisiones (safe vs aggressive):**

- Safe: límites conservadores, caching agresivo, feature flags, presupuestos por tenant.
- Aggressive: más automatización LLM (mayor costo variable) a cambio de más productividad; requiere guardrails y monitoreo estricto.

**needs_clarification:**

- Si no existe visibilidad mínima de costos (ni por proveedor ni por cuenta) o no hay forma de medir tokens → needs_clarification.

***

## Templates

### (a) Template — Tabla de inventario auditado

| Item_ID | Componente | Tipo | Repo/Artefacto | Entorno(s) | Owner | Datos (PII/PCI/No) | Integraciones | Criticidad (H/M/L) | Evidencia (links) | Estado (ok/risk/needs_clarification) |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| INV-001 | CRM-API | Backend | git@... | stage/prod | @equipo | PII | PSP, ERP | H | runbook link, logs link | needs_clarification |

**Inferences (reglas de uso):**

- “Evidencia” debe ser clickeable y verificable (log, screenshot con timestamp, export de config, query output).
- Si no hay owner → automáticamente needs_clarification (nadie responde por el riesgo).

***

### (b) Template — Ficha de hallazgo (Finding Card)

**Finding_ID:** FIND-\#\#\#
**Título:** (claro y accionable)
**Dominio:** Security / Data / Integrations / QA / Reliability / Performance / Cost / LLM
**Severidad:** Critical / High / Medium / Low
**Impacto negocio:** (fraude, fuga, caída ventas, comisiones mal, breach, etc.)
**Activo afectado:** (servicio, tabla, integración, endpoint)
**Descripción (qué pasa):**
**Riesgo (por qué importa):**
**Evidencia:** (links, logs, configs, query output, reporte)
**Pasos de reproducción / verificación:**
**Validación requerida:** (quién valida y cómo)
**Recomendación SAFE:** (mínimo cambio, bajo riesgo)
**Recomendación AGGRESSIVE:** (más impacto, más riesgo/costo)
**Esfuerzo estimado:** (S/M/L)
**Owner de remediación:**
**ETA objetivo:**
**Estado:** Open / In progress / Fixed / Accepted risk / needs_clarification
**Notas:**

***

### (c) Template — Mapeo hallazgo → evidencia → validación

| Finding_ID | Claim (qué afirmas) | Evidencia mínima | Dónde se obtiene | Validación (test/consulta) | Resultado esperado | Estado |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| FIND-012 | “Webhook acepta payload sin firma” | Request logs + config endpoint | Gateway logs, app config | Replay con payload sin HMAC | Rechazo 401/403 | Open |

**Inferences (regla):**

- Si “Dónde se obtiene” no es accesible con los permisos actuales → needs_clarification (es un bloqueo, no un hallazgo cerrado).

***

## Anti-patterns

**Facts:** Una política SRE típica frena releases cuando se excede error budget; ignorarlo degrada confiabilidad.[^4]
**Facts:** ASVS se usa para verificar controles técnicos; “cumple” sin verificación contradice el propósito del estándar.[^2]
**Inferences (anti-patrones comunes en auditorías de CRM):**

- Auditar solo el repo y no el runtime: “en el código está bien” pero en prod hay configs distintas.
- “Seguridad por checklist” sin evidencia: capturas viejas, links rotos, o “lo vimos una vez”.
- No auditar integraciones de dinero/identidad con idempotencia/reconciliación.
- Performance sin DB plans: optimizar app sin entender el cuello real (índices/queries).
- LLM sin token telemetry: costos variables descontrolados, prompts crecen, y nadie sabe por qué subió la factura.

***

## Diagnostic questions

**Facts:** Error budgets requieren una política de actuación cuando se agotan.[^3]
**Facts:** DORA Four Keys ofrecen señales de performance de entrega.[^5]
**Facts:** Token counting puede implementarse con `tiktoken`.[^6]
**Inferences (preguntas para descubrir gaps rápido):**

- ¿Puedes trazar un journey crítico end-to-end con evidencia (logs + IDs correlacionados) en menos de 30 minutos?
- ¿Qué parte del CRM es “source of truth” de comisiones y facturación, y cómo se auditan cambios?
- ¿Qué integraciones tienen idempotencia comprobada y reconciliación automatizada?
- ¿Cuáles son los SLOs (si existen) de “crear lead”, “emitir”, “cobrar” y “postventa”, y qué pasa cuando se incumplen?[^3]
- ¿Cuál es tu baseline DORA hoy y qué te impide mejorar (aprobaciones, pruebas, despliegue, incidentes)?[^5]
- Si hay LLM: ¿cuántos tokens por workflow y por tenant/agencia, y dónde se ve eso en un dashboard?[^6]
- ¿Qué evidencia falta hoy para cerrar auditoría sin “fe” (y quién la puede producir)?

***

## Sources

**NIST / Secure SDLC**

- NIST CSRC — *Secure Software Development Framework (SSDF) Version 1.1 (SP 800-218)*. (Consultado: 2026-02-17) https://csrc.nist.gov/pubs/sp/800/218/final[^1]

**OWASP / AppSec verification**

- OWASP — *Application Security Verification Standard (ASVS) project page*. (Consultado: 2026-02-17) https://owasp.org/www-project-application-security-verification-standard/[^2]
- OWASP (GitHub) — *ASVS 4.0.3 English PDF (raw)*. (Consultado: 2026-02-17) https://github.com/OWASP/ASVS/raw/v4.0.3/4.0/OWASP Application Security Verification Standard 4.0.3-en.pdf[^8]
- OWASP Developer Guide — *ASVS overview (niveles y orientación)*. (Consultado: 2026-02-17) https://devguide.owasp.org/en/03-requirements/05-asvs/[^7]

**SRE / Reliability governance**

- Google SRE Workbook — *Implementing SLOs (error budgets y policy)*. (Consultado: 2026-02-17) https://sre.google/workbook/implementing-slos/[^3]
- Google SRE Workbook — *Error Budget Policy for Service Reliability*. (Consultado: 2026-02-17) https://sre.google/workbook/error-budget-policy/[^4]

**DevOps / DORA**

- Google Cloud Blog — *Using the Four Keys to measure DevOps performance*. (Consultado: 2026-02-17) https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance[^5]

**LLM tokens**

- OpenAI Developers Cookbook — *How to count tokens with tiktoken*. (Consultado: 2026-02-17) https://developers.openai.com/cookbook/examples/how_to_count_tokens_with_tiktoken/[^6]

**SOURCES.md additions (sin duplicados) — Inferences**

- Agregar las entradas anteriores con el mismo título + URL + fecha de consulta, evitando repetir URLs ya existentes.

***

## Key takeaways for PM practice

- Define “done” como evidencia verificable; si falta → **needs_clarification** (no “lo cerramos igual”).
- Ancla seguridad a un estándar verificable (ASVS) y el SDLC a un marco (SSDF) para evitar auditorías subjetivas.[^1][^2]
- Gobernanza operativa: SLO + error budget policy evita discusiones interminables entre “features vs estabilidad”.[^3][^4]
- Baseline DORA te dice si tu problema es técnico o sistémico (aprobaciones, pruebas, releases).[^5]
- En LLM, sin token telemetry no hay control de costo ni de calidad; instrumenta desde el día 1.[^6]

***

## Mini tabla de contenidos (anchors)

- [Title](#kb_00_audit_runbook_crm_endtoend)
- [Executive summary](#executive-summary-10%E2%80%9315-l%C3%ADneas)
- [Definitions and why it matters](#definitions-and-why-it-matters)
- [Principles and best practices](#principles-and-best-practices-con-citas-por-secci%C3%B3n--fecha)
- [Examples](#examples-paso-a-paso--aplicado-a-crm-enterprise)
- [Metrics / success signals](#metrics--success-signals)
- [Operational checklist](#operational-checklist-por-fase)
- [Anti-patterns](#anti-patterns)
- [Diagnostic questions](#diagnostic-questions)
- [Sources](#sources)
- [Key takeaways for PM practice](#key-takeaways-for-pm-practice)
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^9]</span>

<div align="center">⁂</div>

[^1]: https://csrc.nist.gov/pubs/sp/800/218/final

[^2]: https://owasp.org/www-project-application-security-verification-standard/

[^3]: https://sre.google/workbook/implementing-slos/

[^4]: https://sre.google/workbook/error-budget-policy/

[^5]: https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance

[^6]: https://developers.openai.com/cookbook/examples/how_to_count_tokens_with_tiktoken/

[^7]: https://devguide.owasp.org/en/03-requirements/05-asvs/

[^8]: https://github.com/OWASP/ASVS/raw/v4.0.3/4.0/OWASP Application Security Verification Standard 4.0.3-en.pdf

[^9]: pasted-text.txt

[^10]: https://www.youtube.com/watch?v=1hGym9zQN1c

[^11]: https://csrc.nist.gov/pubs/sp/800/218/r1/ipd

[^12]: https://www.blackduck.com/blog/nist-ssdf-secure-software-development.html

[^13]: https://www.pivotpointsecurity.com/services/nist-sp-800-218-ssdf-consulting-services/

[^14]: https://nearshore-it.eu/articles/owasp-asvs/

[^15]: https://regscale.com/blog/regscale-support-nist-800-218-ssdf/

[^16]: https://regscale.com/blog/regscale-support-owasp-asvs/

[^17]: https://sreschool.com/blog/error-budgets-a-complete-guide/

[^18]: https://csrc.nist.gov/pubs/sp/800/218/a/ipd

[^19]: https://checkmarx.com/blog/what-you-need-to-know-about-nist-800-218-the-secure-software-development-framework/

[^20]: https://www.linkedin.com/posts/wojciech-ciemski_owasp-application-security-verification-standard-activity-7283804573230620673-cSaj

[^21]: https://github.com/OWASP/ASVS/blob/master/4.0/OWASP Application Security Verification Standard 4.0.3-es.pdf

[^22]: https://raw.githubusercontent.com/OWASP/ASVS/v4.0.3/4.0/OWASP Application Security Verification Standard 4.0.3-en.pdf

[^23]: https://github.com/OWASP/ASVS

[^24]: https://getdx.com/blog/dora-metrics/

[^25]: https://www.vellum.ai/blog/count-openai-tokens-programmatically-with-tiktoken-and-vellum

[^26]: https://github.com/OWASP/ASVS/blob/master/4.0/OWASP Application Security Verification Standard 4.0.3-fr.pdf

[^27]: https://www.thoughtworks.com/en-us/radar/techniques/four-key-metrics

[^28]: https://www.reddit.com/r/OpenAI/comments/1bqqole/how_to_count_tokens_before_you_hit_openais_api/

[^29]: https://github.com/OWASP/ASVS/releases

[^30]: https://codefresh.io/learn/software-deployment/dora-metrics-4-key-metrics-for-improving-devops-performance/

