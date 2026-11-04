# Install

Pick the tool, then pick the scope. The scope is the whole pack, or a glob such as `terraform-*` and `principle-*`. A repository with no cluster does not need the Kubernetes skills. A repository that does not use ServiceNow does not need the ServiceNow skills.

| Tool | Page |
| --- | --- |
| Cursor | [Install for Cursor](cursor.md) |
| GitHub Copilot | [Install for GitHub Copilot](copilot.md) |
| Claude Code, Codex, Gemini CLI, and others | [Install for other agents](other-agents.md) |

When you want the pack gone, follow [Remove](remove.md).

`scripts/lint-skills` is for people editing this repository. It is not an install step. The authoring rules are on [Writing a skill](../writing-a-skill.md).

Do not paste skills into a chat, and do not copy secrets, kubeconfigs, or cloud keys into the target.
