---
name: terraform-module-design
description: "Design Terraform modules for Azure and AWS. Use when you add or change a child module: typed inputs and outputs, a pinned registry or git tag, and no provider block inside the module."
license: MIT
---

# Module design

Build small modules and pin every published version. The root module configures providers. A child module does not.

## Use when

- You add a module that Azure or AWS stacks will call.
- You change inputs, outputs or the version a caller pins.
- A child module contains a `provider` block or a `source` that tracks a branch.

## Steps

1. Split by concern. One module owns the network, another the data store, another the workload identity. The root module composes them. Pass outputs through the root. A network module does not call the database module.
2. Give every variable a `type` and a `description`. Add `validation` when a bad value would plan the wrong region, SKU or address space. State the meaning and the unit. Do not repeat the variable name as the description.
3. Give every output a `description` and a `value`. Set `sensitive` only when the value must stay out of logs. Do not output an access key, a storage account key or a client secret. Callers authenticate with OIDC or workload identity federation. See `principle-no-static-credentials`.
4. Show the contract in the module. Reject a variable that has no type or no description.

   ```hcl
   variable "location" {
     type        = string
     description = "Azure region for resources this module creates."

     validation {
       condition     = contains(["westeurope", "eastus"], var.location)
       error_message = "location must be westeurope or eastus."
     }
   }

   output "resource_group_id" {
     description = "Resource id of the group this module creates."
     value       = azurerm_resource_group.this.id
   }
   ```

5. Pin Terraform and the provider to the release that was reviewed. A child module includes `required_providers` and does not include a `provider` block. An AWS module uses the same block with `hashicorp/aws` and `5.84.0`. Do not use a lower-bound range. It moves on the next `terraform init`.

   ```hcl
   terraform {
     required_version = "1.10.5"

     required_providers {
       azurerm = {
         source  = "hashicorp/azurerm"
         version = "4.14.0"
       }
     }
   }
   ```

6. Put `provider` blocks only in the root module. The root turns on OIDC there. `hashicorp/azurerm` 4.x requires `subscription_id` in that block. Do not set `access_key` or `secret_key` on `aws`. Do not set a client secret on `azurerm`.

   ```hcl
   provider "azurerm" {
     features {}

     subscription_id = "00000000-0000-0000-0000-000000000000"
     use_oidc        = true
   }
   ```

7. A child that needs a second region declares `configuration_aliases` on its `required_providers` entry. The root passes that alias in the module `providers` argument. An alias that exists only inside the child is hidden. Reject it.
8. Publish to a registry or an immutable git tag. Callers pin that exact version. Never overwrite a published version. Never move a tag a caller already uses. A fix is a new version.

   ```hcl
   module "network" {
     source  = "example.com/team/network/azurerm"
     version = "1.4.2"
   }
   ```

   A git source follows the same rule: `git::https://example.com/network.git?ref=v1.4.2`. `ref=main` is not a pin.

9. Keep IAM and RBAC to the actions the module documents. Follow `principle-least-privilege`. A new grant is its own review, not a side effect of a rename.
10. Leave the backend to the root. State is remote and locked. A child that ships a backend forces every caller onto one state key.
11. When the module adds a larger SKU, a second region or a log archive, price it before callers adopt it. See `principle-cost-awareness`.

## Safety checks

- No child module contains a `provider` block, an access key, a storage account key or a client secret.
- Every variable has a type and a description. Every output has a description.
- Callers pin a registry version or a git tag, and that version is still the bytes that were reviewed.
- Pins match the reviewed release. These examples use Terraform `1.10.5`, `hashicorp/azurerm` `4.14.0` and `hashicorp/aws` `5.84.0`.
- Grants list actions and scope. See `principle-least-privilege`.
- The root uses a locked remote backend. Review a saved plan before apply. See `principle-change-safety`.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Roll back by pinning the previous module version in the caller and applying a saved plan. Do not republish old bytes over the new version. Follow `principle-rollback-first` before that pin reaches production. If the new version has already been applied, the reverse plan is the previous pin.

## Done when

- Inputs and outputs are typed and described, and validation rejects values that would plan the wrong thing.
- The published version is immutable, and every caller pins it.
- No child module configures a provider or hides an alias.
- A saved plan for a caller shows only the composition change you intended.
