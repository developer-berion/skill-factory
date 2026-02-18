# KB_04 — Security, Privacy & Compliance para CRM Enterprise

## Executive Summary

Todo CRM que aspire a vender enterprise necesita pasar tres filtros duros antes de que el equipo de procurement abra siquiera la conversación: **seguridad técnica demostrable**, **privacidad regulatoria verificable** y **marcos de compliance auditados por terceros**. Este documento compila los requisitos core agrupados en siete dominios — RBAC/ABAC, Tenant Isolation, Audit Logs, Encryption, Data Retention, GDPR/CCPA, y marcos SOC 2 / ISO 27001 — y los traduce a requisitos de producto verificables con criterios de aceptación concretos. El enfoque es B2B SaaS multi-tenant orientado a mayoristas y operadores donde la cadena de confianza pasa por el administrador de la organización cliente (la agencia), no por el usuario final. Cada sección distingue Facts vs Inferences y cierra con un checklist operativo, anti-patterns y preguntas diagnóstico. La meta: que un PM o tech lead pueda tomar este documento y convertirlo en epics/stories sin ambigüedad.

***

## Definitions and Why It Matters

| Término | Definición | Por qué importa en CRM enterprise |
|---|---|---|
| **RBAC** | Role-Based Access Control — acceso basado en roles predefinidos (Admin, Editor, Viewer) | Base mínima que todo enterprise buyer exige antes de iniciar evaluación [^1][^2] |
| **ABAC** | Attribute-Based Access Control — acceso basado en atributos dinámicos (tenant, IP, horario, clasificación del dato) | Permite políticas contextuales tipo "solo desde dispositivo corporativo en horario laboral" [^3][^4] |
| **Tenant Isolation** | Separación lógica o física de datos entre organizaciones/clientes en un entorno multi-tenant | Sin aislamiento, un bug o query mal escrito expone datos de un cliente a otro [^5][^3] |
| **Audit Log** | Registro inmutable de toda acción en el sistema (quién, qué, cuándo, desde dónde) | Obligatorio para SOC 2, ISO 27001 y GDPR. Sin logs auditables no hay certificación [^6][^7] |
| **Encryption at Rest** | Cifrado de datos almacenados en disco/DB (estándar: AES-256) | Protege contra acceso físico a medios o backups robados [^8][^9] |
| **Encryption in Transit** | Cifrado de datos en movimiento (estándar: TLS 1.2/1.3) | Previene interceptación man-in-the-middle [^8][^9] |
| **Data Retention** | Políticas que definen cuánto tiempo se almacena cada tipo de dato y cuándo se elimina | GDPR exige "storage limitation"; CCPA exige declarar períodos; sobre-retención = riesgo legal [^10][^11] |
| **GDPR** | General Data Protection Regulation (EU) — aplica por ubicación del sujeto de datos | Multas hasta 4% del revenue global o €20M [^12][^13] |
| **CCPA/CPRA** | California Consumer Privacy Act / California Privacy Rights Act — aplica por umbrales de negocio | Multas de $2,500–$7,500 por violación; exige declarar retención por categoría de dato [^13][^14] |
| **SOC 2 Type II** | Auditoría AICPA que evalúa controles operando efectivamente en el tiempo (6–12 meses) | Requisito de facto para vender SaaS a enterprise en US [^15][^16] |
| **ISO 27001:2022** | Estándar global de ISMS con 93 controles en Annex A (Organizacionales, Personas, Físicos, Tecnológicos) | Gold standard internacional; alinea con GDPR, SOC 2, HIPAA [^17][^18] |

**Fact:** Enterprise procurement teams bloquean proveedores que no pueden demostrar RBAC, encryption y audit logs antes del POC.[^1]
**Inference:** Un CRM orientado a B2B turismo que vende a cadenas hoteleras o mayoristas multinacionales necesita estos fundamentos incluso si la regulación local no los exige explícitamente, porque los partners internacionales sí lo harán.

***

## Principles and Best Practices

### 1. RBAC/ABAC — Control de Acceso

**Principio:** Least privilege by default. Ningún usuario debe tener más acceso del necesario para su función.[^2][^4]

**Best Practices:**
- Implementar RBAC como capa base con roles predefinidos (Owner, Admin, Manager, Agent, Viewer) scoped a tenant/organización[^3][^2]
- Permitir **custom roles** — enterprise buyers no sobreviven con roles estáticos "Admin/Member/Viewer"[^1]
- Complementar con ABAC para políticas dinámicas: acceso condicional por IP, horario, dispositivo, clasificación del dato[^4][^19]
- En multi-tenant, los roles DEBEN evaluarse dentro del contexto del tenant — un Admin en Tenant A no puede ser Admin en Tenant B salvo asignación explícita[^3]
- El mapeo role → permissions debe ser auditable y generar log en cada decisión de autorización[^2]

