<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_05_Security_RBAC_Multitenancy_AuditLogs — Seguridad en SaaS multi-tenant

## Executive summary (10–15 líneas)

**Facts:** En SaaS multi-tenant, el riesgo principal es el *cross-tenant data leak* (que un usuario/servicio lea o modifique datos de otro tenant) y se materializa sobre todo por fallas de autorización a nivel objeto/registro en APIs.[^1]
**Facts:** OWASP API Security Top 10 (2023) pone como riesgo \#1 “Broken Object Level Authorization (BOLA)”, que ocurre cuando endpoints usan IDs y no validan autorización por objeto.[^1]
**Facts:** Para multi-tenancy, OWASP recomienda tratar el aislamiento de tenant como una preocupación de seguridad transversal (arquitectura, datos, identidad, operaciones).[^2]
**Facts:** ABAC (según NIST SP 800-162) evalúa reglas contra atributos del sujeto/objeto/entorno para permitir/denegar accesos, y se usa para control más fino y dinámico.[^3][^4]
**Facts:** El logging de seguridad debe capturar “quién/hizo qué/dónde/cuándo/resultado”, y además exige protección (restricción de acceso, monitoreo de accesos a logs, detección de manipulación).[^5]
**Facts:** Gestión de secretos requiere rotación, trazabilidad de uso, y controles para evitar fuga en CI/CD (forks/copias) y reutilización de secretos expirados.[^6]
**Inferences:** Para un CRM enterprise multi-tenant, la estrategia ganadora combina: (1) aislamiento por tenant en capa datos, (2) autorización por registro y por propiedad, (3) APIs “OWASP-first”, (4) auditoría útil para compliance y forense, (5) secretos “operables” (rotación sin downtime).
**Inferences:** Comercialmente (B2B), vender “seguridad” significa vender confianza operativa: menos incidentes, menos fricción de soporte y más retención; el audit log y el control por registro son diferenciales para cuentas enterprise y partners.

***

## Definitions and why it matters

**Facts:** *BOLA* (Broken Object Level Authorization) es cuando una API expone endpoints con identificadores de objeto y no valida autorización por cada función que accede a datos usando un ID provisto por el usuario.[^1]
**Facts:** *Broken Object Property Level Authorization* agrupa problemas de exposición/manipulación de propiedades por falta de validación de autorización a nivel de campos/propiedades.[^1]
**Facts:** *ABAC* es un modelo lógico donde la autorización se decide evaluando atributos de entidades (sujeto/objeto), operación y entorno contra políticas.[^4][^3]
**Facts:** En logging de seguridad, campos recomendados incluyen identidad del usuario, fuente, tipo/severidad de evento, resultado, razón, y metadatos del contexto; además se debe considerar enmascarar/sanitizar o cifrar partes sensibles.[^5]
**Facts:** La gestión de secretos incluye monitorear quién pidió/uso/rotó un secreto, cuándo expiró, intentos de reutilización, y errores de authn/authz asociados.[^6]
**Inferences:** *RBAC* (roles) funciona bien para “qué puede hacer alguien” (acciones), mientras ABAC suele cubrir “sobre qué datos y en qué contexto” (tenant, región, nivel de riesgo, residencia de datos, plan, etc.).
**Inferences:** “Aislamiento por tenant” no es solo un flag en la UI; debe estar garantizado por diseño en datos + servicios + observabilidad, porque el punto de falla típico son APIs internas/ETLs/jobs.

***

## Principles and best practices (con citas por sección + fecha)

### 1) Aislamiento por tenant (OWASP Multi-Tenant, s/f)

**Facts:** OWASP describe que aplicaciones multi-tenant sirven múltiples clientes desde infraestructura/código compartidos, lo que obliga a diseñar controles explícitos de seguridad para separar tenants.[^2]
**Inferences:** Define dos posturas vendibles (y operables): **Opción segura** = aislamiento fuerte (p.ej., base de datos por tenant en cuentas enterprise); **Opción agresiva** = BD compartida con controles estrictos y pruebas automatizadas anti-leak.

### 2) Autorización a nivel registro/objeto (OWASP API Top 10, 2023)

