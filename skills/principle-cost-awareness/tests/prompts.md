# Prompts for principle-cost-awareness

Example asks for `principle-cost-awareness`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

A change adds or resizes Azure or AWS resources.

### Expected for ask 1

- Load `principle-cost-awareness` and follow that file through its own done-when.
- Rule: Put a monthly estimate on the pull request before merge. Use the Azure Pricing Calculator, the AWS Pricing Calculator, or Infracost against the Terraform plan. A plan with no destroys can still add a large bill.
- Red flag: The pull request adds a NAT Gateway, a firewall or a premium SKU and states no monthly figure.
- Done when: The pull request states the estimated monthly cost and the main drivers.

## Ask 2

Name the usual drivers: NAT Gateway hours and processed data, public IPv4, inter-region and internet egress, Azure Firewall, Premium disks, cross-AZ data transfer, and Log Analytics or CloudWatch ingestion.

### Expected for ask 2

- Load `principle-cost-awareness` and follow that file through its own done-when.
- Rule: Name the usual drivers: NAT Gateway hours and processed data, public IPv4, inter-region and internet egress, Azure Firewall, Premium disks, cross-AZ data transfer, and Log Analytics or CloudWatch ingestion.
- Red flag: Dev uses the production SKU and the pull request gives no reason.
- Done when: A budget alert covers the paying subscription or account.
