<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_11_DX_PlatformEngineering_GoldenPaths — Platform Engineering para CI/CD en CRM (Golden Paths, templates, catálogo, self‑service, build acceleration, runners y métricas DX)

## Executive summary (10–15 líneas)

- **[Fact]** Platform Engineering busca reducir carga cognitiva y acelerar entrega ofreciendo capacidades internas con buena UX, incluyendo portales, APIs/CLI, documentación y templates (“golden paths”).[^1]
- **[Fact]** En organizaciones con muchos servicios, un “golden path” suele ser un bundle de template + docs que estandariza un workflow extremo-a-extremo (build, test, deploy, observabilidad).[^1]
- **[Fact]** Self-service (solicitar/provisionar capacidades autónoma y automáticamente) es un atributo clave para escalar a muchos equipos sin saturar al equipo de plataforma.[^1]
- **[Fact]** Backstage se usa como portal/catálogo y sus Software Templates scaffoldean componentes (código “skeleton”, variables, publicación a GitHub/GitLab).[^2]
- **[Fact]** Golden path templates en Backstage se usan para habilitar self-service, automatizar buenas prácticas y estandarizar workflows.[^3]
- **[Fact]** Métricas recomendadas combinan satisfacción/productividad (incluyendo SPACE), eficiencia organizacional (latencia request→fulfillment) y delivery (DORA: deployment frequency, lead time, MTTR, change failure rate).[^4][^1]
- **[Inference]** En equipos de CRM con muchas integraciones, el dolor principal es variabilidad (pipelines distintos), tiempos de build/test, y entornos frágiles para pruebas de integración; el golden path “mata” esa variabilidad con caminos soportados y seguros.
- **[Inference]** Build acceleration/caching y runners bien diseñados son “palancas” de DX: bajan tiempos, reducen cola, y convierten CI/CD en infraestructura confiable (no en un cuello de botella).
- **[Inference]** El catálogo (Backstage) debe ser el punto único para descubrir servicios, APIs, owners, runbooks, plantillas, y “cómo se despliega aquí”, especialmente crítico en CRM multi-servicio.
- **[Inference]** La adopción se gana con valor (menos fricción + soporte) y con métricas de DX visibles; no con mandates.

***

## Definitions and why it matters

- **[Fact] Platform (internal)**: colección integrada de capacidades presentada según necesidades de usuarios internos, con experiencias consistentes (portales web, templates, self-service APIs).[^1]
- **[Fact] Golden path**: workflow reutilizable ofrecido como template inicial + documentación para acelerar onboarding y ejecutar un supply chain estándar (build/scan/test/deploy/observe).[^1]
- **[Fact] Self-service**: usuarios solicitan y reciben capacidades de forma autónoma y automática, clave para que el equipo de plataforma escale a múltiples equipos.[^1]
- **[Fact] Backstage Software Templates**: funcionalidad para crear componentes; carga skeletons, templatea variables y publica a destinos como GitHub o GitLab.[^2]

Por qué importa en CRM con muchas integraciones:

- **[Inference]** CRM enterprise suele tener decenas/centenas de servicios (core, integraciones, jobs, webhooks, APIs), y el costo de coordinación/variabilidad se dispara si cada equipo resuelve CI/CD distinto.
- **[Fact]** El objetivo explícito de plataformas incluye reducir carga cognitiva en equipos de producto y acelerar delivery.[^1]

***

## Principles and best practices (con citas por sección + fecha)

1) **Trata la plataforma como producto (UX + roadmap + feedback)**

- **[Fact]** Plataformas exitosas se diseñan y evolucionan según requisitos de usuarios, como cualquier producto (“platform as a product”). (CNCF, 2018)[^1]
- **[Inference]** En CRM, define “personas” internas (equipo integraciones, core CRM, data/BI, soporte) y su golden path principal; evita diseñar para el caso raro.

2) **Golden paths: opinados, soportados y medibles**

