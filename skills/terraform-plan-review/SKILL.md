---
name: terraform-plan-review
description: "Review a Terraform plan before any Azure or AWS apply. Use when a pull request changes infrastructure: read the full plan, flag destroys and grants, name the blast radius, and apply only a saved plan file."
license: MIT
---

# Plan review

Read the whole plan. Apply that saved file and nothing else.

## Use when

- You are about to run `terraform apply` for Azure or AWS.
- A pull request changes Terraform, tfvars or `.terraform.lock.hcl`.
- A plan can destroy, replace, grant access or change a network.

## Steps

1. Authenticate with OIDC or workload identity federation. Do not export a static access key, a storage account key or a client secret. See `principle-no-static-credentials`.
2. Init the remote backend for this environment. Locking must be on. A plan that cannot lock is not ready to review.
3. Write a saved plan. In PowerShell, read `$LASTEXITCODE` after the command. Do not treat exit 2 as a crash.

```text
terraform plan -input=false -lock-timeout=5m -detailed-exitcode -out=tfplan
```

Exit 0 means no changes. Exit 2 means the plan has changes. Exit 1 means the plan failed. Fix exit 1 before anyone reviews. Do not review a partial plan.

4. Read the full plan, not the summary line. Search the text for destroys, replacements, grants and network edits.

```text
terraform show -no-color tfplan
```

5. Flag every destroy and every `forces replacement`. A `-/+` line is a destroy plus a create. Name the resource address and the attribute that forced it.
6. Flag IAM and RBAC. Include `azurerm_role_assignment`, `aws_iam_policy`, `aws_iam_role_policy_attachment` and any change to a policy document. The actions and the scope must match the job. See `principle-least-privilege`.
7. Flag network changes. Subnets, routes, network security groups, security groups, network ACLs and firewall rules all count. Name the virtual network or VPC and the environment.
8. Flag `moved` and `import` blocks. A move must not show a destroy of the old address. An import must not show an unexpected update after the import. If it does, stop and fix the code before apply.
9. Diff `.terraform.lock.hcl`. A provider or module version bump is part of this review even when the resource diff is empty.

```text
git diff -- .terraform.lock.hcl
```

The lock must match the pins that were reviewed, such as Terraform `1.10.5`, `hashicorp/azurerm` `4.14.0` and `hashicorp/aws` `5.84.0`.

10. Name the blast radius on the pull request: subscription or account, region, resource group or VPC, state key and environment. See `principle-change-safety`. If the plan adds spend, price it. See `principle-cost-awareness`.
11. Apply only the saved file, and only after that review. A later plan can differ from the one you read.

```text
terraform apply -input=false tfplan
```

Do not run `terraform apply` with no plan file. Do not apply a plan you have not read.

12. Plan again after a successful apply. A stable change exits 0 on that second plan. See `principle-idempotent-automation`. If it still shows changes, stop and fix the configuration before you call the apply done.
13. Reject `terraform apply -auto-approve` and an apply from a branch nobody reviewed. A `-target` plan hides every resource outside that address. Accept a target only when the pull request names it and says what the next full plan must still show.
14. Write the review on the pull request before apply. List each destroy, replacement, grant, network edit, move, import and lockfile bump. If the request was a tag and the plan replaces a database, stop.
15. Treat a replace line as a stop until you can name the attribute. Search the plan for this shape.

```text
# azurerm_linux_virtual_machine.this must be replaced
-/+ resource "azurerm_linux_virtual_machine" "this" {
```

16. Read the provider version in the plan header. If it does not match the pin in the pull request, stop. Do not run `terraform init -upgrade` during the review. That rewrites `.terraform.lock.hcl` under you.

## Safety checks

- The file passed to `terraform apply` is the file that was reviewed.
- Destroys, replacements, grants, network edits, moves, imports and lockfile bumps are listed, or the plan has none.
- The identity is federated. It is not Owner and it is not `AdministratorAccess`. See `principle-least-privilege`.
- Production has a second approver. Promotion order follows `principle-change-safety`.
- The plan file is not committed. It can hold values that must stay out of git.

## Rollback

Write the reverse change before apply. Follow `principle-rollback-first`. Keep the previous configuration and a versioned state snapshot. Rollback is a new saved plan from that configuration, not an unreviewed apply. If you cannot describe the reverse plan, do not apply.

## Done when

- Exit 0 is recorded, or exit 2 was reviewed and that saved plan was applied.
- The blast radius is written on the change.
- No apply used an unreviewed plan.
- A follow-up plan exits 0, or the change is stopped with the rollback ready.
