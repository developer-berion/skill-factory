<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# KB_06_Design_Systems_Salesforce_HubSpot.md

“Resume patrones y componentes clave de design systems relevantes (ej. Salesforce Lightning Design System) y cómo adaptarlos a un CRM custom. Incluye tokens, theming, estados, guidelines para dev handoff.”

Un CRM “serio” (operativo, data-denso y con muchos estados) se beneficia de un design system tipo SLDS/Canvas porque estandariza **componentes**, tokens, estados y reglas de interacción, y eso baja fricción y costo de cambio a largo plazo. En Salesforce, por ejemplo, los “design tokens” capturan atributos visuales como spacing, tipografías o colores, y en SLDS 2 se impulsa más el uso de variables CSS (“global styling hooks”) para que tus componentes se adapten al branding/tema sin reescribir estilos.[^1]

## Patrones y componentes clave (CRM)

Estos son los “must” que suelen estar muy bien resueltos en sistemas tipo SLDS (enterprise UI) y que conviene copiar/normalizar en un CRM custom:

- Navegación: app launcher/sidebar, breadcrumbs, tabs, “recent items”, búsqueda global.
- List views: tablas densas con sorting, filtros guardados, columnas configurables, selección múltiple, acciones bulk.
- Record pages: header con estado (pipeline/etapa), acciones primarias/secundarias, layout por secciones, timeline/actividad, panel de insights.
- Formularios: inputs, selects, lookups/autocomplete, inline edit, validación, ayuda contextual, máscaras/formatos.
- Overlays: modal, drawer, popover/tooltips (con reglas claras de cuándo usar cada uno).
- Feedback: toasts, banners, empty states, skeleton/loading, errores recuperables vs “hard stop”.
- Permisos/roles: estados “no autorizado” y “solo lectura” como first-class (no como edge case).


## Tokens y theming (cómo montarlo)

Define tokens como el “contrato” entre diseño y código: nombres estables que representan intención visual, no valores sueltos. En Salesforce se describe que los tokens son entidades nombradas para atributos visuales (p. ej., márgenes/espaciado, familias/tamaños de fuente, hex de color).[^1]

Arquitectura recomendada (práctica para CRM):

- Primitive tokens (escala): paletas/rampas y constantes (p. ej., `color.blue.600`, `space.12`, `radius.8`).
- Semantic tokens (roles): lo que la UI “significa” (p. ej., `bg.surface`, `text.primary`, `border.subtle`, `accent.primary`). (Este enfoque de capas ayuda a que el theming sea mapeo, no “renombrar colores”).[^2]
- Component tokens (excepciones): solo si un componente necesita un override consistente y recurrente.[^2]

Theming práctico para CRM custom:

- Implementa tokens como CSS variables (o equivalente en tu stack) para permitir cambios de tema sin recompilar; en el ecosistema Lightning, SLDS 2 reemplaza tokens “clásicos” por variables CSS llamadas global styling hooks.[^1]
- Soporta al menos: tema base (light), tema alterno (dark opcional) y “brand accents” (color primario/links/CTA) desacoplados del resto.

Ejemplo mínimo de “semantic tokens” (idea, no dogma):

```json
{
  "bg": { "canvas": "#F7F9FB", "surface": "#FFFFFF" },
  "text": { "primary": "#111827", "secondary": "#4B5563", "inverse": "#FFFFFF" },
  "border": { "default": "#D1D5DB", "subtle": "#E5E7EB" },
  "accent": { "primary": "#2563EB", "hover": "#1D4ED8", "pressed": "#1E40AF" },
  "status": { "success": "#16A34A", "warning": "#D97706", "danger": "#DC2626" }
}
```


## Estados (UI) y accesibilidad (sin sorpresas)

En CRM lo que más rompe UX es inconsistencia de estados; documenta estados como parte del componente, no como “CSS extra”.

Estados base que debes especificar para cada componente interactivo:

- Default / Hover / Focus / Active(Pressed)
- Disabled / Read-only
- Loading (skeleton o spinner inline)
- Validation: error, warning, success; con mensaje y reglas de persistencia

Reglas que conviene fijar por guideline:

- Focus visible siempre: para usuarios de teclado es obligatorio mostrar el estado de foco; es un requerimiento en WCAG 2.4.7 “Focus Visible”.[^3]
- Contenido que aparece por hover o focus (tooltips/popovers) debe ser descartable, “hoverable” y persistir mientras aplique, según WCAG 1.4.13.[^4]

Tip operativo: en inputs define explícitamente “dirty/touched” vs “error” (cuándo se dispara la validación), porque en CRM hay mucho inline edit y el timing importa para productividad.

## Guidelines para dev handoff (lo que sí evita retrabajo)

Tu handoff debe bajar ambigüedad en: tokens, componentes, estados, y criterios de aceptación.

Checklist de handoff por componente (recomendado):

- API del componente: props/slots/events (p. ej., `value`, `onChange`, `error`, `helpText`, `loading`, `disabled`, `readOnly`).
- Estados documentados con reglas: qué cambia visualmente y qué cambia en comportamiento (tab order, shortcuts, bloqueo de acciones).
- Specs medibles: spacing, tamaños, alturas, densidad (comfortable/compact), truncamiento, responsive.
- Accesibilidad: roles ARIA cuando aplique, navegación por teclado, foco inicial en modales/drawers, labels/aria-describedby para errores.
- Tokens consumidos: lista de semantic tokens permitidos + prohibiciones (ej.: “no uses hex directo en componentes”).
- Ejemplos: 1) caso feliz, 2) caso error, 3) caso vacío, 4) caso loading.

Entrega “living” (para escalar):

- Storybook (o catálogo) con estados y knobs.
- Un paquete de tokens versionado (JSON) + build a CSS variables.
- Changelog y versionado semántico (breaking vs non-breaking).


### Qué incluye / qué no incluye / sensible

Qué incluye:

- Biblioteca de componentes + tokens + guías de estado + patrones CRM (list/record/form/overlays).
- Theming por variables y mapeo semantic→primitive.

Qué no incluye:

- Reglas de negocio del CRM (pipelines, permisos, scoring) — eso va en producto, no en UI kit.
- Diseño “pixel perfect” por pantalla; el DS define piezas y reglas, no layouts únicos.

Sensible (decisiones que cambian costos):

- Nivel de densidad (compact vs comfortable) en tablas y formularios; afecta productividad y accesibilidad.
- Estrategia de theming (solo accents vs theming completo + dark mode).
- Qué tan estricta será la “prohibición” de estilos ad-hoc (si aflojas, el DS se degrada rápido).

Si me dices tu stack (React/Vue/Angular, Tailwind sí/no, CSS-in-JS sí/no) y si el CRM tendrá “multi-tenant branding” (varias marcas), te propongo una estructura de tokens + pipeline de build (safe vs agresivo) para implementarlo sin deuda.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://developer.salesforce.com/docs/platform/lwc/guide/create-components-css-design-tokens.html

[^2]: https://www.setproduct.com/blog/how-to-design-a-ui-kit-foundation

[^3]: https://trailhead.salesforce.com/content/learn/modules/designing-for-web-accessibility/learn-about-visual-state-indicators

[^4]: https://www.w3.org/WAI/WCAG21/Understanding/content-on-hover-or-focus.html

[^5]: https://developer.salesforce.com/docs/atlas.en-us.lightning.meta/lightning/tokens_intro.htm

[^6]: https://developer.salesforce.com/docs/atlas.en-us.lightning.meta/lightning/tokens_standard.htm

[^7]: https://developer.salesforce.com/docs/atlas.en-us.lightning.meta/lightning/tokens_standard_communities.htm

[^8]: https://dbanks.design/blog/documenting-design-tokens/

[^9]: https://samiamdesigns.substack.com/p/part-1-create-living-documentation

[^10]: https://codebycody.com/slds-design-tokens/

[^11]: https://www.lightningdesignsystem.com

[^12]: https://www.wcag.com/authors/1-4-13-content-on-hover-or-focus/

[^13]: https://canvas.hubspot.com

[^14]: https://developer.salesforce.com/docs/atlas.en-us.lightning.meta/lightning/tokens_standard_force_base.htm

[^15]: https://www.lightningdesignsystem.com/2e1ef8501/p/8268ee-input

