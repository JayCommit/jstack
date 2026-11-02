# Prompts for principle-change-safety

Example asks for `principle-change-safety`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I are about to plan or apply Terraform against Azure or AWS.

### Expected for ask 1

- Load `principle-change-safety` and follow that file through its own done-when.
- Rule: Read the whole `terraform plan` or pipeline diff before you approve it. List every destroy, replace, IAM or RBAC grant, and network change.
- Red flag: An apply runs without a saved plan, or from a branch nobody reviewed.
- Done when: The reviewed plan or diff matches the request and nothing else.

## Ask 2

`terraform plan -detailed-exitcode` exits 0 when nothing changes, 2 when the plan contains changes, and 1 when the plan fails.

### Expected for ask 2

- Load `principle-change-safety` and follow that file through its own done-when.
- Rule: `terraform plan -detailed-exitcode` exits 0 when nothing changes, 2 when the plan contains changes, and 1 when the plan fails. Review exit 2. Fix exit 1 before you continue.
- Red flag: The plan destroys or replaces resources and the pull request does not say so.
- Done when: The blast radius is written on the change.
