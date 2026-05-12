# Research Intent Router

Routes scholarly nonfiction research prompts to the smallest useful skill. It protects speed and rigor by using light routing first and allowing deep lookup only when it materially improves evidence quality.

## Research modes

Normal mode is the default. Use it for plan-first routing: classify the request, choose the smallest useful skill, and only do deep lookup when the deep-work gate is met.

Deep mode always attempts deep lookup for scholarly research tasks after routing. It still labels source access, refuses fabricated evidence, and marks lookup as unavailable when tools or full text are missing.

Switches:

- `research normal mode`
- `research deep mode`

## When to use it

Use at the start of a research interaction, when the user's next step is unclear, or when a request could match several research-book skills.

## Useful inputs

- Topic, thesis, question, draft, source list, bibliography, chapter, manuscript, or proposal.
- Any available source access: full text, excerpt, citation only, or no source material.
- The user's goal: plan, discover, map, audit, draft, revise, verify, or propose.

## Procedure

1. Detect whether the prompt is a scholarly research task.
2. Classify intent, artifact stage, source access level, and risk level.
3. Choose the smallest useful skill or a short 2-4 skill sequence.
4. Apply normal mode or deep mode.
5. State what can be verified, what remains uncertain, and what the user must verify.

## Quality checks

- Route choice must reduce a concrete scholarly risk.
- Deep lookup must be denied unless it is explicitly requested or needed for evidence quality.
- Deep mode must attempt lookup where available without treating unavailable lookup as verified.
- The answer must label source access and verification limits.
- Do not invent citations, page numbers, quotes, DOIs, field consensus, or source metadata.

## Failure modes

- Treating any mention of a topic as permission for live source search.
- Routing to multiple skills when one skill is enough.
- Claiming field consensus from model knowledge only.
- Auditing citations before extracting claims from an uncited draft.
- Ignoring pure fiction, casual opinion, or grammar-only requests that should not trigger.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, and `agents/openai.yaml`.
- Routing docs such as `docs/SKILL_INDEX.md`, `MODE_REGISTRY.md`, and `docs/ARCHITECTURE.md` when package-level context matters.
- User-provided files explicitly named in the request.

## Files/folders it may write

- None by default.
- User-requested workflow notes or routing artifacts in the current project.

## What it must not do

- Do not browse, validate sources, or verify citations by default.
- Do not treat model knowledge as source verification.
- Do not route casual, fictional, grammar-only, or non-research tasks.

## Best next steps

Use the optional `## Suggested next step` section only when one follow-on skill reduces a named scholarly risk. Common gated routes:

- Use `scholarly-research-agenda` for broad topics whose scope is unstable.
- Use `systematic-source-discovery` when the question is stable but no corpus exists.
- Use `claim-evidence-ledger` before citation audit on unsupported drafts.
- Use `citation-integrity-auditor` only when citations, quotes, pages, bibliography entries, or cited claims need audit.
