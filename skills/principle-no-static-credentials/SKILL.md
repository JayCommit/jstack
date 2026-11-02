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

- For GitHub Actions to Azure, add a federated credential on the app registration or the user-assigned managed identity. The issuer is `https://token.actions.githubusercontent.com` and the audience is `api://AzureADTokenExchange`. Copy the `sub` claim from a token issued for this repository. A repository created after 15 July 2026 uses `repo:<org>@<owner-id>/<repo>@<repo-id>:environment:<name>`. A repository that still uses name-only subjects uses `repo:<org>/<repo>:environment:<name>`. GitHub Enterprise Server keeps the name-only subject. Use one ref subject when the platform has no environment. The job sets `id-token: write`.
- For GitHub Actions to AWS, register an IAM OIDC identity provider for `token.actions.githubusercontent.com`. Trust `sts:AssumeRoleWithWebIdentity` only when `token.actions.githubusercontent.com:aud` is `sts.amazonaws.com` and `token.actions.githubusercontent.com:sub` is that same subject, including the owner id and the repository id when the token carries them.
- For Azure DevOps, use an Azure Resource Manager service connection with workload identity federation. Azure DevOps generates the issuer and subject; copy them from the connection into the federated credential rather than typing them by hand. Scope the connection as in `principle-least-privilege`.
- Workloads use a managed identity, an ECS task role, or EKS Pod Identity or IRSA.
- Keep tokens out of logs, artefacts and chat, and request them only in the job that needs them. Short-lived does not mean safe to print.
- On a leak, revoke the credential, rotate its replacement and read Entra sign-in logs or CloudTrail before continuing. How to read those logs is `principle-observe-before-you-fix`.
- Local development uses `az login` or IAM Identity Center.

Use one of these logins in the job that deploys. Each asks for an OIDC token and passes no long-lived secret. Pin the commit SHA you reviewed for the action. A major tag such as `azure/login@v3` or `aws-actions/configure-aws-credentials@v6` still moves.

Azure:

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
```

AWS:

```yaml
permissions:
  id-token: write
  contents: read
steps:
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
