<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_02 — Diseño de record pages (CRM enterprise)

## Executive summary (10–15 líneas)

Fact: En CRMs modernos, el record page suele organizarse en **columnas/zonas** (sidebars + columna central) con cards y tabs para agrupar información y acciones.[^1]
Inference: El objetivo del diseño no es “ver todo”, sino reducir tiempo a decisión y a primera acción (llamar, cotizar, escalar, cerrar).
Fact: HubSpot describe explícitamente un layout típico con left sidebar (propiedades), middle column (tabs como Overview/Activities) y right sidebar (associations/adjuntos/segmentos).[^1]
Fact: Salesforce permite crear y reordenar tabs/tab sets en record pages con Lightning App Builder, además de reglas de visibilidad por tab/componente.
Fact: Salesforce indica que en Lightning Experience muchos registros no muestran “Open Activities / Activity History” como related lists, porque se usa Activity Timeline para seguimiento.[^2]
Fact: Microsoft (Power Apps / model-driven) posiciona Timeline como el lugar para capturar y revisar interacciones (notas, emails, llamadas, tareas) y hacerlo visible en el tiempo.[^1]
Inference: “Above the fold” debe contener identidad del registro + estado + siguientes pasos + riesgos, y dejar el detalle profundo para tabs.
Fact: En HubSpot el tab *Activities* no se puede editar ni borrar, y hay un máximo de cinco tabs (incluyendo Overview).[^1]
Fact: En Dynamics/Power Apps, habilitar demasiados tipos de actividad en Timeline puede impactar performance; Microsoft recomienda limitar a 10 o menos activity types.[^1]
Inference: Diseña dos variantes: opción segura (estándar, baja fricción) vs opción agresiva (más personalización/condicionalidad) para acelerar adopción sin romper gobernanza.

***

## Definitions and why it matters

Fact: Un **record page** es la vista principal de un registro (contacto, empresa, deal, ticket, etc.) donde se leen propiedades, se ven asociaciones y se ejecutan acciones.[^1]
Fact: **Tabs** agrupan información en secciones navegables; Salesforce permite crear/editar/reordenar tabs y agregar componentes dentro de cada tab.
Fact: **Timeline / Activity feed** es el patrón para ver historial e interacciones; en Salesforce se usa Activity Timeline en lugar de related lists tradicionales para actividades en muchos objetos.[^2]
Fact: En model-driven apps, Timeline captura actividades (notes, appointments, emails, phone calls, tasks) y permite revisar “activity history” de forma rápida.[^1]
Inference: Importa porque una record page bien diseñada sube productividad (menos búsqueda), mejora calidad de datos (captura en el flujo) y baja riesgo operativo (visibilidad de estado/alertas).

***

## Principles and best practices (con citas por sección + fecha)

### 1) Above the fold = identidad + control + próxima acción (Fecha: 2026-02-16)

Fact: HubSpot ejemplifica que en el centro suele existir un tab de *Overview* con “highlighted property values” y actividad reciente, y un tab de *Activities* con timeline de interacciones.[^1]
Inference: Above the fold debe incluir: nombre/ID, etapa/estado, owner, “next step”, y 2–4 campos “highlight” que muevan la venta (p.ej., probabilidad, monto, fecha de cierre, riesgo de pago).
Inference (Qué incluye): datos mínimos para decidir y actuar en <10 segundos (contexto + CTA principal + señal de riesgo).
Inference (Qué no incluye): formularios largos, related lists extensas, reportes embebidos pesados.
Inference (Sensible): si pones crédito/riesgo “above the fold”, define permisos/visibilidad por rol (evita fuga de información y fricción comercial).

### 2) Timeline/activity feed como “centro de gravedad” (Fecha: 2026-02-16)

