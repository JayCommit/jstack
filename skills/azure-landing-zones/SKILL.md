---
name: azure-landing-zones
description: "Use when you add or change an Azure landing zone. Set the management group hierarchy, keep each subscription as the isolation boundary, and pin a reviewed hub or Virtual WAN module behind a federated pipeline identity."
license: MIT
---

# Azure landing zones

Place each workload in the existing landing-zone hierarchy. Do not add a second tree beside it.

## Use when

- You add a management group, a subscription, or a hub or Virtual WAN network.
- You move a subscription between management groups.
- A pipeline will create or update landing-zone resources.
- A portal edit has changed the hierarchy or a subscription placement.

## Steps

1. Read the current tree with `az account management-group list` and the subscription list. The hierarchy is Platform, with Identity, Management and Connectivity under it, plus Landing zones, Sandbox and Decommissioned. The `alz` architecture also places Corp and Online under Landing zones. Keep those groups. Do not add another root, a shadow platform group, or a parallel set of names.

2. Treat the subscription as the isolation boundary. Put the identity subscription under Identity, log analytics and state storage under Management, and the hub or Virtual WAN under Connectivity. Put each workload environment in its own subscription under Landing zones. Put experiments under Sandbox. Put subscriptions being emptied under Decommissioned, and do not deploy new resources there. Sandbox is not peered to production.

3. Pick one connectivity model per region. Use hub-and-spoke or Virtual WAN, the model the connectivity subscription already runs. Do not add the other model in the same change. Spoke and firewall detail is `azure-networking`.

4. Pin Terraform `1.10.5` and the reviewed module. `Azure/avm-ptn-alz/azurerm` `0.12.3` is the example pin. Replace that pin only with a release you have reviewed. That module requires `azure/alz` on the `0.17` line and `azure/azapi` on the `2.2` line. Pin the exact releases you reviewed, such as `azure/alz` `0.17.4` and `azure/azapi` `2.2.0`. Pin `hashicorp/azurerm` `4.14.0` when the same root also manages AzureRM resources. Do not use a floating constraint. An open range is not a pin.

5. Keep state in the management subscription, in a storage account that already exists before this apply. Use Azure AD auth and the backend blob lease as the lock. Do not pass a storage account key. Do not share the state key with another pipeline. Add `.alzlib` to `.gitignore`. Pass literals into the module. Do not set `depends_on` on it, and do not pass values that are known only after apply.

   ```hcl
   terraform {
     required_version = "1.10.5"

     required_providers {
       alz = {
         source  = "azure/alz"
         version = "0.17.4"
       }
       azapi = {
         source  = "azure/azapi"
         version = "2.2.0"
       }
       azurerm = {
         source  = "hashicorp/azurerm"
         version = "4.14.0"
       }
     }

     backend "azurerm" {
       resource_group_name  = "rg-example"
       storage_account_name = "stexampletfstate"
       container_name       = "tfstate"
       key                  = "landing-zones.tfstate"
       use_oidc             = true
       use_azuread_auth     = true
     }
   }

   module "landing_zones" {
     source  = "Azure/avm-ptn-alz/azurerm"
     version = "0.12.3"

     architecture_name  = "alz"
     location           = "uksouth"
     parent_resource_id = "00000000-0000-0000-0000-000000000000"
   }
   ```

6. Replace `parent_resource_id` with the tenant id from `az account show --query tenantId --output tsv`, or with the parent management group name. Do not prefix it with `/providers/Microsoft.Management/managementGroups/`.

7. Authenticate the pipeline with workload identity federation. No client secret, no storage account key, and no service principal password. Create the federated credential as in `azure-rbac-entra`. Scope the hierarchy identity to the management group it owns. Scope an application identity to the one landing-zone subscription it deploys. Do not reuse one identity for both. Keep Owner and User Access Administrator off both. Follow `principle-least-privilege` and `principle-no-static-credentials`.

8. Plan one change. Split hierarchy, connectivity and application resources into separate applies. Run `terraform plan -out=tfplan` and read every destroy, replace and role change. Name the blast radius: parent management group, subscriptions, region, state key and pipeline. Follow `principle-change-safety`. Put a budget on a new subscription before you call it done. Follow `principle-cost-awareness`.

9. If someone moved a subscription in the portal, import that placement or revert it. Do not leave the next apply to fight the portal. Follow `principle-everything-as-code`.

## Safety checks

- The groups match the hierarchy above, and no second tree was added.
- The module and provider versions are exact pins of releases you reviewed.
- State uses a locked remote backend and Azure AD auth. No account key is in the pipeline.
- The pipeline identity is federated and scoped only to the management group or subscription it owns.
- The plan contains no unexpected destroy, replace or Owner grant.
- The blast radius names the parent group, subscriptions, state key and pipeline.
- A new subscription has a budget alert, or the change does not create one.

## Rollback

Write the rollback before production. Follow `principle-rollback-first`. Rehearse it on a non-production parent.

1. Keep the previous module pin and the previous `tfplan` review notes.
2. Move a subscription back to its previous management group with a reviewed plan. Do not delete a management group that still has children.
3. Stop if the reverse plan destroys policy assignments you did not mean to drop. Fix the plan. Do not apply it.

## Done when

- The live tree matches the hierarchy in this skill and the reviewed plan.
- Each new workload has its own subscription in the correct group.
- Connectivity is hub-and-spoke or Virtual WAN, not a second model added beside it.
- The pipeline is federated, least privilege, and uses locked remote state.
- The change is verified in this environment before anyone promotes it.
