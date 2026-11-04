---
name: ops-observability-alerts
description: "Use when you add an alert or an SLO. Page on the symptom the user hits, attach one runbook, and wire Azure Monitor or CloudWatch only after you have read the series."
license: MIT
---

# Observability and alerts

Page when a user is hurt and a person must act. Everything else is a ticket. Every page names one runbook.

## Use when

- You add an SLO, an alert, an action group, or a dashboard.
- An alert fires on CPU, on a single log line, or on a metric nobody has read.
- A page has no runbook, or two alerts page for the same outage.
- You are about to scale or restart a service from a chart you have not read.

## Steps

1. Read the series and the recent logs before you add the alert or change the service. Follow `principle-observe-before-you-fix`. Record the symptom you can already see: failed requests, latency, queue age, or a failed synthetic check. CPU and memory are context. They are not the page by themselves.

2. Write the SLI and the SLO on the change. The SLI is the user action. The SLO is the target over 30 days, such as 99.9% of requests succeeding, or 99% of them finishing under the latency the user can feel. The error budget is what remains. Do not copy the production SLO onto dev.

3. Page on a fast burn. Ticket on a slow burn. For a 30-day SLO, page when the last hour has used about 2% of the error budget and the last five minutes are still burning. Open a ticket when the last six hours have used about 5% and the last thirty minutes agree. A one-minute spike does not page. The page and the ticket are two alerts. The ticket action does not page.

4. One alert is one symptom. Do not add a second page for the same failed user action. Put the runbook URL in the alert description. The runbook is `ops-runbook-authoring`. An alert with no runbook is unfinished.

5. On AWS, create the alarm as in `aws-cloudwatch`. Put the runbook URL in the alarm description. Use the same metric on the dashboard. Retention, missing data and the SNS topic stay in that skill.

6. On Azure, send the page to an action group the on-call already receives. Prove the action group with a test notification before production depends on it. Set the workspace retention you wrote down. A workspace with no retention is a cost. Follow `principle-cost-awareness` and `azure-cost-review`.

   ```bash
   az monitor action-group create --resource-group rg-example --name ag-example --short-name example --action email oncall ops@example.com
   az monitor metrics alert create --name example-app-5xx --resource-group rg-example --scopes /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-example/providers/Microsoft.Web/sites/app-example --condition "total Http5xx > 10" --window-size 5m --evaluation-frequency 1m --action ag-example --description "Runbook: https://example.com/runbooks/app-example-5xx"
   ```

7. Replace the scope, the condition and the threshold with the resource and the number you read in step 1. A log alert queries a line you have already seen match. This query only counts. It is not an alert until you have seen it return rows for a real failure.

   ```text
   AppRequests
   | where TimeGenerated > ago(1h)
   | where ResultCode startswith "5"
   | summarize count()
   ```

8. Treat missing data on purpose. A synthetic check that stops reporting is a page. A missing CPU sample is not. Do not turn on verbose logs in every subscription because production has them.

9. The identity that creates the alert can write this alert and this action group. It cannot read secrets. Follow `principle-least-privilege`. If Terraform applies the alert, follow `terraform-plan-review` and `terraform-state-backends`. One alert change. Follow `principle-change-safety`.

## Safety checks

- You read the series or the logs before adding the alert.
- The page is the user-facing symptom, with a fast-burn window, not a one-minute spike.
- The ticket path does not page.
- The alert description contains one runbook URL.
- The Azure action group or the CloudWatch alarm action reaches the on-call, and you have tested it off production.
- The dashboard uses the same SLI as the alert.
- Log retention is set, and the cost is on the change.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Write the rollback before production. Follow `principle-rollback-first`.

1. Keep the previous alert. Deleting the alert you just added, or putting the previous definition back, is the rollback. Do not delete the workspace or the log group.
2. Rehearse the action group on a non-production address before it can page the production on-call.
3. If a new alert is paging on noise, disable that alert. Do not raise the threshold until the series says the original line was wrong.

## Done when

- The SLO, the SLI and the burn windows are written on the change.
- The alert has fired in test, or the series shows it would have fired on the last incident.
- The runbook URL resolves, and the on-call path was tested.
- The dashboard matches the alert.