Fact: Salesforce afirma que en Lightning Experience los registros no muestran Open Activities y Activity History related lists; en su lugar se rastrean actividades en Activity Timeline.[^2]
Fact: Microsoft describe Timeline como un mecanismo para capturar y hacer visibles interacciones (notas, emails, llamadas, tareas) en el tiempo.[^1]
Inference: Buen patrón: timeline en un tab dedicado (*Activities*) y/o visible sin scroll excesivo, porque ahí ocurre el trabajo real (log + seguimiento).
Inference (Opción segura): timeline con tipos de actividad mínimos (llamada, email, nota, tarea) y orden descendente.
Fact (Opción agresiva, cuidado): en Dynamics/Power Apps, si habilitas demasiados activity types, Microsoft advierte impacto de performance y sugiere limitar a 10 o menos.[^1]

### 3) Associations = contexto comercial y operativo (Fecha: 2026-02-16)

Fact: HubSpot ubica en la right sidebar asociaciones como company/deal/ticket, además de memberships y attachments.[^1]
Inference: En enterprise CRM, asociaciones deben responder “¿con qué más está conectado esto?” (cuentas, deals, tickets, bookings, invoices, aprobaciones) sin obligar a abrir 5 pantallas.
Inference (Qué incluye): top asociaciones por frecuencia de uso + “conteos” y atajos (ver todo/crear nuevo).
Inference (Sensible): orden y visibilidad de asociaciones impacta adopción; si no puedes personalizar orden fácilmente, al menos fija un estándar por rol (ventas vs ops).

### 4) Tabs para separar “ahora” vs “profundo” (Fecha: 2026-02-16)

Fact: Salesforce permite crear, actualizar, borrar y reordenar tabs/tab sets en record pages y agregar componentes a cada tab.
Fact: Salesforce soporta reglas de visibilidad; si todos los componentes de un tab están ocultos por reglas, el tab se oculta automáticamente.
Fact: HubSpot permite cambiar orden de tabs, renombrar Overview y agregar tabs custom, con máximo cinco tabs; además, el tab *Activities* no se puede editar ni borrar.[^1]
Inference: Patrón recomendado de tabs (genérico enterprise): Overview (decisión rápida), Activities (trabajo), Details (propiedades completas), Related/Associations (relaciones), Finance/Risk (si aplica y con permisos).
Inference (Qué no incluye): más de 5–6 tabs “porque sí”; cada tab extra es fricción y diluye el uso.

### 5) Side panels = “panel de mando” por rol (Fecha: 2026-02-16)

Fact: HubSpot describe left sidebar con cards de propiedades (incluyendo lógica condicional) y right sidebar con asociaciones/adjuntos, mientras la columna central concentra tabs.[^1]
Inference: Usa side panels para lo que se consulta “todo el tiempo” pero no necesita ocupar el centro: propiedades clave, SLA/alertas, asociaciones críticas, adjuntos y quick actions.
Inference (Opción segura): 1–2 cards fijas por sidebar, sin condicionalidad compleja.
Inference (Opción agresiva): condicionalidad por etapa/segmento (p.ej., mostrar card de riesgo sólo si forma de pago = crédito), pero valida mantenimiento y consistencia.

### 6) Configurabilidad y gobernanza (Fecha: 2026-02-16)

Fact: En Salesforce, al seleccionar **Edit Page** por primera vez, se crea una copia de la página estándar y esa es la que se edita en Lightning App Builder.
Fact: En Dynamics/Power Apps, para ver cambios de Timeline hay que guardar y publicar (save + publish).[^1]
Inference: Define un “baseline” global (seguro) y capas por equipo/rol (agresivo) con control de cambios, porque la record page es infraestructura de ejecución, no decoración.

***

## Examples (aplicado a CRM enterprise)

### Ejemplo A: Deal/Opportunity para ventas (consultivo B2B)

Fact: Salesforce Trailhead muestra un ejemplo de record page con tabs donde se agrega Related Lists en un tab “Related” y Activities en un tab “Activity”, además de cambiar el orden de tabs.[^3]
Inference (Above the fold): etapa + monto + fecha cierre + probabilidad + owner + “next step” + botón principal (Log call / Create task / Send email).
Inference (Timeline): tab *Activities* como default para reps; registrar llamada/nota sin navegar.
Inference (Associations): cuenta, contactos clave, cotización/itinerario, casos/tickets (si postventa comparte CRM).

### Ejemplo B: Ticket/Case para operaciones (backoffice)

