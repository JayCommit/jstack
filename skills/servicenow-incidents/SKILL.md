---
name: servicenow-incidents
description: "Use when you open or update a ServiceNow incident for the signed-in user. Search the open queue first, set impact and urgency, and resolve only after the user confirms the symptom has stopped."
license: MIT
---

# ServiceNow incidents

The incident is the ticket. If production users are failing, the response is `ops-incident-response`. This skill records that work. It does not replace it.

## Use when

- You open, update, or resolve an incident.
- A caller reports a broken service and you have not searched for an open incident on that CI.
- Someone wants an incident resolved to clear the queue while the symptom is still there.

## Steps

1. Act as the user on the instance they named. Follow `servicenow-queue` for the session and the open list. If an active incident already matches this caller and this CI, update that record. Do not open a second one.

2. If users cannot complete the action, run the production response first. Follow `ops-incident-response`. Then write the ticket. A restore in that response follows `ops-backup-restore`.

3. On a new incident, set the caller, the CI, the assignment group the user named, impact, and urgency. Use the choice values this instance shows for the level you agreed. Let the instance calculate priority. The short description says who is hurt and which action fails. Work notes are internal. Additional comments are what the caller sees. Do not put a secret, a token, or a password in either. Follow `ops-secrets-handling`.

   ```bash
   curl --silent --show-error --request POST --header "Authorization: Bearer ${SNOW_TOKEN}" --header "Accept: application/json" --header "Content-Type: application/json" --data "{\"short_description\":\"Example service fails for the caller\",\"caller_id\":\"00000000-0000-0000-0000-000000000000\"}" "https://example.service-now.com/api/now/table/incident"
   ```

   Replace the caller id with the user from `servicenow-queue`. Add `cmdb_ci`, `assignment_group`, `impact`, and `urgency` only with values from this instance. Read the state label this instance uses. Do not force a state number from another instance.

4. To update, patch work notes or comments on the number you listed. Do not change the caller, the CI, or the assignment group unless the user asked.

5. Resolve only after the user confirms the symptom has stopped. Set the instance's resolved state, a close code that exists on this instance, and close notes that say what changed. Do not move the record straight to closed. Do not resolve an incident whose problem is still unknown if the user asked for a problem. Follow `servicenow-problems`.

6. A fix that changes production is a change request. Follow `servicenow-changes`. Do not implement it from the incident. The agent does not approve that change. Follow `principle-stop-at-approval`.

## Safety checks

- An existing active incident was searched before a new one was opened.
- The caller, impact, and urgency are set. Priority was left to the instance.
- Work notes and comments contain no secret.
- Production user impact also has `ops-incident-response` in progress.
- Resolve happened only after the user confirmed the symptom stopped.
- The agent did not approve a related change.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Reopen the incident if it was resolved while the symptom remains. Use the instance's reopen path. Do not delete the record. A bad work note is corrected with a new note, not by editing history. Follow `principle-rollback-first` when the underlying production change must be undone. That undo is `ops-rollback-plan`.

## Done when

- The incident number is the one already open, or a new number the API returned.
- The user can see the state and the latest comment.
- A resolve has the user's confirmation and a close note, or the incident is still active.
