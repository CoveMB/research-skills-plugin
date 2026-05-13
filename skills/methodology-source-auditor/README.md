# methodology-source-auditor

## What it does

Use this skill to judge whether sources are strong enough for the claims a research book wants to make. It looks at source type, author expertise, venue, method, evidence quality, transparency, bias risk, recency, generalizability, and relation to opposing evidence.

Not every source can do the same job. A memoir may be valuable as a primary source, but weak as proof of a broad social trend. A report may provide useful data, but still need scrutiny if the organization has an incentive to frame the issue in a particular way.

## When to use it

Use it after source discovery, during annotation, before claim-evidence auditing, and before a draft relies heavily on a source. It is especially important for causal claims, controversial claims, recent events, policy claims, and case-study generalizations.

Use it when the author is unsure whether a source should be core evidence, context, counterpoint, or an object of critique.

## Good inputs

- Source metadata, abstracts, excerpts, methods sections, reports, articles, datasets, or notes.
- The claim each source is supposed to support.
- The book's field, audience, and evidentiary standard.
- Any known conflicts of interest, publication context, or methodological concerns.

## Example requests

```text
Audit these sources and tell me what each one can and cannot support in my manuscript.
```

```text
This chapter relies on two reports and one case study. Check whether that evidence is strong enough for the claims.
```

```text
Classify these sources as core evidence, context, counterpoint, or not suitable for the argument.
```

## Typical output

The output usually includes a source audit table with type, method, credibility, bias risk, supportable claims, unsupported claims, and use recommendation. It also lists high-risk sources, missing stronger evidence, recommended upgrades, and a risk-gated follow-up when it is useful. Ask for compact output when you want source-use triage focused on what each source can and cannot support. Compact output should include `How to use this result: TRIAGE ONLY - Use this only for provisional source-use triage; do not treat it as method or evidence verification when access is limited.` It changes output shape, not route selection or evidence requirements.

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

After this skill, use `claim-evidence-ledger` to connect claims to evidence. Use `citation-integrity-auditor` later, once draft citations and quoted material are in place.
