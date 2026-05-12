# research-book-orchestrator

## What it does

Use this skill when the project needs a map before it needs more text. It looks at the state of a research book and decides which specialized skill should come next. It can route a project through accessibility triage, research agenda work, source discovery, literature mapping, argument design, chapter planning, evidence checks, citation review, continuity review, and proposal work.

Use it when the author feels stuck because there are too many possible next steps. Should the project search for sources, sharpen the thesis, outline chapters, audit citations, or revise prose? This skill answers that by diagnosing the manuscript stage and building a practical sequence of work.

## When to use it

Use it at the beginning of a book project, after a long pause, before a major revision, or whenever the project has sprawled. It works well as a first pass for a new research book because it turns a broad idea into a staged workflow with deliverables.

Use it again when the project changes shape. For example, if a literature map reveals a stronger thesis, the orchestrator can reset the sequence and decide whether to move into argument architecture, chapter architecture, or evidence auditing.

## Good inputs

- A book premise or working thesis.
- A table of contents, even if rough.
- Notes about the audience, field, deadline, or intended press.
- A list of available materials, such as sources, chapter drafts, interviews, or case notes.
- A description of where the author feels blocked.
- Any rough-note, dictation, spelling, or reading-load constraint that affects the first step.

## Example requests

```text
I am writing a research book about the politics of urban climate adaptation. Build a staged workflow from idea to proposal.
```

```text
I have a thesis, three chapter drafts, and a rough bibliography. Tell me which skill sequence should come next and why.
```

```text
My project has too many sources and no clear structure. Diagnose the phase and give me the next three deliverables.
```

## Typical output

Expect a workflow plan, not a finished chapter. The output usually includes a project diagnosis, assumptions, recommended skill sequence, immediate next deliverable, quality gates, and a longer manuscript roadmap.

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

After this skill, use the skill it recommends. Projects blocked by text friction often move to the smallest accessibility entry point in `docs/ROUTING_MATRIX.md`. Early projects often move to `scholarly-research-agenda`. Projects with sources often move to `literature-review-mapper` or `annotated-bibliography-builder`. Draft-heavy projects often move to `claim-evidence-ledger`, `chapter-architecture`, or `manuscript-continuity-editor`.
