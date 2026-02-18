<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_06 — IaC + GitOps + Policy-as-Code para CRM enterprise (Terraform/Pulumi, Argo/Flux, OPA/Conftest)

## Executive summary (10–15 líneas)

Facts: IaC define infraestructura “como código” y reduce cambios manuales que generan drift (divergencia entre estado real y deseado).[^1]
Facts: Terraform (y su ecosistema) permite detectar drift comparando configuración vs estado real, y en HCP Terraform se pueden correr “refresh-only plans” periódicos para hallarlo automáticamente.[^1]
Facts: GitOps usa Git como “source of truth”; Argo CD es una herramienta GitOps/CD declarativa para Kubernetes que monitorea estado live vs estado deseado y marca `OutOfSync` cuando divergen.[^2]
Facts: Argo CD soporta sync automático o manual, RBAC/multi-tenancy y audit trail, útiles en entornos enterprise con controles.[^2]
Facts: Policy-as-code con OPA permite evaluar políticas en Kubernetes vía admission control durante create/update/delete, para permitir/denegar objetos.[^3]
Facts: Conftest permite testear configs estructuradas (Kubernetes, Terraform, etc.) usando Rego (OPA) antes de llegar a producción.[^4][^5]
Inferences: Para CRM enterprise (datos sensibles, integraciones, uptime), el combo IaC+GitOps+policies crea un “cinturón de seguridad”: cambios trazables, aprobables y reversibles por commit.
Inferences: Separación de duties (SoD) se implementa con ramas, CODEOWNERS, entornos protegidos y credenciales de deploy que no viven en laptops.
Inferences: Drift detection debe ser “continuo” (scheduled) y “event-driven” (alertas), porque el drift no avisa y suele venir de urgencias o accesos privilegiados.
Inferences: El mejor diseño es PR→checks→aprobación→promoción por ambientes (dev/stage/prod) con gates explícitos para seguridad y plataforma.

## Definitions and why it matters

Facts: “Drift” es cuando el estado real de infraestructura difiere del declarado en tu configuración; puede ocurrir por cambios manuales, updates del cloud o modificaciones no autorizadas, y afecta confiabilidad/seguridad.[^1]
Facts: Argo CD aplica el patrón GitOps usando repos Git como fuente de verdad y reconcilia continuamente live vs desired state; si el live se desvía se considera `OutOfSync`.[^2]
Facts: OPA como admission controller permite imponer reglas (labels obligatorias, imágenes desde registry corporativo, requests/limits, etc.) al crear/actualizar recursos.[^3]
Facts: Conftest testea configs estructuradas con políticas Rego para fallar o advertir antes del deploy.[^5][^4]
Inferences: En un CRM enterprise, esto importa porque los cambios “pequeños” (un SG abierto, un Secret mal rotado, un namespace sin quotas) terminan en incidentes, costos o auditorías dolorosas.
Inferences: Comercialmente (B2B), baja fricción operativa = más velocidad para entregar features/automatizaciones sin perder control (y menos “no puedo porque riesgo”).

## Principles and best practices (con citas por sección + fecha)

Fecha: 2026-02-18.

Facts: Mantén Git como fuente de verdad para despliegues; Argo CD está diseñado para automatizar despliegue desde Git y mostrar divergencias (drift) como `OutOfSync`.[^2]
Inferences: Regla operativa: “si no está en Git, no existe”; excepciones (hotfix) deben volver a Git con PR retroactivo.

Facts: Diseña sync con seguridad “a prueba de errores”; Argo CD permite opciones como `Prune=confirm` (confirmación manual antes de podar recursos) para evitar acciones destructivas.
Inferences: En CRM, usa `Prune=confirm` en namespaces/CRDs/recursos “tier-1” y deja prune automático en dev para velocidad.

Facts: Implementa drift detection programado; HCP Terraform permite health assessments que corren “refresh-only Terraform plans” periódicos para detectar drift por workspace.[^1]
Inferences: Define SLO interno: drift crítico detectado < 15 min (prod) y < 2 h (no prod); si no puedes, al menos diario.

Facts: “Shift-left” de políticas: Conftest valida Terraform/Kubernetes/etc. con Rego en CI para bloquear violaciones antes de merge.[^4][^5]
Inferences: Política práctica: todo PR que toque IaC/manifests pasa por Conftest; OPA en runtime es el “último gate”, no el primero.

