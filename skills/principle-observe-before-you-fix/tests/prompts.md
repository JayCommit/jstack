# Prompts for principle-observe-before-you-fix

Example asks for `principle-observe-before-you-fix`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

A plan, apply, deployment or health check has failed.

### Expected for ask 1

- Load `principle-observe-before-you-fix` and follow that file through its own done-when.
- Rule: Record the exit code and the first Azure, AWS or provider error. Terraform names the resource address. Start from that line.
- Red flag: The job was rerun and nobody kept the error text.
- Done when: The error, metric or log line is recorded on the change.

## Ask 2

On Azure, check Activity Log for control-plane changes, the resource metrics, and the Log Analytics workspace that holds the diagnostic settings.

### Expected for ask 2

- Load `principle-observe-before-you-fix` and follow that file through its own done-when.
- Rule: On Azure, check Activity Log for control-plane changes, the resource metrics, and the Log Analytics workspace that holds the diagnostic settings. Restart an App Service or an AKS node only after those show why.
- Red flag: The first action is a restart, a scale-out or a force-unlock.
- Done when: The edit addresses that cause.
