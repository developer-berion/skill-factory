<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_02_TrunkBased_Flags_ProgressiveDelivery (2026): Trunk-based + Flags + Progressive Delivery para CRM multi-tenant (sin incidentes)

## Executive summary (10–15 líneas)

Fact: En SRE de Google, los *rollbacks* se tratan como “normales” y la recomendación operativa es “rollback primero, investiga después” para reducir impacto y MTTR.[^1]
Inference: En un CRM enterprise, esto se traduce en diseñar cada cambio como “apagable” (kill switch) y “reversible” (rollback probado), no solo “deployable”.
Fact: Canarying se define como un despliegue parcial y **time-limited** que se evalúa contra un “control” antes de continuar el rollout.
Inference: Para CRM multi-tenant, el canary más útil casi nunca es “usuarios aleatorios”: es por tenant (o por cohorte de tenants) con telemetría segregada por tenant.
Fact: El enfoque de canarying ayuda a conservar *error budget* al limitar el tráfico expuesto a defectos.
Inference: Tu gobernanza debe impedir cambios “globales” irreversibles (schema + feature) sin fase intermedia compatible.
Fact: Google advierte que los rollbacks se vuelven difíciles cuando hay cambios incompatibles (por ejemplo, cambios de esquema) y propone una “feature-free release” intermedia antes de activar features.[^1]
Inference: En CRM, separa siempre: compatibilidad de datos (migración) vs activación funcional (flag), y no las mezcles en la misma ventana de riesgo.
Fact: Blue/green mantiene dos entornos (uno sirviendo y otro listo), permite cutover sin downtime y rollback simple, pero consume el doble de recursos.
Inference: Blue/green es potente para releases grandes del core CRM, pero caro; úsalo con criterios explícitos y no “por moda”.
Fact: Unleash describe trunk-based con “trunk siempre deployable”, rollout controlado y capacidad de desactivar rápido vía flags.[^2]

***

## Definitions and why it matters

Fact: Canarying es un despliegue parcial y evaluado (canary vs control) para decidir si se continúa el rollout.
Inference: En CRM, “evaluar” significa medir SLIs que reflejen operación real (creación de leads, actualización de pipeline, carga de reporting, integraciones).

Fact: Blue/green es un patrón con dos instancias (green sirve, blue está lista), con cutover/rollback por routing, a costa de duplicar recursos.
Inference: Para CRM multi-tenant, blue/green reduce riesgo de cambios de infraestructura, pero no sustituye controles de datos (migraciones y compatibilidad).

Fact: En la práctica de SRE, una parte material de incidentes proviene de pushes de binario o configuración, y por eso se enfatiza detección/rollback/canarying.
Inference: En CRM, “configuración” incluye reglas de negocio, permisos, pricing/planes por tenant y toggles; todo eso requiere trazabilidad y auditoría como si fuera código.

***

## Principles and best practices (con citas por sección + fecha)

### 1) Trunk-based como “sistema”, no como branching (2025-10-20 / 2025-12-31)

Fact: Trunk-based se apoya en integrar cambios pequeños y frecuentes a una rama principal con automatización (CI/CD) para mantener el trunk deployable.[^3][^2]
Inference: Regla CRM: “merge diario o no merges”; si un cambio no puede integrarse pequeño, necesitas *slicing* funcional + flags (no branches largos).

Fact: Unleash posiciona flags como mecanismo para integrar código sin exponerlo y permitir desactivación rápida si hay problemas.[^2]
Inference: Estándar interno: toda feature “no trivial” debe tener ruta de fallback (código viejo) y *kill switch* documentado (quién lo acciona, en qué entorno, con qué criterio).

**Cuando NO usar trunk-based (o cuándo no forzarlo):**
Inference: Si no tienes CI confiable, pruebas automatizadas mínimas, y disciplina de cambios pequeños, trunk-based te puede aumentar incidentes por “main roto” (mejor un enfoque transicional con ramas cortas + gates estrictos).
Inference: Si tu CRM tiene releases regulados con ventanas fijas y ambientes poco automatizados, adopta trunk-based primero en servicios periféricos (APIs internas, jobs) antes del core transaccional.

