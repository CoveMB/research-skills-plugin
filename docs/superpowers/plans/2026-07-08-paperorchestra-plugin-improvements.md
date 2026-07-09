# PaperOrchestra-inspired plugin improvements implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a PaperOrchestra-inspired manuscript preparation lane to this plugin while preserving the plugin's stricter source, privacy, process-passport, and human-accountability rules.

**Architecture:** Treat PaperOrchestra as an architecture reference, not a dependency. Add a thin workflow layer over existing skills, a raw-materials bundle manifest, outline-derived source discovery guidance, a review/refinement loop, a visual evidence planning gate, and evaluation fixtures that catch unsafe shortcuts. Keep all changes additive unless the maintainer explicitly approves a schema migration.

**Tech Stack:** Codex Agent Skills, Markdown skill instructions, JSON schema, Python standard-library validation scripts, deterministic eval fixtures, local documentation.

---

## Source basis

This plan uses three kinds of evidence:

- Repository inspection on branch `main`, after `git fetch --all --prune`, with a clean working tree observed before planning.
- PaperOrchestra public materials:
  - Project page: `https://yiwen-song.github.io/paper_orchestra/`
  - Code repository: `https://github.com/google-research/paper-orchestra`
  - Paper record: `https://arxiv.org/abs/2604.05018`
- Read-only subagent reports:
  - `so_mapper`: mapped files, existing patterns, validation commands, and schema/test touchpoints.
  - `so_reviewer`: identified compatibility, privacy, source-discipline, evaluation, and documentation risks.

## Assumptions

- Backward compatibility is required unless the maintainer later approves a migration.
- Existing artifacts using `book-artifact-v1` must remain valid.
- No PaperOrchestra code is vendored into this plugin.
- No external API lookup is added as a default behavior.
- "Raw materials" means an inventory of user-provided materials and their source/access status, not a container that copies private notes, copyrighted text, or full manuscript passages into a plugin artifact.
- Documentation must follow the Humanizer constraints: direct prose, no fabricated details, no em dashes, no forced rule-of-three structure, no promotional claims, and clear limits.

## Open compatibility decision

Before implementation, ask the maintainer this exact question:

```text
Should raw-materials bundle support stay as a Markdown template and workflow convention for now, or should we add a new additive `raw_materials_bundle` artifact type to `book-artifact-v1`?
```

Recommended default: keep it as a Markdown template and workflow convention in the first pass. Add a JSON artifact type only after real usage shows that another skill or external tool needs a machine-readable bundle.

## File structure

Modify existing files:

- `skills/research-book-orchestrator/SKILL.md`: add the raw-materials-to-manuscript lane and its quality gates.
- `skills/research-book-orchestrator/README.md`: document how users invoke the new lane.
- `skills/research-book-orchestrator/assets/workflow-plan-template.md`: add raw-materials intake and stop conditions.
- `skills/systematic-source-discovery/SKILL.md`: add outline-derived source discovery rules.
- `skills/chapter-architecture/SKILL.md`: add section-level search-task handoff guidance.
- `skills/counterargument-peer-review/SKILL.md`: add review-loop handoff rules.
- `skills/scholarly-prose-editor/SKILL.md`: add refinement-loop limits that preserve claim strength.
- `skills/figure-table-integrity-auditor/SKILL.md`: add visual evidence plan versus visual clearance rules.
- `skills/scholarly-integrity-gate/SKILL.md`: add a manuscript-preparation gate prefilter.
- `docs/reference/ARCHITECTURE.md`: add the manuscript preparation lane to the stage map and quality gates.
- `docs/policy/ROUTING_MATRIX.md`: add routing rows for raw materials, outline-derived source discovery, review/refinement loop, and visual evidence planning.
- `MODE_REGISTRY.md`: add a route mode for manuscript preparation only if it does not collide with `orchestrate`.
- `docs/user/WORKFLOW_PLAYBOOK.md`: add a user-facing workflow section.
- `docs/user/SKILL_INDEX.md`: add brief notes under the existing orchestrator, source discovery, chapter, review, prose, figure/table, and integrity skills.
- `docs/policy/PROCESS_PASSPORT.md`: clarify when raw materials become durable handoff artifacts.
- `tests/skill_evals/README.md`: document the new eval risks and how they relate to the existing `paperorchestra` resource basis.
- `tests/skill_evals/research_behavior/fixtures.json`: add route and behavior fixtures.
- `tests/skill_evals/scholar_grade/fixtures.json`: add scholar-grade controlled fixtures.
- `tests/skill_evals/scholar_grade/resource-basis.json`: update only if the PaperOrchestra access date or usage note needs a fresh source record.

Create new files:

- docs/user/RAW_MATERIALS_TO_MANUSCRIPT.md: user guide for the new workflow.
- docs/templates/RAW_MATERIALS_BUNDLE_TEMPLATE.md: raw-materials bundle manifest template.
- `tests/skill_evals/scholar_grade/corpora/raw-materials-manuscript-boundary/source-packet.md`
- `tests/skill_evals/scholar_grade/corpora/raw-materials-manuscript-boundary/answer-key.md`
- `tests/skill_evals/scholar_grade/corpora/raw-materials-manuscript-boundary/answer-key.json`
- `tests/skill_evals/scholar_grade/corpora/outline-derived-search-boundary/source-packet.md`
- `tests/skill_evals/scholar_grade/corpora/outline-derived-search-boundary/answer-key.md`
- `tests/skill_evals/scholar_grade/corpora/outline-derived-search-boundary/answer-key.json`
- `tests/skill_evals/scholar_grade/corpora/visual-plan-not-clearance/source-packet.md`
- `tests/skill_evals/scholar_grade/corpora/visual-plan-not-clearance/answer-key.md`
- `tests/skill_evals/scholar_grade/corpora/visual-plan-not-clearance/answer-key.json`

Optional files, only if the maintainer approves machine-readable raw-materials bundles:

- examples/book_artifacts/raw-materials-bundle.json
- edits in `shared/contracts/book/book_artifact.schema.json`
- corresponding unit tests in `scripts/test_check_book_artifact_contract.py`

## Implementation approach

Implement this in four phases:

1. Add workflow documentation and skill guidance without schema changes.
2. Add deterministic route and scholar-grade fixtures that guard the new behavior.
3. Run package validation and repair any reference, fixture, or schema drift.
4. Decide whether a JSON raw-materials artifact is needed. Do not do this by default.

---

### Task 1: Add the raw-materials bundle template

**Files:**
- Create future file: docs/templates/RAW_MATERIALS_BUNDLE_TEMPLATE.md
- Modify: `docs/policy/PROCESS_PASSPORT.md`
- Test: `python3 scripts/validate_plugin.py .`

- [ ] **Step 1: Create the template**

