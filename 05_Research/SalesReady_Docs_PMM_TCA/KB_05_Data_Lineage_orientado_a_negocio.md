<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_05 — Data Lineage orientado a negocio para CRMs: SQL, RPC y ETL


***

## Executive Summary

Este documento es la guía operativa para documentar de dónde viene cada dato en un CRM enterprise, cómo se refresca y qué garantías son prometibles al negocio sin mentir. En entornos B2B complejos (turismo mayorista, fintech LATAM, SaaS multicanal), los datos del CRM provienen de al menos tres fuentes técnicas distintas: consultas **SQL directas** a la base operacional, llamadas **RPC/API** a sistemas externos, y pipelines **ETL/ELT** que transforman y consolidan. Cada origen tiene su propio contrato de latencia, consistencia y frescura. Sin documentar ese contrato, el negocio toma decisiones sobre datos que pueden tener 24h de atraso sin saberlo.

El problema central no es técnico: es de confianza. Cuando un agente de viajes ve un KPI de "cierres del mes" en el CRM, asume que es tiempo real. Si ese KPI viene de un ETL nocturno, la realidad puede diferir en horas. Documentar el lineage convierte ese riesgo invisible en un acuerdo explícito.[^1][^2]

La solución estructurada incluye: (1) un mapa de origen por cada campo crítico, (2) una **KPI Lineage Card** por cada métrica de negocio, (3) niveles de frescura con SLA contractual o "best effort" claramente separados, y (4) reglas de caché con TTL o invalidación por evento según criticidad del dato.[^3][^4]

Este KB aplica tanto a PMs de producto como a operadores técnicos-comerciales que necesitan comunicar garantías de datos a stakeholders internos y agencias cliente.

***

## Definitions and Why It Matters

**`FACT`** — **Data Lineage**: proceso de trazar el origen, movimiento y transformación de un dato desde su fuente hasta su uso final. En un CRM, significa saber si el campo `revenue_ytd` viene de la base transaccional (SQL), de un API externo (RPC), o fue calculado en un job nocturno (ETL).[^1]

**`FACT`** — **KPI Lineage Card**: documento estructurado que describe el contrato técnico-comercial de un indicador: origen, transformación, frecuencia de refresco, latencia máxima y nivel de garantía prometible. Es el puente entre el equipo de datos y el usuario de negocio.[^5]

**`FACT`** — **SLA vs Best Effort**: un SLA (Service Level Agreement) formaliza expectativas con penalidad o escalamiento definido. "Best effort" es un compromiso informal sin consecuencias contractuales. La diferencia importa cuando una agencia te pregunta "¿puedo fiarme de este número para cotizar?".[^6]

**`INFERENCE`** — En entornos mayoristas B2B con mercados de alta fricción (Venezuela, Colombia), la falta de lineage documentado es una fuente directa de erosión de confianza en el CRM, lo que lleva a que los vendedores validen manualmente datos que ya existen en el sistema.

***

## Principles and Best Practices

### 1. Los tres orígenes técnicos y sus contratos nativos

Cada tipo de origen tiene características distintas que determinan qué puedes prometer:[^7][^1]


| Origen | Latencia típica | Consistencia | Caso de uso en CRM |
| :-- | :-- | :-- | :-- |
| **SQL directo** | < 1 seg (read) | Fuerte (ACID) | Estado actual de oportunidad, pipeline activo |
| **RPC / API externa** | 200ms–5s | Eventual | Precio de proveedor, disponibilidad, estado de reserva |
| **ETL / ELT** | 15 min–24h | Eventual → Fuerte post-job | KPIs históricos, reportes consolidados, comisiones |

**`FACT`** — Los pipelines ETL son la principal fuente de latencia oculta en CRMs enterprise. Un KPI calculado en un job nocturno puede mostrarse con hasta 24h de atraso sin ninguna alerta visible al usuario.[^2]

**`FACT`** — Para columnas derivadas en ETL, la práctica recomendada es etiquetar el origen directamente en el código SQL de transformación para que las herramientas de lineage capturen la relación automáticamente:[^1]

