# Secure defaults

Examples in this pack use placeholders. A real subscription, tenant, account, hostname, or address does not belong in a skill, a doc, or a commit.

| Placeholder | Stands for |
| --- | --- |
| `00000000-0000-0000-0000-000000000000` | Subscription, tenant, or object id |
| `123456789012` | AWS account id |
| `example.com` | A hostname you own |
| `example-org/example` | A GitHub repository |
| `rg-example` | A resource group |

## Which principle to load

| You are about to | Load |
| --- | --- |
| Log a pipeline or a workload in to Azure or AWS | `principle-no-static-credentials` |
| Grant IAM, RBAC, or `GITHUB_TOKEN` rights | `principle-least-privilege` |
| Change Terraform, a pipeline, or production | `principle-change-safety` and `principle-rollback-first` |
| Create a resource | `principle-resource-baseline` |
| Touch a failure you have not read yet | `principle-observe-before-you-fix` |
| Add cloud spend | `principle-cost-awareness` |
| Apply, merge, or grant | `principle-stop-at-approval` |

`jay-mode` loads `principle-stop-at-approval` for every classification, and `principle-resource-baseline` when the change creates a resource.

## Do not invent a second copy

Federation subjects stay in `principle-no-static-credentials`. Copy the `sub` claim from a token issued for that repository. Azure DevOps issuer and subject values are copied from the service connection. This page does not restate them.

The remote state procedure and the provider pins stay in `terraform-state-backends` and `terraform-module-design`. This page does not paste a backend block.

Skill text stays in `skills/<name>/SKILL.md`. The [catalog](catalog.md) links to those files. It does not paste the playbooks.
