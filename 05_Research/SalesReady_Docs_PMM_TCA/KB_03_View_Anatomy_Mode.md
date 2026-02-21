<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_03_View_Anatomy_Mode.md

Prompt:
“Define el modo ‘Anatomía de Vista’ para documentación extrema (sin omisiones) de dashboards en CRM.
Incluye:
Checklist exhaustivo (componentes UI, filtros, estados, accesibilidad, microcopy)
KPI Dictionary (definición, fórmula, periodicidad, owner, decisiones)
Buenas prácticas docs-as-code para mantener esto vivo
Citas por sección, priorizando 2025–2026 (docs-as-code, doc portals).”

---

# KB_03 — View Anatomy Mode: Documentación Extrema de Dashboards CRM


***

## Executive Summary

El **Modo Anatomía de Vista** (*View Anatomy Mode*) es un protocolo de documentación exhaustiva que trata cada dashboard o pantalla de CRM como un artefacto viviente, describiendo sin omisiones cada componente UI, estado de datos, filtro, lógica de negocio, regla de acceso y microcopy visible. Su premisa central: si no está documentado, no existe para el equipo que hereda o escala el sistema.

En entornos B2B con alta rotación comercial (agencias de viaje, distribuidores, operadores mayoristas), la pérdida de contexto sobre cómo funciona un dashboard CRM genera decisiones comerciales erróneas, onboarding lento y deuda técnica invisible. Un solo dashboard de pipeline con KPIs mal definidos puede costarle semanas de re-trabajo a un equipo de ventas.

El modo se compone de tres capas: **(1) Anatomía UI** (qué hay en pantalla y cómo se comporta), **(2) Diccionario KPI** (qué mide cada número y quién lo tiene), y **(3) Docs-as-Code** (cómo mantener viva esta documentación sin que se pudra).[^1]

Aplicado a CRM enterprise, este modo transforma el dashboard de "reporte bonito" a "contrato de datos" entre producto, ventas y operaciones.[^2]

> **`[FACT]`** El enfoque docs-as-code integra la documentación en el mismo repositorio que el código, pasando por los mismos pipelines de CI/CD y pull requests.[^1]
> **`[INFERENCE]`** En CRM configurados en plataformas como Zoho, HubSpot o Salesforce, la "documentación" equivale a configuraciones, fórmulas calculadas y reglas de visibilidad que cambian con cada sprint comercial.

***

## Definitions and Why It Matters

**Anatomía de Vista** es la descripción atómica y sin ambigüedad de una pantalla funcional. Va más allá del screenshot: documenta el *contrato de comportamiento* de cada elemento.[^3]

**Docs-as-Code** trata la documentación con el mismo rigor que el software: texto plano (Markdown), control de versiones en Git, publicación automatizada via CI/CD.  Herramientas como MkDocs, Docusaurus y Sphinx implementan este enfoque con integración nativa a GitHub/GitLab.[^4][^1]

**KPI Dictionary** es el catálogo formal de cada métrica del dashboard: su definición de negocio, fórmula exacta, fuente de datos, periodicidad de actualización, owner y decisiones que habilita.[^2]

**¿Por qué importa en CRM enterprise?**

- Los dashboards acumulan lógica de negocio oculta (filtros por defecto, exclusiones, condiciones de fecha) que ningún usuario ve pero que distorsiona los datos si no se documenta.[^5]
- La rotación de equipos comerciales hace que el conocimiento tácito sobre "cómo leer este número" se pierda en semanas.[^2]
- WCAG 2.2 (2025) exige que componentes interactivos sean accesibles; sin documentación de estados, los equipos de QA no pueden validarlo.[^6]

> **`[FACT]`** La documentación close-to-code reduce el "drift" entre lo que el sistema hace y lo que está escrito sobre él.[^7]
> **`[INFERENCE]`** En un mayorista de turismo B2B, el dashboard de cotizaciones activas es probablemente la vista con mayor impacto comercial y menor documentación formal.

***

## Principles and Best Practices

### Principio 1: Documentar el "Por Qué", No Solo el "Qué"

Cada componente debe explicar la *intención de negocio* detrás de su existencia, no solo su nombre. Un widget "Tasa de Conversión" sin contexto de qué embudo mide, en qué rango de fechas y con qué exclusiones, es un KPI vacío.  *(2025-10-24)*[^7]

