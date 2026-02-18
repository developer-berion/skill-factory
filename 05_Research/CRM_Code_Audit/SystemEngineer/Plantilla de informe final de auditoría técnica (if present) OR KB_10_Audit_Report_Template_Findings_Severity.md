<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Plantilla de informe final de auditoría técnica (hallazgos + severidad + evidencia + plan 30/60/90)

## Executive summary (10–15 líneas)

**Facts:** Un informe final de auditoría técnica debe traducir hallazgos técnicos en riesgo accionable, con una estructura repetible: planificación, ejecución y post-ejecución (análisis, mitigación y reporte).[^1]
**Facts:** NIST SP 800-115 recomienda un enfoque por fases (Planning / Execution / Post-Execution) y resalta que el valor real aparece al convertir hallazgos en acciones de mitigación, apoyadas por análisis de causa raíz y reporte “tailored” a las audiencias.[^1]
**Facts:** Para que el reporte “cierre” operativamente, la evidencia debe ser objetiva, trazable y gestionada como dato sensible durante todo el assessment (recolección, almacenamiento, transmisión y destrucción).[^1]
**Inferences:** Esta plantilla está diseñada para acelerar decisiones (qué se arregla ya vs qué requiere refactor), reducir fricción con equipos (DevOps/Sec/Producto) y habilitar seguimiento (tickets, owners, fechas, validación).
**Inferences:** El entregable se arma en dos capas: (1) lectura ejecutiva (riesgo, prioridades, impacto), (2) apéndice técnico (pruebas, evidencias, pasos de reproducción, contexto).
**Inferences:** Incluye un esquema de severidad consistente, requisitos mínimos de evidencia por severidad, recomendaciones priorizadas (quick wins vs structural) y un plan 30/60/90 días con hitos verificables.

***

## Definitions and why it matters

**Facts:** NIST define “assessment” como el proceso de determinar qué tan efectivamente un objeto evaluado cumple objetivos de seguridad, usando testing, examination e interviewing para obtener evidencia.[^1]
**Facts:** En auditorías internas (ISO 27001), el principio operativo es “evidence-based review”: confirmar conformidad y que el sistema está implementado y mantenido (no solo documentado), registrando evidencia objetiva (IDs, screenshots, documentos, decisiones).[^1]
**Inferences:** “Hallazgo” = condición comprobable (hecho) + impacto potencial + causa probable + recomendación accionable + evidencia verificable; si falta cualquiera, se vuelve opinión.
**Inferences:** “Severidad” (para priorizar) conviene modelarla como Impacto (negocio/seguridad/operación) × Probabilidad (explotabilidad/frecuencia), y no solo como “qué tan feo suena”.
**Inferences:** “Quick win” = cambio acotado, bajo riesgo de regresión, alto retorno y validación rápida; “Structural fix” = elimina la causa raíz (arquitectura/proceso/control), requiere coordinación y ventanas de cambio.

***

## Principles and best practices (con citas por sección + fecha)

### 1) Estructura por fases y entregables claros (Feb 2026)

**Facts:** NIST SP 800-115 plantea una metodología por fases (Planning, Execution, Post-Execution) y ubica el reporte final y mitigación en post-ejecución.[^1]
**Inferences:** Tu documento final debería reflejar esa misma fase: “Qué se hizo” (metodología), “Qué se encontró” (hallazgos), “Qué se recomienda” (mitigación), “Qué se hará” (plan 30/60/90), “Cómo se valida” (retest/controles).

**Plantilla de secciones (orden sugerido)**

