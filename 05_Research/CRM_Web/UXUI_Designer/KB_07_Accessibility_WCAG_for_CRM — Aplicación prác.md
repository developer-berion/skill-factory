<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_07_Accessibility_WCAG_for_CRM — Aplicación práctica de WCAG a CRMs (forms densos, tablas, modals, toasts, focus y shortcuts)

Un CRM es “teclado-first”, denso en formularios y con UI dinámica; por eso la accesibilidad se gana o se pierde en focus management, errores de formularios, tablas/grids, diálogos modales y atajos. WCAG 2.2 está pensado como criterios **testeables** (con automatización + evaluación humana), y documenta técnicas y “common failures” como apoyo de implementación.[^1]

## Alcance (qué incluye / no / sensible)

Incluye: flujos de captura (create/edit), validación y mensajes de error, navegación con teclado, tablas de datos y grids, modals/drawers, notificaciones tipo toast, y atajos de teclado.[^1]
No incluye: auditoría legal de conformidad, ni “certificación”; esto es un playbook práctico para producto/QA.[^1]
Sensible: acciones irreversibles (borrar, cerrar oportunidad, emitir factura, cambios de permisos), porque el manejo de foco y confirmaciones impacta directamente riesgo operacional.[^2]

## Forms densos (CRM real)

Checklist de implementación (lo que más pega en CRM):

- Etiquetas e instrucciones: cada input debe tener label/instrucciones claras para evitar ambigüedad (“Labels or instructions are provided…”).[^1]
- Errores: si detectas error automáticamente, identifica el campo y describe el error en texto (no solo color/ícono).[^1]
- Sugerencias: si conoces la corrección (p. ej. formato de email/fecha), muéstrala; si no, al menos identifica el error.[^3][^1]
- Teclado: toda acción del formulario (guardar, cancelar, abrir pickers) debe ser operable por teclado.[^1]

Common failures típicos (lo que rompe en CRMs):

- “Required” solo con asterisco rojo o borde rojo, sin texto equivalente (falla por depender de características sensoriales/solo color).[^1]
- Error message genérico arriba (“Hubo un error”) sin anclar a campos ni explicar qué falló (falla de identificación de error).[^1]
- Validación en blur que cambia contexto (p. ej. abre modal, salta de sección) apenas recibe foco (ojo con predictibilidad al recibir foco).[^1]

Patrones que funcionan (operativo, no académico):

- “Error summary” al guardar: lista de errores con links que muevan foco al campo (reduce fricción en forms largos).
- Agrupa por secciones con encabezados reales (no solo visuales) para que lector de pantalla navegue por estructura (en CRMs, esto reduce “scroll infinito” mental).
- Autoguardado: opción segura = auto-save silencioso + confirmación no intrusiva; opción agresiva = auto-save con toast + undo (pero cuida no robar foco).


## Tablas, grids y listas (datos + acciones)

En CRMs, la tabla suele ser “workspace”: selección, ordenamiento, acciones por fila, paginación, filtros.

Checklist mínimo:

- La tabla debe exponer estructura/relaciones de forma programática (encabezados, asociaciones), porque “information, structure, and relationships” deben ser determinables.[^1]
- Evita convertir todo en un “div soup” sin semántica; si usas grid custom, asegúrate de que siga siendo operable por teclado y con foco manejable.[^1]
- Sorting y filtros: el cambio debe ser predecible y operable por teclado (si hay cambio de contexto por interacción, avisa/controle).[^1]

Common failures:

- Header visual sin `<th>`/asociación real: lector de pantalla pierde contexto columna/fila (relaciones no determinables).[^1]
- Acciones solo en hover (“⋯” que aparece al pasar mouse): teclado no las descubre o no las opera bien.[^1]

Patrón recomendado para CRM:

- “Row actions” siempre focusables (aunque estén en overflow menu), y con nombre accesible claro (“Acciones de Juan Pérez”, “Editar oportunidad”, etc.).


## Modals, drawers y focus management

