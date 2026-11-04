---
name: pipelines-oidc-federation
description: "Use when a GitHub Actions or Azure DevOps pipeline logs in to Azure or AWS. Federate the identity with an exact subject and drop any stored cloud key or client secret."
license: MIT
---

# OIDC federation for pipelines

A pipeline assumes a cloud role with a short-lived token. The trust names one repository and one environment. Nothing in the workflow is a long-lived key.

## Use when

- A GitHub Actions job or an Azure DevOps pipeline calls Azure or AWS.
- You add a federated credential, an IAM OIDC provider or a cloud role trust.
- Someone proposes a client secret, an AWS access key or a shared access signature for the pipeline.
- A login works from the wrong branch, the wrong repository or a fork.

## Steps

1. Follow `principle-no-static-credentials`. Do not create a client secret or an access key for the pipeline. Local work uses `az login` or IAM Identity Center.

2. Read the GitHub subject from a token this repository has issued, or from the repository OIDC settings. Do not invent it. Repositories created after 15 July 2026 include the owner id and the repository id: `repo:<org>@<owner-id>/<repo>@<repo-id>:environment:<name>`. Repositories that still use a name-only subject, including GitHub Enterprise Server, use `repo:<org>/<repo>:environment:<name>`. A job that sets `environment` receives a subject ending in `:environment:<name>`, not a ref subject. Trust one ref subject only when that platform has no environment. The example commands use `repo:example-org@123456/example-repo@456789:environment:production`. Drop the `@123456` and `@456789` segments for a name-only repository.

3. On Azure, add a federated credential to the user-assigned managed identity or the app registration. The GitHub issuer is `https://token.actions.githubusercontent.com`. The audience is `api://AzureADTokenExchange`. An app registration or managed identity holds at most 20 federated credentials. The subject has no wildcard. Flexible federated credentials are a preview on app registrations only. Keep every subject exact. Scope the identity as in `azure-rbac-entra` and `principle-least-privilege`.

   ```bash
   az identity federated-credential create --name github-example-production --identity-name id-pipeline --resource-group rg-example --issuer https://token.actions.githubusercontent.com --subject repo:example-org@123456/example-repo@456789:environment:production --audiences api://AzureADTokenExchange
   ```

4. Set `permissions: contents: read` on the workflow. On the login job, set `id-token: write` and repeat `contents: read`, because a job permissions block replaces the workflow set. Add `timeout-minutes`. A deploy also sets `concurrency` with `cancel-in-progress: false`. Follow `pipelines-github-actions-authoring` and `pipelines-environments-approvals`.

   ```yaml
   permissions:
     contents: read
   concurrency:
     group: deploy-production
     cancel-in-progress: false
   jobs:
     deploy:
       runs-on: ubuntu-latest
       timeout-minutes: 20
       environment: production
       permissions:
         id-token: write
         contents: read
       steps:
         - uses: azure/login@a641126d1b8aa4d1fa005f4f92df94a3a4c4c906 # v3.1.0
           with:
             client-id: 00000000-0000-0000-0000-000000000000
             tenant-id: 00000000-0000-0000-0000-000000000000
             subscription-id: 00000000-0000-0000-0000-000000000000
   ```

5. For GitHub to AWS, keep one IAM OIDC provider for `token.actions.githubusercontent.com` with audience `sts.amazonaws.com`. IAM checks GitHub's certificate against its trusted root authorities, so the thumbprint is not what protects this role. The `aud` and `sub` conditions are. Trust `sts:AssumeRoleWithWebIdentity` with `StringEquals` on `token.actions.githubusercontent.com:aud` and `token.actions.githubusercontent.com:sub`. Use `StringLike` only for one narrow pattern you can name, and never for `repo:*`. Follow `aws-iam-least-privilege`. Separate the plan role from the apply role. A pull-request plan job has no environment, so its subject ends in `:pull_request`. Give that subject the read-only plan role only.

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "GitHubActionsProduction",
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

   ```yaml
   - uses: aws-actions/configure-aws-credentials@e1253824e5c10ff9df46874f81ed3ec929e19cfd # v6.3.0
     with:
       role-to-assume: arn:aws:iam::123456789012:role/example-deploy
       aws-region: eu-west-2
   ```

6. For Azure DevOps to Azure, create an Azure Resource Manager service connection with workload identity federation. Azure DevOps generates the issuer and the subject. Copy both from that connection into the federated credential. Copy the audience from the connection too. Do not type a guessed issuer or subject, and do not copy either value from a blog or a sample. The same limit of 20 credentials and the same exact-subject rule apply. Follow `pipelines-azure-devops-yaml`.

7. For Azure DevOps to AWS, use an AWS service connection from the AWS Toolkit for Azure DevOps. Set the role to assume, leave the access key fields empty, and tick Use OIDC. Azure DevOps issues the token, so its issuer is per organization. Copy the issuer, audience and subject from the connection or from the first run's log into the IAM OIDC provider and the `StringEquals` trust. Do not guess them. If the connection cannot federate, stop and raise it. Do not fall back to an access key on the connection.

## Safety checks

- The workflow stores no client secret and no AWS access key.
- The GitHub subject was copied from a token or from the repository OIDC settings.
- A job that sets `environment` trusts the environment subject, not a ref subject.
- Azure subjects are exact. The credential count on that identity stays at or below 20.
- The AWS trust uses `StringEquals` on `aud` and `sub`, or a `StringLike` pattern narrow enough to name.
- Azure DevOps issuer and subject were copied from the service connection.
- `id-token: write` is present only on the job that logs in.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Delete the federated credential or the trust statement you added if the subject was wrong. Leave the identity or the role in place when other jobs still use it. Follow `principle-rollback-first`. Rehearse the delete on a non-production identity before you rely on it for production. Do not fall back to a stored key while you fix the subject.

## Done when

- The pipeline role is assumed with federation, and no cloud key is stored for it.
- The trust or federated subject matches one repository and one environment, or one ref where no environment exists.
- Plan and apply use different identities. A login from any other subject fails.
