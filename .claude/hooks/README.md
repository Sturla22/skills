# Claude Hooks

These project hooks are enabled from [settings.json](/home/sturlalange/Dev/my-claude-skills/.claude/settings.json).

They are intentionally lightweight starter hooks:

- `user_prompt_submit.py`
  nudges non-trivial requests back toward `product-owner`, work packets, planner-owned parallelism, and Claude-native runtime files when relevant
- `instructions_loaded_log.py`
  records instruction-load events under `.claude/logs/` for debugging which rules were active
- `precompact_context.py`
  reminds Claude to preserve work-packet pointers, current owner, lane, worktree, risks, and next action across compaction
- `subagent_stop_guard.py`
  blocks once when a subagent stop message looks too thin to serve as a useful worker handoff
- `stop_guard.py`
  blocks once when the main stop message claims completion without enough verification, residual-risk, or durable-artifact context

These are safe starters, not sacred policy. Teams can tighten, relax, or remove them as usage data accumulates.
