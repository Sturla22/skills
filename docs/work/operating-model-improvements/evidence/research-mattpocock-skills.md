# Research: mattpocock/skills Repository

## Research Question

What skills exist in the public GitHub repository `https://github.com/mattpocock/skills`, what is the complete content of each SKILL.md file (particularly grill-me, write-a-prd, prd-to-issues, prd-to-plan, tdd, and skills related to design, architecture, systems engineering, or project management), what meta-documentation describes how the skills are used together, and what structural patterns are present in the skill files?

## Retrieval Date

2026-03-23. All sources fetched via GitHub raw content and GitHub REST API (`api.github.com`).

---

## Sources

- Repository index: `https://api.github.com/repos/mattpocock/skills/git/trees/main?recursive=1` (retrieved 2026-03-23)
- README: `https://raw.githubusercontent.com/mattpocock/skills/main/README.md` (retrieved 2026-03-23)
- Individual SKILL.md files: `https://raw.githubusercontent.com/mattpocock/skills/main/<skill-name>/SKILL.md` (all retrieved 2026-03-23)
- Supplementary reference files under `tdd/` and `improve-codebase-architecture/` (retrieved 2026-03-23)

No version tag or pinned commit SHA was identified in the README. The tree above corresponds to the `main` branch as of retrieval date. No release tags were observed in the API response.

---

## Full Skill Inventory

The repository contains 17 skills, each in its own top-level directory containing at minimum a `SKILL.md` file. The category grouping below is from the README; the file system does not use subdirectories for categories.

### Planning and Design

| Skill | One-line description |
|---|---|
| `grill-me` | Conduct a relentless interview to stress-test a plan or design until shared understanding is reached |
| `write-a-prd` | Create a Product Requirements Document through user interview, codebase exploration, and module design; submit as a GitHub issue |
| `prd-to-plan` | Convert a PRD into a phased implementation plan using vertical slices; output a Markdown file under `./plans/` |
| `prd-to-issues` | Break a PRD into independently-assignable GitHub issues using vertical tracer-bullet slices |
| `design-an-interface` | Generate 3+ radically different interface designs in parallel using the "Design It Twice" methodology |
| `request-refactor-plan` | Develop a detailed refactoring plan with incremental commits; document as a GitHub issue |

### Development

| Skill | One-line description |
|---|---|
| `tdd` | Implement test-driven development using the red-green-refactor cycle with a vertical-slice (tracer bullet) discipline |
| `triage-issue` | Diagnose a bug and create a TDD-based fix plan as a GitHub issue |
| `improve-codebase-architecture` | Surface architectural friction and propose module-deepening refactors as GitHub issue RFCs |
| `migrate-to-shoehorn` | Replace TypeScript `as` assertions in tests with `@total-typescript/shoehorn` utilities |
| `scaffold-exercises` | Create structured exercise directory structures for a course repo |

### Tooling and Setup

| Skill | One-line description |
|---|---|
| `git-guardrails-claude-code` | Install pre-tool-use hooks in Claude Code to block destructive git operations |
| `setup-pre-commit` | Install Husky, lint-staged, and Prettier as a pre-commit hook stack |

### Writing and Knowledge

| Skill | One-line description |
|---|---|
| `write-a-skill` | Guide the creation of new skills with proper SKILL.md structure and description best practices |
| `edit-article` | Edit an article draft section-by-section for clarity, coherence, and flow |
| `ubiquitous-language` | Extract domain terminology from conversation into a canonical glossary file |
| `obsidian-vault` | Configure and query a personal Obsidian vault using shell commands |

---

## Full Content of Each SKILL.md

### grill-me

Source: `https://raw.githubusercontent.com/mattpocock/skills/main/grill-me/SKILL.md`

No YAML frontmatter was observed in the fetched content. Full description as synthesized from the raw file:

> Interview the user relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between choices sequentially. For each question, provide a recommended answer. If a question can be answered by exploring the codebase, explore the codebase instead of speculating.
>
> Activate when the user wants to stress-test a plan, get design critique, or explicitly says "grill me."

Key behavioral rules:
- Walk decision trees branch by branch, resolve dependencies sequentially
- Provide a recommended answer alongside each question
- Prefer codebase exploration over speculation when the codebase can resolve a question
- Goal is genuine shared understanding, not surface-level agreement

---

### write-a-prd

Source: `https://raw.githubusercontent.com/mattpocock/skills/main/write-a-prd/SKILL.md`

