#!/usr/bin/env bash
# install.sh — Install / update the shortdrama-producer agent for any terminal.
#
# Targets (2026 cross-terminal convention):
#   codex     -> $HOME/.agents/skills/shortdrama-producer        (OpenAI Codex, USER scope)
#   claude    -> $HOME/.claude/skills/shortdrama-producer        (Claude Code)
#   workbuddy -> $HOME/.workbuddy/skills/shortdrama-producer     (WorkBuddy)
#   repo      -> <dir>/.agents/skills/shortdrama-producer        (any AGENTS.md-based terminal:
#               Cursor / Windsurf / Gemini CLI / GitHub Copilot)
#
# Usage:
#   ./install.sh                          # install to all detected targets
#   ./install.sh --target codex           # install to one target
#   ./install.sh --update                 # git-pull update existing installs
#   ./install.sh --target repo --repo ~/myproject   # repo-scoped install
#   ./install.sh --from-local <dir>       # copy from local dir instead of git clone
#
# No dependencies beyond bash, git, and (for clone) network access.

set -euo pipefail

NAME="shortdrama-producer"
REPO_URL="https://github.com/Eleven1111/shortdrama-producer-agent.git"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

TARGETS=""
UPDATE=0
FROM_LOCAL=""
REPO_DIR=""

usage() {
  sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGETS="$2"; shift 2 ;;
    --update) UPDATE=1; shift ;;
    --from-local) FROM_LOCAL="$2"; shift 2 ;;
    --repo) REPO_DIR="$2"; shift 2 ;;
    --help|-h) usage ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

# Resolve target list ---------------------------------------------------------
declare -A DEST
detect() {
  if [[ -n "$TARGETS" ]]; then
    IFS=',' read -ra arr <<< "$TARGETS"
    for t in "${arr[@]}"; do DEST["$t"]=""; done
    return
  fi
  # Auto-detect: install only where a matching host exists
  [[ -d "$HOME/.agents" || -x "$(command -v codex)" ]] && DEST[codex]=""
  [[ -d "$HOME/.claude" || -x "$(command -v claude)" ]] && DEST[claude]=""
  [[ -d "$HOME/.workbuddy" ]] && DEST[workbuddy]=""
  if [[ ${#DEST[@]} -eq 0 ]]; then
    echo "⚠️  No supported terminal detected. Use --target (codex|claude|workbuddy|repo)."
    exit 1
  fi
}
detect

dest_path() {
  case "$1" in
    codex)     echo "$HOME/.agents/skills/$NAME" ;;
    claude)    echo "$HOME/.claude/skills/$NAME" ;;
    workbuddy) echo "$HOME/.workbuddy/skills/$NAME" ;;
    repo)      echo "${REPO_DIR:-$PWD}/.agents/skills/$NAME" ;;
    *) echo "Unknown target: $1" >&2; exit 1 ;;
  esac
}

# Install / update one target -------------------------------------------------
install_one() {
  local t="$1" dest; dest="$(dest_path "$t")"
  echo "==> [$t] -> $dest"

  if [[ "$UPDATE" -eq 1 && -d "$dest" ]]; then
    if [[ -d "$dest/.git" ]]; then
      git -C "$dest" pull --ff-only
      echo "    ✅ updated (git pull)"
      return
    fi
    # Installs made with --from-local have no .git, so a plain `git pull` update is
    # impossible — without this branch they could never be updated at all, only
    # deleted by hand. Re-sync from source instead, keeping one backup.
    local src="$FROM_LOCAL"
    if [[ -z "$src" ]]; then
      src="$(mktemp -d)/src"
      git clone --depth 1 "$REPO_URL" "$src" >/dev/null 2>&1 || {
        echo "    ⚠️  no .git and clone failed; re-run with --from-local <dir>"; return; }
    fi
    local bak="$dest.bak.$(date +%Y%m%d%H%M%S)"
    mv "$dest" "$bak"
    cp -R "$src" "$dest"
    echo "    ✅ updated (re-synced; previous copy kept at $bak)"
    return
  fi

  mkdir -p "$(dirname "$dest")"
  if [[ -d "$dest" ]]; then
    echo "    ⚠️  exists ($dest). Use --update to refresh it, or remove it first."
    return
  fi

  if [[ -n "$FROM_LOCAL" ]]; then
    cp -R "$FROM_LOCAL" "$dest"
    echo "    ✅ installed from local copy"
  else
    git clone --depth 1 "$REPO_URL" "$dest"
    echo "    ✅ installed (git clone)"
  fi
}

for t in "${!DEST[@]}"; do
  install_one "$t"
done

echo ""
echo "Done. Restart your terminal/agent so the skill is discovered."
echo "For AGENTS.md-only terminals (Cursor / Windsurf / Gemini CLI / Copilot):"
echo "  ./install.sh --target repo --repo /path/to/your/project"

# Retrieval needs python3. The agent degrades gracefully without it (SKILL.md Step 2),
# but it loses its main differentiator — so say this plainly instead of failing silently
# the first time someone asks for a video.
echo ""
if command -v python3 >/dev/null 2>&1; then
  echo "✅ python3 found — retrieval over 7,824 real production prompts is enabled."
else
  echo "⚠️  python3 NOT found."
  echo "    The agent still works, but skips Step 2 (retrieval of real production"
  echo "    examples) — that is its main advantage over a generic prompt tool."
  echo "    macOS:  brew install python3     Ubuntu: sudo apt install python3"
fi

echo ""
echo "Try it — just describe an idea in plain words, no options to learn:"
echo "    \"雨夜，一个女孩在便利店门口等人\""
echo "    \"make me a funny video\"        (it will offer you 3 directions)"