> **`[FACT]`** El principio "document the why, not just the what" preserva el contexto de decisión y previene errores repetidos en iteraciones futuras.[^7]

### Principio 2: Versionado de Docs junto al Código/Config

Cada cambio en un dashboard (nuevo filtro, cambio de fórmula, nuevo estado) debe ir acompañado de un PR que actualice la documentación. Los dashboards de CRM que se actualizan sin documentar equivalen a código sin tests.  *(2026-01-05)*[^1]

> **`[FACT]`** MkDocs y Docusaurus permiten que la documentación viva en el mismo repo y se publique automáticamente con GitHub Actions.  *(2025-10-30)*[^4]

### Principio 3: Un Owner por KPI, No por Dashboard

La responsabilidad de la veracidad de un KPI debe recaer en una persona, no en el equipo que "usa el dashboard". Sin owner explícito, los KPIs se vuelven datos zombi.  *(2025-12-18)*[^2]

> **`[INFERENCE]`** En estructuras B2B de mayoristas, el owner natural de KPIs comerciales (pipeline, cierre) es el líder de ventas; el de KPIs operativos (tiempo de respuesta, errores de carga) es el líder de operaciones.

### Principio 4: Documentar Estados, No Solo el Estado Ideal

Todo componente UI tiene estados: vacío, cargando, error, parcial, sin permisos. Documentar solo el estado "lleno con datos" es la causa \#1 de bugs de UX no reportados en dashboards CRM.  *(2025-08-16)*[^3]

> **`[FACT]`** Los design systems de referencia (2025) exigen documentar todos los estados de cada componente: default, hover, focus, disabled, error y loading.[^3]

### Principio 5: Microcopy como Contrato de Expectativa

Cada label, tooltip, mensaje de error y texto de estado vacío es microcopy que establece expectativas del usuario. Cambiar "Sin resultados" por "No hay cotizaciones activas este mes" reduce tickets de soporte.  *(2025-12-18)*[^2]

***

## Examples (Aplicado a CRM Enterprise)

### Ejemplo: Dashboard "Pipeline de Ventas B2B" — Mayorista de Turismo

**Contexto:** Vista principal del equipo comercial en Zoho CRM / HubSpot. Muestra oportunidades activas por etapa, valor en USD y proyección del mes.

***

**`[Anatomía UI Completa]`**


| Componente | Tipo | Comportamiento | Estados documentados |
| :-- | :-- | :-- | :-- |
| Header de vista | Texto + ícono | Muestra nombre de vista guardada + botón editar | Default / Edit mode |
| Selector de período | Dropdown | Filtra por mes actual, trimestre, custom range | Default (mes actual), Custom, Sin datos |
| Pipeline Kanban | Board drag-and-drop | Columnas = etapas del funnel; cards = oportunidades | Lleno, Vacío por etapa, Loading, Sin permiso |
| Widget "Valor Total Pipeline" | KPI Card | Suma de deal value en etapas activas | Número positivo, Cero, Error de cálculo |
| Tabla de detalle | Data grid | Sortable, filtrable por agencia/destino/vendedor | Lleno, Vacío, Paginado, Export disponible |
| Botón "Nueva Oportunidad" | CTA primario | Abre modal de creación | Enabled, Disabled (sin permisos), Loading |
| Filtro "Vendedor" | Multi-select | Filtra todas las vistas de la pantalla | Sin selección = todos; error si usuario inactivo |

**Microcopy crítico:**

- Estado vacío Kanban: *"No hay oportunidades en esta etapa. ¿Quieres agregar una?"* → debe linkearse a acción.
- Tooltip en "Valor Total Pipeline": *"Suma de deal value en etapas 2–5. Excluye etapa Cerrado-Perdido."*[^2]

***

## KPI Dictionary

Plantilla estándar por cada métrica del dashboard:


| Campo | Descripción |
| :-- | :-- |
| **Nombre** | Nombre visible en pantalla |
| **Definición** | Qué mide en términos de negocio |
| **Fórmula** | Expresión matemática o lógica exacta |
| **Fuente de datos** | Módulo/objeto CRM o tabla de origen |
| **Periodicidad** | Frecuencia de actualización (real-time, diario, mensual) |
| **Owner** | Cargo responsable de validar veracidad |
| **Decisiones habilitadas** | Qué acción de negocio activa este dato |
| **Exclusiones** | Registros o condiciones que no se cuentan |
| **Alerta / umbral** | Valor que dispara revisión manual |

