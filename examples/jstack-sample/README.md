# jstack sample

A fixture for trying the pack. Nothing in this directory is applied to Azure or AWS. GitHub Actions runs only the workflows in the repository root, so `examples/jstack-sample/.github/workflows/deploy.yml` is an example, not a live deploy.

## Terraform

`terraform/azure` is a resource group, a virtual network, a subnet, and a subnet NSG in `uksouth`. It has no public IP. `terraform/aws` is a VPC `10.0.0.0/16`, a private subnet, a route table with no `0.0.0.0/0` route, an S3 gateway endpoint, and a security group with no ingress from the internet. Region `eu-west-2`. Account `123456789012` and subscription `00000000-0000-0000-0000-000000000000` are placeholders.

Tests use `mock_provider`. The Azure file asserts on `command = plan`. The AWS file adds a mock `command = apply` so the empty ingress set and the absence of a `0.0.0.0/0` route are known. Follow `terraform-testing`. Pins are Terraform `1.10.5`, `hashicorp/azurerm` `4.14.0`, and `hashicorp/aws` `5.84.0`.

`backend.tf.example` is the remote backend with locking. It is not named `.tf`, so `terraform test` does not load it. A live root copies that file to `backend.tf` and passes the state key with `-backend-config`. Follow `terraform-state-backends`. Dev, test, and prod each get their own key.

```text
terraform init -input=false -backend=false
terraform test
```

## Pipelines

`azure-pipelines.yml` and `.github/workflows/deploy.yml` show workload identity federation. They store no client secret and no access key. The Azure DevOps issuer and subject come from the service connection. Follow `pipelines-oidc-federation`. Do not copy a guessed issuer out of this sample.

## Helm

`charts/example` is a non-root Deployment pinned by digest, with a values schema and a disruption budget. The namespace comes from `.Release.Namespace`. A default-deny NetworkPolicy selects every pod. A second policy allows port 8080 only from pods labelled `app: example-client`, and allows DNS egress. The chart has no dependencies, so there is no `Chart.lock`. Follow `k8s-helm-review` and `k8s-manifest-review`. The chart is not installed by CI.

## What this sample does not do

Cursor, Copilot, and Claude Code trials of the pack are still open. The repository tag `v0.1.0` is not cut here.
