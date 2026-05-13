# claim-evidence-ledger

## What it does

Use this skill to turn a chapter, outline, thesis, or draft into a ledger of claims. It extracts the claims that carry the argument, classifies each one, checks evidence status, flags overclaiming, and suggests safer wording.

Use it to catch research prose that sounds confident but outruns the evidence. It shows which sentences are interpretive, which need citations, which need stronger evidence, and which should be narrowed.

## When to use it

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

Expect a table with claim, claim type, evidence status, current support, evidence needed, risk, and safer wording. The output also lists high-risk claims, claims that can remain interpretive or normative, source priorities, and a risk-gated follow-up when it is useful. Ask for compact output when you want only the claims whose evidence status changes the next action. Compact output should include `How to use this result: TRIAGE ONLY - Use this only to spot visible claim risks; do not treat it as final evidence clearance.` It changes output shape, not route selection or evidence requirements.

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

After this skill, use `citation-integrity-auditor` to verify citation placement, source-claim fit, quotes, page numbers, and bibliography issues. Use `scholarly-prose-editor` once the claim support is stable.
