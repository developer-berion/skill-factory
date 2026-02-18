<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_09 — Integraciones confiables para CRM (Salesforce-like): iPaaS, ETL/ELT y Eventing

## Executive summary (10–15 líneas)

- **Facts:** iPaaS es una plataforma cloud para construir, desplegar y gobernar flujos de integración entre aplicaciones y datos (incluye conectores, monitoreo y controles) (Consultado: 2026-02-18).[^1]
- **Facts:** ETL transforma antes de cargar; ELT carga primero y transforma dentro del warehouse, ganando agilidad cuando el DW tiene cómputo elástico (Consultado: 2026-02-18).[^2]
- **Facts:** En Salesforce Change Data Capture, los eventos se almacenan temporalmente en el event bus (3 días) y cada mensaje trae `ReplayId` para permitir “replay” desde un punto del stream (Consultado: 2026-02-18).[^3]
- **Facts:** Para platform events, Salesforce recomienda identificar de forma única con `EventUuid` y no con `ReplayId` (Consultado: 2026-02-18).[^4]
- **Facts:** Salesforce limita requests concurrentes “long running” (>=20s); en producción y sandboxes el límite citado es 25, y el API puede responder `REQUEST_LIMIT_EXCEEDED` (Consultado: 2026-02-18).[^5]
- **Facts:** Cuando un API aplica rate limiting puede responder HTTP 429 y (en algunos casos) `Retry-After`, que el cliente debe respetar antes de reintentar (Consultado: 2026-02-18).[^6]
- **Facts:** Un DLQ permite apartar mensajes no consumidos y luego moverlos (“redrive”) a otra cola/destino para reproceso controlado (Consultado: 2026-02-18).[^7]
- **Facts:** Pact formaliza contract testing “consumer-driven”: el consumidor escribe tests, se genera un contrato (JSON), se publica/compart e, y el proveedor verifica compatibilidad ejecutando esos contratos (Consultado: 2026-02-18).[^8]
- **Inferences:** En integraciones CRM reales, “confiable” = tolerar duplicados, reintentos, límites y caídas parciales sin romper datos (idempotencia + DLQ + observabilidad).
- **Inferences:** La decisión ganadora suele ser híbrida: event-driven para cambios operativos/near-real-time y batch/ELT para analítica y backfills.
- **Inferences:** El mayor riesgo B2B con partners no es “la API”, es el cambio silencioso; por eso necesitas contratos, versionado y pruebas por tenant/sandbox.

***

## Definitions and why it matters

### iPaaS

- **Facts:** iPaaS es una plataforma cloud para construir, desplegar y administrar flujos de integración dentro del cloud y entre cloud/on‑prem, con foco en conectividad, seguridad y gobernanza (Consultado: 2026-02-18).[^1]
- **Inferences:** Importa porque reduce time-to-integrate (conectores + mapeos + scheduling) y te da control operativo (alertas, reintentos, colas, trazabilidad) sin “inventar” infraestructura.


### ETL vs ELT

- **Facts:** En ETL la transformación ocurre antes de cargar; en ELT se carga primero (raw/preprocesado) y se transforma después dentro del warehouse, lo que suele dar más agilidad (Consultado: 2026-02-18).[^2]
- **Inferences:** Importa porque separa dos mundos: (a) integraciones operativas (consistencia, SLAs cortos) vs (b) pipelines analíticos (backfills, modelos, auditoría).


### Event-driven (CDC / Platform Events)

- **Facts:** En Salesforce CDC, los mensajes se guardan 3 días en el event bus y `ReplayId` permite reanudar/reproducir desde un evento específico (Consultado: 2026-02-18).[^3]
- **Facts:** Para identificar de forma única un mensaje de platform events, Salesforce indica usar `EventUuid` y no `ReplayId` (Consultado: 2026-02-18).[^4]
- **Inferences:** Importa porque el modo event-driven casi siempre es “at-least-once”: si no diseñas idempotencia, duplicas órdenes, pagos, reservas, comisiones o estados.


