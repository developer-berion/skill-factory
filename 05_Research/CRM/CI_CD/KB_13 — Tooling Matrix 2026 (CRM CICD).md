<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_13 — Tooling Matrix 2026 (CRM CI/CD)

## Executive summary (Feb 2026)

**Facts:** GitHub y GitLab están entre las herramientas más usadas para colaboración/gestión de código a nivel industria, lo que vuelve razonable construir CI “pegado” a esas plataformas cuando tu código vive ahí.[^1]
**Inferences:** En CRM enterprise, esa decisión reduce fricción operativa (SSO, permisos, auditoría) y acelera onboarding de equipos, a costa de más “lock-in” de plataforma.

**Facts:** En el ecosistema cloud-native, Argo y Flux se usan como base de GitOps para CD, y Prometheus/OpenTelemetry/Jaeger/Grafana aparecen como pilares de observabilidad.[^2]
**Inferences:** Si tu CRM corre en Kubernetes (o va hacia ahí), GitOps + observabilidad estándar te da control y repetibilidad, que es lo que más impacta incidentes y velocidad de releases.

**Facts:** SLSA define niveles (L1→L3) alrededor de “provenance” (qué se construyó, cómo y con qué inputs) y endurecimiento progresivo contra manipulación.[^3]
**Inferences:** Para un CRM enterprise, el salto más costo/beneficio suele ser: SBOM + firma + provenance verificable “en CI” antes de perseguir niveles altos sin base.

**Facts:** Syft y Cosign soportan SBOM en CycloneDX y SPDX, y es común firmar/adjuntar atestaciones para consumo posterior.[^4]
**Inferences:** Esto te habilita “policy gates” reales (admisión/registro/deploy) sin depender de confianza implícita en el registry o en el pipeline.

**Facts:** GitLab documenta feature flags como mecanismo para desplegar y activar gradualmente, con ejemplo de uso de Unleash proxy.[^5]
**Inferences:** En CRM enterprise, feature flags no es “nice to have”: es el seguro para vender/activar módulos por cliente sin re-deploy y con rollback inmediato.

***

## Definitions and why it matters (Feb 2026)

**Facts:** GitOps (p.ej., Argo/Flux) se usa para CD basado en Git como fuente de verdad del estado deseado.[^2]
**Inferences:** En CRM enterprise, GitOps baja el riesgo de “config drift” entre entornos (dev/uat/prod) y hace auditables los cambios (quién, qué, cuándo).

**Facts:** Observabilidad (Prometheus, OpenTelemetry, Jaeger, Grafana) permite monitoreo/tracing/telemetría para detectar y depurar fallas en sistemas distribuidos.[^2]
**Inferences:** Si el CRM tiene integraciones (pagos, ERP, mensajería), la observabilidad es lo que convierte incidentes “imposibles” en tickets accionables.

**Facts:** SLSA define “provenance” como metadata del build (entidad, proceso, inputs), con niveles que elevan resistencia a manipulación.[^3]
**Inferences:** Para enterprise, provenance + SBOM + firma es el idioma común entre seguridad, auditoría y delivery (sin frenar releases).

***

## Principles and best practices (Feb 2026)

**Facts:** CNCF lista Argo/Flux para GitOps-driven CI/CD y Prometheus/OpenTelemetry/Jaeger/Grafana para observabilidad, como herramientas típicas para mejorar el loop DevOps.[^2]
**Inferences:** Define una “columna vertebral” mínima (CI→GitOps→Observabilidad→Supply chain) y prohíbe soluciones paralelas por equipo; la diversidad descontrolada se paga en on-call y auditoría.

**Facts:** SLSA enfatiza que la provenance ayuda a depurar, reconstruir y verificar releases, y que niveles superiores aumentan protección contra tampering.[^3]
**Inferences:** Implementa “evidencia primero”: generar SBOM + provenance en cada build, firmar, y recién después automatizar enforcement en CD/admisión.

**Facts:** Syft/Cosign soportan formatos estándar (CycloneDX/SPDX) y flujo de atestación/firma alrededor de artefactos.[^4]
**Inferences:** Estandariza 1–2 formatos (CycloneDX para tooling cloud-native; SPDX si tu foco es licencias/compliance) y evita mezclar sin necesidad.

**Facts:** GitLab describe feature flags como mecanismo para activar/desactivar features por cohortes y reducir riesgo en producción.[^5]
**Inferences:** Trata feature flags como “producto interno”: ownership, convenciones de naming, expiración (flag debt) y auditoría de cambios.

***

## Tooling matrix (Feb 2026)

> Regla de este documento: solo incluyo herramientas con soporte explícito en las fuentes citadas; donde falte evidencia aquí, lo marco como “No cubierto”.


