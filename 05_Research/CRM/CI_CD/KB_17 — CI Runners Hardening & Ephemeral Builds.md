<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_17 — CI Runners Hardening \& Ephemeral Builds (2024–2026) para CRM enterprise

## Executive summary (10–15 líneas)

- Fact: En CI/CD, el runner ejecuta código remoto definido por el job, así que **cualquier** actor con capacidad de modificar pipelines puede convertir el runner en punto de entrada.
- Fact: GitHub recomienda autoscaling con runners efímeros (1 job por runner) para limitar exposición y reducir el riesgo de reutilizar un runner comprometido.[^1]
- Fact: En GitHub, un runner efímero se registra con `--ephemeral` y se desregistra automáticamente tras procesar un job.[^1]
- Fact: GitLab advierte que el riesgo se vuelve más agudo cuando los runners no son efímeros y se comparten entre proyectos (movimiento lateral entre repos).
- Fact: OIDC en GitHub Actions permite intercambiar tokens de corta vida con un cloud provider, reduciendo dependencia de secretos de larga vida.[^2]
- Fact: GitLab recomienda segmentación de red y sugiere filtrar/bloquear acceso a endpoints de metadata del cloud para reducir impacto de jobs maliciosos.
- Fact: Hay vectores reales de supply-chain en CI como cache poisoning en GitHub Actions (un atacante puede forzar evicción y “poison” de entradas).[^3]
- Fact: Controles anti-exfiltración prácticos incluyen allowlist de egreso (dominios) y monitoreo de escrituras de archivos durante el build.[^4]
- Fact: GitLab considera el Shell executor de alto riesgo y desaconseja `--privileged` porque habilita escalamiento/escape al host.
- Fact: Para evitar “shadow runners”, GitHub permite restringir runner groups a workflows específicos (además de repos).[^5]
- Inference: El objetivo operativo es que un runner comprometido “muera” rápido, tenga permisos mínimos y no tenga rutas fáciles para exfiltrar secretos, artefactos o datos de cliente (CRM).
- Inference: Para CRM enterprise, la decisión clave es: managed runners para builds estándar; self-hosted efímero + red segmentada solo para necesidades justificadas (VPN/legacy/PCI/data residency).

***

## Definitions and why it matters

**Facts**

- Fact: Un self-managed runner en GitLab ejecuta el código del job; por diseño, eso es un servicio de ejecución remota (RCE) y requiere hardening del stack y revisiones continuas.
- Fact: En GitHub Actions, “ephemeral runners for autoscaling” significa 1 job por runner, y GitHub no recomienda autoscaling con runners persistentes.[^1]
- Fact: OIDC en GitHub Actions permite que un step pida un token al OIDC provider de GitHub y lo intercambie por credenciales cloud **de corta vida** válidas solo durante el job.[^2]

**Inferences**

- Inference: “Aislamiento de builds” en la práctica es: (1) aislamiento de *estado* (no heredar filesystem/credenciales/cache de builds anteriores), (2) aislamiento de *red* (egreso controlado), (3) aislamiento de *identidad* (tokens de corta vida y permisos mínimos).
- Inference: En CRM enterprise, CI/CD suele tocar datos sensibles indirectamente (endpoints internos, llaves de integraciones, artefactos con configuración), por lo que el runner debe tratarse como un “sistema de alto riesgo”.

***

## Principles and best practices (con citas por sección + fecha)

### 1) Ephemeral-by-default (2026-02)

**Facts**

- Fact: GitHub recomienda implementar autoscaling con self-hosted runners efímeros; con efímeros se garantiza 1 job por runner y se limita la exposición de recursos sensibles de jobs anteriores.[^1]
- Fact: GitLab indica que el riesgo es más agudo cuando runners no efímeros se usan para múltiples proyectos (un repo malicioso puede comprometer otros).

**Inferences**

- Inference: Diseño objetivo: “no hay nada valioso que persistir”; si necesitas persistencia (cache), que sea explícita, con controles y tratada como input no confiable.
- Inference: Si tienes que usar self-hosted, prioriza VM/containers efímeros con “MaxBuilds=1 / 1 job” (concepto) y destrucción total del entorno.


