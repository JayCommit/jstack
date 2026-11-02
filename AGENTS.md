# AGENTS.md

This repo is jstack, a DevOps skill pack focused on Azure, AWS, Terraform and CI/CD pipelines (GitHub Actions, Azure DevOps). When working here:

- Each skill lives in `skills/<name>/SKILL.md`. The folder name and the `name` field must match and be lowercase-hyphenated.
- Every `SKILL.md` needs YAML frontmatter with `name` and `description`. The description says what the skill does and when to use it.
- Name skills by area prefix: `terraform-*`, `azure-*`, `aws-*`, `pipelines-*`, `k8s-*`, `gitops-*`, `policy-*`, `ops-*`, and `principle-*` for principles. `jay-mode` and `setup-jstack` are the only names without a prefix.
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

## AWS

- `aws-iam-least-privilege`: Write the API calls the job makes, validate the policy, and keep AdministratorAccess off pipelines. Load `skills/aws-iam-least-privilege/SKILL.md` when you add or widen IAM.
- `aws-organizations-scps`: Keep workloads out of the management account and treat an SCP as a ceiling. Load `skills/aws-organizations-scps/SKILL.md` when you add an account, an OU or an SCP.
- `aws-vpc`: Private data subnets, gateway endpoints for S3 and DynamoDB, and security groups as the main control. Load `skills/aws-vpc/SKILL.md` when you change a VPC, route, endpoint or Transit Gateway.
- `aws-eks`: Private API, Pod Identity for new pods, and one Kubernetes minor at a time. Load `skills/aws-eks/SKILL.md` when you create or upgrade EKS.
- `aws-ecs`: Fargate, a separate task role, and a circuit breaker on the service. Load `skills/aws-ecs/SKILL.md` when you create or deploy an ECS service.
- `aws-secrets-ssm`: Rotating credentials in Secrets Manager, other secrets as SecureString, and one ARN for the pipeline. Load `skills/aws-secrets-ssm/SKILL.md` when you store or read a secret.
- `aws-cloudwatch`: Retention on every log group, and an alarm on the symptom the user hits. Load `skills/aws-cloudwatch/SKILL.md` when you add logs, metrics, alarms or a dashboard.
- `aws-codepipeline-awareness`: Read the pipeline before you change it, and send a new deploy through GitHub Actions with OIDC. Load `skills/aws-codepipeline-awareness/SKILL.md` when you touch CodePipeline or CodeBuild.
- `aws-cost-review`: Estimate the change, set a budget, and include NAT, public IPv4 and cross-AZ transfer. Load `skills/aws-cost-review/SKILL.md` before a change that adds AWS spend.

## Pipelines

- `pipelines-github-actions-authoring`: Least-privilege `permissions:`, full-SHA pins, timeouts and concurrency, and event text kept out of `run:`. Load `skills/pipelines-github-actions-authoring/SKILL.md` when you write or change a GitHub Actions workflow.
- `pipelines-github-actions-debugging`: Read the failing step's log and the run's inputs before you change anything, and fix the cause rather than re-run. Load `skills/pipelines-github-actions-debugging/SKILL.md` when a workflow run fails or hangs.
- `pipelines-azure-devops-yaml`: YAML in the repo, stages for environments, build validation for pull requests, and workload identity service connections. Load `skills/pipelines-azure-devops-yaml/SKILL.md` when you write, change, or diagnose an Azure DevOps pipeline.
- `pipelines-oidc-federation`: Federate to Azure and AWS with a narrow subject and audience, and copy Azure DevOps issuer and subject values rather than guess them. Load `skills/pipelines-oidc-federation/SKILL.md` when a pipeline needs cloud access.
- `pipelines-environments-approvals`: Required reviewers, branch rules and environment secrets on production, with no admin bypass. Load `skills/pipelines-environments-approvals/SKILL.md` when you add or change a deploy gate.
- `pipelines-reusable-templates`: Pin shared workflows and actions to a commit SHA and Azure DevOps templates to a protected tag, and pass only the permissions and secrets each needs. Load `skills/pipelines-reusable-templates/SKILL.md` when you share pipeline logic across repos.
- `pipelines-terraform-workflow`: Lint with no credential, plan on the pull request, and apply the saved plan after approval. Load `skills/pipelines-terraform-workflow/SKILL.md` when a pipeline runs Terraform.
- `pipelines-artifacts-releases`: Build once, deploy the digest, and attach provenance and an SBOM. Load `skills/pipelines-artifacts-releases/SKILL.md` when you build, tag or promote an image or package.

