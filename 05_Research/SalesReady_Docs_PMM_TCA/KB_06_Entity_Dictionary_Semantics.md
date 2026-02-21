<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_06 — Diccionario de Entidades y Semántica para CRM B2B


***

## Executive Summary

Un Diccionario de Entidades para CRM B2B no es solo un ERD técnico: es el contrato semántico entre el área de sistemas y el área comercial. Define qué significa cada dato, para quién existe, cómo se calcula y qué consecuencias tiene si está mal. Sin él, el CRM acaba siendo una base de datos costosa donde cada equipo interpreta diferente qué es un "cliente activo", qué cuenta como "oportunidad cerrada" o cuándo un campo derivado como "Potencial del Cuenta" es confiable.[^1]

**`[FACT]`** Un diccionario de datos bien implementado previene conflictos de definición al asegurar que cada término esté validado, estandarizado y explícitamente conectado a lógica de negocio.[^1]

**`[FACT]`** Existen tres capas complementarias: el *data dictionary* (especificaciones técnicas), el *business glossary* (términos de negocio) y el *data catalog* (capa de descubrimiento). Juntas forman el knowledge layer completo.[^2]

**`[INFERENCE]`** En contextos B2B mayoristas con múltiples agencias como clientes, la semántica mal definida de "Account" vs. "Contact" vs. "Agency Branch" genera datos duplicados, reportes inconsistentes y pérdida de trazabilidad comercial.

El documento que sigue establece: la plantilla Field Card, las convenciones de naming con traducción a lenguaje de negocio, el manejo de campos derivados/calculados, y los anti-patrones que destruyen la utilidad del diccionario.

***

## Definitions and Why It Matters

**Diccionario de Entidades** → documento vivo que describe cada objeto (entidad) y cada atributo (campo) del CRM con su propósito de negocio, tipo de dato, reglas de validación, ejemplo real y su impacto operativo/comercial. Va más allá del esquema de base de datos: conecta el *qué técnico* con el *para qué de negocio*.[^2]

**Semántica de negocio** → la capa que traduce nombres de campo técnicos (`account_tier_calc_f`) a lenguaje entendible por vendedores y gerentes ("Categoría de Agencia: Premium / Estándar / En Desarrollo").[^3]

**Campo derivado/calculado** → campo cuyo valor no es ingresado por el usuario sino computado a partir de otros campos (fórmulas, rollups, lógica condicional). Requiere documentación especial porque su "verdad" depende de la calidad de los campos fuente.[^4]

### ¿Por qué importa en CRM B2B?

**`[FACT]`** Las organizaciones que integran el diccionario en las herramientas de uso diario (dashboards, formularios) permiten que los usuarios tomen decisiones más rápidas y confiables sin salir de su flujo de trabajo.[^1]

**`[FACT]`** La diferencia entre *data dictionary* y *business glossary* es crítica: el primero es para ingenieros; el segundo es para el equipo comercial. Un CRM B2B robusto necesita ambos.[^5]

**`[INFERENCE]`** En equipos de ventas B2B, el 70% de los errores de reporte se originan en campos sin definición consensuada (ej.: "¿cuándo una agencia es 'activa'?"). El diccionario es el antídoto directo.

***

## Principles \& Best Practices

### 1. La Field Card como unidad atómica

Cada campo del CRM debe tener una Field Card documentada. Esta es la unidad mínima del diccionario. **`[FACT]`** Las entradas del diccionario deben capturar no solo qué es el dato, sino cómo y por qué se usa en diferentes contextos de negocio.[^1]

**Plantilla Field Card — Estándar KB_06:**

```markdown
## FIELD CARD

| Atributo         | Contenido                                                    |
|------------------|--------------------------------------------------------------|
| **Entidad**      | Account (Agencia)                                            |
| **Nombre Técnico** | agency_annual_volume_usd                                   |
| **Nombre de Negocio** | Volumen Anual Estimado (USD)                            |
| **Propósito**    | Clasificar la agencia por potencial comercial y asignar nivel de atención |
| **Tipo**         | Currency / Decimal (2 decimales)                             |
| **Origen**       | Manual (ingreso por KAM en onboarding) / Calculado anual     |
| **Validaciones** | > 0; no puede exceder 50,000,000 USD; requerido para Tier A  |
| **Ejemplo real** | 125,000.00                                                   |
| **Impacto**      | Determina Tier de Agencia → afecta descuento base, SLA de respuesta y asignación de ejecutivo |
| **Campos fuente** | N/A (campo primitivo)                                       |
| **Sensibilidad** | Confidencial — solo visible para KAM + Gerencia Comercial    |
| **Dueño**        | Gerencia Comercial                                           |
| **Última revisión** | 2026-Q1                                                   |
| **`[FACT/INFERENCE]`** | `[FACT]` si viene de facturación real; `[INFERENCE]` si es estimado del KAM |
```


