# Prompts for azure-networking

Example asks for `azure-networking`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I add or change a hub VNet, a spoke VNet, a peering or a route table.

### Expected for ask 1

- Load `azure-networking` and follow that file through its own done-when.
- Step: Read the live hub, spokes, peerings, route tables and DNS links before you edit them. Record the failing path if this is a fix. Follow `principle-observe-before-you-fix`. Do not add a wide allow as the first step.
- Check: Both peering directions exist and show Connected. No spoke-to-spoke peering was added.
- Done when: Spoke egress and spoke-to-spoke traffic go through the hub firewall.

## Ask 2

Use the ranges already reserved for this region.

### Expected for ask 2

- Load `azure-networking` and follow that file through its own done-when.
- Step: Use the ranges already reserved for this region. In examples the hub is `vnet-hub-example` `10.0.0.0/16` and the spoke is `vnet-spoke-example` `10.1.0.0/16`. Put `AzureFirewallSubnet` at `10.0.0.0/26` or larger. Do not rename that subnet. Do not place other resources in it. The firewall private IP in that subnet is `10.0.0.4`.
- Check: `default-to-firewall` still points at `10.0.0.4`. BGP route propagation is off on the spoke table.
- Done when: The peerings, the route and the DNS links named above are in place.