YAML frontmatter present:

```yaml
---
name: write-a-prd
description: Create a PRD through user interview, codebase exploration, and module design, then submit as a GitHub issue. Use when user wants to write a PRD, create a product requirements document, or plan a new feature.
---
```

Process steps (may be skipped if not necessary):

1. Ask for a long, detailed description of the problem and potential solutions.
2. Explore the repo to verify assertions and understand the current codebase state.
3. Interview the user relentlessly about every aspect of the plan. Walk each branch of the design tree, resolving dependencies between decisions one-by-one.
4. Sketch major modules to build or modify. Actively look for opportunities to extract **deep modules** — a deep module has a lot of functionality behind a simple, testable interface that rarely changes, contrasted with a shallow module. Check with the user which modules to test.
5. Write the PRD using the template below and submit as a GitHub issue.

PRD template sections:
- **Problem Statement**: the problem from the user's perspective
- **Solution**: the solution from the user's perspective
- **User Stories**: a long, numbered list in "As a <actor>, I want <feature>, so that <benefit>" format; must be extremely extensive
- **Implementation Decisions**: modules to build/modify, interface changes, architectural decisions, schema changes, API contracts — no specific file paths or code snippets
- **Testing Decisions**: what makes a good test, which modules will be tested, prior art in the codebase
- **Out of Scope**: what is explicitly excluded
- **Further Notes**: anything else

---

### prd-to-issues

Source: `https://raw.githubusercontent.com/mattpocock/skills/main/prd-to-issues/SKILL.md`

No frontmatter observed. Process:

1. Locate the PRD: ask the user for the GitHub issue number or URL; fetch with `gh issue view <number>` if not already in context.
2. Optionally explore the codebase to understand current state.
3. Draft vertical slices. Each slice is a **tracer bullet**: a thin, complete path through ALL integration layers, not a horizontal slice of one layer. Slices are either HITL (require human interaction, e.g., architectural decision or design review) or AFK (can be implemented and merged without human interaction). Prefer AFK.
   - Vertical slice rules: each slice delivers a narrow but complete path through every layer (schema, API, UI, tests); a completed slice is demoable or verifiable on its own; prefer many thin slices over few thick ones.
4. Quiz the user: present the breakdown as a numbered list showing Title, Type (HITL/AFK), Blocked by, and User stories covered. Iterate on granularity, dependency relationships, HITL/AFK classification.
5. Create GitHub issues in dependency order using `gh issue create`.

Issue template:
- **Parent PRD**: reference to PRD issue number
- **What to build**: end-to-end behavior description, not layer-by-layer
- **Acceptance criteria**: checklist
- **Blocked by**: list of blocking issues or "None - can start immediately"
- **User stories addressed**: by number from the parent PRD

Constraint: do NOT close or modify the parent PRD issue.

---

### prd-to-plan

Source: `https://raw.githubusercontent.com/mattpocock/skills/main/prd-to-plan/SKILL.md`

No frontmatter observed. Process:

1. Confirm the PRD is in context; if not, ask the user to paste it or point to a file.
2. Explore the codebase to understand current architecture, existing patterns, and integration layers.
3. Identify durable architectural decisions before slicing: route structures/URL patterns, database schema shape, key data models, authentication/authorization approach, third-party service boundaries. These go in the plan header.
4. Draft vertical slices using the same tracer-bullet rules as `prd-to-issues`: each phase is complete through all layers, demoable on its own. Rules additionally specify: do NOT include specific file names, function names, or implementation details likely to change; DO include durable decisions (route paths, schema shapes, data model names).
5. Quiz the user: present as numbered list with Title and User stories covered. Iterate on granularity.
6. Write the plan as a Markdown file named after the feature under `./plans/` (create the directory if needed).

Plan file template:
- Header: feature name, source PRD reference
- **Architectural decisions**: durable decisions applying across all phases (routes, schema, key models)
- Per phase: Title, User stories, What to build (end-to-end behavior), Acceptance criteria (checklist)

Key distinction from `prd-to-issues`: output is a local Markdown file rather than GitHub issues; phases instead of issues; explicitly identifies durable architectural decisions before slicing.

---

### tdd

Source: `https://raw.githubusercontent.com/mattpocock/skills/main/tdd/SKILL.md` plus supplementary files `tests.md`, `mocking.md`, `deep-modules.md`, `interface-design.md`, `refactoring.md`

