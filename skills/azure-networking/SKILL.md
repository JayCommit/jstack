---
name: azure-networking
description: "Use when you change hub or spoke networks, peering, routes, NSGs, private endpoints or Private DNS. Send traffic through the hub firewall and name every route, zone and peering the change can break."
license: MIT
---

# Azure networking

Send spoke traffic through the hub firewall. Peering is not transitive. Name every route, zone and peering you can break.

## Use when

- You add or change a hub VNet, a spoke VNet, a peering or a route table.
- You add an NSG, a private endpoint or a Private DNS zone link.
- A workload cannot resolve a private name or cannot reach another spoke.
- A plan changes a firewall, a route or a peering.

## Steps

1. Read the live hub, spokes, peerings, route tables and DNS links before you edit them. Record the failing path if this is a fix. Follow `principle-observe-before-you-fix`. Do not add a wide allow as the first step.

2. Use the ranges already reserved for this region. In examples the hub is `vnet-hub-example` `10.0.0.0/16` and the spoke is `vnet-spoke-example` `10.1.0.0/16`. Put `AzureFirewallSubnet` at `10.0.0.0/26` or larger. Do not rename that subnet. Do not place other resources in it. The firewall private IP in that subnet is `10.0.0.4`.

3. Peer in both directions. Create `peer-hub-to-spoke-example` on the hub and `peer-spoke-to-hub-example` on the spoke. Allow forwarded traffic so the firewall can send packets on. Do not peer spokes to each other. A spoke reaches another spoke only through the firewall, not through a chain of peerings.

   ```bash
   az network vnet peering create --name peer-hub-to-spoke-example --resource-group rg-hub-example --vnet-name vnet-hub-example --remote-vnet /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-spoke-example/providers/Microsoft.Network/virtualNetworks/vnet-spoke-example --allow-vnet-access --allow-forwarded-traffic
   az network vnet peering create --name peer-spoke-to-hub-example --resource-group rg-spoke-example --vnet-name vnet-spoke-example --remote-vnet /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-hub-example/providers/Microsoft.Network/virtualNetworks/vnet-hub-example --allow-vnet-access --allow-forwarded-traffic
   ```

4. On `rt-spoke-example`, keep the route `default-to-firewall` for `0.0.0.0/0` with next hop type `VirtualAppliance` and next hop `10.0.0.4`. Associate that route table with `snet-app` (`10.1.1.0/24`) and `snet-pe` (`10.1.2.0/24`). Turn off BGP route propagation on the spoke route table so a gateway route does not replace `default-to-firewall`.

   ```bash
   az network route-table route create --resource-group rg-spoke-example --route-table-name rt-spoke-example --name default-to-firewall --address-prefix 0.0.0.0/0 --next-hop-type VirtualAppliance --next-hop-ip-address 10.0.0.4
   ```

5. Put an NSG on every spoke subnet, including `nsg-spoke-app-example` on `snet-app` and an NSG on `snet-pe`. Do not attach an NSG to `AzureFirewallSubnet`. Name each rule you add or remove in the change record. Do not allow inbound management ports from `0.0.0.0/0`. That prefix belongs on `default-to-firewall` only. On `snet-pe`, enable network policies so the NSG applies to private endpoints. Read the subnet first if you are not sure of the current flag value.

6. Put private endpoints in `snet-pe`. Create the Private DNS zone in the hub resource group and link it to `vnet-hub-example` as `link-hub-example`. Also link each spoke that resolves names itself, or send spoke DNS through the hub resolver. A link on the hub alone does not make Azure DNS in the spoke see the zone. Do not enable registration on these zones. Zones this change can break:

   - `privatelink.vaultcore.azure.net`
   - `privatelink.blob.core.windows.net`
   - `privatelink.database.windows.net`

   ```bash
   az network private-dns zone create --resource-group rg-hub-example --name privatelink.vaultcore.azure.net
   az network private-dns link vnet create --resource-group rg-hub-example --zone-name privatelink.vaultcore.azure.net --name link-hub-example --virtual-network vnet-hub-example --registration-enabled false
   ```

7. Repeat that link for `privatelink.blob.core.windows.net` and `privatelink.database.windows.net`. Keep registration off. Confirm both peerings are Connected before you send traffic.

8. If the region uses Virtual WAN, do not also build this hub peering. Connect the spoke with a Virtual WAN VNet connection and route through the firewall in the secured hub. One model per region. Follow `azure-landing-zones`.

9. Authenticate the pipeline with workload identity federation, scoped to the connectivity subscription or the spoke resource group it owns. No client secret, no storage account key, and no service principal password. Follow `principle-least-privilege` and `principle-no-static-credentials`.

10. If Terraform applies the network, pin versions and store state as in `terraform-module-design` and `terraform-state-backends`. Run `terraform plan -out=tfplan`. Name the blast radius: subscriptions, region, VNets, route `default-to-firewall`, peerings `peer-hub-to-spoke-example` and `peer-spoke-to-hub-example`, and DNS link `link-hub-example`. Load `principle-change-safety` before you apply. Load `principle-cost-awareness` when the change adds a firewall or a public IP. Load `principle-everything-as-code` when a peering was created in the portal.

## Safety checks

- Both peering directions exist and show Connected. No spoke-to-spoke peering was added.
- `default-to-firewall` still points at `10.0.0.4`. BGP route propagation is off on the spoke table.
- `AzureFirewallSubnet` is at least `/26` and is named exactly that.
- Every spoke subnet in the change has an NSG. `AzureFirewallSubnet` has none. No new inbound allow comes from `0.0.0.0/0`.
- The Private DNS zones listed above stay linked. Registration is off.
- The plan does not destroy a peering, a route or a zone link unless the change says so.
- The pipeline is federated and the provider pin is exact.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Write the rollback before production. Follow `principle-rollback-first`. Rehearse it on a non-production spoke.

1. Put `default-to-firewall` back to next hop `10.0.0.4` if you changed it.
2. Recreate `peer-hub-to-spoke-example` and `peer-spoke-to-hub-example` if either was deleted. One direction left in place still drops traffic.
3. Restore `link-hub-example` on each zone you unlinked. Deleting a zone is not a rollback step.
4. Do not delete the hub firewall as a rollback.

## Done when

- Spoke egress and spoke-to-spoke traffic go through the hub firewall.
- The peerings, the route and the DNS links named above are in place.
- NSGs are on the subnets this change touched.
- The reviewed plan matches the request, and this environment is checked before promotion.
