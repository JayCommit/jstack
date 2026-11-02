# Prompts for policy-as-code

Example asks for `policy-as-code`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I add an OPA or Conftest rule for a Terraform plan or a Kubernetes manifest.

### Expected for ask 1

- Load `policy-as-code` and follow that file through its own done-when.
- Step: Write down the decision the rule enforces. One rule is one change. A storage account is not public. A container runs as non-root. A production resource carries the tag you require. Generic Terraform scans stay in `terraform-static-analysis`. This skill is for the rule those scans do not encode.
- Check: The rule encodes one decision, and Checkov or Trivy is not being asked to carry it instead. Those stay in `terraform-static-analysis`.
- Done when: A bad plan or a bad manifest fails in CI, and a good one passes.

## Ask 2

Test the plan JSON with Conftest.

### Expected for ask 2

- Load `policy-as-code` and follow that file through its own done-when.
- Step: Test the plan JSON with Conftest. `terraform show -json` can print secret values. Keep the file out of a public artefact. Follow `pipelines-terraform-workflow` for how the plan is stored. The policy job can read the repo and cannot apply. Follow `principle-least-privilege`.
- Check: Conftest is pinned, the policy bundle is pinned, and a deny fails the pull request.
- Done when: Cloud and admission policies are still in the mode you chose, audit or enforce.
