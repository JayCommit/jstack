---
name: aws-cost-review
description: "Use before a change that adds AWS spend, and when you read a bill. Check Cost Explorer, set a budget, right-size from Compute Optimizer, and include NAT, public IPv4 and cross-AZ data transfer."
license: MIT
---

# AWS cost review

Price the change before you ship it. NAT gateways, public IPv4 addresses, interface endpoints and cross-AZ transfer belong in the estimate even when the plan shows no destroy.

## Use when

- A change adds or resizes compute, NAT, a public address, a load balancer, an interface endpoint or more logs.
- You are reading an account bill.
- An account has no budget.
- You see unattached volumes, unassociated addresses, idle load balancers or NAT gateways with no traffic.

## Steps

1. Put a monthly estimate on the pull request before merge. Name the drivers: instance type and count, Fargate CPU and memory, NAT hourly and per-GB, public IPv4 hourly, interface endpoints per AZ, EBS, cross-AZ transfer, and log ingestion. Follow `principle-cost-awareness`. A plan with no destroys can still add a large bill.

2. Open Cost Explorer for the paying account. Group by service. Compare the last full month with the month to date. An organization bill is grouped by linked account as well. Do not stop at the grand total.

   ```bash
   aws ce get-cost-and-usage --time-period Start=2026-10-01,End=2026-11-01 --granularity MONTHLY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE
   ```

3. Set a monthly budget on the account that will grow. Alert at 50 percent, 80 percent and 100 percent of the amount. Record the amount on the change. A budget action that stops production resources is not part of this budget. When the change creates an account, load `aws-organizations-scps`. A new account without a budget is incomplete.

4. Recommend a Compute Savings Plan only after the same usage has been steady. Do not recommend one from the first bill, or while the size is still changing. An EC2 Instance Savings Plan is narrower. Use it when the instance family is the commitment you mean. A Reserved Instance is for a capacity reservation a Savings Plan does not give you. Name the term and the monthly commitment. A one-year or three-year commit is its own reviewed decision.

5. Right-size from Compute Optimizer and from the metric, not from the instance picker. Opt the account in before you treat an empty recommendation as a clean bill. Read CPU, memory and network for the resource before you change its size. Load `principle-observe-before-you-fix` when the resize is a response to an incident. Keep dev and test smaller than production, and stop what can stop outside working hours.

   ```bash
   aws compute-optimizer get-ec2-instance-recommendations --region eu-west-2
   ```

6. List orphans. Do not delete them in this step. A delete is its own change.

   ```bash
   aws ec2 describe-volumes --region eu-west-2 --filters Name=status,Values=available --query "Volumes[].[VolumeId,Size]" --output table
   aws ec2 describe-addresses --region eu-west-2 --query "Addresses[?AssociationId==null].[PublicIp,AllocationId]" --output table
   aws elbv2 describe-load-balancers --region eu-west-2 --query "LoadBalancers[].[LoadBalancerName,State.Code]" --output table
   aws ec2 describe-nat-gateways --region eu-west-2 --filter Name=state,Values=available --query "NatGateways[].[NatGatewayId,SubnetId,State.State]" --output table
   ```

7. A public IPv4 address has an hourly charge while it exists, associated or not. An unassociated address is waste. An associated address is still a line in the estimate. Prefer a gateway endpoint for S3 and DynamoDB over NAT for that traffic. An interface endpoint replaces NAT only when its hourly cost is lower than the NAT data you measured. Load `aws-vpc` when the change adds a NAT gateway or a VPC endpoint.

8. For each load balancer, check target health and request count. A balancer with no healthy targets and a flat request count is idle. Confirm with the metric before you call it idle. Snapshot an EBS volume before any later delete. A volume delete without a snapshot is not reversible.

9. When this change adds a log group, load `aws-cloudwatch` and set its retention. When it creates a cluster, load `aws-eks`. Extended support is a higher control plane price. Do not land a new cluster there.

10. The identity that reads cost gets Cost Explorer read and Compute Optimizer read. It does not get `AdministratorAccess`. When a pipeline reads cost, load `aws-iam-least-privilege` and `principle-no-static-credentials`. Authenticate with the OIDC role.

11. A resize, a Savings Plan purchase or a delete still goes through a reviewed plan. When Terraform applies it, load `terraform-plan-review` and `terraform-state-backends`. Name the account and the resources. Load `principle-change-safety` before you apply.

12. After apply, compare Cost Explorer with the estimate. If the bill is well above it, stop. Do not buy a Savings Plan to hide the gap.

## Safety checks

- The pull request states the estimated monthly cost and the main drivers.
- A budget alert covers the paying account at 50, 80 and 100 percent, with no action that stops production.
- No Savings Plan or Reserved Instance is recommended for usage that is new or still changing.
- The size change cites Compute Optimizer or a metric.
- Orphan lists are attached. Nothing was deleted in the review step.
- NAT, public IPv4, interface endpoints, cross-AZ transfer and new logs are in the estimate when the change adds them.
- The pipeline that would apply a cost change is federated and least privilege.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Write the rollback before production. Follow `principle-rollback-first`.

1. Keep the previous size and the previous plan. Rehearse the reverse plan in a non-production account.
2. Do not delete an unattached volume until a snapshot exists and you have restored a test volume from a snapshot once.
3. A Savings Plan or Reserved Instance is not undone by a Terraform revert. Record the term before you buy.
4. If the bill after apply is well above the estimate, stop and compare the resources created with the plan.

## Done when

- The estimate, the drivers and the budget are on the change.
- Idle volumes, addresses, load balancers and NAT gateways are listed, not silently deleted.
- Any resize or purchase has a reviewed plan and a rehearsed rollback.
- Spend the design does not need is removed or explicitly accepted.