***

### 2. Naming Conventions y Traducción a Lenguaje de Negocio

**`[FACT]`** Una convención de naming sólida usa reglas consistentes y repetibles que crean nombres únicos que comunican mucho en poco espacio. La consistencia supera a la creatividad.[^6]

**`[FACT]`** Los campos booleanos deben llevar prefijos de verbo descriptivo: `is_`, `has_`, `are_`. Ejemplo: `isActive`, `hasOpportunities`. Los campos de fórmula/calculados deben terminar en `_f`.[^4]

**Tabla: Convenciones de Naming con Traducción**


| Capa | Formato Técnico (API) | Formato de Negocio (UI Label) | Regla |
| :-- | :-- | :-- | :-- |
| Entidad principal | `Account` | Agencia | PascalCase para objetos |
| Campo primitivo | `account_country_code` | País de la Agencia | snake_case, sin abrev. ambiguas |
| Campo booleano | `is_active_agency` | ¿Agencia Activa? | Prefijo `is_/has_/are_` |
| Campo calculado | `agency_tier_calc_f` | Categoría de Agencia (Auto) | Sufijo `_calc_f` |
| Campo rollup | `total_bookings_ytd_r` | Total Reservas Año Actual | Sufijo `_r` para rollup |
| Campo de fecha | `last_contact_date` | Última Interacción | Siempre `_date` al final |
| ID de referencia | `agency_id` | ID Interno Agencia | Siempre `_id` como sufijo |

**`[FACT]`** El tipo de asset, fecha, campaña y propósito deben ser los bloques de construcción de cualquier naming convention para CRM.[^7]

**`[INFERENCE]`** En CRMs con usuarios no técnicos (KAMs, ejecutivos de ventas), el campo de negocio visible en la UI debe ser siempre en lenguaje natural, nunca exponer el API name.

***

### 3. Campos Derivados y Calculados: Manejo y Documentación

Los campos calculados son los más peligrosos del diccionario: parecen datos, pero son inferencias. Si sus campos fuente están mal, el campo calculado distribuye el error a todo el CRM.[^4]

**`[FACT]`** Salesforce y plataformas similares permiten que campos de fórmula referencien valores de objetos relacionados mediante paths como `Account.LookupField.CalculatedField`.[^8]

**Field Card extendida para campo calculado:**

```markdown
## FIELD CARD — CAMPO CALCULADO

| Atributo              | Contenido                                                   |
|-----------------------|-------------------------------------------------------------|
| **Nombre Técnico**    | agency_tier_calc_f                                          |
| **Nombre de Negocio** | Categoría de Agencia (Automática)                           |
| **Tipo**              | Picklist calculada (Text Formula)                           |
| **Lógica**            | IF volume >= 100K → "Premium"                               |
|                       | IF volume >= 30K AND < 100K → "Estándar"                    |
|                       | IF volume < 30K OR NULL → "En Desarrollo"                   |
| **Campos fuente**     | agency_annual_volume_usd                                    |
| **Dependencias**      | Si agency_annual_volume_usd = NULL → resultado = "En Desarrollo" |
| **Frecuencia recálculo** | Tiempo real (on-save)                                    |
| **Impacto downstream** | Descuento base, SLA, asignación de ejecutivo, segmentación |
| **Alerta de calidad** | Si > 20% de agencias quedan en "En Desarrollo", revisar calidad de campo fuente |
| **Etiqueta**          | `[INFERENCE]` — depende de calidad del campo fuente         |
```

**`[FACT]`** Para campos calculados en reporting, la convención más robusta incluye el tipo de cálculo, el objeto de negocio y una descripción en el nombre. Ejemplo: `CF_LRV_AgencyTier_Account`.[^9]