No frontmatter observed in SKILL.md. The skill has five supplementary reference files in the same directory.

**Philosophy:**
- Tests should verify behavior through public interfaces, not implementation details. Code can change entirely; tests should not.
- Good tests are integration-style: exercise real code paths through public APIs; describe what the system does, not how; survive refactors; read like specifications.
- Bad tests are coupled to implementation: mock internal collaborators, test private methods, verify through external means (e.g., querying a database directly). Warning sign: test breaks on rename of internal function.

**Anti-pattern explicitly named: Horizontal Slices**
- Do NOT write all tests first, then all implementation. This is called "horizontal slicing" and produces crap tests: tests written in bulk test imagined behavior, not actual behavior; they test the shape of things rather than user-facing behavior; they outrun the developer's understanding.
- Correct approach: vertical slices via tracer bullets. One test -> one implementation -> repeat.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED->GREEN: test1->impl1
  RED->GREEN: test2->impl2
  ...
```

**Workflow:**

1. **Planning** (before writing any code):
   - Confirm interface changes needed with user
   - Confirm which behaviors to test (prioritize)
   - Identify opportunities for deep modules
   - Design interfaces for testability
   - List behaviors to test (not implementation steps)
   - Get user approval
   - Key question: "What should the public interface look like? Which behaviors are most important to test?"
   - Acknowledge: "You can't test everything" — focus on critical paths and complex logic

2. **Tracer Bullet**: Write ONE test for ONE thing. Red then Green. This proves the end-to-end path works.

3. **Incremental Loop**: For each remaining behavior: one test at a time, only enough code to pass the current test, no anticipation of future tests, stay focused on observable behavior.

4. **Refactor**: Only after all tests pass. Look for: extract duplication, deepen modules, apply SOLID naturally, consider what new code reveals about existing code. Run tests after each refactor step. Never refactor while RED.

**Per-cycle checklist:**
- Test describes behavior, not implementation
- Test uses public interface only
- Test would survive internal refactor
- Code is minimal for this test
- No speculative features added

**Supplementary: tests.md** — Good tests are integration-style, testing observable behavior through the public API. Bad tests mock internal collaborators or bypass the interface to verify via external state.

**Supplementary: mocking.md** — Mock at system boundaries only (external APIs, databases sometimes, time/randomness, filesystem sometimes). Do not mock your own classes/modules or internal collaborators. Design for mockability via dependency injection and SDK-style interfaces (specific functions per operation rather than one generic fetcher).

**Supplementary: deep-modules.md** — Deep module: small interface + lots of implementation. Shallow module: large interface + little implementation. Ask when building interfaces: Can I reduce methods? Can I simplify parameters? Can I hide more complexity inside?

**Supplementary: interface-design.md** — Three principles: (1) accept dependencies, don't create them (dependency injection); (2) return results, don't produce side effects (pure functions); (3) minimal API surface (fewer methods and parameters).

**Supplementary: refactoring.md** — Refactor candidates after TDD: duplication, long methods, shallow modules, feature envy, primitive obsession, and existing code revealed as problematic by new code.

---

### design-an-interface

Source: `https://raw.githubusercontent.com/mattpocock/skills/main/design-an-interface/SKILL.md`

No frontmatter observed. This skill implements "Design It Twice" from John Ousterhout's "A Philosophy of Software Design."

Process:

1. **Gather requirements**: problem domain, users, key operations, constraints, what stays internal vs. exposed.
2. **Generate designs**: deploy 3+ parallel sub-agents, each with a different design constraint:
   - Agent 1: minimize methods (1-3 max)
   - Agent 2: maximize flexibility
   - Agent 3: optimize for the most common case
   - Agent 4: borrow from a specific paradigm (e.g., ports and adapters)
   Each agent produces: interface signature, usage examples, hidden complexity details, trade-off analysis.
3. **Present designs**: display each sequentially with signatures, examples, and internal abstractions.
4. **Compare designs**: evaluate across interface simplicity, general-purpose applicability, implementation efficiency, and depth. "Small interface hiding significant complexity = deep module (good). Large interface with minimal substance = shallow (bad)."
5. **Synthesize**: identify which design best matches the primary use case; consider hybrid approaches.

Constraint: avoid similar designs — enforce radical differences. Skip implementation details; focus purely on interface shape.

---

### request-refactor-plan