### Rate limits y concurrencia

- **Facts:** Salesforce publica límites de requests concurrentes “long running” (>=20s); en producción/sandboxes el límite citado es 25 y puede devolver `REQUEST_LIMIT_EXCEEDED` cuando se excede (Consultado: 2026-02-18).[^5]
- **Facts:** Existen APIs que al alcanzar rate limit responden HTTP 429 y entregan `Retry-After` para indicar cuándo reintentar (Consultado: 2026-02-18).[^6]
- **Inferences:** Importa porque el “éxito” comercial de la integración se rompe por picos (campañas, cierres, importaciones masivas) si no gobiernas throughput.


### DLQ (Dead-letter queue)

- **Facts:** AWS SQS documenta el “redrive” para mover mensajes no consumidos desde un DLQ a un destino (por defecto, a la cola fuente), y permite controlar la velocidad de movimiento (Consultado: 2026-02-18).[^7]
- **Inferences:** Importa porque separa “errores recuperables” (reintentos) de “errores que requieren intervención” (DLQ + runbook), evitando que se “trabe” toda la operación.


### Contract testing con partners

- **Facts:** Pact describe contract testing consumer-driven: el consumidor define expectativas en tests con un mock, se genera un contrato JSON, se publica/compart e, y el proveedor lo verifica contra su implementación (Consultado: 2026-02-18).[^8]
- **Inferences:** Importa porque reduce caídas por cambios de payload/campos y convierte integraciones B2B en una disciplina repetible (como CI/CD, pero para APIs).

***

## Principles and best practices (con citas por sección + fecha)

### 1) Selecciona el “modo” por caso de uso

- **Facts:** ELT suele favorecer agilidad al cargar primero y transformar después dentro del warehouse (Consultado: 2026-02-18).[^2]
- **Inferences:** Regla práctica:
    - Operación (estado de reservas, cuentas, crédito, límites): event-driven o near-real-time.
    - Analítica (reporting, cohortes, LTV, margen): batch + ELT.
    - Sincronización bidireccional “en vivo”: iPaaS con cola/eventos y reglas estrictas de ownership de campos.


### 2) Diseña para “at-least-once” (idempotencia obligatoria)

- **Facts:** En streams de Salesforce, `ReplayId` existe para replay, pero no es el identificador único recomendado para platform events; Salesforce indica usar `EventUuid` (Consultado: 2026-02-18).[^4]
- **Inferences:** Patrón mínimo de idempotencia (CRM enterprise):
    - Define un `idempotency_key` por objeto/operación (por ejemplo: `source_system + object + source_id + operation + version`).
    - Persiste “dedupe state” (tabla o store) con TTL y “último estado aplicado”.
    - En Salesforce-like: usa External IDs + upsert donde aplique, y controla “last write wins” vs “merge” por reglas de negocio.


### 3) Reintentos: controlados, con backoff, y respetando `Retry-After`

- **Facts:** Algunos endpoints devuelven HTTP 429 y `Retry-After`, y se indica que el cliente debe esperar ese tiempo antes del próximo intento (Consultado: 2026-02-18).[^6]
- **Facts:** Salesforce puede rechazar nuevas requests si se exceden límites de concurrencia de “long running” (>=20s), devolviendo `REQUEST_LIMIT_EXCEEDED` (Consultado: 2026-02-18).[^5]
- **Inferences:** Buenas prácticas concretas:
    - Backoff exponencial con jitter, límite de reintentos y “circuit breaker” por tenant.
    - Clasifica errores: 429/limit/concurrency => reintentar; 4xx de validación => no reintentar, a DLQ con causa.
    - “Retry budget”: si el sistema entra en tormenta de reintentos, prioriza transacciones críticas (pagos/ordenes) vs sync de catálogo.


### 4) Rate limiting: gobierna throughput por tenant y por conector

