<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_07 — Observabilidad para delivery y CRM (SLOs, error budgets, release markers)

## Executive summary (10–15 líneas)

**Facts:** Los SLOs definen el nivel objetivo de servicio y permiten derivar un error budget (tolerancia a fallo) para tomar decisiones de entrega con control de riesgo.[^1][^2]
**Facts:** Un error budget se calcula como $1 - SLO$ (ej.: 99.9% ⇒ 0.1% de presupuesto de error).[^1]
**Facts:** Alertar “sobre SLOs” busca señales accionables y reduce ruido frente a alertas sueltas por métricas aisladas.[^3]
**Facts:** OpenTelemetry usa propagación de contexto para correlacionar señales (traces, métricas, logs) y puede inyectar Trace ID/Span ID en logs para verlos “en contexto”.[^4]
**Facts:** Los deployment/release markers (p. ej., anotaciones en dashboards) permiten ver si un cambio coincide con variaciones en métricas.[^5]
**Facts:** Argo Rollouts soporta análisis con proveedores de métricas y puede promover/pausar o hacer rollback automático si las métricas indican fallo.[^6]
**Facts:** Herramientas APM como Datadog pueden correlacionar rendimiento por versión usando un tag de versión y mostrar métricas tipo RED por versión para detectar regresiones.[^7]
**Inferences:** En un CRM enterprise (B2B), esto habilita “venta + operación” más confiable: menos incidentes en horas pico, más previsibilidad en releases, y mejor postura ante objeciones de agencias (“no me rompas la operación”).
**Inferences:** La palanca práctica es conectar release→telemetría (marcadores + versión + trazas) y gobernar el delivery con políticas de error budget (gating) y rollback automatizable.

***

## Definitions and why it matters

**Facts:** SLO (Service Level Objective) es el objetivo medible del servicio; al implementarlo, se usa para derivar un error budget y una política de qué hacer cuando se agota.[^2]
**Facts:** Error budget es $1 - SLO$ y representa cuánto “mal servicio” es aceptable en una ventana; si se consume, se prioriza confiabilidad sobre features.[^1]
**Inferences:** Para un CRM, el “servicio” no es la app completa: son journeys críticos de agencias (login, búsqueda, cotización, emisión, conciliación), y cada uno debe tener SLO propio por impacto comercial.
**Inferences:** “Observabilidad para delivery” importa porque conecta cambios (release) con resultado (métricas) y te deja decidir rápido: continuar, pausar, o revertir con evidencia.

***

## Principles and best practices (con citas por sección + fecha)

Fecha de verificación: 2026-02-18.[^1]

**Facts:** Define SLOs primero y explícita una política de error budget para gobernar decisiones cuando la confiabilidad cae.[^2][^1]
**Facts:** Convierte SLOs en alertas accionables para mejorar precisión/recall y reducir alert fatigue.[^3]
**Facts:** Usa correlación entre señales (traces/métricas/logs) con propagación de contexto; OTel puede correlacionar logs con trazas inyectando Trace ID y Span ID en el log record.[^4]
**Facts:** Marca releases/deployments en los dashboards (anotaciones) para ver cambios en series temporales alineados a eventos.[^5]
**Facts:** Implementa progressive delivery con análisis y umbrales; un rollout puede avanzar si métricas están “bien” o hacer rollback automático si muestran fallo.[^6]
**Facts:** Para correlación release→métricas, captura la versión desplegada; Datadog usa un tag `version` para agregar performance por versión y comparar RED metrics entre versiones.[^7]

**Inferences (decisiones “safe vs aggressive”):**

- Opción segura: error budget gating “soft” (avisa/requiere aprobación) + rollback manual guiado por SLO (evitas rollback por falsos positivos).
- Opción agresiva: gating “hard” (bloquea) + rollback automático si se viola SLO/burn-rate por N minutos (maximiza protección operativa, puede frenar velocidad si la instrumentación es débil).

***

## Examples (aplicado a CRM enterprise)

**Facts:** Datadog permite comparar rendimiento por versión (RED metrics) para detectar problemas introducidos por un deployment.[^7]
**Facts:** Grafana soporta anotaciones en visualizaciones para “marcar” eventos (como despliegues) sobre los gráficos.[^5]
**Facts:** Argo Rollouts puede basar promoción/rollback en análisis de métricas con umbrales.[^6]
**Inferences (3 escenarios concretos):**

1) **Journey “Búsqueda + cotización” (agencias):**
    - SLI: % requests OK + latencia p95/p99 de endpoints de búsqueda/cotización.
    - Release marker: “crm-search vX.Y.Z” en el dashboard; si sube p99 y cae conversión de cotización, congelas releases por política de error budget y evalúas rollback.
2) **Integración crítica (GDS / consolidadores / pagos):**
    - SLI: ratio de errores por proveedor + tiempo de respuesta por proveedor, segmentado por versión (cuando aplique).
    - Progressive delivery: canary 10%→50%→100% con análisis; si el SLI empeora, rollback automático del rollout.
