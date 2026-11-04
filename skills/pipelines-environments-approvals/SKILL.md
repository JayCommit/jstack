---
name: pipelines-environments-approvals
description: "Use when a pipeline deploys to a shared environment. Require a reviewer on the GitHub environment or an Azure DevOps check, and bind the federated subject to that environment."
license: MIT
---

# Environments and approvals

Production waits for a second person. The wait is a setting on the environment, and the cloud trust names that same environment.

## Use when

- A job deploys, applies Terraform, or otherwise changes a shared environment.
- You add required reviewers, a wait timer, or a limit on which branches may deploy.
- An Azure DevOps stage should stop for approval, branch control or an exclusive lock.
- The cloud role must trust only the production environment subject. Follow `pipelines-oidc-federation`.

## Steps

1. Create one GitHub environment per stage you promote through, such as `development`, `test` and `production`. Follow `principle-change-safety`. Do not point every job at `production`.

2. On `production`, add required reviewers and turn on prevent self-review so the author cannot approve their own run. Add a wait timer when the release needs a pause before the job starts. Limit deployment branches and tags to the branch or tag you actually ship. Turn off the setting that lets administrators bypass the rules, unless the change record says who may bypass and why. Keep secrets the deploy needs as environment secrets on `production`, not repository secrets. On a private repository, some protection rules are not available on every plan. Check your plan. Do not claim a rule is active when the UI cannot store it.

3. Set `environment` on the deploy job. That run's OIDC subject ends in `:environment:production`, not in a ref. Copy that subject into the federated credential. Follow `pipelines-oidc-federation`. Put `timeout-minutes` on the job. Set `concurrency` with `cancel-in-progress: false` so a second production deploy waits.

   ```yaml
   permissions:
     contents: read
   concurrency:
     group: deploy-production
     cancel-in-progress: false
   jobs:
     deploy:
       runs-on: ubuntu-latest
       timeout-minutes: 30
       environment: production
       permissions:
         id-token: write
         contents: read
       steps:
         - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
   ```

4. In Azure DevOps, use a deployment job with `environment`. Follow `pipelines-azure-devops-yaml`. Configure Approvals and checks on the resource, not in the YAML. The same checks can sit on an environment, a service connection, an agent pool, a variable group, a secure file or a repository.

5. Use the checks that match the risk. An approval names a second person. Branch control limits the branch that may deploy. Business hours stops a production run outside the window you set. A required template forces `extends` from `pipelines-reusable-templates`. An exclusive lock stops two deploys of that environment at once.

   ```yaml
   jobs:
     - deployment: deploy_example
       timeoutInMinutes: 30
       environment: production
       pool:
         vmImage: ubuntu-latest
       strategy:
         runOnce:
           deploy:
             steps:
               - checkout: self
   ```

6. Keep secret material in a variable group linked to Key Vault. Follow `azure-key-vault`. Protect the group with a check. Do not print the approved values in the step log.

7. Write the blast radius on the change: the environment name, the subscription or account `123456789012`, and the region `eu-west-2` or `uksouth`. A production approval is still one change. Follow `principle-change-safety`.

## Safety checks

- Production has a required reviewer who is not the author. Prevent self-review is on where the plan allows it.
- Deployment branches and tags, or an Azure DevOps branch control check, name the ref that may deploy.
- The OIDC subject is the environment subject for any job that sets `environment`.
- Deploy concurrency does not cancel a run that is already in progress.
- Azure DevOps checks are on the resource. They are not a script step.
- You checked the plan before relying on a protection rule the UI may hide.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Write the service rollback before the first approved deploy. Follow `principle-rollback-first`. If a bad change is approved, stop and run that rollback. Removing reviewers or checks is not a rollback. Restore the previous protection settings if an edit weakened them.

## Done when

- The production job does not start until a second person approves it.
- The federated subject matches that environment and no wider ref.
- A fork, or a branch outside the deployment rule, cannot use the production environment.
- The approver, the wait and the branch rule are recorded on the change, or the plan cannot store them and the change says so.
