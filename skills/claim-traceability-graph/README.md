# claim-traceability-graph

## What it does

Use this skill to see whether claims can be traced back to source notes, citekeys, locators, and evidence status. It catches orphan claims and broken support chains.

It is a chain audit, not a general claim ledger. It works best when claims or source notes already exist.

## When to use it

Use it after a claim ledger, source notes, or cited draft exists and before citation polish or external review.

Use it when a manuscript has citations but the support chain is hard to follow.

## Good inputs

- Draft passage, claim list, outline, or note set.
- Claim ledger, source notes, citekeys, bibliography, or citation list.
- Locator data and known verification status when available.
- Chapter or section where each claim appears.

## Example requests

```text
Map these claims to source notes, citekeys, locators, and evidence status.
```

```text
Find orphan claims and broken evidence chains in this chapter.
```

```text
Show which cited claims still need source-note or locator repair.
```

## Typical output

Expect a traceability table with claim text, claim type, source note pointer, citekey, locator need, verification status, missing link, and repair action. Optional graph notation can be included when it helps.

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

After this skill, use `citation-integrity-auditor` only when source text, citations, quotes, or locators exist to check. Use `claim-evidence-ledger` first if the claims have not been extracted.