**Ejemplo aplicado — KPI "Tasa de Conversión Cotización→Venta":**


| Campo | Valor |
| :-- | :-- |
| **Nombre** | Conv. Rate Cotización→Venta |
| **Definición** | % de cotizaciones enviadas que se convierten en reserva confirmada |
| **Fórmula** | `(Reservas confirmadas / Cotizaciones enviadas) × 100` — en el período seleccionado |
| **Fuente de datos** | Módulo Deals; status = "Cotización Enviada" y "Reserva Confirmada" |
| **Periodicidad** | Diario (actualiza a las 06:00 UTC-4) |
| **Owner** | Gerente Comercial |
| **Decisiones** | Ajuste de pricing, training de vendedores, revisión de propuesta |
| **Exclusiones** | Cotizaciones canceladas por el cliente antes de 24h; grupos +20 PAX (flujo diferente) |
| **Umbral** | < 18% → revisión de proceso; < 10% → escalamiento directo |

> **`[FACT]`** El framework SMART para KPIs exige que cada indicador sea Específico, Medible, Alcanzable, Relevante y con marco temporal definido.  *(2025-12-18)*[^2]
> **`[INFERENCE]`** En mercados LATAM con alta volatidad (Venezuela/Colombia), la periodicidad "mensual" puede ser insuficiente para KPIs de conversión; se recomienda revisión semanal mínima.

***

## Docs-as-Code: Mantener la Documentación Viva

### Stack Recomendado (2025–2026)

| Herramienta | Rol | Ideal para |
| :-- | :-- | :-- |
| **MkDocs + Material Theme** | Static site generator | Documentación interna versionada, hosting en GitHub Pages [^4] |
| **Docusaurus** | Portal de docs + versioning | Equipos con múltiples releases de CRM config [^4] |
| **Mermaid.js** | Diagramas as-code | Flujos de datos, estados de UI, arquitectura de vistas [^8] |
| **GitHub Actions** | CI/CD de docs | Auto-deploy en cada PR aprobado [^7] |
| **Confluence + Jira** | Wiki corporativo | Org grandes con stack Atlassian; links directos a tickets [^4] |

### Flujo Operativo Recomendado

1. **Cada cambio en el dashboard** genera un ticket (Jira/Linear) con campo "¿Requiere actualización de docs?"
2. El PR de configuración del CRM incluye un commit en `/docs/views/` con el archivo `.md` actualizado[^7]
3. GitHub Actions valida que el Markdown tiene las secciones obligatorias (linter de estructura)[^1]
4. La doc se publica automáticamente al merge del PR  *(2025-10-27)*[^9]
5. Owner del KPI recibe notificación si su métrica fue modificada

> **`[FACT]`** La integración Git ↔ docs-as-code garantiza que actualizaciones de documentación pasen por el mismo proceso de revisión y aprobación que el código.[^9]

***

## Metrics / Success Signals

Indicadores para saber si tu View Anatomy Mode está funcionando:


| Métrica | Señal de éxito | Frecuencia |
| :-- | :-- | :-- |
| **Doc coverage %** | > 90% de vistas documentadas con plantilla completa | Mensual |
| **Doc drift rate** | < 5% de KPIs desactualizados vs. config actual | Sprint |
| **Tiempo de onboarding de nuevo vendedor** | Reducción > 30% en tiempo para entender dashboards | Por cohorte |
| **Tickets "no entiendo este número"** | Reducción > 50% vs. baseline | Mensual |
| **PR con doc incluida** | > 80% de PRs de config incluyen actualización de docs | Sprint |
| **Owner response time** | KPI sin owner asignado = 0 en producción | Semanal |

> **`[FACT]`** Crear una guía de datos que explique qué significa cada KPI, su fuente y frecuencia de actualización reduce directamente el soporte reactivo.  *(2025-12-18)*[^2]

***

## Operational Checklist

### ✅ Checklist: Anatomía UI Completa

**Estructura visual:**

