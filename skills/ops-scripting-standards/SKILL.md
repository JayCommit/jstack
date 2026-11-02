---
name: ops-scripting-standards
description: "Use when you write a Bash, PowerShell, or Python automation script. Fail on errors and unset variables, support a dry run, and make a second run change nothing."
license: MIT
---

# Scripting standards

A script fails loudly, prints what it would change, and a second run with the same inputs changes nothing.

## Use when

- You add or change a Bash, PowerShell, or Python script that touches Azure, AWS, Terraform, or a pipeline.
- A script succeeds the first time and fails the second because the resource exists.
- A destructive script runs as soon as you invoke it, with no dry run.
- A secret is passed as an argument or written to the log.

## Steps

1. Make a second run safe. Read the current object, then create or update it. A create that errors when the resource already exists is unfinished. Names do not include the clock. Follow `principle-idempotent-automation`.

2. Bash starts with `set -euo pipefail`. Quote expansions. Do not parse `ls`. Do not pipe a remote script into a shell. Run shellcheck, and add the file to the shellcheck invocation that CI already runs. In this repo that step lists `scripts/sync` and `tests/sync/*.sh`. A new Bash file is not covered until you add it there.

   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   ```

3. PowerShell fails closed and supports `-WhatIf`. `Invoke-ScriptAnalyzer` already runs on `scripts/` in CI. Keep that clean. Use approved verbs. A script that changes Azure uses the Az module so `-WhatIf` is real. A one-off `az` command in a skill example is not this script.

   ```powershell
   #Requires -Modules Az.Accounts
   [CmdletBinding(SupportsShouldProcess = $true)]
   param(
     [Parameter(Mandatory = $true)]
     [string] $ResourceGroupName
   )

   Set-StrictMode -Version Latest
   $ErrorActionPreference = 'Stop'

   if ($PSCmdlet.ShouldProcess($ResourceGroupName, 'Create or update the resource')) {
     Write-Output "Updating $ResourceGroupName"
   }
   ```

4. Python takes `--apply` and otherwise prints the actions and changes nothing. Exit non-zero on failure. Do not use a bare `except`. Do not put a secret in an argument. It shows up in the process list. Pin the dependencies you import.

   ```python
   import argparse
   import sys

   def main() -> int:
       parser = argparse.ArgumentParser()
       parser.add_argument("--apply", action="store_true")
       args = parser.parse_args()
       if not args.apply:
           print("dry run: no changes")
           return 0
       # Read the current object, then create or update it.
       return 0

   if __name__ == "__main__":
       sys.exit(main())
   ```

5. A script that deletes or replaces defaults to the dry run. `--apply`, or omitting `-WhatIf` on the PowerShell script, is the apply. The dry run prints each object it would change and does not call the cloud. Follow `principle-change-safety` for the radius of that apply.

6. Keep secrets out of the file, the arguments, and the log. Read them from the home in `ops-secrets-handling`. The identity is federated. Follow `principle-no-static-credentials`. Do not catch an error and continue with `|| true` unless the change record says that command is optional.

7. If the script applies Terraform, it applies a saved plan. Follow `terraform-plan-review`. One script, one job. Say which subscription or account it can touch. Follow `ops-blast-radius`.

## Safety checks

- Bash uses `set -euo pipefail`, shellcheck is clean, and the CI shellcheck invocation includes the file.
- PowerShell uses strict mode, stops on errors, and implements `-WhatIf`. PSScriptAnalyzer is clean.
- Python defaults to a dry run, exits non-zero on failure, and has no bare `except`.
- A second run with the same inputs changes nothing.
- No secret is in the file, the arguments, or the output.
- A delete or a replace does not run unless `--apply` was passed, or `-WhatIf` was left off on purpose.

## Rollback

A script that changes a resource has a rehearsed way back: a flag, a second script, or the rollback command for that change type. Follow `ops-rollback-plan` and `principle-rollback-first`. Run that path on a non-production resource before production uses the script. If the script fails halfway, a rerun reaches the same end state or stops with the error. It does not create a second copy.

## Done when

- The linter for that language is clean, and the new Bash file is in the shellcheck step when it lives in this repo.
- A dry run prints the change and touches nothing. An apply run, then a second run, leaves no further change.
- The rollback path has been run off production.
