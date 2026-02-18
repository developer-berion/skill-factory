<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_20 — Certs/Education Signals 2024–2026 (CI/CD, SRE, Platform, Security)

## Executive summary (10–15 líneas)

**Facts:** Entre 2024–2026, las credenciales con “uso real” para CI/CD/SRE/Platform/Security se concentran en (1) cloud DevOps (Google/Microsoft), (2) Kubernetes hands‑on (CNCF/Linux Foundation), (3) IaC (HashiCorp Terraform), y (4) seguridad de SDLC/supply chain (GitHub Advanced Security, AWS Security Specialty).[^1][^2][^3][^4][^5][^6]
**Facts:** En Kubernetes (CKA/CKAD/CKS) hubo un cambio relevante de señal: actualmente son válidas por 2 años, con nota explícita de que CKA/CKAD logradas antes del 01‑Abr‑2024 fueron válidas por 3 años.[^1]
**Facts:** Microsoft DevOps Engineer Expert (AZ‑400) sigue vigente, con prerequisito formal de tener Azure Administrator Associate o Azure Developer Associate, y su versión en inglés fue actualizada el 26‑Jul‑2024.[^2]
**Facts:** Google Professional Cloud DevOps Engineer explicita CI/CD + SRE + observability como parte de lo evaluado.[^4]
**Facts:** GitHub Actions y GitHub Advanced Security (GHAS) se consolidan como credenciales directas de “pipeline + enterprise scale” y “security en el SDLC”, con GHAS indicando validez de 2 años.[^7][^3]
**Inferences:** Como señal comercial/operativa, prioriza credenciales **performance-based** (ej. CKA) para roles de plataforma, y credenciales orientadas a control de riesgo (GHAS/AWS Security) para reducir fricción con compliance y auditorías.
**Inferences:** Para enterprise, el ROI aparece cuando la credencial se “amarró” a prácticas internas (plantillas, políticas, runbooks, control de cambios) y no a estudiar por estudiar.

***

## Definitions and why it matters

**Facts:** Una credencial/certificación es una validación formal (examen) de habilidades/competencias, normalmente con vigencia/renovación definida por el proveedor (p. ej., 2 años en varias rutas actuales).[^3][^5][^1]
**Inferences:** En B2B enterprise, la certificación importa como **señal**: reduce riesgo percibido (capacidad de ejecución), acelera onboarding de proveedores/talento, y ayuda a estandarizar lenguaje (CI/CD, SRE, IaC, security).
**Inferences:** La “reputación y uso real” se detecta cuando la credencial está vinculada a herramientas dominantes (Kubernetes, Terraform, GitHub, cloud hyperscalers) y a tareas diarias (pipelines, incident response, observability, policy).

***

## Principles and best practices (con citas por sección + fecha)

### 1) Prioriza señales que validen ejecución (hands‑on)

**Facts (Feb-2026):** CKA se describe como examen online, proctored y performance‑based, resolviendo múltiples tareas desde línea de comando en Kubernetes.[^8]
**Inferences:** Para Platform/SRE, esta señal suele ser más fuerte que exámenes solo teóricos cuando tu objetivo es bajar fallos por cambios y dependencia de “héroes”.

### 2) Trata vigencia/renovación como parte del costo total

**Facts (Feb-2026):** CKA/CKAD/CKS son válidas por 2 años, con la nota de transición para CKA/CKAD logradas antes del 01‑Abr‑2024 (3 años).[^1]
**Facts (Dec-2024):** Terraform Associate (HashiCorp) muestra expiración del credential a 2 años.[^5][^9]
**Facts (Jun-2025):** GitHub Advanced Security indica que, una vez lograda, la certificación será válida por 2 años.[^3]
**Inferences:** Si tu rotación es alta o tu equipo vive en “modo fuego”, credenciales de 2 años pueden convertirse en carga; decide si renuevas por rol crítico o por célula (champions).

### 3) Para CI/CD enterprise, evalúa “scale + governance”

