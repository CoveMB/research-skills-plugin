# AGENTS.md

This repository is a Codex-compatible plugin package. When modifying it:

- Keep `.codex-plugin/plugin.json` valid JSON.
- Keep every skill folder name equal to its `SKILL.md` frontmatter `name`.
- Keep skill names lowercase kebab-case.
- Keep descriptions specific enough for implicit invocation.
- Run `python3 scripts/validate_plugin.py .` before packaging.
- Do not add fabricated citations, example sources, page numbers, or bibliographic claims to skill instructions.

## Contract coherence

Apply this coherence pass to every change that can alter plugin behavior, routing, artifact structure, shared research policy, package or installation behavior, or documented user expectations. This includes skills, agent metadata, shared policies, schemas, templates, examples, scripts, package metadata, documentation, tests, fixtures, evaluations, and standalone bundles.

1. Before editing, state the intended semantic change and identify its canonical owner.

2. Use the repository's existing ownership boundaries:
   - `.codex-plugin/plugin.json` owns plugin identity, version, description, and skill entry path.
   - `docs/policy/ROUTING_MATRIX.md` owns automatic skill-routing choices.
   - `MODE_REGISTRY.md` owns mode names, aliases, outputs, and oversight levels; it must not redefine routing rules.
   - Each file under `docs/policy/` owns the shared policy named by that file.
   - `shared/contracts/book/book_artifact.schema.json` owns machine-readable book-artifact structure, fields, enums, and constraints.
   - `docs/policy/PROCESS_PASSPORT.md` owns durable handoff and process-passport semantics.
   - Each `skills/<name>/SKILL.md` owns that skill's runtime procedure and skill-specific behavior.
   - Each `skills/<name>/agents/openai.yaml` represents that skill's discovery, invocation, and agent-policy metadata.
   - `shared/standalone-skill-registry.json` owns standalone classification and declared bundle dependencies.
   - Maintenance and packaging scripts own their executable behavior, subject to the policies and contracts they implement.

3. Inventory every direct consumer and representation affected by the change. Check, as applicable:
   - skill instructions, agent metadata, assets, and references
   - shared policies, routing tables, mode definitions, and schemas
   - root, skill, user, architecture, installation, and script documentation
   - templates and valid or invalid examples
   - validators, package helpers, and marketplace metadata
   - structural tests, behavioral fixtures, traces, manifests, expected outputs, mutation tests, and gold-set workflows
   - generated standalone bundles and packaged or installed runtime copies

4. Define every meaningful state, precedence rule, authority boundary, exception, and failure condition before changing prose or executable behavior. Pay particular attention to controlled vocabularies such as route modes and aliases, artifact types, source-access levels, corpus labels, compact-output statuses, passport and handoff states, lookup permissions, payload boundaries, gate dispositions, and standalone classifications.

5. Update the canonical owner and all affected consumers as one coherent change. Remove superseded requirements instead of layering new wording over them.

6. Keep shared normative definitions in their canonical owner. Consumers should link to that owner and contain only the skill-specific procedure, user-facing explanation, executable representation, or validation logic they own. Repeat a shared rule only when runtime usability requires it, and keep that repetition minimal and tested for alignment.

7. Preserve dependency order. Put prerequisites before dependent actions. Place an exception beside the rule it qualifies, or link directly to the canonical exception.

8. Treat the full plugin source as canonical. Do not edit files under `dist/standalone-skills` as a second source of truth. Rebuild every affected eligible bundle after changing a source skill, shared policy, contract, registry entry, or runtime helper.

9. After editing, search the repository for the old wording, new wording, synonyms, negations, universal terms, exception terms, controlled vocabulary, and affected file references. Compare the resulting requirements across runtime instructions, policies, schemas, documentation, scripts, examples, and evaluations.

10. Stop and ask when canonical sources conflict, ownership is unclear, a script enforces behavior that no policy or contract clearly owns, or the intended behavior cannot satisfy all applicable contracts.

11. Prefer behavioral tests that exercise allowed behavior, prohibited behavior, boundary conditions, and failure states. Use exact phrase assertions only for controlled vocabulary, stable interfaces, schema literals, or explicitly owned user-facing text. Do not weaken a test merely to accommodate semantic drift.

12. Exercise every meaningful state and exception when behavior uses a finite mode, status, disposition, authority, permission, artifact type, or lifecycle model.

13. Before completion:
    - run `./validate.sh` for a source checkout
    - run focused tests for every affected contract and consumer
    - rebuild and validate affected standalone bundles when their dependency closure changes
    - for packaging or installation changes, validate the package-safe runtime with `python3 scripts/run_package_checks.py --scope package`
    - when installed discovery or version behavior changes, verify the installed version and skill inventory in a fresh Codex task

## Test and evaluation economy

Optimize validation for confidence per token and minute. Token savings must never excuse a known deterministic failure. For a source checkout, `./validate.sh` is the canonical full validation command.

### Validation sequence

1. Before running tests, identify:
   - the smallest targeted deterministic check;
   - the canonical full validation command;
   - any expensive, nondeterministic, live-model, visual, network, or external evaluation.
2. During implementation, run only targeted tests relevant to the changed behavior.
3. Run the canonical full suite once after the coherent implementation batch is complete.
4. Rerun the canonical suite only when the tested tree changes materially, including after conflict resolution, rebase, or merge.
5. Do not rerun an unchanged command against an unchanged commit. Reuse the recorded result.

### Expensive and nondeterministic evaluations

- Do not use live-model or external evaluations as an open-ended implementation loop.
- Preselect the cases, controls, acceptance criteria, and maximum attempts before starting.
- Allow at most:
  - one baseline execution; and
  - one confirmation execution after a material repair.
- An additional execution requires either:
  - a new concrete hypothesis supported by evidence;
  - a material change affecting the evaluated behavior; or
  - explicit user direction.
- If a nondeterministic evaluation fails inconsistently, rerun it at most once. If results still conflict, classify the evidence as inconclusive and report it instead of repeatedly sampling.
- Do not expand the evaluation matrix during implementation unless a newly discovered material risk requires it.

### Stop conditions

Stop implementation and validation when all of the following are true:

- targeted deterministic checks pass;
- the canonical full suite passes on the current tree;
- required structural and security validation passes;
- no material review finding remains;
- remaining limitations are explicitly documented and accepted.

Accepted evidence limitations are closed decisions. Do not reopen them without new evidence or explicit user direction.

### Delegated work

- Subagents must not run the full suite or live evaluations unless explicitly assigned.
- Use at most one bounded final reviewer for a coherent task unless that reviewer identifies a material defect.
- Reviewers should report only merge-blocking or materially beneficial findings, not style preferences.
- Do not delegate repeated reviews of unchanged code.

### Output discipline

- Prefer quiet or summary test output.
- Report the command, commit or tree identity, exit status, and test totals.
- Preserve verbose logs only when diagnosing a failure.
- Do not paste or repeatedly inspect successful verbose output.
