# Prompts for ops-postmortem

Example asks for `ops-postmortem`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

A SEV1 or SEV2 has ended. Follow `ops-incident-response` for the severity.

### Expected for ask 1

- Load `ops-postmortem` and follow that file through its own done-when.
- Step: Start from the incident timeline. Do not invent times. Draft it within three business days of the impact stopping. A short SEV1 still gets this document. A SEV3 gets a short note only when there is a lesson the next on-call needs.
- Check: The times come from the incident timeline.
- Done when: The draft has impact, detection, timeline, contributing factors, and what worked.

## Ask 2

Use this shape.

### Expected for ask 2

- Load `ops-postmortem` and follow that file through its own done-when.
- Step: Use this shape.
- Check: Impact names users, duration, and data loss or none.
- Done when: Every action item has an owner and a date, and the people who responded have read the draft.
