<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_03_CI_TestStrategy_ContractTesting — Estrategia de pruebas por capas para CRM (unit/integration/contract/e2e/performance)

## Executive summary (10–15 líneas)

- **Fact:** Usa una pirámide de pruebas: muchas unitarias, algunas de integración/contrato y muy pocas E2E/UI para mantener velocidad y mantenibilidad.
- **Inference:** En CRM enterprise, el cuello de botella casi siempre está en integraciones + datos, no en lógica pura; diseña la estrategia alrededor de eso.
- **Fact:** Las pruebas de integración validan puntos de borde (DB, filesystem, APIs) y son más lentas que unit tests, pero suben la confianza.
- **Fact:** Contract tests reducen el riesgo de “dobles” (mocks/stubs) desalineados con el servicio real y detectan cambios de contrato temprano.[^1]
- **Fact:** En CDC (consumer-driven contracts), el consumidor expresa expectativas y el proveedor las corre continuamente en su pipeline para evitar breaking changes.
- **Fact:** El patrón Consumer-Driven Contracts busca dar al proveedor visibilidad de obligaciones con consumidores y soporte a evolución del servicio.[^2]
- **Fact:** Un test “flaky” puede pasar y fallar con el mismo código, generando ruido y decisiones equivocadas en CI.[^3]
- **Inference:** Controla flakiness con (a) aislamiento, (b) observabilidad, (c) cuarentena inteligente y (d) sacar flakes del “critical path” sin perder señal.
- **Fact:** Una causa común de inestabilidad es mala higiene de test data; la limpieza automatizada reduce contaminación y conflictos entre corridas.[^4]
- **Fact:** Ambientes efímeros (temporales) ayudan al aislamiento y a evitar “state leak” entre pipelines.[^4]
- **Inference:** Mide éxito con tiempo de pipeline, tasa de flakes, MTTR de flakes y % de contratos verificados antes de merge.

***

## Definitions and why it matters

**Facts**

- Unit tests: validan unidades pequeñas (función/clase) y son la base rápida del suite.
- Integration tests: validan integración con componentes externos (DB, servicios, colas), típicamente en boundaries donde serializas/deserializas.
- Contract tests: verifican que las llamadas a un servicio externo “cumplen el contrato” y que tu test double representa al servicio real; suelen ejecutarse con cadencia alineada a cambios del servicio externo (p.ej., diario) más que al ritmo de tu repo.[^1]
- Consumer-Driven Contract (CDC): los consumidores publican expectativas ejecutables y el proveedor las corre para evitar cambios que rompan consumidores.
- Flaky test: el mismo test puede pasar y fallar con el mismo código (señal no determinista).[^3]

**Inferences**

- En un CRM enterprise, el “contrato” relevante no es solo payload/JSON: también incluye semántica (campos obligatorios), políticas (auth, rate limits) y SLOs prácticos (latencia/errores) que afectan ventas y operación.
- Si no tienes contract testing, el costo lo pagas como fricción comercial: incidentes en integraciones, hotfixes, pérdida de confianza de usuarios internos y “margen” quemado en soporte.

***

## Principles and best practices (con citas por sección + fecha)

**Facts (con fecha)**

- (2018-02-26) Mantén forma de pirámide: muchas unitarias; “some” pruebas más coarse-grained (p.ej. integración/contrato); “very few” end-to-end para evitar una suite lenta e inmantenible.
- (2018-02-26) Contract tests ayudan a que el fake/stub usado en integration tests sea un double fiel del servicio real, evitando que cambie el API y tus tests sigan “verdes” engañosamente.
- (2011-01-12) Para servicios externos, complementa tests contra double con contract tests que comparen resultados contra el servicio real (idealmente instancia de test), y que disparen trabajo de alineación más que romper el build sin contexto.[^1]
- (2006-06-12) Consumer-Driven Contracts busca dar al proveedor insight sobre cómo se usa su contrato y qué obligaciones debe mantener al evolucionar.[^2]
- (2025-02-01) Automatizar limpieza/rollback de datos de prueba mejora confiabilidad; sin cleanup, el test data se vuelve inestable y produce resultados no confiables y demoras de despliegue.[^4]

**Inferences (aplicables a CRM)**

- Capas recomendadas (regla operativa):
    - Unit: reglas de negocio, validaciones, mapeos, cálculos (rápido, local).
    - Integration (narrow): repositorios/DB, serialización de eventos, clientes HTTP con un fake controlado.
    - Contract: contratos con ERP/marketing automation/payment/email/SMS/BI, tanto inbound como outbound.
    - E2E: 3–8 “journeys” críticos (lead→oportunidad→cotización→orden→factura/nota), no más.
    - Performance: smoke de latencia/throughput y “degradación” bajo carga para endpoints top.
- “Opción segura” vs “agresiva” para gates de PR:
    - Segura: unit + integración narrow + contratos (consumer side) + static checks siempre; E2E nightly.
    - Agresiva: agrega subset E2E en PR solo para módulos tocados + contratos provider-side obligatorios antes de deploy.

***

