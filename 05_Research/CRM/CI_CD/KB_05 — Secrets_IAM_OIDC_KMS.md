<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_05_Secrets_IAM_OIDC_KMS — Gestión de secretos 2026 (pipelines + runtime) para CRM enterprise

## Executive summary (10–15 líneas)

[Fact] En 2026, la práctica dominante es **eliminar credenciales estáticas** en CI/CD usando federación OIDC para obtener credenciales temporales “just-in-time”.[^1]
[Fact] GitHub Actions permite emitir un token OIDC por corrida y usarlo para asumir un rol en AWS con credenciales de corta duración.[^2]
[Fact] Google Cloud recomienda Workload Identity Federation para que pipelines usen tokens OIDC y obtengan credenciales “short-lived”, evitando llaves largas.[^3]
[Fact] OWASP recomienda reducir impacto con credenciales temporales/OTP y reforzar “least privilege” en pipelines.[^4]
[Fact] Para runtime en Kubernetes, Vault soporta autenticación que favorece tokens de vida corta; también advierte límites de revocación cuando se valida JWT vía OIDC en vez de TokenReview.[^5]
[Fact] Vault documenta que, si usas JWT/OIDC contra Kubernetes como OIDC provider, tokens revocados pueden seguir válidos hasta expirar; mitigación: TTL corto o usar Kubernetes auth con TokenReview.[^6]
[Fact] OWASP indica rotar secretos regularmente y, cuando sea posible, forzar expiración para limitar ventana de abuso.[^7]
[Fact] Una gestión sólida de claves incluye ciclo de vida y rotación con frecuencia mínima anual como referencia en guías alineadas a NIST.[^8]
[Inference] En CRM enterprise (muchas integraciones + datos sensibles), tu objetivo operativo es: 1) cero secretos en repos, 2) credenciales efímeras por workload/tenant/entorno, 3) auditoría y respuesta rápida ante leaks.
[Inference] RBAC te da velocidad y claridad; ABAC te da control fino (tenant, entorno, región, clasificación de datos) para reducir riesgo comercial y operativo.
[Inference] Secret scanning y controles de “egress” no reemplazan vault/KMS; son capas para detectar filtraciones y acotar blast radius.
[Inference] La “opción segura” es OIDC + credenciales efímeras + policies estrictas; la “opción agresiva” acelera delivery, pero exige monitoreo/alertas y rotación más frecuente para sostener el riesgo.

***

## Definitions and why it matters

[Fact] “Secret” incluye credenciales (API keys, passwords, tokens), material criptográfico, y cualquier dato que habilite acceso o firma/cifrado.[^7]
[Fact] OWASP diferencia entre rotación (cambiar un secreto) vs creación dinámica (emitir credenciales cortas que mueren con el consumidor), destacando que lo dinámico reduce filtración y facilita detectar abuso.[^7]
[Inference] En un CRM enterprise, “secreto” también es cualquier credencial de integración (ERP, pagos, mensajería, data warehouse, marketing automation) y su mal manejo pega directo en SLA, fraude, churn B2B y reputación.
[Inference] “Pipelines” (CI/CD) y “runtime” (apps corriendo) deben tener modelos distintos: el pipeline necesita permisos explosivos pero ultra acotados en tiempo; runtime necesita permisos mínimos pero persistentes con renovación automática.

***

## Principles and best practices (2026-02-18)

### 1) Preferir OIDC + credenciales de corta vida en CI/CD

[Fact] GitHub documenta la configuración de OIDC con AWS para que workflows asuman roles sin guardar access keys, usando identidad federada.[^9]
[Fact] AWS explica que con OIDC + roles puedes borrar access keys de IAM users y usar credenciales temporales desde el workflow.[^1]
[Fact] Google Cloud describe Workload Identity Federation para que pipelines usen tokens OIDC y obtengan credenciales de corta vida (sin llaves largas).[^3]
[Inference] Patrón recomendado: “No secrets en CI” → el pipeline solo porta un token OIDC del proveedor (GitHub/GitLab/etc.) y lo intercambia por credenciales temporales en el cloud/Vault; si se filtra, expira rápido y es rastreable por claims (repo, branch, job).

