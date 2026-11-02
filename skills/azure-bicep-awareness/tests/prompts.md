# Prompts for azure-bicep-awareness

Example asks for `azure-bicep-awareness`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I must read or change a Bicep file, an ARM template or a deployment stack.

### Expected for ask 1

- Load `azure-bicep-awareness` and follow that file through its own done-when.
- Step: Read `targetScope`, parameters, variables, resources, modules and outputs. Note each resource type, `apiVersion` and name expression. Implicit references are dependencies even when `dependsOn` is absent. Record whether a deployment stack already owns the resources.
- Check: `az bicep build` succeeded, and the generated JSON is not committed unless it was reviewed.
- Done when: You can say who owns each resource, Bicep or Terraform, and it is not both.

## Ask 2

Compile to check the file.

### Expected for ask 2

- Load `azure-bicep-awareness` and follow that file through its own done-when.
- Step: Compile to check the file. Read the JSON only to understand the compile. Do not commit `main.json` unless someone reviewed that exact file. A generated template that nobody reviewed does not get merged.
- Check: The what-if delete list is empty, or every delete is named on the change.
- Done when: The what-if or the Terraform plan matches the request and nothing else.