**Facts:** OWASP API Security Top 10 (2023) indica que los endpoints que manejan identificadores crean una superficie amplia de problemas de control de acceso a nivel objeto y que los chequeos de autorización deben considerarse en toda función que accede a datos usando un ID del usuario.[^1]
**Inferences:** Regla práctica: *ningún* query por ID (REST/GraphQL/SQL) sale sin “tenant scope” + “ownership/entitlement check”; si no puedes demostrarlo con tests, no está listo para enterprise.

### 3) RBAC/ABAC bien aplicado (NIST SP 800-162, 2019; guía/explicación, 2024)

**Facts:** NIST SP 800-162 define ABAC como evaluación de reglas contra atributos de sujeto/objeto/entorno para conceder o denegar acceso.[^3][^4]
**Facts:** ABAC permite políticas flexibles y decisiones que pueden cambiar entre requests si cambian atributos, habilitando control dinámico.[^3]
**Inferences:** Usa RBAC para permisos “macro” (crear deal, exportar, administrar usuarios) y ABAC para condiciones (solo región X, solo pipeline Y, solo datos no marcados como “sensitive”, solo horario/geo permitido).

### 4) OWASP API Security “by default” (OWASP API Top 10, 2023)

**Facts:** OWASP lista riesgos como Broken Authentication, Security Misconfiguration, Improper Inventory Management y Unsafe Consumption of APIs, además de BOLA y controles a nivel propiedad/función.[^1]
**Inferences:** Para PM/Producto: cada épica de API debería declarar qué riesgos OWASP cubre (mínimo: BOLA + authn + rate/resource controls + inventario/versionado).

### 5) Gestión de secretos operable (OWASP Secrets Mgmt, 2021)

**Facts:** OWASP recomienda rotación regular de secretos y controles para evitar fuga en CI/CD (por ejemplo, que forks/copias no arrastren secretos).[^6]
**Facts:** OWASP sugiere registrar quién accede al secreto, si fue aprobado, cuándo se usó, expiración, intentos de reutilización y eventos de rotación.[^6]
**Inferences:** “Secreto” incluye: API keys de integraciones, credenciales de BD, tokens de partners, claves de firma JWT; si no puedes rotarlos sin parar ventas/operación, tu riesgo comercial sube.

### 6) Auditoría y logging seguro (OWASP Logging, 2009; NIST Log Mgmt, 2021)

**Facts:** OWASP Logging Cheat Sheet detalla atributos recomendados del evento (who/what/where/result/reason/HTTP status, etc.) y también controles: restringir privilegios de lectura de logs, registrar y monitorear accesos a logs, y considerar detección de manipulación.[^5]
**Facts:** NIST (proyecto de log management) describe que SP 800-92 aborda la necesidad de una estrategia de log management, conceptos y retos, y recomienda planificación (roles/responsabilidades y políticas viables).[^7]
**Inferences:** Un audit log “vendible” para B2B debe responder rápido: qué usuario (y qué agencia/tenant) hizo qué cambio en qué registro, desde dónde, con qué resultado, y cómo lo demuestras sin exponer PII.

***

## Examples (aplicado a CRM enterprise)

**Facts:** OWASP (BOLA) exige que la autorización se valide en cada función que accede a una fuente de datos usando un ID de usuario.[^1]
**Inferences (ejemplo de diseño CRM):**

- **Modelo de datos:** todas las tablas core (Accounts, Contacts, Deals, Activities) tienen `tenant_id` obligatorio + índices compuestos (`tenant_id`, `id`) + “soft delete” auditado.
- **Control por registro (row/object-level):** `GET /deals/{dealId}` valida: (a) `deal.tenant_id == user.tenant_id`, (b) entitlement (owner/team/role), (c) condición ABAC (p.ej. `region == user.region` si aplica).
- **Control por propiedad:** en update masivo, bloquea que un rol “Sales” pueda cambiar campos como `commission_rate` o `risk_override` (si no tiene permiso), aunque el endpoint permita patch. (Esto apunta directo a *Broken Object Property Level Authorization*).[^1]
- **Auditoría:** evento `DEAL_UPDATED` guarda: actor, tenant, `deal_id`, lista de campos cambiados (sin valores sensibles), resultado, razón, request_id/correlation_id; y restringe acceso a logs y monitorea accesos.[^5]
- **Secretos e integraciones:** si el CRM integra con WhatsApp/Email/ERP, cada conector usa secretos rotables, con trazabilidad de uso/rotación y controles anti-fuga en CI/CD.[^6]

