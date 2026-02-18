<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_01_CRM_IA_Enterprise – IA en CRMs web enterprise (2024–2026)

Este documento resume patrones 2024–2026 para diseñar CRMs web con IA (Salesforce/HubSpot/Zendesk) con foco en navegación, búsqueda, taxonomía y escalabilidad multi‑rol en entornos enterprise B2B.

***

## Executive summary (10–15 líneas)

#### Facts

- Los grandes CRMs (Salesforce, HubSpot, Zendesk) están moviendo la experiencia desde “pantallas de objeto” hacia copilots conversacionales y agentes especializados que ejecutan flujos multi‑objeto a partir de lenguaje natural.[^1][^2][^3]
- Salesforce Einstein Copilot se incrusta en la UI estándar y sugiere acciones contextuales como “Show top opportunities” en cuentas y oportunidades, además de resumir registros y redactar emails.[^1]
- Einstein Copilot se apoya en Data Cloud y en herramientas como Copilot Builder, Prompt Builder y Model Builder para personalizar prompts y conectar LLMs con datos de CRM de forma segura.[^4][^3]
- HubSpot introdujo Breeze Copilot y una familia de agentes (Prospecting, Customer, Content, Social) que automatizan prospección, soporte y contenido, integrados con el Smart CRM.[^2][^5]
- HubSpot está ampliando su Object Library con nuevos tipos de objeto y plantillas por industria, facilitando modelos de datos más ricos sin necesidad de desarrollos avanzados.[^2]
- Zendesk AI ofrece Intelligent Triage que clasifica y prioriza tickets por intención, sentimiento e idioma, y sugiere macros inteligentes para los agentes.[^6][^7]
- Varios vendors resaltan que la calidad y estandarización de datos es condición crítica para que la IA (especialmente generativa) dé respuestas fiables.[^8][^4]
- Las soluciones modernas de búsqueda en CRMs están evolucionando de full‑text básico a search semántico con contexto (ejemplo: integraciones tipo Dashworks sobre HubSpot).[^9]
- Hay una tendencia a una “capa de inteligencia compartida” que cruza marketing, ventas, servicio y RevOps, orquestando automatizaciones y next‑best‑actions desde IA.[^5]


#### Inferences

- La arquitectura ganadora combina navegación clásica por objetos para usuarios expertos + capas de IA orientadas a tareas (copilots, agentes, asistentes en flujo) para acelerar el trabajo diario.
- En enterprise, el mayor riesgo no es “falta de IA” sino IA sin governance: scores opacos, prompts sin controles y acciones automatizadas sin trazabilidad.
- El diseño multi‑rol efectivo se logra cuando cada rol tiene vistas y copilots específicos, pero todos consumen el mismo modelo de datos y taxonomía.
- Para entornos con fricción (LATAM, B2B complejo) la prioridad práctica es: 1) búsqueda que encuentra, 2) acciones guiadas simples, 3) automatización de tareas repetitivas, y solo después “magia” generativa.
- El KPI clave no es “número de features de IA”, sino reducción de pasos operativos y mejora en tasa de uso efectivo del CRM por parte de los equipos comerciales y de soporte.

***

## Definitions and why it matters

#### Facts

- CRM con IA: sistema CRM que usa modelos de IA para scoring, automatización de workflows, personalización a escala y recomendaciones de next‑best‑action, más allá de simples reglas.[^10][^11]
- Copilot/Assistant en CRM: interfaz conversacional integrada que entiende lenguaje natural, ejecuta acciones (consultar, actualizar, crear registros) y genera contenido (mails, resúmenes, planes) sobre datos del CRM.[^3][^4][^1]
- Salesforce Einstein Copilot usa un LLM conectado a Salesforce Data Cloud para responder y ejecutar acciones dentro del flujo de trabajo del usuario, con una Trust Layer que controla seguridad y uso de datos.[^8][^4][^1]
- HubSpot Breeze Copilot y sus agentes se integran con el Smart CRM para recomendar leads, automatizar outreach, gestionar contenido y enrutar casos de soporte con datos enriquecidos y scoring avanzado.[^11][^5][^2]
- Zendesk Intelligent Triage clasifica, etiqueta y enruta tickets automáticamente según intención y sentimiento, reduciendo esfuerzo manual de los agentes en el front line de soporte.[^7][^6]


#### Inferences

