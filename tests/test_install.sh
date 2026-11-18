#!/usr/bin/env bash
# Exercise installation from a source archive and update in an isolated project.
set -euo pipefail

test_dir="$(mktemp -d)"
trap 'rm -rf "$test_dir"' EXIT
mkdir -p "$test_dir/src" "$test_dir/project with spaces"
cp -R scripts references AGENTS.md SKILL.md "$test_dir/src/"
source_dir="$test_dir/src"
project="$test_dir/project with spaces"
dest="$project/.agents/skills/shortdrama-producer"

/bin/bash install.sh --target repo --repo "$project" --from-local "$source_dir"
test -f "$dest/SKILL.md"
python3 "$dest/scripts/seedance_search.py" "rain at night" 1 | python3 -c 'import json, sys; assert json.load(sys.stdin)["hits"]'

printf 'updated\n' > "$source_dir/version-marker"
/bin/bash install.sh --target repo --repo "$project" --from-local "$source_dir" --update
cmp "$source_dir/version-marker" "$dest/version-marker"
test -f "$(find "$project/.agents/skill-backups" -name SKILL.md -print)"
