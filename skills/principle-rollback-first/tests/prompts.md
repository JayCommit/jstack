# Prompts for principle-rollback-first

Example asks for `principle-rollback-first`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

The change will be applied to production.

### Expected for ask 1

- Load `principle-rollback-first` and follow that file through its own done-when.
- Rule: Record the rollback beside the change: the previous Terraform configuration, the previous container digest or package, and the previous pipeline file.
- Red flag: The change record says rollback is possible and lists no steps.
- Done when: Rollback steps are written on the change and name the first command.

## Ask 2

Rehearse it on dev or test.

### Expected for ask 2

- Load `principle-rollback-first` and follow that file through its own done-when.
- Rule: Rehearse it on dev or test. A reverse Terraform plan must apply cleanly there. For an app, put the previous revision back and confirm the health check.
- Red flag: A production Terraform apply has no previous state snapshot and no reverse plan.
- Done when: Those steps have succeeded on a non-production environment, or the production change has been stopped.