```sql
SELECT
  customer_id,                            -- source: crm.customers.id
  order_total * 1.12 AS total_con_iva     -- source: sales.orders.total, transform: +12% IVA
FROM sales.orders;
```


### 2. Niveles de frescura y tiers de SLA

**`FACT`** — Definir tiers de frescura específicos por caso de uso es la forma más efectiva de alinear expectativas técnicas con el negocio sin sobre-comprometer:[^2]

- **Tier 1 — Real-time** (< 5 min): datos operacionales críticos. Solo prometible con SQL directo o RPC con caché corto. Ejemplo: disponibilidad de habitación antes de confirmar una reserva.
- **Tier 2 — Near-real-time** (cada hora): dashboards de ventas del día. Requiere pipeline de micro-batch o polling frecuente.
- **Tier 3 — Daily refresh** (1x/día, entrega antes de las 8am): KPIs de gestión, comisiones, pipeline de cierres. Prometible con ETL nocturno. Es el tier adecuado para la mayoría de datos de CRM B2B.
- **Tier 4 — Weekly / on-demand**: reportes estratégicos, análisis histórico, cohorts.

**`FACT`** — Construir pipelines real-time para todo puede costar 8–10× más que un schedule diario, con impacto casi nulo en decisiones de negocio que son naturalmente diarias.[^2]

### 3. Estrategias de caché: TTL vs Event-Driven

**`FACT`** — La invalidación de caché basada en TTL (Time-To-Live) es el punto de partida recomendado porque actúa como red de seguridad aunque la lógica de invalidación falle. Siempre setear TTL incluso cuando existan otras estrategias.[^4]

**`FACT`** — Para datos críticos (precios, disponibilidad, estados de reserva), la invalidación event-driven garantiza consistencia inmediata: cuando el dato fuente cambia, el caché se invalida en el mismo evento.[^8]

**`INFERENCE`** — En CRMs con datos de proveedores externos (pricing de hoteles, vuelos), un modelo híbrido es el más pragmático: TTL de 15 min como fallback + invalidación por webhook cuando el proveedor notifica cambio de precio.

Estrategias de caché según tipo de dato en CRM:


| Dato | Estrategia de caché | TTL recomendado |
| :-- | :-- | :-- |
| Precio de proveedor | Event-driven + TTL fallback | 15 min |
| Perfil de agencia | TTL largo + invalidación en update | 4h |
| KPI de ventas del día | TTL corto (refresh por job) | 60 min |
| Historial de reservas | Solo-read, TTL largo | 24h |
| Disponibilidad de producto | Event-driven estricto | 5 min |

### 4. Reglas para no prometer imposibles

**`FACT`** — Un SLA formaliza expectativas con métricas medibles y definición de incumplimiento. Antes de comprometer un SLA, verificar: ¿el origen del dato lo soporta? ¿hay monitoreo que detecte breaches? ¿hay plan de escalamiento?[^5][^6]

**Reglas operativas:**

1. **Nunca prometer real-time si el origen es ETL** — documentar explícitamente el horario del job y añadir timestamp de último refresco visible en el dashboard.
2. **Distinguir "dato disponible" de "dato correcto"** — un campo puede refrescarse cada hora pero con una hora de lag por diseño; no son lo mismo.
3. **Best effort solo cuando no hay consecuencia de negocio** — si un agente toma una decisión comercial con ese dato, necesita un SLA con tier definido, no "best effort".
4. **Documentar el peor caso, no el promedio** — si el ETL normalmente corre en 10 min pero puede tardar 2h en pico, el SLA debe decir 2h.
5. **Agregar alertas de breach antes de que el usuario lo reporte** — el monitoreo de frescura es parte del contrato, no un extra.[^9]

***

## KPI Lineage Card — Plantilla