***

### 2) Feature flags con gobernanza (RBAC), auditoría y “flag hygiene” (2026-01-22 / 2024-12-31 / 2026-02-07)

Fact: LaunchDarkly indica que su audit log da visibilidad del “quién, qué y cuándo” de cambios de flags.[^4]
Fact: La documentación de LaunchDarkly describe que mantiene un registro de cambios y que se puede acceder/filtrar vía Audit Log API (p. ej., por timestamps).[^5]
Inference: Política CRM multi-tenant: cualquier cambio de targeting por tenant (enable/disable, reglas, porcentajes) es un “cambio de control” y debe quedar auditado, con ticket/razón.

Fact: LaunchDarkly menciona que el audit log se visualiza por ambiente (entorno), y se cambia de entorno para ver otros registros.[^4]
Inference: En CRM, esto es clave: separa *environments* por riesgo (prod vs staging) y prohíbe “promover” manualmente configuraciones sin historial y sin revisión.

Fact: Un ejemplo de buenas prácticas 2026 para flags incluye programar auditorías periódicas (p. ej., trimestrales) para evitar “flag debt” (flags sin dueño, vencidos, o al 100% demasiado tiempo).[^6]
Inference: En CRM, “flag debt” pega directo en incidentes: rutas viejas no probadas, permisos divergentes por tenant, y lógica condicional que nadie entiende en on-call.

**Playbook: Gobernanza mínima de flags (operable en CRM)**

- Inference: Inventario obligatorio: key, descripción de negocio, owner (equipo + persona), tipo (release/ops/experimento), alcance (global/tenant), fecha de expiración.
- Inference: RBAC: solo un grupo reducido puede cambiar flags en prod; el resto solo en staging.
- Inference: Auditoría: todo cambio en prod debe tener razón (incidente, rollout plan, experimento aprobado) y correlación con despliegue/versión.

**Cuando NO usar feature flags:**
Inference: No uses flags para *permanentes* “planes comerciales” si no tienes un sistema de entitlement claro; terminarás con combinaciones imposibles de testear (mejor modelar planes/permissions como data/entitlements versionados).
Inference: No uses flags para ocultar cambios de datos irreversibles (migraciones destructivas) sin estrategia de compatibilidad; el “off” no desmigra datos.

***

### 3) Canary: métricas, aislamiento, y gates automatizados (SRE Workbook, 2017; actualizado en prácticas 2026)

Fact: El workbook de SRE recomienda automatizar builds/tests/deployments y hacer deployments pequeños para facilitar rollback y reducir riesgo.
Fact: SRE describe que canarying reduce impacto porque expone una fracción del tráfico y permite detectar defectos antes del despliegue total.
Inference: Para CRM: canary por tenant (5–20 tenants), luego por cohorte (por país/moneda/plan), luego global; evita mezclar cambios grandes en un solo canary.

Fact: SRE advierte que canaries simultáneos aumentan carga mental y pueden contaminar señales; aconseja limitar la simultaneidad.
Inference: Política: 1 canary activo por “dominio” (por ejemplo: pipeline/ventas, facturación, integraciones) para que soporte y ventas entiendan el estado.

Fact: SRE recomienda seleccionar pocas métricas (no demasiadas) y priorizar señales que reflejen problemas percibidos por usuarios (SLIs) para evitar falsos positivos y pérdida de confianza.
Inference: En CRM, gates típicos: error rate por endpoint crítico, latencia p95/p99 de escritura, tasa de fallos en integraciones (WhatsApp/email/ERP), y “data correctness” con checks (por ejemplo, totales y estados coherentes).

**Playbook: Canary en CRM (operable)**

1) Inference: Pre-canary: habilita logging/metrics por tenant + por versión + por ruta de código (flag on/off).
2) Inference: Stage 1 (tenant canary): 1–5 tenants internos o “friendly”; duración suficiente para carga real (no solo 5 minutos).
3) Inference: Gate: si SLIs empeoran vs control, pausa y revierte (flag off o rollback binario según causa).
4) Inference: Stage 2: amplía cohorte; repite gates; solo luego pasa a 100%.

