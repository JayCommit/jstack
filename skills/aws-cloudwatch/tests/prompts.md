# Prompts for aws-cloudwatch

Example asks for `aws-cloudwatch`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I create a log group, a metric filter, an alarm or a dashboard.

### Expected for ask 1

- Load `aws-cloudwatch` and follow that file through its own done-when.
- Step: Read the series and the recent logs before you change the resource. Run a Logs Insights query and `aws cloudwatch get-metric-statistics` for the metric you think is wrong. Follow `principle-observe-before-you-fix`. A restart is not the first step.
- Check: The log group has a retention, and that retention is in the cost note.
- Done when: New log groups have a retention and an owner.

## Ask 2

Set retention on every log group this change creates.

### Expected for ask 2

- Load `aws-cloudwatch` and follow that file through its own done-when.
- Step: Set retention on every log group this change creates. A group with no retention keeps logs until someone deletes them, and that is a cost change. Pick the retention the change record names. Thirty days is a starting point for a non-production group. Production retention is a decision you write down. Follow `principle-cost-awareness` and `aws-cost-review`.
- Check: You read the series or the logs before changing the service.
- Done when: Each new alarm has fired in test, or the series shows it would have fired on the last incident.
