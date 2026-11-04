---
name: pipelines-github-actions-authoring
description: "Use when you add or edit a GitHub Actions workflow. Pin every action to a reviewed commit SHA, keep permissions least privilege, and stop overlapping deploys with timeouts and concurrency."
license: MIT
---

# Author GitHub Actions workflows

Treat the workflow as production code. Pin it, narrow what the token can do, and stop a second deploy from starting while the first is still running.

## Use when

- You add or edit a workflow under `.github/workflows` in `example-org/example-repo`.
- A job caches dependencies, fans out with a matrix, or skips work with a path filter.
- Someone proposes a floating action tag, or Dependabot opens a pin bump.
- A deploy or an apply must not overlap another run on the same environment.

## Steps

1. Set `permissions: contents: read` on the workflow. Add a wider permission only on the job that needs it. A job `permissions` block replaces the workflow block for that job, so repeat `contents: read` there. Only the job that logs in to Azure or AWS sets `id-token: write`. Follow `principle-least-privilege` and `principle-no-static-credentials`.

2. Pin every `uses:` to the full commit SHA you reviewed, and put the release in a trailing comment. A tag such as `@v7` still moves. Call a workflow you own as `example-org/platform-workflows/.github/workflows/ci.yml@<commit-sha> # v1.2.0`. Follow `pipelines-reusable-templates`.

3. Let Dependabot open the pin bumps. Use the `github-actions` ecosystem. Review the action diff before you merge it. Follow `principle-everything-as-code` and `principle-change-safety`.

   ```yaml
   version: 2
   updates:
     - package-ecosystem: github-actions
       directory: /
       schedule:
         interval: weekly
   ```

4. Set `timeout-minutes` on every job. A job with no timeout holds a runner until the platform kills it. Follow `pipelines-github-actions-debugging` when a run dies with exit code 137.

5. Set `concurrency` so two deploys or applies cannot overlap. Those groups use `cancel-in-progress: false`. A pull-request test group may cancel the older run. Name the group with the workflow and the environment.

6. Filter `paths` so a docs-only change does not plan infrastructure. A path filter is not an approval. The deploy job still waits on the environment in `pipelines-environments-approvals`.

7. Treat event text as untrusted input. Do not put `${{ github.event.pull_request.title }}`, a branch name or an issue body straight into a `run:` script. Pass it through `env:` and quote the variable. Do not use `pull_request_target` or `workflow_run` to check out and run pull-request code with a write token or secrets.

8. Use a matrix for a small set of versions you name. Keep `fail-fast: false` so one red cell does not hide the others. Do not set `continue-on-error` to force a green workflow.

9. Cache only inputs you can rebuild. Key the cache on the lockfile. A hit must produce the same artefact as a miss. Follow `principle-idempotent-automation`. On a private repository, GitHub-hosted minutes are billed beyond the plan quota. Larger runners are always billed. Artefact storage and cache storage count. Say that on the pull request. Follow `principle-cost-awareness`.

10. Log in with federation in the one job that needs the cloud. Follow `pipelines-oidc-federation`. The test job below does not set `id-token: write`.

    ```yaml
    name: ci
    on:
      pull_request:
        paths:
          - "src/**"
          - ".github/workflows/ci.yml"
    permissions:
      contents: read
    concurrency:
      group: ci-${{ github.workflow }}-${{ github.ref }}
      cancel-in-progress: true
    jobs:
      test:
        runs-on: ubuntu-latest
        timeout-minutes: 15
        strategy:
          fail-fast: false
          matrix:
            node: ["22", "24"]
        steps:
          - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
            with:
              persist-credentials: false
          - uses: actions/setup-node@949feb2413d6458794dcd2491c4babbbce0c15c1 # v7.1.0
            with:
              node-version: ${{ matrix.node }}
          - uses: actions/cache@55cc8345863c7cc4c66a329aec7e433d2d1c52a9 # v6.1.0
            with:
              path: ~/.npm
              key: npm-${{ runner.os }}-${{ matrix.node }}-${{ hashFiles('package-lock.json') }}
          - run: npm ci
          - run: npm test
    ```

## Safety checks

- Workflow permissions stay `contents: read` except on the job that needs more.
- Every `uses:` line is a full SHA plus a version comment. Checkout sets `persist-credentials: false` unless a later step pushes.
- Every job sets `timeout-minutes`. Deploy and apply groups do not cancel in progress.
- No `run:` script expands event text directly, and no `pull_request_target` job runs pull-request code.
- The matrix lists named cells. Path filters do not replace a reviewer.
- The workflow stores no client secret, access key or personal access token.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Revert the workflow to the last green commit and run that SHA again. Follow `principle-rollback-first`. If a bad pin is already on the default branch, restore the previous SHA in a new pull request. Do not delete the workflow to hide a red check.

## Done when

- The diff shows pinned SHAs, top-level `contents: read`, a timeout on every job, and concurrency where runs must not overlap.
- Dependabot is set to the `github-actions` ecosystem, or the change record names who bumps pins.
- A pull request run completed, or the edit was stopped and the previous workflow is still the one that runs.
