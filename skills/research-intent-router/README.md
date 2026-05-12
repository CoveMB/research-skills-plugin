# research-intent-router

Routes scholarly nonfiction research prompts to the smallest useful skill. It protects speed and rigor by using light routing first and allowing deep lookup only when it materially improves evidence quality.

## Research modes

Normal mode is the default. Use it for plan-first routing: classify the request, choose the smallest useful skill, and only do deep lookup when the deep-work gate is met.

Deep mode always attempts deep lookup for scholarly research tasks after routing. It still labels source access, refuses fabricated evidence, and marks lookup as unavailable when tools or full text are missing.

Switches:

- `research normal mode`
- `research deep mode`

## When to use it

Use at the start of a research interaction, when the user's next step is unclear, or when a request could match several research-book skills.

Use the smallest accessibility skill first when text friction blocks the user's intended claim or next action: `dictation-to-research-notes` for voice transcripts, `reading-load-reducer` for dense material, `dyslexia-friendly-prose-editor` for existing prose repair, and `dyslexia-research-companion` when the bottleneck is mixed.

## Useful inputs

- Topic, thesis, question, draft, source list, bibliography, chapter, manuscript, or proposal.
- Any available source access: full text, excerpt, citation only, or no source material.
- The user's goal: plan, discover, map, audit, draft, revise, verify, or propose.

## Procedure

Follow the shared procedure in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Quality checks

Apply the shared quality checks in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`; keep any skill-specific caveats visible in the output.

## Failure modes

Use the shared failure modes in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`; call out the skill-specific failure most relevant to the request.

## Files/folders it may read

Follow the shared read boundary in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Files/folders it may write

Follow the shared write boundary in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## What it must not do

Follow the shared prohibitions in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Best next steps

Use the optional `## Suggested next step` section only when one follow-on skill reduces a named scholarly risk. Common gated routes:

- Use `scholarly-research-agenda` for broad topics whose scope is unstable.
- Use `dictation-to-research-notes`, `reading-load-reducer`, `dyslexia-friendly-prose-editor`, or `dyslexia-research-companion` when text friction prevents reliable routing.
- Use `systematic-source-discovery` when the question is stable but no corpus exists.
- Use `claim-evidence-ledger` before citation audit on unsupported drafts.
- Use `citation-integrity-auditor` only when citations, quotes, pages, bibliography entries, or cited claims need audit.
