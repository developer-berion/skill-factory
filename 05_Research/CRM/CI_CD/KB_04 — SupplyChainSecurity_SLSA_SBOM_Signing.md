<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_04_SupplyChainSecurity_SLSA_SBOM_Signing — prácticas maduras 2026 (CRM + contenedores)

## Executive summary (10–15 líneas)

- **[Fact]** SLSA v1.0 pone el foco no solo en *generar* provenance, sino en **verificarla** contra expectativas (lo que cierra el “gap” típico de pipelines que “atestiguan” pero nadie valida).[^1]
- **[Fact]** La provenance en SLSA debe identificar el artefacto por digest criptográfico y describir cómo se produjo; es un requisito explícito de “Provenance Exists”.[^2]
- **[Fact]** Firmar artefactos cloud-native con Sigstore Cosign es un patrón maduro para contenedores y OCI, con verificación estándar.[^3][^4]
- **[Fact]** “Keyless signing” en CI funciona bien porque usa identidad OIDC para obtener un certificado de corta vida (en vez de llaves largas).[^4][^3]
- **[Fact]** GitHub Actions soporta OIDC para autenticación sin secretos estáticos y entrega credenciales de corta duración durante el job.[^5]
- **[Fact]** En Kubernetes, Kyverno puede verificar firmas y *in-toto attestations* con Cosign al momento de admisión, y además forzar uso de digest (pinning).[^6]
- **[Fact]** OPA Gatekeeper es un admission webhook para Kubernetes que aplica políticas vía OPA y permite control declarativo (policies-as-code).[^7]
- **[Fact]** CycloneDX y SPDX son estándares de SBOM; CycloneDX se adopta para cumplir mínimos de SBOM (p.ej., alineados a requisitos “mínimos” impulsados por EO 14028/NTIA).[^8]
- **[Fact]** Una práctica madura es automatizar SBOM en el pipeline y accionar sobre hallazgos (no “generar por generar”), manteniéndolo actualizado.[^9]
- **[Inference]** Para un CRM enterprise, el “endgame” operativo es: *solo* despliego imágenes firmadas, con SBOM + provenance verificadas por política, y con pinning a digests para evitar “tag drift”.
- **[Inference]** Comercialmente (B2B), esto reduce riesgo operacional (incidentes), acelera aprobaciones de seguridad del cliente y baja el costo de soporte post-release.

***

## Definitions and why it matters

- **[Fact]** *Provenance (SLSA)* es información verificable sobre dónde/cuándo/cómo se produjo un artefacto, y SLSA v1.0 describe explícitamente cómo verificarla.[^10][^1]
- **[Fact]** *SBOM* (Software Bill of Materials) es el inventario de componentes de software; CycloneDX se posiciona como formato capaz de cubrir requisitos de SBOM y madurar a casos de uso más sofisticados.[^8]
- **[Fact]** *Signing (firmado de artefactos)* con Cosign permite firmar/verificar artefactos (especialmente OCI) y soporta modalidad keyless basada en OIDC.[^3][^4]
- **[Fact]** *Policy enforcement* en Kubernetes suele implementarse con admission control (p.ej., Gatekeeper) para impedir recursos no conformes antes de persistirlos.[^7]

**Por qué importa en un CRM con contenedores**

- **[Inference]** Un CRM enterprise típicamente tiene muchas dependencias (SDKs, librerías, imágenes base, plugins, conectores) y múltiples equipos/terceros; eso multiplica superficie de ataque y hace difícil “saber qué está corriendo” en producción.
- **[Inference]** SBOM + signing + provenance verificadas convierten ese caos en control: inventario (SBOM), identidad/integridad (firmas) y trazabilidad verificable (provenance).

***

## Principles and best practices (2026)

**Fecha:** 2026-02-18.

### 1) “Generate + verify” (no solo generar)

- **[Fact]** SLSA v1.0 documenta la necesidad de **verificación** de provenance (porque muchas amenazas se mitigan solo cuando el consumidor verifica).[^1]
- **[Fact]** La provenance debe identificar el output por digest y describir cómo se produjo; es un requisito mínimo de SLSA para “provenance exists”.[^2]
- **[Inference]** Regla práctica: “si no se verifica en deploy/admisión o en promoción de artefactos, es paperwork”.


### 2) Keyless signing con identidad (OIDC) en CI

