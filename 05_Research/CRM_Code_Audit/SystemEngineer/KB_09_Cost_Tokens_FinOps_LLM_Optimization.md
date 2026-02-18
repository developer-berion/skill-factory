<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_09 — FinOps + optimización de tokens (LLM)

## Executive summary (10–15 líneas)

- [Fact] El gasto en LLM escala casi linealmente con tokens; por eso FinOps aplicado a LLM debe medir y asignar costo por uso (no solo “facturas”) para poder optimizar.[^1]
- [Fact] FOCUS (FinOps Open Cost and Usage Specification) busca **normalizar** datos de costo/uso entre vendors para habilitar chargeback, asignación, presupuestos y forecasting con un esquema común.[^2][^3]
- [Inference] En LLM, el “recurso” a costear no es una VM: es una *interacción* (request) con atributos (tenant, caso de uso, modelo, prompt version, cache-hit, tokens in/out).
- [Fact] Hay precios diferenciados por tokens de entrada, salida y *cached input* (cuando aplica), lo que abre palancas directas de ahorro vía caching/dedupe.[^4]
- [Inference] La forma más rápida de bajar costo sin romper calidad es: (1) límites por tenant y por flujo, (2) dedupe/caching de prompts y respuestas, (3) routing de modelos por complejidad, (4) control de longitud de salida.
- [Fact] “FOCUS reduce complejidad” para que FinOps impulse decisiones data-driven y maximice valor del gasto tecnológico.[^2]
- [Inference] Si no instrumentas observabilidad de tokens (por tenant/feature/modelo), no puedes negociar márgenes internos ni evitar “runaway costs” en features tipo copiloto.
- [Fact] Existen patrones de *semantic caching* (embeddings + vector DB) para reutilizar respuestas ante consultas similares, evitando llamadas repetidas al LLM.[^5]
- [Inference] En CRM enterprise, el mayor ROI viene de optimizar los flujos repetitivos (resúmenes, emails, logging, clasificación) antes que los “casos wow”.
- [Fact] Un enfoque de “cost management for LLM operations” recomienda gobernanza + medición + control continuo (prácticas de LLMOps orientadas a costo).[^6]

***

## Definitions and why it matters

**Facts**

- [Fact] FinOps es una práctica de gestión financiera orientada a maximizar valor del gasto tecnológico; aplicada a LLM se enfoca en controlar y optimizar consumo de API/modelos.[^1]
- [Fact] FOCUS es una especificación abierta (FinOps Foundation) para normalizar datasets de costo/uso y soportar capacidades como cost allocation/chargeback, budgeting y forecasting.[^3][^2]
- [Fact] En pricing de APIs de LLM suele haber cobro por tokens de entrada y de salida, y puede existir tarifa reducida para *cached input*.[^4]

**Inferences**

- [Inference] “Optimización de tokens” no es solo recortar texto: es diseñar un sistema que reduzca llamadas y/o mueva llamadas a modelos más baratos manteniendo calidad objetivo.
- [Inference] “Cost accounting” para LLM en B2B multi-tenant te permite: margen por cliente/tenant, pricing interno por feature, y políticas de riesgo (evitar abuso/uso no intencional).

***

## Principles and best practices (con citas + fecha)

**(A) Cost accounting (FOCUS mindset)**

- [Fact] FOCUS define un esquema común para datos de billing/usage con el fin de habilitar cost allocation/chargeback y forecasting de forma vendor-agnostic (FOCUS spec v1.2, 2025-05).[^3]
- [Inference] Modela cada request como “línea de costo” con dimensiones: `tenant_id`, `app`, `feature`, `model`, `prompt_version`, `environment`, `cache_status`, `tokens_in`, `tokens_out`, `latency_ms`, `result_type`.

**(B) Límites por tenant (guardrails comerciales)**

- [Fact] FinOps para LLM busca extraer valor controlando gasto; los límites son un mecanismo práctico de control en operación. (ThoughtSpot, 2025-12-01).[^1]
- [Inference] Aplica límites “duros” (bloqueo) y “suaves” (degradación a modelo más barato / menor longitud / modo extractivo) por tenant, por usuario y por feature; esto evita que una sola cuenta te consuma el presupuesto.

