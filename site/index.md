# jstack

DevOps skills for Azure, AWS, Terraform, and the pipelines that ship them. The agent opens one playbook, prepares the work, and stops.

The pack is 0.0.1. Live trials in Cursor, Copilot, and Claude Code are still open.

<div class="jstack-launch">
<a href="install/"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v10m0 0 4-4m-4 4-4-4M5 19h14" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg><strong>Install</strong><span>Cursor, Copilot, or another agent.</span></a>
<a href="how-it-works/"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 7h8M8 12h8M8 17h5" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg><strong>How it works</strong><span>One playbook, then you approve.</span></a>
<a href="examples/"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4h7l5 5v11H7V4z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg><strong>Try an example</strong><span>Copy a prompt and name the place.</span></a>
<a href="catalog/"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5h6v6H5V5zm8 0h6v6h-6V5zM5 13h6v6H5v-6zm8 0h6v6h-6v-6z" fill="none" stroke="currentColor" stroke-width="1.7"/></svg><strong>Skills</strong><span>Every playbook in the pack.</span></a>
</div>

## Quick start

### Install

<!-- markdownlint-disable MD046 -->

=== "Cursor"

    Install the plugin from this repository. The manifest is `.cursor-plugin/plugin.json`.

    Do not also copy the skills into the project. Two copies drift.

    The steps are on the [Cursor](install/cursor.md) page.

=== "GitHub Copilot"

    The repository is private. The account that installs it has to be able to read it.

    ```bash
    gh skill install JayCommit/jstack --all --scope user --agent github-copilot
    ```

    Prove the copy:

    ```bash
    gh skill list --scope user --agent github-copilot
    ```

    The steps are on the [GitHub Copilot](install/copilot.md) page.

=== "Other agents"

    Point the agent at `AGENTS.md`. Dry-run, then sync into `.agents/skills` or `.claude/skills`.

    ```bash
    scripts/sync --dry-run --target-dir .agents/skills --all /path/to/target-repo
    scripts/sync --target-dir .agents/skills --all /path/to/target-repo
    ```

    PowerShell 7 is on the [Other agents](install/other-agents.md) page.

<!-- markdownlint-enable MD046 -->

There is no uninstall command. Delete the directory this repository installed, and nothing else. The steps are on the [Remove](install/remove.md) page.

### Name the place

Say where the change lands: the subscription or account, the resource group or VPC, the state key, and the pipeline. The agent opens one playbook. When several skills fit, it loads `jay-mode` and takes the first row.

### You approve

The agent prepares the diff, the saved plan, or the ticket, and stops. Apply, merge, and grant stay with a person. The pipeline runs the change.

## What it does

The skill description is the trigger. The agent reads that file before it edits. It does not load the whole pack.

A principle is a short rule used across areas. Every request also loads `principle-stop-at-approval`. The path is drawn on [How it works](how-it-works.md).

## Start from a job

Open one example, copy the prompt, and name where the change lands.

<div class="jstack-guides">
<a href="examples/plan-review/"><strong>Review a plan</strong><span>Read this plan. Do not apply.</span></a>
<a href="examples/federate-azure/"><strong>Federate a pipeline to Azure</strong><span>Replace the client secret. Copy the sub claim from a token.</span></a>
<a href="examples/private-aks/"><strong>Create a private AKS cluster</strong><span>Private API, Azure CNI overlay, workload identity.</span></a>
<a href="examples/drift/"><strong>Triage drift</strong><span>A scheduled plan changed, and nobody shipped it.</span></a>
<a href="examples/azure-cost/"><strong>Price an Azure change</strong><span>Estimate and a budget before anyone applies.</span></a>
<a href="examples/failing-pipeline/"><strong>A failing pipeline</strong><span>Here is the failed step. Do not edit yet.</span></a>
<a href="examples/servicenow-change/"><strong>Raise a change</strong><span>Act as me. Fill the change. Stop before approval.</span></a>
</div>

Principles, Terraform, Azure, AWS, pipelines, repositories, ServiceNow, platform, and operations are in the repository. The [catalog](catalog.md) lists every skill. Progress is on [issue 1](https://github.com/JayCommit/jstack/issues/1). Inspired by [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan. The words here are written for this pack.
