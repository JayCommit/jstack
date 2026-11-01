---
name: principle-observe-before-you-fix
description: "Apply before changing Azure, AWS, Terraform or a pipeline to fix a failure or an alert. Read the actual logs, metrics and error text first, then fix the root cause those records show."
license: MIT
---

# Observe before you fix

Read the logs, metrics and error text before you change Azure, AWS, Terraform or a pipeline. Fix the cause those records show.

## Use when

- A plan, apply, deployment or health check has failed.
- An alert fires, or a service looks unhealthy.
- You are about to rerun, restart, scale or force-unlock.
- A fix is proposed and nobody has quoted the error.

## Rules

- Record the exit code and the first Azure, AWS or provider error. Terraform names the resource address. Start from that line.
- On Azure, check Activity Log for control-plane changes, the resource metrics, and the Log Analytics workspace that holds the diagnostic settings. Restart an App Service or an AKS node only after those show why.
- On AWS, use CloudTrail for who changed the resource, and CloudWatch metrics plus the service log group for what it did. An alarm without the matching log line is not a diagnosis yet.
- Open the failed step before you rerun it. Read the GitHub Actions job log or the Azure DevOps task log before you turn on debug logging.
- If Terraform reports a state lock, identify the holder and the running pipeline. Leave the lock in place while that run is alive.
- Change the cause. A longer timeout, an extra retry or a larger SKU leaves a bad probe, a quota or a wrong plan in place. Review the eventual edit with `principle-change-safety`.
- After the fix, run the same query or open the same metric. The symptom should be gone. A single green rerun is weak evidence on its own.

## Red flags

- The job was rerun and nobody kept the error text.
- The first action is a restart, a scale-out or a force-unlock.
- The failure is called flaky and no error code is written down.
- A fix merges with no reference to the log line or error code it addresses.
- Debug logging is turned on before the original error is read.

## Done when

- The error, metric or log line is recorded on the change.
- The edit addresses that cause.
- The same check is clean after the fix.