**Fact:** NIST SP 800-162 define ABAC como el modelo donde las decisiones de acceso se basan en atributos del sujeto, recurso, acción y entorno evaluados en tiempo real.[^20]
**Fact:** WorkOS documenta que RBAC tenant-aware es checkpoint obligatorio para deals enterprise y auditorías SOC 2.[^1]

### 2. Tenant Isolation

**Principio:** Cada organización/cliente opera como si fuera el único en la plataforma.[^21][^5]

**Best Practices:**
- **Modelo recomendado:** Aislamiento lógico con tenant_id propagado en toda query (row-level security), con option de policy stores por tenant[^5]
- Los datos RBAC (role mappings) NO deben residir en un store compartido sin aislamiento — riesgo de fuga cross-tenant[^5]
- Validar aislamiento con pruebas automatizadas: un usuario autenticado en Tenant A NO debe poder acceder a recursos de Tenant B bajo ninguna combinación de parámetros
- AWS Verified Permissions recomienda per-tenant policy store para garantizar evaluación independiente de políticas por organización[^5]

**Fact:** AWS Prescriptive Guidance documenta que en modelos shared multi-tenant, el role mapping data no debe residir dentro del motor de autorización (OPA/Verified Permissions) para mantener tenant isolation.[^5]
**Inference:** Para un CRM de turismo B2B, cada agencia (tenant) debe tener su propio espacio aislado de cotizaciones, bookings y datos de pasajeros.

### 3. Audit Logs

**Principio:** Todo evento relevante debe registrarse de forma inmutable, tamper-proof y consultable.[^7][^22]

**Best Practices:**
- Logs **append-only** — ni siquiera sysadmins pueden alterar o eliminar entradas[^23]
- Sellado criptográfico (hash chains): cada entrada vinculada a la anterior; alteración rompe la cadena y es detectable inmediatamente[^24][^7]
- Almacenamiento WORM (Write-Once Read-Many) o retention-locked buckets[^22][^24]
- Campos mínimos por entry: `timestamp`, `actor_id`, `tenant_id`, `action`, `resource`, `old_value`, `new_value`, `ip_address`, `user_agent`
- Retención mínima de logs: 1 año para SOC 2; 6 años para HIPAA admin docs[^25][^11]
- Exportación a SIEM externo del cliente (requisito enterprise común)[^6]

**Fact:** IBM define audit trail como registro histórico que "cannot be altered or deleted", requiriendo inmutabilidad a nivel de storage.[^24]
**Fact:** SOC 2 CC7 exige logging and review procedures como control de system operations.[^26]

### 4. Encryption

**Principio:** Datos protegidos tanto almacenados como en movimiento, con gestión de llaves separada.[^8][^9]

**Best Practices:**
- **At Rest:** AES-256 obligatorio para DB, backups y medios removibles[^9]
- **In Transit:** TLS 1.3 (mínimo TLS 1.2); deshabilitar SSL 3.0, TLS 1.0, cipher suites débiles como RC4[^27][^9]
- Key Management: llaves en HSM dedicado o cloud KMS (AWS KMS, GCP KMS, Azure Key Vault) con rotación cada 6–12 meses[^9]
- Mutual TLS (mTLS) entre capas application ↔ database para entornos de alta seguridad[^9]
- Tokenización de identificadores de cliente para desacoplar PII del perfil de negocio[^9]
- Módulos criptográficos validados FIPS 140-2/3 para enterprise que lo requieran[^9]

**Fact:** GDPR Art. 32 exige "appropriate technical measures" — la guía del ICO UK especifica AES-256 at rest, TLS 1.2+ in transit, RSA-2048+ para key exchange.[^9]
**Inference:** Para el mercado LATAM, aunque no hay equivalente exacto a GDPR enforcement, los partners internacionales (Expedia, Amadeus) exigen estos estándares como requisito de integración.

### 5. Data Retention

**Principio:** Solo retener datos el tiempo necesario para el propósito declarado; eliminar de forma segura y documentada.[^10][^11]

**Best Practices:**
- Definir períodos por categoría de dato, no genéricos:[^10]
  - **Datos financieros/transaccionales:** 7 años (SOX, tax)[^11]
  - **Datos de empleados:** 3–10 años según jurisdicción[^11]
  - **Datos de marketing/leads:** 12–24 meses[^10]
  - **Datos de pasajeros (PII):** según propósito + regulación local
  - **Logs de auditoría:** mínimo 1 año (SOC 2); 6 años (HIPAA admin)[^11]
