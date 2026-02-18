# KB_02 — Data Model & Custom Objects en CRM Enterprise

***

## Executive Summary

El data model de un CRM define cómo se estructura, almacena y relaciona la información de clientes, transacciones y operaciones dentro de la plataforma. Un modelo bien diseñado reduce fricción operativa, habilita reporting confiable, evita duplicados y soporta integraciones sin romper sistemas downstream.[^1][^2]

Las plataformas CRM líderes (Salesforce, HubSpot, Dynamics 365) comparten una arquitectura común de 4 capas: **objetos** (tablas), **registros** (filas), **propiedades/campos** (columnas) y **asociaciones/relaciones** (foreign keys). La diferencia entre plataformas radica en la filosofía central — HubSpot es contact-centric, Salesforce es account-centric — y eso impacta directamente cómo mapeas flujos de ventas B2B.[^2][^1]

Las decisiones de modelado tomadas al inicio (cuándo crear un custom object vs. agregar campos, qué tipo de relación usar, cómo nombrar campos internos) son costosas de revertir después. Los nombres API en HubSpot son permanentes; en Salesforce, los master-detail no se pueden convertir fácilmente a lookups. Este documento cubre las mejores prácticas para tomar esas decisiones correctamente desde el diseño, con ejemplos aplicados a operación CRM enterprise B2B.[^3][^1]

**Fact:** Las 4 capas (objetos → registros → propiedades → asociaciones) son consistentes en Salesforce, HubSpot y Dynamics 365.
**Inference:** Un operador mayorista de turismo B2B necesita modelar agencias, contactos, cotizaciones, reservas y proveedores como objetos separados con relaciones claras, no como campos planos en un solo objeto.

***

## Definitions and Why It Matters

### Conceptos Fundamentales

| Concepto | Definición | Ejemplo en CRM |
|---|---|---|
| **Objeto (Object)** | Tabla de base de datos que representa una entidad de negocio | Contacts, Companies, Deals, Tickets [^4][^5] |
| **Registro (Record)** | Instancia individual dentro de un objeto (una fila) | "Agencia Viajes Caribe" como registro de Company |
| **Propiedad/Campo (Property/Field)** | Columna que almacena un dato específico del registro | Email, phone, deal_amount, close_date [^1] |
| **Asociación/Relación** | Vínculo entre registros de distintos objetos | Contact → Company, Deal → Contact [^4] |
| **Custom Object** | Tabla definida por el usuario para datos que no caben en objetos estándar | Subscriptions, Facilities, Contracts [^1] |
| **Junction Object** | Objeto intermedio que modela relaciones N:N entre dos objetos | OpportunityContactRole, PriceBookEntry [^6][^7] |
| **ERD** | Entity Relationship Diagram — representación visual de objetos y sus relaciones | Diagrama Salesforce con crow's foot notation [^8][^9] |
| **Golden Record** | Registro maestro consolidado que representa la verdad única de un cliente/entidad | Resultado de identity resolution + merge [^10][^11] |

### Por qué importa el Data Modeling en CRM

- **Reporting roto** → Si las relaciones no están bien definidas, los reportes cross-object no funcionan. No puedes agrupar contactos por industria de su empresa si no hay asociación Contact → Company.[^1]
- **Property sprawl** → Equipos crean 200+ campos custom cuando 40 bastarían, generando confusión y degradación de performance.[^1]
- **Duplicados** → Sin dedup y reglas de identidad, el mismo cliente aparece N veces con datos fragmentados, destruyendo la confianza del equipo de ventas.[^12]
- **Deuda técnica** → Decisiones como nombres API permanentes o relaciones master-detail incorrectas se pagan durante años.[^3][^1]

***

## Principles and Best Practices

### 1. Objetos Core: La Base del Modelo

Todo CRM enterprise tiene un set de objetos estándar que cubren el 80% de los casos:[^4][^2]

**HubSpot (Contact-Centric):**
- **Contacts** → Personas (dedup por email)
- **Companies** → Organizaciones (dedup por dominio)
- **Deals** → Oportunidades de venta
- **Tickets** → Casos de soporte
- **Leads** (Sales Hub Pro+), Line Items, Quotes, Products[^5]

**Salesforce (Account-Centric):**
- **Accounts** → Empresas/Organizaciones
- **Contacts** → Personas dentro de Accounts
- **Leads** → Prospectos no cualificados (se convierten en Account + Contact + Opportunity)
- **Opportunities** → Oportunidades de ingreso
- **Cases** → Soporte/servicio[^2]

**Mapeo entre plataformas:**

| HubSpot | Salesforce | Nota |
|---|---|---|
| Contact | Contact o Lead | Decidir regla de sync antes de integrar [^2][^13] |
| Company | Account | HubSpot dedup por domain; Salesforce no automáticamente |
| Deal | Opportunity | Stages y pipelines mapean 1:1 |
| Ticket | Case | Lógica similar, campos diferentes |
| Custom Object (Enterprise) | Custom Object | Requiere mapping manual [^13] |

**Fact:** HubSpot dedup contacts por email y companies por domain automáticamente. Salesforce no tiene dedup nativa comparable — requiere herramientas externas o DemandTools.[^14][^2]