```markdown
## KPI Lineage Card

**KPI Name:**         [ej. Revenue MTD por agencia]
**Owner:**            [Nombre / equipo responsable]
**Versión:**          [1.0 | Fecha: YYYY-MM-DD]

### Origen técnico
- **Sistema fuente:**    [ej. PostgreSQL CRM prod / API Amadeus / DWH Redshift]
- **Tipo de origen:**    [SQL directo | RPC/API | ETL/ELT]
- **Query / job:**       [enlace o nombre del job en el orquestador]
- **Campos fuente:**     [tabla.columna → campo destino CRM]
- **Transformaciones:**  [ej. SUM(amount) WHERE status='closed', agrupado por agency_id]

### Frescura y latencia
- **Frecuencia de refresco:**  [ej. Diario 02:00 UTC | Cada 60 min | On-demand]
- **Latencia máxima:**         [ej. Datos con máximo 24h de atraso]
- **Tier de frescura:**        [Tier 1 / 2 / 3 / 4]
- **Timestamp visible en UI:** [Sí / No — campo: last_refreshed_at]

### Caché
- **Cacheado:**                [Sí / No]
- **Estrategia:**              [TTL | Event-driven | Híbrido]
- **TTL:**                     [ej. 60 min]
- **Trigger de invalidación:** [ej. Webhook POST /crm/cache/invalidate]

### Garantías
- **Nivel de garantía:**   [SLA contractual | SLA interno | Best effort]
- **SLA comprometido:**    [ej. Dato disponible antes de las 08:00 cada día hábil]
- **Breaches documentados en últimos 30d:** [N ocurrencias | Causa]
- **Escalamiento si breach:** [Canal / responsable / tiempo de respuesta]

### Qué incluye / qué NO incluye
✅ Incluye: ventas confirmadas (status = 'closed'), todas las monedas convertidas a USD
❌ No incluye: cancelaciones del mismo día, ventas pendientes de aprobación
⚠️ Sensible: reconciliación contable no es parte de este KPI — usar reporte financiero

### Dependencias
- **Upstream:**  [job anterior / sistema que debe correr antes]
- **Downstream:** [dashboards, reports, modelos ML que consumen este KPI]
```


***

## Metrics / Success Signals

**`FACT`** — Los KPIs de calidad de lineage y frescura deben definirse como SLOs medibles antes de comprometerse como SLAs:[^6]

- **Data Freshness Rate**: % de KPIs entregados dentro del window prometido. Target: ≥ 99% para Tier 1-2; ≥ 95% para Tier 3.
- **Lineage Coverage**: % de campos críticos del CRM con KPI Lineage Card documentada. Target inicial: 100% de campos usados en decisiones comerciales.
- **Cache Hit Ratio**: % de requests servidos desde caché. Target: ≥ 85% para reducir carga sobre sistemas fuente.
- **Breach Rate**: nº de SLA breaches por mes por KPI. Alerta si > 2 en 30 días para Tier 1-2.
- **MTTD (Mean Time to Detect) stale data**: tiempo promedio desde que un dato se vuelve stale hasta que se detecta. Target: < 15 min para Tier 1.
- **Self-report rate**: % de stale data reportado por usuarios antes de que lo detecte el sistema → debe ser 0%.

***

## Operational Checklist

**Para cada nuevo KPI que entre al CRM:**

- [ ] Identificar origen técnico (SQL / RPC / ETL) y documentar en Lineage Card
- [ ] Definir tier de frescura y negociar con el negocio (no asumir que quieren real-time)
- [ ] Configurar timestamp de último refresco visible en la UI del CRM
- [ ] Definir estrategia de caché + TTL antes de ir a producción
- [ ] Establecer alertas de breach de frescura (no esperar a que el usuario reporte)
- [ ] Separar explícitamente qué incluye / qué no incluye el KPI en la card
- [ ] Documentar dependencias upstream (jobs que deben correr antes)
- [ ] Asignar owner responsable del KPI (no "el equipo")
- [ ] Revisar lineage cards en cada sprint de cambio de schema o job ETL[^5]
- [ ] Validar que los SLAs comprometidos sean soportables por el tier técnico del origen

***

## Anti-patterns

