# Prompts for principle-resource-baseline

Example asks for `principle-resource-baseline`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I create an Azure or AWS resource, a state backend, or a log sink.

### Expected for ask 1

- Load `principle-resource-baseline` and follow that file through its own done-when.
- Rule: Take the name from the scheme the repository already uses. If the repository has no scheme, write one short pattern and use it for every resource in the change. Do not invent a second prefix for a single resource.
- Red flag: A new name pattern appears for one resource while the rest of the subscription uses another.
- Done when: The name matches the scheme already in the repository, or the change writes the one pattern it will keep using.

## Ask 2

Use the tag keys the subscription or account already requires.

### Expected for ask 2

- Load `principle-resource-baseline` and follow that file through its own done-when.
- Rule: Use the tag keys the subscription or account already requires. When nothing is required yet, set `environment`, `owner`, `cost-centre` (or the existing `cost-center` key), and `data-class`. Do not add a second key for the same fact. Values are codes such as `prod` or `internal`. A person's name, an email, or a secret is not a tag value.
- Red flag: A production resource ships with no environment tag, or a tag value holds an email or a secret.
- Done when: The required tags are on the resource, and no tag value is a secret or a person's name.