Facts: Enforcement en runtime: OPA vía admission control evalúa requests del API server sobre objetos durante create/update/delete.[^3]
Inferences: Divide políticas en 3 severidades: block (seguridad/PII), warn (costos/estándares), inform (higiene).

Facts: Argo CD incluye RBAC/multi-tenancy y audit trails, útil para control y trazabilidad.[^2]
Inferences: SoD “real”: dev propone (PR), platform aprueba infraestructura/base, security aprueba políticas; nadie que aprueba puede ejecutar cambios fuera del pipeline.

### Qué incluye / qué no incluye / qué es sensible

Facts: Argo CD soporta sync manual/automático y hooks (PreSync/Sync/PostSync) para rollouts complejos.[^2]
Inferences (incluye): Flujo PR→aprobación→deploy con gates, drift detection, políticas en CI y en cluster.
Inferences (no incluye): Diseño de org/roles específico (depende de tu IAM, regulaciones y tamaño), ni arquitectura completa del CRM (microservicios vs monolito).
Inferences (sensible): Manejo de credenciales, accesos break-glass, y cambios manuales en prod (son la fuente \#1 de drift y hallazgos de auditoría).

## Examples (aplicado a CRM enterprise)

Facts: Argo CD reconcilia continuamente y expone estado `OutOfSync` cuando live ≠ desired, lo que encaja con un modelo de “promoción por commit” entre ambientes.[^2]
Inferences: Caso CRM: tienes `crm-core` (API), `crm-ui`, `crm-integrations` (colas/webhooks), y `crm-data` (jobs/ETL) en Kubernetes; infra (VPC/IAM/DB) con Terraform; policies con Rego.

### Ejemplo 1 — Repo y promoción por PR (safe)

Inferences: Estructura típica:

```text
repo/
  infra/terraform/            # VPC, IAM, RDS, etc.
  clusters/apps/              # manifests/helm/kustomize por ambiente
    dev/
    stage/
    prod/
  policy/                     # Rego para Conftest/OPA
```

Inferences: Flujo PR→aprobación→deploy:

1) Dev abre PR cambiando `clusters/apps/dev/crm-core/values.yaml`.
2) CI corre unit tests + `conftest test` sobre manifests y/o Terraform plan output. (Gate)[^5][^4]
3) CODEOWNERS exige aprobación de Platform + Security para rutas sensibles (`infra/` y `policy/`).
4) Merge a `main` actualiza desired state; Argo CD detecta el cambio y sincroniza (auto o manual según ambiente).[^2]
5) Para prod, promoción se hace con PR separado `stage → prod` (mismo artefacto/version), y Argo CD aplica al merge.

### Ejemplo 2 — Gate de “prune con confirmación” (prod)

Facts: Argo CD permite `Prune=confirm` para requerir confirmación manual antes de podar recursos.
Inferences: En CRM prod, activas prune confirm para evitar que un refactor de Helm borre un `PersistentVolumeClaim` o un `Namespace` crítico por error de chart.

### Ejemplo 3 — Drift detection IaC (Terraform) + decisión de remediación

Facts: HCP Terraform puede correr refresh-only plans periódicos para detectar drift automáticamente, y ante drift puedes optar por aplicar para restaurar desired state o actualizar config para reflejar el nuevo estado.[^1]
Inferences: Playbook CRM:

- Drift “peligroso” (SG abierto, IAM ampliado): aplicar para revertir a desired (y abrir incidente).
- Drift “válido” (hotfix aprobado por CAB): capturar en código y mergear (para cerrar el loop).


### Ejemplo 4 — Policy-as-code: CI (Conftest) + runtime (OPA)

Facts: Conftest prueba configs estructuradas con Rego (OPA).[^4][^5]
Facts: OPA en Kubernetes admission control puede exigir labels o restringir imágenes a registry corporativo.[^3]
Inferences: Políticas CRM típicas:

- Bloqueo: “No se permite `Service` tipo `LoadBalancer` en prod sin annotation de aprobación de costos.”
- Bloqueo: “Pods deben tener requests/limits y `runAsNonRoot`.”
- Advertencia: “Ingress sin WAF annotation” (si tu plataforma lo usa).


## Metrics / success signals

Facts: Argo CD ofrece métricas Prometheus para actividad/estado, útil para instrumentar tu operación GitOps.[^2]
Facts: Argo CD muestra drift (OutOfSync) y permite sync manual/automático, lo que habilita medir “tiempo a reconciliar” por ambiente.[^2]
Inferences: Señales que importan en CRM enterprise:

