# Examples

Each page is one job. Copy the prompt, name where the change lands, and tell the agent which skill to load.

The agent prepares the work and stops. You approve.

<!-- markdownlint-disable MD030 -->

<div class="grid cards" markdown>

-   **Review a Terraform plan**

    ---

    Read this plan. Do not apply.

    [Open the prompt](plan-review.md)

-   **Federate a pipeline to Azure**

    ---

    Replace the client secret with federation.

    [Open the prompt](federate-azure.md)

-   **Create a private AKS cluster**

    ---

    Private API, Azure CNI overlay, workload identity.

    [Open the prompt](private-aks.md)

-   **Triage Terraform drift**

    ---

    A scheduled plan changed, and nobody shipped it.

    [Open the prompt](drift.md)

-   **Price an Azure change**

    ---

    Estimate and a budget before anyone applies.

    [Open the prompt](azure-cost.md)

-   **A failing pipeline**

    ---

    Here is the failed step. Do not edit yet.

    [Open the prompt](failing-pipeline.md)

-   **Raise a ServiceNow change**

    ---

    Act as me. Fill the change. Stop before approval.

    [Open the prompt](servicenow-change.md)

</div>

<!-- markdownlint-enable MD030 -->

!!! warning "A page is an incident"

    A production failure that is paging people stays on `ops-incident-response`. The ServiceNow ticket comes after the mitigation.

When more than one skill could fit, ask the agent to load `jay-mode` and take the first matching row.

Leave `examples/jstack-review/expected.md` closed until a review is written down. Copy from `examples/jstack-sample`. The review fixture is a target, not a pattern.
