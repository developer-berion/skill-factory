<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Archivo objetivo: KB_16_VulnManagement_SBOM_PolicyGates_CRM.md

Prompt:
Con base en prácticas maduras (2024–2026), documenta cómo manejar vulnerabilidades cuando ya generas SBOM y firmas artefactos: SLAs por severidad, excepciones gobernadas, priorización por explotación, “break-glass” con auditoría, y gates progresivos (PR vs build vs deploy).
Incluye cómo evitar “security theater”: qué métricas miden eficacia (time-to-remediate, % builds bloqueados por policy con falsos positivos, etc.).
Entrega KB estándar + SOURCES.md.

```markdown
# KB_16_VulnManagement_SBOM_PolicyGates_CRM.md

## Executive summary (10–15 líneas)
Este KB define un manejo “maduro” de vulnerabilidades cuando ya generas SBOM y firmas artefactos: SLAs por severidad, priorización por explotación, excepciones gobernadas, break-glass auditado y policy gates progresivos desde PR hasta deploy.  
Facts (2026-01): EPSS es un score probabilístico (0–1) que estima la probabilidad de explotación “en los próximos 30 días” y ayuda a priorizar por **probabilidad**, no solo por impacto. [web:18]  
Facts (2021-12): CISA recomienda monitorear el catálogo KEV y priorizar la remediación de esas vulnerabilidades; para agencias federales hay plazos bajo BOD 22-01. [web:17]  
Facts (SLSA v1.0): SLSA define niveles donde existe “provenance” y, a partir de L2, la provenance se liga al build platform mediante firma digital, habilitando verificación downstream. [web:19]  
Facts (Cosign): Cosign verifica claims y su integración en un transparency log, y valida contra la clave/certificado indicado. [web:12]  
Inferences: Con SBOM + firmas, el objetivo operativo no es “ver más hallazgos”, sino reducir riesgo real con decisiones repetibles: qué bloquear, cuándo excepcionar y cómo auditar sin frenar delivery.  
Inferences: El patrón ganador es “gates por etapa” (PR/build/deploy) + “excepciones con caducidad” + “priorización KEV/EPSS/exposición” + métricas anti–security-theater.  
Inferences: En un CRM enterprise (multi-tenant, integraciones, módulos), los gates deben ser progresivos por componente (core vs connectors) y por entorno (staging vs prod).  
Inferences: Break-glass debe existir, pero caro: temporal, trazable, con reversión y retro post-mortem.  
Inferences: Si mides bien (TTR, falsos positivos, overrides), puedes endurecer gates trimestre a trimestre sin “matar” a los equipos.

## Definitions and why it matters
Facts (2025-11): Los SBOM ayudan a responder más rápido a vulnerabilidades al saber qué componentes están presentes y dónde. [web:3]  
Facts (SLSA v1.0): La “provenance” describe cómo se construyó un artefacto (plataforma, proceso e inputs top-level), y se distribuye para verificación por consumidores. [web:19]  
Facts (2026-01): EPSS probabiliza explotación y su percentil ayuda a interpretar “qué tan alto” es un valor en la distribución global. [web:18]  
Inferences: Con SBOM + artefactos firmados, puedes pasar de “gestión de vulnerabilidades por lista” a “gestión por evidencia”: qué está explotado (KEV), qué es probable (EPSS), qué te expone (internet-facing), y si el binario es el que dices (firma/provenance).  
Inferences: En CRM enterprise, el impacto típico es doble: continuidad comercial (no caer el servicio) y confianza (cumplimiento/seguridad para clientes B2B), por eso los SLAs y gates deben estar ligados a riesgo y a rutas críticas (auth, pagos, integraciones, datos).

## Principles and best practices (con citas por sección + fecha)
Facts (2022-02): NIST SSDF (SP 800-218) es un marco de prácticas de desarrollo seguro impulsado por el foco en cadena de suministro y gestión de vulnerabilidades. [page:0]  
Facts (2026-01): Una práctica SSDF “Respond to Vulnerabilities” se implementa típicamente con tracking central, priorización (CVSS+EPSS) y remediación dentro de SLAs definidos. [web:7]  
Facts (SLSA v1.0): En SLSA, L1 exige que exista provenance; L2 añade que la provenance esté firmada y verificable downstream, reduciendo riesgo de tampering post-build. [web:19]  
Facts (Cosign): La verificación contempla validación de claims, presencia en transparency log e integración cuando el certificado era válido, además de verificar contra clave/cert. [web:12]  
Facts (2021-12): KEV aporta señal de explotación confirmada y se recomienda priorizar su remediación. [web:17]  
Facts (2026-01): EPSS es una probabilidad absoluta; por ejemplo, 0.10 puede estar en percentiles altos aunque “suene” bajo, por la baja tasa base de explotación. [web:18]  
Inferences: “Maduro” aquí significa: (1) SLA explícito y automático por severidad+contexto, (2) gates que fallan por políticas claras, (3) excepción como producto (workflow), no como “favor”, (4) auditoría y aprendizaje (root cause + hardening de reglas).  
Inferences: El orden de señales recomendado para priorización práctica es: KEV (explotado) > EPSS alto (probable) > exposición (internet-facing/privilegios/datos) > CVSS (impacto) > “ruido” de scanners.  
Inferences: Donde ya firmas artefactos, el gate mínimo de supply chain en deploy es “solo correr artefactos firmados por identidades autorizadas” (y opcionalmente con provenance).  
Inferences: Progresividad: en PR no bloquees por todo (solo “stop-ship”); en build endurece SCA/secret scanning; en deploy exige firma/provenance y bloquea “known-bad”.

### SLAs por severidad (modelo operativo)
Facts (2026-01): EPSS se actualiza y se interpreta como probabilidad en ventana corta (30 días), por lo que puede “subir” la urgencia aunque el CVSS no sea el más alto. [web:18]  
Facts (2021-12): KEV implica explotación confirmada y justifica plazos agresivos. [web:17]  
Inferences (baseline sugerido; ajustar por regulación y criticidad):
- Critical (stop-ship): 24–72h si (KEV) o (EPSS muy alto + internet-facing) o afecta auth/tenant isolation; si no, 7 días.
- High: 7–14 días (más cerca de 7 si exposición externa o datos sensibles).
- Medium: 30–60 días (o siguiente release train).
- Low: 90 días o “cuando toque”, salvo que escale por explotación.
Inferences: Define “cumplimiento de SLA” como “mitigación efectiva” (patch, upgrade, compensating control, feature flag) y no solo “cerrar ticket”.

### Excepciones gobernadas (sin romper el sistema)
Facts (SLSA v1.0): La verificación downstream de provenance/firma permite enforcement objetivo (pasa/no pasa) si defines políticas. [web:19]  
Inferences: Excepción = objeto versionado con: CVE/package, alcance (servicio/imagen), razón, evidencia (no alcanzable / compensating controls), aprobadores, expiración (TTL), plan de remediación y owner.  
Inferences: Toda excepción debe generar “deuda visible” (SLO de cierre de excepciones) y caducar por defecto; renovar requiere re-aprobación y nueva evidencia.

### Break-glass con auditoría (necesario, pero caro)
Facts (2026-02): En enforcement de verificación de imágenes se recomienda iniciar en modo no-bloqueante/observabilidad y “gradualmente” pasar a bloqueo. [web:9]  
Inferences: Break-glass solo para continuidad (incidente, rollback urgente, hotfix de revenue) y debe dejar rastro: quién, qué, cuándo, por qué, qué gate se saltó, y qué compensación activaste (WAF rule, rate limit, deshabilitar feature).  
Inferences: Reglas de oro: TTL corto (horas/días), scope mínimo (un artefacto/servicio), logging central + alerta, revisión en 24–48h, y post-mortem con acción correctiva (mejorar política o pipeline).

### Gates progresivos (PR vs build vs deploy)
Facts (Cosign): Cosign soporta verificación de firmas y transparencia (Rekor) para validar integridad y trazabilidad. [web:12]  
Facts (SLSA v1.0): SLSA L1/L2 provee un lenguaje para exigir provenance y autenticidad ligada al builder. [web:19]  
Inferences (patrón recomendado):
- Gate en PR (rápido, baja fricción): bloquear solo “stop-ship” (secrets reales, dependencia con KEV en componente expuesto, cambios en auth/crypto sin review), el resto como warnings con ticket auto-creado.
- Gate en build (calidad de artefacto): SCA completo + SBOM generado/adjunto + firma del artefacto; fallar si hay Critical/High sin excepción válida.
- Gate en deploy (control de ejecución): admitir solo artefactos firmados por identidades permitidas; opcionalmente exigir provenance (SLSA) y denegar si artefacto no coincide con SBOM/provenance esperado.

## Examples (aplicado a CRM enterprise)
Facts (2021-12): Vulnerabilidades KEV deben tratarse como prioridad alta por explotación confirmada. [web:17]  
Facts (2026-01): EPSS da señal de probabilidad y percentil para priorización cuando hay miles de CVEs. [web:18]  
Inferences (escenario CRM):
- Contexto: CRM multi-tenant con módulos (core API, web, workers), integraciones (WhatsApp/email/PSP), y conectores para agencias enterprise.
- Caso 1 (KEV en librería del gateway): Gate en build bloquea release; SLA = 24–72h; si hay outage comercial, break-glass permite deploy con WAF rule + rate limit, TTL 24h, y upgrade comprometido en siguiente ventana.
- Caso 2 (High CVSS pero EPSS bajo en módulo interno sin exposición): No bloqueas deploy; creas ticket con SLA 14–30 días; si hay evidencia de no alcanzabilidad, documentas excepción con TTL 30–60 días.
- Caso 3 (supply chain): Deploy gate rechaza imagen no firmada o firmada por identidad no autorizada; para rollback, break-glass autoriza solo ese digest y solo en prod por 2 horas, con alerta al canal de incidentes.

## Metrics / success signals
Facts (2026-01): EPSS ayuda a distinguir “probable” vs “poco probable” y a evitar priorización basada solo en impacto teórico. [web:18]  
Facts (2021-12): KEV es una lista práctica para priorización por explotación confirmada. [web:17]  
Inferences (métricas anti–security theater; mide eficacia, no actividad):
- Time-to-remediate (TTR) por severidad y por señal: KEV vs EPSS alto vs resto.
- % de builds/deploys bloqueados por policy, y de esos, % revertidos por “falso positivo” (o mala regla).
- Ratio de excepciones: creadas vs expiradas vs renovadas; “edad” promedio de excepción; % excepciones sin plan de salida.
- Break-glass rate: # eventos/mes, duración promedio, % con post-mortem cerrado en 48h, % repetidos por misma causa.
- Coverage real: % artefactos en prod con firma válida; % con SBOM adjunto; % con provenance verificable (si aplica).
- “Exploit-driven closure”: % de KEV cerradas dentro de SLA; “backlog KEV” en días.
- Noise control: vulnerabilidades “reabiertas” por upgrades parciales; duplicados por toolchain; CVEs sin asset mapping.

## Operational checklist
Facts (Cosign): La verificación de firmas y transparencia permite automatizar checks de integridad antes de ejecutar artefactos. [web:12]  
Facts (SLSA v1.0): Exigir provenance y autenticidad (L1/L2) habilita políticas verificables downstream. [web:19]  
Inferences (paso a paso):
- Definir taxonomía: severidad (Critical/High/Med/Low) + señales (KEV, EPSS umbral, exposición, datos).
- Implementar SLAs como código: reglas que setean due-date y “stop-ship” automáticamente según señales.
- Estándar de excepción: plantilla obligatoria + TTL + aprobadores + evidencia + plan de remediación.
- Break-glass: runbook, roles, logging/alerting, TTL por defecto, revisión obligatoria post-evento.
- Gates por etapa:
  - PR: fast checks + stop-ship mínimo.
  - Build: SBOM + SCA + firma + policy evaluation; bloquear solo con reglas objetivas.
  - Deploy: verificación de firma (y opcional provenance) + allowlist de identidades/firmantes.
- Métricas: dashboard mensual con TTR, falsos positivos, overrides, backlog KEV, cobertura de firma/SBOM.
- Revisión trimestral: endurecer umbrales (por ejemplo, bajar tolerancia EPSS en internet-facing) basado en métricas, no en percepción.

## Anti-patterns
Facts (2026-01): EPSS como probabilidad puede “dampening” si se comunica mal; necesitas percentiles/umbrales para no trivializar riesgo. [web:18]  
Facts (2026-02): Un rollout recomendado es iniciar en modo observación y luego pasar a enforcement para reducir fricción. [web:9]  
Inferences (security theater típico):
- “Bloquear por CVSS alto” sin considerar explotación (KEV/EPSS) ni exposición → genera fricción y bypass.
- “Cero excepciones” en papel → en la práctica se vuelve bypass informal (peor).
- Gates idénticos en PR/build/deploy → tiempos lentos y equipos deshabilitando seguridad.
- Métricas de volumen (tickets creados, scans corridos) sin medir TTR, falsos positivos, y overrides.
- Firmar artefactos “porque sí” pero sin enforcement en deploy (nadie verifica, no cambia el riesgo).

## Diagnostic questions
- ¿Qué condiciones exactas disparan un “stop-ship” hoy (KEV, EPSS, exposición, datos), y están codificadas?
- ¿Cuál es el SLA real (p50/p90) para KEV vs EPSS alto, y cuántos incumplimientos aceptas?
- ¿Cuántas excepciones están expiradas pero “siguen vivas” en prod (deuda oculta)?
- ¿Qué porcentaje de bloqueos fueron falsos positivos o reglas mal calibradas el último mes?
- ¿Cuántos break-glass ocurrieron y cuántos tuvieron post-mortem con acción correctiva cerrada?
- ¿Qué porcentaje de artefactos en producción tienen firma válida y verificada en deploy?
- ¿Puedes trazar de CVE → componente SBOM → artefacto firmado → deployment en prod en minutos?

## Sources (o referencia a SOURCES.md)
Ver SOURCES.md (entradas sugeridas al final de este output). [page:0][web:19][web:18][web:17][web:12][web:9][web:7]

## Key takeaways for PM practice
- Prioriza por explotación (KEV) y probabilidad (EPSS) antes que por severidad “de papel”.
- Haz gates progresivos: PR rápido, build exigente, deploy estricto con firmas (y opcional provenance).
- Excepciones y break-glass son parte del producto operativo: TTL, auditabilidad y plan de salida.
- Mide eficacia: TTR, falsos positivos, overrides, cobertura de firma/SBOM y cierre de KEV dentro de SLA.
- Endurece políticas por datos trimestrales, no por presión o incidentes aislados.
```