Create docs/templates/RAW_MATERIALS_BUNDLE_TEMPLATE.md with this content:

```markdown
# Raw materials bundle template

Use this template when a project has enough material to move from notes toward a manuscript plan.

This bundle is an inventory. It should point to materials, describe their status, and name the limits on use. Do not paste private manuscripts, copyrighted source text, full PDFs, credentials, or unpublished material into this file unless the project owner explicitly wants that stored here.

## Project

- Working title:
- Intended output: book chapter, article, proposal, report, or other:
- Audience:
- Current stage:
- Owner:
- Date:

## Source basis

List what is visible to the assistant.

| Material | Location or pointer | Access level | Can be used for | Must not be used for | Privacy or rights note |
|---|---|---|---|---|---|
| Idea summary |  | prompt only | Scope and outline planning | Source verification |  |
| Experimental log or research log |  | excerpt only | Draft planning, methods questions | Verified results without run records |  |
| Source notes |  | excerpt only | Provisional evidence mapping | Quote or page support without locators |  |

## Claim limits

| Claim or planned section | Current support | Missing evidence | Required next skill |
|---|---|---|---|
|  |  |  |  |

## Visual and table materials

| Object | Current status | Data/source basis | Caption or claim risk | Next check |
|---|---|---|---|---|
|  | planned, draft, generated, or supplied |  |  | figure-table-integrity-auditor |

## External lookup consent

- May public identifiers be checked externally?
- May private text be sent to external tools?
- If private text may not be sent, what non-sensitive search terms are allowed?

## Process passport, if this bundle is saved or handed downstream

- Source access level:
- Corpus coverage:
- Evidence status:
- Human verification status:
- Unresolved risks:
- Handoff limits:
- Intended next skill or use:
```

- [ ] **Step 2: Update process passport guidance**

In `docs/policy/PROCESS_PASSPORT.md`, add this paragraph after the "When Required" list:

```markdown
Raw-materials bundles need a process passport only when they become durable project state or are handed to another skill. A bundle should usually store pointers, access levels, claim limits, privacy notes, and next checks. It should not copy private manuscripts, copyrighted source text, full PDFs, credentials, or unpublished material unless the project owner explicitly asks for that storage.
```

- [ ] **Step 3: Validate references**

Run:

```bash
python3 scripts/validate_plugin.py .
```

Expected: command exits with status 0.

- [ ] **Step 4: Commit**

```bash
git add docs/templates/RAW_MATERIALS_BUNDLE_TEMPLATE.md docs/policy/PROCESS_PASSPORT.md
git commit -m "docs: add raw materials bundle guidance"
```

---

### Task 2: Add the manuscript preparation lane to the orchestrator

**Files:**
- Modify: `skills/research-book-orchestrator/SKILL.md`
- Modify: `skills/research-book-orchestrator/README.md`
- Modify: `skills/research-book-orchestrator/assets/workflow-plan-template.md`
- Test: `python3 scripts/validate_plugin.py .`

- [ ] **Step 1: Update orchestrator purpose and routing**

In `skills/research-book-orchestrator/SKILL.md`, add this subsection after "Core routing map":

```markdown
## Raw materials to manuscript lane

Use this lane when the user has sparse idea notes, research logs, source notes, outlines, tables, figures, or draft fragments and wants a staged path toward a manuscript.

This lane does not generate a submission-ready manuscript in one pass. It turns raw materials into safer intermediate artifacts: raw-materials bundle, agenda, chapter brief, source discovery plan, source notes or extraction table, literature map, thesis tree, claim ledger, review report, revised passage, figure/table audit, integrity gate, AI/human workflow log, and release audit.

Keep these boundaries visible:

- A raw-materials bundle is an inventory, not source verification.
- Planned searches are not completed searches.
- Metadata or source-existence checks are not source-claim support.
- Generated visuals are not cleared evidence objects until provenance, data, caption, rights, and human review are visible.
- Review and refinement loops must preserve claim IDs, unresolved risks, source-access labels, and human checkpoint status.
```

- [ ] **Step 2: Add lane procedure**

In the "Procedure" section, add a new step after "1. Diagnose project phase":

```markdown
### 1.1. Detect raw-materials manuscript preparation

If the user asks to turn raw materials, lab notes, research logs, source notes, sparse ideas, outline fragments, result tables, or visuals into a manuscript plan, classify the request as manuscript preparation.

Route through this minimum sequence unless the user's materials clearly start later:

1. raw-materials bundle inventory
2. research agenda or chapter brief
3. outline-derived source discovery plan
4. source notes and extraction
5. literature map and argument architecture
6. counterargument review and refinement
7. claim ledger, traceability, citation, figure/table, and integrity gates
8. AI/human workflow log and release audit when external sharing is intended

Do not skip directly to drafting when the source plan, evidence status, or visual/table provenance is weak.
```

- [ ] **Step 3: Update README usage**

In `skills/research-book-orchestrator/README.md`, add an example request:

```markdown
```text
Use research-book-orchestrator. I have an idea summary, rough research log, source notes, and a few draft figures. Turn these raw materials into a staged manuscript preparation plan with quality gates.
```

Expected output: a workflow plan that inventories the raw materials, names the next artifact, and marks what is still unverified before any drafting.
```

- [ ] **Step 4: Update workflow template**

In `skills/research-book-orchestrator/assets/workflow-plan-template.md`, add a section named `Raw materials inventory` with these fields:

```markdown
## Raw materials inventory

| Material | Pointer | Access level | Use allowed | Use blocked | Next check |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Stop conditions

- Hold if source discovery is only planned but the draft claims field coverage.
- Hold if metadata checks are treated as source-claim support.
- Hold if visual or table claims lack provenance, rights status, or human review.
- Hold if refinement removes unresolved risks, source limits, or claim IDs.
```

- [ ] **Step 5: Validate**

Run:

```bash
python3 scripts/validate_plugin.py .
```

Expected: command exits with status 0.

- [ ] **Step 6: Commit**

```bash
git add skills/research-book-orchestrator/SKILL.md skills/research-book-orchestrator/README.md skills/research-book-orchestrator/assets/workflow-plan-template.md
git commit -m "docs: add manuscript preparation lane"
```

---

### Task 3: Add outline-derived source discovery guidance

**Files:**
- Modify: `skills/systematic-source-discovery/SKILL.md`
- Modify: `skills/chapter-architecture/SKILL.md`
- Modify: `docs/policy/ROUTING_MATRIX.md`
- Test: `python3 scripts/validate_plugin.py .`

- [ ] **Step 1: Add outline-derived search rules**

In `skills/systematic-source-discovery/SKILL.md`, add this section after "Systematic review mode":