***

## Metrics / success signals

**Facts:** OWASP Logging sugiere capturar identidad, origen, tipo/severidad, resultado y razón, y aplicar controles de integridad/monitoreo de accesos a logs.[^5]
**Facts:** OWASP API Top 10 (2023) destaca BOLA como riesgo principal por falta de autorización a nivel objeto.[^1]
**Inferences (métricas accionables):**

- **Leak-prevention:** % de endpoints con “tenant scope” obligatorio + tests de acceso cross-tenant (debería tender a 100%).
- **Señales de ataque/abuso:** tasa de intentos fallidos de acceso a objetos (403/404 “seguro”) por tenant/usuario; spikes pueden indicar scraping o enumeración.
- **Logging útil:** % de eventos críticos con `request_id` + `tenant_id` + actor + objeto + resultado; tiempo promedio para reconstruir un incidente (MTTR forense).
- **Secret hygiene:** frecuencia real de rotación, % secretos sin owner/rotación definida, tiempo para rotar sin downtime.

***

## Operational checklist

**Facts:** OWASP recomienda proteger logs (restricción de acceso, registrar/monitorear accesos, tamper detection) y cuidar exposición de datos (mask/sanitize/hash/encrypt donde aplique).[^5]
**Facts:** OWASP Secrets Management incluye rotación, controles anti-fuga en CI/CD, y trazabilidad de solicitudes/usos/expiración.[^6]
**Inferences (checklist por fase):**

- **Diseño:** definir “tenant boundary” (qué es tenant, qué comparte/no comparte), escoger postura (segura vs agresiva), definir RBAC básico + atributos ABAC mínimos.
- **Build:** políticas de autorización centralizadas (policy/guard), `tenant_id` obligatorio en repositorios/queries, pruebas automáticas anti-BOLA (por endpoint).
- **API:** rate/resource controls para evitar consumo abusivo (cost/DoS), inventario de endpoints/versiones y retiro de endpoints legacy.
- **Observabilidad:** esquema de audit events, correlation IDs end-to-end, retención y acceso a logs por rol; procesos de revisión periódica.
- **Secret ops:** vault/gestor, rotación programada, break-glass controlado, trazas de uso, y pipeline sin secretos embebidos.

***

## Anti-patterns

**Facts:** OWASP API Top 10 (2023) describe BOLA y fallas de autorización a nivel función/propiedad como categorías de riesgo frecuentes.[^1]
**Facts:** OWASP Logging advierte que ciertos datos pueden requerir exclusión/enmascarado/sanitización/hasheo/cifrado, y pide controles fuertes de acceso a logs.[^5]
**Facts:** OWASP Secrets Management alerta sobre fugas vía CI/CD (forks/copias) y enfatiza rotación y trazabilidad.[^6]
**Inferences (lo que rompe enterprise rápido):**

- “Aislamiento” solo en frontend (filtro por tenant en UI) y backend consulta por `id` sin `tenant_id`.
- “Admin global” sin separación clara entre funciones administrativas y de usuario (cae en Broken Function Level Authorization).
- Logs con PII/secretos (tokens, headers, payloads) sin masking; o logs accesibles a demasiada gente.
- Secretos “eternos” (sin owner, sin rotación, sin expiración), o secretos que viajan por tickets/chat.

***

## Diagnostic questions

**Facts:** OWASP recomienda autorización por objeto en cada función que accede a datos por IDs provistos por el usuario.[^1]
**Facts:** OWASP Logging detalla campos y controles para que logs sean útiles y resistentes a manipulación/accesos indebidos.[^5]
**Facts:** OWASP Secrets Management pide trazabilidad de accesos/uso/rotación/expiración.[^6]
**Inferences (preguntas de PM/Producto):**