- Portada: nombre del assessment, cliente/sistema, fechas, versión del informe, clasificación de confidencialidad.
- Alcance: sistemas, entornos, exclusiones, supuestos, limitaciones.
- Metodología: técnicas usadas, ventanas, perfiles (black/gray/white), herramientas (si aplica), criterios de severidad.
- Resumen ejecutivo: postura general, distribución por severidad, top 5 riesgos, dependencias.
- Tabla de hallazgos (resumen) + detalle por hallazgo (fichas).
- Recomendaciones priorizadas: quick wins vs structural, dependencias, riesgos de implementación.
- Plan 30/60/90 días: hitos, owners, definición de “done”, validación.
- Apéndice técnico: evidencias, pasos de reproducción, logs sanitizados, configuraciones relevantes, trazabilidad a tickets.


### 2) Evidencia objetiva y trazable (Feb 2026)

**Facts:** En auditoría interna, se espera capturar evidencia objetiva mientras se ejecuta el trabajo (títulos/versions de documentos, fechas, URLs, IDs de tickets, screenshots) y enlazarla a requisitos/controles/hallazgos.[^1]
**Facts:** NIST SP 800-115 enfatiza el manejo de datos del assessment (colección, almacenamiento, transmisión, destrucción) como parte del proceso, por el riesgo de que la evidencia contenga información sensible.[^1]
**Inferences:** Regla práctica: cada hallazgo debe poder “defenderse” sin el auditor presente, solo con evidencia y reproducibilidad (o procedimiento de verificación).

**Evidencia mínima requerida (por tipo)**

- Captura visual: screenshots con timestamp, URL/host, usuario/rol (sanitizado), resaltando el punto exacto.
- Evidencia de sistema: extractos de logs, eventos SIEM, trazas (sanitizadas), IDs correlacionables.
- Evidencia de configuración: export/print de settings (IAM, firewall, CRM permissions), versión y entorno.
- Evidencia de proceso: políticas/procedimientos, aprobaciones, minutas, historial de cambios (PR/commit/ticket).
- Evidencia de verificación: resultado de retest, query/consulta de control, “before/after” comprobable.


### 3) Severidad consistente y accionable (Feb 2026)

**Facts:** NIST SP 800-115 sugiere traducir hallazgos técnicos en acciones de mitigación que mejoren la postura de seguridad, lo que requiere priorización práctica orientada a riesgo.[^1]
**Inferences:** Un esquema de 4 niveles suele ser suficiente para operación: Critical / High / Medium / Low, con criterios explícitos que reduzcan discusiones subjetivas.

**Criterios sugeridos de severidad (modelo simple)**

- Critical: compromiso de datos sensibles/PII, ejecución remota, bypass de auth, impacto operacional severo (caída o fraude), explotación probable y/o ya observada.
- High: explotación viable con esfuerzo moderado, impacto alto (datos, integridad, privilegios), o control clave ausente (logging/auditoría/backup) con exposición real.
- Medium: requiere condiciones específicas o impacto acotado, pero amerita planificación y fecha.
- Low: hardening, buenas prácticas, o deuda con baja probabilidad/impacto; se agrupa y se agenda.

**Qué es sensible (declararlo en el reporte)**

- Riesgo de interrupción (SLA), pérdida de integridad (cambios no autorizados), fuga de datos (clientes/contratos), credenciales/secrets, y evidencia que exponga topología o configuración.


### 4) Recomendaciones “doble carril”: quick wins vs structural (Feb 2026)

**Facts:** NIST SP 800-115 recomienda análisis (incluida causa raíz) para convertir hallazgos en mitigaciones accionables, no solo “parches” sueltos.[^1]
**Facts:** En auditoría ISO, las acciones correctivas deben abordar la causa (no solo el síntoma) y luego verificarse por efectividad, manteniendo evidencia de implementación.[^1]
**Inferences:** Para cada hallazgo, entrega dos opciones: segura (quick win con mínimo cambio) y agresiva (structural que elimina la causa), con riesgos y dependencias.

**Formato recomendado por hallazgo**

- Recomendación Quick win: qué cambiar hoy, quién lo hace, riesgo de regresión, cómo validar.
- Recomendación Structural: qué rediseñar (control/proceso/arquitectura), dependencia inter-áreas, costo/tiempo estimado, cómo validar y cómo prevenir recurrencia.