- **[Fact]** Un golden path puede entregarse como template + documentación para un workflow reutilizable. (CNCF, 2018)[^1]
- **[Inference]** “Opinados” significa: si te sales del camino, puedes hacerlo, pero pierdes soporte (SLA interno) o entras a “modo experto” con más responsabilidad.

3) **Self-service primero, para escalar de verdad**

- **[Fact]** Self-service autónomo y automático es clave para que el equipo de plataforma habilite muchos equipos y escale. (CNCF, 2018)[^1]
- **[Fact]** En Backstage, los templates habilitan self-service y estandarización de workflows. (Red Hat, 2025-06-24)[^3]
- **[Inference]** En CRM, self-service debe cubrir: crear servicio + pipeline + secrets + entornos + observabilidad mínima, y no solo “crear repo”.

4) **Catálogo como “source of truth” operativo**

- **[Fact]** El whitepaper enumera web portals para publicar documentación, service catalogs y project templates como capacidad de plataforma. (CNCF, 2018)[^1]
- **[Inference]** En CRM con integraciones, el catálogo debe responder rápido: “¿quién es owner?”, “¿qué contratos (OpenAPI/AsyncAPI) maneja?”, “¿cómo se prueba?”, “¿cómo se despliega y se revierte?”.

5) **Templates (Backstage) como empaquetado de estándares**

- **[Fact]** Backstage Software Templates crea componentes a partir de skeletons, variables y publicación a repos. (Backstage docs, s/f)[^2]
- **[Inference]** Diseña templates por “tipo de servicio” en CRM: API REST, consumer de eventos, webhook receiver, job batch, con sus pruebas y checks mínimos.

6) **Build acceleration/caching: obsesión por el ciclo local→CI**

- **[Fact]** El objetivo de plataforma incluye acelerar onboarding y delivery con workflows reutilizables. (CNCF, 2018)[^1]
- **[Inference]** Estándares prácticos: caché de dependencias, caché de layers de contenedor, test selection, paralelización, y “artifact reuse” entre stages; mide cache hit-rate y minutos ahorrados.

7) **Runners: capacidad de plataforma, no “infra suelta”**

- **[Fact]** Una plataforma provee capacidades como automation for building/testing y delivering/verifying. (CNCF, 2018)[^1]
- **[Inference]** En CRM, el cuello típico es cola de CI y tests de integración; usa runners autoscalables/efímeros, límites por repo, y prioridades (hotfix > feature).

8) **Métricas DX: mezcla DORA + SPACE + señales operativas**

- **[Fact]** DORA sugiere medir deployment frequency, lead time, time to restore y change failure rate. (CNCF citando DORA, 2018)[^1]
- **[Fact]** SPACE complementa a DORA: DORA mide performance DevOps; SPACE amplía a experiencia de desarrollo y factores humanos. (LinearB, 2024-03-18)[^4]
- **[Inference]** Para CRM multi-servicio: agrega métricas “plataforma” (queue time CI, build duration, flaky tests, latencia de entornos, % adopción golden path) y úsalas para priorizar roadmap.

***

## Examples (aplicado a CRM enterprise)

### Ejemplo 1 — “Nuevo microservicio de integración” (WhatsApp/Email/ERP)

- **[Fact]** Con Software Templates, el dev inicia un componente desde `/create` y se ejecuta una tarea que genera/publica repos/artefactos.[^2]
- **[Inference]** Template “crm-integration-service” incluye: repo + pipeline CI (lint/test/build) + IaC/K8s manifests + librería estándar de observabilidad + contract tests (OpenAPI/AsyncAPI) + despliegue a staging + registro automático en catálogo.
- **[Inference]** El golden path define “cómo se hace bien aquí”: naming, versionado de API, retries/idempotencia, manejo de PII, y políticas de secrets.

**Qué incluye (operativo)**

- **[Inference]** Scaffolding completo + CI/CD estándar + registro en catálogo + runbook básico + dashboards mínimos + alertas base.

**Qué no incluye**

- **[Inference]** Lógica específica del negocio (mapeos de campos del CRM con cada proveedor), ni acuerdos con terceros (tokens/credenciales reales), ni “resolver” integraciones rotas de proveedores externos.

