# Work Plan

## Storage

- Work ID: `enforceable-cpp-architecture-rules`
- File path: `docs/work/enforceable-cpp-architecture-rules/plan.md`
- Source brief: `docs/work/enforceable-cpp-architecture-rules/brief.md`

## Problem statement
Determine which architecture rules are mechanically enforceable in C++ codebases and which current tools provide enforcement, gating, or only advisory analysis.

## Stakeholders / system context
- The immediate consumer is the requester
- The likely next consumer is a planner selecting a practical enforcement approach for a real repo
- Source material is external documentation, not local product code

## Scope
- Research build-graph enforcement
- Research source-level semantic enforcement
- Research architecture-conformance tooling for dependency and cycle rules
- Capture limitations and non-applicable tools for C++

## Non-goals
- Recommend a specific stack
- Draft rollout steps for any one repository
- Implement custom checks or CI wiring

## Requirements / constraints / assumptions to keep visible
- Prefer primary sources
- Keep conclusions explicitly labeled when inferred
- Do not overstate advisory tooling as hard enforcement
- Focus on C++ support, not general language-agnostic claims

## Public contract / compatibility impact
None. Packet and evidence only.

## SemVer / changelog expectation
None for this research slice.

## Key behavior rules / scenarios
- A finding counts only if it states both the rule type and the enforcement surface
- Unsupported or non-C++ tools must be called out clearly
- Build-level and source-level enforcement must not be conflated

## Trade studies / decision points
Out of scope for this slice. This plan stops before option comparison or stack selection.

## Preferred test strategy
- Verify packet completeness with `python3 scripts/cli.py check-work enforceable-cpp-architecture-rules`
- Manually inspect the evidence file for citation completeness and explicit gap statements

## Validation plan
- Confirm the brief and status files are fully filled
- Confirm the research summary includes key findings, gaps, and an explicit research boundary

## Walking skeleton
1. Gather primary sources for build-system enforcement
2. Gather primary sources for analysis and conformance tooling
3. Synthesize findings into a durable research summary
4. Validate the packet structure and summarize results to the requester

## Minimal configuration / iteration target
Single work packet with brief, plan, status, and one evidence file.

## Exit criteria / milestone criteria
- Packet files are filled
- Research summary is written and cited
- Gaps and limitations are explicit
- Final user summary includes links and a clear research boundary

## Plan steps
1. Collect official documentation for CMake, Bazel, Clang/LLVM, CodeQL, IWYU, and selected architecture-conformance tools.
2. Extract specific enforcement capabilities and constraints from those sources.
3. Separate definitive source facts from cross-source inference.
4. Write the durable research summary under `evidence/`.
5. Validate packet completeness and report the distilled findings.

## Parallel lanes

For each active lane, capture:
- lane name
- owner
- write surface
- worktree / isolation plan
- merge point / integration checkpoint

No active parallel lanes.

## Ownership boundaries
- This plan covers research execution only
- Tool recommendation and rollout design are left for a later planning slice

## Blockers / dependencies
- Availability and clarity of official documentation
- Some commercial tool claims may require care to avoid overstatement from marketing-oriented pages

## Verification gates
- `brief.md` and `status.md` pass `check-work`
- Evidence file contains source-backed findings, gaps, and research boundary

## Risks / unknowns
- Architecture-tool marketing language can blur enforcement and visualization
- C++ support varies by edition, platform, and compiler integration
- Build-tool capabilities may depend on toolchain features that are not universally available

## Escalation triggers
- If primary sources are insufficient to determine whether a capability is enforceable versus advisory
- If conflicting official docs emerge for a tool's C++ support or enforcement scope
