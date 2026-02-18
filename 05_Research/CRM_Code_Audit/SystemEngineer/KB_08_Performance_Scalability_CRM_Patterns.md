<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Performance y escalabilidad en CRMs: patrones prácticos (paginación, búsqueda, índices, caching, colas, batch, export streaming, backpressure)

## Executive summary (10–15 líneas)

- **Facts (2026-02-17):** En CRMs con datasets grandes, la paginación basada en `OFFSET` se degrada y además puede tener límites duros (p. ej., SOQL impone máximo 2.000 de offset).[^1]
- **Inferences (2026-02-17):** Prioriza keyset/cursor pagination para listas operativas (Contactos, Oportunidades, Actividades) y reserva `OFFSET` para vistas pequeñas o internas.
- **Facts (2026-02-17):** En Salesforce, `OFFSET` existe para paginar resultados de SOQL, pero tiene restricciones conocidas.[^2][^1]
- **Inferences (2026-02-17):** Si tu CRM es multi-tenant B2B, diseña UX y APIs para “continuar desde último registro” (cursor) y no para “saltarme la página 400”.
- **Facts (2026-02-17):** La eficacia de un índice depende de la selectividad; columnas con alta cardinalidad suelen dar mejores resultados, y compuestos siguen reglas tipo “leftmost-prefix”.[^3][^4]
- **Facts (2026-02-17):** En PostgreSQL, B-tree es el default útil para igualdad y rangos; GIN suele ser la opción para búsquedas full‑text.[^5]
- **Facts (2026-02-17):** En caching, un “cache stampede/dogpile” ocurre cuando expira una clave caliente y muchas requests vuelven al origen; mitigaciones incluyen request coalescing/single-flight.[^6][^7]
- **Inferences (2026-02-17):** En CRMs, “hot keys” típicas: dashboards por equipo, conteos por pipeline, permisos/ACL, pricing y reglas de asignación.
- **Facts (2026-02-17):** Request coalescing asegura que, en un miss concurrente, solo una ejecución reconstruye el valor y las demás esperan/comparten resultado.[^6]
- **Inferences (2026-02-17):** Para exportaciones y procesos masivos, usa colas + batch + streaming con backpressure para no tumbar la DB ni saturar workers.
- **Inferences (2026-02-17):** Checklist: keyset pagination, índices alineados a filtros/orden, cache con anti-stampede, colas idempotentes, límites por tenant, y observabilidad por ruta/consulta.
- **Inferences (2026-02-17):** Anti-patterns: `OFFSET` profundo, `LIKE '%texto%'` sin índice adecuado, invalidación de cache global, exports “todo en memoria”, y jobs sin idempotencia.

***

## Definitions and why it matters

**Facts (2026-02-17):** `OFFSET` en SOQL permite paginar resultados, pero en Salesforce tiene un máximo de 2.000 filas de offset.[^2][^1]
**Facts (2026-02-17):** Un “cache stampede/dogpile effect” es cuando expira una entrada popular y muchas solicitudes golpean simultáneamente al backend/origen.[^7]
**Inferences (2026-02-17):** En un CRM enterprise, performance = velocidad percibida + estabilidad bajo picos + costos controlados; escalabilidad = crecer en datos/usuarios sin reescribir todo ni degradar SLAs.

***

## Principles and best practices (con citas + fecha)

**Facts (2026-02-17):** Evita paginación profunda con `OFFSET` cuando esperas muchos registros; en Salesforce además te topas con el límite de 2.000 y debes usar alternativas.[^8][^1]
**Inferences (2026-02-17):** Implementa keyset pagination: “dame los próximos N a partir de (created_at, id) o id”, y fija un orden estable (si el orden cambia, aparecen duplicados/saltos).

**Facts (2026-02-17):** En PostgreSQL, B-tree sirve para igualdad y rangos; para full-text search, GIN es una opción típica.[^5]
**Facts (2026-02-17):** La selectividad/cardenalidad influye en qué tan útil es un índice; evitar indexar columnas de baja cardinalidad suele ser buena práctica.[^4][^3]
**Inferences (2026-02-17):** Diseña índices “según el WHERE + ORDER BY real” (no “según el modelo”): si tu lista siempre filtra por `account_id` y ordena por `updated_at`, piensa en índice compuesto (y en particionar por tenant si aplica).

