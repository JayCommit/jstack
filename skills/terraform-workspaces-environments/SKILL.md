---
name: terraform-workspaces-environments
description: "Separate Terraform environments for Azure and AWS. Use when you choose a directory, workspace or Terragrunt layout, or when you promote one pinned module version to the next environment."
license: MIT
---

# Environments

Give each environment its own state key. Promote a module version. Do not copy state.

## Use when

- You lay out dev, test and prod for Azure or AWS.
- A stack is small and someone suggests workspaces instead of directories.
- Many accounts call one module and only inputs change.
- You promote a module from one environment to the next.

## Steps

1. Prefer one directory per environment. Apply from that directory so the state key is obvious. Do not also use workspaces inside those directories. Two mechanisms hide which state you wrote.

   ```text
   live/dev
   live/test
   live/prod
   ```

2. Give each directory its own backend key. Keep the storage account or bucket in shared partial config. Keep the key in the environment file. Dev, test and prod must not share a key.

   ```hcl
   key = "app/dev.tfstate"
   ```

   Init from that directory. The backend is remote and locked. Azure uses a blob lease and `use_azuread_auth = true`. A new S3 backend uses `encrypt = true` and `use_lockfile = true` on Terraform 1.10 or newer. Pin Terraform `1.10.5` or the later release that was reviewed. Authenticate with OIDC. See `principle-no-static-credentials`.

3. Put names and sizes in `terraform.tfvars` in that directory. Terraform loads that file. Do not keep `prod.tfvars` beside dev. Allowed values are the environment name, region, SKU, instance count and RFC1918 ranges such as `10.10.0.0/16`. Do not put tokens, keys or client secrets in tfvars.
4. Use a workspace only when the stack is small and a directory per environment would be noise. Workspaces share one backend and differ by a suffix. Print the active workspace before plan and before apply. Stop if the name is not the environment you mean.

   ```text
   terraform workspace show
   ```

   `terraform workspace select prod` in a shared directory is easy to get wrong. Directories are the default for that reason.

5. Use Terragrunt when many accounts share one module and only inputs change. Pin `source` to a tag. Do not point it at a branch. Each unit still has its own locked remote state.

   ```hcl
   terraform {
     source = "git::https://example.com/modules/network.git?ref=v1.4.2"
   }

   inputs = {
     environment = "dev"
     location    = "westeurope"
   }
   ```

6. Promote by shipping that same tag or registry version to the next environment. Plan there, review the saved plan, then apply that file. See `principle-change-safety`. For Terragrunt, pass the same flags: `terragrunt plan -out=tfplan`, then `terragrunt apply tfplan`. Do not copy state between environments. Do not `terraform state pull` from prod to seed dev.
7. Keep provider pins on the reviewed release, such as `hashicorp/azurerm` `4.14.0` and `hashicorp/aws` `5.84.0`. The identity for each environment is federated and scoped to that subscription or account. See `principle-least-privilege`.
8. Prod may cost more than dev. Price the difference before you promote a larger SKU. See `principle-cost-awareness`. Write the prod rollback before the prod apply. See `principle-rollback-first`.
9. A second plan against the same directory and the same inputs must exit 0. See `principle-idempotent-automation`.
10. Plan and apply from that directory. `-chdir` does not change the PowerShell location, so the next command cannot land in prod by accident. Apply only when the plan exits 0. Read `$LASTEXITCODE`.

    ```text
    terraform -chdir=live/dev plan -input=false -out=tfplan
    ```

    ```text
    terraform -chdir=live/dev apply -input=false tfplan
    ```

## Safety checks

- Each environment has its own state key, and the key is named on the pull request.
- The directory, or the printed workspace, matches the environment you apply.
- tfvars hold names and sizes, not secrets.
- The version promoted to prod is the version already applied and checked in the lower environment.
- Workspaces are not mixed with per-environment directories on the same stack.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Roll one environment back by pinning the previous module version in that environment only, then apply a saved plan. Do not roll prod back by copying dev state or by selecting another workspace. Follow `principle-rollback-first`. Other environments stay on their current pin until you promote again.

## Done when

- Dev, test and prod each have a distinct backend key, or a workspace is used and its name was printed before apply.
- The change promotes one pinned module version, not a copy of state.
- tfvars for the environment contain names and sizes only.
- The lower environment was checked before prod, and a second plan there exited 0.