### 5) Seguimiento: owners, fechas y verificación (Feb 2026)

**Facts:** En ISO 27001 internal audit, los hallazgos deben alimentar acciones correctivas con responsables y fechas, y conservar evidencia (docs actualizados, registros, screenshots, minutas) para demostrar mejora continua.[^1]
**Facts:** NIST SP 800-115 incluye “reporting” y “remediation/mitigation” como actividades posteriores al testing, para asegurar que el esfuerzo derive en mejoras reales.[^1]
**Inferences:** Si no existe “Definition of Done” por hallazgo (incluido retest), el reporte se convierte en backlog eterno o en “promesas”.

***

## Examples (aplicado a CRM enterprise)

**Facts:** Un buen reporte suele separar una capa ejecutiva y un apéndice técnico con detalles y evidencias, para que distintos stakeholders puedan actuar sin perder trazabilidad.[^1]
**Inferences:** Ejemplo aplicado a un CRM enterprise (multi-tenant interno, integraciones, perfiles/roles, workflows, API keys, módulos de atención/ventas), con hallazgos típicos y cómo documentarlos.

### Ejemplo de tabla de hallazgos (resumen)

| ID | Hallazgo | Severidad | Evidencia requerida (mínima) | Recomendación quick win | Recomendación structural | Owner | Validación / “Done” |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| CRM-01 | Roles permiten exportar PII sin justificación (over-permission) | High | Screenshot de permisos por rol + export realizado (sanitizado) + ID de usuario/rol y entorno | Reducir permisos de export a roles mínimos; activar aprobación para export | Rediseñar RBAC por “job function”; implementar revisiones trimestrales de acceso | Security + CRM Admin | Retest: rol no autorizado no exporta; evidencia de cambio y aprobación registrada |
| CRM-02 | API key de integración almacenada en texto plano en pipeline/config | Critical | Extracto de config/secret store (sanitizado) + ruta de exposición + evidencia de uso | Rotar credenciales; mover a secret manager; revocar key expuesta | Implementar gestión central de secretos + scanning en CI + policy “no secrets” | DevOps | Retest: no hay secretos en repos/pipelines; key rotada y auditoría de rotación |
| CRM-03 | Falta de logging/audit trail para cambios en cuentas y límites de crédito | High | Config actual + ejemplo de cambio sin rastro + ausencia de eventos | Habilitar audit logs; alertas básicas para cambios críticos | Modelo de “tamper-evident logging” + integración SIEM + segregación de duties | CRM Admin + SecOps | Retest: cada cambio crítico genera evento; dashboards/alertas funcionando |
| CRM-04 | No hay prueba documentada de restore de backups (últimos 90 días) | Medium | Evidencia de backups + ausencia de restore test + procedimiento | Ejecutar restore test controlado; documentar resultados | Automatizar restore testing y métricas; runbook y RTO/RPO por módulo | Infra | Retest: restore test con evidencia; métricas reportadas mensualmente |
| CRM-05 | Reglas de workflow permiten aprobación “self-approve” en descuentos | High | Caso reproducible + configuración de workflow + log/ticket | Bloquear self-approve en reglas; revisión rápida de workflows críticos | Motor de aprobaciones con segregación por monto/cliente; auditoría y monitoreo | Producto + RevOps | Retest: self-approve no posible; pruebas automatizadas de reglas |

**Facts:** En auditoría interna se espera registrar evidencia como IDs, screenshots, minutos y vincular hallazgos a acciones y verificación de efectividad.[^1]
**Inferences:** En CRM enterprise, los “hallazgos caros” suelen vivir en (a) permisos/roles, (b) integraciones y secretos, (c) trazabilidad de cambios, (d) lógica de negocio (workflows), (e) continuidad operativa (backup/restore).

***

## Metrics / success signals

