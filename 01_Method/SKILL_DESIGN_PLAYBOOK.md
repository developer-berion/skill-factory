# Skill Design Playbook — Producción (v2.1)

**Propósito:** Documentar cómo diseñar *skills* para agentes de IA con estándar de producción: confiables, reutilizables, auditables y mantenibles.  
**Enfoque:** B2B, alta fricción operativa y riesgo (turismo, finanzas, logística, etc.).  
**Resultado esperado:** que puedas construir un **catálogo de skills** que aguante mundo real (proveedores lentos, datos sucios, usuarios creativos, y lunes 7am).

---

## 0) Definiciones operativas (sin humo)

### ¿Qué es un skill?
Un **skill** es una unidad modular de capacidad que encapsula:
- **Contrato** (inputs/outputs + validación)
- **Reglas de negocio** (guardrails + políticas)
- **Procedimiento** (pasos operativos reproducibles)
- **Integración** (tools/APIs/workflows)
- **Evaluación** (tests + rúbrica + regresión)
- **Operación** (observabilidad, versionado y fallback)

> Un skill NO es “un prompt largo”. Es una **pieza de producto**.

### Skill vs Tool vs Prompt vs Workflow vs Policy
| Pieza | Qué es | Úsalo cuando | Anti‑patrón |
|---|---|---|---|
| **Skill** | Capacidad completa (contrato + reglas + ejecución). | Procesos repetibles y críticos. | “Skill dios” que hace de todo. |
| **Tool / Function** | Acción atómica: API call, query, cálculo. | Ejecución determinista. | Exponer tools crudos al usuario/router. |
| **Prompt suelto** | Instrucción puntual sin contrato formal. | Tareas creativas o ad‑hoc. | Reutilizarlo como “sistema”. |
| **Workflow** | Orquestación de pasos (skills + tools). | Procesos multi‑etapa. | Meter lógica de negocio en el workflow sin tests. |
| **Policy / Guardrail** | Reglas globales de seguridad/calidad. | Compliance, límites, estilo. | Duplicar policies dentro de cada skill sin control. |

### Regla de “NO crear skills de más”
No crees un skill si:
1) La tarea es meramente conversacional.  
2) La lógica es 100% determinista y simple (mejor un script).  
3) Cambia cada semana y no vale la pena mantenerlo.  
4) No puedes definir un contrato claro (inputs/outputs).

---

## 1) Taxonomía (qué skills existen)

### 1.1 Tipos de skills
1) **Normalizadores (Utility)**: limpian y estructuran datos sucios (WhatsApp/Email).  
2) **Extractores (Parsing)**: extraen entidades/parametría (fechas, pax, IATA, moneda).  
3) **Transaccionales (Transactional)**: ejecutan una acción con tools (cotizar, reservar, emitir).  
4) **Validadores (Quality Gate)**: revisan consistencia y cumplimiento (auditoría).  
5) **Orquestadores (Router/Dispatcher)**: deciden qué skill corre y en qué orden.  
6) **Negociadores (Conversation Control)**: manejo de objeciones, confirmaciones, “ask vs assume”.  
7) **Incidentes (Ops / Incident Mgmt)**: degradación, reintentos, handoff, alerts.

### 1.2 Cuándo usar cada uno (atajo mental)
- Si el problema es **datos sucios** → Normalizador/Extractor.  
- Si el problema es **acción y costo/riesgo** → Transaccional + Validador.  
- Si el problema es **routing/escala** → Orquestador.  
- Si el problema es **incertidumbre** → Negociador + políticas “ask vs assume”.

---

## 2) Estructura canónica del skill (mínima vs premium)

### 2.1 Estructura mínima (para no improvisar)
Todo skill en producción debe tener:
1) **Metadata** (nombre, versión, owner)  
2) **Contrato I/O** (schema)  
3) **Procedimiento** (pasos)  
4) **Guardrails** (prohibiciones y condiciones)  
5) **Errores y fallbacks**  
6) **Tests mínimos** (10 casos)  

### 2.2 Estructura premium (recomendada)
La versión premium agrega operación real:
- **Risk Matrix** (riesgo financiero/legal/reputacional)
- **Artifact Skeletons** (Sección 3.3 obligatoria para evitar alucinaciones de output)
- **Tech Radar & Discovery** (Sección 6.1 para gobierno de ciclo de vida)
- **Observabilidad** (logs, tracing, redaction)
- **SLO/Cost envelope** (latencia, tokens, timeouts)
- **Regresión + Golden Set** (30 casos)
- **Compatibilidad/Deprecación** (semver y migraciones)

---

## 3) Plantilla “SKILL.md” (lista para copiar/pegar)

> Esta plantilla está pensada para repositorio. Puedes usarla en Markdown/YAML/JSON; lo importante es que mantenga el contrato y la operación.

