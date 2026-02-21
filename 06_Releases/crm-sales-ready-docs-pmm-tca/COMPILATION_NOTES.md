# COMPILATION_NOTES.md
## Skill: crm-sales-ready-docs-pmm-tca | v1.0.0
**Compilado:** 2026-02 | **Compilador:** Antigravity (Berion) | **KB fuente:** `/05_Research/SalesReady_Docs_PMM_TCA/`

---

## 1. Archivos KB Utilizados

| KB | Título | Modos que alimenta |
|---|---|---|
| KB_01 | Feature Excellence As Guarantee | A |
| KB_02 | Benefit–Functionality Mapping (DBPOR) | A, B |
| KB_03 | View Anatomy Mode | C |
| KB_04 | Data Logic Deep Dive | D |
| KB_05 | Data Lineage orientado a negocio | E |
| KB_06 | Entity Dictionary Semantics | F |
| KB_07 | Functional Audit No Omissions | G |
| KB_08 | Senior Solution Architect Narrative | H |
| KB_09 | Sales-Ready Markdown Formatting | I |
| KB_10 | Credibility Grounding Claim Ledger | J |
| KB_11 | Enterprise Readiness RBAC Audit Compliance | K |
| KB_12 | Measurement Adoption Value Instrumentation | L |
| KB_13 | Dedup Matching Explainability | G (test A) |
| KB_14 | Dedup Survivorship Merge Policies | K.3, Golden Test A |
| KB_15 | KPI Cards Stale Degraded Partial Data | C, D |
| KB_16 | Data Incidents Playbook | Failure Modes, E |
| KB_17 | Calculation Contracts Testing Versioning | D, L |
| KB_18 | Evidence Standards Proof Types | J |
| KB_19 | Claim Ledger System | J |
| KB_20 | Analytics Event Governance SemVer | L.1 |
| KB_21 | Value Attribution Framework | L.2, J |
| KB_22 | ABAC Policies for CRM | K.1 |
| KB_23 | Audit Logs Export Retention Tamper Evidence | K.2 |
| KB_24 | Semantic Ownership Conflict Resolution | F, Risk Matrix |
| SOURCES.md | Task definition, reglas, output paths | Todos (instrucciones) |
| KB_INDEX.md | Vacío — sin contenido | — |

**Total KBs procesados:** 24 + SOURCES.md + KB_INDEX.md (vacío)

---

## 2. Items needs_clarification (Información Faltante)

Los siguientes items no pudieron resolverse desde los KBs y requerirán insumos del equipo de producto antes de completar artefactos específicos:

| ID | Item faltante | Modo afectado | Acción requerida |
|---|---|---|---|
| NC-01 | Latencias reales de actualización de KPIs (Weighted Forecast, Pipeline Coverage) | C, E | Solicitar a Engineering la frecuencia de refresh real, documentada por escrito |
| NC-02 | Fórmulas formales de KPIs adicionales más allá de Weighted Forecast | D | Solicitar Mathematical Spec del equipo de producto por cada KPI |
| NC-03 | Matriz de roles y permisos reales del CRM (RBAC table) | K | Solicitar a Admin/IT la matriz actual de roles → permisos → campos |
| NC-04 | Evidencia tipo A o B para claims de deduplicación (% mejora, tasa de detección) | J, Golden Test A | Ejecutar audit de producción; documentar N, período y condiciones del benchmark |
| NC-05 | Umbral de confianza (threshold) configurado actualmente en el motor de dedup | D, G | Solicitar valor actual y política de configuración a Engineering |
| NC-06 | Schema real de audit logs en el CRM (si está implementado) | K.2 | Solicitar a Engineering el schema de eventos auditados y política de retención actual |
| NC-07 | Política de survivorship field-level (qué campo gana en merge) | K.3 | Definir con RevOps + Data Council; documentar como Survivorship Policy |
| NC-08 | ARR/MRR: aplicabilidad para el modelo de negocio del cliente | F | Confirmar si el CRM maneja ARR o si el modelo es transaccional puro |
| NC-09 | Regulaciones locales aplicables (LATAM: Venezuela, Colombia, México) | K | Solicitar revisión de Legal sobre aplicabilidad de GDPR/SOC2/PCI-DSS en cada jurisdicción |
| NC-10 | Owners semánticos formales de entidades críticas (Opportunity, Account, Revenue) | F, K | Constituir Data Council (Sales + Finance + RevOps + IT) y asignar RACI |

---

## 3. Asunciones Realizadas (Mínimas)

