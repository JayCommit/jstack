---
name: principle-least-privilege
description: "Apply when granting IAM, Azure RBAC or pipeline access for Azure, AWS, Terraform, GitHub Actions or Azure DevOps. Give each identity only the actions and scope the job needs, including GITHUB_TOKEN permissions and service connection scope."
license: MIT
---

# Least privilege

Each identity receives only the actions and the scope that its job needs. Widen access for a named task and a limited time, then narrow it again.

## Use when

- You add or widen Azure RBAC, AWS IAM or a permission boundary.
- You set `permissions` for `GITHUB_TOKEN` in a workflow.
- You create or share an Azure DevOps service connection, environment or variable group.
- A Terraform plan adds a role assignment or an IAM policy.

## Rules

- Assign Azure roles at the resource or resource group. Prefer a narrow built-in role or a custom role. Keep Owner and User Access Administrator off pipeline identities.
- Write the AWS policy for the API calls this pipeline makes. Leave out `AdministratorAccess` and an `Action` of `*`. Put a permission boundary on roles this pipeline can create.
- Set GitHub Actions `permissions` on the workflow. Start from `contents: read`. A job-level block replaces the workflow block for that job, so repeat every permission it needs. Grant `id-token: write` only on the job that federates. See `principle-no-static-credentials`.
- Scope an Azure DevOps service connection to the resource group or subscription it deploys. Keep a management-group connection off application pipelines. Grant the environment and the variable group to that pipeline only.
- Separate plan and apply identities where the platform allows it. A pull-request plan should not apply production state.
- Give people just-in-time access with Privileged Identity Management or IAM Identity Center, and remove Owner when the task ends.
- Treat a new role assignment in the plan as a production-class change. Review the actions and the data actions.

```yaml
permissions:
  contents: read

jobs:
  plan:
    permissions:
      contents: read
      pull-requests: write
      id-token: write
```

## Red flags

- A workflow sets `permissions: write-all`, or a new workflow sets no `permissions` block.
- A service connection is scoped to a management group for a single resource group.
- Owner or `AdministratorAccess` is added as a temporary grant with no expiry.
- Every repository shares one pipeline identity.
- A copied policy uses a `Resource` of `*` on write actions.

## Done when

- The actions and the scope of each identity are listed and match the job.
- The workflow has an explicit `permissions` block.
- Any wider grant has an expiry or a tracked follow-up to narrow it.
