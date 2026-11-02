---
name: azure-cost-review
description: "Use before a change that adds Azure spend, and when you read a bill. Check Cost Management, set a budget alert, right-size from metrics, and list orphaned disks, public IPs, idle load balancers and unused application gateways."
license: MIT
---

# Azure cost review

Price the change before you ship it. A cost change still goes through a reviewed plan.

## Use when

- A change adds or resizes Azure resources, or adds NAT, a firewall, a public IP or more log volume.
- You are reading a subscription or resource group bill.
- A subscription or resource group has no budget alert.
- You see unattached disks, idle public IPs, load balancers or application gateways.

## Steps

1. Put a monthly estimate on the pull request before merge. Name the drivers: VM size and count, Azure Firewall, NAT and public IPv4, Premium disks, egress, and Log Analytics ingestion. Follow `principle-cost-awareness`. A plan with no destroys can still add a large bill.

2. Open Cost Management for the paying subscription and for the resource group. Group by service and by resource group. Compare the last full month with the month to date. Do not stop at the subscription total.

3. Set a monthly budget on that subscription and on the resource group that will grow. Alert at 50 percent, 80 percent and 100 percent of the amount. Record the amount on the change. A new landing zone without a budget is incomplete. Follow `azure-landing-zones`.

4. Recommend a reservation or a savings plan only after the same SKU has been steady. Do not recommend one from the first bill, or while the size is still changing. Name the term and the monthly commitment on the change. A one-year or three-year commit is its own reviewed decision.

5. Right-size from metrics, not from the SKU picker. Read CPU, memory and connection counts for the resource. Follow `principle-observe-before-you-fix`. A larger SKU is not a diagnosis. Keep dev and test on smaller SKUs than production, and stop what can stop outside working hours.

6. List orphans. Do not delete them in this step. A delete is its own change.

```bash
az disk list --query "[?diskState=='Unattached'].[name,resourceGroup,diskSizeGb]" --output table
az network public-ip list --query "[?ipConfiguration==null].[name,resourceGroup]" --output table
az network lb list --query "[].[name,resourceGroup]" --output table
az network application-gateway list --query "[].[name,resourceGroup]" --output table
```

7. For each load balancer, check backend pools and outbound rules. For each application gateway, check listeners, backends and recent throughput. An empty pool or a flat zero throughput series is unused. Confirm with the metrics before you call it idle. A name on this list is not enough.

8. Snapshot a disk before any later delete. A disk delete without a snapshot is not reversible. Write that rollback before production. Follow `principle-rollback-first`.

```bash
az snapshot create --resource-group rg-example --name snap-disk-example --source disk-example
```

9. Check diagnostic settings on resources this change adds. Set retention and a daily cap, or an ingestion estimate, on Log Analytics. Unbounded verbose logs are a cost change. Do not copy the production retention into dev.

10. If the change adds a public IP, a NAT gateway or Azure Firewall, include the hourly charge and the processed-data charge. Drop the resource when a private endpoint or a service endpoint meets the design at a lower monthly cost. Record the choice.

11. The identity that reads cost gets Cost Management Reader on the subscription or the resource group. It does not get Owner. Authenticate with workload identity federation. No client secret and no storage account key. Follow `principle-least-privilege` and `principle-no-static-credentials`.

12. A resize, a reservation or a delete still goes through `terraform plan -out=tfplan` or `az deployment group what-if`. Pin `hashicorp/azurerm` `4.14.0` and Terraform `1.10.5` when Terraform applies it. Use a remote backend with the blob lease lock and Azure AD auth. Name the blast radius. Follow `principle-change-safety`. Import a portal resize or revert it. Follow `principle-everything-as-code`.

13. After apply, open Cost Management again and compare the new resources with the estimate. If the bill is well above it, stop. Do not buy a reservation to hide the gap.

## Safety checks

- The pull request states the estimated monthly cost and the main drivers.
- A budget alert covers the paying subscription and the resource group.
- No reservation or savings plan is recommended for a SKU that is new or still changing.
- The SKU change cites a metric, not the portal picker.
- Orphan lists are attached. Nothing was deleted in the review step.
- The pipeline that would apply a cost change is federated and least privilege.
- The reviewed plan matches the cost change and nothing else.
- Log retention and any new firewall, NAT or public IP are in the estimate.
- A disk delete has a snapshot, and that snapshot was restored once in test.

## Rollback

Write the rollback before production. Follow `principle-rollback-first`.

1. Keep the previous SKU and the previous plan. Rehearse the reverse plan on dev or test.
2. Do not delete an unattached disk until a snapshot exists and you have restored a test disk from a snapshot once.
3. A reservation purchase is not undone by a Terraform revert. Record the vendor term before you buy.
4. If the bill after apply is well above the estimate, stop and compare the resources created with the plan.

## Done when

- The estimate, the drivers and the budget are on the change.
- Idle disks, public IPs, load balancers and application gateways are listed, not silently deleted.
- Any resize or purchase has a reviewed plan and a rehearsed rollback.
- Spend the design does not need is removed or explicitly accepted.