| ID | Asunción | Justificación | Riesgo si incorrecta |
|---|---|---|---|
| AS-01 | Timestamps en UTC (ISO 8601) en audit logs y event specs | Estándar de industria documentado en KB_23 y KB_20 | Ambigüedad en auditorías cross-border |
| AS-02 | Retención mínima: SOC 2 baseline (1 año accesible + 6 años cold storage) | KB_23 establece SOC 2 como piso recomendado para LATAM sin regulación local | Puede ser insuficiente si cliente tiene SOX o PCI-DSS |
| AS-03 | DENY-override como combining algorithm por defecto en ABAC | KB_22 recomienda fail-secure; DENY-override es el patrón más seguro | Si el cliente tiene políticas menos restrictivas, puede crear fricción operativa |
| AS-04 | BACKWARD_TRANSITIVE como compatibility mode para schemas de eventos | KB_20 lo establece como el modo más seguro para CRM enterprise | Requiere confirmación de la plataforma de schema registry en uso |
| AS-05 | proof_type = C con disclaimer para correlaciones no randomizadas | KB_21 establece que correlación controlada no implica causalidad | Si el cliente tiene experimentos controlados disponibles, actualizar a tipo A |

---

## 4. Conflictos entre KBs y Resolución

| Conflicto identificado | KBs involucrados | Resolución adoptada |
|---|---|---|
| KB_10 y KB_19 cubren el Claim Ledger con diferente nivel de detalle | KB_10 (principios), KB_19 (sistema completo) | Se usó KB_19 como spec canónica del Claim Ledger en Modo J; KB_10 aporta el contexto de por qué existe. Sin contradicción real; son complementarios. |
| KB_11 (RBAC clásico) y KB_22 (ABAC) describen sistemas de control de acceso distintos | KB_11, KB_22 | Se integran en Modo K: RBAC como baseline + ABAC como capa de refinamiento contextual. El patrón híbrido está explícitamente documentado en KB_22. Sin contradicción. |
| KB_12 (instrumentación general) y KB_20 (gobernanza de eventos con SemVer) solapan en la definición de Event Specs | KB_12, KB_20 | KB_20 es la spec más reciente y detallada para event governance (schema registry, SemVer, cardinality). KB_12 aporta el framework de valor y KPIs de adopción. Se separaron en sub-modos L.1 (KB_20) y L.2 (KB_21). Sin contradicción. |
| KB_21 habla de atribución de valor; KB_12 habla de instrumentación y métricas de adopción — conceptualmente relacionados | KB_12, KB_21 | Se agruparon en Modo L (Measurement + Event Governance + Value Attribution). El árbol de decisión de KB_21 dicta el método de atribución; KB_12 define qué medir. Complementarios sin conflicto. |

---

## 5. Evidencia Adicional Sugerida (Para Completar Artefactos)

Para elevar la calidad y confiabilidad de la documentación producida, se recomienda recopilar los siguientes artefactos del producto real:

### Prioridad Alta (bloquea claims y calculation specs)

1. **Screenshots del UI de deduplicación** en todos sus estados: suggestion_ready, merge_pending, merge_confirmed, error, rollback_available. Necesarios para Modes C y G.
2. **Logs de producción (anonimizados)** de merges realizados: N total, distribution de match scores, rollback rate. Necesarios para elevar CL-D01 de draft a approved.
3. **Confirmación escrita de Engineering** de latencias de refresh para cada KPI del dashboard de Forecast. Resuelve NC-01.
4. **Fórmula matemática formal del motor de dedup** (weights w₁..w₄, fórmula de score normalizado). Resuelve NC-05 y desbloquea Golden Test A completo.

### Prioridad Media (mejora calidad pero no bloquea el artefacto base)

5. **Matriz de roles existente** (export de la configuración de permisos del CRM). Resuelve NC-03; desbloquea Modo K completo.
6. **Resultados de cualquier experimento o análisis causal** realizado sobre features. Permite actualizar claims de proof_type C a A o B.
7. **Definiciones actuales de pipeline stages** con criterios de entrada/salida formales. Enriquece Entity Dictionary (Modo F) y Calculation Spec de Pipeline Coverage.

### Prioridad Baja (enriquecimiento)

8. **Capturas de estado Stale/Degraded** si ya están implementados en el UI. Ilustran el Modo C con evidencia visual real.
9. **Política de retención actual** del CRM si está documentada. Permite validar o reemplazar AS-02.
10. **Registro de incidentes de datos pasados** (si existe postmortem). Alimenta el Incident Playbook (KB_16) con casos reales.

---

## 6. Nota de Estilo

- **Idioma:** Español venezolano corporativo. Directo. Sin hipérboles.
- **Voz:** Arquitecto de Soluciones Senior. Cada afirmación tiene sustento.
- **Separación Fact/Inference:** Aplicada en todo el skill spec. Obligatoria en todos los artefactos que genere la skill.
- **Templates:** Todos los modos usan plantillas canónicas extraídas de los KBs. No se inventaron estructuras adicionales.

