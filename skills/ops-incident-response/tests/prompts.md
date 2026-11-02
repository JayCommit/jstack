# Prompts for ops-incident-response

Example asks for `ops-incident-response`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

Production users cannot complete an action, or the data is at risk.

### Expected for ask 1

- Load `ops-incident-response` and follow that file through its own done-when.
- Step: Open one incident channel and name one lead. The lead owns the call. On a small team the lead can also post updates. The lead does not also have to be the only person reading logs. Say that there is an incident in the first message.
- Check: One lead is named, and the severity matches the user impact.
- Done when: User impact has stopped, or a SEV3 has an owner and a ticket.

## Ask 2

Set the severity from user impact.

### Expected for ask 2

- Load `ops-incident-response` and follow that file through its own done-when.
- Step: Set the severity from user impact.
- Check: The impact sentence says who, which action, and since when.
- Done when: The timeline shows the mitigation and the time the impact stopped.