- [ ] Nombre de la vista documentado (¿coincide con el label en pantalla?)
- [ ] Jerarquía de componentes mapeada (header → filtros → body → footer)
- [ ] Screenshot anotado con IDs por componente incluido en el `.md`
- [ ] Responsive behavior documentado (desktop / tablet si aplica)
- [ ] Z-index y overlays documentados (modales, tooltips, dropdowns)

**Filtros y parámetros:**

- [ ] Cada filtro tiene: nombre, tipo (single/multi-select, date range, boolean), valor por defecto, impacto en qué componentes
- [ ] Filtros persistentes vs. de sesión identificados
- [ ] Combinaciones de filtros que producen estado vacío documentadas
- [ ] Filtros con impacto en permisos (ej: "Ver todos los vendedores" solo para managers)

**Estados de cada componente:**

- [ ] Estado default (datos normales)
- [ ] Estado loading / skeleton
- [ ] Estado vacío (zero data) — con microcopy específico
- [ ] Estado error (falla de API o cálculo)
- [ ] Estado sin permisos / restringido
- [ ] Estado con datos parciales (carga incompleta)

**Accesibilidad (WCAG 2.2):**[^6]

- [ ] Contraste de color ≥ 4.5:1 para texto normal, ≥ 3:1 para texto grande
- [ ] Todos los elementos interactivos accesibles por teclado (Tab order documentado)
- [ ] ARIA labels en iconos sin texto visible
- [ ] Mensajes de error anunciados por screen readers
- [ ] Focus visible en todos los elementos interactivos
- [ ] No depender solo del color para comunicar estados

**Microcopy:**

- [ ] Labels de cada campo/columna documentados (¿hay abreviaciones no obvias?)
- [ ] Tooltips transcritos en la doc
- [ ] Mensajes de estado vacío transcritos
- [ ] Mensajes de error transcritos con código de error si aplica
- [ ] CTAs documentados con texto exacto + acción que ejecutan
- [ ] Placeholders de campos de búsqueda/filtro documentados

**Permisos y roles:**

- [ ] Qué roles ven esta vista
- [ ] Qué componentes son visibles/ocultos por rol
- [ ] Acciones restringidas por rol documentadas (export, edit, delete)

***

### ✅ Checklist: KPI Dictionary

- [ ] 100% de los KPIs visibles tienen entrada en el diccionario
- [ ] Fórmula verificada contra la config real del CRM (no la intención original)
- [ ] Owner asignado y confirmado (no "el equipo")
- [ ] Periodicidad de actualización verificada (no asumida)
- [ ] Exclusiones documentadas explícitamente
- [ ] Al menos una "decisión habilitada" por KPI
- [ ] Umbral de alerta definido
- [ ] Fecha de última validación de fórmula registrada

***

### ✅ Checklist: Docs-as-Code

- [ ] Docs viven en el mismo repo que la configuración del CRM (o en repo dedicado con link explícito)
- [ ] Estructura de carpetas definida: `/docs/views/`, `/docs/kpis/`, `/docs/filters/`
- [ ] Template Markdown estándar aplicado (este documento)
- [ ] Linter de Markdown configurado en CI (ej: `markdownlint`)
- [ ] Pipeline de publicación automática activo (GitHub Actions / GitLab CI)
- [ ] Proceso de review de docs definido (¿quién aprueba cambios de docs?)
- [ ] Política de "doc freeze" para lanzamientos mayores documentada[^7]

***

## Anti-Patterns

| Anti-patrón | Consecuencia | Corrección |
| :-- | :-- | :-- |
| **Screenshot sin anotaciones** como única documentación | Inútil cuando la UI cambia; no explica comportamiento | Reemplazar con Markdown + screenshot anotado + tabla de componentes |
| **KPI definido por el nombre visible** ("Ventas del Mes") sin fórmula | Interpretaciones divergentes entre equipos | KPI Dictionary obligatorio con fórmula y exclusiones [^2] |
| **Doc en Confluence desconectada del repo** | Drift garantizado en < 3 sprints | Migrar a docs-as-code o establecer proceso de sync automático [^1] |
| **Un solo dueño del dashboard** (el que lo creó) | Single point of failure de conocimiento | Owner por KPI, no por vista completa |
| **Documentar solo el happy path** | QA no puede validar estados de error ni accesibilidad | Documentar los 6 estados mínimos por componente [^3] |
| **Microcopy "por implementar"** en la doc | El texto real difiere del documentado | Doc se escribe/actualiza DESPUÉS de verificar el texto en producción |
| **Periodicidad asumida** ("se actualiza en tiempo real") | Malentendidos en decisiones críticas | Verificar y documentar la frecuencia real de actualización del CRM |
| **Accesibilidad omitida** en dashboards internos | Riesgo legal creciente + exclusión de usuarios | Aplicar WCAG 2.2 checklist incluso en herramientas internas [^6] |