**`FACT`** — El mayor fallo en lineage es construirlo una vez y dejarlo desactualizar. El lineage debe tratarse como un producto con owner, SLA propio y ciclos de revisión.[^5]

1. **Prometer real-time sobre ETL nocturno** — el campo se ve "en vivo" pero tiene 18h de atraso. Crea desconfianza cuando el usuario lo descubre.
2. **No mostrar el timestamp de refresco en la UI** — el usuario no sabe si el dato tiene 5 min o 5 horas. Toda vista del CRM con KPIs debe mostrar "Actualizado: hace X".
3. **Caché sin TTL** — si la lógica de invalidación falla, el dato queda zombie indefinidamente.[^4]
4. **Documentar solo el flujo feliz** — el SLA debe definirse sobre el peor caso (p99), no el promedio.
5. **Asumir que todos los datos del CRM son del mismo tier** — mezclar datos operacionales (SQL) con reportes ETL sin distinguirlos en la UI lleva a decisiones erróneas.
6. **Lineage solo técnico, sin contexto de negocio** — "arrows entre sistemas sin contexto no son suficientes"; el lineage debe incluir definiciones de negocio, ownership y sensibilidad.[^1]
7. **Best effort sin límite** — decir "best effort" sin definir un piso mínimo es equivalente a no tener acuerdo. Siempre definir un worst-case aceptable.

***

## Diagnostic Questions

Usar estas preguntas para auditar cualquier KPI o campo del CRM antes de comprometer una garantía:

1. ¿Sabes exactamente de qué tabla/API/job viene este dato hoy?
2. ¿Cuándo fue la última vez que ese job corrió exitosamente? ¿Tienes alerta si falla?
3. ¿El usuario que ve este KPI sabe cuándo fue actualizado por última vez?
4. Si el origen externo (API proveedor) cae 2h, ¿qué ve el CRM? ¿Dato stale o error visible?
5. ¿El SLA que prometiste es el que soporta el tier técnico del origen, o fue negociado sin consultarlo?
6. ¿Tienes medición de cuántas veces se breachó ese SLA en los últimos 30 días?
7. ¿Quién es el owner si el dato llega tarde? ¿Hay proceso de escalamiento?
8. ¿Los campos "no incluidos" en el KPI están documentados y visibles para el usuario?
9. ¿El caché tiene TTL configurado como fallback aunque exista invalidación event-driven?
10. ¿Cuándo fue la última vez que revisaste que el lineage documentado sigue siendo correcto?[^5]

***

## Sources

| \# | Fuente | Fecha | Relevancia |
| :-- | :-- | :-- | :-- |
| S1 | SeeMoreData — Data Lineage Techniques 2025 | Jul 2025 | Capas de lineage, SQL tagging, ETL parsing |
| S2 | Dagster — Data Lineage 2025 | Feb 2026 | Definición y tipos de lineage |
| S3 | OvalEdge — Data Lineage Best Practices 2026 | Dic 2025 | Best practices y compliance |
| S4 | Datadef — Data Lineage Best Practices 2025 | Nov 2025 | Operacionalización, SLAs de lineage, Gold assets |
| S5 | OWOX BI — Freshness SLAs vs Real-Time | Oct 2025 | Tiers de frescura, CRM daily refresh, cost tradeoffs |
| S6 | Acceldata — Data Quality Measures | Nov 2025 | SLA vs SLO, timeliness metrics |
| S7 | OneUptime — Cache Invalidation Strategies | Ene 2026 | TTL, event-driven, version-based, hybrid cache |
| S8 | DragonflyDB — Ultimate Guide to Caching 2026 | Dic 2025 | TTL, pub/sub, multi-instance consistency |
| S9 | LeadSavvy — Data Management Best Practices | Ago 2025 | SLA metrics: pipeline latency, freshness, error rates |
| S10 | DataGalaxy — Data Lineage Step-by-Step | Ene 2026 | Parsing-based, tagging, pattern-based lineage |
| S11 | Collate — Data Lineage Examples 2025 | Dic 2024 | Column-level y cross-system lineage |


***

## Key Takeaways for PM Practice

