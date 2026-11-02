# Prompts for pipelines-github-actions-authoring

Example asks for `pipelines-github-actions-authoring`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I add or edit a workflow under `.github/workflows` in `example-org/example-repo`.

### Expected for ask 1

- Load `pipelines-github-actions-authoring` and follow that file through its own done-when.
- Step: Set `permissions: contents: read` on the workflow. Add a wider permission only on the job that needs it. A job `permissions` block replaces the workflow block for that job, so repeat `contents: read` there. Only the job that logs in to Azure or AWS sets `id-token: write`. Follow `principle-least-privilege` and `principle-no-static-credentials`.
- Check: Workflow permissions stay `contents: read` except on the job that needs more.
- Done when: The diff shows pinned SHAs, top-level `contents: read`, a timeout on every job, and concurrency where runs must not overlap.

## Ask 2

Pin every `uses:` to the full commit SHA you reviewed, and put the release in a trailing comment.

### Expected for ask 2

- Load `pipelines-github-actions-authoring` and follow that file through its own done-when.
- Step: Pin every `uses:` to the full commit SHA you reviewed, and put the release in a trailing comment. A tag such as `@v7` still moves. Call a workflow you own as `example-org/platform-workflows/.github/workflows/ci.yml@<commit-sha> # v1.2.0`. Follow `pipelines-reusable-templates`.
- Check: Every `uses:` line is a full SHA plus a version comment. Checkout sets `persist-credentials: false` unless a later step pushes.
- Done when: Dependabot is set to the `github-actions` ecosystem, or the change record names who bumps pins.
