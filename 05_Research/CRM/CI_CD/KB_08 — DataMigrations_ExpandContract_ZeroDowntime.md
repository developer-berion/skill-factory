<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_08_DataMigrations_ExpandContract_ZeroDowntime (2026)

## Executive summary (10–15 líneas)

**Facts**

1. El patrón *expand → migrate/backfill → contract* permite cambios de esquema con compatibilidad hacia atrás y rollback de app sin romper producción, porque mantiene el esquema “viejo + nuevo” coexistiendo por etapas.[^1]
2. En “expand”, lo típico es agregar columnas/tablas nuevas de forma aditiva (p. ej., nullable) para no romper escrituras existentes.[^1]
3. En “expand app”, se recomienda que la aplicación escriba a viejo+nuevo (dual-write) para comprobar que el nuevo camino funciona sin impacto al usuario.[^1]
4. El “migrate/backfill” se hace con scripts o jobs en background, en lotes, para no degradar la base en producción.[^1]
5. Antes de mover lecturas al nuevo esquema, es el último punto donde puedes validar que el backfill está completo/correcto con bajo riesgo.[^1]
6. En “contract”, primero se deja de escribir al esquema viejo y luego se elimina lo viejo cuando ya no hay dependencias.[^1]
7. La complejidad real del zero-downtime se mueve al layer de app (dual-write, feature flags, coordinación de despliegues).[^2]
8. El dual-write en sistemas distribuidos introduce riesgo de inconsistencias; un enfoque común para mitigarlo es Transactional Outbox (escritura atómica en tabla de negocio + outbox en la misma transacción).[^3]
9. Un ejemplo práctico de outbox usa log-tailing/CDC con Debezium para propagar cambios de forma confiable.[^4]

**Inferences**
10. En un CRM enterprise (multi-equipos, integraciones, “reporting”), el mayor riesgo no es “downtime” sino corrupción silenciosa (datos parciales o divergentes), por eso validación + observabilidad son gates obligatorios.
11. Para B2B (agencias) conviene preferir “opción segura” (expand/contract + gates + cooling period) y usar “opción agresiva” solo con límites claros (scope pequeño, rollback fácil).
12. Rollback efectivo casi siempre es “rollback de rutas” (feature flags / read-path) más que “deshacer datos”; si ya escribiste datos nuevos, normalmente haces roll-forward con corrección.

***

## Definitions and why it matters

**Facts**

- **Expand/Contract (Expand–Migrate–Contract)**: secuencia por etapas para hacer cambios de esquema sin downtime, manteniendo compatibilidad en cada paso.[^1]
- **Backward compatibility (compatibilidad hacia atrás)**: el código en producción sigue funcionando aunque el esquema cambie, habilitando rollback de app sin perder servicio.[^1]
- **Online migration**: migración aplicada con el sistema vivo; evita bloqueos/ventanas de mantenimiento, pero requiere coordinación y controles extra.[^2]
- **Backfill**: proceso que rellena datos históricos hacia el nuevo esquema, idealmente en background y por lotes para no afectar performance.[^1]
- **Dual-write**: la app escribe simultáneamente en “viejo y nuevo” para asegurar continuidad; es útil pero crea riesgo de inconsistencias si no se controla.[^2][^1]
- **Rollback**: capacidad de volver a un estado seguro; en zero-downtime suele significar “volver a leer/escribir al camino anterior” mientras el esquema sigue compatible.[^2][^1]
- **Validation**: verificación de integridad/completitud/corrección (comparaciones, conteos, checks) antes de cutover/contract para evitar corrupción silenciosa.[^1]

**Inferences**

- En CRM, “esquema” incluye no solo DB: también API contracts, integraciones (ETL/BI), automatizaciones y reglas de negocio; si migras sin compatibilidad, rompes ventas/ops (tickets, reportes, comisiones).
- El valor comercial es continuidad + confianza: menos incidentes → más adopción interna → mejor velocidad de operación y menos fricción con clientes B2B.

***

## Principles and best practices (con citas por sección + fecha)

### 1) Separa despliegues de código y esquema (2023-05-08)

**Facts**

- Acoplar cambios de app + esquema “en el mismo instante” aumenta el riesgo y no es atómico; el patrón propone etapas para reducir riesgo y permitir rollback.[^1]

**Inferences**

