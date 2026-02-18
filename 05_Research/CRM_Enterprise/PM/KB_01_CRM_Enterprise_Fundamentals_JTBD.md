# KB_01 — CRM Enterprise: Fundamentals & JTBD

***

## Executive Summary

CRM (Customer Relationship Management) enterprise es un software estratégico que centraliza datos, procesos y relaciones con clientes a lo largo de todo su ciclo de vida — desde la primera interacción hasta la renovación y expansión. A diferencia de un CRM para PYME, un CRM enterprise cubre **todas** las operaciones customer-facing: ventas, marketing, servicio, commerce e incluso workflows específicos por industria, entregando una vista 360° del cliente. Sus capacidades core incluyen automatización de procesos, analítica con IA, control de acceso por roles, integraciones con ERP/CPQ y personalización no-code/low-code.[^1][^2]

En un contexto B2B mayorista (como Alana Tours), el CRM no es un "nice to have" sino la **infraestructura operativa** que conecta al SDR que prospecta agencias, al AE que cierra acuerdos comerciales, al CS que retiene cuentas y al Admin que mantiene el sistema limpio y funcional. Cada rol tiene un Job-to-be-Done (JTBD) distinto dentro del CRM, y cuando se entiende y se configura correctamente, el resultado es mayor velocidad de cierre, datos confiables para decisiones y recurrencia real del cliente B2B.

Este documento define los fundamentos, mapea el lifecycle completo, desglosa JTBD por rol, presenta flujos típicos, métricas de éxito y los anti-patrones más comunes que sabotean implementaciones enterprise.

**Fact:** La definición y módulos son estándar de industria documentados por Salesforce, Oracle/NetSuite, Creatio y Gartner.  
**Inference:** La aplicación específica a turismo B2B mayorista es una extrapolación razonable de los frameworks genéricos.

***

## Definitions and Why It Matters

### ¿Qué es CRM Enterprise?

CRM Enterprise es una solución de software que proporciona un enfoque estratégico para gestionar interacciones con clientes dentro de organizaciones de escala significativa. Integra tecnologías, procesos y estrategias para optimizar el ciclo de vida completo del cliente. A nivel funcional, permite almacenar información de contacto de clientes y prospectos, identificar oportunidades de venta, registrar issues de servicio y gestionar campañas de marketing — todo desde un solo lugar accesible por los stakeholders relevantes.[^3][^4]

### Tipos de CRM

| Tipo | Foco principal | Ejemplo de uso |
|------|---------------|----------------|
| **Operacional** | Automatizar ventas, marketing y servicio | Pipeline tracking, email automation, routing de tickets [^1] |
| **Analítico** | Data analysis para insights | Reportes de conversión, forecasting, segmentación [^3] |
| **Colaborativo** | Compartir información cross-departamento | Vista unificada cliente entre ventas y servicio [^3] |
| **Estratégico** | Cliente al centro de la estrategia de negocio | Customer-centricity a nivel organizacional [^3] |

**Fact:** Estos cuatro tipos están documentados por Salesforce y NetSuite como categorías estándar de la industria.[^1][^3]

### ¿Por qué importa en B2B?

En B2B, donde el cliente es una empresa (la agencia de viajes, no el pasajero), el CRM es el sistema de registro (system of record) que:

- Centraliza el historial de interacciones para que cualquier miembro del equipo pueda continuar una conversación sin perder contexto.[^5]
- Estandariza el proceso de ventas con etapas claras para evitar que cada vendedor opere de forma distinta.[^5]
- Habilita decisiones basadas en datos reales: tasas de conversión, actividades que generan cierre, valor del pipeline.[^5]
- Automatiza tareas administrativas que quitan tiempo de venta activa.[^5]

***

## Modules: Sales / Marketing / Service

### Sales Module (Módulo de Ventas)

El módulo de ventas es el core del CRM para equipos comerciales. Gestiona todo el pipeline desde la prospección hasta el cierre.[^2][^6]

**Capacidades clave:**