**Cuando NO usar canary (o cuándo no confiar en él):**
Inference: Si no puedes aislar métricas canary vs control (por tenant o por versión), el canary te dará “ruido” y falsas conclusiones.
Inference: Si el cambio es 100% *backoffice* (sin tráfico representativo) o se activa por eventos raros (cierre mensual), complementa con “replay/traffic teeing” o pruebas sintéticas enfocadas (sin asumir que canary cubrirá ese caso).

***

### 4) Blue/green: cutover reversible, pero caro (SRE Workbook, 2017)

Fact: Blue/green permite cutover sin downtime y rollback como reversión de routing, pero consume el doble de recursos.
Inference: En CRM, úsalo para: upgrades de infraestructura, cambios grandes de runtime, o releases del core donde un rollback rápido de routing es la mejor palanca.

**Playbook: Blue/green en CRM (cutover seguro)**

- Inference: Mantén green estable, despliega a blue, valida *smoke tests* + checks de integraciones salientes.
- Inference: Cutover gradual (si puedes) o cutover total con ventana; prepara rollback inmediato por routing.
- Inference: Post-cutover: monitorea SLIs + colas de jobs + integraciones por tenant durante al menos 1 ciclo operativo.

**Cuando NO usar blue/green:**
Inference: Si el costo de duplicar recursos es prohibitivo o si el sistema tiene estado acoplado (jobs, colas, caches) que hace que “dos mundos” se interfieran, preferir canary progresivo por tráfico/tenant.

***

### 5) Rollback “de verdad”: practicarlo y diseñar compatibilidad (Google CRE, 2018)

Fact: Google CRE enfatiza que antes de rollout debes tener un plan de rollback, y recomienda rollback primero e investigar después cuando hay sospecha razonable.[^1]
Fact: CRE advierte contra “roll forward” apurado bajo presión porque suele introducir errores adicionales.[^1]
Inference: En CRM, el rollback no es “git revert”: es una capacidad del sistema (binario/config/data) con runbook probado en simulacros.

Fact: CRE explica que cambios incompatibles (p. ej. schema) rompen rollbacks y propone una versión intermedia “feature-free” que soporte el nuevo schema antes de activar features.[^1]
Inference: Patrón CRM recomendado:

- v+1: compatibilidad (leer/escribir en ambos formatos, columnas nuevas opcionales, migración gradual).
- v+2: activación funcional detrás de flag (por tenant/cohorte).

**Cuando NO “rollbackear” (y qué hacer):**
Inference: Si ya escribiste datos irreversibles sin compatibilidad (migración destructiva), un rollback binario puede agravar corrupción; en ese caso, apaga features (flags), detén writes peligrosos, y ejecuta plan de reparación de datos (runbook específico).

***

## Examples (aplicado a CRM enterprise)

### Ejemplo A: Nuevo motor de “Asignación de leads” por tenant (Flags + canary)

Fact: Canarying es una evaluación A/B (canary vs control) en producción para decidir si se continúa.
Inference: Implementación: `lead_assignment_engine_v2` (release flag) con targeting por tenant; canary en 3 tenants internos, luego 20 tenants con alto volumen.

Inference (incluye):

- Qué incluye: reglas nuevas detrás de flag, métricas por tenant, kill switch por tenant, rollback plan (flag off + rollback binario si es crash).
- Qué no incluye: migración destructiva de datos, cambios de permisos permanentes sin modelo de entitlement.
- Qué es sensible: latencia de escritura de lead, duplicados, integraciones downstream (ERP/marketing), y “idempotencia” en reintentos.


### Ejemplo B: Cambio de schema para “etapas de pipeline” (Compatibilidad + rollout en 2 fases)

Fact: CRE menciona que cambios de schema pueden dejarte con binario viejo incompatible al hacer rollback, y por eso sugiere una versión intermedia compatible (“feature-free release”).[^1]
Inference: Fase 1 (v+1): agrega columnas/tabla nueva, doble escritura (old+new) y lectura tolerante; Fase 2 (v+2): activa UI/logic nueva por tenant con flag.

