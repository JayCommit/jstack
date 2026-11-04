# Create a private AKS cluster

You need a cluster the pipeline can deploy to, with a private API server and no local accounts.

## Ask this

```text
Create AKS in subscription 00000000-0000-0000-0000-000000000000,
resource group rg-example, region uksouth, name aks-example.
Private API, Azure CNI overlay, Azure RBAC, workload identity.
User-assigned cluster identity id-aks-example.
System pool and user pool stay split.
Load azure-aks, azure-networking, principle-least-privilege, and principle-cost-awareness.
Price the node size before apply. Stop before apply.
```

## Load

- `azure-aks` keeps the API private, uses Azure CNI overlay, Azure RBAC, and workload identity, and splits system and user pools. The cluster identity is user-assigned.
- `azure-networking` is the spoke path to that private API. Load it before anyone opens the API to the internet to get unblocked.
- `principle-least-privilege` keeps Cluster Admin off the pipeline. Deployers get the Kubernetes RBAC role the skill names.
- `principle-cost-awareness` prices the node SKU and the count. Dev and test do not copy the production size.

## What good looks like

The change record says the API is private, local accounts are off, and pod identity is off. Application pods are on the user pool. The version is one exact patch, one minor at a time.

The agent does not run `az aks get-credentials --admin`. It stops before the create or the upgrade. The control plane does not downgrade, so the rollback is written before the upgrade starts.
