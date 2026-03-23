# 🧠 AI for Firmware Engineers @ Össur R&D Bionics

### From Copilot → Skills → Agent Systems

---

# 🎯 Opening (2–3 min)

## What this is NOT

* Not a “what is AI” talk
* Not hype
* Not replacing engineers

## What this IS

> How AI can become part of our **firmware development workflow**

---

## Core Thesis

> We are moving from:
>
> * writing code
>   to:
> * designing systems that produce code

---

## Mental Model

```text
Prompt → Skill → Agent → Agent System
```

---

## One-liner to remember

> “Skills are your HAL for AI”

---

---

# 🧩 Session 1 — Copilot: Smart Pair Programming

---

## Key Idea

> AI is just **context-aware autocomplete**

---

## What works well

* Small functions
* Clear intent
* Good naming

---

## What doesn’t

* Large files
* Vague tasks
* “Write everything”

---

## Example

```c
// Add timeout handling to I2C transfer
// No heap
// Must be ISR-safe
```

---

## Nugget

> “Nudge, don’t outsource”

---

## Loop

```text
Engineer → Comment → Copilot → Review → Commit
```

---

## What to say

* “Copilot is not here to think for you”
* “It’s here to accelerate what you already understand”

---

---

# 🧩 Session 2 — Prompting & Roles

---

## Shift

> From autocomplete → **directing behavior**

---

## Bad prompt

> “Review this”

---

## Good prompt

```text
Role: Senior embedded firmware engineer
Context: Cortex-M, no heap, ISR-safe
Task: Review this module
Focus:
- race conditions
- memory safety
- edge cases
Output:
- issues + fixes
```

---

## Nugget

> “Prompts are specifications, not questions”

---

## Key insight

> Giving a role compresses expertise

---

## Structure

```text
Role → Context → Task → Constraints → Output
```

---

## What to say

* “We stop treating AI like Google”
* “We treat it like a junior engineer with context”

---

---

# 🧩 Session 3 — Skills (Claude Skills 2.0)

---

## THIS IS THE INFLECTION POINT

---

## Shift

```text
Prompt → Skill
```

---

## Definition

> A skill is a **reusable, structured capability**

---

## Example Skill

```markdown
# SKILL: Firmware Code Review

## Role
Senior embedded firmware engineer

## Inputs
- code
- platform
- constraints

## Process
1. Check memory safety
2. Check concurrency
3. Check edge cases

## Output
- issues
- fixes
```

---

## Nugget

> “If you use a prompt twice → make it a skill”

---

## Firmware analogy

```text
Skill = function/module
```

---

## Key idea

> Skills encode **how we think**, not just what we do

---

## What to say

* “This is where things get interesting”
* “We’re no longer just using AI—we’re building capability”

---

---

# 🧩 Session 4 — CLI & Automation

---

## Shift

> From chat → **workflow integration**

---

## Example

```bash
git diff | ai --skill firmware_review
```

---

## Nugget

> “If it’s text, it’s automatable”

---

## Pipeline thinking

```text
Input → Transform → Validate → Iterate
```

---

## Real leverage

* PR review
* test generation
* log analysis

---

## What to say

* “CLI is where AI becomes practical”
* “This is where we start saving real time”

---

---

# 🧩 Session 5 — Context Engineering

---

## Most underrated skill

---

## Key idea

> Context quality > model quality

---

## Bad

* dump entire repo

---

## Good

* relevant files
* constraints
* examples

---

## Nugget

> “Curate, don’t dump”

---

## Insight

> More context ≠ better context

---

## What to say

* “This is the difference between frustration and usefulness”

---

---

# 🧩 Session 6 — Debugging with AI

---

## This is where firmware teams lean in

---

## Key idea

> AI is a **hypothesis generator**

---

## Loop

```text
Observe → Hypothesize → Test → Refine
```

---

## Example

Input:

* logs
* crash data

AI:

* suggests root causes
* suggests instrumentation

---

## Nugget

> “Logs are gold”

---

## Important

> AI does NOT validate—you do

---

## What to say

* “This aligns perfectly with how we already debug”
* “It just speeds up the thinking”

---

---

# 🧩 Session 7 — Agents

---

## Definition

> Agent = Skill + Process + Loop

---

## Example

```text
1. Analyze logs
2. Generate hypotheses
3. Suggest test
4. Evaluate result
```

---

## Nugget

> “Agents are structured thinking”

---

## Important

> Agents loop—they don’t just answer

---

## What to say

* “This feels like a junior engineer working step-by-step”

---

---

# 🧩 Session 8 — Agent Teams

---

## Shift

> From one agent → **many specialized agents**

---

## Roles

* Planner
* Developer
* Tester
* Reviewer

---

## Flow

```text
Planner → Dev → Tester → Reviewer → Human
```

---

## Nugget

> “One agent = one responsibility”

---

## Insight

> Coordination is the system

---

## What to say

* “This mirrors how we already work as a team”

---

---

# 🧩 Session 9 — Systems Thinking (Gastown)

---

## Big shift

> From writing code → designing systems of work

---

## Inspired by

* Steve Yegge
* Andrej Karpathy

---

## Key ideas

* validation > generation
* feedback loops
* decomposition

---

## System view

```text
Skills ↔ Agents ↔ Tools ↔ CI ↔ Feedback
```

---

## Nugget

> “You are not writing code—you are orchestrating work”

---

## What to say

* “This is the real transformation”
* “Everything before this was setup”

---

---

# 🔥 Real Example — Össur (THIS IS YOUR KILLER SECTION)

---

## Bitbucket Skill

Enables agent to:

* create PR
* comment on PR
* read pipeline results

---

## B3C Migration Skill

Encodes:

* architecture rules
* migration patterns
* platform knowledge

---

## Combined Flow

```text
Code → PR (Bitbucket skill)
     ↓
CI Pipeline
     ↓
Agent reads results
     ↓
Agent suggests fixes
     ↓
Updates PR
```

---

## Key message

> “The agent is now part of the development lifecycle”

---

## Strong framing

### Without skills

* AI is generic
* no context
* no integration

### With skills

* AI understands B3C
* AI uses Bitbucket
* AI participates in workflows

---

## What to say

* “This is not theoretical—we can already do this”
* “This is where the real value comes from”

---

---

# 🧱 Final Takeaways

---

## The 12 Rules

1. Give the agent a role
2. Add constraints
3. Keep tasks small
4. Ask for process
5. Use CLI
6. Build skills
7. Reuse everything
8. Verify outputs
9. Think in loops
10. Use specialized agents
11. Context matters most
12. Design systems, not prompts

---

## Final statement

> “We are not just using AI—we are extending it with our engineering system”

---

---

# 🚀 Closing

> “In a year, writing firmware without AI will feel like writing C without a compiler.”

---
