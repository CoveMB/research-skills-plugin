# claim-evidence-ledger

## What it does

Use this skill to turn a chapter, outline, thesis, or draft into a ledger of claims. It extracts the claims that carry the argument, classifies each one, checks evidence status, flags overclaiming, and suggests safer wording.

This is one of the best safeguards against research prose that sounds confident but outruns the evidence. It helps the author see which sentences are interpretive, which need citations, which need stronger evidence, and which should be narrowed.

## When to use it in the book writing process

Use it before polishing prose and before citation integrity review. It works well after a chapter draft exists, after an argument architecture has been built, or before sending a chapter to readers.

Use it when a draft has too many broad claims, causal claims, predictions, historical claims, or field-specific statements that may need support.

## Good inputs

- A chapter draft, section draft, outline, or thesis tree.
- Available sources or notes, if any.
- The intended audience and level of evidentiary rigor.
- Questions about which claims are too strong or unsupported.

## Example requests

```text
Extract the major claims from this chapter and build a claim-evidence ledger.
```

```text
Tell me which claims need citations, which are interpretive, and which are overstated.
```

```text
Rewrite the risky claims in safer language without weakening the argument too much.
```

## Typical output

Expect a table with claim, claim type, evidence status, current support, evidence needed, risk, and safer wording. The output also lists high-risk claims, claims that can remain interpretive or normative, source priorities, and the next best skill.

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

After this skill, use `citation-integrity-auditor` to verify citation placement, source-claim fit, quotes, page numbers, and bibliography issues. Use `scholarly-prose-editor` once the claim support is stable.