- **Pipeline & Opportunity Management:** Etapas definidas (Prospecting → Qualification → Needs Analysis → Proposal → Negotiation → Closed Won/Lost) con criterios de entrada/salida por stage.[^6][^7]
- **Contact & Account Management:** Vista 360° del cliente con historial de interacciones, deals y documentos.[^1]
- **Forecasting & Analytics:** Predicción de ingresos basada en pipeline, stage probability y tendencias históricas.[^2]
- **Task & Activity Management:** Asignación, priorización y tracking de tareas por deal y por rep.[^2]
- **Contract & Document Management:** Almacenamiento y control de versiones de propuestas, contratos y documentos de venta.[^2]
- **Automatización:** Triggers automáticos para follow-ups, reminders por stage, alertas de deals estancados y progresión automática de stages basada en actividades completadas.[^6]

**Inference:** En un mayorista de turismo B2B, el "opportunity" es el acuerdo comercial con la agencia (contrato de crédito, condiciones, markup), no la reserva individual del pasajero.

### Marketing Module (Módulo de Marketing)

El módulo de marketing se enfoca en generación de demanda, nurturing de leads y ejecución de campañas cross-channel.[^8][^2]

**Capacidades clave:**

- **Lead Scoring:** Asignación de valores numéricos a leads basados en demografía y engagement para identificar prospectos de alto potencial.[^9][^8]
- **Lead Nurturing Automatizado:** Secuencias de contenido personalizadas activadas por comportamiento del lead (descarga un recurso, visita pricing, se registra a webinar).[^10][^8]
- **Segmentación:** Agrupación de leads por traits, comportamiento o intereses para entregar contenido relevante.[^8]
- **Multichannel Engagement:** Coordinación de comunicaciones automatizadas por email, SMS, social media y retargeting.[^8]
- **Campaign Management:** Programas de marketing multi-step donde eventos disparan acciones automáticas.[^11]
- **Analytics & A/B Testing:** Monitoreo de métricas clave (CTR, open rates) y tests automatizados para optimización continua.[^8]

**Inference:** Para un mayorista B2B, marketing en CRM no es "branding" — es la máquina que identifica agencias con potencial, las nutre con contenido relevante (destinos, tarifas, promos) y las pasa calificadas al equipo comercial.

### Service Module (Módulo de Servicio)

El módulo de servicio gestiona el soporte post-venta, resolución de problemas y satisfacción del cliente.[^12][^1]

**Capacidades clave:**

- **Case/Ticket Management:** Creación automática de casos desde email, teléfono o portal, con información detallada (tipo de problema, severidad, prioridad, SLA, status).[^13][^12]
- **Routing & Escalation:** Asignación automática de tickets al agente correcto basada en reglas predefinidas y IA; escalación automática de issues críticos.[^14][^12]
- **Knowledge Base:** Acceso rápido a soluciones comunes, FAQs, resoluciones de casos anteriores similares — integrado con el sistema de ticketing.[^12]
- **SLA Management:** Configuración de acuerdos de nivel de servicio con timers y alertas para cumplimiento.[^13]
- **Customer Portal & Self-Service:** Portal donde el cliente puede abrir tickets, consultar status y acceder a la knowledge base.[^13]
- **Timeline & History:** Tracking dinámico de emails, notas, tareas y contacto para establecer una línea de tiempo del caso.[^14]

***

## Lifecycle End-to-End

El customer lifecycle en CRM mapea la relación completa desde el primer contacto hasta la advocacy. Existen diferentes modelos (3, 4, 5, 6 etapas), pero el modelo de 5 etapas es el más aceptado:[^15][^16]

| Etapa | Descripción | Módulo CRM primario | Rol principal |
|-------|-------------|-------------------|---------------|
| **Awareness / Reach** | El prospecto conoce tu marca por marketing o investigación | Marketing | Marketing / SDR |
| **Acquisition** | Primer contacto activo, busca información o soporte | Marketing + Sales | SDR |
| **Conversion** | Completa una compra / firma acuerdo, se convierte en cliente | Sales | AE |
| **Retention** | Se mantiene la relación post-venta para fomentar recurrencia | Service + Sales | CS |
| **Loyalty / Advocacy** | El cliente se convierte en promotor de tu marca | Service + Marketing | CS |

[^16][^17]

**Fact:** Las 5 etapas (Reach, Acquisition, Conversion, Retention, Loyalty) son un framework estándar documentado por Gainsight, Nextiva e Insightly.[^17][^15][^16]

