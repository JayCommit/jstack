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
