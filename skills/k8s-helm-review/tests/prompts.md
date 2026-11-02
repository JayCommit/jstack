# Prompts for k8s-helm-review

Example asks for `k8s-helm-review`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I add a chart, change a template, or bump a chart version.

### Expected for ask 1

- Load `k8s-helm-review` and follow that file through its own done-when.
- Step: Read the release before you upgrade it. Run `helm history example -n example` and `helm get values example -n example --all`. Record the chart version, the app version and the revision you would roll back to. Follow `principle-observe-before-you-fix`. A stuck pending release is a failed hook or a timeout. Read that before you run another upgrade.
- Check: `values.schema.json` exists, and `helm lint` fails on a bad values file.
- Done when: The chart lints, the schema rejects a bad values file, and the diff matches the request.

## Ask 2

Add `values.schema.json`.

### Expected for ask 2

- Load `k8s-helm-review` and follow that file through its own done-when.
- Step: Add `values.schema.json`. A value the chart cannot default is required in the schema. `helm lint` must fail when that value is missing or the wrong type. A comment in `values.yaml` is not a schema.
- Check: Dependencies are pinned and `Chart.lock` is in git.
- Done when: The release is `deployed`, and the pods are ready.