3) **Operación de backoffice (emisión / reemisiones):**
    - SLI: tasa de fallas en emisión + tiempo de confirmación; alertas SLO para evitar “incendios” en horarios pico.
    - Correlación: al abrir incidente, navegas de métrica→trace→logs correlacionados (Trace ID/Span ID) para llegar a causa raíz más rápido.[^4]

**Incluye / No incluye / Sensible (B2B real):**

- **Incluye:** SLOs por journey, política de error budget, markers de release, dashboards, alertas SLO, y rollback por umbrales.[^2][^6][^5]
- **No incluye:** definir SLAs comerciales con clientes finales (eso requiere legal/comercial y negociación por mercado).
- **Sensible:** si tus SLIs están mal definidos (p. ej., miden “CPU OK” pero no “cotización OK”), el gating/rollback automatizado puede tomar decisiones equivocadas.

***

## Metrics / success signals

**Facts:** Alertar desde SLOs apunta a alertas accionables con mejor señal/ruido.[^3]
**Facts:** El estado del error budget deriva del SLO (por definición $1 - SLO$).[^1]
**Inferences (qué mirar en delivery + CRM):**

- Confiabilidad: % cumplimiento SLO por journey, error budget restante, burn rate (consumo acelerado).
- Velocidad con control: lead time de cambios, frecuencia de deploy, y % releases bloqueados por política (indicador de deuda de confiabilidad).
- Calidad de cambios: change failure rate (regresiones por release), tasa de rollbacks, tiempo medio a detectar (MTTD) y a recuperar (MTTR).
- Operación comercial: tickets de agencias post-release, caída de conversión en cotización/emisión durante ventana de despliegue.

***

## Operational checklist

**Facts:** OpenTelemetry permite correlacionar señales con propagación de contexto y correlación logs↔traces vía IDs.[^4]
**Facts:** Grafana permite anotar visualizaciones mediante queries de anotaciones.[^5]
**Facts:** Argo Rollouts puede pausar/progresar/rollback basado en análisis de métricas.[^6]
**Facts:** Datadog agrega performance por versión con `version` tag y muestra RED metrics por versión.[^7]
**Inferences (pasos ejecutables):**

1) Define 5–10 **journeys** críticos del CRM (agencias) y sus SLIs (éxito + latencia).
2) Fija SLOs por journey y formaliza política de error budget (qué se bloquea, qué requiere aprobación, qué se permite).[^2][^1]
3) Instrumenta trazas y logs con correlación (propagación de contexto; Trace/Span IDs en logs).[^4]
4) Estandariza release metadata: versión, entorno, región; asegúrate de que se refleje en APM/metrics (p. ej., por tag de versión).[^7]
5) Emite release markers: anotación en dashboards y/o evento de deployment en tu stack.[^5]
6) Dashboards mínimos (ver abajo) + alerting por SLO (no por “CPU alta” aislada).[^3]
7) Progressive delivery con análisis y umbrales; habilita rollback automático donde el costo de fallo sea alto.[^6]

***

## Anti-patterns

**Facts:** El enfoque de alerting sobre SLOs busca alertas accionables y reduce ruido.[^3]
**Facts:** Los marcadores (anotaciones) ayudan a relacionar eventos (deploy) con series de métricas.[^5]
**Inferences (lo que más rompe CRM + delivery):**

- “Observabilidad = dashboards bonitos”: sin SLOs y sin política de error budget, no hay decisión operativa.[^2][^1]
- Alertas por infraestructura (CPU/mem) sin contexto de journey: mucho ruido, poca acción.[^3]
- No marcar releases: post-mortems eternos (“¿qué cambió?”) y baja trazabilidad.[^5]
- Rollback automático sin ventanas/criterios robustos: flapping (rollback↔redeploy) y pérdida de confianza del equipo/comercial.
- SLIs que no representan valor B2B (miden uptime pero no “cotización OK”): pasan “verdes” mientras agencias sufren.

***

## Diagnostic questions

**Facts:** SLOs se implementan para derivar error budgets y guiar políticas cuando se consumen.[^1][^2]
**Facts:** Argo Rollouts puede decidir promoción/rollback por umbrales de métricas.[^6]
**Inferences (preguntas para aterrizarlo en tu CRM):**

- ¿Cuáles 3 journeys de agencia generan más margen y deben tener SLO primero (cotizar, emitir, cobrar)?
- ¿Qué umbral de error budget consumido dispara “freeze de releases” y quién aprueba excepciones?[^2][^1]
- ¿Puedes ir de una caída en conversión → métrica → trace → logs correlacionados en <5 minutos?[^4]
- ¿Tus releases quedan visibles como eventos en los dashboards para correlación inmediata?[^5]
- ¿Qué componentes ameritan rollback automático vs manual (por costo de error y riesgo de falsos positivos)?[^6]

***

## Dashboards recomendados

**Facts:** Datadog ofrece gráficos out-of-the-box para ver RED metrics por versión (útil para comparar releases).[^7]
**Facts:** Grafana permite anotaciones sobre paneles para marcar eventos como despliegues.[^5]
**Inferences (set mínimo de tableros):**

