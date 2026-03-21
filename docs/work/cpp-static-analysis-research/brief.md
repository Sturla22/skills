# Product Brief

## Storage

- Work ID: `cpp-static-analysis-research`
- File path: `docs/work/cpp-static-analysis-research/brief.md`

## Request summary
Research static analysis for C++.

## Problem / desired outcome
Produce a durable, source-backed summary of the current C++ static-analysis landscape: what major categories exist, what the mainstream tools officially claim to do, and where the practical boundaries are between linting, bug-finding, security analysis, standards enforcement, and specialized analyses.

## Why this matters
“Static analysis for C++” is broad enough to be misleading. The requester needs a current map of the tool families and the official claims behind them before deciding what a real tool stack or rollout should look like.

## Code drivers
Selected drivers for this work:

- Epistemic uncertainty — reduce ambiguity around what “static analysis for C++” actually covers.
- Design intent communication — capture the current tool landscape in a form that can be handed to planning later.

Which of the following justify this work?

- User scenarios — enables or improves a real actor workflow
- Risk — addresses a known failure mode, safety, security, or reliability concern
- Epistemic uncertainty — a spike or prototype to reduce unknowns before committing to a design
- Design intent communication — types, assertions, structure, or naming chosen to make intent explicit for future maintainers
- External obligation — regulatory, certification, or standards mandate

Code traceable to none of these is a candidate for removal, not refinement.

## Stakeholders / users
- Maintainers choosing static-analysis coverage for C++ codebases
- Developers integrating static-analysis tools into local or CI workflows
- Planners comparing future rollout options

## Stakeholder needs / system outcomes
- Distinguish tool categories instead of treating all static analysis as one capability
- Understand official support boundaries and configuration expectations
- Know which tools target bugs, coding standards, security, concurrency, or buffer safety

## Design criteria / key parameters
- Prefer official tool and vendor documentation
- Keep the scope broad enough to be useful but narrow enough to finish in one turn
- Separate source-backed facts from cross-source inferences
- Stop before recommending a tool stack

## In scope
- Mainstream C++ static-analysis categories
- Clang/LLVM analysis tooling relevant to C++
- GCC’s built-in analyzer status for C++
- Standalone C++ analyzers and platforms such as Cppcheck, CodeQL, SonarQube CFamily, and PVS-Studio
- Notable specialized static analyses for C++ such as thread-safety and buffer-safety analysis

## Out of scope
- Exhaustive product catalog of every commercial analyzer
- Detailed pricing, procurement, or license comparison
- Repo-specific rollout or selection recommendation
- Runtime sanitizers except where needed to distinguish them from static analysis

## Constraints
- Use primary sources when available
- Keep a durable packet under `docs/work/cpp-static-analysis-research/`
- If the topic stays too broad, narrow to the mainstream tool landscape and note the remainder as a gap

## Commit and PR title policy

- Should Jira ticket IDs prefix commit messages? Not applicable to this research turn.
- Should Jira ticket IDs prefix PR titles? Not applicable to this research turn.

## Existing conventions to preserve

- Existing issue tracker, commit, or PR conventions: None needed for this research packet.
- Existing release or branching process: No release artifact is expected from this slice.
- Existing docs, ADR, or architecture layout: Use the standard work-packet structure.
- Existing build, test, and CI expectations: Verify the packet with `tools/cli.py check-work`.
- Existing agent, instruction, or automation files: Follow `AGENTS.md` and the repo research workflow.

## System context / external interfaces
- Official documentation from LLVM/Clang, GCC, GitHub CodeQL, Cppcheck, SonarSource, and PVS-Studio
- No product code changes are in scope

## Acceptance criteria
- A durable research summary exists under `docs/work/cpp-static-analysis-research/evidence/`
- The summary explains the main C++ static-analysis categories and maps tools onto them
- Source-backed limitations and gaps are explicit
- The summary states the research boundary and stops before recommendation

## Measures of effectiveness / performance
- The summary answers “what kinds of static analysis exist for C++?” and “what do the major tools officially claim to cover?”
- Cross-source inferences are clearly labeled
- The result is concise enough to hand to a planner without restating the research in chat

## Behavior rules / examples (BDD)
- Given a tool in the summary, the research should state what kind of analysis it performs, not just name it.
- Given a claimed capability, the research should identify whether it comes from official docs or cross-source inference.

## Behavior scenarios (BDD)
- Scenario: A maintainer asks whether `clang-tidy` and a path-sensitive bug finder are the same thing.
  Outcome: The research distinguishes lint-style checks from deeper symbolic-execution-based analysis.
- Scenario: A team assumes GCC’s analyzer is a general C++ answer.
  Outcome: The research states the current official caveat for C++ support.
- Scenario: A team wants to understand whether compile databases matter.
  Outcome: The research notes where official tools rely on `compile_commands.json` or equivalent build context.

## Derived requirements / traceability notes
- Main claims must be tied to official tool documentation
- The narrowed scope must be explicit if the user’s question is broader than one-turn research can cover

## Public contract / compatibility impact
No public contract change. This slice adds research evidence only.

## Delivery class
Non-productized research work.

## TDD expectation
Not applicable. Verification for this slice is citation completeness and packet validation.

## Validation intent / evidence
Validation is limited to the usefulness and traceability of the summary; no separate stakeholder validation is planned in this turn.

## SemVer / changelog expectation
No changelog entry expected.

## Assumptions
- The highest-value narrowing is the mainstream current tool landscape for C++ static analysis
- Official documentation is sufficient to establish the major capability boundaries

## Open questions
- Whether the next step should be a recommendation matrix or a repo-specific rollout plan
- Whether safety-certified or MISRA-focused analyzers need a separate deeper research pass

## Recommended next owner(s)
- `planner`, if the requester wants a selection or rollout recommendation after the research

## Parallelization notes
No parallel write lanes used.

## Delegation notes
Research performed directly in the control thread using the repo research workflow.
