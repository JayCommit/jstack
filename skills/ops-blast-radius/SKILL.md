---
name: ops-blast-radius
description: "Use when you plan a change across Azure, AWS, or a pipeline. Name every subscription, account, cluster, and pipeline the change can touch before you apply it."
license: MIT
---

# Blast radius

`principle-change-safety` says to name the blast radius. This skill is how you find what else moves when you change one object.

## Use when

- You plan or apply Terraform, or you edit a pipeline that deploys it.
- A change touches a shared network, a shared key, a shared cluster, or a policy above the resource.
- The pull request calls the change small and names no subscription, account, or state key.
- A mitigation during an incident can affect more than the one service. Follow `ops-incident-response`.

## Steps

1. Start from the object you mean to change. List what shares it. Write the list on the pull request. "Small" is not a list. Follow `principle-change-safety`.

2. Terraform. Read the backend key from the root module. Follow `terraform-state-backends`. Every person and every pipeline that uses that key is in the radius. `terraform state list` shows the addresses in this state. A module used by more than one root is more than one apply. Follow `terraform-workspaces-environments`.

   ```text
   terraform state list
   ```

3. Azure. Record the subscription, the resource group, and then the things that reach outside the group: the VNet and its peerings, the Private DNS zone, the Key Vault, the managed identity, and a policy assigned above the subscription. Follow `azure-networking`, `azure-key-vault`, and `azure-landing-zones`. A management group policy hits every subscription under it. List the group, then do not stop there when the network is peered.

   ```bash
   az resource list --resource-group rg-example --output table
   ```

4. AWS. Record the account, the VPC, the security group, the KMS key, and any role that other roles assume. An SCP on a parent OU hits every account under it. Follow `aws-organizations-scps` and `aws-vpc`. A shared image repository or a shared log archive is in the radius when you change its policy.

   ```bash
   aws resourcegroupstaggingapi get-resources --region eu-west-2 --tag-filters Key=example,Values=example
   ```

5. Kubernetes. Record the cluster, the node pool, the namespace, and any NetworkPolicy, quota, or admission rule that selects more than this app. A disruption budget on the namespace affects the neighbours at upgrade time. Follow `k8s-manifest-review`. The cluster path is `azure-aks` or `aws-eks`.

6. Pipeline. List the workflows and environments that use this identity, this variable group, or this state key. A wider federated subject is a wider radius. Follow `pipelines-oidc-federation` and `principle-least-privilege`. The rollback path has to be in the list too. Follow `ops-rollback-plan`.

7. Stop when you cannot name the subscription or account, the state key or the cluster, and the pipeline. Do not apply from a guess. Split a change that crosses two items on the list unless they have to move together, and write why.

## Safety checks

- The pull request names the subscription or account, the region, the network, the state key or cluster, and the pipeline.
- Shared dependents are listed, or you wrote how you checked that there are none.
- A parent policy, SCP, peering, or shared vault is on the list when the change can reach it.
- The apply does not include a second unrelated item from that list.
- The rollback pipeline is inside the same list.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Narrow the change. Revert the part that reached past the list you wrote. Follow `ops-rollback-plan` and `principle-rollback-first`. Do not discover the rest of the radius by reading production after the apply.

## Done when

- The pull request has the list from the safety checks, including how you looked for neighbours.
- The plan or the diff stays inside that list.
- You can point at the pipeline that would roll it back.