*(Fuentes: HubSpot Knowledge Base, enero 2026; RevBlack, octubre 2025; HubSpot Objects doc, enero 2026 )*[^15][^5][^2]

### 2. Tipos de Relaciones

Las relaciones entre objetos son el esqueleto del data model. La decisión entre tipos de relación impacta seguridad, integridad referencial y flexibilidad:[^16][^3]

| Tipo | Acoplamiento | Cascade Delete | Roll-up Summary | Independencia del hijo | Cuándo usar |
|---|---|---|---|---|---|
| **Master-Detail** | Fuerte (tight) | Sí — se borra el hijo al borrar el padre | Sí (SUM, COUNT, AVG, MIN, MAX) | No — el hijo NO puede existir sin padre | Order → Line Items, Campaign → Campaign Members [^3][^17] |
| **Lookup** | Débil (loose) | No — el hijo sobrevive | No (requiere herramientas como RollUp Magic) | Sí — el hijo existe independiente | Contact → Account (un contacto puede no tener cuenta) [^3][^17] |
| **Junction Object** | N:N via 2 master-detail | Dependiente de ambos padres | Sí en ambos padres | No | Opportunity ↔ Contact (con roles), Product ↔ PriceBook [^6][^7] |
| **Self-Lookup (Recursiva)** | Variable | No | No | Variable | Employee → Manager (misma tabla) [^18] |

**Decisión clave en Salesforce:** Master-Detail vs. Lookup:[^17][^3]
- Usa **Master-Detail** cuando el hijo NO tiene sentido sin el padre (Line Items sin Order = basura)
- Usa **Lookup** cuando el hijo tiene vida propia (un Contact puede existir sin Account en ciertos modelos)
- Si necesitas N:N → crea un **Junction Object** con 2 master-detail fields[^6][^16]

**En HubSpot:** Las asociaciones son más simples — se definen como direccionales con labels customizables. Cardinality rules se configuran al crear custom objects. Límite: 100 association labels por par de objetos.[^1]

*(Fuentes: Ksolves, febrero 2025; Salesforce Object Reference; SmallBuilder, septiembre 2024 )*[^16][^6][^3]

### 3. Custom Objects: Cuándo Sí, Cuándo No

**Crear un Custom Object cuando**:[^19][^1]

1. **Relación 1:N donde el "N" necesita tracking independiente** — Ejemplo: Company con múltiples Facilities, cada una con dirección, contacto y historial propio. Agregar facility_1_address, facility_2_address crea schema frágil.[^1]

2. **Necesitas relación N:N con contexto** — Ejemplo: Deals multi-party donde necesitas saber qué Company representa cada Contact y su rol. Solución: Custom Object "Deal Participants" entre Contacts, Companies y Deals.[^1]

3. **El dato tiene lifecycle propio** — Ejemplo: Contratos anuales que se renuevan independientemente del Deal original, con su propio estado (active/expiring/renewed/cancelled).[^1]

4. **Hay varios data elements que pueden ocurrir más de una vez** — Ejemplo: Múltiples contratos asociados a un Deal, cada uno con fecha de firma, firmante, duración.[^19]

**NO crear Custom Object cuando**:[^1]

- El dato **describe atributos** de un registro existente → usar custom properties (ejemplo: compliance_status en Company)
- Es información **simple yes/no, fecha o categoría** → checkbox o dropdown en objeto existente
- La relación es **1:1 sin atributos complejos** → 10 campos en el Deal vs. un objeto "Project Plans" separado con asociación 1:1 es overhead innecesario
- Quieres "organizar propiedades" → usa **Property Groups**, no objetos separados

**Fact:** HubSpot permite máximo 10 custom objects en Professional y 100 en Enterprise.[^1]
**Inference:** Para un mayorista de turismo, candidatos a custom objects incluyen: Reservas (con lifecycle propio), Itinerarios (N:N con servicios/proveedores), Documentos de viaje (asociados a contactos y reservas).

*(Fuentes: Hypha Dev, enero 2026; Engaging.io, septiembre 2025 )*[^19][^1]

### 4. Campos (Properties/Fields): Governance y Naming

**Tipos de campo y consideraciones**:[^1]

| Tipo | Límite/Nota | Precaución |
|---|---|---|
| Text | Hasta 65,536 chars | Multi-line NO soporta evaluación en workflows |
| Number | Floating-point precision | Para montos financieros: guardar en centavos (integer), dividir por 100 en reporting |
| Date | Solo fecha, no hora (salvo date picker) | Workflows evalúan en timezone del portal |
| Dropdown | Valores internos + labels editables | Workflows referencian valor INTERNO — cambiar label no rompe, cambiar valor interno SÍ rompe |
| Calculated | Fórmula auto-recalculada | Falla silenciosamente — queda en blanco sin error. Máximo 2 niveles de dependencia |

**Reglas de naming obligatorias**:[^20][^1]

