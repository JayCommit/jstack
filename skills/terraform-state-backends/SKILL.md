---
name: terraform-state-backends
description: "Configure remote Terraform state with locking for Azure and AWS. Use when you add a backend, split state by environment, move or import resources, or restore a versioned state blob or object."
license: MIT
---

# State backends

Keep state in a remote backend with a lock. Never commit a state file. Never migrate state and change resources in the same apply.

## Use when

- You add or change a Terraform backend for Azure or AWS.
- You split state, move an address or import an existing resource.
- You must recover state from a versioned blob or object.
- Someone proposes a storage account key, a local state file or a shared `terraform.tfstate`.

## Steps

1. Authenticate with OIDC or workload identity federation. See `principle-no-static-credentials`. Do not put an access key, a storage account key or a client secret in the backend block or in tfvars.
2. For Azure, use the `azurerm` backend. Locking is a lease on the state blob. Set `use_azuread_auth = true` so the blob and the lease use Entra ID, not an account key. Set `use_oidc = true` for the pipeline. Turn on blob versioning before the first apply. Disable shared key access on that storage account once Entra auth works.
3. Leave `key` out of the shared block. Pass it per environment so dev, test and prod cannot share a blob. Pin Terraform to the release that was reviewed.

   ```hcl
   terraform {
     required_version = "1.10.5"

     backend "azurerm" {
       resource_group_name  = "rg-tfstate"
       storage_account_name = "stexampletfstate"
       container_name       = "tfstate"
       use_azuread_auth     = true
       use_oidc             = true
     }
   }
   ```

4. Point `terraform init` at the environment file. The dev file holds only the key.

   ```text
   terraform init -input=false -backend-config=envs/dev.backend.hcl
   ```

   ```hcl
   key = "app/dev.tfstate"
   ```

   Test uses `app/test.tfstate`. Prod uses `app/prod.tfstate`. Split further when two products must not share a blast radius.

5. Grant the plan identity read on that blob and the apply identity read and write. On Azure, scope Storage Blob Data Reader or Storage Blob Data Contributor to the container. On AWS, scope the role to the state key and its lock object. Do not grant `s3:*`. See `principle-least-privilege`.
6. For AWS, use the `s3` backend. Set `encrypt = true`. On Terraform 1.10 or newer, set `use_lockfile = true` so the lock is an object next to the state. Turn on bucket versioning. Do not set `access_key` or `secret_key`. The pipeline role comes from OIDC.

   ```hcl
   terraform {
     backend "s3" {
       bucket       = "example-tfstate"
       key          = "app/dev.tfstate"
       region       = "eu-west-2"
       encrypt      = true
       use_lockfile = true
     }
   }
   ```

7. A `dynamodb_table` argument is the older lock, still seen on existing stacks. Leave it only where that table already exists. Do not add a DynamoDB table for a new backend.
8. Move an address with `terraform state mv` in its own change. Plan afterwards. The plan must show no destroy. Put an import in git as an `import` block. A one-off `terraform import` leaves no record. See `principle-everything-as-code`.

   ```hcl
   import {
     to = azurerm_resource_group.this
     id = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-example"
   }
   ```

   ```text
   terraform state mv azurerm_resource_group.old azurerm_resource_group.this
   ```

9. Migrate state in its own change. Run `terraform init -migrate-state`, then plan. Continue only when that plan changes no resources. A later change edits resources. See `principle-change-safety`.
10. If init reports a lock, find the holder and the running pipeline before you touch it. See `principle-observe-before-you-fix`. Do not run `terraform force-unlock` while that run is alive.
11. Recover by restoring the previous blob version or the previous S3 object version, then plan. Apply only when that restored generation is the one you meant, and only from a saved plan. Follow `principle-rollback-first` when the snapshot is production.
12. Do not commit `*.tfstate`, `*.tfstate.*`, `.terraform/`, `crash.log` or `tfplan`. A plan file can hold sensitive values. A second apply with the same config must not fork a second state. See `principle-idempotent-automation`.

## Safety checks

- The backend uses Entra ID or the OIDC role. No account key and no static AWS key.
- Locking is on: a blob lease for Azure, `use_lockfile = true` for a new S3 backend.
- Each environment has its own key. The key is named on the change.
- Versioning is on for the blob or the bucket before you rely on it for recovery.
- A migrate plan and a resource-change plan are not the same apply.
- Provider pins on the stack match the reviewed release, such as `hashicorp/azurerm` `4.14.0` and `hashicorp/aws` `5.84.0`.

## Rollback

Restore the previous versioned blob or object, plan, and apply a saved plan only if the restored state is the generation you meant. Do not hand-edit state. Follow `principle-rollback-first` for production. If the restore plan is not the reverse of the last apply, stop.

## Done when

- State is remote, locked, versioned and absent from git.
- The environment key is unique, and the identity can only touch that key.
- Moves and imports were planned in their own change and show no unexpected destroy.
- A migrate was not mixed with a resource change.
