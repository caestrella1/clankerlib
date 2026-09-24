#!/usr/bin/env bash
# Copy skills from this library into an agent's skills directory.
#
# Usage:
#   scripts/install.sh --dest DIR [--symlink] <skill>... | --all
#   scripts/install.sh --list
#
# DIR is wherever your agent discovers skills; see its documentation.
set -euo pipefail

LIB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$LIB_ROOT/skills"
DEST=""
MODE="copy"
SKILLS=()

usage() {
  sed -n '2,8p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

list_skills() {
  for dir in "$SKILLS_DIR"/*/; do
    name="$(basename "$dir")"
    [[ "$name" == _* ]] && continue
    echo "$name"
  done
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dest) DEST="${2:?--dest needs a directory}"; shift 2 ;;
    --symlink) MODE="symlink"; shift ;;
    --all) mapfile -t SKILLS < <(list_skills); shift ;;
    --list) list_skills; exit 0 ;;
    -h|--help) usage; exit 0 ;;
    -*) echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
    *) SKILLS+=("$1"); shift ;;
  esac
done

if [[ -z "$DEST" || ${#SKILLS[@]} -eq 0 ]]; then
  usage >&2
  exit 1
fi

for skill in "${SKILLS[@]}"; do
  if [[ ! -f "$SKILLS_DIR/$skill/SKILL.md" ]]; then
    echo "Skill not found: $skill (run with --list)" >&2
    exit 1
  fi
done

mkdir -p "$DEST"
for skill in "${SKILLS[@]}"; do
  src="$SKILLS_DIR/$skill"
  target="$DEST/$skill"
  rm -rf "$target"
  if [[ "$MODE" == "symlink" ]]; then
    ln -s "$src" "$target"
  else
    cp -R "$src" "$target"
  fi
  echo "Installed $skill -> $target ($MODE)"
done