**(C) Caching: exacto, por prefijo y semántico**

- [Fact] La existencia de tarifas de *cached input* implica que reutilizar entradas repetidas puede reducir costo de forma material (OpenAI pricing, 2025-10-31).[^4]
- [Fact] En prompt caching por prefijo (concepto común en inferencia), los tokens de un prefijo idéntico pueden recibir descuento y menor latencia (ejemplo documentado por Groq, 2025-04-28).[^7]
- [Fact] En *semantic caching*, se guarda embedding + respuesta y se responde si la consulta nueva es suficientemente similar (patrón descrito con umbrales de similitud).[^5]
- [Inference] Estrategia recomendada:
    - Cache exacto para prompts templados y outputs deterministas (resúmenes estándar, clasificaciones con esquema fijo).
    - Cache por prefijo para system prompts largos y estáticos (políticas, instrucciones base, contexto fijo).
    - Cache semántico para FAQs internas (políticas comerciales, “cómo hago X en CRM”, definiciones) con TTL y auditoría.

**(D) Prompt dedupe (eliminar redundancia estructural)**

- [Fact] Patrones de reducción de costo en LLMOps incluyen eliminar redundancias y gestionar prompts repetidos como parte de cost management.[^6]
- [Inference] Implementa “prompt fingerprinting”: hash del *prompt canonicalizado* (sin timestamps/IDs variables), y dedupe antes de llamar al modelo; esto maximiza cache-hit y evita pagar por reintentos duplicados.

**(E) Selección de modelo (routing por complejidad)**

- [Fact] El pricing por modelo difiere y el costo por token es un factor directo; por eso el costo se gestiona eligiendo el modelo adecuado al trabajo.[^4]
- [Inference] Define un router con reglas simples:
    - “Barato” para tareas extractivas/estructuradas (clasificar, validar, resumir a 3 bullets).
    - “Caro” solo para razonamiento multi-hop, redacción crítica o cuando el evaluador detecte baja confianza.
    - “Fallback” cuando hay ambigüedad: pedir aclaración (menos tokens que alucinar).

**(F) Evaluación costo/calidad (gobernanza de trade-offs)**

- [Fact] FinOps promueve decisiones data-driven para maximizar valor del gasto; eso implica medir valor vs costo, no solo costo.[^2]
- [Inference] Usa un “scorecard” por feature: costo por 1.000 ejecuciones, tasa de aceptación por usuario, tiempo ahorrado, y tasa de escalamiento a humano; congela cambios de prompt/modelo si sube costo y baja calidad.

**(G) Observabilidad de tokens (sin esto no hay FinOps)**

- [Fact] Cost management en LLM operations se apoya en instrumentación/telemetría para entender y controlar gasto de inferencia.[^6]
- [Inference] Log mínimo por request (y por tenant): tokens_in/out, cache-hit, modelo, latencia, error type, tamaño de contexto, versión de prompt, tamaño de salida; construye alertas de “token spikes” por feature.

***

## Examples (aplicado a CRM enterprise)

**Caso 1: Copiloto de emails para equipo comercial (multi-tenant)**

- [Fact] La reutilización de entradas (cached input) puede abaratar prompts repetidos cuando hay plantillas/estructuras constantes.[^4]
- [Inference] Diseño: system prompt fijo (cache por prefijo) + variables pequeñas (cliente, deal stage) + límite de salida (máx. 120–180 palabras); si el tenant excede cuota mensual, degradar a “plantilla + variables” sin LLM.

**Caso 2: Resumen de “última interacción” en ficha de cuenta**

- [Fact] Semantic caching evita llamadas al LLM cuando la consulta es similar y ya existe una respuesta almacenada.[^5]
- [Inference] Guarda resúmenes por `account_id + timeframe` con TTL (p.ej., 24h) y refresco solo cuando cambie el timeline; esto baja costo y mejora latencia percibida por el vendedor.

**Caso 3: Clasificación de tickets/actividades para reporting**

