# Work Plan

## Storage

- Work ID: `cpp-static-analysis-research`
- File path: `docs/work/cpp-static-analysis-research/plan.md`
- Source brief: `docs/work/cpp-static-analysis-research/brief.md`

## Problem statement
Determine what “static analysis for C++” currently covers in practice and what the major documented tool families officially claim to do.

## Stakeholders / system context
- Immediate consumer is the requester
- Likely follow-on consumer is a planner selecting or shaping a static-analysis stack
- Source material is external documentation, not local product code

## Scope
- Research mainstream tool families and official capability boundaries
- Capture important caveats and gaps
- Produce a durable research summary under `evidence/`

## Non-goals
- Recommend a particular tool or stack
- Implement any analyzer integration
- Exhaustively enumerate every analyzer in the market

## Requirements / constraints / assumptions to keep visible
- Prefer primary sources
- Label inferred conclusions explicitly
- Keep the question narrowed to mainstream C++ static-analysis tooling
- Distinguish static analysis from runtime sanitization where needed

## Public contract / compatibility impact
None. Research packet only.

## SemVer / changelog expectation
None.

## Key behavior rules / scenarios
- The output must separate linting, bug-finding, security analysis, standards enforcement, and specialized analyses
- Current official support boundaries must be explicit where they materially change the answer
- Compile-database dependence should be called out when it appears across tools

## Trade studies / decision points
Out of scope for this slice. This work ends before any recommendation or selection.

## Preferred test strategy
- Validate `brief.md` and `status.md` with `tools/cli.py check-work`
- Manually inspect the research summary for citations, gaps, and an explicit research boundary

## Validation plan
- Confirm that the research file can stand alone as input to a future planning task
- Defer tool selection and stakeholder-fit validation to a follow-on planning slice

## Walking skeleton
1. Gather primary sources for the main tool families
2. Extract official claims and limitations
3. Synthesize them into a categorized research summary
4. Validate packet completeness and deliver the summary

## Minimal configuration / iteration target
One work packet with brief, plan, status, and a single research evidence file.

## Exit criteria / milestone criteria
- Packet files are filled
- The research summary is written with citations
- Gaps and limitations are explicit
- The final user summary links to the durable evidence and states the research boundary

## Plan steps
1. Collect official docs for Clang/LLVM, GCC, Cppcheck, CodeQL, SonarQube CFamily, and PVS-Studio.
2. Extract tool type, notable capabilities, and official limitations from those sources.
3. Group findings by analysis category and mark cross-source inferences clearly.
4. Write the research summary under `evidence/`.
5. Validate the packet and summarize the findings to the requester.

## Parallel lanes

For each active lane, capture:
- lane name
- owner
- write surface
- worktree / isolation plan
- merge point / integration checkpoint

No active parallel lanes.

## Ownership boundaries
- This plan covers research only
- Tool recommendation, rollout, and policy design are explicitly deferred

## Blockers / dependencies
- Availability of primary documentation for commercial tools
- The broadness of the initial question, which is handled by narrowing the scope to mainstream tools

## Verification gates
- `tools/cli.py check-work cpp-static-analysis-research` passes
- The research file contains cited findings, gaps, and a research boundary

## Risks / unknowns
- Tool marketing pages may overstate capability without enough technical detail
- The topic is broad enough that omitted specialist tools may matter in some domains
- Some static-analysis features blur into compiler diagnostics or security scanning platforms

## Escalation triggers
- If official docs are too sparse to place a tool honestly in the landscape
- If the requester wants recommendation or selection work rather than research-only output
