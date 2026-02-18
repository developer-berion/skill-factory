# KB_INDEX — CRM Web UX/UI Expert (Enterprise, 2026)

## 0) Qué es esta KB
Base de conocimiento para diseñar y evaluar UX/UI de **CRMs web B2B enterprise** (2026): IA, record pages, tablas/listas, flujos de alta frecuencia, personalización por **rol + lugar/territorio**, gobernanza/seguridad (RBAC/auditoría), accesibilidad, IA asistiva, métricas e instrumentación, onboarding, búsqueda global y resiliencia/performance.

**Regla de oro:** toda recomendación debe estar soportada por evidencia en estos KBs. Si falta, se marca `needs_clarification`.

---

## 1) Mapa de archivos (source of truth)

### Núcleo CRM (IA + pantallas clave)
- **KB_01_CRM_IA_Enterprise.md**  
  IA (arquitectura de información) en CRMs web enterprise: navegación por objetos vs tareas, escalabilidad multi-rol, búsqueda, taxonomía.
- **KB_02 — Diseño de record pages (CRM enterprise).md**  
  Record page “power user”: above-the-fold, timeline, asociaciones, tabs, side-panels, métricas UX.
- **KB_03 — Patrones avanzados de data tables_listas +.md**  
  Tablas/listas enterprise: filtros, bulk actions, inline edit, column chooser, estados, accesibilidad aplicada.
- **KB_04 — Userflows de alta frecuencia en CRM (crear...).md**  
  Flujos high-frequency: crear/editar, logging, mover etapas, tareas, adjuntos, accelerators (shortcuts/command palette).

### Contexto por lugar/territorio (priorización de información)
- **KB_05_Context_By_Location_Territory.md**  
  Modelo “context-aware”: qué mostrar primero según país/ciudad/sucursal/territorio + rol. Reglas de priorización.

### Sistema de diseño + accesibilidad
- **KB_06_Design_Systems_Salesforce_HubSpot.md**  
  Tokens, theming, estados, handoff dev, consistencia enterprise.
- **KB_07_Accessibility_WCAG_for_CRM — Aplicación prác.md**  
  WCAG aplicada a CRM: tablas, forms densos, modals, focus, shortcuts, lectores.
- **KB_08_Forms_Data_Quality_Governance.md**  
  Forms, validaciones, progressive profiling, dedupe, field permissions, data hygiene.

### IA asistiva (2026) + métricas
- **KB_09_AI_Assist_UX_in_CRM_2026.md**  
  Copilots/recomendaciones: sugerir vs actuar, controles de escritura, citación, human-in-the-loop, riesgos.
- **KB_10_Metrics_Instrumentation_Adoption.md**  
  Métricas UX/Producto para CRM: adopción, eficiencia, calidad, funnels, esquema de eventos.

### “Enterprise hard mode” (seguridad, búsqueda, onboarding, resiliencia)
- **KB_11_RBAC_Audit_SafeOps_UX.md**  
  RBAC + Field-level security, acciones sensibles (confirm/diff), audit log visible, undo/restore.  
- **KB_12_Global_Search_Saved_Views_Navigation.md**  
  Búsqueda global, SERP CRM, saved views, filtros compartibles, command palette, métricas de búsqueda.
- **KB_13_Onboarding_EmptyStates_RoleBased_Enablement.md**  
  Onboarding por rol, empty states accionables, progressive disclosure, TTFV, activation loops.
- **KB_14_Performance_Resilience_State_Model.md**  
  Playbook de estados UI (loading/error/empty/skeleton), retries/backoff, optimistic UI, conflictos, offline parcial.

### Bibliografía consolidada
- **SOURCES.md**  
  Fuentes únicas, agrupadas por tema, sin duplicados.

---

## 2) Guía rápida: “qué archivo usar según intención” (router)

### A) Diseñar una Record Page (Account/Deal/Ticket/etc.)
1) KB_02 (layout y jerarquía)
2) KB_03 (tablas y módulos listables dentro del record)
3) KB_07 (a11y)
4) KB_05 (priorización por lugar/territorio)
5) KB_11 (acciones sensibles, permisos, audit)
6) KB_14 (estados, fallos, resiliencia)

