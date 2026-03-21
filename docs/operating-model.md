# Operating Model

## Principle

Keep one human-facing control thread. `product-owner` owns requester alignment, context, and synthesis; specialist agents are internal workers, not separate personalities.
Keep one durable work packet per task so context is read from one place instead of recopied by every role.
Treat integration and V&V as continuous signals inside each iteration, not as a final gate that appears only at the end.

## Suggested loop

1. `product-owner` turns the request into a shared brief with scope, non-goals, constraints, and acceptance criteria.
2. `planner` scopes the task, writes the canonical plan, names the evidence required, and identifies safe parallel lanes plus worktree or isolation plans when the work can be split cleanly.
3. `developer` makes the smallest change that could work, optionally using a bounded autonomy loop when the current slice is narrow and auto-checkable.
4. `verifier` checks the claim independently.
5. `reviewer` attacks the plan and patch.
6. `firmware-architect` is brought in for HAL, contracts, migration, or structure-heavy work.
7. `technical-writer` is brought in for release notes, migration/deprecation guidance, doc-structure cleanup, or substantial reader-facing docs.
8. `release-manager` is brought in for version bump, release shape, release readiness, and final release communication.
9. `integration-engineer` is brought in for reproducible integration, bench, HIL, environment work, or flaky-lab triage.
10. `workflow-architect` is brought in for process evolution, role or skill changes, or recurring workflow friction.

## Delegation rules

- Do not delegate raw user text when the desired outcome is still ambiguous.
- Parallel specialists are allowed only when the planner has defined ownership boundaries, blockers, integration checkpoints, and the write-lane isolation plan.
- If a specialist finds requirement drift or unclear acceptance criteria, hand the work back to `product-owner`.
- Use bounded autonomy only when `planner` has defined the slice, checks, budget, and stop states explicitly.
- By default, specialists return structured results to `product-owner` rather than talking directly to the requester.
- Store durable task context under `docs/work/<work-id>/`.
- Store role-to-role handoffs under `docs/work/<work-id>/handoffs/`.
- Store bounded process-improvement experiments under `docs/workflow-experiments/`.
- Keep handoffs delta-focused: point to canonical packet files and describe only what changed.
- Prefer isolated worktrees for planner-approved parallel write lanes when the tool supports them.

## Escalation rules

Bring in **planner** early when:
- scope is unclear
- the user request contains multiple plausible implementations
- acceptance criteria are not yet concrete
- stakeholder needs, system context, or external interfaces are still fuzzy
- the next step feels too large to verify
- a trade study or validation plan may be needed before implementation
- there may be independent work that could run in parallel
- the safe parallel split would be clearer if each write lane had its own worktree or other explicit isolation
- a narrow execution slice may benefit from bounded autonomy with explicit checks and stop conditions

Bring in **firmware-architect** when:
- a hardware seam is missing
- platform code is leaking upward
- a migration path is unclear
- interface stability matters more than immediate speed
- multiple interface or architecture options need an explicit trade study
- the change affects timing, concurrency, or long-term architecture

Bring in **verifier** early when:
- the bug is not reproducible
- the test seam is unclear
- hardware availability is limited
- requirement coverage is unclear
- validation is being implied by verification evidence
- the change is risky or safety-sensitive

Bring in **reviewer** early when:
- the plan feels large
- multiple abstractions are being introduced
- the change crosses platform boundaries
- there is a temptation to "rewrite it cleanly"

Bring in **technical-writer** when:
- release notes or changelog entries need curation
- migration or deprecation guidance is needed
- setup, usage, or operator docs are substantial enough to deserve their own lane
- the implementation is understood but the reader-facing explanation is still weak
- the right doc form is unclear: tutorial, how-to, reference, or explanation
- the docs have drifted into duplication, weak information architecture, or unclear recommended paths

Bring in **release-manager** when:
- SemVer impact or release readiness is disputed or unclear
- changelog, release notes, and evidence need a single final owner
- a release cut has enough coordination cost to deserve its own lane
- the honest choice between pre-release, canary, and full release is still unclear
- artifact identity, release inputs, or explicit release gates need one accountable owner

Bring in **integration-engineer** when:
- HIL or bench setup is the critical bottleneck
- flashing, wiring, environment setup, or log capture are slowing verification
- the environment is flaky and someone needs to make the setup reproducible
- integration evidence is needed before verifier can make a strong call
- hardware identity, fixture mapping, or shared-rig ownership is still ad hoc
- repeated reruns are not distinguishing product failures from environment failures

Bring in **workflow-architect** when:
- the same workflow friction appears across multiple tasks or work packets
- role boundaries are repeatedly unclear in practice
- a prompt, template, skill, or role may need to be created or refined
- the team wants onboarding or process improvements grounded in evidence instead of anecdotes
- the process change should be run as a bounded experiment before being treated as settled

## Anti-patterns

- writing code that cannot be justified by any driver: user scenario, risk, epistemic uncertainty, design intent communication, or external obligation
- delegating before restating the real problem
- copying the same scope, assumptions, and risks into every artifact instead of using one canonical work packet
- letting every specialist improvise its own handoff format
- keeping handoffs only in chat instead of in-repo Markdown files
- letting the implementer declare victory
- doing hardware-only debugging when a deterministic host repro is possible
- treating integration as a late phase instead of continuous work
- introducing an abstraction before naming its real pressure
- widening scope because "we are already in the file"
- letting a specialist invent missing product requirements
- parallelizing overlapping work without explicit ownership
- parallelizing write-heavy lanes without naming the isolation plan
- treating resource issues as post-processing
- creating a new role for a one-off problem that a prompt, template, or skill would solve
- changing multiple workflow surfaces at once with no way to tell what actually helped
- turning a bounded autonomy loop into an unbounded retry habit on ambiguous work

## Cross-tool note

The same role model is shared across Claude Code, GitHub Copilot, and OpenAI Codex.

- Edit canonical role definitions under `.agents/agents/*.toml`
- Edit canonical shared skills under `.agents/skills/`
- Regenerate downstream files with `python3 scripts/cli.py sync`

Keep the role names and skill names aligned even when the native file formats differ, so prompts and handoffs stay portable.
