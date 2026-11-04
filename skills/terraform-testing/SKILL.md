---
name: terraform-testing
description: "Test Terraform modules before they ship to Azure or AWS. Use when a module change needs a plan assertion with mocked providers, or a short-lived apply in an ephemeral test subscription or account."
license: MIT
---

# Testing

Assert on a plan with `terraform test`. Apply only when the plan cannot answer the question, and destroy that stack before the job ends.

## Use when

- You change a module and need a check that fails the pull request.
- You want to assert arguments without calling Azure or AWS.
- A behaviour is invisible in the plan and needs a real apply.
- A test job might touch production state or leave resources behind.

## Steps

1. Add a `.tftest.hcl` file next to the module. Set `command = plan`. Assert arguments that must not drift, such as region, SKU and address space.
2. Mock `azurerm` for an Azure module and `aws` for an AWS module. The mock does not call the cloud API. `terraform test` still installs the pinned provider so the schema is real. Pin Terraform `1.10.5`, `hashicorp/azurerm` `4.14.0` and `hashicorp/aws` `5.84.0`, or the later release that was reviewed.

   ```hcl
   mock_provider "azurerm" {}

   mock_provider "aws" {}

   run "plan_network" {
     command = plan

     variables {
       location = "westeurope"
     }

     assert {
       condition     = azurerm_resource_group.this.location == "westeurope"
       error_message = "Resource group location must be westeurope."
     }
   }
   ```

3. Run the tests from the module directory. A failing assert fails the job. Do not skip a run to go green.

   ```text
   terraform test
   ```

4. Do not point tests at production state. `terraform test` keeps temporary state for the run. Do not pass a production backend key and do not export a production state path.
5. Use Terratest only when the test must apply to a real cloud. A provisioner side effect or a contract the plan cannot see is that case. A normal argument check stays on `command = plan`. When `mock_provider` leaves a set unknown during plan, add a second run with `command = apply` in that same file. The mock still does not call Azure or AWS. Do not set `command = apply` against live providers on every pull request.
6. Run that apply in an ephemeral subscription or account that holds no production data. Examples use subscription `00000000-0000-0000-0000-000000000000` and account `123456789012`. Never paste a real id. Authenticate with OIDC or workload identity federation. See `principle-no-static-credentials`. Grant only that ephemeral scope. See `principle-least-privilege`.
7. Give the ephemeral job its own remote state key with locking. It is not the production key. Review the apply plan before that job applies it. See `principle-change-safety`.
8. Destroy at the end of the same job. Save the destroy plan, then apply that file. In PowerShell, apply only when the plan command leaves `$LASTEXITCODE` at 0. If destroy fails, the job fails.

   ```text
   terraform plan -destroy -input=false -out=tfplan-destroy
   ```

   ```text
   terraform apply -input=false tfplan-destroy
   ```

9. A second run of the same test must pass with no leftovers. See `principle-idempotent-automation`. Keep the ephemeral stack small. If a failed destroy can add spend, price that risk. See `principle-cost-awareness`.
10. Do not commit `tfplan`, `tfplan-destroy` or any state file. Do not put keys in a `variables` block inside the test.

## Safety checks

- Pull-request tests use `mock_provider`. A plan run covers arguments the plan knows. A mock apply covers values the plan leaves unknown. Neither calls production.
- The ephemeral account or subscription holds no production data, and its state key is not the production key.
- Destroy is a saved plan applied at the end of the same job.
- The test identity is federated and cannot write production state.
- Provider versions in the test match the pins that were reviewed.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Destroy is the rollback for an ephemeral apply. Run the saved destroy plan. If destroy fails, keep the job red and remove the leftovers from the ephemeral account before the next run. Do not delete them from production. Follow `principle-rollback-first` if a test ever touched a shared environment, and stop the suite until that is closed.

## Done when

- `terraform test` passes on the pull request with plan asserts and mocked providers.
- No test reads or writes production state.
- Any real apply ran in an ephemeral subscription or account and was destroyed with a saved plan.
- A rerun does not fail on leftovers and does not create a second copy of the stack.
