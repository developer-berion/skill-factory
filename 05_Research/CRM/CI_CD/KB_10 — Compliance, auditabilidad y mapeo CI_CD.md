<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_10 — Compliance, auditabilidad y mapeo CI/CD → controles (SOC 2 / ISO 27001 / GDPR)

## Executive summary (10–15 líneas)

**Facts:** En auditorías SOC 2, los entornos CI/CD añaden “control points” que deben estar documentados, monitoreados y ser auditables (ej. revisión por PR, identificadores únicos, y trazabilidad end‑to‑end de quién cambió qué y cuándo).[^1]
**Facts:** En SOC 2, el change management se espera como un proceso controlado con autorización, documentación y pruebas, y con énfasis en registros de cambios.
**Facts:** ISO/IEC 27001:2022 explicita controles para change management (Anexo A 8.32) y para logging (Anexo A 8.15), lo que hace que la evidencia de pipeline (aprobaciones, registros, monitoreo) sea “first‑class citizen” para auditoría.[^2][^3]
**Facts:** ISO 27001 también exige segregación de funciones (Anexo A 5.3) para reducir riesgo de fraude/error/bypass de controles, típico punto sensible en despliegues a producción.[^4]
**Facts:** GDPR refuerza accountability (Art. 5(2)) y vuelve críticos los audit trails y logs de acceso/procesamiento de datos personales, cuidando minimización y retención.[^5]
**Facts:** Para GDPR, prácticas de logging deben registrar accesos (quién/cuándo/propósito) y proteger logs contra manipulación, incluso “logs de los logs” (meta‑logs) para auditar el acceso a los propios registros.[^6]
**Inferences:** El enfoque más eficiente es “compliance by design”: convertir el pipeline en generador automático de evidencias (artefactos, reportes, aprobaciones, bitácoras) con retención y trazabilidad por release.
**Inferences:** La clave operativa es mapear cada control a 1–3 piezas de evidencia repetibles (no PDFs manuales), y blindar SoD: quien desarrolla no debe ser quien aprueba/promueve a producción.
**Inferences:** Para CRM enterprise (alto volumen de cambios + PII), el pipeline debe producir evidencia tanto de cambios de código como de cambios de configuración/datos (migraciones) y de accesos privilegiados.

***

## Definitions and why it matters

**Facts:** “Audit trail” en SOC 2/CI‑CD se apoya en identificar cambios con IDs únicos (build/change numbers, cuentas de sistema) y registrar quién cambió qué y cuándo, de forma monitoreable end‑to‑end.[^1]
**Facts:** “Change management” en el contexto SOC 2 se describe como prácticas para controlar cambios a infraestructura/datos/software con autorización, documentación y pruebas.
**Inferences:** En B2B enterprise, auditabilidad no es “para el auditor”: es una palanca comercial para cerrar deals (security review) y reducir fricción operativa (menos retrabajo, menos “evidencia a mano”).
**Inferences:** Si el pipeline no “emite evidencia”, la organización paga el impuesto de auditoría cada trimestre: capturas, correos, aprobaciones fuera de sistema y trazabilidad incompleta.

***

## Principles and best practices (Feb 2026)

### 1) Change management trazable (SOC 2 + ISO 27001)

**Facts:** En CI/CD, auditores SOC 2 esperan un proceso de revisión enforced (ej. pull request con peer review) antes de merge a la base de código.[^1]
**Facts:** ISO 27001:2022 Anexo A 8.32 requiere procedimientos/reglas para gestionar cambios y proteger activos mientras se hacen cambios.[^3]
**Inferences:** Regla práctica: “no hay ticket/PR/aprobación → no hay deploy”; cada release debe enlazar ticket ↔ PR ↔ build ↔ artefacto ↔ despliegue ↔ monitoreo post‑deploy.

### 2) Evidencia automática “por defecto”

