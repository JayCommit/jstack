---
name: ops-rollback-plan
description: "Use when a change can reach production. Write the rollback for that change type, Terraform, deploy, migration, network, or IAM, and rehearse it before the change starts."
license: MIT
---

# Rollback plan

`principle-rollback-first` says to write the rollback and rehearse it. This skill is the procedure for each change type. Production waits until the rehearsal has worked.

## Use when

- A Terraform apply, an app deploy, a database migration, a network change, or an IAM change can reach production.
- The change record says rollback is possible and names no command.
- A migration ships with an up script only.
- The rollback pipeline can run only when the new revision is healthy.

## Steps

1. Name the change type. Write the first rollback command on the change. Rehearse that command on dev or test and keep the output. Follow `principle-rollback-first`. If the rehearsal fails, do not promote.

2. Terraform. Roll back with the previous configuration and a plan that reverses this diff. Save that plan and apply that file. Follow `terraform-plan-review`. State stays in the remote backend. Follow `terraform-state-backends`. A resource rollback is a reverse plan. Restoring a state snapshot is a state recovery, and it follows that skill. It is not the default rollback. Re-applying does not bring back data a destroy deleted. For a data store, the rollback is a restore you have already practised, or you do not apply.

3. App deploy. Deploy the previous digest. Follow `pipelines-artifacts-releases`. Do not rebuild an old tag. For Helm, roll back to the revision you recorded. Follow `k8s-helm-review`. For Argo CD or Flux, revert the overlay commit and let the controller sync. Follow `gitops-argocd-flux`. For ECS, deploy the previous task definition. Follow `aws-ecs`.

4. Database migration. Expand, then contract. Add the new column or table so the current app still works. Deploy the app that writes both shapes. Backfill. Deploy the app that reads the new shape. Drop the old shape in a later change. Before the drop, rollback is the previous app digest. After the drop, rollback is a restore of a backup you have already restored on a copy. Do not ship the drop in the same change as the first deploy. Do not ship an up script with no tested forward fix.

5. Network. Export the current routes, NSG rules, security group rules, or DNS records before you change them. The rollback is that export applied again. Follow `azure-networking` or `aws-vpc`.

   ```bash
   az network nsg rule list --nsg-name nsg-example --resource-group rg-example --output json
   aws ec2 describe-security-groups --group-ids sg-example --region eu-west-2
   ```

   Do not delete a peering or a route table as the first rollback step. Prove name resolution after a private DNS rollback.

6. IAM. The rollback of an assignment you added is deleting that assignment. Follow `azure-rbac-entra`. The rollback of a customer managed AWS policy is setting the previous version as the default. An inline policy has no versions. Put the previous document back. Follow `aws-iam-least-privilege`. Do not detach a policy another role still uses.

   ```bash
   az role assignment delete --ids /subscriptions/00000000-0000-0000-0000-000000000000/providers/Microsoft.Authorization/roleAssignments/00000000-0000-0000-0000-000000000000
   aws iam set-default-policy-version --policy-arn arn:aws:iam::123456789012:policy/example --version-id v2
   ```

   Replace the role assignment id with the assignment you added. Replace `v2` with the version `aws iam list-policy-versions` showed you before the change.

7. The pipeline that rolls back must be allowed to run while the new revision is failing. An approval gate must not require the broken revision to pass its health check. Follow `pipelines-environments-approvals`.

8. Name what this rollback cannot undo: deleted rows, a dropped column, a purged secret, a control plane that does not downgrade. If that list is the whole change, do not start production.

## Safety checks

- The change record names the type and the first command.
- That command has been run on dev or test, and the output is kept.
- Terraform rollback is a reverse plan. A state restore is called out as recovery.
- An app rollback uses the previous digest or task definition, not a rebuild of a tag.
- A migration does not drop the old shape in the same change as the first deploy.
- Network rollback applies the export you took. It does not start by deleting the peering.
- IAM rollback removes the grant you added or restores the previous policy version.
- The rollback pipeline runs when the new revision is unhealthy.

## Rollback

If the rehearsal itself fails, stop the promotion. That is the result you wanted from the rehearsal. If a production rollback makes the impact worse, undo that rollback step before you try a third change, and say so on the incident timeline. Follow `ops-incident-response`. A one-way migration uses the forward fix you tested on a copy. Do not invent one during the incident.

## Done when

- The first rollback command is on the change, and it has succeeded off production.
- The notes say what the command cannot restore.
- Production has not started, or the rehearsed command is the one the pipeline will run.