- ¿Puedo demostrar (con tests) que *ningún* endpoint permite leer/modificar un objeto de otro tenant aunque tenga el ID?
- ¿Qué campos del CRM son “sensibles” (margen, comisiones, risk flags) y cómo se controla su lectura/escritura por rol y contexto?
- Si mañana un cliente pide “audit log para compliance”, ¿qué puede ver, cuánto retenemos y cómo evitamos exponer PII?
- ¿Cuánto tarda rotar un secreto crítico (ERP/Payments/Email) sin downtime y sin tocar código?

***

## Sources (o referencia a SOURCES.md)

**Facts (fuentes usadas):** OWASP API Security Top 10 (2023).[^1]
**Facts (fuentes usadas):** OWASP Multi-Tenant Security Cheat Sheet (s/f).[^2]
**Facts (fuentes usadas):** OWASP Logging Cheat Sheet (publicación indicada en la página).[^5]
**Facts (fuentes usadas):** OWASP Secrets Management Cheat Sheet (publicación indicada en la página).[^6]
**Facts (fuentes usadas):** NIST SP 800-162 (ABAC) landing page (fecha indicada en CSRC).[^4]
**Facts (fuentes usadas):** NIST Log Management project page (contexto sobre SP 800-92 y recomendaciones de planificación).[^7]

**Añadir a `SOURCES.md` (sin duplicados):**

- OWASP — *OWASP Top 10 API Security Risks – 2023* — https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- OWASP Cheat Sheet Series — *Multi Tenant Security Cheat Sheet* — https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html
- OWASP Cheat Sheet Series — *Logging Cheat Sheet* — https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- OWASP Cheat Sheet Series — *Secrets Management Cheat Sheet* — https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- NIST CSRC — *SP 800-162: Guide to Attribute Based Access Control (ABAC)* — https://csrc.nist.gov/pubs/sp/800/162/upd2/final
- NIST CSRC — *Log Management (SP 800-92 context)* — https://csrc.nist.rip/Projects/log-management

***

## Key takeaways for PM practice

- Diseña multi-tenancy como control de seguridad, no como “feature”: el default debe impedir cross-tenant por construcción.
- Prioriza autorización por registro (BOLA) y por propiedad: es donde se rompen CRMs enterprise con más frecuencia.
- RBAC te ordena permisos; ABAC te da el “control fino” que piden enterprise (contexto, región, sensibilidad, riesgo).
- Audit logs y secretos son producto + operación: si no son consultables/rotables sin drama, te costarán churn y soporte.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://owasp.org/API-Security/editions/2023/en/0x11-t10/

[^2]: https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html

[^3]: https://www.archtis.com/nist-sp-800-162-attribute-based-access-control-abac-guide/

[^4]: https://csrc.nist.gov/pubs/sp/800/162/upd2/final

[^5]: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html

[^6]: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

[^7]: https://csrc.nist.rip/Projects/log-management

[^8]: pasted-text.txt

[^9]: https://www.visual-guard.com/ES/seguridad-aplicaciones/asegurar-saas-y-multi-tenant-apps-con-asp-net-o-wcf-Silverlight.html

[^10]: https://www.opentext.com/es/products/security-log-analytics

[^11]: https://www.fortinet.com/lat/resources/cyberglossary/owasp

[^12]: https://www.youtube.com/watch?v=4BNVpgYH-pM

[^13]: https://logcentral.io/fr/blog/best-practices-for-multi-tenant-data-segregation

[^14]: https://learn.microsoft.com/es-es/azure/api-management/mitigate-owasp-api-threats

[^15]: https://apisecurity.io/owasp-api-security-top-10/

[^16]: https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-162.pdf

[^17]: https://www.tenupsoft.com/blog/strategies-for-tenant-data-isolation-in-multi-tenant-based-saas-applications.html

[^18]: https://docs.automationanywhere.com/es-ES/bundle/enterprise-v2019/page/enterprise-cloud/topics/control-room/audit-log/cloud-audit-log.html

[^19]: https://owasp.org/www-project-api-security/

[^20]: https://en.wikipedia.org/wiki/NIST_SP_800-92

[^21]: https://www.scribd.com/document/752825173/OWASP-Logging-Cheat-Sheet

[^22]: https://www.youtube.com/watch?v=tV40sLtJOmY

[^23]: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Vocabulary_Cheat_Sheet.html

[^24]: https://cheatsheetseries.owasp.org/IndexTopTen.html

