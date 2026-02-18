<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_12 — Data Governance: PII, Retention \& Audit Trail en CRM (Enterprise)

## Executive summary (10–15 líneas)

**Facts**

- Un CRM enterprise concentra PII y datos comerciales; si se exportan sin control (CSV/API/reportes), el riesgo de exfiltración y “data sprawl” se dispara.[^1][^2]
- “Storage limitation” exige conservar datos personales solo el tiempo necesario; borrar/anonomizar reduce riesgo de uso indebido y brechas.[^3][^4]
- Logging seguro implica **no** registrar PII sensible ni secretos (tokens, passwords, keys); se deben enmascarar/hashear/sanitizar para evitar fugas y “log injection”.[^5]
- Un audit trail útil necesita: qué pasó, quién, cuándo, resultado; además retención definida y protección contra alteración.[^6][^7]
- “Tamper-evident logging” (concepto) busca que si alguien modifica o borra eventos, eso sea detectable (append-only, hash chaining/Merkle, WORM, o controles equivalentes).[^8][^9][^5]

**Inferences**

- Para un CRM B2B, el mayor riesgo operativo suele venir de: permisos excesivos de exportación, integraciones sin “scope”, backups/adjuntos sin retención alineada, y logs que accidentalmente guardan PII o credenciales.
- La forma más vendible (y auditable) de gobernanza es convertirla en: clasificación por entidad + controles por canal de salida + checklists con evidencia mínima.

***

## Definitions and why it matters

**Facts**

- DLP (Data Loss Prevention) se usa para proteger PII y otros datos sensibles de exposición o salida no autorizada.[^2]
- El principio de “storage limitation” (limitación del plazo de conservación) indica que los datos personales deben guardarse el menor tiempo posible según la finalidad.[^4][^3]

**Inferences**

- **PII en CRM**: cualquier dato que identifique (directa o indirectamente) a una persona (ej.: email, teléfono, documento, dirección), más “quasi-identifiers” (combinaciones que re-identifican).
- **Retención**: reglas por tipo de dato/entidad/evento (no “un número único”), con excepciones (legal hold, auditoría, disputa comercial).
- **Audit trail**: registro de actividades relevante para reconstruir quién hizo qué y soportar investigación/controversias (fraude, reclamos, incidentes, chargebacks B2B).
- **Tamper-evident**: no garantiza “imposible de alterar”, sino “si alteras, queda evidencia criptográfica/operativa”.

***

## Principles and best practices (con citas por sección + fecha)

### 1) Clasificación por entidad CRM (Account/Contact/Lead/Opportunity/Activities) — (2026-02-17)

**Facts**

- La clasificación/etiquetado de datos es una base práctica para ejecutar políticas de retención y reducir riesgo.[^10]

**Inferences**

- Modelo recomendado de clases (simple y auditable):
    - **Public**: publicable sin daño.
    - **Internal**: uso interno, daño limitado.
    - **Confidential**: daño material si se expone.
    - **Restricted**: PII/sensibles/regulatorios; acceso mínimo y exportación controlada.

Tabla sugerida (ejemplo “mínimo útil”):


| Entidad CRM | Campos típicos | Clase sugerida | ¿PII? | Sensibilidad de exportación |
| :-- | :-- | --: | --: | :-- |
| Account | Razón social agencia, RIF/NIT (si aplica), dirección fiscal, condiciones comerciales, cuentas bancarias | Confidential / Restricted | A veces (si hay unipersonal) | Alta: incluye pricing, condiciones, potencial fraude |
| Contact | Nombre, email, teléfono, cargo, WhatsApp, documento (si lo guardan), preferencias | Restricted | Sí | Muy alta: exfil directa y suplantación |
| Lead | Origen, email, teléfono, notas de calificación, campañas | Restricted | Sí | Muy alta: fuga de base comercial |
| Opportunity | Monto, margen, etapa, motivo de pérdida, cotizaciones, acuerdos | Confidential | No siempre | Alta: inteligencia comercial + pricing |
| Activities (calls/emails/notes) | Transcripciones, adjuntos, negociaciones, IDs de reserva, incidencias | Confidential / Restricted | Frecuente | Crítica: suele contener “PII accidental” y secretos |

Checklist verificable (evidencia mínima):

- Inventario de campos sensibles por entidad (exportable a CSV interno): nombre de campo, clase, justificación, owner.
- Screenshot/config export-permissions por rol (o JSON de IAM/permission sets).
- Muestreo de 20 registros por entidad mostrando que no hay campos “prohibidos” sin necesidad (ej.: documento en Activities).