**En B2B mayorista:** El lifecycle se traduce a: una agencia descubre Alana Tours → solicita información → firma acuerdo comercial → opera reservas recurrentes → recomienda a otras agencias. Cada etapa tiene triggers, métricas y acciones específicas en el CRM.

***

## JTBD por Rol (Jobs-to-be-Done)

### SDR (Sales Development Representative)

**Job principal:** "Necesito generar pipeline calificado de forma consistente para que los AEs tengan deals reales que cerrar."

| Dimensión | Detalle |
|-----------|---------|
| **Functional Job** | Identificar, contactar y calificar prospectos usando secuencias estandarizadas |
| **Emotional Job** | Sentir que mi trabajo de prospección tiene impacto medible en revenue |
| **Social Job** | Ser reconocido como generador de pipeline, no como "el que hace llamadas" |

**Hábito CRM non-negotiable:** Trabajar desde una vista priorizada y usar disposiciones estandarizadas en cada touch.[^18]

**Flujo típico en CRM:**
1. Recibe MQL asignado automáticamente por routing rules → se crea tarea automática.[^18]
2. Ejecuta secuencia de contacto (llamada, email, LinkedIn) registrando cada touch.
3. Califica usando criterios estandarizados (BANT, MEDDIC o custom).
4. Si califica → convierte lead en oportunidad y la asigna al AE con notas de contexto.
5. Si no califica → marca disposición y programa re-engagement futuro.

[^19][^18]

### AE (Account Executive)

**Job principal:** "Necesito cerrar deals de forma predecible, manejando todo el ciclo de venta con visibilidad sobre qué deals avanzan y cuáles se estancan."

| Dimensión | Detalle |
|-----------|---------|
| **Functional Job** | Gestionar oportunidades complejas, hacer discovery, presentar propuestas, negociar y cerrar |
| **Emotional Job** | Confianza en que mi pipeline refleja la realidad y puedo forecast con precisión |
| **Social Job** | Ser visto como closer consultivo, no como tomador de pedidos |

**Hábito CRM non-negotiable:** Actualizar stage, close date y next step inmediatamente después de cada reunión crítica.[^18]

**Flujo típico en CRM:**
1. Recibe oportunidad calificada del SDR con contexto completo.
2. Ejecuta discovery call → documenta pain points, stakeholders, timeline, presupuesto.
3. Mueve deal por stages (Qualified → Discovery → Demo/Proposal → Negotiation → Close).
4. En cada stage: registra actividad, actualiza probability, ajusta close date.
5. Genera propuesta/cotización desde el CRM → tracking de apertura y feedback.
6. Cierra Won → handoff a CS con contexto. Cierra Lost → registra motivo para análisis.

[^7][^19][^6]

### CS (Customer Success Manager)

**Job principal:** "Necesito retener y expandir cuentas existentes, asegurando que el cliente obtenga valor y se convierta en recurrente."

| Dimensión | Detalle |
|-----------|---------|
| **Functional Job** | Onboarding, adopción, renovaciones, upsell/cross-sell, resolución de issues |
| **Emotional Job** | Satisfacción de que mis cuentas crecen y no churnan |
| **Social Job** | Ser el trusted advisor del cliente, no "soporte técnico" |

**Flujo típico en CRM:**
1. Recibe handoff del AE con contexto del deal (qué se vendió, expectativas, timeline).
2. Ejecuta onboarding: configura la cuenta, capacita al cliente, establece milestones.
3. Monitorea health score de la cuenta (actividad, tickets, engagement).
4. Pre-renewal: revisa métricas, prepara business review, identifica oportunidades de expansión.
5. Gestiona renovación → cierra o escala issues de riesgo.
6. Identifica oportunidades de advocacy (referrals, case studies, testimonios).

[^19]

### Admin (CRM Administrator)

**Job principal:** "Necesito que el CRM funcione como un reloj: limpio, configurado correctamente, adoptado por los usuarios y alineado con los procesos del negocio."

| Dimensión | Detalle |
|-----------|---------|
| **Functional Job** | Configurar, mantener, integrar y optimizar el sistema CRM |
| **Emotional Job** | Confianza en que el sistema es confiable y los datos son limpios |
| **Social Job** | Ser reconocido como enabler del negocio, no como "el de IT" |

**Responsabilidades core:**

