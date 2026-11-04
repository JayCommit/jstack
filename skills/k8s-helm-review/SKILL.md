---
name: k8s-helm-review
description: "Use when you add or upgrade a Helm chart. Require a values schema, read the rendered manifests, run helm diff, and keep a tested rollback to the previous release."
license: MIT
---

# Helm chart review

Review the rendered manifests, not the values file alone. Upgrade one release, and keep the previous revision.

## Use when

- You add a chart, change a template, or bump a chart version.
- You upgrade a release in a cluster.
- A values file is about to contain a secret, or a template uses `tpl` or `lookup`.
- A release is stuck `pending-upgrade` or `pending-install`.

## Steps

1. Read the release before you upgrade it. Run `helm history example -n example` and `helm get values example -n example --all`. Record the chart version, the app version and the revision you would roll back to. Follow `principle-observe-before-you-fix`. A stuck pending release is a failed hook or a timeout. Read that before you run another upgrade.

2. Add `values.schema.json`. A value the chart cannot default is required in the schema. `helm lint` must fail when that value is missing or the wrong type. A comment in `values.yaml` is not a schema.

3. Pin dependencies in `Chart.yaml` and commit `Chart.lock`. A dependency bump is its own change. Replace the repository below with the chart host you already use.

   ```yaml
   apiVersion: v2
   name: example
   version: 0.4.2
   appVersion: "1.8.0"
   dependencies:
     - name: example-lib
       version: 1.3.0
       repository: https://example.com/charts
   ```

4. Render, then diff. Run `helm template example ./chart -n example -f values.yaml` and read the Deployment, the hooks and the CRDs. Run `helm diff upgrade example ./chart -n example -f values.yaml` with the helm-diff plugin version you pinned. If the plugin is not installed, diff `helm template` output against `helm get manifest example -n example`. Review that output with `k8s-manifest-review`.

5. Keep templates predictable. Use `required` for a value with no safe default. Quote strings that YAML can read as a bool or a number. Keep the release name short enough that a resource name stays within 63 characters. Do not run `tpl` on a value a tenant sets. Do not use `lookup`. A `lookup` renders differently in each cluster, so the promotion is not the same chart.

6. Keep secrets out of `values.yaml` and out of git. The release reads a secret the cluster syncs. Follow `gitops-argocd-flux`, `azure-key-vault`, or `aws-secrets-ssm`.

7. Treat CRDs as their own change. Helm installs files in `crds/` and does not upgrade them on a later release. Do not hide a CRD change inside an app values bump.

8. Hooks must be safe to run twice. Set a weight and a delete policy. A hook that fails leaves the release pending. Do not put a one-way migration in a hook. Follow `principle-idempotent-automation`. A hook that changes data needs a rehearsed rollback. Follow `principle-rollback-first`.

9. Upgrade one release with a timeout and a wait. `--atomic` rolls back if the wait fails, and it needs the previous revision in history. Keep at least five revisions. Do not make `--force` the default.

   ```text
   helm upgrade example ./chart --namespace example --install --history-max 5 --wait --timeout 5m --atomic -f values.yaml
   ```

10. Rehearse that upgrade on a non-production namespace. The deploy job is federated and can change this namespace only. Follow `azure-aks` or `aws-eks` for cluster identity, and `pipelines-oidc-federation` when the job logs in to the cloud. Do not commit a kubeconfig. If GitOps owns the release, ship the chart through git. Follow `gitops-argocd-flux`. A second helm upgrade will fight the controller.

11. Promote a chart version. Production does not track a moving ref. One chart change. Name the cluster, the namespace and the release. Follow `principle-change-safety`.

## Safety checks

- `values.schema.json` exists, and `helm lint` fails on a bad values file.
- Dependencies are pinned and `Chart.lock` is in git.
- You read the rendered manifests and a diff against the live release.
- Templates do not `tpl` tenant input and do not `lookup` the cluster.
- No secret value is in values or in the chart.
- CRD changes are split out of the app upgrade.
- The upgrade uses `--wait` and `--atomic`, and history still holds the previous revision.
- The identity that runs Helm cannot administer the cluster.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Roll back to the revision you recorded. Follow `principle-rollback-first`.

```text
helm rollback example 4 --namespace example --wait --timeout 5m
```

Replace `4` with the revision from `helm history`. Rehearse it on a non-production release before production depends on `--atomic`. If GitOps owns the release, revert the git change. The next sync will undo a live `helm rollback`. A CRD is not rolled back by `helm rollback`. Restore the previous CRD only when the old revision still needs it, as its own change.

## Done when

- The chart lints, the schema rejects a bad values file, and the diff matches the request.
- The release is `deployed`, and the pods are ready.
- History contains the previous revision, and a rollback has been rehearsed off production.
- The same chart version is what you promote.