- [Fact] FinOps/FOCUS habilita cost allocation/chargeback: puedes asignar costo por feature y por unidad organizativa si capturas dimensiones consistentes.[^3]
- [Inference] Corre clasificación en batch (no on-click) y con modelo barato; solo escalas a modelo caro si la confianza < umbral o si el registro es “VIP tenant”.

***

## Metrics / success signals

**Facts**

- [Fact] FOCUS está orientado a habilitar budgeting/forecasting y cost allocation con datos consistentes.[^3]
- [Fact] Existe diferenciación de costo por tipo de tokens (input/output/cached input) que impacta el costo unitario por request.[^4]

**Inferences (métricas accionables)**

- [Inference] Unit economics: `costo por conversación`, `costo por 1.000 acciones CRM`, `costo por tenant/mes`, `costo por feature`.
- [Inference] Eficiencia: `tokens_in median`, `tokens_out median`, `p95 tokens_out`, `% cache-hit (exact/prefix/semantic)`, `ratio tokens_out/tokens_in`.
- [Inference] Calidad: `acceptance rate`, `edit distance` (cuánto reescribe el usuario), `escalation rate a humano`, `CSAT interno por feature`.
- [Inference] Riesgo: `% prompts con PII`, `bloqueos por policy`, `top tenants por consumo`, “runaway sessions” detectadas por anomalías.

***

## Operational checklist

**Facts**

- [Fact] FOCUS proporciona un marco/esquema para que datasets de costo/uso soporten asignación y reporting consistente (FOCUS v1.2, 2025-05).[^3]
- [Fact] El caching (incluyendo cached input pricing cuando aplique) es una palanca directa para bajar costo en prompts repetidos.[^4]

**Inferences (pasos de implementación)**

- [Inference] 1) Instrumenta logging por request con dimensiones (tenant/feature/model/prompt_version/tokens/cache).
- [Inference] 2) Define presupuesto y cuotas por tenant: mensual + límites diarios; crea “kill switch” por feature.
- [Inference] 3) Implementa dedupe: canonicaliza prompt, calcula hash, consulta cache exacto antes de llamar al LLM.
- [Inference] 4) Añade cache por prefijo para instrucciones base largas y repetidas.
- [Inference] 5) Implementa semantic cache para FAQs/consultas repetibles; define umbral de similitud, TTL, y lista de exclusiones (cosas sensibles o volátiles).
- [Inference] 6) Router de modelos: barato por defecto; caro solo con criterios (baja confianza, alta complejidad, alto valor).
- [Inference] 7) Control de salida: límites de longitud + formatos estructurados (JSON) cuando aplique.
- [Inference] 8) Eval costo/calidad semanal por feature; si sube costo sin subir calidad, rollback de prompt/modelo.

***

## Anti-patterns

**Facts**

- [Fact] Sin datos de costo/uso consistentes, capacidades como chargeback y cost allocation se vuelven difíciles; FOCUS existe precisamente para reducir esa fricción.[^2][^3]
- [Fact] Semantic caching mal calibrado (umbral de similitud inadecuado) puede devolver respuestas incorrectas; es un riesgo reportado en experiencias de implementación.[^5]

**Inferences**

- [Inference] “Un solo modelo caro para todo” (sin routing): quema margen y hace imposible escalar B2B.
- [Inference] No separar entornos (dev/staging/prod) en métricas: confundes experimentación con consumo real.
- [Inference] Cachear respuestas con contenido sensible sin políticas: puedes filtrar información cross-tenant.
- [Inference] Prompts gigantes “por si acaso”: inflan tokens_in y reducen cache-hit por variabilidad.

***

## Diagnostic questions

**Facts**

- [Fact] FinOps para LLM busca maximizar valor con decisiones data-driven; sin medición por unidad de valor, no hay optimización real.[^2]

**Inferences (preguntas que destraban)**