**Facts (Feb-2025 / Jul-2025):** DevOps Engineer Expert (AZ‑400) incluye tareas como diseñar/implementar source control, build \& release pipelines, plan de security \& compliance, e instrumentation strategy; además requiere una certificación prerequisito (Azure Administrator Associate o Azure Developer Associate).[^2]
**Facts (Feb-2026):** GitHub Actions certifica automatización de workflows, creación/mantenimiento de workflows y actions, y administración de GitHub Actions “at scale” para orgs/enterprises.[^7]
**Inferences:** En entornos regulados, “gobernanza del pipeline” (aprobaciones, runners, secretos, permisos, auditoría) vale más que saber escribir YAML rápido.

### 4) Para security/supply chain, busca credenciales que hablen de SDLC

**Facts (Jun-2025):** GHAS evalúa features y configuración de secret scanning, dependency management, code scanning y CodeQL, e incluye prácticas y configuración en GitHub Enterprise.[^3]
**Facts (Sep-2024):** AWS Certified Security – Specialty (SCS‑C03) incluye dominios como Detection, Incident Response, Infrastructure Security, IAM, Data Protection, y “Security Foundations and Governance”, y menciona “managing software supply chain risks” dentro del conocimiento recomendado.[^10]
**Inferences:** Si vendes/operas para enterprise, esto se traduce en menos bloqueos por auditoría y menos “excepciones” manuales en releases.

### 5) Observability como parte del rol (no como tool‑badge)

**Facts (Feb-2026):** Google Professional Cloud DevOps Engineer explicita “implement observability practices and troubleshoot issues” como habilidad evaluada, junto con CI/CD y prácticas SRE.[^4]
**Inferences:** En la práctica, observability útil = SLO/SLI + alerting accionable + postmortems; evita credenciales que no te obliguen a aterrizarlo en operación.

***

## Map 2024–2026 (credenciales con reputación/uso real)

> Nota: solo se incluyen credenciales con evidencia citada en fuentes oficiales/proveedor en este KB.