- En CRM con varios consumidores (frontend, integraciones, jobs), esta separación es aún más crítica: alguien siempre queda en “versión vieja” por un rato.


### 2) “Expand” siempre aditivo y tolerante (nullable/defaults) (2023-05-08)

**Facts**

- En expand, agregar columnas/tablas suele ser seguro si se hacen nullable y/o con defaults para no romper inserciones.[^1]

**Inferences**

- Si tu CRM tiene escrituras desde múltiples canales (API + importadores + integraciones), “nullable primero” evita caídas por inputs incompletos durante el rollout.


### 3) Dual-write con intención y con mitigación del “dual-write problem” (2023-05-08; 2025-05-13)

**Facts**

- El patrón recomienda dual-write como parte de “expand app”: escribir a viejo+nuevo mientras validas el nuevo camino.[^1]
- El dual-write en distribuidos es un problema conocido; Transactional Outbox mitiga al escribir (tabla de negocio + outbox) en una misma transacción y publicar después.[^3]

**Inferences**

- Opción segura: dual-write *solo* dentro de la misma base (o misma transacción) y propagar asíncrono; opción agresiva: dual-write cross-systems directo (más riesgo de divergencia).


### 4) Backfills “throttled”, pausables y observables (2023-05-08; 2025-11-05)

**Facts**

- Para grandes volúmenes, se recomienda distribuir la migración en background jobs para no afectar performance de producción.[^1]
- Un playbook común es limitar batch sizes, correr por rangos y pausar cuando métricas/alertas lo indiquen.[^5]

**Inferences**

- En CRM, backfills deben respetar horas pico comerciales (aperturas, cierres, campañas) y regiones; define “ventanas suaves” y un botón de pausa real.


### 5) Cutover por rutas (read-path / write-path) con flags (2025-06-29)

**Facts**

- En estrategias de multi-versión (ej. pgroll), el enfoque es permitir coexistencia de versiones y habilitar despliegues graduales (canary/blue-green) sin downtime.[^2]

**Inferences**

- En CRM enterprise, el cutover ideal es por “capability” (módulo de cuentas, pipeline, tickets) y no “todo el CRM a la vez”.


### 6) Contract solo con pruebas + cooling period (2023-05-08)

**Facts**

- “Contract” llega cuando confirmas que todo funciona y puedes dejar de escribir al esquema viejo, y recién después eliminas lo viejo.[^1]

**Inferences**

- Si tu CRM alimenta reportes financieros, define un cooling period alineado al ciclo de cierre (ej. 7–30 días) antes de borrar columnas/tablas legacy.


### 7) Rollback realista: rollback de app/rutas, y “roll-forward” para datos (2025-06-29)

**Facts**

- En un enfoque como pgroll, puedes hacer rollback de una migración activa antes de completarla (rollback rápido) como red de seguridad.[^2]

**Inferences**

- En práctica, “rollback de datos” completo suele ser caro y lento; diseña para rollback de lectura/escritura + correcciones (roll-forward) con scripts idempotentes.

***

## Examples (aplicado a CRM enterprise)

### Ejemplo A: Renombrar campo `lead_source` → `acquisition_channel` sin downtime

**Facts**

1. Expand: agrega `acquisition_channel` nullable.[^1]
2. Expand app: actualiza el servicio de CRM para escribir en ambos campos (dual-write) y leer aún del viejo (feature flag “read_new=false”).[^1]
3. Backfill: job por lotes copia histórico `lead_source` → `acquisition_channel` (con throttling).[^5][^1]
4. Validate: compara conteos y distribución de valores (top-N, null-rate) antes de mover lecturas.[^1]
5. Cutover: cambia read-path a `acquisition_channel` (flag “read_new=true”), mantén dual-write por un tiempo corto.[^5]
6. Contract: deja de escribir al viejo y luego elimina `lead_source`.[^1]

**Inferences**

- Red flag CRM: si BI/ETL consume `SELECT *`, el contract puede romper reportes; exige “consumidores declarados” antes de borrar.
- Opción agresiva: cortar lecturas rápido tras validar; opción segura: mantener dual-write + shadow reads por una semana completa de tráfico real.


### Ejemplo B: Hacer `contact.email` NOT NULL con datos históricos sucios

**Facts**

- Para cambios “breaking” como `NOT NULL`, un enfoque zero-downtime requiere transición + backfill antes de aplicar la restricción definitivamente.[^2]
- Una herramienta como pgroll automatiza backfill y sincronización temporal (triggers) para aplicar el cambio sin bloquear y con rollback rápido antes de completar.[^2]

