---
hide:
  - navigation
  - toc
---

<!-- markdownlint-disable-file MD041 -->

<div class="jstack-home">
<div class="jstack-intro">
<h1 id="prepare">One skill, then you approve.</h1>
<p class="jstack-lead">Azure, AWS, Terraform, and the pipelines that ship them. The agent opens one playbook, prepares the work, and stops.</p>
<p class="jstack-actions"><a class="jstack-btn" href="install/">Install</a> <a class="jstack-btn jstack-btn-ghost" href="examples/">Try an example</a></p>
</div>
<div class="jstack-snippet" aria-label="What a session looks like">
<input type="radio" name="jstack-session" id="jstack-prompt" checked>
<input type="radio" name="jstack-session" id="jstack-loaded">
<input type="radio" name="jstack-session" id="jstack-holds">
<div class="jstack-snippet-bar">
<label for="jstack-prompt">Prompt</label>
<label for="jstack-loaded">Loaded</label>
<label for="jstack-holds">Holds</label>
</div>
<pre class="jstack-pane jstack-pane-prompt"><code><span class="tok-c"># rg-example · production</span>
<span class="tok-p">Review examples/jstack-review/terraform/plan.txt.</span>
<span class="tok-p">Subscription 00000000-0000-0000-0000-000000000000. Resource group rg-example. Region uksouth.</span>
<span class="tok-p">State key example-prod.tfstate. Pipeline example-org/example/.github/workflows/deploy.yml.</span>
<span class="tok-k">Do not apply. Do not edit the files.</span></code></pre>
<pre class="jstack-pane jstack-pane-loaded"><code><span class="tok-c"># the playbook, then the principles it needs</span>
<span class="tok-s">terraform-plan-review</span>
<span class="tok-s">principle-stop-at-approval</span>
<span class="tok-s">principle-change-safety</span>
<span class="tok-s">principle-rollback-first</span></code></pre>
<pre class="jstack-pane jstack-pane-holds"><code><span class="tok-c"># stays with a person</span>
<span class="tok-m">apply</span>  <span class="tok-m">merge</span>  <span class="tok-m">grant</span>
<span class="tok-c"># the pipeline runs the saved plan</span></code></pre>
</div>
<div class="jstack-board">
<section class="jstack-panel" aria-labelledby="install">
<h2 id="install">Install</h2>
<p class="jstack-deck">Pick the tool. Then pick a scope: the whole pack, or a glob such as terraform-*.</p>
<a href="install/cursor/"><span class="jstack-row-copy"><strong>Cursor</strong><span>Install from this repository. Do not also copy the skills in.</span></span><span class="jstack-meta">plugin.json</span></a>
<a href="install/copilot/"><span class="jstack-row-copy"><strong>GitHub Copilot</strong><span>gh skill install for your user, or scripts/sync. Dry-run first.</span></span><span class="jstack-meta">machine or repo</span></a>
<a href="install/other-agents/"><span class="jstack-row-copy"><strong>Claude Code, Codex, Gemini</strong><span>Point the agent at AGENTS.md. Sync into .agents/skills or .claude/skills.</span></span><span class="jstack-meta">AGENTS.md</span></a>
<a href="install/remove/"><span class="jstack-row-copy"><strong>Remove</strong><span>There is no uninstall command. Delete the directory this repo installed.</span></span><span class="jstack-meta">no command</span></a>
</section>
<section class="jstack-panel" aria-labelledby="start-from-a-job">
<h2 id="start-from-a-job">Start from a job</h2>
<p class="jstack-deck">Open one example, copy the prompt, and name where the change lands.</p>
<a href="examples/plan-review/"><span class="jstack-row-copy"><strong>Review a plan</strong><span>Read this plan. Do not apply.</span></span><span class="jstack-meta">Terraform</span></a>
<a href="examples/federate-azure/"><span class="jstack-row-copy"><strong>Federate a pipeline to Azure</strong><span>Replace the client secret. Copy the sub claim from a token.</span></span><span class="jstack-meta">Identity</span></a>
<a href="examples/private-aks/"><span class="jstack-row-copy"><strong>Create a private AKS cluster</strong><span>Private API, Azure CNI overlay, workload identity.</span></span><span class="jstack-meta">Azure</span></a>
<a href="examples/drift/"><span class="jstack-row-copy"><strong>Triage drift</strong><span>A scheduled plan changed, and nobody shipped it.</span></span><span class="jstack-meta">Terraform</span></a>
<a href="examples/azure-cost/"><span class="jstack-row-copy"><strong>Price an Azure change</strong><span>Estimate and a budget before anyone applies.</span></span><span class="jstack-meta">Cost</span></a>
<a href="examples/failing-pipeline/"><span class="jstack-row-copy"><strong>A failing pipeline</strong><span>Here is the failed step. Do not edit yet.</span></span><span class="jstack-meta">Pipeline</span></a>
<a href="examples/servicenow-change/"><span class="jstack-row-copy"><strong>Raise a change</strong><span>Act as me. Fill the change. Stop before approval.</span></span><span class="jstack-meta">ServiceNow</span></a>
</section>
</div>
<p class="jstack-note">Principles, Terraform, Azure, AWS, pipelines, repositories, ServiceNow, platform, and operations are in the repository. The <a href="catalog/">catalog</a> lists every skill. Live trials in Cursor, Copilot, and Claude Code are still open. The pack is 0.0.1. Progress is on <a href="https://github.com/JayCommit/jstack/issues/1">issue 1</a>. Inspired by <a href="https://github.com/cursor/plugins/tree/main/pstack">pstack</a> by Lauren Tan. The words here are written for this pack.</p>
</div>
