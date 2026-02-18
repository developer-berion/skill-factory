<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_19_FinOps_CICD_CostControls_EphemeralEnvs (2024–2026)

## Executive summary (10–15 líneas)

**Facts:** En GitHub Actions, el costo se mide principalmente por minutos de ejecución y por almacenamiento (artefactos y cachés), con cobro por uso que excede lo incluido en el plan.[^1]
**Facts:** En GitHub Actions, el cache storage incluido por repositorio es 10 GB, y el cobro de caché se basa en el “peak usage” por hora.[^1]
**Facts:** GitHub Actions impone límites que impactan estrategia de paralelización/caching, por ejemplo: matriz máxima 256 jobs por workflow run y límite de 200 uploads de cache por minuto por repositorio.[^2]
**Facts:** En GitLab CI/CD, para que el caching funcione bien con múltiples runners/autoscaling, se recomienda cache distribuido (p. ej., S3) y aplicar lifecycle rules para borrar objetos de caché tras un período.[^3]
**Facts:** Para visibilidad de costo por “servicio” en Kubernetes (incluyendo entornos efímeros), OpenCost ofrece asignación por service/deployment/pod, etc., y busca estandarizar la asignación de costos.[^4][^5]
**Facts:** DORA define 4 métricas (frecuencia de despliegue, lead time, change failure rate, y tiempo de recuperación), y su investigación sostiene que velocidad y estabilidad no requieren trade-off.[^6][^7]
**Inferences:** Controlar costo de CI/CD sin degradar confiabilidad se logra combinando: optimización de runners, caching con TTL, paralelización con límites, presupuestos/budgets por repo/equipo, y chargeback/showback por servicio (repos + entornos).
**Inferences:** La práctica más rentable suele ser “medir y recortar desperdicio” (jobs redundantes, caches sin caducidad, ambientes efímeros sin auto-destrucción) antes de “comprar más runner”.
**Inferences:** Usa heurísticas “safe vs aggressive” para decidir cuánto apretar (p. ej., spot instances, auto-cancel, TTL corto) según criticidad, SLO y variabilidad del pipeline.

***

## Definitions and why it matters

**Facts:** En GitHub Actions, los minutos consumidos en repos privados se cargan al owner del repositorio/organización (no a quien dispara el workflow), y el storage se cobra por acumulación horaria (GB-Hours).[^1]
**Facts:** En GitHub Actions, la caché se mide por “peak usage” por hora y hay 10 GB incluidos por repositorio; por encima, hay costo si se configuró el límite por encima del incluido.[^1]
**Facts:** Un “ephemeral environment” es un entorno aislado y de vida corta, típicamente levantado por branch/PR/MR, para probar cambios sin afectar ambientes compartidos.[^8]
**Inferences:** “FinOps para CI/CD” = gobernar consumo (minutos, cómputo, storage, ambientes efímeros) con accountability por equipo/servicio, sin sacrificar el flujo (DORA) ni la confiabilidad (SLO).
**Inferences:** Importa porque CI/CD tiende a crecer “en silencio” (más repos, más PRs, más matrices, más artefactos), y el costo se vuelve una fuga recurrente si no hay guardrails operativos.

***

## Principles and best practices (con citas por sección + fecha)

### 1) Optimización de runners (2024–2026)

**Facts (2024-12-31):** En GitHub Actions, los self-hosted runners no consumen minutos facturables de GitHub Actions (la infraestructura igual cuesta, pero no como “Actions minutes”).[^1]
**Facts (2024-12-31):** Los costos por minuto varían por SKU/OS (p. ej., Linux vs Windows vs macOS), por lo que estandarizar Linux donde aplique reduce costo directo.[^1]
**Facts (2025-12-28):** Un patrón para bajar costo en runners autoscalados es usar Spot Instances; AWS reporta “hasta 90%” de reducción de costo en un enfoque con GitLab Runners en EKS Auto Mode + Spot.[^9]
**Inferences:**

- **Safe:** Rightsize y segmenta runners por “clase de job” (lint/unit vs integración vs build de imagen), define concurrencia máxima por repo/equipo, y estandariza imágenes base pre-calentadas (para reducir tiempo muerto).
- **Aggressive:** Autoscaling + Spot (o preemptibles) para workloads no críticos, con reintentos idempotentes y tolerancia a interrupciones; exige timeouts estrictos y fallbacks (on-demand) para pipelines de release.