### B) Diseñar List Views / Tablas enterprise
1) KB_03
2) KB_12 (saved views + compartir)
3) KB_07 (a11y de tablas)
4) KB_14 (loading/error/empty)

### C) Diseñar Flujos de alta frecuencia
1) KB_04
2) KB_11 (fricción proporcional y confirmaciones)
3) KB_14 (optimistic, retries, conflictos)
4) KB_10 (eventos y métricas)

### D) “Qué info mostrar primero” por lugar/territorio + rol
1) KB_05 (modelo de contexto y pseudoreglas)
2) KB_11 (scope/seguridad visible)
3) KB_10 (medición de impacto)
4) KB_06 (consistencia por variantes)

### E) IA asistiva (copilot) en CRM (2026)
1) KB_09 (política UX de IA)
2) KB_11 (diff, auditoría, permisos, acciones sensibles)
3) KB_10 (métricas de valor)
4) KB_14 (fallos/reintentos y estados)

### F) Búsqueda global + navegación + command palette
1) KB_12
2) KB_03 (tablas de resultados)
3) KB_11 (permisos al compartir vistas/links)

### G) Onboarding / Empty states / Progressive disclosure
1) KB_13
2) KB_10 (TTFV, activation loops)
3) KB_05 (onboarding por región/mercado)
4) KB_11 (permisos vs “no hay data”)

---

## 3) Glosario mínimo (para alinear equipo)
- **Objeto:** entidad principal (Account/Lead/Deal/Ticket/Custom Object).
- **Registro (Record):** instancia de un objeto (ej. Deal #8921).
- **Timeline / Activity feed:** secuencia de eventos/actividades (emails, calls, notas, cambios).
- **List view / Saved view:** vista de tabla con filtros/sorts; puede ser personal o compartida.
- **Scope:** alcance (sucursal/país/territorio/BU) aplicado a datos y permisos.
- **RBAC:** permisos por roles.
- **FLS (Field-level security):** permisos por campo (ver/editar/enmascarado).
- **Acción sensible:** acción con impacto alto (financiero, regulatorio, irreversible).
- **Diff before apply:** previsualización “antes/después” antes de ejecutar cambios riesgosos.
- **TTFV:** time to first value (tiempo hasta el primer valor real por rol).
- **SSR / TTR / ZRR:** métricas de búsqueda (Search Success Rate, Time-To-Record, Zero-results recovery).
- **Optimistic UI:** UI que refleja el cambio antes de confirmación del servidor (con rollback).
- **409 Conflict:** conflicto por edición concurrente.

---

## 4) Matriz Competencias → KB (para compilar skill sin lagunas)

1. Research & Domain Immersion → KB_13 (onboarding/roles), KB_05 (contexto)
2. Information Architecture → KB_01, KB_12
3. Record Page Mastery → KB_02, KB_11, KB_14
4. Data Table & List Experience → KB_03, KB_12, KB_07
5. High-frequency Flows → KB_04, KB_14, KB_11
6. Context-aware UX (lugar/territorio) → KB_05, KB_11
7. Design Systems & Consistency → KB_06
8. Accessibility → KB_07 (+ KB_03/KB_02 como aplicación)
9. Forms & Data Governance UX → KB_08, KB_11
10. AI-assist UX → KB_09, KB_11
11. Performance UX & Resilience → KB_14
12. Metrics & Instrumentation → KB_10 (+ KB_12/KB_13 como casos)

---

## 5) Plantilla de “evidence tags” (recomendado)
Para cada recomendación, etiquetar:
- `role:` Sales Rep / Manager / RevOps / CS / Admin
- `context:` country / city / branch / territory
- `object:` account / contact / deal / ticket / custom
- `risk:` low/med/high (y si es regulatorio)
- `a11y:` keyboard/focus/screenreader/contrast
- `metric:` (KPI principal + evento sugerido)

---