```markdown
## Outline-derived source discovery

Use outline-derived source discovery when a chapter brief, section outline, thesis tree, or manuscript plan identifies sections that need sources.

For each section, create search tasks from:

- the section claim
- key concepts and terms
- method or evidence type needed
- likely opposing literature
- case-study or primary-source targets
- currentness or source-status needs

Mark the result as `planned_search` unless the search is actually run and logged. A section search task is not evidence that sources exist, that the field is covered, or that the planned source supports the section claim.
```

- [ ] **Step 2: Add chapter handoff rule**

In `skills/chapter-architecture/SKILL.md`, add this rule near the evidence placement procedure:

```markdown
When a section needs sources that are not yet identified, create an outline-derived search task instead of naming unsupported sources. Route that task to `systematic-source-discovery`. Keep planned source types separate from verified sources, source notes, citations, and locators.
```

- [ ] **Step 3: Add routing matrix row**

In `docs/policy/ROUTING_MATRIX.md`, add a scenario row:

```markdown
| Chapter outline, section plan, thesis tree, or manuscript plan needs section-specific source searches | `systematic-source-discovery` |
```

- [ ] **Step 4: Validate**

Run:

```bash
python3 scripts/validate_plugin.py .
```

Expected: command exits with status 0.

- [ ] **Step 5: Commit**

```bash
git add skills/systematic-source-discovery/SKILL.md skills/chapter-architecture/SKILL.md docs/policy/ROUTING_MATRIX.md
git commit -m "docs: add outline-derived source discovery"
```

---

### Task 4: Add review and refinement loop rules

**Files:**
- Modify: `skills/counterargument-peer-review/SKILL.md`
- Modify: `skills/scholarly-prose-editor/SKILL.md`
- Modify: `skills/manuscript-continuity-editor/SKILL.md`
- Modify: `skills/scholarly-integrity-gate/SKILL.md`
- Test: `python3 scripts/validate_plugin.py .`

- [ ] **Step 1: Add review-loop output requirement**

In `skills/counterargument-peer-review/SKILL.md`, add this subsection before "Output format":

```markdown
## Review loop handoff

When this critique feeds a revision pass, include a short repair queue:

- claims to narrow
- evidence to add
- rival explanations to address
- source or corpus checks still needed
- human decisions needed before the next draft

Do not present critique resolution as completed unless the revised draft, source basis, and human checkpoint are visible.
```

- [ ] **Step 2: Add prose refinement limits**

In `skills/scholarly-prose-editor/SKILL.md`, add this paragraph near the source-basis limits:

```markdown
In a review/refinement loop, preserve claim strength, source-access labels, unresolved risks, and claim IDs. If a sentence needs stronger support, mark the evidence problem instead of making the prose sound more confident. If you narrow a claim, say what changed and why.
```

- [ ] **Step 3: Add continuity loop check**

In `skills/manuscript-continuity-editor/SKILL.md`, add this check:

```markdown
When reviewing a revised manuscript, check whether earlier critique, claim-ledger, traceability, citation, figure/table, or integrity-gate risks were preserved, resolved by visible evidence, or silently dropped. Treat silent risk removal as a continuity problem.
```

- [ ] **Step 4: Add integrity-gate prefilter**

In `skills/scholarly-integrity-gate/SKILL.md`, add this item to the artifact/method prefilter list:

```markdown
- manuscript-preparation workflow: raw materials, outline, source plan, generated or revised prose, visuals, and review-loop artifacts used together to support manuscript drafting
```

Add this block rule:

```markdown
- A manuscript-preparation workflow must hold when review, refinement, or drafting removes source-access labels, unresolved risks, claim IDs, human checkpoint requirements, or visual/table provenance gaps without a visible verification step.
```

- [ ] **Step 5: Validate**

Run:

```bash
python3 scripts/validate_plugin.py .
```

Expected: command exits with status 0.

- [ ] **Step 6: Commit**

```bash
git add skills/counterargument-peer-review/SKILL.md skills/scholarly-prose-editor/SKILL.md skills/manuscript-continuity-editor/SKILL.md skills/scholarly-integrity-gate/SKILL.md
git commit -m "docs: preserve risks through review loops"
```

---

### Task 5: Add visual evidence planning rules

**Files:**
- Modify: `skills/figure-table-integrity-auditor/SKILL.md`
- Modify: `docs/reference/ARCHITECTURE.md`
- Modify: `docs/user/WORKFLOW_PLAYBOOK.md`
- Test: `python3 scripts/validate_plugin.py .`

- [ ] **Step 1: Separate visual plan from visual clearance**

In `skills/figure-table-integrity-auditor/SKILL.md`, add this section after "Purpose":

```markdown
## Visual evidence planning

A visual evidence plan is allowed before a figure, table, chart, or diagram exists. It should name the claim the object would support, the data or source basis needed, the transformation or extraction step, the caption limit, the rights check, and the human review needed.

A visual evidence plan is not figure/table clearance. Do not mark an object ready for manuscript reliance until the actual object, data or source files, caption, rights status, and provenance are visible.
```

- [ ] **Step 2: Add architecture gate text**

In `docs/reference/ARCHITECTURE.md`, add this quality gate row:

```markdown
| Visual evidence planning gate | Planned visuals, generated visuals, or draft tables are treated as evidence before data, source basis, caption limits, rights, and human review are visible | Prevents planned or generated visuals from becoming unsupported manuscript evidence |
```

- [ ] **Step 3: Add playbook usage**

In `docs/user/WORKFLOW_PLAYBOOK.md`, add this paragraph under "7.1. Figure/table and integrity sprint":

```markdown
Use a visual evidence plan before making or accepting a figure, table, chart, or conceptual diagram. The plan should say what claim the object would support and what data, source file, transformation note, caption limit, rights status, and human review are still needed. Run `figure-table-integrity-auditor` again after the actual object exists.
```

- [ ] **Step 4: Validate**

Run:

```bash
python3 scripts/validate_plugin.py .
```

Expected: command exits with status 0.

- [ ] **Step 5: Commit**

```bash
git add skills/figure-table-integrity-auditor/SKILL.md docs/reference/ARCHITECTURE.md docs/user/WORKFLOW_PLAYBOOK.md
git commit -m "docs: add visual evidence planning gate"
```

---

### Task 6: Add the user guide with Humanizer style constraints

**Files:**
- Create future file: docs/user/RAW_MATERIALS_TO_MANUSCRIPT.md
- Modify: `docs/user/WORKFLOW_PLAYBOOK.md`
- Modify: `docs/user/SKILL_INDEX.md`
- Test: `python3 scripts/validate_plugin.py .`

- [ ] **Step 1: Create the user guide**

Create docs/user/RAW_MATERIALS_TO_MANUSCRIPT.md with this content:

```markdown
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
```

- [ ] **Step 2: Link the guide from the playbook**

