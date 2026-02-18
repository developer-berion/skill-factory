<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_05_Context_By_Location_Territory.md

“Diseña CRM ‘context-aware’: qué información priorizar según país/ciudad/tienda/territorio + rol. Incluye: moneda/idioma/formatos, compliance regional (ej. GDPR), y reglas de priorización (pseudoregla). Da ejemplos: ventas por territorios, operaciones por sucursales, soporte por región.”

Diseña tu CRM “context-aware” como una capa de **políticas** que, según (país/ciudad/tienda/territorio + rol), decide: qué campos mostrar primero, qué validaciones aplicar, qué permisos exigir y qué alertas disparar.

## Modelo de contexto (mínimo viable)

**Dimensiones de contexto**

- Ubicación: país → ciudad → sucursal/tienda (o punto de venta/operación) → zona operativa.
- Territorio comercial: región/vertical → cartera → ruta/ejecutivo (territory management es precisamente “enfocar reps por áreas de responsabilidad” con modelos de territorio).[^1]
- Rol: ventas, operaciones, soporte, finanzas/riesgo, admin.

**Entidades (qué incluye)**

- Cuenta (agencia B2B) + sucursales/filiales.
- Contactos (por rol del cliente: dueños, counter, pagos, emergencias).
- Oportunidad/Reserva (cotización → confirmación → postventa).
- Caso (soporte) + SLA.
- Territorio (asignación, cobertura, reglas de ruteo).

**Qué no incluye (para evitar “CRM Frankenstein”)**

- Contabilidad completa (solo “output” necesario: totales, impuestos estimados, estado de cobro).
- Motor de pricing avanzado (solo “inputs” y “decisiones” clave: margen objetivo, límites, overrides).
- Documentos sensibles sin control (si se almacenan, debe ser repositorio con permisos y auditoría).

**Qué es sensible (y debe tratarse como “alto riesgo”)**

- Identificadores oficiales (pasaporte/ID), datos de pago, geolocalización precisa, credenciales, y cualquier dato personal que active obligaciones legales de privacidad/seguridad (ej. CPRA amplía “sensitive personal information”).[^2][^3]


## Información a priorizar por ubicación/territorio

Regla práctica: “lo que cambia con la geografía va primero”; lo estable va después.


| Contexto | Prioriza (arriba del todo) | Formatos/moneda/idioma | Sensibles / cuidado |
| :-- | :-- | :-- | :-- |
| País | Moneda base + moneda de cobro; métodos de pago válidos; reglas de facturación; impuestos/retenciones; riesgo (fraude/chargebacks) | Moneda y redondeos; idioma por defecto; formato fecha (dd/mm vs mm/dd); teléfonos (prefijo) | Campos KYC/identidad: visibles solo a roles autorizados; logs obligatorios |
| Ciudad | Horario local; cut-offs operativos; aeropuertos cercanos; tiempos de entrega de vouchers; contactos de proveedores locales | Zona horaria; dirección normalizada | Direcciones completas solo si el rol las necesita (operaciones/soporte) |
| Sucursal/tienda | Inventario operativo (qué puede vender/emitir); responsables; límites de descuento; caja/tesorería | Plantillas de email/WhatsApp por sucursal; firma comercial local | Evitar que ventas vea datos de pago si no cobra |
| Territorio comercial | Cartera asignada; potencial (MRR/volumen); estado de relación; “next best action” | Idioma por mercado; guiones por territorio | Notas internas de riesgo (fraude, mora) con permisos estrictos |
| Rol (capa transversal) | Ventas: pipeline+margen; Operaciones: checklists+fechas; Soporte: SLA+historial; Finanzas/riesgo: aging+método de cobro | UI/formatos cambian por rol (no solo por país) | “Need-to-know”: mostrar lo mínimo necesario por rol |

## Compliance regional (ejemplos concretos)

No necesitas convertir el CRM en “legal-tech”, pero sí codificar disparadores y restricciones.

- **GDPR (UE)**: aplica si procesas datos en el contexto de un establecimiento en la UE, o si (aunque estés fuera) ofreces bienes/servicios a personas en la UE o monitoreas su comportamiento en la UE.[^4][^5]
- **LGPD (Brasil)**: es la ley brasileña de protección de datos (Lei 13.709/2018) y regula operaciones de tratamiento de datos personales en Brasil; además, guías prácticas suelen resumir criterios de aplicación cuando el tratamiento ocurre en Brasil, se orienta a individuos en Brasil o los datos se recolectaron allí.[^6][^7]
- **CCPA/CPRA (California)**: otorga derechos como conocer, borrar, optar por no venta/compartición, corregir, y limitar uso/divulgación de información sensible (CPRA).[^3]

