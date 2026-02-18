<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_01_CRM_Domain_Model_At_Code_Level.md

## Executive summary (10–15 líneas)

Un CRM a nivel implementación se modela como un conjunto de entidades “core” (Account/Company, Contact, Lead, Opportunity/Deal), con **actividades** como timeline transversal y un pipeline representado por etapas y transiciones controladas por reglas.
**Facts:** Un CRM es una solución que centraliza y mejora interacciones (ventas/marketing/servicio) y suele ser data-driven, lo que empuja a modelar auditabilidad, ownership y permisos como primitives del dominio.[^1]
**Facts:** En DDD, conviene dividir el sistema en Bounded Contexts cuando el lenguaje/modelo cambia, porque un modelo único para todo el negocio no suele ser viable/costeable.[^2][^3]
**Facts:** A nivel táctico DDD, los agregados definen límites de consistencia transaccional; se accede por el identificador del Aggregate Root.[^4]
**Facts:** Domain Events capturan “cosas que pasaron” que disparan reacción y pueden sostener un audit log; además son base de Event Sourcing.[^5]
**Facts:** Event Sourcing garantiza que los cambios del dominio se inician por eventos, no por mutaciones ad-hoc.[^6]
**Facts:** En multi-tenant, elegir el modelo de tenancy es una decisión técnica y comercial; compartir todo baja costo pero aumenta riesgo de “noisy neighbor” y de impacto sistémico.[^7]
**Facts:** En bases multitenant, el esquema necesita columna(s) tenant identifier; y se recomienda enforcement (p. ej., Row-Level Security) para evitar fugas entre tenants.
**Inferences:** Para CRM enterprise B2B, el “happy path” es: ownership + actividades + pipeline + multi-tenant + auditoría; todo lo demás (custom fields, scoring, automatizaciones) se cuelga de esos ejes.

***

## Definitions and why it matters

**Facts (definiciones):**

- CRM: sistema que centraliza/optimiza interacciones con clientes entre áreas (ventas/marketing/servicio).[^1]
- Bounded Context: límite donde el modelo y el lenguaje ubicuo se mantienen consistentes; cuando cambia el lenguaje, suele requerirse otro modelo.[^3][^2]
- Aggregate (DDD): frontera de consistencia; un root y entidades hijas accesibles desde el root.[^4]
- Domain Event: objeto que registra algo ocurrido relevante para el negocio y que puede disparar cambios/reacciones y sostener auditoría.[^5]
- Tenancy model: cómo se organiza el almacenamiento por tenant; impacta diseño/operación y cambiarlo después puede ser costoso.

**Inferences (por qué importa en CRM):**

- El modelo de dominio “define fricción”: si ownership, pipeline y actividades quedan ambiguos, la agencia/cliente (B2B) sufre en control, forecast, comisiones, disputas y auditoría.
- Multi-tenant no es un “detalle infra”: condiciona claves, índices, permisos, particionamiento, y tu capacidad de vender planes (tiers) con aislamiento/riesgo controlado.

Fecha: 2026-02-17.

***

## Principles and best practices (con citas por sección + fecha)

### 1) Bounded Contexts primero (antes de tablas)

**Facts:** DDD usa modelos del dominio como lenguaje ubicuo para alinear devs y expertos, y propone dividir en Bounded Contexts cuando un modelo total no es factible.[^2][^3]
**Inferences (aplicación CRM):**

- Separa contextos típicos: **Sales** (pipeline), **Customer/Accounts** (jerarquías), **Engagement** (actividades), **Identity \& Access** (usuarios/roles), **Billing/Entitlements** (planes), **Automation** (rules/workflows).
- Contratos entre contextos vía eventos (Domain Events) y APIs explícitas, no por joins entre esquemas.

Fecha: 2026-02-17.

### 2) Agregados y consistencia: no todo en una transacción

**Facts:** Un aggregate define un límite de consistencia; se hace lookup por el id del root; el propósito es modelar invariantes transaccionales.[^4]
**Inferences (aplicación CRM):**

- Aggregate candidates (roots): `Account`, `Contact`, `Opportunity`, `Activity` (o `EngagementThread`), `Pipeline` (catálogo), `User/Team` (en IAM context).
- Regla práctica: lo que necesitas “cerrar” en una sola operación (p. ej., `Opportunity.changeStage()`) vive dentro del aggregate; lo demás se coordina por eventos/sagas.

Fecha: 2026-02-17.

### 3) Pipeline como máquina de estados (no como texto libre)

**Facts:** En CRMs comerciales, “Stage” suele ser un campo configurable del objeto Opportunity para mapear el proceso de ventas.[^8]
**Inferences (implementación):**

