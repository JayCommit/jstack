# Prompts for principle-least-privilege

Example asks for `principle-least-privilege`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I add or widen Azure RBAC, AWS IAM or a permission boundary.

### Expected for ask 1

- Load `principle-least-privilege` and follow that file through its own done-when.
- Rule: Assign Azure roles at the resource or resource group. Prefer a narrow built-in role or a custom role. Keep Owner and User Access Administrator off pipeline identities.
- Red flag: A workflow sets `permissions: write-all`, or a new workflow sets no `permissions` block.
- Done when: The actions and the scope of each identity are listed and match the job.

## Ask 2

Write the AWS policy for the API calls this pipeline makes.

### Expected for ask 2

- Load `principle-least-privilege` and follow that file through its own done-when.
- Rule: Write the AWS policy for the API calls this pipeline makes. Leave out `AdministratorAccess` and an `Action` of `*`. Put a permission boundary on roles this pipeline can create.
- Red flag: A service connection is scoped to a management group for a single resource group.
- Done when: The workflow has an explicit `permissions` block.
