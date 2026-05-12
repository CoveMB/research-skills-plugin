---
name: case-study-integration
description: Select, compare, and integrate case studies into research arguments while avoiding cherry-picking, weak analogy, anecdotal overreach, and unsupported generalization.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Case Study Integration

## Purpose

Help a research book use case studies responsibly. Cases can illustrate, test, complicate, or generate theory, but they should not be treated as proof of universal claims unless the research design supports it.

## When to use

Use when the user needs examples, cases, comparative examples, narrative dossiers, or comparative case design.

## Inputs expected

- Claim needing a case, candidate cases, source base, chapter context, or comparison set.
- Scope conditions: time period, geography, institutions, actors, and outcome of interest.
- Known counter-cases, failed cases, or cases the user wants to avoid.
- Whether the case is meant to illustrate, test, compare, complicate, or generate theory.

## Source basis and AI limits

Before selecting or integrating cases, state the source access level as one of:

- user-provided full text
- excerpt only
- citation only
- model knowledge only
- live/current search needed

Every output must separate source basis, what can be verified from available material, what remains uncertain, and what the user must verify. Do not invent citations, page numbers, quotations, DOIs, datasets, market facts, field consensus, source metadata, or claims of having searched a database. Separate verified facts, interpretation, speculation, and recommendation.

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

- This skill's `SKILL.md`, `README.md`, `assets/case-study-dossier-template.md`, and `agents/openai.yaml`.
- User-provided case notes, source excerpts, timelines, datasets, chapter drafts, and argument artifacts explicitly named in the request.
- Related claim ledgers or chapter briefs when case function depends on the argument.

## Files/folders it may write

- None by default.
- May create or update user-requested case dossiers, comparison tables, or integration plans in the current project.
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
# Case Study Integration Plan

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

## Next best skill
```

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