| Credencial | Qué valida realmente (skills) | Prerequisitos (formales o esperados) | Señales / limitaciones | Cuándo **sí** vale la pena | Cuándo **no** vale la pena |
| :-- | :-- | :-- | :-- | :-- | :-- |
| CKA (Certified Kubernetes Administrator) | Administración de Kubernetes en examen performance‑based (tareas prácticas desde CLI). [^8] | No se listan prerequisitos formales aquí; la señal viene del carácter hands‑on del examen. [^8] | **Limitación:** validez actual 2 años (con excepción histórica para CKA logradas antes del 01‑Abr‑2024). [^1] | Cuando operas clusters o tu plataforma depende de K8s y necesitas prueba de ejecución real. [^8] | Si tu operación no toca Kubernetes o es “managed-only” y no administras nada (señal puede ser sobre‑kill). |
| CKAD / CKS (CNCF/Linux Foundation) | Señal de competencias en el ecosistema Kubernetes (la FAQ agrupa CKA/CKAD/CKS en vigencia/renovación). [^1] | No detallado aquí; sí consta la regla de renovación por re‑tomar examen. [^1] | **Limitación:** vigencia 2 años y requiere renovación (retake) antes de expirar. [^1] | Cuando necesitas estandarizar skill‑baseline K8s y mantenerlo “fresco” por ciclos cortos. [^1] | Si no tienes tiempo/capacidad de renovar cada 2 años o si el rol no usa K8s. |
| Microsoft Certified: DevOps Engineer Expert (AZ‑400) | Diseño/implementación de procesos, source control, build/release pipelines, plan de security \& compliance, e instrumentation strategy. [^2] | Requiere Azure Administrator Associate o Azure Developer Associate + AZ‑400 para obtener la certificación. [^2] | Señal fuerte en organizaciones Microsoft (Azure DevOps/GitHub); además se actualiza (en inglés, update 26‑Jul‑2024). [^2] | Si tu delivery está en Azure/GitHub y vendes confiabilidad + control (compliance, trazabilidad, instrumentación). [^2] | Si tu stack no es Microsoft/Azure y solo buscas “CI/CD genérico” (puede no transferir 1:1). |
| Exam AZ‑400 (examen) | Implementar DevOps con entrega continua de valor, incluyendo seguridad, integración, testing, delivery/deployment, monitoring y feedback. [^11] | Se espera experiencia administrando y desarrollando en Azure, y usando GitHub y Azure DevOps. [^11] | Señal: cubre coordinación cross‑functional (dev, SRE, security) además de pipelines. [^11] | Cuando necesitas formar “puentes” entre dev y ops en enterprise con herramientas Microsoft. [^11] | Si tu necesidad es puramente SRE infra (sin ownership de pipelines) y el rol no tocará Azure/GitHub. |
| Google Professional Cloud DevOps Engineer | Bootstrap org en GCP, aplicar prácticas SRE, construir CI/CD (incl. continuous testing) y observability/troubleshooting; optimización performance/costo. [^4] | No se explicita prerequisito formal en la página; define el rol y alcance del examen. [^4] | Señal fuerte si tu operación corre en GCP; incluye observability como parte del rol (no accesorio). [^4] | Si tus equipos operan en GCP y quieres elevar madurez de CI/CD + SRE + observability. [^4] | Si estás 100% fuera de GCP y buscas una señal neutral (podría no ser la mejor inversión). |
| GitHub Actions (certificación) | Automatizar workflows con GitHub Actions: crear y mantener workflows/actions, administrar Actions “at scale”, y asegurar automatización eficiente. [^7] | Se describe para perfiles con experiencia intermedia en GitHub Actions. [^7] | Señal muy “hands-on de pipeline”, pero centrada en GitHub Actions (no cubre todo el SDLC fuera de GitHub). [^7] | Si tu CI/CD está (o migrará) a GitHub y necesitas consistencia, velocidad y control por org. [^7] | Si tu CI/CD vive en otra plataforma y no planeas estandarizar en GitHub Actions. |
| GitHub Advanced Security (GHAS) | Seguridad del SDLC en GitHub: secret scanning, dependencias, code scanning y CodeQL; mejores prácticas y configuración en GitHub Enterprise. [^3] | Diseñado para profesionales con experiencia en desarrollo y seguridad, con práctica asegurando workflows. [^3] | Validez indicada de 2 años; señal fuerte para supply chain y auditoría técnica dentro de GitHub. [^3] | Si vendes/operas software en enterprise y te piden evidencias de scanning, gestión de dependencias, y hardening del pipeline. [^3] | Si tu repo/pipeline no está en GitHub o tu organización no habilitará GHAS (señal no se puede “ejercer”). |
| HashiCorp Certified: Terraform Associate | Fundamentos de Terraform (IaC), workflow (plan/apply/destroy), state, módulos, y nociones de HCP Terraform; examen 1 hora, multiple choice, expiración 2 años. [^5] | No exige prerequisito formal; HashiCorp indica que experiencia profesional es recomendada y se puede preparar con práctica en demo setup. [^5] | Señal buena de baseline IaC, pero no prueba “producción” por sí sola (multiple choice). [^5] | Si estás estandarizando IaC y necesitas un baseline común para cloud/platform/ops. [^5] | Si tu problema real es arquitectura/seguridad avanzada de plataforma: la Associate puede quedarse corta. |
| HashiCorp Terraform Authoring \& Operations Professional | Habilidades avanzadas “production-level” en Terraform, incluyendo módulo/authoring, workflows, remote state, policy/governance en HCP Terraform; expiración 2 años. [^5] | Orientada a personas con experiencia avanzada en producción; la propia descripción exige demostrar habilidades profesionales. [^5] | Señal más fuerte para Platform/IaC por formato más intensivo (lab-based + multiple choice). [^5] | Cuando necesitas demostrar capacidad real de escalar Terraform con colaboración, governance y módulos reutilizables. [^5] | Si tu organización aún no tiene práctica en Terraform (primero necesitas base y adopción). |
| AWS Certified Security – Specialty (SCS‑C03) | Detección, incident response, infraestructura, IAM, data protection, governance; incluye supply chain risk dentro del conocimiento recomendado; blueprint con pesos por dominio. [^10] | AWS lo posiciona para personas con experiencia (menciona 5 años de experiencia en IT security, entre otros criterios de audiencia). [^6] | Señal fuerte para seguridad cloud en AWS; puede ser amplia y exigir experiencia real (no “entry”). [^6] | Si tu operación corre en AWS y necesitas reforzar controles, auditoría, IR y estrategia de seguridad en cloud. [^10][^6] | Si tu equipo no opera AWS o estás buscando una credencial específica de CI/CD (esta es seguridad cloud, no “pipelines-only”). |


