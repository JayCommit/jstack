---
name: azure-bicep-awareness
description: "Use when you read, preview or take over a Bicep or ARM stack. Compile and run what-if before you deploy, keep Bicep if it already owns an Azure-only stack, and move to Terraform only when the rest of the estate is Terraform."
license: MIT
---

# Bicep awareness

Read the template, compile it, and preview the deployment. One tool owns each resource.

## Use when

- You must read or change a Bicep file, an ARM template or a deployment stack.
- You are about to deploy to a resource group, a subscription or a management group.
- You want to move an Azure-only Bicep stack into Terraform.
- A generated JSON template is sitting unreviewed in the repository.

## Steps

1. Read `targetScope`, parameters, variables, resources, modules and outputs. Note each resource type, `apiVersion` and name expression. Implicit references are dependencies even when `dependsOn` is absent. Record whether a deployment stack already owns the resources.

2. Compile to check the file. Read the JSON only to understand the compile. Do not commit `main.json` unless someone reviewed that exact file. A generated template that nobody reviewed does not get merged.

   ```bash
   az bicep build --file main.bicep
   ```

3. Preview before you deploy. Read every create, modify and delete. Ignore a change only when you can say why it is noise. Follow `principle-change-safety`.

   ```bash
   az deployment group what-if --resource-group rg-example --template-file main.bicep --parameters main.bicepparam
   ```

4. Match the scope. Use `az deployment sub what-if --location uksouth` when `targetScope` is `subscription`. Use the management-group or tenant command when the template says so. Do not deploy a subscription template with `az deployment group`.

5. Leave the stack in Bicep when it is Azure-only and Bicep or a deployment stack already owns it. Do not start a Terraform copy of the same resources. Do not pass `--mode Complete` unless the change record lists every delete and a second person has approved it. The default mode is Incremental.

6. Move to Terraform only when the rest of that environment is already Terraform. Map each resource to an `azurerm` address. Pin the live names so Terraform does not rename or replace. Pin versions and store state as in `terraform-module-design` and `terraform-state-backends`.

   ```hcl
   import {
     to = azurerm_resource_group.example
     id = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-example"
   }
   ```

7. Import first, then plan. Run `terraform plan -out=tfplan`. Confirm there is no destroy and no replace. If there is, stop and fix the address or the arguments. Do not apply. Follow `principle-everything-as-code`.

8. After the plan is a no-op, remove those resources from the Bicep file or the deployment stack in the same reviewed change. Remove them only after the import is in state. Removing them first can delete them. Do not let both tools own the same resource. Not Bicep for deletes and Terraform for updates.

9. Authenticate the what-if and the apply with workload identity federation. No client secret and no service principal password. Parameter files in git must not contain secret values. Read those at deploy time from Key Vault. Follow `principle-no-static-credentials`, `principle-least-privilege` and `azure-key-vault`.

10. Name the blast radius: subscription, resource group, deployment name, stack name, state key and pipeline. One stack per change. A straight import should not change spend. If the plan changes a SKU, stop and follow `principle-cost-awareness`.

11. After a deploy, list the deployment before you call it done. A clean what-if is not a clean deploy. Read the error text before you rerun. Follow `principle-observe-before-you-fix`.

    ```bash
    az deployment group list --resource-group rg-example --output table
    ```

## Safety checks

- `az bicep build` succeeded, and the generated JSON is not committed unless it was reviewed.
- The what-if delete list is empty, or every delete is named on the change.
- Complete mode is not set, unless the approved change says so.
- A Terraform move uses an `import` block, an exact provider pin and locked remote state.
- The Terraform plan after import shows no destroy and no replace.
- Bicep no longer contains the resources Terraform now owns.
- The pipeline is federated, and no secret sits in a parameter file.
- The deployment list shows the operation you approved, not an older failure.

## Rollback

Write the rollback before production. Follow `principle-rollback-first`.

1. Redeploy the previous reviewed template. Run what-if on that template first. Do not use Complete mode to undo.
2. If the Terraform plan shows a destroy, do not apply. Revert the import change.
3. If a deployment failed, read the deployment error before you rerun it. Follow `principle-observe-before-you-fix`.
4. Rehearse the previous template on a non-production resource group.

## Done when

- You can say who owns each resource, Bicep or Terraform, and it is not both.
- The what-if or the Terraform plan matches the request and nothing else.
- No unreviewed generated template is in the commit.
- The change is verified in this environment before anyone promotes it.