“Checks” simples que sí conviene implementar:

- Clasificación de datos (personal / sensible / operativo no personal) para permisos y retención.
- Registro de base legal/consentimiento cuando aplique (campo + timestamp + fuente).
- Gestión de solicitudes del titular (acceso/borrado/corrección) en forma de “caso” con SLA (especialmente útil para CCPA/CPRA).[^3]


## Reglas de priorización (pseudoreglas) + ejemplos

### Pseudoreglas (plantilla)

- `context = {country, city, branch, territory, role, channel, customer_tier, risk_level}`
- `UI.priority = sort(fields, weight(role) + weight(country) + weight(territory) + weight(risk))`
- `currency = if opportunity.currency set else country.default_currency`
- `language = if contact.language set else country.default_language`
- `show(field) = role.hasPermission(field.classification) AND (country.allows(field) OR field.isOperational)`
- `require(field) = (role in [Ops, Finance] AND stage in [Confirm, Ticketed]) OR (risk_level == High)`
- `block(action) = (discount > territory.max_discount) OR (payment_method not in country.allowed_methods)`


### Ejemplo 1: Ventas por territorios (B2B agencias)

- Si el ejecutivo abre una cuenta del territorio “Andina”, arriba ve: margen objetivo del territorio, límite de descuento, score de riesgo de la agencia, aging de deuda y próximos vencimientos; abajo deja “info bonita” (redes, notas largas).
- Si el territorio tiene regla “cobro anticipado” para agencias nuevas, el CRM marca la oportunidad como “no confirmable” hasta que Finanzas valide (control de riesgo antes de emitir).


### Ejemplo 2: Operaciones por sucursales

- Al pasar una reserva a “Confirmada”, Operaciones ve checklist específico por sucursal (cut-off, responsables, proveedores preferidos) y fechas en la zona horaria local (reduce errores de horario).
- Si la sucursal no puede emitir cierto producto (por contrato o capacidad), el CRM bloquea la tarea de emisión y propone ruta alternativa (otra sucursal o central).


### Ejemplo 3: Soporte por región

- Al crear un caso desde Colombia, el CRM asigna cola regional, aplica SLA y plantillas en español neutro; si entra desde un país con alta tasa de fraude, prioriza verificación antes de reembolsos.
- Si el caso involucra datos sensibles (pasaporte/pago), el CRM fuerza canal seguro, limita visibilidad a soporte senior y registra auditoría (alineado con el enfoque de “sensitive personal information” en CPRA).[^2][^3]

Si me dices tus territorios reales (p. ej., VE/CO/Caribe/USA), roles internos y 10 campos “críticos” de tu venta B2B, te lo devuelvo como un esquema de configuración (JSON) listo para implementar en tu CRM actual.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://help.salesforce.com/s/articleView?id=sales.tm2_territory_mgmt_concepts_managing.htm\&language=es_MX\&type=5

[^2]: https://legal.thomsonreuters.com/blog/key-aspects-of-california-privacy-rights-act-cpra/

[^3]: https://oag.ca.gov/privacy/ccpa

[^4]: https://gdpr-info.eu/art-3-gdpr/

[^5]: https://www.edpb.europa.eu/sites/default/files/files/file1/edpb_guidelines_3_2018_territorial_scope_after_public_consultation_en_1.pdf

[^6]: https://en.wikipedia.org/wiki/General_Personal_Data_Protection_Law

[^7]: https://secureprivacy.ai/blog/lgpd-compliance-requirements

[^8]: https://www.wiley.law/newsletter-May_2017_PIF-The_GDPRs_Reach-Material_and_Territorial_Scope_Under_Articles_2_and_3

[^9]: https://rgpd.com/gdpr/chapter-1-general-provisions/article-3-territorial-scope/

[^10]: https://www.privacyworld.blog/2019/12/territorial-scope-of-the-gdpr-following-edpbs-final-guidelines-part-2/

[^11]: https://gdpr-text.com/en/read/article-3/

[^12]: https://usercentrics.com/knowledge-hub/brazil-lgpd-general-data-protection-law-overview/

[^13]: https://www.caprivacy.org/cpra-text/

[^14]: https://securiti.ai/infographics/the-intersection-of-gdpr-article-3-and-chapter-v-real-world-scenarios-of-international-data-transfers/

[^15]: https://www.dlapiperdataprotection.com/index.html?t=law\&c=BR

