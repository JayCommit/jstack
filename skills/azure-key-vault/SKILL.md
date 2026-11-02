---
name: azure-key-vault
description: "Use when you create a Key Vault or let a pipeline or app read it. Turn on RBAC authorization, purge protection and a private endpoint, split secrets, keys and certificates, and keep values out of logs and plan output."
license: MIT
---

# Azure Key Vault

Use RBAC on a new vault. Keep values out of logs, plan output and git. Applications read the vault at runtime.

## Use when

- You create a Key Vault or change its network or authorization mode.
- A pipeline or a workload needs to read a secret, a key or a certificate.
- Terraform or a pipeline will write a secret.
- You rotate a secret, a key or a certificate, or you recover a deleted one.

## Steps

1. Create the vault with RBAC authorization, soft delete and purge protection. Soft delete cannot be turned off. Set retention at creation. Use 90 days for production. Do not pass `--enable-rbac-authorization false`. Do not add an access policy on a new vault.

   ```bash
   az keyvault create --name kv-example --resource-group rg-example --location uksouth --enable-rbac-authorization true --enable-purge-protection true --retention-days 90
   ```

2. On an existing vault that still uses access policies, create the RBAC assignments first and prove the app still reads. Then switch the vault to RBAC in a separate reviewed change. Switching first drops policy access and causes an outage.

3. Keep secrets, keys and certificates on their own planes. Do not store a key or a certificate as a secret string. Grant Key Vault Secrets User for secret reads, Key Vault Crypto User for key use, and Key Vault Certificate User for certificate reads. Scope the assignment to the vault resource, not the resource group. Do not grant Key Vault Administrator to a pipeline.

   ```bash
   az role assignment create --assignee-object-id 00000000-0000-0000-0000-000000000000 --assignee-principal-type ServicePrincipal --role "Key Vault Secrets User" --scope /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-example/providers/Microsoft.KeyVault/vaults/kv-example
   ```

4. Give the workload a user-assigned managed identity. The app reads the vault at runtime. Do not copy the secret into app settings, a pipeline variable or git. Follow `principle-no-static-credentials`.

5. Federate the pipeline identity as in `azure-rbac-entra`. Grant it Key Vault Secrets User, or a custom role whose data actions are narrower, on this vault only. No client secret and no storage account key. Follow `principle-least-privilege`.

6. Put a private endpoint on the vault in `snet-pe`. The group id is `vault`. Link Private DNS zone `privatelink.vaultcore.azure.net` as in `azure-networking`. Prove the app resolves the vault name before you close the public path.

   ```bash
   az network private-endpoint create --name pe-kv-example --resource-group rg-example --vnet-name vnet-spoke-example --subnet snet-pe --private-connection-resource-id /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-example/providers/Microsoft.KeyVault/vaults/kv-example --group-id vault --connection-name pec-kv-example
   ```

7. Turn public network access off only after that proof. Do not turn it off first.

   ```bash
   az keyvault update --name kv-example --resource-group rg-example --public-network-access Disabled
   ```

8. Read the vault back. RBAC authorization must be true. Public network access must be Disabled only when the private endpoint works.

   ```bash
   az keyvault show --name kv-example --resource-group rg-example --query "{rbac:properties.enableRbacAuthorization,publicNetwork:properties.publicNetworkAccess}" --output json
   ```

9. If Terraform must write a secret, mark the variable sensitive, write no output, and do not run `terraform state show` or `terraform output` on that address in a log. Treat state as sensitive. Pin `hashicorp/azurerm` `4.14.0` and Terraform `1.10.5`. Use a remote backend with the blob lease lock and Azure AD auth. Stop if the plan prints a plaintext value. Prefer the app or a rotation job to write the value so it never enters state.

10. Give every rotation an owner and a next date on the change. Set an expiry when the secret is written. Do not put the value on the command line or in the pull request. For a key that supports a rotation policy, record the policy expiry and the owner. A date with no owner is not a rotation plan.

11. Name the blast radius: subscription, resource group, vault, private endpoint, DNS zone and pipeline. One change. Follow `principle-change-safety`. A new vault or a Premium SKU is a cost change. Follow `principle-cost-awareness`. Import a portal vault or revert it. Follow `principle-everything-as-code`.

## Safety checks

- The new vault uses RBAC. No access policy was added.
- Soft delete retention is set. Purge protection is on for production.
- The pipeline role is Key Vault Secrets User or narrower, scoped to this vault, and the identity is federated.
- Public network access is off only after the private endpoint and `privatelink.vaultcore.azure.net` work.
- The plan and the logs do not contain a secret value.
- Rotation has a named owner and a date.
- Provider and Terraform versions are pinned when Terraform touches the vault.

## Rollback

Purge protection cannot be turned off. Write the rollback before production. Follow `principle-rollback-first`.

1. Recover a deleted object. Do not recreate it with a guessed value.

   ```bash
   az keyvault secret recover --vault-name kv-example --name example-setting
   az keyvault key recover --vault-name kv-example --name example-key
   az keyvault certificate recover --vault-name kv-example --name example-cert
   ```

2. If the private path fails after you disable public access, turn public network access back on only as the rehearsed rollback, then fix the endpoint. Do not leave public access on once the private path works.
3. Remove the role assignment you added if the grant was wrong. Do not delete the vault as a rollback while purge protection will only soft-delete it.

## Done when

- The vault is RBAC, purge-protected, and private once the endpoint is proven.
- Callers have a role on one object plane, scoped to the vault.
- No secret value is in git, state output or the pipeline log.
- The owner and the next rotation date are on the change.