Source: `https://raw.githubusercontent.com/mattpocock/skills/main/request-refactor-plan/SKILL.md`

No frontmatter observed. Eight-step process:

1. Gather requirements: collect detailed problem description and solution ideas.
2. Verify assumptions: explore the repository to understand current codebase state.
3. Explore alternatives: discuss other potential approaches.
4. Implementation interview: conduct thorough technical discussion.
5. Define scope: precisely determine what will and won't change.
6. Assess testing: evaluate existing test coverage and plan testing strategy.
7. Break into commits: decompose work into minimal, working steps. Reference: Martin Fowler's guidance to "make each refactoring step as small as possible, so that you can always see the program working."
8. Create GitHub issue using a structured template.

Issue template sections:
- **Problem Statement**: developer's perspective
- **Solution**: proposed approach
- **Commits**: detailed implementation plan in plain English with tiny, incremental steps
- **Decision Document**: module changes, interface modifications, architectural decisions, technical clarifications — without specific file paths
- **Testing Decisions**: quality standards, modules to test, similar test patterns in the codebase
- **Out of Scope**: excluded items
- **Further Notes**: additional context

---

### improve-codebase-architecture

Source: `https://raw.githubusercontent.com/mattpocock/skills/main/improve-codebase-architecture/SKILL.md` and `improve-codebase-architecture/REFERENCE.md`

No frontmatter observed. Explicitly draws on John Ousterhout's "A Philosophy of Software Design" concept of deep modules.

Process:

1. **Explore the codebase**: use an Agent tool in Explore mode; navigate organically, not with rigid heuristics. Look for friction:
   - Understanding one concept requires bouncing between many small files
   - Modules so shallow the interface is nearly as complex as the implementation
   - Pure functions extracted just for testability, hiding real bugs in how they're called
   - Tightly-coupled modules creating integration risk at seams
   - Untested or hard-to-test code
   "The friction you encounter IS the signal."

2. **Present candidates**: numbered list of deepening opportunities. For each: Cluster (modules/concepts involved), Why they're coupled (shared types, call patterns, co-ownership), Dependency category (see REFERENCE.md), Test impact (which existing tests would be replaced by boundary tests). Do NOT propose interfaces at this stage.

3. User picks a candidate.

4. **Frame the problem space**: write a user-facing explanation of the constraints, dependencies, and a rough illustrative code sketch. Show to user, then immediately proceed to step 5.

5. **Design multiple interfaces**: spawn 3+ sub-agents in parallel. Each agent has a separate technical brief and a different design constraint (same as `design-an-interface`). Each sub-agent outputs: interface signature, usage example, what complexity it hides, dependency strategy, trade-offs. Present designs sequentially, then compare in prose. Give an opinionated recommendation; propose hybrids if useful.

6. User picks an interface.

7. **Create GitHub issue**: use `gh issue create` without asking user to review first.

**Dependency categories (from REFERENCE.md)**:
1. In-process: pure computation, in-memory state, no I/O — always deepenable, just merge and test directly
2. Local-substitutable: deps with local test stand-ins (e.g., PGLite for Postgres, in-memory filesystem) — deepenable if stand-in exists
3. Remote but owned (Ports and Adapters): own services across a network boundary — define a port at the boundary, inject the transport, test with in-memory adapter
4. True external (Mock): third-party services (Stripe, Twilio, etc.) — mock at the boundary, inject as a port

**Testing strategy (from REFERENCE.md)**: "replace, don't layer" — old unit tests on shallow modules are waste once boundary tests exist; delete them. Write new tests at the deepened module's interface boundary. Tests assert on observable outcomes through the public interface, not internal state. Tests should survive internal refactors.

**Issue template (from REFERENCE.md)**:
- Problem: architectural friction, shallow coupling, integration risk
- Proposed Interface: signature, usage example, what complexity it hides
- Dependency Strategy: which category and how deps are handled
- Testing Strategy: new boundary tests, old tests to delete, test environment needs
- Implementation Recommendations: durable guidance not coupled to current file paths (what the module should own, hide, expose, and how callers should migrate)

---

### triage-issue

Source: `https://raw.githubusercontent.com/mattpocock/skills/main/triage-issue/SKILL.md`

No frontmatter observed. Five-phase workflow:

