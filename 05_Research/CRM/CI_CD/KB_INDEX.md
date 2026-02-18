\# KB\_INDEX — CI/CD \& Platform Engineering para CRM Enterprise (2026)



\## Propósito

Este Knowledge Base (KB) reúne prácticas, patrones operables y fuentes para diseñar, operar y mejorar CI/CD (integración y despliegue continuos) específicamente en un \*\*CRM enterprise\*\* (multi-tenant, integraciones B2B, compliance, auditoría, disponibilidad).



\## Cómo usar este KB (Golden Path)

1\) Empieza por \*\*arquitectura de delivery + estrategia de releases\*\* (KB\_01, KB\_02, KB\_18).

2\) Define \*\*calidad y pruebas\*\* (KB\_03) y \*\*migraciones sin downtime\*\* (KB\_08).

3\) Asegura \*\*identidades/secretos\*\* (KB\_05), \*\*supply chain\*\* (KB\_04) y \*\*vulnerability mgmt\*\* (KB\_16).

4\) Estándar de operación: \*\*GitOps/IaC/Policy\*\* (KB\_06), \*\*observabilidad\*\* (KB\_07), \*\*incidentes/on-call\*\* (KB\_14), \*\*DR\*\* (KB\_15).

5\) Escala y eficiencia: \*\*DX/platform engineering\*\* (KB\_11), \*\*runners hardening\*\* (KB\_17), \*\*FinOps\*\* (KB\_19).

6\) Mantén actualización controlada: \*\*TechRadar/adopción\*\* (KB\_12), \*\*tooling matrix\*\* (KB\_13), \*\*certs/education\*\* (KB\_20).



---



\## Índice de archivos (orden recomendado)



\### Fundaciones de Delivery (CRM)

\- \*\*KB\_01 — Delivery Architecture for CRM.md\*\*

&nbsp; - Qué cubre: arquitectura de delivery, DORA/SLO alignment, canary, multi-tenant risk.

&nbsp; - Úsalo cuando: definas “cómo se entrega” el CRM y cómo se gobierna el riesgo.

\- \*\*KB\_02 — TrunkBased\_Flags\_ProgressiveDelivery (2026).md\*\*

&nbsp; - Qué cubre: trunk-based, feature flags, progressive delivery, rollback discipline.

&nbsp; - Úsalo cuando: quieras releases frecuentes sin romper integraciones ni tenants.

\- \*\*KB\_18 — MultiTenant\_ReleaseOrchestration\_TenantCanary\_DataResidency.md\*\*

&nbsp; - Qué cubre: tenant catalog/control plane, cohort rollouts, data residency por región, tiering SMB/Enterprise.

&nbsp; - Úsalo cuando: tu CRM es multi-tenant y necesitas “canary por tenant” + compliance regional.



\### Calidad, pruebas y compatibilidad

\- \*\*KB\_03 — CI\_TestStrategy\_ContractTesting.md\*\*

&nbsp; - Qué cubre: estrategia de pruebas en CI (unit/integration/e2e/contract), contract testing para integraciones.

\- \*\*KB\_08 — DataMigrations\_ExpandContract\_ZeroDowntime.md\*\*

&nbsp; - Qué cubre: expand/migrate/contract, zero downtime, backfills por cohortes, rollback-safe schema.



\### Seguridad, supply-chain y compliance (enterprise-grade)

\- \*\*KB\_04 — SupplyChainSecurity\_SLSA\_SBOM\_Signing.md\*\*

&nbsp; - Qué cubre: SLSA, SBOM (CycloneDX/SPDX), firma (Cosign), verificación en admisión.

\- \*\*KB\_05 — Secrets\_IAM\_OIDC\_KMS.md\*\*

&nbsp; - Qué cubre: OIDC en CI/CD, secretos efímeros, Vault/KMS, least privilege.

\- \*\*KB\_10 — Compliance, auditabilidad y mapeo CI\_CD.md\*\*

&nbsp; - Qué cubre: SOC2/ISO/GDPR mapeado a controles CI/CD; evidencia y auditoría.

\- \*\*KB\_16 — VulnManagement\_SBOM\_Policy.md\*\*

&nbsp; - Qué cubre: priorización KEV/EPSS, gates progresivos, enforcement gradual, métricas TTR/FP/overrides.



\### Infra, GitOps y gobierno por políticas

\- \*\*KB\_06 — IaC + GitOps + Policy-as-Code para CRM.md\*\*

&nbsp; - Qué cubre: Argo/Flux, drift detection, OPA/Conftest, promotion pipelines, SoD.

\- \*\*KB\_13 — Tooling Matrix 2026 (CRM CICD).md\*\*

&nbsp; - Qué cubre: matriz de herramientas por capa (CI, CD/GitOps, registries, observabilidad, supply-chain), pros/contras/riesgos.



\### Observabilidad y Operación (Run)

\- \*\*KB\_07 — Observabilidad para delivery y CRM (SLOs).md\*\*

&nbsp; - Qué cubre: SLOs/error budgets, correlación release→métrica, OTel, rollback por métricas.

\- \*\*KB\_14 — IncidentResponse\_OnCall\_ReleaseOps\_CRM.md\*\*

&nbsp; - Qué cubre: on-call, release ops, incident response, runbooks (pendiente normalizar fuentes si usa \[web:x]).

\- \*\*KB\_15 — DisasterRecovery\_BackupRestore\_RPO\_RTO.md\*\*

&nbsp; - Qué cubre: RPO/RTO por journey, restore drills, DR como pipeline con evidencia.



\### Platform Engineering, DX, runners y costos

\- \*\*KB\_11 — DX\_PlatformEngineering\_GoldenPaths.md\*\*

&nbsp; - Qué cubre: platform engineering, golden paths, templates, autoservicio seguro.

\- \*\*KB\_17 — CI Runners Hardening \& Ephemeral Builds.md\*\*

&nbsp; - Qué cubre: runners efímeros, OIDC, anti-exfil, cache poisoning, governance de runner groups.

\- \*\*KB\_19 — FinOps\_CICD\_CostControls\_EphemeralEnvs.md\*\*

&nbsp; - Qué cubre: control de costos de CI/CD y entornos efímeros, billing/limits, OpenCost.



\### Integraciones CRM y adopción/innovación “probada”

\- \*\*KB\_09 — Integraciones confiables para CRM (Salesforce,HubSpot,etc).md\*\*

&nbsp; - Qué cubre: patrones de integración, resiliencia, contratos, versionado.

\- \*\*KB\_12 — TechRadar\_ContinuousDiscovery\_AdoptionProces.md\*\*

&nbsp; - Qué cubre: proceso de adopción de prácticas/herramientas “innovadoras pero comprobadas”, con gates y criterios.

\- \*\*KB\_20 — Certs\_Education Signals 2024–2026.md\*\*

&nbsp; - Qué cubre: señales de credenciales (cloud DevOps, Kubernetes, IaC, SDLC security) y cómo usarlas como estándar interno.



---



\## TODO de higiene (para que quede 100% “audit-ready”)

\- Reemplazar referencias tipo `pasted-text.txt` por URLs reales en KBs donde aparezca.

\- Normalizar KB\_14 para que su sección `Sources` incluya URLs explícitas y entradas “SOURCES.md additions”.



