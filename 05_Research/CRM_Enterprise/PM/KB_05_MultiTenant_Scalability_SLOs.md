# KB_05 — Multi-Tenant Scalability & SLOs

***

## Executive Summary

Los sistemas SaaS multi-tenant sirven a múltiples organizaciones (tenants) desde una infraestructura compartida, lo que exige un diseño explícito de aislamiento, escalabilidad y observabilidad por tenant. Este documento cubre los tres modelos canónicos de particionamiento de datos (silo, bridge, pool), las estrategias para mantener la performance de búsqueda a escala, los patrones de activity feeds/timelines, la ejecución justa de background jobs, y el framework completo de SLO/SLI con error budgets y burn rate alerting. Cada sección incluye métricas recomendadas, umbrales de alerta y consideraciones operativas para un entorno B2B donde la recurrencia y la confiabilidad son el diferenciador comercial. El objetivo es proveer una referencia RAG-ready que permita a equipos de producto y operaciones tomar decisiones informadas sobre aislamiento, fairness y observabilidad tenant-aware, con impacto directo en retención de clientes enterprise y cumplimiento de SLAs contractuales.

***

## Definitions and Why It Matters

### Definiciones clave

| Concepto | Definición |
|---|---|
| **Tenant** | Unidad lógica de cliente (organización/workspace) dentro de un sistema compartido [^1] |
| **Multi-tenancy** | Arquitectura donde una sola instancia de software sirve a múltiples tenants con aislamiento lógico o físico [^2] |
| **Silo model** | Cada tenant tiene recursos dedicados (DB, compute). Máximo aislamiento, mayor costo [^3][^4] |
| **Bridge model** | Tenants comparten una DB pero cada uno tiene su propio schema. Balance entre aislamiento y eficiencia [^3][^4] |
| **Pool model** | Todos los tenants comparten DB, schema y tablas. Se usa `tenant_id` como partition key. Mínimo costo, máximo riesgo de noisy neighbor [^3][^4] |
| **Noisy neighbor** | Cuando un tenant consume recursos desproporcionados y degrada la experiencia de otros [^5][^6] |
| **SLO (Service Level Objective)** | Meta interna de confiabilidad (ej: 99.9% disponibilidad mensual) [^7] |
| **SLI (Service Level Indicator)** | Métrica que mide el cumplimiento real del SLO (ej: ratio de requests exitosos) [^7] |
| **SLA (Service Level Agreement)** | Compromiso contractual con el cliente basado en SLOs [^8] |
| **Error budget** | 100% − SLO target. Margen de degradación tolerable antes de violar el objetivo [^7] |
| **Burn rate** | Velocidad a la que se consume el error budget. Burn rate = 1 significa consumo constante durante todo el período [^9] |

### Por qué importa (Fact)

En un negocio B2B mayorista, cada tenant (agencia) genera ingresos recurrentes. Un incidente de noisy neighbor o una caída de performance afecta directamente la retención. Multi-tenancy bien diseñada permite escalar clientes sin escalar costos linealmente, pero requiere controles explícitos de aislamiento, fairness y observabilidad.[^2][^1]

***

## Principles and Best Practices

### 1. Particionamiento de datos — Elegir el modelo correcto

**Fact:** AWS documenta tres modelos canónicos: silo, bridge y pool, cada uno con trade-offs distintos de costo, aislamiento y complejidad operativa.[^3]

| Dimensión | Silo (DB-per-tenant) | Bridge (Schema-per-tenant) | Pool (Shared schema) |
|---|---|---|---|
| Aislamiento de datos | Muy alto (físico) | Alto (lógico por schema) | Medio (depende de app-level filtering) |
| Costo por tenant | Alto | Medio | Bajo |
| Complejidad de deploy | Alta (N databases) | Media (N schemas, 1 DB) | Baja (1 schema) |
| Noisy neighbor risk | Nulo | Bajo-medio | Alto |
| Backup/restore granular | Fácil | Medio | Difícil |
| Ideal para | Tenants enterprise regulados | Tenants medianos con necesidad de aislamiento | Alto volumen de tenants pequeños |

**Best practice:** Empezar con pool model (shared schema + `tenant_id`) y diseñar el código para poder "graduar" tenants a bridge o silo cuando lo requieran por compliance, volumen o SLA premium.[^1][^2]