## Examples (aplicado a CRM enterprise)

**Facts**

- CDC se implementa haciendo que el consumidor escriba tests con expectativas y el proveedor los ejecute continuamente para bloquear cambios incompatibles.
- Contract tests existen precisamente por el riesgo de que un test double deje de representar al servicio real cuando cambia el contrato externo.[^1]

**Inferences (ejemplo concreto CRM)**

- Contexto: CRM B2B con integraciones:
    - Inbound: Webhooks de pagos, eventos de marketing (lead scoring), actualizaciones de ERP.
    - Outbound: creación de clientes en ERP, emisión de factura, disparo de emails/SMS, registro de actividades a BI.
- Contract test “consumer-side” (CRM consume ERP):
    - Expectativa: `GET /customers/{id}` devuelve `id`, `status`, `creditLimit`, `updatedAt` y códigos de error estables.
    - Regla: si `status=BLOCKED`, CRM debe bloquear creación de órdenes; esto se valida con contract test + unit test de la regla.
- Contract test “provider-side” (Agencias/Front consume CRM API):
    - Endpoint: `POST /opportunities` y `PATCH /opportunities/{id}`.
    - Contrato: campos requeridos, enumeraciones, validación, y backward compatibility (campos nuevos opcionales).
- E2E mínimo (3 journeys):
    - Journey 1: lead→oportunidad→cotización→cierre (happy path).
    - Journey 2: creación de orden bloqueada por crédito (riesgo).
    - Journey 3: reintento idempotente de webhook de pago (duplicados).
- Performance smoke (pre-prod):
    - Prueba: `GET /customers/{id}` p95 < X ms con 50–100 RPS, y `POST /opportunities` sin degradación lineal anómala (solo smoke, no benchmark).

***

## Metrics / success signals

**Facts**

- Flaky tests se identifican por inconsistencia (pasa/falla con el mismo código), por lo que una métrica clave es su tasa/ratio en el tiempo.[^3]
- Re-ejecutar y capturar contexto (logs, historial CI, etc.) es una práctica común para diagnosticar flakiness y dejar evidencia accionable.[^5]
- La contaminación de datos de prueba impacta confiabilidad; estrategias de rollback/cleanup apuntan a estabilizar runs repetibles.[^4]

**Inferences (definiciones operativas)**

- Métricas recomendadas (con fórmulas simples):
    - Tiempo de pipeline (PR): `T_total = T_build + T_unit + T_int + T_contract + T_e2e_subset`.
    - Tasa de flakes: `flake_rate = (#fails_intermitentes) / (#ejecuciones_totales)` por suite y por test.
    - % de “gating confidence”: `%PRs que pasan sin re-run manual` (proxy de fricción).
    - MTTR flake: tiempo desde primer flake hasta fix/mitigación (quarantine, refactor, data fix).
    - Contract coverage: `% de integraciones críticas con contrato versionado + verificación en CI`.
- Señales de éxito:
    - PR pipeline < 15–25 min (dependiendo del tamaño) y con varianza baja.
    - flake_rate < 0.5% en PR (y flakes fuera del critical path si excede).
    - Menos hotfixes por integraciones: proxy “incidentes por cambio” en endpoints integrados.

***

## Operational checklist

**Facts**

- En contract testing para servicios externos, es útil correr contract tests con cadencia distinta al pipeline principal (p.ej. diario) alineada a cambios del proveedor.[^1]
- Contract tests “no necesariamente deben romper el build” como un unit failure, pero sí deben disparar una tarea para restaurar consistencia y conversación con el equipo proveedor.[^1]
- El aislamiento por ambientes temporales ayuda a evitar conflictos de data/state entre ejecuciones.[^4]

**Inferences (paso a paso)**

- Diseño por capas
    - Define qué entra en unit vs integration vs contract vs E2E (documenta 1 página por módulo).
    - Establece “gates” por tipo: PR (rápido) vs nightly (profundo) vs weekly (perf/soak).
- Flakiness control
    - Etiqueta y mide flakes; si un test cruza umbral, pásalo a “quarantine suite” (no bloquea PR) con ticket automático.
    - Añade “rerun inteligente” solo para diagnosticar (guardar artefactos), no para ocultar falla.
- Test data management
    - Define datasets versionados (seed) + estrategia de cleanup (rollback/transactions, reset de DB, o fixtures por test).
    - Evita datos compartidos entre pipelines paralelos (reserva/namespace por run).
- Ambientes efímeros
    - Por PR: levantar stack mínimo (DB + servicios fake + service under test) y destruir al final.
    - Mantén “golden config” (IaC) para que sea reproducible.
- Contract testing (APIs e integraciones)
    - Define contratos por consumidor (CRM→ERP, CRM→Email, AgencyApp→CRM).
    - Versiona contratos y exige verificación en CI antes de deploy del proveedor.
    - Alinea manejo de cambios: deprecations con ventana + backward compatibility por defecto.

***

## Anti-patterns

**Facts**