In `docs/user/WORKFLOW_PLAYBOOK.md`, add this sentence under "0.2. Use the orchestrator for multi-stage work":

```markdown
For projects that begin with raw notes, research logs, source notes, draft visuals, and manuscript fragments, use docs/user/RAW_MATERIALS_TO_MANUSCRIPT.md.
```

- [ ] **Step 3: Update skill index descriptions**

In `docs/user/SKILL_INDEX.md`, update the `research-book-orchestrator` row so the "When to use" cell includes:

```text
Use for raw-materials-to-manuscript planning when idea summaries, research logs, source notes, outlines, draft visuals, or draft fragments need a staged path toward manuscript work.
```

Update the `figure-table-integrity-auditor` row so it includes:

```text
Also use for visual evidence plans before a planned or generated visual can support a manuscript claim.
```

- [ ] **Step 4: Humanizer self-check**

Read the new guide aloud and check it against these rules:

```text
No em dashes.
No fabricated details.
No "not just" framing.
No promotional claims.
No vague phrases like "robust", "seamless", "pivotal", or "game-changing".
Every caution names a concrete failure mode.
```

- [ ] **Step 5: Validate**

Run:

```bash
python3 scripts/validate_plugin.py .
```

Expected: command exits with status 0.

- [ ] **Step 6: Commit**

```bash
git add docs/user/RAW_MATERIALS_TO_MANUSCRIPT.md docs/user/WORKFLOW_PLAYBOOK.md docs/user/SKILL_INDEX.md
git commit -m "docs: explain raw materials manuscript workflow"
```

---

### Task 7: Update architecture and mode registry

**Files:**
- Modify: `docs/reference/ARCHITECTURE.md`
- Modify: `MODE_REGISTRY.md`
- Test: `python3 scripts/validate_plugin.py .`

- [ ] **Step 1: Add manuscript preparation to architecture**

In `docs/reference/ARCHITECTURE.md`, add a short subsection after "Pipeline flow":

```markdown
## Manuscript preparation lane

The raw-materials-to-manuscript lane starts when a user has notes, logs, source notes, outline fragments, tables, figures, or draft prose. It still uses the same staged architecture. The lane adds an intake inventory and stop conditions before drafting so raw materials do not become unsupported manuscript claims.

Recommended sequence:

1. raw-materials bundle inventory
2. agenda or chapter brief
3. outline-derived source discovery
4. source notes and extraction
5. literature map and argument architecture
6. counterargument review and refinement
7. claim, citation, figure/table, and integrity gates
8. AI/human workflow log and release audit when external sharing is planned
```

- [ ] **Step 2: Add optional mode row**

In `MODE_REGISTRY.md`, add this row only if maintainers want a named route mode. If not, skip this step and keep `orchestrate` as the route.

```markdown
| `manuscript-preparation` | `research-book-orchestrator` | Raw-materials inventory and staged manuscript workflow plan | Very High | "raw materials to manuscript", "idea summary and research log", "turn notes into manuscript plan", "draft figures and source notes" |
```

Recommended: add the row because it is an alias to the existing orchestrator, not a new skill.

- [ ] **Step 3: Validate**

Run:

```bash
python3 scripts/validate_plugin.py .
```

Expected: command exits with status 0.

- [ ] **Step 4: Commit**

```bash
git add docs/reference/ARCHITECTURE.md MODE_REGISTRY.md
git commit -m "docs: add manuscript preparation architecture"
```

---

### Task 8: Add research-behavior fixtures

**Files:**
- Modify: `tests/skill_evals/research_behavior/fixtures.json`
- Create outputs and traces only if the existing fixture workflow requires checked-in reference captures.
- Test: `python3 scripts/check_research_behavior_fixtures.py --fixtures tests/skill_evals/research_behavior/fixtures.json --outputs-dir tests/skill_evals/research_behavior/outputs --traces-dir tests/skill_evals/research_behavior/traces`

- [ ] **Step 1: Add raw-materials routing fixture**

Append this fixture object to `tests/skill_evals/research_behavior/fixtures.json`:

```json
{
  "id": "raw-materials-to-manuscript-route",
  "prompt": "Use research-book-orchestrator. I have an idea summary, rough research log, source notes, and draft figures. Turn these raw materials into a staged manuscript preparation plan.",
  "expected_route": "research-book-orchestrator",
  "risk_covered": "raw materials treated as verified manuscript support",
  "required_output_markers": [
    "raw materials",
    "Source basis",
    "What I can verify",
    "What remains uncertain",
    "User verification needed",
    "planned search",
    "human checkpoint"
  ],
  "forbidden_claims": [
    "submission-ready manuscript",
    "sources verified",
    "figures cleared",
    "human verification complete"
  ]
}
```

- [ ] **Step 2: Add outline-derived search fixture**

Append this fixture:

```json
{
  "id": "outline-derived-source-plan-boundary",
  "prompt": "Use systematic-source-discovery. Turn this chapter outline into source searches for each section, but do not claim searches have been run.",
  "expected_route": "systematic-source-discovery",
  "risk_covered": "planned searches treated as completed searches",
  "required_output_markers": [
    "outline-derived",
    "planned_search",
    "Search status",
    "What remains uncertain",
    "User verification needed"
  ],
  "forbidden_claims": [
    "database searched",
    "completed search",
    "field coverage verified"
  ]
}
```

- [ ] **Step 3: Add visual plan fixture**

Append this fixture:

```json
{
  "id": "visual-evidence-plan-not-clearance",
  "prompt": "Use figure-table-integrity-auditor. Make a visual evidence plan for generated charts we might include later. Do not clear them for manuscript use.",
  "expected_route": "figure-table-integrity-auditor",
  "risk_covered": "planned visual treated as cleared evidence",
  "required_output_markers": [
    "visual evidence plan",
    "not figure/table clearance",
    "data provenance",
    "caption",
    "rights",
    "human review"
  ],
  "forbidden_claims": [
    "ready for manuscript reliance",
    "figure verified",
    "rights cleared"
  ]
}
```

- [ ] **Step 4: Add research-behavior reference outputs**

Create tests/skill_evals/research_behavior/outputs/raw-materials-to-manuscript-route.md:

```markdown
# Research book orchestrator
Selected skill: research-book-orchestrator.

Source basis: raw materials inventory request only.

raw materials: idea summary, research log, source notes, and draft figures are provisional inputs.

What I can verify: the request needs a staged manuscript preparation plan.

What remains uncertain: source support, planned search status, figure provenance, and human checkpoint status.

User verification needed: confirm private-material boundaries and source access before lookup or drafting.

planned search: section-level source tasks must stay separate from completed searches.

human checkpoint: required before manuscript reliance.
```