### 2) Identidad de corta vida con OIDC (2026-02)

**Facts**

- Fact: En GitHub Actions, OIDC permite a workflows intercambiar un token de identidad por un token cloud de corta vida, disponible solo durante el job.[^2]
- Fact: `aws-actions/configure-aws-credentials` recomienda OIDC para obtener credenciales temporales y asume un rol con credenciales de corto plazo usando el OIDC endpoint.[^6]

**Inferences**

- Inference: Regla comercial: “nada de llaves cloud estáticas en secretos del repo” salvo excepciones con aprobación y expiración; OIDC reduce el blast radius y el costo operativo de rotación.
- Inference: Amarra claims del OIDC (repo, branch/tag, environment) a políticas IAM/Cloud (trust policy) para evitar que forks/branches no autorizados obtengan credenciales.


### 3) Permisos mínimos y control de superficie (2026-02)

**Facts**

- Fact: GitHub Actions requiere conectividad saliente a dominios específicos para operaciones (incluye dominios para caches/artefactos y también para obtener tokens OIDC).[^1]
- Fact: StepSecurity Harden-Runner ofrece (entre otras cosas) allowlist de egreso por dominios para prevenir exfiltración y visibilidad de archivos escritos durante el build.[^4]

**Inferences**

- Inference: Control práctico: allowlist de egreso “por perfil de pipeline” (build, test, release) y deny-by-default para cualquier cosa que no sea repos, registries, y endpoints explícitos.
- Inference: En self-hosted dentro de tu red, segmenta runners fuera de subredes “core” (CRM DB, ERP, backoffice) y expón recursos vía API gateway cuando se pueda (menos movimiento lateral).


### 4) Controles anti-exfiltración (2026-02)

**Facts**

- Fact: GitLab recomienda segmentación de red, restringir tráfico entre VMs de runners, bloquear SSH desde Internet y filtrar acceso a metadata endpoints del cloud.
- Fact: Praetorian recomienda postura zero-trust para self-hosted runners, minimizar acceso a red interna y aplicar egress allow-list.[^7]

**Inferences**

- Inference: Bloquea por defecto: metadata endpoints (ej. 169.254.169.254), resolvers DNS no aprobados, y salida a pastebins/anon file hosts; eso baja muchísimo el riesgo real de exfil en incidentes.
- Inference: Usa detección por “señales” (picos de DNS, conexiones a dominios nuevos, escrituras masivas a archivos) para cortar builds en caliente.


### 5) Caches seguros y “treat as untrusted” (2026-02)

**Facts**

- Fact: Se han documentado técnicas de cache poisoning en GitHub Actions donde un atacante puede forzar evicción y luego envenenar entradas para afectar otros workflows que restauran cache.[^3]
- Fact: En GitLab, `GIT_STRATEGY: fetch` en entornos compartidos puede permitir que usuarios inyecten código que se ejecute en pipelines de otros, y se recomienda usarlo solo si confías en todos los usuarios del entorno compartido.

**Inferences**

- Inference: Política: caches solo para acelerar compilación (dependencias), no para transportar artefactos de release; y nunca caches reutilizados entre niveles de confianza distintos (PR externos vs default branch).
- Inference: Valida/rehidrata: checksums, lockfiles, “clean build” en etapas de release, y separación fuerte de keys (branch + workflow + contexto) para evitar contaminación cruzada.


### 6) Gobernanza y “anti shadow runners” (2026-02)

**Facts**

- Fact: GitHub permite restringir runner groups a workflows específicos, además de repositorios, para control de acceso más fino.[^5]
- Fact: En GitHub Enterprise, el enfoque recomendado incluye gestionar acceso mediante grupos y (opcionalmente) restringir qué repositorios pueden usar el runner group.[^8]
- Fact: GitHub endurece la operación exigiendo versiones mínimas del self-hosted runner (enforcement/cronograma comunicado en 2026).[^9]

**Inferences**

