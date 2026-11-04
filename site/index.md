# jstack

<p class="jstack-kicker">DevOps skills for agents</p>
<p class="jstack-lead">One pack for Azure, AWS, Terraform, and the pipelines that ship them. Cursor, GitHub Copilot, and any agent that reads <code>AGENTS.md</code> use the same files.</p>

The agent loads one playbook, then the principles that apply. It prepares the diff and stops. You approve. The pipeline applies.

<!-- markdownlint-disable MD030 -->

<div class="grid cards" markdown>

-   **Install**

    ---

    Put the pack on Cursor, Copilot, or another agent. Take a glob, or take the whole set.

    [Install jstack](install/index.md)

-   **How it works**

    ---

    A description match, one skill, and a stop before apply, merge, or grant.

    [See the load path](how-it-works.md)

-   **Examples**

    ---

    A situation, a prompt you can paste, the skills to load, and what good looks like.

    [Use an example](examples/index.md)

-   **Remove**

    ---

    Delete the jstack copy. Leave every skill that came from somewhere else.

    [Remove jstack](install/remove.md)

</div>

<!-- markdownlint-enable MD030 -->

## A request, in order

| Step | What happens |
| --- | --- |
| 1 | You name the subscription or account, the repository, and the environment. |
| 2 | The description on `skills/<name>/SKILL.md` matches the request. |
| 3 | If several skills fit, `jay-mode` takes the first row and names the one skill to load. |
| 4 | The agent reads that file. It stops before an apply, a merge, or a grant. |

[Day to day](day-to-day.md) is the operator guide. [Skills](catalog.md) is the generated catalog. [Secure defaults](secure-defaults.md) says which principle to load.

## Status

The principles, Terraform, Azure, AWS, pipelines, GitHub and Azure DevOps repositories, ServiceNow, platform, and operations skills are in the repository. The catalog is generated from those files on each build.

Live trials in Cursor, Copilot, and Claude Code are still open, and the repository is still `0.0.1`. Progress is on [issue 1](https://github.com/JayCommit/jstack/issues/1).

## Credit

jstack is inspired by [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan, MIT licence. The words here are written for this pack.