- **System Management:** Monitorear estabilidad, performance, auditorías regulares y updates.[^20]
- **User Administration:** Gestionar cuentas, permisos, roles y profiles.[^21][^20]
- **Data Management:** Validación de imports/exports, deduplicación, reglas de data quality.[^21]
- **Customization:** Crear y gestionar objetos custom, campos, fórmulas, layouts, reportes y dashboards.[^21]
- **Workflow & Automation:** Diseñar workflow rules, validaciones, procesos de aprobación.[^21]
- **Integration Management:** Coordinar integraciones con otros sistemas (ERP, marketing automation, facturación) y troubleshoot issues.[^20]
- **Governance:** Ser el single owner de cambios al sistema — validar business value antes de agregar campos o stages.[^18]

[^22]

***

## Principles and Best Practices

### 1. Diseña el CRM alrededor de tus sales plays, no al revés

Mapea primero tus personas target, triggers, patrones de contacto y criterios de calificación. Luego configura stages y campos requeridos para reflejar esos plays. Cuando cada actividad y status indica "dónde está el comprador" y "qué sigue", el sistema se convierte en workflow engine, no en database pasiva.[^18]

**Fuente:** SalesHive, "CRMs for B2B Sales: Best Practices", diciembre 2025.

### 2. Gobernanza centralizada: un solo dueño de la configuración

Dejar que cada manager y rep cree sus propios stages y campos destruye la confianza en los datos. "Qualified" termina significando algo diferente en cada territorio. La solución: definiciones globales de stages, campos requeridos bloqueados y un único RevOps owner que valida valor de negocio real antes de agregar cualquier cosa.[^18]

**Fuente:** SalesHive, diciembre 2025.

### 3. "Si no está en el CRM, no existe"

Forecasts y pipeline reviews solo deben referenciar datos del CRM — no spreadsheets paralelos ni threads de Slack. Cuando los managers consistentemente coachean desde dashboards del CRM, los reps aprenden rápidamente que datos limpios y updates oportunos son parte del trabajo, no admin opcional.[^18]

**Fuente:** SalesHive, diciembre 2025.

### 4. Involucra al frontline en el diseño

Los mejores SDRs y AEs deben tener voz real en cómo se diseñan layouts, campos y workflows. Un "CRM council" mensual donde reps pueden proponer cambios y eliminar campos no usados mantiene el sistema alineado con la realidad y mejora dramáticamente la adopción.[^18]

**Fuente:** SalesHive, diciembre 2025.

### 5. Procesos antes que tecnología

Organizaciones sin procesos documentados y optimizados antes de implementar CRM luchan para configurar sistemas efectivamente. Los equipos pasan meses debatiendo diseño de procesos durante la implementación en lugar de llegar con requerimientos claros.[^23]

**Fuente:** LinkedIn Pulse, "Why CRM Implementations Fail", enero 2026.

***

## Examples (Aplicado a CRM Enterprise — Contexto Mayorista B2B)

### Flujo 1: Prospección de nueva agencia (SDR → AE)

1. **Trigger:** Marketing identifica agencia activa en destinos que Alana opera (lead scoring automático).
2. **SDR:** Recibe lead en vista priorizada → ejecuta secuencia (email personalizado con destinos relevantes + llamada).
3. **Calificación:** Agencia confirma volumen mínimo, mercados de interés y disposición a abrir cuenta → SDR convierte a oportunidad.
4. **AE:** Recibe opp con notas → programa reunión de discovery → presenta propuesta de condiciones comerciales (markup, crédito, soporte).
5. **Cierre:** Agencia firma acuerdo → AE marca Closed Won → handoff a CS con condiciones pactadas.

### Flujo 2: Retención y expansión de cuenta (CS)

1. **Trigger:** CRM alerta que agencia no ha cotizado en 30 días (health score baja).
2. **CS:** Contacta agencia → identifica que pasaron a cotizar con otro mayorista por un destino específico.
3. **Acción:** CS escala a producto para evaluar competitividad en ese destino → ofrece tarifa especial o bloqueo garantizado.
4. **Resultado:** Agencia retoma operación → CS actualiza health score y registra insight competitivo en CRM.

### Flujo 3: Resolución de incidencia operativa (Service)

