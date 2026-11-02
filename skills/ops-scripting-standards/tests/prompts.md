# Prompts for ops-scripting-standards

Example asks for `ops-scripting-standards`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I add or change a Bash, PowerShell, or Python script that touches Azure, AWS, Terraform, or a pipeline.

### Expected for ask 1

- Load `ops-scripting-standards` and follow that file through its own done-when.
- Step: Make a second run safe. Read the current object, then create or update it. A create that errors when the resource already exists is unfinished. Names do not include the clock. Follow `principle-idempotent-automation`.
- Check: Bash uses `set -euo pipefail`, shellcheck is clean, and the CI shellcheck invocation includes the file.
- Done when: The linter for that language is clean, and the new Bash file is in the shellcheck step when it lives in this repo.

## Ask 2

Bash starts with `set -euo pipefail`.

### Expected for ask 2

- Load `ops-scripting-standards` and follow that file through its own done-when.
- Step: Bash starts with `set -euo pipefail`. Quote expansions. Do not parse `ls`. Do not pipe a remote script into a shell. Run shellcheck, and add the file to the shellcheck invocation that CI already runs. In this repo that step lists `scripts/sync` and `tests/sync/*.sh`. A new Bash file is not covered until you add it there.
- Check: PowerShell uses strict mode, stops on errors, and implements `-WhatIf`. PSScriptAnalyzer is clean.
- Done when: A dry run prints the change and touches nothing. An apply run, then a second run, leaves no further change.