- Modela `PipelineStage` como catálogo (por tenant) y `StageTransition` con reglas (permitidas, condiciones, side-effects).
- `OpportunityStageChanged` como Domain Event para: recalcular forecast, disparar SLAs, generar tareas, notificar.

Fecha: 2026-02-17.

### 4) Actividades como timeline transversal (auditabilidad real)

**Facts:** En CRMs, las actividades se enlazan a entidades y se guardan en la “timeline”; una actividad puede vincularse a múltiples entidades (ej.: un email a deal y contacto).[^9]
**Inferences (implementación):**

- `Activity` como entidad con `type` (call/email/meeting/task), `occurredAt`, `actorId`, `body/metadata`, `links[]` (polimórfico).
- Evita “notas sueltas”: una Activity es un hecho con actor, tiempo, y vínculos, útil para auditoría y para ventas consultivas.

Fecha: 2026-02-17.

### 5) Ownership y relaciones: cascadas con intención

**Facts:** En plataformas CRM, relaciones 1:N y comportamientos de cascada (delete/assign) son decisiones explícitas para integridad y procesos; y hay decisiones de negocio sobre si reasignar oportunidades al cambiar dueño de cuenta.[^10]
**Inferences (implementación):**

- Ownership = `ownerType` (User/Team), `ownerId`, más `visibility` (private/team/org) y reglas ABAC/RBAC.
- Define cascadas por caso: `AccountOwnerChanged` ¿reasigna deals abiertos? ¿preserva deals cerrados por reporting? (hazlo regla, no “script” ad-hoc).

Fecha: 2026-02-17.

### 6) Multi-tenant: modelo comercial + enforcement técnico

**Facts:** El tenancy model define cómo mapeas datos de tenants a storage; hay modelos single-tenant, multi-tenant e híbridos, con trade-offs de aislamiento, costo y complejidad.
**Facts:** En B2B, un tenant suele mapear a una organización cliente; un tenant típicamente contiene múltiples usuarios, y a veces un cliente requiere múltiples tenants (p. ej., dev/prod o por regiones/divisiones).[^7]
**Facts:** En multitenant DB, el esquema requiere columnas tenant identifier para filtrar por tenant; y se recomienda enforcement (p. ej., RLS) para asegurar que queries no devuelvan datos de otros tenants.
**Facts:** Compartir infraestructura reduce costo, pero sube riesgo de seguridad/filtración y del “noisy neighbor”; y cambios pueden impactar a toda la base si todo está compartido.[^7]
**Inferences (implementación):**

- `tenantId` debe estar en **todas** las entidades “business”, y en índices compuestos (ej.: `(tenantId, naturalKey)`).
- El `tenantId` no se “infiera” del user; se valida en cada request y se propaga hasta DB (defensa en profundidad).

Fecha: 2026-02-17.

***

## Examples (aplicado a CRM enterprise)

### A) Entidades y relaciones (esqueleto implementable)

**Facts:** Agregados = límites de consistencia y acceso por root id.[^4]
**Inferences (modelo):**

- `Account { accountId, tenantId, legalName, taxId?, ownerId, status, createdAt }`
- `Contact { contactId, tenantId, accountId?, name, emails[], phones[], ownerId }`
- `Lead { leadId, tenantId, source, status, ownerId, qualificationScore? }`
- `Opportunity { opportunityId, tenantId, accountId?, primaryContactId?, pipelineId, stageId, amount, currency, closeDate, ownerId, forecastCategory }`
- `Activity { activityId, tenantId, type, occurredAt, actorId, subject, payload, links[] }`
    - `links[] = [{ entityType, entityId, role }]` (ej.: Opportunity, Contact, Account)


### B) Pipeline como API de dominio (DDD táctico)

**Facts:** Domain Event captura cosas que pasaron y puede usarse para auditoría y reacciones.[^5]
**Inferences (pseudo-API):**

- `Opportunity.changeStage(toStageId, changedBy)`:
    - valida transición (matriz de StageTransition)
    - actualiza `stageId`, `stageChangedAt`
    - emite `OpportunityStageChanged { tenantId, opportunityId, from, to, actorId, occurredAt }`


### C) Activities: un email que toca múltiples entidades

**Facts:** Una actividad puede vincularse a múltiples entidades en CRM.[^9]
**Inferences (ejemplo):**

- `Activity(type=Email, links=[Opportunity#123, Contact#9, Account#55])`
- Resultado: timeline consistente por entidad, sin duplicar el email en 3 tablas distintas.


### D) Multi-tenant: 2 modelos “safe vs aggressive”

**Facts:** Existen modelos single-tenant, multi-tenant e híbridos; el choice impacta aislamiento/costo/operación.[^7]
**Inferences:**