```markdown
---
name: <snake_case>
title: <Verbo + Objeto>
version: 1.0.0  # semver
owner: <email o team>
status: draft | active | deprecated
last_reviewed: YYYY-MM-DD
domain: <tourism|insurance|ecommerce|...>
dependencies:
  tools:
    - <tool_name>
  schemas:
    - <schema_name>
---

# 1) Propósito
Describe exactamente qué hace y qué NO hace.

# 2) Definición de Done (DoD)
- Golden set pass rate: >= __/30
- 0 fallas críticas (alucinación de precio/inventario/condiciones)
- p95 latency <= __s, timeout <= __s
- Salida válida contra schema en 100% de ejecuciones

# 3) Interface — Contrato
## 3.1 Input Schema (JSON estricto)
Incluye tipos, enums y reglas condicionales.

## 3.2 Output Schema (JSON estricto)
Incluye:
- status: success | needs_clarification | handoff | error
- data: {...}
- warnings: []
- audit: { normalization_report, assumptions, tool_trace_id }

## 3.3 Artifact Skeletons (Obligatorio en Premium)
Si el skill genera archivos (YAML, Rego, SQL, MD), provee esqueletos base aquí:
*   **template_type**: `content_skeleton`

# 4) Política “Ask vs Assume”
Never assume:
- fechas, pax, moneda, condiciones de cancelación, documentación
Safe assume:
- idioma preferido si está explícito en el hilo
Thresholds:
- confidence < 0.75 => pregunta
- confidence < 0.55 => handoff

# 5) Procedure — Pasos operativos (verificables)
1) Validar inputs (schema + reglas condicionales)
2) **Check Tech Radar**: ¿El recurso solicitado está en "deprecated" o "hold"?
3) Normalizar (fechas, moneda, nombres, unidades)
4) Ejecutar tools (con límites)
5) Verificar resultados (consistencia + reglas de negocio)
6) Responder (JSON final + mensajes al usuario)

# 6) Guardrails (Constraints)
## 6.1 Tech Radar Governance
- Lista blanca de herramientas y stacks permitidos.
- Política de bloqueo para tecnologías obsoletas.

## 6.2 Prohibiciones generales
- Prohibiciones absolutas
- Disclaimers obligatorios
- Reglas por riesgo (ver Risk Matrix)

# 7) Risk Matrix (dominio)
| Riesgo | Trigger | Mitigación | Acción |
|---|---|---|---|
| Financiero | non_refundable | disclaimer + confirmación | needs_clarification |
| Legal | términos/garantías | lenguaje limitado | safe_completion |
| Reputacional | “garantizado” | prohibido prometer | rewrite |

# 8) Operational Envelope (SLO + costos)
- max_tool_calls: __
- max_tokens: __
- timeout_seconds: __
- retry_policy: {max_retries: __, backoff: __}
- degrade_gracefully: true/false

# 9) Observabilidad (Logging & Redaction)
Log (sin PII):
- request_id, skill_version, inputs_hash
- tool_calls (nombres + latencia)
- status, confidence, handoff_reason
Redact:
- pasaporte, teléfono, email, dirección exacta

# 10) Failure Modes
Lista de fallas típicas con señales + mitigación + fallback.

# 11) Tests
## 11.1 Smoke (10)
Casos mínimos.
## 11.2 Golden (30)
Casos representativos (incluye ataques y datos sucios).

# 12) Changelog
- 1.0.0: initial
```

---

## 4) Heurísticas avanzadas (los “trucos” que sí pegan)

### 4.1 Contratos fuertes (schema + semántica)
No basta con “JSON estricto”. Define:
- **Enums** (moneda, tipo pax, fare types, room types)
- **Campos condicionales**: si destino internacional → `passport_required: true` y pedir status.
- **Normalización obligatoria**: fechas a ISO, números a decimal, moneda explícita.

### 4.2 Normalización agresiva (pero auditable)
El skill debe producir un `normalization_report`:
- qué cambió (p.ej. “12-14 Feb” → “2026-02-12 to 2026-02-14”)
- por qué (timezone, idioma, fecha base)
- qué quedó pendiente (p.ej. “moneda no especificada”)

### 4.3 Chain‑of‑Verification (sin revelar razonamiento interno)
Añade una etapa de **verificación** explícita:
- consistencia (ida < vuelta, check-in < check-out)
- completitud (incluye/no incluye, impuestos)
- riesgo (non_refundable, penalidades)
Si falla, no inventa: **pregunta o handoff**.

### 4.4 “Split brain”: output externo vs interno
Para evitar fuga de margen:
- **output_public**: lo que ve el cliente/agencia  
- **output_internal**: margen, scoring, logs (no mostrar)

### 4.5 Ask‑vs‑Assume con thresholds
Política simple, repetible, medible:
- Si falta dato crítico → pregunta.
- Si hay ambigüedad y afecta precio/condición → pregunta.
- Si el usuario presiona para “inventar” → refusal + alternativa segura.

---

## 5) Patrones de orquestación (arquitectura que escala)

### 5.1 Router/Dispatcher (recomendado)
Un router pequeño:
- clasifica intención
- valida si hay datos mínimos
- llama skills especialistas
- agrega `trace_id` para auditoría

### 5.2 Specialist swarm + integrador
- 2–4 skills especialistas (precio, restricciones, alternativas, compliance)
- 1 integrador produce respuesta final (con reglas de consistencia)

