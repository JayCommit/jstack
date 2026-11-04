---
name: servicenow-queue
description: "Use when you look up what is open for a person in ServiceNow. Call the instance as that user, list their incidents, problems, changes, and requests, and do not create a record from this list."
license: MIT
---

# ServiceNow queue

This skill reads the user's open work. It does not create or close a record. Updates go to the skill for that record type.

## Use when

- Someone asks what is open, assigned to them, or waiting on their group.
- You are about to open an incident, problem, change, or request and have not looked for one that already exists.
- A ticket number was quoted and you need the record before you edit it.

## Steps

1. Use the instance hostname the user gave you. In examples that host is `example.service-now.com`. Do not guess a company instance. Call the API as that user, with their OAuth or SSO bearer token. Do not use a shared admin account and do not put the token or a password in the repo, the chat, or the command line. Follow `principle-no-static-credentials` and `ops-secrets-handling`.

2. Read the signed-in user. If that user is not the person you were asked to act for, stop.

   ```bash
   curl --silent --show-error --header "Authorization: Bearer ${SNOW_TOKEN}" --header "Accept: application/json" "https://example.service-now.com/api/now/ui/user/current_user"
   ```

3. List active incidents, problems, change requests, and requested items assigned to that user's `sys_id`. Ask for the group name when the user wants the group queue. Do not guess a group. Request display values and only the fields you will show. Cap the page.

   ```bash
   curl --silent --show-error --header "Authorization: Bearer ${SNOW_TOKEN}" --header "Accept: application/json" "https://example.service-now.com/api/now/table/incident?sysparm_query=active%3Dtrue%5Eassigned_to%3D00000000-0000-0000-0000-000000000000&sysparm_display_value=all&sysparm_fields=number,short_description,state,priority&sysparm_limit=20"
   ```

   Use the same query shape for `problem`, `change_request`, and `sc_req_item`. Replace the zero id with the id from step 2. Read the state label. Do not assume a state integer from another instance.

4. Report the number, the short description, the state, and the type. Do not paste work notes into the chat. If a note contains a secret, follow `ops-secrets-handling`.

5. Hand a write to the matching skill. An incident follows `servicenow-incidents`. A problem follows `servicenow-problems`. A change follows `servicenow-changes`. A catalog request follows `servicenow-requests`. Creating a record is not part of this list.

## Safety checks

- The hostname and the person match what the user named.
- The call is authenticated as that person, not as a shared admin.
- The list is limited to active records assigned to them, or to the group they named.
- State is the label from this instance.
- No token, password, or secret from a work note is in the chat.
- No record was created, updated, or closed.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

This skill does not write. If a later skill changed the wrong record, that skill rolls it back. Stop if step 2 is not the person you meant to represent.

## Done when

- The user has the numbers, states, and short descriptions of their open records.
- Each record that needs a write is named against the skill that owns that write.
- Nothing was created or closed from the list.
