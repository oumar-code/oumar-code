#!/usr/bin/env bash
# Run this once with a GitHub PAT that has repo scope:
#   GH_TOKEN=<your-pat> bash .github/scripts/setup-labels.sh

set -e

REPO="oumar-code/oumar-code"

create_label() {
  local name="$1" color="$2" desc="$3"
  gh label create "$name" --color "$color" --description "$desc" -R "$REPO" 2>/dev/null \
    || gh label edit  "$name" --color "$color" --description "$desc" -R "$REPO"
  echo "✅  $name"
}

# Core type labels
create_label "bug"          "d73a4a" "Something isn't working"
create_label "feature"      "0075ca" "New feature or request"
create_label "chore"        "cfd3d7" "Maintenance, refactor, or housekeeping"

# Priority labels
create_label "p0"           "b60205" "P0 — critical / blocks work"
create_label "p1"           "e4e669" "P1 — high priority"
create_label "p2"           "0e8a16" "P2 — nice-to-have"

# Triage
create_label "needs-triage" "fbca04" "Needs review and prioritisation"

echo ""
echo "All labels created/updated on $REPO"
