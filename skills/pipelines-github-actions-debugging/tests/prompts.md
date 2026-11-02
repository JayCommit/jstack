# Prompts for pipelines-github-actions-debugging

Example asks for `pipelines-github-actions-debugging`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

A job in `example-org/example-repo` failed, was cancelled, or never left the queue.

### Expected for ask 1

- Load `pipelines-github-actions-debugging` and follow that file through its own done-when.
- Step: Open the failed job and read the step that exited non-zero. Follow `principle-observe-before-you-fix`. Record the run id, the job name, the commit SHA and the `runs-on` label before you change the workflow. An Azure DevOps run follows `pipelines-azure-devops-yaml` instead of this file.
- Check: You read the failed log, or `gh run view --log-failed`, before editing the workflow.
- Done when: The failing step, the run and the cause are written on the change.

## Ask 2

Pull the same evidence from the CLI.

### Expected for ask 2

- Load `pipelines-github-actions-debugging` and follow that file through its own done-when.
- Step: Pull the same evidence from the CLI. Watch a run that is still going. Re-run failed jobs only after you know why they failed.
- Check: Debug flags are on only for the re-run you are inspecting, then off again.
- Done when: The new run is green because the cause was fixed, or the edit was stopped and the previous workflow is restored.
