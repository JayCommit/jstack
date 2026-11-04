---
name: aws-secrets-ssm
description: "Use when you store a secret or a configuration value in AWS. Put rotating credentials in Secrets Manager, put other secrets in Parameter Store as SecureString, and scope the pipeline to one ARN."
license: MIT
---

# Secrets Manager and Parameter Store

A secret has one home. Rotating credentials live in Secrets Manager. Other secrets live as SecureString parameters. The pipeline can read one ARN.

## Use when

- You create a secret, a SecureString parameter or a rotation.
- A task, a pod or a pipeline must read a secret.
- A secret is in a plain environment variable, a String parameter, a tfvars file or a log.
- Someone proposes `--force-delete-without-recovery` or a shared wildcard ARN.

## Steps

1. Decide the home before you write the value. Use Secrets Manager when the value rotates, when AWS provides a managed rotation such as RDS, or when another account must read it. Use Parameter Store SecureString for a secret that does not rotate. Use a String parameter only for a value that can be public. Do not store the same secret in both services.

2. Keep the value out of the command line, the pull request, Terraform variables and chat. Read it from a gitignored file at create time. A `secret_version` or parameter value that Terraform manages is stored in state. State stays encrypted and out of git. Follow `terraform-state-backends`.

   ```bash
   aws secretsmanager create-secret --name example/app/db --region eu-west-2 --secret-string file://secret.json --kms-key-id alias/example
   aws ssm put-parameter --name /example/app/token --region eu-west-2 --type SecureString --value file://value.txt --key-id alias/example
   ```

3. Use a customer managed key when a principal who can call `GetSecretValue` or `GetParameter` must still be unable to decrypt. Otherwise the AWS managed key is enough. Either way the identity policy names the secret or parameter ARN, not `*`.

4. For Secrets Manager, allow `secretsmanager:GetSecretValue` on that secret ARN. For Parameter Store, allow `ssm:GetParameter` on that parameter ARN. Allow `kms:Decrypt` only via the service that stores the secret.

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "ReadOneSecret",
         "Effect": "Allow",
         "Action": ["secretsmanager:GetSecretValue"],
         "Resource": "arn:aws:secretsmanager:eu-west-2:123456789012:secret:example/app/db-*"
       },
       {
         "Sid": "DecryptViaSecretsManager",
         "Effect": "Allow",
         "Action": ["kms:Decrypt"],
         "Resource": "arn:aws:kms:eu-west-2:123456789012:key/00000000-0000-0000-0000-000000000000",
         "Condition": {
           "StringEquals": {
             "kms:ViaService": "secretsmanager.eu-west-2.amazonaws.com"
           }
         }
       }
     ]
   }
   ```

5. The suffix after the secret name is the random suffix AWS adds. Scope the ARN to that secret's prefix, as above. Do not grant `secretsmanager:*` on `*`. Follow `aws-iam-least-privilege`.

6. Turn on rotation only when a rotation function or a managed RDS rotation is ready. Call `aws secretsmanager rotate-secret` after that function exists. Rotation without a function fails, and the current value stays. Test rotation on a non-production secret first.

7. Cross-account read is a resource policy on the secret plus the identity policy in the other account. Name the other account. Do not use `Principal: "*"`.

8. A pipeline reads the secret in the job that uses it and masks the output. It does not print `get-secret-value`. It authenticates with the OIDC role from `aws-iam-least-privilege`. Follow `principle-no-static-credentials`. ECS injects the value with `valueFrom`. Follow `aws-ecs`.

9. Deletion uses a recovery window. Thirty days is the production window. `--force-delete-without-recovery` is not a production step.

   ```bash
   aws secretsmanager delete-secret --secret-id example/app/db --region eu-west-2 --recovery-window-in-days 30
   ```

10. If Terraform applies the secret resource, follow `terraform-plan-review` and `terraform-state-backends`. The value is not in the repository. Name the account, the secret and the pipeline. Follow `principle-change-safety`.

## Safety checks

- The value is in one service, and a secret is not a String parameter.
- The value was not committed, pasted into the plan, or passed on the command line.
- The identity policy names one secret or one parameter, plus `kms:Decrypt` via that service.
- Rotation is configured only where a function or a managed rotation exists, and it was tested off production.
- The pipeline is federated and does not log the value.
- A production delete has a recovery window of 30 days.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Write the rollback before production. Follow `principle-rollback-first`.

1. `aws secretsmanager restore-secret` works until the recovery window ends. Rehearse a delete and a restore on a non-production secret.
2. A rotated password needs the previous version, `AWSPREVIOUS`, and a tested path back to the consumer. Do not rotate production until that path has worked once.
3. Parameter Store keeps earlier versions. `aws ssm get-parameter-history --name /example/app/token --region eu-west-2` lists them. Put the previous value back. Copy that value to the password manager you already use before you overwrite a parameter you cannot afford to lose.

## Done when

- The secret or parameter exists in the service this skill names, encrypted, with one reader role.
- Rotation either works in test or is explicitly not required.
- The pipeline and the workload read it without storing a second copy.
