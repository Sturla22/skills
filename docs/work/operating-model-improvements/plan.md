# Plan: Operating Model Improvements

**Work ID:** operating-model-improvements  
**Planner:** product-owner (trivial enough to skip separate planner delegation)  
**TDD:** Not applicable — documentation and skill files. Verification is `cli.py sync --check` + manual review.

---

## Sequencing

Changes are independent. Group into two commits for clean attribution:

**Commit A — New skills (additive, no risk)**
- Step 1: `story-loop` skill
- Step 2: `grill-me` skill
- Step 3: `write-a-brief` skill

**Commit B — Model edits (targeted changes to existing files)**
- Step 4: Research skill durability backport
- Step 5: AGENTS.md — "why roles" + three-tier skill model
- Step 6: operating-model.md — context engineering section + agent failure note
- Step 7: workflow-evolution skill — autoresearch + AI-friendly code

**Commit C — Release**
- Step 8: CHANGELOG.md update + sync check

---

## Step Detail

### Step 1: `story-loop` skill
**File:** `.agents/skills/story-loop/SKILL.md`  
**Description:** Concrete Ralph-style loop. Pick next story → implement → run checks → commit on green → repeat. References `bounded-autonomy-loop` as the safety contract.  
**Done-when:** File exists with correct frontmatter, process matches Ralph pattern, explicitly states it is an instantiation of bounded-autonomy-loop.

### Step 2: `grill-me` skill
**File:** `.agents/skills/grill-me/SKILL.md`  
**Description:** Structured interrogation of a brief or plan. Traverse decision tree branch by branch. One probing question at a time. Supply recommended answer. Read codebase instead of asking when possible. Usable by product-owner (brief interrogation) and planner (plan stress-test).  
**Done-when:** File exists, trigger conditions are explicit, process covers the branch-by-branch pattern, codebase-read shortcut is specified.

### Step 3: `write-a-brief` skill
**File:** `.agents/skills/write-a-brief/SKILL.md`  
**Description:** Guided brief-writing interview. Modelled on Pocock's write-a-prd but targeting our `brief.md` format: problem discovery, codebase analysis, requirements interview, acceptance criteria synthesis. Optional for small tasks, recommended for medium/large.  
**Done-when:** File exists, 4-step process defined, outputs a complete `brief.md` in our template format.

### Step 4: Research skill durability backport
**File:** `.agents/skills/research/SKILL.md`  
**Change:** Add as step 1 (before current step 1): "Write partial findings early — write to the output file within the first 3 tool uses. Refine incrementally. If turns exhaust, the file should already contain the most valuable findings so far."  
**Done-when:** Step exists as the first numbered step in the process.

### Step 5: AGENTS.md targeted edits
**Two insertions:**
1. Before the role definitions: 2-3 sentence "why roles" rationale (focused roles, no conflicting objectives, explicit handoffs)
2. In the skills section or a new "Skills tiers" subsection: three-tier model (canonical `.agents/`, team-installed, personal/gitignored)  
**Done-when:** Both passages present, no existing content removed or restructured.

### Step 6: operating-model.md edits
**Two insertions:**
1. New "Context engineering" section: name the principle, describe the three layers (project rules → skills → work packets), point to the concrete files (CLAUDE.md, AGENTS.md, .agents/skills/)
2. New "Agent failure notes" convention: one paragraph, three fields (expected / happened / guardrail), lives in docs/workflow-experiments/, reviewed by workflow-architect  
**Done-when:** Both sections present and self-contained.

### Step 7: workflow-evolution skill edits
**File:** `.agents/skills/workflow-evolution/SKILL.md`  
**Two additions:**
1. Under guardrails or a new "optimization loops" note: Karpathy autoresearch pattern — for performance/memory work, consider an autonomous experiment loop (measurable objective + narrow write surface + auto-check + fixed budget)
2. Under the "when workflow change stalls" section or a new note: AI-friendly code structure (clear naming, discriminating test names, explicit invariants in comments) is a legitimate hypothesis to test under the existing experiment framework  
**Done-when:** Both notes present without disrupting existing content.

### Step 8: CHANGELOG + sync check
- Add entries under `Unreleased` for each new skill (Added) and each model edit (Changed)
- Run `python3 tools/cli.py sync` to generate .claude/skills entries for new skills
- Run `python3 tools/cli.py sync --check` — must exit 0  
**Done-when:** CHANGELOG updated, sync passes.

---

## Verification

- `python3 tools/cli.py sync --check` exits 0
- All new SKILL.md files have valid frontmatter (name, description, allowed-tools)
- AGENTS.md and operating-model.md changes reviewed for coherence
- No existing skill, role, or template removed or structurally changed

---

## Residual Risk

Low. All changes are additive or targeted insertions. No existing behaviour is removed. The only risk is incoherence (a new skill that contradicts an existing one) — mitigated by the review step.
