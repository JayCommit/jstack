---
name: area-skill-name
description: "Replace this with what the skill does and when to use it. Name the trigger, the cloud area and the outcome. Keep it between 50 and 1024 characters."
license: MIT
---

# Area skill title

## Use when

Use this skill when an agent is about to change this area of Azure, AWS, Terraform or the pipeline that ships it. Say which environments and which repositories it covers.

## Steps

1. Read the plan or pipeline diff and list every destroy, replace and permission change.
2. Use OIDC workload identity, pin provider and action versions, and keep state in a remote backend with locking.
3. Apply least-privilege IAM or RBAC. Use placeholders such as `00000000-0000-0000-0000-000000000000`, `123456789012` and `example.com`.
4. Change one thing at a time and promote it through environments after a check.

## Safety checks

- The blast radius is named: subscription, account, cluster and pipeline.
- Examples use federated identity, pinned versions and a locked remote backend.
- Production has a second person to approve it.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Write the rollback before the change. For Terraform, keep the previous state and a plan that reverses this diff. For a pipeline, keep the previous workflow or release definition. Stop if the rollback depends on a step that has not been tried.

## Done when

- The plan or diff matches the requested change and nothing else.
- The safety checks above have been ticked off.
- The change is verified in the target environment, or it has been stopped with the rollback ready.