1. **Trigger:** Agencia reporta problema con reserva (hotel no confirma) vía email → case se crea automáticamente.
2. **Routing:** Ticket se asigna a agente de operaciones basado en destino y severidad.
3. **Resolución:** Agente contacta proveedor, resuelve o propone alternativa → actualiza case con timeline.
4. **Cierre:** Agencia confirma resolución → case se cierra → SLA se valida automáticamente.

***

## Metrics / Success Signals

### Por módulo

| Módulo | Métricas clave | Signal de éxito |
|--------|---------------|-----------------|
| **Sales** | Pipeline value, win rate, sales cycle length, stage conversion rates, forecast accuracy | Pipeline saludable (3x target), cycle ≤ benchmark, forecast ±10% |
| **Marketing** | MQL volume, MQL→SQL conversion, lead score accuracy, campaign ROI, cost per qualified lead | MQLs consistentes, >25% conversión a SQL, CAC decreciente |
| **Service** | First response time, resolution time, CSAT, ticket volume trends, SLA compliance | SLA >95%, CSAT >4/5, volumen decreciente (signals mejor producto/onboarding) |

### Por rol

| Rol | Métrica primaria | Métrica secundaria |
|-----|-----------------|-------------------|
| **SDR** | SQLs generados / mes | Meetings booked, contact rate, sequence completion rate |
| **AE** | Revenue cerrado / quarter | Win rate, avg deal size, pipeline coverage ratio |
| **CS** | Net Revenue Retention (NRR) | Churn rate, expansion revenue, CSAT, health score distribution |
| **Admin** | Adoption rate (DAU/MAU) | Data quality score, avg fields completed, automation success rate |

***

## Operational Checklist

### Pre-implementación
- [ ] Documentar procesos de venta actuales (as-is) antes de tocar el CRM[^23]
- [ ] Definir métricas de éxito y baselines[^23]
- [ ] Nombrar executive sponsor con autoridad real[^23]
- [ ] Designar un RevOps owner único como gobernante del sistema[^18]
- [ ] Establecer estándares de data quality (formatos, campos obligatorios, reglas de validación)[^24]
- [ ] Mapear integraciones necesarias (ERP, facturación, email, calendario)[^20]

### Implementación
- [ ] Configurar stages del pipeline alineados a los sales plays reales del equipo[^18]
- [ ] Definir criterios de entrada/salida por stage con acciones específicas[^6]
- [ ] Configurar lead scoring basado en criterios reales de calificación[^9]
- [ ] Implementar automations prioritarias: asignación de leads, reminders por stage, alertas de deals estancados[^6]
- [ ] Limpiar y migrar datos con validación pre y post migración[^24]
- [ ] Crear dashboards por rol (SDR, AE, CS, Manager)[^21]

### Post-implementación
- [ ] Establecer "CRM council" mensual con reps del frontline[^18]
- [ ] Implementar "CRM hygiene hour" semanal (30-60 min para limpieza de datos)[^18]
- [ ] Revisar pipeline reports mensualmente para identificar stages problemáticos[^6]
- [ ] Ejecutar plan de change management continuo (no es one-time)[^25]
- [ ] Alimentar insights de CRM de vuelta al ICP y messaging[^18]

***

## Anti-Patterns

### 1. "Frankenstein CRM" — Cada quien crea sus propios campos y stages

**Síntoma:** "Qualified" significa algo diferente en cada territorio. Los dashboards no son confiables. Los managers dejan de mirar reportes.  
**Causa raíz:** Falta de governance centralizada.  
**Fix:** Un único RevOps owner valida business value antes de agregar cualquier campo o stage. Stage definitions globales y bloqueadas.[^18]

### 2. Technology-first thinking — Comprar antes de definir procesos

**Síntoma:** Se selecciona el CRM antes de definir procesos y requerimientos. Se force-fittean las operaciones a las limitaciones del software.  
**Causa raíz:** Se aborda CRM como compra de tecnología, no como transformación de negocio.[^23]
**Fix:** Definir procesos, roles y success criteria ANTES de evaluar plataformas.[^23]

### 3. Automatizar procesos rotos

**Síntoma:** Se automatizan workflows que ya eran ineficientes. La automatización amplifica las deficiencias.  
**Causa raíz:** Process immaturity — no se documentaron ni optimizaron procesos antes del CRM.[^23]
**Fix:** Optimizar el proceso primero en papel/whiteboard, luego automatizar.[^23]

