---
name: ops-incident-response
description: "Use when a production service is failing. Name a lead, set a severity from user impact, mitigate with a rehearsed rollback, and send updates on a fixed cadence."
license: MIT
---

# Incident response

Name a lead, say who is hurt, and mitigate with a step you have already rehearsed. The explanation comes after the user impact stops.

## Use when

- Production users cannot complete an action, or the data is at risk.
- An alert is paging, or a customer report says the service is down.
- Several people are changing production at the same time.
- You are about to restart, scale, or edit IAM in the middle of a failure.

## Steps

1. Open one incident channel and name one lead. The lead owns the call. On a small team the lead can also post updates. The lead does not also have to be the only person reading logs. Say that there is an incident in the first message.

2. Set the severity from user impact.

   - SEV1: production users cannot complete the main action, or data is at risk. Page.
   - SEV2: production is degraded, a workaround exists, or one region or one tenant is hit.
   - SEV3: there is no user impact, or only an internal tool is affected. Track it. Do not page the whole roster.

3. Write one impact sentence: who, which action, since when. Read the alert, the dashboard and the last deploy before you change anything. Follow `principle-observe-before-you-fix` and `ops-observability-alerts`. If you cannot write the sentence, you do not have a mitigation yet.

4. Mitigate before you explain the cause. The first change is the rehearsed rollback for this change type. Follow `ops-rollback-plan` and `principle-rollback-first`. Do not start a new fix and a rollback in the same minute. Do not restart or scale as a guess.

5. Keep a timeline in the incident channel. Each line has a time and what changed: alert fired, lead named, mitigation started, user impact stopped. Do not keep that record in a private chat.

6. Update on a clock. SEV1 every 15 minutes. SEV2 every 30 minutes. Say what changed, what the user sees now, and when the next update is. Send "no change" when nothing changed.

7. When user impact stops, stop changing production unless the mitigation is incomplete. Write down what you changed. A postmortem for SEV1 and SEV2 follows `ops-postmortem`. Do not write that document in the first fifteen minutes.

8. Hand off with the impact sentence, the severity, the mitigation in progress, and the next update time. A link with no sentence is not a handoff.

9. Use the access you already have. A temporary elevation follows `azure-rbac-entra` or `aws-iam-least-privilege` and is removed when the impact stops. Do not create a standing admin role. Follow `principle-least-privilege`.

10. If the mitigation can touch more than this service, list that radius before you run it. Follow `ops-blast-radius`. One incident, one channel.

## Safety checks

- One lead is named, and the severity matches the user impact.
- The impact sentence says who, which action, and since when.
- The first production change is a rehearsed mitigation, not a new idea.
- Updates went out on the 15-minute or 30-minute cadence, including "no change".
- The timeline is in the incident channel.
- No standing admin role was added.
- The blast radius of the mitigation is named before it runs.

## Rollback

If the mitigation makes the impact worse, undo that mitigation with the next rehearsed step and write the time on the timeline. Follow `ops-rollback-plan`. Do not add a third change while the second is still in progress. Stop and update the channel.

## Done when

- User impact has stopped, or a SEV3 has an owner and a ticket.
- The timeline shows the mitigation and the time the impact stopped.
- The channel has a handoff or a close note.
- A SEV1 or SEV2 has a postmortem time. Follow `ops-postmortem`.
