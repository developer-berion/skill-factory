<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_03 — Patrones avanzados de data tables/listas + A11y WCAG (Enterprise)

## Executive summary (10–15 líneas)

- **Objetivo**: diseñar tablas/listas enterprise con filtros, acciones masivas, selector de columnas e inline edit, sin romper accesibilidad ni velocidad operativa.
- (Facts) WCAG 2.2 define criterios verificables y agnósticos de tecnología para accesibilidad web (Recomendación W3C, 11-dic-2024). (Fecha: 2026-02-16)[^1]
- (Facts) Para tablas de datos, es clave preservar semántica y relaciones (encabezados/estructura) para lectores de pantalla y navegación. (Fecha: 2026-02-16)[^2][^3]
- (Inferences) En enterprise CRM, el “power user” vive en listas: si el grid no es 100% teclado y predecible, suben errores, baja throughput y aparecen atajos “por fuera” (exportar/Excel).
- (Facts) Todo lo operable debe poder hacerse por teclado, salvo interacciones que dependan del trazo/ruta (SC 2.1.1). (Fecha: 2026-02-16)
- (Facts) Debe existir un modo donde el foco sea visible (SC 2.4.7). (Fecha: 2026-02-16)[^4]
- (Inferences) En features “avanzadas” el riesgo real no es visual: es focus management, anuncios (sort/selection/edit), y consistencia de modelo mental (qué afecta al dataset completo vs la página actual).
- (Facts) En paginación, si el usuario filtra u ordena, aplícalo al conjunto completo y vuelve a la primera página de resultados. (Fecha: 2026-02-16)[^5]
- (Facts) ARIA Grid/Data Grid tiene ejemplos con sort, edición y show/hide; útil pero complejo. (Fecha: 2026-02-16)[^6]
- (Inferences) Regla práctica: “HTML `<table>` primero; ARIA grid solo si de verdad necesitas interacción tipo spreadsheet”.

***

## Definitions and why it matters

- (Facts) **Data table**: información tabular (filas/columnas) que debe expresarse con el elemento `table` y encabezados `th` (con `scope`) más `caption` cuando aplique, para que la relación entre celdas sea entendible por AT. (Fecha: 2026-02-16)[^3][^2]
- (Facts) **Grid (ARIA)**: patrón interactivo para presentación tabular con soporte de teclado y estados ARIA (p. ej., `aria-sort`, `aria-colcount`, `aria-rowindex`) en implementaciones avanzadas. (Fecha: 2026-02-16)[^6]
- (Inferences) **Lista enterprise (CRM)**: “la pantalla de trabajo” donde se priorizan throughput (teclado), control de riesgo (bulk actions), y trazabilidad (qué cambió, dónde y por qué).

**Por qué importa (enterprise)**

- (Facts) El orden de foco debe seguir significado/operabilidad (SC 2.4.3), o el grid se vuelve “imposible” para teclado y lectores de pantalla. (Fecha: 2026-02-16)[^7]
- (Inferences) Si tu tabla soporta filtros/sort/edición, cada acción puede reordenar DOM/datos: sin reglas claras de foco y anuncios, generas errores silenciosos (editar el registro equivocado, aplicar bulk a selección incorrecta).

***

## Principles and best practices (con citas por sección + fecha)

### 1) Semántica primero: table vs grid

- (Facts) Usa `<table>` para datos en filas/columnas; marca encabezados con `th` y `scope`, y usa `caption` para describir la tabla. (Fecha: 2026-02-16)[^2][^3]
- (Facts) “ARIA grid” puede ser un anti‑pattern si se usa cuando un `<table>` alcanza, porque añade carga de foco/teclado y compatibilidad AT. (Fecha: 2026-02-16)[^8]
- (Inferences) Criterio de decisión: si no necesitas navegación por celdas tipo spreadsheet, edición por celda, o virtualización compleja con interacción rica, quédate en `<table>` + controles externos (más simple, más robusto).


### 2) Teclado y foco: sin esto, todo falla

