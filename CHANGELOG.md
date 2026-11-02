# Changelog

## Unreleased

Repository versions in `plugin.json` and `.cursor-plugin/plugin.json` stay at `0.0.1`. The `v0.1.0` tag is still open.

### Added

- `jay-mode` classifies a request as an incident, a review, a pipeline change, or an infrastructure change, then loads the skill that owns it.
- `setup-jstack` installs the pack for Cursor, GitHub Copilot, or Claude Code and proves the copy with a dry run.
- Agents `terraform-reviewer`, `pipeline-doctor`, `cloud-security-reviewer`, and `incident-commander`, with the same files under `.github/agents/`.
- Copilot prompts `/plan-review`, `/pipeline-review`, `/postmortem`, and `/runbook`.
- Path instructions for Terraform, GitHub Actions, Azure DevOps, Bicep, Dockerfiles, Helm, PowerShell, and shell.
- `skills/<name>/tests/prompts.md` for every skill, checked by `tests/test_prompt_files.py`.
- Sample stack `examples/jstack-sample`: mocked Azure and AWS Terraform tests, OIDC pipeline examples, and a Helm chart.

### Changed

- `jay-mode` gives each request one skill. A failed Azure DevOps run and an Azure DevOps review both load `pipelines-azure-devops-yaml`, which reads the failing step before the YAML changes.
- `pipeline-doctor` loads the GitHub Actions debugging skill or the Azure DevOps skill for that host, and keeps an Azure DevOps YAML defect in the Azure DevOps skill.
- Example asks record a later step on ask 2. `tests/test_prompt_files.py` fails when both asks record the same step.
- The AzureRM provider example in `terraform-module-design` sets `subscription_id`, which 4.x requires.
- `terraform-testing` allows a second `command = apply` run under `mock_provider` when plan leaves a set unknown. The AWS sample uses that run for ingress and for a `0.0.0.0/0` route.

Live trials in Cursor, GitHub Copilot, and Claude Code are still open.