- Implementar eliminación automatizada con schedule configurable por tenant[^12]
- Proceso de revisión antes de deletion[^12]
- Documentar excepciones (legal hold, archival)[^10]
- CCPA/CPRA exige declarar al momento de la recolección cuánto tiempo se retendrá cada categoría[^11]

**Fact:** GDPR storage limitation principle: datos personales no pueden mantenerse más allá del tiempo necesario para el propósito declarado.[^28]
**Fact:** Secureframe documenta que ISO 27001 requiere "Protection of Records" con schedules de retención y disposal.[^10]

### 6. GDPR / CCPA Compliance

**Principio:** Privacy by design — la privacidad se construye en la arquitectura, no se agrega después.[^12]

| Requisito | GDPR | CCPA/CPRA |
|---|---|---|
| **Consent** | Opt-in explícito previo | Opt-out (derecho a rechazar venta de datos) [^13] |
| **Acceso/Portabilidad** | Art. 15 — derecho de acceso; Art. 20 — portabilidad | Derecho de acceso y portabilidad [^14] |
| **Eliminación** | Art. 17 — derecho al olvido | Derecho a eliminar datos personales [^14] |
| **Data minimization** | Solo recolectar lo necesario | Solo retener lo necesario para propósito declarado [^13] |
| **Breach notification** | 72 horas a la autoridad | "Sin demora irrazonable" [^13] |
| **DPA** | Obligatorio con todos los procesadores | N/A explícito, pero recomendable [^12] |
| **Penalidades** | Hasta 4% revenue global o €20M | $2,500–$7,500 por violación [^13] |
| **Alcance** | Por ubicación del sujeto de datos | Umbrales de negocio en California [^13] |

**Requisitos de producto para compliance:**
- Consent management: capturar, almacenar y mostrar timestamps de consentimiento[^12]
- Portal self-service para data subject: ver, corregir, exportar y eliminar sus datos[^6]
- Data masking en ambientes de testing/demo[^6]
- Data residency controls: permitir elegir región geográfica de almacenamiento[^6]
- Privacy Impact Assessment (PIA) tooling para procesamiento de alto riesgo[^12]

### 7. Marcos: SOC 2 Type II & ISO 27001:2022

#### SOC 2 Type II

Basado en cinco Trust Services Criteria (TSC) de AICPA:[^16][^29]

| TSC | Obligatorio | Scope CRM |
|---|---|---|
| **Security** (CC1–CC9) | ✅ Sí | Acceso, firewalls, MFA, IDS, vulnerability scans [^16] |
| **Availability** | Opcional | Uptime SLA, backup, DR, capacity management [^30] |
| **Processing Integrity** | Opcional | Validación de transacciones, reconciliation [^16] |
| **Confidentiality** | Opcional | Identificar, proteger y destruir info confidencial al fin de retención [^15] |
| **Privacy** | Opcional | Notice/consent, PII inventory, data subject rights [^26] |

**Controles clave mapeados a producto CRM:**
- CC6 — Logical & physical access: Identity lifecycle management, MFA, access logs[^26]
- CC7 — System operations: Logging, review procedures, backup/restore probados[^26]
- CC8 — Change management: Proceso formal de change-request; emergency-change procedures[^26]
- CC4 — Monitoring: Vulnerability scans continuos, SIEM alerts, auditorías internas periódicas[^26]

#### ISO 27001:2022 — Annex A (93 controles)

Reorganizados en 4 dominios:[^17]

| Dominio | # Controles | Controles clave para CRM |
|---|---|---|
| **Organizational** (A.5) | 26 | A.5.15 Access Control, A.5.12 Classification, A.5.14 Info Transfer, A.5.22 Cloud Security, A.5.23 Incident Mgmt |
| **People** (A.6) | 8 | A.6.1 Screening, A.6.3 Security Awareness, A.6.5 Termination, A.6.8 Privileged Accounts |
| **Physical** (A.7) | 9 | A.7.2 Entry Controls, A.7.7 Secure Disposal, A.7.9 Clear Desk |
| **Technological** (A.8) | 12 | A.8.6 Encryption, A.8.7 Logging & Monitoring, A.8.9 IAM (RBAC), A.8.10 Secure Auth, A.8.11 Cloud Security, A.8.12 Vuln Mgmt |

**Fact:** ISO 27001:2022 redujo de 114 a 93 controles reorganizándolos en estos 4 dominios.[^17]
**Fact:** Certificación requiere Statement of Applicability (SoA) justificando inclusión/exclusión de cada uno de los 93 controles.[^31][^32]

***

