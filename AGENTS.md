# AGENTS.md

This repo is jstack, a DevOps skill pack focused on Azure, AWS, Terraform and CI/CD pipelines (GitHub Actions, Azure DevOps). When working here:

- Each skill lives in `skills/<name>/SKILL.md`. The folder name and the `name` field must match and be lowercase-hyphenated.
- Every `SKILL.md` needs YAML frontmatter with `name` and `description`. The description says what the skill does and when to use it.
- Name skills by area prefix: `terraform-*`, `azure-*`, `aws-*`, `pipelines-*`, `k8s-*`, `gitops-*`, `policy-*`, `ops-*`, and `principle-*` for principles.
- Default to secure cloud practice in every example: OIDC/workload identity federation over static keys, least-privilege IAM/RBAC, pinned provider and action versions, remote state with locking.
- Keep skills tool-neutral. Don't refer to tools that only one agent has without saying what to do elsewhere.
- Don't copy text from pstack or other sources. Write it fresh.
- Never put real secrets, subscription/tenant/account IDs, hostnames or IPs in examples. Use placeholders such as `00000000-0000-0000-0000-000000000000`, `123456789012` and `example.com`.

## Principles

- `principle-change-safety`: Read the plan, name the blast radius, change one thing at a time and promote through environments. Load `skills/principle-change-safety/SKILL.md` when changing Azure, AWS, Terraform or a pipeline.
- `principle-rollback-first`: Write and test the rollback before any production change. Load `skills/principle-rollback-first/SKILL.md` when a change touches production.
- `principle-least-privilege`: Grant only the IAM, RBAC and pipeline permissions the job needs. Load `skills/principle-least-privilege/SKILL.md` when adding or widening access, including `GITHUB_TOKEN` and service connections.
- `principle-no-static-credentials`: Use OIDC or workload identity federation and short-lived tokens. Load `skills/principle-no-static-credentials/SKILL.md` when a pipeline or workload authenticates to Azure or AWS.
- `principle-everything-as-code`: Codify console edits and import drift. Load `skills/principle-everything-as-code/SKILL.md` when resources change outside the repository.
- `principle-idempotent-automation`: Pipelines and scripts must be safe to rerun. Load `skills/principle-idempotent-automation/SKILL.md` when writing or rerunning automation.
- `principle-observe-before-you-fix`: Read the logs, metrics and errors before changing anything. Load `skills/principle-observe-before-you-fix/SKILL.md` when diagnosing a failure.
- `principle-cost-awareness`: Price a change before you ship it. Load `skills/principle-cost-awareness/SKILL.md` when a change can add cloud spend.

## Terraform

- `terraform-module-design`: Typed inputs and outputs, an immutable version pin, and provider blocks only in the root module. Load `skills/terraform-module-design/SKILL.md` when you add or change a Terraform module.
- `terraform-plan-review`: Read the full plan, flag destroys, grants, network edits, moves, imports and provider bumps, and apply only the saved plan. Load `skills/terraform-plan-review/SKILL.md` before a Terraform apply.
- `terraform-state-backends`: Remote state with locking on Azure Storage or S3, one key per environment, and separate moves, imports and migrations. Load `skills/terraform-state-backends/SKILL.md` when you add, move or recover state.
- `terraform-drift`: A scheduled plan detects drift. Triage Activity Log or CloudTrail, then update the code, import, or revert the live change. Load `skills/terraform-drift/SKILL.md` when a plan reports changes nobody shipped.
- `terraform-testing`: Plan assertions with `terraform test` and mocked providers. Apply only in an ephemeral account, then destroy from a saved plan. Load `skills/terraform-testing/SKILL.md` when a module change needs a test.
- `terraform-static-analysis`: Run fmt, validate, tflint, Checkov and Trivy in pre-commit and on the pull request. Load `skills/terraform-static-analysis/SKILL.md` when Terraform changes or you add those checks.
- `terraform-workspaces-environments`: One directory and backend key per environment. Promote a pinned module version. Load `skills/terraform-workspaces-environments/SKILL.md` when you lay out or promote environments.

## Azure

- `azure-landing-zones`: Keep the Platform, Landing zones, Sandbox and Decommissioned hierarchy, and pin the landing-zone module. Load `skills/azure-landing-zones/SKILL.md` when you add a management group, subscription or hub.
- `azure-rbac-entra`: Assign the narrowest role at the resource, use Privileged Identity Management for people, and federate pipeline identities. Load `skills/azure-rbac-entra/SKILL.md` when you grant Azure access.
- `azure-aks`: Private cluster, Azure CNI overlay, Azure RBAC and workload identity, with system and user pools split. Load `skills/azure-aks/SKILL.md` when you create or upgrade AKS.
- `azure-networking`: Hub and spoke, both peering directions, Azure Firewall, NSGs on spoke subnets, and Private DNS. Load `skills/azure-networking/SKILL.md` when you change VNets, routes, peerings or private endpoints.
- `azure-key-vault`: RBAC authorization, purge protection, a private endpoint, and a federated reader on the vault. Load `skills/azure-key-vault/SKILL.md` when you create a vault or grant access to it.
- `azure-bicep-awareness`: Compile, run what-if, and keep one owner per resource. Load `skills/azure-bicep-awareness/SKILL.md` when you read or take over a Bicep or ARM stack.
- `azure-cost-review`: Estimate the change, set a budget, right-size from metrics, and list orphaned resources. Load `skills/azure-cost-review/SKILL.md` before a change that adds Azure spend.
