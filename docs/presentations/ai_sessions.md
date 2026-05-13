# Fundamentals of AI Development — Össur R&D Bionics

**From Copilot → Skills → Agent Systems** · Article notes from a 9-session series

---

## Core Thesis

AI development is not just about getting better answers from a chat window. It is a shift in how engineering work is specified, decomposed, executed, checked, and reused.

The core movement is from **writing code** to **designing systems that produce code**. The engineer is still responsible for intent, quality, tradeoffs, and verification, but more of the mechanical work can be delegated to tools that operate inside the development workflow.

```
Prompt → Skill → Agent → Agent System
```

> “Skills are your HAL for AI.”

A prompt is a one-off instruction. A skill is a reusable capability. An agent is a skill wrapped in process, tools, and a feedback loop. An agent system is a set of specialized agents working against shared context, constraints, and evidence. The deeper lesson is that AI becomes more useful when it is treated less like a clever autocomplete and more like an engineering subsystem.

---

## Session Arc

| # | Session | Key Shift | Nugget |
|---|---------|-----------|--------|
| 1 | **Copilot** | AI as context-aware autocomplete | “Nudge, don’t outsource” |
| 2 | **Prompting & Roles** | Autocomplete → directing behavior | “Prompts are specifications, not questions” |
| 3 | **Skills** ⚡ | One-off prompt → reusable capability | “If you use a prompt twice, make it a skill” |
| 4 | **CLI & Automation** | Chat → workflow integration | “If it’s text, it’s automatable” |
| 5 | **Context Engineering** | More context → right context | “Curate, don’t dump” |
| 6 | **Debugging with AI** | AI as hypothesis generator | “Logs are gold” |
| 7 | **Agents** | Single answer → structured loop | “Agent = Skill + Process + Loop” |
| 8 | **Agent Teams** | One agent → specialized roles | “One agent, one responsibility” |
| 9 | **Systems Thinking** | Writing code → orchestrating work | “You are not writing code — you are designing systems of work” |

---

## The Inflection Point — Skills

A skill is a **reusable, structured capability** that encodes how we think, not just what we do. It turns a good prompt into an engineering asset.

This is the key inflection point because prompts do not scale well on their own. They are easy to forget, hard to standardize, and often depend on the author remembering the right context at the right moment. Skills make the important parts explicit: the role, the inputs, the process, the constraints, and the expected output.

```markdown
# SKILL: Firmware Code Review
Role: Senior embedded firmware engineer
Inputs: code, platform, constraints
Process: check memory safety → concurrency → edge cases
Output: issues + fixes
```

Skills give AI your engineering context. Without them, AI is generic. With them, AI understands your platform, your rules, your workflow, and your definition of done.

For firmware teams, this matters because correctness depends on constraints that generic models do not naturally infer: timing, memory ownership, concurrency, hardware boundaries, watchdog behavior, partial failures, and integration evidence. A skill can force those concerns into the work every time instead of relying on the user to remember them.

---

## Real Example — Össur

Two skills wired together into a live development loop:

- **Bitbucket Skill** — agent creates PRs, comments, reads pipeline results
- **B3C Migration Skill** — encodes architecture rules and migration patterns

```
Code change → PR → CI pipeline → Agent reads results → Agent suggests fixes → PR updated
```

> “The agent is now part of the development lifecycle — not a chat window.”

The important change is not that the agent writes code. The important change is that the agent participates in a closed engineering loop. It can make a change, publish it for review, observe the pipeline, interpret the failure, and propose the next correction.

That loop changes the role of the engineer. Instead of manually carrying every task from idea to patch to test result, the engineer designs the boundaries: what the agent is allowed to change, which evidence counts, when to stop, and when to escalate to a human. This is where AI development starts to look like systems engineering.

---

## The 12 Rules

### 1. Give the agent a role

An agent performs better when it knows what it is supposed to be. "Senior embedded firmware engineer", "release manager", and "test verifier" imply different priorities, vocabulary, and failure modes. A role narrows the behavior.

### 2. Add constraints

Constraints turn vague help into bounded work. Tell the agent what not to do, what files it may touch, what checks must pass, what safety rules matter, and which tradeoffs are unacceptable.

### 3. Keep tasks small

Small tasks are easier to review, easier to verify, and easier for agents to complete without drifting. A good AI task has a clear input, a clear output, and a clear stopping condition.

### 4. Plan before acting

Do not let the agent jump straight from request to patch. Ask it to frame the work first: shared understanding, scope, non-goals, constraints, acceptance criteria, steps, and verification. Planning makes the work inspectable before it becomes expensive to correct.

The plan does not need to be heavy. For small work it can be a few bullets. For risky work it should name assumptions, alternatives, dependencies, and unresolved risks. The point is to make the next action deliberate instead of merely plausible.

### 5. Use CLI

Use or create CLI tools for work that should be deterministic. Agents are good at judgment, synthesis, and iteration, but they should not guess at facts a tool can compute. A small command that validates a work packet, extracts IDs, checks formatting, runs a migration, or summarizes test results gives the agent a reliable primitive it can call repeatedly.

This is where AI becomes operational: the agent uses tools to inspect files, run checks, read logs, create branches, update pull requests, and respond to real feedback from the system. The better the CLI surface, the less the agent has to improvise.

### 6. Build skills

If you use a prompt twice, make it a skill. Skills preserve team knowledge and make repeated work more consistent. They are especially valuable when the task depends on local conventions or domain-specific constraints.

### 7. Reuse everything

Reuse prompts, skills, templates, tests, scripts, work packets, examples, and prior decisions. AI performs better when it can stand on existing structure instead of recreating context from scratch.

### 8. Verify outputs

AI output is not done when it looks plausible. Code needs tests. Analysis needs evidence. Documentation needs reader checks. Verification is what turns generated work into engineering work.

### 9. Think in loops

Useful agent work is usually iterative: inspect, change, run, observe, correct. The loop matters more than the first answer because the environment gives feedback the model did not have at generation time.

### 10. Use specialized agents

One general agent can do many things, but specialized agents make better tradeoffs. A planner, developer, verifier, reviewer, and release manager should not optimize for the same thing.

### 11. Context matters most

The limiting factor is often not model intelligence but context quality. Curate the relevant files, constraints, examples, failure history, and acceptance criteria. Do not dump everything and hope the model finds the signal.

### 12. Design systems, not prompts

Prompts are useful, but systems are durable. The goal is to design repeatable workflows with roles, skills, tools, evidence, and feedback loops. That is how AI moves from assistant to engineering infrastructure.

---

## What This Means for Engineers

The engineer's job does not disappear. It moves up a level.

AI can draft, search, transform, summarize, and iterate quickly, but it cannot own the product context, the safety case, the customer need, or the final judgment. Engineers still define what good means. They decide which risks matter, which evidence is enough, and which tradeoffs are acceptable.

The practical skill is learning how to delegate without abdicating responsibility. Good AI development looks like good engineering management at small scale: clear roles, small tasks, explicit constraints, fast feedback, and reviewable outputs.

For firmware and embedded systems, that discipline is even more important. The cost of a plausible-but-wrong answer is higher when software touches hardware, batteries, motors, sensors, timing deadlines, and user safety. AI helps most when it is inside a workflow that already respects those constraints.

---

## Closing

> “We are not just using AI — we are extending it with our engineering system.”

> “In a year, writing firmware without AI will feel like writing C without a compiler.”

The fundamentals of AI development are not prompt tricks. They are engineering fundamentals applied to a new kind of tool: specify the work, constrain the system, reuse the knowledge, close the loop, and verify the result.
