# Install

Pick a tool, then pick a scope.

The scope is the whole pack, or a glob such as `terraform-*` and `principle-*`. A repository with no cluster does not need the Kubernetes skills. A repository that does not use ServiceNow does not need those skills.

<!-- markdownlint-disable MD030 -->

<div class="grid cards" markdown>

-   **Cursor**

    ---

    Install the plugin. Do not also copy the same skills into the project.

    [Install for Cursor](cursor.md)

-   **GitHub Copilot**

    ---

    On your machine with `gh skill install`, or in one repository with `scripts/sync`.

    [Install for Copilot](copilot.md)

-   **Other agents**

    ---

    Point Claude Code, Codex, or Gemini at `AGENTS.md`, then sync the skills you chose.

    [Install for other agents](other-agents.md)

-   **Remove**

    ---

    Delete the jstack copy. Leave every skill that came from somewhere else.

    [Remove jstack](remove.md)

</div>

<!-- markdownlint-enable MD030 -->

!!! note "Lint is for authors"

    `scripts/lint-skills` is not an install step. The authoring rules are on [Writing a skill](../writing-a-skill.md).

Do not paste skills into a chat, and do not copy secrets, kubeconfigs, or cloud keys into the target.
