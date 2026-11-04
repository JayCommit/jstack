# Price an Azure change

The pull request adds virtual machines, a firewall, a public IP, NAT, or more log volume. Price it before anyone applies.

## Ask this

```text
This change adds nodes and a public IP in subscription 00000000-0000-0000-0000-000000000000,
resource group rg-example.
Load azure-cost-review and principle-cost-awareness.
Put a monthly estimate and a budget on the pull request.
List orphaned disks and unused public IPs. Do not delete them. Stop before apply.
```

## Load

- `azure-cost-review` estimates the change, sets a budget, right-sizes from metrics, and lists orphaned disks, public IPs, idle load balancers, and unused application gateways.
- `principle-cost-awareness` is the rule the estimate has to satisfy. A plan with no destroys can still add a large bill.

## What good looks like

The pull request states the monthly estimate and the drivers: VM size and count, firewall, NAT, public IPv4, disks, egress, and log ingestion. A budget alert covers the subscription and the resource group.

Orphans are listed. Nothing is deleted in the review. A resize still goes through a reviewed plan. The agent stops before that apply.