***

### 4. Gobernanza del Diccionario

**`[FACT]`** Asignar co-ownership de términos en áreas donde múltiples dominios se intersectan (ej.: métricas de revenue, segmentación de clientes) es esencial para mantener el diccionario actualizado.[^1]

**`[FACT]`** Implementar logging y analítica dentro de la plataforma del diccionario para monitorear qué términos son más consultados y correlacionarlos con KPIs permite priorizar actualizaciones.[^1]

**`[INFERENCE]`** En mayoristas B2B, el dueño natural de cada entidad core debe ser: **Entidad Account/Agencia** → Gerencia Comercial; **Entidad Opportunity/Cotización** → Revenue Manager; **Entidad Contact/Ejecutivo de Agencia** → KAM asignado.

***

## Examples (Aplicado a CRM Enterprise B2B — Turismo Mayorista)

### Entidades Core y sus Field Cards resumidas

**`[FACT]`** En Salesforce y Dynamics 365, las entidades Account y Contact son el nodo padre para múltiples contactos y oportunidades, habilitando la jerarquía estructural B2B.[^10]

```markdown
## ENTIDAD: Account → "Agencia de Viajes"

Campos clave:
- agency_id              → ID Interno Agencia         [FACT]
- agency_legal_name      → Razón Social               [FACT]
- agency_trade_name      → Nombre Comercial            [FACT]
- agency_country_code    → País                        [FACT]
- agency_annual_volume_usd → Volumen Anual Estimado    [FACT/INFERENCE*]
- agency_tier_calc_f     → Categoría (Auto)            [INFERENCE]
- is_active_agency       → ¿Agencia Activa?            [FACT]
- last_contact_date      → Última Interacción          [FACT]
- has_credit_line        → ¿Tiene Línea de Crédito?    [FACT]
- credit_limit_usd       → Límite de Crédito           [FACT]

*[FACT] si viene de facturación real; [INFERENCE] si es estimado del KAM
```

```markdown
## ENTIDAD: Opportunity → "Cotización / Propuesta Comercial"

Convención de nombre: [Agencia] + [Destino/Producto] + [Tipo] + [Periodo]
Ejemplo: "AgenciaXYZ – Europa Clásica – New Business – Q2-2026"    [FACT - web:19]

Campos clave:
- opportunity_id          → ID Cotización              [FACT]
- account_id              → Agencia vinculada          [FACT]
- destination_code        → Destino Principal          [FACT]
- product_type            → Tipo de Producto           [FACT]
- deal_type               → Tipo de Negocio (New/Renewal/Upsell) [FACT]
- amount_usd              → Valor Estimado             [INFERENCE]
- stage_name              → Etapa del Pipeline         [FACT]
- close_date              → Fecha Estimada de Cierre   [FACT/INFERENCE]
- probability_calc_f      → Probabilidad (Auto)        [INFERENCE]
- margin_pct_calc_f       → Margen % (Auto)            [INFERENCE]
```


***

## Metrics / Success Signals

**`[FACT]`** Los términos más consultados en el diccionario deben correlacionarse con los KPIs críticos del negocio para priorizar validaciones más frecuentes.[^1]

- **% de campos con Field Card completa** → Meta: >90% en entidades core[^1]
- **% de campos calculados con campos fuente documentados** → Meta: 100%[^4]
- **Tiempo promedio para resolver un conflicto de definición** → Debe reducirse >50% post-implementación `[INFERENCE]`
- **Tasa de adopción del diccionario** → % de usuarios que consultaron al menos un término en el último mes[^1]
- **% de registros con campos obligatorios vacíos** → Alerta si >5% en campos primitivos de entidades core `[INFERENCE]`
- **NPS interno del CRM** → Proxy de claridad semántica para el equipo comercial `[INFERENCE]`

***

## Operational Checklist