### 2) Caching efectivo (dependencias, build, contenedores) (2024–2026)

**Facts (2025-11-25):** En GitLab, con múltiples runners/autoscaling conviene cache distribuido (p. ej., S3) y lifecycle rules para expirar objetos.[^3]
**Facts (2024-12-31):** En GitHub Actions existe límite por repositorio de 200 cache uploads por minuto y 1500 downloads por minuto, lo cual afecta estrategias “muy fragmentadas” de caché.[^2]
**Inferences:**

- **Safe:** Cachea dependencias “caras” y estables (package managers), usa claves por lockfile (no por commit), y TTL/retención definida (para evitar “cache bloat” y costos de storage).
- **Aggressive:** Cachea layers de Docker/buildkit y artefactos intermedios para recortar minutos, pero con políticas de expiración y controles de invalidación (si no, puedes bajar minutos y subir storage/costo de caché).


### 3) Paralelización con límites (y sin “explosión” de matriz) (2024–2026)

**Facts (2024-12-31):** En GitHub Actions, una job matrix puede generar hasta 256 jobs por workflow run.[^2]
**Facts (2024-12-31):** Existen límites de concurrencia por plan y otros límites de encolado/eventos, que pueden convertirse en “cuellos” si paralelizas sin control.[^2]
**Inferences:**

- **Safe:** Paraleliza por “shards” solo donde reduce wall-clock real (tests), y agrupa tareas pequeñas para reducir overhead de jobs; aplica concurrency groups por PR para evitar duplicar ejecuciones.
- **Aggressive:** Paralelización masiva solo para ramas críticas (main/release) y con sampling en PRs (por ejemplo, smoke tests + subset), dejando el full suite para merges o ventanas programadas.


### 4) Límites por repo/equipo + presupuestos (budgets) (2024–2026)

**Facts (2024-12-31):** GitHub Actions permite limitar gasto con budgets para productos medidos, y si no hay método de pago válido se bloquea el uso al agotar cuota.[^1]
**Facts (2024-12-31):** El cache storage incluido (10 GB por repo) y su cobro por peak hourly usage hacen que “repos ruidosos” puedan disparar costo si no se controla retención y tamaño de caché.[^1]
**Inferences:**

- **Safe:** Define budgets por organización y “alertas” por repo; agrega guardrails por equipo (máximo minutos/mes, máximo concurrencia, máximo tamaño de artefactos).
- **Aggressive:** “Showback/chargeback” interno por repo o por service owner (quien decide calidad vs costo), con revisiones quincenales de top pipelines por gasto.


### 5) Entornos efímeros (preview envs) con control de costo (2024–2026)

**Facts (2025-01-16):** Los entornos efímeros en CI/CD pueden ser resource-intensive, por lo que se recomienda una estrategia mixta (crearlos selectivamente) para balancear feedback vs capacidad/costo.[^10]
**Facts (2025-01-16):** Se destacan prácticas como monitorear y ajustar recursos según demanda para minimizar desperdicio, y automatizar su provisión/gestión con controles de acceso.[^10]
**Inferences:**

- **Safe:** Entornos efímeros solo para PRs etiquetados (o para features de alto riesgo), con TTL por defecto (p. ej., 4–24h) y auto-destrucción al cerrar PR.
- **Aggressive:** Entorno por PR para todo, pero con cuotas por equipo, hibernación automática, y “scale-to-zero”; si no puedes garantizar cleanup, no lo hagas.


### 6) Dashboards de costo por servicio (repos + Kubernetes) (2024–2026)

**Facts (2025-02-01):** GitHub migró endpoints de “workflow usage” hacia el “billing platform usage endpoint”, que resume uso por SKU, organización y repositorio.[^11]
**Facts (2022-11-27, ejemplo vigente en docs):** La API de GitHub para usage report puede devolver items con product=Actions, sku, unitType=minutes, pricePerUnit y amounts, incluyendo repositoryName.[^12]
**Facts (2024-10-30):** OpenCost busca dar visibilidad en tiempo real y asignación de costos por componentes de Kubernetes (incluyendo service/deployment/container) y estandarizar cost allocation.[^4]
**Inferences:**

- **Safe:** Dashboard “top spenders” por repo (Actions minutes + artefactos/caché) + costo por namespace/service (OpenCost) para entornos efímeros.
- **Aggressive:** Enlaza costo a ownership (CODEOWNERS/service catalog), y crea “cost SLO” (presupuesto mensual por servicio) con alertas que disparan acciones automáticas (bajar paralelismo, acortar TTL, bloquear re-runs no justificados).


