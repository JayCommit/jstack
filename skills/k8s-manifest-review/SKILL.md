---
name: k8s-manifest-review
description: "Use when you add or review a Kubernetes workload. Set requests and a memory limit, probes, a restricted security context, a disruption budget and a NetworkPolicy before the manifest is applied."
license: MIT
---

# Kubernetes manifest review

Read the rendered workload. A pod gets a budget, a policy and a security context before it shares a cluster with anything else.

## Use when

- You add or change a Deployment, StatefulSet, DaemonSet, Job or CronJob.
- A namespace has no NetworkPolicy, no LimitRange, or a pod that runs as root.
- You are about to apply a manifest to AKS or EKS.
- A chart or an overlay renders a workload and you need to review the output. Follow `k8s-helm-review` for the chart, then review the manifests here.

## Steps

1. Read the live objects before you change them. Run `kubectl get deploy,sts,ds,pdb,netpol,sa -n example`. Record replicas, images and any disruption budget. Follow `principle-observe-before-you-fix`.

2. Pin the image by digest. Follow `pipelines-artifacts-releases` and `k8s-dockerfile-hardening`. `latest` and a moving tag are not a release. `imagePullPolicy` does not turn a tag into a pin.

3. Set a CPU request and a memory request. Set a memory limit, and set it equal to the memory request unless the change record says why a burst is safe. A CPU limit throttles the process. Set one only when a quota requires it, and write that down. Do not copy the production sizes into dev or test. Follow `principle-cost-awareness`.

4. Put a LimitRange on the namespace so a pod with no request gets a small default, and a ResourceQuota so one workload cannot take the pool. A high default hides a missing request. Read the quota before you raise it.

5. Add a startup probe when the process is slow to listen. The readiness probe gates traffic. The liveness probe exists for a deadlock the process cannot leave. Point liveness at a path that does not call the database or another service. A failing dependency must make the pod unready, not restarted.

6. Set the security context on the pod and on each container. The image user is `k8s-dockerfile-hardening`. The manifest still sets `runAsNonRoot`.

   ```yaml
   spec:
     securityContext:
       runAsNonRoot: true
       runAsUser: 65532
       seccompProfile:
         type: RuntimeDefault
     containers:
       - name: app
         securityContext:
           allowPrivilegeEscalation: false
           readOnlyRootFilesystem: true
           capabilities:
             drop: ["ALL"]
   ```

7. Workload namespaces enforce the restricted Pod Security Standard. Leave system namespaces out of that label. Read the pods already in the namespace. When any of them would violate restricted, set the label to `warn` first and move to `enforce` after those pods match. Do not label a workload namespace `privileged` so one pod will schedule. `privileged`, `hostNetwork`, `hostPID` and `hostPath` need a named node feature and their own change.

   ```yaml
   apiVersion: v1
   kind: Namespace
   metadata:
     name: example
     labels:
       pod-security.kubernetes.io/enforce: restricted
   ```

8. Give the pod its own ServiceAccount. Set `automountServiceAccountToken: false` unless the pod calls the Kubernetes API. On AKS, authenticate to Azure with workload identity. Follow `azure-aks`. On EKS, use Pod Identity. Follow `aws-eks`. Do not mount a cloud key into the pod.

9. Run at least two replicas in production, spread across the zones the cluster actually has. A PodDisruptionBudget uses `maxUnavailable: 1` or a `minAvailable` that leaves room for a surge. Do not set `minAvailable` equal to the replica count. Do not set both fields. The upgrade path is in `azure-aks` and `aws-eks`.

10. Start the namespace with a default-deny NetworkPolicy for ingress and egress, and allow the app port, DNS, and the private endpoints it calls in the same change. A deny with no allow rules takes the namespace off the network. Select the pods you mean to select.

11. Keep secret values out of the manifest. Reference a secret the cluster already syncs. Follow `azure-key-vault`, `aws-secrets-ssm`, or `gitops-argocd-flux`. A ConfigMap is for values that can be public.

12. Diff before you apply. `kubectl diff -f app.yaml -n example` or the GitOps diff is the review. Do not apply to production from a laptop. One workload. Name the cluster, the namespace and the pipeline. Follow `principle-change-safety`. If Terraform renders the manifest, follow `terraform-plan-review`.

## Safety checks

- The image reference contains `@sha256:<digest>`.
- CPU and memory requests are set. The memory limit is set. A CPU limit is justified or absent.
- Readiness and liveness check different things. Liveness does not depend on another service.
- The pod is non-root, drops all capabilities, and uses a read-only root filesystem.
- The workload namespace enforces restricted Pod Security. System namespaces were not relabelled.
- The ServiceAccount token is unmounted unless the pod calls the API. Cloud access is workload identity or Pod Identity.
- A disruption budget leaves a surge, and a default-deny NetworkPolicy has the allows it needs.
- No secret value is in the manifest or the diff.

## Rollback

Put the previous manifest back. Follow `principle-rollback-first`. Rehearse `kubectl rollout undo` on a non-production namespace. If Argo CD or Flux has self-heal or a later sync, a live undo is reverted. Roll the git revision back instead. Follow `gitops-argocd-flux`. A NetworkPolicy rollback is restoring the previous allow rules, not deleting every policy and leaving the namespace open.

## Done when

- The rendered workload matches the requests, probes, security context, budget and policy above.
- `kubectl diff` is empty after apply, or the GitOps sync is healthy.
- The pod becomes ready and passes its readiness probe in this environment.
- The change is verified here before anyone promotes the same digest.
