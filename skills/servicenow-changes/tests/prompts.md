# Prompts for servicenow-changes

Example asks for `servicenow-changes`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I raise, update, schedule, implement, or close a change.

### Expected for ask 1

- Load `servicenow-changes` and follow that file through its own done-when.
- Step: Act as the user. Follow `servicenow-queue`. Search active change requests for the same CI and the same short description. Update that record if it is still before implementation. Do not open a duplicate.
- Check: An active change for this CI and description was searched first.
- Done when: The change number is the one the API returned, with backout and window filled in, and it is waiting on a person.

## Ask 2

Choose the type.

### Expected for ask 2

- Load `servicenow-changes` and follow that file through its own done-when.
- Step: Choose the type. Normal is the default. Standard is allowed only when this instance already has a template for this exact change and you use that template. Emergency is allowed only when production is failing and `ops-incident-response` is already open. Emergency still has a backout. Follow `ops-rollback-plan`.
- Check: The type is normal, or the standard template or the open incident is named.
- Done when: Or the window has finished, the result is recorded, and an unsuccessful change has been backed out.
