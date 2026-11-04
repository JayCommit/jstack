# Prompts for ops-backup-restore

Example asks for `ops-backup-restore`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I add a database, a disk, or a volume, and the change names no backup.

### Expected for ask 1

- Load `ops-backup-restore` and follow that file through its own done-when.
- Step: Write what you must get back, the oldest recovery point you can accept, and how long the restore may take. Those three sit on the change. A data store with no numbers does not go to production. Follow `principle-change-safety`.
- Check: The change names the data, the oldest acceptable point, and the restore time.
- Done when: A non-production restore has been read back, and the output is on the change.

## Ask 2

Use the backup home the estate already runs.

### Expected for ask 2

- Load `ops-backup-restore` and follow that file through its own done-when.
- Step: Use the backup home the estate already runs. On Azure that is the Recovery Services vault or Backup vault in the platform subscription. Follow `azure-landing-zones`. On AWS that is an AWS Backup vault outside the management account. Follow `aws-organizations-scps`. A cluster volume uses the backup the cluster already runs. Object storage keeps the versioning that landing zone already chose. Do not add a second vault per application. If there is no home, add one, and say so.
- Check: The vault is the one the estate already runs, or the change says this is the first home.
- Done when: The vault denies delete, and the locked mode is still the reversible one unless a drill has already succeeded.
