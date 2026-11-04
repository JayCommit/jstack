---
name: pipelines-azure-devops-yaml
description: "Use when you write, change, or diagnose an Azure DevOps YAML pipeline. Read a failed run before you edit it, put checks on the resource, and deploy with workload identity federation."
license: MIT
---

# Azure DevOps YAML pipelines

Keep the pipeline in YAML and the approvals on the resource. A check that lives only inside a script is not a control.

## Use when

- A run failed or hung and you are about to edit the YAML.
- You add or edit `azure-pipelines.yml` for `example-org/example-repo`.
- You choose a Microsoft-hosted image or a self-hosted pool.
- A stage deploys to Azure or AWS, or it reads a variable group.
- You call a template from this repository or from another one.

## Steps

1. When a run has already failed or hung, open that run and read the step that exited non-zero before you edit the YAML. Follow `principle-observe-before-you-fix`. Record the run, the stage, the job and the commit. A rerun of the same revision is not the fix. GitHub Actions failures follow `pipelines-github-actions-debugging` instead of this file.

2. Declare `trigger` and `pr` for the branches this pipeline should build. In Azure Repos Git the `pr` key is ignored. Pull-request builds come from a build validation branch policy. A pull-request build is not a production deploy. Follow `principle-change-safety`.

3. Set `timeoutInMinutes` on every job. A hung step should fail inside that budget.

4. Use a Microsoft-hosted `vmImage` when the job only needs the public internet. Use a named self-hosted pool, such as a Managed DevOps Pool or a scale set pool, when the job must reach a private network. Do not send a production deploy to a pool that also builds untrusted forks. Parallel jobs beyond the free grant are billed, on either kind of pool. Follow `principle-cost-awareness`.

5. Keep secret values in a variable group linked to Key Vault, not in the YAML. Follow `azure-key-vault`. The group is a protected resource. Checks on it are configured outside this file. Follow `pipelines-environments-approvals`.

6. Log in with an Azure Resource Manager service connection that uses workload identity federation, or with the AWS federation path. Copy the issuer and the subject from that connection. Follow `pipelines-oidc-federation` and `principle-no-static-credentials`. Do not store a client secret or an access key on the connection.

7. Deploy from a deployment job in its own stage. The `environment` name is the resource that holds the checks. Those checks are not keys in this file. `azureSubscription` is the name of the federated service connection, not an id.

   ```yaml
   stages:
     - stage: production
       dependsOn: test
       variables:
         - group: vg-example-production
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
                   - task: AzureCLI@2
                     inputs:
                       azureSubscription: sc-example-production
                       scriptType: bash
                       scriptLocation: inlineScript
                       inlineScript: az group show --name rg-example
   ```

8. Insert shared steps or jobs with `template` and `parameters`. When the project requires a whole pipeline template, use `extends` and pin the repository to a tag. A branch ref moves. Follow `pipelines-reusable-templates`.

   ```yaml
   resources:
     repositories:
       - repository: platform
         type: git
         name: example-project/platform-templates
         ref: refs/tags/v1.2.0
   extends:
     template: templates/required.yml@platform
     parameters:
       environmentName: production
   ```

9. Give the plan connection a read role and the deploy connection a narrow deploy role. Follow `principle-least-privilege` and `azure-rbac-entra`. On AWS, follow `aws-iam-least-privilege`.

10. Promote the same build through stages. Do not rebuild the artefact in production. Follow `pipelines-artifacts-releases` when the stage ships an image.

## Safety checks

- `timeoutInMinutes` is set on every job.
- Each deploy is a `deployment` job that names an `environment`.
- Approvals, branch control and exclusive lock are on the resource, not in the steps.
- Variable groups pull secrets from Key Vault. The YAML holds none.
- The service connection is federated. It stores no static cloud key.
- A template from another repository uses `ref: refs/tags/v1.2.0`.
- The pool is Microsoft-hosted or a named self-hosted pool, and the change says which.
- A failed or hung run was read, and the failing step is named, before the YAML changed.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Keep the previous YAML until the new pipeline has deployed once to a non-production environment. Revert the file if the new pipeline mis-deploys. Follow `principle-rollback-first`. Do not delete the environment checks to force a run through.

## Done when

- A pull-request run uses the pinned template and the named pool.
- The production stage is a deployment job whose environment has the checks in `pipelines-environments-approvals`.
- No client secret or access key was added to the pipeline or the service connection.
- A failure names the failing step and the cause. The YAML changed only because that cause required it.
