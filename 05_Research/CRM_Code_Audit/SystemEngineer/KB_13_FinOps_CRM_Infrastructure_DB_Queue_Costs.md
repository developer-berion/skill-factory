<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_13_FinOps_CRM_Infrastructure_DB_Queue_Costs

## Executive summary (10–15 líneas)

[Facts] En un CRM multi-tenant, la infraestructura “silenciosa” (DB, índices, exports, colas, storage y observabilidad) suele explicar una parte relevante del COGS y de incidentes de performance.
[Inferences] El objetivo FinOps aquí no es “bajar el bill”, sino **atribuir** costo por tenant y por feature para decidir pricing, límites y prioridades de ingeniería.
[Facts] Showback es visibilidad de costos por producto/equipo sin mover el gasto a sus presupuestos; chargeback sí formaliza el traspaso a P\&L/budgets internos.[^1]
[Inferences] Para CRM enterprise, showback interno funciona mejor si se expresa en moneda y unidades físicas (GB, IOPS, requests), no en “tokens” abstractos.
[Facts] En bases de datos gestionadas, señales como FreeableMemory e IOPS de lectura/escritura ayudan a detectar sobre/sub aprovisionamiento y sus costos asociados.[^2]
[Facts] En PostgreSQL, más/extra índices incrementan trabajo de VACUUM/Autovacuum y mantenimiento; y el bloat de tablas/índices eleva storage e I/O.[^3][^4][^5]
[Facts] Exportar snapshots puede cobrarse por GB del tamaño completo del snapshot, incluso si exportas parcialmente (por schema/tabla).[^6]
[Facts] En colas tipo SQS, el costo se mueve por requests y el tamaño del payload (chunks), así que “chatty + payload grande” escala directo en gasto.[^7]
[Facts] Observabilidad típicamente cobra por ingesta, almacenamiento y consulta; si no controlas retención/cardinalidad, el costo crece de forma monotónica.[^8]
[Inferences] Quick wins: higiene (índices/retención/sampling/batching); estructural: rediseñar particionamiento multi-tenant, aislar “ballenas”, y productizar límites por feature.
[Inferences] Este documento entrega drivers, métricas por tenant/feature, un modelo de showback interno y un checklist de instrumentación listo para operar.

***

## Definitions and why it matters

[Facts] **Showback**: método de asignación/visibilidad de costos que muestra cargos por producto/departamento sin facturar internamente.[^1]
[Facts] **Chargeback**: asigna responsabilidad financiera formal a equipos/departamentos (se refleja en presupuestos oficiales).[^1]
[Inferences] **Cost driver**: variable técnica que explica el costo (p. ej., IOPS, GB-mes, requests, GB ingeridos en logs) y permite atribución consistente por tenant/feature.
[Inferences] Importa porque en CRM enterprise la conversación con negocio no es “la DB está cara”, sino “qué clientes/funciones están empujando DB/colas/observabilidad y qué decisión tomamos: precio, límites, arquitectura o backlog”.

***

## Principles and best practices (con citas por sección + fecha)

### 1) Showback interno “en moneda” (no tokens)

[Facts] La diferencia práctica: showback muestra costos por unidad organizativa sin mover el gasto a su P\&L; chargeback sí lo hace, y depende de política contable.[^1]
[Inferences] En CRM, evita “puntos/tokens” internos: usa \$/tenant/mes y desglósalo por dominios (DB, queue, storage, observabilidad) con unidades físicas detrás para auditabilidad.
[Inferences] Regla operativa: si un equipo no puede explicar el número con 2–3 métricas (GB, IOPS, req), no es showback útil; es ruido.

Fecha de referencia (fuente principal): 2024-06-30.[^1]

### 2) Atribución por drivers medibles (tenant + feature)

[Facts] OpenTelemetry no “trae multi-tenancy” listo; para atribución se recomienda medir volumen de telemetría por tenant (p. ej., contar spans por tenant) vía collector.[^9]
[Facts] Se puede controlar costo de observabilidad manteniendo granularidad por tenants de pago y agregando/sampling para tiers free, reduciendo cardinalidad.[^10]
[Inferences] Para CRM enterprise, tu “clave de costo” mínima debería ser: tenant_id, feature_name, tier/plan, y environment; todo lo demás (equipo, región, canal) es secundario.

Fecha de referencia: 2026-02-05.[^9][^10]

### 3) DB: dimensiona por señales, no por miedo

