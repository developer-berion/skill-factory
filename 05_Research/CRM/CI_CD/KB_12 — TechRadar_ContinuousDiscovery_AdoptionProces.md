<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_12_TechRadar_ContinuousDiscovery_AdoptionProcess — Proceso de adopción tecnológica “sin hype” (Tech Radar + Continuous Discovery)

## Executive summary (10–15 líneas)

- (Fact) Un “Tech Radar” bien gobernado sirve para separar moda vs productividad, alineado con el ciclo de madurez/adopción (trigger → pico → desilusión → productividad).[^1]
- (Inference) El objetivo no es “probar todo”, sino reducir fricción comercial/operativa con decisiones repetibles: evaluar, pilotear, escalar, estandarizar o retirar.
- (Fact) La adopción debe ser iterativa: evaluar madurez, identificar brechas y ajustar en ciclos, no como proyecto único.[^2]
- (Inference) Define criterios de madurez antes de ver vendors (evita sesgo por demo): valor, operabilidad, riesgo, costo total y reversibilidad.
- (Fact) Los pilotos deben operar como experimentos: construir–medir–aprender con métricas accionables, no “opiniones”.[^3]
- (Inference) Todo piloto nace con “exit criteria” (escalamiento o descarte) y con plan de deprecación si entra a estándar.
- (Fact) Mide performance con un set corto y consistente; las métricas DORA balancean velocidad y estabilidad (frecuencia, lead time, CFR, MTTR).[^4]
- (Inference) Estandarizar es empaquetar: playbook, training, plantillas, monitoreo, soporte, contratos, y ownership (quién responde cuando falla).
- (Inference) Deprecar es parte del sistema: sin retiro, el stack se vuelve “cementerio” (costos ocultos + riesgo).
- (Inference) Mantén cadencia trimestral: intake → triage → evaluación → decisión → ejecución → post-mortem; con un tablero único para toda la empresa.
- (Inference) Incluye dos modos de decisión: opción segura (optimiza riesgo/operación) vs opción agresiva (optimiza velocidad/ventaja).
- (Inference) Resultado esperado: menos improvisación, más repetibilidad, y adopción que mejora margen/tiempo de entrega sin aumentar incidentes.

***

## Definitions and why it matters

- (Fact) “Hype Cycle” describe una curva de madurez/adopción donde tecnologías pasan por entusiasmo inicial, desilusión y luego productividad; usarlo como lente ayuda a no confundir visibilidad con valor real.[^1]
- (Inference) “Adopción sin hype” = un proceso con gates (criterios) que obliga evidencia operativa/comercial antes de escalar, y obliga retiro si no sostiene ROI o genera riesgo.
- (Fact) “Build–Measure–Learn” plantea aprendizaje validado con medición (no narrativa) para decidir pivotar o perseverar en iniciativas.[^3]
- (Inference) En CRM enterprise, este proceso protege 3 cosas: calidad de datos (pipeline/forecast), continuidad operativa (SLA interno) y control de riesgo (compliance, seguridad, vendor lock-in).

***

## Principles and best practices (con citas por sección + fecha)

- (Fact, 2025-02-06) Haz la evaluación de adopción de forma iterativa para entender madurez, brechas y ajustar el plan conforme evoluciona la estrategia.[^2]
- (Inference) Principio 1 — “Primero criterio, luego vendor”: crea una scorecard fija (0–3) con pesos; si no pasa el mínimo, no hay demo/piloto.
- (Fact, 2011-06-30) Diseña pilotos como ciclos Build–Measure–Learn, empezando por el problema y un MVP que permita aprender rápido con métricas accionables.[^3]
- (Inference) Principio 2 — “Reversibilidad obligatoria”: toda adopción debe tener plan de rollback/migración y un camino de salida contractual (datos, integraciones, costos).
- (Fact, 2026-02-16) Usa métricas tipo DORA para balancear rapidez y estabilidad (frecuencia de despliegue, lead time, change failure rate, MTTR).[^4]
- (Inference) Principio 3 — “No estandarices sin operación”: no se declara “estándar” algo que no tenga soporte, observabilidad, runbooks y ownership claro.
- (Fact, 2020-05-04) El “pico de expectativas” suele venir con buzzwords y marketing; el radar debe protegerte de decisiones tomadas por presión de mercado.[^1]
- (Inference) Principio 4 — “El radar es cartera, no wishlist”: limita WIP (p.ej., máximo 2 tecnologías en piloto por trimestre por dominio) para que los pilotos terminen.

Criterios de madurez (scorecard 0–3; umbrales sugeridos):