1. **Problem capture**: obtain a brief issue description with minimal questioning.
2. **Exploration and diagnosis**: investigate where the bug manifests, what code path is involved, why it fails, and what related code exists. Examine source files, tests, recent changes, error handling, and similar patterns.
3. **Fix approach identification**: determine the minimal necessary change, affected modules, required test behaviors, and whether this is a regression or design flaw.
4. **TDD fix plan design**: create ordered RED-GREEN cycles. Each cycle = "a specific test that captures broken/missing behavior" followed by "minimal code change to make that test pass." Tests must verify behavior through public interfaces and survive internal refactors.
5. **GitHub issue creation**: use `gh issue create` without asking user to review first.

Durability principle: fix suggestions must "survive radical codebase changes" by describing "behaviors and contracts" rather than implementation details. Assert on observable outcomes (API responses, UI state, user-visible effects) rather than internal state.

---

### write-a-skill

Source: `https://raw.githubusercontent.com/mattpocock/skills/main/write-a-skill/SKILL.md`

No frontmatter observed in fetched content. This is the meta-skill for creating other skills.

Structure of a skill:
- Required: `SKILL.md` (main instructions, ideally under 100 lines)
- Optional: `REFERENCE.md` for detailed documentation that would bloat the main file
- Optional: `EXAMPLES.md` for concrete examples
- Optional: `scripts/` subdirectory for deterministic utility helpers

Description field design (critical):
- The description is the primary mechanism for skill selection — "the only thing your agent sees" when deciding which skill to load
- Must be under 1024 characters
- Use third-person voice
- Two-sentence structure: sentence 1 explains what the skill does; sentence 2 specifies activation contexts using "Use when [specific triggers]"
- Must clearly signal both capability and activation triggers

Quality checklist before finalizing:
- Description includes triggers
- Main file stays concise (under 100 lines)
- No time-sensitive information
- Terminology is consistent
- Examples are concrete
- References are one level deep (no nested REFERENCE.md chains)

Process: gather requirements from user about task domain and use cases, draft the skill, review collaboratively.

---

### ubiquitous-language

Source: `https://raw.githubusercontent.com/mattpocock/skills/main/ubiquitous-language/SKILL.md`

No frontmatter observed. Domain-language extraction skill.

Process:
1. Scan conversation for domain-relevant nouns, verbs, and concepts.
2. Identify problems: same word used for different concepts (ambiguity); different words for same concept (synonyms); vague or overloaded terms.
3. Propose a canonical glossary with opinionated term choices.
4. Write to `UBIQUITOUS_LANGUAGE.md` in the working directory.
5. Output a summary inline.

Output format: Markdown table grouped by domain cluster (Order lifecycle, People, Relationships, etc.) with columns: Term, Definition, Aliases to avoid. Also includes a Relationships section (cardinality between terms), an Example dialogue section (3-5 exchanges between dev and domain expert demonstrating precise term usage), and a Flagged ambiguities section.

Rules:
- Be opinionated: pick the best term, list others as aliases to avoid
- Flag conflicts explicitly
- Keep definitions to one sentence max: define what it IS, not what it does
- Show relationships with cardinality
- Only include domain terms, not generic programming concepts
- Group by natural clusters; don't force groupings

Re-running behavior: read existing file, incorporate new terms, update changed definitions, mark entries "(updated)" and "(new)", re-flag new ambiguities, rewrite example dialogue.

Post-output instruction: state "I've written/updated UBIQUITOUS_LANGUAGE.md. From this point forward I will use these terms consistently."

---

### git-guardrails-claude-code

Source: `https://raw.githubusercontent.com/mattpocock/skills/main/git-guardrails-claude-code/SKILL.md`

No frontmatter observed. Installs a `PreToolUse` hook in Claude Code settings to intercept and block destructive git operations before execution.

Operations intercepted: `git push`, `git reset --hard`, `git clean`, `git branch -D`, checkout operations.

Setup:
1. Choose scope: single project (`.claude/settings.json`) or global (`~/.claude/settings.json`).
2. Copy blocking script to hooks directory, make executable.
3. Add `PreToolUse` hook entry targeting the "Bash" tool.
4. Customize blocked patterns by editing the script.
5. Test by piping a sample git command — should return exit code 2 with a blocked message.

Supplementary file: `scripts/block-dangerous-git.sh` (the actual blocking script).

---

### setup-pre-commit

Source: `https://raw.githubusercontent.com/mattpocock/skills/main/setup-pre-commit/SKILL.md`

No frontmatter observed. Installs Husky + lint-staged + Prettier as a pre-commit hook.

