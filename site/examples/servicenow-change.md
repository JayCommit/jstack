# Raise a ServiceNow change

Production work needs a change record. The agent acts as you, fills the record, and stops before approval.

## Ask this

```text
Act as me on https://example.service-now.com.
Raise a normal change for CI app-example.
Short description: example change.
Pull request: https://github.com/example-org/example/pull/1.
Window: the one I name.
Load servicenow-changes.
Search for an open change on this CI first.
Fill justification, implementation, backout, and test plan.
Stop before approval. Do not move it to implement.
```

Use a token for the signed-in user. Do not paste a password into the chat, and do not ask the agent to use a shared admin account.

## Load

- `servicenow-changes` defaults to a normal change. Standard is allowed only when this instance already has a template for this exact change. Emergency is allowed only when production is failing and `ops-incident-response` is already open.
- `principle-change-safety` and `principle-rollback-first` apply when the change can reach production. The backout is the rollback.
- `servicenow-queue` is how the agent acts as the signed-in user. Load it when the change skill points there.

## What good looks like

The change number is the one the API returned. Justification, implementation, backout, and the test plan are filled in. The pull request URL is on the record. The state is still waiting on a person.

A paging outage stays on `ops-incident-response`. Open the incident ticket after the mitigation, with `servicenow-incidents`. The agent does not approve the change and does not start the pipeline.