**Inferences**

- En CRM, “NOT NULL” en email suele ser mala idea si hay leads incompletos; alternativa segura: `email` nullable + constraint parcial (según caso) y validación en la capa de negocio.


### Ejemplo C: Migrar escrituras a un “nuevo store” (CRM → data service) con Outbox

**Facts**

- El dual-write distribuido puede producir inconsistencias; Transactional Outbox reduce riesgo al registrar eventos en DB en la misma transacción.[^3]
- Un patrón práctico es usar CDC/log-tailing con Debezium para propagar cambios desde el outbox/transaction log.[^4]

**Inferences**

- Para CRM enterprise, esto habilita desacoplar integraciones (marketing automation, BI, scoring) sin tocar el core de ventas cada vez.

***

## Metrics / success signals

**Facts**

- Señales de éxito del patrón: capacidad de rollback de app sin pérdida de servicio mientras el esquema está en estado compatible por etapas.[^1]
- En migraciones con backfill, la guía recomienda medir impacto y distribuir el trabajo para no degradar producción.[^1]

**Inferences (métricas recomendadas para CRM)**

- **Data correctness**: discrepancia viejo vs nuevo (% de registros distintos), null-rate por campo, checksums por partición (por tenant/region).
- **Backfill health**: throughput (rows/min), lag (pendientes), tasa de retries/errores, tiempo estimado a completar (ETA).
- **Production safety**: p95/p99 de endpoints de escritura/lectura, locks/slow queries, CPU/IO DB, cola de jobs.
- **Cutover confidence**: % de tráfico en read_new, ratio de fallos del feature flag, incidencias por integración (ETL/BI).

***

## Operational checklist

**Facts**

- El flujo expand → dual-write → backfill → mover lecturas → contract está explícitamente descrito como secuencia segura para cambios incompatibles.[^1]
- En enfoques multi-versión como pgroll, existe lifecycle “start (expand) → deploy → complete (contract) → rollback (si aplica antes de complete)”.[^2]

**Checklist (práctico, CRM)**

- Pre-flight: inventario de consumidores (apps, jobs, BI), define flags (read_path, write_path), define plan de validación (queries/checks) y plan de pausa del backfill.
- Expand: migración aditiva (nullable/default), despliegue sin romper, dashboards listos (latencia, errores, DB health).
- Expand app: habilita dual-write con idempotencia; registra métricas de divergencia (viejo vs nuevo) y auditoría.
- Backfill: ejecución por lotes/rangos, throttling y pause/resume; reintentos controlados; logs con correlación por tenant.
- Validate gate: conteos, muestreo, reglas de negocio (estado de pipeline, ownership, timestamps), comparación por cohortes.
- Cutover: canary (por equipo/tenant/region), shadow reads si aplica, plan de comunicación a operación/BI.
- Contract: deshabilitar escrituras legacy, mantener cooling period, borrar/renombrar legacy solo con “consumidores en verde”.
- Rollback readiness: runbook con “switch back” (flags), snapshot/restore policy, y criterios objetivos de abortar (SLOs/errores).

***

## Anti-patterns

**Facts**

- La guía de pgroll advierte que el enfoque zero-downtime transfiere complejidad al equipo (dual-write, backfills, flags) y que bugs ahí pueden causar corrupción silenciosa.[^2]
- El dual-write problem existe y requiere estrategias para mitigar inconsistencias (ej. outbox) en distribuidos.[^3]

**Inferences (red flags típicos en CRM)**

- “Lo hacemos en una sola migración SQL” para un cambio breaking en tablas grandes.
- Backfill sin throttle, sin pausa, sin alertas, corriendo en horas pico comerciales.
- Validación solo con “conteo total” (sin segmentar por tenant/region/estado de negocio).
- Contract sin cooling period y sin confirmar integraciones (BI/ETL/exports).
- Dual-write cross-systems sin outbox/CDC y sin reconciliación programada.

***

## Diagnostic questions

**Facts**

- Antes de mover lecturas al nuevo esquema, el patrón sugiere validar que migración y nuevo esquema están correctos porque luego el impacto al usuario puede aumentar.[^1]

**Inferences (preguntas de control)**

