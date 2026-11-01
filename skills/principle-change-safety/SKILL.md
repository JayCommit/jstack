---
name: principle-change-safety
description: "Apply before any change to Azure or AWS infrastructure, Terraform, or a GitHub Actions or Azure DevOps pipeline. Read the plan, name the blast radius, make one change at a time and promote it through environments."
license: MIT
---

# Change safety

Read the plan and name what it can break before you change Azure, AWS, Terraform or a pipeline. Ship one change at a time, and promote it only after the previous environment checks out.

## Use when

- You are about to plan or apply Terraform against Azure or AWS.
- You are editing a GitHub Actions workflow or an Azure DevOps pipeline that deploys infrastructure.
- You are changing IAM, RBAC, routes, state or a production setting.
- A plan shows a destroy, a replace or a permission change.

## Rules

- Read the whole `terraform plan` or pipeline diff before you approve it. List every destroy, replace, IAM or RBAC grant, and network change.
- `terraform plan -detailed-exitcode` exits 0 when nothing changes, 2 when the plan contains changes, and 1 when the plan fails. Review exit 2. Fix exit 1 before you continue.
- Save the reviewed plan with `terraform plan -out=tfplan` and apply that file. A later apply without the file can ship a different diff.
- Name the blast radius on the pull request: subscription or account, region, resource group or VPC, state key, pipeline and environment, plus anything else that shares that state or network.
- Keep one logical change in each pull request and each apply. Split unrelated identity, network and compute edits.
- Promote from dev to test, then to production. Production needs a second person to approve it. Check the lower environment before you promote.
- Give a pipeline edit the same path. Review the workflow diff and run it on a pull request or a non-production environment first.
- Write the rollback before production. Follow `principle-rollback-first`.

## Red flags

- An apply runs without a saved plan, or from a branch nobody reviewed.
- The plan destroys or replaces resources and the pull request does not say so.
- One change mixes identity, networking and application resources.
- Production is edited while dev and test still run the old code.
- The blast radius is called small, and no subscription, account or state key is named.

## Done when

- The reviewed plan or diff matches the request and nothing else.
- The blast radius is written on the change.
- The change is verified in this environment before anyone promotes it.
