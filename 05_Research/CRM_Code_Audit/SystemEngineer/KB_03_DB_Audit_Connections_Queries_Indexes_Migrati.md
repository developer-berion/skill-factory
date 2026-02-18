<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_03_DB_Audit_Connections_Queries_Indexes_Migrations.md

## Executive summary (10–15 líneas)

- **Fact:** Para diagnosticar performance real, usa planes de ejecución; en PostgreSQL `EXPLAIN` muestra el plan y `EXPLAIN ANALYZE` además ejecuta la query y reporta tiempos/filas reales por paso, útil cuando las estimaciones fallan.[^1][^2]
- **Fact:** Las fugas de conexión se pueden detectar a nivel pool; HikariCP permite activar `leakDetectionThreshold` para loguear “possible connection leak” cuando una conexión permanece demasiado tiempo fuera del pool.[^3]
- **Inference:** En un CRM enterprise, las fugas + picos de tráfico suelen convertirse en “caídas intermitentes” que el equipo comercial percibe como “el sistema está lento” y terminan afectando conversión y retención.
- **Fact:** El problema N+1 ocurre cuando haces 1 query inicial y luego N queries adicionales por cada fila para traer relaciones, típico de ORMs con lazy loading mal controlado.[^4]
- **Inference:** N+1 rara vez aparece como “una query lenta”; aparece como “muchas queries pequeñas” que saturan CPU/IO y el pool.
- **Fact:** Para crear índices en producción sin bloquear escrituras en PostgreSQL existe `CREATE INDEX CONCURRENTLY`, que evita locks que impiden inserts/updates/deletes (con caveats).[^5]
- **Inference:** En entornos B2B con SLAs y ventanas limitadas, `CONCURRENTLY` suele ser la opción “segura” para minimizar impacto operativo.
- **Fact:** Para cambios de esquema sin downtime, patrones tipo expand/contract (o expand-migrate-contract) separan: agregar estructuras, migrar/actualizar app, y luego remover lo viejo.[^6][^7]
- **Fact:** En logging, OWASP recomienda no registrar datos sensibles/PII (ej. salud, IDs gubernamentales), ni secretos como passwords, access tokens, strings de conexión o llaves.[^8]
- **Inference:** En auditoría DB de un CRM, la parte técnica (pool/queries/índices/migrations/PII) debe traducirse a riesgo operacional: caída, corrupción de datos, fuga de información, o degradación de respuesta.
- **Inference:** Esta guía propone checklist, señales de riesgo y “opción segura vs agresiva” para priorizar correcciones sin frenar despliegues.

***

## Definitions and why it matters

**Facts**

- Un plan de ejecución es la estrategia que el motor elige para ejecutar una query; en PostgreSQL puedes inspeccionarlo con `EXPLAIN`.[^2]
- N+1 es un patrón donde una lista inicial provoca queries adicionales por cada registro al cargar relaciones, generando $N+1$ ejecuciones en total.[^4]
- En PostgreSQL, `CREATE INDEX CONCURRENTLY` permite construir un índice sin tomar locks que prevengan escrituras concurrentes sobre la tabla.[^5]

**Inferences**

- En apps tipo CRM, la auditoría DB importa porque la DB suele ser el “cuello de botella” común a ventas, operaciones y reporting: cuando falla, todo se siente.
- La auditoría DB bien hecha reduce incidentes (agotamiento de conexiones, degradación, timeouts), y también reduce riesgo legal/contractual al evitar exposición de PII en logs/backups.

***

## Principles and best practices (con citas por sección + fecha)

### 1) Pool y conexiones (Fecha: 2026-02-17)

**Facts**

- HikariCP ofrece `leakDetectionThreshold`, que controla cuánto tiempo una conexión puede estar “fuera del pool” antes de loguear un posible leak; si es 0, está desactivado.[^3]
- OWASP indica que no deben registrarse strings de conexión a DB (además de otros secretos) en logs.[^8]

**Inferences**

