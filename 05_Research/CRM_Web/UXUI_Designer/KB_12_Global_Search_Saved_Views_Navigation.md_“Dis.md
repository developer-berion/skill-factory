<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_12_Global_Search_Saved_Views_Navigation.md

“Diseño UX de búsqueda global en CRM + saved views + filtros compartidos + comandos rápidos. Incluye métricas: search success, time-to-record, zero-results recovery.”

```markdown
# KB_12_Global_Search_Saved_Views_Navigation
Diseño UX de búsqueda global en CRM + saved views + filtros compartidos + comandos rápidos. Incluye métricas: search success, time-to-record, zero-results recovery.

## 1) Objetivo y alcance
Diseñar una experiencia de **búsqueda global** en CRM que acelere “encontrar → abrir → actuar”, y que soporte trabajo recurrente con vistas guardadas y filtros compartibles.  
- **Incluye:** búsqueda global (cross-objetos), página de resultados con scopes, filtros (chips + panel), saved views (personales y compartidas), links compartibles, comandos rápidos (command palette), telemetría y métricas.  
- **No incluye:** diseño visual final (UI kit), modelo de permisos/seguridad completo, ni ranking/ML a profundidad (solo puntos de decisión).  
- **Sensible:** permisos/visibilidad de registros al compartir vistas y filtros (links nunca deben “elevar” acceso), y exposición de PII en autosuggest, logs y URLs.

## 2) Arquitectura UX (búsqueda + resultados + navegación)
La búsqueda global debe arrancar en “All” por defecto y permitir ampliar el scope en 1 click si el usuario buscó en un scope estrecho y falló. [web:11]  
- **Entry points (siempre visibles):** caja de búsqueda en topbar (⌘K/CTRL+K opcional), acceso desde listas/objetos, y desde “no results” con el query preservado. [web:1]  
- **Resultados (SERP CRM):** tabs o pills por objeto (Clientes/Empresas/Oportunidades/Tickets/Reservas/Documentos), contador por tab, y “Top hits” mixto si el usuario está en All.  
- **Filtros:** panel lateral con campos “high-signal” (estado, owner, fecha, pipeline, país/mercado, tags), + chips arriba para ver/remover rápido lo aplicado.  
- **Scoped search (regla dura):** si el usuario buscó dentro de un objeto, muestra el scope explícito y ofrece “Search all” a la vista. [web:11]  

### Saved views (personal + compartida)
Las saved views deben permitir múltiples vistas nombradas por pantalla/tarea, incluyendo filtros y sorts cuando aplique, para volver rápido a datasets frecuentes. [page:1]  
- **Guardar no debe ser implícito:** exigir acción explícita “Save / Save as” para evitar que filtros de 1 vez ensucien una vista estable. [page:1]  
- **Default view:** permitir “Pin as default” por usuario (y por contexto si aplica, ej. entidad/BU) para aterrizar directo en la vista más usada. [page:1]  
- **Vistas publicadas (compartidas):** permitir publicar a roles/grupos para estandarizar operación; esas vistas quedan bloqueadas para edición y el usuario puede clonar (“Save as”) si tiene permisos. [page:1]  

### Filtros compartibles (links)
El link compartible debe abrir la misma vista/filtros sin necesidad de “explicación por chat”, y debe ser estable para colaboración operativa (“mira exactamente lo que estoy viendo”). [page:2]  
- **Share como producto:** botón “Share” visible en la barra de filtros/vista, con opción “Copy link” y (si aplica) “Share to role/team”.  
- **Regla de seguridad:** el link solo serializa filtros/orden/objeto; el backend siempre reevalúa permisos (si no hay acceso, debe degradar con mensajes claros).

## 3) Comandos rápidos (command palette)
El command palette es un atajo de navegación/acciones que se diseña como extensión de atajos de teclado, definiendo explícitamente dónde termina el palette y dónde continúa el UI tradicional (handoffs). [web:13]  
- **Qué debe resolver:** “ir a registro”, “crear X”, “cambiar pipeline/owner”, “abrir vista guardada”, “aplicar filtro frecuente”, “ejecutar acción masiva segura”.  
- **Resultados del palette:** mezcla de comandos + registros + vistas guardadas, con fuzzy search y labels claros (“Cliente · ACME”, “Vista · Oportunidades Hoy”).  
- **Handoff recomendado:** comandos que requieren input corto pueden completarse dentro del palette; flujos largos deben saltar a pantalla con foco en el campo correcto. [web:13]  

## 4) Métricas (definiciones operables)
“Search success” se define como si el usuario ejecutó la búsqueda y vio resultados apropiados; no equivale a éxito de tarea final, pero indica si la búsqueda no estorbó. [web:6]  
- **Search success (SSR):** % de sesiones de búsqueda que terminan en “resultado apropiado visto” (proxy: click/open de un resultado o apertura de tab relevante) dentro de una ventana T (ej. 60–120s). [web:6]  
- **Time-to-record (TTR):** tiempo desde “submit query” hasta “record detail opened”; es una métrica tipo “time on task”, útil para comparar rediseños y fricción. [web:9]  
- **Zero-results recovery (ZRR):** % de búsquedas con 0 resultados que luego terminan en apertura de registro/resultado mediante reformulación, cambio de scope o uso de sugerencias. [web:1][web:11]  

### Instrumentación mínima (eventos)
- `search_submitted` (query_length, scope, source=topbar/palette/list, user_role)
- `search_results_loaded` (result_count_total, result_count_by_object, latency_ms)
- `search_result_opened` (object_type, rank_position)
- `search_scope_changed` (from, to, reason=manual/zero_results_cta) [web:11]
- `zero_results_shown` (scope, query_length) + `zero_results_action_taken` (edit_query, broaden_scope, suggested_query_clicked) [web:1]
- `view_saved` / `view_saved_as` / `view_pinned_default` [page:1]
- `view_shared` / `view_opened_from_share_link` [page:2]
- `command_palette_opened` / `command_executed` [web:13]

## 5) Patrones “no results” (recuperación)
La página de 0 resultados debe decir explícitamente que no hay matches, ofrecer caminos concretos para seguir (editar query, sugerencias, categorías/scopes) y mantener respeto por el usuario. [web:1]  
- **Componentes obligatorios:** mensaje claro “No encontramos resultados”, caja de búsqueda con el query intacto, CTA “Buscar en todo el CRM”, sugerencias (sinónimos/ortografía), y “ver vistas guardadas relacionadas”. [web:1][web:11]  
- **Si hay scoped search:** si falló en un objeto, el CTA principal debe ampliar el scope a All en 1 click. [web:11]  

---

## Opción segura vs opción agresiva (para rollout)
- **Segura:** global search + results por objeto + filtros básicos + saved views personales; compartir solo por link interno con revalidación de permisos.  
- **Agresiva:** además, publicación de vistas a roles (estándares operativos), command palette con acciones, sugerencias inteligentes (sinónimos) y “shares” persistentes tipo bookmarks.

## Objeciones típicas de agencias (y cómo cubrirlas)
- “Compartí un link y al otro no le abre igual”: explicar “no ves lo mismo si no tienes permiso”, y ofrecer “request access” o vista alternativa sin PII.  
- “Se me dañó mi vista por un filtro rápido”: separar “Quick filters (no guardados)” vs “Vista guardada”, y exigir guardado explícito. [page:1]  
- “Me tarda”: medir latencia + TTR y atacar ranking, caching y scopes; la métrica de tiempo es clave para demostrar mejora. [web:9]
```

