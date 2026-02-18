<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_01 — Delivery Architecture for CRM

## Executive summary (10–15 líneas)

- [Facts] Las métricas DORA ayudan a medir desempeño de entrega y se recomiendan a nivel de aplicación/servicio (no “promediadas” sin contexto).
- [Facts] DORA define métricas de throughput e inestabilidad, y sostiene que velocidad y estabilidad no son necesariamente un trade-off en el tiempo.
- [Inference] En CRM enterprise, “arquitectura de entrega” es cómo organizas código, repos, entornos y releases para mover cambios a producción con control de riesgo (especialmente en multi-tenant y API pública).
- [Facts] Canarying es un despliegue parcial y limitado en el tiempo que compara “canary vs control” para decidir si continúas el rollout.[^1]
- [Facts] En SRE, canary reduce impacto porque expone solo una fracción del tráfico y por lo tanto “consume” menos presupuesto de error.[^1]
- [Facts] El error budget se relaciona con SLO y se usa para balancear confiabilidad vs velocidad de cambios.[^2]
- [Facts] Multi-tenancy “shared runtime/shared schema” acelera onboarding y upgrades, pero te obliga a ser la capa de aislamiento (riesgo de fuga por bugs con `tenant_id`).[^3]
- [Facts] Alternativas de tenancy incluyen schema-per-tenant o database-per-tenant, con trade-offs en migraciones/operación y aislamiento.[^4][^3]
- [Inference] La decisión monolito modular vs microservicios debe seguir “límites de dominio” del CRM y la madurez de tu plataforma de entrega (CI/CD, observabilidad, SRE).
- [Inference] Mono-repo vs multi-repo impacta coordinación de cambios cross-service, “blast radius” de pipelines y costos de gobernanza (versionado, compatibilidad, ownership).
- [Inference] La promoción por entornos debe estar diseñada para proteger SLOs: gates por SLI + canary + rollback, no solo “aprobaciones humanas”.


## Definitions and why it matters

- [Facts] DORA propone métricas de desempeño de entrega que permiten establecer una línea base, priorizar mejoras y validar progreso a lo largo del tiempo.
- [Facts] DORA distingue métricas de throughput (flujo de cambios) e inestabilidad (qué tan “problemáticos” son los despliegues) para entender entrega con seguridad.
- [Inference] “Arquitectura de entrega” para CRM = decisiones de (1) forma del sistema (monolito modular/microservicios), (2) forma del código (mono/multi repo), (3) forma del camino a prod (entornos, promoción, releases) y (4) forma de control de riesgo (SLO/error budget, canary, rollback).

**Por qué importa en CRM multi-tenant + API pública (lo sensible)**

- [Facts] En shared database/shared schema, el aislamiento depende de diseño: el `tenant_id` debe estar siempre presente y correctamente aplicado, y un bug puede convertirse en fuga de datos.[^3]
- [Facts] En database-per-tenant, se provisiona una base por tenant, lo que cambia el patrón operativo (catálogo/gestión de múltiples DBs) y puede mejorar aislamiento a costo de overhead.[^4]
- [Inference] En una API pública, tu “contrato” (versionado, compatibilidad, rate limits) se convierte en parte de la arquitectura de entrega: cada release puede romper integraciones B2B si no hay estrategia.


## Principles and best practices (con citas + fecha)

### 1) Medir delivery con DORA (2026-01-04)

- [Facts] DORA define **Change lead time** (commit → deploy), **Deployment frequency**, **Change fail rate** (ratio de despliegues que requieren intervención inmediata) y **Failed deployment recovery time** (tiempo de recuperación ante despliegue fallido), además de **Deployment rework rate** como métrica de despliegues no planificados por incidentes.
- [Facts] DORA advierte que el contexto importa y que mezclar métricas entre aplicaciones muy distintas puede ser engañoso; sugiere medir por aplicación/servicio.
- [Inference] En CRM, mide DORA por “plataforma CRM” y por “API pública” por separado si tienen perfiles de riesgo distintos (latencia, dependencia externa, cumplimiento).


### 2) Release safety con canary y automatización (Google SRE, 2017-12-31)

