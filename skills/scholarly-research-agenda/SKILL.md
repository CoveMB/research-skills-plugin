---
name: scholarly-research-agenda
description: Turn a broad research book idea, topic, thesis intuition, manifesto, or interdisciplinary question into precise research questions, scope boundaries, contribution claims, key terms, evidence needs, and an initial agenda before source gathering or outlining.
license: MIT
metadata:
  version: "1.0.0"
  category: research-book-writing
---
# Research agenda

## Purpose

Transform a broad nonfiction or research book idea into a disciplined research agenda: central question, subquestions, scope boundaries, key terms, provisional thesis, contribution, and evidence plan.

## When to use

Use this when the user has a broad intellectual project, book premise, thesis idea, manifesto, research theme, or interdisciplinary question and needs it made researchable.

## Automatic selection guidance

- High-signal triggers: start research on a subject, broad topic, research question, scope, contribution, audience, key terms, or evidence plan.
- Light-route behavior: clarify the question, boundaries, contribution, and evidence needs before source discovery.
- Deep-work gate: continue to `systematic-source-discovery` only after the question and scope are stable enough to guide a search.
- Noise and slowdown guard: do not browse or validate sources just because a topic is named.

## Do not use this skill when

- The user already has a stable question and asks to find sources; use `systematic-source-discovery`.
- The user asks for chapter structure; use `chapter-architecture`.
- The user asks for citation verification; use `citation-integrity-auditor`.

## Inputs expected

- Working topic or book premise
- Intended audience
- Discipline or fields involved
- Current thesis or intuition
- Preferred examples, source types, scope boundaries, or authors
- Constraints such as word count, timeline, or academic/public style

If inputs are missing, proceed with assumptions and label them.

## Source basis and AI limits

Follow `docs/SOURCE_LIMITS.md`: state the source access level, separate source basis from interpretation, include What I can verify, What remains uncertain, and User verification needed. Do not invent citations or source support.

## Machine-readable artifacts

When the user explicitly asks for JSON or a contract artifact, use `shared/contracts/book/book_artifact.schema.json` with `artifact_type: book_research_agenda`. If the output is normal Markdown, do not force the JSON contract.

## Files/folders it may read

- Bundled skill instructions, metadata, and assets if available (including, but not limited to, `SKILL.md`, `README.md`, `assets/`, `references/`, and `agents/openai.yaml` in this project or equivalent files in another project).
- Shared policy docs, especially `docs/SOURCE_LIMITS.md` and `docs/AUTO_SELECTION_GUARDRAILS.md`.
- User-provided book premises, notes, outlines, bibliographies, or project files explicitly named in the request.
- Repository quality docs when the user asks for contract-compatible or workflow-aligned artifacts.

## Files/folders it may write

- None by default.
- May create or update a user-requested research agenda artifact in the user-designated project or workspace.
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
# Research agenda

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

```

Use the optional Suggested next step policy in `docs/AUTO_SELECTION_GUARDRAILS.md`; it may be omitted unless one skill reduces a named scholarly risk.

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
- Premature citation audit before citations, quotes, page numbers, bibliography entries, or cited claims exist.
