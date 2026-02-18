<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_13_Onboarding_EmptyStates_RoleBased_Enablement.md

Onboarding enterprise para CRM debe llevar a cada rol a su “primer valor” rápido, con empty states que empujan acciones, guías in‑product contextuales, plantillas por rol y progressive disclosure, todo medido con TTFV y loops de activación.

***

## 1) Empty states accionables (no decorativos)

Un empty state bien hecho no solo “informa que está vacío”: debe comunicar estado del sistema, aumentar learnability y dar un camino directo a la tarea clave (CTA hacia el siguiente paso).[^1]
Para CRM enterprise, piensa empty states como “pantallas de arranque” por módulo (Deals, Contacts, Activities, Reports), siempre con 1 acción primaria y 1 secundaria.

Qué incluye

- Mensaje claro de por qué no hay data y qué se espera ver aquí (ej. “Aún no hay oportunidades porque no has importado o creado tu primer deal”).[^2]
- Acción primaria que complete el siguiente paso crítico (ej. “Importar contactos”, “Crear pipeline”, “Conectar correo”).[^1]
- Acción secundaria de bajo riesgo (ej. “Ver plantilla”, “Ver ejemplo”, “Leer guía”), con link a doc o tour corto.[^2]

Qué no incluye

- Ilustraciones sin instrucción ni CTA (vacío “bonito” pero inútil).
- 3+ CTAs compitiendo (parálisis por elección).
- Copys ambiguos (“Empieza aquí”) sin decir qué pasa después.

Qué es sensible (enterprise)

- Permisos: el empty state debe reconocer “no tienes permisos” vs “no hay data”.
- Dependencias: si no hay email/calendar conectado, no prometas automatizaciones.

***

## 2) Guías in‑product + enablement por rol (role-based)

El onboarding product-led se apoya en elementos in‑app (tours, walkthroughs, checklists) para guiar al usuario a puntos de activación (“aha moment”) temprano.[^3]
Además, una buena práctica es mapear el punto de activación y “reverse‑engineer” el camino mínimo para llegar a él (sin pasos extra que no aporten a ese valor inicial).[^3]

Plantillas por rol (ejemplo CRM enterprise)

- Admin/IT: “SSO + permisos + estructura base” (crear workspace, roles, políticas, SSO/SCIM si aplica) → valor: usuarios pueden entrar y ver lo correcto.
- RevOps/Ops: “Pipeline + campos + reglas” (pipeline plantilla, stages, campos obligatorios, reason codes) → valor: primer flujo consistente y reportable.
- Sales Rep/BDR: “Mi primera oportunidad gestionada” (crear deal desde plantilla, 1 actividad, 1 nota, 1 próxima tarea) → valor: control diario y seguimiento.
- Sales Manager: “Visibilidad del forecast” (dashboard plantilla, reporte de pipeline, alertas) → valor: control y coaching.
- CS/AM: “Handoff + salud de cuenta” (playbook de handoff, tareas recurrentes, health signals) → valor: continuidad y retención.

Checklist dinámica (por rol y contexto)

- Mostrar checklist solo cuando sea relevante y que el usuario pueda cerrarlo/saltarlo (sin “trampa”).[^3]
- Cada ítem lleva directo a la pantalla donde se ejecuta (deep link a la acción).[^3]

***

## 3) Progressive disclosure (enterprise sin abrumar)

Progressive disclosure difiere funciones avanzadas o raras a pantallas secundarias para hacer el producto más fácil de aprender y menos abrumador.[^4]
También se usa para reducir carga cognitiva revelando información solo cuando se necesita, por ejemplo, desbloqueando controles en función de selecciones previas.[^5]

Aplicación práctica en CRM

- Nivel 1 (día 0): solo lo mínimo para “registrar y mover” oportunidades (pipeline, deal, actividad, próximo paso).
- Nivel 2 (día 3–7): automatizaciones ligeras (asignaciones, recordatorios, templates).
- Nivel 3 (día 14+): gobernanza y escalado (aprobaciones, scoring, integraciones avanzadas, auditoría).

Regla simple

- Si una feature no reduce TTFV, no debe estar en el camino crítico de onboarding.

***

## 4) Medición: TTFV + activation loops (instrumentación real)

TTFV mide qué tan rápido un usuario experimenta el valor core del producto tras registrarse.[^6]
Una forma común de calcularlo es: TTFV = momento del “primer valor” − momento de sign‑up (o primera sesión).[^7]

Cómo definir “First Value” en CRM (ejemplos)

- Sales Rep: primer deal creado + primera actividad programada + próximo paso definido.
- Manager: primer dashboard visto con datos reales (no demo) + primer forecast exportado/compartido.
- RevOps: primer pipeline publicado + primer campo requerido activo + primer reporte de conversión.

Activation loop (de onboarding a hábito)