***

## Examples (aplicado a CRM enterprise)

**Facts:** AZ‑400 incluye “develop a security and compliance plan” e “implement an instrumentation strategy”, lo cual calza con necesidades típicas de CRM enterprise (cumplimiento + trazabilidad + monitoreo).[^2]
**Inferences (caso práctico):** Si estás implementando un CRM enterprise con integraciones (ERP, pagos, data warehouse), arma una “matriz de señales” por rol:

- Platform Lead: CKA + Terraform (Associate o Professional según seniority) para demostrar operación K8s + IaC.
- DevOps Lead (Microsoft shop): DevOps Engineer Expert (AZ‑400) para gobernar pipelines, compliance e instrumentación.
- AppSec/DevSecOps: GHAS + (si estás en AWS) AWS Security Specialty para supply chain + postura cloud.

**Inferences (objeción real):** “¿Y si el proveedor viene certificado pero no entrega?” → exige evidencia operativa: repos con plantillas, políticas de branching, pipeline con aprobaciones, y runbooks; la credencial solo abre la puerta, no cierra la venta.

***

## Metrics / success signals

**Facts:** Google Professional Cloud DevOps Engineer explícitamente cubre CI/CD, SRE y observability/troubleshooting como habilidades evaluadas.[^4]
**Inferences (señales medibles en operación):**

- Lead time de cambio y frecuencia de despliegue (si sube sin aumentar incidentes, la práctica está madurando).
- Change failure rate y MTTR (si bajan, tu “SRE + observability” está funcionando).
- % de pipelines con controles de seguridad habilitados (secret scanning/dependency/code scanning) cuando usas GHAS.

***

## Operational checklist

**Facts:** GHAS cubre secret scanning, dependency management, code scanning y CodeQL, con foco también en GitHub Enterprise.[^3]
**Inferences (checklist de decisión 30–60 min):**

- Define el objetivo: ¿velocidad CI/CD, confiabilidad SRE, plataforma K8s, o control de riesgo security/supply chain?
- Elige 1 credencial “core” por rol y 1 “adjunta” solo si impacta una métrica operativa.
- Verifica vigencia/renovación (2 años en varias rutas) y planifica presupuesto/tiempo de recertificación.
- Exige “prueba de transferencia”: un repo demo interno con pipeline, policies, observability mínima y checklist de hardening.
- Decide política: opción segura (solo roles críticos), opción agresiva (cert‑baseline para todo el equipo + champions).

***

## Anti-patterns

**Facts:** Linux Foundation indica que CKA/CKAD/CKS requieren renovación vía retomar el examen y tienen vigencia definida.[^1]
**Inferences (errores típicos):**

- Comprar certificaciones como “marketing” sin cambiar prácticas (no baja incidentes ni acelera delivery).
- Certificar sin plataforma estándar (cada squad con su CI/CD) → la credencial no “compone” en operación.
- No planificar renovaciones (credenciales expiran y se pierde la señal justo cuando más la necesitas).
- Confundir tool‑skill con diseño de sistema (ej. saber GitHub Actions sin governance, permisos y runners).

***

## Diagnostic questions

**Facts:** AZ‑400 incluye diseño de pipelines, security/compliance e instrumentación como parte de lo medido.[^2]
**Inferences (preguntas para decidir inversión):**

