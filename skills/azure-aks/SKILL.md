---
name: azure-aks
description: "Use when you create or upgrade an AKS cluster. Prefer a private cluster, Azure CNI overlay, Azure RBAC and workload identity, keep system and user pools apart, and move one Kubernetes minor at a time."
license: MIT
---

# Azure Kubernetes Service

Create a private cluster with Azure RBAC and workload identity. Upgrade one minor at a time, control plane first.

## Use when

- You create an AKS cluster or a node pool.
- You upgrade the control plane or a node pool.
- You turn on workload identity, Azure RBAC or a private API server.
- A cluster still uses local accounts or the AAD pod-identity addon.

## Steps

1. Read the cluster before you change it. Run `az aks show --resource-group rg-example --name aks-example --output table` and `az aks get-upgrades --resource-group rg-example --name aks-example --output table`. Record the current version, the node pool versions and the error text if something is unhealthy. Follow `principle-observe-before-you-fix`. Do not restart nodes as the first step.

2. Use a private cluster when the network can reach a private API server. If it cannot, stop and add that path. Do not switch the API server to public to get unblocked. Follow `azure-networking` for the spoke path.

3. Use Azure CNI overlay unless the design needs a subnet address per pod. Turn network policy on. Use Azure network policy unless the design already chose Cilium. Keep local accounts disabled. Turn on Azure RBAC for Kubernetes authorization, the OIDC issuer and workload identity. Do not pass `--enable-pod-identity`. Do not install AAD pod-identity. If that addon is already on, remove it in its own change before you add workload identity.

4. Keep a system node pool for system pods only. Put application pods on user node pools. Create the user-assigned identity `id-aks-example` before the cluster and pass it as `--assign-identity`. Do not copy the production VM size into dev or test. Price the node SKU and the count before you apply. Follow `principle-cost-awareness`.

   ```bash
   az aks create --resource-group rg-example --name aks-example --location uksouth --kubernetes-version 1.31.1 --network-plugin azure --network-plugin-mode overlay --network-policy azure --enable-private-cluster --disable-local-accounts --enable-aad --enable-azure-rbac --enable-oidc-issuer --enable-workload-identity --assign-identity /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-example/providers/Microsoft.ManagedIdentity/userAssignedIdentities/id-aks-example --nodepool-name system --node-count 2
   az aks nodepool add --resource-group rg-example --cluster-name aks-example --name user --mode User --node-count 2 --max-surge 1
   ```

5. Replace `1.31.1` with the full patch you planned. It must appear in `az aks get-upgrades` or `az aks get-versions --location uksouth --output table`. Do not pass `latest`. Do not commit an SSH private key. Disable node SSH if the CLI requires a key and the design does not need SSH.

6. Authenticate the pipeline and the pods with workload identity federation. No client secret and no service principal password. The cluster identity and the deploy identity are user-assigned managed identities. Follow `principle-no-static-credentials` and `azure-rbac-entra`. Grant Azure Kubernetes Service Cluster User Role only to callers who may fetch a non-admin kubeconfig. Grant Azure Kubernetes Service RBAC Writer to deployers. Do not grant RBAC Cluster Admin to every pipeline. Do not run `az aks get-credentials --admin`. Follow `principle-least-privilege`.

7. If Terraform owns the cluster, pin `hashicorp/azurerm` `4.14.0` and Terraform `1.10.5`. Use a remote backend with the blob lease lock and Azure AD auth. Do not set a storage account key. Codify portal edits. Follow `principle-everything-as-code`.

8. Upgrade one Kubernetes minor at a time. Do not skip a minor. Turn cluster autoupgrade off only as its own reviewed change. Autoupgrade blocks `--control-plane-only`.

9. Read pod disruption budgets with `kubectl get pdb -A`. If `minAvailable` equals the replica count, fix the budget before you upgrade nodes. Do not pass `--enable-force-upgrade`.

10. Upgrade the control plane, confirm it, then upgrade user node pools. Set max surge before the node upgrade. System pool upgrades are a separate step from the user pool.

    ```bash
    az aks upgrade --resource-group rg-example --name aks-example --control-plane-only --kubernetes-version 1.31.1
    az aks nodepool update --resource-group rg-example --cluster-name aks-example --name user --max-surge 1
    az aks nodepool upgrade --resource-group rg-example --cluster-name aks-example --name user --kubernetes-version 1.31.1
    ```

11. Name the blast radius: subscription, resource group, cluster, node pools, state key and pipeline. One change. Follow `principle-change-safety`.

12. Confirm the result. `az aks show --resource-group rg-example --name aks-example --query kubernetesVersion --output tsv` must be the patch you planned. `az aks nodepool list --resource-group rg-example --cluster-name aks-example --output table` must show that same patch on the user pool before you promote.

13. Federate each workload identity to its Kubernetes service account. The subject is `system:serviceaccount:<namespace>:<service-account>`. Take the issuer from `az aks show --resource-group rg-example --name aks-example --query oidcIssuerProfile.issuerUrl --output tsv`. The audience is `api://AzureADTokenExchange`. Do not print the token. Follow `azure-rbac-entra`.

## Safety checks

- The API server is private, or the change record says why the network cannot reach it yet and the apply has stopped.
- Overlay, network policy, Azure RBAC, OIDC and workload identity are on. Local accounts are off. Pod identity is off.
- System and user pools are separate. Application pods are not on the system pool.
- The target version is the exact patch you planned, one minor ahead at most.
- Pod disruption budgets allow the surge. Force upgrade is not set.
- The pipeline is federated and does not use admin kubeconfig.
- Provider and Terraform versions are pinned when Terraform applies the cluster.
- The live control plane and the user pool show the planned patch.
- Each workload subject uses this cluster's OIDC issuer and one service account.

## Rollback

The control plane does not downgrade. Write that limit down before production. Follow `principle-rollback-first`.

1. Before the control plane upgrade, rollback is not starting the upgrade.
2. After the control plane has moved, fix forward to a patch `az aks get-upgrades` lists. Do not invent a downgrade command.
3. Rehearse the node-pool upgrade on a non-production cluster. Confirm the previous user-pool version is still allowed before you depend on a node-pool rollback.
4. Stop if the only rollback is `--enable-force-upgrade`.

## Done when

- The cluster matches the private, RBAC and workload-identity settings above.
- System and user pools are split, and the version pin matches the live control plane.
- Node pools have caught up one minor, with disruption budgets respected.
- The change is verified on this cluster before anyone promotes it.
