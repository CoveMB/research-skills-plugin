---
name: case-study-integration
description: Select, compare, and integrate case studies when examples, analogies, counter-cases, comparison sets, or case dossiers must strengthen a research argument without cherry-picking or overgeneralization.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Case study integration

## Purpose

Help a research book use case studies responsibly. Cases can illustrate, test, complicate, or generate theory, but they should not be treated as proof of universal claims unless the research design supports it.

## When to use

Use when the user needs examples, cases, comparative examples, narrative dossiers, or comparative case design.

## Automatic selection guidance

- High-signal triggers: case study, example selection, analogy, comparison, counter-case, narrative dossier, cherry-picking risk, or generalization limits.
- Light-route behavior: classify the intended case function and name what each case can and cannot prove.
- Deep-work gate: only assess case evidence quality when case sources, notes, datasets, or citations are available.
- Noise and slowdown guard: do not treat illustrative cases as proof of broad causal or universal claims.

## Do not use this skill when

- The user needs a general literature map; use `literature-review-mapper`.
- The user asks whether a source's method is credible; use `methodology-source-auditor`.
- The example is only decorative and does not affect the research argument.

## Inputs expected

- Claim needing a case, candidate cases, source base, chapter context, or comparison set.
- Scope conditions: time period, geography, institutions, actors, and outcome of interest.
- Known counter-cases, failed cases, or cases the user wants to avoid.
- Whether the case is meant to illustrate, test, compare, complicate, or generate theory.

## Source basis and AI limits

Follow `docs/SOURCE_LIMITS.md`: state the source access level, separate source basis from interpretation, include What I can verify, What remains uncertain, and User verification needed. Do not invent citations or source support.

## Case functions

Classify each case as:

- illustrative example
- typical case
- deviant case
- critical case
- comparative case
- precedent
- counterexample
- theory-generating case
- implementation case
- failure case

## Files/folders it may read

- Bundled skill instructions, metadata, and assets if available (including, but not limited to, `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml` in this project or equivalent files in another project).
- Shared policy docs, especially `docs/SOURCE_LIMITS.md` and `docs/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided case notes, source excerpts, timelines, datasets, chapter drafts, and argument artifacts explicitly named in the request.
- Related claim ledgers or chapter briefs when case function depends on the argument.

## Files/folders it may write

- None by default.
- May create or update user-requested case dossiers, comparison tables, or integration plans in the user-designated project or workspace.
- Must not alter original sources, datasets, or manuscript files unless explicitly asked.

## What it must not do

- Do not cherry-pick favorable cases as if they prove a general claim.
- Do not use an illustrative case as causal proof without design support.
- Do not invent timelines, actors, data, or case outcomes.

## Procedure

### 1. Define the claim the case is meant to support

A case must be tied to a claim. Avoid adding cases only because they are interesting.

### 2. Choose case function

Decide whether the case illustrates, tests, complicates, or challenges the argument.

State case-selection logic: why this case, why not others, what comparison class it belongs to, and what selection bias risk remains.

### 3. Evaluate comparability

Check scope, context, time period, institutions, actors, incentives, and data availability.

### 4. Add counter-cases

For high-stakes claims, include cases that challenge or limit the thesis.

### 5. Prevent overclaiming

Provide safer language:

- "This case illustrates..."
- "This case suggests..."
- "This case does not prove..."
- "Under these conditions..."

### 6. Build a case dossier

Include timeline, actors, source base, relevance, limits, and chapter placement.

## Output format

```markdown
# Case study integration plan

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## Claim needing a case

## Case-selection logic

## Candidate cases
| Case | Function | Supports | Challenges | Source base | Selection risk | Generalization limit | Chapter use |

## Recommended case set

## Counter-cases to include

## Case dossier template

## Safer wording for claims

## Limits / failure risks

```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless one skill reduces a named scholarly risk.

## Quality checks

- Do not cherry-pick only successful or favorable cases.
- Do not use a case as causal proof without design support.
- Include failures and counterexamples where they strengthen credibility.
- Make the limits of comparison explicit.
- Do not generalize beyond the case-selection design.

## Failure modes

- Case is interesting but not tied to a claim.
- Comparison ignores key contextual differences.
- Counter-cases are absent, making selection bias invisible.
- Case wording overgeneralizes beyond the evidence base.
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