**Inference:** Para un mayorista con miles de agencias pequeñas y decenas de agencias enterprise, un modelo **híbrido** (pool default + silo para premium) maximiza eficiencia sin sacrificar el upside comercial de ofrecer aislamiento como feature de plan.

### 2. Tenant como objeto de primera clase

**Fact:** El `tenant_id` debe ser requerido, indexado y parte de constraints de unicidad en todo el modelo de datos. Queries sin `tenant_id` son bugs, no features.[^1]

```sql
-- ✅ Correcto: siempre scoped
SELECT * FROM invoices WHERE id = $1 AND tenant_id = $2;

-- ❌ Bug: cross-tenant read posible
SELECT * FROM invoices WHERE id = $1;
```

**Best practice:** Usar repositorios tenant-scoped que reciben el `tenant_id` en el constructor y lo inyectan automáticamente en toda query.[^1]

### 3. Performance de búsqueda en multi-tenant

**Fact:** PostgreSQL full-text search funciona bien hasta ~100K rows, pero degrada significativamente en datasets de millones de filas. Elasticsearch mantiene latencias de milisegundos incluso en datasets masivos gracias a su índice invertido optimizado con BM25.[^10][^11]

**Best practices de indexación multi-tenant:**

- Agregar `tenant_id` como primera columna de cualquier índice compuesto (btree, GIN, GiST) para que la búsqueda primero filtre por tenant[^12]
- Para PostgreSQL con GIN/GiST: instalar extensiones `btree_gin` o `btree_gist` para combinar búsqueda full-text con filtrado por tenant[^12]
- Para Elasticsearch: usar index-per-tenant (silo) o routing por `tenant_id` (pool) para garantizar que queries solo toquen shards relevantes[^13]
- Considerar `pg_search` (BM25 nativo en Postgres) que muestra performance 20-1000x superior al FTS nativo y comparable a Elasticsearch[^10]

**Inference:** Para un CRM B2B con búsqueda de contactos/reservas, Postgres + índices compuestos con `tenant_id` al frente es suficiente hasta escala media. Si la búsqueda debe ser real-time sobre catálogos grandes (destinos, hoteles, tarifas), Elasticsearch con routing por tenant ofrece mejor escalabilidad.

### 4. Timelines y Activity Feeds

**Fact:** Los activity feeds usan el patrón **fan-out** que tiene dos variantes principales:[^14]

- **Fan-out-on-write (push):** Al crear un evento, se escribe inmediatamente en el timeline de cada suscriptor. Lecturas rápidas, writes costosos.
- **Fan-out-on-read (pull):** El evento se almacena una vez; cada usuario lo consulta al abrir su timeline. Writes baratos, reads más lentos.

**Best practice para multi-tenant:**

- Usar **fan-out-on-write** para eventos críticos (cambios de estado de reserva, alertas de pricing) donde la latencia de lectura importa
- Usar **fan-out-on-read** para feeds de actividad secundarios (logs de auditoría, historial)
- Modelo híbrido: push para tenants activos, pull para inactivos o datos históricos[^14]
- Incluir `tenant_id` + timestamps en la clave de partición para evitar hot spots y garantizar aislamiento de lectura

**Inference:** En un contexto de turismo B2B, el timeline de "últimos cambios en cotizaciones/reservas de mi agencia" es un fan-out-on-write scoped a tenant_id + agencia. No necesita escala social-media, pero sí consistencia.

### 5. Background Jobs con Fairness por Tenant

**Fact:** En sistemas multi-tenant, un tenant que genera exceso de jobs puede monopolizar los workers y crear un efecto noisy neighbor en la cola.[^6][^15][^16]

**Patrones de fairness:**

| Patrón | Descripción | Pros | Contras |
|---|---|---|---|
| Queue-per-tenant | Cada tenant tiene su propia cola; workers poll round-robin [^17] | Fuerte aislamiento | Overhead de muchas colas |
| Priority queue adaptativa | Bajar prioridad de tenants con mucho volumen [^18] | Eficiente | Complejo de implementar bien |
| Concurrency limits por tenant | Limitar ejecuciones concurrentes por tenant [^15] | Simple y efectivo | Requiere estado por tenant |
| Time-boxed processing | Procesar máximo N items por tenant antes de rotar [^6] | Fairness garantizada | Posible latencia adicional |

**Best practice (Temporal/Inngest pattern):** Task queues per tenant con workers que pollan múltiples queues. Implementar per-tenant rate limiting y mover tenants problemáticos a workers dedicados.[^17][^15]

