---
name: azure-rbac-entra
description: "Use when you grant Azure RBAC or Entra access to a person, a workload or a pipeline. Assign the narrowest built-in or custom role at the resource, use Privileged Identity Management for people, and federate pipeline identities."
license: MIT
---

# Azure RBAC and Entra

Grant the actions the job needs, at the smallest scope that covers them. Do not grant a standing Owner.

## Use when

- You add or widen a role assignment for a person, a group, a workload or a pipeline.
- You choose a built-in role or write a custom role.
- A GitHub Actions or Azure DevOps pipeline needs a federated credential.
- A plan or template adds `Microsoft.Authorization/roleAssignments/write`.

## Steps

1. List who needs access, which API calls they make, and which resource they touch. Include data actions. Run `az role assignment list --scope /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-example --include-inherited --output table` before you add anything.

2. Assign at the resource or the resource group. Use a subscription or management group only when the job owns that whole scope. Follow `principle-least-privilege`.

3. Use a built-in role when its actions match the job and it adds no extra write. Typical matches are Reader, Key Vault Secrets User, AcrPull, and Azure Kubernetes Service RBAC Writer. Reject Contributor on a subscription when the job deploys one resource group.

4. Write a custom role when every built-in role is wider than the API calls you listed. Put only those actions and data actions in the role. Set `AssignableScopes` to the resource group or the resource, not the tenant.

   ```text
   {
     "Name": "example-rg-reader-restart",
     "IsCustom": true,
     "Actions": [
       "Microsoft.Resources/subscriptions/resourceGroups/read",
       "Microsoft.Compute/virtualMachines/read",
       "Microsoft.Compute/virtualMachines/restart/action"
     ],
     "NotActions": [],
     "DataActions": [],
     "AssignableScopes": [
       "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-example"
     ]
   }
   ```

5. Create and assign that role. Do not use a wildcard action.

   ```bash
   az role definition create --role-definition ./example-role.json
   az role assignment create --assignee-object-id 00000000-0000-0000-0000-000000000000 --assignee-principal-type ServicePrincipal --role example-rg-reader-restart --scope /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-example
   ```

6. Give people Privileged Identity Management, not a standing active Owner. Use an Entra group. Make the assignment eligible, with an end date. Set activation to the shortest window the task needs, and require approval for Owner. Remove the eligible assignment when the task ends.

7. Give each workload a user-assigned managed identity. Do not create a service principal password. Do not use a system-assigned identity for a pipeline or for a pod that must survive a resource replacement.

8. Federate GitHub Actions to that user-assigned identity. Issuer `https://token.actions.githubusercontent.com`. Audience `api://AzureADTokenExchange`. Copy the subject from a token for this repository. The subject forms live in `principle-no-static-credentials`. The command below uses the immutable subject for a repository created after 15 July 2026. A repository that still uses name-only subjects omits `@123456` and `@456789`. Use one environment, or one ref when the platform has no environment. Match only that subject. The deploy job sets `id-token: write` and `contents: read`. It stores no cloud key.

   ```bash
   az identity federated-credential create --name github-prod-example --identity-name id-example --resource-group rg-example --issuer https://token.actions.githubusercontent.com --subject repo:example-org@123456/example-repo@456789:environment:production --audiences api://AzureADTokenExchange
   ```

9. For Azure DevOps, use an Azure Resource Manager service connection with workload identity federation. Copy the issuer and the subject from the connection. Do not type them. Scope the connection to the resource group or subscription it deploys.

10. Keep Owner, User Access Administrator and Role Based Access Control Administrator off pipeline identities. Those roles can grant Owner. If a pipeline must create role assignments, use a custom role limited to the role definitions it assigns, at that scope only.

11. If Terraform applies the assignment, pin `hashicorp/azurerm` `4.14.0` and Terraform `1.10.5`. Use a remote backend with the blob lease lock and `use_azuread_auth`. Save `terraform plan -out=tfplan`. A new role assignment is a production-class change. Follow `principle-change-safety`. Codify a portal grant or remove it. Follow `principle-everything-as-code`.

## Safety checks

- The actions and the scope match the job. No wildcard write.
- People have an eligible PIM assignment with an end date, not standing Owner.
- The pipeline identity is federated. No client secret, password or storage account key is stored.
- The federated subject matches a token from this repository: one environment, or one ref.
- Owner, User Access Administrator and Role Based Access Control Administrator are not on the pipeline identity.
- The plan or `az role assignment list` output shows this grant and no extra grant.

## Rollback

Write the rollback before production. Follow `principle-rollback-first`.

1. Delete the role assignment you added: `az role assignment delete --ids 00000000-0000-0000-0000-000000000000`.
2. Remove the eligible PIM assignment the same way you created it. Do not leave an active Owner behind.
3. Delete the federated credential if the subject was wrong. Leave the identity in place if other workloads still use it.
4. Rehearse the delete on a non-production scope before you rely on it in production.

## Done when

- Each identity has one role, one scope and a named job.
- Human access expires through PIM. Workload and pipeline access is federated.
- The reviewed plan or the assignment list matches the request and nothing else.
- A wider grant has an end date or a tracked follow-up to narrow it.
