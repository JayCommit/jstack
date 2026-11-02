# Prompts for pipelines-reusable-templates

Example asks for `pipelines-reusable-templates`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

The same deploy, lint or login steps are copied across repositories.

### Expected for ask 1

- Load `pipelines-reusable-templates` and follow that file through its own done-when.
- Step: Pick one shape. A reusable workflow is a whole job, with `on: workflow_call`. A composite action is steps inside the caller's job. An Azure DevOps template is steps, jobs or stages, and `extends` when the template must be the whole pipeline. Follow `pipelines-github-actions-authoring` or `pipelines-azure-devops-yaml`.
- Check: Callers pin a full commit SHA or `refs/tags/v1.2.0`, not a branch.
- Done when: Each caller names the ref it runs, and that ref was reviewed.

## Ask 2

Declare inputs and the secrets this workflow uses.

### Expected for ask 2

- Load `pipelines-reusable-templates` and follow that file through its own done-when.
- Step: Declare inputs and the secrets this workflow uses. Do not set `secrets: inherit`. A callee that receives every secret can use one the job does not need. Each called job sets `timeout-minutes`.
- Check: Secrets are passed by name. `secrets: inherit` is absent.
- Done when: Named secrets and inputs are the only values passed in.