- “IA en CRM” hoy significa menos navegar menús y más pedir “lo que quiero lograr” y que el sistema arme el camino (tareas, datos y contenido) sobre la marcha.
- Para un CRM enterprise, la IA deja de ser “feature linda para demos” y se vuelve infraestructura que impacta: velocidad de respuesta, calidad de pipeline, priorización de riesgos y capacidad de escalar equipos sin duplicar headcount.
- Sin una buena taxonomía de objetos y campos, los copilots y búsquedas semánticas terminan volviéndose poco confiables y erosionan la adopción interna.

***

## Principles and best practices (con citas por sección + fecha)

### 1. Navegación: objetos vs tareas vs copilots

#### Facts

- El patrón histórico de CRMs (Salesforce, HubSpot, Zendesk Sell) se basa en navegación por objetos: cuentas, contactos, deals, tickets, con vistas tipo lista y kanban.[^10][^2]
- Salesforce está añadiendo Einstein Copilot directamente en la página de cuenta u oportunidad, ofreciendo acciones como “Show top opportunities” o “Show recent opportunities” al abrir un registro.[^1]
- Einstein Copilot puede orquestar planes de acción multi‑paso (multi‑step action plans) que combinan varias acciones de CRM en una sola recomendación, acercándose a una navegación por tareas.[^3]
- HubSpot Breeze Copilot introduce agentes orientados a tareas (prospecting, customer support, content) que operan sobre múltiples objetos y canales en un solo flujo.[^5][^2]


#### Inferences

- Mantener navegación por objetos es clave para usuarios avanzados (sales ops, administradores, analistas) que necesitan control fino; la IA no debe romper estos flujos, sino superponer atajos.
- La navegación por tareas funciona mejor cuando las tareas están muy claras (“priorizar leads de hoy”, “preparar resumen de cuenta antes de llamada”) y el sistema puede resolver 80% del flujo sin que el usuario cambie de pantalla.
- Buen patrón: vista por objeto bien diseñada + panel lateral de copilot + atajos de acciones frecuentes; mal patrón: copilot en una pestaña aparte que obliga al usuario a re‑describir contexto manualmente.


#### Tabla: tradeoffs navegación por objetos vs por tareas (AI‑enabled)

| Dimensión | Navegación por objetos (clásica) | Navegación por tareas / copilot (moderna) |
| :-- | :-- | :-- |
| Mental model | “¿Qué hay en esta cuenta/oportunidad/ticket?” | “¿Qué tengo que hacer ahora / con este cliente / con este pipeline?” |
| Fortaleza principal | Control, trazabilidad, reporting preciso | Velocidad operativa, reducción de clicks, mejor experiencia para usuarios menos expertos |
| Riesgo principal | Usuarios se pierden entre listas y filtros, navegación lenta | Opacidad de lógica, dependencia de prompts y calidad de datos |
| Patrones en vendors | List views, kanban, sub‑tabs, related lists (Salesforce, HubSpot, Zendesk) [^10][^2] | Copilots contextuales y agentes que recomiendan acciones y planes multi‑paso.[^1][^2][^3][^5] |

*(primera columna Inferences, tercera y cuarta combinan Facts + Inferences)*

***

### 2. Búsqueda y descubrimiento

#### Facts

- Muchos CRMs nativos tienen búsqueda por texto limitado (dependiente de nombres/IDs y filtros) y aparecen integraciones que añaden búsqueda semántica sobre HubSpot para encontrar contactos, deals, emails y notas por contexto.[^9]
- Estas integraciones de búsqueda semántica se conectan vía API a HubSpot y permiten preguntar en lenguaje natural (“¿qué clientes preguntaron por X la semana pasada?”) retornando registros relevantes sin recordar campos específicos.[^9]
- Zendesk Intelligent Triage usa IA para detectar intención y lenguaje de los tickets y asignar tags útiles, lo que mejora la capacidad de filtrado y búsqueda posterior por categorías reales de problema.[^6][^7]


#### Inferences

- En 2024–2026 el estándar de UX de búsqueda en CRM se parece más a “Google interno” + filtros de negocio que a un simple buscador de texto con operadores.
- La combinación ideal: 1) barra de búsqueda global con semántica, 2) filtros por campos clave de negocio, 3) shortcuts en la UI para guardar búsquedas frecuentes como vistas compartidas por rol.
- Medir “search success” (veces que la primera búsqueda lleva a la acción correcta) es tan importante como medir performance de formularios o pipelines.

***

### 3. Taxonomía de datos y objetos

#### Facts

