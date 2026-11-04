---
name: github-pull-requests
description: "Use when you open or review a GitHub pull request. Target the default branch, wait for the ruleset and the checks, and stop before you approve or merge your own change."
license: MIT
---

# GitHub pull requests

The pull request is the change. The ruleset on the repository decides when it can merge. Follow `github-repositories` for that ruleset.

## Use when

- You open a pull request, or you review one.
- A check is red and someone wants it merged anyway.
- The author is about to approve their own pull request.
- A change that can reach production has no ServiceNow change number.

## Steps

1. Branch from the default branch. One change. Follow `principle-change-safety`. Do not commit secrets. Follow `ops-secrets-handling`.

2. Open the pull request into the default branch. The body says what changed, how you checked it, and the rollback. If this can reach production, include the ServiceNow change number. Follow `servicenow-changes`. Do not invent that number.

   ```bash
   gh pr create --repo example-org/example --base main --head example-branch --title "Example change" --body-file example.md
   ```

3. Read the checks before anyone merges. A red check is fixed or the pull request stays open. An Actions failure follows `pipelines-github-actions-debugging`. Do not re-run a failed job and call the re-run the fix.

   ```bash
   gh pr checks --repo example-org/example
   ```

4. Reviewers are the code owners from `github-repositories`. The author does not approve. The agent does not approve and does not merge. Follow `principle-stop-at-approval`.

5. A person merges only after the ruleset is satisfied, with the merge method the organisation already uses, and without an admin bypass. The head branch is deleted on merge. A production deploy still waits for the environment approval. Follow `pipelines-environments-approvals`.

   ```bash
   gh pr merge --repo example-org/example --squash --delete-branch
   ```

   Replace `--squash` only when the organisation already requires a different method. Do not add `--admin`.

## Safety checks

- The pull request targets the protected default branch.
- The body names the check you ran and, for production, the ServiceNow change number.
- Required checks are green. A red check is still open.
- The author has not approved the pull request.
- The merge does not use an admin bypass.
- No secret is in the diff, the body, or the chat.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Revert with a new pull request that restores the previous revision. Follow `principle-rollback-first` and `ops-rollback-plan`. Do not force-push the default branch. A bad merge that already deployed uses the rollback in the skill for that change.

## Done when

- The pull request is open with the checks and the rollback written down, and it is waiting on a reviewer who is not the author.
- Or a person has merged it under the ruleset, the head branch is gone, and production has not moved without its approval.