- Señal práctica de “conexiones huérfanas”: el pool se queda sin conexiones disponibles en picos aunque la DB “parezca sana”; en CRM esto se manifiesta como timeouts erráticos (difícil de reproducir) y tickets de soporte.
- Opción segura: activar leak detection en entornos controlados o con umbrales altos para detectar el stack trace del préstamo (y corregir el código que no cierra).[^3]
- Opción agresiva: bajar umbrales para detectar rápido en producción; riesgo: ruido de logs y falsos positivos si hay transacciones legítimamente largas.[^3]

**Qué incluye**

- Revisión de configuración del pool (timeouts, max pool, leak detection), patrones de uso (transacciones largas), y prácticas de logging seguras.[^8][^3]

**Qué no incluye**

- Un “valor universal” de tamaño de pool; depende de concurrencia, latencia y límites de la DB.

**Sensible**

- Cualquier traza/log que exponga PII o secretos; si habilitas diagnóstico, sanitiza/filtra primero.[^8]

***

### 2) Queries, N+1 y carga ORM (Fecha: 2025-06-22)

**Facts**

- N+1 pasa cuando una query inicial trae N filas y luego se ejecuta una query extra por cada fila para traer datos relacionados, típico con ORMs.[^4]

**Inferences**

- En CRM enterprise (cuentas, contactos, reservas, facturas), N+1 aparece en pantallas “listas + detalle” (ej. lista de agencias con su último pedido, deuda, ejecutivo asignado).
- Mitigación segura: instrumentar y presupuestar “queries por request” y “tiempo total DB por request” para detectar N+1 aunque ninguna query individual sea lenta.
- Mitigación agresiva: reescribir a joins/CTEs/cargas eager selectivas; riesgo: sobre-traer datos y aumentar payload si no se controla.

**Qué incluye**

- Auditoría de endpoints críticos (listados, dashboards, exports) buscando multiplicación de queries por request.[^4]

**Qué no incluye**

- Optimización de código UI o caching a nivel CDN; aquí el foco es DB + capa de acceso.

**Sensible**

- Exports y reportes: suelen juntar mucha PII; un N+1 en export masivo puede tumbar el pool y además generar archivos con datos excesivos.

***

### 3) Planes de ejecución y “por qué está lenta” (Fecha: 2026-02-11)

**Facts**

- En PostgreSQL, `EXPLAIN` muestra el plan que el planner genera para una sentencia.[^2]
- `EXPLAIN ANALYZE` ejecuta la query y muestra tiempos/filas reales por paso, lo que es “indispensable” para analizar performance.[^1]

**Inferences**

- Buen hábito enterprise: antes de “poner un índice”, primero verificar si el plan hace seq scan por falta de selectividad, joins mal ordenados o estimaciones erradas; el índice equivocado solo agrega costo de escritura.
- Opción segura: usar `EXPLAIN` en entornos de staging con datos parecidos a producción; llevar el plan como evidencia al equipo (dev/DBA).[^2]
- Opción agresiva: `EXPLAIN ANALYZE` en producción para un caso real; riesgo: ejecuta la query y puede agravar carga si se corre sin control.[^1]

**Qué incluye**

- Lectura guiada del plan (scans, joins, filtros) y correlación con el patrón de acceso del CRM.[^1][^2]

**Qué no incluye**

- “Tuning” específico del motor (parámetros del planner, memory settings); eso requiere contexto de infraestructura.

**Sensible**

- Ejecutar queries pesadas “para medir”: si es producción, define ventanas y límites para evitar impacto.[^1]

***

### 4) Índices: creación segura y riesgo de lock (Fecha: 2026-02-11)

**Facts**

- `CREATE INDEX CONCURRENTLY` en PostgreSQL construye el índice sin tomar locks que impidan inserts/updates/deletes; un build estándar sí bloquea escrituras hasta terminar.[^5]
- PostgreSQL documenta progreso/fases asociadas a creación de índices concurrentes (incluyendo que escanea para validar en una fase).[^9]