- **`FACT`** El origen técnico del dato (SQL/RPC/ETL) determina el máximo nivel de frescura prometible; prometer más es crear deuda de confianza.[^2][^1]
- **`FACT`** Cada KPI de negocio en el CRM necesita una KPI Lineage Card con owner, tier, TTL, y separación explícita de qué incluye/no incluye.
- **`FACT`** El timestamp de último refresco debe ser visible en la UI — sin él, el usuario nunca sabe si confiar en el número.[^2]
- **`INFERENCE`** En mercados B2B con alta fricción operativa, la transparencia sobre latencia de datos es más valiosa que fingir real-time.
- **`FACT`** SLA contractual solo cuando el sistema fuente soporta el tier prometido y existe monitoreo activo de breaches.[^6]
- **`FACT`** Caché siempre con TTL como red de seguridad, más invalidación event-driven para datos críticos de negocio.[^4]
- **`FACT`** El lineage se depreca si no tiene ciclos de revisión en cada cambio de schema o job; tratar como producto, no como documentación estática.[^5]
- **`INFERENCE`** Para mayoristas B2B, el tier más práctico para la mayoría de KPIs de gestión es Tier 3 (daily, entrega antes de las 8am) — suficiente para decisiones operativas y sostenible en costo de infraestructura.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30]</span>

<div align="center">⁂</div>

[^1]: https://seemoredata.io/blog/data-lineage-in-2025-examples-techniques-best-practices/

[^2]: https://www.owox.com/blog/articles/real-time-data-freshness-slas

[^3]: https://dagster.io/learn/data-lineage

[^4]: https://oneuptime.com/blog/post/2026-01-30-cache-invalidation-strategies/view

[^5]: https://datadef.io/guides/en/data-lineage-best-practices

[^6]: https://www.acceldata.io/blog/data-quality-measures-practical-frameworks-for-accuracy-and-trust

[^7]: https://www.datagalaxy.com/en/blog/data-lineage-a-step-by-step-guide/

[^8]: https://www.dragonflydb.io/guides/ultimate-guide-to-caching

[^9]: https://leadsavvy.pro/post/data-management-best-practices/

[^10]: pasted-text.txt

[^11]: https://www.getcollate.io/learning-center/data-lineage-examples

[^12]: https://www.ovaledge.com/blog/data-lineage-best-practices

[^13]: https://datacrossroads.nl/2025/10/01/part-1-technological-challenges-data-lineage/

[^14]: https://cloudvara.com/data-governance-best-practices/

[^15]: https://oneuptime.com/blog/post/2026-02-16-how-to-trace-end-to-end-data-lineage-in-microsoft-purview/view

[^16]: https://cloudconsultings.com/salesforce-best-practices/

[^17]: https://tdwi.org/blogs/data-101/2025/09/understanding-data-lineage.aspx

[^18]: https://marketreachresults.com/8-essential-b2b-demand-generation-best-practices/

[^19]: https://www.ataccama.com/blog/top-data-lineage-tools-in-2025

[^20]: https://www.decube.io/post/lessons-learned-data-engineering

[^21]: https://www.resolution.de/post/service-level-agreement-best-practices/

[^22]: https://www.linkedin.com/posts/alis06922_azure-dataengineering-sla-activity-7425939834839502849-mO8B

[^23]: https://www.tencentcloud.com/techpedia/107989

[^24]: https://salesforcenegotiations.com/salesforce-support-tiers-standard-vs-premier-vs-signature/

[^25]: https://www.myshyft.com/blog/service-level-agreement-tracking/

[^26]: https://support.google.com/analytics/answer/12233314?hl=en

[^27]: https://dev.to/nk_sk_6f24fdd730188b284bf/cache-invalidation-the-hardest-problem-in-computer-science-3imd

[^28]: https://intuitionlabs.ai/articles/veeva-support-sla-severity-tiers

[^29]: https://materialize.com/blog/redis-cache-invalidation/

[^30]: https://syncari.com/blog/your-data-architecture-is-failing-at-the-hierarchy-layer/