- **Facts:** Hay límites publicados para concurrencia (p.ej. 25 long-running en prod/sandboxes) que bloquean nuevas requests hasta bajar del umbral (Consultado: 2026-02-18).[^5]
- **Facts:** Un mecanismo de rate limiting puede devolver 429 y `Retry-After` (Consultado: 2026-02-18).[^6]
- **Inferences:** Implementación práctica:
    - “Token bucket” por tenant + por integración (Salesforce vs ERP vs Marketing), con colas internas para smoothing.
    - Evita jobs masivos en horario pico comercial; crea ventanas y prioridades.
    - “Plan de picos”: define capacidad máxima por cliente/agencia (o partner) y qué se degrada primero.


### 5) DLQ + redrive con runbooks (operación, no teoría)

- **Facts:** AWS SQS permite redrive desde DLQ hacia la cola fuente u otra cola/destino para reprocesar, y ajustar la velocidad de redrive (Consultado: 2026-02-18).[^7]
- **Inferences:** Política recomendada:
    - DLQ por conector + por tipo de evento (no mezcles “Lead” con “Invoice”).
    - Redrive solo después de corregir causa (fix de mapeo, permisos, schema), nunca “a ciegas”.
    - Registra en el DLQ: payload original, headers, intentos, error class, y el `idempotency_key`.


### 6) Contract testing con partners: “rompe antes en CI”

- **Facts:** En Pact, el consumidor escribe tests, se genera un contrato JSON y el proveedor lo verifica; esto evita breaking changes para lo que el consumidor realmente usa (Consultado: 2026-02-18).[^8]
- **Inferences:** En B2B con partners:
    - Contratos por versión (`v1`, `v1.1`) y por tenant (si hay custom fields).
    - “Contract gates” antes de deploy y antes de activar un nuevo campo obligatorio.
    - Incluye casos de error esperados (validaciones, límites, 429) para que el cliente sepa qué hacer.


### 7) Sandboxes/tenants: separa entornos como si fueran clientes distintos

- **Facts:** La tabla de límites citada incluye “Production orgs and Sandboxes” juntos para concurrencia long-running (Consultado: 2026-02-18).[^5]
- **Inferences:** Checklist de aislamiento: credenciales por entorno, llaves por tenant, colas y DLQ por entorno, y datos sintéticos (o enmascarados) para pruebas de regresión.

***

## Examples (aplicado a CRM enterprise)

### Pipelines por conector (patrones)

| Conector | Trigger / Entrada | Transporte | Proceso | Idempotencia | Reintentos / límites | DLQ / Recuperación |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Salesforce CDC → Integraciones internas | Change events (CDC) con replay | Pub/Sub/Streaming | Normalizar + enrutar por objeto | Usar `EventUuid` como ID único recomendado para platform events [^4] | Reanudar con `ReplayId`; eventos en bus 3 días [^3] | DLQ por tipo de evento; redrive controlado (concepto) [^7] |
| Salesforce REST/SOAP → iPaaS | Polling o webhooks externos | HTTP | Upsert a objetos CRM | External ID + dedupe store (inference) | Manejar `REQUEST_LIMIT_EXCEEDED` por concurrencia long-running [^5] | DLQ por error de validación/permisos; reprocesar tras fix (inference) |
| Partner API (B2B) ↔ CRM | Requests event-driven o batch | HTTP + cola | Validación + mapping + enriquecimiento | `idempotency_key` por operación (inference) | Respetar 429 + `Retry-After` cuando aplique [^6] | DLQ para payloads “poison”; runbook + redrive [^7] |
| ETL/ELT CRM → DWH | Carga diaria / incremental | Batch (archivos/connector) | Load raw → transform in-warehouse | Dedupe por keys en staging (inference) | ELT: transformar dentro del DW, agilidad [^2] | Reprocesos por partición/fecha (inference) |
| Contract testing (Consumer CRM apps ↔ Provider) | Cambios de API y payloads | CI/CD | Generar + verificar contratos | Contrato como “fuente de verdad” (inference) | Prevenir breaking changes verificando contracts [^8] | Fallo de verificación bloquea release (inference) |