- **Los API names son PERMANENTES** (HubSpot). Si creas `q4_2024_campaign_source`, te queda para siempre aunque el uso cambie.
- Usa nombres genéricos y atemporales: `campaign_source_primary` en vez de `q4_2024_campaign_source`
- Prefijos por dominio/equipo: `mkt_` (marketing), `ops_` (operaciones), `sales_` (ventas), `custom_` (genérico)
- Documenta convenciones ANTES de construir
- Audita propiedades existentes antes de crear nuevas — HubSpot viene con cientos de propiedades nativas[^19]

**Validaciones en punto de entrada**:[^21][^22][^23]

- Email: validar formato `user@domain.tld`
- Teléfono: incluir código de país (+58, +57)
- Campos obligatorios: solo los estrictamente necesarios — demasiados campos required matan la adopción[^19]
- Formato de datos: normalizar antes de guardar (capitalización, abreviaciones consistentes)
- Implementar via: workflow rules, validation rules nativas, plugins o JavaScript según plataforma[^21]

**Fact:** Teams routinely create 200+ custom properties when 40 would suffice.[^1]
**Inference:** Reducir property sprawl a 30-40% es factible post-auditoría y mejora directamente la adopción de reps de ventas.

*(Fuentes: Hypha Dev, enero 2026; DCKAP, octubre 2025; Dynamics Community, 2023 )*[^23][^21][^1]

### 5. Deduplicación e Identity Resolution

La deduplicación no es un evento one-time — es un **proceso continuo** de 3 fases:[^12]

**Fase 1: Identificación de duplicados**
- Matching por email, teléfono, unique ID
- Fuzzy matching para nombres (José vs Jose, García vs Garcia)
- Reglas configurables por objeto (Leads, Contacts, Accounts)[^12]

**Fase 2: Prevención de duplicados**
- Bloquear o flaggear en punto de entrada (forms, imports, API syncs)
- Normalizar formatos automáticamente (teléfonos, emails)
- Server-side validation para procesos en background[^12]

**Fase 3: Merge de duplicados**
- Seleccionar master record (el más completo)
- Consolidar relaciones, actividades, ownership e historial
- Single-click o bulk merging con preview antes de ejecutar[^12]

**Identity Resolution → Golden Record**:[^10][^11]

El Golden Record es el registro maestro unificado que consolida todo lo conocido sobre un cliente de todas las fuentes. El proceso incluye:

- **Data Quality**: Limpieza, normalización y validación al ingerir datos
- **Data Matching**: Algoritmos de matching (exact + fuzzy) para vincular registros
- **Data Merging**: Consolidación controlada con reglas de merge/split documentadas
- **Persistent Key Management**: IDs persistentes que sobreviven merges y splits[^11]

**Herramientas por plataforma:**
- Salesforce: DemandTools (~$50/user/mes), Cloudingo
- HubSpot: Dedup nativo (Operations Hub), AI dedup
- Dynamics 365: DeDupeD (Inogic), nativo con reglas personalizables[^14][^12]

**Fact:** HubSpot dedup contacts por email y companies por domain automáticamente.[^2]
**Inference:** En mercados LATAM con data sucia (Venezuela/Colombia), el fuzzy matching es crítico — variaciones de nombre, múltiples emails por persona, cambios de teléfono frecuentes.

*(Fuentes: Inogic/Dynamics 365, enero 2026; Redpoint Global, octubre 2024; Paciolan, abril 2024 )*[^10][^11][^12]

### 6. Migraciones de Datos

**Proceso ETL (Extract → Transform → Load)**:[^24][^14]

1. **Extract**: Exportar datos del CRM origen con IDs únicos (Contact ID, Company ID, Deal ID)
2. **Transform**: Limpiar, deduplicar, normalizar, mapear campos al esquema destino
3. **Load**: Importar al CRM destino en CSVs separados por objeto, UTF-8, sin line breaks

**Checklist pre-migración**:[^25][^14]

- [ ] Auditar tasa de duplicados (correr dedup ANTES de migrar)
- [ ] Identificar registros incompletos (< 3 campos populated) → no migrar
- [ ] Flaggear registros inactivos (sin actividad en 18+ meses) → evaluar si migrar
- [ ] Listar TODOS los custom fields → marcar cuáles migrar, dropear los no usados
- [ ] Inventario de integraciones (email, calendar, accounting, marketing automation)
- [ ] Definir matching rules: email (contacts), domain (companies), deal name + close date (deals)[^14]

**Estrategias de migración:**

| Estrategia | Pros | Contras | Mejor para |
|---|---|---|---|
| **Big Bang** | Rápido, una sola fecha | Downtime 24h, rollback complejo | < 20K registros, modelo simple [^14] |
| **Phased** | Bajo riesgo, < 2h downtime, rollback fácil | 6-12 semanas, sync bidireccional, doble licencia | > 20K registros, datos complejos [^14] |

**Métricas de éxito:**
- Data accuracy: 99%+ (< 1% error rate)
- Downtime: < 2h (phased), < 24h (Big Bang)
- User adoption: 90%+ usando nuevo CRM daily by week 2
- Zero duplicados creados durante import[^14]

**Post-migración:**
- Correr dedup semanal durante el primer mes
- Verificar que todas las relaciones (Contact → Company) estén intact
- Testear integraciones una por una
- Backup en 2 ubicaciones (cloud + local) ANTES de migrar[^14]

