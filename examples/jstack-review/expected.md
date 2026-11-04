# Answer key

Open this file only after the review is written. The prompts do not name these findings.

## Plan

- `azurerm_linux_virtual_machine.app` will be destroyed. That is a stop.
- Do not apply the plan.
- The packet names subscription `00000000-0000-0000-0000-000000000000`, resource group `rg-example`, region `uksouth`, state key `example-prod.tfstate`, environment `production`, and pipeline `example-org/example`.
- The provider line is `hashicorp/azurerm` `v4.14.0` and Terraform `v1.10.5`. Those pins match the pack. A review that flags a provider bump on this file is wrong.

## Workflow

- `actions/checkout@v4` is a moving tag. The skill requires a full commit SHA and a version comment.
- `azure/login@v2` is a moving tag. The skill requires a full commit SHA and a version comment.
- `permissions: contents: write` is wider than `contents: read`. A cloud login uses `id-token: write` on that job only.
- The job sets `AWS_ACCESS_KEY_ID` to `example-access-key` and `AWS_SECRET_ACCESS_KEY` to `example-secret-key`. Those are static credentials. The login is federation.
- `azure/login` reads `secrets.AZURE_CREDENTIALS`. That is a stored credential. The login is workload identity federation.
- The job has no `timeout-minutes`.
- The deploy has no `concurrency` group, and `cancel-in-progress` is unset.
- Checkout does not set `persist-credentials: false`.
- The deploy does not wait on an environment.
- Do not change the file as part of the review. A fix is a separate change.