## Platform

- `k8s-dockerfile-hardening`: Multi-stage build, a non-root user, a base image pinned by digest, and a scan before the push. Load `skills/k8s-dockerfile-hardening/SKILL.md` when you write or change a Dockerfile.
- `k8s-manifest-review`: Requests, a memory limit, probes, a restricted security context, a disruption budget and a NetworkPolicy. Load `skills/k8s-manifest-review/SKILL.md` when you add or review a Kubernetes workload.
- `k8s-helm-review`: A values schema, a rendered diff, and a rollback to the previous release. Load `skills/k8s-helm-review/SKILL.md` when you add or upgrade a Helm chart.
- `gitops-argocd-flux`: Promote a digest through overlays, and keep secrets in SOPS or External Secrets. Load `skills/gitops-argocd-flux/SKILL.md` when you deliver with Argo CD or Flux.
- `policy-as-code`: Conftest on the plan and the manifests, Azure Policy and admission in audit first, and SCPs left as the AWS ceiling. Load `skills/policy-as-code/SKILL.md` when you add or change a policy check.

## Operations

- `ops-observability-alerts`: Page on a fast error-budget burn, ticket on a slow one, and put one runbook on the alert. Load `skills/ops-observability-alerts/SKILL.md` when you add an SLO, an alert or a dashboard.
- `ops-incident-response`: Name a lead, mitigate with the rehearsed rollback, and update on a fixed cadence. Load `skills/ops-incident-response/SKILL.md` when production is failing.
- `ops-runbook-authoring`: One command, the output you expect, and who to call when it does not appear. Load `skills/ops-runbook-authoring/SKILL.md` when you write or change a runbook.
- `ops-postmortem`: A blameless timeline, contributing factors, and action items with owners and dates. Load `skills/ops-postmortem/SKILL.md` when a SEV1 or SEV2 is over.
- `ops-secrets-handling`: One home for a secret, and rotation before a leak is closed. Load `skills/ops-secrets-handling/SKILL.md` when you store a secret or one has leaked.
- `ops-rollback-plan`: The rehearsed rollback for a Terraform apply, a deploy, a migration, a network change or an IAM change. Load `skills/ops-rollback-plan/SKILL.md` before a change can reach production.
- `ops-blast-radius`: List the subscription or account, the shared network, the state key and the pipeline before you apply. Load `skills/ops-blast-radius/SKILL.md` when a change can reach past the one object you mean to edit.
- `ops-scripting-standards`: Fail closed, dry-run by default, and a second run changes nothing. Load `skills/ops-scripting-standards/SKILL.md` when you write a Bash, PowerShell or Python automation script.

## Modes

- `jay-mode`: Take the first matching row. That row names the one skill to load. Load `skills/jay-mode/SKILL.md` when several skills look relevant.
- `setup-jstack`: Install the pack for Cursor, Copilot, or Claude Code, and prove the copy with a dry run. Load `skills/setup-jstack/SKILL.md` when you install jstack or sync a subset of skills.

## Agents

Personas live in `agents/`. The same files are in `.github/agents/` for Copilot. Change `agents/` first, then copy again. Copilot slash prompts are `.github/prompts/*.prompt.md`. Path rules are `.github/instructions/*.instructions.md`.

- `terraform-reviewer`: Read the plan, flag destroys, grants, network edits, and provider bumps. Do not apply.
- `pipeline-doctor`: Read the failing step, then fix the cause. Do not re-run the same revision and call that the fix.
- `cloud-security-reviewer`: Review identity, exposure, and secrets. Do not grant access to clear a finding.
- `incident-commander`: Set severity from user impact, mitigate with the rehearsed rollback, and keep the update cadence.