---

## 8. Patch Log — v1.0.0 → v1.0.1

**Fecha de patch:** 2026-02-21 | **Motivo:** Hardening de precisión epistémica y schemas (Changesets A, B, C).

### Patch Summary

Aplicados tres changesets de refuerzo sobre el skill spec original `crm-sales-ready-docs-pmm-tca.skill.md`:

| Changeset | Objetivo |
|---|---|
| A | Impedir que Golden Tests se lean como verdad de producto |
| B | Convertir todos los defaults en `[INFERENCE]` + triggers de `needs_clarification` |
| C | Cerrar schemas JSON para eliminar ambigüedad e invención de datos |

---

### Files Changed

| Archivo | Tipo de cambio |
|---|---|
| `03_Skills/crm-sales-ready-docs-pmm-tca.skill.md` | PATCH (6 bloques de reemplazo) |
| `06_Releases/crm-sales-ready-docs-pmm-tca/COMPILATION_NOTES.md` | APPEND (este bloque) |

---

### Behavioral Changes

#### Changeset A — Golden Tests no pueden leerse como verdad de producto

1. **Regla global añadida** en sección "¿Qué NO hace?" (antes de los Modos de Operación):
   - Bloque `[!WARNING]` que declara explícitamente que los Golden Tests usan datos ficticios y mecanismos ilustrativos.
   - Establece el protocolo de sustitución: Example-only → `[FACT]` solo cuando hay `evidence_source` declarado.

2. **Golden Test A — Deduplicación:**
   - `logic_summary` del input de test reemplazado por `"[PLACEHOLDER — rellenar con evidencia real del producto]"`. Se eliminaron las referencias a Levenshtein, embeddings, LLM y SHA-256 que antes aparecían como datos del producto.
   - Bloque `[!WARNING]` añadido antes de outputs esperados.
   - Sección D (Calculation Spec) reescrita: fórmula de score ahora marcada línea por línea como `[INFERENCE] Example-only`.
   - Tabla G (Audit): período de rollback "72h" reemplazado por `[RELLENAR — período confirmado por producto]` con nota `[INFERENCE] Example-only`.
   - Tabla J: columna `proof_type` reemplazada por `proof_strength`; `evidence_source` reemplazado por `evidence_link`.
   - Sección L: evento names marcados como `example-only; confirmar con Engineering`.
   - Disclaimer de test añadido al final de la sección L.

3. **Golden Test B — Forecast Dashboard:**
   - KPIs del input reescritos: `formula` libre reemplazada por `formula_formal: "[RELLENAR]"`, campo `definition` añadido, `decision_supported` añadido, `source_type: "SQL"` y `latency_confirmed: false` añadidos.
   - Bloque `[!WARNING]` añadido antes de outputs esperados.
   - Sección D (Calculation Spec) reescrita: fórmula WF ahora marcada línea por línea como `[INFERENCE] Example-only`.
   - Sección C: assertions actualizadas para reflejar que `latency_confirmed: false` activa `needs_clarification` automáticamente.
   - Sección C: `permission_denied` añadido como estado requerido (del enum cerrado).
   - Tabla J: columnas actualizadas a `proof_strength` + `evidence_link`; `methodology_disclaimer` inline en CL-F02.
   - Sección L: evento marcado como `— Example-Only` en el título; propiedades marcadas como `example-only`.
   - Disclaimer de test añadido al final de la sección L.

#### Changeset B — Defaults convertidos a `[INFERENCE]` + MUST ASK

1. **Sección "PUEDE ASUMIR"** completamente reescrita:
   - Título cambiado a: "PUEDE ASUMIR — Solo como punto de partida declarado (todo ítem es `[INFERENCE]`)".
   - Bloque `[!WARNING]` añadido al inicio de la sección.
   - Tabla expandida de 2 columnas a 3: `Asunción [INFERENCE]` / `Condición para asumir` / `MUST ASK si no se confirma`.
   - Cada ítem ahora genera un `needs_clarification` específico si no hay confirmación del usuario.
   - Período numérico de retención ("1 año") eliminado de la columna de asunción; reemplazado por "piso de referencia" sin número comprometido.

2. **Modo K.1 — RBAC/ABAC:**
   - Primer paso cambiado a: REQUIERE `security_compliance_input.rbac_defined = true` antes de producir documentación de seguridad.
   - Combining algorithm (DENY-override) convertido de "recomendado" a `[INFERENCE] Example-only` con MUST ASK explícito.
   - PAP/PDP/PEP: si no está confirmado → `needs_clarification`.