**Facts:** Un assessment tiene valor cuando los hallazgos se convierten en mitigaciones verificables y mejoran la postura, no solo cuando se enumeran vulnerabilidades.[^1]
**Inferences:** Métricas recomendadas para medir cierre real (por severidad y por dominio CRM).

- Time-to-triage: días desde entrega del reporte hasta owner + plan aprobado por hallazgo.
- Time-to-fix por severidad: mediana y P90 para Critical/High/Medium.
- Closure con evidencia: % de hallazgos cerrados con retest + artefactos (ticket, change, screenshot/log).
- Recurrencia: % de hallazgos reabiertos o repetidos en el siguiente ciclo.
- Cobertura de controles: % de módulos CRM con audit logging, RBAC revisado, secretos en vault, pruebas de restore realizadas.
- Riesgo residual aceptado: \# de excepciones aprobadas, con fecha de expiración y compensating controls.

***

## Operational checklist

**Facts:** NIST SP 800-115 enfatiza planificación (scope, objetivos, limitaciones, entregables) y post-ejecución (análisis, mitigación, reporte) para que el assessment sea exitoso.[^1]
**Facts:** En auditoría interna, durante el trabajo se debe capturar evidencia objetiva y luego transformar hallazgos en acciones con verificación de efectividad.[^1]
**Inferences:** Checklist práctico para producir el informe final sin “huecos”.

- Confirmar alcance final (incluye/excluye), entornos, fechas, limitaciones y supuestos.
- Congelar el esquema de severidad y criterios antes de redactar hallazgos.
- Para cada hallazgo: redactar en formato “condición → evidencia → impacto → causa probable → recomendación → validación”.
- Adjuntar evidencia mínima: screenshot/log/config/ticket, con sanitización y trazabilidad.
- Etiquetar quick win vs structural, con riesgo de implementación y dependencias.
- Asignar owner, ETA y definición de “done” (incluye retest).
- Armar plan 30/60/90 con hitos y capacidad real del equipo.
- Revisar consistencia: severidad vs impacto, duplicados, hallazgos derivados (misma causa raíz).
- Revisión final con stakeholders (Security, IT/DevOps, Producto/RevOps) y levantar “riesgos aceptados” explícitos.


### Plan 30/60/90 (plantilla)

**Facts:** La verificación de efectividad y la trazabilidad (acciones + evidencia) son claves para que el ciclo de auditoría produzca mejora continua.[^1]
**Inferences:** Estructura sugerida (adaptar a tu release cadence).

- 0–30 días (contención + quick wins): rotación de credenciales expuestas, hardening de permisos críticos, activar audit logs básicos, bloquear flujos de aprobación inseguros, agregar monitoreo mínimo.
- 31–60 días (estabilización): RBAC por función, secret management formal, dashboards y alertas, restore test documentado, playbooks.
- 61–90 días (estructural): rediseño de arquitectura/procesos (segregación de duties, motor de aprobaciones, CI policies), automatización de controles, auditoría de efectividad y retest completo.

***

## Anti-patterns

**Facts:** NIST SP 800-115 advierte que sin análisis y recomendaciones de mitigación, el assessment no mejora la postura; el reporte debe traducir hallazgos en acciones.[^1]
**Facts:** En auditoría interna, “pasar el audit” sin evidencias y sin acciones correctivas verificadas no demuestra mejora continua.[^1]
**Inferences:** Cosas que rompen la utilidad comercial/operativa del reporte.

- Severidad “a ojo” sin criterios; discusiones eternas y cero ejecución.
- Hallazgos sin evidencia mínima o sin reproducibilidad.
- Recomendaciones genéricas (“mejorar seguridad”, “capacitar usuarios”) sin owner, cambio concreto y validación.
- Listas enormes de Low sin agrupación (ruido) que tapan los High/Critical.
- No separar quick wins vs structural; todo entra al mismo backlog y nada se cierra.
- No declarar exclusiones/limitaciones; se asume cobertura total y luego hay reclamos.

***

## Diagnostic questions

