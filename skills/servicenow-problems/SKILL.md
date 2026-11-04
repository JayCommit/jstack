---
name: servicenow-problems
description: "Use when you open or update a ServiceNow problem for the signed-in user. Relate the incidents that share a cause, record a workaround, and send the fix through a change."
license: MIT
---

# ServiceNow problems

A problem is the cause behind one or more incidents. One alert that already has a fix does not need a problem.

## Use when

- The same CI or the same symptom has more than one incident.
- You record a root cause, a workaround, or a known error.
- Someone wants a problem closed because a single incident was resolved and the cause is still present.

## Steps

1. Act as the user. Follow `servicenow-queue`. Search active problems for this CI before you open another. Update the one that matches.

2. Open a problem only when you can name the shared symptom and at least one incident number. Set impact, urgency, the CI, and the assignment group the user named. Do not copy priority by hand if the instance calculates it.

   ```bash
   curl --silent --show-error --request POST --header "Authorization: Bearer ${SNOW_TOKEN}" --header "Accept: application/json" --header "Content-Type: application/json" --data "{\"short_description\":\"Example service fails after the same change\",\"cmdb_ci\":\"00000000-0000-0000-0000-000000000000\"}" "https://example.service-now.com/api/now/table/problem"
   ```

   Replace the CI id with the CI the user named. Omit `cmdb_ci` when they have not named one.

3. Relate each incident. Patch the incident's `problem_id` to this problem. Follow `servicenow-incidents` for any other incident field. Do not close those incidents from this skill.

4. Write the workaround in the problem when callers need a way to keep working. A known error is that workaround plus the cause, on this instance's known-error flag. Do not put a secret or a command that prints a secret in the workaround. Follow `ops-secrets-handling`.

5. The permanent fix is a change. Follow `servicenow-changes`. Do not move the problem to resolved from the chat while the fix is still a proposal. The agent does not approve the change. Follow `principle-stop-at-approval`.

6. Resolve the problem only after the user confirms the cause is removed and the related incidents are resolved or no longer recurring. Use this instance's resolved state. Read the label. Do not reuse an integer from another instance.

## Safety checks

- An active problem for this CI was searched first.
- At least one incident number is related, or the change says this is a cause found with no open incident.
- The workaround contains no secret.
- A proposed fix is a change request, not an edit done from the problem.
- The problem is not resolved while the cause is still present.
- The call is as the user, not a shared admin.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Remove the problem link from an incident that was related in error by clearing `problem_id` on that incident. Do not delete the problem if any incident still points at it. Reopen a problem that was resolved early, using this instance's reopen path. A fix that already reached production follows `ops-rollback-plan`.

## Done when

- The problem number is known, and each related incident points at it.
- The workaround or known error is recorded, or the change says there is no workaround yet.
- A fix is a ServiceNow change still waiting on approval, or the user has confirmed the cause is gone.
