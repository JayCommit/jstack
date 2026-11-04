# Federate a pipeline to Azure

A workflow logs in to Azure with a client secret or a `creds` JSON blob. Replace that with a short-lived federated token.

## Ask this

```text
The deploy job in example-org/example logs in to Azure with a client secret.
Subscription 00000000-0000-0000-0000-000000000000.
Environment production.
Load principle-no-static-credentials and azure-rbac-entra.
Copy the sub claim from a token issued for this repository.
Do not store a client secret. Stop before any grant.
```

## Load

- `principle-no-static-credentials` owns the login. Copy the `sub` claim from a token for this repository. That skill names the issuer and the audience. Do not type a subject from memory, and do not copy one from this page.
- `azure-rbac-entra` assigns the narrowest role at the resource. The pipeline identity is federated. It is not Owner.

An Azure DevOps pipeline copies the issuer and the subject from the service connection. The same skill says so. AWS trusts the subject that token already carries. Load `pipelines-oidc-federation` when the job needs both clouds.

## What good looks like

The workflow sets `id-token: write` only on the job that logs in, and `contents: read` on that job too. The federated credential matches the repository and the environment that deploys. No client secret, access key, or `AZURE_CREDENTIALS` blob remains in the workflow or the repository secrets for this login.

The agent prepares the federated credential and the workflow diff, then stops. A person grants the role.