| Capa | Herramientas (evidencia) | Cuándo usar | Pros | Contras | Señales de madurez | Costos operativos | Riesgos y controles |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| CI runners | GitHub (plataforma) y GitLab (plataforma) como base común de colaboración. [^1] | Si tu repo/flujo vive en GitHub/GitLab y quieres CI con permisos/auditoría integrados. | Menos fricción (SSO, permisos, PRs) (Inference). | Dependencia de plataforma (Inference). | Builds reproducibles, caché controlada, secrets rotados (Inference). | Admin de runners, cuotas, troubleshooting (Inference). | Compromiso de runner; controlar con hardening, OIDC, mínimos privilegios (Inference). |
| CD / GitOps | Argo, Flux. [^2] | Deploy a Kubernetes con trazabilidad/auditoría y rollback vía Git. | Git como fuente de verdad, reconciliación automática (Inference). | Requiere disciplina de repos/entornos (Inference). | PR-based deploys, separación apps/infra repos, drift=0 (Inference). | Operar controllers, upgrades, RBAC, incidentes de sync (Inference). | “Auto-sync” mal gobernado; controles: approvals, branch protection, entornos segregados (Inference). |
| Artifact registry | Harbor (en CNCF Landscape). [^6] | Registry propio cuando necesitas control (tenancy, políticas, aire-gapped) (Inference). | Control de retención y acceso (Inference). | Operación/almacenamiento y upgrades (Inference). | Retención por política, limpieza, alta disponibilidad (Inference). | Storage + backup + upgrades + vulnerab scanning si aplica (Inference). | Riesgo de borrado/compromiso; controles: immutability, backups, MFA/RBAC (Inference). |
| Signing / SBOM | Syft + Cosign; formatos CycloneDX/SPDX. [^4] | Si necesitas SBOM estándar y firmada/atestada para gates y auditoría. | Estándares soportados y automatizables en CI (Inference). | Curva de integración, manejo de llaves/identidad (Inference). | SBOM por build, firma/attestation por artefacto, verificación en deploy (Inference). | Mantener pipelines, rotación de identidad/keys (Inference). | “Confianza ciega” sin verificación; control: verify en CD/admisión (Inference). |
| Supply-chain maturity | Niveles SLSA y requisitos de provenance. [^3] | Para roadmap de seguridad del delivery (qué implementar primero). | Marco común para priorizar (Inference). | Puede volverse “checkbox” sin impacto (Inference). | Pasar de L1 (provenance existe) a L2 (firmada/atada a infraestructura dedicada) (Inference). | Ajustes de plataforma CI, credenciales, controles (Inference). | Falsa sensación de seguridad; control: auditoría de verificación real y excepciones (Inference). |
| Secret management | **No cubierto con evidencia suficiente en fuentes de este turno.** | — | — | — | — | — | — |
| IaC / Infra automation | Crossplane; estandarización con Kubernetes/HelM mencionada como práctica. [^2] | Multi-cloud o “infra como APIs” desde Kubernetes (Crossplane). [^2] | Unifica aprovisionamiento con patrones K8s (Inference). | Complejidad de CRDs/providers (Inference). | Infra declarativa, módulos/providers gobernados, drift controlado (Inference). | Operar providers, upgrades, RBAC, troubleshooting (Inference). | Escalada de permisos; control: least privilege, entornos, auditoría (Inference). |
| Policy-as-code | OPA, Kyverno (mencionados como ejemplo de detección de violaciones de policy). [^7] | Si necesitas gates repetibles en CI y/o post-deploy. | Políticas versionadas y automatizables (Inference). | Riesgo de frenar delivery si reglas no están bien diseñadas (Inference). | “Policy tests” en CI, excepciones con caducidad, métricas de violaciones (Inference). | Mantener reglas, debugging de denegaciones (Inference). | Bloqueos por falsos positivos; control: modo “audit” primero, rollout gradual (Inference). |
| Observabilidad | Prometheus, OpenTelemetry, Jaeger, Grafana. [^2] | Sistemas distribuidos, microservicios, integraciones, SLOs. | Stack estándar y composable (Inference). | Ruido/alto costo si no hay gobernanza (Inference). | SLOs definidos, tracing end-to-end, dashboards accionables (Inference). | Storage/retención, cardinalidad, on-call, instrumentación (Inference). | Alert fatigue; control: SLO-based alerting y presupuestos de error (Inference). |
| Feature flags | Feature flags en GitLab; ejemplo con Unleash proxy. [^5] | Releases con activación gradual, rollback instantáneo, módulos por cliente. | Reduce riesgo de deploy; habilita “release ≠ launch” (Inference). | Flag debt y complejidad de testing (Inference). | Catálogo de flags, expiración, segmentación, auditoría (Inference). | Operar servicio de flags/proxy, SDKs, gobierno (Inference). | Activaciones accidentales; control: roles, approvals, ambientes, límites (Inference). |


