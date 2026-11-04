---
name: ops-access-review
description: "Use when someone joins, moves, or leaves, or you review who still has standing access on Azure or AWS. Remove what the job no longer needs, and keep break-glass out of daily use."
license: MIT
---

# Access review

Granting a role is `azure-rbac-entra` or `aws-iam-least-privilege`. This skill is the list of who still has access, and the removals. Do not grant a wider role to finish the review.

## Use when

- A person joins, changes role, or leaves.
- You review standing Owner, subscription Contributor, `AdministratorAccess`, or a pipeline admin.
- A break-glass account was used, or it has no named owner.
- An access review is due and the last export is only the active assignments.

## Steps

1. Export active and eligible access before you remove anything. On Azure, `az role assignment list` is the active set. Eligible Privileged Identity Management assignments are a second list. An export of active roles only is an incomplete review. On AWS, review Identity Center permission sets when people sign in that way, and review IAM users when those users still exist. Follow `azure-rbac-entra` or `aws-iam-least-privilege` for the assignment you will change. Follow `aws-organizations-scps` for the ceiling. Do not create an IAM user to replace a permission set.

   ```bash
   az role assignment list --scope /subscriptions/00000000-0000-0000-0000-000000000000 --include-inherited --output json
   ```

2. A leaver loses access the same day. Remove the group membership, the eligible assignment, the active assignment, the federated subject, and any access key. Disabling the sign-in and leaving the role in place is not removal. Record the secret names you rotated. Do not record the values. Follow `ops-secrets-handling`.

3. A mover loses the old scope in the same change that adds the new one. The new grant is the job they have now, scoped as in `azure-rbac-entra` or `aws-iam-least-privilege`. Do not copy a colleague's standing Owner.

4. Standing Owner, User Access Administrator, `AdministratorAccess`, and `IAMFullAccess` for a person become eligible with an end date, or they are removed. Pipeline identities stay federated. Follow `principle-no-static-credentials` and `principle-least-privilege`.

5. Break-glass is two named accounts. They are not used for daily work and not used by a pipeline. Credentials live in the vault. Follow `ops-secrets-handling`. An alert fires when either account signs in. Follow `ops-observability-alerts`. A sign-in is an incident. Follow `ops-incident-response`.

6. Write who was reviewed, what you removed, what you kept and why, and the next review date. The note has no tokens, keys, or passwords. The agent prepares the removals and stops for approval. Follow `principle-stop-at-approval`.

## Safety checks

- The export includes eligible access, not only roles that are active today.
- A leaver has no remaining assignment, group, federated subject, or access key.
- A mover's old scope is in the same change as the new scope.
- People do not keep standing Owner or `AdministratorAccess`. Pipelines are federated.
- Break-glass accounts are named, alerted, and absent from daily jobs.
- The review note has no secret value.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Put back an assignment you removed in error with the same scope and role, as a new reviewed change. Follow `azure-rbac-entra` or `aws-iam-least-privilege`. Do not restore access by granting Owner. A leaver is not restored this way. A wrong leaver removal is a joiner grant for the person who still works here. Follow `principle-rollback-first`.

## Done when

- Every person in the review has a remove, a keep with a reason, or an eligible grant with an end date.
- Leavers have no remaining cloud access from this estate.
- The next review date is written down, and break-glass was not used to do the review.