**Fact:** `SKIP LOCKED` en PostgreSQL permite construir colas ligeras, pero lograr fairness round-robin entre tenants requiere lógica adicional de partición o prioridad dinámica.[^18]

### 6. Mitigación del Noisy Neighbor

**Fact:** Las estrategias principales son:[^5][^19][^6]

1. **Per-tenant rate limiting** en la capa de API (quotas de operaciones/tiempo)
2. **Service isolation** con límites de recursos por contenedor/servicio
3. **Connection pool tiering** (Enterprise: 50 conexiones, Premium: 20, Basic: 5)[^19]
4. **Workload segregation** — operaciones pesadas (reportes, bulk imports) de forma asíncrona con fairness rules[^19]
5. **Tenant-level kill switches** — poder deshabilitar un tenant sin afectar la plataforma[^1]
6. **Proactive monitoring** con alertas por spike de recursos por tenant[^5]

***

## SLO / SLI Framework

### Definiciones operativas

**Fact:** Google SRE define las "4 Golden Signals" como base para SLIs: **Latency**, **Traffic**, **Errors**, **Saturation**.[^20][^21]

| Golden Signal | SLI recomendado | Impacto de negocio |
|---|---|---|
| **Latency** | p50, p95, p99 de response time | Satisfacción del usuario, tasa de conversión (+100ms = −7% conversión) [^20] |
| **Traffic** | Requests/segundo por tenant | Engagement, crecimiento |
| **Errors** | Ratio de 5xx / total requests | Frustración, tickets de soporte |
| **Saturation** | CPU, memoria, conexiones DB, disk I/O | Escalabilidad, eficiencia de costos |

### Targets recomendados por tier

| Tipo de servicio | SLO Target | Error Budget (30 días) | Contexto |
|---|---|---|---|
| API user-facing crítica | 99.9% | 43.8 min/mes | Booking, pagos [^7] |
| API user-facing estándar | 99.5% | 3.6 hrs/mes | Búsqueda, catálogo |
| APIs internas | 99.0% | 7.3 hrs/mes | Servicios internos sin user impact directo [^7] |
| Background jobs | 99.0% | 7.3 hrs/mes | Processing asíncrono |

**Best practice:** Empezar con 2-3 SLIs críticos por servicio. No medir todo — la abundancia de indicadores diluye el foco.[^7]

### Error Budget y Burn Rate Alerting

**Fact:** Google recomienda un esquema de multi-window, multi-burn-rate alerting:[^9][^7]

| Tipo de alerta | Ventana | Consumo tolerado | Burn Rate | Tiempo hasta agotar budget |
|---|---|---|---|---|
| **Fast burn** (crítico) | 1 hora | 2% del budget | 13.44x (para SLO 99.9%, 28 días) | ~50 horas |
| **Slow burn** (warning) | 6 horas | 5% del budget | 5.6x | ~5 días |
| **Budget exhaustion** | Rolling period | 80% consumido | N/A | N/A |

**Fórmula de burn rate crítico**:[^9]

\[
\text{critical burn rate} = \frac{\text{tolerated budget consumption} \times \text{SLO period [h]}}{\text{evaluation period [h]}}
\]

**Ejemplo concreto:** Para SLO 99.9% en ventana de 28 días:[^9]
- Error budget = 0.1%
- Fast burn threshold = error_budget × critical_burn_rate = 0.001 × 13.44 = 0.01344
- Maximum burn rate = 1/(1 − 0.999) = 1000

**Best practice:** New Relic recomienda fast burn alert = 2% budget en 1 hora; slow burn alert = 5% budget en 6 horas. Configurar también alerta de budget exhaustion al 80% consumido.[^9]

***

## Observabilidad Multi-Tenant

### Instrumentación con OpenTelemetry

**Fact:** OpenTelemetry permite tagear cada trace, métrica y log con `tenant.id`, habilitando debugging per-tenant, capacity planning y SLA monitoring.[^22]

**Patrón de implementación:**

1. **Middleware** extrae `tenant_id` (JWT, subdomain, header) y lo inyecta en el span activo + baggage de OTel[^22]
2. **Propagación** vía W3C Baggage header a servicios downstream (HTTP) y headers explícitos para message queues (Kafka, RabbitMQ)[^22]
3. **Métricas per-tenant** con dimensiones `tenant.id`, `tenant.plan`, `http.route`[^22]
4. **Sampling tenant-aware:** 100% para enterprise, 20% para standard, 5% para free[^22]
5. **Routing en collector:** enterprise a backend dedicado, otros a backend compartido[^22]

