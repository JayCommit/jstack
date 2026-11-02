# Prompts for pipelines-oidc-federation

Example asks for `pipelines-oidc-federation`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

A GitHub Actions job or an Azure DevOps pipeline calls Azure or AWS.

### Expected for ask 1

- Load `pipelines-oidc-federation` and follow that file through its own done-when.
- Step: Follow `principle-no-static-credentials`. Do not create a client secret or an access key for the pipeline. Local work uses `az login` or IAM Identity Center.
- Check: The workflow stores no client secret and no AWS access key.
- Done when: The pipeline role is assumed with federation, and no cloud key is stored for it.

## Ask 2

Read the GitHub subject from a token this repository has issued, or from the repository OIDC settings.

### Expected for ask 2

- Load `pipelines-oidc-federation` and follow that file through its own done-when.
- Step: Read the GitHub subject from a token this repository has issued, or from the repository OIDC settings. Do not invent it. Repositories created after 15 July 2026 include the owner id and the repository id: `repo:<org>@<owner-id>/<repo>@<repo-id>:environment:<name>`. Repositories that still use a name-only subject, including GitHub Enterprise Server, use `repo:<org>/<repo>:environment:<name>`. A job that sets `environment` receives a subject ending in `:environment:<name>`, not a ref subject. Trust one ref subject only when that platform has no environment. The example commands use `repo:example-org@123456/example-repo@456789:environment:production`. Drop the `@123456` and `@456789` segments for a name-only repository.
- Check: The GitHub subject was copied from a token or from the repository OIDC settings.
- Done when: The trust or federated subject matches one repository and one environment, or one ref where no environment exists.