- Drift rate: \# drifts detectados/semana por workspace/cluster (y su severidad).
- MTTD drift y MTTR drift: detección y corrección por tipo (seguridad vs config).
- Policy effectiveness: % PR bloqueados por Conftest vs % incidentes por config (debe bajar).
- Change failure rate (prod): deploys que requieren rollback/hotfix.
- Lead time PR→prod: por equipo y por servicio (sin sacrificar gates).


## Operational checklist

Facts: Conftest incluye `conftest verify` para verificar políticas (y tests de políticas por convención).[^4]
Facts: Flux permite disparar reconciliación de una fuente Git (`flux reconcile source git`) y también vía annotation `reconcile.fluxcd.io/requestedAt`.[^6][^7]
Facts: Argo CD se basa en Git como source of truth y automatiza despliegue de desired state en ambientes target.[^2]
Inferences: Checklist ejecutable (CRM enterprise):

- Definir repos separados o carpetas por ambiente (dev/stage/prod) y estrategia de promoción por PR.
- Implementar CODEOWNERS + ramas protegidas: `infra/` requiere Platform; `policy/` requiere Security; `prod/` requiere aprobación doble.
- CI obligatorio: lint + tests + `conftest test` (manifests/IaC) antes de merge.[^5][^4]
- Argo CD: auto-sync solo en dev/stage; en prod manual sync + `Prune=confirm` en recursos críticos.[^2]
- Drift detection IaC: refresh-only plan programado por workspace (min diario; ideal cada hora en prod).[^1]
- OPA admission: bloquear lo “no negociable” (PII, exposición pública, privilegios) y dejar warnings para estándares.[^3]
- Break-glass: si existe acceso manual, que sea temporal, auditado y con PR de “backport” obligatorio para cerrar drift (operación, no teoría).


## Anti-patterns

Facts: Argo CD considera `OutOfSync` cuando el live state se desvía del target state definido en Git.[^2]
Inferences: Anti-patterns comunes en CRM enterprise:

- “kubectl apply” en prod como rutina (te compra velocidad hoy y drift/bugs mañana).
- Políticas solo en runtime (OPA) pero no en CI (llegas tarde y rompes el flujo con denegaciones).
- Un solo repo/branch sin separación por ambientes (promoción sin trazabilidad real).
- Prune agresivo en prod sin confirmación (riesgo de borrado accidental).
- SoD “de PowerPoint”: mismos usuarios aprueban y ejecutan, o credenciales compartidas.


## Diagnostic questions

Facts: Argo CD soporta sync manual o automático, y puede requerir confirmación para pruning de recursos con `Prune=confirm`.[^2]
Facts: OPA admission control permite permitir/denegar objetos en create/update/delete.[^3]
Facts: Conftest permite tests sobre Terraform/Kubernetes y otros configs usando Rego.[^5][^4]
Inferences: Preguntas para diagnosticar madurez (CRM enterprise):

- ¿Cuánto de prod se puede cambiar sin PR (y quién puede hacerlo)?
- ¿Tu promoción dev→stage→prod es el mismo artefacto o “rebuild” por ambiente?
- ¿Qué políticas bloquean merge (CI) vs cuáles bloquean deploy (admission)?
- ¿Tienes drift detection automatizado con cadencia definida por criticidad?[^1]
- Cuando hay urgencia: ¿tu proceso reduce riesgo o solo lo mueve “a la madrugada”?
- ¿Qué porcentaje de cambios incluye rollback plan y owner responsable?


## Sources (o referencia a SOURCES.md)

- Argo CD Overview (GitOps CD, OutOfSync, RBAC, audit, sync modes). https://argo-cd.readthedocs.io/en/stable/[^2]
- Argo CD Sync Options (`spec.syncPolicy.syncOptions`, `Prune=confirm`, etc.). https://argo-cd.readthedocs.io/en/latest/user-guide/sync-options/
- HashiCorp: drift y detección automatizada con refresh-only plans y health assessments. https://developer.hashicorp.com/well-architected-framework/optimize-systems/monitor-system-health/detect-configuration-drift[^1]
- Terraform tutorial (drift/policy). https://developer.hashicorp.com/terraform/tutorials/cloud/drift-and-policy[^8]
- OPA Kubernetes admission control. https://openpolicyagent.org/docs/kubernetes[^3]
- Conftest (policy testing con Rego). https://www.conftest.dev[^4]
- Conftest GitHub (testing de Kubernetes/Terraform configs). https://github.com/open-policy-agent/conftest[^5]
- Flux: reconciliación de GitRepository y annotation `reconcile.fluxcd.io/requestedAt`. https://github.com/fluxcd/source-controller/blob/main/docs/spec/v1/gitrepositories.md[^6]
- Flux CLI: `flux reconcile source git`. https://fluxcd.io/flux/cmd/flux_reconcile_source_git/[^7]