**Fact:** Success rate migración phased con overlap: 99.8% vs Big Bang: 87%.[^14]
**Inference:** Para un mayorista de turismo con datos de agencias en múltiples sistemas, la migración phased con 3 meses de overlap es la apuesta segura aunque cueste doble licencia temporalmente.

*(Fuentes: Optif.ai, diciembre 2025; Velvetech, diciembre 2025; Cobalt, mayo 2024 )*[^25][^24][^14]

### 7. Backward Compatibility

Cuando evolucionas el schema de tu CRM (nuevos campos, nuevas relaciones), la regla de oro es: **los consumidores existentes no deben romperse**.[^26][^27][^28]

**Cambios SEGUROS (backward compatible):**
- Agregar campos opcionales con valores default[^28][^29]
- Agregar nuevas tablas/objetos sin alterar los existentes[^27]
- Ampliar tipos numéricos (int → bigint)[^28]
- Cambiar display labels (no rompe workflows que referencian API names)[^1]

**Cambios QUE ROMPEN:**
- Eliminar campos requeridos[^28]
- Renombrar campos sin alias[^29]
- Cambiar valores internos de dropdowns referenciados por workflows[^1]
- Convertir relaciones master-detail a lookup o viceversa[^3]

**Patrones de mitigación**:[^27]

1. **Additive Schema Changes**: Solo agregar, nunca alterar ni eliminar
2. **Dual-Write Pattern**: Durante migración, escribir en schema viejo Y nuevo simultáneamente
3. **Semantic Versioning**: MAJOR.MINOR.PATCH para cambios de schema
4. **Schema Registry + CI/CD**: Validar compatibilidad automáticamente antes de producción[^28]
5. **Deprecation Strategy**: Marcar campo como deprecated → migrar datos → esperar N ciclos → eliminar

**Fact:** Mantener múltiples versiones de schema puede incrementar storage entre 11% y 39%.[^28]
**Inference:** En un CRM operativo, el costo de storage extra es negligible vs. el costo de romper workflows de ventas en producción.

*(Fuentes: TiDB/PingCap, diciembre 2024; DataExpert.io, febrero 2026; Solace, docs actuales )*[^26][^27][^28]

***

## Examples (Aplicado a CRM Enterprise B2B)

### Ejemplo 1: ERD Simplificado — Mayorista de Turismo B2B

```
┌─────────────┐       1:N        ┌──────────────┐
│  COMPANIES  │◄─────────────────│   CONTACTS   │
│ (Agencias)  │                  │ (Agentes)    │
│             │                  │              │
│ - domain*   │                  │ - email*     │
│ - name      │                  │ - firstname  │
│ - country   │                  │ - role       │
│ - credit_   │                  │ - whatsapp   │
│   status    │                  └──────┬───────┘
└──────┬──────┘                         │
       │ 1:N                            │ N:N (via Deal Contacts)
       │                                │
       ▼                                ▼
┌──────────────┐      N:1       ┌──────────────┐
│    DEALS     │◄───────────────│   QUOTES     │
│ (Reservas)   │                │ (Cotizaciones│
│              │                │  de paquetes)│
│ - deal_name  │                │              │
│ - amount     │                │ - pax_count  │
│ - pax_count  │                │ - destination│
│ - travel_    │                │ - margin_%   │
│   date       │                └──────────────┘
│ - status     │
└──────┬───────┘
       │ 1:N
       ▼
┌──────────────────┐        N:N (via junction)       ┌──────────────┐
│   LINE ITEMS     │◄───────────────────────────────►│  SERVICES    │
│ (Servicios del   │                                 │ (Catálogo)   │
│  paquete)        │                                 │              │
│                  │                                 │ - type       │
│ - quantity       │                                 │ - provider   │
│ - unit_price     │                                 │ - cost       │
│ - supplier_ref   │                                 └──────────────┘
└──────────────────┘
```

**Decisiones típicas en este modelo:**

1. **¿Agencia es Company o Custom Object?** → Company. Es el objeto core, dedup por domain, con todas las propiedades nativas de empresa.

2. **¿Cotización vive como propiedades del Deal o como objeto separado?** → Objeto separado (Quote/Custom). Una agencia puede pedir 5 cotizaciones antes de confirmar 1 reserva. Relación N:1 con Deal.

3. **¿Servicios del paquete como campos del Deal?** → No. Son Line Items (1:N con Deal). Cada servicio tiene precio, proveedor, fecha — datos que varían por instancia.

4. **¿Necesito junction object?** → Sí, si un servicio del catálogo puede estar en múltiples deals (hotel X aparece en paquete A y paquete B). Line Items es el junction entre Deals y Services.

### Ejemplo 2: ERD Salesforce — Sales Cloud Core

