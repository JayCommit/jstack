# Prompts for terraform-testing

Example asks for `terraform-testing`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I change a module and need a check that fails the pull request.

### Expected for ask 1

- Load `terraform-testing` and follow that file through its own done-when.
- Step: Add a `.tftest.hcl` file next to the module. Set `command = plan`. Assert arguments that must not drift, such as region, SKU and address space.
- Check: Pull-request tests use `mock_provider`. A plan run covers arguments the plan knows. A mock apply covers values the plan leaves unknown. Neither calls production.
- Done when: `terraform test` passes on the pull request with plan asserts and mocked providers.

## Ask 2

Mock `azurerm` for an Azure module and `aws` for an AWS module.

### Expected for ask 2

- Load `terraform-testing` and follow that file through its own done-when.
- Step: Mock `azurerm` for an Azure module and `aws` for an AWS module. The mock does not call the cloud API. `terraform test` still installs the pinned provider so the schema is real. Pin Terraform `1.10.5`, `hashicorp/azurerm` `4.14.0` and `hashicorp/aws` `5.84.0`, or the later release that was reviewed.
- Check: The ephemeral account or subscription holds no production data, and its state key is not the production key.
- Done when: No test reads or writes production state.