- (Facts) Toda funcionalidad debe ser operable por teclado (SC 2.1.1), incluyendo equivalentes a acciones con puntero. (Fecha: 2026-02-16)
- (Facts) Debe existir un modo con indicador de foco visible para elementos operables por teclado (SC 2.4.7). (Fecha: 2026-02-16)[^4]
- (Facts) El foco secuencial debe seguir un orden consistente con significado/operación (SC 2.4.3). (Fecha: 2026-02-16)[^7]
- (Inferences) Regla operativa: después de aplicar filter/sort/bulk/edit, el foco vuelve a un punto “estable” (toolbar de tabla, encabezado de columna activa, o la fila afectada), nunca “desaparece”.


### 3) Sorting: estado anunciable y reversible

- (Facts) Para tablas/encabezados ordenables, `aria-sort` en `th` comunica a lectores de pantalla el estado (none/ascending/descending). (Fecha: 2026-02-16)[^9][^6]
- (Inferences) Patrón enterprise: 3 estados por columna (none → asc → desc) + un “Reset sort” global; muestra el criterio activo cerca del título para evitar “orden fantasma”.
- (Inferences) Evita ordenar “al enfocar” (focus) un header: que sea explícito (Enter/Espacio o botón).


### 4) Filters: claridad de alcance + costo de cambio

- (Facts) Si el usuario filtra u ordena, aplícalo al conjunto completo y redirígelo a la primera página del nuevo resultado (consistencia en listas largas). (Fecha: 2026-02-16)[^5]
- (Facts) Hay fricción conocida: en componentes de filtros, el usuario (teclado) puede tener que volver arriba para “Aplicar”, lo cual no necesariamente es “fallo WCAG”, pero sí un problema de usabilidad a considerar. (Fecha: 2026-02-16)[^10]
- (Inferences) “Incluye / no incluye / sensible” (para vender internamente el patrón):
    - Incluye: chips de filtros activos, botón “Limpiar”, conteo de resultados actualizado.
    - No incluye: auto‑apply agresivo en cada tecla si tu backend es lento o el dataset es grande (genera jitter/foco inestable).
    - Sensible: filtros dependientes (A cambia opciones de B) → debes anunciar cambios y evitar que el foco quede en opciones desaparecidas.


### 5) Bulk actions: selección confiable (y auditable)

- (Facts) El grid pattern contempla estructuras y atributos para datasets grandes/virtualizados (p. ej., `aria-rowcount`, `aria-rowindex`) cuando no todo está en el DOM. (Fecha: 2026-02-16)[^11]
- (Inferences) Patrón recomendado:
    - Checkbox por fila + “Seleccionar todo” (con estado indeterminado cuando aplica) + barra de acciones contextual con “X seleccionados”.
    - Diferencia explícita: “Seleccionar todo en esta página” vs “Seleccionar todo en el resultado (N)” (evita riesgo operativo).
    - Para acciones destructivas: confirmación + resumen de alcance (cuántos, filtros activos).


### 6) Column chooser (show/hide): personalización sin perder contexto

- (Facts) APG muestra ejemplos de grid con funciones avanzadas como show/hide. (Fecha: 2026-02-16)[^6]
- (Inferences) Buenas prácticas:
    - Selector de columnas como diálogo/popover con búsqueda; cada columna como checkbox con nombre claro.
    - “Recomendadas” vs “Opcionales” (para no romper lectura mínima).
    - Persistencia por usuario/rol; botón “Restaurar default del equipo” (evita soporte eterno).


### 7) Inline edit: predecible, no sorpresivo

- (Facts) En WCAG, no deben ocurrir cambios de contexto inesperados al interactuar con inputs sin confirmación (SC 3.2.2 On Input). (Fecha: 2026-02-16)[^12]
- (Facts) APG incluye ejemplos de grid con content editing. (Fecha: 2026-02-16)[^6]
- (Inferences) Dos modos válidos (elige uno y estandariza):
    - Opción segura: “Editar” abre modo edición de fila (con Guardar/Cancelar) y valida al guardar.
    - Opción agresiva: edición por celda + auto-save; solo si tienes latencia baja, control de errores excelente y UX de conflictos (optimistic locking) madura.

***

## Examples (aplicado a CRM enterprise)

### Ejemplo A: Lista de Oportunidades (ventas B2B)

- (Facts) Debes garantizar operación completa por teclado (SC 2.1.1) y foco visible (SC 2.4.7). (Fecha: 2026-02-16)[^4]
- (Inferences) Implementación: filtros por etapa/owner/fecha; sort por “Monto” y “Última actividad”; bulk “Asignar owner” y “Cambiar etapa”; column chooser para “Margen estimado”, “Riesgo” y “SLA”.


