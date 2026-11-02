# Prompts for jay-mode

Example asks for `jay-mode`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

A request could be an infrastructure change, a pipeline change, a review, or an incident.

### Expected for ask 1

- Load `jay-mode` and follow that file through its own done-when.
- Step: Read the request and take the first row that fits. The rows already put user impact before a review, and a review before a change.
- Check: The playbook is one of incident, review, pipeline, or infra.
- Done when: The request is classified, and the skill for that row has been followed through its own done-when.

## Ask 2

Load that one skill.

### Expected for ask 2

- Load `jay-mode` and follow that file through its own done-when.
- Step: Load that one skill. Follow its steps, safety checks, rollback, and done-when. The infra row is the only row that still needs `AGENTS.md` to name the skill. Do not copy the skill into the answer and then skip the file.
- Check: The skill that owns the work was loaded, not summarised from memory.
- Done when: The principles for that row were loaded.
