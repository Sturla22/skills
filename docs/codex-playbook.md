# Codex Playbook

This repo includes Codex-native project files in addition to the Claude Code and GitHub Copilot files.

## What is included

- `AGENTS.md` at repo root for durable project guidance
- `.agents/skills/` for shared repo skills that Codex can discover automatically
- `.agents/agents/*.toml` as the canonical role specs
- `.codex/config.toml` for project-scoped Codex settings
- `.codex/agents/*.toml` as generated Codex subagents

## Why the repo has both `.agents` and `.codex/agents`

- `.agents/skills` is the Codex repo skill location.
- `.agents/agents/*.toml` is the canonical shared role layer.
- `.codex/agents/*.toml` is generated so Codex subagent config stays tool-native.
- `.claude/` and `.github/agents/` are generated from the same canonical role definitions.

## Suggested first setup

1. Install Codex CLI: `npm i -g @openai/codex`
2. Run `codex` in the repo root and sign in.
3. Ask Codex: `Summarize the current instructions and available skills.`
4. Open `.codex/config.toml` and tune approvals, sandboxing, and any model defaults.
5. Decide whether your team will run mostly in the CLI, the IDE extension, or the Codex app.

Recommended Codex baseline for this repo:

- trusted local startup defaults: `sandbox_mode = "danger-full-access"` and `approval_policy = "never"`
- keep enough agent headroom for real delegation: `max_threads = 6`, `max_depth = 2`
- prefer prompt guidance that names the next owner or safe parallel owner set explicitly
- bias toward subagents for bounded specialist work, not for vague exploratory delegation

## Regenerating role files

Whenever you edit `.agents/agents/*.toml`, run:

```bash
python3 scripts/cli.py sync
```

To enforce this in CI:

```bash
python3 scripts/cli.py sync --check
```

## Quick checks

### Instruction loading
Run from the repo root:

```bash
codex --ask-for-approval never "Summarize the current instructions."
```

### Skill discovery
From the repo root, ask Codex to list skills or invoke one explicitly using the skill name.
Examples:

```text
Use codebase-exploration to map the files involved in the boot sequence.
Use hypothesis-driven-debugging to investigate this flaky integration test.
Use simplify-without-behavior-change on this storage adapter.
Use operation-cost-optimization to reduce flash wear in this persistence path by counting erases, writes, and reads.
Use bounded-autonomy-loop to drive this narrow implementation slice with explicit done-when criteria, checks each round, and a max-iteration budget.
```

### Subagent usage
Custom agents live in `.codex/agents/` and mirror the repo role model.
Examples:

- product-owner: shared understanding, success criteria, and delegation
- planner: framing, scope, acceptance criteria, and safe parallelism
- developer: minimal implementation
- verifier: proof and focused checks
- reviewer: adversarial critique
- firmware-architect: contracts and boundaries
- technical-writer: reader-facing docs, release notes, migration guidance, and doc-structure cleanup
- release-manager: version bump, release readiness, and final release communication
- integration-engineer: bench, HIL, and integration-environment execution
- workflow-architect: evolve prompts, templates, skills, and roles from recurring evidence

Codex is more likely to use subagents well when the prompt names:

- the current owner
- the next owner or owner set
- whether the split is serial or parallel
- the expected output from each delegated lane
- the merge point or synthesis owner

## Embedded-firmware defaults worth keeping

- Keep `AGENTS.md` short and durable.
- Put repeatable workflows into skills, not giant prompts.
- Use dedicated skills for release gating and bench reproducibility instead of burying those workflows in role prose.
- Capture stakeholder needs, trade studies, and validation intent explicitly when the work is system-heavy.
- For process changes, prefer a bounded workflow experiment with one small mutable surface and a keep / revise / revert decision.
- Prefer BDD scenarios, the test pyramid, and simulation-first host checks as the default testing shape.
- Treat bounded autonomous loops as an optional execution mode for narrow, auto-checkable slices, not as a replacement for planning or verification.
- Prefer explicit cost models over intuition when optimizing performance, endurance, or footprint: count indirect costs, measure direct RAM/flash costs, and weight tradeoffs when useful.
- Bias toward simulation and host verification before hardware-only work when practical.
- Keep one work packet per non-trivial task under `docs/work/<work-id>/`, with handoffs under `handoffs/` and evidence under `evidence/`.
- Treat resource use and failure behavior as part of correctness.
- Keep migration decisions and interface constraints documented.

## Good Codex prompts for this repo

See [templates/reusable-prompts.md](/home/sturlalange/Dev/my-claude-skills/templates/reusable-prompts.md) for a reusable prompt library that matches this repo's role model.

Short examples:

- "Use product-owner to turn this request into a shared brief, then delegate to the right next owner."
- "Use planner to scope this change from the agreed brief, list affected modules, identify safe parallel lanes, and define verification steps before any edits."
- "Use product-owner to keep the user-facing thread, then delegate the concrete implementation and verification slices to subagents instead of carrying them locally."
- "Use planner to decide whether parallel subagents would shorten the critical path here; if yes, name the owners, write surfaces, and merge point explicitly."
- "Use developer to make the smallest defensible change for this bug, then hand off to verifier."
- "Have reviewer critique this patch for correctness, complexity, and missing evidence."
- "Use firmware-architect and planner to propose an incremental migration path with characterization checkpoints."
- "Use technical-writer to turn this work packet into release notes and migration guidance for downstream users, and choose the right doc form for each update."
- "Use release-manager to turn this work packet and changelog into a release recommendation."
- "Use integration-engineer to make this HIL lane reproducible and capture durable bench evidence."
- "Use planner to decide whether this slice is a good fit for bounded-autonomy-loop, then use developer to run it with explicit done-when criteria, checks, budget, and stop states."
- "Use bounded-autonomy-loop on this contained implementation task, keep TDD inside the loop, and write the loop record under docs/work/<work-id>/evidence/bounded-autonomy-loop.md."
- "Use release-readiness to classify the version impact, decide the honest release shape, and summarize go / no-go gates."
- "Use lab-and-hil-reproducibility to capture exact rig identity, repeatable flashing steps, and product-versus-environment failure classification."
- "Use workflow-architect to review recent work packets, identify repeated friction, and choose the smallest process change: prompt, template, skill, or role."
- "Use workflow-architect to propose a bounded workflow experiment, land the smallest change, and decide keep, revise, or revert after the next few work packets."
- "Use requirements-and-traceability to link the stakeholder needs, derived requirements, design touchpoints, verification, and validation for this work packet."
- "Use trade-study-and-decision-analysis to compare the viable concepts before we commit to one architecture path."
- "Use validation-planning to define how we will show this change solved the real stakeholder problem, not just passed tests."