- Inference: Gobernanza operativa: inventario único de runners (tags, owner, propósito, criticidad), y un “runner onboarding” formal; cualquier runner no registrado = se drena/bloquea.
- Inference: Control de cambios: runner images (AMI/VM templates) versionadas y aprobadas; prohibir instalaciones “manuales” fuera del pipeline de plataforma.

***

## Threat model típico (2024–2026)

| Threat | Cómo pasa | Impacto típico | Controles recomendados |
| :-- | :-- | :-- | :-- |
| Token theft (CI job token / credenciales) | Un job malicioso roba variables/credenciales en un entorno comprometido o compartido | Acceso a repos, artefactos, despliegues, cloud | Ephemeral runners (1 job) [^1]; segmentación de red + bloquear metadata endpoints ; OIDC para credenciales de corta vida [^2] |
| Cache poisoning | Atacante manipula/evicta y envenena caches para que otros workflows restauren contenido malicioso | Supply-chain interno, backdoor en releases | Evitar caches en release; keys segregadas; tratar cache como input no confiable (validar) [^3] |
| Secrets in logs | Scripts imprimen secretos por error o con intención (stdout/stderr, artifacts) | Exposición de secretos, accesos laterales | Inference: “no-print secrets” (linters), redacción/masking, revisión de logs/artefactos, y separación de permisos por entorno |
| Persistencia en runner | Runner no efímero queda backdooreado y recibe nuevos jobs | Compromiso prolongado, movimiento lateral | Reciclado agresivo/rotación; zero-trust y egress allow-list [^7]; recomendación de efímeros para autoscaling [^1] |
| Container breakout / host takeover | Uso de `--privileged` o Shell executor en hosts compartidos | Control del host, robo de credenciales, pivote a red interna | Evitar `--privileged` ; no usar Shell executor salvo builds confiables ; dedicación por tipo de job (protected branches) |


***

## Examples (aplicado a CRM enterprise)

**Facts**

- Fact: GitLab sugiere runners dedicados para jobs que requieren `--privileged` y restringirlos a protected branches; además recomienda que esos entornos sean aislados y efímeros.
- Fact: GitHub documenta que para obtener OIDC tokens se necesita acceso saliente a `*.actions.githubusercontent.com` (dominios requeridos).[^1]

**Inferences (casos típicos CRM)**

- Inference: “Pipeline de integraciones CRM” (Salesforce/HubSpot/ERP): usa managed runners para build/test; usa OIDC para asumir roles cloud por job; allowlist de egreso solo a APIs de terceros + registries + GitHub/GitLab.
- Inference: “Release CRM on-prem” (requiere VPN): self-hosted runner efímero dentro de una subred aislada; acceso a on-prem vía API gateway/jump controlado; sin acceso directo a DB del CRM, solo a endpoints de despliegue.
- Inference: “Jobs de data migration”: runner dedicado, sin cache, sin artefactos persistentes; logs con redacción; ventanas de ejecución y approvals (porque tocan datos de cliente y reputación).

***

## Metrics / success signals

**Facts**

- Fact: GitHub lista dominios requeridos para operaciones esenciales, caches/artefactos y OIDC; esto permite definir baseline de egreso “esperado” por runner.[^1]
- Fact: Harden-Runner reporta/monitorea egreso y recomienda permisos mínimos (capacidad declarada), además de allowlist de dominios.[^4]

**Inferences (métricas accionables)**

- Inference: % de pipelines en runners efímeros (target alto en repos críticos).
- Inference: “Egress drift”: número de dominios nuevos por workflow/semana (debería tender a cero en pipelines estables).
- Inference: MTTR de runner compromise: tiempo desde alerta → runner destruido y reemplazado (minutos, no horas).
- Inference: Incidentes por cache: número de releases que dependen de caches compartidos; objetivo: 0 en releases.

***

## Operational checklist

**Facts**

- Fact: En GitHub, runners efímeros se habilitan con `--ephemeral` y se recomienda reenviar logs a almacenamiento externo para troubleshooting.[^1]
- Fact: GitLab recomienda `always` pull policy (evitar `if-not-present`) en runners compartidos para prevenir reutilización indebida de imágenes privadas.

**Checklist (seguro vs agresivo)**