```markdown
# SOURCES.md (additions — sin duplicados)

- NIST. “Secure Software Development Framework (SSDF) Version 1.1 (SP 800-218).” Published 2022-02-03. https://csrc.nist.gov/pubs/sp/800/218/final  [page:0]
- OpenSSF / SLSA. “SLSA v1.0 — Security levels.” (Spec v1.0). https://slsa.dev/spec/v1.0/levels  [web:19]
- FIRST. “Understanding EPSS Probabilities and Percentiles.” Published 2026-01-08. https://www.first.org/epss/articles/prob_percentile_bins  [web:18]
- NIST NVD. “Known Exploited Vulnerabilities” (nota sobre integración con catálogo KEV y recomendación de priorización). Published 2021-12-31. https://nvd.nist.gov/general/news/cisa-exploit-catalog  [web:17]
- Sigstore. “cosign (GitHub repository) — code signing and transparency.” https://github.com/sigstore/cosign  [web:12]
- Aikido. “NIST SSDF (SP 800-218) Secure Software Development Explained” (incluye ejemplo de SLAs y uso de EPSS en RV.2). Published 2026-01-04. https://www.aikido.dev/learn/compliance/compliance-frameworks/nist-ssdf  [web:7]
- OneUptime. “How to Set Up Sigstore Policy Controller for Kubernetes Image Verification” (recomienda iniciar con warning mode y rollout gradual). Published 2026-02-08. https://oneuptime.com/blog/post/2026-02-09-sigstore-policy-controller-image-verification/view  [web:9]
```

