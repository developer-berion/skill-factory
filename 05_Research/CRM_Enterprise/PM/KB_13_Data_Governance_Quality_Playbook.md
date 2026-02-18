# KB_14 — Data Governance, Quality & Stewardship para CRM

***

## Executive Summary

Data governance en CRM no es un proyecto de una sola vez: es infraestructura operativa continua que impacta directamente ventas, retención y margen. Este playbook cubre los siete pilares necesarios para operar un CRM enterprise con datos confiables: **(1)** políticas de deduplicación y merge, **(2)** identity resolution, **(3)** golden record y survivorship rules, **(4)** reglas de validación de datos, **(5)** workflows de data stewardship, **(6)** data lineage básico, y **(7)** métricas de data quality.[^1][^2]

**Fact:** El 44% de las empresas reportan pérdida de revenue por decisiones basadas en datos CRM de mala calidad. Cerca del 30% de duplicados son coincidencias exactas que nunca debieron existir — pura negligencia en controles de entrada. Gartner proyectó que el 30% de proyectos GenAI serían abandonados por mala calidad de datos.[^3][^4][^1]

**Inference:** Para un mayorista B2B como Alana Tours, donde el CRM maneja agencias (no pasajeros finales), datos sucios generan cotizaciones duplicadas, seguimientos perdidos, comisiones mal calculadas y fricción con la agencia — todo impacto directo en recurrencia y confianza.

El enfoque correcto: gobernanza embebida en el flujo operativo, no como proyecto paralelo. Prevención > detección > corrección, en ese orden de prioridad.

***

## Definitions and Why It Matters

| Concepto | Definición | Por qué importa en CRM B2B |
|---|---|---|
| **Data Governance** | Políticas, roles y procesos para gestionar datos como activo organizacional [^5] | Sin governance, cada vendedor entra datos como quiere y el CRM se vuelve inútil en 6 meses |
| **Deduplicación** | Eliminación de registros duplicados dentro de una fuente [^6] | Agencias duplicadas = comisiones mal atribuidas, reportes inflados |
| **Identity Resolution** | Unificación de identidades fragmentadas a través de múltiples fuentes y canales [^7][^8] | Una agencia puede aparecer como "Viajes Express", "V. Express SAS" y "viajes.express@gmail.com" en 3 sistemas |
| **Golden Record** | Versión única, completa y verificada de un registro maestro [^3][^9] | La "ficha oficial" de cada agencia que todos los equipos usan |
| **Survivorship Rules** | Reglas que determinan qué valor gana cuando hay conflicto entre registros [^9] | ¿Quién decide si el email correcto es el del CRM o el del ERP? |
| **Data Stewardship** | Implementación táctica de políticas de governance — el "quién hace qué" [^10][^11] | Sin steward asignado, nadie limpia nada |
| **Data Lineage** | Rastreo del origen, movimiento y transformación de datos a través de sistemas [^12][^13] | Saber de dónde vino un dato incorrecto para corregir la fuente, no solo el síntoma |
| **Data Quality** | Grado en que los datos cumplen estándares de completeness, accuracy, consistency, timeliness y uniqueness [^14][^15] | Si no lo mides, no lo mejoras |

***

## Principles and Best Practices

### 1. Dedupe / Merge Policies

La deduplicación no es un evento: es un proceso de tres fases — prevención, detección y post-merge.[^1]

**Fase 1 — Prevención (antes del merge):**
- Implementar autocomplete contra registros existentes en formularios de entrada[^1]
- Bloquear duplicados obvios en tiempo real: verificar email exacto antes de guardar (captura ~30% de duplicados)[^1]
- Estandarizar formatos al punto de entrada: teléfonos, direcciones, nombres de empresa[^16][^1]
- Campos obligatorios: nombre, email, teléfono, país, tipo de agencia[^4]

**Fase 2 — Detección (durante):**
- Matching en múltiples campos (no solo email): nombre + teléfono + dirección[^1]
- Usar fuzzy matching para variaciones sutiles ("Viajes Express" vs "V Express")[^3]
- Matching determinístico para IDs exactos (RIF/NIT, email) + probabilístico para el resto[^6][^8]
- Definir umbrales de confianza: auto-merge >95%, review 70-95%, ignorar <70%

