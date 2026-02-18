<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_10_Metrics_Instrumentation_Adoption.md

“Métricas UX para CRM: adopción por rol, eficiencia (time-on-task), calidad de datos, pipeline hygiene, error rates, feature usage. Incluye esquema de eventos sugerido (sin código) y dashboard mínimo.”

Aquí tienes el contenido para **KB_10_Metrics_Instrumentation_Adoption.md**: un set de métricas UX para CRM orientadas a adopción (por rol), eficiencia (time-on-task), calidad de datos, pipeline hygiene, error rates y feature usage, con esquema de eventos sugerido (sin código) y un dashboard mínimo.

## 1) Objetivo y definiciones

El objetivo es medir si el CRM está “vendiendo con el equipo”: adopción real por rol, velocidad operativa, reducción de errores y mejor salud de datos/pipeline (no solo “logins”).
Como marco simple para ordenar UX metrics, puedes mapear estas métricas a **Adoption / Engagement / Task Success / Retention / Happiness** (HEART) si necesitas alineación producto–negocio.[^1][^2]

## 2) Métricas UX clave (CRM)

Usa siempre segmentación por **rol** (ej.: SDR/BDR, AE/Closer, Manager, Ops/RevOps, Admin) y por **equipo/país/canal** si aplica.

- Adopción por rol
    - Usuarios activos: DAU/WAU/MAU por rol.
    - Activación (activation): % de nuevos usuarios que completan el “primer valor” (ej.: crear oportunidad + mover etapa + registrar próxima acción) dentro de X días.
    - Retención: % que vuelve a ejecutar el “loop de valor” semana a semana (no solo iniciar sesión).
- Eficiencia (time-on-task)
    - Time-on-task por tarea crítica: p50/p90 para “crear lead”, “convertir a contacto”, “crear oportunidad”, “actualizar etapa”, “cerrar ganada/perdida”, “registrar actividad”.
    - Tiempo total “para hacer trabajo” (sumatoria de tareas clave por sesión) para comparar antes/después de cambios de UX.[^3]
    - Nota: time-on-task es una métrica de eficiencia; compárala entre versiones/segmentos y léela junto con éxito/errores para evitar falsos positivos.[^4]
- Calidad de datos (data quality)
    - Field completion rate: % de registros con campos obligatorios completos (por objeto: Lead/Account/Contact/Opp).[^5]
    - Duplicate rate: % de registros marcados como potencial duplicado (por objeto).[^5]
    - Validez: % emails válidos / teléfonos con formato válido / dominios corporativos vs genéricos (si es política).
    - “Stale records”: \# y % registros sin actividad/actualización en X días.[^5]
- Pipeline hygiene (salud operativa del pipeline)
    - Oportunidades “sin próxima acción”: % con next_step vacío o activity_due_date vencida.
    - Close date hygiene: % con close_date en el pasado y etapa abierta; % close_date cambiada >N veces (señal de forecast inflado).
    - Aging por etapa: días en etapa vs umbral (por segmento y dueño).
    - Cobertura por categorías de forecast (si lo manejan): open pipeline, commit, best case, closed won/lost, etc.[^6]
- Error rates (fricción real)
    - Error rate por tarea: errores/intent (ej.: fallas de validación, permisos, integraciones, timeouts).[^3]
    - Rework rate: % de registros editados 2+ veces en <24h para corregir campos “core” (mala UX o mala gobernanza).
    - Escape rate: % de tareas iniciadas pero no completadas (abandono).