**Inferences**

- Opción segura: para tablas “vivas” del CRM (reservas, pagos, movimientos), preferir `CONCURRENTLY` y monitorear progreso; asume que tardará más y tiene caveats operativos.[^9][^5]
- Opción agresiva: crear índice normal en ventana corta; útil si la tabla es pequeña o si puedes pausar escrituras, riesgo: bloqueo y caída parcial.[^5]
- Señal de riesgo: “muchos índices” sin uso en tablas con alta escritura; aunque no esté citado aquí, en práctica aumenta costo de writes y bloat (validar con métricas internas).

**Qué incluye**

- Identificación de índices candidatos (por queries críticas) y estrategia de creación con bajo impacto.[^5]

**Qué no incluye**

- Diseño completo de modelo de datos; solo auditoría y remediación incremental.

**Sensible**

- En índices únicos o cambios grandes, la estrategia puede requerir coordinación con migraciones y despliegue (ver siguiente).[^7]

***

### 5) Migrations seguras (expand/contract) (Fecha: 2025-11-30)

**Facts**

- El patrón expand-migrate-contract: expand (agregar estructuras manteniendo compatibilidad), migrate (deploy de app usando lo nuevo), contract (remover lo viejo post-deploy) está descrito como práctica de despliegue en GitLab.[^7]
- Expand \& contract es un enfoque para cambios de esquema con zero downtime: agregar soporte nuevo, backfill, app consciente de ambos esquemas, luego eliminar lo anterior.[^6]

**Inferences**

- Opción segura: migraciones aditivas (agregar columna/índice), deploy de app compatible hacia atrás, y solo luego “contract”; minimiza rollback doloroso.[^6][^7]
- Opción agresiva: migración destructiva en un paso (drop/rename directo) por velocidad; riesgo: rompe versiones antiguas, jobs en background y scripts de soporte.
- En CRM enterprise, los background jobs (sync, ETL, facturación) suelen ser los que “se quedan con el esquema viejo”, así que el contract debe esperar a que todo esté actualizado.[^7]

**Qué incluye**

- Diseño del plan de migración por fases, validaciones y rollback “operable”.[^6][^7]

**Qué no incluye**

- Herramienta específica (Liquibase/Flyway/etc.); el patrón aplica igual.

**Sensible**

- Cambios que tocan PII (campos de documento, salud, identificadores) requieren revisar también logging/export/backups para no duplicar exposición.[^8]

***

### 6) PII: logging y trazabilidad sin filtrar datos (Fecha: 2009-07-31)

**Facts**

- OWASP enumera explícitamente datos que no deben loguearse: PII sensible (ej. salud, IDs gubernamentales), passwords, access tokens, strings de conexión a DB, llaves de cifrado y otros secretos.[^8]
- OWASP sugiere, cuando se necesita correlación, considerar reemplazar valores sensibles por hashes (ej. IDs de sesión) para rastrear sin exponer el valor.[^10]

**Inferences**

- En CRM, el “daño” típico no es solo exfiltración; es que PII termine replicada en logs centralizados, backups y tickets, haciendo el incidente más caro y más difícil de contener.[^8]
- Opción segura: por defecto, logging redacted/masked (email parcial, doc truncado) y correlación por ID interno o hash.[^10]
- Opción agresiva: loguear payloads completos para debug rápido; riesgo: incumplimiento y exposición masiva (especialmente en integraciones y errores).[^8]

**Qué incluye**

- Checklist de “no log” + revisión de trazas en errores y auditoría de accesos a logs.[^8]

**Qué no incluye**

- Asesoría legal; esto es práctica de ingeniería/seguridad aplicada.

**Sensible**

- Atención a “logs de DB” y “APM traces”: también pueden capturar queries con parámetros (PII) si no se configura sanitización.

***

## Examples (aplicado a CRM enterprise)

**Facts**