- (Inference) Valor negocio: impacto en revenue, margen, CAC, retención, velocidad de venta (en CRM: ciclo, win-rate, forecasting).
- (Inference) Madurez técnica: APIs, integración, estabilidad, comunidad/roadmap, costos previsibles.
- (Inference) Operabilidad: monitoreo, permisos, auditoría, soporte, DR/BCP, tiempos de respuesta.
- (Inference) Riesgo: seguridad, compliance, residencia de datos, fraude/abuso, lock-in, vendor viability.
- (Inference) Economía: TCO 12 meses (licencias + implementación + operación), costo por usuario/acción, costo de salida.

***

## Examples (aplicado a CRM enterprise)

Caso: “Adoptar un copiloto IA para ventas” (CRM enterprise)

- (Fact) Plantea el piloto como MVP medible (Build–Measure–Learn): hipótesis explícita, experimento corto, métricas accionables y decisión al cierre.[^3]
- (Inference) Evaluación (1 semana): scorecard; define 3 casos de uso (p.ej., resumen de llamadas, borrador de emails, next-best-action) y “datos mínimos” (campos CRM, permisos).
- (Inference) Piloto (2–4 semanas): 10–20 vendedores, 2 managers, 1 analista RevOps; scope cerrado (solo pipeline activo) y control (grupo sin herramienta).
- (Inference) Métricas del piloto (mínimas): tiempo a primer valor (TTFV), adopción semanal, reducción de tiempo administrativo, calidad de datos (campos completos), impacto en actividades (touches) y en conversión por etapa (si aplica).
- (Inference) Decisión:
    - Opción segura: escalar solo a un equipo y solo a 1–2 casos de uso que reduzcan trabajo (no decisiones críticas).
    - Opción agresiva: ampliar a toda la fuerza comercial si el piloto supera umbrales y tienes monitoreo + guardrails (permisos, logging, QA de outputs).
- (Inference) Estandarización: crea “CRM AI Playbook” (prompts aprobados, política de datos, checklist de managers, plantillas, entrenamiento) y define soporte L1/L2.
- (Inference) Deprecación: si en 2 trimestres no sostiene adopción/ROI o aumenta riesgo, se retira (desactivar features, migrar logs, cerrar contrato, comunicar cambios).

***

## Metrics / success signals

- (Fact) DORA define un set de métricas para performance de entrega (deployment frequency, lead time for changes, change failure rate, MTTR) que equilibra velocidad y estabilidad.[^4]
- (Inference) Métricas por etapa (recomendado):
    - Intake/Triage: % propuestas con scorecard completo; tiempo de decisión (días).
    - Piloto: TTFV; adopción semanal (% usuarios activos/target); tasa de tareas completadas con la herramienta; error rate/incident rate; ahorro de tiempo (min/semana).
    - Escala: costo por usuario activo; tasa de tickets por 100 usuarios; cumplimiento de seguridad/auditoría; impacto en KPI del CRM (data completeness, forecast accuracy, win-rate por cohorte).
    - Deprecación: reducción de superficie (apps/features retiradas); costo evitado; tiempo de migración; incidentes post-retiro (debe ser ~0).
- (Inference) Señales de éxito “sin hype”: adopción sostenida 6–8 semanas, tickets decrecientes, y KPI de negocio mejora sin degradar estabilidad (si suben incidentes, no está listo para estándar).

***

## Operational checklist

- (Fact) Mantén el proceso como evaluación iterativa y repetible (ciclos), no evento único; ajusta con la madurez.[^2]
- (Inference) Checklist end-to-end (gates):
    - Intake: problema claro, dueño de negocio, usuarios afectados, alternativa “no hacer nada”.
    - Triage: scorecard 0–3, riesgo alto/medio/bajo, reversibilidad (sí/no), costo 12 meses.
    - Evaluación técnica: integración CRM, permisos, auditoría, export de datos, límites, soporte vendor.
    - Diseño de piloto: hipótesis, cohortes, duración, métricas, plan de rollback, criterios de “go/no-go”.
    - Ejecución: enablement, canal de soporte, logging, revisión semanal (20 min), ajuste de configuración.
    - Post-piloto: resultados vs umbrales, decisión documentada, lecciones, deuda creada.
    - Estandarización: playbook, runbook, training, monitoreo, budget, RACI, contrato.
    - Deprecación: trigger, plan de migración, comunicación, cierre de accesos, borrado/retención de datos según política.

Cadencia trimestral (Tech Radar operativo):

- (Inference) Semana 1: intake + triage (máximo WIP).
- (Inference) Semana 2–6: pilotos en paralelo (pocos, con dueño).
- (Inference) Semana 7: comité de decisión (adopt / trial / hold / retire).
- (Inference) Semana 8–12: estandarizar o retirar; actualizar documentación; retro del proceso.

***

## Anti-patterns

