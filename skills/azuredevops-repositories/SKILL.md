---
name: azuredevops-repositories
description: "Use when you create or protect an Azure DevOps Git repository, or you open or review its pull request. Require a reviewer who is not the author, and do not bypass branch policy."
license: MIT
---

# Azure DevOps repositories

New work goes in Git. The default branch has a policy. Pipelines, service connections, and environments stay in the pipeline skills.

## Use when

- You create a repository, or you change branch policy or repository permissions.
- You open or review a pull request.
- Contributors can force-push or bypass policy.
- A production change has no ServiceNow change, and the project also demands an Azure DevOps work item you have not linked.

## Steps

1. Use the organisation and project the user named, such as `https://dev.azure.com/example` and project `example`. Do not invent them. The agent prepares the policy and the pull request, then stops. Follow `principle-stop-at-approval`.

2. Create a Git repository. Do not create a TFVC repository.

   ```bash
   az repos create --name example --organization https://dev.azure.com/example --project example
   ```

3. On the default branch, require at least one reviewer. Use the project's existing minimum when that minimum is higher. Ignore the creator's vote, and reset votes when the source branch moves. Require comment resolution. Add build validation for the pipeline this repository already runs. Follow `pipelines-azure-devops-yaml` for that pipeline. Do not add a second build just to satisfy the policy.

   ```bash
   az repos policy approver-count create --blocking true --branch main --creator-vote-counts false --enabled true --minimum-approver-count 1 --repository-id 00000000-0000-0000-0000-000000000000 --reset-on-source-push true --organization https://dev.azure.com/example --project example
   ```

   Replace the repository id with the id from `az repos show`. Replace `main` when the project uses another default branch.

4. Contributors cannot force-push and cannot bypass policy. The pipeline identity cannot bypass policy. Follow `principle-least-privilege`. Copy the permission namespace from `az devops security permission namespace list`. Do not type a namespace id from memory.

5. Link a ServiceNow change when the change can reach production. Follow `servicenow-changes`. Link an Azure DevOps work item only when this project already requires work-item linking. Do not invent a second tracking system.

6. Open the pull request into the default branch. The description names the check, the rollback, and the ServiceNow number when there is one. The agent does not complete the pull request. A person completes it after policy passes, including the build. Follow `pipelines-github-actions-debugging` only for a GitHub Actions run. An Azure DevOps build failure stays in `pipelines-azure-devops-yaml`.

   ```bash
   az repos pr create --organization https://dev.azure.com/example --project example --repository example --source-branch example-branch --target-branch main --title "Example change" --description "Example change"
   ```

## Safety checks

- The repository is Git, in the named organisation and project.
- The default branch requires a reviewer who is not the author, and votes reset on a new push.
- Build validation uses the pipeline the repository already has.
- Contributors and the pipeline identity cannot bypass policy or force-push.
- A production change names its ServiceNow change. A work item is present only when policy already requires one.
- The pull request is not completed by its author or by the agent.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Revert policy in its own change to the previous required reviewer count and the previous build. Follow `principle-rollback-first`. Completing a revert pull request is the rollback of a bad merge. Do not bypass policy to undo a merge. A change that already deployed follows `ops-rollback-plan`.

## Done when

- The default branch policy matches the checks above, or an existing organisation standard is the one you kept.
- The pull request is open and waiting on a reviewer, or a person has completed it with policy intact.
- Production work names the ServiceNow change.
