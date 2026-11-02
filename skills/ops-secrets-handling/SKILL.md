---
name: ops-secrets-handling
description: "Use when a secret is created, copied, or leaked. Keep one home in Key Vault, Secrets Manager, or SOPS, and rotate a leaked value before you close the leak."
license: MIT
---

# Secrets handling

A secret has one home. A leak is closed by rotation. Deleting the line that contained it does not close it.

## Use when

- You are about to store a secret for an app, a pipeline, or a git repo.
- A secret is in a chat, a pull request, a log, a tfvars file, or a shell history.
- A scan finds a credential in git history.
- Someone proposes to force-push the secret away and leave the old value valid.

## Steps

1. Pick one home before you write the value. An app on Azure reads Key Vault. Follow `azure-key-vault`. An app on AWS reads Secrets Manager or a SecureString parameter. Follow `aws-secrets-ssm`. A value that has to live in git is SOPS ciphertext. Follow `gitops-argocd-flux`. A value only the pipeline needs is a GitHub Actions environment secret or an Azure DevOps variable group linked to Key Vault. Do not also put it in tfvars, chat, or a log. Follow `principle-no-static-credentials`.

2. On GitHub, put production values on the `production` environment, not in a repository secret that every branch job can read. Follow `pipelines-environments-approvals`. Set the secret from stdin so it is not in the shell history. Do not pass the value as an argument. Do not print it. Do not interpolate an event field into `run:`. Follow `pipelines-github-actions-authoring`.

   ```bash
   gh secret set EXAMPLE_SETTING --env production
   ```

3. On Azure DevOps, keep the value in a variable group linked to Key Vault. Follow `pipelines-azure-devops-yaml`. The YAML names the variable. It does not contain the value. The log must show a mask, not the value.

4. Prefer federation so the pipeline has no long-lived cloud key. Follow `pipelines-oidc-federation`. The identity that reads the secret can read that one secret. Follow `principle-least-privilege`.

5. When a value has leaked, rotate it before you clean up the text. Assume the old value was copied. Do these in order.

   - Revoke or rotate in the home from step 1. Disable a cloud access key. Do not only delete the line in the repo.
   - Point the consumer at the new value. A running app that cached the old value needs a restart after the rotation, and that restart is a change you name.
   - Scan the history with redaction so the tool does not print the secret again. Run `gitleaks detect --source . --redact` on the repo that leaked. CI in this repo runs gitleaks on pull requests. That does not replace a scan of a repository that already leaked.
   - Read the pipeline logs and the artefacts for the value. Follow `principle-observe-before-you-fix`. A force-push that drops a commit does not replace rotation. History on other clones still has the old value.

6. Do not put the new value in the issue, the pull request, the runbook, or the incident channel. Write the secret name and the time you rotated it. Follow `ops-runbook-authoring` and `ops-postmortem`.

7. If Terraform stored the value in state, treat the state as sensitive and follow `terraform-state-backends`. Do not `terraform output` the value into a log. A leak of state is the same rotation as a leak of the file.

## Safety checks

- The value lives in one home. A second copy in git, tfvars, or chat is still a leak.
- GitHub production secrets are environment secrets. Azure DevOps secrets come from Key Vault.
- The pipeline is federated, or the change record says which one secret the static credential still has to read.
- A leak was rotated, and the old credential was disabled or deleted after the new value worked.
- `gitleaks` was run with redaction. The pull request does not contain the value.
- The identity that reads the secret cannot read every secret in the account or vault.

## Rollback

Do not roll back to a leaked value. Follow `principle-rollback-first`.

1. If the new value is wrong and the old value was not leaked, restore the previous version. Key Vault recovery is `azure-key-vault`. Secrets Manager `AWSPREVIOUS` is `aws-secrets-ssm`. Rehearse that restore on a non-production secret.
2. If you rotated because of a leak, a bad new value is fixed by a second rotation. Putting the leaked value back reopens the leak.
3. Rehearse a non-production rotation before you depend on it for production.

## Done when

- The secret has one home, and the consumer reads it from there.
- A leaked value has been rotated, and the old credential cannot authenticate.
- The issue, the pull request, and the logs do not contain the value.
