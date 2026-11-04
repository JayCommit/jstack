---
hide:
  - navigation
  - toc
---

<!-- markdownlint-disable-file MD041 -->

<div class="jstack-home">
<div class="jstack-stage">
<div class="jstack-stage-copy">
<h1 id="prepare">One skill.<br>Then you approve.</h1>
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
<span class="tok-p">Subscription 00000000-0000-0000-0000-000000000000.</span>
<span class="tok-p">Resource group rg-example. Region uksouth.</span>
<span class="tok-p">State key example-prod.tfstate.</span>
<span class="tok-p">Pipeline example-org/example/.github/workflows/deploy.yml.</span>
<span class="tok-k">Do not apply. Do not edit the files.</span></code></pre>
<pre class="jstack-pane jstack-pane-loaded"><code><span class="tok-c"># the playbook, then the principles it needs</span>
<span class="tok-s">terraform-plan-review</span>
<span class="tok-s">principle-stop-at-approval</span>
<span class="tok-s">principle-change-safety</span>
<span class="tok-s">principle-rollback-first</span></code></pre>
<pre class="jstack-pane jstack-pane-holds"><code><span class="tok-c"># stays with a person</span>
<span class="tok-m">apply</span>
<span class="tok-m">merge</span>
<span class="tok-m">grant</span>
<span class="tok-c"># the pipeline runs the saved plan</span></code></pre>
</div>
</div>
<h2 id="install">Install</h2>
<p class="jstack-deck">Pick the tool. Then pick a scope: the whole pack, or a glob such as terraform-*.</p>
<div class="jstack-cards">
<a class="jstack-card" href="install/cursor/">
<span class="jstack-card-head"><strong>Cursor</strong><span class="jstack-pill">Plugin</span></span>
<span class="jstack-card-copy">Install from this repository. Do not also copy the skills into the project.</span>
<span class="jstack-specs"><span><span>Reads</span><span>plugin.json</span></span><span><span>Also copy</span><span>No</span></span></span>
<span class="jstack-card-go">Open steps</span>
</a>
<a class="jstack-card" href="install/copilot/">
<span class="jstack-card-head"><strong>GitHub Copilot</strong><span class="jstack-pill">Machine or repo</span></span>
<span class="jstack-card-copy">gh skill install for your user, or scripts/sync into one repository. Dry-run first.</span>
<span class="jstack-specs"><span><span>Machine</span><span>your user</span></span><span><span>Repository</span><span>scripts/sync</span></span></span>
<span class="jstack-card-go">Open steps</span>
</a>
<a class="jstack-card" href="install/other-agents/">
<span class="jstack-card-head"><strong>Claude Code, Codex, Gemini</strong><span class="jstack-pill">AGENTS.md</span></span>
<span class="jstack-card-copy">Point the agent at AGENTS.md. Sync into .agents/skills or .claude/skills.</span>
<span class="jstack-specs"><span><span>Index</span><span>AGENTS.md</span></span><span><span>Copy</span><span>.agents/skills</span></span></span>
<span class="jstack-card-go">Open steps</span>
</a>
<a class="jstack-card" href="install/remove/">
<span class="jstack-card-head"><strong>Remove</strong><span class="jstack-pill">Undo</span></span>
<span class="jstack-card-copy">There is no uninstall command. Delete the directory this repo installed, and nothing else.</span>
<span class="jstack-specs"><span><span>Command</span><span>none</span></span><span><span>Delete</span><span>installed path</span></span></span>
<span class="jstack-card-go">Open steps</span>
</a>
</div>
<h2 id="start-from-a-job">Start from a job</h2>
<p class="jstack-deck">Open one example, copy the prompt, and name where the change lands.</p>
<div class="jstack-jobs">
<a class="jstack-job" href="examples/plan-review/"><span class="jstack-pill">Terraform</span><strong>Review a plan</strong><span>Read this plan. Do not apply.</span><span class="jstack-card-go">Open</span></a>
<a class="jstack-job" href="examples/federate-azure/"><span class="jstack-pill">Identity</span><strong>Federate a pipeline to Azure</strong><span>Replace the client secret. Copy the sub claim from a token.</span><span class="jstack-card-go">Open</span></a>
<a class="jstack-job" href="examples/private-aks/"><span class="jstack-pill">Azure</span><strong>Create a private AKS cluster</strong><span>Private API, Azure CNI overlay, workload identity.</span><span class="jstack-card-go">Open</span></a>
<a class="jstack-job" href="examples/drift/"><span class="jstack-pill">Terraform</span><strong>Triage drift</strong><span>A scheduled plan changed, and nobody shipped it.</span><span class="jstack-card-go">Open</span></a>
<a class="jstack-job" href="examples/azure-cost/"><span class="jstack-pill">Cost</span><strong>Price an Azure change</strong><span>Estimate and a budget before anyone applies.</span><span class="jstack-card-go">Open</span></a>
<a class="jstack-job" href="examples/failing-pipeline/"><span class="jstack-pill">Pipeline</span><strong>A failing pipeline</strong><span>Here is the failed step. Do not edit yet.</span><span class="jstack-card-go">Open</span></a>
<a class="jstack-job" href="examples/servicenow-change/"><span class="jstack-pill">ServiceNow</span><strong>Raise a change</strong><span>Act as me. Fill the change. Stop before approval.</span><span class="jstack-card-go">Open</span></a>
</div>
<h2 id="elsewhere-in-the-pack">Elsewhere in the pack</h2>
<div class="jstack-columns">
<div>
<p class="jstack-col-label">Install</p>
<ul>
<li><a href="install/">Overview</a></li>
<li><a href="install/cursor/">Cursor</a></li>
<li><a href="install/copilot/">GitHub Copilot</a></li>
<li><a href="install/other-agents/">Other agents</a></li>
<li><a href="install/remove/">Remove</a></li>
</ul>
</div>
<div>
<p class="jstack-col-label">Guide</p>
<ul>
<li><a href="how-it-works/">How it works</a></li>
<li><a href="day-to-day/">Day to day</a></li>
<li><a href="secure-defaults/">Secure defaults</a></li>
<li><a href="writing-a-skill/">Writing a skill</a></li>
<li><a href="examples/">Examples</a></li>
</ul>
</div>
<div>
<p class="jstack-col-label">Skills</p>
<ul>
<li><a href="catalog/">All skills</a></li>
<li><a href="catalog/#principles">Principles</a></li>
<li><a href="catalog/#terraform">Terraform</a></li>
<li><a href="catalog/#azure">Azure</a></li>
<li><a href="catalog/#aws">AWS</a></li>
<li><a href="catalog/#pipelines">Pipelines</a></li>
<li><a href="catalog/#github">GitHub</a></li>
<li><a href="catalog/#azure-devops">Azure DevOps</a></li>
<li><a href="catalog/#servicenow">ServiceNow</a></li>
<li><a href="catalog/#kubernetes">Kubernetes</a></li>
<li><a href="catalog/#operations">Operations</a></li>
</ul>
</div>
</div>
<p class="jstack-note">Principles, Terraform, Azure, AWS, pipelines, repositories, ServiceNow, platform, and operations are in the repository. Live trials in Cursor, Copilot, and Claude Code are still open. The pack is 0.0.1. Progress is on <a href="https://github.com/JayCommit/jstack/issues/1">issue 1</a>. Inspired by <a href="https://github.com/cursor/plugins/tree/main/pstack">pstack</a> by Lauren Tan. The words here are written for this pack.</p>
</div>
