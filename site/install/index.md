# Install

Pick the tool. Then pick a scope: the whole pack, or a glob such as `terraform-*`.

<div class="jstack-cards">
<a class="jstack-card" href="cursor/"><span class="jstack-card-head"><strong>Cursor</strong><span class="jstack-pill">Plugin</span></span><span class="jstack-card-copy">Install from this repository. Do not also copy the skills into the project.</span><span class="jstack-specs"><span><span>Reads</span><span>plugin.json</span></span><span><span>Also copy</span><span>No</span></span></span><span class="jstack-card-go">Open steps</span></a>
<a class="jstack-card" href="copilot/"><span class="jstack-card-head"><strong>GitHub Copilot</strong><span class="jstack-pill">Machine or repo</span></span><span class="jstack-card-copy"><code>gh skill install</code> for your user, or <code>scripts/sync</code> into one repository. Dry-run first.</span><span class="jstack-specs"><span><span>Machine</span><span>your user</span></span><span><span>Repository</span><span>scripts/sync</span></span></span><span class="jstack-card-go">Open steps</span></a>
<a class="jstack-card" href="other-agents/"><span class="jstack-card-head"><strong>Claude Code, Codex, Gemini</strong><span class="jstack-pill">AGENTS.md</span></span><span class="jstack-card-copy">Point the agent at <code>AGENTS.md</code>. Sync into <code>.agents/skills</code> or <code>.claude/skills</code>.</span><span class="jstack-specs"><span><span>Index</span><span>AGENTS.md</span></span><span><span>Copy</span><span>.agents/skills</span></span></span><span class="jstack-card-go">Open steps</span></a>
<a class="jstack-card" href="remove/"><span class="jstack-card-head"><strong>Remove</strong><span class="jstack-pill">Undo</span></span><span class="jstack-card-copy">There is no uninstall command. Delete the directory this repo installed, and nothing else.</span><span class="jstack-specs"><span><span>Command</span><span>none</span></span><span><span>Delete</span><span>installed path</span></span></span><span class="jstack-card-go">Open steps</span></a>
</div>

A repository with no cluster does not need the Kubernetes skills. A repository that does not use ServiceNow does not need those skills.

!!! note "Lint is for authors"

    `scripts/lint-skills` is not an install step. The authoring rules are on [Writing a skill](../writing-a-skill.md).

Do not paste skills into a chat, and do not copy secrets, kubeconfigs, or cloud keys into the target.