## Examples (aplicado a CRM enterprise B2B Turismo)

### Ejemplo 1: RBAC + Tenant Isolation para mayorista
Una agencia (Tenant A) tiene roles: `Owner` (ve todo, configura), `Sales Manager` (ve ventas + reportes de su equipo), `Agent` (solo sus cotizaciones). Un counter de otra agencia (Tenant B) jamás ve datos de Tenant A, aunque ambos comparten la misma instancia SaaS. Si un Agent intenta acceder vía API manipulando el `tenant_id` en el request, el sistema bloquea y genera audit log con severity HIGH.

### Ejemplo 2: Data Retention en reservas
- **Booking activo:** Retención completa durante vigencia + 2 años post-servicio (reclamaciones)
- **Datos de pasajero (PII):** Auto-anonimización a los 24 meses post-viaje (nombre → hash, pasaporte → masked)
- **Datos financieros:** 7 años completos para auditoría fiscal
- **Logs de auditoría:** Mínimo 13 meses (SOC 2); 7 años para financial audit trail

### Ejemplo 3: Encryption en flujo de cotización
1. Agente crea cotización → datos viajan TLS 1.3 al servidor
2. Datos de pasajero almacenados con AES-256 en PostgreSQL (pgcrypto / KMS)
3. Backup nocturno → cifrado con key diferente, almacenado en S3 con SSE-KMS
4. PDF de cotización enviado al pasajero → TLS 1.3 en tránsito; link expirable

***

## Metrics / Success Signals

| Métrica | Target | Fuente |
|---|---|---|
| % de endpoints con RBAC enforced | 100% | Test suite automatizado |
| Tiempo medio para revocar acceso post-terminación | < 1 hora | IAM lifecycle dashboard |
| Cross-tenant access violations detectadas en pen-test | 0 | Pen-test trimestral |
| Uptime de audit log pipeline | 99.99% | Monitoring (Datadog/CloudWatch) |
| Encryption coverage (at rest) | 100% de PII y datos financieros | Scan automatizado |
| DSAR (Data Subject Access Request) response time | < 30 días (GDPR) / < 45 días (CCPA) | Ticket tracking [^13] |
| SOC 2 Type II findings (gaps) | 0 critical, < 3 moderate | Auditor report |
| Time to remediate critical vulnerability | < 48 horas | Vuln management dashboard |
| Data retention compliance rate | 100% categorías con schedule activo | Retention policy engine |

***

## Operational Checklist

- [ ] **RBAC:** Definir role matrix (mínimo 5 roles) con permisos granulares por recurso
- [ ] **Custom Roles:** API para que admins de tenant creen/editen roles propios
- [ ] **ABAC policies:** Al menos 3 atributos dinámicos (IP range, horario, device type)
- [ ] **Tenant isolation:** Row-level security con `tenant_id` en toda query; test automatizado cross-tenant
- [ ] **Audit logs:** Schema definido (timestamp, actor, tenant, action, resource, old/new value, IP, user-agent)
- [ ] **Audit immutability:** Storage append-only (WORM o retention-locked); hash chain verificable
- [ ] **Audit export:** Endpoint para exportar logs a SIEM del cliente (Splunk, Datadog, etc.)
- [ ] **Encryption at rest:** AES-256 en DB principal + backups; validar con scan
- [ ] **Encryption in transit:** TLS 1.3 enforced; deshabilitar TLS 1.0, SSL 3.0, RC4
- [ ] **Key management:** Keys en KMS/HSM dedicado; rotación automática cada 6 meses
- [ ] **Data retention:** Tabla de períodos por categoría de dato; cron job de auto-deletion/anonimización
- [ ] **Consent management:** Capture timestamp + versión de privacy policy aceptada
- [ ] **DSAR portal:** Self-service para ver, exportar y solicitar eliminación de datos
- [ ] **Data masking:** Campos PII masked en ambientes staging/demo
- [ ] **SOC 2 readiness:** Controles CC1–CC9 documentados con owner y evidencia
- [ ] **ISO 27001 SoA:** Statement of Applicability con justificación para cada uno de los 93 controles
- [ ] **Pen-test:** Trimestral, con scope explícito en tenant isolation y privilege escalation
- [ ] **Incident Response Plan:** Documentado, probado y actualizado semestralmente

***

## Anti-patterns