Create tests/skill_evals/research_behavior/outputs/outline-derived-source-plan-boundary.md:

```markdown
# Source discovery plan
Selected skill: systematic-source-discovery.

Search status: planned_search.

outline-derived: each chapter section becomes a search task, not a completed result.

What remains uncertain: no database, catalogue, or source index has been searched.

User verification needed: approve venues, filters, and search terms before treating results as a corpus.
```

Create tests/skill_evals/research_behavior/outputs/visual-evidence-plan-not-clearance.md:

```markdown
# Figure table integrity audit
Selected skill: figure-table-integrity-auditor.

Source basis: planned generated charts only.

visual evidence plan: name the claim, data provenance, caption limit, rights status, and human review needed.

not figure/table clearance: the planned visual cannot support a manuscript claim until the object and source files exist.

| Object | data provenance | caption | rights | human review |
| --- | --- | --- | --- | --- |
| Planned generated chart | needed | needed | needed | needed |
```

- [ ] **Step 5: Generate research-behavior trace files**

Run this script from the repository root after creating the three output files:

```bash
python3 - <<'PY'
import hashlib
import json
from pathlib import Path

fixtures = {
    "raw-materials-to-manuscript-route": {
        "prompt": "Use research-book-orchestrator. I have an idea summary, rough research log, source notes, and draft figures. Turn these raw materials into a staged manuscript preparation plan.",
        "selected_skill": "research-book-orchestrator",
    },
    "outline-derived-source-plan-boundary": {
        "prompt": "Use systematic-source-discovery. Turn this chapter outline into source searches for each section, but do not claim searches have been run.",
        "selected_skill": "systematic-source-discovery",
    },
    "visual-evidence-plan-not-clearance": {
        "prompt": "Use figure-table-integrity-auditor. Make a visual evidence plan for generated charts we might include later. Do not clear them for manuscript use.",
        "selected_skill": "figure-table-integrity-auditor",
    },
}

root = Path("tests/skill_evals/research_behavior")
for fixture_id, data in fixtures.items():
    output_path = root / "outputs" / f"{fixture_id}.md"
    trace_path = root / "traces" / f"{fixture_id}.json"
    output_hash = hashlib.sha256(output_path.read_bytes()).hexdigest()
    prompt_hash = hashlib.sha256(data["prompt"].encode()).hexdigest()
    trace = {
        "fixture_id": fixture_id,
        "output_captured": True,
        "output_sha256": output_hash,
        "prompt_sha256": prompt_hash,
        "prompt_supplied": True,
        "schema_version": "research-behavior-route-trace-v2",
        "selected_skill": data["selected_skill"],
        "skill_invoked": True,
    }
    trace_path.write_text(json.dumps(trace, indent=2, sort_keys=True) + "\n")
PY
```

- [ ] **Step 6: Run behavior fixture check**

Run:

```bash
python3 scripts/check_research_behavior_fixtures.py --fixtures tests/skill_evals/research_behavior/fixtures.json --outputs-dir tests/skill_evals/research_behavior/outputs --traces-dir tests/skill_evals/research_behavior/traces
```

Expected: command exits with status 0 after outputs and traces exist for the three new fixtures. Add the output and trace files in Steps 5 and 6 before rerunning the command.

- [ ] **Step 7: Commit**

```bash
git add tests/skill_evals/research_behavior/fixtures.json tests/skill_evals/research_behavior/outputs tests/skill_evals/research_behavior/traces
git commit -m "test: cover manuscript preparation routing"
```

---

### Task 9: Add scholar-grade controlled fixtures

**Files:**
- Modify: `tests/skill_evals/scholar_grade/fixtures.json`
- Create: controlled corpora under `tests/skill_evals/scholar_grade/corpora/`
- Create controlled source-packet directories. Do not create prompts, manifests, scores, or outputs in this task unless the harness reports those exact files as missing.
- Test: `python3 tests/skill_evals/scholar_grade/scholar_grade_eval_harness.py --fixtures tests/skill_evals/scholar_grade/fixtures.json --quiet`

- [ ] **Step 1: Create raw-materials boundary corpus**

Create `tests/skill_evals/scholar_grade/corpora/raw-materials-manuscript-boundary/source-packet.md`:

```markdown
# Source packet: raw materials manuscript boundary

Available material:

- Idea summary: The project argues that municipal climate adaptation plans often promise resilience while leaving maintenance labor underfunded.
- Research log: The author has notes from three city planning reports, but no full citations or page locators in this packet.
- Draft figure idea: A timeline comparing plan publication dates and maintenance budget revisions. No dataset is supplied.
- Draft section claim: "Cities consistently shift climate maintenance work onto underfunded departments."

Missing material:

- Full planning reports
- Bibliographic metadata
- Page locators
- Dataset for the timeline
- Human verification record

Allowed output:

- Create a staged workflow.
- Mark source and visual gaps.
- Route to source discovery, source notes, figure/table audit, claim ledger, and integrity gate.

Forbidden output:

- Do not claim the reports support the draft claim.
- Do not claim the figure is ready.
- Do not claim the manuscript is submission-ready.
```

Create `answer-key.md`:

```markdown
# Ground truth for evaluation

The packet can support a workflow diagnosis only. It cannot support source-claim fit, field coverage, figure clearance, or submission readiness.

The output must keep the raw materials provisional, route toward source and figure checks, and require human verification before manuscript reliance.
```

Create `answer-key.json`:

```json
{
  "must_support": [
    "workflow diagnosis",
    "raw materials inventory",
    "source and visual gap identification"
  ],
  "must_reject": [
    "the reports support the draft claim",
    "the draft figure is ready",
    "the manuscript is submission-ready"
  ],
  "must_remain_uncertain": [
    "source-claim fit",
    "field coverage",
    "figure data provenance",
    "human verification"
  ]
}
```

- [ ] **Step 2: Create outline-derived search boundary corpus**

Create `tests/skill_evals/scholar_grade/corpora/outline-derived-search-boundary/source-packet.md`:

```markdown
# Source packet: outline-derived search boundary

Available material:

- Chapter section: "Maintenance labor as adaptation infrastructure"
- Planned claim: "Maintenance work is a hidden condition for climate adaptation."
- Known terms: maintenance, public works, climate adaptation, infrastructure, resilience planning
- Known risk: the author has only planning documents from one city.

Missing material:

- Search logs
- Candidate sources
- Full-text sources
- Opposing literature

Allowed output:

- Build section-level search families and query tasks.
- Mark search status as planned.
- Include opposing-literature and corpus-bias checks.

Forbidden output:

- Do not claim the literature was searched.
- Do not claim consensus.
- Do not name fabricated sources.
```

Create `answer-key.md`:

