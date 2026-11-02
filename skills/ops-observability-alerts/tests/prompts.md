# Prompts for ops-observability-alerts

Example asks for `ops-observability-alerts`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I add an SLO, an alert, an action group, or a dashboard.

### Expected for ask 1

- Load `ops-observability-alerts` and follow that file through its own done-when.
- Step: Read the series and the recent logs before you add the alert or change the service. Follow `principle-observe-before-you-fix`. Record the symptom you can already see: failed requests, latency, queue age, or a failed synthetic check. CPU and memory are context. They are not the page by themselves.
- Check: You read the series or the logs before adding the alert.
- Done when: The SLO, the SLI and the burn windows are written on the change.

## Ask 2

Write the SLI and the SLO on the change.

### Expected for ask 2

- Load `ops-observability-alerts` and follow that file through its own done-when.
- Step: Write the SLI and the SLO on the change. The SLI is the user action. The SLO is the target over 30 days, such as 99.9% of requests succeeding, or 99% of them finishing under the latency the user can feel. The error budget is what remains. Do not copy the production SLO onto dev.
- Check: The page is the user-facing symptom, with a fast-burn window, not a one-minute spike.
- Done when: The alert has fired in test, or the series shows it would have fired on the last incident.