| Anti-pattern | Riesgo | Corrección |
|---|---|---|
| **Roles hardcoded** ("solo Admin y User") | Enterprise buyer rechaza el producto por falta de granularidad [^1] | Implementar custom roles con permission matrix editable por tenant |
| **tenant_id solo en la capa de aplicación** | Un bug en un endpoint expone datos cross-tenant | Enforced a nivel de DB (row-level security) + middleware + test automatizado |
| **Audit logs en tabla SQL regular (mutable)** | Auditor SOC 2 rechaza la evidencia; cualquiera con DB access puede borrar rastro [^7] | Migrar a storage WORM/append-only con hash chain |
| **Encryption "opcional" o configurable por cliente** | Un solo tenant sin encryption compromete la postura de seguridad de toda la plataforma | Encryption by default, no opt-in. Zero-config para el cliente |
| **Retención indefinida ("guardamos todo por si acaso")** | Violación directa de GDPR storage limitation y CCPA disclosure requirements [^11][^28] | Definir schedules explícitos por categoría; auto-deletion |
| **Privacy policy genérica sin timestamps de consent** | Consent no demostrable = consent inexistente para un regulador [^12] | Versionar privacy policies; almacenar timestamp + version aceptada por usuario |
| **SOC 2 Type I y declarar "somos SOC 2 compliant"** | Type I solo demuestra diseño de controles en un punto en el tiempo, no operación sostenida [^25] | Avanzar a Type II (6–12 meses de evidencia operativa) |
| **ISO 27001 SoA sin justificación de exclusiones** | Auditor rechaza la certificación [^31] | Documentar razón de exclusión para cada control no aplicable |

***

## Diagnostic Questions

1. **¿Puede un admin de Tenant A ver, aunque sea por error, datos de Tenant B?** → Si la respuesta no es un "no" verificable con test automatizado, hay un gap crítico de tenant isolation.

2. **¿Qué pasa si un empleado de una agencia es despedido a las 5pm un viernes?** → Si el acceso no se revoca en < 1 hora con audit trail, el proceso IAM lifecycle está roto.

3. **¿Puedes mostrarme el audit log de quién accedió a los datos de pasaporte del pasajero X hace 6 meses?** → Si no puedes, no pasas SOC 2 CC7 ni GDPR Art. 30.

4. **¿Qué encryption key protege los backups? ¿Cuándo se rotó por última vez?** → Si nadie sabe, key management es un riesgo activo.

5. **¿Cuánto tiempo retienes datos de un pasajero que viajó hace 3 años?** → Si la respuesta es "indefinidamente", hay violación potencial de GDPR/CCPA.

6. **¿Puedo como pasajero pedir que eliminen mis datos de tu CRM?** → Si no hay proceso documentado + portal, falta DSAR compliance.

7. **¿Tu SOC 2 es Type I o Type II? ¿De qué fecha?** → Type I antiguo = marketing, no seguridad real. Enterprise exige Type II vigente.

8. **¿Cuántos de los 93 controles Annex A has evaluado en tu SoA?** → Si no hay SoA, no hay camino a ISO 27001.

***

## Requisitos de Producto Verificables

### Matriz de Requisitos con Criterios de Aceptación

