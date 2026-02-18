<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_11 — Secure SDLC: SAST, Secrets \& Dependency Scanning (CRM Enterprise)

## Executive summary (10–15 líneas)

**Facts:** Un SDLC seguro para un CRM enterprise se sostiene en “gates” automáticos en CI/CD (PR → build → release) que bloquean cambios inseguros antes de producción, apoyado por SAST, secret scanning y análisis de dependencias con SBOM.[^1][^2]
**Facts:** NIST SSDF recomienda integrar toolchains y definir criterios de verificación (“security checks”) como parte del proceso de desarrollo y release, no como actividad ad-hoc.[^1]
**Facts:** Para supply chain, NTIA define elementos mínimos de SBOM y reconoce formatos interoperables como SPDX y CycloneDX para intercambiarlo entre organizaciones.[^2]
**Facts:** Secret scanning reduce el riesgo de exfiltración por “secrets” en repositorios y se relaciona con CWE-540 (inclusión de info sensible en código).[^3]
**Facts:** SPDX estandariza identificadores de licencia para expresar licencias de forma no ambigua y automatizable.[^4][^5]
**Inferences:** En CRM (datos personales, integraciones, roles, auditoría), la estrategia práctica es: gates rápidos en PR (diff-based), gates completos en main (full scan + SBOM), y gates estrictos antes de deploy (sin críticos; excepciones con “break-glass”).
**Inferences:** Define severidades y SLAs por tipo de hallazgo (SAST/Secrets/SCA/License), y exige evidencia trazable como artefactos CI (reports, SBOM, logs, firmas) anexados al informe final para auditoría y para el cliente B2B.
**Inferences:** La matriz “hallazgo → impacto → quick win → structural fix → validación” convierte findings técnicos en acciones operativas vendibles (reducción de riesgo + control + evidencia).

***

## Definitions and why it matters

**Facts:** **SAST** (Static Application Security Testing) analiza el código/commit para detectar patrones de vulnerabilidad temprano en el ciclo (idealmente en PR y en builds).[^1]
**Facts:** **Secret scanning** detecta credenciales/tokens/keys expuestos en repositorios y puede complementarse con enforcement para prevenir pushes con secretos.[^3]
**Facts:** **Dependency scanning / SCA** identifica vulnerabilidades y riesgos en dependencias directas y transitivas; se operacionaliza mejor si existe un SBOM consumible.[^2]
**Facts:** **SBOM** es un inventario de componentes; NTIA define mínimos (p.ej., proveedor, nombre, versión, relaciones, autor, timestamp) y menciona SPDX/CycloneDX como formatos interoperables.[^2]
**Facts:** **Licensing scanning** valida obligaciones/compatibilidad de licencias OSS usando identificadores estandarizados (SPDX), reduciendo ambigüedad legal.[^5][^4]
**Inferences:** En un CRM enterprise, estos controles importan porque el “blast radius” de un bug es grande (multi-tenant, integraciones, datos sensibles, workflows), y porque ventas B2B exige evidencia repetible para compliance y due diligence (no promesas).

***

## Principles and best practices (con citas por sección + fecha)

### 1) CI/CD gates por capas (PR → main → release)

**Fecha:** 2026-02-17
**Facts:** SSDF promueve integrar toolchains y definir criterios de checks/gates (ej.: bloquear releases con vulnerabilidades críticas) como parte del proceso.[^1]
**Inferences (recomendado en CRM):**

- **Gate PR (rápido, 3–10 min):** SAST incremental, secret scanning (diff), política de dependencias (solo manifests/lockfiles), chequeos de calidad y “policy-as-code”.
- **Gate main (completo):** SAST full + baseline, dependency scan full (incluye transitivas), generación de SBOM, reporte de licencias.
- **Gate release/deploy (estricto):** “No Critical/High sin excepción”, SBOM adjunto, evidencia de integridad/provenance cuando aplique (attestations).

**Incluye / No incluye / Sensible:**

- **Incluye:** reglas automáticas “pass/fail”, umbrales por severidad, y “break-glass” auditable.
- **No incluye:** revisar manualmente cada finding (eso se prioriza por riesgo).
- **Sensible:** permitir bypass sin registro (esto mata la trazabilidad para auditoría y para clientes).


### 2) SAST operativo (reglas, ruido y ownership)

