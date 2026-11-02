# Prompts for terraform-static-analysis

Example asks for `terraform-static-analysis`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

A pull request adds or edits Terraform for Azure or AWS.

### Expected for ask 1

- Load `terraform-static-analysis` and follow that file through its own done-when.
- Step: Format-check the whole tree. Do not trust a laptop that formatted a different subset.
- Check: Pre-commit and the pipeline run the same commands.
- Done when: fmt, `terraform init -backend=false`, validate, tflint, Checkov and Trivy all run in pre-commit and on the pull request.

## Ask 2

Validate without touching state.

### Expected for ask 2

- Load `terraform-static-analysis` and follow that file through its own done-when.
- Step: Validate without touching state. `terraform init -backend=false` downloads the pinned providers and does not configure the backend. Commit `.terraform.lock.hcl` so init cannot float the provider. In PowerShell, stop when `$LASTEXITCODE` is not 0. Do not validate a half-initialised directory.
- Check: Plugins and providers are pinned. The lock file is in git.
- Done when: The pull request is red when any of those commands reports a new finding.