**Fase 3 — Post-merge (survivorship y conflictos):**
- Definir reglas de survivorship explícitas por campo, no por registro completo[^9]
- Preservar historial: no borrar el valor perdedor, moverlo a log/notas[^1]
- Flaggear merges inciertos para revisión humana[^1]
- Mantener audit trail completo: qué cambió, cuándo, por qué regla, valores originales y nuevos[^1]

**Fact:** La deduplicación sin estrategia de prevención regenera duplicados en 6 meses.[^1]

### 2. Identity Resolution

Identity resolution unifica fragmentos de identidad de una misma entidad a través de múltiples touchpoints y sistemas.[^7][^8]

**Pasos de implementación:**
1. **Ingest & normalize:** emails (raw/hashed), teléfonos, IDs CRM, nombres normalizados[^6]
2. **Stitching logic:** reglas determinísticas (email exacto, ID fiscal) + modelos probabilísticos (similitud nombre/teléfono/dirección)[^6]
3. **Profile graphing:** mantener grafos de persona/empresa con provenance y survivorship[^6]
4. **Governance:** consent, limitación de propósito, retención y audit trails[^6]
5. **Activación y feedback:** exponer IDs resueltos a sistemas downstream; re-ingestar performance para refinar reglas[^6]

**Fact:** Los componentes core incluyen data onboarding, matching persistente en tiempo real, deduplicación y supresión, creación de perfil unificado, y enriquecimiento de perfil.[^8]

**Selección de modelo según contexto B2B:**
- **Determinístico** (alta precisión): para matching por RIF/NIT, email corporativo, código IATA → contactos conocidos[^8][^6]
- **Probabilístico** (mayor cobertura): para matching por nombre de agencia + ciudad + teléfono → agencias con datos inconsistentes[^8]
- **Híbrido** (recomendado): determinístico primero, probabilístico como fallback[^8]

### 3. Golden Record & Survivorship Rules

El golden record es la versión única, completa, precisa y verificada de cada entidad maestra. Sus características clave son: accuracy, completeness, uniqueness, timeliness y trustworthiness.[^3]

**Arquitectura Medallion (Bronze → Silver → Gold):**
- **Bronze:** Datos crudos de sistemas fuente (CRM, ERP, marketing automation)[^3]
- **Silver:** Datos procesados, mapeados y almacenados centralmente[^3]
- **Gold:** Golden records maestros en MDM[^3]

**6 pasos para crear un golden record**:[^3]
1. Ingestar datos de múltiples fuentes
2. Matchear registros que refieren a la misma entidad
3. Aplicar survivorship rules para determinar mejores valores
4. Validar y enriquecer para accuracy y completeness
5. Publicar a sistemas downstream
6. Mantener governance y stewardship continuo

**Reglas de survivorship — tipos principales**:[^9]

| Regla | Cómo funciona | Mejor para | Riesgo |
|---|---|---|---|
| **Source priority** | Jerarquía de sistemas como fuente de verdad | Orgs reguladas con fuentes claras | Rigidez si cambian sistemas |
| **Most recent** | Valor más reciente gana | Datos que cambian frecuentemente (email, cargo) | Requiere timestamps confiables |
| **Most complete** | Registro con menos campos vacíos gana | Atributos descriptivos, notas | Alto riesgo de error solo |
| **Data quality score** | Score compuesto (accuracy + completeness + conformidad) | Leads de múltiples fuentes | Más setup inicial |
| **Conditional (if-then)** | Lógica condicional por contexto | Diferentes reglas por país, tamaño, tipo | Complejidad de mantenimiento |
| **Híbrido** | Combina múltiples tipos con cascading logic | Organizaciones maduras | Requiere documentación sólida |

**Best practices de survivorship**:[^9]
- Definir reglas a nivel de atributo, no de registro completo
- Combinar múltiples tipos de regla con fallback
- Documentar no solo QUÉ es la regla sino POR QUÉ se decidió
- Monitorear resultados con métricas de data quality
- Involucrar stakeholders de negocio en la definición de reglas
- Revisar y actualizar reglas cuando cambian sistemas o prioridades

### 4. Data Validation Rules

La validación en el punto de entrada previene que errores se propaguen por todo el sistema.[^17][^16]

**Reglas de validación esenciales para CRM B2B:**