**Facts:** En SOC 2, la evidencia típica incluye logs de acceso e historial de cambios de permisos, entre otros artefactos que demuestran operación consistente de controles.[^7]
**Facts:** SOC 2 change management enfatiza documentación detallada de alteraciones y change logs (quién/hizo/por qué).
**Inferences:** Define un “evidence bundle” por release (carpeta o registro inmutable) con: reportes de tests, resultados SAST/DAST, SBOM, aprobaciones, y bitácoras de despliegue; auditoría = consultar bundle, no reconstruir historia.

### 3) Segregación de funciones (SoD) y “break-glass” controlado

**Facts:** ISO 27001:2022 Anexo A 5.3 busca prevenir que una sola persona pueda cometer/ocultar/justificar acciones que afecten negativamente a la organización, evitando el override de controles.[^4]
**Facts:** Buenas prácticas de SOC 2 change management incluyen limitar permisos de despliegue a producción a personal calificado y separar ambientes (dev/test/staging/prod).
**Inferences:** Implementa SoD con RBAC + branch protections + approvals obligatorias; y para emergencias, “break-glass” con expiración, registro reforzado, y post‑mortem obligatorio.

### 4) Logs de auditoría: completos, protegidos y revisables

**Facts:** ISO 27001:2022 Anexo A 8.15 define la necesidad de logging de eventos relevantes (incluyendo acciones/modificaciones en sistemas/datos durante una sesión) y buenas prácticas de gestión/protección de logs.[^2]
**Facts:** Para GDPR, mantener logs/audit trails de acceso y procesamiento de datos personales soporta accountability (Art. 5(2)), y se deben definir periodos de retención y aplicar minimización/pseudonimización cuando sea posible.[^5]
**Facts:** GDPR y logging: se recomienda registrar accesos (quién/cuándo/propósito), asegurar almacenamiento de logs y auditar incluso el acceso a los propios logs (meta‑logs).[^6]
**Inferences:** En pipeline, lo crítico es “immutability + time sync + correlación”: logs centralizados, firmados o WORM (si aplica), con correlación por release/build y retención alineada a riesgo/contratos.

***

## Examples (aplicado a CRM enterprise)

**Facts:** En CI/CD para SOC 2, es relevante trackear identificadores únicos (build/change numbers, system accounts) y registrar acciones end‑to‑end para audit trail.[^1]
**Inferences (ejemplo 1 — cambio de código CRM):**

- Un PR que toca el módulo de “permisos de cuenta” exige: 2 aprobaciones (Tech Lead + Security), checks obligatorios (tests + SAST), y etiqueta de riesgo “HIGH”; el pipeline bloquea merge si falta algo.
- Evidencia generada: link PR, approvals, resultados de tests, reporte SAST, commit hash firmado, build ID, artefacto versionado, log de deploy y verificación post‑deploy.

**Facts:** ISO 27001:2022 Anexo A 8.33 pide seleccionar/proteger/gestionar información de prueba; usar datos productivos en test sin control es un fallo común.[^8][^9]
**Inferences (ejemplo 2 — datos para testing CRM):**

- Para pruebas de performance del CRM, se genera dataset sintético (o seudonimizado) en job controlado; si se requiere copia parcial de prod, se exige aprobación explícita y se registra la operación.
- Evidencia: job run + aprobación + hash del dataset + política de masking aplicada + logs de acceso al entorno de test.

**Facts:** ISO 27001:2022 Anexo A 5.3 se implementa típicamente con separación de roles y controles para evitar conflicto (ej. deploy a prod y admin).[^4]
**Inferences (ejemplo 3 — SoD en despliegue CRM):**

- Devs no tienen permisos de “promote to prod”; solo SRE/Release Managers pueden promover, y siempre con aprobación registrada; emergencias usan “break‑glass” con expiración.
- Evidencia: políticas RBAC/IAM, logs de cambios de permisos, registros de promoción por ambiente, bitácora de break‑glass y revisión posterior.