### 7) Alineación costo con DORA/SLO (sin degradar confiabilidad) (2024–2026)

**Facts (2023-01-31):** DORA se apoya en 4 métricas: deployment frequency, lead time for changes, change failure rate y time to recover (recovery time).[^7]
**Facts (2024-11-25):** El mensaje consistente del reporte DORA es que no hace falta trade-off entre throughput y estabilidad (speed y stability se habilitan mutuamente).[^6]
**Facts (2025-12-28):** Un enfoque práctico es usar métricas de inestabilidad y SLOs de confiabilidad como contrapeso: ir más rápido, pero no a costa de estabilidad.[^13]
**Inferences:**

- Trata “costo” como tercera dimensión junto a throughput (DORA) y estabilidad (SLO): optimizas el triángulo, no solo una esquina.
- Regla operativa: cualquier recorte de costo que suba change failure rate o aumente el time to recover es “falso ahorro” (te lo cobra producción).

***

## Examples (aplicado a CRM enterprise)

**Facts:** GitHub Actions puede exportar/entregar datos de uso por repositorio a nivel de billing/usage, lo que habilita showback por equipo/servicio en un CRM con múltiples repos (core, integraciones, data sync, mobile).[^11][^12]
**Inferences (escenario):** CRM enterprise con 12 servicios (API, billing, workflow engine, integraciones), 60 devs, 400 PR/mes, 3 ambientes efímeros concurrentes promedio.

- **Safe playbook:** PRs corren lint + unit + smoke; full integration solo en merge; preview env solo si PR tiene label `needs-preview`; TTL 8h; budgets por repo con alerta al 70/90%.
- **Aggressive playbook:** Preview env por PR + tests paralelos shardizados, pero con “auto-cancel” de runs anteriores por PR y cuotas duras (máx 2 preview envs por equipo); si excede presupuesto semanal, se degrada automáticamente a smoke-only.
**Facts:** En GitHub Actions, los límites de caching (uploads/downloads por minuto) hacen que un diseño con “muchísimas caches pequeñas por job” sea más propenso a fallos/rate limiting en repos muy activos.[^2]

***

## Metrics / success signals

**Facts:** DORA recomienda medir throughput (deployment frequency, lead time) y estabilidad (change failure rate, recovery time) para performance de entrega.[^7]
**Inferences (FinOps + DevEx):**

- Costo por PR (USD/PR) y por pipeline (USD/run), y percentil 95 de minutos por workflow (para detectar colas/ineficiencia).
- Costo por release (USD/deploy) correlacionado con change failure rate (si baja costo pero sube fallas, mala optimización).
- “Cache hit ratio” por job tipo (deps/build/images) + “cache storage growth” semanal (señal de bloat).
- Ephemeral env: TTL compliance (% destruidos a tiempo), costo por env-hora, y “orphaned env count”.

***

## Operational checklist

**Facts:** En GitHub Actions, el costo de storage se acumula por hora y borrar artefactos/cachés corta cobros futuros pero no “borra” lo ya acumulado en el ciclo.[^1]
**Inferences (pasos operativos):**

1. Define ownership: repo → equipo; servicio → owner; entorno efímero → owner.
2. Habilita budgets/alertas: org + repos top 10; umbrales 70/90/100 con acción asociada (alerta, bloquear no-main, requerir aprobación).
3. Runner policy: clases de runner, concurrencia máxima por repo, timeouts por job, y cola máxima aceptable.
4. Caching policy: qué se cachea, claves, TTL/retención, límites de tamaño; revisa semanalmente crecimiento de caché/artefactos.
5. Paralelización policy: matrix cap por workflow (por debajo de 256 aunque sea posible), shards solo donde reduzca tiempo total y no sature límites.[^2]
6. Ephemeral env policy: quién puede crearlos, TTL default, auto-destrucción al cerrar PR, cuotas por equipo y “scale-to-zero” cuando aplique.
7. Cost dashboards:
    - GitHub: ingesta de usage report/API para costo por repo/SKU.[^12][^11]
    - Kubernetes: OpenCost para costo por namespace/service/deployment, incluyendo entornos efímeros.[^5][^4]
8. Revisión quincenal: top pipelines por gasto, top repos por storage, top causas de reruns; decide “safe vs aggressive” por servicio crítico vs no crítico.

***

