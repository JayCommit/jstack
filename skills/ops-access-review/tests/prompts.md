# Prompts for ops-access-review

Example asks for `ops-access-review`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

A person joins, changes role, or leaves.

### Expected for ask 1

- Load `ops-access-review` and follow that file through its own done-when.
- Step: Export active and eligible access before you remove anything. On Azure, `az role assignment list` is the active set. Eligible Privileged Identity Management assignments are a second list. An export of active roles only is an incomplete review. On AWS, review Identity Center permission sets when people sign in that way, and review IAM users when those users still exist. Follow `azure-rbac-entra` or `aws-iam-least-privilege` for the assignment you will change. Follow `aws-organizations-scps` for the ceiling. Do not create an IAM user to replace a permission set.
- Check: The export includes eligible access, not only roles that are active today.
- Done when: Every person in the review has a remove, a keep with a reason, or an eligible grant with an end date.

## Ask 2

A leaver loses access the same day.

### Expected for ask 2

- Load `ops-access-review` and follow that file through its own done-when.
- Step: A leaver loses access the same day. Remove the group membership, the eligible assignment, the active assignment, the federated subject, and any access key. Disabling the sign-in and leaving the role in place is not removal. Record the secret names you rotated. Do not record the values. Follow `ops-secrets-handling`.
- Check: A leaver has no remaining assignment, group, federated subject, or access key.
- Done when: Leavers have no remaining cloud access from this estate.
