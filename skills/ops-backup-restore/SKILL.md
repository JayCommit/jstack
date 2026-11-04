---
name: ops-backup-restore
description: "Use when you protect or restore data on Azure or AWS. Name the recovery point and the restore time, lock the backup vault, and prove a restore on a copy before you delete anything."
license: MIT
---

# Backup and restore

A backup you have never restored is a job that went green. This skill is the recovery you can prove. A Terraform reverse plan is not a restore.

## Use when

- You add a database, a disk, or a volume, and the change names no backup.
- Someone asks to restore, or to delete data, a disk, or a database.
- A production rollback depends on a restore. Follow `ops-rollback-plan` for the change type, and do the restore proof here.
- You are about to lock a backup vault so that retention cannot be shortened.

## Steps

1. Write what you must get back, the oldest recovery point you can accept, and how long the restore may take. Those three sit on the change. A data store with no numbers does not go to production. Follow `principle-change-safety`.

2. Use the backup home the estate already runs. On Azure that is the Recovery Services vault or Backup vault in the platform subscription. Follow `azure-landing-zones`. On AWS that is an AWS Backup vault outside the management account. Follow `aws-organizations-scps`. A cluster volume uses the backup the cluster already runs. Object storage keeps the versioning that landing zone already chose. Do not add a second vault per application. If there is no home, add one, and say so.

3. The policy names the resources, the frequency, and the retention. A cross-region copy is its own decision. Price the retention and the copy. Follow `azure-cost-review` or `aws-cost-review`.

4. The identity that writes recovery points cannot delete the vault. The identity that restores is a different one, eligible for the drill, then removed. Follow `principle-least-privilege` and `azure-rbac-entra` or `aws-iam-least-privilege`.

5. Deny delete on the vault. On Azure, add a CanNotDelete lock. Immutability may be enabled while it is still reversible. Lock it only after a restore has worked, because a locked vault does not unlock. On AWS, leave AWS Backup vault lock in governance mode until a restore has worked. Compliance mode cannot be shortened. Do not turn compliance mode on in the same change as the first backup.

6. Restore to a copy in a non-production subscription or account. List the recovery points, then restore that point with the command for the item type. A virtual machine restores disks into the non-production resource group. A database or a file share uses that item's restore command, still into a copy. Point a non-production app at the copy and read a row you already know. Keep the output. A successful backup job is not this step.

   ```bash
   az backup recoverypoint list --resource-group rg-example --vault-name vault-example --backup-management-type AzureIaasVM --container-name vm-example --item-name vm-example --query [0].name --output tsv
   az backup restore restore-disks --resource-group rg-example --vault-name vault-example --container-name vm-example --item-name vm-example --storage-account stexample --rp-name example --target-resource-group rg-example-restore
   ```

   Replace the names with the vault and the recovery point from the list. `rg-example-restore` is the non-production group. On AWS, list points with `aws backup list-recovery-points-by-backup-vault`, then restore that point with `aws backup start-restore-job` in the non-production account.

7. A delete, a drop, or a destroy of data waits until step 6 has a date and kept output. Follow `ops-rollback-plan`. Do not treat `terraform apply` of the previous code as a restore of rows. A migration that drops a column is that skill's expand-then-contract rule, and the drop still waits on this restore proof.

8. Codify the policy. Follow `principle-everything-as-code` and `terraform-plan-review`. One change. The agent prepares the plan and stops. Follow `principle-stop-at-approval`.

## Safety checks

- The change names the data, the oldest acceptable point, and the restore time.
- The vault is the one the estate already runs, or the change says this is the first home.
- The backup identity cannot delete the vault. The restore identity is removed after the drill.
- A locked immutable vault, or an AWS Backup compliance-mode lock, waits until a restore has worked.
- The drill restored a copy, and the output is kept. A green backup job is not the drill.
- No data delete is in this change unless that drill is already done.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Stop the promotion if the drill fails. That is a successful drill result. Do not unlock an immutable vault and do not shorten a compliance-mode lock. Those are not available. The rollback of a policy you have not locked is to remove that policy assignment. Follow `principle-rollback-first`. A restore that wrote into the wrong account is an incident. Follow `ops-incident-response`. Do not "clean up" by deleting the only good copy.

## Done when

- A non-production restore has been read back, and the output is on the change.
- The vault denies delete, and the locked mode is still the reversible one unless a drill has already succeeded.
- Production data is unchanged, or a delete went ahead only after that proof.
