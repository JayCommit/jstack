---
name: principle-everything-as-code
description: "Apply when Azure, AWS, Terraform or pipeline resources change, including a portal or console edit. Codify the change in the repository and import any drift so the next plan matches what is running."
license: MIT
---

# Everything as code

The repository is the source of truth for Azure, AWS and the pipelines that ship them. A console edit is drift until it is imported and reviewed as code.

## Use when

- Someone changes a resource in the Azure portal or the AWS console.
- Terraform shows a diff nobody authored in this change.
- A resource already exists and is not in state.
- A pipeline setting is changed in the GitHub or Azure DevOps UI.

## Rules

- Make the change in Terraform, or in the pipeline that applies it. If the portal or console was used, open a follow-up the same day to codify that edit.
- Bring an existing resource into state with an `import` block, then plan and apply through review. A one-off `terraform import` leaves no record in git.
- Run a scheduled plan. Pending changes are drift or an edit that has not been applied. Import the drift, revert it, or raise a reviewed change. Plan exit codes are in `principle-change-safety`.
- A click-fix that is left unimported is overwritten or duplicated on the next apply.
- Keep pipeline definitions and environment checks in code where the platform allows it. A UI-only edit still needs a reviewed follow-up.
- Treat `terraform plan -generate-config-out` as a draft. Rename resources, drop unused arguments and strip secret material before you commit it. See `principle-no-static-credentials`.
- Keep the rollback in code as well, so a revert is another reviewed plan. See `principle-rollback-first`.

```hcl
import {
  to = azurerm_resource_group.example
  id = "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/example"
}
```

## Red flags

- Production was fixed in the portal and the code was left stale.
- Resources in the subscription or account belong to no state and no owner.
- The next apply would overwrite a live hotfix.
- A scheduled plan reports changes and nobody is assigned to triage them.
- Role assignments exist in the portal and not in Terraform.

## Done when

- The desired change is in reviewed code.
- An imported resource plans with no unexpected diff.
- Console drift has been imported or deliberately reverted.
