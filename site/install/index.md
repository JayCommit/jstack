# Install

Pick the tool. Then pick a scope: the whole pack, or a glob such as `terraform-*`.

<div class="jstack-choices">
<a class="jstack-choice" href="cursor/"><span class="jstack-tag">Plugin</span><strong>Cursor</strong><span>Install from this repository. Do not also copy the skills into the project.</span></a>
<a class="jstack-choice" href="copilot/"><span class="jstack-tag">Machine or repo</span><strong>GitHub Copilot</strong><span><code>gh skill install</code> for your user, or <code>scripts/sync</code> into one repository. Dry-run first.</span></a>
<a class="jstack-choice" href="other-agents/"><span class="jstack-tag">AGENTS.md</span><strong>Claude Code, Codex, Gemini</strong><span>Point the agent at <code>AGENTS.md</code>. Sync into <code>.agents/skills</code> or <code>.claude/skills</code>.</span></a>
<a class="jstack-choice" href="remove/"><span class="jstack-tag">Undo</span><strong>Remove</strong><span>There is no uninstall command. Delete the directory this repo installed, and nothing else.</span></a>
</div>

A repository with no cluster does not need the Kubernetes skills. A repository that does not use ServiceNow does not need those skills.

!!! note "Lint is for authors"

    `scripts/lint-skills` is not an install step. The authoring rules are on [Writing a skill](../writing-a-skill.md).

Do not paste skills into a chat, and do not copy secrets, kubeconfigs, or cloud keys into the target.