> **`[FACT]`** Los "vanity metrics" — números que se ven bien pero no correlacionan con resultados de negocio — son el anti-patrón más común en dashboards CRM.  *(2025-12-18)*[^2]

***

## Diagnostic Questions

Estas preguntas sirven para auditar si una vista en tu CRM necesita pasar por View Anatomy Mode:

**Sobre la vista en general:**

1. ¿Puede un vendedor nuevo entender esta vista sin que nadie se la explique en < 10 minutos?
2. ¿Sabes exactamente qué pasa con los datos si cambias cada filtro disponible?
3. ¿Tienes documentado qué ve un gerente vs. un ejecutivo de ventas en esta misma vista?

**Sobre KPIs:**
4. ¿Puedes escribir la fórmula exacta de cada número visible sin abrir el CRM?
5. ¿Hay algún número cuyo significado depende de "preguntarle a alguien"?
6. ¿Alguien ha tomado una decisión incorrecta por malinterpretar un KPI de esta vista?

**Sobre estados y comportamiento:**
7. ¿Sabes exactamente qué ve el usuario si no hay datos para el período seleccionado?
8. ¿Qué pasa si la API del CRM falla a mitad de carga? ¿Eso está documentado?
9. ¿Los mensajes de error de esta vista son accionables (dicen qué hacer)?

**Sobre docs-as-code:**
10. ¿La última vez que cambiaron un filtro o KPI, alguien actualizó la documentación?
11. ¿Tienes forma de saber qué versión de la documentación corresponde a la config actual?
12. ¿Existe un proceso formal para que cambios en el dashboard disparen actualización de docs?[^1]

***

## Sources

```
web:2  — DeepDocs. "8 Code Documentation Best Practices for 2025." 2025-10-24
         https://deepdocs.dev/code-documentation-best-practices/

web:3  — Fern. "Best docs-as-code solutions for API teams in January 2026." 2026-01-05
         https://buildwithfern.com/post/docs-as-code-solutions-api-teams

web:8  — Authencio. "How to Build a CRM KPI Dashboard: Practical Guide." 2025-12-18
         https://www.authencio.com/blog/how-to-build-a-crm-kpi-dashboard-practical-guide-for-crm-users

web:18 — AllAccessible. "WCAG 2.2 Compliance Checklist: Complete 2025 Implementation." 2025-11-19
         https://www.allaccessible.org/blog/wcag-22-compliance-checklist-implementation-roadmap

web:19 — Design Systems Collective. "Design system best practices: Components and documentation." 2025-08-16
         https://www.designsystemscollective.com/design-system-best-practices-components-and-documentation-bdb020e02172

web:22 — Compresto. "12 Best Developer Documentation Tools for 2025." 2025-10-30
         https://compresto.app/blog/developer-documentation-tools

web:24 — LinkedIn / Vivek Rudrappa. "Documentation as Code: The Future of Software Architecture." 2025-04-06
         https://www.linkedin.com/pulse/documentation-code-future-software-architecture-vivek-rudrappa-tuthc

web:26 — Guidejar. "Top software documentation tools for 2026." 2025-10-27
         https://www.guidejar.com/blog/top-software-documentation-tools-for-2026
```


***

## Key Takeaways for PM Practice