### 4. Ignorar data hygiene

**Síntoma:** Registros duplicados, incompletos o desactualizados. La personalización falla, el outreach se enruta mal, los reps pierden confianza en el sistema.[^18]
**Causa raíz:** No hay políticas de data governance, ni data stewards, ni rutinas de limpieza.  
**Fix:** Ownership rules claros, deduplicación regular, enrichment automatizado y "CRM hygiene hour" semanal.[^24][^18]

### 5. Over-customization

**Síntoma:** El CRM se vuelve tan customizado que los upgrades son imposibles, el mantenimiento requiere un equipo dedicado y los nuevos features del vendor no se pueden adoptar.  
**Causa raíz:** Se pelea contra las capacidades nativas de la plataforma en lugar de aprovecharlas.[^23]
**Fix:** Implementaciones exitosas típicamente aprovechan las capacidades de la plataforma en lugar de pelear contra ellas con customización excesiva.[^23]

### 6. Adopción forzada sin value para el usuario

**Síntoma:** Reps mantienen spreadsheets personales y emails mientras "cumplen" nominalmente con el sistema. Change fatigue.[^23]
**Causa raíz:** El CRM hace el trabajo del rep más difícil, no más fácil. Campos innecesarios, UX pobre, sin beneficio visible.[^26]
**Fix:** Automatizar logging repetitivo, eliminar campos innecesarios, dar voz a reps en cambios de layout, y vincular actividad a beneficios visibles (mejor asignación de territorio, distribución justa de leads).[^18]

### 7. Ejecutive sponsor ausente

**Síntoma:** El proyecto se delega a project managers sin autoridad ejecutiva. No se remueven barreras organizacionales ni se exige accountability de adopción.[^23]
**Causa raíz:** La organización subestima la transformación cultural requerida.  
**Fix:** El executive sponsor debe championar el cambio activamente, remover barreras y hacer accountable a los equipos.[^23]

***

## Diagnostic Questions

Para evaluar la salud de tu implementación CRM:

1. **¿Tu equipo comercial trabaja DESDE el CRM o solo lo actualiza DESPUÉS?** (Si es después, el CRM es un sistema de reporte, no un workflow engine).
2. **¿Puedes generar un forecast confiable (±10%) solo con datos del CRM, sin preguntar a cada AE?**
3. **¿"Qualified" significa exactamente lo mismo para todos tus vendedores?**
4. **¿Existe un solo dueño (RevOps/Admin) que aprueba cambios a la configuración del CRM?**
5. **¿Los reps del frontline fueron consultados en el diseño de stages, campos y layouts?**
6. **¿Puedes trazar el journey completo de una agencia desde primer contacto hasta última reserva sin salir del CRM?**
7. **¿Qué porcentaje de tus registros tiene todos los campos obligatorios completos?** (Si es <80%, tienes un problema de data quality).
8. **¿Tu equipo de servicio puede ver el contexto comercial (deal, condiciones, AE asignado) cuando recibe un ticket?**
9. **¿Cuándo fue la última vez que eliminaste un campo o stage que ya no se usa?**
10. **¿Los managers coachean desde dashboards del CRM o desde spreadsheets paralelos?**

***

## Sources

