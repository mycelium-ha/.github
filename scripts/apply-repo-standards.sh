#!/usr/bin/env bash
# Apply the mycelium-ha repository standards to one repository.
#
# Repositories created from the integration template do not inherit settings,
# rulesets or team access, so run this once for every new repository (and again
# whenever the standards change; it is idempotent).
#
#   scripts/apply-repo-standards.sh <repo>
#
# Requires `gh` logged in as an org admin (scopes: repo, admin:org).
#
# What it sets:
# - merge: squash only (PR title/body), delete branch on merge, auto-merge,
#   "update branch"; wiki and projects off
# - private vulnerability reporting on
# - team "maintainers" with the maintain role (needed for CODEOWNERS)
# - ruleset "main": PR required (0 approvals, squash only), no force push or
#   deletion, linear history, required CI checks when the repository has
#   .github/workflows/validate.yml; org admins may bypass
# - ruleset "release tags": only org admins and maintainers create, move or
#   delete v* tags
#
# Org-wide settings (security configuration, allowed actions) are not touched;
# they apply to all repositories automatically.

set -euo pipefail

ORG="mycelium-ha"
TEAM="maintainers"
# App ID of GitHub Actions, so only Actions can satisfy the required checks.
ACTIONS_APP_ID=15368

REPO="${1:-}"
if [[ -z "$REPO" ]]; then
  sed -n '2,25p' "$0" | sed 's/^# \{0,1\}//'
  exit 2
fi
FULL="$ORG/$REPO"

echo "==> $FULL: merge settings"
gh api -X PATCH "repos/$FULL" --silent \
  -F allow_squash_merge=true \
  -F allow_merge_commit=false \
  -F allow_rebase_merge=false \
  -f squash_merge_commit_title=PR_TITLE \
  -f squash_merge_commit_message=PR_BODY \
  -F delete_branch_on_merge=true \
  -F allow_auto_merge=true \
  -F allow_update_branch=true \
  -F has_wiki=false \
  -F has_projects=false

echo "==> $FULL: private vulnerability reporting"
gh api -X PUT "repos/$FULL/private-vulnerability-reporting" --silent

echo "==> $FULL: team $TEAM (maintain)"
gh api -X PUT "orgs/$ORG/teams/$TEAM/repos/$FULL" -f permission=maintain --silent
TEAM_ID=$(gh api "orgs/$ORG/teams/$TEAM" --jq .id)

# Required checks: the job names of the shared ha-validate.yml workflow, called
# as job "validate". "Type check & tests" only when the repository enables it.
CHECKS=()
if VALIDATE=$(gh api "repos/$FULL/contents/.github/workflows/validate.yml" \
  -H "Accept: application/vnd.github.raw" 2>/dev/null); then
  if grep -q "ha-validate.yml" <<<"$VALIDATE"; then
    CHECKS+=(
      "validate / Validate with hassfest"
      "validate / Validate for HA Marketplace (HACS)"
      "validate / Lint & Format (Ruff)"
      "validate / Translation parity"
    )
    if grep -Eq "run_(pytest|mypy): *true" <<<"$VALIDATE"; then
      CHECKS+=("validate / Type check & tests")
    fi
  fi
fi

checks_json() {
  local first=1
  printf '['
  for check in "${CHECKS[@]}"; do
    [[ $first -eq 1 ]] || printf ','
    first=0
    printf '{"context":"%s","integration_id":%d}' "$check" "$ACTIONS_APP_ID"
  done
  printf ']'
}

STATUS_RULE=""
if [[ ${#CHECKS[@]} -gt 0 ]]; then
  STATUS_RULE=$(printf ',{"type":"required_status_checks","parameters":{"strict_required_status_checks_policy":false,"do_not_enforce_on_create":false,"required_status_checks":%s}}' "$(checks_json)")
fi

# Create the ruleset, or update it in place if one with that name exists.
upsert_ruleset() {
  local name="$1" body="$2" id
  id=$(gh api "repos/$FULL/rulesets" --jq ".[] | select(.name == \"$name\") | .id")
  if [[ -n "$id" ]]; then
    gh api -X PUT "repos/$FULL/rulesets/$id" --input - --silent <<<"$body"
    echo "    updated ruleset \"$name\""
  else
    gh api -X POST "repos/$FULL/rulesets" --input - --silent <<<"$body"
    echo "    created ruleset \"$name\""
  fi
}

echo "==> $FULL: ruleset main (${#CHECKS[@]} required checks)"
upsert_ruleset "main" "$(cat <<EOF
{
  "name": "main",
  "target": "branch",
  "enforcement": "active",
  "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
  "bypass_actors": [
    {"actor_id": 1, "actor_type": "OrganizationAdmin", "bypass_mode": "always"}
  ],
  "rules": [
    {"type": "deletion"},
    {"type": "non_fast_forward"},
    {"type": "required_linear_history"},
    {"type": "pull_request", "parameters": {
      "required_approving_review_count": 0,
      "dismiss_stale_reviews_on_push": false,
      "require_code_owner_review": false,
      "require_last_push_approval": false,
      "required_review_thread_resolution": true,
      "allowed_merge_methods": ["squash"]
    }}${STATUS_RULE}
  ]
}
EOF
)"

echo "==> $FULL: ruleset release tags"
upsert_ruleset "release tags" "$(cat <<EOF
{
  "name": "release tags",
  "target": "tag",
  "enforcement": "active",
  "conditions": {"ref_name": {"include": ["refs/tags/v*"], "exclude": []}},
  "bypass_actors": [
    {"actor_id": 1, "actor_type": "OrganizationAdmin", "bypass_mode": "always"},
    {"actor_id": $TEAM_ID, "actor_type": "Team", "bypass_mode": "always"}
  ],
  "rules": [
    {"type": "creation"},
    {"type": "update"},
    {"type": "deletion"}
  ]
}
EOF
)"

for check in "${CHECKS[@]}"; do
  echo "    required: $check"
done
echo "==> $FULL: done"
