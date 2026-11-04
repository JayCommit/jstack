# Changelog

## Unreleased

Repository versions in `plugin.json` and `.cursor-plugin/plugin.json` stay at `0.0.1`. The `v0.1.0` tag is still open.

### Added

- `principle-stop-at-approval` tells the agent to prepare the diff and stop. A person approves, and the pipeline applies.
- `principle-resource-baseline` keeps names, tags, and delete protection on the scheme the estate already uses.
- `ops-backup-restore` names the recovery point and the restore time, and requires a restore of a copy before data is deleted.
- `ops-access-review` removes access a joiner, mover, or leaver no longer needs, and keeps break-glass out of daily use.
- `ops-certificates` renews TLS into the existing store and proves the new certificate before the old binding is removed.
- `pipelines-runners` keeps a runner you operate ephemeral, free of cloud keys, and off the path used by untrusted builds.
- `github-repositories` and `github-pull-requests` protect a GitHub repository and stop before the author approves or merges.
- `azuredevops-repositories` protects an Azure DevOps Git repository and its pull request without a policy bypass.
- `servicenow-queue`, `servicenow-incidents`, `servicenow-problems`, `servicenow-changes`, and `servicenow-requests` act as the signed-in user for day-2 incidents, problems, changes, and catalog requests.
- `jay-mode` classifies a request as an incident, a review, a pipeline change, or an infrastructure change, then loads the skill that owns it.
- `setup-jstack` installs the pack for Cursor, GitHub Copilot, or Claude Code and proves the copy with a dry run.
- Agents `terraform-reviewer`, `pipeline-doctor`, `cloud-security-reviewer`, and `incident-commander`, with the same files under `.github/agents/`.
- Copilot prompts `/plan-review`, `/pipeline-review`, `/postmortem`, and `/runbook`.
- Path instructions for Terraform, GitHub Actions, Azure DevOps, Bicep, Dockerfiles, Helm, PowerShell, and shell.
- `skills/<name>/tests/prompts.md` for every skill, checked by `tests/test_prompt_files.py`.
- Sample stack `examples/jstack-sample`: mocked Azure and AWS Terraform tests, OIDC pipeline examples, and a Helm chart.
- `examples/jstack-review` is a blinded plan and workflow review. `prompts.md` is the ask. `expected.md` is the answer key.
- [Operator guide](docs/operator-guide.md) covers a plan, a failing pipeline, a workflow review, and a ServiceNow change.
- MkDocs Material source under `site/` covers install, day-to-day use, examples, and removal. `scripts/render-docs.py` builds the catalog from skill frontmatter. The site publishes to [https://jaycommit.github.io/jstack/](https://jaycommit.github.io/jstack/).

### Changed

- The docs home is a short introduction, a compact session, and two indexes for install and jobs.
- Every playbook names `principle-stop-at-approval` in Safety checks. `scripts/lint-skills` warns when that line is missing. Principles stay exempt, because the playbook is what a direct match loads.
- `jay-mode` gives each request one skill. A failed Azure DevOps run and an Azure DevOps review both load `pipelines-azure-devops-yaml`, which reads the failing step before the YAML changes.
- `jay-mode` loads `principle-stop-at-approval` for every classification and `principle-resource-baseline` when the change creates a resource. Access reviews, runners, backups, and certificates each have a row.
- An incident whose mitigation is a restore follows `ops-backup-restore`. A certificate bind or renewal follows `ops-certificates`. Standing access in a security review follows `ops-access-review`.
- `pipeline-doctor` loads the GitHub Actions debugging skill or the Azure DevOps skill for that host, and keeps an Azure DevOps YAML defect in the Azure DevOps skill.
- Example asks record a later step on ask 2. `tests/test_prompt_files.py` fails when both asks record the same step.
- The AzureRM provider example in `terraform-module-design` sets `subscription_id`, which 4.x requires.
- `terraform-testing` allows a second `command = apply` run under `mock_provider` when plan leaves a set unknown. The AWS sample uses that run for ingress and for a `0.0.0.0/0` route.

Live trials in Cursor, GitHub Copilot, and Claude Code are still open.
