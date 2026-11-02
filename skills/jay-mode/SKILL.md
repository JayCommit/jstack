---
name: jay-mode
description: "Use when a request covers Azure, AWS, Terraform, or a pipeline and more than one skill could fit. Take the first matching row. That row names the one skill to load."
license: MIT
---

# Jay mode

Pick one playbook before you edit anything. The playbook names the skill. The skill does the work. This file does not replace it.

## Use when

- A request could be an infrastructure change, a pipeline change, a review, or an incident.
- Several skills look relevant and you need to choose the one to load.
- You are about to invent steps that `AGENTS.md` already points at a skill for.

## Steps

1. Read the request and take the first row that fits. The rows already put user impact before a review, and a review before a change.

   | Request | Playbook | Load |
   | --- | --- | --- |
   | Production is failing, or an alert is paging | Incident | `ops-incident-response` |
   | A GitHub Actions run failed, hung, or stayed queued | Pipeline | `pipelines-github-actions-debugging` |
   | An Azure DevOps run failed or hung | Pipeline | `pipelines-azure-devops-yaml` |
   | Review a Terraform plan, and do not apply it | Review | `terraform-plan-review` |
   | Lint or scan Terraform | Review | `terraform-static-analysis` |
   | A plan shows changes nobody shipped | Review | `terraform-drift` |
   | Review a GitHub Actions workflow, and do not apply it | Review | `pipelines-github-actions-authoring` |
   | Review an Azure DevOps pipeline, and do not apply it | Review | `pipelines-azure-devops-yaml` |
   | Review a Dockerfile | Review | `k8s-dockerfile-hardening` |
   | Review a Helm chart | Review | `k8s-helm-review` |
   | Review a Kubernetes manifest | Review | `k8s-manifest-review` |
   | Review Azure RBAC or Entra access | Review | `azure-rbac-entra` |
   | Review AWS IAM | Review | `aws-iam-least-privilege` |
   | Review Azure network exposure | Review | `azure-networking` |
   | Review AWS network exposure | Review | `aws-vpc` |
   | Review Azure spend or a bill | Review | `azure-cost-review` |
   | Review AWS spend or a bill | Review | `aws-cost-review` |
   | Review a secret or a leak | Review | `ops-secrets-handling` |
   | Add or change a GitHub Actions workflow | Pipeline | `pipelines-github-actions-authoring` |
   | Add or change an Azure DevOps pipeline | Pipeline | `pipelines-azure-devops-yaml` |
   | Create or change Azure, AWS, Terraform, Kubernetes, or policy | Infra | The one area skill `AGENTS.md` names for that resource |

2. Load that one skill. Follow its steps, safety checks, rollback, and done-when. The infra row is the only row that still needs `AGENTS.md` to name the skill. Do not copy the skill into the answer and then skip the file.

3. Load the principles that apply. An incident also loads `principle-observe-before-you-fix`. A production change also loads `principle-change-safety` and `principle-rollback-first`. A new or wider permission loads `principle-least-privilege`. A cloud login loads `principle-no-static-credentials`. A rerun loads `principle-idempotent-automation`. Spend loads `principle-cost-awareness`. A console edit loads `principle-everything-as-code`.

4. Name the blast radius before the first edit: subscription or account, region, state key or cluster, and pipeline. Follow `ops-blast-radius` when the change can reach past the one object in the request.

5. One playbook per change. A review that finds a defect becomes a separate change. An incident mitigation is the rehearsed rollback, not a new design.

## Safety checks

- The playbook is one of incident, review, pipeline, or infra.
- The skill that owns the work was loaded, not summarised from memory.
- Production work has a rollback. Follow `principle-rollback-first`.
- The blast radius is named before an edit.
- No static cloud key is introduced while choosing a skill.

## Rollback

Stop the change if the classification was wrong. The rollback of an edit that already shipped is the rollback in the skill you loaded, not a new path invented here. Follow `ops-rollback-plan`.

## Done when

- The request is classified, and the skill for that row has been followed through its own done-when.
- The principles for that row were loaded.
- No second playbook was mixed into the same change.