## Anti-patterns

**Facts:** GitHub Actions tiene límites duros (p. ej., cache uploads/min, matriz máxima), por lo que “escalar” sin diseño puede derivar en cancelaciones/fallos y desperdicio de minutos.[^2]
**Inferences:**

- “Paralelizar todo” sin concurrency groups: duplicas costo en PRs con commits frecuentes.
- Caches sin TTL/evicción: bajas minutos hoy, pagas storage indefinidamente (y complicas invalidación).
- Artefactos gigantes “por si acaso”: storage accrued + tiempo extra de upload/download.
- Ephemeral envs sin auto-cleanup: el costo real aparece en infraestructura (K8s/DB) y es difícil de rastrear sin asignación por servicio.
- Optimizar costo recortando tests críticos: baja minutos, sube change failure rate y MTTR (te cuesta más en incidentes).

***

## Diagnostic questions

**Facts:** DORA propone medir estabilidad y throughput con métricas estándar; úsalo como lenguaje común para decidir recortes de costo sin romper confiabilidad.[^6][^7]
**Inferences (preguntas de decisión):**

- ¿Cuáles repos/servicios están en el top 20% de gasto y por qué (tests, builds, reruns, colas)?
- ¿Qué porcentaje de runs son redundantes (mismo PR, mismos jobs) y se podría auto-cancelar?
- ¿Qué caches crecen semana a semana y no muestran mejora de tiempo (hit ratio bajo)?
- ¿Qué pipelines podrían moverse a self-hosted runners (si el costo directo de minutos domina) vs quedarse hosted (si domina la ops overhead)?[^1]
- ¿Cuántos entornos efímeros quedan “huérfanos” y cuánto cuestan por día?
- ¿Qué “recorte” propuesto afecta SLO (p. ej., baja coverage) y qué guardrail lo evitaría?

***

## Sources (o referencia a SOURCES.md)

**Fuentes clave usadas (para agregar/actualizar en `SOURCES.md`):**

- GitHub Docs — “GitHub Actions billing” (2024-12-31): https://docs.github.com/billing/managing-billing-for-github-actions/about-billing-for-github-actions[^1]
- GitHub Docs — “Actions limits” (2024-12-31): https://docs.github.com/en/actions/reference/limits[^2]
- GitLab Docs — “Caching in GitLab CI/CD” (2025-11-25): https://docs.gitlab.com/ci/caching/[^3]
- GitHub Changelog — billing usage endpoint / deprecaciones de workflow usage endpoints (2025-02-01): https://github.blog/changelog/2025-02-02-actions-get-workflow-usage-and-get-workflow-run-usage-endpoints-closing-down/[^11]
- GitHub REST API Docs — Billing usage report (ejemplos) (2022-11-27): https://docs.github.com/en/rest/billing/usage[^12]
- OpenCost Blog — CNCF incubation (2024-10-30): https://opencost.io/blog/cncf-incubation/[^4]
- OpenCost GitHub — features de asignación de costos por K8s objetos: https://github.com/opencost/opencost[^5]
- DORA metrics (definición 4 métricas) — Octopus (2023-01-31): https://octopus.com/devops/metrics/dora-metrics/[^7]
- DORA 2024 (trade-off speed vs stability) — RedMonk (2024-11-25): https://redmonk.com/rstephens/2024/11/26/dora2024/[^6]
- DORA + SLO como contrapeso — InfoQ (2025-12-28): https://www.infoq.com/articles/DORA-metrics-PBCs/[^13]
- Ephemeral envs (estrategia mixta, costo/capacidad) — Mia-Platform (2025-01-16): https://mia-platform.eu/blog/why-should-you-adopt-ephemeral-environments/[^10]
- Spot/optimización costo runners — AWS Containers Blog (2025-12-28): https://aws.amazon.com/blogs/containers/streamline-your-containerized-ci-cd-with-gitlab-runners-and-amazon-eks-auto-mode/[^9]

**SOURCES.md additions (sin duplicados; Accessed 2026-02-18):**