| ID | Fuente | Tipo | Fecha |
|----|--------|------|-------|
| 1 | Salesforce — "What Is CRM" | Vendor documentation | Jul 2024 |
| 2 | NetSuite/Oracle — "What Is CRM: An Expert Guide" | Vendor documentation | Nov 2025 |
| 3 | Creatio — "What is Enterprise CRM?" | Vendor documentation | Dec 2025 |
| 4 | Freshworks — "What is Enterprise CRM Software?" | Vendor documentation | Apr 2024 |
| 5 | SalesHive — "CRMs for B2B Sales: Best Practices" | Industry blog | Dec 2025 |
| 6 | LinkedIn Pulse — "Why CRM Implementations Fail" | Industry analysis | Jan 2026 |
| 7 | Databar.ai — "CRM Adoption Challenges in Large Enterprises" | Industry analysis | Feb 2026 |
| 8 | Workable — "CRM Administrator Job Description" | Job reference | Jan 2024 |
| 9 | FullEnrich — "CRM Administrator: Ultimate Guide" | Industry guide | Feb 2026 |
| 10 | Gainsight — "Customer Lifecycle" | Framework reference | Oct 2025 |
| 11 | Nextiva — "Customer Lifecycle Management" | Framework reference | Jan 2026 |
| 12 | Insightly — "Customer Lifecycle in CRM" | Framework reference | Aug 2024 |
| 13 | Monday.com — "SDR Career Roadmap" | Role reference | Feb 2026 |
| 14 | ProspectSoft — "6 Best Practices for CRM Opportunity Stages" | Best practices | Jun 2025 |
| 15 | Gary Smith Partnership — "Opportunity Stages in Salesforce" | Platform guide | Feb 2026 |
| 16 | Salesforce — "Automated Lead Nurturing" | Vendor documentation | Nov 2025 |
| 17 | Panorama Consulting — "Why CRM Implementations Fail" | Consulting | Nov 2023 |
| 18 | VendeDigital — "B2B CRM Implementation Guide" | Strategy guide | Oct 2024 |

***

## Key Takeaways for PM Practice

- **CRM enterprise no es un proyecto de IT — es una transformación de negocio.** La tecnología es la parte fácil; cambiar cómo trabaja la gente es el reto real.[^25][^23]
- **Cada rol tiene un JTBD distinto en el CRM:** SDR = generar pipeline calificado, AE = cerrar predeciblemente, CS = retener y expandir, Admin = mantener el sistema como infraestructura confiable.[^19][^18]
- **El anti-patrón más caro es automatizar procesos rotos.** Documenta y optimiza antes de configurar.[^23]
- **Governance mata al "Frankenstein CRM":** un solo owner (RevOps/Admin) que valide business value antes de agregar campos o stages.[^18]
- **La métrica de adopción real no es "login rate" sino "¿trabajan DESDE el CRM o solo lo llenan después?"**.[^18]
- **En B2B mayorista, el lifecycle es: agencia descubre → agencia firma → agencia opera → agencia crece → agencia refiere.** Cada etapa debe tener triggers, automations y métricas en el CRM.
- **El CRM council mensual con reps del frontline es el arma secreta** contra la brecha entre diseño del sistema y trabajo real.[^26][^18]

---

## References