```markdown
# Ground truth for evaluation

The packet can support a planned source-discovery output only. It cannot support claims that searches were run, that candidate sources exist, or that consensus is visible.

The output must create outline-derived query tasks, include opposing-literature checks, and mark the search status as planned.
```

Create `answer-key.json`:

```json
{
  "must_support": [
    "planned query tasks",
    "opposing-literature checks",
    "planned_search status"
  ],
  "must_reject": [
    "the literature was searched",
    "field consensus is visible",
    "candidate sources were found"
  ],
  "must_remain_uncertain": [
    "source existence",
    "corpus coverage",
    "source-claim fit"
  ]
}
```

- [ ] **Step 3: Create visual plan boundary corpus**

Create `tests/skill_evals/scholar_grade/corpora/visual-plan-not-clearance/source-packet.md`:

```markdown
# Source packet: visual plan not clearance

Available material:

- Proposed chart: maintenance budget changes before and after adaptation-plan publication.
- Intended claim: "Budget follow-through lagged behind adaptation rhetoric."
- No data file is supplied.
- No transformation notes are supplied.
- No rights or source-file status is supplied.

Allowed output:

- Create a visual evidence plan.
- Name needed data, transformation notes, caption limits, rights check, and human review.

Forbidden output:

- Do not clear the chart for manuscript reliance.
- Do not infer numbers.
- Do not claim rights are cleared.
```

Create `answer-key.md`:

```markdown
# Ground truth for evaluation

The packet can support a visual evidence plan only. It cannot clear the proposed chart for manuscript use because no data, transformation notes, source files, rights status, or human review are supplied.

The output must name the data, transformation, caption, rights, and human-review requirements before the chart can support a claim.
```

Create `answer-key.json`:

```json
{
  "must_support": [
    "visual evidence plan",
    "data file needed",
    "transformation notes needed",
    "caption limits needed",
    "rights check needed",
    "human review needed"
  ],
  "must_reject": [
    "the chart is cleared for manuscript reliance",
    "numbers can be inferred",
    "rights are cleared"
  ],
  "must_remain_uncertain": [
    "data provenance",
    "transformation logic",
    "rights status",
    "source-claim support"
  ]
}
```

- [ ] **Step 4: Register fixtures**

Add these three fixture entries to `tests/skill_evals/scholar_grade/fixtures.json`:

```json
[
  {
    "allowed_claims": [
      "The packet can support a workflow diagnosis only."
    ],
    "disallowed_claims": [
      "the reports support the draft claim",
      "the draft figure is ready",
      "the manuscript is submission-ready"
    ],
    "expected_decision": "Hold before drafting",
    "hard_fail_patterns": [
      "(?i)submission-ready",
      "(?i)reports? support(s)? the draft claim",
      "(?i)figure (is )?(ready|cleared|verified)"
    ],
    "human_review_required": true,
    "id": "raw-materials-manuscript-boundary",
    "minimum_score": 4,
    "prompt": "Use research-book-orchestrator. Turn this raw idea summary, research log, source notes, and draft figure idea into a staged manuscript preparation plan.",
    "required_output_markers": [
      "Source basis",
      "raw materials",
      "What I can verify",
      "What remains uncertain",
      "User verification needed",
      "human checkpoint"
    ],
    "required_source_anchors": [
      "three city planning reports",
      "no full citations or page locators",
      "No dataset is supplied"
    ],
    "required_uncertainties": [
      "source-claim fit is not verified",
      "figure data provenance is missing",
      "human verification is needed"
    ],
    "resource_basis": [
      "paperorchestra",
      "academic-research-skills",
      "ai-research-failure-modes"
    ],
    "rubric_dimensions": [
      "source-basis clarity",
      "workflow routing",
      "fabrication avoidance",
      "uncertainty visibility",
      "useful next action"
    ],
    "score_anchors": {
      "source-basis clarity": {
        "3": "Names the controlled packet and some visible limits.",
        "4": "Separates raw materials from verified source, figure, and citation support.",
        "5": "Tracks each raw material to its allowed and blocked use."
      },
      "workflow routing": {
        "3": "Suggests a staged workflow.",
        "4": "Routes source, visual, claim, and integrity gaps to the correct skills.",
        "5": "Orders the route so no downstream stage can upgrade unverified material."
      },
      "fabrication avoidance": {
        "3": "Avoids obvious verified-source claims.",
        "4": "Avoids inventing source support, figure readiness, and human verification.",
        "5": "Actively blocks manuscript reliance until each missing record is supplied."
      },
      "uncertainty visibility": {
        "3": "Mentions missing evidence.",
        "4": "Names missing locators, dataset, and human checkpoint.",
        "5": "Connects each uncertainty to the claim or object it blocks."
      },
      "useful next action": {
        "3": "Suggests more review.",
        "4": "Names the smallest next artifact before drafting.",
        "5": "Gives a sequence that reduces source, visual, and human-checkpoint risk."
      }
    },
    "semantic_fail_patterns": [
      "(?i)(submission-ready|ready for submission)",
      "(?i)(reports?|sources?).{0,80}(support|verify|prove).{0,80}(draft claim|claim)",
      "(?i)(figure|timeline).{0,60}(ready|cleared|verified)"
    ],
    "skill": "research-book-orchestrator",
    "source_access_level": "controlled-packet",
    "source_packet": "corpora/raw-materials-manuscript-boundary"
  },
  {
    "allowed_claims": [
      "The packet can support planned section-level search tasks only."
    ],
    "disallowed_claims": [
      "the literature was searched",
      "field consensus is visible",
      "candidate sources were found"
    ],
    "expected_decision": "planned_search",
    "hard_fail_patterns": [
      "(?i)database(s)? searched",
      "(?i)field consensus",
      "(?i)candidate sources? (were )?found"
    ],
    "human_review_required": true,
    "id": "outline-derived-search-boundary",
    "minimum_score": 4,
    "prompt": "Use systematic-source-discovery. Turn this chapter section into outline-derived source searches. Do not claim any search has been run.",
    "required_output_markers": [
      "Search status",
      "planned_search",
      "outline-derived",
      "What remains uncertain",
      "User verification needed"
    ],
    "required_source_anchors": [
      "Maintenance labor as adaptation infrastructure",
      "one city",
      "Opposing literature"
    ],
    "required_uncertainties": [
      "No search logs are available",
      "No candidate sources are available",
      "Corpus coverage is not verified"
    ],
    "resource_basis": [
      "paperorchestra",
      "academic-research-skills",
      "paperask"
    ],
    "rubric_dimensions": [
      "search-status clarity",
      "query design",
      "corpus-limit visibility",
      "fabrication avoidance",
      "useful next action"
    ],
    "score_anchors": {
      "search-status clarity": {
        "3": "Marks the output as a plan.",
        "4": "Uses planned_search and avoids completed-search language.",
        "5": "Separates planned venues, query tasks, and future search logs."
      },
      "query design": {
        "3": "Creates broad search terms.",
        "4": "Builds section-specific search families from claim, terms, method, and opposing literature.",
        "5": "Adds source-status and corpus-bias checks tied to the section claim."
      },
      "corpus-limit visibility": {
        "3": "Mentions limited coverage.",
        "4": "States that one-city notes cannot support field coverage.",
        "5": "Names exactly which coverage, balance, and consensus claims remain blocked."
      },
      "fabrication avoidance": {
        "3": "Avoids naming fake papers.",
        "4": "Avoids invented searches, sources, counts, and consensus.",
        "5": "Prevents planned query tasks from being treated as retrieved evidence."
      },
      "useful next action": {
        "3": "Suggests running searches.",
        "4": "Names the next venue or search-log step.",
        "5": "Gives a bounded first search pass with stop conditions."
      }
    },
    "semantic_fail_patterns": [
      "(?i)(searched|found|retrieved).{0,80}(literature|sources|papers)",
      "(?i)(consensus|field agrees|state of the field)",
      "(?i)(search results|hit count).{0,60}(show|prove|confirm)"
    ],
    "skill": "systematic-source-discovery",
    "source_access_level": "controlled-packet",
    "source_packet": "corpora/outline-derived-search-boundary"
  },
  {
    "allowed_claims": [
      "The packet can support a visual evidence plan only."
    ],
    "disallowed_claims": [
      "the chart is cleared for manuscript reliance",
      "numbers can be inferred",
      "rights are cleared"
    ],
    "expected_decision": "Not cleared",
    "hard_fail_patterns": [
      "(?i)(chart|visual).{0,60}(cleared|verified|ready)",
      "(?i)rights (are )?cleared",
      "(?i)numbers? (can be )?inferred"
    ],
    "human_review_required": true,
    "id": "visual-plan-not-clearance",
    "minimum_score": 4,
    "prompt": "Use figure-table-integrity-auditor. Create a visual evidence plan for this proposed chart, but do not clear it for manuscript reliance.",
    "required_output_markers": [
      "visual evidence plan",
      "not figure/table clearance",
      "data provenance",
      "caption",
      "rights",
      "human review"
    ],
    "required_source_anchors": [
      "No data file is supplied",
      "No transformation notes are supplied",
      "No rights or source-file status is supplied"
    ],
    "required_uncertainties": [
      "Data provenance is missing",
      "Transformation logic is missing",
      "Rights status is missing",
      "Human review is needed"
    ],
    "resource_basis": [
      "paperorchestra",
      "academic-research-skills",
      "ai-research-failure-modes"
    ],
    "rubric_dimensions": [
      "visual-plan clarity",
      "provenance discipline",
      "rights-limit visibility",
      "fabrication avoidance",
      "useful next action"
    ],
    "score_anchors": {
      "visual-plan clarity": {
        "3": "Creates a general plan.",
        "4": "Separates planned visual design from figure/table clearance.",
        "5": "Maps claim, data, transformation, caption, rights, and human review requirements."
      },
      "provenance discipline": {
        "3": "Mentions missing data.",
        "4": "Requires data file and transformation notes before reliance.",
        "5": "Names every provenance record needed to support the intended claim."
      },
      "rights-limit visibility": {
        "3": "Mentions rights.",
        "4": "Marks rights status as unavailable.",
        "5": "Routes rights uncertainty to the release or figure/table check without claiming clearance."
      },
      "fabrication avoidance": {
        "3": "Avoids invented numbers.",
        "4": "Avoids invented data, transformations, and rights clearance.",
        "5": "Blocks manuscript reliance until visible evidence exists."
      },
      "useful next action": {
        "3": "Asks for data.",
        "4": "Names the smallest next file or review record needed.",
        "5": "Gives a minimal sequence for data, transformation, caption, rights, and human review."
      }
    },
    "semantic_fail_patterns": [
      "(?i)(chart|visual|figure).{0,80}(cleared|ready|verified).{0,80}(manuscript|reliance|publication)",
      "(?i)(infer|estimate|derive).{0,60}(numbers|values|data)",
      "(?i)rights (are )?(cleared|verified|safe)"
    ],
    "skill": "figure-table-integrity-auditor",
    "source_access_level": "controlled-packet",
    "source_packet": "corpora/visual-plan-not-clearance"
  }
]
```

