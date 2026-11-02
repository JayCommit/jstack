# Prompts for azure-cost-review

Example asks for `azure-cost-review`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

A change adds or resizes Azure resources, or adds NAT, a firewall, a public IP or more log volume.

### Expected for ask 1

- Load `azure-cost-review` and follow that file through its own done-when.
- Step: Put a monthly estimate on the pull request before merge. Name the drivers: VM size and count, Azure Firewall, NAT and public IPv4, Premium disks, egress, and Log Analytics ingestion. Follow `principle-cost-awareness`. A plan with no destroys can still add a large bill.
- Check: The pull request states the estimated monthly cost and the main drivers.
- Done when: The estimate, the drivers and the budget are on the change.

## Ask 2

Open Cost Management for the paying subscription and for the resource group.

### Expected for ask 2

- Load `azure-cost-review` and follow that file through its own done-when.
- Step: Open Cost Management for the paying subscription and for the resource group. Group by service and by resource group. Compare the last full month with the month to date. Do not stop at the subscription total.
- Check: A budget alert covers the paying subscription and the resource group.
- Done when: Idle disks, public IPs, load balancers and application gateways are listed, not silently deleted.