- **[Fact]** Cosign soporta keyless signing usando un token OIDC para obtener un certificado de corta vida (p.ej., vía Fulcio), ideal para CI/CD.[^4][^3]
- **[Fact]** GitHub Actions permite usar tokens OIDC en lugar de secretos y recibir credenciales de corta duración válidas solo durante el job.[^5]
- **[Inference]** En B2B, esto reduce fricción con auditorías (“no guardamos llaves de firma en repos”), y baja el riesgo de filtraciones.


### 3) Pinning a digests (anti “tag drift”)

- **[Fact]** Kyverno soporta atributos como `mutateDigest` (convertir tags a digests) y `verifyDigest` (enforzar uso de digest) en reglas `verifyImages`.[^6]
- **[Inference]** Política recomendada: dev puede usar tags; staging/prod se promueve **solo** por digest + firma válida.


### 4) Policy-as-code en runtime (admisión)

- **[Fact]** Gatekeeper aplica políticas en Kubernetes como admission webhook, interceptando requests antes de persistir objetos.[^7]
- **[Fact]** Kyverno puede verificar firmas e *in-toto attestations* con Cosign al momento de admisión.[^6]
- **[Inference]** Divide responsabilidades: CI produce (SBOM/provenance/firma); el clúster **verifica** y bloquea lo no conforme.


### 5) SBOM operacional (no “compliance theater”)

- **[Fact]** CycloneDX se plantea como estándar que ayuda a cumplir requisitos mínimos de SBOM y permite madurar casos de uso con el tiempo.[^8]
- **[Fact]** Buenas prácticas incluyen automatizar SBOM en el pipeline, mantenerlo actualizado y enfocarse en tomar acción (remediación) más que en “generar por generar”.[^9]
- **[Inference]** Para CRM: SBOM debe existir por *servicio* y por *imagen*, y alimentar un proceso de “vuln-to-patch SLA” (con excepciones explícitas).

***

## Examples (aplicado a CRM enterprise)

### Ejemplo A: Pipeline CI para servicio del CRM (contenedor)

- **[Fact]** En GitHub Actions, el job puede solicitar un token OIDC y usarlo para autenticación sin secretos estáticos.[^5]
- **[Fact]** Con Cosign keyless, la identidad OIDC del workload se usa para firmar artefactos con certificados de corta vida.[^3][^4]
- **[Inference]** Flujo recomendado (alto nivel): build imagen → generar SBOM (CycloneDX o SPDX) → generar attestation/provenance → firmar imagen y adjuntar attestations → publicar en registry → promover por digest.

**Qué incluye**

- **[Fact]** Firma/verificación de contenedores usando Cosign (artefactos OCI).[^4][^3]
- **[Fact]** SBOM en CycloneDX como formato adoptado para requisitos de SBOM y evolución de casos de uso.[^8]

**Qué no incluye**

- **[Inference]** No resuelve por sí solo “riesgo de dependencia” si no hay proceso de remediación y decisiones (aceptar/mitigar/bloquear).

**Sensible (riesgo/objeciones reales)**

- **[Inference]** SBOM puede exponer stack y versiones; define qué compartes con clientes/terceros y qué queda interno (y cómo lo proteges en el registry).
- **[Inference]** Si usas infraestructura pública de Sigstore en software cerrado, evalúa implicaciones de privacidad/metadata (decisión de seguridad y legal).


### Ejemplo B: Enforcing en Kubernetes (CRM en producción)

- **[Fact]** Kyverno `verifyImages` usa Cosign para verificar firmas y *in-toto attestations* almacenadas en un OCI registry.[^6]
- **[Fact]** Kyverno puede forzar digest pinning con `verifyDigest` y convertir tags a digest con `mutateDigest`.[^6]
- **[Inference]** Política “segura”: en `prod`, `required: true` y solo permite imágenes firmadas por identidades/repos esperados; además, bloquea despliegues por tag.


### Ejemplo C: Gobernanza complementaria con Gatekeeper

- **[Fact]** Gatekeeper permite enforcement declarativo de políticas vía admission control en Kubernetes.[^7]
- **[Inference]** Úsalo para guardrails “no cripto”: prohibir `latest`, exigir `runAsNonRoot`, limitar registries permitidos, exigir labels de trazabilidad (repo, equipo, owner).

***

## Metrics / success signals

- **[Fact]** SLSA v1.0 enfatiza que la mitigación real depende de verificación de provenance; por eso una métrica útil es “% de artefactos verificados” y no solo “% generados”.[^1]
- **[Inference]** % de imágenes en prod con: firma válida + digest pinning + SBOM adjunta + provenance/attestations verificadas.
- **[Inference]** \# de deploys bloqueados por policy (tendencia a la baja) y tiempo de ciclo para “hacer compliant” un servicio nuevo.
- **[Inference]** MTTR de vulnerabilidades explotables: desde alerta (por SBOM + scan) hasta release parchado, con “excepción” auditada cuando aplique.
- **[Inference]** Ratio de excepciones por equipo/proyecto (si sube, tu política es impracticable o tu plataforma no ayuda).