***

### 2) Riesgos de exportación (CSV/API/Integraciones/Adjuntos/Backups) — (2026-02-17)

**Facts**

- Sin controles DLP/monitoreo, datos sensibles en un CRM pueden exponerse o descargarse/exfiltrarse; el problema suele ser permisos excesivos y mala configuración.[^1]
- DLP busca descubrir/monitorear/remediar datos sensibles (PII, financieros, secretos) en registros y adjuntos para evitar exposición.[^2][^1]

**Inferences**
Riesgos típicos por canal (lo que duele en auditoría y en operación):

- **Export “one-click” (CSV/Excel/reportes)**: extracción masiva sin rastro suficiente, envío por email/Drive.
- **API tokens / connected apps**: integraciones con “scope” amplio, tokens largos, rotación pobre.
- **Adjuntos**: pasaportes, vouchers, capturas de pagos (aunque “no debería”, termina pasando).
- **Backups**: retención infinita “por si acaso” rompe borrado efectivo.
- **Sandboxes**: copias de producción sin masking.

Controles recomendados (seguro vs agresivo):

- **Seguro**: exportación solo a roles específicos + aprobación para export masivo + watermarking + logs de export + DLP sobre adjuntos.
- **Agresivo**: bloquear export masivo por defecto, “just-in-time access” para export, y scopes de API por objeto/campo con caducidad corta.

Checklist verificable (evidencia mínima):

- Lista de roles con permiso de export + fecha última revisión.
- Registro de eventos “export/report download/API bulk read” (conteo semanal) y 3 ejemplos con actor/tiempo/objeto.
- Matriz de integraciones: nombre app, owner, scopes, rotación token, last used, plan de revocación.

***

### 3) Masking y logging seguro (no filtrar PII/secretos) — (2026-02-17)

**Facts**

- OWASP recomienda no registrar directamente datos personales sensibles ni secretos (tokens, passwords, keys); en su lugar, remover/enmascarar/hashear/cifrar según necesidad.[^5]
- OWASP también recomienda sanitizar datos para prevenir ataques de “log injection” (CR/LF y delimitadores).[^5]

**Inferences**
Patrones prácticos:

- **Masking**: mostrar solo últimos 2–4 caracteres (teléfono/email parcial) para soporte.
- **Hashing**: para correlación (ej.: hash(email) para deduplicación) sin exponer el valor.
- **Tokenización**: reemplazo por token reversible solo vía servicio autorizado (útil si necesitas “re-hidratar” por proceso).
- **Logging de eventos, no de payloads**: registra “se exportaron 1,240 Contacts” y el filtro, pero no la data.

Checklist verificable (evidencia mínima):

- Reglas de redacción en logs (lista de patrones): email, teléfono, doc-id, access_token, authorization header.
- 10 líneas de log muestreadas (redactadas) demostrando: sin PII en claro y con request-id/actor.
- Prueba negativa: intento de inyectar CR/LF en un campo “notes” y ver que el log queda sanitizado.

***

### 4) Retención y borrado (incluye legal hold y backups) — (2026-02-17)

**Facts**

- La guía del ICO (principio de storage limitation) enfatiza borrar o anonimizar datos personales cuando ya no se necesitan; esto reduce riesgos de tener datos irrelevantes/excesivos y de usarlos por error.[^3]
- La UE explica que los datos deben almacenarse por el período más corto posible, considerando el propósito del tratamiento.[^4]

**Inferences**
Diseño recomendado (operable en CRM):

- Retención por **estado** y **finalidad** (ej.: Lead no convertido, Opportunity perdida, Contact inactivo, Activity cerrada).
- Borrado por capas: **soft delete** (operación) → **hard delete** (compliance) → **purga de backups** (o “crypto-shredding” si aplica).
- “Legal hold” como override auditable: quién lo activó, por qué, alcance, expiración.

Checklist verificable (evidencia mínima):

- Política de retención (tabla): entidad, condición, plazo, acción (anonimizar/borrar/archivar), excepción legal hold.
- Evidencia de jobs/automatizaciones: última corrida, volumen afectado, errores, y 3 tickets de verificación.
- Evidencia de borrado efectivo: registro de solicitud + id del registro + confirmación de purga (incluye adjuntos) o justificación de imposibilidad.

***

### 5) Tamper-evident logging (conceptual) — (2026-02-17)

**Facts**