| Campo | Regla de validación | Ejemplo |
|---|---|---|
| Email | Formato válido + dominio existente | Rechazar "agencia@.com" |
| Teléfono | Formato estandarizado con código país | +58-XXX-XXXXXXX |
| Nombre agencia | Min 3 caracteres, sin solo números | Rechazar "123" |
| País | Selección de lista controlada (picklist) | No texto libre |
| RIF/NIT/Tax ID | Formato por país + dígito verificador | V-12345678-9 |
| Campos obligatorios | No guardar sin: nombre, email, teléfono, país | Bloqueo en formulario |
| Fechas | Formato único MM/DD/YYYY o ISO | No mezclar formatos |
| Moneda | Código ISO 4217 (USD, COP, VES) | No texto libre |

**Implementación práctica**:[^17][^16]
- Mandatory fields para datos críticos: bloquear guardado sin ellos
- Format checks automáticos al momento de entrada
- Autocomplete contra registros existentes para prevenir duplicados
- Scripts de validación que verifican datos antes de guardar
- Revisión y actualización periódica de reglas según cambios en procesos
- Training al equipo sobre importancia y cumplimiento de estándares

**Validaciones de referencial**:[^3]
- Verificar que la relación parent/child sea correcta (agencia → sub-agencia)
- Verificar que campos relacionados sean consistentes (país + código telefónico)
- Verificar contra fuentes externas cuando sea posible (LinkedIn, registros públicos)

### 5. Stewardship Workflows

Data stewardship es la implementación táctica del governance — el "quién hace qué, cuándo y cómo".[^18][^10]

**Rol del Data Steward en CRM**:[^11][^18]
- Implementar y supervisar estándares de entrada de datos
- Conducir auditorías regulares de calidad
- Colaborar cross-functionally (ventas, marketing, ops, IT)
- Resolver inconsistencias y errores puntualmente
- Gestionar metadata y definiciones de datos
- Asegurar compliance con políticas de governance y regulaciones
- Actuar como subject matter expert de su dominio de datos[^5]

**Workflow operativo recomendado:**

```
[Entrada de dato] → [Validación automática] → [¿Pasa?]
    → SÍ → [Dedupe check] → [¿Match?]
        → NO → [Crear registro]
        → SÍ (>95%) → [Auto-merge con survivorship rules]
        → SÍ (70-95%) → [Cola de revisión steward]
    → NO → [Rechazo + mensaje al usuario con corrección sugerida]

[Weekly sweep] → [Detección de duplicados nuevos]
    → [Auto-merge alta confianza]
    → [Cola de revisión media confianza]
    → [Reporte de métricas]

[Monthly audit] → [Data quality scorecard]
    → [Identificar campos con baja completeness]
    → [Identificar fuentes con alta tasa de error]
    → [Ajustar reglas de validación/survivorship]
```

**Stewardship no es un rol dedicado necesariamente**: puede distribuirse en roles existentes — Business Analysts aseguran calidad al generar insights, Data Engineers mantienen infraestructura, Department Heads aseguran compliance en su dominio. Lo importante es que haya ownership explícito.[^11]

**Skills clave del steward**: atención al detalle, comunicación y colaboración, habilidades analíticas, conocimiento de herramientas CRM y data management.[^18]

### 6. Data Lineage Básico

Data lineage rastrea el viaje del dato desde su origen, a través de transformaciones, hasta su destino final.[^12][^13]

**Por qué importa en CRM:**
- **Root cause analysis:** Identifica el origen de errores para corregir la fuente, no solo el síntoma[^12]
- **Data governance:** Base para establecer políticas de gestión[^12]
- **Migración segura:** Antes de migrar CRM, documentar lineage permite confirmar que cada elemento fue replicado correctamente[^19]
- **Change management:** Identificar impacto upstream/downstream de campos migrados o modificados[^19]

**Implementación pragmática para CRM:**

| Nivel | Qué documentar | Herramienta/método |
|---|---|---|
| **Campo** | Origen del campo (qué sistema lo genera) | Spreadsheet de mapping |
| **Registro** | Qué sistemas contribuyen a cada golden record | MDM/log de merge |
| **Flujo** | Cómo fluye data entre CRM ↔ ERP ↔ Marketing ↔ Billing | Diagrama de flujo simple |
| **Transformación** | Qué reglas transforman datos en tránsito | Documentación de ETL/integración |