- Un exceso de UI/E2E tests tiende a volver la suite lenta y frágil; la pirámide busca evitar un “ice-cream cone” de demasiados tests de alto nivel.
- Si usas doubles sin verificación de contrato, puedes tener falsos verdes: el fake responde “lo que tú crees” y no lo que el proveedor realmente ofrece.[^1]

**Inferences**

- “Retry hasta que pase” como política: convierte flaky en deuda invisible y mata la señal de calidad.
- Datos de prueba “manuales” en ambientes compartidos: produce flakes por colisión y genera soporte constante.
- Contract tests que solo validan “schema happy path”: no cubren errores, auth, límites, idempotencia, ni campos opcionales críticos.
- Performance testing solo al final: descubres regresiones cuando ya están integradas y es más caro revertir.

***

## Diagnostic questions

**Facts**

- Si el contrato externo cambia, un contract test fallando indica que debes actualizar doubles y probablemente el código, además de coordinar con el proveedor.[^1]
- CDC fomenta comunicación entre equipos porque el proveedor ve fallas como señal para hablar del cambio.

**Inferences (preguntas para tu CRM)**

- ¿Qué 5 integraciones te rompen operación con más frecuencia (por volumen o criticidad), y tienen contrato automatizado hoy?
- ¿Cuál es tu flake_rate en PR y cuánto tiempo humano se pierde por semana en re-runs e investigaciones?
- ¿Cuántos E2E realmente bloquean revenue/operación si fallan, y cuántos son “nice to have”?
- ¿Tu test data se “resetea” por ejecución (o al menos por pipeline), o depende de estado acumulado?
- ¿Puedes levantar un ambiente efímero reproducible por PR en <10 min con IaC, o dependes de un QA shared?

***

## Sources (o referencia a SOURCES.md)

**Fuentes usadas**

- Martin Fowler — *The Practical Test Pyramid* (2018-02-26).
- Martin Fowler — *Contract Test* (2011-01-12).[^1]
- Ian Robinson / Martin Fowler — *Consumer-Driven Contracts: A Service Evolution Pattern* (2006-06-12).[^2]
- Google Testing Blog — *Flaky Tests at Google and How We Mitigate Them* (2016-05-26) (definición de flaky en snippet).[^3]
- Qase — *Flaky tests* (2024-04-14) (prácticas de identificación y captura de evidencia).[^5]
- The Green Report — *Techniques for Effective Test Data Cleanup in CI/CD* (2025-02-01).[^4]

**Añadir a `SOURCES.md` (sin duplicados)**

- https://martinfowler.com/articles/practical-test-pyramid.html — “The Practical Test Pyramid” (2018-02-26).
- https://martinfowler.com/bliki/ContractTest.html — “Contract Test” (2011-01-12).
- https://martinfowler.com/articles/consumerDrivenContracts.html — “Consumer-Driven Contracts: A Service Evolution Pattern” (2006-06-12).
- https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html — “Flaky Tests at Google and How We Mitigate Them” (2016-05-26).
- https://qase.io/blog/flaky-tests/ — “Flaky tests…” (2024-04-14).
- https://www.thegreenreport.blog/articles/techniques-for-effective-test-data-cleanup-in-cicd/ — “Techniques for Effective Test Data Cleanup in CI/CD” (2025-02-01).

***

## Key takeaways for PM practice

- Prioriza contracts en integraciones críticas: es la forma más barata de bajar riesgo operativo sin inflar E2E.
- Flakiness es fricción de delivery: mídela y sácala del critical path sin perder trazabilidad.
- Test data + ambientes efímeros son producto (infra) que habilita velocidad: sin eso, cualquier suite se degrada.
- Diseña gates por objetivo (PR vs nightly vs performance) para equilibrar rapidez y confianza.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: pasted-text.txt

[^2]: https://www.youtube.com/watch?v=lvR4qJ3hSKY

[^3]: https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html

[^4]: https://www.thegreenreport.blog/articles/techniques-for-effective-test-data-cleanup-in-cicd/techniques-for-effective-test-data-cleanup-in-cicd.html

[^5]: https://qase.io/blog/flaky-tests/

[^6]: https://www.sngular.com/es/insights/280/contract-testing-vs-testing-funcional

[^7]: https://www.coursehero.com/file/148692645/Plantilla-de-Plan-de-Pruebas-de-Software-1doc/

[^8]: https://www.sngular.com/es/insights/132/pruebas-contract-testing

[^9]: https://martinfowler.com/articles/practical-test-pyramid.html

[^10]: https://aaltodoc.aalto.fi/bitstreams/1c80b39b-cd84-490e-bccc-b2ba9071c52f/download

[^11]: https://talent500.com/blog/google-flaky-test-mitigation-strategies/

[^12]: https://seifrajhi.github.io/blog/ephemeral-environments-kubernetes-cicd/

[^13]: https://martinfowler.com/articles/consumerDrivenContracts.html

[^14]: https://research.google/pubs/de-flake-your-tests-automatically-locating-root-causes-of-flaky-tests-in-code-at-google/

[^15]: https://www.k2view.com/what-is-test-data-management/

[^16]: https://martinfowler.com/bliki/ContractTest.html