- **SLO Overview (CRM):** SLO compliance por journey, error budget restante, burn rate, top contributors (endpoint/proveedor).
- **Release Health:** paneles RED (requests, errors, duration) segmentados por versión/entorno, con release markers encima.[^7][^5]
- **Journey Drilldown:** trazas por endpoint crítico, distribución de latencia, errores por dependencia, logs correlacionados por Trace ID.[^4]
- **Integraciones/Proveedores:** éxito/latencia por proveedor (GDS, pagos, consolidadores), rate limits, timeouts.
- **Progressive Delivery / Canary:** estado del rollout, umbrales de análisis, decisiones (promote/pause/rollback) y motivo.[^6]

***

## Sources (o referencia a SOURCES.md)

**Facts (fuentes usadas):** Google SRE Workbook (SLOs, error budgets, alerting), OpenTelemetry Docs (context propagation/correlación), Argo Rollouts Docs (analysis/rollback), Grafana Docs (annotations), Datadog (deployment tracking/version tag).[^1][^2][^3][^4][^7][^6][^5]

**SOURCES.md — entradas a añadir (sin duplicados):**

- Google SRE Workbook — “Error Budget Policy for Service Reliability”: https://sre.google/workbook/error-budget-policy/[^1]
- Google SRE Workbook — “Implementing SLOs”: https://sre.google/workbook/implementing-slos/[^2]
- Google SRE Workbook — “Alerting on SLOs”: https://sre.google/workbook/alerting-on-slos/[^3]
- OpenTelemetry Docs — “Context propagation”: https://opentelemetry.io/docs/concepts/context-propagation/[^4]
- Argo Rollouts Docs — “Architecture” (analysis/rollback descrito): https://argo-rollouts.readthedocs.io/en/stable/architecture/[^6]
- Grafana Docs — “Annotate visualizations”: https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/annotate-visualizations/[^5]
- Datadog Blog — “Monitor code deployments with Deployment Tracking…”: https://www.datadoghq.com/blog/datadog-deployment-tracking/[^7]

***

## Key takeaways for PM practice

- Amarra roadmap a confiabilidad con **SLOs + error budgets**: es el puente entre “quiero sacar features” y “no puedo romper operación B2B”.[^2][^1]
- Exige release→métrica: markers en dashboards + performance por versión, para decidir rápido si un release es “culpable”.[^7][^5]
- Alerting por SLO reduce ruido y mejora la conversación negocio-operación (“se está quemando el budget del journey de emisión”).[^3][^1]
- Rollback automático es viable cuando hay umbrales de análisis confiables y progressive delivery; si no, empieza con gating/rollback manual.[^6]
- OpenTelemetry (context propagation) habilita el “drilldown” real: de síntoma a causa, uniendo métricas, trazas y logs con IDs correlacionados.[^4]
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://sre.google/workbook/error-budget-policy/

[^2]: https://sre.google/workbook/implementing-slos/

[^3]: https://sre.google/workbook/alerting-on-slos/

[^4]: https://opentelemetry.io/docs/concepts/context-propagation/

[^5]: https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/annotate-visualizations/

[^6]: https://argo-rollouts.readthedocs.io/en/stable/architecture/

[^7]: https://www.datadoghq.com/blog/datadog-deployment-tracking/

[^8]: pasted-text.txt

[^9]: https://www.opentext.com/es/products/core-application-observability

[^10]: https://bindplane.com

[^11]: https://oneuptime.com/blog/post/2026-02-17-how-to-establish-error-budget-policies-for-release-gating-on-google-cloud/view

[^12]: https://oneuptime.com/blog/post/2026-02-06-opentelemetry-signal-correlation-traces-logs-metrics/view

[^13]: https://engineering.empathy.co/progressive-delivery-argo-rollouts-adoption/

[^14]: https://www.nobl9.com/resources/a-complete-guide-to-error-budgets-setting-up-slos-slis-and-slas-to-maintain-reliability

[^15]: https://opentelemetry.io/docs/concepts/signals/traces/

[^16]: https://argo-rollouts.readthedocs.io/en/stable/features/analysis/

[^17]: https://www.devopsinstitute.com/site-reliability-engineering-key-concepts-slo-error-budget-toil-and-observability/

[^18]: https://opentelemetry.io/docs/specs/otel/logs/

[^19]: https://dev.to/wesley_skeen/add-deployment-annotations-to-grafana-dashboards-hag

[^20]: https://mybinder-sre.readthedocs.io/en/latest/components/dashboards.html

[^21]: https://github.com/newrelic/deployment-marker-action

[^22]: https://oneuptime.com/blog/post/2026-01-30-grafana-annotations-advanced/view

[^23]: https://www.datadoghq.com/about/latest-news/press-releases/datadog-releases-deployment-tracking/

[^24]: https://www.bionconsulting.com/blog/new-relic-change-tracking

[^25]: https://community.grafana.com/t/prometheus-and-deploy-annotations/30113

[^26]: https://docs.datadoghq.com/tracing/services/deployment_tracking/

[^27]: https://www.amaysim.technology/blog/deployment-markers-in-new-relic-for-a-mono-repo

[^28]: https://grafana.com/docs/plugins/grafana-jira-datasource/latest/annotations/

[^29]: https://www.datadoghq.com/blog/serverless-changes/

