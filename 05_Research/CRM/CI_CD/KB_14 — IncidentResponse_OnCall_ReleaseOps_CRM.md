<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# crea KB_14_IncidentResponse_OnCall_ReleaseOps_CRM.md. Investiga mejores prácticas 2024–2026 para operar CI/CD y releases en sistemas enterprise (SRE/Release Engineering) aplicadas a un CRM multi-tenant. Quiero: modelo de on-call, severidades, runbooks, criterios “rollback primero”, release freeze, gestión de cambios de emergencia, postmortems sin culpa, y cómo instrumentar esto con evidencias auditables (quién hizo qué, cuándo).

Incluye: checklists accionables, plantillas (runbook/postmortem), métricas (MTTR, change failure rate, rollback rate), y anti-patrones.
Entrega en Markdown RAG-ready con estructura estándar KB (Executive summary, Definitions, Principles, Examples CRM, Metrics, Checklist, Anti-patterns, Diagnostic questions, Sources + entradas para SOURCES.md).

```markdown
# KB_14_IncidentResponse_OnCall_ReleaseOps_CRM

## Executive summary (10–15 líneas)

[Facts] Las métricas DORA siguen siendo el lenguaje común para discutir performance y riesgo de cambios en CI/CD (p. ej., change failure rate y “failed deployment recovery time”, antes llamado MTTR en DORA). [web:2][web:4]  
[Inference] En un CRM multi-tenant enterprise, el objetivo operativo no es “cero incidentes”, sino reducir blast radius por tenant, recuperar rápido y dejar evidencia auditable de cada cambio (quién/hizo-qué/cuándo) para cumplir compliance y responder a clientes B2B.  
[Facts] La cultura de postmortems “sin culpa” busca enfocarse en “qué” falló en el sistema y en acciones para mejorar el sistema (no culpar personas). [web:10][web:13]  
[Inference] Un buen modelo de on-call para ReleaseOps/SRE en SaaS multi-tenant separa: incident commander (IC), subject matter experts (SME), y owner de cambio; y define gatillos claros para “rollback primero” cuando el tiempo corre en contra.  
[Facts] GitHub audit logs registran eventos con actor, acción, repositorio, fecha/hora y (en enterprise) contexto de identidad como SAML/SCIM, útil para trazabilidad y auditoría. [web:32][web:42]  
[Facts] GitHub Actions permite “deployment protection rules” (aprobaciones/rechazos) para jobs que despliegan a un environment, dejando control explícito de aprobación antes de desplegar. [web:46]  
[Inference] Para agencias/partners enterprise (B2B), “release freeze” y “cambios de emergencia” deben ser políticas operables: reglas simples, excepciones trazables, y evidencia automática en el pipeline.  
[Facts] En ITIL, los cambios de emergencia se canalizan con autorización acelerada (p. ej., ECAB) y documentación proporcional al riesgo/urgencia. [web:26][web:29]  
[Inference] Si instrumentas bien, puedes correlacionar: PR/commit → build → aprobación → deploy → métricas/alertas → incidente → rollback/fix → postmortem; y convertir eso en prueba audit-ready sin trabajo manual.

---

## Definitions and why it matters

[Facts] **Change failure rate (CFR)**: porcentaje de despliegues que causan fallas en producción. [web:2][web:4]  
[Facts] **Failed deployment recovery time** (antes “MTTR” en el marco DORA): tiempo para recuperar/volver a un estado saludable tras un despliegue fallido. [web:4]  
[Inference] **Rollback primero**: heurística operativa donde la acción por defecto ante degradación atribuible a un cambio reciente es revertir (o cambiar tráfico a versión anterior) antes de intentar “debug en vivo”, salvo excepciones explícitas.  
[Inference] **Release freeze**: ventana donde se restringen releases/cambios (total o parcial) para proteger periodos críticos (picos comerciales, cierres contables, campañas), con un mecanismo formal de excepción.  
[Facts] **Blameless postmortem**: práctica de análisis posterior al incidente que evita culpar individuos y se centra en debilidades del sistema/proceso y acciones correctivas. [web:10][web:13]  
[Inference] En un **CRM multi-tenant**, estas definiciones importan porque el costo real del incidente es: churn enterprise, penalizaciones SLA, escalamiento soporte, y pérdida de confianza; y porque el blast radius puede ser “un tenant VIP” aunque el resto esté estable.

---

## Principles and best practices (con citas por sección + fecha)

### 1) Modelo de on-call (SRE/ReleaseOps) — 2026-02

[Inference] Diseña el on-call como una “línea de producción”: un Primary (24/7) + Secondary (backup) + SME rotativo (DB, infra, app) y un rol de Incident Commander (IC) que no hace troubleshooting profundo, solo coordina.  
[Inference] Define **handoff** obligatorio: contexto mínimo, estado actual, próximos pasos, riesgo y ETA; si no hay handoff, se asume rollback/congelación.  
[Inference] Separa “on-call de incidentes” vs “on-call de releases” si tienes suficiente volumen; si no, rota por semanas pero con ventanas de deploy acotadas.

**Severidades sugeridas (operables en SaaS multi-tenant)**  
[Inference] Sev0: riesgo legal/seguridad o caída masiva, Sev1: degradación severa multi-tenant o tenant estratégico, Sev2: bug con workaround, Sev3: issue menor/soporte.  
[Inference] Para cada severidad: define tiempos (ack, update cadence, mitigación), quién aprueba cambios, y si aplica freeze automático.

---

### 2) Runbooks como producto (no docs) — 2026-02

[Facts] Google SRE recomienda postmortems y checklists que aseguren evaluación completa del impacto, análisis suficiente para definir acciones, y compartir aprendizaje; esto se apoya en materiales/checklists operativos. [web:10]  
[Facts] Un postmortem puede incluir timeline y “artefactos” (logs, gráficos, chats) como evidencia. [web:16]  
[Inference] Convierte runbooks en rutas de decisión: “si métrica X + síntoma Y → haz Z”, con prechecks/postchecks y comandos listos; y versiónalos en el mismo repo que el servicio (PR + review).  
[Inference] Mínimo 1 runbook por: rollback, feature-flag kill switch, degradación DB, saturación colas, incidentes de autenticación, y errores de migración.

---

### 3) “Rollback primero” (criterios y excepciones) — 2026-02

[Facts] Una práctica operable es **timebox**: intentar identificar/fijar en caliente por un tiempo corto y, si no se resuelve, ejecutar rollback para restaurar servicio. [web:27]  
[Facts] Estrategias modernas de rollback pueden apoyarse en patrones como blue/green (dos versiones en prod con conmutación de tráfico) y automatización basada en detección de errores. [web:17]  
[Inference] Define “rollback primero” como default cuando se cumpla: (a) hubo deploy en los últimos N minutos, (b) hay degradación en SLO/errores, (c) el cambio es reversible sin pérdida de datos, (d) la mitigación más rápida es volver a versión previa.  
[Inference] Excepciones explícitas (documentadas): cambios de esquema irreversibles, hotfix de seguridad donde rollback reabre una vulnerabilidad, o incidentes causados por dependencia externa (rollback no ayuda).

**Regla práctica (simple y vendible internamente)**  
[Inference] “Si no puedes demostrar en 15–30 min que fix-forward es más rápido y más seguro, ejecuta rollback”.

---

### 4) Release freeze y ventanas de riesgo — 2026-02

[Inference] Implementa freeze por **capas**, no “todo o nada”: código app (sí), config (depende), feature flags (permitidas), cambios de infraestructura (solo emergencia), cambios de esquema (no).  
[Inference] Dispara freeze automático cuando: CFR sube, incidentes Sev0/Sev1 activos, o hay eventos comerciales críticos; levanta freeze con criterios medibles (salud estable X horas, backlog P0 controlado).  
[Inference] Define un proceso de excepción: sponsor, motivo, evaluación rápida de riesgo, plan de rollback, ventana, aprobaciones y evidencia (ticket + aprobación en pipeline).

---

### 5) Gestión de cambios de emergencia (Emergency Change) — 2026-02

[Facts] ITIL plantea que un cambio de emergencia inicia con una solicitud de cambio y se revisa con un cuerpo de aprobación acelerada (ECAB), ponderando riesgo de ejecutar vs riesgo de esperar. [web:26]  
[Facts] Guías de ITIL describen pasos para autorización rápida y ejecución acelerada en cambios de emergencia. [web:29]  
[Inference] En SaaS enterprise, “emergency change” debe ser una **clase de cambio** con controles mínimos obligatorios: (1) ticket, (2) aprobación (ECAB/autoridad), (3) evidencia del diff (PR/commit), (4) plan de rollback, (5) post-implementation review en 24–72h.  
[Inference] Evita que “emergencia” sea sinónimo de “me salté el proceso”: si no hay evidencia, no existe el cambio (y compliance te lo cobra luego).

---

### 6) Postmortems sin culpa (blameless) — 2026-02

[Facts] En la cultura SRE, los postmortems deben ser blameless y enfocarse en cómo mejorar sistemas, procedimientos y training, no en culpar individuos. [web:13]  
[Facts] Guías de Google SRE recomiendan usar lenguaje sin culpa, enfocarse en “what” vs “who”, y definir action items orientados a mejorar el sistema. [web:10]  
[Inference] Para que funcione en enterprise: establece “no castigo por reportar” + “sí exigencia por cerrar acciones”, con tracking y fechas; el aprendizaje sin ejecución no reduce reincidencia.

---

### 7) Evidencias auditables (quién hizo qué, cuándo) — 2026-02

[Facts] GitHub audit logs incluyen datos como actor, acción, repositorio, fecha/hora y (según setup) identidad SAML/SCIM, útiles para trazabilidad. [web:32][web:42]  
[Facts] El audit log retiene eventos del enterprise/organización por una ventana (p. ej., 180 días), y se puede consultar por rango de fechas usando parámetros de búsqueda. [web:35][web:42]  
[Facts] GitHub Actions permite aprobar o rechazar despliegues en environments con “Review deployments”, dejando un control explícito antes de ejecutar el job de deploy. [web:46]  
[Inference] Patrón audit-ready: “no deploy sin PR + revisión + environment approval + registro de cambio + correlación con observabilidad (release marker)”.  
[Inference] A nivel multi-tenant, agrega evidencia de “qué tenants fueron impactados”: logs con tenant_id, toggles por tenant, y reportes de blast radius (antes/durante/después).

---

## Examples (aplicado a CRM enterprise)

### Ejemplo A: Deploy rompe facturación de 1 tenant VIP

[Inference] Síntoma: subida de errores 5xx solo para `tenant_id=ACME`, latencia normal para el resto; quejas directas del equipo de cuentas enterprise.  
[Inference] Decisión: Sev1 (tenant estratégico) aunque el sistema global esté “verde”; activar IC + SME app + SME DB; pausar releases (freeze parcial).  
[Inference] “Rollback primero”: si el deploy coincide con el inicio del error y el rollback es seguro (sin migración irreversible), revertir; si hay migración, activar feature-flag kill switch y plan de compensación.

**Checklist operativa (mini-runbook)**  
[Inference] 1) Confirmar blast radius: dashboard por `tenant_id`, error budget burn por tenant, endpoints críticos.  
[Inference] 2) Congelar releases: bloquear merge/deploy a prod salvo ECAB.  
[Inference] 3) Mitigar: rollback o switch de tráfico (blue/green) o desactivar feature por tenant.  
[Inference] 4) Verificar: smoke tests por tenant, métricas vuelven a baseline, confirmar con soporte/CS.  
[Inference] 5) Evidencia: link a PR/deploy, aprobación, timestamp, logs y gráfico “before/after”.

---

### Ejemplo B: Cambio de emergencia por incidente de autenticación (multi-tenant)

[Inference] Síntoma: login falla para múltiples tenants; impacto transversal → Sev0/Sev1 según alcance.  
[Inference] Proceso: abrir “Emergency Change” (ticket), aprobar ECAB, aplicar hotfix con pruebas mínimas + plan de rollback, post-implementation review obligatoria.

**Evidencia mínima exigible**  
[Inference] Ticket ID + motivo, PR/commit hash + reviewer, aprobación del environment, ventana de despliegue, verificación post-deploy (métricas y logs), y seguimiento de acciones postmortem.

---

## Metrics / success signals

[Facts] DORA define **change fail rate** como porcentaje de despliegues que causan fallas en producción. [web:2][web:4]  
[Facts] DORA documenta la evolución de “MTTR” hacia “failed deployment recovery time” en su historia de métricas. [web:4]  
[Inference] Métricas núcleo (con metas por servicio/tenant tier):
- **MTTR/Failed deployment recovery time**: P50/P90, por severidad y por tipo de cambio (app/config/db).
- **Change failure rate (CFR)**: por servicio y por equipo, y por ventana (7/30/90 días).
- **Rollback rate**: rollbacks por 100 deploys (y ratio rollback automático vs manual).
- **Emergency change rate**: % de cambios marcados como emergencia (si sube, hay deuda de calidad/proceso).
- **Freeze exceptions**: cuántas excepciones se aprobaron y cuántas generaron incidente.

[Inference] Señales de madurez (lo que quieres ver): CFR baja sin caer en “fear-driven freeze”, MTTR baja por automatización (runbooks + traffic shifting), y disminución de emergencias a medida que mejora la calidad del release process.

---

## Operational checklist

### Pre-release (antes de desplegar)

[Inference] Definir severidad esperada si falla (qué se rompe, qué tenants), y plan de rollback validado.  
[Inference] Confirmar compatibilidad multi-tenant: migraciones forward/backward, toggles por tenant, y límites de rate/quotas.  
[Inference] Asegurar evidencia: PR link, reviewers, ticket de cambio, checklist de pruebas, y “release marker” para observabilidad.

### During release (durante despliegue)

[Inference] Canary por cohort/tenant (si aplica), monitoreo de errores/latencia por tenant_id, y “stop-the-line” si se quema error budget.  
[Inference] Si hay degradación: aplicar regla “rollback primero” con timebox; documentar decisión en el canal del incidente.

### Incident response (cuando ya hay incidente)

[Inference] Nombrar IC, declarar severidad, establecer cadencia de updates, y fijar objetivo inmediato: restaurar servicio.  
[Inference] Ejecutar runbook (rollback/kill-switch) y registrar artefactos: links, timestamps, gráficos, comandos/outputs relevantes.

### Post-incident (24–72h)

[Facts] Postmortem blameless: describir qué ocurrió, timeline y acciones enfocadas en mejorar el sistema, no culpar personas. [web:10][web:13]  
[Facts] Un postmortem puede incluir timeline y enlaces a evidencias (logs, gráficos, chats). [web:16]  
[Inference] Cerrar acciones con due date + owner + prioridad; no se considera “cerrado” sin verificación (control de reincidencia).

---

## Anti-patterns

[Inference] “Freeze eterno”: bloquear releases por miedo, sin resolver causas raíz (solo acumula riesgo).  
[Inference] “Emergencia” como atajo habitual: si todo es emergencia, nada es controlado (y compliance lo detecta).  
[Inference] Runbooks “bonitos” pero no ejecutables: pasos incompletos, sin comandos, sin prechecks, sin ownership.  
[Inference] Rollback sin compatibilidad de datos: migraciones no reversibles sin estrategia (terminas en incidente más largo).  
[Inference] Postmortem performativo: sin acciones, sin seguimiento, o centrado en “quién falló”.

---

## Diagnostic questions

[Inference] ¿Tu on-call tiene autoridad real para pausar releases y ejecutar rollback sin pedir “permiso político” en medio del incidente?  
[Inference] ¿Puedes demostrar en 5 minutos (con links) quién aprobó y quién desplegó el último cambio en prod, y a qué hora?  
[Inference] ¿Tienes un criterio objetivo de “rollback primero” (timebox + condiciones) o depende del humor del momento?  
[Inference] ¿Tu CRM puede “apagar” features por tenant sin redeploy (kill switch) y con auditoría del cambio?  
[Inference] ¿Cuántos cambios de emergencia hiciste en los últimos 30 días y cuántos generaron incidentes posteriores?

---

## Sources (o referencia a SOURCES.md)

[Facts] DORA Metrics Guide (definiciones actuales de CFR y métricas relacionadas). [web:2]  
[Facts] DORA Metrics History (renombre/ajustes de MTTR → failed deployment recovery time). [web:4]  
[Facts] Google SRE: Postmortem culture y prácticas blameless. [web:10]  
[Facts] Google SRE: incident management guide (tenet: postmortems blameless). [web:13]  
[Facts] Google SRE: ejemplo de postmortem y artefactos/timeline. [web:16]  
[Facts] GitHub Docs: audit log (campos actor/acción/fecha/identidad) y retención/consulta por fecha. [web:32][web:35][web:42]  
[Facts] GitHub Docs: reviewing deployments (aprobación/rechazo de despliegues por environments). [web:46]  
[Facts] ITIL emergency change / ECAB (explicación del flujo de emergencia). [web:26][web:29]  
[Facts] Rollback decisioning con timebox (fix-forward vs rollback). [web:27]  
[Facts] Rollback strategies (blue/green, detección de errores, automatización). [web:17]  

---

## Plantillas (listas para copiar/pegar)

### Plantilla: Runbook (Rollback / Kill-switch)

[Inference]
**Título:** Rollback / Feature Kill-switch — Servicio X (CRM multi-tenant)  
**Objetivo:** Restaurar servicio en < N minutos minimizando blast radius.  
**Severidades:** Sev0/Sev1/Sev2 aplicables.  
**Triggers (ejemplos):** 5xx > umbral, latencia P95 > umbral, errores concentrados en tenant VIP.  
**Prechecks:** confirmar último deploy, confirmar si hubo migración, identificar tenants impactados.  
**Acción A — Rollback:** pasos exactos (comandos), verificación, criterio de éxito, criterio de abortar.  
**Acción B — Kill-switch por tenant:** toggle, alcance, TTL, verificación, comunicación a soporte.  
**Postchecks:** smoke tests por tenant tier, dashboards, error budget burn.  
**Evidencia:** ticket, PR/commit, aprobación, timestamps, links a logs/graphs.

### Plantilla: Postmortem blameless

[Facts] Guías SRE recomiendan enfocarse en “what not who”, usar lenguaje sin culpa, y definir action items orientados a mejorar el sistema; además se suele incluir timeline y evidencia. [web:10][web:16]  
[Inference]
**Resumen del impacto:** qué pasó, quién fue impactado (tenants), duración, severidad.  
**Timeline (UTC):** detección → declaración → mitigación → recuperación → cierre.  
**Root cause vs Trigger:** causa sistémica y evento detonante (separados).  
**Qué funcionó / qué no funcionó:** herramientas, comunicación, runbooks.  
**Acciones (priorizadas):** Prevent/Mitigate/Detect, owner, due date, verificación.  
**Evidencia:** links a PR/deploy, approvals, dashboards, logs, tickets, transcript del canal.  
**Seguimiento:** fecha de review y criterio de “acción cerrada”.

---

## Añadidos para SOURCES.md (sin duplicados)

- DORA — “DORA's software delivery performance metrics” https://dora.dev/guides/dora-metrics/ (consultado 2026-02-18)  
- DORA — “A history of DORA's software delivery metrics” https://dora.dev/guides/dora-metrics/history/ (consultado 2026-02-18)  
- Google SRE Workbook — “Postmortem Practices for Incident Management” https://sre.google/workbook/postmortem-culture/ (consultado 2026-02-18)  
- Google SRE — “Incident management guide” https://sre.google/resources/practices-and-processes/incident-management-guide/ (consultado 2026-02-18)  
- Google SRE Book — “Incident Postmortem Example” https://sre.google/sre-book/example-postmortem/ (consultado 2026-02-18)  
- GitHub Docs — “Reviewing the audit log for your organization” https://docs.github.com/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization (consultado 2026-02-18)  
- GitHub Docs — “Using the audit log for your enterprise” https://docs.github.com/en/enterprise-cloud@latest/enterprise-onboarding/govern-people-and-repositories/using-the-audit-log-for-your-enterprise (consultado 2026-02-18)  
- GitHub Docs — “Reviewing deployments” https://docs.github.com/actions/managing-workflow-runs/reviewing-deployments (consultado 2026-02-18)  
- InvGate Blog — “Emergency Change Control Process” https://blog.invgate.com/emergency-change-control-process (consultado 2026-02-18)  
- Virima — “ITIL types of changes… (incluye emergency change)” https://virima.com/blog/understanding-itil-types-of-changes-a-comprehensive-guide (consultado 2026-02-18)  
- xMatters — “After a deployment error: fix forward or roll back” https://www.xmatters.com/blog/after-a-deployment-error-should-you-fix-forward-or-roll-back (consultado 2026-02-18)  
- Octopus Deploy — “Modern Rollback Strategies” https://octopus.com/blog/modern-rollback-strategies (consultado 2026-02-18)  

---

## Key takeaways for PM practice

- Define “rollback primero” como política con timebox y excepciones explícitas; evita debates en caliente.  
- Congela releases por capas (código/config/db) y haz que las excepciones sean trazables, no heroicas.  
- Postmortems sin culpa + acciones con dueño y fecha: aprendizaje operativo medible.  
- Auditabilidad no es un documento: es una cadena de evidencias (PR → aprobación → deploy → métricas → incidente → postmortem).  
- En multi-tenant, severidad y prioridad deben considerar “tenant VIP” aunque el global esté estable.
```

