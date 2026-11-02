# Prompts for aws-secrets-ssm

Example asks for `aws-secrets-ssm`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I create a secret, a SecureString parameter or a rotation.

### Expected for ask 1

- Load `aws-secrets-ssm` and follow that file through its own done-when.
- Step: Decide the home before you write the value. Use Secrets Manager when the value rotates, when AWS provides a managed rotation such as RDS, or when another account must read it. Use Parameter Store SecureString for a secret that does not rotate. Use a String parameter only for a value that can be public. Do not store the same secret in both services.
- Check: The value is in one service, and a secret is not a String parameter.
- Done when: The secret or parameter exists in the service this skill names, encrypted, with one reader role.

## Ask 2

Keep the value out of the command line, the pull request, Terraform variables and chat.

### Expected for ask 2

- Load `aws-secrets-ssm` and follow that file through its own done-when.
- Step: Keep the value out of the command line, the pull request, Terraform variables and chat. Read it from a gitignored file at create time. A `secret_version` or parameter value that Terraform manages is stored in state. State stays encrypted and out of git. Follow `terraform-state-backends`.
- Check: The value was not committed, pasted into the plan, or passed on the command line.
- Done when: Rotation either works in test or is explicitly not required.