Steps:
1. Detect package manager from lock file (npm/pnpm/yarn/bun).
2. Install `husky lint-staged prettier` as devDependencies.
3. Run `npx husky init`.
4. Create `.husky/pre-commit` running `lint-staged`, `typecheck`, and `test` (omit typecheck/test if no such scripts exist).
5. Create `.lintstagedrc` running `prettier --ignore-unknown --write` on all files.
6. Create `.prettierrc` only if no Prettier config exists (specific defaults provided).
7. Verify: check file existence, run `npx lint-staged`.
8. Commit everything with message `Add pre-commit hooks (husky + lint-staged + prettier)` — this smoke-tests the hooks.

---

### edit-article

Source: `https://raw.githubusercontent.com/mattpocock/skills/main/edit-article/SKILL.md`

No frontmatter observed. Short two-phase process:

1. Divide the article into sections based on headings; consider information dependencies ("information is a directed acyclic graph"). Confirm section structure with the user.
2. For each section, rewrite for clarity, coherence, and flow; maintain maximum 240 characters per paragraph.

---

### obsidian-vault

Source: `https://raw.githubusercontent.com/mattpocock/skills/main/obsidian-vault/SKILL.md`

No frontmatter observed. Configuration for a specific personal vault at `/mnt/d/Obsidian Vault/AI Research/`. This skill appears to be personalized to the author's setup rather than a generalizable template.

Structure: flat layout using wikilinks and index notes instead of folders. All note names in Title Case. Shell commands provided for search (by filename, by content, by backlinks, for index files).

---

### scaffold-exercises

Source: `https://raw.githubusercontent.com/mattpocock/skills/main/scaffold-exercises/SKILL.md`

No frontmatter observed. Highly specific to a particular course repo (`ai-hero-cli`). Creates numbered exercise directories passing a project-specific linter.

---

### migrate-to-shoehorn

Source: `https://raw.githubusercontent.com/mattpocock/skills/main/migrate-to-shoehorn/SKILL.md`

No frontmatter observed. TypeScript-specific skill for replacing `as` assertions in test files with `@total-typescript/shoehorn` utilities (`fromPartial()`, `fromAny()`, `fromExact()`). Constrained to test code only, never production code.

---

## README Meta-Documentation

Source: `https://raw.githubusercontent.com/mattpocock/skills/main/README.md`

The README is a catalog of all skills grouped into four categories (Planning and Design, Development, Tooling and Setup, Writing and Knowledge). Each entry has a short one-line description.

Installation pattern: `npx skills@latest add mattpocock/skills/<skill-name>`

The README does not describe a prescribed workflow order for combining skills, dependency relationships between skills, or how to sequence them for complex tasks. It presents them as independent units installable on demand.

The `write-a-skill` skill is the only explicit meta-documentation about how to author skills. It establishes the format contract.

---

## Structural Patterns Observed

### Pattern 1: YAML Frontmatter — Inconsistently Used

Only `write-a-prd` was observed to have explicit YAML frontmatter with `name` and `description` fields. The `write-a-skill` meta-skill specifies that descriptions are the primary selection mechanism (under 1024 characters, third-person, two-sentence with trigger clause), but most existing skills do not include the frontmatter block. This is a structural inconsistency between the documented standard and the actual files.

### Pattern 2: Process Steps are Numbered Lists

Every skill uses a numbered list of sequential process steps. Steps are described in imperative voice. Optional steps are explicitly flagged ("You may skip steps if you don't consider them necessary" in `write-a-prd`).

### Pattern 3: User Quiz / Iteration Loop

Multiple planning skills (`prd-to-issues`, `prd-to-plan`, `write-a-prd`, `design-an-interface`, `improve-codebase-architecture`) include an explicit step of presenting a draft to the user, soliciting structured feedback on granularity and correctness, and iterating before proceeding to output. This is a recurring pattern: draft-quiz-iterate.

### Pattern 4: Output to GitHub Issues via CLI

Six skills (`write-a-prd`, `prd-to-issues`, `request-refactor-plan`, `triage-issue`, `improve-codebase-architecture`, and implied by `tdd` indirectly) terminate in a `gh issue create` step. Several explicitly instruct the agent to create the issue without asking the user to review first ("Do NOT ask the user to review before creating — just create it and share the URL" in `improve-codebase-architecture`).

### Pattern 5: Vertical Slices / Tracer Bullets as a Cross-Cutting Concept