***

## Examples (aplicado a CRM enterprise) (Feb 2026)

**Facts:** GitOps con Argo/Flux se usa para CD y Prometheus/OpenTelemetry/Jaeger/Grafana para observabilidad del sistema en producción.[^2]
**Inferences (escenario):** Tu CRM tiene un módulo “Automations v2” para un cliente enterprise, pero quieres deployar a prod sin exponerlo a todos: despliegas el código normalmente, y controlas activación con feature flags por tenant/rol; si hay incidencia, apagas el flag sin rollback de infraestructura.

**Facts:** GitLab describe feature flags para togglear features y desplegar en lotes más pequeños.[^5]
**Inferences (flujo operativo):**

- CI: build + tests + genera SBOM + firma/attestation (Syft/Cosign), publica artefacto (p.ej. en Harbor).[^6][^4]
- CD (GitOps): PR modifica manifiestos Helm/K8s; Argo/Flux reconcilian, y observabilidad valida salud post-deploy (SLO/errores/traces).[^2]

***

## Metrics / success signals (Feb 2026)

**Facts:** El artículo de CNCF menciona métricas como MTTR, lead time y error rate como anclas comunes para equipos.[^2]
**Inferences:**

- DORA-ish: lead time (commit→prod), frecuencia de deploy, MTTR, change failure rate (por servicio y por equipo).
- Supply chain: % builds con SBOM + firma verificada en CD, % deploys bloqueados por policy con “excepción” documentada.
- Feature flags: % flags con fecha de expiración, tiempo promedio de “flag cleanup”, ratio de rollback vía flag vs rollback de deploy.

***

## Operational checklist (Feb 2026)

**Facts:** SLSA describe provenance y su valor para verificación y análisis del release.[^3]
**Inferences (checklist mínimo, orden recomendado):**

- Definir “source of truth”: repos de app vs repos de entorno (dev/uat/prod) para GitOps.
- Implementar CD con Argo o Flux; empezar en 1 servicio y 1 entorno.[^2]
- Instrumentar observabilidad base: métricas (Prometheus), trazas (Jaeger), telemetría/instrumentación (OpenTelemetry), dashboards (Grafana).[^2]
- Supply chain: generar SBOM con Syft y firmar/adjuntar/verificar con Cosign; estandarizar CycloneDX/SPDX.[^4]
- Feature flags: establecer owner, naming, expiración, y proceso de aprobación para cambios críticos.[^5]
- Policy-as-code: iniciar en modo “audit” (sin bloquear), luego pasar a “enforce” en los gates que realmente reducen riesgo.[^7]

***

## Anti-patterns (Feb 2026)

**Facts:** Sin monitoreo adecuado, los equipos reaccionan tarde y los problemas se detectan después del impacto; la observabilidad propuesta (Prometheus/OpenTelemetry/Jaeger/Grafana) apunta a cubrir ese vacío.[^2]
**Inferences:**

- “GitOps sin gobernanza”: auto-sync en prod sin approvals ni separación de entornos.
- “SBOM teatro”: generar SBOM pero nunca verificar firmas/attestations en CD.
- “Feature flags eternas”: flags sin expiración y sin owner → deuda y bugs por ramas muertas.
- “Observabilidad por vanity”: dashboards bonitos sin SLOs ni alertas accionables (alert fatigue).

***

## Diagnostic questions (Feb 2026)

**Facts:** GitLab plantea feature flags para togglear features y desplegar gradualmente.[^5]
**Inferences (preguntas para aterrizar tu matriz):**

- ¿Tu rollback típico hoy es “revert + redeploy”, o puedes apagar comportamiento con flags en minutos?
- ¿Puedes demostrar (con evidencia) qué se desplegó, cómo se construyó y con qué dependencias (provenance/SBOM)?[^3]
- ¿Tu CD es “push manual” o reconciliación declarativa basada en Git (Argo/Flux)?[^2]
- ¿Tus políticas de seguridad se rompen en runtime o se detectan antes (CI/CD) con policy-as-code?[^7]
- ¿La observabilidad permite explicar un incidente con trazas y métricas, o solo con logs sueltos?[^2]

***

## Sources (Feb 2026)

**Fuentes usadas (para incluir en SOURCES.md, sin duplicados):**