**Facts (2026-02-17):** Request coalescing (single-flight/deduplicación) reduce thundering herd al asegurar que solo un request reconstruye datos en un cache miss y los demás reutilizan el resultado.[^6]
**Inferences (2026-02-17):** En CRMs, cachea “lecturas repetidas y caras” (permisos, configuraciones, catálogos, agregados), pero define explícitamente TTL, estrategia de invalidación, y comportamiento “stale-while-revalidate” para evitar picos.

**Inferences (2026-02-17):** Colas/batch/backpressure:

- “Cola” para desacoplar (eventos de actividad, cálculo de scoring, sincronizaciones).
- “Batch” para cargas masivas (importaciones, normalizaciones, recomputes).
- “Backpressure” para frenar al productor cuando el consumidor/DB va al límite (p. ej., limitar concurrencia por tenant y por tipo de job).

**Inferences (2026-02-17):** Export streaming: entrega CSV/Parquet por chunks con cursor y firma de reanudación (resume token), y aplica rate limits; nunca bloquees una transacción por “exportar todo”.

***

## Examples (aplicado a CRM enterprise)

**Facts (2026-02-17):** Si tu CRM está sobre Salesforce, paginar con `OFFSET` puede romperse al pasar 2.000 y además tiene costo creciente con offsets altos; por eso se recomienda un enfoque offset‑free (keyset).[^1][^8]
**Inferences (2026-02-17):** Ejemplo “Lista de oportunidades por agencia (B2B)”: API `GET /deals?agency_id=...&limit=50&after=({updated_at},{id})` ordenada por `updated_at desc, id desc`; el frontend guarda el cursor y pide “más” (infinite scroll) sin saltos de página arbitrarios.

**Facts (2026-02-17):** Para búsquedas textuales y filtros, elegir el tipo de índice correcto importa (p. ej., B-tree vs GIN en PostgreSQL).[^5]
**Inferences (2026-02-17):** Ejemplo “Búsqueda en actividades”:

- Filtros estructurados (owner, estado, fecha): B-tree/compuestos.
- Texto libre (notas/correos): índice full‑text (GIN) + ranking; evita `LIKE '%...'` como default.

**Facts (2026-02-17):** En cache, el stampede se mitiga con request coalescing y control de expiración/refresh para evitar que miles de requests reconstruyan lo mismo.[^7][^6]
**Inferences (2026-02-17):** Ejemplo “Dashboard de pipeline por equipo”: cachea agregados por equipo por 30–120s; al expirar, single-flight hace 1 recompute, y el resto recibe el valor anterior (stale) hasta que llegue el nuevo.

***

## Metrics / success signals

**Facts (2026-02-17):** Un objetivo explícito de request coalescing es reducir carga en backend y evitar thundering herd durante cache misses concurrentes.[^6]
**Inferences (2026-02-17):** Señales por área:

- Paginación/listas: p95 de `GET /list` estable al crecer el dataset; “page drift” (duplicados/saltos) ≈ 0; errores por límites (p. ej., offset) ≈ 0.
- DB/índices: % de consultas top que usan índice esperado; reducción de “rows scanned” vs “rows returned”; p95 de queries críticas.
- Cache: hit rate por endpoint; “single-flight coalesced ratio” (cuántos requests se agruparon) y “origin QPS” bajando en expiraciones.
- Colas/batch: lag por tipo de job; tasa de reintentos; tiempo a consistencia eventual (p. ej., scoring visible en < X min).
- Export streaming: time-to-first-byte bajo; throughput sostenido; ratio de reanudaciones exitosas.

***

## Operational checklist

**Facts (2026-02-17):** Si estás en Salesforce, valida si tus listados dependen de `OFFSET` porque existe el límite de 2.000 y necesitas alternativa para escalar.[^1]
**Inferences (2026-02-17):** Checklist (qué incluye / qué no / sensible):