### Ejemplo 1: “Cuenta/Agencia creada en CRM” → ERP + scoring riesgo

- **Facts:** En CDC, el orden se basa en commits y el stream permite replay vía `ReplayId` (Consultado: 2026-02-18).[^3]
- **Inferences:** Flujo: CDC (Account) → cola → servicio de scoring → iPaaS → ERP; la salida al ERP se hace idempotente (misma cuenta no se crea dos veces) y los errores de validación van a DLQ con razón de negocio (RIF inválido, país no soportado).


### Ejemplo 2: “Órdenes / reservas” con picos (campaña) sin reventar límites

- **Facts:** Si se exceden límites de concurrencia long-running, Salesforce puede rechazar con `REQUEST_LIMIT_EXCEEDED` y no procesa nuevas requests hasta bajar del umbral (Consultado: 2026-02-18).[^5]
- **Facts:** Rate limiting puede responder 429 y `Retry-After`, que el cliente debe respetar (Consultado: 2026-02-18).[^6]
- **Inferences:** Estrategia: throttling por tenant + colas internas; “modo seguro” degrada a async (acepta pedido, confirma luego) y “modo agresivo” intenta sync inmediato solo para agencias VIP.


### Ejemplo 3: Partner que cambia campos sin avisar → evitar incidentes

- **Facts:** Pact define consumer-driven contracts donde el consumidor publica contratos y el proveedor verifica compatibilidad (Consultado: 2026-02-18).[^8]
- **Inferences:** Regla operativa: ningún partner puede introducir un campo obligatorio o cambiar tipo sin pasar verificación de contrato; si el partner no tiene CI, se usa un “contract harness” en tu lado como pre-flight antes de habilitar en producción.

***

## Metrics / success signals

- **Facts:** Ventana de replay/retención en Salesforce CDC: 3 días en el event bus (útil para definir RTO de consumo y política de backfill) (Consultado: 2026-02-18).[^3]
- **Facts:** Señal de saturación: errores `REQUEST_LIMIT_EXCEEDED` por concurrencia long-running (>=20s) (Consultado: 2026-02-18).[^5]
- **Inferences (métricas recomendadas):**
- Latencia p95 por integración (evento→aplicado en destino).
- Tasa de duplicados detectados (debería tender a ~0; si sube, falla idempotencia).
- “Retry rate” y “retry success rate” (reintentos que recuperan vs reintentos inútiles).
- Consumo de límites (requests/min, concurrencia, batch windows) por tenant.
- DLQ depth + edad del mensaje más viejo + tiempo medio de resolución.
- Drift de contratos: % contracts verificados por release y fallos por provider.

***

## Operational checklist

- **Facts:** Si hay 429 con `Retry-After`, debes esperar ese tiempo para que el próximo request sea exitoso (Consultado: 2026-02-18).[^6]
- **Facts:** DLQ redrive existe para mover mensajes desde DLQ a un destino para reproceso controlado (Consultado: 2026-02-18).[^7]
- **Inferences (pasos accionables):**

1. Define ownership por objeto/campo (quién “manda” en CRM vs ERP vs Marketing).
2. Establece `idempotency_key` estándar y una tabla/store de dedupe con TTL.
3. Implementa clasificación de errores: retryable (429, timeouts) vs no-retryable (validación).
4. Aplica backoff exponencial con jitter y respeta `Retry-After`.
5. Throttling por tenant + colas internas; prioriza flujos críticos.
6. DLQ por conector/tipo; runbook: “cómo inspeccionar”, “cómo corregir”, “cómo redrive”.
7. Contract testing: versionado, publicación, verificación por release; bloquear deploy si falla.
8. Observabilidad: correlation IDs end-to-end, métricas de duplicados, DLQ, límites, latencias.

**Qué incluye (mínimo viable confiable)**

- Idempotencia, reintentos con backoff, rate limiting, DLQ + redrive, trazabilidad y contracts con partners.

**Qué no incluye (si no lo pides explícito)**

