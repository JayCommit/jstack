# Prompts for principle-everything-as-code

Example asks for `principle-everything-as-code`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

Someone changes a resource in the Azure portal or the AWS console.

### Expected for ask 1

- Load `principle-everything-as-code` and follow that file through its own done-when.
- Rule: Make the change in Terraform, or in the pipeline that applies it. If the portal or console was used, open a follow-up the same day to codify that edit.
- Red flag: Production was fixed in the portal and the code was left stale.
- Done when: The desired change is in reviewed code.

## Ask 2

Bring an existing resource into state with an `import` block, then plan and apply through review.

### Expected for ask 2

- Load `principle-everything-as-code` and follow that file through its own done-when.
- Rule: Bring an existing resource into state with an `import` block, then plan and apply through review. A one-off `terraform import` leaves no record in git.
- Red flag: Resources in the subscription or account belong to no state and no owner.
- Done when: An imported resource plans with no unexpected diff.
