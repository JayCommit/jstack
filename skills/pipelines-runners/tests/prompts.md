# Prompts for pipelines-runners

Example asks for `pipelines-runners`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I add, replace, or harden a GitHub Actions runner, a runner group, or a larger runner.

### Expected for ask 1

- Load `pipelines-runners` and follow that file through its own done-when.
- Step: Use a GitHub-hosted runner when the job only needs the public internet. On Azure DevOps, the hosted image versus a named pool is decided in `pipelines-azure-devops-yaml`. Follow that step. Add a runner you operate only when the job must reach a private network you can name. A larger runner is a cost. Follow `principle-cost-awareness`.
- Check: A job that only needs the public internet stays on a hosted runner.
- Done when: The pool is hosted, or it is ephemeral, scoped to named repositories, and free of long-lived cloud keys.

## Ask 2

Make that runner ephemeral.

### Expected for ask 2

- Load `pipelines-runners` and follow that file through its own done-when.
- Step: Make that runner ephemeral. One job, then the machine is destroyed. Do not reuse a VM that keeps a workspace, a Docker layer with a secret, or a cloud credential. A registration token is short-lived and is not baked into the image.
- Check: The runner is destroyed after the job. The image has no cloud key and no kubeconfig.
- Done when: A public repository and untrusted fork builds do not land on it.