**Facts:** En auditoría interna, entrevistas y revisión de evidencias ayudan a ubicar dónde está la evidencia y confirmar que lo documentado se ejecuta en la práctica.[^1]
**Inferences:** Preguntas para diagnosticar (y para evitar objeciones típicas) en un CRM enterprise.

- ¿Cuál es el “crown jewel” en el CRM (PII, pricing, crédito, contratos) y quién debería poder exportarlo?
- ¿Qué integraciones tienen llaves/tokens? ¿Dónde viven hoy y cómo se rotan?
- ¿Qué cambios son “críticos” (límites de crédito, cuentas, descuentos) y cómo se auditan end-to-end?
- ¿Cuál es el RTO/RPO esperado por módulo y cuándo fue el último restore test con evidencia?
- ¿Dónde se registra la aprobación de excepciones (riesgo aceptado) y cuándo expira?
- ¿Qué hallazgos comparten la misma causa raíz (p. ej., falta de gobierno de accesos)?

***

## Sources (o referencia a SOURCES.md)

**Facts:** NIST SP 800-115 es una guía base para planificar, ejecutar y reportar assessments técnicos, incluyendo fases, reporte y mitigación.[^1]
**Facts:** La guía de auditoría interna ISO 27001 usada aquí refuerza el enfoque evidence-based, registro de hallazgos y conversión a acciones correctivas con evidencia.[^1]

**Entradas para añadir a `SOURCES.md` (sin duplicados)**

- NIST. *SP 800-115: Technical Guide to Information Security Testing and Assessment* (Sep 2008). https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-115.pdf (accessed 2026-02-17).
- Iseo Blue. *How to run an ISO 27001 internal audit* (page content). https://iseoblue.com/iso-27001/implementation-guides/internal-audit/ (accessed 2026-02-17).

***

## Key takeaways for PM practice

- Diseña el reporte como un artefacto de ejecución: cada hallazgo debe cerrar con owner, fecha, evidencia y retest.
- Separa quick wins vs structural para evitar que “lo urgente” mate “lo importante” (y viceversa).
- En CRM enterprise, prioriza permisos/roles, integraciones (secrets), audit trail y workflows: ahí viven los riesgos de negocio.
- La evidencia no es un anexo: es el producto que reduce fricción y acelera aprobación/cierre.
- Un buen plan 30/60/90 convierte auditoría en roadmap operativo verificable.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^2][^3][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: pasted-text.txt

[^2]: https://csrc.nist.gov/pubs/sp/800/115/final

[^3]: https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-115.pdf

[^4]: https://csrc.nist.rip/library/NIST SB 2008-12 Guide To Information Security Testing And Assessment.pdf

[^5]: https://www.nist.gov/privacy-framework/nist-sp-800-115

[^6]: https://www.konfirmity.com/glossary/nist-sp-800-115

[^7]: https://www.isms.online/iso-27001/requirements-2022/how-to-implement-iso-27001-2022-clause-10-1-nonconformity-and-corrective-action/

[^8]: https://bluefire-redteam.com/what-is-owasp-asvs-and-how-it-guides-web-application-penetration-testing/

[^9]: https://kirkpatrickprice.com/blog/how-nist-sp-800-115-informs-information-security-practices/

[^10]: https://iseoblue.com/iso-27001/implementation-guides/internal-audit/

[^11]: https://www.centraleyes.com/how-the-owasp-application-security-verification-standard-helps-improve-software-security/

[^12]: https://www.softwaresecured.com/post/nist-sp-800-115-and-penetration-testing

[^13]: https://hightable.io/iso-27001-clause-10-2-nonconformity-and-corrective-action-essential-guide/

[^14]: https://haxoris.com/testing-methodologies/asvs

[^15]: https://redbotsecurity.com/nist-800-and-its-impact-on-penetration-testing-requirements-redbot-security/

[^16]: https://www.scribd.com/document/787346047/Non-Conformity-Report-01-3-Copy