- Opción segura (más aislamiento, más costo): database-per-tenant o “stamps” por segmento premium; facilita restores por tenant y reduce blast radius.
- Opción agresiva (más eficiencia, más riesgo): shared multitenant DB con `tenantId` + enforcement fuerte (RLS/guards) + monitoreo por tenant; útil para long tail.

***

## Metrics / success signals

**Facts:** En arquitectura multitenant, aislamiento impacta performance y riesgo de “noisy neighbor”; y se recomienda validar que no haya fugas entre tenants.[^7]
**Inferences (métricas):**

- Data isolation: % queries con filtro `tenantId` enforced, nº hallazgos de “cross-tenant access” (debe ser 0).
- Pipeline health: tiempo promedio por etapa, % deals “stale” (sin Activity en N días), accuracy forecast por owner.
- Actividades: ratio Activities/Opportunity por semana, SLA de logging (latencia de ingesta), deduplicación (email/thread).
- Ownership: % entidades sin owner, tiempo de reasignación, disputas por propiedad (tickets internos).
- Operación multi-tenant: p95 latencia por tenant, top tenants por consumo (detectar noisy neighbors), costo por tenant (si lo trackeas).

***

## Operational checklist

**Facts:** En multitenant DB, necesitas `tenant identifier` en esquema y mecanismos para evitar exposición cross-tenant; y debes testear el modelo de aislamiento.[^7]
**Checklist (acción):**

- Definir qué es “tenant” (B2B: organización cliente; casos de múltiples tenants por cliente).[^7]
- Estándar de claves: todas las entidades con `tenantId` + `id` (UUID/ULID) y índices compuestos por `tenantId`.
- Guards de acceso: resolver `tenantId` desde identidad + validarlo en cada request; test de “no cross-tenant reads”.[^7]
- Pipeline: catálogo de etapas por tenant; matriz de transiciones; `Opportunity.changeStage()` como operación de dominio.[^8]
- Activities: modelo de timeline con `links[]` multi-entidad; idempotencia para emails/eventos.[^9]
- Ownership: reglas explícitas de reasignación/cascadas (ej.: al cambiar owner de Account, qué pasa con Opportunities).[^10]
- Eventos: definir Domain Events mínimos (StageChanged, OwnerChanged, ActivityLogged, LeadQualified) y consumidores.[^5]
- Auditoría: “quién, cuándo, qué cambió” (diffs) en entidades sensibles (amount, stage, owner).

***

## Anti-patterns

**Facts:** En Event Sourcing, el principio es que los cambios del dominio se inician por eventos; mezclar mutaciones directas rompe el enfoque.[^6]
**Anti-patterns (concretos):**

- “God entity” `Customer` que mezcla Account+Contact+Opportunity+Tickets+Billing en una tabla/aggregate.
- Pipeline como texto libre (sin transiciones), lo que destruye forecast y automatización.
- Actividades como “nota” sin actor/tiempo/links; luego no puedes auditar ni medir.
- Custom fields con EAV sin límites: mata performance, validaciones, y reporting; termina en queries imposibles.
- Ownership implícito (derivado por joins o “último editor”): genera disputas y reasignaciones invisibles.
- Multi-tenant “por convención” (solo en app): sin enforcement en DB/políticas, es riesgo de fuga.
- “Event sourcing de show”: guardar eventos pero también editar estado directo “porque urgía”, quedas con doble verdad.[^6]

***

## Diagnostic questions

1) ¿Cuál es tu definición operativa de tenant (cliente B2B, división, región, ambiente dev/prod)?
2) ¿Qué entidades son Aggregate Roots y cuáles invariantes sí o sí deben ser transaccionales?[^4]
3) ¿Cómo impides (técnica + pruebas) lecturas cross-tenant, y cómo lo monitoreas?[^7]
4) ¿El pipeline es una máquina de estados (transiciones + reglas) o un campo editable?[^8]
5) ¿Activities soporta links multi-entidad (email a deal+contact) o duplicas actividad en varios lados?[^9]
6) ¿Qué pasa cuando cambia el owner de una cuenta: reasignas oportunidades, solo activas, o ninguna? ¿Es regla o excepción?[^10]
7) ¿Qué Domain Events mínimos necesitas para auditoría y automatización sin acoplar contextos?[^5]

***

## Sources (o referencia a SOURCES.md)

**Fuentes usadas (para citas):**