***

## Metrics / success signals

**Facts:** Wipfli recomienda mantener trazabilidad con identificadores únicos (build/change numbers) y registro de quién cambió qué y cuándo, como base de audit trail para SOC.[^1]
**Inferences (métricas operables):**

- % de despliegues a prod con PR aprobado + checks verdes (target: 100%).
- Lead time “ticket → prod” segmentado por riesgo (LOW/MED/HIGH) y tasa de emergency changes.
- Cobertura de evidencia: % releases con “evidence bundle” completo y consultable (target: >95% en 30 días).
- SoD health: \# eventos de bypass (break‑glass) por mes y tiempo a cierre de post‑mortem.
- Logging health: % servicios con logs centralizados + correlación por release, y tasa de fallas de ingesta de logs.

***

## Operational checklist

**Facts:** SOC 2 change management incluye autorización, documentación y testing como componentes centrales.
**Facts:** ISO 27001 Anexo A 8.32 y 8.15 refuerzan procedimientos de cambio y logging como controles auditables.[^3][^2]
**Inferences (lista accionable para implementar en 2–4 semanas):**

- Enforce PR reviews (mínimo 1–2), branch protection, y checks obligatorios (tests, lint, SAST).
- Exigir “change ID” (ticket) en el PR y propagarlo al build/release (misma clave en todo el pipeline).
- Separar roles: dev ≠ approver ≠ deployer; definir break‑glass con expiración, justificación y revisión.
- Generar y almacenar artefactos inmutables por build (version + hash), y promover entre ambientes (no “rebuild”).
- Centralizar logs (CI runner, SCM, artifact repo, deploy tool, cloud) con retención definida; habilitar alertas ante bypass o deploy manual.
- Para GDPR/PII: minimizar datos en logs, seudonimizar IDs cuando aplique, y documentar retención/propósito de logging.

***

## Anti-patterns

**Facts:** Wipfli advierte que cambios de emergencia pueden saltarse procedimientos estándar; los controles deben loguear y monitorear esos emergency changes.[^1]
**Facts:** Para GDPR, retención y minimización aplican también a logs; registrar “todo para siempre” sin base/riesgo es un problema.[^5]
**Inferences (lo que más te rompe auditoría y operaciones):**

- Deploys manuales “por consola” sin registro estructurado ni aprobación rastreable.
- PRs aprobados “por WhatsApp/Slack” sin evidencia en el sistema (no auditable).
- Misma persona: escribe el cambio + lo aprueba + lo despliega (SoD roto).
- Logs sin protección contra manipulación, sin time sync, o sin retención definida.
- Copiar data productiva a testing sin control, sin masking, sin trazabilidad.

***

## Diagnostic questions

**Facts:** En SOC 2 para CI/CD, el auditor busca un proceso de revisión enforced (PR/peer review) y trazabilidad con IDs únicos.[^1]
**Facts:** ISO 27001:2022 incluye control explícito de change management (8.32) y logging (8.15).[^2][^3]
**Inferences (preguntas que revelan gaps rápido):**

- ¿Puedes tomar un incidente en prod y reconstruir en <15 min: ticket → PR → build → deploy → cambios exactos → quién aprobó?
- ¿Qué porcentaje de deploys a prod ocurre sin “promoción” desde un artefacto ya construido y firmado/hasheado?
- ¿Quién puede hacer deploy a prod hoy, y dónde queda la evidencia de su aprobación y del evento?
- ¿Cuántos sistemas generan logs de auditoría y cuántos los centralizan con retención y protección?
- ¿Cómo controlas emergency changes y cómo demuestras revisión posterior (post‑implementation)?

***

## Tabla: control → evidencia generada por pipeline

