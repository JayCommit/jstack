# AGENTS.md

This repo is jstack, a DevOps skill pack focused on Azure, AWS, Terraform and CI/CD pipelines (GitHub Actions, Azure DevOps). When working here:

- Each skill lives in `skills/<name>/SKILL.md`. The folder name and the `name` field must match and be lowercase-hyphenated.
- Every `SKILL.md` needs YAML frontmatter with `name` and `description`. The description says what the skill does and when to use it.
- Name skills by area prefix: `terraform-*`, `azure-*`, `aws-*`, `pipelines-*`, `k8s-*`, `gitops-*`, `policy-*`, `ops-*`, and `principle-*` for principles.
- Default to secure cloud practice in every example: OIDC/workload identity federation over static keys, least-privilege IAM/RBAC, pinned provider and action versions, remote state with locking.
- Keep skills tool-neutral. Don't refer to tools that only one agent has without saying what to do elsewhere.
- Don't copy text from pstack or other sources. Write it fresh.
- Never put real secrets, subscription/tenant/account IDs, hostnames or IPs in examples. Use placeholders such as `00000000-0000-0000-0000-000000000000`, `123456789012` and `example.com`.