- OWASP sugiere incorporar detección de manipulación (tamper detection) y/o mover logs a medios “read-only” lo antes posible para reducir alteraciones.[^5]
- Una aproximación clásica para detectar manipulación en audit logs usa estructuras como **hash chaining** (y MAC) para que cambios/borrados sean detectables.[^8]
- En entornos regulados, WORM (Write Once, Read Many) y/o sistemas de audit-trail se usan como caminos de cumplimiento para retención inmutable.[^9]

**Inferences**
Opciones de arquitectura (de menor a mayor robustez):

- **A) Centralizado + controles de acceso + alertas**: logs a SIEM, RBAC estricto, separación de duties.
- **B) Append-only lógico**: tabla/event store donde no hay UPDATE/DELETE; solo append, con “tombstones” para correcciones.
- **C) Hash chain / Merkle**: cada evento incluye hash del anterior (o raíz Merkle por lote diario) + firma; auditor valida integridad.
- **D) Inmutabilidad de storage (WORM/object lock)**: storage con retención inmutable y “legal hold” a nivel de bucket/objeto.

Checklist verificable (evidencia mínima):

- Prueba de integridad: recalcular hash chain de un día y verificar que coincide con “root hash” almacenado/firmado.
- Evidencia de separación de funciones: admins del CRM no pueden borrar logs; seguridad/auditoría tiene lectura y trazabilidad de accesos.
- Evidencia de inmutabilidad: política de retención en storage + intento controlado de borrado que falle + ticket de cambio aprobado.

***

## Examples (aplicado a CRM enterprise)

**Facts**

- Los logs deben evitar PII/secretos y protegerse contra manipulación; OWASP describe explícitamente exclusiones (tokens, PII sensible) y controles de protección/tamper detection.[^5]
- NIST 800-53 incluye controles de auditoría (familia AU) orientados a definir eventos, contenido, retención y protección de logs.[^7]

**Inferences**
Ejemplo 1 — Exportación masiva de Contacts (hallazgo + evidencia mínima)

- Hallazgo: Rol “Sales_All” puede exportar todos los Contacts sin aprobación.
- Evidencia mínima: screenshot de permisos del rol + 1 evento de auditoría “export contacts” (actor, timestamp, cantidad) + lista de usuarios con ese rol (conteo).
- Remediación: mover export a rol “Ops_Compliance”, requerir aprobación para >N registros, y alertas por umbral.

Ejemplo 2 — Logs con PII en claro (hallazgo + evidencia mínima)

- Hallazgo: el servicio de integración registra payload completo de “Contact create” incluyendo email/teléfono.
- Evidencia mínima: 3 líneas de log (redactadas) mostrando que el campo aparece, más el commit/config que habilitó debug logging.
- Remediación: logging por eventos (status code, request-id), redacción automática por regex, y rotación de logs.

Ejemplo 3 — Retención inconsistente (Activities infinito; backups eternos)

- Hallazgo: Activities (notas) nunca expiran; backups se guardan 7 años “por default” sin mapeo a política.
- Evidencia mínima: política inexistente o desactualizada + configuración de retención de backups + muestreo de Activities >36 meses con PII.
- Remediación: retención por tipo de Activity y finalidad; anonimizar texto libre; alinear backups con “borrado efectivo” (incluye adjuntos).

Ejemplo 4 — Tamper-evident “light” con hash diario

- Diseño: generar “daily root hash” (Merkle o hash chain por lote) de eventos críticos (export, cambio de permisos, borrado) y guardarlo en storage inmutable.
- Evidencia mínima: script de cálculo + root hash del día + verificación independiente por auditoría interna.

***

## Metrics / success signals

**Facts**

- Borrar/anonomizar cuando ya no se necesita reduce el riesgo asociado a retención excesiva.[^3]
- DLP/controles de exfil buscan reducir exposición de PII y datos sensibles.[^2]

**Inferences**
Métricas recomendadas (operables en CRM + SIEM):

- % de entidades/campos clasificados (objetivo: 100% en objetos core).
- 
# de eventos de export masivo por semana y por rol (tendencia a la baja, con razones justificadas).

- % de integraciones con token rotado en <90 días; % con scopes mínimos por objeto/campo.
- % de logs muestreados sin PII/secretos (objetivo: 0 hallazgos críticos).
- Cumplimiento de SLA de borrado: p95 días desde solicitud hasta purga efectiva (incluye adjuntos).
- Cobertura de audit trail: % de eventos críticos con “quién/qué/cuándo/resultado” + correlación (request-id).

***

## Operational checklist

**Facts**