| ID | Dominio | Requisito | Criterio de Aceptación Verificable | Prioridad |
|---|---|---|---|---|
| SEC-01 | RBAC | Sistema soporta mínimo 5 roles base por tenant | Test: crear 5 roles distintos con permisos diferentes; verificar que cada rol solo accede a lo asignado | P0 |
| SEC-02 | RBAC | Admins de tenant pueden crear custom roles | Test: admin crea rol "Supervisor Ventas" con subset de permisos; nuevo usuario asignado solo ve lo permitido | P0 |
| SEC-03 | ABAC | Políticas de acceso condicional por atributos | Test: configurar regla "solo desde IP X en horario 9-18"; verificar bloqueo fuera de condiciones | P1 |
| SEC-04 | Tenant Isolation | Row-level security enforced a nivel de DB | Test: query directa a DB sin WHERE tenant_id retorna error o vacío; pen-test cross-tenant = 0 findings | P0 |
| SEC-05 | Tenant Isolation | API valida tenant_id en cada request | Test: request con token de Tenant A + tenant_id de Tenant B → HTTP 403 + audit log generado | P0 |
| SEC-06 | Audit | Toda acción CRUD genera log inmutable | Test: crear/leer/actualizar/eliminar recurso; verificar entrada en audit log con todos los campos requeridos | P0 |
| SEC-07 | Audit | Logs son append-only y tamper-proof | Test: intentar UPDATE/DELETE en storage de logs → operación rechazada; hash chain validable | P0 |
| SEC-08 | Audit | Exportación de logs a SIEM externo | Test: configurar webhook/API a Splunk; verificar que eventos llegan en < 5 min | P1 |
| SEC-09 | Encryption | Datos PII cifrados at rest con AES-256 | Test: inspección directa de DB/storage muestra datos cifrados; validar algoritmo via metadata | P0 |
| SEC-10 | Encryption | TLS 1.3 enforced en todos los endpoints | Test: SSL Labs scan = A+; conexiones TLS 1.0/1.1 rechazadas | P0 |
| SEC-11 | Encryption | Key rotation automática cada 6 meses | Test: verificar en KMS que key activa tiene < 6 meses; key anterior marcada como deprecated | P1 |
| SEC-12 | Retention | Schedules de retención configurables por categoría | Test: configurar retención de 24 meses para PII pasajeros; verificar auto-deletion/anonimización al vencer | P0 |
| SEC-13 | Retention | Eliminación segura con evidencia auditable | Test: dato expirado → eliminado de DB + backups; audit log registra deletion event | P1 |
| SEC-14 | GDPR | Consent management con timestamp y versión | Test: usuario acepta privacy policy v2.1; sistema almacena timestamp ISO 8601 + version string | P0 |
| SEC-15 | GDPR/CCPA | Portal DSAR self-service | Test: data subject solicita export → recibe archivo en < 72h; solicita deletion → dato eliminado en < 30 días | P0 |
| SEC-16 | GDPR | Data masking en ambientes no-producción | Test: restaurar backup en staging; campos PII aparecen masked/tokenizados | P1 |
| SEC-17 | SOC 2 | Controles CC1–CC9 documentados con owner | Verificar: documento con cada control, owner asignado, artefacto de evidencia linkado | P0 |
| SEC-18 | ISO 27001 | Statement of Applicability (SoA) completo | Verificar: 93 controles listados con justificación de inclusión o exclusión | P1 |
| SEC-19 | MFA | MFA obligatorio para roles Admin y Owner | Test: login sin segundo factor → acceso denegado para roles privilegiados | P0 |
| SEC-20 | Incident Response | Plan documentado y probado | Verificar: documento actualizado < 6 meses; evidencia de tabletop exercise | P1 |

***

## Key Takeaways for PM Practice

- **RBAC + custom roles es el requisito #1** que enterprise procurement evalúa antes de cualquier demo. Sin esto, no hay pipeline enterprise.[^2][^1]
- **Tenant isolation debe ser enforced a nivel de DB**, no solo de aplicación. Un middleware roto no debe exponer datos cross-tenant.[^5]
- **Audit logs inmutables son infraestructura, no feature**. Sin ellos, SOC 2 y ISO 27001 son imposibles.[^7][^26]
- **Encryption no es negociable ni configurable** — AES-256 at rest + TLS 1.3 in transit, siempre activado, zero-config.[^9]
- **Data retention con schedules por categoría** evita el anti-pattern de "guardamos todo forever" que viola GDPR y CCPA.[^11][^10]
- **SOC 2 Type II > Type I** siempre. Type I es una foto; Type II es una película que demuestra operación sostenida.[^25][^16]
- **ISO 27001 SoA es el artefacto más importante** — sin justificación de los 93 controles, no hay certificación.[^31]
- **Privacy by design, no privacy by patch** — consent, DSAR, retention y masking deben diseñarse desde la arquitectura, no agregarse después.[^12]
- **El criterio de aceptación debe ser testeable automáticamente** — si no se puede verificar con un script o pen-test, no es un requisito; es un deseo.
- **Para mercados LATAM vendiendo a partners internacionales**, adoptar GDPR-level protections como baseline global simplifica compliance multi-jurisdiccional.[^13]

***

## Sources

- WorkOS (2025) — Top RBAC providers for multi-tenant SaaS[^1]
- Auth0 (2024) — Authorization models for multi-tenant SaaS[^3]
- AWS Prescriptive Guidance — Tenant isolation and privacy of RBAC data[^5]
- LoginRadius (2025) — SaaS Identity & Access Management multi-tenant[^21]
- GDPR Local (2025) — GDPR CRM compliance guide[^12]
- Business Software (2025) — CRM Data Privacy & Compliance[^6]
- Secureframe (2021) — SOC 2 Compliance Requirements[^15]
- Copla (2025) — SOC 2 audit checklist[^26]
- Copla (2025) — ISO 27001 controls list Annex A complete guide[^17]
- ISMS Online (2025) — ISO 27001:2022 Annex A explained[^31]
- Vanta (2025) — ISO 27001 for SaaS 8-step guide[^18]
- HubiFi (2026) — Immutable audit log basics[^7]
- HubiFi (2025) — Immutable logs complete guide[^22]
- Spendflo (2025) — Audit trail complete guide[^24]
- Konfirmity (2026) — GDPR encryption requirements[^9]
- LinkedIn/Agarwal (2023) — AES-256 and TLS 1.3 explained[^8]
- Secureframe (2025) — Data retention policy guide[^10]
- TermsFeed (2025) — Retention policies legal timeframes[^11]
- Secure Privacy (2025) — SaaS privacy compliance 2025 guide[^13]
- Insight Assurance (2025) — CCPA compliance SaaS[^14]
- EnterpriseReady — RBAC guide for SaaS[^2]
- CrowdStrike (2025) — ABAC access control[^19]
- NIST SP 800-162 — Guide to ABAC[^20]
- CloudEagle (2025) — RBAC vs ABAC comparison[^4]
- Scytale (2025) — SOC 2 controls for SaaS[^16]
- 4C Consulting (2025) — Trust Services Criteria SOC 2 guide[^29]
- Cynomi (2025) — SOC 2 compliance checklist[^25]
- DPO Centre (2025) — CRM data retention GDPR[^28]
- Scrut (2025) — ISO 27001 documentation requirements[^32]
- Intuition Labs (2026) — Audit trail compliance[^23]