- Opción segura: Managed runners (cuando aplique) + OIDC + permisos mínimos + sin acceso a red interna (solo APIs expuestas).[^2]
- Opción agresiva: Self-hosted efímero con autoscaling + egress allowlist + segmentación estricta; solo si hay dependencia real (VPN, compliance, latency, hardware).[^7][^1]
- Implementa runners efímeros (1 job) y destrucción total del entorno (VM/container) al finalizar.[^1]
- Bloquea metadata endpoints del cloud desde runners (regla de red).
- Define allowlist de egreso por tipo de workflow; monitorea y bloquea egreso fuera de baseline.[^7][^4]
- Evita Shell executor para entornos no “trusted”; si existe, úsalo solo para builds confiables.
- Evita `--privileged`; si es inevitable, runners dedicados, aislados, efímeros y en protected branches.
- Cache policy: separa caches por nivel de confianza; no uses caches compartidos en release; valida inputs restaurados.[^3]
- GitHub governance: runner groups restringidos por repos y por workflow; inventario y ownership (sin runners “sueltos”).[^8][^5]
- Hygiene: actualización/compatibilidad del runner (SLO interno) y control de versiones mínimas exigidas por el proveedor.[^9][^1]

***

## Anti-patterns

**Facts**

- Fact: GitLab considera el Shell executor de alto riesgo porque los jobs corren con permisos del usuario del runner y pueden robar código de otros proyectos en el mismo servidor.
- Fact: GitLab indica que contenedores privilegiados dan capacidades de root del host y no se aconsejan.

**Inferences**

- Inference: “Runner compartido para todo” (PR externos + main + releases) con caches comunes: receta para poisoning y pivote.
- Inference: “Runners snowflake” (config manual) sin imagen base versionada: imposible auditar, parchear y reproducir.
- Inference: Secretos largos (PAT/keys) reutilizados por meses: cuando se filtran, el incidente se vuelve caro y silencioso.

***

## Diagnostic questions

**Facts**

- Fact: GitHub indica que autoscaling con persistent self-hosted runners no es recomendado y que con efímeros se garantiza 1 job por runner.[^1]
- Fact: GitLab remarca que cualquier Developer con control del job puede comprometer el entorno del runner.

**Preguntas**

- ¿Qué pipelines hoy corren en runners persistentes y por qué (requisito real vs costumbre)?
- ¿Los pipelines de release usan cache? Si sí, ¿cómo previenes poisoning entre workflows/branches?[^3]
- ¿Puedes bloquear metadata endpoints y egreso no aprobado sin romper builds?
- ¿Dónde se registran/permiten runners nuevos y cómo evitas “shadow runners”?[^5][^8]
- ¿Qué porcentaje de accesos a cloud ya va por OIDC vs secretos estáticos?[^2]

***

## Sources (y referencia a SOURCES.md)

- GitHub Docs — Self-hosted runners reference (incluye efímeros, dominios requeridos, autoscaling).[^1]
- GitHub Docs — OpenID Connect (OIDC) for GitHub Actions.[^2]
- GitLab Docs — Security for self-managed runners (riesgos por executor, segmentación, cleanup).
- Praetorian — Riesgos de self-hosted GitHub runners y recomendaciones (zero-trust, egreso, recycling).[^7]
- Research blog — GitHub Actions cache poisoning (técnicas y riesgos).[^3]
- GitHub Changelog — Restrict runner groups to specific workflows (control de acceso).[^5]
- GitHub Changelog — Self-hosted runner minimum version enforcement (operación y compliance).[^9]
- aws-actions/configure-aws-credentials — Recomendación de OIDC para credenciales temporales.[^6]


### Entradas para agregar a `SOURCES.md` (sin duplicados)

