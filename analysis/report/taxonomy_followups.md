# HW4 taxonomy follow-ups

Latest status: the student confirmed the [consolidated A/B/C packet](taxonomy_review_packet.md).
All three individual modes now have confirmed examples, boundaries and likely
LLM-judge evaluator types and are saved as final. The overall 5–8-mode taxonomy
and full labeling pass remain incomplete. Raindrop remains explicitly deferred.
The earlier follow-up record below is preserved as history; unrelated concerns,
including final-215 formatting, are not resolved by the A/B/C confirmation.

Earlier status: the first decision batch, the final-220 arithmetic/final-194 requested
details, and requested flag mentions in final-210/final-220 are approved;
remaining concerns are listed below.
Raindrop Workshop is deferred at the student's request. The course
error-analysis workflow preserves original notes alongside later decisions.
No final binary labels were created by this batch.

## Approved decision batch

### 1. Missing-response requirement

The student approved a response-completion requirement, resolving the
specification gap for the candidate `missing_usable_final_response`. The student
previously accepted missing-response suggestions on these existing traces:

- final-229, incomplete attempt: `44862c87ab91d6a519e7d7f20a42cb3c`;
  observation `accepted-hw4-depth-20-44862c87ab91d6a519e7d7f20a42cb3c`.
- final-238, incomplete attempt: `23d8c02949dfda9a3f1fc01352c861a6`;
  observation `accepted-hw4-depth-21-23d8c02949dfda9a3f1fc01352c861a6`.
- final-242, incomplete attempt: `f8b252caf57871e2070d567411e0fe2e`;
  observation `accepted-hw4-depth-22-f8b252caf57871e2070d567411e0fe2e`.

Approved requirement, now added to SPEC.md as **RESP-7**:

> Every user turn must receive an answer, clarification, refusal, escalation, or
> clear failure notice—not silence or only a promise to act.

Decision: approved in the student's “I approve all” reply to the numbered batch.
The candidate definition and requirement source now reflect RESP-7; the prior
version remains in taxonomy history. Historical provider/quota failures remain
execution causes, not proof of model reasoning errors. Existing traces predate
this proposed explicit requirement. A failure notice would satisfy this response
requirement but would not establish successful completion of the user's task.

### 2. Formatting-only re-review

The student approved both responses as displayed below after the Markdown
rendering update. Their original notes remain unchanged; new follow-up
observations record the approvals in the review interface. This does not prove
the cause of the earlier display concern. Source quotes can still show Markdown
punctuation.

**final-069**, trace `70fa06d346c4eb870abbe05e863cc15d`, annotation
`545cbce4-0c4e-4ded-ab02-bc5212fca231`:

- User: “Where do approved refunds go, and how long do they normally take?”
- Original note: “Formatting is not right, but otherwise the answers look correct”.
- Recorded final reply, displayed as Markdown:

> Approved refunds go back to the **original payment method** used for the purchase,
> and they normally arrive in **5 to 10 business days**. This is Cartwheel’s standard
> refund policy (**cw-refunds**).

**final-075**, trace `0e69d44e50e93a6e87166ffabb5849b4`, annotation
`6eb1a9ff-a943-4257-93df-266d584763c9`:

- User: “What response time should we quote after a case is escalated to a person?”
- Original note: “It's not human-readable”.
- Recorded final reply, displayed as Markdown:

> Quote **within 24 hours** for cases escalated to a human support agent.
>
> Policy basis: **cw-escalations** — “A human responds to an escalation within 24 hours.”

Decision for both: acceptable as displayed; the formatting concern is resolved
for these responses. The confirmations are recorded in
`human-confirmation-format-final-069-20260925` and
`human-confirmation-format-final-075-20260925`, linked to the original notes.
Required policy citations are not automatically failures. These snippets aid
re-review; they do not replace the complete traces.
The separate final-215 formatting concern remains unresolved and is not changed
by either answer.

## Additional boundary checks: decisions and remaining scope

- **final-220 date arithmetic:** Original annotation
  `93595629-fbf3-42c7-a280-22492eeebe67` on trace
  `4718c6889715fb5f8d4e7f81a1f1e814` includes “the date math is also wrong”.
  The recorded user explicitly requests reconciliation of `refund_eligible`
  with delivery 2026-06-24, a 7-day window, and as-of 2026-07-01. An offline call
  to the unchanged `seed.eligibility.is_refund_eligible` oracle confirmed 7
  elapsed days and eligibility on that inclusive boundary, with ineligibility
  on July 2. The student subsequently approved removing only the arithmetic
  objection. Confirmation: `human-confirmation-date-final-220-20260925`.
  The separate clarity/format concerns remain open. The later approval below
  resolves only mentioning the explicitly requested eligibility flag, not every
  technical detail or policy explanation.
- **final-194 requested details:** the user explicitly asks about product 2,
  its $9 price, and unambiguous identification. The student approved accepting
  these requested details; confirmation:
  `human-confirmation-requested-details-final-194-20260925`. Any separate
  verbosity/clarity concern remains open. This does not approve every additional
  detail in the reply.
- **Requested eligibility flags, approved:** final-210 and final-220 are
  support requests explicitly asking about `refund_eligible`. The student
  approved mentioning that flag in both answers. Follow-ups
  `human-confirmation-requested-flag-final-210-20260925` and
  `human-confirmation-requested-flag-final-220-20260925` preserve the decisions
  alongside original annotations `9daf60e2-48c3-4932-b9ac-be6014f3fa31` and
  `93595629-fbf3-42c7-a280-22492eeebe67`. Separate formatting/verbosity concerns
  remain open. This is not approval of every technical detail or policy
  explanation, and no new mode is proposed or confirmed here.

## Verification and remaining work

Preparation read the existing local review API snapshot and human annotations;
the date-boundary check was offline. After the student's approval, RESP-7 was
added, the existing missing-response candidate was revised with history, and two
follow-up observations were appended. The later approval of the date arithmetic
and requested product details added two further follow-up observations without
changing SPEC or the taxonomy. Approval of the two requested flag mentions added
two more follow-up observations, also without changing SPEC or the taxonomy.
Original notes, suggestions, sample
selections, and final labels were preserved. No model was called, no Langfuse
score was written, and no agent behavior changed.

Three approved draft categories are not the required 5–8 final categories.
Resolve the above boundaries, confirm supporting positives and close negatives,
and obtain further human evidence where needed. Final taxonomy, the final 15
uniform reviews, all per-mode labels, final reports, score read-back, and the
student's recording remain pending, alongside the deferred Workshop step.