- “Activación” se trata de lograr ese primer valor y convertirlo en hábito, y un time‑to‑value corto ayuda a reducir duda y acelerar esa activación.[^8]
- Úsalo como loop: Trigger (recordatorio/empty state) → Action (crear/actualizar) → Reward (visibilidad/ahorro de tiempo) → Next trigger (tarea siguiente).

Growth loops (a nivel producto/empresa)

- Un growth loop es un ciclo auto‑reforzado donde una acción genera output que alimenta el siguiente ciclo, y conviene medir el tiempo de ciclo del loop (mientras más corto, mejor feedback).[^9]

Eventos mínimos a trackear (sugerencia)

- account_created, user_invited, first_login, role_selected
- template_applied (pipeline/fields/dashboard), import_started/import_completed
- first_deal_created, first_activity_logged, next_task_scheduled
- integration_connected (email/calendar), automation_enabled
- report_viewed, dashboard_created, forecast_shared

KPIs operables

- TTFV por rol (p50/p75/p90).
- Activation rate por rol (alcanzó “First Value” en X días).
- Drop-off por step del checklist.
- Tiempo de ciclo del loop (ej. de “crear deal” a “actualizar etapa” a “cerrar/ganar”).

***

## 5) Opciones: segura vs agresiva (para enterprise)

Opción segura (menor riesgo operativo)

- Onboarding guiado con plantillas “read‑only” primero (preview), luego “Apply”.
- Importaciones opcionales y asistidas, con validación y rollback.
- Progressive disclosure estricto: lo avanzado no aparece hasta completar hitos.

Opción agresiva (máxima velocidad de activación)

- “1‑click setup” por rol (aplica pipeline + dashboards + campos + reglas de forma automática).
- Import rápido (CSV/HubSpot/Salesforce) como CTA principal en el primer empty state.
- Nurture in‑product (nudges) para empujar el loop diario (registrar actividad, actualizar etapa, agendar siguiente paso).

Punto sensible a vigilar

- En enterprise, un onboarding agresivo sin control (permisos, gobernanza, calidad de datos) puede generar rechazo interno y tickets; si lo haces, pon límites claros y opción de deshacer.

***

Si me dices 3 cosas (industria, tamaño típico de cuenta: 5–20 vs 50–200 usuarios, y el “First Value” que más te importa comercialmente), te lo aterrizo a un flujo único con checklist por rol + definición exacta de eventos/propiedades para medir TTFV y activación.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^30]</span>

<div align="center">⁂</div>

[^1]: https://www.nngroup.com/articles/empty-state-interface-design/

[^2]: https://carbondesignsystem.com/patterns/empty-states-pattern/

[^3]: https://userguiding.com/blog/product-led-onboarding

[^4]: https://www.nngroup.com/articles/progressive-disclosure/

[^5]: https://blog.logrocket.com/ux-design/progressive-disclosure-ux-types-use-cases/

[^6]: https://productschool.com/blog/analytics/product-success

[^7]: https://payproglobal.com/answers/what-is-saas-time-to-first-value-ttfv/

[^8]: https://www.statsig.com/perspectives/plg-metrics-activation-retention

[^9]: https://productschool.com/blog/product-strategy/growth-loops

[^10]: https://www.nngroup.com/articles/design-guidance/

[^11]: https://www.nngroup.com/videos/empty-states-in-application-design-guidelines/

[^12]: https://www.setproduct.com/blog/empty-state-ui-design

[^13]: https://www.loginradius.com/blog/identity/progressive-disclosure-user-onboarding

[^14]: https://app.uxcel.com/courses/common-patterns/empty-states-best-practices-330

[^15]: https://soul.emplifi.io/latest/patterns/patterns/empty-states-Q4JtHNtG

[^16]: https://www.interaction-design.org/literature/topics/progressive-disclosure

[^17]: https://www.alexanderjarvis.com/what-is-time-to-first-value-in-saas-how-to-improve-it/

[^18]: https://raw.studio/blog/empty-states-error-states-onboarding-the-hidden-ux-moments-users-notice/

[^19]: https://www.getloops.ai/blog/defining-activation-metrics

[^20]: https://www.gainsight.com/blog/the-beginners-guide-to-product-led-growth-metrics/

[^21]: https://learningloop.io/glossary/product-metrics

[^22]: https://www.productledalliance.com/all-you-need-to-know-about-building-a-killer-product-led-growth-loop/

[^23]: https://www.fishmanafnewsletter.com/p/how-ai-products-drive-adoption-in-onboarding-through-template-activation-loop

[^24]: https://qubit.capital/blog/product-led-growth-metrics

[^25]: https://productled.com/blog/growth-loops-accelerants-for-plg-saas

[^26]: https://www.appcues.com/blog/pirate-metric-saas-growth

[^27]: https://amplitude.com/blog/product-led-growth-diagrams

[^28]: https://productloops.com/user-activation

[^29]: https://amplitude.com/guides/what-is-product-led-growth-plg

[^30]: https://www.productled.org/foundations/the-product-led-growth-flywheel