- ¿Qué fricción estás comprando con esta credencial: velocidad, margen, o reducción de riesgo?
- ¿Qué parte del flujo se cae hoy: build/release, infraestructura, incident response, o seguridad de dependencias?
- ¿Tu stack es GitHub/Azure, GCP, AWS, o híbrido? (elige señales alineadas al stack real).
- ¿Puedes convertir la credencial en estándar operativo (plantillas, policy, runbooks), o quedará en CV?

***

## Sources (o referencia a SOURCES.md)

- Linux Foundation — Certified Kubernetes Administrator (CKA).[^8]
- Linux Foundation Docs — FAQ CKA/CKAD/CKS (vigencia/renovación; nota cambio Abril 2024).[^1]
- CNCF Blog — CKA valid 3 years (histórico para contexto).[^12]
- Microsoft Learn — Microsoft Certified: DevOps Engineer Expert (prereqs + update 26‑Jul‑2024 + skills).[^2]
- Microsoft Learn — Exam AZ‑400 role/overview.[^11]
- Google Cloud — Professional Cloud DevOps Engineer (skills evaluadas).[^4]
- Microsoft Learn — GitHub Actions certification overview.[^7]
- Microsoft Learn — GitHub Advanced Security certification (dominios + validez 2 años).[^3]
- HashiCorp Developer — Infrastructure Automation Certifications (Terraform Associate/Professional, objetivos + expiración 2 años).[^5]
- HashiCorp Developer — Certifications (validez 2 años, reglas generales).[^9]
- AWS Documentation — Exam guide SCS‑C03 (dominios + supply chain risk en conocimiento recomendado).[^10]
- AWS — AWS Certified Security – Specialty (audiencia/experiencia).[^6]


### Añadidos propuestos a `SOURCES.md` (sin duplicados)

- https://docs.linuxfoundation.org/tc-docs/certification/faq-cka-ckad-cks
- https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/
- https://learn.microsoft.com/en-us/credentials/certifications/devops-engineer/
- https://learn.microsoft.com/en-us/credentials/certifications/exams/az-400/
- https://cloud.google.com/learn/certification/cloud-devops-engineer
- https://learn.microsoft.com/en-us/credentials/certifications/github-actions/
- https://learn.microsoft.com/en-us/credentials/certifications/github-advanced-security/
- https://developer.hashicorp.com/certifications/infrastructure-automation
- https://developer.hashicorp.com/certifications
- https://docs.aws.amazon.com/aws-certification/latest/examguides/security-specialty-03.html
- https://aws.amazon.com/certification/certified-security-specialty/

***

## Key takeaways for PM practice

- Usa certificaciones como “señales de ejecución” y “reducción de riesgo”, no como vanity metrics.
- Optimiza por stack real (GitHub/Azure vs GCP vs AWS) y por fricción dominante (delivery vs seguridad vs operación).
- Trata la vigencia (2 años en varias rutas) como parte del diseño operativo: presupuesto, tiempo y champions.
- Exige transferencia a artefactos operativos: plantillas, policies, pipelines y runbooks, o no hay ROI.
<span style="display:none">[^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31][^32][^33][^34][^35][^36][^37][^38][^39][^40][^41][^42][^43][^44][^45][^46]</span>

<div align="center">⁂</div>

[^1]: https://docs.linuxfoundation.org/tc-docs/certification/faq-cka-ckad-cks

[^2]: https://learn.microsoft.com/en-us/credentials/certifications/devops-engineer/

[^3]: https://learn.microsoft.com/en-us/credentials/certifications/github-advanced-security/

[^4]: https://cloud.google.com/learn/certification/cloud-devops-engineer

[^5]: https://developer.hashicorp.com/certifications/infrastructure-automation

[^6]: https://aws.amazon.com/certification/certified-security-specialty/

[^7]: https://learn.microsoft.com/en-us/credentials/certifications/github-actions/

[^8]: https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/

[^9]: https://developer.hashicorp.com/certifications