[Facts] Métricas como FreeableMemory e IOPS de lectura/escritura sirven para identificar oportunidades de right-sizing o detectar IOPS sobreaprovisionado como driver de costo.[^2]
[Inferences] En multi-tenant CRM, separa “costo por capacidad” (instancia/cluster base) de “costo por actividad” (IOPS/queries/WAL) para evitar castigar a tenants pequeños por el “mínimo viable” de plataforma.
[Inferences] Si no puedes medir IOPS/latencia por tenant, al menos mide por feature (endpoints/reporting/jobs) y asigna por proporción de actividad.

Fecha de referencia: 2024-04-10.[^2]

### 4) Índices: cada índice es performance… y factura

[Facts] VACUUM/Autovacuum escanea y limpia también los índices asociados, así que más índices incrementan trabajo de mantenimiento.[^5]
[Facts] El bloat (tabla/índice) aumenta consumo de disco y puede degradar performance; VACUUM ayuda a manejar dead rows pero tiene trade-offs de recursos.[^3]
[Facts] Mantener un set de índices “lean” reduce autovacuum work y también genera menos WAL, impactando replicación/backups.[^4]
[Inferences] Best practice FinOps-DB: cada índice debe tener “dueño” (feature) + prueba de uso (query stats) + costo estimado (tamaño + write amplification).

Fechas de referencia: 2024-12-03, 2024-01-30, 2025-11-09.[^4][^5][^3]

### 5) Exports: el “costo fantasma” de compliance y analytics

[Facts] Export de snapshots a S3 puede cobrarse por GB del tamaño completo del snapshot, incluso si exportas parcialmente.[^6]
[Facts] Mientras un export task corre, sigues pagando el storage del snapshot hasta que termine.[^11]
[Inferences] Política sana: exports sólo por demanda (o por retención regulatoria explícita), con budget guardrails, y con ownership por feature (Reporting/Compliance/DataOps).

Fechas de referencia: 2020-05-28, 2019-08-11.[^11][^6]

### 6) Colas: requests + payload = costo lineal (y backlog = riesgo)

[Facts] En SQS, una request puede incluir 1–10 mensajes y el payload se factura por chunks (p. ej., cada 64KB cuenta como “1 request” adicional).[^7]
[Facts] AWS indica que no cobra data transfer al enviar/recibir mensajes de SQS si los recursos están en la misma región.[^12]
[Inferences] “Quick win” universal: batching + payload pequeño + idempotencia (para bajar retries) suele ser la palanca más rápida sin tocar arquitectura.

Fechas de referencia: 2025-11-25, 2026-02-11.[^12][^7]

### 7) Observabilidad: ingesta, storage, consulta (triple peaje)

[Facts] En CloudWatch Logs (ejemplo representativo), el costo se compone de ingesta, almacenamiento y consultas; si no defines retención, el storage crece con el tiempo.[^8]
[Inferences] En CRM enterprise, la observabilidad debe ser “value-based”: full fidelity para tenants enterprise y features críticas; sampling/agregación para long-tail.

Fecha de referencia: 2026-02-14.[^8]

***

## Examples (aplicado a CRM enterprise)

### Ejemplo A: Showback mensual por tenant (sin tokens)

[Facts] Showback es visibilidad sin imputación formal a presupuestos internos.[^1]
[Inferences] Output recomendado (ejemplo):

- Tenant ACME: \$1,240/mes = DB \$620 + Storage \$140 + Queue \$80 + Observabilidad \$400.
- Drivers trazables: DB (read/write IOPS, storage GB); Queue (requests, avg payload KB); Observabilidad (log GB, span count).

[Inferences] Fórmula simple (por dominio) para asignar costo variable:

- $costo\_tenant = costo\_total\_dominio \times \frac{driver\_tenant}{\sum driver\_todos}$


### Ejemplo B: Atribución por feature (para decidir pricing o límites)

[Facts] Es viable contar spans por tenant en el collector y obtener una métrica tipo `tenant.span.count` para showback/atribución.[^9]
[Inferences] En CRM, define “feature_name” como el producto real que vende el negocio:

- `reporting_exports` (exports/snapshots)
- `bulk_import_contacts` (DB writes + queue)
- `activity_sync` (colas + retries)
- `audit_trail` (storage + observabilidad)

[Inferences] Luego creas un “P\&L técnico” por feature: costo mensual + margen estimado + top tenants consumidores, y priorizas: (1) subir precio/packaging, (2) límites, (3) refactor.

### Ejemplo C: Control de costo de observabilidad por tier

[Facts] Se puede bucketing/agregación para reducir cardinalidad en métricas por tenant, manteniendo detalle para tenants pagadores.[^10]
[Inferences] Política típica:

- Enterprise: 100% traces + logs completos en incidentes.
- Pro/SMB: sampling 10–20% en traces, logs con límites por request.
- Free: métricas agregadas + sampling bajo, para no subsidiar.

***

## Metrics / success signals

### Métricas mínimas por tenant (drivers)

[Inferences] **DB**

- GB almacenados por tenant (tabla + índices si es posible).
- Read IOPS / Write IOPS por tenant (o proxy por feature/endpoints si no hay visibilidad directa).
- Queries/seg, conexiones activas, WAL generado (proxy de write amplification).

[Inferences] **Índices**

- Top-N índices por tamaño (GB) y por write overhead (updates/inserts afectados).
- Ratio de uso (queries que lo tocan) vs costo (tamaño + mantenimiento).

[Inferences] **Exports**

- 
# exports/mes, GB exportados (o GB snapshot cobrado), duración de export task.

- Egress/transfer asociado (si aplica fuera de región/cuenta).

[Inferences] **Colas**

- Requests (send/receive/delete), mensajes en vuelo, edad del mensaje más antiguo (backlog).
- Avg payload KB; retries/redrives a DLQ.

[Inferences] **Storage**

- GB-mes por tipo (hot/cold), requests (PUT/GET/LIST) por tenant/feature.
- Retención efectiva (días) vs política.

[Inferences] **Observabilidad**

- Log GB ingeridos por tenant/feature; spans por tenant (ej. `tenant.span.count`); cardinalidad de labels.
[Facts] Contar spans por tenant es un patrón soportado a nivel collector para atribución de costos.[^9]


### Success signals (operativos y comerciales)

[Inferences]

- 90%+ de costo variable atribuible a tenant o feature (no “shared/unknown”).
- Top 10 tenants por costo explicados por 3 drivers cada uno (auditables).
- Reducción de crecimiento de observabilidad con retención/sampling sin degradar MTTR.
- Pricing/packaging actualizado: features caros (exports, audit, bulk) monetizados o limitados.

***

## Operational checklist

### Checklist de instrumentación (lista “de verdad”)

[Inferences]

- Estándar de dimensiones: `tenant.id`, `tenant.plan/tier`, `feature.name`, `env`, `region`, `workspace/account` (si aplica).
- Propagación obligatoria en sync + async: headers/context en APIs, y metadata en mensajes de cola.
- DB attribution: tags por conexión (application_name / role), y logging de “query fingerprint” a nivel feature cuando sea viable.
- Queue attribution: incluye `tenant.id` y `feature.name` en atributos del mensaje (o en el envelope), y mide payload size.
- Storage attribution: prefijos/buckets por tenant o por feature cuando sea posible; si no, metadatos/manifest para reconstruir.
- Exports: cada export task debe registrar `tenant.id`, `feature.name`, “motivo” (compliance/analytics/support) y owner.
- Observabilidad: métricas por tenant con control de cardinalidad (bucketing de free), sampling por tier, límites de logs por request.

[Facts] Un enfoque concreto para atribución de telemetría es producir métricas por tenant desde el collector (p. ej., conteo de spans por tenant).[^9]
[Facts] Estrategias como bucketing por plan ayudan a controlar cardinalidad/costo manteniendo visibilidad donde hay SLA.[^10]

### Quick wins vs structural (para priorizar)

[Inferences] **Quick wins (1–2 sprints)**

- Índices: eliminar/merge de índices no usados; revisar duplicados; detener “index creep” por feature owner.
- DB: right-size guiado por señales (memoria libre alta, IOPS sobrado); optimizar queries “top offenders”.
- Exports: apagar exports automáticos sin ROI; programar ventanas; deduplicar exports por tenant.
- Colas: batching; reducir payload; backoff; dedupe/idempotencia para bajar retries.
- Observabilidad: retención explícita; sampling por tier; bajar verbosidad de logs en paths calientes.

[Inferences] **Structural (trimestres)**

- Aislamiento de “ballenas”: partición por tenant (shards/DB separados) o límites fuertes por plan.
- Multi-tenant data model: particionado por tenant para reducir contención e I/O; colas por clase de tráfico.
- Productización de costos: features caros (exports/audit/bulk) como add-ons, cuotas o límites por plan.
- Plataforma de showback: pipeline estable de métricas→costos→dashboards→alertas.

***

## Anti-patterns