---

## References

1. [Top RBAC providers for multi-tenant SaaS in 2025 - WorkOS](https://workos.com/blog/top-rbac-providers-for-multi-tenant-saas-2025) - A practical guide to choosing the right role-based access control provider for modern multi-tenant S...

2. [Enterprise Ready SaaS App Guide to Role Based Access Control ...](https://www.enterpriseready.io/features/role-based-access-control/) - A guide for SaaS products to implement role based access control (RBAC) in their application to offe...

3. [How to Choose the Right Authorization Model for Your Multi-Tenant ...](https://auth0.com/blog/how-to-choose-the-right-authorization-model-for-your-multi-tenant-saas-application/) - This guide provides a deeper dive into how RBAC, ABAC, and ReBAC can be implemented for multi-tenanc...

4. [RBAC vs. ABAC: Choosing the Right Access Control Model](https://www.cloudeagle.ai/blogs/rbac-vs-abac-choosing-the-right-access-control-model) - ✓ RBAC provides structured, role-based management, making it ideal for enterprises with well-defined...

5. [Recommendations for tenant isolation and privacy of data](https://docs.aws.amazon.com/prescriptive-guidance/latest/saas-multitenant-api-access-authorization/devops-isolation-privacy.html) - Secure approaches with OPA for maintaining the privacy and tenant isolation of RBAC data include usi...

6. [CRM Data Privacy & Compliance: Navigating GDPR, CCPA, and ...](https://www.business-software.com/blog/crm-data-privacy-compliance-navigating-gdpr-ccpa-and-global-regulations/) - Learn how to ensure CRM data privacy and compliance with global regulations like GDPR and CCPA. Disc...

7. [The Ultimate Guide to Immutable Audit Trails - HubiFi](https://www.hubifi.com/blog/immutable-audit-log-basics) - An immutable audit trail provides a tamper-proof record of all system activity. Learn why this is cr...

8. [What is 256-bit AES Encryption at Rest and TLS 1.3 in Transit used ...](https://www.linkedin.com/pulse/what-256-bit-aes-encryption-rest-tls-13-transit-used-data-agarwal) - TLS 1.3 guarantees secure communication between users and websites, preventing unauthorized intercep...

9. [GDPR Encryption Requirements: A Practical Guide with Steps ...](https://www.konfirmity.com/blog/gdpr-encryption-requirements) - These points suggest that enterprises should deploy AES‑256 for data at rest, TLS 1.2/1.3 for data i...

10. [Creating a Data Retention Policy: Examples, Best Practices ...](https://secureframe.com/blog/data-retention-policy) - Set clear retention timelines for every type of data based on its legal, operational, and historical...

11. [Retention Policies: How Long Can You Keep Customer Data?](https://www.termsfeed.com/blog/retention-policies-how-long-can-you-keep-customer-data/) - This article breaks down relevant legal timeframes for storing your customers' data, as well as how ...

12. [GDPR CRM: Guide to Compliant Customer Data Management](https://gdprlocal.com/gdpr-crm/) - GDPR CRM compliance means managing personal data lawfully. Learn how to secure, process, and store C...

13. [SaaS Privacy Compliance Requirements: Complete 2025 Guide](https://secureprivacy.ai/blog/saas-privacy-compliance-requirements-2025-guide) - GDPR requires proactive consent while CCPA provides opt-out rights. GDPR applies based on data subje...

14. [Mastering CCPA Compliance: A Guide for SaaS Providers](https://insightassurance.com/insights/blog/mastering-ccpa-compliance-a-guide-for-saas-providers/) - Learn strategies for SaaS providers to achieve CCPA compliance, automate data privacy requests, and ...

15. [SOC 2 Compliance Requirements - Secureframe](https://secureframe.com/hub/soc-2/requirements) - There is no specific SOC 2 requirements checklist. Instead, the AICPA Trust Services Criteria provid...

16. [SOC 2 Controls Explained for SaaS Startups](https://scytale.ai/center/soc-2/soc-2-controls-explained-for-saas-startups/) - By expanding controls in each category, SaaS startups can see concrete examples that map directly to...

17. [ISO 27001 controls list: Full Annex A guide - Copla](https://copla.com/blog/compliance-regulations/iso-27001-controls-list-a-complete-guide-to-annex-a-and-control-objectives/) - The ISO 27001 controls list is outlined in Annex A, providing the essential security measures organi...

18. [ISO 27001 for SaaS: An 8-step guide to certification](https://www.vanta.com/resources/iso-27001-certification-for-saas) - 8 key steps for ISO 27001 for SaaS companies · Step 1: Define the scope of your ISMS · Step 2: Perfo...

19. [What is Attribute-Based Access Control (ABAC)? - CrowdStrike](https://www.crowdstrike.com/en-us/cybersecurity-101/identity-protection/attribute-based-access-control-abac/) - ABAC is an advanced access control method that determines permissions based on a combination of attr...

20. [[PDF] Guide to Attribute Based Access Control (ABAC) Definition and ...](https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-162.pdf) - This document describes the functional components of ABAC, as well as a set of issues for employing ...

21. [SaaS Identity & Access Management: Multi-Tenant Best Practices](https://www.loginradius.com/blog/engineering/saas-identity-access-management) - Look for flexible and composable support for Role-Based Access Control (RBAC), Attribute-Based Acces...

22. [What Are Immutable Logs? A Complete Guide - HubiFi](https://www.hubifi.com/blog/immutable-audit-log-guide) - A genuinely immutable audit log means that once a record is written, it cannot be changed, overwritt...

23. [Automating Audit Trail Compliance for 21 CFR Part 11 & Annex 11](https://intuitionlabs.ai/articles/audit-trails-21-cfr-part-11-annex-11-compliance) - Immutability – Tamper-evidence and tamper-resistance of the audit log. A compliant audit trail is ap...

24. [What Is An Audit Trail? A Complete Guide in 2025 - Spendflo](https://www.spendflo.com/blog/audit-trail-complete-guide) - 1) Data immutability and tamper-proof storage ... Industry guidance highlights tamper-evidence as a ...

25. [SOC 2 Compliance Checklist - Cynomi](https://cynomi.com/soc2/soc-2-compliance-checklist/) - SOC 2 compliance checklist: Core requirements · 1. Define audit scope · 2. Conduct a readiness (gap)...

26. [The ultimate SOC 2 audit checklist: Requirements and template](https://copla.com/blog/compliance-regulations/the-ultimate-soc-2-audit-checklist-requirements-and-template/) - 1. Engage a Certified Public Accountant (CPA) firm auditor · 2. Conduct Type 2 testing if needed · 3...

27. [HIPAA Encryption Rules for Data in Transit | Censinet, Inc.](https://censinet.com/perspectives/hipaa-encryption-rules-for-data-in-transit) - Recommended Standards: Use protocols like TLS 1.2 or 1.3, AES encryption (128-bit or 256-bit), and P...

28. [CRM Data Retention and GDPR Compliance - DPO Centre](https://www.dpocentre.com/blog/crm-data-retention-gdpr-compliance/) - In this blog, we explore how organisations can manage CRM data retentionData retention refers to the...

29. [Trust Services Criteria in SOC 2 Audits: SaaS Compliance Guide](https://www.4cpl.com/blog/trust-services-criteria-in-soc-2-audits-a-saas-compliance-guide/) - Built around five Trust Services Criteria—Security, Availability, Processing Integrity, Confidential...

30. [Choose Trust Service Criteria (TSC) for SOC 2 Compliance](https://www.processunity.com/resources/blogs/how-to-choose-trust-service-criteria-tsc-for-soc-2-compliance/) - Selecting Trust Service Criteria (TSC) is a crucial step in achieving SOC 2 compliance: the TSC you ...

31. [ISO 27001:2022 Annex A Explained & Simplified](https://www.isms.online/iso-27001/annex-a-2022/) - The biggest change is Annex A which specific controls derived from ISO 27002:2022. In this guide we'...

32. [ISO 27001 Documentation Requirements](https://www.scrut.io/hub/iso-27001/iso-27001-documentation) - Complete Annex A control listing: Your SoA must list all 93 Annex A controls from ISO 27001:2022. .....