```
┌───────────────┐     N:1 (Lookup)     ┌───────────────┐
│    LEAD       │                       │   CAMPAIGN    │
│               │─────────────────────►│               │
│ - Status      │                       │ - Name        │
│ - Source      │                       │ - Type        │
│ - Company     │                       │ - Status      │
└───────┬───────┘                       └───────┬───────┘
        │ Convert                               │ 1:N (Master-Detail)
        ▼                                       ▼
┌───────────────┐     1:N (Lookup)     ┌───────────────┐
│   ACCOUNT     │◄─────────────────────│ CAMPAIGN      │
│               │                       │ MEMBER        │
│ - Name        │                       │ (Junction)    │
│ - Industry    │                       └───────────────┘
│ - Revenue     │
└───────┬───────┘
        │ 1:N (Lookup)
        ▼
┌───────────────┐     N:N (Junction)   ┌───────────────┐
│   CONTACT     │◄────────────────────►│ OPPORTUNITY   │
│               │  via Opp Contact     │               │
│ - Email       │  Role                │ - Amount      │
│ - Title       │                       │ - Stage       │
│ - Phone       │                       │ - Close Date  │
└───────────────┘                       └───────┬───────┘
                                                │ 1:N (Master-Detail)
                                                ▼
                                        ┌───────────────┐
                                        │ OPP LINE ITEM │
                                        │ (Junction →   │
                                        │  Product via  │
                                        │  PriceBook    │
                                        │  Entry)       │
                                        └───────────────┘
```

**Notación en ERD Salesforce**:[^9]
- **Crow's foot notation** para cardinalidad (N = pata de cuervo)
- **Diamante** en lado singular = relación Master-Detail (cascade delete, security inheritance)[^9]
- **Línea simple** sin diamante = Lookup (loose coupling)
- **Cajas con bordes sólidos** = objetos con tabla física
- **Cajas con borde punteado** = record types (subtipos lógicos)

*(Fuentes: Salesforce Architect, docs actuales; Salesforce Data Model, enero 2026; SmallBuilder, septiembre 2024 )*[^8][^6][^9]

### Ejemplo 3: Decisiones Típicas con Trade-offs

| Decisión | Opción Segura | Opción Agresiva | Criterio de elección |
|---|---|---|---|
| ¿Custom Object o campos extra? | Campos extra si < 5 atributos y relación 1:1 | Custom Object si hay lifecycle propio o 1:N [^1] | ¿El dato puede ocurrir más de una vez? |
| ¿Master-Detail o Lookup? | Lookup (más flexible, hijo independiente) | Master-Detail (rollup summaries, cascade delete) [^3] | ¿El hijo tiene sentido sin el padre? |
| ¿Dedup pre o post-migración? | Ambos — pre para limpieza, post para validación [^12] | Solo pre si el volumen es < 5K records | ¿Cuántos registros y cuántas fuentes? |
| ¿Big Bang o Phased migration? | Phased con 3 meses overlap [^14] | Big Bang si < 10K records y modelo simple | ¿Cuánto puedes tolerar de downtime? |
| ¿Naming genérico o descriptivo? | Genérico atemporal (`source_primary`) | Descriptivo si el campo es efímero (`q4_promo`) [^1] | ¿El campo va a sobrevivir > 6 meses? |

***

## Metrics / Success Signals

| Métrica | Target | Señal de alerta |
|---|---|---|
| **Tasa de duplicados** | < 2% del total de registros | > 5% indica falta de reglas de prevención [^12] |
| **Property sprawl ratio** | < 50 custom properties por objeto | > 100 custom properties = auditoría urgente [^1] |
| **Association coverage** | > 95% de Contacts asociados a Company | < 80% = reporting cross-object roto [^1] |
| **Data completeness** | > 90% de registros con ≥ 5 campos key populated | < 70% = problema de adopción o forms [^14] |
| **Migration accuracy** | 99%+ post-migración | < 95% = stop, fix, re-run [^14] |
| **Workflow breakage post-change** | 0 workflows rotos por cambio de schema | > 0 = falta de backward compatibility check |
| **Dedup merge accuracy** | < 1% false merges | > 3% = revisar matching rules [^12] |
| **Field naming compliance** | 100% campos nuevos siguen convención | Cualquier violación = review obligatorio |

***

## Operational Checklist

### Pre-Diseño
- [ ] Mapear entidades de negocio en papel/whiteboard ANTES de tocar el CRM[^1]
- [ ] Definir convención de naming (prefijos, snake_case, sin fechas en API names)[^20][^1]
- [ ] Auditar objetos y propiedades existentes — eliminar duplicados de campo[^19]
- [ ] Documentar cardinalidad de cada relación (1:1, 1:N, N:N)
- [ ] Definir qué campos son required vs optional — minimizar required[^19]

### Durante Construcción
- [ ] Crear custom objects solo cuando pasan el test de "lifecycle propio" o "puede ocurrir más de una vez"[^19][^1]
- [ ] Definir association labels ANTES de crear asociaciones[^1]
- [ ] Configurar validation rules en punto de entrada (email format, phone con country code)[^23]
- [ ] Testear con 10-20 registros por objeto antes de rollout[^1]
- [ ] Verificar que calculated properties no fallen silenciosamente[^1]

### Post-Implementación
- [ ] Correr dedup semanal durante primer mes[^14]
- [ ] Monitorear property usage — deprecar campos sin uso en 90 días
- [ ] Revisar y actualizar validation rules trimestralmente[^22]
- [ ] Auditar association coverage mensualmente
- [ ] Documentar cada cambio de schema con versión semántica[^27]