**Qué es sensible (riesgo CRM)**

- **[Inference]** PII/PCI, rate limits de proveedores, contratos inestables, pruebas end-to-end que dependen de sandbox externos; requiere gates (aprobación, masking, entornos aislados).


### Ejemplo 2 — “Entorno efímero para pruebas de integración”

- **[Fact]** Self-service debe permitir request/fulfillment autónomo con mínima intervención manual. (CNCF, 2018)[^1]
- **[Inference]** Golden path “integration-env” crea entorno por PR: DB + colas + mocks/record-replay + seed de datos; al merge, se destruye; métricas: tiempo de provisionado y tasa de fallos.

***

## Metrics / success signals

- **[Fact] DORA (resultado de delivery)**: deployment frequency, lead time for changes, time to restore, change failure rate.[^1]
- **[Fact] Eficiencia plataforma**: latencia request→fulfillment (p.ej., pedir DB/entorno) y latencia para llevar un servicio nuevo a producción.[^1]
- **[Fact] Satisfacción/productividad**: active users/retención del portal, NPS/surveys, y métricas tipo SPACE.[^1]

Señales prácticas para CRM multi-servicio (recomendadas):

- **[Inference]** DX de CI: p50/p90 build time, p50/p90 queue time en runners, cache hit-rate, % pipelines “verdes” en main, flaky rate.
- **[Inference]** Golden path adoption: % repos creados con template, % servicios con ownership + docs + runbook, % con dashboards/alertas estándar.
- **[Inference]** Integraciones: tiempo de “nuevo conector” (idea→staging), tasa de incidentes por cambios de contrato, % contract tests ejecutados en PR.

***

## Operational checklist

- **[Fact]** Una plataforma debe ofrecer interfaces consistentes (GUI/CLI/API/portal) y documentación/onboarding para usuarios.[^1]
- **[Inference]** Checklist por iteración (2–4 semanas):
- Definir 1–2 golden paths prioritarios (por volumen y dolor) y su “definition of done” operativo.
- Construir template Backstage por golden path (inputs mínimos, outputs verificables) y publicar en catálogo.
- Estandarizar pipeline: stages, políticas (security scanning), artefactos y convenciones.
- Implementar aceleración: caching + paralelización + límites de recursos; instrumentar tiempos.
- Estandarizar runners: capacity planning, autoscaling, prioridades, aislamiento, costos.
- Observabilidad del CI/CD: dashboards para cola, duración, fallos, flakes, y tiempo request→fulfillment.
- Gobernanza ligera: cuándo puedes salirte del golden path, cómo pedir excepción, y quién la aprueba.

***

## Anti-patterns

- **[Fact]** Plataformas que se lanzan sin feedback de usuarios o basadas en mandates tienden a generar resistencia y fallar en capturar valor. (CNCF, 2018)[^1]
- **[Inference]** “Template = boilerplate”: templates que solo crean carpetas sin pipeline, sin métricas y sin soporte real; nadie los usa después del kickoff.
- **[Inference]** Catálogo desactualizado: owners incorrectos, docs rotas, links muertos; en CRM esto mata operación (incidentes e integraciones) más que en otros dominios.
- **[Inference]** Golden path rígido: no permite composabilidad; fuerza a todos a lo mismo aunque existan casos legítimos (batch pesado, integración legacy, restricciones regulatorias).
- **[Inference]** Optimizar solo velocidad: bajar checks para “deploy rápido” y terminar con change failure rate alto (impacta CRM: ventas/operación/soporte).

***

## Diagnostic questions

- **[Fact]** El éxito de plataforma se mide también con feedback de usuarios y actividad/uso del producto interno.[^1]
- **[Inference]** Preguntas para diagnóstico en CRM:
- ¿Cuánto tarda hoy crear un servicio nuevo “listo para prod” con observabilidad mínima?
- ¿Cuál es el p90 de build+tests en PR y cuánto es cola vs ejecución?
- ¿Qué % de fallos es por flakiness, por contratos de integración o por configuración inconsistente?
- ¿Cuántos “caminos” de despliegue existen hoy (por equipo/stack) y cuántos soporta realmente la organización?
- ¿El catálogo responde “quién es dueño” y “cómo se prueba” en <60 segundos?
- ¿Qué se puede pedir en self-service (DB, entorno, secrets) y qué sigue siendo ticket/manual?