### Ejemplo C: Release grande del core CRM (Blue/green)

Fact: Blue/green permite cutover y rollback por routing y requiere más recursos.
Inference: Úsalo cuando cambias runtime, librerías base o config global; complementa con flags para features que cambian comportamiento por tenant.

***

## Metrics / success signals

Fact: SRE recomienda usar SLIs como base para métricas de canary y limitar el número de métricas para evitar ruido y falsos positivos.
Inference: Señales clave en CRM (por tenant y global):

- Error rate de escrituras (crear/actualizar lead, mover etapa, crear oportunidad).
- Latencia p95/p99 en endpoints críticos de escritura.
- Tasa de fallos de integraciones (email/WhatsApp/webhooks/ERP), backlog de colas y reintentos.
- Indicadores de “correctitud” (duplicados, estados imposibles, totales inconsistentes).

Fact: CRE sugiere desglosar métricas por versión de binario para detectar fallas sutiles que no aparecen en el agregado global.[^1]
Inference: En CRM, exige dashboards por versión + por tenant/cohorte durante canary y durante 24–72h post-release.

***

## Operational checklist

Fact: CRE recomienda planear el rollback antes del rollout y tratar el rollback como acción normal ante sospecha razonable.[^1]
Inference: Checklist operable (pre / durante / post):

- Inference: Pre (diseño): fallback path en código, flag con owner+expiración, compatibilidad de schema en 2 fases si aplica.
- Inference: Pre (gobernanza): RBAC para prod, auditoría de cambios de flags, naming estándar, límites de targeting (por tenant/cohorte).
- Inference: Pre (observabilidad): métricas por tenant, por versión, y por estado de flag; alertas con umbrales acordados.
- Inference: Durante: canary único por dominio, gates automáticos, comunicación a soporte/ventas con “qué cambia” y “cómo apagar”.
- Inference: Post: cleanup de flags (remover cuando llegue a 100% estable), retro (postmortem) si hubo degradación, actualización de runbooks.

***

## Anti-patterns

Fact: SRE advierte que before/after evaluation (comparar antes vs después en el tiempo) es riesgoso por ruido temporal y atribución débil.
Inference: Anti-patterns típicos en CRM:

- “Flag eterno” sin owner ni expiración (deuda + rutas sin test).
- Canary sin control comparable (sin segmentación por tenant/versión) → decisiones a ciegas.
- Mezclar migración destructiva + activación funcional en el mismo release (rollback imposible).
- Roll forward apurado bajo presión (más cambios sobre un estado inestable).
- Blue/green sin validar colas/jobs/consistencia → doble procesamiento o pérdidas.

***

## Diagnostic questions

Fact: SRE indica que para canary necesitas método de desplegar a subset, proceso de evaluación y su integración al release process.
Inference: Preguntas para diagnosticar madurez (CRM multi-tenant):

- ¿Puedes apagar una feature **por tenant** en menos de 5 minutos sin deploy?
- ¿Tienes auditoría de “quién cambió qué flag, cuándo y en qué entorno”, y puedes reconstruir el estado durante un incidente?[^5][^4]
- ¿Tu canary compara canary vs control con métricas segregadas por versión y tenant?[^1]
- ¿Tu estrategia de schema garantiza rollback seguro (fase compatible + fase feature)?[^1]
- ¿Cuántos flags activos están vencidos o sin owner (flag debt), y cada cuánto haces auditoría?[^6]

***

## Sources (y adiciones a SOURCES.md)

Fact: SRE Workbook documenta canarying, selección de métricas, y explica blue/green y sus tradeoffs.
Fact: Google CRE documenta filosofía de rollbacks, riesgos de roll forward bajo presión, y estrategia para cambios incompatibles (feature-free release).[^1]
Fact: LaunchDarkly describe audit log y su utilidad para trazabilidad de cambios de flags, y su documentación expone acceso/filtrado vía API.[^4][^5]
Fact: Unleash relaciona trunk-based con flags para mantener trunk deployable y permitir desactivación rápida.[^2]
Fact: Una guía 2026 de buenas prácticas de flags recomienda auditorías periódicas para reducir flag debt.[^6]