- Artículos sobre Einstein Copilot remarcan que la calidad y estandarización de datos condicionan directamente la precisión de respuestas y recomendaciones de IA.[^4]
- En el ecosistema CRM se observa una carrera por combinar Data Clouds (Salesforce Data Cloud, Snowflake, Databricks) con la capa de IA para ofrecer vistas unificadas de cliente.[^8]
- HubSpot está ampliando su librería de objetos con tipos como citas, propiedades, cursos y servicios, más plantillas por industria para adaptar el modelo de datos sin necesidad de desarrollo complejo.[^2]
- Guías de CRM con IA destacan que diferentes industrias requieren capacidades específicas: lead scoring, predicción de churn, bots de soporte, etc., lo que se traduce en diferentes taxonomías de objetos y eventos.[^10]


#### Inferences

- Un modelo de datos explícito (objetos y relaciones claros) vale más que 20 features de IA: sin él, los copilots terminan “inventando estructura” y generan desconfianza.
- Buen patrón: objetos core estandarizados (Account/Company, Contact, Deal, Ticket) + objetos secundarios por industria (ej. “Reserva”, “Ruta”, “Contratos”) con naming consistente y properties normalizadas.
- Governance de campos (quién crea, quién aprueba, cómo se documenta) pasa a ser una responsabilidad de producto, no solo de IT, porque impacta la calidad de la IA.

***

### 4. Escalabilidad multi‑rol y multi‑región

#### Facts

- HubSpot Breeze y sus agentes están diseñados como una capa de inteligencia compartida entre marketing, ventas, servicio y RevOps, rompiendo silos de dashboards y métricas por equipo.[^5]
- Estos agentes pueden: recomendar audiencias en marketing basándose en datos de ventas y soporte, predecir pipeline incorporando engagement, y alertar a account managers sobre issues detectados en tickets de servicio.[^5]
- Zendesk AI ofrece precios por agente en sus planes profesionales, buscando que todos los agentes tengan acceso a capacidades de IA a medida que la organización escala.[^7]


#### Inferences

- En enterprise, diseñar solo para “el vendedor” es un error: el CRM con IA debe resolver para SDRs, account executives, customer success, soporte, marketing y management, todos sobre la misma base de datos.
- Escalabilidad multi‑rol implica: vistas y copilots distintos por rol, pero objetos y definiciones de estados globales coordinados (un solo estado de “Activo/Inactivo”, un solo “tipo de cliente”, etc.).
- Multi‑región añade capas de permisos, idiomas y reglas locales; la IA debe respetar esta segmentación (ej. copilots que responden en el idioma correcto y solo con datos de la región autorizada).

***

### 5. Data readiness, privacidad y governance

#### Facts

- Consultoras especializadas en Salesforce señalan que antes de desplegar Einstein Copilot, es clave limpiar fuentes, deduplicar y estandarizar datos, aplicando políticas de calidad robustas para evitar inconsistencias.[^4]
- Expertos de CRM mencionan que la madurez en uso de datos y la elección adecuada de opciones de IA (propias, del vendor, o de terceros) son fundamentales para implementar IA de forma efectiva en el ecosistema CRM.[^8]


#### Inferences

- Línea base: sin definición clara de qué datos puede consumir la IA (fields, objetos, regiones), se abre un riesgo de compliance y exposición de información sensible.
- Buen patrón: catálogo de datos + clasificación (público interno, restringido, confidencial) y mapeo explícito a qué copilots/agents pueden ver qué.
- Para CRMs en mercados regulados o de alto riesgo, conviene empezar con IA “observada”: recomendaciones que requieren confirmación humana, logs detallados y revisión periódica de calidad.

***

## Examples (aplicado a CRM enterprise)

### 1. Salesforce Einstein Copilot en una organización global

#### Facts

- Einstein Copilot se presenta como asistente conversacional que ayuda a resumir registros, redactar emails y ejecutar tareas clave directamente dentro del CRM.[^1][^4]
- Al abrir cuentas y oportunidades, Copilot muestra una pantalla de bienvenida con acciones recomendadas basadas en el contexto de la página, como ver oportunidades top o recientes.[^1]
- Copilot puede combinar acciones en planes multi‑paso de estilo next‑best‑action, permitiendo al usuario aceptar o ajustar el plan.[^3]


#### Inferences

- En un CRM enterprise, un buen diseño sería:
    - Página de cuenta con layout clásico (datos clave, oportunidades, casos) + panel lateral de Copilot.
    - Prompts preconfigurados por rol: “preparar briefing de cuenta para llamada”, “identificar riesgos de churn”, “sugerir próximos pasos para todas las oportunidades abiertas de este cliente”.