**Fecha:** 2026-02-17
**Facts:** SSDF enfatiza seguridad en el proceso de construcción y verificación y el uso de herramientas integradas al flujo de desarrollo.[^1]
**Inferences (recomendado):**

- Configura SAST con **reglas alineadas a tu dominio CRM** (authz, multi-tenant isolation, validación de input en APIs, SSRF en integraciones, logging de PII).
- Controla “ruido”: baseline/triage inicial, y luego “no new critical/high” como gate.
- Define **owner** por área (plataforma, backend, integraciones, data) para que los hallazgos no queden “huérfanos”.


### 3) Secret scanning con prevención (shift-left real)

**Fecha:** 2026-02-17
**Facts:** Secret scanning detecta secretos en repositorios, y el enforcement puede bloquear pushes con secretos (con alertas al bypass).[^3]
**Facts:** Incluir secretos en código es un error común y se vincula con CWE-540.[^3]
**Inferences (recomendado):**

- Aplica scanning en: PR (diff), main (full), y repos históricos (one-time).
- Define runbook: rotación, revocación, invalidación de sesiones, y búsqueda de uso del secreto.
- Métrica clave: “tiempo a revocar” más que “tiempo a cerrar ticket”.


### 4) Dependency scanning + SBOM como contrato B2B

**Fecha:** 2026-02-17
**Facts:** NTIA define mínimos de SBOM y requiere formatos interoperables como SPDX y CycloneDX para intercambio entre organizaciones.[^2]
**Inferences (recomendado):**

- Genera SBOM **por build** (no “por release manual”), y guárdalo como artefacto inmutable.
- Gatea por: vulnerabilidades críticas/altas en dependencias y por componentes no permitidos (bloqueados).
- Mantén un “allowlist/denylist” (proveedores, paquetes, versiones) por criticidad del módulo CRM (core vs. plugins/integraciones).


### 5) Licencias: política simple, enforcement fuerte

**Fecha:** 2026-02-17
**Facts:** SPDX License List permite identificar licencias con short identifiers estandarizados y URLs canónicas para referenciarlas.[^5]
**Facts:** Usar identificadores SPDX en archivos facilita cumplimiento y mejora precisión de herramientas de scanning.[^4]
**Inferences (recomendado):**

- Política de licencias por “zonas”: **permitidas**, **restringidas (requiere legal)**, **prohibidas**.
- Gate de PR/main: si aparece licencia prohibida o “unknown”, bloquea hasta clarificar (o reemplazar componente).
- En CRM enterprise, trata “unknown license” como **riesgo alto** (no por seguridad técnica, sino por riesgo contractual).


### 6) Políticas de PR (control de cambio y seguridad)

**Fecha:** 2026-02-17
**Facts:** OWASP recomienda integrar revisiones de seguridad en Pull Requests y automatización en CI como parte del proceso de revisión diff-based.[^6]
**Inferences (recomendado):**

- Requiere: 1–2 aprobaciones, CODEOWNERS para módulos críticos, y “checks must pass”.
- “PR description template” obligatorio: impacto, riesgos, migraciones, rollout/rollback, evidencia CI.
- Prohíbe merge directo a ramas protegidas; excepciones solo con break-glass + ticket.

***

## Examples (aplicado a CRM enterprise)

### Ejemplo A — Pipeline genérico (PR gate)

```yaml
pipeline: pr_gate
on: pull_request

stages:
  - checkout
  - build_fast
  - sast_diff
  - secrets_diff
  - deps_policy_check
  - unit_tests
  - report_and_status

rules:
  - fail_if: secrets_found == true
  - fail_if: sast.new_critical > 0
  - fail_if: deps.license in BLOCKED || deps.vuln_critical > 0
artifacts:
  - sast_report.sarif
  - secrets_report.json
  - deps_report.json
  - ci_run_metadata.json
```

**Facts:** Secret scanning puede configurarse para detectar y prevenir intentos de introducir secretos.[^3]
**Inferences:** En CRM, el PR gate debe ser rápido para no frenar a ventas/operaciones con ciclos largos; lo pesado pasa a main/release.

### Ejemplo B — Pipeline genérico (main build + SBOM + licencias)