- Master Data Management completo, reconciliación contable, ni gobierno de calidad de datos a nivel corporativo (solo “lo necesario para que no se rompa”).

**Qué es sensible (riesgo comercial/operativo)**

- Bidireccional en tiempo real sin ownership; reintentos sin dedupe; y “bulk jobs” en horario pico sin throttling.

**Opción segura vs agresiva**

- Segura: async + colas + confirmación diferida, prioriza integridad sobre inmediatez.
- Agresiva: sync donde se pueda, pero con degradación automática a async al detectar 429/limits.

***

## Anti-patterns

- **Facts:** Usar `ReplayId` como identificador único de platform events en vez de `EventUuid` (Salesforce indica `EventUuid` como el identificador único) (Consultado: 2026-02-18).[^4]
- **Facts:** Ignorar 429/`Retry-After` y “martillar” el API incrementa fallas y no respeta el mecanismo de protección (Consultado: 2026-02-18).[^6]
- **Inferences (errores típicos):**
- “Retry infinito” sin budget ni DLQ (tormenta de reintentos).
- Un solo DLQ para todo (imposible operar/priorizar).
- Sin contratos: cambios de partner se descubren en producción.
- Cargas masivas sin ventanas, sin throttling por tenant, y sin monitoreo de límites.
- No separar sandbox/tenant a nivel de credenciales, colas y métricas (mezcla de señales, debugging imposible).

***

## Diagnostic questions

- ¿Qué objetos/flujos son “dinero” (reservas, facturación, crédito) y cuáles toleran delay?
- ¿Cuál es tu definición explícita de idempotencia por operación (create/update/cancel)?
- ¿Dónde persistes el estado de dedupe y por cuánto tiempo?
- ¿Qué errores reintentas y cuáles van directo a DLQ con intervención humana?
- ¿Cómo detectas que estás pegando límites (429, `REQUEST_LIMIT_EXCEEDED`) y cómo degradás?
- ¿Tienes contracts versionados por partner y un gate de verificación antes de deploy?
- ¿Tu operación puede hacer redrive seguro (con runbook) sin “reprocesar y duplicar”?

***

## Sources (y referencias para SOURCES.md)

**Fuentes usadas**

- MuleSoft — “iPaaS: Integration Platform as a Service” (Consultado: 2026-02-18).[^1]
- Snowflake — “What Is ELT?” (Consultado: 2026-02-18).[^2]
- Salesforce Developers — “API Request Limits and Allocations (Concurrent API Request Limits)” (Consultado: 2026-02-18).[^5]
- Salesforce Developers — “Change Event Storage and Delivery (CDC)” (Consultado: 2026-02-18).[^3]
- Salesforce Developers — “Message Durability (Streaming API) — EventUuid vs ReplayId” (Consultado: 2026-02-18).[^4]
- Salesforce Developers (Commerce API) — “Load Shedding and Rate Limiting (HTTP 429, Retry-After)” (Consultado: 2026-02-18).[^6]
- AWS — “Configure a dead-letter queue redrive in Amazon SQS” (Consultado: 2026-02-18).[^7]
- Pact Docs — “Consumer Tests (consumer-driven contract testing)” (Consultado: 2026-02-18).[^8]
- Google Cloud — “Cloud API Design Guide: Errors (ejemplo incluye 429)” (Consultado: 2026-02-18).

**Añadir a `SOURCES.md` (sin duplicados, sugerido)**

- https://www.mulesoft.com/integration/ipaas-integration-platform-as-a-service
- https://www.snowflake.com/en/fundamentals/understanding-extract-load-transform-elt/
- https://developer.salesforce.com/docs/atlas.en-us.salesforce_app_limits_cheatsheet.meta/salesforce_app_limits_cheatsheet/salesforce_app_limits_platform_api.htm (API limits / concurrencia)
- https://developer.salesforce.com/docs/atlas.en-us.change_data_capture.meta/change_data_capture/cdc_subscribe_delivery.htm
- https://developer.salesforce.com/docs/atlas.en-us.api_streaming.meta/api_streaming/using_streaming_api_durability.htm
- https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-dead-letter-queue-redrive.html
- https://docs.pact.io/implementation_guides/javascript/docs/consumer
- https://developer.salesforce.com/docs/commerce/commerce-api/guide/throttle-rates.html
- https://cloud.google.com/apis/design/errors

