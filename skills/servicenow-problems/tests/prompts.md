# Prompts for servicenow-problems

Example asks for `servicenow-problems`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

The same CI or the same symptom has more than one incident.

### Expected for ask 1

- Load `servicenow-problems` and follow that file through its own done-when.
- Step: Act as the user. Follow `servicenow-queue`. Search active problems for this CI before you open another. Update the one that matches.
- Check: An active problem for this CI was searched first.
- Done when: The problem number is known, and each related incident points at it.

## Ask 2

Open a problem only when you can name the shared symptom and at least one incident number.

### Expected for ask 2

- Load `servicenow-problems` and follow that file through its own done-when.
- Step: Open a problem only when you can name the shared symptom and at least one incident number. Set impact, urgency, the CI, and the assignment group the user named. Do not copy priority by hand if the instance calculates it.
- Check: At least one incident number is related, or the change says this is a cause found with no open incident.
- Done when: The workaround or known error is recorded, or the change says there is no workaround yet.
