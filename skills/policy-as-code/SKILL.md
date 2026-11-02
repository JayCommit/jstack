---
name: policy-as-code
description: "Use when you add or change a policy on a Terraform plan or a Kubernetes manifest. Run Conftest in CI, start Azure Policy and admission in audit, and keep an SCP as the AWS ceiling."
license: MIT
---

# Policy as code

A policy fails a bad change in CI, or it reports first and enforces in a later change. It does not grant access.

## Use when

- You add an OPA or Conftest rule for a Terraform plan or a Kubernetes manifest.
- The organisation uses Sentinel in HCP Terraform or Terraform Enterprise.
- You assign Azure Policy, or you add a Kyverno or Gatekeeper policy.
- You add an AWS Config rule, or someone asks a policy to stand in for IAM.

## Steps

1. Write down the decision the rule enforces. One rule is one change. A storage account is not public. A container runs as non-root. A production resource carries the tag you require. Generic Terraform scans stay in `terraform-static-analysis`. This skill is for the rule those scans do not encode.

2. Test the plan JSON with Conftest. `terraform show -json` can print secret values. Keep the file out of a public artefact. Follow `pipelines-terraform-workflow` for how the plan is stored. The policy job can read the repo and cannot apply. Follow `principle-least-privilege`.

   ```text
   terraform show -json tfplan > plan.json
   conftest test plan.json --policy policy/plan --namespace terraform
   ```

3. Write Rego in the version your pinned Conftest uses. Current Conftest expects Rego v1, with `if` and `contains`. Pin Conftest. A floating policy bundle means yesterday's exception fails today's build. Pin the bundle to a commit or a tag.

   ```rego
   package terraform

   deny contains msg if {
     some resource in input.resource_changes
     resource.type == "azurerm_storage_account"
     resource.change.after.public_network_access_enabled == true
     msg := sprintf("%s allows public network access", [resource.address])
   }
   ```

4. Test rendered manifests the same way, after `helm template` or `kustomize build`. Follow `k8s-helm-review` and `k8s-manifest-review`. A warn-only job is not a gate. The pull request goes red when `conftest test` finds a deny.

5. An exception names the rule, the resource, the reason and an expiry. Do not add a wildcard exception to clear one address.

6. If the organization uses Sentinel, read the existing policy set before you add a rule. Do not encode the same decision in Sentinel and in Conftest. Advisory reports. Soft-mandatory can be overridden. Hard-mandatory cannot. Run the rule as soft-mandatory on a non-production workspace, then make it hard-mandatory. Follow `terraform-workspaces-environments`. A production override needs the same approval as the apply. Follow `pipelines-environments-approvals`.

7. Assign Azure Policy at the management group the landing zone already uses. Follow `azure-landing-zones`. Look the definition id up with `az policy definition list`. The id below is a placeholder. When the definition takes an effect parameter, set it to Audit. Move that effect to Deny in a later change, after you have read the non-compliant list. An exemption has an expiry. A policy assignment does not grant RBAC. Follow `azure-rbac-entra`.

   ```bash
   az policy assignment create --name audit-public-storage --scope /providers/Microsoft.Management/managementGroups/example --policy 00000000-0000-0000-0000-000000000000 --params "{\"effect\":{\"value\":\"Audit\"}}"
   ```

8. On AWS, an SCP is the ceiling and it does not grant access. Follow `aws-organizations-scps`. Do not edit a Control Tower policy. A Config rule detects. It does not grant and it does not replace the SCP. Turn the recorder on before you depend on the rule. A rule with no recorder never evaluates. Deleting a rule is the rollback. Do not turn the recorder off. Config rules are a cost. Follow `principle-cost-awareness` and `aws-cost-review`.

9. Pick Kyverno or Gatekeeper for a new cluster. Do not install both. Start in audit. Enforce after the audit is clean, or every violation has an exception with an expiry. Read the audit before you enforce. A deny that rejects a DaemonSet can block a node upgrade. Follow `azure-aks` or `aws-eks` when the policy affects an upgrade.

   ```yaml
   apiVersion: kyverno.io/v1
   kind: ClusterPolicy
   metadata:
     name: require-non-root
   spec:
     background: true
     rules:
       - name: run-as-non-root
         match:
           any:
             - resources:
                 kinds:
                   - Pod
         validate:
           failureAction: Audit
           message: Pods run as a non-root user.
           pattern:
             spec:
               securityContext:
                 runAsNonRoot: true
   ```

10. For Gatekeeper, add a ConstraintTemplate and a Constraint. Leave `enforcementAction` as `dryrun` until the audit is clean, then set `deny`. Do not upgrade Gatekeeper and add a deny constraint in the same change.

11. The identity that assigns policy is federated and can do that job only. Follow `principle-no-static-credentials`. If Terraform applies the assignment, follow `terraform-plan-review` and `terraform-state-backends`. One policy. Name the management group, the account, or the cluster. Follow `principle-change-safety`.

## Safety checks

- The rule encodes one decision, and Checkov or Trivy is not being asked to carry it instead. Those stay in `terraform-static-analysis`.
- Conftest is pinned, the policy bundle is pinned, and a deny fails the pull request.
- The plan JSON is not published as a public artefact.
- Sentinel, if present, is not duplicated in Conftest. Production is hard-mandatory only after a soft-mandatory run.
- Azure Policy starts at Audit. An exemption expires.
- The SCP was not used as a grant, and a Control Tower policy was not edited.
- Admission is audit or dry-run until the violations are triaged.
- Kyverno and Gatekeeper are not both new on this cluster.

## Rollback

Put the policy back to audit, or detach the assignment you added. Follow `principle-rollback-first`.

1. Rehearse the detach or the return to Audit on a sandbox subscription, account, or cluster.
2. Do not delete a policy definition or a ConstraintTemplate that other assignments still use.
3. For Kyverno, set `failureAction` back to `Audit`. For Gatekeeper, set `enforcementAction` back to `dryrun`.
4. A bad Conftest rule is reverted in git. Do not skip the job to go green.

## Done when

- A bad plan or a bad manifest fails in CI, and a good one passes.
- Cloud and admission policies are still in the mode you chose, audit or enforce.
- Every exception has an owner and an expiry.
- The change is verified on sandbox or a non-production cluster before it covers production.
