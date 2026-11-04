---
name: terraform-drift
description: "Detect and reconcile Terraform drift on Azure and AWS. Use when a scheduled plan exits with changes you did not ship, or Activity Log or CloudTrail shows a change made outside the code."
license: MIT
---

# Drift

A scheduled plan detects drift. It does not apply. Reconcile only after you can name who changed the live resource.

## Use when

- A scheduled `terraform plan` reports changes nobody shipped in this commit.
- Azure Activity Log or AWS CloudTrail shows a write you did not plan.
- Someone wants a job that applies whenever the plan is not empty.
- A console edit has to be imported or reverted.

## Steps

1. Run the check on a schedule from the default branch. Use the plan identity, not the apply identity. See `principle-least-privilege`. Authenticate with OIDC or workload identity federation. See `principle-no-static-credentials`.
2. Plan with a lock and a detailed exit code. Save the plan as an artifact. Do not apply it in this job. Pin the reviewed Terraform release, such as `1.10.5`.

   ```text
   terraform plan -input=false -lock-timeout=5m -detailed-exitcode -out=tfplan
   ```

   Exit 0 means the code and the live resources match. Exit 2 means drift or a change that was never applied. Exit 1 means the plan failed. An error is not drift. Fix the error before you triage a diff. In PowerShell, read `$LASTEXITCODE`.

3. On exit 2, read the plan before you edit code. Record the resource address, the action and the attributes that differ.

   ```text
   terraform show -no-color tfplan
   ```

4. Read the control-plane log before you change Terraform. On Azure, open Activity Log for that subscription and resource. On AWS, open CloudTrail for that account and event name. Note the caller: a pipeline role, a person, or a principal you do not recognise. See `principle-observe-before-you-fix`.
5. Pick one path. Do not mix them in one change. See `principle-change-safety`. State stays in the locked remote backend for that environment.
6. Update the code when the live change was deliberate and should remain. The next plan is empty because the code matches, not because you applied a surprise diff. Follow `principle-everything-as-code`.
7. Import when the resource exists and is not in state. Add an `import` block, plan, and review that plan on its own. A one-off `terraform import` with no block in git is not done.
8. Revert the live change when it was a mistake or it was not authorised. Put the resource back by hand or with a reviewed rollback plan. Confirm with a new plan that exits 0. Do not apply the drift plan just to make it empty. That writes an unreviewed change into the desired state.
9. Do not run `terraform apply`, `terraform apply -refresh-only` or `-auto-approve` from the schedule. Refresh-only copies live values into state and hides the drift.
10. If the diff adds spend you did not plan, price it before you accept a code update. See `principle-cost-awareness`. A production revert follows `principle-rollback-first`.
11. Assign the exit 2 result the same day. Keep the plan artifact and the log line that names the caller. A green rerun is not triage. Provider pins stay on the reviewed release, such as `hashicorp/azurerm` `4.14.0` and `hashicorp/aws` `5.84.0`.
12. Run one scheduled pipeline per environment from the default branch. Serialize it on the state key so it does not take the lock from an apply. See `principle-idempotent-automation`.
13. Write this note before you edit code. A note that only says "drift" is not triage.

    ```text
    resource: azurerm_resource_group.this
    caller: principal from Activity Log or CloudTrail
    path: update code, import, or revert live
    ```

14. Do not clear a diff with `ignore_changes` unless that attribute is known to churn. Record the attribute, the reason and an expiry on the pull request. Do not ignore a security group, a route or a role assignment.
15. Codify a console create with an `import` block in its own change. Plan it alone. Do not mix it with an unrelated edit.

    ```hcl
    import {
      to = azurerm_resource_group.this
      id = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-example"
    }
    ```

16. If exit 2 repeats for the same address after you reconciled, read the log again before you edit the code a second time. See `principle-observe-before-you-fix`.

## Safety checks

- The scheduled job can plan and cannot apply. Its identity is federated and is not Owner or `AdministratorAccess`.
- Exit 1 is fixed as a failure. Exit 2 is a tracked review, not an automatic apply.
- Activity Log or CloudTrail was read before the code changed.
- The job uses the locked backend for that one state key and does not apply.
- The reconcile change is one path: a code update, an import or a live revert.
- The triage note names the resource, the caller and the path.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

If a reconcile apply made the wrong object the desired state, roll back from the previous configuration and the versioned state snapshot. Follow `principle-rollback-first`. Restore the previous blob or object version if state itself moved, then plan. Do not force-unlock a drift job that is still running.

## Done when

- The schedule records exit 0, or exit 2 has an owner and one chosen path.
- That path is in git as a code change or an `import` block, or the live mistake was reverted.
- A later scheduled plan exits 0 for that state key.
- No apply ran only to make a plan empty.
