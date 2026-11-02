---
name: pipelines-reusable-templates
description: "Use when you share a GitHub Actions workflow, a composite action or an Azure DevOps template. Pin the caller to a reviewed ref and pass named secrets instead of inheriting every secret."
license: MIT
---

# Reusable workflows and templates

Share a job or a step by pinning a ref you reviewed. Callers pass the inputs they need. They do not hand over every secret.

## Use when

- The same deploy, lint or login steps are copied across repositories.
- You add a reusable workflow, a composite action, or an Azure DevOps template.
- A caller uses a branch name, a floating tag, or `secrets: inherit`.
- A required pipeline template should be the only way to reach production.

## Steps

1. Pick one shape. A reusable workflow is a whole job, with `on: workflow_call`. A composite action is steps inside the caller's job. An Azure DevOps template is steps, jobs or stages, and `extends` when the template must be the whole pipeline. Follow `pipelines-github-actions-authoring` or `pipelines-azure-devops-yaml`.

2. Declare inputs and the secrets this workflow uses. Do not set `secrets: inherit`. A callee that receives every secret can use one the job does not need. Each called job sets `timeout-minutes`.

   ```yaml
   on:
     workflow_call:
       inputs:
         environment:
           required: true
           type: string
       secrets:
         EXAMPLE_CONFIG:
           required: true
   permissions:
     contents: read
   jobs:
     deploy:
       runs-on: ubuntu-latest
       timeout-minutes: 20
       environment: ${{ inputs.environment }}
       permissions:
         id-token: write
         contents: read
       steps:
         - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
   ```

3. Pin the caller to the reviewed commit. Pass each secret by name. The called workflow can request an OIDC token only when the caller grants `id-token: write`. Repeat `contents: read` on that job. A job permissions block replaces the workflow set. Follow `pipelines-oidc-federation`.

   ```yaml
   jobs:
     deploy:
       permissions:
         id-token: write
         contents: read
       uses: example-org/platform-workflows/.github/workflows/terraform.yml@<commit-sha> # v1.2.0
       with:
         environment: production
       secrets:
         EXAMPLE_CONFIG: ${{ secrets.EXAMPLE_CONFIG }}
   ```

4. Keep nesting shallow. GitHub allows ten levels, counting the top-level caller, and a nested workflow can keep or reduce permissions but not raise them. Secrets reach only the workflow they are passed to, so pass them again at each level. Do not add another layer to hide a step.

5. Use a composite action when the caller must keep the job. The action has no permissions of its own. It runs with the token and the permissions of the calling job. Pin it the same way as any other action. Every `run` step needs `shell`. Pass inputs through `env`, not straight into the script.

   ```yaml
   name: example-plan-summary
   description: Write a short Terraform plan summary.
   inputs:
     working-directory:
       required: true
   runs:
     using: composite
     steps:
       - shell: bash
         env:
           WORKDIR: ${{ inputs.working-directory }}
         run: terraform -chdir="$WORKDIR" show -no-color tfplan | grep -E '^(Plan:|No changes)'
   ```

   Callers use `example-org/platform-actions/plan-summary@<commit-sha> # v1.2.0`.

6. In Azure DevOps, pin the template repository to a tag. Call it with `template` and `parameters`, or with `extends` when a required-template check demands that file. `extends` replaces the pipeline body. Do not point `ref` at a branch. A tag can be moved, so limit who can create, delete or force-push tags in the template repository. Follow `pipelines-environments-approvals`.

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

7. Change the template in its own pull request, and let callers stay on the previous tag until they bump the pin. Follow `principle-change-safety` and `principle-everything-as-code`. A template edit is not also an application release.

## Safety checks

- Callers pin a full commit SHA or `refs/tags/v1.2.0`, not a branch.
- Secrets are passed by name. `secrets: inherit` is absent.
- The caller grants `id-token: write` only on the job that needs a cloud token.
- Called jobs set `timeout-minutes`. The called workflow does not widen permissions above the caller.
- Nesting stays shallow, within GitHub's limit of ten levels, and each level passes only the secrets it names.
- A required Azure DevOps template is pulled in with `extends` from a tag.

## Rollback

Point callers back at the previous SHA or tag. Follow `principle-rollback-first`. Leave the new template in place until those callers have moved, then fix it in a later change. Do not retarget `ref` to a branch to get unreviewed fixes into production.

## Done when

- Each caller names the ref it runs, and that ref was reviewed.
- Named secrets and inputs are the only values passed in.
- A production run uses the pinned template or workflow, and the previous ref still deploys if you put it back.
