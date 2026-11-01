---
name: principle-cost-awareness
description: "Apply before you ship a change that adds or resizes Azure or AWS resources, or that increases log, NAT, public IP or data-transfer use. Price the monthly cost, set a budget alert and drop spend the design does not need."
license: MIT
---

# Cost awareness

Price the change before you ship it. Remove spend the design does not need, and put a budget alert on the account that will pay.

## Use when

- A change adds or resizes Azure or AWS resources.
- The design adds NAT, public IPv4, a firewall, a load balancer, premium disks or more log volume.
- You copy a production SKU into dev or test.
- A subscription or account still has no budget alert.

## Rules

- Put a monthly estimate on the pull request before merge. Use the Azure Pricing Calculator, the AWS Pricing Calculator, or Infracost against the Terraform plan. A plan with no destroys can still add a large bill.
- Name the usual drivers: NAT Gateway hours and processed data, public IPv4, inter-region and internet egress, Azure Firewall, Premium disks, cross-AZ data transfer, and Log Analytics or CloudWatch ingestion.
- Keep dev and test on smaller SKUs, and stop what can stop outside working hours. Production size is not the template for every environment.
- Add a budget and an alert on the subscription or account that pays. A new landing zone without a budget is an incomplete change.
- Compare NAT Gateway hours and data charges with service endpoints or gateway endpoints for traffic that can stay on the provider network. Keep the option that meets the design at the lower monthly cost.
- Set retention, and a daily cap or an ingestion estimate, on diagnostic settings and log groups. Unbounded verbose logs are a cost change.
- If the bill after apply sits well above the estimate, stop and check what was created. Use `principle-observe-before-you-fix` for the metrics and `principle-everything-as-code` if a console edit added the spend.

## Red flags

- The pull request adds a NAT Gateway, a firewall or a premium SKU and states no monthly figure.
- Dev uses the production SKU and the pull request gives no reason.
- Diagnostic settings send full logs and set no retention.
- The merge note says cost will be reviewed later.
- Unattached disks, idle public IP addresses or unused load balancers remain in the account.

## Done when

- The pull request states the estimated monthly cost and the main drivers.
- A budget alert covers the paying subscription or account.
- Spend the design does not need has been removed or explicitly accepted.