### Métricas recomendadas por categoría

| Categoría | Métrica | Dimensiones | Alerta recomendada |
|---|---|---|---|
| **Disponibilidad** | `http.server.request.duration_count` (ratio 2xx/total) | tenant_id, endpoint | < SLO target en ventana de 5 min |
| **Latencia** | p99 de `http.server.request.duration` | tenant_id, endpoint | p99 > 500ms por tenant [^22] |
| **Errores** | Tasa de 5xx por tenant | tenant_id, status_code | > 1% error rate sostenido |
| **Saturación** | CPU, memoria, conexiones DB por tenant | tenant_id, resource_type | > 80% de quota asignada |
| **Noisy neighbor** | `tenant.quota.exceeded` counter | tenant_id, resource_type | Cualquier incremento [^22] |
| **Background jobs** | Queue backlog, completion rate, failure rate por tenant | tenant_id, job_type | Backlog > threshold o failure rate > 5% [^17] |
| **Search** | Latencia de búsqueda por tenant | tenant_id, search_type | p95 > 200ms |
| **Error budget** | Burn rate por SLO | service, slo_name | Fast burn > 13.4x, slow burn > 5.6x [^9] |

### Dashboards per-tenant (Grafana/PromQL)

**Fact:** Queries de ejemplo para dashboards SLA per-tenant:[^22]

```promql
# Availability SLI
sum(rate(http_server_request_duration_count{
  tenant_id="$tenant",
  http_status_code!~"5.."
}[5m]))
/
sum(rate(http_server_request_duration_count{
  tenant_id="$tenant"
}[5m]))

# Latency SLI (p99)
histogram_quantile(0.99,
  sum(rate(http_server_request_duration_bucket{
    tenant_id="$tenant"
  }[5m])) by (le)
)
```

### Control de cardinalidad

**Fact:** Con 10,000 tenants × 50 endpoints = 500,000 series temporales solo para latencia. Estrategias de control:[^22]

- Agregar tenants free-tier en bucket "aggregated_free_tier"
- Mantener granularidad completa solo para tenants de pago
- Usar tail-based sampling diferenciado por plan

***

## Examples (Aplicado a CRM Enterprise / Mayorista B2B)

### Ejemplo 1: Particionamiento híbrido para mayorista de turismo

**Escenario:** Plataforma B2B con 2,000 agencias pequeñas y 15 agencias enterprise.

- **Pool** (shared schema + `tenant_id`) para las 2,000 agencias con Row-Level Security (RLS)
- **Silo** (DB dedicada) para las 15 enterprise con SLA contractual y datos sensibles
- Tenant lookup table en el control plane para enrutar requests al pool o silo correcto

### Ejemplo 2: Búsqueda de disponibilidad por tenant

```sql
-- Índice compuesto tenant-first para búsqueda de hoteles
CREATE INDEX idx_hotels_tenant_search 
ON hotels(tenant_id, destination, category) 
INCLUDE (name, price_from);

-- Query siempre scoped
SELECT name, price_from 
FROM hotels 
WHERE tenant_id = $1 
  AND destination ILIKE $2 || '%'
  AND category = $3
ORDER BY price_from
LIMIT 20;
```

### Ejemplo 3: Background job fairness para generación de cotizaciones

- Cada agencia puede generar bulk quotes
- Concurrency limit = 3 jobs concurrentes por tenant
- Si un tenant excede, jobs adicionales van a low-priority queue
- Monitor: `tenant.jobs.queued` y `tenant.jobs.active` con alerta si backlog > 100 por más de 5 min

***

## Metrics / Success Signals

| Signal | Métrica | Target | Fuente |
|---|---|---|---|
| Aislamiento efectivo | Incidentes cross-tenant por trimestre | 0 | Logs de auditoría |
| Noisy neighbor incidents | Alertas de quota exceeded / mes | < 5 | Monitoring [^22] |
| SLO compliance | % de ventanas cumplidas | > 99% de períodos en target | SLO dashboard [^7] |
| Search performance | p95 latencia de búsqueda por tenant | < 200ms | APM |
| Job fairness | Desviación estándar de wait-time entre tenants | < 2x del promedio | Job monitoring |
| Error budget health | % de budget restante al cierre de período | > 20% | Burn rate monitoring [^9] |
| Time to detect (TTD) | Tiempo desde degradación hasta alerta | < 5 min (fast burn) | Alert logs |
| Time to resolve (TTR) | Tiempo desde alerta hasta resolución | < 30 min (P1) | Incident management |