- Paginación
- Qué incluye: keyset/cursor, orden estable, filtros obligatorios por tenant/cliente.
- Qué no incluye: “ir a página N” para N arbitrario en listas enormes (ofrece búsqueda/filtros).
- Sensible: orden por columnas no únicas (riesgo de duplicados), cambios concurrentes de datos.
- Búsqueda
- Qué incluye: separar “filtros estructurados” vs “texto libre”; límites de resultados; ranking.
- Qué no incluye: `LIKE '%term%'` como estrategia principal en tablas grandes.
- Sensible: permisos/ACL (filtrar antes de rankear), multi-idioma.
- Índices
- Qué incluye: indexar columnas de alta cardinalidad, usar compuestos alineados a WHERE/ORDER, considerar índices parciales cuando aplica.[^4]
- Qué no incluye: indexar todo “por si acaso” (costo de writes y mantenimiento).
- Sensible: degradación de escrituras, lock/maintenance, crecimiento de storage.
- Cache
- Qué incluye: TTL + jitter, stale-while-revalidate, request coalescing, métricas de hit/miss.[^7][^6]
- Qué no incluye: invalidación global por cada write (mata el cache).
- Sensible: consistencia vs frescura; “hot keys” y picos de expiración.
- Colas / batch / exports
- Qué incluye: jobs idempotentes, reintentos con backoff, rate limit por tenant, export streaming por chunks.
- Qué no incluye: exports “en una sola query gigante” y “en memoria”.
- Sensible: PII, cumplimiento, timeouts, límites del proveedor/DB.

***

## Anti-patterns

**Facts (2026-02-17):** Usar `OFFSET` profundo en Salesforce te lleva al límite de 2.000 y a problemas de escalado; es una señal de que necesitas paginación offset‑free.[^8][^1]
**Facts (2026-02-17):** Dejar expirar claves calientes sin mitigación provoca cache stampede/dogpile y picos contra el origen.[^7]
**Inferences (2026-02-17):** Anti-patterns típicos en CRMs:

- “Lista infinita” con `OFFSET` + sort no estable (duplicados, saltos).
- “Búsqueda” basada en wildcard inicial en campos grandes, sin estrategia full‑text ni límites.
- Índices sin relación con patrones de consulta (mucho costo, poco beneficio).
- Cache sin anti-stampede (picos) o con invalidación total (hit rate colapsa).
- Workers que consumen sin backpressure (DB al 100%, colas que crecen y timeouts en cascada).
- Exportación “todo o nada” que mantiene locks/tx abiertas y rompe la operación.

***

## Diagnostic questions

**Facts (2026-02-17):** ¿Tu producto/stack usa Salesforce y por ende está expuesto al límite de `OFFSET` 2.000 en SOQL para ciertas paginaciones?[^1]
**Inferences (2026-02-17):** Preguntas para diagnosticar rápido:

- ¿Qué 10 endpoints/listas concentran el 80% del tráfico operativo (ventas/CS/ops)?
- ¿Dónde existen “hot keys” de cache (dashboards, permisos, agregados) y qué pasa exactamente al expirar?
- ¿Qué consultas top tienen filtros de baja selectividad o devuelven poco pero escanean mucho?
- ¿Qué jobs asíncronos son re-ejecutables e idempotentes (sí/no) y cómo deduplicas eventos?
- ¿Cuál es tu política de límites por tenant (QPS, concurrencia de exports, tamaño de importaciones)?
- En exportaciones: ¿cuál es el time-to-first-byte y cómo reanudas tras fallos?

***

## Sources (o referencia a SOURCES.md)

- Salesforce Developers Docs — SOQL `OFFSET` clause (actualizado 2026-02-07).[^2]
- Salesforce Help — “Workaround for offset 2000 limit on SOQL query” (2022-10-12).[^1]
- TheSalesforceDev.in — “Server Side OFFSET-Free… Keyset Pagination” (2025-11-01).[^8]
- Percona — “A Practical Guide to PostgreSQL Indexes” (2025-08-26).[^5]
- MyDBOps — “PostgreSQL Index Best Practices…” (2025-08-06).[^4]
- DIVA portal (PDF) — Selectividad e índices compuestos / leftmost-prefix (sin fecha en snippet).[^3]
- OneUptime — “Redis Request Coalescing” (2026-01-20).[^6]
- Labvent — “Caching Strategies That Scale” (2025-09-10).[^7]