- [Facts] Release engineering recomienda builds reproducibles, builds/tests/deploys automatizados y despliegues pequeños para reducir riesgo y facilitar rollback.[^1]
- [Facts] Canarying es un despliegue parcial y limitado en el tiempo que evalúa señales para decidir continuar o parar.[^1]
- [Facts] Canarying minimiza riesgo al SLO/error budget porque expone solo una fracción del tráfico; el impacto en el presupuesto se relaciona con cuánto tráfico se expone y por cuánto tiempo.[^1]
- [Facts] Blue/green mantiene dos instancias (una sirviendo y otra standby) y permite cutover sin downtime con rollback simple, pero usa el doble de recursos.[^1]


### 3) SLO, error budgets y “gates” (Harness, 2026-02-10 + Google SRE, 2017-12-31)

- [Facts] El error budget se vincula al SLO (expresado como $1 - \text{SLO}$) y sirve para alinear velocidad de releases con confiabilidad.[^2]
- [Facts] Google SRE plantea explícitamente que puedes usar SLOs y error budgets para medir el impacto de releases en confiabilidad, y que canary ayuda a “gastar” menos error budget al limitar exposición.[^1]
- [Inference] Política práctica: si el servicio está “quemando” error budget, cambias de modo “feature” a modo “stability” (solo fixes, debt y hardening) hasta recuperar el objetivo.


### 4) Multi-tenancy como decisión de entrega (WorkOS 2025-12-02; Azure 2025-08-20)

- [Facts] Shared runtime/shared schema acelera onboarding (alta rápida) y upgrades (un solo despliegue), pero incrementa el riesgo de aislamiento: tú eres la capa que previene fugas.[^3]
- [Facts] Schema-per-tenant mejora aislamiento y restores por tenant, pero complica migraciones al multiplicar cambios por N esquemas.[^3]
- [Facts] Database-per-tenant provisiona una DB por tenant y cambia el patrón de escalado y operación; se apoya en mecanismos de catálogo/mapeo tenant→DB para gestión centralizada.[^4]
- [Inference] En CRM, la arquitectura de entrega debe “entender tenants”: migraciones, backfills, canaries y rollbacks requieren plan por tenant tier (SMB vs enterprise regulado).


## Examples (aplicado a CRM enterprise)

### Ejemplo A: Monolito modular (multi-tenant) + API pública “estabilizada”

- [Facts] En multi-tenancy compartida, el control de aislamiento requiere que el runtime y el acceso a datos sean tenant-aware; un bug con `tenant_id` puede causar fuga.[^3]
- [Inference] Patrón: un monolito modular con módulos por dominio (Accounts, Deals, Activities, Billing, Integrations), y una “capa de tenant context” obligatoria (middleware + RLS/filters + tests de fuga).
- [Inference] Promoción: dev → staging → prod con canary en prod (1–5% tráfico) y gate por SLI (p.ej., error rate y latencia de endpoints críticos).
- [Facts] Canary requiere comparar métricas canary vs control, y seleccionar pocas métricas representativas/atribuibles para evitar falsos positivos y pérdida de confianza.[^1]
- [Inference] API pública: versionado por ruta (`/v1`) o header, compatibilidad hacia atrás por defecto; cambios breaking solo con `/v2` y ventana de deprecación (comunicada a integradores).


### Ejemplo B: Microservicios “mínimos” alrededor de riesgos (API pública y jobs)

- [Facts] DORA recomienda aplicar métricas por servicio/aplicación, porque comparar o mezclar sin contexto puede distorsionar decisiones.
- [Inference] Patrón: mantener Core CRM (multi-tenant) como monolito modular, pero extraer dos servicios con ciclos distintos: (1) API Gateway/Developer Platform (auth, rate limits, analytics), (2) Async Jobs (imports/exports, sync con ERPs).
- [Facts] Los cambios y releases son una fuente común de incidentes; SRE enfatiza medir su impacto con SLOs/error budgets y usar canary para reducir exposición.[^1]
- [Inference] Estrategia de release para API pública: canary por “cohorte” de integradores (allowlist de client_ids) antes de abrir a todo el tráfico, con rollback rápido y “kill switch” de features.


### Ejemplo C: Tenancy por “tier” (pooled default + excepciones enterprise)

