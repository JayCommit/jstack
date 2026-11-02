---
name: gitops-argocd-flux
description: "Use when you deliver workloads with Argo CD or Flux. Promote a digest through overlays, keep production sync from deleting on the first apply, and store secrets with SOPS or External Secrets."
license: MIT
---

# Argo CD and Flux

Git is the source the cluster converges to. Promote one digest through environments. One controller owns a set of apps.

## Use when

- You add Argo CD or Flux, or you add an app to either.
- You promote a workload from dev to test to production.
- A sync would prune, self-heal, or track a moving branch in production.
- A Kubernetes Secret with real data is about to be committed.

## Steps

1. Read what the cluster is already running. For Argo CD, run `argocd app list` and `argocd app get app-example`. For Flux, run `flux get kustomizations -A`. Record the revision, whether prune is on, and whether the app is healthy. Follow `principle-observe-before-you-fix`. Do not install the other controller over apps this one already reconciles.

2. Pick one controller per set of apps. Argo CD and Flux reconciling the same path will fight. A migration from one to the other is its own change, after the new controller is proven on a non-production cluster.

3. Lay environments out as overlays, for example `overlays/dev`, `overlays/test` and `overlays/prod`. Each overlay pins the image digest. Follow `pipelines-artifacts-releases`. Promote by copying that digest into the next overlay in a pull request. Sync the lower environment and read its health before you open the next promotion. Follow `principle-change-safety`.

4. Production tracks a tag or a commit, not a branch head. A branch is allowed only when the only way it moves is a reviewed merge. An ApplicationSet or an image-update automation may write the dev overlay. It does not push to production, and it does not track pull requests from forks.

5. For Argo CD, put the app in a project that names the source repo and the destination namespace. The root app, or the app-of-apps, creates Application objects. It does not also contain the workload manifests. The first sync is manual and does not prune. Automated sync, self-heal and prune come later, after a non-production rehearsal has shown what they delete. Self-heal reverts a live edit. Codify the edit. Follow `principle-everything-as-code`.

   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: app-example
     namespace: argocd
   spec:
     project: example
     source:
       repoURL: https://example.com/example-org/example-repo
       targetRevision: v1.8.0
       path: overlays/prod
     destination:
       server: https://kubernetes.default.svc
       namespace: example
     syncPolicy:
       syncOptions:
         - CreateNamespace=true
   ```

6. For Flux, point a Kustomization at the overlay. Leave `prune` false until you have read a diff that would delete resources. Add a health check so a bad rollout shows as not ready. Set an interval you can afford. Hundreds of one-minute reconciles are a load and a cost. Follow `principle-cost-awareness`.

   ```yaml
   apiVersion: kustomize.toolkit.fluxcd.io/v1
   kind: Kustomization
   metadata:
     name: app-example
     namespace: flux-system
   spec:
     interval: 10m
     prune: false
     sourceRef:
       kind: GitRepository
       name: example
     path: ./overlays/prod
     healthChecks:
       - apiVersion: apps/v1
         kind: Deployment
         name: app-example
         namespace: example
   ```

7. A rename in git is a delete and a create when prune is on. Read that diff. Add `ignoreDifferences` only for a field a controller writes, such as a replica count an autoscaler owns. Do not ignore the image.

8. Give the controller a key for this repo only. Use a GitHub App or a deploy key. Do not put a personal access token or a password in the cluster or in git. The cluster credential is a role in the destination namespace, not a cluster-admin kubeconfig in the repo. On AKS use workload identity. Follow `azure-aks`. On EKS use Pod Identity. Follow `aws-eks`.

9. Keep plaintext secrets out of git. Prefer External Secrets when the value already lives in Key Vault or Secrets Manager, so you do not make a second copy. Follow `azure-key-vault` and `aws-secrets-ssm`. The store uses the same workload identity. The ExternalSecret names the remote key and does not contain the value. Refresh on the order of an hour, not every second.

   ```yaml
   apiVersion: external-secrets.io/v1
   kind: ExternalSecret
   metadata:
     name: app-example
     namespace: example
   spec:
     refreshInterval: 1h
     secretStoreRef:
       name: example
       kind: SecretStore
     target:
       name: app-example
     data:
       - secretKey: setting
         remoteRef:
           key: example-setting
   ```

10. Use SOPS when the value has to live in git. Encrypt with age or a cloud KMS key. Commit the ciphertext. The key is not in the repo. A `.sops.yaml` creation rule limits the path and the key. Flux can decrypt with its SOPS provider. Argo CD needs a pinned plugin such as KSOPS. Pin that plugin. Do not add SOPS, External Secrets and another sealing tool in one change.

11. The production promotion is the approved deploy. Follow `pipelines-environments-approvals`. Automated sync must not bypass that approval. Review the rendered manifests with `k8s-manifest-review`. One app or one overlay. Name the cluster, the namespace and the revision.

## Safety checks

- One controller reconciles these apps.
- Production is pinned to a tag or a commit. The digest matches the digest that passed in the lower environment.
- The first sync does not prune. Prune and self-heal were rehearsed before they were turned on.
- The Argo CD project, if used, names one source and one destination namespace.
- The git credential is a repo-scoped app or deploy key. The cluster role is not cluster-admin.
- No Secret manifest contains data. The value is in External Secrets or in SOPS ciphertext.
- Image-update automation does not write to the production overlay.

## Rollback

Revert the overlay commit to the previous digest and let the controller sync. Follow `principle-rollback-first`. Rehearse that revert on dev or test. Do not `kubectl edit` a live object while self-heal is on. The next sync will put it back. Prune does not restore data that lived only on a volume. Call that out on the change before you enable prune. If a first sync deleted something unexpected, turn prune off, restore the git object, and sync again.

## Done when

- The app is healthy at the revision you merged.
- The production overlay runs the same digest you verified in the lower environment.
- Prune and self-heal are off, or they were rehearsed and the change says so.
- Secrets in git are ciphertext, or the cluster pulls them from Key Vault or Secrets Manager.
