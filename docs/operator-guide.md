# Operator guide

This is the guide for the person asking an agent to do the work. Authors who are adding a skill follow [Writing skills](writing-skills.md).

Name the subscription or account, the repository, and the environment in the request. When more than one skill could fit, ask the agent to load `jay-mode` and take the first matching row. The agent prepares the diff and stops. You approve. The pipeline applies.

The secure stack to copy is `examples/jstack-sample`. The review target is `examples/jstack-review`. Leave `examples/jstack-review/expected.md` closed until the review is written down.

## A Terraform plan

Point at the plan file. Ask for a review and say not to apply. The skill is `terraform-plan-review`.

You want every destroy, replacement, grant, network edit, move, import, and provider bump named, with the resource address. You also want the subscription or account, the state key, and the pipeline.

To trial it, ask the agent to follow `examples/jstack-review/prompts.md` and to do only the Plan section.

## A failing pipeline

Paste the log of the failing step and the run inputs. Ask for the cause before any edit.

A GitHub Actions failure loads `pipelines-github-actions-debugging`. An Azure DevOps failure loads `pipelines-azure-devops-yaml`. A second run of the same commit is not the fix.

## A workflow change

Point at the workflow file. Ask for a review and say not to change the file in that pass.

A GitHub Actions workflow loads `pipelines-github-actions-authoring`. An Azure DevOps pipeline loads `pipelines-azure-devops-yaml`. A job that calls Azure or AWS also loads `pipelines-oidc-federation`.

To trial it, ask the agent to follow `examples/jstack-review/prompts.md` and to do only the Workflow section.

## A ServiceNow change

Ask the agent to act as you, on the instance you name. The skill is `servicenow-changes`. It fills the change and stops before approval. It does not move the change to implement.

Production also loads `principle-change-safety` and `principle-rollback-first`. An outage that is paging stays on `ops-incident-response`. The ticket comes after the mitigation.

## After a trial

Run the same ask in Cursor, in GitHub Copilot, and in Claude Code. Write down each miss beside the skill that should have caught it.

When the same miss shows up in more than one harness, edit the skill that owns the fact, or add a warning in `scripts/lint-skills`. Do not add a skill to hold one repeated sentence. Record the trial on issue #1. This guide does not cut the `v0.1.0` tag.
