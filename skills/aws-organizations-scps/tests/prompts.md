# Prompts for aws-organizations-scps

Example asks for `aws-organizations-scps`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I create an account or an organizational unit, or you move an account.

### Expected for ask 1

- Load `aws-organizations-scps` and follow that file through its own done-when.
- Step: Read the tree before you change it. Run `aws organizations list-roots`, then `aws organizations list-organizational-units-for-parent --parent-id r-example` with the root id that command returned, then `aws organizations list-accounts`. Record the management account id and which OU the affected account is in. Follow `principle-observe-before-you-fix`.
- Check: No workload, pipeline or data store is being added to the management account.
- Done when: The account sits in the OU this design names, and the management account still has no workload.

## Ask 2

Keep workloads, pipelines and data out of the management account.

### Expected for ask 2

- Load `aws-organizations-scps` and follow that file through its own done-when.
- Step: Keep workloads, pipelines and data out of the management account. SCPs and resource control policies do not apply there. People who administer the organization are few, and they use IAM Identity Center. Root has no access keys. Delegate Identity Center, GuardDuty and Security Hub to member accounts so daily work is not done in the management account.
- Check: The SCP denies. It is not the policy that grants the job its actions. Those actions are in `aws-iam-least-privilege`.
- Done when: The new SCP or RCP is attached where you intended and nowhere else.