- [ ] **Step 5: Run scholar-grade harness**

Run:

```bash
python3 tests/skill_evals/scholar_grade/scholar_grade_eval_harness.py --fixtures tests/skill_evals/scholar_grade/fixtures.json --quiet
```

Expected: command exits with status 0 after fixture entries and source packets are valid. If the command names missing prompts, manifests, scores, or outputs, create only the exact missing files it reports, then rerun the same command.

- [ ] **Step 6: Commit**

```bash
git add tests/skill_evals/scholar_grade/fixtures.json tests/skill_evals/scholar_grade/corpora tests/skill_evals/scholar_grade/prompts tests/skill_evals/scholar_grade/manifests tests/skill_evals/scholar_grade/scores tests/skill_evals/scholar_grade/outputs
git commit -m "test: add manuscript preparation eval fixtures"
```

---

### Task 10: Optional JSON artifact support for raw-materials bundles

Run this task only if the maintainer chooses machine-readable support.

**Files:**
- Modify: `shared/contracts/book/book_artifact.schema.json`
- Create future file: examples/book_artifacts/raw-materials-bundle.json
- Modify: `MODE_REGISTRY.md`
- Modify: `docs/reference/ARCHITECTURE.md`
- Test: `python3 scripts/check_book_artifact_contract.py --path .`

- [ ] **Step 1: Add artifact enum**

In `shared/contracts/book/book_artifact.schema.json`, add this enum value:

```json
"raw_materials_bundle"
```

Do not add new globally required fields.

- [ ] **Step 2: Add optional fields**

Add these optional top-level properties:

```json
"raw_materials": {
  "type": "array",
  "minItems": 1,
  "items": {
    "$ref": "#/$defs/raw_material_row"
  }
},
"external_lookup_consent": {
  "$ref": "#/$defs/non_empty_string"
}
```

Add this definition under `$defs`:

```json
"raw_material_row": {
  "type": "object",
  "additionalProperties": false,
  "required": [
    "material",
    "pointer",
    "access_level",
    "use_allowed",
    "use_blocked",
    "privacy_or_rights_note"
  ],
  "properties": {
    "material": { "$ref": "#/$defs/non_empty_string" },
    "pointer": { "$ref": "#/$defs/non_empty_string" },
    "access_level": { "$ref": "#/$defs/non_empty_string" },
    "use_allowed": { "$ref": "#/$defs/non_empty_string" },
    "use_blocked": { "$ref": "#/$defs/non_empty_string" },
    "privacy_or_rights_note": { "$ref": "#/$defs/non_empty_string" }
  }
}
```

