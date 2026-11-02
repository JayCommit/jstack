---
name: aws-eks
description: "Use when you create or upgrade an EKS cluster. Prefer a private API endpoint, Pod Identity for new pods, managed node groups or Karpenter, and move one Kubernetes minor at a time."
license: MIT
---

# Elastic Kubernetes Service

Create a private cluster. Give pods their own roles. Upgrade one minor at a time, control plane first unless an upgrade insight says an add-on blocks it.

## Use when

- You create an EKS cluster, a managed node group or a Karpenter pool.
- You upgrade the control plane, a node group or an add-on.
- A pod needs AWS API access, or a cluster still uses the `aws-auth` ConfigMap for a new mapping.
- A node group still launches with an Amazon Linux 2 AMI.

## Steps

1. Read the cluster before you change it. Run `aws eks describe-cluster --name eks-example --region eu-west-2` and `aws eks list-insights --cluster-name eks-example --region eu-west-2`. Record the version, whether the API is public, the node group versions and any insight in `ERROR` or `WARNING`. Follow `principle-observe-before-you-fix`.

2. For a new cluster, choose a version that `aws eks describe-cluster-versions --version-status STANDARD_SUPPORT --region eu-west-2` lists. Extended support costs more. Do not start a cluster there. Follow `aws-cost-review`.

3. Keep the API private when the network can reach it. If it cannot, stop and add that path. Do not open the public endpoint to get unblocked. Place the cluster in the private subnets from `aws-vpc`. On the same `create-cluster` call, encrypt Kubernetes secrets with a customer managed key and enable log types `api`, `audit`, `authenticator`, `controllerManager` and `scheduler`. Set retention on those groups. Follow `aws-cloudwatch`. The command below shows the network shape. Add the key and the log types before you run it.

   ```bash
   aws eks create-cluster --name eks-example --region eu-west-2 --kubernetes-version 1.33 --role-arn arn:aws:iam::123456789012:role/eks-cluster-example --resources-vpc-config subnetIds=subnet-examplea,subnet-exampleb,endpointPublicAccess=false,endpointPrivateAccess=true
   ```

4. Replace `1.33` with the standard-support version you chose. The cluster role is `AmazonEKSClusterPolicy` only. Do not attach `AdministratorAccess` to it.

5. Use a managed node group or Karpenter for new compute. Do not add both to the same pool in one change. New AMIs are Amazon Linux 2023 or Bottlerocket. Do not start a node group on Amazon Linux 2. Require IMDSv2 and set the hop limit to 1 so a pod cannot use the node role. Nodes go in private subnets and do not get a public IP. Do not copy the production instance size into dev or test. Follow `principle-cost-awareness`.

6. On a new cluster, install the `eks-pod-identity-agent` add-on before nodes join, at a version `aws eks describe-addon-versions` lists for this Kubernetes version. Create the VPC CNI Pod Identity role and association first. Then leave `AmazonEKS_CNI_Policy` off the node role. The node role keeps `AmazonEKSWorkerNodePolicy` and `AmazonEC2ContainerRegistryReadOnly`.

7. Give each new workload Pod Identity. The role trusts `pods.eks.amazonaws.com` for `sts:AssumeRole` and `sts:TagSession`. The association names this cluster, one namespace and one service account. The role's identity policy is the job, as in `aws-iam-least-privilege`.

   ```bash
   aws eks create-pod-identity-association --cluster-name eks-example --region eu-west-2 --namespace app --service-account app --role-arn arn:aws:iam::123456789012:role/app-example
   ```

8. Use IRSA only for Fargate, for Windows nodes, or for an SDK that does not support Pod Identity. Keep IRSA that is already in production. Map new human and role access with EKS access entries. Do not add a new mapping to the `aws-auth` ConfigMap.

9. For Karpenter, use `karpenter.sh/v1` NodePool and `karpenter.k8s.aws/v1` EC2NodeClass. Do not add a `Provisioner`. Upgrade a pre-v1 Karpenter in its own change before you add a NodePool. Pin an AL2023 alias you have reviewed. Do not use `@latest`. Set a CPU limit on the pool. Select private subnets, set `associatePublicIPAddress` to false, and set the metadata hop limit to 1. The controller role is Pod Identity, not the node role. Consolidation must respect pod disruption budgets. On EKS Auto Mode the compute is a NodePool and Pod Identity is the pod identity. Do not add a self-managed node group beside it in the same change.

10. Upgrade one minor at a time. Read insights first and clear any add-on they mark as blocking. Then upgrade the control plane, then node groups, then the remaining add-ons to versions compatible with the new cluster. Pin each add-on version. The control plane does not downgrade. Follow `principle-rollback-first`.

    ```bash
    aws eks update-cluster-version --name eks-example --region eu-west-2 --kubernetes-version 1.33
    aws eks update-nodegroup-version --cluster-name eks-example --region eu-west-2 --nodegroup-name system --kubernetes-version 1.33
    ```

11. If Terraform applies the cluster, follow `terraform-plan-review` and `terraform-state-backends`. Name the account, the cluster, the node groups and the pipeline. Follow `principle-change-safety`.

## Safety checks

- The API endpoint is private, or the change record says why the network cannot reach it yet and the apply has stopped.
- The version is one you listed under standard support, at most one minor ahead.
- New pods use Pod Identity, except Fargate, Windows or an SDK that cannot. The node hop limit is 1.
- The node role does not carry the VPC CNI policy on a new cluster. Nobody added an `aws-auth` mapping.
- Karpenter, if used, pins an AMI alias and a CPU limit, and its controller is not the node role.
- Add-on versions were read from `describe-addon-versions`, not typed from memory.
- Upgrade insights were read. The control plane moves before the node groups.

## Rollback

The control plane does not downgrade. Write that limit down before production. Follow `principle-rollback-first`.

1. Before the control plane upgrade, rollback is not starting the upgrade.
2. After the control plane has moved, fix forward to a version `describe-cluster-versions` lists. Do not invent a downgrade command.
3. Rehearse the node group upgrade on a non-production cluster. Keep the previous node group AMI until that rehearsal has worked.
4. Delete a bad Pod Identity association and leave the role if another association still uses it.

## Done when

- The cluster matches the private endpoint, identity and AMI choices above.
- Workload roles are scoped to one namespace and one service account.
- The live control plane and the node group show the version you planned.
- The change is verified on this cluster before anyone promotes it.
