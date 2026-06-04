# systematic-source-discovery

## What it does

Use this skill to design a source search that can be repeated, audited, and improved. It turns a research agenda into search families, Boolean queries, database targets, primary-source targets, inclusion rules, exclusion rules, and a search log.

The purpose is to avoid source gathering by accident. A research book needs more than a pile of interesting articles. It needs a visible search method so the author can explain what was searched, what counted as relevant, and what kinds of opposing evidence were included.

## When to use it

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

Follow the shared procedure in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Quality checks

Apply the shared quality checks in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`; keep any skill-specific caveats visible in the output.

## Failure modes

Use the shared failure modes in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`; call out the skill-specific failure most relevant to the request.

## Files/folders it may read

Follow the shared read boundary in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Files/folders it may write

Follow the shared write boundary in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

## What it must not do

Follow the shared prohibitions in `docs/policy/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Best next steps

After sources are gathered, use `annotated-bibliography-builder` to capture what each source contributes. Then use `literature-review-mapper` to group sources into debates, schools, and gaps.