### Ejemplo B: Tabla de Actividades (seguimiento)

- (Facts) Preserva relaciones en tablas (encabezados y estructura) para que AT entienda qué columna/valor estás leyendo (SC 1.3.1). (Fecha: 2026-02-16)[^3]
- (Inferences) Inline edit solo en “Estado” y “Fecha próxima”; todo lo demás abre detalle (reduce errores). Al filtrar, vuelve a página 1 y conserva chips activos visibles (evita “¿por qué desaparecieron filas?”).

***

## Metrics / success signals

- (Facts) Si el foco/orden de foco no es consistente, incumples la intención de SC 2.4.3 y afectas operabilidad real para teclado. (Fecha: 2026-02-16)[^7]
- (Inferences) Métricas útiles (enterprise):
    - Throughput: tiempo para “filtrar → seleccionar 20 → aplicar acción masiva” (p50/p95).
    - Error rate: deshacer/cancelar, acciones aplicadas a registro incorrecto, “bulk accidental”.
    - A11y: % de flujos críticos completos solo con teclado; hallazgos por SC (2.1.1, 2.4.7, 1.3.1, 3.2.2).
    - Soporte: tickets “lista no cuadra”, “se me movió”, “perdí selección”.

***

## Operational checklist

- (Facts) Checklist base de tablas: usa `table`, `th` con `scope`, y `caption` cuando describa el contenido; esto soporta comprensión por AT. (Fecha: 2026-02-16)[^2][^3]


### A11y checklist específico (data tables enterprise)

- (Facts) Teclado: toda funcionalidad operable por teclado (SC 2.1.1). (Fecha: 2026-02-16)
- (Facts) Foco visible: indicador de foco presente en modo teclado (SC 2.4.7). (Fecha: 2026-02-16)[^4]
- (Facts) Orden de foco lógico y estable (SC 2.4.3). (Fecha: 2026-02-16)[^7]
- (Facts) Estructura: encabezados correctamente asociados a celdas (técnicas como `scope`, `headers/id`) para SC 1.3.1. (Fecha: 2026-02-16)[^3]
- (Facts) Sorting: expón estado con `aria-sort` (none/ascending/descending) en encabezados cuando exista ordenamiento. (Fecha: 2026-02-16)[^9][^6]
- (Facts) Virtualización/datasets grandes (si usas ARIA grid): considera `aria-rowcount`/`aria-rowindex` para representar filas no renderizadas. (Fecha: 2026-02-16)[^11]
- (Facts) Inline edit: evita cambios de contexto inesperados “on input” sin confirmación (SC 3.2.2). (Fecha: 2026-02-16)[^12]


### Checklist funcional (patrones avanzados)

- (Inferences) Filters: define alcance (“aplica al resultado completo”), muestra filtros activos (chips), botón “Limpiar”, y comportamiento claro de paginación.
- (Inferences) Bulk actions: diferencia “página” vs “resultado completo”, confirma destructivos, muestra conteo seleccionado y mantiene selección al paginar cuando sea seguro.
- (Inferences) Column chooser: nombres consistentes con headers, previews o descripción corta, persistencia por usuario, y “restaurar defaults”.
- (Inferences) Inline edit: Guardar/Cancelar explícito (seguro) o auto-save con rollback visible (agresivo), sin perder foco ni saltar de fila.

***

## Anti-patterns

- (Facts) Usar ARIA grid donde un `<table>` funcionaba suele añadir complejidad y puede ser anti‑pattern. (Fecha: 2026-02-16)[^8]
- (Facts) Fallas comunes incluyen desorden de foco/operación con teclado y ocultar/quitar foco por script (relacionado con requisitos de teclado y foco visible). (Fecha: 2026-02-16)
- (Inferences) Anti‑patterns típicos en enterprise:
    - Sort que se activa por hover/focus (sorpresivo), o que no muestra estado actual.
    - Filtros que aplican solo a la página actual (inconsistencia, “me estafa la lista”).
    - Bulk “Select all” ambiguo (no dice si es página vs resultado) → riesgo operativo.
    - Inline edit que dispara validación/guardado al tabear sin intención.

***

