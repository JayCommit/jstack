---
name: ops-runbook-authoring
description: "Use when you write or update a runbook. Give each step a command, the output you expect, and the person to escalate to when that output does not appear."
license: MIT
---

# Runbook authoring

An operator who did not write the runbook can follow it. Each step has a command and the output that means it worked.

## Use when

- You add an alert and it needs a runbook. Follow `ops-observability-alerts`.
- You change a deploy, a failover, or a certificate rotation and the old steps are wrong.
- A runbook says "check the service" and gives no command.
- Someone followed a runbook and had to invent the next step.

## Steps

1. Put the runbook where the on-call already looks, and link it from the alert description. One alert, one runbook. Name the owner and the date you last ran the steps.

2. Use this shape. Replace the placeholders. Do not put a secret value, a real subscription, or a real account id in the page.

   ```text
   # App example is returning 5xx

   Owner: example-team
   Last reviewed: 2026-11-02
   Alert: example-app-5xx

   Use when the alert fires or users cannot complete the main action.
   If you do nothing, users keep failing that action.

   ## Check
   Command: kubectl get deploy app-example -n example
   Expected: READY 2/2 and the digest you deployed
   Otherwise: stop. Escalate to example-team. Do not restart the deploy.

   ## Action
   Command: the first rollback command from the change record
   Expected: the previous digest is running and the 5xx count drops
   Otherwise: stop. Escalate. Do not run a second change.

   ## Escalate
   example-team, in the incident channel, if the expected line is not there after 10 minutes.
   ```

3. One command per step. The operator can paste it. The expected output is a line you have seen, not "it should succeed". If the output is anything else, the step says stop and who to call.

4. A step that changes production names the undo command before the change command. Follow `ops-rollback-plan` and `principle-rollback-first`. The first action during a page is that rehearsed rollback, not a new fix. Follow `ops-incident-response`.

5. Commands that only read can be run twice. A command that creates or updates must also be safe to run twice, or the step says it has already been run and must not be repeated. Follow `principle-idempotent-automation` and `ops-scripting-standards`.

6. Point at a secret by name. The value stays in Key Vault, Secrets Manager, or the pipeline store. Follow `ops-secrets-handling`. Do not paste a connection string into the runbook.

7. Have someone who did not write the runbook follow it on a non-production environment. Fix the step they had to guess. Update the reviewed date. When the deploy path changes, review the runbook in the same change.

8. Keep production steps out of a runbook you have not rehearsed. Name the cluster, namespace, subscription or account, and pipeline the commands touch. Follow `ops-blast-radius`.

## Safety checks

- Every step has one command, the output you expect, and a stop line.
- The alert description links this runbook.
- The owner and the last reviewed date are on the page.
- No secret value, real tenant, real subscription, or real account id is in the page.
- A changing step shows the undo command first.
- Someone other than the author has followed it off production.

## Rollback

The runbook's own undo is the rollback. If a step was wrong and someone ran it, run the undo you wrote above that step and mark the runbook stale until it is corrected. Follow `principle-rollback-first`. Do not leave a known-bad step in the page the alert links to.

## Done when

- The page matches the shape above for this alert.
- A second person has followed it on a non-production environment without inventing a step.
- The alert points at this runbook, and the reviewed date is today.