***

## Sources (o referencia a SOURCES.md)

- CNCF TAG App Delivery — “CNCF Platforms White Paper” (publicado 2018; URL consultada 2026-02-18).[^1]
- Backstage — “Software Templates” docs (URL consultada 2026-02-18).[^2]
- Red Hat Developer — “How to implement developer self-service with Backstage” (2025-06-24; URL consultada 2026-02-18).[^3]
- LinearB — “SPACE Metrics Framework… Explained” (2024-03-18; URL consultada 2026-02-18).[^4]
- PlatformEngineering.org — “What are golden paths? …” (2026-01-20; URL consultada 2026-02-18).[^5]


### Añadir a `SOURCES.md` (sin duplicados)

- CNCF TAG App Delivery. “CNCF Platforms White Paper.” 2018. https://tag-app-delivery.cncf.io/whitepapers/platforms/ (accessed 2026-02-18)
- Backstage. “Software Templates.” https://backstage.io/docs/features/software-templates/ (accessed 2026-02-18)
- Red Hat Developer. “How to implement developer self-service with Backstage.” 2025-06-24. https://developers.redhat.com/articles/2025/06/25/how-implement-developer-self-service-backstage (accessed 2026-02-18)
- LinearB. “SPACE Metrics Framework for Developers Explained.” 2024-03-18. https://linearb.io/blog/space-framework (accessed 2026-02-18)
- PlatformEngineering.org. “What are golden paths? A guide to streamlining developer workflows.” 2026-01-20. https://platformengineering.org/blog/what-are-golden-paths-a-guide-to-streamlining-developer-workflows (accessed 2026-02-18)

***

## Key takeaways for PM practice

- Golden paths son producto: define usuario, promesa (DX), y métricas desde el día 1.[^1]
- Si no hay self-service real, la “plataforma” se convierte en mesa de ayuda y no escala.[^1]
- Backstage Templates son un buen mecanismo para empaquetar estándares operativos en un flujo repetible.[^3][^2]
- Mide DORA para delivery y complementa con señales DX/SPACE para evitar optimizar velocidad rompiendo calidad o salud del equipo.[^4][^1]
- En CRM con integraciones, prioriza golden paths que reduzcan variabilidad y riesgo (contratos, PII, entornos de integración), no solo “crear repos”.[^1]
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://tag-app-delivery.cncf.io/whitepapers/platforms/

[^2]: https://backstage.io/docs/features/software-templates/

[^3]: https://developers.redhat.com/articles/2025/06/25/how-implement-developer-self-service-backstage

[^4]: https://linearb.io/blog/space-framework

[^5]: https://platformengineering.org/blog/what-are-golden-paths-a-guide-to-streamlining-developer-workflows

[^6]: pasted-text.txt

[^7]: https://backstage.io

[^8]: https://www.youtube.com/watch?v=WmTa_vxn0oU

[^9]: https://about.gitlab.com/solutions/platform-engineering/

[^10]: https://www.paradigmadigital.com/techbiz/guia-practica-entender-golden-paths/

[^11]: https://www.paradigmadigital.com/techbiz/4-elementos-clave-platform-engineering/

[^12]: https://backstage.spotify.com/learn/onboarding-software-to-backstage/setting-up-software-templates/11-spotify-templates/

[^13]: https://shiftmag.dev/dora-space-gsm-or-devex-how-to-measure-developer-productivity-1304/

[^14]: https://www.paradigmadigital.com/formula/platform-engineering/

[^15]: https://www.youtube.com/watch?v=53f4oAbVaWo

[^16]: https://blog.funda.nl/how-golden-paths-give-our-developers-more-time-to-actually-develop/