**Best practices**:[^13]
- Integrar lineage con governance broader (no como ejercicio aislado)
- Monitorear y actualizar regularmente — lineage es un "living asset"
- Automatizar integrity checks después de deployments o cambios de schema
- Correlacionar lineage con métricas de data quality para identificar puntos débiles en pipelines[^19]
- Mantener audit trail de cambios a registros de lineage[^19]

### 7. Métricas de Data Quality

Las seis dimensiones core de data quality son: completeness, accuracy, consistency, timeliness, uniqueness y validity.[^14][^20][^15]

**Framework de métricas para CRM B2B:**

| Dimensión | Qué mide | KPI operativo | Target sugerido |
|---|---|---|---|
| **Completeness** | % de campos obligatorios poblados [^21] | `campos_poblados / campos_requeridos × 100` | >95% |
| **Accuracy** | Datos reflejan realidad [^22] | % registros validados contra fuente externa | >90% |
| **Consistency** | Mismo dato = mismo formato cross-system [^14] | % registros con formato estandarizado | >98% |
| **Timeliness** | Datos actualizados y disponibles cuando se necesitan [^15] | Data freshness (edad promedio del dato), latencia entre generación y disponibilidad | <30 días desde última actualización |
| **Uniqueness** | Sin duplicados [^15] | Tasa de duplicados sobre total de registros | <2% |
| **Validity** | Datos conforman reglas de negocio [^22] | % registros que pasan todas las validation rules | >97% |

**KPIs adicionales para dashboard**:[^23]
- Número de incidentes de data quality por período
- Time-to-response (detección → corrección)
- Tasa de duplicados creados vs resueltos por semana
- % de registros excluidos de análisis por mala calidad
- Data quality score compuesto por entidad (Accounts, Contacts, Opportunities)
- Trend lines sobre tiempo para detectar mejoras o degradación[^24]

**Fact:** Las métricas de data quality deben monitorizarse como trends, no como snapshots — snapshots solos son engañosos.[^24]

**Tipos de dashboard recomendados**:[^25]
1. **Dimension-focused:** Score por dimensión (completeness, accuracy, etc.)
2. **Critical Data Element (CDE):** Enfocado en campos de alto impacto (email agencia, RIF, datos de contacto principal)
3. **Business goal-focused:** Liga calidad a objetivos de negocio (revenue, retención agencias)

***

## Examples (Aplicado a CRM Enterprise — Mayorista B2B Turismo)

### Ejemplo 1: Deduplicación de Agencias
**Escenario:** "Viajes Express C.A." aparece como 3 registros: "Viajes Express", "V. Express SAS", "VIAJES EXPRESS CA".

**Solución aplicada:**
1. Fuzzy matching detecta similitud >85% en nombre + misma ciudad + teléfono similar
2. Regla de survivorship: source priority (CRM > import Excel), recency para email/teléfono, most complete para dirección
3. Golden record creado: "Viajes Express C.A." con todos los campos más completos
4. Audit log registra merge con valores originales preservados
5. Notificación al vendedor asignado para validar

### Ejemplo 2: Identity Resolution Cross-System
**Escenario:** La misma agencia existe en CRM (como lead), en sistema de reservas (como cliente activo) y en billing (como cuenta por cobrar).

**Solución aplicada:**
1. Deterministic match por RIF: V-J-12345678-9 → mismo entity
2. Stitching de perfiles con Golden ID compartido
3. Customer 360 muestra: lead history + reservas activas + balance de cartera
4. Steward valida y confirma merge, lineage documenta las 3 fuentes

### Ejemplo 3: Validation Rule Prevents Bad Data
**Escenario:** Vendedor intenta guardar agencia nueva sin email y con teléfono en formato incorrecto.

**Solución aplicada:**
1. CRM bloquea guardado: email es mandatory field
2. Teléfono reformateado automáticamente: "04121234567" → "+58-412-1234567"
3. Autocomplete sugiere: "¿Es esta agencia existente? 'Viajes Express' en la misma ciudad"
4. Vendedor selecciona registro existente en lugar de crear duplicado

***

## Metrics / Success Signals

