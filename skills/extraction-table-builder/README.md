# extraction-table-builder

## What it does

Use this skill to turn source notes, annotations, excerpts, or reading notes into extraction tables and source matrices. It helps compare sources before synthesis.

It is useful when the problem is not "write the argument yet" but "make the evidence comparable."

## When to use it

Use it after source notes or annotations exist and before literature mapping, claim drafting, or chapter synthesis.

Use it when the source base is uneven and the author needs to see what each source can actually support.

## Good inputs

- Source notes, annotations, excerpts, PDFs, or bibliographies.
- Research question, chapter question, variables, or codes.
- Source metadata, citekeys, source types, methods, and locators.
- Desired output format, such as Markdown table or source matrix.

## Example requests

```text
Build an extraction table from these source notes before I synthesize them.
```

```text
Turn these annotations into a source matrix with method, evidence type, relevance, and limitations.
```

```text
Compare these sources only where the notes give enough evidence.
```

## Typical output

Expect source-level and passage-level extraction tables, a cross-source comparison matrix when supported, coding decisions, follow-up questions, and a list of uneven or insufficient extraction.

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

After this skill, use `literature-review-mapper` when the extraction is broad enough to map debates. Use `claim-evidence-ledger` when the extraction is ready to support draft claims.