- N+1: ejemplo típico (conceptual) en ORM es traer una lista y luego ejecutar una query adicional por cada elemento para cargar una relación; eso es exactamente el patrón descrito como N+1.[^4]
- Para validar hipótesis de performance, `EXPLAIN`/`EXPLAIN ANALYZE` son herramientas estándar para ver plan y runtime real (en PostgreSQL).[^2][^1]

**Inferences (escenarios CRM)**

- “Listado de agencias” (100 agencias) + “última reserva” + “saldo” + “último pago”: si el backend hace 1 query de agencias y luego 100 queries por último pago, tienes N+1; solución típica es traer en una sola query con join/aggregation o precomputar un resumen.[^4]
- “Dashboard operativo” que tarda: antes de cachear, revisa plan; si ves seq scans en tablas grandes, un índice correcto (y creado concurrentemente) puede ser el fix con menor cambio de producto.[^2][^5]
- “Cambio de campo documento_fiscal → tax_id”: hacerlo expand/contract; primero agregar `tax_id`, backfill, app escribe ambos; después de estabilizar, contract y eliminas `documento_fiscal`.[^7][^6]

***

## Metrics / success signals

**Facts**

- Si habilitas leak detection en HikariCP, el sistema puede emitir logs cuando una conexión supera el umbral fuera del pool, útil como señal objetiva de leak.[^3]
- `EXPLAIN ANALYZE` reporta tiempos/filas reales por paso, lo que permite medir si un cambio realmente mejoró ejecución.[^1]

**Inferences (KPIs operables)**

- Salud de pool: % de tiempo con pool saturado (threads esperando), número de eventos de leak detection, y distribución de duración de transacciones (p95/p99).[^3]
- Salud de queries: queries por request (p95), tiempo total en DB por request, y proporción de endpoints con patrones N+1 detectados.[^4]
- Salud de despliegues: porcentaje de migraciones “expand/contract” vs destructivas, y número de incidentes asociados a schema changes.[^6][^7]
- Salud de privacidad: número de hallazgos de PII/secret en logs (muestreo automatizado), y cumplimiento de “no log list”.[^8]

***

## Operational checklist

**Facts**

- Verificar si hay leaks: habilitar `leakDetectionThreshold` (si aplica) y revisar logs de “possible connection leak”.[^3]
- Para performance: obtener plan con `EXPLAIN` y, cuando sea seguro, `EXPLAIN ANALYZE` para runtime real.[^2][^1]
- Para índices en producción Postgres: evaluar `CREATE INDEX CONCURRENTLY` para evitar bloquear escrituras.[^5]
- Para migraciones: aplicar expand/contract (expand-migrate-contract) para mantener compatibilidad durante despliegues.[^7][^6]
- Para PII: revisar que no se logueen PII sensible/secretos (passwords, tokens, strings de conexión, llaves).[^8]

**Inferences (pasos accionables)**

- Mapear 10 endpoints CRM más críticos (listados, dashboard, export, conciliación) y medir: queries/request, tiempo DB, y saturación del pool.
- Clasificar cambios DB en “seguros” (aditivos) vs “sensibles” (destructivos, tablas grandes, PII) y forzar aprobación extra para los sensibles.
- Definir un “runbook” de incidentes DB: qué mirar primero (pool, N+1, plan, locks por índices, migraciones en curso, logs con PII).

***

## Anti-patterns

**Facts**

- Ejecutar `EXPLAIN ANALYZE` implica correr la query para reportar runtime real; usarlo sin control en producción puede agravar carga.[^1]
- Crear índices sin considerar impacto de locking: Postgres diferencia entre build estándar y `CONCURRENTLY` (este último evita locks que impiden escrituras).[^5]
- Loguear PII/secretos (tokens, passwords, strings de conexión) contradice recomendaciones explícitas de OWASP.[^8]

**Inferences**

- “Arreglar N+1 con cache” sin medir queries/request: suele enmascarar el síntoma y deja el costo latente para otros flujos (exports, backoffice).[^4]
- Migraciones destructivas “porque es rápido”: en enterprise, el costo aparece después (rollbacks imposibles, jobs rotos, data drift).[^7]