- Microsoft Learn (Azure SQL): “Multitenant SaaS database tenancy patterns” (actualizado 2025-08-21).
- Microsoft Learn (Azure Architecture Center): “Tenancy models for a multitenant solution” (2025-06-27).[^7]
- Martin Fowler: “Domain Event” (2005-12-11).[^5]
- Martin Fowler: “Event Sourcing” (2005-12-11).[^6]
- Martin Fowler: “Bounded Context” (2014-01-14).[^2]
- Martin Fowler: “Ubiquitous Language” (2006-10-30).[^3]
- Microsoft Learn: Dynamics 365 (Dev Guide) “Entity relationship behavior…” (2024-12-12).[^10]
- Bitrix24 REST API: “Activities in CRM: Overview…” (s/f visible en snippet).[^9]
- Salesforce Trailhead: “Optimizing/Manage Opportunity Stages” (s/f visible en snippet).[^8]
- Microsoft Dynamics 365: “What is a CRM system?” (s/f en la ficha, contenido definicional).[^1]


### Añadir a SOURCES.md (sin duplicados)

- https://learn.microsoft.com/en-us/azure/azure-sql/database/saas-tenancy-app-design-patterns?view=azuresql
- https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/tenancy-models
- https://martinfowler.com/eaaDev/DomainEvent.html
- https://martinfowler.com/eaaDev/EventSourcing.html
- https://www.martinfowler.com/bliki/BoundedContext.html
- https://martinfowler.com/bliki/UbiquitousLanguage.html
- https://learn.microsoft.com/en-us/dynamics365/customerengagement/on-premises/developer/entity-relationship-behavior?view=op-9-1
- https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/index.html
- https://trailhead.salesforce.com/content/learn/projects/create-an-opportunity-record-type-for-npsp/create-and-manage-stages-and-

***

## Key takeaways for PM practice

- Diseña el CRM como “ownership + actividades + pipeline + auditoría” y luego extiende; eso reduce fricción comercial y operativa.
- Separa Bounded Contexts cuando cambia el lenguaje (ventas vs engagement vs cuentas), y conéctalos por eventos.[^3][^2][^5]
- Multi-tenant es estrategia de producto/precio: el modelo de tenancy define costo, aislamiento y riesgo; hazlo explícito desde el day 1.[^7]
- Activities con links multi-entidad y timestamps/actor son la base de control y calidad de ventas; sin eso, reportar es “fe”.[^9]
- Pipeline = máquina de estados con transiciones; si es texto libre, pierdes forecast y automatización.[^8]
<span style="display:none">[^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27]</span>

<div align="center">⁂</div>

[^1]: https://www.microsoft.com/es-es/dynamics-365/resources/what-is-a-crm-system

[^2]: https://www.martinfowler.com/bliki/BoundedContext.html

[^3]: https://martinfowler.com/bliki/UbiquitousLanguage.html

[^4]: https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-ddd

[^5]: https://martinfowler.com/eaaDev/DomainEvent.html

[^6]: https://martinfowler.com/eaaDev/EventSourcing.html

[^7]: pasted-text.txt

[^8]: https://trailhead.salesforce.com/content/learn/projects/create-an-opportunity-record-type-for-npsp/create-and-manage-stages-and-sales-processes

[^9]: https://apidocs.bitrix24.com/api-reference/crm/timeline/activities/index.html

[^10]: https://learn.microsoft.com/en-us/dynamics365/customerengagement/on-premises/developer/entity-relationship-behavior?view=op-9-1

[^11]: https://www.microsoft.com/es-co/dynamics-365/resources/what-is-crm

[^12]: https://www.youtube.com/watch?v=Ztr24-JBL2s

[^13]: https://learn.microsoft.com/es-es/azure/cloud-adoption-framework/scenarios/cloud-scale-analytics/architectures/data-domains

[^14]: https://learn.microsoft.com/en-us/answers/questions/1920935/how-to-isolate-each-tenants-data-in-a-multi-tenant

[^15]: https://www.rtdynamic.com/blog/salesforce-opportunity-stages-guide/

[^16]: https://learn.microsoft.com/en-us/answers/questions/2240069/need-help-setting-up-isolation-models-for-secure-m

[^17]: https://martinfowler.com/eaaDev/EventNarrative.html

[^18]: https://learn.microsoft.com/en-us/azure/azure-sql/database/saas-tenancy-app-design-patterns?view=azuresql

[^19]: https://ascendix.com/blog/salesforce-opportunity-stages/

[^20]: https://www.youtube.com/watch?v=ck7t592bvBg

[^21]: https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/tenancy-models

[^22]: https://stackoverflow.com/questions/36374929/ddd-conceptual-model-to-domain-model-with-aggregate-roots

[^23]: https://stackoverflow.com/questions/11324973/bounded-contexts-and-aggregate-roots

[^24]: https://deviq.com/domain-driven-design/bounded-context

[^25]: https://www.edrawmax.com/templates/1021802/

[^26]: https://stackoverflow.com/questions/18625576/confused-about-bounded-contexts-and-subdomains

[^27]: https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/ddd-oriented-microservice