Un modal de verdad vuelve “inert” lo de atrás; por patrón WAI-ARIA, el foco debe entrar al diálogo al abrir y quedarse dentro con Tab/Shift+Tab, y Escape debe cerrar.[^2]
Cuando cierra, el foco debe volver al elemento que lo invocó (o a uno lógico si ya no existe) para mantener el “point of regard”.[^4][^2]
Además, no marques `aria-modal="true"` si en realidad dejas interactuar el fondo, porque APG advierte consecuencias severas para usuarios de AT si dices “modal” pero no se comporta como modal.[^2]

Common failures:

- Abrir modal y dejar foco detrás (el usuario tabbea “por debajo” del overlay) → se siente “UI rota” y es un bug de accesibilidad/operabilidad.[^2]
- Cerrar modal y mandar foco al `<body>` o al inicio de página (pierdes contexto operacional, típico en CRMs).[^4][^2]

Decisión “segura vs agresiva” (focus inicial):

- Segura: enfoca el primer campo accionable si el modal es formulario corto.[^2]
- Agresiva (pero válida): si el modal tiene texto estructurado largo, enfoca un elemento estático con `tabindex="-1"` al inicio para que se lea bien, como sugiere APG.[^2]


## Toasts, shortcuts y cómo testear

Shortcuts en CRM: si implementas atajos de una sola tecla (letra/número/símbolo), WCAG exige al menos una: permitir apagar, remapear (con modificadores), o que solo esté activo cuando el componente tiene foco.[^5]
Esto es crítico en CRMs porque una tecla suelta puede disparar acciones (p. ej. “D” = delete) y generar errores costosos.[^5]

Toasts (notificaciones no modales):

- No deben robar foco por defecto; si informan estado (“Guardado”), trátalos como feedback pasivo (con región viva/announcement) y deja que el usuario siga tipeando.
- Si el toast implica acción (“Deshacer”), haz el botón alcanzable por teclado sin secuestrar el foco; opción segura = link persistente en UI (“Ver cambios”) además del toast.

Cómo testear (práctico, repetible):

- Teclado-only: recorre el flujo core (crear lead → convertir → crear deal → cerrar) asegurando que todo es operable por teclado y sin traps (alineado a “keyboard accessible”).[^1]
- Focus: abre/cierra cada modal verificando foco inicial, tab loop interno y retorno al trigger, y que Escape cierra.[^4][^2]
- Forms: fuerza errores (vacío, formato inválido) verificando identificación en texto y, cuando aplique, sugerencias de corrección.[^3][^1]
- Shortcuts: prueba dictado/voice input o escritura rápida en inputs para confirmar que single-key shortcuts no se disparan accidentalmente y que hay toggle/remap/focus-only.[^5]

Si me dices tu stack (React/Vue/Angular) y si tu “tabla” es HTML table o data-grid custom, te dejo snippets concretos (dialog manager, focus restore, y contrato de componentes: `label`, `description`, `error`, `aria-*`) para estandarizarlo en el design system.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://www.w3.org/TR/WCAG22/

[^2]: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/

[^3]: https://w3c.github.io/wcag21/understanding/error-suggestion.html

[^4]: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/dialog/

[^5]: https://www.w3.org/WAI/WCAG21/Understanding/character-key-shortcuts.html

[^6]: https://dequeuniversity.com/resources/wcag2.1/2.1.4-character-key-shortcuts

[^7]: https://www.digitalpolicy.gov.hk/en/our_work/digital_government/digital_inclusion/accessibility/promulgating_resources/handbook/wcag2a/8_12_character_key_shortcuts.html

[^8]: https://www.youtube.com/watch?v=UjUvrHyMCYc

[^9]: https://www.deque.com/blog/aria-modal-alert-dialogs-a11y-support-series-part-2/

[^10]: https://www.boia.org/wcag2/cp/2.1.4

[^11]: https://www.boia.org/blog/tips-for-meeting-wcags-requirement-for-error-suggestion

[^12]: https://silktide.com/accessibility-guide/the-wcag-standard/2-1/keyboard-accessible/2-1-4-character-key-shortcuts/

[^13]: https://www.digitala11y.com/understanding-sc-3-3-3-error-suggestion/

[^14]: https://github.com/w3c/wcag2ict/issues/76

[^15]: https://www.tpgi.com/the-current-state-of-modal-dialog-accessibility/

