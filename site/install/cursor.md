# Cursor

Cursor uses the plugin. The manifest is `.cursor-plugin/plugin.json`. It points `skills` at `./skills/` and `agents` at `./agents/`.

Install the jstack plugin from this repository. Do not also copy the same skills into the project. Two copies drift.

## What loaded looks like

Ask for a Terraform plan review, a pipeline change, or a ServiceNow change. The agent reads the matching `SKILL.md` before it edits. If several skills could fit, ask it to load `jay-mode` and take the first row.

The four agents are `terraform-reviewer`, `pipeline-doctor`, `cloud-security-reviewer`, and `incident-commander`. They live in `agents/`. A reviewer does not apply. The incident agent mitigates with the rehearsed rollback.

## Prove it

Open a file the change would touch and ask for the review, not the apply. A plan review names every destroy and does not run `terraform apply`. A workflow review names an unpinned action and does not edit the file in that pass.
