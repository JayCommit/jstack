# Prompts for servicenow-incidents

Example asks for `servicenow-incidents`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I open, update, or resolve an incident.

### Expected for ask 1

- Load `servicenow-incidents` and follow that file through its own done-when.
- Step: Act as the user on the instance they named. Follow `servicenow-queue` for the session and the open list. If an active incident already matches this caller and this CI, update that record. Do not open a second one.
- Check: An existing active incident was searched before a new one was opened.
- Done when: The incident number is the one already open, or a new number the API returned.

## Ask 2

If users cannot complete the action, run the production response first.

### Expected for ask 2

- Load `servicenow-incidents` and follow that file through its own done-when.
- Step: If users cannot complete the action, run the production response first. Follow `ops-incident-response`. Then write the ticket. A restore in that response follows `ops-backup-restore`.
- Check: The caller, impact, and urgency are set. Priority was left to the instance.
- Done when: The user can see the state and the latest comment.
