---
name: principle-no-static-credentials
description: "Apply before a pipeline or workload authenticates to Azure or AWS, and again if a credential leaks. Use OIDC or workload identity federation and short-lived tokens. Revoke and rotate anything that has leaked."
license: MIT
---

# No static credentials

Pipelines and workloads authenticate with short-lived federated tokens. Revoke a leaked credential and rotate it before work continues.

## Use when

- A GitHub Actions or Azure DevOps pipeline logs in to Azure or AWS.
- A workload on AKS, App Service, EKS, ECS or a virtual machine needs a cloud API.
- Someone proposes a client secret, an AWS access key or a long-lived shared access signature.
- A credential has appeared in a log, a pull request or a chat.

## Rules

- For GitHub Actions to Azure, add a federated credential on the app registration or the user-assigned managed identity. The issuer is `https://token.actions.githubusercontent.com` and the audience is `api://AzureADTokenExchange`. Limit the subject to `repo:<org>/<repo>:environment:<name>` or a single ref. The job must set `id-token: write`.
- For GitHub Actions to AWS, register an IAM OIDC identity provider for `token.actions.githubusercontent.com`. Trust `sts:AssumeRoleWithWebIdentity` only when `token.actions.githubusercontent.com:aud` is `sts.amazonaws.com` and `token.actions.githubusercontent.com:sub` matches this repository and environment.
- For Azure DevOps, use an Azure Resource Manager service connection with workload identity federation. Azure DevOps generates the issuer and subject; copy them from the connection into the federated credential rather than typing them by hand. Scope the connection as in `principle-least-privilege`.
- Workloads use a managed identity, an ECS task role, or EKS Pod Identity or IRSA.
- Keep tokens out of logs, artefacts and chat, and request them only in the job that needs them. Short-lived does not mean safe to print.
- On a leak, revoke the credential, rotate its replacement and read Entra sign-in logs or CloudTrail before continuing. How to read those logs is `principle-observe-before-you-fix`.
- Local development uses `az login` or IAM Identity Center.

Use one of these logins in the job that deploys. Both ask for an OIDC token and pass no long-lived secret:

```yaml
permissions:
  id-token: write
  contents: read
steps:
  - uses: azure/login@v3
    with:
      client-id: 00000000-0000-0000-0000-000000000000
      tenant-id: 00000000-0000-0000-0000-000000000000
      subscription-id: 00000000-0000-0000-0000-000000000000
  - uses: aws-actions/configure-aws-credentials@v6
    with:
      role-to-assume: arn:aws:iam::123456789012:role/example-deploy
      aws-region: eu-west-2
```

## Red flags

- An AWS access key, a client secret or a `creds` JSON blob is stored for the deploy pipeline.
- The cloud login runs in a job that does not set `id-token: write`.
- The role trust allows any repository, or any subject, to assume the production role.
- A production federated credential matches every branch and every pull request.
- A leaked key stays active while rotation is left for later.

## Done when

- The pipeline or workload assumes a role with federation and stores no cloud key.
- The trust or federated subject is limited to the repository and the environment or branch that deploys.
- Any leaked credential is revoked, and the audit log has been checked.