| Control (marco) | Qué exige (resumen) | Evidencia generada por pipeline (ejemplos concretos) |
| :-- | :-- | :-- |
| SOC 2 (cambio y audit trail en CI/CD) | Revisión enforced (PR), trazabilidad e IDs únicos para audit trail. [^1] | PR con peer review requerido, registro de aprobaciones; build number/change number; mapeo “quién cambió qué y cuándo”; logs de deploy automatizado. [^1] |
| SOC 2 (change management) | Autorización, documentación y testing de cambios; change logs como evidencia. | Aprobación formal (en PR/CAB digital); reporte de tests (unit/integration/regression); bitácora de cambios por release con timestamps y responsables. |
| ISO 27001:2022 Anexo A 8.32 (Change management) | Procedimientos/reglas para gestionar cambios y proteger activos durante cambios. [^3] | Flujo “ticket→PR→build→release”; registro de evaluación de impacto/riesgo en plantilla de PR; aprobaciones y evidencia de rollback plan ejecutable (runbook versionado). |
| ISO 27001:2022 Anexo A 8.15 (Logging) | Definir eventos a loguear (incluye acciones/modificaciones en apps/datos) y gestionar/proteger logs. [^2] | Logs centralizados del pipeline (runner), del SCM, del artefacto y de despliegues; correlación por release/build; alertas por eventos sensibles (deploy manual, bypass). |
| ISO 27001:2022 Anexo A 5.3 (Segregation of duties) | Separar roles para evitar fraude/error/bypass de controles; evitar concentración de poder. [^4] | RBAC/IAM como código (repositorio) + evidencia de “quién puede promover a prod”; approvals obligatorias por rol; logs de cambios de permisos; registro break‑glass con expiración. |
| ISO 27001:2022 Anexo A 8.33 (Test information) | Test data debe seleccionarse, protegerse y gestionarse; evitar uso no controlado de data productiva. [^9][^8] | Job de generación de datos sintéticos/seudonimizados; aprobación explícita para copias desde prod; evidencia de masking; logs de acceso al entorno de test y al dataset. |
| GDPR Art. 5(2) (Accountability) | Logs/audit trails de acceso/procesamiento ayudan a demostrar accountability; definir retención y minimizar/pseudonimizar cuando aplique. [^5] | Auditoría de accesos a tablas/objetos con PII; retención de logs definida por política; pipeline que valida “no PII en logs” (reglas/escáner) y registra excepciones aprobadas. |
| GDPR (logging de accesos y meta-logs) | Registrar quién accede, cuándo y propósito; proteger logs contra manipulación; auditar accesos a los logs (meta‑logs). [^6] | Logs de acceso a sistemas de logging/SIEM; políticas de acceso a logs; evidencia de “quién consultó/exportó logs” y cuándo; alertas ante borrado/alteración. [^6] |


***

## Sources (o referencia a SOURCES.md)

**Facts (fuentes usadas):**

- Wipfli — “SOC 2 audit checklist: How CI/CD impacts audit readiness” (2025-10-15).[^1]
- Thoropass — “Best practices for SOC 2 change management” (2024-12-31).
- ISMS.online — “ISO 27001:2022 Annex A 8.15 – Logging” (2022-08-14).[^2]
- ISMS.online — “ISO 27001:2022 Annex A 8.32 – Change Management” (2025-09-01).[^3]
- Hicomply — “ISO 27001:2022 Annex A Control 5.3: Segregation of Duties” (2025-11-29).[^4]
- Wiz — “What Are GDPR Security Controls?” (2025-11-19).[^5]
- Exabeam — “How Does GDPR Impact Log Management?” (2025-06-26).[^6]
- ISO27001.com — “ISO 27001:2022 Annex A 8.33 Test Information” (2026-01-09).[^9]

**Inferences (cómo usar SOURCES.md):** Mantén estas URLs en `SOURCES.md` y referencia desde futuras KB para no re‑explicar el “por qué” de change management/logging/SoD en cada documento.

**Añadir a `SOURCES.md` (sin duplicados):**