- [Facts] Shared schema es común por simplicidad, pero schema-per-tenant o database-per-tenant aumentan aislamiento con costo operativo y complejidad de migraciones/gestión.[^4][^3]
- [Inference] Patrón comercial/operativo: “pooled” para la mayoría (margen + velocidad) y “DB-per-tenant” premium para cuentas con compliance, data residency o volumen (cobro adicional + SLAs diferenciados).
- [Inference] Delivery: pipelines y migraciones deben soportar ambos modelos, con “catálogo” tenant→ubicación y despliegues/migraciones segmentadas por grupo.


## Metrics / success signals

**DORA (por servicio y por plataforma)**

- [Facts] DORA incluye Change lead time y Deployment frequency como throughput, y Change fail rate y Failed deployment recovery time como estabilidad/recuperación.
- [Inference] Señales saludables en CRM: lead time cae sin subir change fail rate; deployment frequency sube sin degradar SLO; recovery time baja por rollback automatizado y mejores canaries.

**SLO alignment**

- [Facts] El error budget se deriva del SLO (conceptualmente $1 - \text{SLO}$) y se usa para gobernar cuánto cambio puedes introducir sin comprometer confiabilidad.[^2]
- [Facts] Canarying “protege” el error budget al limitar tráfico expuesto y permitir rollback temprano si las métricas se desvían.[^1]
- [Inference] SLIs típicos CRM/API: disponibilidad por endpoint crítico, p95/p99 latency, tasa de errores 5xx, éxito de webhooks, frescura de datos en syncs, y “tenant isolation incidents” como métrica de seguridad (cero tolerancia).


## Operational checklist

- [Facts] Define DORA por aplicación/servicio y evita comparaciones engañosas entre sistemas con contextos distintos.
- [Inference] Decide el “unit of delivery”: plataforma CRM, API pública, jobs async; cada uno con pipeline y métricas separadas.
- [Facts] Implementa despliegues pequeños, builds reproducibles y despliegues automatizados para reducir riesgo y facilitar rollback.[^1]
- [Facts] Implementa canary (población y duración) y evalúa canary vs control con pocas métricas representativas/atribuibles.[^1]
- [Inference] Establece gates automáticos por SLI (latencia/error rate) antes de promover a 100%, y define playbook de rollback “one-click”.
- [Facts] En multi-tenancy compartida, refuerza aislamiento por diseño (tenant context, queries filtradas) porque un bug puede generar fuga.[^3]
- [Inference] Para API pública: contrato explícito, versionado, changelog, sandbox, rate limiting y “deprecation policy” para no romper integradores B2B.
- [Inference] Define política de “release freeze” basada en error budget (si se agota, solo cambios de estabilidad).


## Anti-patterns

- [Facts] Goodhart/pitfalls: convertir métricas en objetivo y “competir” entre equipos puede incentivar gaming y decisiones malas; DORA recomienda usar métricas para mejorar en el tiempo.
- [Facts] Comparar métricas entre aplicaciones muy distintas puede ser engañoso; mide por app/servicio.
- [Inference] “Microservicios por moda” sin plataforma (observabilidad, ownership, CI/CD) → más puntos de falla y lead time peor.
- [Inference] “Staging como espejo perfecto de prod” (falso) → te confías, rompes SLO en producción; usa canary y rollback real.
- [Facts] Usar demasiadas métricas en canary aumenta costo y puede generar falsos positivos, erosionando confianza en el proceso.[^1]
- [Inference] Multi-tenant sin pruebas sistemáticas anti-fuga (y sin auditoría) → el incidente “inevitable” termina siendo reputacional y contractual.


## Diagnostic questions

- [Facts] ¿Estás midiendo DORA por servicio/aplicación o estás mezclando métricas de sistemas distintos?
- [Inference] ¿Tu CRM necesita releases diarios (velocidad comercial) o releases “por ventana” (riesgo/compliance), y cómo lo refleja tu pipeline?
- [Facts] ¿Tienes canary vs control con evaluación clara, o despliegas “a todo” y esperas que monitoreo general te avise?[^1]
- [Inference] ¿Qué porcentaje de releases de API pública incluyen cambios breaking y cuántos integradores se enteran “por caída”?
- [Facts] ¿Tu modelo de tenancy (shared/schema-per-tenant/db-per-tenant) está alineado con necesidades de aislamiento y operación, y aceptas explícitamente sus trade-offs?[^4][^3]
- [Inference] ¿Tienes una regla objetiva que conecta error budget con velocidad de release (acelerar/pausar) o es debate ad-hoc cada incidente?