The term "tracer bullet" and the vertical-slice decomposition pattern appear in `tdd`, `prd-to-issues`, and `prd-to-plan`, using nearly identical language. This is a shared conceptual vocabulary across the planning and development skill categories.

### Pattern 6: Deep Module as a Cross-Cutting Concept

John Ousterhout's "deep module" concept (small interface, large implementation) is referenced in `write-a-prd`, `tdd`, `design-an-interface`, `improve-codebase-architecture`, and `request-refactor-plan`. It functions as the theoretical backbone of the architecture-related skills.

### Pattern 7: Supplementary Reference Files for Long Content

The `tdd` skill has five supplementary Markdown files (`tests.md`, `mocking.md`, `deep-modules.md`, `interface-design.md`, `refactoring.md`). The `improve-codebase-architecture` skill has one (`REFERENCE.md`). The `write-a-skill` meta-skill documents this split as intentional: keep `SKILL.md` under 100 lines, split distinct subject domains into separate reference files. The main SKILL.md links to supplementary files using relative Markdown links.

### Pattern 8: Parallel Sub-Agents for Design Exploration

Both `design-an-interface` and `improve-codebase-architecture` instruct the agent to spawn multiple parallel sub-agents with different design constraints (minimize methods / maximize flexibility / optimize common case / ports-and-adapters paradigm). This is the "Design It Twice" pattern made concrete.

### Pattern 9: GitHub CLI (`gh`) as Standard Tool

The skills assume the `gh` CLI is available and use it as the primary interface to GitHub: `gh issue view`, `gh issue create`. No REST API calls or web UI instructions.

### Pattern 10: Durable vs. Volatile Information Distinction

`prd-to-plan` and `request-refactor-plan` explicitly distinguish durable decisions (route paths, schema shapes, data model names) from volatile details (specific file paths, function names, implementation details likely to change). The plan template instructs to include the former and exclude the latter.

---

## Gaps and Items Not Confirmed

1. **Frontmatter presence**: only `write-a-prd` was confirmed to have YAML frontmatter. The `write-a-skill` standard specifies frontmatter with `name` and `description` fields as the skill selection mechanism. Whether the other 16 skills have frontmatter that was stripped by the WebFetch summarization layer is unconfirmed. The raw content fetch returned the file content via an AI summarization step for most skills, not character-for-character verbatim text. The only skill where the frontmatter was preserved in the fetch was `write-a-prd`. This is a limitation of the retrieval method.

2. **grill-me verbatim text**: the `grill-me` SKILL.md fetch returned an AI summary rather than the verbatim file. The content is consistent with the skill's stated purpose but may omit phrasing details.

3. **`obsidian-vault` generalizability**: this skill contains a hard-coded path to the author's personal vault. It is unclear whether the skill is intended as a personal configuration or as a template for adaptation.

4. **`scaffold-exercises` generalizability**: this skill is tightly coupled to the `ai-hero-cli` linter and a specific repo structure. Its reuse value outside that context is low.

5. **Inter-skill sequencing**: the README does not document a canonical skill sequence for complex workflows (e.g., "run `grill-me` before `write-a-prd`"). No `WORKFLOW.md` or similar sequencing guide was found in the repository.

6. **`write-a-skill` EXAMPLES.md or supplementary files**: the `write-a-skill` meta-skill mentions optional `EXAMPLES.md` files but none were found in the repository tree. The tree scan was confirmed complete.

7. **Version / release state**: no semantic version tags, release notes, or CHANGELOG were found. The repository is tracked at commit-level only on the `main` branch.

8. **License terms**: a `LICENSE` file exists but its content was not fetched. Terms governing adaptation or redistribution are unconfirmed.

---

## Research Boundary Statement

The facts in this document end at the description of what each skill file contains and the structural patterns observable across the file set. The following questions belong to planning and option comparison, not to this research summary:

- Which patterns from this repository should be adopted, adapted, or rejected for the `reflex` operating model
- How the `write-a-prd` / `prd-to-issues` / `prd-to-plan` pipeline compares with the existing `brief.md` / `plan.md` / `handoffs/` packet structure in this repo
- Whether the `grill-me` or `ubiquitous-language` skills address gaps in the current role or skill set
- Whether the deep-module and vertical-slice vocabulary should be incorporated into existing skills
- Whether the `write-a-skill` format standard should replace or augment the current skill file format in `.agents/`