### Pre-Migración
- [ ] Exportar full backup en 2 ubicaciones (cloud + local)[^14]
- [ ] Correr dedup en datos origen ANTES de migrar[^25][^12]
- [ ] Crear CSVs separados por objeto (contacts.csv, companies.csv, deals.csv)[^14]
- [ ] Verificar UTF-8 encoding (crítico para nombres con acentos: José, François)[^14]
- [ ] Trial migration con sample de 10-20 rows → validar antes de full run[^14]

***

## Anti-patterns

1. **Property Sprawl Silencioso** — Marketing crea `lead_source_campaign`, Sales agrega `campaign_source`, Ops construye `utm_campaign_source`. Tres campos trackeando lo mismo. Resultado: reporting inconsistente y desconfianza.[^1]

2. **Custom Object para "Organización"** — Crear un objeto "Company Details" 1:1 con Company para "organizar campos". Duplica record counts, complica reporting, cero beneficio arquitectónico. Usa Property Groups.[^1]

3. **API Names con fechas** — `q4_2024_campaign_source` queda permanente. En 6 meses trackea campañas de todos los quarters pero el nombre confunde a todos.[^1]

4. **Master-Detail donde debería ser Lookup** — El hijo no puede existir sin padre. Si un Contact necesita vivir sin Account en tu modelo, Master-Detail es la decisión incorrecta.[^17][^3]

5. **Dedup como "paso final"** — Dejar deduplicación para después de go-live. Los duplicados migrados son más difíciles de limpiar que los pre-migración y destruyen la confianza del equipo desde día 1.[^12]

6. **Ignorar Backward Compatibility** — Cambiar valor interno de dropdown sin verificar qué workflows lo referencian. Resultado: automaciones rotas en producción sin error visible.[^28][^1]

7. **Campos Required en exceso** — Hacer 15 campos obligatorios en un form de creación de contacto. Los reps inventan datos para pasar el form, contaminando la base.[^19]

8. **Junction Objects sin campos propios** — Crear un junction object vacío (solo 2 lookups, sin metadata). Si no necesitas almacenar contexto de la relación (rol, fecha, estado), una asociación directa o lookup basta.[^6]

***

## Diagnostic Questions

1. **¿Cuántos custom properties tiene cada objeto core?** Si > 100, ¿cuántos se usan activamente en reporting o workflows? Señal de property sprawl.

2. **¿Qué % de tus Contacts están asociados a una Company?** Si < 80%, tu reporting cross-object es unreliable.

3. **¿Tienes naming convention documentada y enforced?** Si no, ¿cuántos campos tienen nombres ambiguos o con fechas?

4. **¿Cuál es tu tasa actual de duplicados?** ¿Tienes prevención activa (real-time blocking) o solo limpieza periódica?

5. **¿Tus custom objects pasan el test de "lifecycle propio"?** Si un custom object tiene relación 1:1 con un objeto estándar y < 5 campos, ¿por qué no son propiedades del objeto estándar?

6. **¿Qué pasa cuando borras un registro padre?** ¿Se borran los hijos (master-detail) o quedan huérfanos (lookup sin cleanup)?

7. **¿Tienes proceso de deprecation para campos?** ¿O acumulas campos muertos indefinidamente?

8. **¿Tu último cambio de schema rompió algún workflow?** Si sí, ¿tienes un proceso de validación pre-deploy?

9. **¿Cuánto tiempo tomaría migrar a otro CRM hoy?** Si la respuesta es "no sé" o "> 6 meses", tu modelo tiene deuda técnica significativa.

10. **¿Quién es el data owner de cada objeto?** Si no hay respuesta clara, no hay governance real.[^30][^22]

***

## Key Takeaways for PM Practice

- **El data model es infraestructura, no decoración.** Las decisiones de modelado tomadas hoy se pagan (o se cobran) durante años. Invertir 2 semanas en diseño ahorra 6 meses de refactoring.

- **Custom Object ≠ "quiero más orden".** Solo crea objetos custom cuando hay lifecycle propio, relación 1:N o N:N, o datos que pueden ocurrir más de una vez por registro.

- **Los nombres API son para siempre.** Define convención de naming y enforceala ANTES de que el primer campo se cree. Prefijos por equipo, snake_case, sin fechas.

- **Dedup es proceso continuo, no evento.** Tres fases: identificar, prevenir, mergear. Pre y post-migración. Semanal el primer mes, mensual después.

- **Backward compatibility > velocidad de cambio.** Cambios aditivos son seguros. Eliminar o renombrar campos sin strategy rompe producción silenciosamente.

- **Menos campos required = mejor adopción.** Cada campo obligatorio extra es fricción para el rep de ventas. Datos inventados son peor que datos faltantes.

- **El ERD no es un diagrama bonito — es el contrato técnico.** Si no puedes dibujarlo, no lo entiendes. Si no lo documentas, nadie más lo entenderá.

- **Property sprawl es el enemigo silencioso.** Audita trimestralmente, depreca agresivamente, documenta obsesivamente.