- El equipo de producto debe decidir qué acciones están permitidas para ejecución automática y cuáles solo como recomendación, especialmente en objetos críticos (precio, crédito, descuentos).

***

### 2. HubSpot Smart CRM + Breeze Agents

#### Facts

- En Inbound 2024, HubSpot anunció Breeze Copilot, diseñado para automatizar actividades rutinarias y simplificar workflows complejos integrados con datos del CRM.[^2]
- Entre sus agentes destacan: Prospecting Agent (identifica leads, personaliza outreach y automatiza comunicación), Social Media Agent, Content Agent y Customer Agent para soporte.[^2]
- HubSpot está reforzando capacidades de enriquecimiento automático de datos, identificación de intención de compra y lead scoring AI con criterios personalizables y ponderaciones avanzadas.[^11][^2]


#### Inferences

- Un uso enterprise típico:
    - Marketing usa Breeze para sugerir audiencias y contenidos por segmento.
    - Ventas recibe un pipeline ya priorizado cada mañana con Prospecting Agent, más plantillas de outreach generadas.
    - CS y soporte operan sobre Customer Agent que enruta y pre‑responde consultas recurrentes, alineado con tickets y deals asociados.
- Para evitar caos, RevOps debe definir qué campos son “fuente de verdad” para scoring y qué acciones automáticas están permitidas (por ejemplo, creación automática de tasks vs cambios de owner).

***

### 3. Zendesk AI + Intelligent Triage

#### Facts

- Zendesk Intelligent Triage analiza intención, sentimiento y lenguaje de los tickets para etiquetarlos y enrutar a la cola o equipo adecuado sin intervención manual.[^6][^7]
- Puede responder automáticamente a preguntas frecuentes (“¿cómo cancelo mi suscripción?”) con enlaces relevantes, dejando a los agentes tiempo para casos complejos.[^7]
- Zendesk AI sugiere macros inteligentes para que los administradores optimicen workflows y para que los agentes apliquen respuestas estándar de forma más rápida.[^6]


#### Inferences

- En un CRM/Service Desk enterprise, diseño recomendado:
    - Entrada de tickets unificada (mail, chat, formulario) → Intelligent Triage etiqueta y enruta por tipo de caso, idioma y prioridad.
    - Los agentes ven sugerencias de macro + contexto clave del cliente (segmento, valor, SLA) en el mismo panel.
- Para ventas B2B, este patrón es trasladable a “oportunidades de recuperación” o “tickets de riesgo” que disparan alertas automáticas al account manager.

***

## Metrics / success signals

#### Facts

- Zendesk posiciona Intelligent Triage como palanca para manejar grandes volúmenes de tickets y reducir tiempos de resolución al enrutar y priorizar automáticamente.[^6]
- Salesforce y partners de consultoría enfatizan que mejorar la calidad de datos antes de usar Copilot incrementa la precisión y confiabilidad de respuestas y predicciones de IA.[^4]
- HubSpot resalta métricas de lead scoring mejorado, engagement y conversión como beneficios clave de su IA aplicada a marketing y ventas.[^11][^2]


#### Inferences

Métricas recomendadas para medir éxito de IA en CRM:

- Adopción de IA
    - % usuarios activos que usan copilots/agents al menos X veces por semana.
    - % acciones críticas (creación de tasks, emails, notas) iniciadas desde IA vs manuales.
- Eficiencia operativa
    - Reducción de tiempo medio para: crear oportunidad, actualizar cuenta, resolver ticket.
    - Reducción de “pantallas promedio” por flujo crítico (antes/después de IA).
- Calidad de resultados
    - Tasa de aceptación/edición de sugerencias de IA (ej. emails generados que se envían casi sin cambios).
    - Precisión percibida de respuestas de IA (encuestas internas rápidas tipo thumbs‑up/down).
- Impacto comercial
    - Mejora en conversión por etapa del pipeline para leads/oportunidades tocados por IA vs no tocados.
    - Reducción de tickets mal enroutados o re‑asignados.

***

## Operational checklist

#### Facts

- Implementadores de Salesforce recomiendan evaluar calidad de datos, consolidar fuentes y establecer políticas de calidad antes de activar Einstein Copilot para evitar respuestas erróneas.[^4]
- Expertos en CRM señalan que hay que alinear la madurez de datos y capacidades de IA con el roadmap tecnológico, incluyendo decisiones de integración con Data Clouds y herramientas externas.[^8]


