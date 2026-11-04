# Prompts for servicenow-requests

Example asks for `servicenow-requests`. The expected behaviour is what that skill requires. Ask 2 records the next step. The check and the done-when beside it are the next items in that skill. These files are not a live trial.

## Ask 1

The user asks for access, a repository, a group membership, or another catalog service.

### Expected for ask 1

- Load `servicenow-requests` and follow that file through its own done-when.
- Step: Act as the user. Follow `servicenow-queue` and include `sc_req_item`. If an active requested item already asks for the same item and the same CI or user, update the user on that number. Do not order it again.
- Check: An active requested item for the same ask was searched first.
- Done when: The user has the request number from the API, and it is waiting on the catalog's approver.

## Ask 2

A production change, including a firewall exception or a pipeline permission that is not a published catalog item, is a change.

### Expected for ask 2

- Load `servicenow-requests` and follow that file through its own done-when.
- Step: A production change, including a firewall exception or a pipeline permission that is not a published catalog item, is a change. Follow `servicenow-changes`. Do not hide that work in a request.
- Check: The item id came from the catalog search, not from memory.
- Done when: Or an existing requested item was reused and no second order was placed.
