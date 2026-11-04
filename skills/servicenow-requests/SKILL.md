---
name: servicenow-requests
description: "Use when the signed-in user wants a ServiceNow catalog item. Search the catalog, submit that item with their variables, and stop before you approve the request."
license: MIT
---

# ServiceNow requests

A request is a catalog item the instance already publishes. It is not a change, and it is not a row inserted straight into `sc_request`.

## Use when

- The user asks for access, a repository, a group membership, or another catalog service.
- An open requested item might already cover the same ask.
- Someone proposes to create `sc_request` or `sc_req_item` by hand to skip the catalog.

## Steps

1. Act as the user. Follow `servicenow-queue` and include `sc_req_item`. If an active requested item already asks for the same item and the same CI or user, update the user on that number. Do not order it again.

2. A production change, including a firewall exception or a pipeline permission that is not a published catalog item, is a change. Follow `servicenow-changes`. Do not hide that work in a request.

3. Find the catalog item by the name the user used. Read its variables. Submit with `order_now` for that item id. Set only variables the item defines. Do not add a variable the item does not have. Do not put a secret in a variable or in the chat. Follow `ops-secrets-handling`.

   ```bash
   curl --silent --show-error --header "Authorization: Bearer ${SNOW_TOKEN}" --header "Accept: application/json" "https://example.service-now.com/api/sn_sc/servicecatalog/items?sysparm_text=example"
   ```

   Order with `POST /api/sn_sc/servicecatalog/items/00000000-0000-0000-0000-000000000000/order_now` after you replace the id with the item you found. The body is that item's variables and the quantity.

4. Record the request number the API returns. Approvals on the item stay where the catalog put them. The agent does not approve. Follow `principle-stop-at-approval`.

5. Tell the user the request number and the state label from this instance. Do not invent a RITM number.

## Safety checks

- An active requested item for the same ask was searched first.
- The item id came from the catalog search, not from memory.
- The body contains only that item's variables.
- A production change was sent to `servicenow-changes` instead of the catalog.
- The agent has not approved the request.
- No secret is in a variable or the chat.
- Stop before an apply, a merge, or a grant. Follow `principle-stop-at-approval`.

## Rollback

Cancel the requested item through this instance's cancel path when it was the wrong item and it has not been fulfilled. Do not delete the request. A fulfilled request is undone by the catalog item's fulfil reversal, or by a change if fulfilment already changed production. Follow `servicenow-changes` and `ops-rollback-plan` for that production undo.

## Done when

- The user has the request number from the API, and it is waiting on the catalog's approver.
- Or an existing requested item was reused and no second order was placed.