## Diagnostic questions

- (Facts) ¿Puedes completar todas las funciones solo con teclado (SC 2.1.1) y con foco visible (SC 2.4.7)? (Fecha: 2026-02-16)[^4]
- (Facts) ¿La estructura de la tabla expone correctamente relaciones (headers/estructura) para AT (SC 1.3.1)? (Fecha: 2026-02-16)[^3]
- (Inferences) Preguntas “de operación enterprise”:
    - Cuando filtras/sorteas, ¿queda clarísimo qué cambió y qué alcance tiene (dataset vs página)?
    - ¿Qué pasa con la selección cuando el resultado cambia (por filtro/sort/paginación)? ¿Es a prueba de errores?
    - Si falla un inline edit (validación/permiso/timeout), ¿el usuario entiende qué pasó y puede recuperar sin perder contexto?

***

## Sources (o referencia a SOURCES.md)

- Web Content Accessibility Guidelines (WCAG) 2.2 (W3C Recommendation, 11-dic-2024).[^1]
- Understanding SC 2.1.1 Keyboard (WCAG 2.2).
- Understanding SC 2.4.7 Focus Visible (WCAG 2.2).[^4]
- Understanding SC 1.3.1 Info and Relationships (técnicas para tablas: `scope`, `headers/id`).[^3]
- Understanding SC 2.4.3 Focus Order (WCAG 2.2).[^7]
- WAI-ARIA APG — Data Grid examples (incluye sort, edición, show/hide).[^6]
- WAI-ARIA Practices — ejemplos con `aria-rowcount`/`aria-rowindex` (datasets no completos en DOM).[^11]
- GOV.UK Design System — paginación: filtros/sort aplican al total y vuelven a página 1.[^5]
- ONS Design System — tabla ordenable con `aria-sort`.[^9]
- Adrian Roselli — “ARIA Grid as an anti-pattern”.[^8]
- A11Y Project checklist — buenas prácticas de tablas (`table`, `th`, `scope`, `caption`).[^2]
- WCAG quick reference — SC 3.2.2 On Input (predictibilidad/cambios de contexto).[^12]

**Añadir a `SOURCES.md` (sin duplicados)**

- https://www.w3.org/TR/WCAG22/[^1]
- https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html
- https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html[^4]
- https://www.w3.org/WAI/ARIA/apg/patterns/grid/examples/data-grids/[^6]
- https://adrianroselli.com/2020/07/aria-grid-as-an-anti-pattern.html[^8]

***

## Key takeaways for PM practice

- La tabla enterprise “se vende” por control: alcance explícito (dataset vs página), foco estable, y acciones masivas a prueba de errores.
- Si puedes resolverlo con `<table>` + controles, hazlo; ARIA grid solo cuando el ROI (edición por celda/virtualización) sea real.
- Define dos perfiles de implementación: opción segura (más confirmaciones, menos sorpresa) vs agresiva (auto-save, alta velocidad) y decide según latencia, riesgo y madurez operativa.
<span style="display:none">[^13][^14][^15][^16]</span>

<div align="center">⁂</div>

[^1]: https://www.w3.org/TR/WCAG22/

[^2]: https://www.a11yproject.com/checklist/

[^3]: https://www.w3.org/WAI/WCAG21/Understanding/info-and-relationships.html

[^4]: pasted-text.txt

[^5]: https://design-system.service.gov.uk/components/pagination/

[^6]: https://www.w3.org/WAI/ARIA/apg/patterns/grid/examples/data-grids/

[^7]: https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html

[^8]: https://adrianroselli.com/2020/07/aria-grid-as-an-anti-pattern.html

[^9]: https://service-manual.ons.gov.uk/design-system/components/table

[^10]: https://design-patterns.service.justice.gov.uk/components/filter/

[^11]: https://wai-aria-practices.netlify.app/aria-practices/examples/grid/layoutgrids

[^12]: https://guia-wcag.com/en/

[^13]: https://www.w3.org/WAI/WCAG22/Techniques/

[^14]: https://reciteme.com/us/news/understanding-the-web-content-accessibility-guidelines-wcag/

[^15]: https://www.section508.gov/develop/guide-accessible-web-design-development/

[^16]: https://www.w3.org/TR/2021/NOTE-wai-aria-practices-1.2-20211129/

