# Prompts for aws-cost-review

Example asks for `aws-cost-review`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

A change adds or resizes compute, NAT, a public address, a load balancer, an interface endpoint or more logs.

### Expected for ask 1

- Load `aws-cost-review` and follow that file through its own done-when.
- Step: Put a monthly estimate on the pull request before merge. Name the drivers: instance type and count, Fargate CPU and memory, NAT hourly and per-GB, public IPv4 hourly, interface endpoints per AZ, EBS, cross-AZ transfer, and log ingestion. Follow `principle-cost-awareness`. A plan with no destroys can still add a large bill.
- Check: The pull request states the estimated monthly cost and the main drivers.
- Done when: The estimate, the drivers and the budget are on the change.

## Ask 2

Open Cost Explorer for the paying account.

### Expected for ask 2

- Load `aws-cost-review` and follow that file through its own done-when.
- Step: Open Cost Explorer for the paying account. Group by service. Compare the last full month with the month to date. An organization bill is grouped by linked account as well. Do not stop at the grand total.
- Check: A budget alert covers the paying account at 50, 80 and 100 percent, with no action that stops production.
- Done when: Idle volumes, addresses, load balancers and NAT gateways are listed, not silently deleted.