- GitHub Docs — GitHub Actions billing — https://docs.github.com/billing/managing-billing-for-github-actions/about-billing-for-github-actions
- GitHub Docs — Actions limits — https://docs.github.com/en/actions/reference/limits
- GitLab Docs — Caching in GitLab CI/CD — https://docs.gitlab.com/ci/caching/
- GitHub Changelog — Actions usage endpoints closing down — https://github.blog/changelog/2025-02-02-actions-get-workflow-usage-and-get-workflow-run-usage-endpoints-closing-down/
- GitHub REST API — Billing usage — https://docs.github.com/en/rest/billing/usage
- OpenCost — CNCF incubation — https://opencost.io/blog/cncf-incubation/
- OpenCost (GitHub) — opencost/opencost — https://github.com/opencost/opencost
- RedMonk — DORA Report 2024 commentary — https://redmonk.com/rstephens/2024/11/26/dora2024/
- InfoQ — Using DORA Metrics and Process Behavior Charts — https://www.infoq.com/articles/DORA-metrics-PBCs/
- Mia-Platform — Ephemeral environments adoption — https://mia-platform.eu/blog/why-should-you-adopt-ephemeral-environments/
- AWS Containers Blog — GitLab Runners + EKS Auto Mode — https://aws.amazon.com/blogs/containers/streamline-your-containerized-ci-cd-with-gitlab-runners-and-amazon-eks-auto-mode/

***

## Key takeaways for PM practice

- **Facts:** DORA te da un marco para que costo no se “coma” confiabilidad: mide throughput y estabilidad con métricas estándar.[^7]
- **Facts:** GitHub Actions tiene límites (matriz, caching rate) que obligan a diseñar paralelización/caching con guardrails, no solo “más jobs”.[^2]
- **Inferences:** PM/PLG interno: trata CI/CD como “producto interno” con budgets, SLOs y ownership; sin esto, el gasto escala más rápido que el delivery.
- **Inferences:** Empieza safe: recorta desperdicio (reruns redundantes, caches sin TTL, artifacts enormes) antes de ir aggressive (Spot, preview env por PR).
- **Inferences:** Lo que no esté “costed” por repo/servicio (dashboard) no se gobierna; showback convierte optimización en hábito, no en proyecto.
<span style="display:none">[^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28]</span>

<div align="center">⁂</div>

[^1]: https://docs.github.com/billing/managing-billing-for-github-actions/about-billing-for-github-actions

[^2]: https://docs.github.com/en/actions/reference/limits

[^3]: https://docs.gitlab.com/ci/caching/

[^4]: https://opencost.io/blog/cncf-incubation/

[^5]: https://github.com/opencost/opencost

[^6]: https://redmonk.com/rstephens/2024/11/26/dora2024/

[^7]: https://octopus.com/devops/metrics/dora-metrics/

[^8]: https://ephemeralenvironments.io

[^9]: https://aws.amazon.com/blogs/containers/streamline-your-containerized-ci-cd-with-gitlab-runners-and-amazon-eks-auto-mode/

[^10]: https://mia-platform.eu/blog/why-should-you-adopt-ephemeral-environments/

[^11]: https://github.blog/changelog/2025-02-02-actions-get-workflow-usage-and-get-workflow-run-usage-endpoints-closing-down/

[^12]: https://docs.github.com/en/rest/billing/usage

[^13]: https://www.infoq.com/articles/DORA-metrics-PBCs/

[^14]: pasted-text.txt

[^15]: https://www.sentinelone.com/es/cybersecurity-101/cloud-security/gitlab-ci-cd-security/

[^16]: https://www.qataclismo.com/herramientas/cicd/gitlab-ci

[^17]: https://www.youtube.com/watch?v=LaHkq5cqcuI

[^18]: https://docs.github.com/en/actions/concepts/billing-and-usage

[^19]: https://www.blacksmith.sh/blog/how-to-reduce-spend-in-github-actions

[^20]: https://chairnerd.seatgeek.com/ci-runner-optimizations/

[^21]: https://mgtechsoft.com/blog/optimizing-ci-cd-pipelines-in-gitlab-strategies-for-speed-and-reliability/

[^22]: https://www.reddit.com/r/devops/comments/1po8hj5/github_actions_introducing_a_perminute_fee_for/

[^23]: https://www.bunnyshell.com/blog/top-7-platforms-for-ephemeral-environments-septemb/

[^24]: https://www.youtube.com/watch?v=ehVx1WDrmkg

[^25]: https://dev.to/depot/how-to-calculate-your-real-github-actions-usage-in-minutes-nlb

[^26]: https://opencost.io/docs/specification/

[^27]: https://www.reddit.com/r/devops/comments/1ffzvms/recs_for_ephemeral_environments_for_testing/

[^28]: https://www.suse.com/c/opencost-kubernetes-cost-monitoring/

