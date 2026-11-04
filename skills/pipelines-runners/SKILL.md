---
name: pipelines-runners
description: "Use when you add or harden a GitHub Actions runner or an Azure DevOps agent pool. Keep it ephemeral, keep cloud keys off the host, and keep untrusted builds away from the production network."
license: MIT
---

# Runners and agent pools

A runner you operate is a machine on your network. Hosted runners stay the default. A persistent VM with a cloud key on disk is not a runner design.

## Use when

- You add, replace, or harden a GitHub Actions runner, a runner group, or a larger runner.
- You add or change an Azure DevOps agent pool or a Managed DevOps Pool that you operate.
- A job is about to run on a VM that already holds a cloud key, a kubeconfig, or a long-lived registration token.
- A public repository or a fork pull request would land on a self-hosted runner.

## Steps

1. Use a GitHub-hosted runner when the job only needs the public internet. On Azure DevOps, the hosted image versus a named pool is decided in `pipelines-azure-devops-yaml`. Follow that step. Add a runner you operate only when the job must reach a private network you can name. A larger runner is a cost. Follow `principle-cost-awareness`.

2. Make that runner ephemeral. One job, then the machine is destroyed. Do not reuse a VM that keeps a workspace, a Docker layer with a secret, or a cloud credential. A registration token is short-lived and is not baked into the image.

3. Do not register a self-hosted runner for a public repository. Fork pull requests from that repository must not schedule onto it. A private repository that builds untrusted code uses a different runner group, with no production network and no production identity. On Azure DevOps, a production deploy pool that also builds untrusted forks is already rejected by `pipelines-azure-devops-yaml`.

4. The job authenticates with federation for that run. Follow `pipelines-oidc-federation`. No access key, client secret, or kubeconfig is on the image. Workflow permissions stay in `pipelines-github-actions-authoring`.

5. Treat labels as an allow-list. `runs-on` matches a runner group this repository is allowed to use. Do not use a label that any repository in the organisation can schedule. A queued job whose label matches nothing is a routing fault. Follow `pipelines-github-actions-debugging` after you have read the log. Do not "fix" it by widening the group.

6. The runner reaches the control plane and the private endpoints named on the change. It does not have a path to the data subnet beyond those endpoints. Follow `azure-networking` or `aws-vpc`.

7. Name the pool, the repositories that can use it, the network path, and the pipeline. Follow `ops-blast-radius`. The agent prepares the change and stops. Follow `principle-stop-at-approval`.

## Safety checks

- A job that only needs the public internet stays on a hosted runner.
- The runner is destroyed after the job. The image has no cloud key and no kubeconfig.
- A public repository has no self-hosted runner. Untrusted builds are not on the production pool.
- The runner group is limited to the repositories that need the private path.
- Egress is the endpoints on the change, not the whole data subnet.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Deregister the runner and destroy the machine. Point the workflow or the pipeline back at the hosted label it used before. Follow `principle-rollback-first`. Do not leave a deregistered VM running with the old credentials on disk. If a job is in progress on that runner, wait for it or cancel it before you destroy the machine, and say which you did.

## Done when

- The pool is hosted, or it is ephemeral, scoped to named repositories, and free of long-lived cloud keys.
- A public repository and untrusted fork builds do not land on it.
- The network path is the one written on the change.