***

## Operational checklist

- **[Fact]** Define como mínimo provenance que identifica artefacto por digest y describe cómo se produjo (requisito SLSA “Provenance Exists”).[^2]
- **[Fact]** Implementa signing de imágenes OCI con Cosign (idealmente keyless con OIDC en CI).[^3][^4]
- **[Fact]** En GitHub Actions, migra autenticaciones a cloud/registry hacia OIDC para evitar secretos estáticos.[^5]
- **[Fact]** Genera SBOM en un estándar como CycloneDX y automatízalo en el pipeline (con actualización continua).[^9][^8]
- **[Fact]** En clúster, aplica verificación con Kyverno `verifyImages` (firmas + attestations) y fuerza digests con `verifyDigest/mutateDigest`.[^6]
- **[Fact]** Complementa con Gatekeeper para políticas generales de admisión y gobernanza.[^7]
- **[Inference]** Define un modelo de “excepciones”: quién aprueba, duración, evidencia requerida, y cómo se revoca automáticamente.

***

## Anti-patterns

- **[Fact]** Generar provenance sin verificación deja un hueco; SLSA v1.0 lo señala como gap que v1.0 busca cerrar con guía explícita de verificación.[^1]
- **[Inference]** “SBOM como PDF” o archivo suelto que nadie consume (sin automatización ni remediación).
- **[Inference]** Firmar con llaves largas guardadas como secretos en CI (alto riesgo de exfiltración; y mala rotación).
- **[Fact]** Desplegar por tags mutables cuando tu política podría forzar digests (`verifyDigest`) y convertir tags a digest (`mutateDigest`).[^6]
- **[Inference]** Políticas “todo o nada” sin carril de adopción (dev/stage/prod) ni mecanismo de excepción: termina en bypass manual.

***

## Diagnostic questions

- **[Fact]** ¿Estás verificando provenance (no solo generándola) como recomienda el enfoque de SLSA v1.0?[^1]
- **[Fact]** ¿Tus imágenes están firmadas y verificadas en admisión (Kyverno/Cosign) antes de correr en el clúster?[^6]
- **[Fact]** ¿Tu CI usa OIDC en vez de secretos estáticos (p.ej., GitHub Actions OIDC)?[^5]
- **[Inference]** ¿Puedes responder en 10 minutos: “qué versiones exactas (digests) corren en prod” y “quién las firmó / desde qué repo y workflow”?
- **[Inference]** ¿Tienes reglas explícitas para qué SBOM compartes con clientes (B2B) y cuál se queda interna por sensibilidad?

***

## Sources (y añadir a SOURCES.md)

- SLSA v1.0 — What’s new (énfasis en verificación de provenance). https://slsa.dev/spec/v1.0/whats-new[^1]
- SLSA v1.0 — Requirements (Provenance Exists, digest, descripción de producción). https://slsa.dev/spec/v1.0/requirements[^2]
- SLSA provenance (conceptos + verificación). https://slsa.dev/spec/v1.0-rc1/provenance[^10]
- Sigstore Cosign — Signing containers (OIDC/keyless). https://docs.sigstore.dev/cosign/signing/signing_with_containers/[^4]
- Chainguard — Introducción a Cosign (keyless + OIDC en CI). https://edu.chainguard.dev/open-source/sigstore/cosign/an-introduction-to-cosign/[^3]
- GitHub Docs — OpenID Connect en GitHub Actions. https://docs.github.com/en/actions/concepts/security/openid-connect[^5]
- Kyverno — Verify Images (Cosign, attestations, digest pinning). https://release-1-9-0.kyverno.io/docs/writing-policies/verify-images/[^6]
- Kubernetes Blog — OPA Gatekeeper (admission webhook + OPA). https://kubernetes.io/blog/2019/08/06/opa-gatekeeper-policy-and-governance-for-kubernetes/[^7]
- OWASP/CycloneDX — Authoritative Guide to SBOM (alineación con requisitos mínimos; capacidad). https://cyclonedx.org/guides/OWASP_CycloneDX-Authoritative-Guide-to-SBOM-en.pdf[^8]
- NexusConnect — Panorama SPDX vs CycloneDX (acción y actualización continua). https://nexusconnect.io/articles/spdx-cyclonedx-or-swid-navigating-the-sbom-standard-landscape[^9]