**Señales de que el governance está funcionando:**
- Tasa de duplicados bajando mes a mes (<2% target)
- Completeness de campos críticos >95%
- Tiempo de resolución de issues de calidad <48h
- Vendedores reportan menos fricción al buscar agencias
- Reportes de ventas coinciden con realidad operativa
- Zero merges incorrectos que requieran rollback en el mes
- Data quality score compuesto mejorando quarter over quarter

**Señales de alarma (actuar inmediato):**
- Tasa de duplicados subiendo → controles de prevención fallando
- Completeness cayendo → probable cambio en proceso de entrada no gobernado
- Inconsistencia cross-system subiendo → integración o lineage roto
- Quejas de vendedores sobre datos incorrectos → survivorship rules necesitan revisión

***

## Operational Checklist

### Setup Inicial (Una vez)
- [ ] Definir campos obligatorios por entidad (Account, Contact, Opportunity)
- [ ] Configurar validation rules en CRM (formatos, mandatory fields, picklists)
- [ ] Establecer reglas de survivorship por atributo (documentar QUÉ y POR QUÉ)[^9]
- [ ] Definir umbrales de dedupe: auto-merge >95%, review 70-95%, ignore <70%
- [ ] Asignar data steward(s) con ownership explícito por dominio
- [ ] Crear dashboard de data quality con las 6 dimensiones
- [ ] Documentar data lineage básico: mapping de campos → sistema fuente
- [ ] Configurar audit trail para merges y cambios de datos críticos[^1]
- [ ] Capacitar equipo en estándares de entrada y por qué importan[^17]
- [ ] Definir Golden ID scheme para identidad cross-system[^26]

### Semanal
- [ ] Ejecutar sweep de deduplicación en registros nuevos[^1]
- [ ] Revisar cola de merges pendientes (confianza 70-95%)[^27]
- [ ] Verificar que integraciones no generaron duplicados
- [ ] Check de completeness en registros creados esa semana

### Mensual
- [ ] Generar data quality scorecard completo (6 dimensiones)
- [ ] Auditar top 10 registros con peor quality score
- [ ] Revisar métricas de duplicados: creados vs resueltos
- [ ] Actualizar reglas de validación si hay cambios en procesos
- [ ] Revisar data lineage si hubo cambios en integraciones

### Trimestral
- [ ] Revisión de survivorship rules con stakeholders de negocio[^9]
- [ ] Evaluar si targets de quality se están cumpliendo
- [ ] Enriquecer golden records con fuentes externas
- [ ] Revisar compliance y audit trails
- [ ] Ajustar umbrales de dedupe basado en resultados

***

## Anti-Patterns

| Anti-patrón | Por qué falla | Qué hacer en su lugar |
|---|---|---|
| **"Limpieza de una sola vez"** | Los duplicados regresan en 6 meses sin controles de prevención [^1] | Governance continuo: prevención + detección + mantenimiento |
| **Governance como proyecto solo de IT** | Sin buy-in de negocio, las políticas se ignoran [^2][^28] | Involucrar ventas, marketing y ops desde el inicio |
| **Survivorship a nivel de registro completo** | "Confiar en todo del CRM" genera datos incorrectos en campos que el CRM no domina [^9] | Definir survivorship a nivel de atributo individual |
| **Sin ownership explícito** | Si nadie es responsable, nadie limpia [^2] | Asignar stewards por dominio con accountability clara |
| **Sobre-automatizar sin monitoreo** | Errores de automatización se propagan sin ser detectados [^29] | Automatizar + monitorear + human-in-the-loop para casos ambiguos |
| **No documentar reglas de survivorship** | Cuando cambia el equipo, nadie sabe por qué se decidió X regla [^9] | Documentar QUÉ y POR QUÉ de cada regla |
| **Tratar de arreglar todo a la vez** | Parálisis por análisis, nunca se lanza [^28] | Empezar con un dominio crítico (Accounts) y expandir |
| **Controles demasiado restrictivos** | Vendedores bypasean el sistema creando registros en hojas de Excel [^30] | Controles proporcionales: obligatorio solo lo que realmente importa |
| **Confiar solo en recency sin timestamps confiables** | Batch updates nocturnos pueden "ganar" sobre datos reales más recientes [^9] | Validar calidad de timestamps antes de usar recency rules |
| **Métricas como snapshot sin trends** | Un número aislado no dice si la calidad mejora o empeora [^24] | Monitorear trends semanales/mensuales |
| **No preservar historial de merges** | Sin rollback posible cuando un merge fue incorrecto [^1] | Audit trail completo + valores originales preservados |
| **Falta de evolución** | Reglas estáticas en un negocio dinámico pierden relevancia [^2] | Review trimestral de reglas con el equipo de negocio |