***

## Operational Checklist

- [ ] `tenant_id` es columna NOT NULL indexada en todas las tablas de negocio
- [ ] Repositorios/DAOs son tenant-scoped por construcción (no por convención)
- [ ] Row-Level Security (RLS) habilitado como segunda capa de defensa en pool model
- [ ] Índices compuestos tienen `tenant_id` como primera columna
- [ ] Per-tenant rate limiting implementado en API gateway
- [ ] Background jobs tienen concurrency limits por tenant
- [ ] Kill switch por tenant implementado y probado
- [ ] OpenTelemetry middleware inyecta `tenant.id` en spans, métricas y logs
- [ ] Tenant context se propaga a servicios downstream vía W3C Baggage
- [ ] Sampling diferenciado por plan de tenant configurado en collector
- [ ] SLOs definidos con 2-3 SLIs por servicio crítico
- [ ] Fast burn alert (1h, 2% budget) y slow burn alert (6h, 5% budget) configurados
- [ ] Dashboard per-tenant de availability y latency disponible
- [ ] Error budget consumption alert al 80% configurado
- [ ] Proceso de expand → backfill → contract documentado para migraciones
- [ ] Tenant cache keys incluyen `tenant_id` en toda capa de caché
- [ ] Plan de "graduación" de tenants (pool → bridge → silo) documentado

***

## Anti-Patterns

| Anti-pattern | Riesgo | Alternativa correcta |
|---|---|---|
| **Queries sin `tenant_id`** | Data leak cross-tenant | Repositorios tenant-scoped obligatorios [^1] |
| **Cache keys sin tenant scope** | Un tenant ve datos de otro | Incluir `tenant:{id}` en toda cache key [^1] |
| **Single shared queue sin fairness** | Un tenant monopoliza processing | Per-tenant concurrency limits + priority queues [^6][^15] |
| **SLOs basados en infra (CPU, RAM)** | No reflejan experiencia del usuario | SLIs user-centric: latencia, error rate, availability [^7] |
| **Alertas con thresholds estáticos** | Alert fatigue en picos, missed alerts en valles | Burn rate alerting con multi-window [^9] |
| **Medir demasiados SLIs** | Dilución de foco, overhead operativo | Máximo 2-3 SLIs por servicio [^7] |
| **Observabilidad sin `tenant_id`** | No puedes responder "¿es este tenant o todos?" | Tagear toda telemetría con tenant context [^22] |
| **Misma sampling rate para todos** | Enterprise sin visibilidad o free-tier con costo excesivo | Sampling diferenciado por plan [^22] |
| **Migrar schema con downtime** | Afecta a todos los tenants simultáneamente | Expand → backfill → contract [^1] |
| **Auto-crear tenants sin validación** | Sprawl de tenants fantasma, problemas de soporte | Require explicit onboarding flow [^1] |

***

## Diagnostic Questions

1. **¿Puedo identificar qué tenant está causando degradación en < 5 minutos?** Si no, falta tenant-aware observability.
2. **¿Qué pasa si un tenant genera 100x su volumen normal de jobs?** Si no hay respuesta clara, falta fairness en background processing.
3. **¿Puedo desactivar un tenant sin afectar a otros?** Si no, falta kill switch.
4. **¿Mis SLOs miden experiencia del usuario o salud de infraestructura?** Si es lo segundo, necesitas repensar tus SLIs.
5. **¿Cuánto error budget me queda para este período?** Si nadie sabe la respuesta, no hay burn rate monitoring.
6. **¿Puedo restaurar los datos de un solo tenant sin afectar a otros?** Si no, evalúa tu estrategia de backup según modelo de partición.
7. **¿Las cache keys incluyen `tenant_id`?** Auditar una muestra. Un solo miss es un data leak potencial.
8. **¿Tengo un camino documentado para graduar un tenant de pool a silo?** Si no, el día que un enterprise lo pida será una crisis.
9. **¿Los índices de búsqueda tienen `tenant_id` como primera columna?** Si no, la performance de búsqueda degradará con cada tenant nuevo.
10. **¿Mis alertas de SLO usan burn rate o thresholds fijos?** Si es lo segundo, estás o sobre-alertando o sub-detectando.

