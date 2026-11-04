---
hide:
  - navigation
  - toc
---

<!-- markdownlint-disable-file MD041 -->

<div class="jstack-stage">

<p class="jstack-kicker">DevOps skill pack</p>

# jstack

<p class="jstack-lead">Azure, AWS, Terraform, and the pipelines that ship them. The agent loads one skill, prepares the change, and stops. You approve.</p>

<p class="jstack-actions"><a class="jstack-btn" href="install/">Install</a> <a class="jstack-btn jstack-btn-ghost" href="examples/">Try an example</a></p>

<ol class="jstack-flow">
<li><span>01</span><strong>Name the place</strong> Subscription or account, repository, and environment.</li>
<li><span>02</span><strong>Ask for the job</strong> Start from an example when you want the words ready to paste.</li>
<li><span>03</span><strong>One skill</strong> If several fit, load <code>jay-mode</code> and take the first row.</li>
<li><span>04</span><strong>You decide</strong> Nothing is applied, merged, or granted until you say so.</li>
</ol>

</div>

## Where it runs

<div class="jstack-choices">
<a class="jstack-choice" href="install/cursor/"><strong>Cursor</strong><span>Install the plugin. Do not keep a second copy of the skills.</span></a>
<a class="jstack-choice" href="install/copilot/"><strong>GitHub Copilot</strong><span>Machine install with <code>gh skill</code>, or a repo copy with <code>scripts/sync</code>.</span></a>
<a class="jstack-choice" href="install/other-agents/"><strong>Other agents</strong><span>Point Claude Code, Codex, or Gemini at <code>AGENTS.md</code>.</span></a>
<a class="jstack-choice" href="install/remove/"><strong>Remove</strong><span>Delete the jstack copy. Leave every other skill where it is.</span></a>
</div>

## What you came to do

<div class="jstack-jobs">
<a class="jstack-job" href="examples/plan-review/"><span class="jstack-tag">Terraform</span><strong>Review a plan</strong><span>Read the plan. Do not apply.</span></a>
<a class="jstack-job" href="examples/federate-azure/"><span class="jstack-tag">Identity</span><strong>Federate a pipeline</strong><span>Replace the client secret. Copy the subject from a token.</span></a>
<a class="jstack-job" href="examples/private-aks/"><span class="jstack-tag">Azure</span><strong>Private AKS</strong><span>Private API, Azure CNI overlay, workload identity.</span></a>
<a class="jstack-job" href="examples/drift/"><span class="jstack-tag">Terraform</span><strong>Triage drift</strong><span>A scheduled plan changed, and nobody shipped it.</span></a>
<a class="jstack-job" href="examples/azure-cost/"><span class="jstack-tag">Cost</span><strong>Price a change</strong><span>Estimate and a budget before anyone applies.</span></a>
<a class="jstack-job" href="examples/failing-pipeline/"><span class="jstack-tag">Pipeline</span><strong>A failing run</strong><span>Here is the failed step. Do not edit yet.</span></a>
<a class="jstack-job" href="examples/servicenow-change/"><span class="jstack-tag">ServiceNow</span><strong>Raise a change</strong><span>Act as me. Fill the record. Stop before approval.</span></a>
</div>

## The pack

<div class="jstack-areas">
<a href="catalog/#principles">Principles</a>
<a href="catalog/#terraform">Terraform</a>
<a href="catalog/#azure">Azure</a>
<a href="catalog/#aws">AWS</a>
<a href="catalog/#pipelines">Pipelines</a>
<a href="catalog/#github">GitHub</a>
<a href="catalog/#azure-devops">Azure DevOps</a>
<a href="catalog/#servicenow">ServiceNow</a>
<a href="catalog/#kubernetes">Kubernetes</a>
<a href="catalog/#operations">Operations</a>
<a href="how-it-works/">How a request loads</a>
<a href="day-to-day/">Day to day</a>
</div>

<p class="jstack-note">Principles, Terraform, Azure, AWS, pipelines, repositories, ServiceNow, platform, and operations are in the repository. Live trials in Cursor, Copilot, and Claude Code are still open. The pack is <code>0.0.1</code>. Progress is on <a href="https://github.com/JayCommit/jstack/issues/1">issue 1</a>. Inspired by <a href="https://github.com/cursor/plugins/tree/main/pstack">pstack</a> by Lauren Tan. The words here are written for this pack.</p>