**Qué incluye**: federación OIDC, trust policy por repo/branch/environment, TTL corto (minutos), y scope mínimo por job.[^2]
**Qué no incluye**: acceso humano directo con esos roles (separa identidades humanas vs workloads), ni tokens reutilizables entre jobs.[^1]
**Sensible**: claims demasiado amplios (p.ej., permitir cualquier repo de una org), o TTL largo “por conveniencia”.[^2]

### 2) Runtime en Kubernetes: autenticación fuerte, TTL corto, renovación automática

[Fact] HashiCorp Vault indica que validar JWT con Kubernetes como OIDC provider permite “short-lived tokens for all clients”, pero no puedes revocar antes del TTL; recomienda TTL corto.[^5]
[Fact] Vault detalla que JWT auth no usa TokenReview; tokens revocados pueden seguir válidos hasta expirar; mitigación: TTL corto o usar Kubernetes auth (TokenReview).[^6]
[Inference] Para CRM: usa identidad por servicio (service account) y “policy per app” (y, si aplica, per tenant) para que cada microservicio solo lea los secretos que consume (no “carpetas completas”).

**Qué incluye**: auth method (Kubernetes auth o JWT/OIDC), policies por namespace/app, tokens periódicos/renovables, y fallback operacional (break-glass) con expiración.[^6]
**Qué no incluye**: montar secretos como variables de entorno permanentes sin refresh (favorece dumps y “accidental logging”).[^7]
**Sensible**: TTLs altos para “evitar caídas”; mejor resolverlo con renovación y sidecar/agent, no con TTL infinito.[^7]

### 3) Vault/KMS: centralizar, auditar, y reducir “blast radius”

[Fact] OWASP recomienda centralizar gestión de secretos y aplicar expiración/rotación mediante el sistema de secrets management, limitando ventana de abuso.[^7]
[Fact] Guías de manejo de claves (key management) recomiendan rotación mínima anual y que el schedule puede basarse en edad o volumen de uso.[^8]
[Inference] En CRM, separa claramente: “secrets de acceso” (tokens/keys) vs “keys de cifrado” (KMS/HSM) vs “config sensible”; cada uno con controles distintos y dueños distintos (SecOps/Platform/App).

**Qué incluye**: logging/auditoría de lecturas, versiones, expiración/lease, rotación automatizada y procedimientos de emergencia.[^7]
**Qué no incluye**: “un KMS para todo” sin segmentación por entorno/tenant; eso te deja con un single point of failure/riesgo.[^8]
**Sensible**: accesos “wildcard” a paths o keys maestras; eso mata el least privilege en una sola mala policy.[^7]

### 4) Rotación, expiración y “dynamic secrets” como default

[Fact] OWASP recomienda rotación regular y, cuando sea posible, secretos con expiración definida (forzada por el sistema).[^7]
[Fact] OWASP destaca credenciales dinámicas/short-lived como forma de reducir filtración y facilitar detección de uso indebido.[^7]
[Inference] “Rotación” sin automatización es aspiracional: define SLO de rotación y mide cumplimiento; si no, el negocio terminará pidiendo excepciones para “no romper integraciones”.

**Qué incluye**: TTL por tipo de secreto (minutos/horas para access tokens; días/semanas para integraciones heredadas), rotación automática y runbooks de rollback.[^7]
**Qué no incluye**: rotar “a mano” por calendario sin inventario ni ownership.[^7]
**Sensible**: integraciones legacy (CRMs/ERPs antiguos) donde no hay soporte real para credenciales efímeras; ahí necesitas compensaciones (scopes mínimos, IP allowlist, monitoreo).[^4]

### 5) Secret scanning como control de higiene (no como “seguridad”)

[Fact] OWASP CI/CD enfatiza que, si secretos son robados, credenciales temporales reducen impacto y que debes aplicar least privilege/identity lifecycle.[^4]
[Inference] Secret scanning debe correr en: pre-commit (ideal), PR/MR, y en repos históricos; la meta comercial es bajar “incidentes por error humano” (copiar-pegar keys) y acelerar respuesta cuando pasa.

