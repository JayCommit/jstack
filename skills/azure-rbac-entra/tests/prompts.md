# Prompts for azure-rbac-entra

Example asks for `azure-rbac-entra`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I add or widen a role assignment for a person, a group, a workload or a pipeline.

### Expected for ask 1

- Load `azure-rbac-entra` and follow that file through its own done-when.
- Step: List who needs access, which API calls they make, and which resource they touch. Include data actions. Run `az role assignment list --scope /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/rg-example --include-inherited --output table` before you add anything.
- Check: The actions and the scope match the job. No wildcard write.
- Done when: Each identity has one role, one scope and a named job.

## Ask 2

Assign at the resource or the resource group.

### Expected for ask 2

- Load `azure-rbac-entra` and follow that file through its own done-when.
- Step: Assign at the resource or the resource group. Use a subscription or management group only when the job owns that whole scope. Follow `principle-least-privilege`.
- Check: People have an eligible PIM assignment with an end date, not standing Owner.
- Done when: Human access expires through PIM. Workload and pipeline access is federated.