## Sources (y adiciones a SOURCES.md)

- DORA — “DORA’s software delivery performance metrics” (2026-01-04): https://dora.dev/guides/dora-metrics/
- Google SRE Workbook — “Canarying Releases” (2017-12-31): https://sre.google/workbook/canarying-releases/[^1]
- WorkOS — “The developer’s guide to SaaS multi-tenant architecture” (2025-12-02): https://workos.com/blog/developers-guide-saas-multi-tenant-architecture[^3]
- Microsoft Learn (Azure SQL) — “Multitenant SaaS database tenancy patterns” (2025-08-20): https://learn.microsoft.com/en-us/azure/azure-sql/database/saas-tenancy-app-design-patterns[^4]
- Harness — “How to Use Error Budgets for Reliability Management” (2026-02-10): https://www.harness.io/blog/how-use-error-budgets-reliability-management[^2]

**Additions to `SOURCES.md` (sin duplicados)**

- DORA. “DORA’s software delivery performance metrics.” 2026-01-04. https://dora.dev/guides/dora-metrics/
- Google SRE. “Canarying Releases.” 2017-12-31. https://sre.google/workbook/canarying-releases/
- WorkOS. “The developer’s guide to SaaS multi-tenant architecture.” 2025-12-02. https://workos.com/blog/developers-guide-saas-multi-tenant-architecture
- Microsoft Learn (Azure SQL). “Multitenant SaaS database tenancy patterns.” 2025-08-20. https://learn.microsoft.com/en-us/azure/azure-sql/database/saas-tenancy-app-design-patterns
- Harness. “How to Use Error Budgets for Reliability Management.” 2026-02-10. https://www.harness.io/blog/how-use-error-budgets-reliability-management


## Key takeaways for PM practice

- Alinea roadmap con “capacidad de entrega” medible (DORA por servicio), no con deseos de calendario.
- Usa SLO/error budget como lenguaje común entre producto, ingeniería y operaciones para decidir cuándo acelerar o frenar releases.[^2][^1]
- En API pública, la estrategia de release es parte del producto: canary por cohortes + rollback + política de versiones evita churn de integradores.[^1]
- En multi-tenant, el aislamiento es un riesgo existencial; tu arquitectura de entrega debe incluir pruebas, migraciones y rollouts con conciencia de tenant.[^3]
- Diseña “opción segura vs agresiva”: safe = monolito modular + canary + SLO gates; agresiva = extraer servicios solo donde el riesgo/ritmo lo justifica (API/async).[^1]
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: pasted-text.txt

[^2]: https://www.harness.io/blog/how-use-error-budgets-reliability-management

[^3]: https://workos.com/blog/developers-guide-saas-multi-tenant-architecture

[^4]: https://learn.microsoft.com/en-us/azure/azure-sql/database/saas-tenancy-app-design-patterns?view=azuresql

[^5]: https://getdx.com/blog/dora-metrics/

[^6]: https://dora.dev/guides/dora-metrics/

[^7]: https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance

[^8]: https://www.dynatrace.com/knowledge-base/doras-four-keys/

[^9]: https://abstracta.us/blog/devops/dora-metrics-in-devops/

[^10]: https://swiss-digital-network.ch/effective-sre-slo-engineering-and-error-budget/

[^11]: https://www.atlassian.com/devops/frameworks/dora-metrics

[^12]: https://www.linkedin.com/posts/srisainath3456_your-slo-is-999-that-means-you-have-a-activity-7426468435154538496-z3R4

[^13]: https://bix-tech.com/multi-tenant-architecture-the-complete-guide-for-modern-saas-and-analytics-platforms-2/

[^14]: https://launchdarkly.com/blog/dora-metrics/

[^15]: https://www.datadoghq.com/knowledge-center/dora-metrics/

[^16]: https://sre.google/workbook/canarying-releases/