**Entradas a agregar en `SOURCES.md` (sin duplicados)**

- SLSA v1.0 — What’s new in SLSA v1.0 — https://slsa.dev/spec/v1.0/whats-new — Accessed: 2026-02-18.[^1]
- SLSA v1.0 — Requirements — https://slsa.dev/spec/v1.0/requirements — Accessed: 2026-02-18.[^2]
- Sigstore Cosign — Signing Containers — https://docs.sigstore.dev/cosign/signing/signing_with_containers/ — Accessed: 2026-02-18.[^4]
- GitHub Docs — OpenID Connect (Actions) — https://docs.github.com/en/actions/concepts/security/openid-connect — Accessed: 2026-02-18.[^5]
- Kyverno Docs — Verify Images — https://release-1-9-0.kyverno.io/docs/writing-policies/verify-images/ — Accessed: 2026-02-18.[^6]
- Kubernetes Blog — OPA Gatekeeper — https://kubernetes.io/blog/2019/08/06/opa-gatekeeper-policy-and-governance-for-kubernetes/ — Accessed: 2026-02-18.[^7]
- CycloneDX — Authoritative Guide to SBOM (PDF) — https://cyclonedx.org/guides/OWASP_CycloneDX-Authoritative-Guide-to-SBOM-en.pdf — Accessed: 2026-02-18.[^8]

***

## Key takeaways for PM practice

- Diseña el producto/plataforma para que “build produce evidencia” y “runtime la verifique” (no aceptes evidencia que nadie valida).[^1][^6]
- Empuja OIDC + keyless signing para bajar fricción y riesgo operativo en CI/CD.[^3][^4][^5]
- Define una estrategia explícita de pinning a digests y hazla política (no guideline).[^6]
- Trata SBOM como input operativo (remediación, SLAs, excepciones), no como artefacto de compliance.[^9][^8]
- Para CRM enterprise, separa carriles dev/stage/prod con enforcement progresivo y mecanismo de excepciones auditable (si no, te lo van a bypassear).
<span style="display:none">[^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24]</span>

<div align="center">⁂</div>

[^1]: https://slsa.dev/spec/v1.0/whats-new

[^2]: https://slsa.dev/spec/v1.0/requirements

[^3]: https://edu.chainguard.dev/open-source/sigstore/cosign/an-introduction-to-cosign/

[^4]: https://docs.sigstore.dev/cosign/signing/signing_with_containers/

[^5]: https://docs.github.com/en/actions/concepts/security/openid-connect

[^6]: https://release-1-9-0.kyverno.io/docs/writing-policies/verify-images/

[^7]: https://kubernetes.io/blog/2019/08/06/opa-gatekeeper-policy-and-governance-for-kubernetes/

[^8]: https://cyclonedx.org/guides/OWASP_CycloneDX-Authoritative-Guide-to-SBOM-en.pdf

[^9]: https://nexusconnect.io/articles/spdx-cyclonedx-or-swid-navigating-the-sbom-standard-landscape

[^10]: https://slsa.dev/spec/v1.0-rc1/provenance

[^11]: pasted-text.txt

[^12]: https://cloud.google.com/security/solutions/software-supply-chain-security?hl=es-419

[^13]: https://www.paloaltonetworks.es/prisma/cloud/software-supply-chain-security

[^14]: https://docs.cloud.google.com/software-supply-chain-security/docs/overview?hl=es-419

[^15]: https://snyk.io/es/solutions/software-supply-chain-security/

[^16]: https://www.verimatrix.com/es/ciberseguridad/base-de-conocimientos/software-supply-chain-security-critical-vulnerabilities-and-fixes/

[^17]: https://www.covulor.com/2025-10-15-blindando-la-cadena-de-suministro/

[^18]: https://adoptium.net/es/docs/slsa

[^19]: https://cycode.com/blog/securing-artifacts-keyless-signing-with-sigstore-and-ci-mon/

[^20]: https://oneuptime.com/blog/post/2025-12-20-oidc-cloud-authentication-github-actions/view

[^21]: https://oneuptime.com/blog/post/2026-02-09-kyverno-image-verification-cosign/view

[^22]: https://docs.rapid7.com/insightcloudsec/opa-gatekeeper/

[^23]: https://kyverno.io/policies/other/verify-image/verify-image/

[^24]: https://oneuptime.com/blog/post/2026-02-09-opa-gatekeeper-policy-admission/view

