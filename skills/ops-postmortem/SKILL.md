---
name: ops-postmortem
description: "Use when a SEV1 or SEV2 incident is over. Write a blameless postmortem with the timeline, the contributing factors, and action items that each have an owner and a date."
license: MIT
---

# Postmortem

Write what happened, what contributed, and what will change. The cause is a set of conditions, not a person.

## Use when

- A SEV1 or SEV2 has ended. Follow `ops-incident-response` for the severity.
- People are writing a single root cause or a sentence that blames a person.
- An action item says "be more careful" or has no owner.
- A short incident is about to be closed with no record.

## Steps

1. Start from the incident timeline. Do not invent times. Draft it within three business days of the impact stopping. A short SEV1 still gets this document. A SEV3 gets a short note only when there is a lesson the next on-call needs.

2. Use this shape.

   ```text
   # Postmortem: app example 5xx

   Incident: example-2026-11-02
   Severity: SEV1
   Lead: named on the timeline
   Impact: users could not complete checkout for 24 minutes. No data loss.

   ## Detection
   The alert example-app-5xx fired, or say that a customer reported it first.

   ## Timeline
   14:02 alert fired
   14:06 lead named
   14:11 previous digest deployed
   14:26 error rate back inside the SLO

   ## Contributing factors
   - The deploy went out without the rehearsed rollback written on the change.
   - The readiness probe checked a dependency, so pods restarted together.

   ## What worked
   The previous digest was still in the registry. The runbook named it.

   ## Action items
   - prevent: pin the probe to the local health path. Owner: example-team. Date: 2026-11-16.
   - detect: page on the checkout SLO, not only on 5xx. Owner: example-team. Date: 2026-11-16.
   - mitigate: add the rollback command to the runbook. Owner: example-team. Date: 2026-11-09.
   ```

3. Impact is who, how long, and whether data was lost. Detection is the alert, a person, or neither. If nobody was paged, the detect action is an alert. Follow `ops-observability-alerts`.

4. Write contributing factors. A single root-cause line hides the missing check, the missing rollback, or the probe. The timeline may name who ran a command. That is the record. The factors do not say a person was careless.

5. Each action item is prevent, detect, or mitigate. It has an owner and a date. "Be more careful" is not an item. An item that changes Terraform, a pipeline, or a cloud resource goes through review. Follow `principle-change-safety`. Do not change production from the postmortem document.

6. The people who were in the incident read the draft before you call it done. Publish it where the next on-call finds the runbook. Follow `ops-runbook-authoring` when an item changes a runbook.

7. Leave secret values and customer payloads out of the document. Follow `ops-secrets-handling`. A log excerpt that contains a secret is not evidence. Redact it before you paste.

## Safety checks

- The times come from the incident timeline.
- Impact names users, duration, and data loss or none.
- Factors describe conditions and missing controls. They do not blame a person.
- Every action item has a type, an owner and a date.
- No action item is a slogan, and none of them skip review for a production change.
- The document has no secret value and no customer payload.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

An action item that is wrong is closed and replaced. If the item already shipped and made things worse, roll that change back like any other production change. Follow `principle-rollback-first` and `ops-rollback-plan`. Correct the document in place so the next reader does not follow the bad item.

## Done when

- The draft has impact, detection, timeline, contributing factors, and what worked.
- Every action item has an owner and a date, and the people who responded have read the draft.
- Production changes from those items are still ahead of you, in review, not applied from this document.
