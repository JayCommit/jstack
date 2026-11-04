# Examples

Each card is one job. Open it, copy the prompt, and name where the change lands.

The agent prepares the work and stops. You approve.

<div class="jstack-rows">
<a href="plan-review/"><span class="jstack-tag">Terraform</span><strong>Review a plan</strong><span>Read this plan. Do not apply.</span></a>
<a href="federate-azure/"><span class="jstack-tag">Identity</span><strong>Federate a pipeline to Azure</strong><span>Replace the client secret. Copy the <code>sub</code> claim from a token.</span></a>
<a href="private-aks/"><span class="jstack-tag">Azure</span><strong>Create a private AKS cluster</strong><span>Private API, Azure CNI overlay, workload identity.</span></a>
<a href="drift/"><span class="jstack-tag">Terraform</span><strong>Triage drift</strong><span>A scheduled plan changed, and nobody shipped it.</span></a>
<a href="azure-cost/"><span class="jstack-tag">Cost</span><strong>Price an Azure change</strong><span>Estimate and a budget before anyone applies.</span></a>
<a href="failing-pipeline/"><span class="jstack-tag">Pipeline</span><strong>A failing pipeline</strong><span>Here is the failed step. Do not edit yet.</span></a>
<a href="servicenow-change/"><span class="jstack-tag">ServiceNow</span><strong>Raise a change</strong><span>Act as me. Fill the change. Stop before approval.</span></a>
</div>

!!! warning "A page is an incident"

    A production failure that is paging people stays on `ops-incident-response`. The ServiceNow ticket comes after the mitigation.

When more than one skill could fit, ask the agent to load `jay-mode` and take the first matching row.

Leave `examples/jstack-review/expected.md` closed until a review is written down. Copy from `examples/jstack-sample`. The review fixture is a target, not a pattern.
