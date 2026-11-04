# Review a Terraform plan

A pull request changes infrastructure. You want the plan read in full before anyone applies it.

## Ask this

```text
Review examples/jstack-review/terraform/plan.txt.
Subscription 00000000-0000-0000-0000-000000000000, resource group rg-example, region uksouth.
State key example-prod.tfstate. Environment production.
Pipeline example-org/example/.github/workflows/deploy.yml.
Load terraform-plan-review, principle-change-safety, and principle-rollback-first.
Do not apply. Do not edit the files.
```

For a real plan, point at the saved plan file instead of the fixture. Say the subscription or account, the state key, and the pipeline.

## Load

- `terraform-plan-review` reads the whole plan and lists destroys, replacements, grants, network edits, moves, imports, and provider bumps.
- `principle-change-safety` names the blast radius: subscription or account, region, resource group or VPC, state key, pipeline, and environment.
- `principle-rollback-first` requires the reverse change before a production apply.

## What good looks like

The review names each resource address that the plan destroys or replaces. It names any new role assignment. It says whether the plan file is the one that would be applied.

A destroy, a new Owner assignment, or an apply with no saved plan file is a stop. The agent writes that down and waits.

## Trial

Ask for the Plan section of `examples/jstack-review/prompts.md` only. The answer key stays closed until the review is written.