- **Un dashboard sin Anatomy Doc es deuda técnica invisible**: afecta onboarding, QA, decisiones comerciales y mantenimiento futuro.
- **El KPI Dictionary no es opcional**: cada número sin fórmula verificada y owner asignado es un riesgo de decisión, no un activo de información.[^2]
- **Docs-as-Code no es para devs únicamente**: cualquier equipo que configure CRM, dashboards o automatizaciones puede (y debe) vivir en Markdown + Git.[^1]
- **Documentar estados de error y vacío es tan importante como el happy path**: es donde los usuarios cometen errores y el equipo pierde confianza en el sistema.[^3]
- **El owner del KPI ≠ el creador del dashboard**: separar responsabilidades evita que el conocimiento quede en una sola persona.
- **Microcopy es parte del contrato del producto**: labels ambiguos generan tickets de soporte; buenos textos de estado vacío generan acción.[^2]
- **Accesibilidad en herramientas internas**: WCAG 2.2 aplica aunque sea "solo para tu equipo". El riesgo legal y la exclusión de usuarios son reales.[^6]
- **La documentación que no se actualiza es peor que no tener documentación**: la confianza falsa en docs desactualizadas genera errores sistémicos. Automatiza el proceso de actualización o no funcionará.[^7]
- **Para mayoristas B2B en LATAM**: prioriza el Anatomy Doc del dashboard de pipeline y el de cotizaciones activas — son las vistas que más impactan el ciclo de venta y donde más malentendidos ocurren con agencias.

***

> 📁 **Referencia:** Añadir entradas de este KB a `SOURCES.md` del Space bajo la categoría `[CRM / Dashboard Documentation]`. Versión: `v1.0 — 2026-02-21`.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30][^31]</span>

<div align="center">⁂</div>

[^1]: https://buildwithfern.com/post/docs-as-code-solutions-api-teams

[^2]: https://www.authencio.com/blog/how-to-build-a-crm-kpi-dashboard-practical-guide-for-crm-users

[^3]: https://www.designsystemscollective.com/design-system-best-practices-components-and-documentation-bdb020e02172

[^4]: https://compresto.app/blog/developer-documentation-tools

[^5]: https://www.customerization.ca/crm-requirements-checklist/

[^6]: https://www.allaccessible.org/blog/wcag-22-compliance-checklist-implementation-roadmap

[^7]: https://deepdocs.dev/code-documentation-best-practices/

[^8]: https://www.linkedin.com/pulse/documentation-code-future-software-architecture-vivek-rudrappa-tuthc

[^9]: https://www.guidejar.com/blog/top-software-documentation-tools-for-2026

[^10]: pasted-text.txt

[^11]: https://www.augmentcode.com/learn/auto-document-your-code-tools-and-best-practices

[^12]: https://www.42coffeecups.com/blog/technical-documentation-best-practices

[^13]: https://www.mintlify.com/blog/top-7-api-documentation-tools-of-2025

[^14]: https://meetzest.com/blog/code-documentation-best-practices

[^15]: https://mriacrm.com/key-components-of-crm-systems-the-complete-overview/

[^16]: https://insightsoftware.com/blog/30-manufacturing-kpis-and-metric-examples/

[^17]: https://www.reddit.com/r/ExperiencedDevs/comments/1ovw11p/do_you_have_a_documentation_strategy/

[^18]: https://www.selecthub.com/customer-relationship-management/crm-requirements-checklist-and-downloadable-template/

[^19]: https://monday.com/blog/project-management/kpi-template/

[^20]: https://konghq.com/blog/learning-center/what-is-docs-as-code

[^21]: https://www.erphub.com/blogs/post/top-20-crm-checklist-items-after-q2-2025

[^22]: https://procreator.design/blog/mobile-app-interface-design-checklist/

[^23]: https://www.authgear.com/post/login-signup-ux-guide

[^24]: https://blog.copyelement.com/web-design-accessibility-checklist-2025-ensure-compliance-and-inclusivity/

[^25]: https://www.bruceandeddy.com/website-accessibility-checklist/

[^26]: https://elfsight.com/blog/website-accessibility-checklist/

[^27]: https://uxdesign.cc/react-ing-to-accessibility-building-accessible-e-commerce-forms-that-everyone-can-use-9713daf7ba69

[^28]: https://clickhelp.com/clickhelp-technical-writing-blog/top-20-software-documentation-tools/

[^29]: https://www.wdb.agency/blog/the-ultimate-website-accessibility-compliance-checklist-for-2025

[^30]: https://www.fluidtopics.com/blog/content-ops/technical-documentation-software-tools/

[^31]: https://axerosolutions.com/insights/technical-documentation-software/