***

## Diagnostic Questions

Usa estas preguntas para evaluar la madurez de data governance en tu CRM:

### Governance General
1. ¿Existe una política escrita de data governance para CRM? ¿Cuándo fue la última actualización?
2. ¿Hay un data steward asignado con ownership explícito? ¿Quién rinde cuentas?
3. ¿Se mide data quality con métricas específicas? ¿Se reportan periódicamente?

### Deduplicación
4. ¿Cuál es la tasa actual de duplicados en Accounts? ¿Se conoce?
5. ¿Existen controles de prevención en el punto de entrada (autocomplete, block on exact match)?
6. ¿Cada cuánto se ejecuta un sweep de deduplicación?
7. ¿Hay reglas de survivorship documentadas y aprobadas por negocio?

### Identity Resolution
8. ¿Se puede identificar a la misma agencia a través de CRM, sistema de reservas y billing?
9. ¿Existe un Golden ID o identificador unificado cross-system?
10. ¿El matching es solo determinístico o también usa probabilístico?

### Golden Record
11. ¿Cuál es el "single source of truth" para cada campo crítico?
12. ¿Las survivorship rules están a nivel de atributo o de registro completo?
13. ¿Se preserva historial cuando se hace un merge?

### Validación
14. ¿Qué campos son mandatory? ¿Se hace enforce en el CRM o solo en documentación?
15. ¿Hay validation rules activas para formato de email, teléfono, tax ID?
16. ¿Los vendedores pueden crear registros sin pasar validación?

### Stewardship
17. ¿Quién revisa los merges con confianza media (70-95%)?
18. ¿Hay un workflow definido para escalar y resolver conflictos de datos?
19. ¿El equipo recibió training sobre estándares de entrada?

### Lineage
20. ¿Se sabe de qué sistema vino cada campo del golden record?
21. ¿Antes de una migración, se documenta el lineage para confirmar replicación correcta?

***

## Sources

- CleanSmartLabs (2026). "Data Deduplication Strategy: Before, During, and After the Merge."
- Profisee (2025). "What Is a Golden Record in MDM?" y "MDM Survivorship: How to Choose the Right Record."
- Stibo Systems (2025). "A Quick Guide to Golden Customer Records in MDM."
- CustomerLabs (2025). "Best 10 Identity Resolution Software Tools."
- Astera Software (2024). "Data Lineage: A Complete Guide."
- Agile Brand Guide (2025). "Identity Resolution."
- Collate (2024). "Mastering Data Lineage."
- Dagster (2026). "Data Lineage in 2025: Types, Techniques, Use Cases & Examples."
- LoginRadius (2024). "How to Leverage Advanced Customer Identity Resolution."
- IBM (2025). "6 Pillars of Data Quality and How to Improve Your Data."
- Monte Carlo Data (2025). "The 6 Data Quality Dimensions."
- Informatica. "Data Quality Metrics & Measures."
- GetDatabees (2025). "CRM Data Stewards and Their Role in Data Quality Management."
- Alation (2024). "The Role of Data Stewards Today."
- DCKAP (2025). "11 CRM Data Quality Best Practices."
- Kenway Consulting (2025). "Data Governance in Salesforce: Best Practices for Data Stewardship."
- Atlan (2023). "7 Common Data Governance Mistakes & How to Avoid."
- Syncari (2025). "Monitoring Data Quality Dashboards for AI-Ready Enterprises."
- DataKitchen (2025). "A Guide to the Six Types of Data Quality Dashboards."
- Plauti (2025). "The Hidden Costs of Poor CRM Data."
- Actian (2026). "Understanding the Pillars of Data Governance."
- 6Sigma.us (2025). "8 Core Dimensions of Data Quality."
- Advantage CG (2026). "How to Solve The 5 Biggest Enterprise Data Governance Challenges."
- Bluesoft (2025). "7 Reasons Why Data Governance Projects Fail."
- TechTarget (2024). "Evaluating data quality requires clear and measurable KPIs."

***

## Key Takeaways for PM Practice