3. **Modo K.2 — Audit Logs:**
   - SHA-256 + WORM: convertido de fact a `[INFERENCE] Example-only` con instrucción de confirmar con Engineering.
   - Períodos de retención (1 año / 6 años): convertidos de "mínimo recomendado" a `[INFERENCE] Example-only` con `needs_clarification` si no se confirman.
   - Bloque de REQUIERE añadido al inicio del sub-modo.

#### Changeset C — Schemas JSON endurecidos

1. **`ui_states`:** Enum CERRADO con 8 valores: `[loading, empty, nominal, stale, degraded, partial, error, permission_denied]`. Antes era array de strings libres.

2. **`view_spec_input.kpis`:**
   - `minItems: 1` añadido.
   - Campos requeridos por KPI: `name`, `definition`, `owner`, `decision_supported`.
   - Nuevo campo: `definition` (lenguaje llano, separado de formula).
   - Nuevo campo: `source_type` (enum cerrado: `SQL, RPC, ETL, CACHE, MANUAL, UNKNOWN`). Si `UNKNOWN` → `needs_clarification`.
   - Nuevo campo: `latency_confirmed` (boolean). Si `false` → `needs_clarification`.

3. **`calculation_spec_input`:**
   - `required: [kpi_name, input_schema, output_schema, examples]` añadido.
   - `inputs` (texto libre) reemplazado por `input_schema` (objeto estructurado con array de `fields`).
   - `output_schema` añadido (objeto estructurado con `name`, `type`, `rounding_mode`, `numeric_tolerance`).
   - `rounding_mode`: el usuario DEBE proveerlo; la skill no asume ninguno.
   - `numeric_tolerance` (number): requerido si algún ejemplo se etiqueta `[FACT]`.
   - `null_policy` y `rounding_policy` (texto libre) eliminados; reemplazados por campos estructurados.

4. **`security_compliance_input` (NUEVO BLOQUE):**
   - `rbac_defined` (boolean, requerido): Si `false` → suspende Modo K.
   - `rbac_matrix` (array estructurado): roles + permisos + visible/hidden fields.
   - `audit_log_available` (boolean, requerido): Si `false` → prohíbe claims de auditabilidad.
   - `audit_log_schema_min_fields` (array, minItems=1): requerido si `audit_log_available=true`.
   - `compliance_reqs_confirmed` (array): regulaciones confirmadas por Legal.

5. **`claims_input`:**
   - `required: [claim_id, claim_text, claim_type, proof_strength, expiry_date, owner]` añadido.
   - `proof_strength` (enum: `A, B, C`) añadido como campo primario (KB_18).
   - `proof_type` conservado como alias legible para artefactos.
   - `evidence_link` (string, requerido si proof_strength A o B) añadido.
   - `methodology_disclaimer` (string, requerido si proof_strength C) añadido.
   - `expiry_date`: descripción clarifica que es REQUERIDO para outputs de ventas.

---

### New `needs_clarification` Triggers (añadidos por este patch)

| ID | Trigger | Modo afectado |
|---|---|---|
| NC-P01 | `source_type = UNKNOWN` en cualquier KPI | C, E |
| NC-P02 | `latency_confirmed = false` en cualquier KPI | C, E |
| NC-P03 | `formula_formal` ausente o marcada como `[RELLENAR]` en KPI | D |
| NC-P04 | `rbac_defined = false` o ausente | K |
| NC-P05 | `audit_log_available = true` pero `audit_log_schema_min_fields` ausente | K.2 |
| NC-P06 | Timezone del sistema no confirmada | Global |
| NC-P07 | Regulación de retención aplicable no confirmada explícitamente | K.2 |
| NC-P08 | Combining algorithm ABAC no confirmado | K.1 |
| NC-P09 | Schema registry y compatibility mode no confirmados | L.1 |
| NC-P10 | `compliance_reqs_confirmed` vacío o ausente en security_compliance_input | K |

---

## 7. DoD Checklist

| Criterio | Estado |
|---|---|
| Purpose & Scope definidos | ✅ |
| 12 Operating Modes (A-L) implementados | ✅ |
| Ask-vs-Assume policy documentada | ✅ |
| Input/Output Schemas (JSON) definidos | ✅ |
| Guardrails & Risk Matrix | ✅ |
| Observabilidad & Quality Gates | ✅ |
| Failure Modes & Recovery | ✅ |
| Smoke Tests por cada modo (12) | ✅ |
| Golden Test A — Deduplicación | ✅ |
| Golden Test B — Forecast Dashboard | ✅ |
| Referencias por modo a KB fuente | ✅ |
| COMPILATION_NOTES.md generado | ✅ |
| Sin datos inventados | ✅ |
| needs_clarification declarados (no inventados) | ✅ |
| Facts vs Inferences etiquetados en golden tests | ✅ |