***

## Diagnostic questions

**Facts**

- ¿Tienes evidencia de leaks vía logs del pool (p. ej., `leakDetectionThreshold` en HikariCP) o solo síntomas?[^3]
- ¿El análisis de performance se apoya en plan (`EXPLAIN`) y runtime real (`EXPLAIN ANALYZE`) cuando corresponde?[^2][^1]
- ¿Tus cambios de esquema siguen expand/contract (expand-migrate-contract) para preservar compatibilidad?[^6][^7]
- ¿Existe una política verificable de “no log” para PII/secretos como recomienda OWASP?[^8]

**Inferences**

- ¿Cuál es tu “presupuesto” aceptable de queries/request por endpoint crítico (y quién lo aprueba)?
- ¿Qué tablas del CRM son “hot write” y por tanto requieren estrategia especial para índices y migraciones?
- ¿Cómo aseguras que exports/reportes no disparen N+1 ni extraigan más PII de la necesaria?

***

## Sources (o referencia a SOURCES.md)

- PostgreSQL Docs — Using EXPLAIN (v18, 2026-02-11).[^2]
- AWS Prescriptive Guidance — PostgreSQL `EXPLAIN` y `EXPLAIN ANALYZE`.[^1]
- PostgreSQL Docs — `CREATE INDEX` y opción `CONCURRENTLY` (v18, 2026-02-11).[^5]
- PostgreSQL Docs — Progress reporting (incluye fases de `CREATE INDEX CONCURRENTLY`) (v18, 2026-02-11).[^9]
- GitLab Blog — expand-migrate-contract para cambios compatibles (2025-11-30).[^7]
- Xata Blog — expand \& contract para zero-downtime schema migrations en Postgres (2024-02-01).[^6]
- OWASP Cheat Sheet Series — Logging (incluye “no log” para PII/secretos) (2009-07-31).[^8]
- OWASP Cheat Sheet Series — Session Management (hash de session ID para correlación) (2010-12-31).[^10]
- HikariCP Javadoc — `leakDetectionThreshold` (API docs).[^3]
- PingCAP — explicación del problema N+1 (2025-06-22).[^4]


### Añadidos propuestos a `SOURCES.md` (sin duplicados)

- PostgreSQL Documentation — “Using EXPLAIN” https://www.postgresql.org/docs/current/using-explain.html (v18; publicado 2026-02-11)[^2]
- PostgreSQL Documentation — “CREATE INDEX” https://www.postgresql.org/docs/current/sql-createindex.html (v18; publicado 2026-02-11)[^5]
- PostgreSQL Documentation — “Progress Reporting” https://www.postgresql.org/docs/current/progress-reporting.html (v18; publicado 2026-02-11)[^9]
- GitLab Blog — “Deploying the world's largest GitLab instance…” (expand-migrate-contract) https://about.gitlab.com/blog/continuously-deploying-the-largest-gitlab-instance/ (publicado 2025-11-30)[^7]
- Xata Blog — “zero-downtime schema migrations postgresql” https://xata.io/blog/zero-downtime-schema-migrations-postgresql (publicado 2024-02-01)[^6]
- OWASP Cheat Sheet Series — “Logging Cheat Sheet” https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html (publicado 2009-07-31)[^8]
- OWASP Cheat Sheet Series — “Session Management Cheat Sheet” https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html (publicado 2010-12-31)[^10]
- HikariCP Javadoc — `HikariConfig` (leakDetectionThreshold) https://www.javadoc.io/doc/com.zaxxer/HikariCP/1.2.4/com/zaxxer/hikari/HikariConfig.html[^3]
- PingCAP — “Solve the N+1 Query Problem” https://www.pingcap.com/article/how-to-efficiently-solve-the-n1-query-problem/ (publicado 2025-06-22)[^4]
- AWS Prescriptive Guidance — “The EXPLAIN query plan” https://docs.aws.amazon.com/prescriptive-guidance/latest/postgresql-query-tuning/explain-query-plan.html[^1]