**Qué incluye**: detección + bloqueo (policy) + proceso de respuesta (revocar/rotar + invalidar sesiones + post-mortem).[^7]
**Qué no incluye**: confiar en scanning para permitir secrets en repos (“igual lo detecta”).
**Sensible**: falsos positivos que bloquean releases; resuélvelo con allowlists gobernadas y “break-glass” auditado, no apagando el control.

### 6) Autorización: RBAC vs ABAC (modelo práctico para CRM)

[Fact] OWASP recomienda “scope of authorization” y least privilege para las credenciales usadas por tooling CI/CD y acceso a secretos.[^7]
[Inference] RBAC: rápido para equipos (SalesOps, Integraciones, Data, Platform) y entornos (dev/stg/prod). ABAC: esencial cuando hay multi-tenant, regiones (residencia de datos), o “tiers” de clientes (Gold/Enterprise) que exigen segmentación.

**Qué incluye**: RBAC para base (roles claros), ABAC para excepciones (tenant_id, env, region, app_id, data_classification) y “policy as code” revisable.
**Qué no incluye**: “admin por defecto” para destrabar tickets; eso se vuelve deuda y fuga de margen por incidentes.
**Sensible**: ABAC mal diseñado puede volverse inmantenible; establece un set pequeño de atributos y un estándar de naming/policies.

***

## Examples (aplicado a CRM enterprise)

### Ejemplo A — Pipeline (GitHub Actions → AWS) sin secretos estáticos

[Fact] La acción `aws-actions/configure-aws-credentials` recomienda usar el OIDC provider de GitHub para obtener credenciales temporales necesarias para el workflow.[^2]
[Fact] AWS describe que con OIDC puedes sustituir access keys por credenciales temporales desde GitHub Actions.[^1]
[Inference] Implementación típica CRM: workflow “deploy-crm-api” asume un rol limitado a desplegar (ECS/EKS) y leer solo parámetros necesarios (no acceso a toda la cuenta).

Flujo:

- [Fact] GitHub emite un token OIDC por corrida; el workflow lo usa para asumir un rol con credenciales de corta vida.[^2]
- [Inference] El rol está restringido por claims (repo, branch, environment) y expira en minutos; si alguien exfiltra logs, el token ya no sirve.


### Ejemplo B — Runtime (Kubernetes → Vault) con TTL corto y políticas por servicio

[Fact] Vault explica que validar JWT vía OIDC implica que revocaciones no aplican hasta expiración; por eso recomienda TTL corto, o usar Kubernetes auth con TokenReview.[^6]
[Fact] Vault también menciona que usar JWT auth con Kubernetes como OIDC provider permite tokens de vida corta para clientes.[^5]
[Inference] Implementación CRM: `crm-notifications` solo puede leer `secret/data/prod/crm-notifications/*`, y su token se renueva automáticamente; si el pod muere, el secreto “vive” solo hasta el TTL/lease.

***

## Metrics / success signals

[Fact] OWASP recomienda expiración/rotación y uso de secretos dinámicos/short-lived para limitar ventana de abuso; eso se puede medir por TTLs y porcentaje de credenciales efímeras.[^7]
[Inference] Métricas operables (que sí mueven riesgo + velocidad en CRM):

- % de pipelines autenticando por OIDC (sin secretos estáticos) por repositorio/equipo.
- % de workloads runtime con credenciales efímeras (TTL ≤ 1h) vs estáticas.
- “Secret leak MTTR”: tiempo desde detección → revocación/rotación completa (objetivo: horas, no días).
- Cobertura de rotación: % secretos con rotación automatizada y “owner” definido.
- Incidentes por “over-permission”: conteo de policies con wildcard en prod (objetivo: tendencia a cero).

***

## Operational checklist

[Fact] OWASP recomienda rotación/expiración, scoping de autorización y credenciales temporales para CI/CD.[^7]
[Fact] Vault recomienda TTL corto cuando validas JWT vía OIDC por limitaciones de revocación.[^5]