- **Prevención > detección > corrección** — el duplicado más barato es el que nunca se crea.[^1]
- **Survivorship a nivel de atributo**, nunca a nivel de registro completo — cada campo tiene su mejor fuente.[^9]
- **Golden record no es estático** — es un "living asset" que requiere stewardship continuo.[^13][^3]
- **Governance sin ownership = governance muerto** — asignar steward con accountability real, no comité sin dientes.[^2][^11]
- **Métricas como trends, no snapshots** — un número aislado no dice nada; la dirección de la curva lo dice todo.[^24]
- **Empezar pequeño, con un dominio crítico** (Accounts/Agencias) y expandir — tratar de arreglar todo a la vez es el anti-patrón #1.[^28]
- **Controles proporcionales** — demasiado restrictivo y el equipo bypasea el sistema; demasiado laxo y el CRM se llena de basura.[^30]
- **Documenta el POR QUÉ** de cada regla, no solo el QUÉ — tu yo del futuro (o tu reemplazo) te lo agradecerá.[^9]
- **Data lineage no es lujo** — cuando un reporte está mal, lineage te dice en 5 minutos dónde está el error; sin lineage, tardas días.[^12][^19]
- **El 44% de empresas pierden revenue por mala data CRM** — esto no es tema técnico, es tema de P&L.[^4]

---

## References