- **Master-Detail vs. Lookup es la decisión de relación más importante en Salesforce.** Equivocarse tiene consecuencias en seguridad, cascade deletes y rollup summaries que son difíciles de revertir.

- **Golden Record = confianza del equipo comercial.** Si el vendedor no confía en los datos del CRM, vuelve a su Excel. Identity resolution no es un lujo técnico, es requisito de adopción.

***

## Sources

| ID | Fuente | Fecha | URL |
|---|---|---|---|
| [^15] | HubSpot Knowledge Base — Data Model Builder | Ene 2026 | knowledge.hubspot.com |
| [^19] | Engaging.io — Custom Objects vs Properties | Sep 2025 | engaging.io |
| [^4] | HS Simple — HubSpot CRM Structure | Jul 2024 | hs-simple.com |
| [^25] | Velvetech — CRM Migration Checklist | Dic 2025 | velvetech.com |
| [^1] | Hypha Dev — Complete Guide HubSpot CRM Architecture | Ene 2026 | hyphadev.io |
| [^2] | RevBlack — HubSpot vs Salesforce Data Model | Oct 2025 | revblack.com |
| [^12] | Inogic — Data Deduplication in CRM | Ene 2026 | inogic.com |
| [^5] | HubSpot — Understand Objects | Ene 2026 | knowledge.hubspot.com |
| [^3] | Ksolves — Master-Detail vs Lookup | Feb 2025 | ksolves.com |
| [^26] | Solace — Schema Registry Best Practices | Current | docs.solace.com |
| [^21] | Dynamics Community — Data Validation | Abr 2023 | community.dynamics.com |
| [^17] | TakeFive — MD and Lookup Relationships | Jun 2025 | takefiveconsulting.org |
| [^27] | PingCap/TiDB — Backward Compatibility Patterns | Dic 2024 | pingcap.com |
| [^22] | Roofing Business Partner — CRM Data Quality | Abr 2023 | roofingbusinesspartner.com |
| [^16] | Salesforce — Object Relationships | Ago 2025 | developer.salesforce.com |
| [^28] | DataExpert.io — Backward Compatibility Guide | Feb 2026 | dataexpert.io |
| [^23] | DCKAP — CRM Data Quality Best Practices | Oct 2025 | dckap.com |
| [^14] | Optif.ai — CRM Migration 14-Day Checklist | Dic 2025 | optif.ai |
| [^10] | Paciolan — Golden Record | Abr 2024 | paciolan.com |
| [^8] | Salesforce — Data Model ERDs | Ene 2026 | developer.salesforce.com |
| [^11] | Redpoint Global — Identity Resolution | Oct 2024 | redpointglobal.com |
| [^9] | Salesforce Architect — Data Model Notation | Current | architect.salesforce.com |
| [^6] | SmallBuilder — Junction Objects Salesforce | Sep 2024 | smallbuilder.com |
| [^30] | NMS Consulting — Data Governance Operating Model | Dic 2025 | nmsconsulting.com |
| [^7] | SalesforceBen — Junction Objects | Jul 2024 | salesforceben.com |
| [^29] | Agile Seekers — Schema Evolution | May 2025 | agileseekers.com |
| [^20] | RecordLinker — Data Warehouse Naming Standards | Jun 2024 | recordlinker.com |

---

## References

