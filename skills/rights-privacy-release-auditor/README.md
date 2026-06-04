# rights-privacy-release-auditor

## What it does

Use this skill to audit research materials before they leave the project. It checks for privacy, copyright, quote, license, secret, credential, and local metadata risks.

It reports risks and required fixes. It does not rewrite, delete, send, publish, or clear material legally.

## When to use it

Use it before sharing notes, source packets, manuscript exports, proposal packets, or research artifacts with outside readers, editors, agents, presses, committees, or public venues.

Use it when the cost of accidental disclosure or copied source text would be high.

## Good inputs

- Files, notes, exports, proposal materials, or artifact lists.
- Intended recipient and whether the material will be public.
- Known permissions, licenses, quotation policies, or privacy constraints.
- Whether the user wants audit only or a later repair pass.

## Example requests

```text
Audit this proposal packet before I send it to an editor.
```

```text
Check these research notes for privacy, copied source text, quote locator, and local metadata risks.
```

```text
Give me a release verdict for these manuscript exports without rewriting them.
```

## Typical output

Expect an issue table with severity, file or artifact pointer, risk, required fix, and release impact, plus a release verdict. Ask for compact output when you want only release blockers and one send/hold next action. Compact output should include `How to use this result: BLOCKER SUMMARY - This lists visible release blockers only; do not treat it as legal clearance or permission to publish.` It changes output shape, not route selection or evidence requirements.

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

After this skill, repair the flagged files only if the user asks. Use `citation-integrity-auditor` for quote and locator problems that need source-text verification.
