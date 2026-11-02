# Prompts for aws-eks

Example asks for `aws-eks`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I create an EKS cluster, a managed node group or a Karpenter pool.

### Expected for ask 1

- Load `aws-eks` and follow that file through its own done-when.
- Step: Read the cluster before you change it. Run `aws eks describe-cluster --name eks-example --region eu-west-2` and `aws eks list-insights --cluster-name eks-example --region eu-west-2`. Record the version, whether the API is public, the node group versions and any insight in `ERROR` or `WARNING`. Follow `principle-observe-before-you-fix`.
- Check: The API endpoint is private, or the change record says why the network cannot reach it yet and the apply has stopped.
- Done when: The cluster matches the private endpoint, identity and AMI choices above.

## Ask 2

For a new cluster, choose a version that `aws eks describe-cluster-versions --version-status STANDARD_SUPPORT --region eu-west-2` lists.

### Expected for ask 2

- Load `aws-eks` and follow that file through its own done-when.
- Step: For a new cluster, choose a version that `aws eks describe-cluster-versions --version-status STANDARD_SUPPORT --region eu-west-2` lists. Extended support costs more. Do not start a cluster there. Follow `aws-cost-review`.
- Check: The version is one you listed under standard support, at most one minor ahead.
- Done when: Workload roles are scoped to one namespace and one service account.