```yaml
pipeline: main_build
on: push_to_main

stages:
  - build
  - sast_full
  - dependency_scan_full
  - generate_sbom
  - license_scan
  - package_artifacts
  - publish_artifacts

artifacts:
  - application_build_artifact.*
  - sbom.cyclonedx.json   # o sbom.spdx.json
  - dependency_vuln_report.json
  - license_report.json
  - sast_report.sarif
```

**Facts:** NTIA define elementos mínimos de SBOM y menciona SPDX/CycloneDX como formatos interoperables.[^2]
**Facts:** SPDX estandariza identificadores de licencia (License List) para referenciar licencias sin ambigüedad.[^5]

### Ejemplo C — Pipeline genérico (release/deploy gate + evidencia)

```yaml
pipeline: release_deploy
on: tag_release

stages:
  - verify_artifacts_integrity
  - deploy_staging
  - smoke_tests
  - security_gate_final
  - deploy_production

security_gate_final:
  rules:
    - fail_if: open_critical_findings > 0
    - fail_if: sbom_missing == true
    - require: change_ticket_id
    - require: approvals.security == true (if exception_used)
attachments_to_release:
  - sbom.*
  - all_security_reports_bundle.zip
  - exception_approval_record.pdf
```

**Facts:** “Provenance” (SLSA) busca describir quién/qué/cómo produjo un artefacto, para poder verificar expectativas del build.[^7]
**Inferences:** Si tu CRM vende a cuentas enterprise, adjuntar SBOM + reportes + excepciones firmadas reduce fricción comercial en cuestionarios de seguridad.

### Matriz operativa: “hallazgo → impacto → quick win → structural fix → validación”

| Hallazgo | Impacto (CRM enterprise) | Quick win (1–3 días) | Structural fix (1–6 semanas) | Validación (evidencia CI) |
| :-- | :-- | :-- | :-- | :-- |
| SAST: bypass de autorización en endpoint | Acceso indebido a registros (multi-tenant), incidente + breach | Hotfix con check de permisos + tests | Modelo central de autorización (policy), tests de regresión por rol/tenant | SAST limpio + tests + PR con reviewers; reporte SARIF adjunto |
| Secret: token/API key en repo | Compromiso de integraciones (correo, pagos, WhatsApp, etc.) | Revocar/rotar secreto, purge del historial si aplica | Secret manager + short-lived tokens + “push protection” | Reporte secret scan (diff+full) y evidencia de rotación (ticket) [^3] |
| Dependencia con CVE crítica | RCE/DoS en módulos core o exposición de datos | Bump versión / patch | Estrategia de actualización continua, allowlist/denylist, SBOM por build | Dependency report + SBOM generado y almacenado [^2] |
| Licencia “unknown” o prohibida | Riesgo contractual, bloqueo en procurement | Reemplazar librería o aclarar licencia | Política y tooling con SPDX IDs en headers | License report + evidencia SPDX IDs [^4][^5] |
| SBOM ausente en release | No puedes responder rápido a incidentes supply chain | Generar SBOM en main/release | Automatizar SBOM por build, retención y trazabilidad | sbom.* como artefacto requerido [^2] |
| PR sin revisiones / sin checks | Cambios inseguros entran “por velocidad” | Activar branch protection + required checks | CODEOWNERS, plantillas PR, gobierno de excepciones | Historial de checks + política PR cumplida [^6] |


***

## Metrics / success signals

**Facts:** Secret scanning reconoce falsos positivos/negativos; por eso conviene medir resultados operativos (alertas, prevención, tiempos) y no solo “cantidad de hallazgos”.[^3]
**Inferences (señales útiles en CRM enterprise):**

- **Change failure rate por seguridad:** % releases con rollback por issue de seguridad.
- **MTTR por severidad (SAST/SCA/Secrets):** tiempo desde detección CI hasta fix/mitigación.
- **Leak prevention rate:** % de secretos bloqueados antes de merge (vs detectados post-merge).
- **Dependency freshness:** edad promedio de dependencias críticas (o “time since last update”).
- **Auditability score:** % releases con bundle completo de evidencias (SBOM + reports + approvals).

***

## Operational checklist

**Facts:** NTIA establece SBOM mínimo y formatos interoperables (SPDX/CycloneDX) para intercambio.[^2]
**Facts:** OWASP recomienda integrar PR reviews y automatización CI para revisiones de seguridad.[^6]
**Checklist (operable, para un CRM enterprise):**

