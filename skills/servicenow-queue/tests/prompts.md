# Prompts for servicenow-queue

Example asks for `servicenow-queue`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

Someone asks what is open, assigned to them, or waiting on their group.

### Expected for ask 1

- Load `servicenow-queue` and follow that file through its own done-when.
- Step: Use the instance hostname the user gave you. In examples that host is `example.service-now.com`. Do not guess a company instance. Call the API as that user, with their OAuth or SSO bearer token. Do not use a shared admin account and do not put the token or a password in the repo, the chat, or the command line. Follow `principle-no-static-credentials` and `ops-secrets-handling`.
- Check: The hostname and the person match what the user named.
- Done when: The user has the numbers, states, and short descriptions of their open records.

## Ask 2

Read the signed-in user.

### Expected for ask 2

- Load `servicenow-queue` and follow that file through its own done-when.
- Step: Read the signed-in user. If that user is not the person you were asked to act for, stop.
- Check: The call is authenticated as that person, not as a shared admin.
- Done when: Each record that needs a write is named against the skill that owns that write.
