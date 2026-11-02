# Prompts for ops-runbook-authoring

Example asks for `ops-runbook-authoring`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I add an alert and it needs a runbook. Follow `ops-observability-alerts`.

### Expected for ask 1

- Load `ops-runbook-authoring` and follow that file through its own done-when.
- Step: Put the runbook where the on-call already looks, and link it from the alert description. One alert, one runbook. Name the owner and the date you last ran the steps.
- Check: Every step has one command, the output you expect, and a stop line.
- Done when: The page matches the shape above for this alert.

## Ask 2

Use this shape.

### Expected for ask 2

- Load `ops-runbook-authoring` and follow that file through its own done-when.
- Step: Use this shape. Replace the placeholders. Do not put a secret value, a real subscription, or a real account id in the page.
- Check: The alert description links this runbook.
- Done when: A second person has followed it on a non-production environment without inventing a step.