Fact: Microsoft plantea Timeline como forma de “catch up” rápido de actividad y últimas interacciones, ayudando a servicio más eficiente.[^1]
Inference (Above the fold): severidad/SLA, estado, responsable, próxima acción, y banderas de riesgo (documentación pendiente, pago pendiente, proveedor confirmado/no).
Inference (Tabs): Overview (SLA + resumen), Timeline (interacciones), Details (campos completos), Related (reservas, pasajeros/PNR, proveedores), Finance/Risk (si aplica).
Inference (Side panels): izquierda para propiedades operativas “siempre visibles”; derecha para asociaciones/adjuntos y checklist de cumplimiento.

***

## Metrics / success signals

Fact: En HubSpot, la configuración de record pages puede variar por “views” (default/team) y cards/tabs, lo que habilita medir adopción por equipo/rol.[^1]
Inference: Métricas que sí dicen si el diseño sirve (no vanity):

- Tiempo a primera acción desde abrir el registro (TTFA).
- % de registros con “next step” actualizado en el mismo día.
- % de interacciones loggeadas en timeline vs fuera del CRM.
- Scroll/click depth: cuánta gente llega a tabs “profundos” (si nadie llega, quizá sobra).
- Calidad de handoff: \# de re-trabajos por falta de contexto (ops/ventas).
Fact: En Dynamics/Power Apps, el número de activity types habilitados en Timeline puede afectar performance; úsalo como señal de “exceso de cobertura” si se degrada la experiencia.[^1]

***

## Operational checklist

Fact: HubSpot permite gestionar orden de tabs, cards y sidebars, y define límites como máximo de cinco tabs.[^1]
Inference (pasos prácticos PM/Admin):

- Define 3 tareas top por rol (ventas, ops, finanzas) que deben ser “1 click” desde el record.
- Diseña arriba del fold con 2–4 highlights + 1 CTA principal + 1 CTA secundario.
- Estructura tabs: Overview / Activities / Details / Related; agrega uno extra solo si hay caso claro (Risk/Finance).
- Normaliza associations: qué objetos deben estar siempre presentes y en qué prioridad (cuenta, contactos, deals, tickets, adjuntos).
- Limita tipos de actividad en timeline (especialmente en Dynamics) para no degradar performance.[^1]
- Define reglas de visibilidad por etapa/rol (agresivo) o mantén layout único (seguro) y mide antes de segmentar.
Fact: En Salesforce puedes usar reglas de visibilidad en tabs/componentes y si todo queda oculto, Salesforce oculta el tab.

***

## Anti-patterns

Fact: Salesforce indica que Activity Timeline reemplaza related lists tradicionales de actividades en muchos registros; duplicar ambos patrones sin intención puede confundir a usuarios.[^2]
Inference (errores comunes):

- Above the fold lleno de campos “por auditoría” y sin CTA claro.
- Timeline escondido detrás de tabs secundarios (se vuelve CRM “de lectura”, no de ejecución).
- 8–12 tabs “porque cada área pidió uno”; nadie los usa y se pierde gobernanza.
- Associations sin criterio (todo visible, nada priorizado).
- Personalización agresiva sin ownership: layouts que nadie mantiene y quedan obsoletos.

***

## Diagnostic questions

Fact: En HubSpot, el diseño se materializa en cards/tabs/sidebars (left/middle/right) por objeto y vista, lo que habilita preguntas por “vista y rol”.[^1]
Inference (preguntas para decidir diseño):

- ¿Cuál es la primera acción esperada al abrir este registro (por rol) y está a 1 click?
- ¿Qué 4 campos “mueven dinero” deben estar arriba del fold (y cuáles solo agregan ruido)?
- ¿El timeline refleja el trabajo real o la gente lo hace por WhatsApp/correo sin log?
- ¿Qué asociaciones son imprescindibles para resolver sin “cazar” links?
- ¿Qué parte es sensible (margen, crédito, riesgo) y cómo se controla visibilidad?
- Si quito un tab, ¿alguien lo extrañaría en su flujo diario?

***

## Sources (o referencia a SOURCES.md)

