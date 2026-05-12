# dyslexia-research-companion

Use this skill as an accessibility router and wrapper when several text-friction bottlenecks overlap and no smaller accessibility skill clearly owns the first pass.

It turns mixed rough thoughts, typo-heavy notes, dictation fragments, dense source material, or unclear accessibility requests into a low-load route and, when needed, a compact structure. It preserves meaning, flags only ambiguities that matter, and keeps evidence gaps visible.

## What it does

It chooses the smallest accessibility route, then produces only the low-load structure needed for the next scholarly action.

## When to use it

- The task mixes dictation, rough notes, spelling ambiguity, dense material, reading fatigue, or existing prose repair.
- The user asks for broad dyslexia or dysorthographia support but the first concrete bottleneck is unclear.
- The user needs one low-load next action before research agenda, argument, chapter, evidence, or prose work.

Use `dictation-to-research-notes` for voice transcripts only, `reading-load-reducer` for source triage only, and `dyslexia-friendly-prose-editor` for existing prose repair only.

## Good inputs

- Rough notes, transcripts, fragments, or draft passages.
- The intended use: idea capture, reading triage, claim cleanup, chapter planning, or prose bridge.
- Any terms, claims, or voice features that must be preserved.
- Source material or locators when evidence support matters.

## Example requests

```text
Use dyslexia-research-companion. I have a voice transcript, typo-heavy fragments, and a source pile. Choose the smallest low-load first step and keep ambiguities visible.
```

```text
Use dyslexia-research-companion. I am not sure whether this needs dictation cleanup, reading triage, or prose repair. Route it and do only the first useful step.
```

```text
Use dyslexia-research-companion. Turn these mixed fragments into a low-load route, then ask only questions that change the argument or next action.
```

## Typical output

Expect short sections, tables, and stable labels. The output usually includes cleaned core idea, claim/evidence/action table, important ambiguities, verification gaps, and one risk-gated next step when useful.

## Boundaries

This skill does not verify sources unless source material or lookup permission is available. It does not replace the smaller accessibility skills, source discovery, literature mapping, claim audit, citation audit, or prose editing when those specialist tasks clearly own the work.

It should not turn rough text into confident scholarly claims without evidence status. It should not hide missing locators, uncertain terms, or unsupported claims.

## Procedure

Follow the shared procedure in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Quality checks

Apply the shared quality checks in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`; keep accessibility-specific ambiguity and meaning-preservation checks visible in the output.

## Failure modes

Use the shared failure modes in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`; call out overcorrection, long output, or hidden evidence gaps when relevant.

## Files/folders it may read

Follow the shared read boundary in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Files/folders it may write

Follow the shared write boundary in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## What it must not do

Follow the shared prohibitions in `docs/SKILL_OPERATIONAL_BOUNDARIES.md`.

## Best next steps

After this skill, use the smallest specialist skill that resolves the visible bottleneck: `dictation-to-research-notes` for voice transcripts, `reading-load-reducer` for source triage, `dyslexia-friendly-prose-editor` for meaning-preserving prose repair, `scholarly-research-agenda` for scope, `argument-architecture` for claim structure, or `claim-evidence-ledger` for evidence risk.