- Feature usage (uso de funcionalidades)
    - Adoption por feature: % de usuarios del rol que usan una feature al menos 1 vez por semana/mes.[^1]
    - Depth: mediana de acciones por sesión en feature (ej.: \# filtros guardados, \# vistas de pipeline, \# notas/llamadas registradas).
    - “Uso correcto”: % de uso que cumple el estándar (ej.: actividades con outcome + next step, oportunidades con campos de forecast completos).


## 3) Esquema de eventos sugerido (sin código)

Convención recomendada: `snake_case`, evento en **pasado** (ej.: `opportunity_stage_changed`), y propiedades consistentes.

### Propiedades comunes (en todos los eventos)

- `event_time` (timestamp), `user_id` (interno), `account_id` (cliente/tenant), `role`, `team`, `country`
- `session_id`, `device_type` (web/mobile), `surface` (pipeline_view, record_detail, bulk_edit, import_wizard)
- `object_type` (lead/contact/account/opportunity/activity), `record_id` (hash o ID interno)


### Eventos “core” (mínimos)

- `session_started`, `session_ended`
- `crm_login_succeeded`, `crm_login_failed` (prop: `reason`)
- `record_created`, `record_updated`, `record_deleted`
    - props clave: `object_type`, `fields_changed_count`, `required_fields_missing_count` (post-save)
- `field_validation_failed`
    - props: `object_type`, `field_name`, `rule_id`, `error_code`, `ui_state` (inline/modal)
- `search_performed`
    - props: `query_length`, `filters_count`, `results_count`
- `bulk_edit_started`, `bulk_edit_completed`
    - props: `records_count`, `errors_count`
- `import_started`, `import_completed`
    - props: `source` (csv/api), `rows_total`, `rows_success`, `rows_failed`, `duplicate_detected_count`
- Pipeline / revenue motion
    - `opportunity_stage_changed` (props: `stage_from`, `stage_to`)
    - `opportunity_amount_changed` (props: `delta`, `currency`)
    - `opportunity_close_date_changed` (props: `days_moved`)
    - `opportunity_closed_won`, `opportunity_closed_lost` (props: `reason_code` si existe)
- Actividades
    - `activity_logged` (props: `activity_type` call/email/meeting/whatsapp, `has_outcome`, `has_next_step`)
    - `task_created`, `task_completed` (props: `due_in_days`)


### Instrumentación de time-on-task (sin SDK, solo concepto)

Para cada tarea crítica, emite:

- `task_started` (props: `task_name`, `entry_point`)
- `task_completed` (props: `task_name`, `success=true/false`, `completion_reason`)
- (opcional) `task_abandoned` (si el usuario navega fuera o pasa X min inactivo)

Cálculo: `time_on_task = task_completed.time - task_started.time`, y acompáñalo siempre con `success` y `error_count` por tarea para que el “rápido” no signifique “se rindió”.[^4][^3]

## 4) Dashboard mínimo (MVP)

Un dashboard operativo (para Growth/RevOps/Product) con filtros por `account_id`, `rol`, `equipo`, `rango de fechas`.

- Adopción
    - MAU/WAU por rol
    - Activación 7 días (% completó “primer valor”)
- Eficiencia
    - Time-on-task p50/p90 por tarea (top 5 tareas)
    - % tareas completadas con éxito (task success)[^3]
- Calidad de datos
    - Field completion rate (obligatorios)[^5]
    - Duplicate rate[^5]
    - Stale records (sin actividad X días)[^5]
- Pipeline hygiene
    - % opps sin próxima acción
    - Aging por etapa (promedio/percentiles)
    - % close_date en pasado con etapa abierta
- Error \& fricción
    - Error rate por formulario/regla (top 10)
    - Abandono de tarea (% started sin completed)


## 5) Incluye / No incluye / Sensibles

Incluye

- Métricas accionables por rol (qué hace cada rol y dónde se tranca) y una instrumentación mínima de tareas/eventos para priorizar mejoras y entrenamientos.

No incluye

- Métricas “vanity” (pageviews genéricos) sin segmentación por rol/tarea, ni dashboards gigantes tipo “BI showroom”.

Sensible (ojo operativo y de riesgo)

- PII: evita capturar valores de campos (emails, teléfonos, notas) en eventos; captura solo “metadatos” (completado/no, longitud, conteos, códigos).
- Auditoría vs analítica: si necesitas trazabilidad legal, sepáralo del tracking UX (pipelines distintos, retención distinta).
- Safe vs agresivo: **safe** = eventos mínimos + propiedades agregadas; **agresivo** = diffs por campo, trazas por paso y alertas automáticas por fricción (más valor, más riesgo y gobierno requerido).

Si me dices qué CRM es (Salesforce/HubSpot/custom) y cuáles son tus 5 tareas críticas (por rol), te lo adapto a un “primer valor” realista y a un set de eventos todavía más corto.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://www.appcues.com/blog/google-improves-user-experience-with-heart-framework

[^2]: https://www.statsig.com/perspectives/heart-framework-measuring-ux

[^3]: https://www.nngroup.com/articles/usability-metrics/

[^4]: https://www.thebehavioralscientist.com/glossary/time-on-task

[^5]: https://www.revenuetools.io/blog/crm-data-hygiene

[^6]: https://trailhead.salesforce.com/es/content/learn/modules/sell-smarter-with-pipeline-inspection/understand-pipeline-health-with-metrics-and-charts

[^7]: https://www.productplan.com/glossary/heart-framework/

[^8]: https://www.heartframework.com

[^9]: http://electrickite.com/current/keep-testing-why-we-use-the-heart-framework/

[^10]: https://www.linkedin.com/pulse/your-crm-lying-you-how-ai-powered-data-hygiene-75-person-david-brown-9bysc

[^11]: https://www.interaction-design.org/literature/topics/heart-framework

[^12]: https://trymata.com/blog/time-on-task/

[^13]: https://www.egrabber.com/blog/data-hygiene-best-practices/

[^14]: https://library.gv.com/how-to-choose-the-right-ux-metrics-for-your-product-5f46359ab5be

[^15]: https://www.nngroup.com/articles/success-rate-the-simplest-usability-metric/

