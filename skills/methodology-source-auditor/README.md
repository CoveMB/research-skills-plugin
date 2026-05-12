# methodology-source-auditor

## What it does

Use this skill to judge whether sources are strong enough for the claims a research book wants to make. It looks at source type, author expertise, venue, method, evidence quality, transparency, bias risk, recency, generalizability, and relation to opposing evidence.

This skill is useful because not every source can do the same job. A memoir may be valuable as a primary source, but weak as proof of a broad social trend. A report may provide useful data, but still need scrutiny if the organization has an incentive to frame the issue in a particular way.

## When to use it in the book writing process

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

The output usually includes a source audit table with type, method, credibility, bias risk, supportable claims, unsupported claims, and use recommendation. It also lists high-risk sources, missing stronger evidence, recommended upgrades, and the next skill to use.

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

After this skill, use `claim-evidence-ledger` to connect claims to evidence. Use `citation-integrity-auditor` later, once draft citations and quoted material are in place.