- [Inference] ¿Cuál es el “unit of value” por feature CRM (email generado, resumen, ticket clasificado) y cuánto cuesta hoy?
- [Inference] ¿Qué % del consumo viene del top 5 tenants y qué guardrails existen?
- [Inference] ¿Qué % de requests son repetidos (exactos o casi) y cuál es el cache-hit actual?
- [Inference] ¿Qué features usan modelo caro y por qué; existe un criterio objetivo de escalamiento?
- [Inference] ¿Puedes hacer chargeback interno por tenant/BU con tus dimensiones actuales?
- [Inference] ¿Qué prompts incluyen datos sensibles y cómo previenes leaks (incluyendo cache)?

***

## Sources (o referencia a SOURCES.md)

- FinOps Foundation — “What is FOCUS?” (2025-11-30).[^2]
- FinOps Foundation — FOCUS Specification page (2025-11-30).[^8]
- FinOps Foundation — **FOCUS spec v1.2 (PDF)** (2025-05, según ruta del archivo).[^3]
- OpenAI — API Pricing (2025-10-31).[^4]
- ThoughtSpot — “FinOps for Large Language Models” (2025-12-01).[^1]
- OneUptime — “How to Build Cost Management for LLM Operations” (2026-01-29).[^6]
- Experiencia comunitaria sobre semantic caching (umbral/efectos) — Reddit r/LangChain (2025-12-30).[^5]
- Groq — Prompt caching / descuento por prefijo idéntico (2025-04-28).[^7]

**Entradas para añadir a `SOURCES.md` (sin duplicados)**

- FinOps Foundation — FOCUS overview: https://focus.finops.org/what-is-focus/  (accedido 2026-02-17)[^2]
- FinOps Foundation — FOCUS spec PDF v1.2: https://focus.finops.org/wp-content/uploads/2025/05/FOCUS-spec-v1_2.pdf (accedido 2026-02-17)[^3]
- OpenAI — API pricing: https://openai.com/api/pricing/ (accedido 2026-02-17)[^4]
- OneUptime — LLMOps cost management: https://oneuptime.com/blog/post/2026-01-30-llmops-cost-management/view (accedido 2026-02-17)[^6]

***

## Key takeaways for PM practice

- Diseña FinOps de LLM como *unit economics por feature y por tenant*, no como “control de factura” genérico.
- Instrumentación de tokens + dimensiones (tenant/feature/modelo/prompt_version/cache) es el prerrequisito para cualquier optimización seria.
- Caching y dedupe suelen dar el ROI más rápido; routing de modelos sostiene el margen a escala.
- Evalúa costo/calidad con scorecards por feature y aplica guardrails (degradación/kill switch) para evitar runaway costs.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^9]</span>

<div align="center">⁂</div>

[^1]: https://www.thoughtspot.com/data-trends/ai/finops-for-llm

[^2]: https://focus.finops.org/what-is-focus/

[^3]: https://focus.finops.org/wp-content/uploads/2025/05/FOCUS-spec-v1_2.pdf

[^4]: https://openai.com/api/pricing/

[^5]: https://www.reddit.com/r/LangChain/comments/1pzno6m/semantic_caching_cut_our_llm_costs_by_almost_50/

[^6]: https://oneuptime.com/blog/post/2026-01-30-llmops-cost-management/view

[^7]: https://groq.com/blog/gpt-oss-improvements-prompt-caching-and-lower-pricing

[^8]: https://focus.finops.org/focus-specification/

[^9]: pasted-text.txt

[^10]: https://www.reddit.com/r/LLMDevs/comments/1qnuyyj/reducing_token_costs_on_autonomous_llm_agents_how/

[^11]: https://konghq.com/solutions/ai-cost-optimization-management

[^12]: https://www.glukhov.org/es/post/2025/11/cost-effective-llm-applications/

[^13]: https://intuitionlabs.ai/articles/chatgpt-api-pricing-2026-token-costs-limits

[^14]: https://www.linkedin.com/pulse/saving-tokens-reducing-cost-practical-hybrid-llm-strategy-devkota-s6mge

[^15]: https://beacon.paloaltonetworks.com/student/award/n5UonvFSyeihtXK2c5gFUnBG

[^16]: https://www.linkedin.com/pulse/cost-effective-llm-systems-guidelines-deepmetis-v4ate