***

## Key takeaways for PM practice

- Define “confiable” como un contrato operativo: idempotencia + retry policy + DLQ + observabilidad, no como “que la API responda”.
- Decide por flujo: event-driven para operación; ELT/batch para analítica y backfills; híbrido casi siempre gana.
- En Salesforce-like, trata límites y 429 como comportamiento normal del sistema, no como excepción.
- Con partners, contract testing es tu seguro anti-cambios silenciosos; sin eso, vas a pagar incidentes en producción.
- Diseña por tenant/sandbox como si fueran clientes distintos: aislamiento + métricas + runbooks, o no podrás escalar.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31][^9]</span>

<div align="center">⁂</div>

[^1]: https://www.mulesoft.com/integration/ipaas-integration-platform-as-a-service

[^2]: https://www.snowflake.com/en/fundamentals/understanding-extract-load-transform-elt/

[^3]: https://developer.salesforce.com/docs/atlas.en-us.change_data_capture.meta/change_data_capture/cdc_subscribe_delivery.htm

[^4]: https://developer.salesforce.com/docs/atlas.en-us.api_streaming.meta/api_streaming/using_streaming_api_durability.htm

[^5]: https://developer.salesforce.com/docs/atlas.en-us.salesforce_app_limits_cheatsheet.meta/salesforce_app_limits_cheatsheet/salesforce_app_limits_platform_api.htm

[^6]: https://developer.salesforce.com/docs/commerce/commerce-api/guide/throttle-rates.html

[^7]: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-dead-letter-queue-redrive.html

[^8]: https://docs.pact.io/implementation_guides/javascript/docs/consumer

[^9]: pasted-text.txt

[^10]: https://www.workato.com/the-connector/ipaas-complete-guide/

[^11]: https://www.qlik.com/us/data-integration/ipaas

[^12]: https://www.oneio.cloud/blog/what-is-ipaas

[^13]: https://www.digitalroute.com/resources/glossary/ipaas/

[^14]: https://coalesce.io/data-insights/etl-vs-elt-key-differences/

[^15]: https://stackoverflow.com/questions/71792521/aws-sqs-dead-letter-queue-redrive-policy

[^16]: https://www.snaplogic.com/blog/what-is-ipaas-integration-platform-as-a-service

[^17]: https://www.youtube.com/watch?v=cGzabBRPxFY

[^18]: https://oneuptime.com/blog/post/2026-02-02-sqs-retry-logic/view

[^19]: https://www.teamcentral.ai/what-is-ipaas-discovering-the-future-of-low-no-code-data-integration-and-automation/

[^20]: https://www.techtarget.com/searchcloudcomputing/definition/iPaaS-integration-platform-as-a-service

[^21]: https://www.integrate.io/blog/etl-vs-elt/

[^22]: https://help.salesforce.com/s/articleView?language=en_US\&id=mktg.mc_overview_limits_api.htm\&type=5

[^23]: https://www.reddit.com/r/SalesforceDeveloper/comments/13s3hiu/concurrent_api_request_limits/

[^24]: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_limits.htm

[^25]: https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/salesforce_app_limits_cheatsheet.pdf

[^26]: https://docs.pact.io

[^27]: https://www.stacksync.com/blog/bypass-salesforce-api-limits-real-time-bi-directional-sync

[^28]: https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/salesforce_change_data_capture.pdf

[^29]: https://pactflow.io/what-is-consumer-driven-contract-testing/

[^30]: https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/implementation_considerations.htm

[^31]: https://developer.salesforce.com/docs/atlas.en-us.change_data_capture.meta/change_data_capture/cdc_allocations.htm

