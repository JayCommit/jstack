# Prompts for terraform-module-design

Example asks for `terraform-module-design`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

I add a module that Azure or AWS stacks will call.

### Expected for ask 1

- Load `terraform-module-design` and follow that file through its own done-when.
- Step: Split by concern. One module owns the network, another the data store, another the workload identity. The root module composes them. Pass outputs through the root. A network module does not call the database module.
- Check: No child module contains a `provider` block, an access key, a storage account key or a client secret.
- Done when: Inputs and outputs are typed and described, and validation rejects values that would plan the wrong thing.

## Ask 2

Give every variable a `type` and a `description`.

### Expected for ask 2

- Load `terraform-module-design` and follow that file through its own done-when.
- Step: Give every variable a `type` and a `description`. Add `validation` when a bad value would plan the wrong region, SKU or address space. State the meaning and the unit. Do not repeat the variable name as the description.
- Check: Every variable has a type and a description. Every output has a description.
- Done when: The published version is immutable, and every caller pins it.