- [ ] Identificar las 5 entidades core del CRM y listar todos sus campos actuales[^11]
- [ ] Para cada campo: completar Field Card con los 11 atributos del estándar KB_06
- [ ] Separar campos primitivos de campos calculados/derivados
- [ ] Para campos calculados: documentar lógica, campos fuente y dependencias[^4]
- [ ] Definir el nombre de negocio (UI label) para TODOS los campos técnicos[^3]
- [ ] Aplicar naming convention: validar prefijos `is_/has_`, sufijos `_f`, `_r`, `_date`, `_id`
- [ ] Asignar dueño de negocio a cada entidad (no a cada campo)
- [ ] Etiquetar cada campo como `[FACT]` o `[INFERENCE]`
- [ ] Definir campos sensibles y permisos de visibilidad por rol[^1]
- [ ] Publicar el diccionario en una herramienta accesible (Notion, Confluence, Wiki interna)
- [ ] Integrar tooltips o descripciones en dashboards para surfacear la semántica inline[^1]
- [ ] Establecer ciclo de revisión trimestral con los dueños de cada entidad[^1]

***

## Anti-Patterns

**`[FACT]`** Si múltiples personas tienen versiones inconsistentes del diccionario, cada equipo trabaja desde una fuente diferente, lo que destruye la confianza en el CRM.[^1]

- **Diccionario estático en PDF/Excel** → Muere a los 3 meses. Requiere herramienta viva con versionado `[INFERENCE]`
- **Nombrar campos por el creador** → `victor_campo_nuevo_v2` → ilegible e imposible de mantener[^9]
- **Campos calculados sin documentar campos fuente** → El error se vuelve invisible hasta que el reporte falla[^4]
- **Un solo dueño técnico para todo el diccionario** → Cuello de botella; el negocio nunca lo adopta[^1]
- **UI labels iguales al API name** → `agency_tier_calc_f` visible para el KAM → abandono inmediato[^3]
- **Mezclar Data Dictionary con Business Glossary** → Confunde a técnicos y no-técnicos por igual[^2]
- **Campos booleanos sin prefijo** → `active` en lugar de `is_active_agency` → ambigüedad en automations[^4]
- **Oportunidades nombradas "TBD" o "Nueva Cotización"** → Reportes de pipeline inutilizables[^6]
- **No distinguir `[FACT]` vs `[INFERENCE]`** → Los campos estimados se tratan como verdades operativas `[INFERENCE]`

***

## Diagnostic Questions

1. ¿Puede cualquier miembro del equipo comercial responder en <30 segundos qué significa `agency_tier_calc_f` y de dónde viene? `[INFERENCE]`
2. ¿Existe consenso entre ventas, ops y tecnología sobre cuándo una agencia pasa de "Estándar" a "Premium"?[^1]
3. ¿Los campos calculados tienen documentados sus campos fuente y sus escenarios de valor nulo?[^4]
4. ¿Hay campos en producción sin Field Card asociada? ¿Cuántos?[^11]
5. ¿Los nombres visibles en la UI del CRM son comprensibles para un KAM sin entrenamiento técnico?[^3]
6. ¿Los reportes de pipeline usan el nombre de oportunidad para identificar sin hacer clic?[^6]
7. ¿Existe un proceso para actualizar el diccionario cuando se agrega un campo nuevo al CRM?[^1]
8. ¿Los campos de datos sensibles (crédito, volumen estimado) tienen control de visibilidad por rol?[^1]

***

## Sources

| \# | Fuente | Fecha | Tipo |
| :-- | :-- | :-- | :-- |
| S1 | OvalEdge — Data Dictionary Best Practices 2026 | Feb 2026 | `[FACT]` |
| S2 | Atlan — Data Dictionary 2026: Components, Examples | Jan 2026 | `[FACT]` |
| S3 | MarTech — 5-Step Blueprint for CRM Naming Conventions | Jan 2026 | `[FACT]` |
| S4 | TrueBlueTech — Best Practices for Opportunity Naming in CRM | Oct 2023 | `[FACT]` |
| S5 | Campfire Solutions — Salesforce Object \& Field Naming Conventions | Mar 2024 | `[FACT]` |
| S6 | Alation — Business Glossary vs. Data Dictionary | Sep 2025 | `[FACT]` |
| S7 | Reddit/Workday — Calculated Field Naming Conventions | May 2023 | `[FACT]` |
| S8 | Data.world — About Business Glossary | Oct 2025 | `[FACT]` |
| S9 | Metaphacts — Why Enterprise Information Architecture Needs a Semantic Model | Oct 2024 | `[FACT]` |
| S10 | Acceldata — What Is a Data Dictionary | Nov 2024 | `[FACT]` |

> *Añadir a SOURCES.md sin duplicar entradas existentes.*