SOURCES.md (entradas a añadir, sin duplicados):

- Añadir las URLs anteriores con una línea de descripción y la fecha de consulta (2026-02-18).


## Key takeaways for PM practice

- Diseña el proceso como producto: PR→checks→aprobación→promoción, con gates explícitos por riesgo (no por burocracia).
- Separa “velocidad” (dev/stage) de “seguridad” (prod) usando sync manual, confirmaciones y políticas bloqueantes.
- Mide drift como señal de salud operativa, no como culpa del equipo; donde hay drift recurrente hay un “atajo” sin control.
- Policy-as-code funciona mejor en dos capas: CI (Conftest) para evitar llegar tarde, y runtime (OPA) para evitar saltos.
- SoD efectivo es un diseño de permisos + repos + entornos protegidos, no un organigrama.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31][^9]</span>

<div align="center">⁂</div>

[^1]: https://developer.hashicorp.com/well-architected-framework/optimize-systems/monitor-system-health/detect-configuration-drift

[^2]: pasted-text.txt

[^3]: https://openpolicyagent.org/docs/kubernetes

[^4]: https://www.conftest.dev

[^5]: https://github.com/open-policy-agent/conftest

[^6]: https://github.com/fluxcd/source-controller/blob/main/docs/spec/v1/gitrepositories.md

[^7]: https://fluxcd.io/flux/cmd/flux_reconcile_source_git/

[^8]: https://developer.hashicorp.com/terraform/tutorials/cloud/drift-and-policy

[^9]: https://www.hashicorp.com/en/blog/detecting-and-managing-drift-with-terraform

[^10]: https://controlmonkey.io/blog/the-definitive-guide-for-terraform-drift-detection/

[^11]: https://terramate.io/rethinking-iac/the-ultimate-guide-for-terraform-and-opentofu-drift-detection-and-remediation/

[^12]: https://www.env0.com/blog/the-ultimate-guide-to-terraform-drift-detection-how-to-detect-prevent-and-remediate-infrastructure-drift

[^13]: https://oneuptime.com/blog/post/2026-02-09-gitops-promotion-pipeline-dev-staging-prod/view

[^14]: https://argo-gitops-promoter.readthedocs.io

[^15]: https://oneuptime.com/blog/post/2026-01-19-kubernetes-opa-gatekeeper-policy-enforcement/view

[^16]: https://www.linkedin.com/pulse/guide-terraform-drift-detection-remediation-spacelift-io-wx0pe

[^17]: https://www.freecodecamp.org/news/from-commit-to-production-hands-on-gitops-promotion-with-github-actions-argo-cd-helm-and-kargo/

[^18]: https://www.linkedin.com/pulse/policy-code-open-agent-opa-terraform-kubernetes-memorres-pjg3c

[^19]: https://devops.com/ai-driven-drift-detection-in-aws-terraform-meets-intelligence/

[^20]: https://amadeusitgroup.github.io/argo-projects-demo/PROMOTION_WORKFLOW/

[^21]: https://argo-cd.readthedocs.io/en/latest/user-guide/sync-options/

[^22]: https://argo-cd.readthedocs.io/en/stable/

[^23]: https://octopus.com/blog/combining-gitops-and-continuous-delivery-with-argo-cd-octopus

[^24]: https://www.gocodeo.com/post/how-argo-cd-works-declarative-deployments-and-sync-mechanisms

[^25]: https://codefresh.io/learn/argo-cd/

[^26]: https://appsecsanta.com/conftest

[^27]: https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/

[^28]: https://www.trek10.com/blog/exploring-gitops-with-argo-cd

[^29]: https://control-plane.io/posts/what-is-fluxcd/

[^30]: https://atlasgo.io/guides/deploying/k8s-argo

[^31]: https://fluxcd.io/flux/cmd/flux_reconcile_source/