#### Inferences

Checklist para PM/PO de CRM enterprise:

**1. Datos y modelo**

- [ ] Inventariar objetos y campos core (Accounts/Companies, Contacts, Deals, Tickets, productos, etc.).
- [ ] Depurar: duplicados, valores basura, estados inconsistentes.
- [ ] Definir taxonomía de estados y tipos (ej. tipos de cliente, tipos de casos, motivos de pérdida).

**2. Casos de uso de IA (priorizados)**

- [ ] Top 3 casos por rol (ventas, CS, soporte, marketing) donde IA reduce mayor fricción.
- [ ] Definir qué es “éxito” por caso (ej. -30% tiempo de pre‑llamada, -20% tiempo de clasificación de tickets).

**3. Navegación y UX**

- [ ] Mapear flujos actuales por objetos (qué pantallas se usan de verdad).
- [ ] Diseñar prompts/acciones predefinidas por contexto de página (ej. acciones sugeridas en cuenta, oportunidad, ticket).
- [ ] Asegurar que copilot pueda leer contexto de la página sin que el usuario lo repita.

**4. Governance y seguridad**

- [ ] Catálogo de datos: qué puede consumir la IA, qué no.
- [ ] Reglas de permisos por rol/region (visibilidad de campos y acciones).
- [ ] Logs y trazabilidad: registrar qué sugirió la IA y qué se ejecutó.

**5. Medición y mejora continua**

- [ ] Definir métricas base (antes de IA) y objetivos.
- [ ] Revisar mensualmente: adopción, errores relevantes, feedback cualitativo.
- [ ] Ajustar prompts, campos, objetos y automatizaciones en base a datos reales, no solo feedback anecdótico.

***

## Anti-patterns

#### Facts

- Casos documentados señalan que una mala calidad de datos genera respuestas de IA imprecisas y reduce confianza en herramientas como Einstein Copilot.[^4]
- Artículos sobre IA en CRM advierten que elegir herramientas que no se integran bien con el stack existente crea más problemas que beneficios.[^10][^8]


#### Inferences

Anti‑patrones típicos en IA para CRM:

- IA como pestaña aislada
    - Copilot que vive en un chat aparte sin contexto de la página ni conexión directa con acciones de CRM.
- UX centrada en “prompt libre”
    - Confiar en que el usuario “sabrá qué pedir” en vez de ofrecer acciones guiadas y prompts curados por rol y contexto.
- Modelo de datos caótico
    - Campos duplicados, naming inconsistente (“customer_type”, “tipo_cliente”, “segmento”) que confunden a la IA y a los usuarios.
- Automatización sin frenos
    - IA que crea/edita registros críticos sin revisión humana ni logs claros (descuentos, condiciones comerciales, SLA).
- Métricas de vanidad
    - Celebrar “número de prompts usados” sin mirar impacto en tiempos, conversión o satisfacción de usuarios internos.
- Ignorar roles y regiones
    - Asistentes genéricos que recomiendan acciones que no aplican al país/mercado/rol del usuario (ej. plantillas de email no válidas legalmente en ciertas jurisdicciones).

***

## Diagnostic questions

#### Facts

- Guías sobre IA en ecosistema CRM recomiendan evaluar madurez de datos, integraciones y casos de uso antes de invertir fuerte en features avanzados de IA.[^8]


#### Inferences

Preguntas para diagnosticar el estado actual de un CRM enterprise respecto a IA:

**Datos y modelo**

- ¿Qué objetos y campos son realmente usados (vs. “ruido heredado”)?
- ¿Qué tan fácil es hoy responder manualmente preguntas típicas de negocio sin IA?

**UX y navegación**

- ¿Cuántos clicks y pantallas necesita un vendedor para: preparar una llamada, actualizar un deal, levantar un caso?
- ¿Los usuarios usan la búsqueda o evitan el CRM y preguntan por chat/WhatsApp al equipo de soporte interno?

**IA actual**

- ¿Qué features de IA del vendor están activas hoy (scoring, recomendaciones, copilots, triage) y quién las usa realmente?
- ¿Qué decisiones de negocio hoy dependen de scores o recomendaciones de IA? ¿Están documentadas?

**Governance**

- ¿Quién es “dueño” del modelo de datos y de las reglas de IA? (persona/rol, no área difusa).
- ¿Existe un proceso para revisar errores graves de IA y ajustar prompts, reglas o datos?

