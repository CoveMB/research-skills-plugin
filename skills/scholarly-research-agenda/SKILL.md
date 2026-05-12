---
name: scholarly-research-agenda
description: Turn a broad research book idea into precise research questions, scope boundaries, contribution claims, key terms, evidence needs, and an initial research agenda. Use before source gathering or outlining.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Research Agenda

## Purpose

Transform a broad nonfiction or research book idea into a disciplined research agenda: central question, subquestions, scope boundaries, key terms, provisional thesis, contribution, and evidence plan.

## When to use

Use this when the user has a broad intellectual project, book premise, thesis idea, manifesto, research theme, or interdisciplinary question and needs it made researchable.

## Inputs expected

- Working topic or book premise
- Intended audience
- Discipline or fields involved
- Current thesis or intuition
- Preferred examples, source types, scope boundaries, or authors
- Constraints such as word count, timeline, or academic/public style

If inputs are missing, proceed with assumptions and label them.

## Source basis and AI limits

Before creating the agenda, state the source access level as one of:

- user-provided full text
- excerpt only
- citation only
- model knowledge only
- live/current search needed

Every output must separate source basis, what can be verified from available material, what remains uncertain, and what the user must verify. Do not invent citations, page numbers, quotations, DOIs, datasets, market facts, field consensus, source metadata, or claims of having searched a database. Separate verified facts, interpretation, speculation, and recommendation.

## Files/folders it may read

- This skill's `SKILL.md`, `README.md`, `assets/research-agenda-template.md`, and `agents/openai.yaml`.
- User-provided book premises, notes, outlines, bibliographies, or project files explicitly named in the request.
- Repository quality docs when the user asks for contract-compatible or workflow-aligned artifacts.

## Files/folders it may write

- None by default.
- May create or update a user-requested research agenda artifact in the current project.
- Must not modify source texts, citation databases, or plugin files unless explicitly asked.

## What it must not do

- Do not present a provisional thesis as established.
- Do not turn an evocative topic into a false research question.
- Do not invent evidence availability, field consensus, sources, or definitions.

## Procedure

### 1. Identify the intellectual object

Clarify what the book is actually about. Separate:

- object of study
- problem or puzzle
- stakes
- proposed intervention
- audience

### 2. Separate question types

Classify candidate questions as:

- descriptive: what is happening?
- contextual/developmental: how did it emerge or change?
- conceptual: what does the term mean?
- causal: why does it happen?
- comparative: how does it differ across cases?
- normative: what should be done?
- practical/design: how could institutions, systems, or practices change?
- speculative: what might happen under uncertain future conditions?

### 3. Define scope boundaries

Set explicit boundaries:

- time period
- geography
- fields
- kinds of evidence
- included/excluded cases
- primary audience
- terms that need definition

### 4. Draft a contribution claim

State what the book may add. Use modest language if evidence is not yet established.

Weak: "This book proves X."

Stronger: "This book argues that X becomes more plausible when Y and Z are considered together, while acknowledging A and B as limits."

### 5. Build an evidence plan

For each major claim, specify the evidence needed:

- primary or source materials
- peer-reviewed empirical studies
- theoretical or conceptual work
- documentation or reference material
- interviews or field notes where available
- quantitative or qualitative data
- case-study dossiers
- opposing literature

### 6. Identify risks

Flag risks such as excessive breadth, weak evidence availability, unstated assumptions, anachronism, presentism, single-cause explanation, or unclear audience.

### 7. Run a feasibility check

Assess whether the project is answerable at book scale. Check scope size, likely evidence availability, field coverage, missing disciplines, source access barriers, and whether the central question can produce a defensible thesis instead of only a theme.

## Output format

```markdown
# Research Agenda

## Source basis

## What I can verify

## What remains uncertain

## User verification needed

## One-sentence project definition

## Central research question

## Subquestions
| Question | Type | Why it matters | Evidence needed | Risk |

## Provisional thesis

## Contribution claim

## Scope boundaries

## Key terms requiring definition

## Evidence plan
| Claim area | Source types needed | Priority | Notes |

## Risks and mitigation

## Feasibility check
| Dimension | Assessment | Risk | Needed next step |

## Limits / failure risks

## Next best skill
```

## Quality checks

- The central question must be answerable, not merely evocative.
- Normative claims must not masquerade as empirical claims.
- Each major question must imply a source strategy.
- The project must have boundaries tight enough to write a chapter, not a conversation topic.
- Treat the provisional thesis as provisional until source discovery and literature mapping test it.

## Failure modes

- Scope remains too broad to research.
- Question mixes empirical, normative, and speculative claims without separation.
- Agenda assumes sources exist without verification.
- Contribution claim overstates novelty before literature mapping.