- GitHub Docs — “Self-hosted runners reference” — https://docs.github.com/en/actions/reference/runners/self-hosted-runners
- GitHub Docs — “OpenID Connect” — https://docs.github.com/en/actions/concepts/security/openid-connect
- GitLab Docs — “Security for self-managed runners” — https://docs.gitlab.com/runner/security/
- GitHub Changelog — “Restrict self-hosted runner groups to specific workflows” — https://github.blog/changelog/2022-03-21-github-actions-restrict-self-hosted-runner-groups-to-specific-workflows/
- GitHub Changelog — “Self-hosted runner minimum version enforcement extended” — https://github.blog/changelog/2026-02-05-github-actions-self-hosted-runner-minimum-version-enforcement-extended/
- Praetorian — “From Self-Hosted GitHub Runner to Self-Hosted Backdoor” — https://www.praetorian.com/blog/self-hosted-github-runners-are-backdoors/
- Adnan the Khan — “The Monsters in Your Build Cache (GitHub Actions Cache Poisoning)” — https://adnanthekhan.com/2024/05/06/the-monsters-in-your-build-cache-github-actions-cache-poisoning/
- GitHub repo — “aws-actions/configure-aws-credentials” (OIDC guidance) — https://github.com/aws-actions/configure-aws-credentials

***

## Key takeaways for PM practice

- Ephemeral runners (1 job) no son “nice to have”: son el control base para cortar persistencia y movimiento lateral.[^1]
- OIDC cambia el juego comercial: menos secretos estáticos, menos rotación manual, menor riesgo operativo por credenciales filtradas.[^6][^2]
- Cache es superficie de ataque: úsalo como acelerador, no como canal de confianza; en release, minimízalo o elimínalo.[^3]
- Anti-exfil es arquitectura: segmentación + bloqueo metadata + egreso allowlisted (y observable) reduce incidentes de alto impacto.[^4][^7]
- “Shadow runners” es un problema de gobernanza: runner groups restringidos (repos + workflows) e inventario/ownership obligatorio.[^8][^5]
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24]</span>

<div align="center">⁂</div>

[^1]: pasted-text.txt

[^2]: https://docs.github.com/en/actions/concepts/security/openid-connect

[^3]: https://adnanthekhan.com/2024/05/06/the-monsters-in-your-build-cache-github-actions-cache-poisoning/

[^4]: https://github.com/marketplace/actions/harden-runner

[^5]: https://github.blog/changelog/2022-03-21-github-actions-restrict-self-hosted-runner-groups-to-specific-workflows/

[^6]: https://github.com/aws-actions/configure-aws-credentials

[^7]: https://www.praetorian.com/blog/self-hosted-github-runners-are-backdoors/

[^8]: https://docs.github.com/en/enterprise-server@3.14/admin/managing-github-actions-for-your-enterprise/getting-started-with-github-actions-for-your-enterprise/getting-started-with-self-hosted-runners-for-your-enterprise

[^9]: https://github.blog/changelog/2026-02-05-github-actions-self-hosted-runner-minimum-version-enforcement-extended/

[^10]: https://docs.github.com/es/actions/reference/runners/self-hosted-runners

[^11]: https://docs.gitlab.com/ci/runners/hosted_runners/

[^12]: https://cml.dev/doc/self-hosted-runners

[^13]: https://docs.github.com/es/enterprise-server@3.17/actions/how-tos/manage-runners/self-hosted-runners/monitor-and-troubleshoot

[^14]: https://docs.github.com/en/actions/reference/runners/self-hosted-runners

[^15]: https://www.stepsecurity.io/blog/ci-cd-security-for-self-hosted-vm-runners

[^16]: https://docs.github.com/es/actions/tutorials/migrate-to-github-runners

[^17]: https://pulsesecurity.co.nz/articles/OMGCICD-gitlab

[^18]: https://docs.github.com/es/actions/reference/runners/github-hosted-runners

[^19]: https://oneuptime.com/blog/post/2026-01-25-github-actions-self-hosted-runners/view

[^20]: https://docs.gitlab.com/runner/security/

[^21]: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Security-Guide/Security-hardening-for-GitHub-Actions/page

[^22]: https://github.com/marketplace/actions/configure-aws-credentials-action-for-github-actions

[^23]: https://www.javacodegeeks.com/2025/05/secure-your-github-actions-pipelines-prevent-secret-leaks-and-token-abuse.html

[^24]: https://www.stepsecurity.io/blog/github-actions-security-best-practices