<span style="display:none">[^1][^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^2][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^3][^30][^31][^32][^33][^34][^35][^36][^37][^38][^39][^4][^40][^41][^42][^43][^44][^45][^46][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: pasted-text.txt

[^2]: https://dora.dev/guides/dora-metrics/

[^3]: https://redmonk.com/rstephens/2024/11/26/dora2024/

[^4]: https://dora.dev/guides/dora-metrics/history/

[^5]: https://devopslaunchpad.com/blog/dora-report-2024/

[^6]: https://abstracta.us/blog/devops/dora-metrics-in-devops/

[^7]: https://raygun.com/blog/blameless-postmortems-part-two/

[^8]: https://hoop.dev/blog/audit-logs-in-github-ci-cd-the-key-to-secure-and-compliant-pipelines/

[^9]: https://circleci.com/blog/dora-metrics/

[^10]: https://sre.google/workbook/postmortem-culture/

[^11]: https://hoop.dev/blog/audit-logs-in-github-ci-cd-strengthening-your-controls/

[^12]: https://www.cloudbees.com/blog/dora-devops-metrics-bandwagon

[^13]: https://sre.google/resources/practices-and-processes/incident-management-guide/

[^14]: https://www.reddit.com/r/devops/comments/1j5kwo2/cicd_compliance_audit/

[^15]: https://www.multitudes.com/blog/dora-metrics

[^16]: https://sre.google/sre-book/example-postmortem/

[^17]: https://octopus.com/blog/modern-rollback-strategies

[^18]: https://sre.google/sre-book/release-engineering/

[^19]: https://www.statsig.com/perspectives/rollback-strategies-reverting-failed-experiments

[^20]: https://www.reddit.com/r/devops/comments/15zqc3f/how_do_you_handle_deployment_failures_fail_back/

[^21]: https://www.aviator.co/blog/best-practices-for-rollbacks-and-cherrypicks/

[^22]: https://www.myshyft.com/blog/schedule-freeze-periods/

[^23]: https://scrumbyte.com/emergency-change-management/

[^24]: https://www.xenonstack.com/insights/application-release-engineering

[^25]: https://monday.com/blog/service/it-release-management/

[^26]: https://blog.invgate.com/emergency-change-control-process

[^27]: https://www.xmatters.com/blog/after-a-deployment-error-should-you-fix-forward-or-roll-back

[^28]: https://www.faronics.com/news/blog/scaling-secure-seasonal-workforces-with-deep-freeze-cloud-best-practices-for-onboarding-offboarding

[^29]: https://virima.com/blog/understanding-itil-types-of-changes-a-comprehensive-guide

[^30]: https://www.harness.io/blog/understanding-software-rollbacks

[^31]: https://octopus.com/devops/software-deployments/release-management-process/

[^32]: https://docs.github.com/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization

[^33]: https://docs.github.com/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/identifying-audit-log-events-performed-by-an-access-token

[^34]: https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/audit-log-events-for-your-organization

[^35]: https://docs.github.com/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization

[^36]: https://github.blog/changelog/2022-09-09-new-audit-log-events-and-event-context/

[^37]: https://github.com/orgs/community/discussions/88692

[^38]: https://about.gitlab.com/direction/software_supply_chain_security/compliance/audit-events/

[^39]: https://docs.github.com/en/enterprise-server@3.14/admin/concepts/security-and-compliance/audit-log-for-an-enterprise

[^40]: https://github.com/orgs/community/discussions/30156

[^41]: https://software.rcc.uchicago.edu/git/help/administration/audit_events.md

[^42]: https://docs.github.com/en/enterprise-cloud@latest/enterprise-onboarding/govern-people-and-repositories/using-the-audit-log-for-your-enterprise

[^43]: https://oneuptime.com/blog/post/2026-01-25-github-actions-environment-protection-rules/view

[^44]: https://docs.gitlab.com/administration/compliance/audit_event_reports/

[^45]: https://documentation.wazuh.com/current/cloud-security/github/monitoring-github-activity.html

[^46]: https://docs.github.com/actions/managing-workflow-runs/reviewing-deployments

