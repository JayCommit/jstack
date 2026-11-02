# Prompts for ops-secrets-handling

Example asks for `ops-secrets-handling`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I are about to store a secret for an app, a pipeline, or a git repo.

### Expected for ask 1

- Load `ops-secrets-handling` and follow that file through its own done-when.
- Step: Pick one home before you write the value. An app on Azure reads Key Vault. Follow `azure-key-vault`. An app on AWS reads Secrets Manager or a SecureString parameter. Follow `aws-secrets-ssm`. A value that has to live in git is SOPS ciphertext. Follow `gitops-argocd-flux`. A value only the pipeline needs is a GitHub Actions environment secret or an Azure DevOps variable group linked to Key Vault. Do not also put it in tfvars, chat, or a log. Follow `principle-no-static-credentials`.
- Check: The value lives in one home. A second copy in git, tfvars, or chat is still a leak.
- Done when: The secret has one home, and the consumer reads it from there.

## Ask 2

On GitHub, put production values on the `production` environment, not in a repository secret that every branch job can read.

### Expected for ask 2

- Load `ops-secrets-handling` and follow that file through its own done-when.
- Step: On GitHub, put production values on the `production` environment, not in a repository secret that every branch job can read. Follow `pipelines-environments-approvals`. Set the secret from stdin so it is not in the shell history. Do not pass the value as an argument. Do not print it. Do not interpolate an event field into `run:`. Follow `pipelines-github-actions-authoring`.
- Check: GitHub production secrets are environment secrets. Azure DevOps secrets come from Key Vault.
- Done when: A leaked value has been rotated, and the old credential cannot authenticate.
