# Prompts for principle-no-static-credentials

Example asks for `principle-no-static-credentials`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

A GitHub Actions or Azure DevOps pipeline logs in to Azure or AWS.

### Expected for ask 1

- Load `principle-no-static-credentials` and follow that file through its own done-when.
- Rule: For GitHub Actions to Azure, add a federated credential on the app registration or the user-assigned managed identity. The issuer is `https://token.actions.githubusercontent.com` and the audience is `api://AzureADTokenExchange`. Copy the `sub` claim from a token issued for this repository. A repository created after 15 July 2026 uses `repo:<org>@<owner-id>/<repo>@<repo-id>:environment:<name>`. A repository that still uses name-only subjects uses `repo:<org>/<repo>:environment:<name>`. GitHub Enterprise Server keeps the name-only subject. Use one ref subject when the platform has no environment. The job sets `id-token: write`.
- Red flag: An AWS access key, a client secret or a `creds` JSON blob is stored for the deploy pipeline.
- Done when: The pipeline or workload assumes a role with federation and stores no cloud key.

## Ask 2

For GitHub Actions to AWS, register an IAM OIDC identity provider for `token.actions.githubusercontent.com`.

### Expected for ask 2

- Load `principle-no-static-credentials` and follow that file through its own done-when.
- Rule: For GitHub Actions to AWS, register an IAM OIDC identity provider for `token.actions.githubusercontent.com`. Trust `sts:AssumeRoleWithWebIdentity` only when `token.actions.githubusercontent.com:aud` is `sts.amazonaws.com` and `token.actions.githubusercontent.com:sub` is that same subject, including the owner id and the repository id when the token carries them.
- Red flag: The cloud login runs in a job that does not set `id-token: write`.
- Done when: The trust or federated subject is limited to the repository and the environment or branch that deploys.
