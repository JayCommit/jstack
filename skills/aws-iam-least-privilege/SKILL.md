---
name: aws-iam-least-privilege
description: "Use when you add or widen an IAM policy, role or permission boundary. Write the API calls the job makes, validate the policy, and keep AdministratorAccess off pipelines and people."
license: MIT
---

# IAM least privilege

Grant the API calls the job makes, on the resources it uses. A wider policy is a production change.

## Use when

- You add or change an IAM policy, role, permission boundary or resource policy.
- A pipeline, a pod or a task needs to call AWS.
- Someone proposes `AdministratorAccess`, `PowerUserAccess`, `IAMFullAccess` or an `Action` of `*`.
- Access Analyzer reports external access or unused access.

## Steps

1. List the API calls and the resource ARNs. Include `kms:Decrypt` when the job reads a secret. Follow `principle-least-privilege`. A copied policy from another account is not that list.

2. Give people access through IAM Identity Center. Give a pipeline or a workload a role it assumes. Do not create an access key for a person or a pipeline. Follow `principle-no-static-credentials`.

3. Write the identity policy with those actions and those ARNs. A write action needs an ARN, not `Resource: "*"`. A permission boundary is the ceiling for roles this pipeline can create. Attach it to those roles.

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "WriteAppPrefix",
         "Effect": "Allow",
         "Action": ["s3:GetObject", "s3:PutObject"],
         "Resource": "arn:aws:s3:::example-bucket/app/*"
       }
     ]
   }
   ```

4. On any statement that allows `iam:CreateRole` or `iam:AttachRolePolicy`, require the boundary. The object below is one statement inside `Statement`, not a whole policy. On any statement that allows `iam:PassRole`, set `iam:PassedToService` to the service that will assume the role.

   ```json
   {
     "Sid": "CreateRoleWithBoundary",
     "Effect": "Allow",
     "Action": ["iam:CreateRole", "iam:AttachRolePolicy"],
     "Resource": "arn:aws:iam::123456789012:role/example-*",
     "Condition": {
       "StringEquals": {
         "iam:PermissionsBoundary": "arn:aws:iam::123456789012:policy/example-boundary"
       }
     }
   }
   ```

5. Validate the document, then simulate the calls you listed against that document. A finding of `ERROR` stops the change. A `SECURITY_WARNING` needs a written reason or a tighter policy.

   ```bash
   aws accessanalyzer validate-policy --policy-type IDENTITY_POLICY --policy-document file://policy.json
   aws iam simulate-custom-policy --policy-input-list file://policy.json --action-names s3:PutObject --resource-arns arn:aws:s3:::example-bucket/app/file
   ```

6. Keep one GitHub OIDC provider in the account: URL `https://token.actions.githubusercontent.com`, audience `sts.amazonaws.com`. Leave the thumbprint unset so IAM fetches it. Reuse the provider if it already exists.

7. Trust `sts:AssumeRoleWithWebIdentity` for one repository and one environment, or one ref. Copy the `sub` claim from a token for this repository. The forms are in `principle-no-static-credentials`. The statement below is the immutable subject. A repository that still uses name-only subjects omits `@123456` and `@456789`. Use `StringEquals`. A `StringLike` of `repo:*` is not a scope.

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
         },
         "Action": "sts:AssumeRoleWithWebIdentity",
         "Condition": {
           "StringEquals": {
             "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
             "token.actions.githubusercontent.com:sub": "repo:example-org@123456/example-repo@456789:environment:production"
           }
         }
       }
     ]
   }
   ```

8. Separate the plan role from the apply role. The plan role can read the resources it plans. It cannot create, delete or pass a role. Follow `principle-least-privilege`.

9. For a resource policy, set `aws:SourceAccount` to `123456789012`, or `aws:PrincipalOrgID` when the caller is another account in the organization. An open principal plus a condition you forgot is public.

10. Triage Access Analyzer before you widen access. An external-access finding on the resource you are changing is part of this review. Turn on unused-access analysis for the account. Do not archive a finding to make the list empty.

11. If Terraform applies the policy, follow `terraform-plan-review` and `terraform-state-backends`. Name the account, the role and the pipeline. One policy change. Follow `principle-change-safety`.

## Safety checks

- The actions match the call list. No `AdministratorAccess`, no `Action` of `*`, no write on `Resource: "*"`.
- People use Identity Center. The pipeline has no access key.
- Roles this pipeline creates carry the permission boundary. `iam:PassRole` names the service.
- `validate-policy` reports no `ERROR`. The simulation result matches the calls you intend.
- The GitHub trust uses `StringEquals` on one subject copied from a token.
- Plan and apply are different roles.
- Access Analyzer external-access findings on this resource are triaged.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Write the rollback before production. Follow `principle-rollback-first`.

1. Keep the previous policy version. `aws iam set-default-policy-version` returns a customer managed policy to that version.
2. Detach a new managed policy before you delete it. Do not delete a boundary that roles still use.
3. Rehearse the policy revert in a non-production account.

## Done when

- The role's actions, ARNs and trust match the job and nothing wider.
- Validation and simulation have been run, and Analyzer findings are triaged.
- A wider grant has an expiry or a tracked follow-up to narrow it.