***

## Sources

| # | Fuente | Fecha | Tipo |
|---|---|---|---|
| 1 | AWS — SaaS Partitioning Models | 2024 | Whitepaper |
| 2 | AWS — Silo, Pool, and Bridge Models | 2024 | Documentation |
| 3 | Bluent — Serverless SaaS Multi-Tenancy | Jan 2026 | Blog |
| 4 | Microsoft Azure — Multitenant SaaS Patterns | Aug 2025 | Documentation |
| 5 | OneUptime — Instrument Multi-Tenant with OTel | Feb 2026 | Guide |
| 6 | WorkOS — Developer's Guide to Multi-Tenant Architecture | Dec 2025 | Guide |
| 7 | Nobl9 — SLO Best Practices | 2022 | Guide |
| 8 | New Relic — Alerting on Service Levels | 2025 | Documentation |
| 9 | Mark Heath — Mitigating Noisy Neighbour | Oct 2024 | Blog |
| 10 | Neon — Noisy Neighbor in Multitenant | Apr 2025 | Blog |
| 11 | Scalable Thread — Multi-Tenant Performance Issues | Oct 2024 | Newsletter |
| 12 | Temporal — Multi-Tenant Patterns | 2025 | Documentation |
| 13 | Inngest — Fixing Multi-Tenant Queueing | Jun 2024 | Blog |
| 14 | GetStream — Fan-Out Architecture | Dec 2024 | Reference |
| 15 | Neon — Postgres FTS vs Elasticsearch | Jun 2025 | Benchmark |
| 16 | Coralogix — Advanced SLO Alerting | Aug 2025 | Blog |
| 17 | Scalewithchintan — Architecting Multi-Tenant DBs | Dec 2025 | Blog |

***

## Key Takeaways for PM Practice

- **Tenancy es dimensión de primera clase:** `tenant_id` no es metadata opcional, es constraint arquitectónico. Sin él, no tienes multi-tenancy — tienes multi-customer con data leaks potenciales.
- **Modelo híbrido > dogma:** Pool para el long-tail, silo para enterprise. Diseña el código para que la "graduación" de tenant sea configuración, no rewrite.
- **Fairness en jobs es retención:** Una agencia cuya cotización tarda 10x porque otra agencia hizo un bulk import no renovará. Per-tenant concurrency limits son no-negociables.
- **SLOs user-centric > SLOs de infra:** "CPU al 40%" no dice nada. "99.9% de búsquedas de disponibilidad completan en < 200ms" sí es una promesa comercial.
- **Burn rate > thresholds estáticos:** Fast burn (1h/2%) para crisis, slow burn (6h/5%) para tendencias. Elimina alert fatigue y detecta problemas reales.
- **Observabilidad per-tenant es el foundation:** Sin `tenant.id` en traces, métricas y logs, la respuesta a "¿quién está afectado?" siempre será "no sé".
- **Kill switch es seguro de vida:** La capacidad de deshabilitar un tenant sin deploy es una de las herramientas más valiosas del toolkit operativo multi-tenant.

---

## References