**Entradas sugeridas para agregar a `SOURCES.md` (sin duplicados):**

```md
- Salesforce Developers Docs — "OFFSET | SOQL and SOSL Reference" (2026-02-07) https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql_select_offset.htm
- Salesforce Help — "Workaround for offset 2000 limit on SOQL query" (2022-10-12) https://help.salesforce.com/s/articleView?id=000387840&language=en_US&type=1
- TheSalesforceDev.in — "Server Side OFFSET-Free Lazy Loading (Keyset Pagination)..." (2025-11-01) https://thesalesforcedev.in/2025/11/02/server-side-offset-free-lazy-loading-keyset-pagination-with-infinite-scroll-in-salesforce/
- Percona — "A Practical Guide to PostgreSQL Indexes" (2025-08-26) https://www.percona.com/blog/a-practical-guide-to-postgresql-indexes/
- MyDBOps — "PostgreSQL Index Best Practices for Faster Queries" (2025-08-06) https://www.mydbops.com/blog/postgresql-indexing-best-practices-guide
- OneUptime — "How to Implement Redis Request Coalescing" (2026-01-20) https://oneuptime.com/blog/post/2026-01-21-redis-request-coalescing/view
- Labvent — "Caching Strategies That Scale" (2025-09-10) https://www.labvent.co/blog/post/caching-strategies-that-scale/
- DIVA Portal (PDF) — "Evaluating Composite B-tree Indexing in PostgreSQL" https://www.diva-portal.org/smash/get/diva2:1987976/FULLTEXT01.pdf
```


***

## Key takeaways for PM practice

- Diseña listas grandes con cursor/keyset; `OFFSET` profundo es deuda (y en Salesforce puede ser un blocker).[^8][^1]
- Alinea índices con patrones reales (filtros + orden) y evita indexar baja cardinalidad “porque sí”.[^3][^4]
- En caching, planea el “día 2”: anti-stampede con request coalescing y expiración controlada, o tu mayor cliente te tumba el origen en hora pico.[^6][^7]
- Exportaciones y procesos masivos deben ser asíncronos, reanudables e idempotentes; sin eso, la operación sufre y ventas pierde confianza.
- Define límites por tenant y backpressure como producto (no solo infra): protegen margen, SLA y reputación B2B.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^9]</span>

<div align="center">⁂</div>

[^1]: https://help.salesforce.com/s/articleView?id=000387840\&language=en_US\&type=1

[^2]: https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql_select_offset.htm

[^3]: https://www.diva-portal.org/smash/get/diva2:1987976/FULLTEXT01.pdf

[^4]: https://www.mydbops.com/blog/postgresql-indexing-best-practices-guide

[^5]: https://www.percona.com/blog/a-practical-guide-to-postgresql-indexes/

[^6]: https://oneuptime.com/blog/post/2026-01-21-redis-request-coalescing/view

[^7]: https://www.labvent.co/blog/post/caching-strategies-that-scale/

[^8]: https://thesalesforcedev.in/2025/11/02/server-side-offset-free-lazy-loading-keyset-pagination-with-infinite-scroll-in-salesforce-lwc/

[^9]: pasted-text.txt

[^10]: https://www.linkedin.com/pulse/workaround-offset-2000-limit-soql-query-using-lwc-ganganapalli-csutc

[^11]: https://www.apexhours.com/soql-sosl-performance-tuning/

[^12]: https://dzone.com/articles/pagination-of-an-infinite-list-of-records-in-sales

[^13]: https://oneuptime.com/blog/post/2026-01-21-redis-cache-stampede/view

[^14]: https://stackoverflow.com/questions/56447511/how-to-handle-an-offset-greater-than-2000-on-soql-without-sorting-by-id-or-date

[^15]: https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/salesforce_soql_sosl.pdf

[^16]: https://oneuptime.com/blog/post/2026-01-30-composite-index-design/view