- Definir **gates** por etapa: PR (rápido), main (completo), release (estricto) y documentar umbrales.
- Habilitar SAST: baseline inicial + regla “no new critical/high” en PR; full scan en main.
- Activar secret scanning + enforcement (bloqueo) y runbook de rotación/revocación.[^3]
- Implementar dependency scanning y generar SBOM por build en SPDX o CycloneDX; almacenar inmutable.[^2]
- Definir política de licencias (allow/restricted/block) basada en identificadores SPDX; bloquear “unknown”.[^4][^5]
- PR policy: approvals mínimas, CODEOWNERS, required checks, plantilla PR con evidencia CI.[^6]
- Evidencias CI obligatorias (artefactos): SARIF SAST, report secrets, report dependencias, SBOM, reporte licencias, metadata run.
- Ensamblar “Release Security Bundle”: zip con artefactos + link a ejecución CI + registro de excepciones.

**Cómo anexar evidencias al informe final (práctico):**

- **Inferences:** En el informe final (PDF/Confluence/cliente), adjunta: (1) links inmutables a artefactos CI, (2) hashes/IDs de ejecución, (3) SBOM del release, (4) listado de excepciones con aprobadores y expiración; esto acelera due diligence y auditorías.

***

## Anti-patterns

**Facts:** Secret scanning no es perfecto (falsos positivos/negativos), así que usarlo como único control es insuficiente.[^3]
**Inferences (lo típico que rompe SDLC en CRM B2B):**

- “Gate simbólico”: siempre pasa, nadie lo respeta, y se normaliza el bypass.
- “Triage infinito”: miles de findings sin ownership ni SLAs; se vuelve ruido y se ignora.
- SBOM “a mano” por release: tarde, incompleto, y no repetible (no sirve para incident response).
- Licencias sin política: compras/procurement te bloquea el deal cuando ya está vendido.
- Excepciones sin caducidad: el riesgo se vuelve permanente y nadie lo retira.

***

## Diagnostic questions

**Facts:** SSDF incluye la idea de definir checks/gates y priorizar remediación por riesgo como parte del proceso.[^1]
**Preguntas (para diagnosticar madurez en un CRM enterprise):**

- ¿Qué exactamente bloquea un PR hoy (y qué porcentajes de PRs son bloqueados por seguridad)?
- ¿Cuánto tardas en **revocar** un secreto filtrado desde que CI lo detecta?[^3]
- ¿Puedes generar el SBOM del release N-2 en < 10 minutos y entregarlo a un cliente?[^2]
- ¿Qué licencias están prohibidas y quién aprueba excepciones? ¿Se bloquea “unknown”?[^5]
- ¿Qué evidencia CI guardas y por cuánto tiempo (retención) para auditoría cliente?
- ¿Existe break-glass? Si existe: ¿queda registro, aprobador, motivo y expiración?

***

## Sources (y entradas para SOURCES.md)

**Fuentes usadas:**

- NIST SSDF (referencias de prácticas y criterios de checks/gates vía guía resumida): Secure-by-Design Handbook — SSDF overview.[^1]
- NIST CSRC — SSDF Version 1.1 (SP 800-218) landing.[^8]
- NTIA — *The Minimum Elements for a Software Bill of Materials (SBOM)* (PDF).[^2]
- SPDX — SPDX License List (definición y propósito de identificadores).[^5]
- Linux Foundation — Open Source License Best Practices (uso de SPDX IDs).[^4]
- OpenSSF Best Practices WG — Secret Scanning (detección, prevención, CWE-540).[^3]
- OWASP Cheat Sheet Series — Secure Code Review (PR + CI como integración de revisión).[^6]
- Chainguard Academy — Introducción a SLSA / provenance.[^7]

**Entradas a añadir en `SOURCES.md` (sin duplicados):**

