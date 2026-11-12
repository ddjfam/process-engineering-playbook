# Controls by Design

**Reusable design template | Adapt thresholds and evidence requirements to the process**

Controls belong in the future-state workflow, with an accountable owner, a failure response and evidence that the control operated.

| Control | Type | Workflow behavior | Evidence / monitoring |
|---|---|---|---|
| Required intake fields | Preventive | Hold incomplete requests before downstream work | Validation outcome, missing fields and aging |
| Approval separation | Preventive | Requester cannot approve their own restricted request | Identity and approval event; exception review |
| Duplicate prevention | Preventive | Check a stable request key before creating another record | Duplicate disposition and linked original |
| Source-to-output reconciliation | Detective | Compare expected records/values with processed outputs | Mismatches, assigned owner and resolution |
| Aging / SLA trigger | Detective | Route overdue work to a named queue and escalate unresolved exceptions | Clock events, alert, acknowledgment and action |
| Change audit trail | Detective / accountability | Capture who changed what, when and why | Before/after state, reviewer and retained history |
| Controlled AI handoff | Preventive | Block missing or unusable evidence; route uncertainty to a reviewer | Readiness reason, reviewer decision and provenance |

## Design questions

Who can submit, change, approve and override? What happens when the system is unavailable? How are failed automations retried without duplicate work? Which exception needs immediate escalation? What evidence proves the process remained controlled after a change?

## Acceptance and sustainment

Test the normal path, incomplete inputs, duplicate requests, unauthorized approval, failed integration and overdue exceptions. The business/control owner approves the design and the technology owner confirms implementation. Define monitoring frequency, thresholds, remediation ownership and a change-review routine before scaling.

[CoE decision rights](coe-charter-and-governance.md) · [Workflow exception design](https://github.com/ddjfam/servicenow-workflow-automation/blob/main/end-to-end-workflow-example.md)