- https://www.wipfli.com/insights/articles/ra-audit-ci-cd-as-part-of-your-soc-exam
- https://www.thoropass.com/blog/best-practices-for-soc-2-change-management
- https://www.isms.online/iso-27001/annex-a-2022/8-15-logging-2022/
- https://www.isms.online/iso-27001/annex-a-2022/8-32-change-management-2022/
- https://www.hicomply.com/hub/iso-27001-annex-a-5-3-segregation-of-duties
- https://www.wiz.io/academy/compliance/gdpr-security-controls
- https://www.exabeam.com/explainers/gdpr-compliance/how-does-gdpr-impact-log-management/
- https://iso27001.com/iso-270012022-annex-a-8-33-test-information/

***

## Key takeaways for PM practice

- Diseña el CI/CD como “máquina de evidencia”: por cada release debe existir un bundle consultable y repetible.
- SoD no es burocracia: es un control vendible (reduce riesgo) y evita que auditoría se vuelva investigación forense.
- Define la trazabilidad mínima: ticket ↔ PR ↔ build ↔ artefacto ↔ deploy ↔ logs/monitoreo.
- Logging sin retención/minimización te puede meter en problemas (costos y GDPR); define política y aplícala en pipeline.
- Para CRM enterprise, trata cambios de configuración/datos (migraciones, permisos) con el mismo rigor que el código.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26]</span>

<div align="center">⁂</div>

[^1]: pasted-text.txt

[^2]: https://www.isms.online/iso-27001/annex-a-2022/8-15-logging-2022/

[^3]: https://www.isms.online/iso-27001/annex-a-2022/8-32-change-management-2022/

[^4]: https://www.hicomply.com/hub/iso-27001-annex-a-5-3-segregation-of-duties

[^5]: https://www.wiz.io/academy/compliance/gdpr-security-controls

[^6]: https://www.exabeam.com/explainers/gdpr-compliance/how-does-gdpr-impact-log-management/

[^7]: https://cynomi.com/soc2/soc-2-criteria-explained/

[^8]: https://www.voragosecurity.com/annex-controls/iso-27001-2022-annex-a-8-33-test-information

[^9]: https://iso27001.com/iso-270012022-annex-a-8-33-test-information/

[^10]: https://www.nedigital.com/es/compliance-managed-services

[^11]: https://secureframe.com/es-es/hub/iso-27001/evidence-list

[^12]: https://continuumgrc.com/es/audit-compliance-solutions-cis/

[^13]: https://xygeni.io/es/blog/cicd-best-practices-transforming-software-development/

[^14]: https://www.iso27000.es/assets/files/ISO27k ISMS and controls status with SoA and gaps Spanish.xlsx

[^15]: https://www.isms.online/soc-2/controls/change-management-cc8-1-explained/

[^16]: https://www.hicomply.com/hub/iso-27001-annex-a-5-22-monitoring-review-change-management-of-supplier-services

[^17]: https://www.wipfli.com/insights/articles/ra-audit-ci-cd-as-part-of-your-soc-exam

[^18]: https://hightable.io/iso-27001-annex-a-5-22-monitor-review-and-change-management-of-supplier-services/

[^19]: https://nxlog.co/news-and-blog/posts/gdpr-compliance

[^20]: https://www.thoropass.com/blog/best-practices-for-soc-2-change-management

[^21]: https://hightable.io/iso27001-annex-a-8-32-change-management/

[^22]: https://hightable.io/iso-27001-annex-a-5-3-segregation-of-duties/

[^23]: https://www.isms.online/iso-27001/annex-a-2022/how-to-implement-iso-27001-2022-annex-a-control-8-32-change-management/

[^24]: https://iso-docs.com/blogs/iso-27001-2022-standard/iso-27001-2022-control-5-3-segregation-of-duties

[^25]: https://cyberzoni.com/standards/iso-27001/control-8-33/

[^26]: https://www.scrut.io/post/iso-27001-change-management

