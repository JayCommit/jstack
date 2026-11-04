---
name: pipelines-github-actions-debugging
description: "Use when a GitHub Actions run fails, hangs or stays queued. Read the failed logs, re-run with debug logging, and fix the runner or the step instead of hiding the failure with a retry."
license: MIT
---

# Debug GitHub Actions runs

Read the failed step before you edit the workflow. A retry that goes green without a cause is not a fix.

## Use when

- A job in `example-org/example-repo` failed, was cancelled, or never left the queue.
- The log says the runner shut down, lost communication, or exited 137.
- Someone wants a retry around a step that fails on some runs.
- A pin from `pipelines-github-actions-authoring` behaved differently from the last green run.

## Steps

1. Open the failed job and read the step that exited non-zero. Follow `principle-observe-before-you-fix`. Record the run id, the job name, the commit SHA and the `runs-on` label before you change the workflow. An Azure DevOps run follows `pipelines-azure-devops-yaml` instead of this file.

2. Pull the same evidence from the CLI. Watch a run that is still going. Re-run failed jobs only after you know why they failed.

   ```bash
   gh run view <run-id> --repo example-org/example-repo --log-failed
   gh run watch <run-id> --repo example-org/example-repo
   gh run rerun <run-id> --repo example-org/example-repo --failed
   ```

3. Turn on debug logging for one re-run. Set the repository secret or variable `ACTIONS_STEP_DEBUG` to true, and set `ACTIONS_RUNNER_DEBUG` to true when you need runner diagnostics. You can instead tick Enable debug logging on the re-run. Turn both off when you have the log. Debug logs can echo more of the environment. Do not print a cloud token. Follow `principle-no-static-credentials`.

4. Treat exit code 137, the line "The runner has received a shutdown signal", and lost communication as the runner dying. The usual cause is that the job ran out of memory or the runner went away. On a self-hosted runner, read the host's kernel log for the out-of-memory killer and check the memory the runner was given. Move that job to a larger runner, or cut its parallelism, only after the log shows a memory symptom. On a private repository, GitHub-hosted minutes are billed beyond the plan quota. Larger runners are always billed. Follow `principle-cost-awareness`.

5. A queued job is not a failing test. Check, in order: the `runs-on` label matches a runner that exists, a self-hosted runner with that label is online, a concurrency group is still holding the slot, and the org runner group is granted to this repository. `cancel-in-progress: false` waits. It does not drop the queued run. Follow `pipelines-github-actions-authoring` for how that group was set.

6. Do not add a retry to hide a flaky step. Fix the step, or quarantine it with a tracked reason and an owner. A retry that masks a red deploy ships the next SHA on luck. Follow `principle-change-safety`.

7. If the failure is an action pin, compare the SHA on the `uses:` line with the commit you reviewed. Do not float the ref to a tag to see whether "latest" passes. Restore the previous pin if the new SHA is the cause. Follow `principle-rollback-first`.

8. If the failure is a cloud login, confirm that job sets `id-token: write` and `contents: read`, and that the subject matches the environment. Follow `pipelines-oidc-federation`. A missing permission is a configuration bug. It is not a reason to paste a key into the log or the workflow.

9. Leave `timeout-minutes` in place while you debug. Raising it without a measured reason hides a hang. Write the new value and the reason on the pull request.

## Safety checks

- You read the failed log, or `gh run view --log-failed`, before editing the workflow.
- Debug flags are on only for the re-run you are inspecting, then off again.
- A queued job was checked for label, an online runner, concurrency and runner-group access.
- Exit 137 or a shutdown signal was treated as memory or a lost runner.
- No retry was added to make a flaky step look green.
- No static cloud credential was added while chasing the failure.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Put the workflow back to the last green commit if a debug edit made later runs worse. Follow `principle-rollback-first`. Remove the temporary debug secret or variable when the investigation ends. Do not leave `ACTIONS_STEP_DEBUG` set for every later run.

## Done when

- The failing step, the run and the cause are written on the change.
- The new run is green because the cause was fixed, or the edit was stopped and the previous workflow is restored.
- Debug logging is off, and the job still has a timeout.