[Facts] Export de snapshot cobrado por tamaño completo incluso si parcial: si lo usas como “export por tabla” sin saberlo, puedes pagar de más.[^6]
[Facts] Dejar retención indefinida en logs hace que el storage crezca con el tiempo.[^8]
[Facts] Payload grande en colas aumenta requests facturadas por chunks, elevando costo con el tamaño del mensaje.[^7]
[Inferences]

- “Shared cost” enorme sin driver: termina en discusiones políticas, no decisiones.
- Métricas por tenant sin control de cardinalidad: rompes tu propia plataforma de observabilidad.
- Índices “porque sí”: mejoras una query y encareces todas las escrituras (y el mantenimiento).
- Showback con unidades inventadas: nadie confía, nadie actúa.

***

## Diagnostic questions

[Inferences]

- ¿Qué % del costo infra variable puedes asignar a tenant_id y a feature_name hoy?
- ¿Cuáles 5 features generan más I/O en DB y por qué (bulk, reportes, sync, audit)?
- ¿Cuántos exports/snapshots corren al mes y quién los “posee” (equipo/feature)? ¿Se cobran por snapshot completo?
- ¿Tu cola está cara por requests, por payload o por retries/DLQ?
- ¿Tu observabilidad está cara por ingesta, por storage acumulado (retención) o por consultas frecuentes?
- ¿Tienes “ballenas” (tenants top 1–5) subsidiadas por el resto? ¿Qué harías si pagaran su costo real?

***

## Sources (o referencia a SOURCES.md)

[Facts] Fuentes clave usadas: FinOps Foundation (showback/chargeback), AWS (RDS y snapshot export docs/blogs), pricing de SQS, y guías de instrumentación multi-tenant con OpenTelemetry.[^2][^7][^6][^9][^1]

### Añadidos propuestos a `SOURCES.md` (sin duplicados)

```md
- FinOps Foundation — Chargeback & Finance Integration (showback vs chargeback). https://www.finops.org/framework/previous-capabilities/chargeback/ (2024-06-30)
- AWS Database Blog — AWS tools to optimize your Amazon RDS costs. https://aws.amazon.com/blogs/database/aws-tools-to-optimize-your-amazon-rds-costs/ (2024-04-10)
- AWS Docs — Exporting DB snapshot data to Amazon S3 for Amazon RDS. https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ExportSnapshot.html (2019-08-11)
- AWS Database Blog — Building data lakes and implementing data retention policies with Amazon RDS snapshot exports to S3 (pricing note: charged per full snapshot size). https://aws.amazon.com/blogs/database/building-data-lakes-and-implementing-data-retention-policies-with-amazon-rds-snapshot-exports-to-amazon-s3/ (2020-05-28)
- AWS — Amazon SQS Pricing (requests/payload model; regional transfer note). https://aws.amazon.com/sqs/pricing/ (consultado 2026-02)
- AWS CN — Amazon SQS Pricing (payload chunks billed per request). https://www.amazonaws.cn/en/sqs/pricing/ (2025-11-25)
- OneUptime — Tenant-aware telemetry routing (per-tenant span count metric). https://oneuptime.com/blog/post/2026-02-06-tenant-aware-telemetry-routing-multi-tenant/view (2026-02-05)
- OneUptime — Instrument SaaS multi-tenant with OpenTelemetry (cardinality control; sampling by plan). https://oneuptime.com/blog/post/2026-02-06-instrument-saas-multi-tenant-application-opentelemetry/view (2026-02-05)
- Percona — Tuning Autovacuum in PostgreSQL and Autovacuum Internals (vacuum cleans indexes; autovacuum cost/IO considerations). https://www.percona.com/blog/tuning-autovacuum-in-postgresql-and-autovacuum-internals/ (2024-01-30)
- PostgresAI — Why keep your index set lean (extra indexes increase autovacuum work/WAL). https://postgres.ai/blog/20251110-postgres-marathon-2-013-why-keep-your-index-set-lean (2025-11-09)
- SigNoz — CloudWatch pricing guide (ingest/store/query framing; retention risk). https://signoz.io/guides/cloudwatch-pricing/ (2026-02-14)
```


***

## Key takeaways for PM practice

- Convierte infraestructura en decisiones de producto: costo por tenant y por feature con drivers auditables (no “tokens”).
- Productiza los features caros (exports/audit/bulk) con límites, tiers o add-ons antes de “optimizar código” a ciegas.
- La higiene (índices, retención, sampling, batching) compra tiempo; el margen real viene de cambios estructurales (aislar ballenas, particionar, packaging).
- Si no puedes explicarlo con 3 métricas, no puedes venderlo, ni operarlo, ni defender el margen.
<span style="display:none">[^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31][^32][^33][^34][^35][^36][^37][^38][^39][^40][^41][^42][^43][^44][^45]</span>