- `NIST_SP_800_218_SSDF_2022` — https://csrc.nist.gov/pubs/sp/800/218/final (NIST Secure Software Development Framework v1.1, publicado 2022-02-02).[^8]
- `NTIA_SBOM_Minimum_Elements_2021` — https://www.ntia.gov/files/ntia/publications/sbom_minimum_elements_report.pdf (NTIA SBOM minimum elements, 2021-07-11).[^2]
- `SPDX_License_List` — https://spdx.org/licenses/ (SPDX License List, identificadores estandarizados).[^5]
- `LF_SPDX_License_Best_Practices` — https://www.linuxfoundation.org/licensebestpractices (recomendación de SPDX IDs en headers).[^4]
- `OpenSSF_Secret_Scanning` — https://best.openssf.org/SCM-BestPractices/github/repository/secret_scanning.html (secret scanning + push protection, CWE-540).[^3]
- `OWASP_Secure_Code_Review_Cheat_Sheet` — https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html (PR/CI como parte del proceso de revisión).[^6]
- `Chainguard_SLSA_Provenance_Intro_2025` — https://edu.chainguard.dev/compliance/slsa/what-is-slsa/ (provenance y verificación de builds).[^7]

***

## Key takeaways for PM practice

- Define gates por etapa (PR/main/release) con umbrales claros; lo que no bloquea, no cambia conducta.
- Vende “evidencia” (artefactos CI + SBOM + políticas) como parte del producto enterprise, no como tarea interna.
- Prioriza secretos y dependencias como riesgos comerciales: integraciones y contratos se caen más rápido que el código.
- Establece SLAs realistas por severidad y un proceso de excepciones con caducidad (break-glass auditable).
- Usa la matriz hallazgo→impacto→quick win→structural fix→validación para transformar seguridad en roadmap y ejecución.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31][^9]</span>

<div align="center">⁂</div>

[^1]: https://www.securebydesignhandbook.com/docs/standards/us/nist-sp-800-218-ssdf-overview

[^2]: https://www.ntia.gov/files/ntia/publications/sbom_minimum_elements_report.pdf

[^3]: https://best.openssf.org/SCM-BestPractices/github/repository/secret_scanning.html

[^4]: https://www.linuxfoundation.org/licensebestpractices

[^5]: https://spdx.org/licenses/archive/archived_ll_v1.17/

[^6]: https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html

[^7]: https://edu.chainguard.dev/compliance/slsa/what-is-slsa/

[^8]: https://csrc.nist.gov/pubs/sp/800/218/final

[^9]: pasted-text.txt

[^10]: https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-218.pdf

[^11]: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218-draft.pdf

[^12]: https://www.aikido.dev/learn/compliance/compliance-frameworks/nist-ssdf

[^13]: https://jfrog.com/learn/grc/ssdf/

[^14]: https://www.kiuwan.com/blog/sbom-standards/

[^15]: https://fossa.com/blog/understanding-using-spdx-license-identifiers-license-expressions/

[^16]: https://edu.chainguard.dev/software-security/secure-software-development/ssdf/

[^17]: https://www.ntia.gov/files/ntia/publications/ntia_sbom_formats_energy_brief_2021.pdf

[^18]: https://www.dwt.com/-/media/files/blogs/privacy-and-security-blog/2026/secure-software-development-framework.pdf?rev=d7b8c596fc69474897e5ff287ce14320\&hash=B47C0AFE54066F6A6DD3E0D7BEF457EB

[^19]: https://cycode.com/blog/sboms-minimum-requirements/

[^20]: https://best.openssf.org/Concise-Guide-for-Developing-More-Secure-Software.html

[^21]: https://scorecard.dev

[^22]: https://github.com/ossf/scorecard

[^23]: https://openssf.org/blog/2023/11/09/how-to-use-open-source-to-help-comply-with-scm-best-practices-a-tutorial-on-combining-openssf-scorecard-and-legitify/

[^24]: https://research.samsung.com/blog/Road-to-Get-Certified-as-gold-Badge-From-OpenSSF-Best-Practices

[^25]: https://www.endorlabs.com/learn/using-artifact-signing-to-establish-provenance-for-slsa

[^26]: https://www.pullchecklist.com/posts/code-review-guide-owasp

[^27]: https://best.openssf.org/SCM-BestPractices/

[^28]: https://github.blog/enterprise-software/devsecops/enhance-build-security-and-reach-slsa-level-3-with-github-artifact-attestations/

[^29]: https://owasp.org/www-project-code-review-guide/

[^30]: https://nocomplexity.com/documents/securityarchitecture/prevention/openSSF-scorecard.html

[^31]: https://www.legitsecurity.com/blog/slsa-provenance-blog-series-part-1-what-is-software-attestation

