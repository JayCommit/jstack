# A failing pipeline

A run failed or hung. Read the failed step before anyone edits the workflow or clicks re-run.

## Ask this

```text
GitHub Actions run 00000000000 in example-org/example failed on job deploy, commit 0000000.
Here is the log of the failing step, and the run inputs.
Load pipelines-github-actions-debugging.
Name the cause before you edit. Do not re-run this SHA and call that the fix.
```

An Azure DevOps failure uses the same shape and loads `pipelines-azure-devops-yaml` instead.

## Load

- `pipelines-github-actions-debugging` for a GitHub Actions run. Record the run id, the job, the commit, and the `runs-on` label.
- `pipelines-azure-devops-yaml` for an Azure DevOps run. Read the failing step before the YAML changes.
- `principle-observe-before-you-fix` sits under both. The log comes first.

## What good looks like

The note names the failing step and the cause. A queued job is checked for the runner label, an online runner, concurrency, and runner-group access before it is called a test failure.

A second run of the same commit is not the fix. Debug logging is turned off after the one re-run that needed it. No static cloud key is added while chasing the failure. The agent stops before it merges a workflow edit.
