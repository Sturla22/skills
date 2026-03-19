#!/usr/bin/env bash
# Link personal skills into ~/.claude/skills/ alongside Anthropic's skills.
# Run after cloning or adding a new skill.

set -euo pipefail

SKILLS_DIR="$HOME/.claude/skills"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

for skill in "$SCRIPT_DIR"/*/; do
  name="$(basename "$skill")"
  target="$SKILLS_DIR/$name"
  if [ -L "$target" ]; then
    # Re-link if it already points somewhere
    rm "$target"
  elif [ -e "$target" ]; then
    echo "skip: $name (exists and is not a symlink)"
    continue
  fi
  ln -s "$skill" "$target"
  echo "linked: $name"
done
