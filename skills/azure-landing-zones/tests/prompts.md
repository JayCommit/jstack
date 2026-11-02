# Prompts for azure-landing-zones

Example asks for `azure-landing-zones`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I add a management group, a subscription, or a hub or Virtual WAN network.

### Expected for ask 1

- Load `azure-landing-zones` and follow that file through its own done-when.
- Step: Read the current tree with `az account management-group list` and the subscription list. The hierarchy is Platform, with Identity, Management and Connectivity under it, plus Landing zones, Sandbox and Decommissioned. The `alz` architecture also places Corp and Online under Landing zones. Keep those groups. Do not add another root, a shadow platform group, or a parallel set of names.
- Check: The groups match the hierarchy above, and no second tree was added.
- Done when: The live tree matches the hierarchy in this skill and the reviewed plan.

## Ask 2

Treat the subscription as the isolation boundary.

### Expected for ask 2

- Load `azure-landing-zones` and follow that file through its own done-when.
- Step: Treat the subscription as the isolation boundary. Put the identity subscription under Identity, log analytics and state storage under Management, and the hub or Virtual WAN under Connectivity. Put each workload environment in its own subscription under Landing zones. Put experiments under Sandbox. Put subscriptions being emptied under Decommissioned, and do not deploy new resources there. Sandbox is not peered to production.
- Check: The module and provider versions are exact pins of releases you reviewed.
- Done when: Each new workload has its own subscription in the correct group.