- OWASP indica que se deben proteger los mecanismos de logging y evitar registrar PII sensible o secretos.[^5]
- La retención debe estar justificada por finalidad y no extenderse innecesariamente.[^4][^3]

**Inferences**
Checklist 1 — Clasificación (verificable)

- Inventario de campos por entidad con clase, owner, justificación, fecha última revisión.
- Etiquetado técnico (metadata) aplicado: PII=true, Restricted=true, ExportControlled=true.
- “Text free-form” (notes/activities) tratado como Restricted por defecto.

Checklist 2 — Exportación / exfil (verificable)

- Export masivo requiere rol específico + aprobación (ticket) + límite por umbral.
- API: scopes mínimos, rotación tokens, “last used” monitoreado, revocación automatizada.
- Adjuntos: scanning/etiquetado + bloqueo de descarga para Restricted salvo excepción.

Checklist 3 — Logging seguro (verificable)

- Redacción automática (PII/secretos) + sanitización CR/LF.
- Niveles de log: debug deshabilitado en prod o con expiración corta.
- Acceso a logs con RBAC + auditoría de accesos a logs.

Checklist 4 — Retención y borrado (verificable)

- Tabla de retención por entidad/estado; legal hold documentado y con expiración.
- Borrado: soft→hard→backups (o crypto-shred) con evidencia por caso.
- Revisión trimestral de “sobre-retención” y eliminación de ROT (redundante/obsoleto/trivial).

Checklist 5 — Tamper-evident (verificable)

- Logs críticos en storage inmutable o append-only + hash chain/Merkle + verificación periódica.
- Separación de duties: admins CRM sin permisos para borrar logs.
- Prueba de alteración controlada detectada (ejercicio interno) y registro del incidente.

***

## Anti-patterns

**Facts**

- Registrar tokens/secretos o PII sensible en logs es una mala práctica explícitamente desaconsejada.[^5]

**Inferences**

- “Export permitido para todos porque es más rápido”.
- “Retención infinita por si acaso” (especialmente en backups y adjuntos).
- Sandboxes con datos productivos sin masking.
- Logs con payload completo “para debug”, sin expiración y con acceso amplio.
- Audit trail solo en el CRM, sin centralización, sin protección, sin verificación de integridad.
- Legal hold informal por chat/correo sin control de alcance/expiración.

***

## Diagnostic questions

**Facts**

- El principio de storage limitation obliga a justificar y limitar el tiempo de conservación de datos personales.[^3][^4]
- OWASP recomienda excluir/enmascarar PII sensible y secretos de los logs.[^5]

**Inferences**
Preguntas (para descubrir brechas rápido):

- ¿Quién puede exportar Contacts/Leads hoy y cómo lo demuestras en 60 segundos (permiso + log)?
- ¿Qué integraciones tienen acceso “read all” y cuándo fue su último uso?
- ¿Dónde pueden terminar adjuntos sensibles (CRM, email, drive, ticketing) y qué control existe en cada salto?
- ¿Cuál es tu tabla de retención por entidad y qué job la hace cumplir (con evidencia de última corrida)?
- ¿Puedes borrar “de verdad” un Contact (incluyendo Activities y adjuntos) y demostrarlo incluyendo backups?
- ¿Tus logs contienen emails/teléfonos/tokens? (muestra de 1000 líneas con detección automática).
- Si un admin intenta borrar 500 eventos de auditoría, ¿cómo lo detectas (tamper-evident) y en cuánto tiempo?

Ejemplos de hallazgos con evidencia mínima (plantillas)

- Hallazgo: “Export masivo sin control” → Evidencia: permiso del rol + 1 log de export + lista de usuarios con rol.
- Hallazgo: “PII en logs” → Evidencia: 3 líneas de log redactadas + config de logging + ticket/commit.
- Hallazgo: “Retención inexistente” → Evidencia: política ausente + query de registros >X meses + captura de config de backups.
- Hallazgo: “Integridad de audit trail no verificable” → Evidencia: ausencia de inmutabilidad/hash roots + prueba de borrado posible por admin.

***

## Sources (o referencia a SOURCES.md)

Fuentes clave usadas:

