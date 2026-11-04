---
name: aws-organizations-scps
description: "Use when you add an account, an OU or a service control policy. Keep workloads out of the management account, treat an SCP as a ceiling that does not grant access, and leave Control Tower policies untouched."
license: MIT
---

# Organizations and SCPs

The account is the blast-radius boundary. A service control policy sets the ceiling. It does not grant anything.

## Use when

- You create an account or an organizational unit, or you move an account.
- You add, change or detach a service control policy or a resource control policy.
- The organization uses AWS Control Tower, or someone proposes editing a guardrail.
- A workload is about to be deployed in the management account.

## Steps

1. Read the tree before you change it. Run `aws organizations list-roots`, then `aws organizations list-organizational-units-for-parent --parent-id r-example` with the root id that command returned, then `aws organizations list-accounts`. Record the management account id and which OU the affected account is in. Follow `principle-observe-before-you-fix`.

2. Keep workloads, pipelines and data out of the management account. SCPs and resource control policies do not apply there. People who administer the organization are few, and they use IAM Identity Center. Root has no access keys. Delegate Identity Center, GuardDuty and Security Hub to member accounts so daily work is not done in the management account.

3. Use a small set of organizational units. Security holds the log archive and the audit account. Infrastructure holds shared network and tooling. Workloads splits production from non-production. Sandbox is for experiments and is not routed to production. Suspended is for accounts being emptied. Do not invent a second tree beside this one.

4. Put one workload environment in its own account when a compromise or a bill must not spread. A new account is its own change. Follow `principle-change-safety` and `aws-cost-review`. Codify a console-created account or close it. Follow `principle-everything-as-code`.

5. Remember the direction of an SCP. Identity policies and resource policies grant access. An SCP only limits principals in member accounts, including the root user of those accounts. It does not limit the management account, and it does not limit a service-linked role. Leave `FullAWSAccess` attached. Add deny statements beside it. Detaching `FullAWSAccess` is an allow-list design and needs its own tested change.

6. Start with a small deny. Attach it to a sandbox account first. A region deny must still allow the home region and the global services the organization uses, and it is not the first policy you attach. `Resource` of `*` in the policy below is the SCP ceiling. An identity policy still names ARNs. Follow `aws-iam-least-privilege`.

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "DenyLeaveOrg",
         "Effect": "Deny",
         "Action": ["organizations:LeaveOrganization"],
         "Resource": "*"
       }
     ]
   }
   ```

7. Put a deny-all SCP on Suspended only. Confirm the account has no running workload first. A deny-all on a live account is an outage, not a guardrail.

8. If the organization is enrolled in Control Tower, leave its SCPs where they are. Do not edit them and do not detach them. Add a new SCP and attach that. Preventive controls are those SCPs. Detective controls are Config rules. Do not call `DisableAWSServiceAccess` for Control Tower. Create the account with Account Factory when Control Tower is the landing zone. An account invited or moved by hand is not enrolled until you enroll it.

9. Use a resource control policy when a bucket, a key or a queue must reject a principal from outside the organization. An RCP does not grant access and does not apply to the management account. One RCP is its own change. Do not add one to every resource by habit.

10. Watch the size. An SCP document is at most 5120 characters. Count the policies already attached to the root, the parent OUs and the account before you attach another. A pipeline that applies SCPs is federated and cannot change the management account's own identity. Follow `principle-no-static-credentials` and `principle-least-privilege`.

11. Send the organization trail to the log archive account. A workload account must not be able to delete that trail. If Terraform applies the policy, follow `terraform-plan-review` and `terraform-state-backends`.

## Safety checks

- No workload, pipeline or data store is being added to the management account.
- The SCP denies. It is not the policy that grants the job its actions. Those actions are in `aws-iam-least-privilege`.
- `FullAWSAccess` is still attached, unless this change is an allow-list you have already tested.
- Control Tower SCPs are unchanged. New guards are new policies.
- The new SCP was applied to a sandbox account before any production OU.
- A Suspended deny-all is not attached to an account that still runs a workload.
- The document fits the size limit, and the attachment count was checked.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Write the rollback before production. Follow `principle-rollback-first`.

1. Detach the SCP you added. Detach is the rollback. Do not delete the policy until nothing inherits it.
2. Move an account back to its previous OU with a separate change. Do not delete an OU that still has accounts.
3. If a Control Tower SCP was edited, re-register the OU or reset the landing zone. Do not keep editing the same policy.
4. Rehearse the detach in the sandbox account first.

## Done when

- The account sits in the OU this design names, and the management account still has no workload.
- The new SCP or RCP is attached where you intended and nowhere else.
- Control Tower, if present, shows no guardrail drift from this change.
- The change is verified in sandbox before anyone attaches it higher in the tree.
