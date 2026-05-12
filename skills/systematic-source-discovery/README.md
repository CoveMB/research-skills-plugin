# systematic-source-discovery

## What it does

Use this skill to design a source search that can be repeated, audited, and improved. It turns a research agenda into search families, Boolean queries, database targets, primary-source targets, inclusion rules, exclusion rules, and a search log.

The purpose is to avoid source gathering by accident. A serious research book needs more than a pile of interesting articles. It needs a visible search method so the author can explain what was searched, what counted as relevant, and what kinds of opposing evidence were included.

## When to use it in the book writing process

Use it after the research agenda is clear and before the literature review map. It is also useful when the bibliography looks one-sided, when the author has relied too heavily on familiar sources, or when the project needs a documented search trail for academic review.

Use it again when a new chapter opens a new field, case, or historical period.

## Good inputs

- Central research question and subquestions.
- Terms, synonyms, and fields involved.
- Known authors, debates, cases, or source types.
- Preferred search venues or library access.
- Inclusion and exclusion concerns, such as dates, geography, methods, languages, or source quality.

## Example requests

```text
Build a source discovery plan for a book about community health workers and public health systems.
```

```text
Create search families, Boolean queries, and inclusion rules for my research agenda.
```

```text
I have mostly supportive sources. Design searches that will find opposing literatures and counterexamples.
```

## Typical output

Expect a source discovery plan with search families, a query bank, priority venues, inclusion and exclusion criteria, citation-chaining plan, primary-source targets, opposing-literature targets, and a search log template.

## Procedure

1. Establish source basis and source access level.
2. Use the skill's `SKILL.md` procedure, not memory-only shortcuts.
3. Produce the stated output format and separate verified facts, interpretation, speculation, and recommendation.
4. End with verification gaps and the next best skill or repair step.

## Quality checks

- Evidence strength must match claim strength.
- Missing source access must be marked, not hidden.
- Uncertainty, limits, and user verification needs must be visible.
- Output should preserve scholarly caution without becoming vague.

## Failure modes

- Fabricated citations, quotes, page numbers, source metadata, datasets, market facts, or field consensus.
- Confident synthesis from partial sources.
- Generic prose or structure that hides weak evidence.
- Overstated claims, missing counterarguments, or unclear source basis.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml` when present and relevant.
- User-provided drafts, notes, sources, artifacts, or project files explicitly named in the request.
- Shared project documentation only when needed for workflow, quality, or artifact compatibility.

## Files/folders it may write

- None by default.
- May create or update user-requested research artifacts, notes, drafts, or review files in the current project.
- Must not overwrite source material, bibliography databases, manuscript files, or plugin files without explicit user request.

## What it must not do

- Invent missing scholarly facts or verification.
- Treat unavailable evidence as confirmed.
- Use style polish to mask weak argument, weak sources, or unsupported claims.
- Claim external searches, source checks, or database access that did not happen.

## Best next steps

After sources are gathered, use `annotated-bibliography-builder` to capture what each source contributes. Then use `literature-review-mapper` to group sources into debates, schools, and gaps.