- ¿Qué parte exacta necesita zero-downtime: escrituras, lecturas, integraciones o reporting?
- ¿Cuál es tu “rollback switch” concreto (flag, config, routing) y quién lo puede activar 24/7?
- ¿Cómo mides divergencia viejo vs nuevo y cuál es tu umbral para abortar?
- ¿Tu backfill es idempotente y reentrante (puede re-correr sin duplicar/corromper)?
- ¿Quiénes consumen el esquema legacy (incluye BI, exports manuales, scripts “olvidados”)?
- Si algo sale mal, ¿tu estrategia real es rollback o roll-forward con corrección? ¿Cuánto tarda cada una?

***

## Sources (o referencia a SOURCES.md)

- PlanetScale — “Backward compatible database changes” (2023-05-08).[^1]
- Neon Guides — “Zero downtime schema migrations with pgroll” (2025-06-29).[^2]
- Auth0 — “Handling the Dual-Write Problem in Distributed Systems” (2025-05-13).[^3]
- SeatGeek — “The Transactional Outbox Pattern…” (2025-02-06).[^4]
- DesignGurus — “plan zero‑downtime data migrations and backfills” (2025-11-05).[^5]
- Enol Casielles — “Migraciones… patrón expand-contract” (2025-08-29).[^2]


### Añadir a `SOURCES.md` (sin duplicados)

- PlanetScale. “Backward compatible database changes” (2023-05-08). https://planetscale.com/blog/backward-compatible-databases-changes
- Neon. “Zero downtime schema migrations with pgroll” (2025-06-29). https://neon.com/guides/pgroll
- Auth0. “Handling the Dual-Write Problem in Distributed Systems” (2025-05-13). https://auth0.com/blog/handling-the-dual-write-problem-in-distributed-systems/
- SeatGeek Engineering. “The Transactional Outbox Pattern…” (2025-02-06). https://chairnerd.seatgeek.com/transactional-outbox-pattern/
- DesignGurus. “How do you plan zero‑downtime data migrations and backfills?” (2025-11-05). https://www.designgurus.io/answers/detail/how-do-you-plan-zerodowntime-data-migrations-and-backfills
- Enol Casielles. “Migraciones en la base de datos. El patrón expand-contract” (2025-08-29). https://www.enolcasielles.com/blog/database-migrations-strategy

***

## Key takeaways for PM practice

- Diseña migraciones como producto: fases, flags, gates de validación, y un “rollback switch” operable.[^2][^1]
- Prioriza prevención de corrupción silenciosa (validación + métricas) sobre “hacerlo rápido”.[^2]
- Dual-write es herramienta, no objetivo: úsalo con mitigación (outbox/CDC) cuando cruces sistemas o haya integraciones críticas.[^4][^3]
- Contract es una decisión de riesgo: exige cooling period y confirmación de consumidores (BI/ETL/exports) antes de borrar legacy.[^1]
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: pasted-text.txt

[^2]: https://www.enolcasielles.com/blog/database-migrations-strategy

[^3]: https://auth0.com/blog/handling-the-dual-write-problem-in-distributed-systems/

[^4]: https://chairnerd.seatgeek.com/transactional-outbox-pattern/

[^5]: https://www.designgurus.io/answers/detail/how-do-you-plan-zerodowntime-data-migrations-and-backfills

[^6]: https://www.techment.com/blogs/data-migration-trends-best-practices-2026/

[^7]: https://clearout.io/blog/crm-migration-best-practices/

[^8]: https://docs.aws.amazon.com/es_es/dms/latest/userguide/CHAP_BestPractices.html

[^9]: https://cobalt.net/crm-data-migration-checklist/

[^10]: https://planetscale.com/blog/backward-compatible-databases-changes

[^11]: https://learn.microsoft.com/es-es/dynamics365/customer-service/administer/migrate-record-routing-config-using-solutions

[^12]: https://www.pingcap.com/article/database-design-patterns-for-ensuring-backward-compatibility/

[^13]: https://neon.com/guides/pgroll

[^14]: https://ftpdocs.broadcom.com/cadocs/0/CA Desktop Migration Manager 12 8-ESP/Bookshelf_Files/PDF/ITCM_DMM_GettingStarted_ESN.pdf

[^15]: https://blog.thepete.net/blog/2023/12/05/expand/contract-making-a-breaking-change-without-a-big-bang/

[^16]: https://www.tinybird.co/blog/clickhouse-schema-migrations

