# Prompts for azure-aks

Example asks for `azure-aks`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I create an AKS cluster or a node pool.

### Expected for ask 1

- Load `azure-aks` and follow that file through its own done-when.
- Step: Read the cluster before you change it. Run `az aks show --resource-group rg-example --name aks-example --output table` and `az aks get-upgrades --resource-group rg-example --name aks-example --output table`. Record the current version, the node pool versions and the error text if something is unhealthy. Load `principle-observe-before-you-fix` when the cluster is unhealthy. Do not restart nodes as the first step.
- Check: The API server is private, or the change record says why the network cannot reach it yet and the apply has stopped.
- Done when: The cluster matches the private, RBAC and workload-identity settings above.

## Ask 2

Use a private cluster when the network can reach a private API server.

### Expected for ask 2

- Load `azure-aks` and follow that file through its own done-when.
- Step: Use a private cluster when the network can reach a private API server. If it cannot, stop and add that path. Do not switch the API server to public to get unblocked. Follow `azure-networking` for the spoke path.
- Check: Overlay, network policy, Azure RBAC, OIDC and workload identity are on. Local accounts are off. Pod identity is off.
- Done when: System and user pools are split, and the version pin matches the live control plane.
