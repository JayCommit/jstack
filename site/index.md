# One skill, then you approve

<div class="jstack-hero" markdown>

<p class="jstack-kicker">jstack</p>
<p class="jstack-lead">A DevOps pack for Azure, AWS, Terraform, and the pipelines that ship them. Cursor, Copilot, and any agent that reads <code>AGENTS.md</code> use the same files.</p>

The agent prepares the diff and stops. You approve. The pipeline applies.

</div>

<!-- markdownlint-disable MD030 -->

<div class="grid cards" markdown>

-   **Install**

    ---

    Cursor, Copilot, or another agent. Whole pack, or one glob.

    [Install jstack](install/index.md)

-   **How it works**

    ---

    One description match. One file. A stop before apply, merge, or grant.

    [See the load path](how-it-works.md)

-   **Examples**

    ---

    Copy a prompt. Name the place. Tell the agent which skill to load.

    [Use an example](examples/index.md)

-   **Remove**

    ---

    Delete the jstack copy. Leave every other skill where it is.

    [Remove jstack](install/remove.md)

</div>

<!-- markdownlint-enable MD030 -->

## A request

<ol class="jstack-steps">
<li><strong>Name the place.</strong> Subscription or account, repository, and environment.</li>
<li><strong>Ask for the job.</strong> Start from an example when you want the words ready to paste.</li>
<li><strong>One skill.</strong> If several could fit, say: load <code>jay-mode</code> and take the first row.</li>
<li><strong>You decide.</strong> Nothing is applied, merged, or granted until you say so.</li>
</ol>

[Day to day](day-to-day.md) [Skills](catalog.md) [Secure defaults](secure-defaults.md)
{ .jstack-next }

## Status

Principles, Terraform, Azure, AWS, pipelines, GitHub and Azure DevOps repositories, ServiceNow, platform, and operations are in the repository. The catalog is built from those files.

Live trials in Cursor, Copilot, and Claude Code are still open. The pack is still `0.0.1`. Progress is on [issue 1](https://github.com/JayCommit/jstack/issues/1).

## Credit

jstack is inspired by [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan, MIT licence. The words here are written for this pack.
