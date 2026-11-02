# Prompts for pipelines-terraform-workflow

Example asks for `pipelines-terraform-workflow`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

A pull request changes Terraform, tfvars or `.terraform.lock.hcl` for Azure or AWS.

### Expected for ask 1

- Load `pipelines-terraform-workflow` and follow that file through its own done-when.
- Step: On the pull request, run fmt, validate, tflint, Checkov and Trivy with no cloud credential. Follow `terraform-static-analysis`. That job keeps `permissions: contents: read`, sets `timeout-minutes`, and does not set `id-token: write`.
- Check: The lint job has no cloud credential and no `id-token: write`.
- Done when: fmt, validate, tflint, Checkov and Trivy ran without a cloud credential.

## Ask 2

Use two federated identities per environment.

### Expected for ask 2

- Load `pipelines-terraform-workflow` and follow that file through its own done-when.
- Step: Use two federated identities per environment. Follow `pipelines-oidc-federation`, `aws-iam-least-privilege` and `azure-rbac-entra`. The plan identity reads the cloud and the state. It trusts the `:pull_request` subject and the `:ref:refs/heads/main` subject. The apply identity can change the stack and trusts only `:environment:production`. A plan takes the state lock, so the plan identity also needs the lock permission. If you keep it strictly read-only, run pull-request plans with `-lock=false` and never apply one of them.
- Check: Plan and apply use different identities. The plan identity cannot change resources.
- Done when: The pull request showed a plan summary, and the reviewed change merged.