- (Fact) Adoptar en “peak hype” por presión de marketing suele inflar expectativas antes de tener evidencia de productividad real.[^1]
- (Inference) “Pilotos-zombie”: pilotos sin fecha de cierre, sin cohortes, sin métricas; se convierten en producción informal.
- (Inference) “Estandarizar por demo”: declarar estándar porque “se ve bien” sin soporte, sin ownership, sin auditoría.
- (Inference) “Sin deprecación”: cada trimestre agregas herramientas, nunca retiras; suben costos, integraciones frágiles y riesgo.
- (Inference) “KPIs vanity”: medir solo NPS interno o “usuarios creados” y no uso real, tickets, estabilidad y ROI.

***

## Diagnostic questions

- (Fact) Si la estrategia se evalúa iterativamente, puedes identificar brechas y ajustar el plan en cada ciclo; si no, repites errores trimestre a trimestre.[^2]
- (Inference) Preguntas de diagnóstico (rápidas y duras):
    - ¿Qué problema comercial/operativo resuelve y qué KPI del CRM debe mover?
    - ¿Cuál es el “mínimo experimento” para aprender en 2–4 semanas?
    - ¿Qué debe pasar para decir “no” aunque el vendor sea top? (umbral y riesgo)
    - ¿Cómo se revierte? (rollback técnico, salida contractual, export de datos)
    - ¿Quién paga el costo operativo cuando falla (on-call/soporte)? ¿Está aceptado?
    - ¿Qué tecnología actual se retirará si esta entra? (regla: 1 entra, 1 sale cuando aplique)
    - ¿Qué parte es sensible? (datos, compliance, fraude, reputación, lock-in)

***

## Sources (o referencia a SOURCES.md)

- (Fact) Microsoft Cloud Adoption Framework — “Evaluación de la estrategia de adopción de la nube” (iteración y evaluación de madurez).[^2]
- (Fact) Lean Startup — principios y loop Build–Measure–Learn, MVP y métricas accionables.[^3]
- (Fact) DORA metrics (explicación de las 4 métricas y su balance velocidad/estabilidad).[^4]
- (Fact) Gartner Hype Cycle (explicación del ciclo y fases; referencia práctica para evitar decisiones por hype).[^1]

SOURCES.md additions (sin duplicados; fecha de acceso: 2026-02-18):

- Microsoft Learn — Cloud Adoption Framework: Strategy assessment — https://learn.microsoft.com/es-es/azure/cloud-adoption-framework/strategy/assessment[^2]
- The Lean Startup — Principles (Build-Measure-Learn, MVP) — https://theleanstartup.com/principles[^3]
- LaunchDarkly — DORA Metrics overview — https://launchdarkly.com/blog/dora-metrics/[^4]
- BMC — Introduction to the Gartner Hype Cycle — https://www.bmc.com/blogs/gartner-hype-cycle/[^1]

***

## Key takeaways for PM practice

- Diseña el sistema para decir “no” rápido con scorecards y umbrales, no para acumular “pruebas”.
- Pilotos = experimentos con métricas y fecha de cierre; si no, son deuda.
- Estandarizar exige operación (soporte, monitoreo, runbooks, ownership) o se vuelve riesgo oculto.
- Deprecar es una capacidad: sin retiro, el stack se pudre y el margen se va en fricción.
- Mantén una cadencia trimestral con WIP limitado y decisiones documentadas (adopt/trial/hold/retire).
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://www.bmc.com/blogs/gartner-hype-cycle/

[^2]: https://learn.microsoft.com/es-es/azure/cloud-adoption-framework/strategy/assessment

[^3]: https://theleanstartup.com/principles

[^4]: https://launchdarkly.com/blog/dora-metrics/

[^5]: pasted-text.txt

[^6]: https://publications.iadb.org/publications/spanish/document/fAIr-Tech-Radar-explorando-la-adopcion-de-inteligencia-artificial-en-America-Latina-y-el-Caribe.pdf

[^7]: http://www.scielo.org.mx/scielo.php?script=sci_arttext\&pid=S2007-09342013000600003

[^8]: https://oa.upm.es/38119/1/PEDRO_FERNANDEZ_CARDADOR.pdf

[^9]: https://data.cnra.ca.gov/es/dataset/svsim/resource/f1586978-1d1a-489a-9a2a-f5ebe095b2f6?view_id=d1117fc6-8576-4a10-8911-5f64b26c0301

[^10]: https://abstracta.us/blog/devops/dora-metrics-in-devops/

[^11]: https://www.thinslices.com/insights/early-stage-development-build-measure-learn-loop

[^12]: https://www.cliffsnotes.com/study-notes/22076537

[^13]: https://en.wikipedia.org/wiki/Gartner_hype_cycle

[^14]: https://www.harness.io/blog/what-is-mttr-dora-metric

[^15]: https://greatdemo.com/es/descubrimiento-y-demostraciones-a-lo-largo-de-la-curva-de-adopcion-tecnologica/

[^16]: https://www.forbes.com/sites/karlmoore/2025/05/27/how-to-navigate-the-hype-cycle-of-emerging-tech/

