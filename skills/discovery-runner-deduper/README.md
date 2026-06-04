# discovery-runner-deduper

## What it does

Use this skill to process candidate source exports after a discovery run. It dedupes records, logs where they came from, supports screening, and drafts search-log updates.

It is for search results already in hand. If the user only has a topic, design the search first.

## When to use it

Use it after a source discovery plan has produced candidate records from an academic index, library catalogue, bibliography export, tabular file, or pasted record set (for example, OpenAlex, Semantic Scholar, Elicit, scite, library catalogues, CSV, BIB, or RIS).

Use it when duplicate records, fuzzy metadata, or undocumented screening decisions are making the source trail hard to audit.

## Good inputs

- Search plan or completed search log.
- Candidate export, bibliography export, tabular file, or pasted records (for example, CSV, BIB, or RIS).
- Venue, query, date, filters, and candidate count.
- Inclusion and exclusion criteria.
- Permission status for any network or API lookup.

## Example requests

```text
Dedupe this tabular candidate export (CSV) and draft a search-log update.
```

```text
Process these bibliography records (RIS) into duplicate clusters, keep/reject decisions, and metadata confidence.
```

```text
Screen these academic index candidates (OpenAlex) against my inclusion criteria without adding them to the bibliography.
```

## Typical output

Expect search status, candidate matrix, duplicate clusters, keep/reject log, search-log update draft, and follow-up metadata checks.

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

After this skill, use `annotated-bibliography-builder` for kept sources that have enough visible material. Use `methodology-source-auditor` for sources whose method or source strength is uncertain.