¿Tu CRM tiene objetos tipo “Reserva/Itinerario/Factura/Agencia” (turismo B2B) o estás modelando sobre un CRM genérico (Lead/Account/Opportunity/Ticket)? Eso define cómo conviene tabear resultados y qué filtros deben ir “arriba” por defecto.
<span style="display:none">[^1][^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^2][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^3][^30][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://www.nngroup.com/articles/search-no-results-serp/

[^2]: https://www.nngroup.com/articles/internal-website-search/

[^3]: https://www.nngroup.com/articles/pinball-pattern-search-behavior/

[^4]: https://wpriders.com/the-complete-guide-to-website-search-to-drive-revenue/

[^5]: https://www.reddit.com/r/UXDesign/comments/195rthy/zero_results_page/

[^6]: https://www.nngroup.com/articles/state-ecommerce-search/

[^7]: https://www.reddit.com/r/webdev/comments/1pu471y/what_web_app_has_a_great_keyboard_ux_shortcuts/

[^8]: https://app.uxcel.com/courses/ui-components-best-practices/search-best-practices-248

[^9]: https://www.nngroup.com/articles/usability-metrics/

[^10]: https://www.youtube.com/watch?v=z5tfqJte2oc

[^11]: https://www.nngroup.com/articles/search-visible-and-simple/

[^12]: https://www.nngroup.com/topic/analytics-and-metrics/?page=6

[^13]: https://solomon.io/designing-command-palettes/

[^14]: https://www.linkedin.com/posts/brandkraft_optimizing-for-ai-search-the-practical-guide-activity-7391427921132830721-xf6Z

[^15]: https://www.nngroup.com/articles/success-rate-the-simplest-usability-metric/

[^16]: https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/get-started/saved-views

[^17]: https://community.dynamics.com/blogs/post/?postid=0b233cce-e5d1-4c96-aef7-237ddf9212f4

[^18]: https://stoneridgesoftware.com/how-to-create-a-personal-view-in-dynamics-365/

[^19]: https://www.randgroup.com/insights/microsoft/dynamics-365-fo-tip-of-the-month-sharing-a-saved-view/

[^20]: https://helpdesk.bridgeport.edu/knowledgebase/article/KA-01182/en-us

[^21]: https://forcewalk.com/salesforce-tips-share-a-list-view-to-several-users/

[^22]: https://temporal.io/blog/introducing-saved-views-in-temporal-web-ui

[^23]: https://learn.microsoft.com/en-us/dynamics365/business-central/ui-views

[^24]: https://stackoverflow.com/questions/59392920/customize-list-views-with-sharing-settings-in-salesforce

[^25]: https://community.weweb.io/t/best-practices-for-saved-filters/5400

[^26]: https://www.youtube.com/watch?v=8EKRRRsbA9c

[^27]: https://www.salesforceben.com/how-to-get-your-salesforce-users-to-love-list-views/

[^28]: https://uxdesign.cc/crafting-a-kickass-filtering-ux-beea1798d64b

[^29]: https://sageitinc.com/reference-center/types-views-in-dynamics-365

[^30]: https://trailhead.salesforce.com/content/learn/modules/list-views-quick-look/get-to-know-list-views