Salesforce Help — “Add and Customize Tabs on Lightning Pages Using the Lightning App Builder”.
Salesforce Help — “Activity Timeline” (Lightning Experience usa timeline en lugar de Open Activities/Activity History en muchos casos).[^2]
Salesforce Trailhead — “Custom Record Pages for Salesforce Lightning Experience” (ejemplo de tabs y componentes: Related Lists, Activities, Recent Items).[^3]
HubSpot Knowledge Base — “Customize records” (layout con sidebars + tabs; límites y reglas como máximo de tabs y Activities no editable).[^1]
Microsoft Learn (Power Apps) — “Set up the timeline control” (qué captura, configuración, performance y recomendación de limitar activity types).[^1]
Salesforce Help — “Activity Timeline Customization Considerations” (personalización con App Builder y consideraciones de ubicación del componente).[^4]
Salesforce Help — “Open Activities and Activity History Related Lists…” (convivencia/alternancia entre related lists y timeline, y configuración por componente).[^1]

***

## Añadir a `SOURCES.md` (sin duplicados)

- Salesforce Help. “Add and Customize Tabs on Lightning Pages Using the Lightning App Builder.” https://help.salesforce.com/s/articleView?id=platform.lightning_app_builder_customize_lex_pages_add_tabs.htm\&language=en_US\&type=5
- Salesforce Help. “Activity Timeline.” https://help.salesforce.com/s/articleView?id=sales.activity_timeline_parent.htm\&language=en_US\&type=5[^2]
- HubSpot Knowledge Base. “Customize records.” https://knowledge.hubspot.com/object-settings/customize-records[^1]
- Microsoft Learn (Power Apps). “Add and configure the timeline control in Power Apps (Set up the timeline control).” https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/set-up-timeline-control[^1]
- Salesforce Trailhead. “Custom Record Pages for Salesforce Lightning Experience.” https://trailhead.salesforce.com/content/learn/modules/lightning_app_builder/lightning_app_builder_recordpage[^3]

***

## Key takeaways for PM practice

- Diseña la record page para ejecución: decisión rápida arriba + trabajo en timeline + profundidad en tabs.
- Mantén tabs pocos y con intención; si necesitas segmentación, úsala por rol/etapa con gobernanza (no por capricho).
- Timeline es producto: limita tipos, cuida performance y vuelve “loggear” la acción más fácil del mundo.
- Associations y side panels son tu “mapa operativo”: prioriza lo que desbloquea la venta y el delivery sin saltos.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://help.salesforce.com/s/articleView?id=000382430\&language=en_US\&type=1

[^2]: pasted-text.txt

[^3]: https://trailhead.salesforce.com/content/learn/modules/lightning_app_builder/lightning_app_builder_recordpage

[^4]: https://help.salesforce.com/s/articleView?id=sales.activity_timeline_customization_considerations_lex.htm\&language=en_US\&type=5

[^5]: https://help.salesforce.com/s/articleView?id=platform.lightning_app_builder_customize_lex_pages_add_tabs.htm\&language=en_US\&type=5

[^6]: https://help.salesforce.com/s/articleView?id=sfdo.ec_set_up_application_timeline_record_page.htm\&language=en_US\&type=5

[^7]: https://knowledge.hubspot.com/object-settings/customize-records

[^8]: https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/set-up-timeline-control

[^9]: https://theeverydayadmincom.wordpress.com/2019/10/16/back-to-classic-part-2-activities-related-lists-view/

[^10]: https://www.youtube.com/watch?v=MW8vE-NBMNc

[^11]: https://siddharthvaghasia.com/timeline-control-in-model-driven-app/

[^12]: https://www.youtube.com/watch?v=79wA0-TjbcA

[^13]: https://community.hubspot.com/t5/HubSpot-Ideas/Order-of-associations-within-record/idi-p/448299

[^14]: https://dynamicscommunities.com/ug/power-platform-ug/how-to-add-a-timeline-control-form-to-a-model-driven-app/

[^15]: https://help.salesforce.com/s/articleView?id=sales.activity_timeline_parent.htm\&language=en_US\&type=5

[^16]: https://knowledge.hubspot.com/data-management/view-a-model-of-your-crm-object-and-activity-relationships

