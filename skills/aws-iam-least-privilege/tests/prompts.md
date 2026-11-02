# Prompts for aws-iam-least-privilege

Example asks for `aws-iam-least-privilege`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I add or change an IAM policy, role, permission boundary or resource policy.

### Expected for ask 1

- Load `aws-iam-least-privilege` and follow that file through its own done-when.
- Step: List the API calls and the resource ARNs. Include `kms:Decrypt` when the job reads a secret. Follow `principle-least-privilege`. A copied policy from another account is not that list.
- Check: The actions match the call list. No `AdministratorAccess`, no `Action` of `*`, no write on `Resource: "*"`.
- Done when: The role's actions, ARNs and trust match the job and nothing wider.

## Ask 2

Give people access through IAM Identity Center.

### Expected for ask 2

- Load `aws-iam-least-privilege` and follow that file through its own done-when.
- Step: Give people access through IAM Identity Center. Give a pipeline or a workload a role it assumes. Do not create an access key for a person or a pipeline. Follow `principle-no-static-credentials`.
- Check: People use Identity Center. The pipeline has no access key.
- Done when: Validation and simulation have been run, and Analyzer findings are triaged.