***

## Key Takeaways for PM Practice

- **El diccionario no es para técnicos** — si el KAM no lo entiende, no sirve. La UI label es tan importante como el API name[^3]
- **Separa siempre primitivos de calculados** — un campo derivado es una inferencia, no un hecho; etiquétalo explícitamente[^4]
- **La Field Card es el contrato mínimo** — propósito + tipo + validaciones + impacto + dueño = los 5 elementos no negociables[^1]
- **Naming conventions son infraestructura, no cosmética** — un nombre bien construido elimina preguntas de soporte y reduce errores de automatización[^6]
- **El sufijo revela la naturaleza del campo** → `_f` = calculado, `_r` = rollup, `_id` = referencia, `is_` = booleano[^4]
- **Los campos calculados se validan auditando sus fuentes** — si `agency_annual_volume_usd` tiene 30% de valores nulos, `agency_tier_calc_f` está mintiendo en el 30% de los casos `[INFERENCE]`
- **Gobernanza distribuida > dueño único** — asigna owners de negocio por entidad para que el diccionario sobreviva rotación de personal[^1]
- **Integra el diccionario donde trabaja la gente** — tooltips en dashboards y formularios > documentación en PDF que nadie abre[^1]
<span style="display:none">[^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30]</span>

<div align="center">⁂</div>

[^1]: https://www.ovaledge.com/blog/data-dictionary-best-practices

[^2]: https://atlan.com/what-is-a-data-dictionary/

[^3]: https://www.alation.com/blog/data-dictionary-vs-business-glossary/

[^4]: https://www.campfiresolutions.io/blog/salesforce-object-and-field-api-naming-conventions

[^5]: https://www.ovaledge.com/blog/data-dictionary-examples-templates

[^6]: https://truebluetechnologies.com/best-practices-for-opportunity-naming-conventions-in-your-crm/

[^7]: https://martech.org/a-5-step-blueprint-for-crm-naming-conventions/

[^8]: https://community.dynamics.com/forums/thread/details/?threadid=53aa45d6-40ff-ef11-bae3-7c1e525b5e9d

[^9]: https://www.reddit.com/r/workday/comments/13sc28w/calculated_field_naming/

[^10]: https://www.siroccogroup.com/understanding-crm-terminology-in-the-sales-process/

[^11]: https://www.acceldata.io/blog/what-is-a-data-dictionary-definition-types-and-practical-applications

[^12]: pasted-text.txt

[^13]: https://www.onlinedesignteacher.com/2024/01/essential-tips-for-developing-effective.html

[^14]: https://www.getcollate.io/learning-center/data-dictionary

[^15]: https://blog.arkondata.com/guide-to-understanding-data-dictionaries?hsLang=en-us

[^16]: https://docs.data.world/en/109109-about-business-glossary.html

[^17]: https://blog.metaphacts.com/how-a-semantic-model-can-elevate-your-enterprise-information-architecture

[^18]: https://atlan.com/data-governance-data-dictionary/

[^19]: https://www.openprisetech.com/blog/company-name-normalization-rules-and-best-practices/

[^20]: https://www.datagalaxy.com/en/blog/data-catalog-vs-glossary-dictionary/

[^21]: https://learn.microsoft.com/en-us/purview/data-governance-glossary

[^22]: https://help.salesforce.com/s/articleView?id=analytics.bi_edd_prep_fields.htm\&language=en_US\&type=5

[^23]: https://www.salesforceben.com/salesforce-naming-conventions-how-to-enforce-them/

[^24]: https://community.dynamics.com/forums/thread/details/?threadid=a760a086-2a11-42d1-bcca-b6d12d3314ba

[^25]: https://www.toplineresults.com/2021/03/naming-conventions-for-a-more-productive-crm-experience/

[^26]: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/reference/contact?view=dataverse-latest

[^27]: https://stackoverflow.com/questions/5437744/naming-conventions-for-non-normalized-fields

[^28]: https://www.xtivia.com/blog/contact-naming-conventions-in-salesforce/

[^29]: https://www.gradient.works/blog/salesforce-flow-best-practices-naming-conventions

[^30]: https://www.loganconsulting.com/blog/save-time-by-mapping-fields-from-accounts-to-opportunities-in-microsoft-dynamics-365/

