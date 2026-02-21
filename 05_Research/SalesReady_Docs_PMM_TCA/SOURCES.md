TASK
Generate a production-ready skill spec file: .skill.md

SKILL ID / SLUG
crm-sales-ready-docs-pmm-tca

ROLE + DOMAIN
Role: Product Marketing Manager Técnico / Technical Content Architect
Domain: CRM B2B — Sales-ready technical/commercial documentation (Solution Architect voice)

SOURCE OF TRUTH (KB FOLDER)
All knowledge is located in:
  /05_Research/CRM/SalesReady_Docs_PMM_TCA/

MANDATORY INPUT FILES (do not ignore)
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_INDEX.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/SOURCES.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_01_Feature_Excellence_As_Guarantee.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_02_Benefit_Functionality_Mapping.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_03_View_Anatomy_Mode.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_04_Data_Logic_Deep_Dive.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_05_Data_Lineage_orientado_a_negocio.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_06_Entity_Dictionary_Semantics.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_07_Functional_Audit_No_Omissions.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_08_Senior_Solution_Architect_Narrative.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_09_Sales_Ready_Markdown_Formatting.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_10_Credibility_Grounding_Claim_Ledger.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_11_Enterprise_Readiness_RBAC_Audit_Compliance.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_12_Measurement_Adoption_Value_Instrumentation.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_13_Dedup_Matching_Explainability.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_14_Dedup_Survivorship_Merge_Policies.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_15_KPI_Cards_Stale_Degraded_Partial_Data.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_16_Data_Incidents_Playbook.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_17_Calculation_Contracts_Testing_Versioning.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_18_Evidence_Standards_Proof_Types.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_19_Claim_Ledger_System.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_20_Analytics_Event_Governance_SemVer.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_21_Value_Attribution_Framework.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_22_ABAC_Policies_for_CRM.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_23_Audit_Logs_Export_Retention_Tamper_Evidence.md
- /05_Research/CRM/SalesReady_Docs_PMM_TCA/KB_24_Semantic_Ownership_Conflict_Resolution.md

NON-NEGOTIABLE RULES
1) Do not invent facts, metrics, formulas, tools, or policies.
2) If a required detail is missing, output `needs_clarification` and ask for the missing artifact or product evidence.
3) Every “sellable claim” must map to an Evidence Standard + Claim Ledger entry pattern (even if placeholders).
4) Maintain strict separation: Facts vs Inferences. Always label them.
5) Prefer reusable templates and checklists over prose.

OUTPUT PATHS
- Skill spec:
  /03_Skills/crm-sales-ready-docs-pmm-tca.skill.md
- Compilation notes:
  /06_Releases/crm-sales-ready-docs-pmm-tca/COMPILATION_NOTES.md

DEFINITION OF DONE (the generated .skill.md MUST contain these sections)
1) Purpose & Scope
   - What the skill does, who it serves, and explicit non-goals.
2) Operating Modes (procedures)
   - Implement at minimum these modes as callable procedures:
     a) Feature Excellence (Guarantee One-Pager)
     b) Benefit–Functionality Mapping (DBPOR)
     c) View Anatomy
     d) Data & Logic Deep Dive (Calculation Spec)
     e) Data Lineage (KPI Lineage Card)
     f) Entity Dictionary (Field Cards)
     g) Functional Audit (No Omissions)
     h) Solution Architect Narrative & Demo Script
     i) Sales-Ready Markdown Formatting (templates)
     j) Claim Ledger creation/check
     k) Enterprise Readiness (RBAC/ABAC/Audit/Retention)
     l) Measurement + Event Governance + Value Attribution
3) Ask-vs-Assume policy
   - Exactly what the skill will ask for vs what it can assume safely.
4) Input/Output Schemas (STRICT)
   - Define JSON schemas for:
     - Product context (modules, personas, environment)
     - View spec input (UI + KPIs + lineage refs)
     - Feature spec input (states, logic, risks, metrics)
     - Calculation spec input (I/O contract, tolerances, tests)
     - Entity dictionary input (fields, validations, ownership)
     - Claims input (claim ledger fields, proof types)
     - Output artifacts (markdown pages, claim ledger table, audit report)
5) Guardrails & Risk Matrix
   - Risks: over-claiming, compliance misstatements, stale data promises, privacy leakage, misleading causality.
   - For each risk: detection + mitigation + required evidence.
6) Observability & Quality Gates
   - Checks: citations present, facts/inferences labeled, claims mapped to proof type, templates used, missing data flagged.
7) Failure Modes & Recovery
   - What to do when: missing lineage, missing RBAC, unclear formula, no proof, conflicting definitions.
8) Tests
   - Smoke tests: run each mode with minimal inputs.
   - Golden tests: at least 2 end-to-end examples:
     - Example A: Deduplicación feature (including matching/explainability + survivorship + merge policy + claims)
     - Example B: Forecast dashboard (KPI cards + lineage + weighted value calculation contract + measurement + attribution notes)
   - Include expected outputs summaries and assertions (no invented metrics; proper labels; templates applied).
9) References
   - For each major mode, reference the KB file(s) that define it.

COMPILATION NOTES REQUIREMENTS (COMPILATION_NOTES.md)
- Files used (list all KB inputs)
- Any missing info flagged as needs_clarification
- Any assumptions made (should be minimal)
- Any conflicts across KBs and how resolved
- Suggested next evidence to collect from the actual CRM product (screenshots, logs, schemas)

STYLE
- Spanish (Venezolano corporativo), directo, elegante. “Arquitecto de Soluciones Senior”.
- Use Markdown with clear headings, checklists, and templates.
- No fluff, no hype.

DELIVERABLE FORMAT
- Produce only the two files at the specified output paths.