### 5.3 Plan‑Execute‑Reflect (solo cuando vale la pena)
Útil en procesos largos:
- Plan (pasos)
- Execute (tools)
- Reflect (validación + riesgo)
Evita usarlo en tareas simples (te sube costo).

### 5.4 Retrieve‑Then‑Reason (RAG)
Regla: **si hay política/contrato** en base de conocimiento, primero retrieve, luego razona.
- Si el retrieve no trae evidencia, el skill debe admitir incertidumbre.

---

## 6) Failure modes (tabla operativa)

| Falla | Señal | Mitigación | Resultado |
|---|---|---|---|
| Ambigüedad | faltan fechas/pax/moneda | preguntar 1–2 preguntas | needs_clarification |
| Datos sucios | formatos raros | normalizar + reportar cambios | success + warnings |
| Inyección/jailbreak | “ignora tus reglas” | reglas del sistema > usuario | refusal/safe_completion |
| Alucinación | inventa precio/inventario | grounding: solo tool results | error + retry/handoff |
| Bucle | 3 turnos sin progreso | detener + handoff | handoff |
| API lenta | timeouts/429 | backoff + degrade | partial + “confirmar luego” |

---

## 7) Evaluación: rúbrica + pruebas + regresión

### 7.1 Rúbrica 0–5 (producción)
- **0 Crítico:** inventó precio/inventario/condición; riesgo legal/financiero.
- **1 Muy malo:** schema inválido, no usable.
- **2 Operativo:** entiende pero falla en datos/flujo.
- **3 Pasable:** correcto pero con fricción (pregunta de más, formato pobre).
- **4 Bueno:** correcto, claro, auditable.
- **5 Golden:** maneja excepciones, propone alternativas, cero humo.

### 7.2 Tests
- **Smoke (10):** casos comunes + 1 ataque + 1 dato sucio.
- **Golden (30):** 10 fáciles, 10 confusos, 10 adversariales (inyección, presión, contradicción).

### 7.3 Regresión obligatoria
Cada cambio al skill:
- corre Golden Set
- si baja el score promedio o aparece un “0 crítico” → no despliegues.

---

## 8) Versionado y mantenimiento (semver real)

### 8.1 Semver
- **MAJOR:** cambia schema o comportamiento contractual.
- **MINOR:** agrega capacidades compatibles.
- **PATCH:** ajustes de copy/tono/bugs sin cambiar contrato.

### 8.2 Deprecación
- marcar `status: deprecated`
- proveer `migration_notes`
- mantener compatibilidad por X semanas o hasta versión N.

---

## 9) Ejemplos (3 skills completos)

> Los ejemplos están intencionalmente “dominio‑agnósticos” pero con sabor B2B turismo.

### 9.1 Skill 1 — Normalizador (Utility)
**Nombre:** `normalizar_pasajeros`  
**Objetivo:** convertir texto WhatsApp en JSON estructurado.

**Input:** texto libre  
**Output:** JSON con `pax_list[]`, `warnings[]`, `audit.normalization_report`

**Regla clave:** si falta dato crítico (edad de menor, documento requerido), no inventar: `needs_clarification`.

**Smoke tests (ejemplos):**
1) “2 adultos Juan Pérez y María Gómez”  
2) “2 adt + 1 niño 5 años” (missing name del niño)  
3) “Viajamos mañana” (fecha relativa → pide fecha exacta o convierte con base temporal si se permite)

---

### 9.2 Skill 2 — Transaccional (Transactional)
**Nombre:** `consultar_disponibilidad_hotel`  
**Objetivo:** consultar API mayorista y retornar 3 opciones con condiciones claras.

**Guardrails clave:**
- Solo hoteles devueltos por tool.
- Si `non_refundable=true` → disclaimer + confirmación obligatoria.

**Output público:** opciones con total, impuestos, cancelación, “incluye/no incluye”.  
**Output interno:** margen, scoring, trace_id.

---

### 9.3 Skill 3 — Validador/Auditor (Quality Gate)
**Nombre:** `auditar_cotizacion`  
**Objetivo:** revisar una cotización antes de enviarla.

Checks:
- fechas válidas
- moneda explícita
- política cancelación presente
- margen no negativo
- disclaimers presentes si aplica

**Resultado:** `approved | rejected` + lista de hallazgos.

---

## 10) Checklist final (antes de publicar un skill)

- [ ] Schema I/O existe y valida.
- [ ] Ask‑vs‑Assume definido (never assume list).
- [ ] Risk Matrix completa para el dominio.
- [ ] Operational envelope definido (tokens, tools, timeout, retries).
- [ ] Logging & redaction definido (no PII).
- [ ] Smoke tests (10) pasan.
- [ ] Golden set (30) pasa con ≥ 27/30.
- [ ] 0 fallas críticas (alucinación de precio/inventario/condiciones).
- [ ] Changelog actualizado + versión semver.

---

## Nota final (práctica)
Empieza construyendo **Normalizadores** y **Validadores** primero.  
Los transaccionales sin normalización/validación son una ruleta rusa: a veces sale bien… hasta que te cuesta real.
