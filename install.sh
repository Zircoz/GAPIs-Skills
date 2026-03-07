#!/usr/bin/env bash
set -e

SKILLS_DIR="${HOME}/.claude/skills"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_SRC="${REPO_DIR}/skills"

usage() {
  echo "Usage: $0 [--all] [--skill <skill-name>]"
  echo ""
  echo "Options:"
  echo "  --all              Install all skills"
  echo "  --skill <name>     Install a specific skill (can be repeated)"
  echo "  --list             List available skills"
  echo "  --help             Show this help"
  echo ""
  echo "Available skills:"
  for d in "${SKILLS_SRC}"/*/; do
    echo "  - $(basename "$d")"
  done
}

install_skill() {
  local name="$1"
  local src="${SKILLS_SRC}/${name}"
  local dest="${SKILLS_DIR}/${name}"

  if [ ! -d "$src" ]; then
    echo "Error: skill '${name}' not found in ${SKILLS_SRC}"
    exit 1
  fi

  mkdir -p "${SKILLS_DIR}"

  if [ -d "$dest" ]; then
    echo "Updating ${name}..."
    rm -rf "$dest"
  else
    echo "Installing ${name}..."
  fi

  cp -r "$src" "$dest"
  echo "  -> ${dest}"
}

if [ $# -eq 0 ]; then
  usage
  exit 0
fi

INSTALL_ALL=false
SKILLS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all)
      INSTALL_ALL=true
      shift
      ;;
    --skill)
      SKILLS+=("$2")
      shift 2
      ;;
    --list)
      echo "Available skills:"
      for d in "${SKILLS_SRC}"/*/; do
        echo "  - $(basename "$d")"
      done
      exit 0
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      usage
      exit 1
      ;;
  esac
done

if $INSTALL_ALL; then
  for d in "${SKILLS_SRC}"/*/; do
    install_skill "$(basename "$d")"
  done
elif [ ${#SKILLS[@]} -gt 0 ]; then
  for name in "${SKILLS[@]}"; do
    install_skill "$name"
  done
else
  usage
  exit 0
fi

echo ""
echo "Done. Restart Claude Code to activate installed skills."