- ICO — UK GDPR Principle (e): Storage limitation (actualizado 2025-07-23).[^3]
- Comisión Europea — “For how long can data be kept…?” (2022-12-31).[^4]
- OWASP Cheat Sheet Series — Logging Cheat Sheet (incluye exclusión/enmascarado de PII/secretos y tamper detection).[^5]
- NIST SP 800-53 Rev. 5 (controles AU de auditoría/retención/protección).[^7]
- Snodgrass et al. — Tamper Detection in Audit Logs (hash chaining/MAC; PDF).[^8]
- Smarsh — SEC Rule 17a-4 (WORM y audit-trail como vías de cumplimiento; 2026-01-09).[^9]
- Salesforce — DLP overview/guide (2026-01-28).[^2]
- Strac — CRM DLP in Salesforce (ejemplo de exposición por mala configuración/permisos; 2025-08-31).[^1]

Añadidos sugeridos a `SOURCES.md` (sin duplicados):

- OWASP Logging Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- ICO Storage limitation (Principle e) — https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/
- EU “For how long can data be kept…” — https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/how-long-can-data-be-kept-and-it-necessary-update-it_en
- NIST SP 800-53 Rev.5 PDF — https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf
- Snodgrass et al., Tamper Detection in Audit Logs (PDF) — https://collberg.cs.arizona.edu/content/research/papers/snodgrass04tamper.pdf
- Smarsh SEC Rule 17a-4 explainer — https://www.smarsh.com/regulations/sec-rule-17a-4-records-preservation/
- Salesforce DLP guide — https://www.salesforce.com/platform/data-loss-prevention/guide/
- Strac CRM DLP in Salesforce — https://www.strac.io/blog/crm-data-loss-prevention-in-salesforce

***

## Key takeaways for PM practice

- Diseña gobernanza como producto: clasificación por entidad + controles por canal de salida + evidencia mínima auditable.
- Exportación es el “punto de fuga” \#1: conviértela en capability controlada (roles, umbrales, approvals, trazabilidad).
- Logging seguro: eventos sí, payloads no; redacción/sanitización por defecto y debug con expiración.[^5]
- Retención/borrado no es policy PDF: es automatización + legal hold + prueba de borrado efectivo (incluye backups).[^4][^3]
- Tamper-evident no requiere “blockchain”: requiere integridad verificable (append-only + hash roots + inmutabilidad + separación de duties).[^9][^8][^5]
<span style="display:none">[^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29]</span>

<div align="center">⁂</div>

[^1]: https://www.strac.io/blog/crm-data-loss-prevention-in-salesforce

[^2]: https://www.salesforce.com/platform/data-loss-prevention/guide/

[^3]: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/

[^4]: https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/how-long-can-data-be-kept-and-it-necessary-update-it_en

[^5]: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html

[^6]: https://hoop.dev/blog/audit-logs-nist-800-53-simplifying-compliance-and-security/

[^7]: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf

[^8]: https://www.vldb.org/conf/2004/RS13P1.PDF

[^9]: https://www.smarsh.com/regulations/sec-rule-17a-4-records-preservation/

[^10]: https://bigid.com/es/blog/what-is-data-retention/

[^11]: pasted-text.txt

[^12]: https://learn.microsoft.com/es-es/dynamics365/customerengagement/on-premises/developer/introduction-entities?view=op-9-1

[^13]: https://gdprlocal.com/gdpr-storage-limitation/

[^14]: https://tietosuoja.fi/en/storage-limitation

[^15]: https://www.scribd.com/document/752825173/OWASP-Logging-Cheat-Sheet

[^16]: https://www.accountablehq.com/post/hipaa-technical-safeguards-list-mapped-to-nist-800-53-controls

[^17]: https://gdpr-info.eu/art-5-gdpr/

[^18]: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

[^19]: https://www.reddit.com/r/gdpr/comments/vwjhck/can_personal_information_be_stored_for_the_entire/

[^20]: https://www.scrut.io/post/nist-800-53-compliance-checklist

[^21]: https://www.usenix.org/legacy/event/sec09/tech/slides/crosby.pdf

[^22]: https://collberg.cs.arizona.edu/content/research/papers/snodgrass04tamper.pdf

[^23]: https://www.archondatastore.com/blog/sec-finra-worm-compliance/

[^24]: https://github.com/dmtkfs/pg-tamper-log

[^25]: https://www.nightfall.ai/blog/dlp-101-how-to-prevent-data-exfiltration-in-the-cloud

[^26]: https://news.ycombinator.com/item?id=25995034

[^27]: https://assurancedimensions.com/understanding-sec-rule-17a4-requirements-for-broker-dealers/

[^28]: https://www.reddit.com/r/CryptoCurrency/comments/1p8ypm2/anyone_using_blockchain_for_proof_nothing_got/

[^29]: https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions/rule-amendments-broker