1. [Data Deduplication Strategy: Before, During, and After the Merge](https://www.cleansmartlabs.com/blog/data-deduplication-strategy-before-during-and-after-the-merge) - Deduplication isn't a one-time event. Here's how to handle duplicates at every stage—from prevention...

2. [7 Common Data Governance Mistakes & How to Avoid - Atlan](https://atlan.com/data-governance-mistakes/) - Mistakes: 1. Lack of clear ownership and accountability 2. Not aligning with business objectives 3. ...

3. [What Is a Golden Record in MDM? - Profisee](https://profisee.com/blog/what-is-a-golden-record/) - A golden record in MDM is a complete and accurate version of a data point stored where it can be acc...

4. [The Hidden Costs of Poor CRM Data (and, how to fix it) | Plauti](https://www.plauti.com/blog/hidden-costs-poor-data-quality-crm-fixes) - Poor data quality within a CRM can become like clogged arteries, data becomes stagnant and corrupt. ...

5. [Understanding the Pillars of Data Governance - Actian Corporation](https://www.actian.com/blog/data-governance/data-governance-pillars/) - Data stewardship ensures that data is managed with clear roles, responsibilities, and accountability...

6. [Identity Resolution - The Agile Brand Guide](https://agilebrandguide.com/wiki/data/identity-resolution/) - Enrich selectively: add third-party data where it clearly improves match quality or completeness; me...

7. [Best 10 Identity Resolution Software Tools 2025 - CustomerLabs](https://www.customerlabs.com/blog/best-identity-resolution-software-tools/) - Find the best identity resolution software of 2024 to enhance brand-customer interactions and optimi...

8. [How Does Identity Resolution Play A Critical Role In The Future of ...](https://lifesight.io/blog/identity-resolution-in-marketing/) - An identity resolution solution eliminates data fragmentation and duplicate data entries and ensures...

9. [MDM Survivorship: How to Choose the Right Record - Profisee](https://profisee.com/blog/mdm-survivorship/) - Learn the top MDM survivorship rules to select accurate, trusted data for your golden record and imp...

10. [Data Governance in Salesforce: Best Practices for Data Stewardship](https://www.kenwayconsulting.com/blog/data-governance-in-salesforce/) - Data stewards are responsible for implementing the tactical aspects of a plan for CRM data governanc...

11. [The Role of Data Stewards Today: Key Responsibilities & Challenges](https://www.alation.com/blog/role-of-data-stewards/) - A data steward is a team member who is responsible for overseeing a subset of an organization's info...

12. [Data Lineage: A Complete Guide - Astera Software](https://www.astera.com/type/blog/data-lineage/) - Data lineage refers to the journey of data from origin through various transformations and movements...

13. [Data Lineage in 2025: Types, Techniques, Use Cases & Examples](https://dagster.io/learn/data-lineage) - Data lineage is the process of tracking the flow of data as it moves through an organization's syste...

14. [6 Pillars of Data Quality and How to Improve Your Data | IBM](https://www.ibm.com/products/tutorials/6-pillars-of-data-quality-and-how-to-improve-your-data) - Measuring data quality metrics, such as completeness, accuracy, consistency, timeliness, or uniquene...

15. [The 6 Data Quality Dimensions (Plus 1 You Can't Ignore) With ...](https://www.montecarlodata.com/blog-6-data-quality-dimensions-examples/) - The traditional framework includes six core dimensions that most teams know well. These are accuracy...

16. [11 CRM Data Quality Best Practices You Must Know - DCKAP](https://www.dckap.com/blog/crm-data-quality-best-practices/) - Implement validation rules within your CRM application, such as mandatory fields, format checks, and...

17. [Mastering CRM Data Quality: 7 Key Strategies for Success](https://www.roofingbusinesspartner.com/blog/mastering-crm-data-quality-7-key-strategies-for-success) - Some examples of data validation rules include verifying email addresses, phone numbers, postal code...

18. [CRM Data Stewards and Their Role in Data Quality Management](https://getdatabees.com/resources/blog/crm-data-steward/) - Data stewards ensure that outbound sales teams have up-to-date client information allowing for effec...

19. [Mastering Data Lineage - Techniques, Use Cases & Pro Tips - Collate](https://www.getcollate.io/learning-center/data-lineage) - Data lineage is the process of tracking the origin, movement, and transformations of data across a s...

20. [[PDF] The Six Primary Dimensions for Data Quality Assessment](https://www.sbctc.edu/resources/documents/colleges-staff/commissions-councils/dgc/data-quality-deminsions.pdf) - Accuracy, Completeness, Consistency and Uniqueness. Optionality. Mandatory. Applicability. Example(s...

21. [8 Core Dimensions of Data Quality: A Guide to Data Excellence](https://www.6sigma.us/six-sigma-in-focus/dimensions-of-data-quality/) - Data completeness refers to having all required data present and usable. Develop a comprehensive fra...

22. [Data Quality Metrics & Measures — All You Need To Know](https://www.informatica.com/resources/articles/data-quality-metrics-and-measures.html) - Common data quality metrics include accuracy, completeness, consistency, timeliness, validity, dupli...

23. [Evaluating data quality requires clear and measurable KPIs](https://www.techtarget.com/searchdatamanagement/tip/Evaluating-data-quality-requires-clear-and-measurable-KPIs) - KPIs enable organizations to determine the current state of data quality and monitor quality improve...

24. [Monitoring Data Quality Dashboards for AI-Ready Enterprises](https://syncari.com/blog/monitoring-measuring-and-scaling-trust-with-data-quality-dashboards/) - Learn how executives use Syncari's data quality dashboards to monitor, measure, and operationalize t...

25. [A Guide to the Six Types of Data Quality Dashboards | DataKitchen](https://datakitchen.io/the-six-types-of-data-quality-dashboards/) - The article outlines six types of dashboards—KPI dashboards, data element dashboards, business goal ...

26. [[PDF] A Best Practices Guide to Deduplication and Merging](https://appexchange.salesforce.com/partners/servlet/servlet.FileDownload?file=00P4V000011djAeUAI) - The trick is to tolerate duplicates without creating confusion for users: the. Golden ID, a unique i...

27. [Handling merging tasks to deduplicate records - Qlik Help](https://help.qlik.com/talend/en-US/data-stewardship-examples/8.0/handling-merging-tasks-to-deduplicate-records) - Merging tasks aim to merge several potential duplicates into one single record: master record. Poten...

28. [7 Reasons Why Data Governance Projects Fail (And How To Avoid It)](https://bluesoft.com/blog/reasons-data-governance-projects-fail-how-to-avoid-it) - 1. Treating Data Governance as a “one-and-done” project · 2. Seeing data problems as just an IT issu...

29. [Data Governance and Troubleshooting Data Challenges: Tools and ...](https://www.dennison-associates.com/data-governance-and-troubleshooting-data-challenges-tools-and-solutions/) - Let's take a look at why data governance is important, then examine common CRM data issues and solut...

30. [How to Solve The 5 Biggest Enterprise Data Governance Challenges](https://www.advantagecg.com/blog/enterprise-data-governance-challenges) - Overly restrictive controls push employees to bypass approved systems, increasing exposure and risk....