**Escalabilidad multi‑rol / multi‑región**

- ¿Todos los roles clave tienen beneficios claros de IA, o solo uno (ej. marketing) está capturando valor?
- ¿Los contenidos/respuestas generados por IA respetan idioma, regulaciones y matices de cada mercado?

***

## Sources (para SOURCES.md)

#### Facts

- Salesforce – Einstein Copilot release notes y documentación de ayuda describen la integración del asistente conversacional en la UI, acciones contextuales y la Trust Layer.[^1]
- Ascendix – Guías de implementación de Einstein Copilot enfatizan preparación de datos, herramientas de construcción de prompts y conexión con Data Cloud.[^4]
- SalesforceBen – Guía definitiva de Einstein GPT detalla capacidades de Copilot y sus planes de acción multi‑paso y next‑best‑action.[^3]
- HubSpot – Resumen de anuncios de Inbound 2024 sobre Breeze Copilot, agentes y Object Library.[^2]
- Fast Slow Motion – Análisis sobre el futuro de HubSpot AI y Breeze Agents como capa de inteligencia compartida marketing‑ventas‑servicio‑RevOps.[^5]
- HubSpot (LATAM) – Material sobre migración de Excel a CRM con IA, scoring predictivo y personalización a escala.[^11]
- Sparkle – Comparativa de CRMs con IA y funcionalidades clave por industria y nivel enterprise.[^10]
- Artículos sobre IA para negocio y búsqueda semántica en HubSpot (ej. Dashworks).[^9]
- RedK / otros partners Zendesk – Contenido sobre Zendesk AI e Intelligent Triage (clasificación y routing de tickets, macros inteligentes, pricing por agente).[^7][^6]
- Solvis Consulting – Análisis del ecosistema CRM + IA y el rol de Data Clouds (Salesforce, Snowflake, Databricks) y madurez de datos.[^8]

***

## Key takeaways for PM practice

#### Inferences

- Diseñar “IA sobre CRM” empieza por taxonomía y datos, no por el copilot: limpia modelo, luego habilita features.
- Mantén navegación por objetos robusta, pero coloca copilots y agentes directamente en el flujo de trabajo de cada rol.
- Prioriza 3–5 tareas críticas por rol donde IA reduzca pasos y errores; evita desplegar un asistente genérico sin foco.
- Mide éxito por impacto en tiempo, conversión y satisfacción interna, no por cantidad de prompts o features activadas.
- Define desde el principio ownership de datos y de IA (quién decide campos, prompts, reglas) y revisa errores graves regularmente.
- Para mercados con fricción, pon primero: búsqueda que funcione, triage inteligente y automatización de tareas repetitivas; la generación de texto “bonito” viene después.
<span style="display:none">[^12][^13][^14][^15][^16]</span>

<div align="center">⁂</div>

[^1]: https://help.salesforce.com/s/articleView?id=release-notes.rn_einstein_copilot.htm\&language=en_US\&release=248\&type=5

[^2]: https://blog.glaremarketing.co/hubspots-inbound-2024-ai-features-you-need-to-know

[^3]: https://www.salesforceben.com/the-definitive-guide-to-einstein-gpt-salesforce-ai/

[^4]: https://ascendix.com/blog/salesforce-einstein-copilot/

[^5]: https://www.fastslowmotion.com/the-future-of-hubspot-ai/

[^6]: https://www.redk.net/blog/how-to-build-scalable-customer-service-with-zendesk-ai

[^7]: https://www.eesel.ai/blog/zendesk-intelligent-triage-use-cases-and-workflows

[^8]: https://www.solvisconsulting.com/blogs/post/Hablemos-de-inteligencia-artificial-en-el-ecosistema-de-CRM

[^9]: https://www.dashworks.ai/blog/hubspot-ai-search-how-dashworks-boosts-your-crm-intelligence

[^10]: https://sparkle.io/es/blog/ai-crm-software/

[^11]: https://blog.hubspot.es/marketing/excel-a-crm

[^12]: pasted-text.txt

[^13]: https://ecosystem.hubspot.com/es/marketplace/featured/apps-for-enterprise-crm-platform

[^14]: https://www.kustomer.com/resources/blog/ai-powered-crm-solutions/

[^15]: https://www.eesel.ai/es/blog/ai-tools-for-business

[^16]: https://www.microsoft.com/es/dynamics-365/solutions/crm

