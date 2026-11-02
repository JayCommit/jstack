---
name: terraform-static-analysis
description: "Run Terraform fmt, validate, tflint, Checkov and Trivy on Azure and AWS code. Use when a pull request changes Terraform, or when you wire the same checks into pre-commit and the pipeline."
license: MIT
---

# Static analysis

Fail the pull request on new findings. Pre-commit and the pipeline run the same commands. Do not disable a check to go green.

## Use when

- A pull request adds or edits Terraform for Azure or AWS.
- You add a pipeline or a pre-commit hook for that code.
- A check is red and someone wants it skipped.
- A tfsec job is still the source of findings and must move to Trivy.

## Steps

1. Format-check the whole tree. Do not trust a laptop that formatted a different subset.

```text
terraform fmt -check -recursive
```

2. Validate without touching state. `terraform init -backend=false` downloads the pinned providers and does not configure the backend. Commit `.terraform.lock.hcl` so init cannot float the provider. In PowerShell, stop when `$LASTEXITCODE` is not 0. Do not validate a half-initialised directory.

```text
terraform init -backend=false -input=false
```

```text
terraform validate
```

3. Pin the tflint plugins for `azurerm` and `aws` in `.tflint.hcl`. Pin the plugin release that was reviewed. Install, then lint. Stop if `tflint --init` fails.

```hcl
plugin "azurerm" {
  enabled = true
  version = "0.32.0"
  source  = "github.com/terraform-linters/tflint-ruleset-azurerm"
}

plugin "aws" {
  enabled = true
  version = "0.37.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}
```

```text
tflint --init
```

```text
tflint --recursive
```

4. Run Checkov for Terraform and Trivy for config. tfsec findings now come from Trivy. Do not keep a second tfsec job. Trivy exits 0 unless you set an exit code, so set one. A scan that cannot fail the job is not a check.

```text
checkov -d . --framework terraform
```

```text
trivy config --exit-code 1 .
```

5. Pin the providers the scan trusts. These examples use Terraform `1.10.5`, `hashicorp/azurerm` `4.14.0` and `hashicorp/aws` `5.84.0`, or the later release that was reviewed. A lock-file bump is a reviewed change, not a side effect of init.
6. Put the same commands in pre-commit and in the pull-request pipeline. A local pass does not replace the pipeline. The pipeline runs them on the merge commit.
7. Give the lint job no cloud credential. Keep `permissions` at `contents: read`. Do not set `id-token: write` on a job that only lints. See `principle-least-privilege`. Do not store an access key, a storage account key or a client secret for this job. See `principle-no-static-credentials`.

```yaml
permissions:
  contents: read

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.10.5
      - name: Format
        shell: pwsh
        run: terraform fmt -check -recursive
```

Pin the action release that was reviewed. Add one step per command so a non-zero exit fails the job. Do not chain commands with `&&`.

8. Fail on a new finding from fmt, validate, tflint, Checkov or Trivy. A suppression needs the rule id, the reason, and an expiry or a tracked follow-up. A skip with no reason is a defect. Do not widen a global ignore to clear one resource.
9. Code that later applies still uses a locked remote backend. This job does not init that backend and does not plan. Plan review stays a separate gate. See `principle-change-safety`.

## Safety checks

- Pre-commit and the pipeline run the same commands.
- Plugins and providers are pinned. The lock file is in git.
- The lint job has `contents: read` and no cloud key.
- Trivy is set to fail the job. tfsec is not a second source of truth.
- Every suppression names a rule, a reason and an expiry or a follow-up.

## Rollback

Roll a bad plugin or action pin back by restoring the previous pin and re-running the pipeline. Do not roll back by deleting the check. If a suppression let a bad change reach production, revert that change in a new review. Follow `principle-rollback-first`. Do not force-merge to go green.

## Done when

- fmt, `terraform init -backend=false`, validate, tflint, Checkov and Trivy all run in pre-commit and on the pull request.
- The pull request is red when any of those commands reports a new finding.
- Suppressions that remain are tracked, scoped and explained.
- The lint job uses no static cloud credential.