<span style="display:none">[^1][^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^2][^20][^21][^22][^23][^24][^25][^26][^3][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: pasted-text.txt

[^2]: https://www.sentinelone.com/es/cybersecurity-101/cybersecurity/software-bill-of-materials-sbom/

[^3]: https://www.wiz.io/es-es/academy/application-security/software-bill-of-material-sbom

[^4]: https://es-la.tenable.com/source/vulnerability-management

[^5]: https://www.penligent.ai/hackinglabs/es/cve-2026-20805-poc-analysis-dwm-information-disclosure-as-the-key-to-bypassing-aslr/

[^6]: https://www.blacklock.io/es/post/guide-to-sbom-what-it-is-and-why-it-matters

[^7]: https://www.aikido.dev/learn/compliance/compliance-frameworks/nist-ssdf

[^8]: https://www.n-able.com/blog/vulnerability-prioritization

[^9]: https://oneuptime.com/blog/post/2026-02-09-sigstore-policy-controller-image-verification/view

[^10]: https://scribesecurity.com/use-cases/ssdf-slsa-compliance/

[^11]: https://www.netrise.io/xiot-security-blog/using-epss-to-modernize-vulnerability-prioritization

[^12]: https://github.com/sigstore/cosign

[^13]: https://csrc.nist.gov/pubs/sp/800/218/final

[^14]: https://www.edgescan.com/how-edgescans-exf-solves-vulnerability-prioritization-with-epss-and-cisa-kev/

[^15]: https://www.youtube.com/watch?v=q0Kh5-94Vcw

[^16]: https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-218.pdf

[^17]: https://nvd.nist.gov/general/news/cisa-exploit-catalog

[^18]: https://www.first.org/epss/articles/prob_percentile_bins

[^19]: https://slsa.dev/spec/v1.0/levels

[^20]: https://www.cvedetails.com

[^21]: https://www.tenable.com/blog/epss-shows-strong-performance-in-predicting-exploits-says-study-from-cyentia-and-first

[^22]: https://jfrog.com/learn/grc/slsa-framework/

[^23]: https://nvlpubs.nist.gov/nistpubs/cswp/nist.cswp.41.pdf

[^24]: https://slsa.dev/spec/v1.0/requirements

[^25]: https://www.indusface.com/learning/exploit-prediction-scoring-system-epss/

[^26]: https://slsa.dev/spec/v1.0/provenance