***

## Key takeaways for PM practice

- Define “riesgos DB” en lenguaje de negocio (caídas, lentitud, fuga de datos) y mapea cada riesgo a una señal observable (pool saturado, N+1, planes malos, migraciones peligrosas).
- Exige evidencia: planes (`EXPLAIN`/`EXPLAIN ANALYZE`) y trazas de leak/N+1 antes de priorizar “optimizaciones”.[^1][^2][^3][^4]
- Estandariza un playbook de cambios seguros: índices concurrentes y migraciones expand/contract por defecto en tablas críticas.[^6][^7][^5]
- Trata PII como incidente esperando ocurrir: “no log list”, redaction, y correlación sin exponer identificadores.[^10][^8]
- Ofrece siempre alternativa “segura vs agresiva” con trade-offs claros para que negocio decida con contexto (velocidad vs riesgo operativo).
<span style="display:none">[^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31]</span>

<div align="center">⁂</div>

[^1]: https://docs.aws.amazon.com/prescriptive-guidance/latest/postgresql-query-tuning/explain-query-plan.html

[^2]: https://www.postgresql.org/docs/current/using-explain.html

[^3]: https://www.javadoc.io/doc/com.zaxxer/HikariCP/1.2.4/com/zaxxer/hikari/HikariConfig.html

[^4]: https://www.pingcap.com/article/how-to-efficiently-solve-the-n1-query-problem/

[^5]: https://www.postgresql.org/docs/current/sql-createindex.html

[^6]: https://xata.io/blog/zero-downtime-schema-migrations-postgresql

[^7]: https://about.gitlab.com/blog/continuously-deploying-the-largest-gitlab-instance/

[^8]: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html

[^9]: https://www.postgresql.org/docs/current/progress-reporting.html

[^10]: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html

[^11]: pasted-text.txt

[^12]: https://alexanderobregon.substack.com/p/connection-leak-detection-with-spring

[^13]: https://stackoverflow.com/questions/35752015/hikaricp-connection-leak-detection-and-hibernate

[^14]: https://oneuptime.com/blog/post/2025-07-02-java-hikaricp-connection-pooling/view

[^15]: https://github.com/brettwooldridge/HikariCP

[^16]: https://www.deployhq.com/blog/database-migration-strategies-for-zero-downtime-deployments-a-step-by-step-guide

[^17]: https://etleap.com/blog/preventing-database-connection-leaks

[^18]: https://docs.gigaspaces.com/latest/dev-java/sql-explain-examples.html

[^19]: https://groups.google.com/g/hikari-cp/c/RcegXZpruAk

[^20]: https://support.atlassian.com/bamboo/kb/bamboo-hikaricp-properties/

[^21]: https://www.snowflake.com/en/developers/guides/snowflake-postgres-execution-plan/

[^22]: https://www.bytebase.com/blog/postgres-create-index-concurrently/

[^23]: https://oneuptime.com/blog/post/2026-01-21-postgresql-concurrent-index/view

[^24]: https://www.postgresql.org/message-id/CAMAof6-=D9jZyBLpbPq7FZJjtuHUtErxyOgAkBkKnVXDj=BDhw@mail.gmail.com

[^25]: https://www.enterprisedb.com/blog/explaining-create-index-concurrently

[^26]: https://forum.liquibase.org/t/postgres-create-concurrently-index/5751

[^27]: https://stackoverflow.com/questions/97197/what-is-the-n1-selects-problem-in-orm-object-relational-mapping

[^28]: https://stackoverflow.com/questions/38889476/postgresql-create-index-concurrently-waiting-column

[^29]: https://docs.sec1.io/user-docs/4-sast/3-javascript/leakage-of-sensitive-information-in-logger-message

[^30]: https://www.tencentcloud.com/techpedia/128956

[^31]: https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet.html

