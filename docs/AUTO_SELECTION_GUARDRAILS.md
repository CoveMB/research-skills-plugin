# Auto-selection guardrails

Use this shared policy when deciding whether a research-book skill should trigger automatically.

## Required fields

Each skill should define:

- High-signal triggers: prompt features that strongly indicate the skill is useful.
- Light-route behavior: the smallest useful response before deeper work.
- Deep-work gate: conditions that justify lookup, source validation, citation audit, or other expensive work.
- Noise and slowdown guard: cases where the skill should not expand scope.

## Selection rules

- Prefer the smallest useful skill over a broad sequence.
- Use the router when multiple skills could reasonably own the request.
- Prefer plan-first routing unless the user selects deep mode or the deep-work gate is met.
- Do not trigger on casual, fictional, grammar-only, or non-research tasks.
- Do not perform deep lookup when it would not reduce a concrete scholarly risk.

## Suggested next step policy

The final `## Suggested next step` section is optional, risk-gated, and should be omitted by default unless it reduces a concrete scholarly risk.

Add the section only when all gates pass:

- A specific unresolved scholarly risk remains.
- One skill clearly reduces that named scholarly risk.
- The required input for that skill exists or can be requested.
- The suggestion does not require automatic lookup unless normal mode or deep mode allows it.
- The explanation fits in 2-4 lines.

Required format:

```md
## Suggested next step

Use `skill-name` to [specific next action].
Why this helps scholarship: [named risk reduced].
Use only if: [condition].
Skip if: [reason it would add noise now].
```

One suggested skill max. Do not add generic skill menus, broad "also use" prompts, or a skill sequence unless the router is explicitly producing a route.

Do not suggest `citation-integrity-auditor` before citations, quotes, page numbers, bibliography entries, or cited claims exist. Use source-access labels visibly: user-provided full text, excerpt only, citation only, model knowledge only, or live or current search needed. Use cautious verbs such as can test, can audit, or can map; do not claim the next skill will prove or verify something without source access.

Omit the section when no specific unresolved scholarly risk remains.
Omit the section when no one skill clearly reduces the remaining risk.
Omit the section for grammar-only edits, casual answers, finished narrow tasks, or when the user asks to just answer.
Omit the section when it would add noise.