1. [HubSpot Custom Objects and Properties: A Complete Guide to CRM ...](https://www.hyphadev.io/blog/complete-guide-hubspot-crm-data-architecture) - Custom objects unlock many-to-many relationships that standard objects cannot support, enabling comp...

2. [HubSpot vs Salesforce: the most important data model differences ...](https://www.revblack.com/articles/data-model-differences-hubspot-salesforce) - HubSpot's data model: the Contact at the center · Contacts represent individual people. · Deals trac...

3. [Master-Detail vs Lookup Relationships in Salesforce - Ksolves](https://www.ksolves.com/blog/salesforce/master-detail-vs-lookup-relationship) - Master-detail and lookup relationships are the two most common types of data relationships used in S...

4. [Understand the HubSpot CRM Structure in 7 Minutes - HS Simple](https://hs-simple.com/en/blog/setup-guide/hubspot-crm-structure) - Here, we deal with objects. Objects are fundamental components in HubSpot, representing different ty...

5. [Understand objects - HubSpot Knowledge Base](https://knowledge.hubspot.com/records/understand-objects) - You can associate records of different objects (e.g., companies and deals) or same objects (e.g., co...

6. [An Explanation of Junction Objects in Salesforce - SmallBuilder blog](https://blog.smallbuilder.com/an-explanation-of-junction-objects-in-salesforce/) - Learn to model many-to-many relationships in Salesforce using junction objects and when to choose th...

7. [What is a Junction Object in Salesforce?](https://www.salesforceben.com/what-is-a-junction-object-in-salesforce/) - A Salesforce Junction Object provides a way to create a many-to-many relationship between Salesforce...

8. [Data Model | Object Reference for the Salesforce Platform](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/data_model.htm) - Entity relationship diagrams (ERDs) for standard Salesforce objects illustrate important relationshi...

9. [Salesforce Data Model Notation | Reference Diagrams](https://architect.salesforce.com/docs/architect/reference-diagrams/guide/data-model-notation.html) - This document provides an overview of Salesforce entity relationship diagram (ERD) notation and conv...

10. [Mastering Customer Data: The Power of the Golden Record - Paciolan](https://www.paciolan.com/post/mastering-customer-data-the-power-of-the-golden-record) - Today, we will dive into the power of Master Data Management (MDM) by harnessing the golden record w...

11. [What is Identity Resolution? - Redpoint Global](https://www.redpointglobal.com/blog/what-is-identity-resolution/) - Identity resolution is the process of finding, cleansing, matching, merging and relating every dispa...

12. [Data Deduplication in CRM - Inogic](https://www.inogic.com/product/productivity-apps/data-deduplication-crm/) - Understand data deduplication in CRM, the causes of duplicate records, and how they impact data qual...

13. [An Expert Guide to a HubSpot Salesforce Integration](https://blog.revpartners.io/en/revops-articles/an-expert-guide-to-a-hubspot-salesforce-integration) - In HubSpot: Go to Data Management > Data Model Overview; HubSpot doesn't use conversion flows—object...

14. [Zero-Downtime CRM Migration — 14-Day Checklist + Framework ...](https://optif.ai/media/articles/crm-data-migration-checklist/) - This comprehensive checklist breaks down the exact 5-phase process used by 200+ companies to migrate...

15. [Utilizar el generador de modelos de datos - HubSpot Knowledge Base](https://knowledge.hubspot.com/es/data-management/use-the-data-model-builder) - En tu CRM de HubSpot, los objetos representan a tus clientes y la información del proceso de negocio...

16. [Relationships Among Standard Objects and Fields](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/relationships_among_objects.htm) - To view the parent and child relationships among standard objects, see the ERD diagrams in Data Mode...

17. [Master-Detail and Lookup Relationships in Salesforce](https://www.takefiveconsulting.org/master-detail-and-lookup-relationships-in-salesforce/) - In Salesforce, a Master-Detail relationship is a tightly coupled relationship between two objects. O...

18. [Entity Relationship Diagrams in Salesforce - LinkedIn](https://www.linkedin.com/pulse/entity-relationship-diagrams-salesforce-yadhu-krishnan-wn24c) - They provide a visual representation of the relationships between different objects (standard and cu...

19. [CRM customization: choosing between custom objects & custom ...](https://www.engaging.io/en/blog/crm-customization-choosing-between-custom-objects-custom-properties) - Best practices · Validate existing properties: Before creating a custom property, ensure that a prop...

20. [Data Warehouse Design: Naming Standards - RecordLinker](https://recordlinker.com/data-warehouse-standards/) - Lack of standardized naming conventions and fragmented data pose significant challenges to data gove...

21. [Improving CRM Data Quality with Automated Data Validation](https://community.dynamics.com/blogs/post/?postid=4fc913e3-6d41-ee11-bdf3-000d3a4e5de0) - Automated data validation is a powerful tool for improving the quality of your CRM data. By implemen...

22. [Mastering CRM Data Quality: 7 Key Strategies for Success](https://www.roofingbusinesspartner.com/blog/mastering-crm-data-quality-7-key-strategies-for-success) - Data validation rules serve as checkpoints for identifying errors and inconsistencies during the dat...

23. [11 CRM Data Quality Best Practices You Must Know - DCKAP](https://www.dckap.com/blog/crm-data-quality-best-practices/) - Implement validation rules within your CRM application, such as mandatory fields, format checks, and...

24. [Data Migration Strategy | Best Practices for CRM and AMS Users](https://cobalt.net/cobalts-crm-data-migration-best-practices/) - Data migration strategies must account for the efficient extraction, transformation, and loading (ET...

25. [CRM Data Migration Checklist: 10 Steps for a Strategic Move](https://velvetech.com/blog/crm-data-migration-checklist/) - Utilize data deduplication tools: They can quickly identify and automatically remove or merge duplic...

26. [Best Practices for Evolving Schemas in Schema Registry](https://docs.solace.com/Schema-Registry/schema-registry-best-practices.htm) - Backward Compatibility. Backward compatibility ensures that newer consumers can process data produce...

27. [Database Design Patterns for Ensuring Backward Compatibility - TiDB](https://www.pingcap.com/article/database-design-patterns-for-ensuring-backward-compatibility/) - Ensure backward compatibility in your database with design patterns for versioning, schema evolution...

28. [Backward Compatibility in Schema Evolution: Guide - DataExpert.io](https://www.dataexpert.io/blog/backward-compatibility-schema-evolution-guide) - Pro Tip: Always upgrade consumers before producers for backward-compatible updates. For long-term co...

29. [Managing Schema Evolution in Data-Intensive Product Features](https://agileseekers.com/blog/managing-schema-evolution-in-data-intensive-product-features) - Ensure that schema changes are backward compatible wherever possible. For example, adding a new opti...

30. [Data Governance Operating Model: Products, Quality KPIs, and ...](https://nmsconsulting.com/data-governance-operating-model/) - Includes data owner vs. steward, a governance council, operating model template, examples, and a PDF...