- Inventario: lista única de secretos/keys por sistema, owner, entorno, criticidad, y consumidor (app/pipeline).
- CI/CD: habilitar OIDC federation (GitHub/GitLab/etc.), roles por repo+environment, TTL minutos, sin secrets en variables del pipeline.[^2]
- Runtime: auth de workloads (Kubernetes auth o JWT/OIDC), policies mínimas por servicio/namespace, TTL corto + renovación automática.[^6]
- Vault/KMS: auditoría habilitada, control de acceso por path/key, versionado, expiración/leases donde aplique.[^7]
- Rotación: calendar + automatización + runbook (incluye emergencia), pruebas de rotación en staging y rollback.[^8]
- Secret scanning: bloqueo en PR/MR + monitoreo de repos históricos + proceso de respuesta (revocar/rotar).
- Observabilidad: alertas por lecturas anómalas de secretos, uso fuera de patrón, y fallas de renovación (para evitar downtime).
- “Break-glass”: acceso excepcional, con expiración obligatoria, logging, y aprobación (evitar “admins permanentes”).

***

## Anti-patterns

[Fact] OWASP recomienda evitar credenciales reutilizables y aplicar expiración/rotación; lo contrario incrementa el impacto si hay robo.[^7]
[Fact] Vault advierte que con JWT auth validado por OIDC, revocación no corta el token antes de expirar; TTL largo agrava ese riesgo.[^6]

- Guardar secrets en repos (aunque sea “privado”) o en artifacts de CI/CD.
- “Un secreto para todo”: misma API key para múltiples microservicios/tenants.
- TTLs largos por comodidad (“para que no se caiga”), sin renovación automática.[^7]
- Policies con wildcards en producción (p.ej., `secret/*`) y sin revisión.
- Rotación manual sin pruebas: rota el viernes y rompe el lunes (y luego nadie quiere rotar).
- Confiar en secret scanning como excusa para mantener estáticos en CI.

***

## Diagnostic questions

[Fact] OWASP recomienda scoping de autorización y expiración; estas preguntas validan si eso existe de forma operable.[^7]
[Fact] GitHub/AWS describen OIDC para eliminar access keys en workflows; aquí validas adopción real.[^1]

- ¿Qué porcentaje de tus pipelines todavía depende de “secrets” estáticos (GitHub Secrets/variables) para cloud access?
- Si hoy se filtra un token de CI, ¿cuánto dura vivo y qué puede hacer exactamente (scope real)?
- ¿Cada microservicio del CRM tiene su propia identidad y policy, o comparten credenciales?
- ¿Puedes revocar acceso de un workload en minutos sin redeploy masivo?
- ¿Rotación está automatizada y probada en staging, o es “procedimiento en Confluence”?
- ¿Tu modelo de autorización necesita ABAC (tenant/región/data tier), o RBAC te alcanza sin sobrecomplicar?

***

## Sources (o referencia a SOURCES.md)

[Fact] OWASP Secrets Management Cheat Sheet (rotación, expiración, dynamic secrets): https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html[^7]
[Fact] OWASP CI/CD Security Cheat Sheet (credenciales temporales, least privilege): https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html[^4]
[Fact] GitHub Docs — OIDC en AWS: https://docs.github.com/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services[^9]
[Fact] AWS Security Blog — OIDC GitHub Actions → AWS (eliminar access keys): https://aws.amazon.com/blogs/security/use-iam-roles-to-connect-github-actions-to-actions-in-aws/[^1]
[Fact] `aws-actions/configure-aws-credentials` (OIDC y credenciales temporales): https://github.com/aws-actions/configure-aws-credentials[^2]
[Fact] HashiCorp Vault — Kubernetes auth method (tokens cortos, recomendaciones): https://developer.hashicorp.com/vault/docs/auth/kubernetes[^5]
[Fact] HashiCorp Vault — Kubernetes como OIDC provider (TTL, revocación): https://developer.hashicorp.com/vault/docs/auth/jwt/oidc-providers/kubernetes[^6]
[Fact] Google Cloud — Workload Identity Federation con deployment pipelines: https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines[^3]
[Fact] CMS Key Management Handbook (rotación mínima anual; referencia a NIST 800-57): https://security.cms.gov/learn/cms-key-management-handbook[^8]

### Entradas para añadir a `SOURCES.md` (sin duplicados)