1. [What Is CRM (Customer Relationship Management)? An Expert Guide](https://www.netsuite.com/portal/resource/articles/crm/what-is-crm.shtml) - CRM systems centralize customer information to help businesses enhance sales, marketing, and custome...

2. [What is Enterprise CRM? 14 Best Enterprise CRM Software | Creatio](https://www.creatio.com/glossary/enterprise-crm) - Enterprise CRM solutions cover all customer-facing operations – sales, marketing, customer service, ...

3. [What Is CRM (Customer Relationship Management)? - Salesforce](https://www.salesforce.com/crm/what-is-crm/) - Learn what CRM is, what it does, and how it can improve your customer relationships.

4. [What is enterprise CRM software? [Guide and Best Picks]](https://www.freshworks.com/crm/enterprise/) - Enterprise CRM is a software solution that provides a strategic approach to managing customer intera...

5. [CRM and Sales 2.0 Course: Pillars of Sales Management (2/16)](https://www.youtube.com/watch?v=mj_qVZH8wYE) - Te gustaría tener una sesión en vivo conmigo una vez al mes y trabajar en tus ventas? ¡Entra a Deton...

6. [6 Best Practices for Defining & Managing CRM Opportunity Stages](https://www.prospectsoft.com/resources/blog/6-best-practices-for-defining-managing-crm-opportunity-stages/) - CRM opportunity stages are defined steps a prospect goes through as they move through your sales pip...

7. [Opportunity Stages Explained With Best Practice Recommendations](https://garysmithpartnership.com/opportunity-stages/) - Opportunity stages in Salesforce help you track a deal's progress. That means your opportunity stage...

8. [What Is Automated Lead Nurturing? How It Works and Benefits](https://www.salesforce.com/sales/engagement-platform/automated-lead-nurturing/) - Automated lead nurturing uses software to send targeted, timely messages to prospects based on their...

9. [CRM Best Practices for Lead Scoring & Qualification - Nimble Blog](https://www.nimble.com/blog/crm-best-practices-for-lead-scoring-qualification/) - In this article, we will explore two best practices for lead scoring and qualification that will hel...

10. [12 best practices for lead nurturing with marketing automation | 2026](https://www.agilecrm.com/blog/12-best-practices-lead-nurturing-marketing-automation/) - Lead scoring—provided by most robust MA solutions—allows marketers to accurately gauge when nurtured...

11. [Glosario de implicación de Marketing Cloud - Salesforce Help](https://help.salesforce.com/s/articleView?id=mktg.mc_overview_glossary.htm&language=es_MX&type=5) - Una aplicación que ayuda a los especialistas de marketing a crear programas de marketing de múltiple...

12. [Customer Service CRM | Case Management Platform - Clear C2](https://www.clearc2.com/c2crm/customer-service/) - C2CRM's Customer Service Ticketing System includes case management, knowledge base articles, auto es...

13. [Dynamics 365 Customer Service Case Management](https://www.iotap.com/blog/2020/01/23/dynamics-365-customer-service-case-management-a-ticketing-application-too/) - Dynamics 365 Customer Service can be set up to jointly serve as a Case Management and a Ticket manag...

14. [Dynamics 365 Customer Service: Ticketing, Analytics, & Integration](https://stoneridgesoftware.com/products/dynamics-365-customer-service/) - Microsoft Dynamics 365 Customer Service Why Use Dynamics 365 Customer Service? Microsoft Dynamics 36...

15. [The Essential Guide to The Customer Lifecycle - Gainsight](https://www.gainsight.com/essential-guide/the-customer-journey-and-lifecycle/) - The five core customer lifecycle stages—reach, acquisition, conversion, retention, and loyalty—each ...

16. [Customer Lifecycle Management: The Ultimate Strategy Guide](https://www.nextiva.com/blog/customer-lifecycle-management.html) - Customer lifecycle management can help you create an engaging, positive customer experience. Here's ...

17. [Customer lifecycle in CRM - learn the stages](https://www.insightly.com/blog/customer-life-cycle-in-crm/) - The customer life cycle in CRM encompasses all stages of the customer journey, from initial awarenes...

18. [CRMs for B2B Sales: Best Practices for Use | SalesHive Blog](https://saleshive.com/blog/b2b-sales-crms-best-practices-use/) - The fix is simple: map your core sales plays first—your target personas, triggers, touch patterns, a...

19. [The SDR career roadmap: moving beyond prospecting in 2026](https://monday.com/blog/crm-and-sales/sdr-career-path/) - Four main career paths emerge from SDR experience: account Executive, Customer Success Manager, Reve...

20. [CRM Administrator: The Ultimate Guide to Success in ... - FullEnrich](https://fullenrich.com/jobtitle/CRM-Administrator) - Core Responsibilities of a CRM Administrator · System Management and Maintenance · User Administrati...

21. [Crm Administrator Job Description [+2024 TEMPLATE]](https://resources.workable.com/crm-administrator-job-description) - A CRM Administrator is a professional responsible for managing and customizing the Customer Relation...

22. [What Is A CRM Administrator, And Does My Business Need One?](https://crmswitch.com/crm-strategy/crm-administrator-benefits/) - The CRM administrator is typically responsible for user management, security, support, training, and...

23. [Why CRM implementations fail: Common pitfalls and strategic ...](https://www.linkedin.com/pulse/why-crm-implementations-fail-common-pitfalls-strategic-solutions-5qduc) - Organizations without documented, optimized business processes before CRM implementation struggle to...

24. [B2B CRM Implementation: A CMO's 20-Point Strategic Guide](https://vendedigital.com/blog/b2b-crm-implementation) - A B2B CRM implementation can boost growth and revenue. Discover the benefits and why it's vital for ...

25. [Why CRM Implementations Fail [6 Surprising Reasons]](https://www.panorama-consulting.com/why-crm-implementations-fail/) - CRM projects can be challenging, and many fall short of their goals. We explore reasons why CRM impl...

26. [CRM Adoption Challenges in Large Enterprises - Databar.ai](https://databar.ai/blog/article/crm-adoption-challenges-in-large-enterprises-why-big-companies-struggle-and-what-really-works) - Resistance to change ranks among the top reasons CRM implementations fail. And resistance in large o...