[^10]: https://docs.aws.amazon.com/aws-certification/latest/examguides/security-specialty-03.html

[^11]: https://learn.microsoft.com/en-us/credentials/certifications/exams/az-400/

[^12]: https://www.cncf.io/blog/2019/05/28/certified-kubernetes-administrator-cka-certification-is-now-valid-for-3-years/

[^13]: pasted-text.txt

[^14]: https://www.cncf.io/training/certification/cka/

[^15]: https://kodekloud.com/learning-path/cka

[^16]: https://www.globalknowledge.com/us-en/training/certification-prep/brands/aws/section/operations/aws-certified-devops-engineer-professional/

[^17]: https://www.rigutins.dev/blog/github-actions-exam-study-guide-resources

[^18]: https://www.learnquest.com/course-detail-v3.aspx?cnum=LNX-CKA-CKS-GB

[^19]: https://www.datacamp.com/blog/aws-certified-devops-engineer-guide

[^20]: https://flashgenius.net/blog-article/your-quest-for-kubernetes-mastery-a-cka-certification-guide-no-boring-bits-promise

[^21]: https://clarusway.com/aws-devops-engineer-professional-certification-guide-tips/

[^22]: https://www.youtube.com/watch?v=Tz7FsunBbfQ

[^23]: https://www.cncf.io/wp-content/uploads/2020/08/rx-m-webinar-everything-you-need-to-know-about-the-cka-ckad.pdf

[^24]: https://www.jeffersonfrank.com/insights/aws-devops-engineer-certification-guide/

[^25]: https://learn.microsoft.com/en-us/answers/questions/1688946/is-there-any-mandatory-prerequisites-to-achieve-az

[^26]: https://learn.microsoft.com/en-us/answers/questions/525066/prerequisites-of-azure-devops-engineer-expert

[^27]: https://learn.microsoft.com/en-us/answers/questions/2259587/is-it-mandatory-to-complete-prerequisite-certifica

[^28]: https://certificationpractice.com/exam-overviews/google-cloud-professional-cloud-devops-engineer-quick-facts

[^29]: https://www.whizlabs.com/microsoft-azure-certification-az-400/

[^30]: https://www.linkedin.com/learning/github-advanced-security-cert-prep-by-microsoft-press

[^31]: https://learn.microsoft.com/en-ie/answers/questions/5750859/about-400-certification

[^32]: https://www.test-king.com/blog/complete-study-guide-for-the-google-professional-cloud-devops-engineer-exam/

[^33]: https://learn.microsoft.com/en-us/training/paths/github-advanced-security/

[^34]: https://www.netcomlearning.com/microsoft-certified-azure-devops-engineer-expert/local/certification/microsoft/seattle-wa/us

[^35]: https://www.skills.google/paths/20

[^36]: https://flashgenius.net/blog-article/hashicorp-certified-terraform-associate-004-the-ultimate-2026-exam-guide

[^37]: https://www.whizlabs.com/blog/hashicorp-terraform-associate-004-prep-guide/

[^38]: https://notes.kodekloud.com/docs/Terraform-Associate-Certification-HashiCorp-Certified/Course-Introduction/Certification-Details/page

[^39]: https://www.sendowl.com/s/grafana-practice-tests/certified-grafana-associate-5-practice-tests-by-udemy/

[^40]: https://cloudfluently.com/blog/terraform-associate-004-exam-guide-everything-you-need-to-know

[^41]: https://www.thedataops.org/grafana-training-course-official-master-certification-program/

[^42]: https://hashicorp-certifications.zendesk.com/hc/en-us/articles/26234761626125-Exam-appointment-rules-and-requirements

[^43]: https://www.linkedin.com/pulse/how-i-passed-aws-certified-security-specialty-exam-scs-c02-kemal--nvyec

[^44]: https://mindmajix.com/grafana-training

[^45]: https://ipspecialist.net/courses/terraform-associate-certification-second-edition/

[^46]: https://www.reddit.com/r/AWSCertifications/comments/1gn0ndi/would_i_be_able_to_study_for_aws_security/

