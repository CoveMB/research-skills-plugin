# research-book-orchestrator

## What it does

Use this skill when the project needs a map before it needs more text. It looks at the state of a research book and decides which specialized skill should come next. It can route a project through research agenda work, source discovery, literature mapping, argument design, chapter planning, evidence checks, citation review, continuity review, and proposal work.

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

1. State the source basis and source access level.
2. Follow the skill's `SKILL.md` procedure instead of working from memory.
3. Produce the stated output format and keep verified facts, interpretation, speculation, and recommendation separate.
4. End with verification gaps. Add a risk-gated follow-up only when it is useful.

## Quality checks

- Evidence strength must match claim strength.
- Missing source access must be marked clearly.
- Uncertainty, limits, and user verification needs must be visible.
- Output should preserve scholarly caution without becoming vague.

## Failure modes

- Fabricated citations, quotes, page numbers, source metadata, datasets, market facts, or field consensus.
- Confident synthesis from partial sources.
- Generic prose or structure that hides weak evidence or weak reasoning.
- Overstated claims, missing counterarguments, or unclear source basis.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml` when present and relevant.
- User-provided drafts, notes, sources, artifacts, or project files explicitly named in the request.
- Shared project documentation when it is needed for workflow, quality, or artifact compatibility.

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

After this skill, use the skill it recommends. Early projects often move to `scholarly-research-agenda`. Projects with sources often move to `literature-review-mapper` or `annotated-bibliography-builder`. Draft-heavy projects often move to `claim-evidence-ledger`, `chapter-architecture`, or `manuscript-continuity-editor`.
