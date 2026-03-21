# Product Brief

## Storage

- Work ID: `enforceable-cpp-architecture-rules`
- File path: `docs/work/enforceable-cpp-architecture-rules/brief.md`

## Request summary
Research enforceable architecture rules in C++ codebases, including the tooling that can mechanically enforce or at least gate those rules.

## Problem / desired outcome
Produce a durable, source-backed summary of which architecture rules are actually enforceable in C++ codebases and which tools support enforcement versus visualization or advisory analysis.

## Why this matters
Architecture guidance that cannot be checked usually degrades into convention. The requester needs a clear boundary between rules that can be enforced in CI or the build and rules that remain social policy.

## Code drivers
Selected drivers for this work:

- Epistemic uncertainty — determine what the current tool landscape can and cannot enforce in C++.
- Design intent communication — capture the current truth about architecture-rule enforcement so later planning can start from evidence.

Which of the following justify this work?

- User scenarios — enables or improves a real actor workflow
- Risk — addresses a known failure mode, safety, security, or reliability concern
- Epistemic uncertainty — a spike or prototype to reduce unknowns before committing to a design
- Design intent communication — types, assertions, structure, or naming chosen to make intent explicit for future maintainers
- External obligation — regulatory, certification, or standards mandate

Code traceable to none of these is a candidate for removal, not refinement.

## Stakeholders / users
- Repository maintainers defining architecture policy
- Tooling owners responsible for CI and static analysis
- Engineers working in large or layered C++ codebases

## Stakeholder needs / system outcomes
- Distinguish hard enforcement from advisory reporting
- Understand the practical enforcement surfaces: build graph, include graph, AST/semantic analysis, and architecture-conformance analysis
- Identify gaps and tool limitations before planning a concrete rollout

## Design criteria / key parameters
- Prefer primary sources and vendor or project documentation
- Anchor findings to specific docs and sections where practical
- Call out tool limitations explicitly, especially language support and platform restrictions
- Stop before recommending a specific stack or rollout plan

## In scope
- Build-system mechanisms that can encode or enforce dependency boundaries in C++
- Static-analysis and query tooling that can enforce source-level rules
- Architecture-conformance tools that can detect or gate dependency violations, cycles, and location rules
- Major limitations relevant to C++ specifically

## Out of scope
- Repository-specific rollout or migration plan
- Cost comparison, procurement recommendation, or detailed product evaluation
- Non-C++ ecosystems except where needed to clarify that a tool does not support C++

## Constraints
- Use primary sources when available
- Preserve a durable work packet in `docs/work/enforceable-cpp-architecture-rules/`
- Keep facts separated from inferred conclusions and recommendations

## Commit and PR title policy

- Should Jira ticket IDs prefix commit messages? Not applicable for this research turn.
- Should Jira ticket IDs prefix PR titles? Not applicable for this research turn.

## Existing conventions to preserve

- Existing issue tracker, commit, or PR conventions: None required for this research packet.
- Existing release or branching process: Preserve the existing repo workflow and avoid unrelated edits.
- Existing docs, ADR, or architecture layout: Use the `docs/work/enforceable-cpp-architecture-rules/` packet structure.
- Existing build, test, and CI expectations: Use `scripts/cli.py check-work` for packet validation where applicable.
- Existing agent, instruction, or automation files: Follow `AGENTS.md` role and packet conventions.

## System context / external interfaces
- External documentation from CMake, Bazel, Clang/LLVM, GitHub CodeQL, include-what-you-use, SciTools Understand, CppDepend, and SonarSource
- No product code changes are in scope

## Acceptance criteria
- A durable research summary exists under `docs/work/enforceable-cpp-architecture-rules/evidence/`
- The summary identifies enforceable rule categories and the tooling surfaces that support them
- Findings are source-backed, with limitations and gaps called out
- The summary states the research boundary explicitly: facts stop before stack selection or rollout planning

## Measures of effectiveness / performance
- The final summary cleanly answers "what is enforceable?" and "with what tooling?"
- The summary distinguishes definitive findings from inferences
- The summary is compact enough to hand to a planner without restating the research in chat

## Behavior rules / examples (BDD)
- Given a rule about dependency direction, the research should state whether the rule can be enforced at build-graph level, source-analysis level, architecture-analysis level, or only socially.
- Given a tool mentioned in the summary, the research should state whether its role is enforcement, advisory analysis, or both.

## Behavior scenarios (BDD)
- Scenario: A maintainer wants to ban direct includes of private implementation headers across components.
  Outcome: The research identifies whether and where that rule can be enforced.
- Scenario: A maintainer wants to prevent a domain layer from calling platform APIs directly.
  Outcome: The research identifies which tools can express that policy and how strong the enforcement is.
- Scenario: A team assumes a mainstream architecture tool supports C++.
  Outcome: The research clarifies current C++ support and flags non-applicable tools.

## Derived requirements / traceability notes
- All major claims must tie back to primary tooling documentation
- Inferred conclusions must be labeled as inference, not source fact

## Public contract / compatibility impact
No public repo contract change. This packet adds research evidence only.

## Delivery class
Non-productized tool / research work.

## TDD expectation
Not applicable. This turn is research only; verification is source citation and packet validation, not executable behavior tests.

## Validation intent / evidence
Validate by producing a cited summary and ensuring required packet files are filled and checkable.

## SemVer / changelog expectation
No changelog entry expected for this research packet.

## Assumptions
- The requester wants a tool-and-rule landscape summary rather than a repo-specific implementation plan
- Current official docs are the best available primary source for tool capabilities

## Open questions
- Whether the next step should be a tooling recommendation memo or a repo-specific enforcement design
- Whether commercial tooling should be considered alongside an open-source stack in a follow-up plan

## Recommended next owner(s)
- `planner`, if the requester wants a concrete enforcement strategy after reviewing the research

## Parallelization notes
No parallel write lanes used.

## Delegation notes
Research performed directly in the control thread using the repo research workflow.