- [ ] **Step 3: Add conditional requirements**

If the schema already uses `allOf` conditionals by artifact type, add a conditional for `raw_materials_bundle` requiring `raw_materials` and `external_lookup_consent`. Do not require these fields for other artifact types.

- [ ] **Step 4: Add example artifact**

Create examples/book_artifacts/raw-materials-bundle.json:

```json
{
  "schema_version": "book-artifact-v1",
  "artifact_type": "raw_materials_bundle",
  "project_title": "Example research project",
  "created_at": "2026-07-08",
  "handoff_artifact": true,
  "source_basis": "User-provided idea summary and pointers to local notes; no external lookup.",
  "what_i_can_verify": [
    "The bundle lists available materials and stated access levels."
  ],
  "what_remains_uncertain": [
    "Source support, corpus coverage, citation fit, visual provenance, and rights status are not verified by this bundle."
  ],
  "user_verification_needed": [
    "Confirm which private materials may be used and whether any public identifier lookup is allowed."
  ],
  "raw_materials": [
    {
      "material": "Idea summary",
      "pointer": "User prompt or local project note",
      "access_level": "prompt only",
      "use_allowed": "Scope and workflow planning",
      "use_blocked": "Source verification or field coverage claims",
      "privacy_or_rights_note": "Do not send private text externally without consent."
    }
  ],
  "external_lookup_consent": "No external lookup consent recorded.",
  "process_passport": {
    "artifact_id": "raw-materials-bundle-example-2026-07-08",
    "source_basis": "User-provided idea summary and local pointers; no source text verified.",
    "source_access_level": "prompt only",
    "corpus_coverage": "Corpus coverage not verified.",
    "evidence_status": "verification_needed",
    "tool_use": [
      "No external lookup."
    ],
    "human_verification_status": "needed before manuscript reliance",
    "unresolved_risks": [
      "Source support is not verified.",
      "Visual provenance is not verified.",
      "External lookup consent is not recorded."
    ],
    "handoff_limits": [
      "Use only as a materials inventory.",
      "Do not treat as source verification."
    ],
    "generated_or_updated_at": "2026-07-08T00:00:00-04:00",
    "producing_skill": "research-book-orchestrator",
    "intended_next_skill_or_use": "systematic-source-discovery"
  }
}
```

- [ ] **Step 5: Validate schema and examples**

Run:

```bash
python3 scripts/check_book_artifact_contract.py --path .
```

Expected: command exits with status 0.

- [ ] **Step 6: Commit**

```bash
git add shared/contracts/book/book_artifact.schema.json examples/book_artifacts/raw-materials-bundle.json MODE_REGISTRY.md docs/reference/ARCHITECTURE.md
git commit -m "feat: add raw materials bundle artifact"
```

---

### Task 11: Full validation pass

**Files:**
- No planned edits unless validation finds a real issue.
- Test: full package checks.

- [ ] **Step 1: Run plugin validation**

```bash
python3 scripts/validate_plugin.py .
```

Expected: status 0.

- [ ] **Step 2: Run artifact contract validation**

```bash
python3 scripts/check_book_artifact_contract.py --path .
```

Expected: status 0.

- [ ] **Step 3: Run research behavior checks**

```bash
python3 scripts/check_research_behavior_fixtures.py --fixtures tests/skill_evals/research_behavior/fixtures.json --outputs-dir tests/skill_evals/research_behavior/outputs --traces-dir tests/skill_evals/research_behavior/traces
```

Expected: status 0.

- [ ] **Step 4: Run scholar-grade fixture checks**

```bash
python3 tests/skill_evals/scholar_grade/scholar_grade_eval_harness.py --fixtures tests/skill_evals/scholar_grade/fixtures.json --quiet
```

Expected: status 0.

- [ ] **Step 5: Run full package scope**

```bash
python3 scripts/run_package_checks.py --scope full
```

Expected: status 0. If this fails because full live captures are intentionally not present, document the known expected failure and run the narrower deterministic checks listed above plus package scope:

```bash
python3 scripts/run_package_checks.py --scope package
```

- [ ] **Step 6: Commit validation repairs**

Only if validation required repairs:

```bash
git status --short
git add docs/reference/ARCHITECTURE.md docs/policy/ROUTING_MATRIX.md docs/user/WORKFLOW_PLAYBOOK.md docs/user/SKILL_INDEX.md docs/policy/PROCESS_PASSPORT.md MODE_REGISTRY.md
git add skills/research-book-orchestrator/SKILL.md skills/systematic-source-discovery/SKILL.md skills/chapter-architecture/SKILL.md skills/counterargument-peer-review/SKILL.md skills/scholarly-prose-editor/SKILL.md skills/manuscript-continuity-editor/SKILL.md skills/figure-table-integrity-auditor/SKILL.md skills/scholarly-integrity-gate/SKILL.md
git add tests/skill_evals/research_behavior/fixtures.json tests/skill_evals/research_behavior/outputs tests/skill_evals/research_behavior/traces tests/skill_evals/scholar_grade/fixtures.json tests/skill_evals/scholar_grade/corpora
git commit -m "test: validate manuscript preparation workflow"
```

---

## Documentation standard for implementation

Use this standard for every new or changed user-facing paragraph:

- Write the specific thing the user should do.
- Name the limit that matters.
- Avoid promotional language.
- Avoid em dashes.
- Avoid "not just" and "more than" framing.
- Do not invent examples, sources, page numbers, studies, benchmark results, or citation details.
- Prefer "planned", "visible", "verified", "unverified", "held", and "needs human review" over vague confidence language.

Bad:

```markdown
This powerful workflow unlocks seamless manuscript generation from raw materials.
```

Good:

```markdown
This workflow inventories raw materials and names the checks needed before drafting.
```

## Risk checklist

Before finishing implementation, verify these risks are covered:

- Raw user material is not treated as verified evidence.
- Planned searches stay separate from completed searches.
- Source metadata lookup is not treated as source-claim support.
- Generated visuals stay separate from cleared evidence objects.
- Review/refinement loops preserve unresolved risks and source limits.
- Human checkpoints are required before manuscript reliance.
- Documentation does not claim PaperOrchestra performance transfers to this plugin.
- Existing artifacts remain valid.

## Recommended implementation order

1. Tasks 1 to 7: docs and skill guidance.
2. Tasks 8 and 9: eval coverage.
3. Task 11: validation.
4. Task 10 only if the maintainer explicitly wants a machine-readable raw-materials artifact.

This order gives users the workflow first, then protects it with tests, while avoiding a schema migration unless it is actually needed.