1. [The developer's guide to SaaS multi-tenant architecture - WorkOS](https://workos.com/blog/developers-guide-saas-multi-tenant-architecture) - A practical, end-to-end deep dive into data isolation, tenant-aware auth, scaling, and compliance fo...

2. [Architecting Multi-Tenant Databases: Strategies for Scalability and ...](https://scalewithchintan.com/blog/architecting-multi-tenant-databases) - Exploring the core strategies for designing robust multi-tenant database systems, focusing on data i...

3. [SaaS partitioning models - SaaS Storage Strategies](https://docs.aws.amazon.com/whitepapers/latest/multi-tenant-saas-storage-strategies/saas-partitioning-models.html) - The following figure shows the three basic models—silo, bridge, and pool—that are commonly used when...

4. [Serverless SaaS Architecture: Scaling Multi-Tenant Apps Efficiently](https://www.bluent.net/blog/serverless-saas-multi-tenancy) - The three key patterns are: Silo where each tenant gets isolated resources; Pool: where all tenants ...

5. [How to Handle Multi-Tenant Performance Issues or "Noisy Neighbor ...](https://newsletter.scalablethread.com/p/how-to-handle-multi-tenant-performance) - Understanding How to Avoid Performance Degradation Caused by Noisy Neighbors in Multi-Tenant Systems...

6. [Mitigating the Noisy Neighbour Multitenancy Problem](https://markheath.net/post/noisy-neighbour-multi-tenancy) - 2. Rate-limiting APIs. Another option at our disposal for mitigating noisy-neighbour issues is to ad...

7. [SLO Best Practices: A Practical Guide - Nobl9](https://www.nobl9.com/service-level-objectives/slo-best-practices) - Alerting on SLOs: from metrics to action​​ Multi-burn rate alerting methodology prevents both missed...

8. [SLO vs SLA: A Best Practices Guide - Nobl9](https://www.nobl9.com/service-level-objectives/slo-vs-sla) - Learn how to develop and differentiate between the related but distinct metrics of SLOs and SLAs, in...

9. [Alerting on service levels | New Relic Documentation](https://docs.newrelic.com/docs/service-level-management/alerts-slm/) - For a 28 day SLO, Google recommends alerting on a 2% SLO budget consumption in the last hour. That m...

10. [Comparing Native Postgres, ElasticSearch, and pg_search for Full ...](https://neon.com/blog/postgres-full-text-search-vs-elasticsearch) - Do you need to reach for ElasticSearch for full-text search, or can you double down on Postgres? We ...

11. [Full-text search engine with PostgreSQL (part 2): Postgres vs ... - Xata](https://xata.io/blog/postgres-full-text-search-postgres-vs-elasticsearch) - We're going to compare the convenience, search relevancy, performance, and scalability of the two op...

12. [Indexing strategy for full text search in a multi-tenant PostgreSQL ...](https://stackoverflow.com/questions/12486642/indexing-strategy-for-full-text-search-in-a-multi-tenant-postgresql-database) - You should add the account identifier as the first column of any index you create. This will in effe...

13. [Weaviate's Native, Efficient and Optimized Multi-Tenancy](https://weaviate.io/blog/weaviate-multi-tenancy-architecture-explained) - Learn how Weaviate's native multi-tenancy architecture delivers scalable vector search with one shar...

14. [Fan-Out - What is it and how does it work? - GetStream.io](https://getstream.io/glossary/fan-out/) - Fan-out works by distributing a single event into multiple, parallel tasks or messages and executing...

15. [Fixing noisy neighbor problems in multi-tenant queueing systems](https://www.inngest.com/blog/fixing-multi-tenant-queueing-concurrency-problems) - In this post, we'll walk through these approaches and how Inngest is purpose-built to handle multi-t...

16. [Fair background processing in a multi-tenant system? - Reddit](https://www.reddit.com/r/ExperiencedDevs/comments/1fl92f2/fair_background_processing_in_a_multitenant_system/) - We're evaluating solutions for background processing, aka job/task systems, especially for a multite...

17. [Multi-tenant application patterns | Temporal Platform Documentation](https://docs.temporal.io/production-deployment/multi-tenant-patterns) - Learn how to build multi-tenant applications using Temporal with task queue isolation patterns, work...

18. [Building a fair multi-tenant queuing system | Hacker News](https://news.ycombinator.com/item?id=39092849) - I found Amazon's Builders Library to have a very insightful list of how to handle building multi ten...

19. [The Noisy Neighbor Problem in Multitenant Architectures - Neon](https://neon.com/blog/noisy-neighbor-multitenant) - The most effective solution to noisy neighbors in RDS is full database-per-tenant isolation, giving ...

20. [SRE Golden Signals: Performance Metrics That Matter - Odown Blog](https://odown.com/blog/sre-golden-signals/) - For example, an SLI might be "99% of requests complete in under 200ms." This translates raw metrics ...

21. [Going for the Gold: Monitoring the Four Golden Signals in K8s](https://www.groundcover.com/blog/monitor-the-four-golden-signals) - The four golden signals concept is a great way to be strategic about which data you monitor – and to...

22. [How to Instrument a SaaS Multi-Tenant Application ... - OneUptime](https://oneuptime.com/blog/post/2026-02-06-instrument-saas-multi-tenant-application-opentelemetry/view) - Learn how to instrument a multi-tenant SaaS application with OpenTelemetry to get per-tenant observa...