<div align="center">⁂</div>

[^1]: https://www.finops.org/framework/previous-capabilities/chargeback/

[^2]: https://aws.amazon.com/blogs/database/aws-tools-to-optimize-your-amazon-rds-costs/

[^3]: https://caw.tech/postgresql-vacuum-managing-dead-rows-database-bloat/

[^4]: https://postgres.ai/blog/20251110-postgres-marathon-2-013-why-keep-your-index-set-lean

[^5]: https://www.percona.com/blog/tuning-autovacuum-in-postgresql-and-autovacuum-internals/

[^6]: https://aws.amazon.com/blogs/database/building-data-lakes-and-implementing-data-retention-policies-with-amazon-rds-snapshot-export-to-amazon-s3/

[^7]: https://www.amazonaws.cn/en/sqs/pricing/

[^8]: https://signoz.io/guides/cloudwatch-pricing/

[^9]: https://oneuptime.com/blog/post/2026-02-06-tenant-aware-telemetry-routing-multi-tenant/view

[^10]: https://oneuptime.com/blog/post/2026-02-06-instrument-saas-multi-tenant-application-opentelemetry/view

[^11]: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ExportSnapshot.html

[^12]: https://aws.amazon.com/sqs/pricing/

[^13]: pasted-text.txt

[^14]: https://www.nops.io/blog/chargeback-vs-showback/

[^15]: https://www.finout.io/blog/showback-vs-chargeback

[^16]: https://www.cloudzero.com/blog/chargeback-vs-showback/

[^17]: https://www.infracost.io/glossary/showback/

[^18]: https://www.stream.security/post/aws-well-architected-framework-cost-optimization

[^19]: https://www.nops.io/blog/ai-cost-visibility-the-ultimate-guide/

[^20]: https://www.prosperops.com/blog/showback-vs-chargeback/

[^21]: https://www.nops.io/blog/amazon-rds-cost-optimization-the-essential-guide/

[^22]: https://www.cloudbolt.io/blog/showback-vs-chargeback/

[^23]: https://www.finops.org/framework/capabilities/invoicing-chargeback/

[^24]: https://spacelift.io/blog/aws-cost-optimization

[^25]: https://docs.aws.amazon.com/solutions/latest/data-transfer-hub/cost.html

[^26]: https://www.pump.co/blog/aws-sqs-pricing

[^27]: https://awsfundamentals.com/blog/sqs-pricing

[^28]: https://www.reddit.com/r/aws/comments/1bfb3qx/sqs_pricing_questions_and_general_tips/

[^29]: https://boringsql.com/posts/vacuum-is-lie/

[^30]: https://cloudchipr.com/blog/cloudwatch-pricing

[^31]: https://hutchpost.eaglewebservices.com/instant-shots/amazon-sqs-pricing-a-comprehensive-guide-1764801385

[^32]: https://virtual-dba.com/blog/why-vacuum-full-can-be-dangerous-what-to-use-instead/

[^33]: https://hykell.com/knowledge-base/aws-cloudwatch-logs-pricing/

[^34]: https://www.nops.io/glossary/what-is-aws-sqs-amazon-simple-queue-service/

[^35]: https://aws.amazon.com/blogs/database/reduce-data-archiving-costs-for-compliance-by-automating-amazon-rds-snapshot-exports-to-amazon-s3/

[^36]: https://www.tothenew.com/blog/snapshot-migration-to-s3-and-extract-data-from-snapshot-using-athena/

[^37]: https://aws.amazon.com/blogs/database/programmatic-approach-to-optimize-the-cost-of-amazon-rds-snapshots/

[^38]: https://freecloudlabs.com/exporting-rds-snapshot-to-s3-ad3b0d63f5bf

[^39]: https://www.cloudflare.com/learning/cloud/what-is-aws-data-transfer-pricing/

[^40]: https://www.reddit.com/r/aws/comments/1b3km7k/rds_manual_snapshot_then_export_to_s3_for_archive/

[^41]: https://www.cloudzero.com/blog/reduce-data-transfer-costs/

[^42]: https://pganalyze.com/blog/introducing-vacuum-advisor-postgres

[^43]: https://dev.to/aws-builders/export-database-snapshots-manually-to-s3-export-s3-content-in-glue-data-catalog-using-crawler-for-tables-fetched-in-athena-5ef6

[^44]: https://www.digitalocean.com/resources/articles/aws-egress-costs

[^45]: https://www.pump.co/blog/aws-data-transfer-pricing

