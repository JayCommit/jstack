# Triage Terraform drift

A scheduled plan shows changes nobody shipped in this commit. The job that found them must not apply them.

## Ask this

```text
The scheduled plan for state key example-prod.tfstate exited 2.
Subscription 00000000-0000-0000-0000-000000000000, resource group rg-example.
Nobody shipped a Terraform change in this commit.
Load terraform-drift, principle-observe-before-you-fix, and principle-everything-as-code.
Read Activity Log or CloudTrail before editing code. Do not apply.
```

## Load

- `terraform-drift` treats exit 2 as a review. Exit 1 is a failed plan, not drift.
- `principle-observe-before-you-fix` reads Activity Log or CloudTrail and names the caller before the code changes.
- `principle-everything-as-code` is the path when the live change was deliberate and should remain.

## What good looks like

The note names the resource address, the caller, and one path: update the code, import, or revert the live change. Those paths stay in separate changes.

The agent does not apply the drift plan to make it empty, and does not add `ignore_changes` on a security group, a route, or a role assignment. A later plan exits 0 because the chosen path landed, not because a surprise diff was applied.