**Añadir a `SOURCES.md` (sin duplicados; Accessed: 2026-02-18):**

- Google SRE Workbook — “Canarying Releases”: https://sre.google/workbook/canarying-releases/
- Google Cloud Blog (CRE/SRE) — “Reliable releases and rollbacks—CRE life lessons”: https://cloud.google.com/blog/products/gcp/reliable-releases-and-rollbacks-cre-life-lessons
- LaunchDarkly Blog — “Launched: Audit Log”: https://launchdarkly.com/blog/launched-audit-log/
- LaunchDarkly Docs — “Audit Log API”: https://launchdarkly.com/docs/api/audit-log
- Unleash Docs — “Implement trunk-based development using feature flags”: https://docs.getunleash.io/guides/trunk-based-development
- DesignRevision — “Feature Flags Best Practices (2026)”: https://designrevision.com/blog/feature-flags-best-practices

***

## Key takeaways for PM practice

- Define “rollbackable” como requisito de producto para features críticas del CRM (no solo “shipping”).
- Exige gobernanza de flags (owner, expiración, RBAC, auditoría) como parte del “Definition of Done”.
- Diseña releases en 2 fases cuando hay datos: compatibilidad primero, activación después (por tenant).
- Canary por tenant/cohorte + métricas segregadas por versión/flag: es la forma más realista de controlar riesgo en multi-tenant.
- Decide blue/green con criterios de costo/estado (jobs, colas, caches), no por preferencia del equipo.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: pasted-text.txt

[^2]: https://docs.getunleash.io/guides/trunk-based-development

[^3]: https://www.getunleash.io/blog/how-to-implement-trunk-based-development-a-practical-guide

[^4]: https://launchdarkly.com/blog/launched-audit-log/

[^5]: https://launchdarkly.com/docs/api/audit-log

[^6]: https://designrevision.com/blog/feature-flags-best-practices

[^7]: https://flagbase.com/blog/intro-to-advance-deployments-using-feature-flags/

[^8]: https://dev.to/marianocodes/por-que-trunk-based-development-i5n

[^9]: https://blog.damavis.com/branching-en-git-github-flow-gitflow-y-trunk-based-development/

[^10]: https://gist.github.com/AppleBoiy/6ae4118d558d1f1d685015fdf3a06339

[^11]: https://www.justaftermidnight247.com/insights/site-reliability-engineering-sre-best-practices-2026-tips-tools-and-kpis/

[^12]: https://www.linkedin.com/pulse/multi-tenant-architecture-building-everyone-breaking-one-manoj-sharma-boyvf

[^13]: https://www.firefly.ai/academy/devops-best-practices

[^14]: https://thinkinglabs.io/articles/2025/08/10/so-yes-trunk-based-development-now-what.html

[^15]: https://swetrix.com/blog/feature-flagging-best-practices

[^16]: https://octopus.com/devops/software-deployments/progressive-delivery/

[^17]: https://www.harness.io/harness-devops-academy/trunk-based-development

[^18]: https://frontegg.com/blog/feature-flag-best-practices

[^19]: https://leaddev.com/technical-direction/why-openfeature-central-modern-feature-management

[^20]: https://cloud.google.com/blog/products/gcp/reliable-releases-and-rollbacks-cre-life-lessons

[^21]: https://launchdarkly.com/features/feature-flags/

[^22]: https://signoz.io/blog/openfeature/

[^23]: https://sre.google/workbook/canarying-releases/

[^24]: https://openfeature.dev/blog/catering-to-the-client-side

[^25]: https://sre.google/sre-book/service-best-practices/

[^26]: https://launchdarkly.com/docs/guides/flags/flag-hierarchy

[^27]: https://openfeature.dev/blog/openfeature-a-standard-for-feature-flagging

