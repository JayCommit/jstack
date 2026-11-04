---
name: servicenow-changes
description: "Use when you raise or handle a ServiceNow change for the signed-in user. Default to a normal change, write the backout, and stop before approval or implementation."
license: MIT
---

# ServiceNow changes

A change is how production is allowed to move. The agent fills the record and stops. A person approves it. The pipeline or the named implementer runs it inside the window.

## Use when

- You raise, update, schedule, implement, or close a change.
- A pull request or a pipeline can reach production and has no change number.
- Someone asks for an emergency change, or for a standard change that has no template on this instance.

## Steps

1. Act as the user. Follow `servicenow-queue`. Search active change requests for the same CI and the same short description. Update that record if it is still before implementation. Do not open a duplicate.

2. Choose the type. Normal is the default. Standard is allowed only when this instance already has a template for this exact change and you use that template. Emergency is allowed only when production is failing and `ops-incident-response` is already open. Emergency still has a backout. Follow `ops-rollback-plan`.

3. Create or update the normal change with the justification, the implementation plan, the backout plan, the test plan, the risk, the impact, the window, the CI, and the assignment group the user named. Use this instance's choice values for type, risk, and impact. Put the GitHub or Azure DevOps pull request URL in the work notes. Follow `github-pull-requests` or `azuredevops-repositories`. Do not invent a ticket number. Do not set the state to implement or closed.

   ```bash
   curl --silent --show-error --request POST --header "Authorization: Bearer ${SNOW_TOKEN}" --header "Accept: application/json" --header "Content-Type: application/json" --data "{\"short_description\":\"Example change\",\"type\":\"normal\",\"justification\":\"Example\",\"implementation_plan\":\"Example\",\"backout_plan\":\"Example\",\"test_plan\":\"Example\"}" "https://example.service-now.com/api/now/table/change_request"
   ```

   Add `cmdb_ci`, `assignment_group`, `start_date`, `end_date`, `risk`, and `impact` when the user named them and the choice exists here. `type` stays `normal` unless step 2 selected standard or emergency. Read conflict or blackout warnings the instance returns. Do not schedule over a conflict you have not shown the user.

4. Stop. Approval and the move to implement belong to a person. The agent does not approve, does not bypass CAB, and does not start the pipeline. Follow `principle-stop-at-approval` and `pipelines-environments-approvals`.

5. After the window, a person records the actual result. Successful, successful with issues, or unsuccessful are the words this instance uses. Read the choice list. An unsuccessful result runs the backout you wrote. Follow `ops-rollback-plan`. Close only when that result is recorded. Do not close a change that is still in implement.

## Safety checks

- An active change for this CI and description was searched first.
- The type is normal, or the standard template or the open incident is named.
- Justification, implementation, backout, and test plan are filled in.
- The pull request URL is on the change when the work is in git.
- The agent has not approved the change or moved it to implement.
- No secret is in the plans or the work notes.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

The backout plan is the rollback. Rehearse it before the window when the change can reach production. Follow `principle-rollback-first` and `ops-rollback-plan`. Cancel a change that has not started by using this instance's cancelled state. Do not delete the record. A change implemented in error is backed out, then updated with that result.

## Done when

- The change number is the one the API returned, with backout and window filled in, and it is waiting on a person.
- Or the window has finished, the result is recorded, and an unsuccessful change has been backed out.
