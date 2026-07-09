# Raw materials to manuscript

Use this workflow when you have idea notes, research logs, source notes, tables, figures, outlines, or draft fragments and want a safer path toward a manuscript.

The workflow does not make raw material trustworthy by itself. It helps you sort what you have, decide what can support a draft, and see which checks must happen before a claim becomes manuscript-ready.

## Start here

```text
Use research-book-orchestrator. I have an idea summary, research notes, source notes, and draft visuals. Build a raw-materials-to-manuscript workflow with quality gates.
```

## What the workflow produces

- A raw-materials bundle that points to the materials and labels access, privacy, rights, and use limits.
- A research agenda or chapter brief that says what the manuscript is trying to do.
- Section-level source discovery tasks for claims that still need evidence.
- Source notes, extraction tables, literature maps, and argument artifacts before confident drafting.
- Review and refinement passes that preserve unresolved risks instead of hiding them.
- Figure/table and integrity checks before visuals, tables, or generated syntheses support manuscript claims.

## What must stay visible

- A planned search is not a completed search.
- A source metadata check is not proof that the source supports a claim.
- A nearby citation is not support by proximity.
- A generated visual is not cleared evidence until provenance, caption, rights, and human review are visible.
- A revised paragraph is not safer if it removes uncertainty that still matters.

## Good first prompt

```text
Use research-book-orchestrator. Turn these materials into a workflow plan. First inventory what is visible, then tell me the smallest next artifact and what must hold before drafting.
```

## Good follow-up prompts

```text
Use systematic-source-discovery. Turn this chapter outline into section-level search tasks. Keep planned searches separate from completed searches.
```

```text
Use counterargument-peer-review. Review this thesis and create a repair queue for the next revision pass.
```

```text
Use figure-table-integrity-auditor. Make a visual evidence plan for these planned charts. Do not clear them for manuscript use yet.
```

## When to stop

Stop and repair the workflow when:

- the draft claims field coverage from a partial or planned search
- source metadata is treated as source-claim support
- a figure or table lacks data, caption, rights, or provenance records
- revision removes claim IDs, unresolved risks, or source limits
- the project needs external lookup but private text has not been cleared for external use

## Before external sharing

Run `ai-human-workflow-log` if AI-assisted work will be shown to collaborators, reviewers, presses, committees, or the public.

Run `rights-privacy-release-auditor` before sharing source packets, notes, proposal materials, manuscript exports, or generated artifacts outside the project.