- OWASP — Secrets Management Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html[^7]
- OWASP — CI/CD Security Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html[^4]
- GitHub Docs — Configuring OpenID Connect in Amazon Web Services — https://docs.github.com/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services[^9]
- AWS Security Blog — Use IAM roles to connect GitHub Actions to actions in AWS — https://aws.amazon.com/blogs/security/use-iam-roles-to-connect-github-actions-to-actions-in-aws/[^1]
- GitHub Repo — aws-actions/configure-aws-credentials — https://github.com/aws-actions/configure-aws-credentials[^2]
- HashiCorp Vault Docs — Kubernetes auth method — https://developer.hashicorp.com/vault/docs/auth/kubernetes[^5]
- HashiCorp Vault Docs — Use Kubernetes for OIDC authentication — https://developer.hashicorp.com/vault/docs/auth/jwt/oidc-providers/kubernetes[^6]
- Google Cloud Docs — Workload Identity Federation with deployment pipelines — https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines[^3]
- CMS — Key Management Handbook — https://security.cms.gov/learn/cms-key-management-handbook[^8]

***

## Key takeaways for PM practice

- Diseña “ventas + operación” alrededor de credenciales efímeras: menos incidentes, menos fricción, mejor continuidad B2B.
- OIDC en CI/CD es el quick win: elimina llaves largas y reduce riesgo sin frenar delivery.[^1]
- En runtime, el detalle que rompe todo es TTL/renovación + policies por servicio; ahí se gana el control real.[^6]
- RBAC primero para claridad; ABAC solo donde el negocio exige segmentación (tenant/región/tier) para no crear complejidad inmantenible.
- Rotación sin automatización no escala: mide cumplimiento y hazlo parte del Definition of Done.[^7]
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31]</span>

<div align="center">⁂</div>

[^1]: https://aws.amazon.com/blogs/security/use-iam-roles-to-connect-github-actions-to-actions-in-aws/

[^2]: https://github.com/aws-actions/configure-aws-credentials

[^3]: https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines

[^4]: https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html

[^5]: https://developer.hashicorp.com/vault/docs/auth/kubernetes

[^6]: https://developer.hashicorp.com/vault/docs/auth/jwt/oidc-providers/kubernetes

[^7]: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

[^8]: https://security.cms.gov/learn/cms-key-management-handbook

[^9]: https://docs.github.com/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services

[^10]: pasted-text.txt

[^11]: https://amplifying.ai/product/owasp-ci-cd-security-cheat-sheet

[^12]: https://cycode.com/blog/the-2025-owasp-top-10-addressing-software-supply-chain-and-llm-risks-with-cycode/

[^13]: https://cheatsheetseries.owasp.org/index.html

[^14]: https://www.kiteworks.com/regulatory-compliance/encryption-key-rotation-strategies/

[^15]: https://www.scribd.com/document/928105859/Ci-CD-Pipeline-Security-Best-Practices

[^16]: https://terrazone.io/nist-800-57/

[^17]: https://www.oligo.security/academy/owasp-top-10-cheat-sheet-of-cheat-sheets

[^18]: https://phuchoang.sbs/posts/gitops-kubernetes-oidc-vault/

[^19]: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html

[^20]: https://oneuptime.com/blog/post/2026-01-30-vault-auth-method-configuration/view

[^21]: https://github.com/marketplace/actions/configure-aws-credentials-action-for-github-actions

[^22]: https://oneuptime.com/blog/post/2026-02-02-github-actions-oidc-aws/view

[^23]: https://www.firefly.ai/academy/setting-up-workload-identity-federation-between-gitlab-ci-cd-and-google-cloud

[^24]: https://aembit.io/blog/what-identity-federation-means-for-workloads-in-cloud-native-environments/

[^25]: https://dev.to/aws-builders/securely-access-amazon-eks-with-github-actions-and-openid-connect-2im2

[^26]: https://security.googlecloudcommunity.com/community-blog-42/securing-your-ci-cd-pipeline-eliminate-long-lived-credentials-with-workload-identity-federation-2-3909

[^27]: https://learn.microsoft.com/en-us/azure/databricks/dev-tools/auth/oauth-federation-provider

[^28]: https://www.rkon.com/articles/github-actions-on-aws-how-to-implement-identity-federation/

[^29]: https://docs.gitlab.com/ci/cloud_services/google_cloud/

[^30]: https://www.tothenew.com/blog/modern-authentication-with-azure-workload-identity-federation/

[^31]: https://github.com/figma/actions-configure-aws-credentials

