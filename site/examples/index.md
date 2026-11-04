# Examples

Each page is one job. Paste the prompt, name the place the change lands, and tell the agent which skill to load. The agent prepares the work and stops. You approve.

Leave `examples/jstack-review/expected.md` closed until a review is written down. The secure stack to copy is `examples/jstack-sample`. The review fixture is a target, not a pattern.

| Job | Prompt starts with |
| --- | --- |
| [Review a Terraform plan](plan-review.md) | Read this plan. Do not apply. |
| [Federate a pipeline to Azure](federate-azure.md) | Replace the client secret with federation. |
| [Create a private AKS cluster](private-aks.md) | Private API, Azure CNI overlay, workload identity. |
| [Triage Terraform drift](drift.md) | A scheduled plan changed and nobody shipped it. |
| [Price an Azure change](azure-cost.md) | Estimate and a budget before anyone applies. |
| [A failing pipeline](failing-pipeline.md) | Here is the failed step. Do not edit yet. |
| [Raise a ServiceNow change](servicenow-change.md) | Act as me. Fill the change. Stop before approval. |

A production failure that is paging people stays on `ops-incident-response`, even when a ServiceNow ticket is also needed. The ticket comes after the mitigation.

When more than one skill could fit, ask the agent to load `jay-mode` and take the first matching row.