- Stack Overflow — “Stack Overflow’s 2025 Developer Survey…” https://stackoverflow.co/company/press/archive/stack-overflow-2025-developer-survey/ (accessed 2026-02-18).[^1]
- CNCF Blog — “The tools for overcoming the top 10 DevOps challenges” https://www.cncf.io/blog/2025/10/14/the-tools-for-overcoming-the-top-10-devops-challenges/ (accessed 2026-02-18).[^2]
- SLSA.dev — “Security levels (spec v1.0)” https://slsa.dev/spec/v1.0/levels (accessed 2026-02-18).[^3]
- Anchore Blog — “Creating SBOM Attestations Using Syft and Sigstore” https://anchore.com/sbom/creating-sbom-attestations-using-syft-and-sigstore/ (accessed 2026-02-18).[^4]
- GitLab Docs — “Feature flags” https://docs.gitlab.com/operations/feature_flags/ (accessed 2026-02-18).[^5]
- CNCF Landscape Guide (Harbor item) https://landscape.cncf.io/guide?item=provisioning--container-registry--harbor (accessed 2026-02-18).[^6]
- CNCF TOC issue (adoption framework example mentioning OPA/Kyverno) https://github.com/cncf/toc/issues/1917 (accessed 2026-02-18).[^7]

***

## Key takeaways for PM practice

- Diseña la matriz como “backbone” (CI→GitOps→Observabilidad→Supply chain→Flags) antes de optimizar herramientas por equipo.
- En enterprise CRM, feature flags + GitOps te separan “deploy” de “launch” y bajan riesgo comercial y operativo.
- Mide madurez por evidencia (SBOM/provenance verificada, drift=0, SLOs), no por cantidad de herramientas.
- Mantén una vía segura (audit mode, rollout gradual) y una vía agresiva (enforce + auto-sync) con criterios explícitos para subir de nivel.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://stackoverflow.co/company/press/archive/stack-overflow-2025-developer-survey/

[^2]: pasted-text.txt

[^3]: https://slsa.dev/spec/v1.0/levels

[^4]: https://anchore.com/sbom/creating-sbom-attestations-using-syft-and-sigstore/

[^5]: https://docs.gitlab.com/operations/feature_flags/

[^6]: https://landscape.cncf.io/guide?item=provisioning--container-registry--harbor

[^7]: https://github.com/cncf/toc/issues/1917

[^8]: https://www.cncf.io

[^9]: https://landscape.cncf.io/guide

[^10]: https://www.linkedin.com/pulse/cncf-landscape-deep-dive-navigating-cloud-native-swapnil-kulkarni-oclff

[^11]: https://launchdarkly.com/blog/managing-feature-flags-with-terraform/

[^12]: https://www.devopscommunity.in/kubernetes-report-2026

[^13]: https://edu.chainguard.dev/open-source/sigstore/cosign/how-to-sign-an-sbom-with-cosign/

[^14]: https://jeevisoft.com/blogs/2025/06/what-is-cncf-and-why-it-matters-in-modern-devops-pipelines/

[^15]: https://spdx.dev/a-step-by-step-guide-to-signing-an-spdx-sbom-with-sigstores-cosign/

[^16]: https://terrateam.io/blog/feature-flag-management-with-terrateam-and-launchdarkly

[^17]: https://www.cncf.io/blog/2025/10/14/the-tools-for-overcoming-the-top-10-devops-challenges/

[^18]: https://ayedo.de/en/posts/supply-chain-security-mit-sbom-und-sigstore/

[^19]: https://survey.stackoverflow.co/2025/

[^20]: https://survey.stackoverflow.co/2025/technology

[^21]: https://meta.stackoverflow.com/questions/433720/2025-developer-survey-call-for-feedback

[^22]: https://dev.to/davidshq/thoughts-on-stackoverflow-2025-developer-survey-part-1-3d5o

[^23]: https://www.techtarget.com/searchitoperations/news/252528152/GitOps-hits-stride-as-CNCF-graduates-Flux-CD-and-Argo-CD

[^24]: https://jfrog.com/learn/grc/slsa-framework/

[^25]: https://stackoverflow.blog/2025/12/29/developers-remain-willing-but-reluctant-to-use-ai-the-2025-developer-survey-results-are-here/

[^26]: https://rawkode.academy/read/fluxcd-the-inevitable-choice

[^27]: https://www.reddit.com/r/programming/comments/1mciiyg/2025_stack_overflow_developer_survey/

[^28]: https://www.cncf.io/news/2022/12/13/the-new-stack-argo-cd-and-flux-are-cncf-grads-but-what-now/

[^29]: https://slsa.dev/spec/v0.1/levels

[^30]: https://stackoverflow.com/beta/discussions/77092002/is-jenkins-still-the-winner-of-ci-cd-space

[^31]: https://codefresh.io/learn/argo-cd/argo-cd-vs-flux-6-key-differences-and-how-to-choose/

