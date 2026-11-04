---
hide:
  - navigation
  - toc
---

<!-- markdownlint-disable-file MD041 -->

<div class="jstack-home" markdown>

<p class="jstack-kicker">DevOps skill pack</p>

# Prepare the change<br>You approve it { #prepare }

<p class="jstack-lead">Azure, AWS, Terraform, and the pipelines that ship them. The agent opens one skill, prepares the work, and stops.</p>

<p class="jstack-actions"><a class="jstack-btn" href="install/">Install</a> <a class="jstack-btn jstack-btn-ghost" href="examples/">Try an example</a> <a class="jstack-textlink" href="install/remove/">Remove</a></p>

<div class="jstack-console" aria-label="What a session looks like">
<div class="jstack-console-bar"><span>jstack</span><span>Waiting for you</span></div>
<div class="jstack-console-body">
<div class="jstack-turns">
<p><span>You</span>Review the plan for rg-example. Do not apply.</p>
<p><span>Loaded</span><span class="jstack-files">terraform-plan-review<br>principle-stop-at-approval</span></p>
<p><span>Next</span>The saved plan is ready. Nothing is applied.</p>
</div>
<div class="jstack-console-side">
<p><span>Place</span>rg-example</p>
<p><span>Holds</span>apply, merge, grant</p>
<p><span>Then</span>you approve</p>
</div>
</div>
</div>

<div class="jstack-metrics">
<p><strong>One skill</strong><span>The description is the trigger. The agent does not load the whole pack.</span></p>
<p><strong>You approve</strong><span>Apply, merge, and grant stay with a person. The pipeline runs the change.</span></p>
<p><strong>Short-lived identity</strong><span>Pipelines use federation. Static cloud keys stay out of the repository.</span></p>
</div>

<p class="jstack-more"><a href="how-it-works/">How a request loads</a></p>

## Install

<p class="jstack-deck">Pick the tool. Then pick a scope: the whole pack, or a glob such as <code>terraform-*</code>.</p>

<div class="jstack-choices">
<a class="jstack-choice" href="install/cursor/"><span class="jstack-tag">Plugin</span><strong>Cursor</strong><span>Install from this repository. Do not also copy the skills into the project.</span></a>
<a class="jstack-choice" href="install/copilot/"><span class="jstack-tag">Machine or repo</span><strong>GitHub Copilot</strong><span><code>gh skill install</code> for your user, or <code>scripts/sync</code> into one repository. Dry-run first.</span></a>
<a class="jstack-choice" href="install/other-agents/"><span class="jstack-tag">AGENTS.md</span><strong>Claude Code, Codex, Gemini</strong><span>Point the agent at <code>AGENTS.md</code>. Sync into <code>.agents/skills</code> or <code>.claude/skills</code>.</span></a>
<a class="jstack-choice" href="install/remove/"><span class="jstack-tag">Undo</span><strong>Remove</strong><span>There is no uninstall command. Delete the directory this repo installed, and nothing else.</span></a>
</div>

## Start from a job

<p class="jstack-deck">Open one example, copy the prompt, and name where the change lands.</p>

<div class="jstack-rows">
<a href="examples/plan-review/"><span class="jstack-tag">Terraform</span><strong>Review a plan</strong><span>Read this plan. Do not apply.</span></a>
<a href="examples/federate-azure/"><span class="jstack-tag">Identity</span><strong>Federate a pipeline to Azure</strong><span>Replace the client secret. Copy the <code>sub</code> claim from a token.</span></a>
<a href="examples/private-aks/"><span class="jstack-tag">Azure</span><strong>Create a private AKS cluster</strong><span>Private API, Azure CNI overlay, workload identity.</span></a>
<a href="examples/drift/"><span class="jstack-tag">Terraform</span><strong>Triage drift</strong><span>A scheduled plan changed, and nobody shipped it.</span></a>
<a href="examples/azure-cost/"><span class="jstack-tag">Cost</span><strong>Price an Azure change</strong><span>Estimate and a budget before anyone applies.</span></a>
<a href="examples/failing-pipeline/"><span class="jstack-tag">Pipeline</span><strong>A failing pipeline</strong><span>Here is the failed step. Do not edit yet.</span></a>
<a href="examples/servicenow-change/"><span class="jstack-tag">ServiceNow</span><strong>Raise a change</strong><span>Act as me. Fill the change. Stop before approval.</span></a>
</div>

## Elsewhere in the pack

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

<p class="jstack-note">Principles, Terraform, Azure, AWS, pipelines, repositories, ServiceNow, platform, and operations are in the repository. Live trials in Cursor, Copilot, and Claude Code are still open. The pack is <code>0.0.1</code>. Progress is on <a href="https://github.com/JayCommit/jstack/issues/1">issue 1</a>. Inspired by <a href="https://github.com/cursor/plugins/tree/main/pstack">pstack</a> by Lauren Tan. The words here are written for this pack.</p>

</div>
