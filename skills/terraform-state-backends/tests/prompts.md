# Prompts for terraform-state-backends

Example asks for `terraform-state-backends`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I add or change a Terraform backend for Azure or AWS.

### Expected for ask 1

- Load `terraform-state-backends` and follow that file through its own done-when.
- Step: Authenticate with OIDC or workload identity federation. See `principle-no-static-credentials`. Do not put an access key, a storage account key or a client secret in the backend block or in tfvars.
- Check: The backend uses Entra ID or the OIDC role. No account key and no static AWS key.
- Done when: State is remote, locked, versioned and absent from git.

## Ask 2

For Azure, use the `azurerm` backend.

### Expected for ask 2

- Load `terraform-state-backends` and follow that file through its own done-when.
- Step: For Azure, use the `azurerm` backend. Locking is a lease on the state blob. Set `use_azuread_auth = true` so the blob and the lease use Entra ID, not an account key. Set `use_oidc = true` for the pipeline. Turn on blob versioning before the first apply. Disable shared key access on that storage account once Entra auth works.
- Check: Locking is on: a blob lease for Azure, `use_lockfile = true` for a new S3 backend.
- Done when: The environment key is unique, and the identity can only touch that key.
