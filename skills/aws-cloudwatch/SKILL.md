---
name: aws-cloudwatch
description: "Use when you add logs, metrics, alarms or a dashboard. Set a retention on every log group, alarm on the symptom the user hits, and read the series before you change the resource."
license: MIT
---

# CloudWatch

Logs have a retention. An alarm pages on the symptom a user hits, after you have read the series. A dashboard is how the next person checks the same thing.

## Use when

- You create a log group, a metric filter, an alarm or a dashboard.
- A service is failing and someone is about to scale or restart it.
- A log group has no retention, or an alarm has no action.
- You add VPC flow logs, EKS control plane logs or a load balancer access log.

## Steps

1. Read the series and the recent logs before you change the resource. Run a Logs Insights query and `aws cloudwatch get-metric-statistics` for the metric you think is wrong. Follow `principle-observe-before-you-fix`. A restart is not the first step.

   ```text
   fields @timestamp, @message
   | filter @message like /ERROR/
   | sort @timestamp desc
   | limit 20
   ```

2. Set retention on every log group this change creates. A group with no retention keeps logs until someone deletes them, and that is a cost change. Pick the retention the change record names. Thirty days is a starting point for a non-production group. Production retention is a decision you write down. Follow `principle-cost-awareness` and `aws-cost-review`.

   ```bash
   aws logs put-retention-policy --log-group-name /example/app --region eu-west-2 --retention-in-days 30
   ```

3. Send application logs as one structured line per event. A metric filter counts the error string you actually emit. Do not alarm on a filter you have not seen match a real line.

4. Alarm on the symptom. For a service behind a load balancer that is HTTP 5xx count, or target response time, or the age of the oldest queue message. CPU is context. It is not the page by itself. Set the period and the evaluation periods so one spike does not page. Treat missing data as `notBreaching` unless missing data means the job is down.

   ```bash
   aws cloudwatch put-metric-alarm --alarm-name example-app-5xx --region eu-west-2 --namespace AWS/ApplicationELB --metric-name HTTPCode_Target_5XX_Count --dimensions Name=LoadBalancer,Value=app/example/0000000000000000 --statistic Sum --period 60 --evaluation-periods 5 --threshold 10 --comparison-operator GreaterThanThreshold --treat-missing-data notBreaching --alarm-actions arn:aws:sns:eu-west-2:123456789012:example-ops
   ```

5. Replace the load balancer dimension and the threshold with the resource and the number you read from the series. An alarm without an `alarm-actions` ARN does not notify anyone. Send it to an SNS topic the on-call already receives. A composite alarm is how several symptoms become one page. Do not add a second page for the same outage.

6. Build one dashboard per service with the same metrics the alarms use. A dashboard that shows a different statistic than the alarm will be ignored during an incident.

7. Flow logs, EKS control plane logs and load balancer access logs are cost lines. Set their retention in the same change that turns them on. Follow `aws-vpc` and `aws-eks`. Do not turn on verbose logs in every account because production has them.

8. The identity that creates alarms can `cloudwatch:PutMetricAlarm` and `logs:PutRetentionPolicy` on the groups it owns. It does not get a read of every secret. Follow `aws-iam-least-privilege`. If Terraform applies the alarm, follow `terraform-plan-review` and `terraform-state-backends`. One alarm change. Follow `principle-change-safety`.

## Safety checks

- The log group has a retention, and that retention is in the cost note.
- You read the series or the logs before changing the service.
- The alarm metric is the user-facing symptom, with a period and an evaluation count.
- Missing data is set on purpose. The alarm action is an SNS topic the on-call receives.
- The dashboard uses the same metrics as the alarms.
- The identity that writes the alarm cannot read secrets it does not need.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Write the rollback before production. Follow `principle-rollback-first`.

1. Keep the previous alarm JSON from `aws cloudwatch describe-alarms`. Putting that document back is the rollback.
2. Do not delete a log group as a rollback. Shorten retention if the cost is the problem.
3. Rehearse an alarm action on a non-production topic before production depends on it.

## Done when

- New log groups have a retention and an owner.
- Each new alarm has fired in test, or the series shows it would have fired on the last incident.
- The dashboard matches the alarms, and the on-call topic is the action.
