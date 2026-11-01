---
name: principle-rollback-first
description: "Apply before any production change to Azure, AWS, Terraform, or a GitHub Actions or Azure DevOps pipeline. Write the rollback, rehearse it on a non-production environment and keep it ready before the change starts."
license: MIT
---

# Rollback first

No production change starts until the rollback is written down and has been run on a non-production environment. If that rehearsal fails, the production change waits.

## Use when

- The change will be applied to production.
- Terraform will replace or destroy resources, or a migration will change data.
- A pipeline, slot swap or task definition will move production traffic.
- You are asked to approve a production environment or release.

## Rules

- Record the rollback beside the change: the previous Terraform configuration, the previous container digest or package, and the previous pipeline file.
- Rehearse it on dev or test. A reverse Terraform plan must apply cleanly there. For an app, put the previous revision back and confirm the health check.
- A schema or data migration needs a tested forward fix or a reversible step. Run that path on a copy before a one-way migration reaches production.
- On Azure, decide whether rollback is a slot swap, a redeploy of the previous revision, or a recover of a soft-deleted resource. Soft-delete counts only after you have practised the recover command.
- On AWS, keep the previous task definition, AMI, Lambda version or launch template, and the IAM policy version you can set as default again.
- The pipeline that rolls back must be allowed to run when the new revision is failing. An environment check must not require the broken revision to succeed.
- If the rollback is untested, or only one person knows the steps, stop. Promotion order is covered by `principle-change-safety`.

## Red flags

- The change record says rollback is possible and lists no steps.
- A production Terraform apply has no previous state snapshot and no reverse plan.
- A migration ships with an up script only.
- The rollback workflow depends on the new change succeeding.
- Approval is given before the rehearsal has been run.

## Done when

- Rollback steps are written on the change and name the first command.
- Those steps have succeeded on a non-production environment, or the production change has been stopped.
- The person applying production can run the rollback without inventing it.
