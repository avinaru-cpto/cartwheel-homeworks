# Homework 4 review summary

Status: **non-deferred analysis complete**. The 100-trace review, five-mode
taxonomy, 500 structured judgments, sample-fraction calculation, taxonomy
revision, AgentDebug comparison, and final-batch assessment are complete. All
500 current judgments are synchronized to Langfuse. Raindrop Workshop and the
video remain deliberately deferred by the student; see the final status section.

Earlier “pending” statements below are preserved as a chronological audit of
the review. The authoritative result is in
[Final results and handoff](#final-results-and-handoff).

## Specification revision: RESP-6

Approved by the student on 2026-09-24 and added to [SPEC.md](../../SPEC.md).

> **RESP-6.** For status-only requests, lead with the current status and relevant dates. Omit prices unless requested or necessary to answer the question.

### Motivating human observation

- Scenario: `final-001`.
- Stable trace ID: `354d27074968be0c96490fb55ce788e9`.
- [Langfuse trace](http://localhost:3000/project/cartwheel-dev/traces/354d27074968be0c96490fb55ce788e9).
- Human annotation: `993df9c1-aedf-4c7c-83b1-0115c1c7cf9d`, saved in
  [annotations.json](../state/annotations.json).
- Selected evidence: `- **Total:** $217.75` in the assistant's final response.
- The same observation is also recorded as the initial first-failure note
  `28bb0868-eace-4e67-8f23-4c1f5bcfcedc` on this trace. These are two records
  of one observation, not two reviewed traces or two distinct failures.

Original human note, preserved unchanged:

> The user asked only for order status. The response unnecessarily included the total price. I would prefer the status and relevant dates without the price. This needs an explicit requirement in SPEC.md.

### Decision and scope

The student identified an unwanted, unsolicited price in an order-status answer
and approved the wording of RESP-6. RESP-5 required direct and respectful
explanations but did not explicitly prohibit unsolicited prices in status-only
answers. This revision makes that desired behavior explicit.

The trace predates RESP-6. It motivated a newly stated requirement; it is not
evidence that the agent disregarded this explicit rule when the trace was
recorded. The student's original notes remain unchanged for the review history.

This change updates documentation only. It does not change the running agent,
system prompt, tools, permissions, or recorded traces. No final failure mode,
binary label, or Langfuse score was created by this revision. Implementing the
new requirement in the agent remains separate work.

## Approved review boundary: requested technical records

The student approved this boundary after reviewing the context of the two
JSON-response observations below:

> JSON is acceptable when support staff explicitly request an exact record.
> Expect plain language for ordinary customer questions; JSON alone is not a
> failure when it serves the explicit technical request.

### Evidence and originating observations

- `final-063`: [trace `ebd7a0e0a7e0e8277eec67e4e2e50a45`](http://localhost:3000/project/cartwheel-dev/traces/ebd7a0e0a7e0e8277eec67e4e2e50a45),
  human annotation `6d80726d-0f03-443b-afcf-92e582309dd6`.
  The support user asked: “Look up Modern Mug at Juniper Home Goods; return the
  exact product record, please.” The final assistant reply returned the product
  record in a JSON code block. The original note was: “It gave a JSON review as
  opposed to giving it in plain text to a human, so not human-readable”.
- `final-066`: [trace `8e629c7bb3805aaaa7b9c818e50e9dc8`](http://localhost:3000/project/cartwheel-dev/traces/8e629c7bb3805aaaa7b9c818e50e9dc8),
  human annotation `6a6678f9-2931-4fbd-b579-6829b0e0b7e8`.
  The support user asked: “Look up Handmade Mug at Juniper Home Goods; return the
  exact product record, please.” The final assistant reply returned the product
  record in a JSON code block. The original note was: “This is in JSON. It's not
  in human-readable text”.

### Grouping revision and scope

The initial observations objected to JSON as not human-readable. The approved
boundary narrows that concern to whether the response format suits the user's
role and explicit request. Do not count these two traces as formatting failures
solely because their final replies contain JSON. Retain them as boundary examples
when drafting a readability or response-format mode, rather than using them to
support a blanket “JSON output is a failure” category.

This is a human-approved interpretation of the response-style concern associated
with RESP-5, not a new prohibition on JSON and not a new final failure mode. The
boundary concerns assistant replies; structured tool arguments and results are
not customer-facing prose and are not failures merely for being structured.

The original annotations remain unchanged in
[annotations.json](../state/annotations.json). This record preserves the later
human decision without replacing the first-pass observations or declaring either
whole trace error-free. Final per-mode judgments and Langfuse scores remain
pending. This JSON-format approval did not resolve the separate escalation
concerns; the student's subsequent decision on those appears below.

## Approved review boundary: appropriate human escalations

The student subsequently accepted the recommendation to treat the escalation
decisions in `final-163` and `final-180` as appropriate. Both users explicitly
requested human escalation; the dispute in `final-163` also requires human
handling under ESC-3.

### Evidence and originating observations

- `final-163`: [trace `b80177ceb82a6bf8ef03495031b94aef`](http://localhost:3000/project/cartwheel-dev/traces/b80177ceb82a6bf8ef03495031b94aef),
  human annotation `b77fef5e-f2df-49f6-9578-a2eb2c8cadcc`.
  The shopper recognized order 461 but disputed the charge and explicitly asked
  for a person to review it without describing it as resolved. The escalation
  tool returned success with ticket 153 and a 24-hour response time. The final
  reply reported the handoff and explicitly said the dispute was not resolved.
  The original observation questioned whether the agent should request more
  information instead of letting the shopper dictate its actions.
- `final-180`: [trace `5b4ef21394b1c7c221b45bc755a6d341`](http://localhost:3000/project/cartwheel-dev/traces/5b4ef21394b1c7c221b45bc755a6d341),
  human annotation `04c40fb4-c163-4dcd-867b-8d28b2187945`.
  The support user requested a concise response about order 8001's
  delivery-before-shipment record and the appropriate escalation. The agent
  looked up the order, identified the conflicting dates, and created ticket 159.
  The tool confirmed success with a 24-hour response time, which the final reply
  reported. The original observation expressed uncertainty about following a
  user's request to escalate.

### Decision and scope

Do not group these observations as failures merely because the agent followed
the request to escalate. Following an authorized, in-scope request for human
review is not itself an authority violation. ESC-3 requires human handling of
disputes, and RESP-3 requires acknowledging inconsistent information rather than
inventing a correction.

This decision is specific to the escalation concern in these two traces. It is
not a rule to obey every requested action, not an approval of every aspect of
either trace, and not a new judgment about the wording of the handoff. Any
separate response-clarity concern still needs its own evidence and human
decision.

The original annotations remain unchanged in
[annotations.json](../state/annotations.json), preserving the initial uncertainty
alongside this later human decision. No final mode, binary label, Langfuse score,
specification change, or agent behavior change was made by recording this
boundary.

## Approved draft categories

The student accepted the following three definitions together as a fair summary
of their observations. They are saved with status `candidate` in
[patterns.json](../state/patterns.json), not as the final HW4 taxonomy.

| Candidate | Approved draft definition | Requirement status |
| --- | --- | --- |
| `unsolicited_status_price` | A status-only answer includes a price that the user did not request and that is not needed to answer the question. | RESP-6, a newly approved specification revision; the motivating traces predate it. |
| `answer_obscured_by_excess_detail` | Irrelevant explanation makes the actual answer to the user's question difficult to find or understand. | RESP-5, with the approved technical-record and escalation boundaries above; required RESP-1 citations are not automatically excessive. |
| `missing_usable_final_response` | The run stops without a usable final response answering the user's request. | Specification gap: an explicit response-completion or graceful execution-error requirement remains to be agreed. |

Each candidate links to originating human annotation IDs. The proposed example
associations are bookkeeping for the next human review, not confirmed per-mode
positive labels. Accordingly, the confirmed-positive and close-negative lists
remain empty; proposed examples are stored separately as
`candidate_example_trace_ids`. No human annotation or binary label was changed.

LLM judges are proposed for the first two definitions, since relevance depends
on the request. A code check is proposed for missing final responses; it must
distinguish absent answers from poor but completed answers and separate recorded
execution causes from model behavior. These evaluator choices are not yet
human-approved, implemented, or validated. Historical quota/provider errors do
not establish the current availability of the provider or a model-reasoning
failure. Different execution causes may require splitting the third draft.

At this checkpoint, all 60 planned breadth traces have initial reviews: 15
uniform, 15 cluster representatives, and 30 role-stratified (10 each for shopper,
merchant, and support). Two additional context traces also have initial-review
records but are not counted toward those prescribed batches. The 25-trace depth
batch and final 15-trace uniform batch have not been selected. The final taxonomy
still needs evidence-backed categories, confirmed positives and close negatives,
and all per-trace binary judgments; three approved drafts do not satisfy the
assignment's 5–8 final-mode requirement.

Verification: the local review API returned all three candidates after saving,
while annotations, labels, suggestions, and the sample manifest were unchanged.
No live model was called and no Langfuse score was written.

## Depth-batch preparation checkpoint

After the student approved preparing the next batch, 25 distinct, previously
unreviewed traces were added to the depth batch. There are now 85 selected traces
and 60 completed initial reviews. The 25 new reviews and their suggestion
decisions are pending; the final 15 uniform traces remain unselected.

The depth selection includes 12 possible matches and 13 possible close negatives
across the three draft categories. These are retrieval groups, not failure
counts. All suggestions are pending, and annotations, taxonomy definitions,
binary labels, and the earlier 60 sample selections were preserved. See
[depth_review_plan.md](depth_review_plan.md) for instructions and remaining
deliverables, and [depth_search_plan.json](../state/depth_search_plan.json) for
per-trace selection evidence.

## Depth-review completion and note-meaning clarification

All 25 depth traces now have initial human reviews, bringing the prescribed
review count to 85. The final 15 uniform traces remain unselected.

The student clarified that a price objection means failure present, while praise
such as “this is perfect” means the response was wanted and no failure was
observed. Generic Accept/Reject buttons had led to opposite recorded dispositions
in some cases. Eleven clear suggestion dispositions were reconciled using that
human clarification: final-004 now accepts the price-failure suggestion, while
ten response-approval notes reject their respective failure suggestions.
Original clicks, reasons, and timestamps remain in each suggestion's
`decision_history`; full provenance is in
[review_clarifications.json](../state/review_clarifications.json).

This is a clarification of the student's intended judgments, not an independent
assistant reassessment. Initial notes and original acceptance observations were
preserved. In particular, rejecting the missing-response suggestion for the
completed final-242 attempt does not remove its separate price objection.

There are now 10 accepted and 13 rejected suggestion dispositions, with 2 still
pending (final-084 and final-109). These are not final failure counts. The accepted
dispositions on final-042 and final-215 remain unresolved for taxonomy purposes:
final-042 is an exact-record request outside the status-only definition, while
final-215 combines format approval with an asterisk-removal request. Neither was
silently reclassified. The incomplete final-229 trace also retains the history of
an initial no-failure record followed by an explicit missing-response concern.

No final mode, binary label, Langfuse score, agent change, or interface-code
change was made during this reconciliation.

### Follow-up confirmation: final-042 and final-215

The student confirmed both outstanding boundary interpretations. For final-042,
the requested exact product record may include JSON and price; its
`unsolicited_status_price` suggestion is now rejected. For final-215, the answer
content was acceptable but the formatting was not good; its
`answer_obscured_by_excess_detail` suggestion is now rejected. The formatting
criticism is preserved for separate review, with no assumption about its cause.

Both previous suggestion decisions remain in history. The follow-up record in
[review_clarifications.json](../state/review_clarifications.json) supersedes the
earlier unresolved status of these two cases, not the original human notes.
Suggestion dispositions now total 8 accepted, 15 rejected, and 2 pending
(final-084 and final-109). These are not final failure counts. The prescribed
review count remains 85, and no final binary label or Langfuse score was created.

### Final depth-suggestion closure

The student approved rejecting the remaining excess-detail suggestions for
final-084 and final-109 based on their saved “no failure observed” reviews.
Both decisions were saved through the review API and read back successfully.
All 25 depth suggestions are now resolved: 8 accepted, 17 rejected, 0 pending.
These are suggestion dispositions, not final failure counts or binary labels.
Annotations, taxonomy definitions, labels, and the sample manifest were unchanged
by this closure. All 85 prescribed initial reviews are complete; the final 15
uniform traces remain unselected.

### Workshop setup preflight

Read-only checks on 2026-09-24 found no `raindrop` executable on PATH or at the
default installation path, no `raindrop-ai` package in the repository's virtual
environment, and no responding local Workshop health endpoint on port 5899.
The environment uses Python 3.12.13, openai-agents 0.17.7, Langfuse 3.15.0, and
opentelemetry-sdk 1.43.0.

The [official Workshop instructions](https://github.com/raindrop-ai/workshop)
and the current installer and instrument-agent skill were inspected. The
installer places a binary under `~/.raindrop/bin`, updates the shell PATH, and
normally runs coding-agent setup. Cloud setup is optional and is not requested.
Integration must preserve the existing Langfuse/OpenTelemetry provider.

Installation and instrumentation remain pending; no package, shell configuration,
agent code, or tracing configuration was changed during preflight. Zero Workshop
runs have been verified or reviewed. No live model was called. The required
5–10-run Workshop inspection and its student assessments are still outstanding.

### Resume decision: defer Raindrop, continue taxonomy work

The student explicitly requested continuing HW4 without doing Raindrop Workshop
now. Workshop is deferred to a later session, not waived or complete. Do not
resume installation or instrumentation without a new request. No Workshop
installation, package change, cloud setup, or live model run has taken place.

The next work is Part D: organize the existing human observations and resolve
taxonomy boundaries. The current review API still reports 85 prescribed initial
reviews and three candidate modes, with no finalized modes or binary decisions.
All 25 depth suggestions are resolved. The final uniform batch remains undrawn.

See [taxonomy_followups.md](taxonomy_followups.md) for a short pending decision
batch and additional evidence-backed follow-ups. These questions do not create
new categories or labels. Original observations and the earlier human-approved
exceptions remain authoritative. The assignment's 5–8-mode requirement is still
unmet; do not split or invent categories merely to reach that number.

## Specification revision: RESP-7 and formatting confirmations

The student replied “I approve all” to the three numbered decisions: add the
response-completion requirement and accept the displayed replies for final-069
and final-075. The approval is recorded as
`hw4-response-and-format-clarification-03` in
[review_clarifications.json](../state/review_clarifications.json).

### Response-completion requirement

Added to [SPEC.md](../../SPEC.md):

> **RESP-7.** Every user turn must receive an answer, clarification, refusal,
> escalation, or clear failure notice—not silence or only a promise to act.

Motivating human-confirmed observations:

- Incomplete final-229: trace `44862c87ab91d6a519e7d7f20a42cb3c`, observation
  `accepted-hw4-depth-20-44862c87ab91d6a519e7d7f20a42cb3c` — “Yeah, this is a
  problem. Nothing showed up.”
- Incomplete final-238: trace `23d8c02949dfda9a3f1fc01352c861a6`, observation
  `accepted-hw4-depth-21-23d8c02949dfda9a3f1fc01352c861a6` — “Correct. No
  response was delivered.”
- Incomplete final-242: trace `f8b252caf57871e2070d567411e0fe2e`, observation
  `accepted-hw4-depth-22-f8b252caf57871e2070d567411e0fe2e` — “Correct. No
  response was delivered.”

The existing `missing_usable_final_response` candidate now references RESP-7,
with its definition and boundary aligned to the approved response types.
Its earlier definition and specification-gap status remain in revision history.
A clear failure notice satisfies this communication requirement without proving
successful task execution. Keep provider/quota causes separate from model
behavior. The historical traces predate RESP-7 and do not establish that the
agent disregarded this explicit instruction when recorded.

This is a specification/taxonomy update only: the prompt and running agent are
unchanged. The mode remains a candidate; example confirmation and the proposed
evaluator choice are not finalized by this approval.

### Formatting-only concerns resolved for the displayed replies

- **final-069**, trace `70fa06d346c4eb870abbe05e863cc15d`: original note
  `545cbce4-0c4e-4ded-ab02-bc5212fca231` said the formatting was wrong but the
  answer looked correct. The student now accepts the displayed refund-timing
  answer. Follow-up: `human-confirmation-format-final-069-20260925`.
- **final-075**, trace `0e69d44e50e93a6e87166ffabb5849b4`: original note
  `6eb1a9ff-a943-4257-93df-266d584763c9` said it was not human-readable. The
  student now accepts the displayed escalation-response-time answer. Follow-up:
  `human-confirmation-format-final-075-20260925`.

These are specific formatting confirmations, not final all-mode judgments or a
diagnosis of the original interface issue. Original notes are unchanged. The
separate final-215 formatting concern, final-220 arithmetic concern, and other
follow-ups remain pending; “all” referred only to the three presented decisions.
Raindrop remains deferred. No live model call or Langfuse score write was made.

### Follow-up approval: final-220 arithmetic and final-194 requested details

The student replied “approve both” to two narrowly scoped boundary checks.
Provenance is saved as `hw4-date-and-requested-detail-clarification-04` in
[review_clarifications.json](../state/review_clarifications.json).

- **final-220**, trace `4718c6889715fb5f8d4e7f81a1f1e814`: remove only the
  wrong-date-math objection from the current interpretation. June 24 to July 1
  is seven elapsed days, and the unchanged eligibility oracle includes day
  seven. Original note `93595629-fbf3-42c7-a280-22492eeebe67` remains intact;
  follow-up `human-confirmation-date-final-220-20260925` records the approval.
  Separate formatting, clarity/verbosity and technical-detail concerns remain
  open. This supersedes the earlier pending arithmetic status above.
- **final-194**, trace `9f089e0afe52e109302663a3fad425c8`: the user explicitly
  requested product ID 2, its $9 price, and unambiguous identification. The
  student accepts those requested details. Original note
  `662e146b-591b-4f57-a6d8-d16d30b6a8eb` remains intact; follow-up
  `human-confirmation-requested-details-final-194-20260925` records the approval.
  Any separate verbosity/clarity concern remains open; this does not approve
  every additional detail in the reply.

Following the course review workflow, these later decisions are appended rather
than replacing the original open codes. No whole trace was declared error-free,
no final binary label was assigned, and neither SPEC nor taxonomy definitions
changed. Raindrop remains deferred. No live model or Langfuse score write was
used; the original date-boundary verification was offline.

### Follow-up approval: requested flags in final-210 and final-220

The student approved mentioning `refund_eligible` in both answers because the
support requests explicitly ask to reconcile that flag. This decision is
recorded as `hw4-requested-flag-clarification-05` in
[review_clarifications.json](../state/review_clarifications.json).

- **final-210**, trace `57fd75858461ca06585e648ed7d5a119`: original annotation
  `9daf60e2-48c3-4932-b9ac-be6014f3fa31` is preserved; follow-up
  `human-confirmation-requested-flag-final-210-20260925` records the approval.
- **final-220**, trace `4718c6889715fb5f8d4e7f81a1f1e814`: original annotation
  `93595629-fbf3-42c7-a280-22492eeebe67` is preserved; follow-up
  `human-confirmation-requested-flag-final-220-20260925` records the approval.

Following the course review workflow, only the requested-flag objection is
resolved. Separate formatting, clarity and verbosity concerns remain open. The
decision does not approve every technical detail or policy explanation, declare
either whole trace error-free, or resolve final-215. No taxonomy definition,
specification, suggestion disposition, sample selection or binary label changed.
No live model or Langfuse score write was used. Raindrop remains deferred.

### Consolidated taxonomy review packet — awaiting human review

Prepared [one review batch](taxonomy_review_packet.md), with a matching
[evidence snapshot](../state/taxonomy_review_packet.json), from 19 already-reviewed
traces. This is proposed taxonomy evidence, not new labels or new sample coverage.
The packet preserves original notes, current depth decisions and prior decision
history, including clarified praise/rejection meanings and the separate final-242
price concern.

- Price and missing-response drafts each have three proposed positive examples
  and three proposed close negatives drawn from explicit depth-review decisions.
- The four original excess-detail concerns (final-108, final-146, final-182 and
  final-195) are shown with complete final replies for re-review under the approved
  definition. All nine excess-detail depth suggestions were rejected; these four
  original concerns are not automatically confirmed positives.
- The packet proposes an LLM judge for the full semantic RESP-7 definition;
  empty-output code checks cover only part of that boundary. The saved unapproved
  code proposal remains unchanged pending the student's choice.

No mode was finalized, no evaluator was implemented, and no runtime, annotation,
suggestion, sample or binary label was changed. Progress remains 85/100 reviewed,
3 candidate modes, 0 final modes and 0 final binary decisions. The 5–8-mode
requirement still needs genuinely distinct human-supported evidence; categories
will not be manufactured to satisfy it. Raindrop remains required but deferred.

Verification: offline JSON integrity checks passed for 19 unique reviewed trace
IDs, pending decisions and exact response anchors; `git diff --check` passed.
A read-only local review-API check confirmed annotations, patterns, suggestions,
sample manifest, labels and state revision were unchanged. No live model call
or remote Langfuse score write was made.

## Completion-session checkpoint — 2026-09-25 06:26 UTC

The student asked to finish HW4 now. The local review API still reports 85
reviewed sampled traces, 87 inspected traces including context, three candidate
modes, zero final modes and zero final binary decisions. No pending decision
was inferred from this request. Taxonomy packet confirmations and whether to
reverse the earlier Workshop deferral have been requested from the student.
Until answered, the earlier deferral remains in force.

### Verified current sample composition

Counts below are computed from the distinct trace IDs in the sample manifest
joined to the loaded trace metadata. They describe the current incomplete sample,
not failure rates. The 30-trace product-dimension batch is balanced by user role.

| Batch | Selected | Reviewed | Shopper | Merchant | Support |
|---|---:|---:|---:|---:|---:|
| uniform_initial | 15 | 15 | 11 | 4 | 0 |
| cluster | 15 | 15 | 10 | 1 | 4 |
| dimension | 30 | 30 | 10 | 10 | 10 |
| depth | 25 | 25 | 13 | 7 | 5 |
| uniform_final | 0 | 0 | 0 | 0 | 0 |
| Total | 85 | 85 | 44 | 22 | 19 |

No trace ID is counted twice across batches. All 25 depth suggestions are
resolved (8 accepted, 17 rejected); these are not final per-mode label counts.
The final-15 new-mode count is **not yet measured**, not zero. The interface is
reading the Langfuse snapshot loaded 2026-09-18T08:19:54.101797+00:00; this check
read the local review API, not a refreshed remote trace collection.

### Verification performed in this completion session

- The explicitly offline full Python suite completed with **161 passed,
  13 skipped, 21 xfailed and 9 xpassed**. Expected failures still represent
  unfinished homework placeholders; unexpected passes are reported as observed,
  not silently treated as a clean all-homework completion signal.
- An initial sandboxed run had one failure because the operating environment
  denied binding a loopback socket in the HTTP-route test. The unchanged suite
  was rerun with local socket permission and had no failures.
- **14 Node Markdown-renderer tests passed**; `git diff --check` passed.
- These checks used no live model and wrote no real Langfuse score. They do not
  replace human reviews, live score read-back, Workshop evidence or the video.

### Remaining requirements, not optional sign-offs

1. Confirm the proposed taxonomy evidence and obtain enough genuine human
   observations for 5–8 distinct final modes; the existing packet has three
   drafts, not five completed categories.
2. Complete the required Workshop review of 5–10 runs if the student elects to
   do it now; otherwise leave Part C explicitly pending. Prepare observed run
   IDs and notes only after those runs are actually inspected.
3. Repeat depth search after definition revision and compare the stable taxonomy
   with AgentDebug. Review the final 15 uniform traces and record new-mode
   discovery; collect another batch if several consequential new modes appear.
4. Record present/absent decisions for every final mode on every reviewed trace,
   synchronize accepted judgments, verify actual Langfuse score read-back and
   compute sample fractions from those labels. A first-failure note is not a
   substitute for the full per-mode matrix.
5. Finish the reports and commit the reviewed submission files; the student
   makes the continuous screen recording of no more than five minutes. No
   commit, submission, recording or completed-Workshop claim was made here.

## A/B/C confirmed; Workshop explicitly deferred

The student replied “Defer Raindrop workshop” and “confirm A, b and C”.
Approval `hw4-taxonomy-packet-confirmation-06` is saved in
[review_clarifications.json](../state/review_clarifications.json), and the
[consolidated packet](taxonomy_review_packet.md) records the outcome while
retaining the original proposed evidence and review questions.

| Final individual mode | Confirmed positives | Confirmed close negatives | Likely evaluator |
|---|---:|---:|---|
| unsolicited_status_price | 3 | 3 | LLM judge |
| answer_obscured_by_excess_detail | 4 | 3 | LLM judge |
| missing_usable_final_response | 3 | 3 | LLM judge |

All four B examples (final-108, final-146, final-182 and final-195) are included
in the student's group confirmation. No new detailed rationale is attributed
to the student; original notes and the packet's countervailing context remain
inspectable. C's former, unapproved code-check proposal is replaced by the
approved likely LLM judge for the full semantic RESP-7 boundary. Empty-output
code checks remain a possible retrieval aid, not a validated full evaluator.
The prior patterns are preserved in revision history. No evaluator was built.

Read-back from the local review API verified all three modes as final. The
overall taxonomy is not complete: the assignment requires 5–8 final modes.
The manifest still has 85 reviewed traces and the final 15 have not been drawn.
There are zero final matrix labels, so the app now shows 255 missing decisions
for the three current modes across those 85 traces. Example confirmation is
not blanket approval of other mode/trace pairs. No Langfuse score was written.
Original annotations, suggestions, sample selections and label files are
unchanged. No live model or Workshop run was performed.

Five unresolved human-note cases (final-077, final-120, final-177, final-199 and
final-215) were inspected read-only. The [next two checks](remaining_observation_review.md)
distinguish the specific cause-explanation concern in final-177 from B and
revisit the still-open formatting concern in final-215. They are not two new
confirmed categories. The complete normalized evidence and pending questions
are saved in `analysis/state/post_abc_observation_review.json`.

## Two additional candidate categories — not finalized

At the student's request to create two categories from the remaining examples,
the existing final-177 and final-215 observations were organized into two draft
modes. Request `hw4-two-additional-candidate-request-07` is preserved in
[review_clarifications.json](../state/review_clarifications.json). Full proposed
definitions, requirement wording, boundaries and evidence gaps are saved in
[additional_mode_candidates.json](../state/additional_mode_candidates.json)
and displayed as candidates in the review interface.

| Candidate | Origin | Proposed distinction | Evidence gap |
|---|---|---|---|
| unsupported_cause_speculation | final-177, annotation `2e32c120-a04c-4e33-994b-0ec362865ecd` | Naming an unsupported cause can be wrong even in a short reply; this is not simply verbosity. | The reply says “likely”. A rule covering hedged hypotheses requires explicit clarification, plus confirmed examples and close negatives. |
| unreadable_response_format | final-215, observation `accepted-hw4-depth-15-5bcc02aa2ef576b0873a738c7731feb7` and clarification `hw4-depth-boundary-clarification-02` | Presentation can impede reading even when the information is relevant. | A defect in the intended rendered reply has not been established; valid Markdown displayed as raw text is a viewer issue, not automatically an agent failure. |

These are **three final modes plus two candidates**, not five final modes.
Each new draft has one originating concern and zero confirmed positive/negative
memberships under its new definition. No examples were invented or silently
reclassified. Each final mode still needs at least three confirmed positives and
three close negatives when available. The proposed requirement clarifications
are not approved SPEC revisions. If further review does not support a draft,
revise, merge or retire it rather than keeping it merely to reach five modes.

Verification: the local review API saved/read back both candidates and preserved
A/B/C exactly, along with all original annotations, suggestions, samples and
labels. The reviewed count remains 85, with no new final labels or Langfuse
scores. No live model was used. Raindrop remains deferred. This completes the
requested draft grouping, not Homework 4 or its evidence requirements.

## Final uniform batch unlocked and selected

The custom review tool had incorrectly required 5–8 finalized modes before
selecting the last 15 traces. HW4 Part B instead says to do this after drafting
the taxonomy. The sampling gate now requires all first 85 sampled traces to be
reviewed and an active draft taxonomy (candidate or final modes). This corrects
the custom tool's sequencing; final-mode evidence requirements, human signoff
and the assignment's 5–8 final-mode completion requirement are unchanged.

The tool was restarted on its existing loopback port with the fix. It reloaded
311 distinct traces across 294 sessions from live Langfuse at
2026-09-25T06:50:22.934755+00:00. Read-back verified all saved notes, modes,
suggestion decisions, labels and the earlier sample manifest survived unchanged.

The final batch selected 15 traces uniformly without replacement from 224
eligible, previously unreviewed and unsampled IDs using seed 20260918. The
manifest records the five mode definitions/revisions/statuses at selection:
three final modes and two candidates. This baseline supports the later
new-mode assessment without falsely treating the candidates as finalized.

Current coverage: **100 distinct traces selected; 85 reviewed; final batch
0/15 reviewed.** No newly selected trace was automatically reviewed or labeled.
The original 85 selections and all existing judgments are preserved. The count
of new consequential modes in the final batch is still unmeasured, not zero.
Selection and verification details are in
[final_batch_unlock.json](../state/final_batch_unlock.json).

Verification: eight new regression tests passed; 14 Node Markdown tests passed;
the explicitly offline full suite reported 169 passed, 13 skipped, 21 xfailed
and 9 xpassed. `git diff --check` passed. The running HTML serves the corrected
sampling instructions, and live API read-back confirms 15 final-batch selections.
Only trace reads used live Langfuse; no live model or Langfuse score write was
used. Raindrop remains deferred and HW4 is not yet complete.

Next human action: refresh the review page, then open **Progress → Final uniform
→ Open batch**. Review each conversation in context, record the first failure
or “no failure observed”, and note any genuinely new issue. Keep the two draft
categories provisional until their definitions and evidence are confirmed.

## Final uniform review completed; requirement decision pending

After the student's “done”, local API read-back verified **100 distinct sampled
traces reviewed**, including all 15 final uniform selections. The sample has
55 shopper, 24 merchant and 21 support traces. The prescribed coverage is
15 initial uniform, 15 cluster, 30 product-dimension, 25 depth and 15 final
uniform, with no trace counted in two batches. Two additional context traces
were inspected but are not counted toward the 100.

The final batch contains **10 first-failure concern notes and five explicit
“no failure observed” notes**. These describe human open coding, not ten
validated specification violations or a completed per-mode labeling pass.
Stable IDs, original notes, supporting session evidence and proposed groupings
are saved in [final_batch_review.json](../state/final_batch_review.json).

| Human observation | Final scenarios | Interpretation pending structured labeling |
| --- | --- | --- |
| Remove raw policy identifiers | 085, 092, 115, 138, 149, 249 | Six explicit objections; existing RESP-1 requires the identifiers, so a product-requirement revision is needed before treating their presence as failure. |
| Remove raw field syntax | 136 | The reply contains `shipped_at: none`; the note says `shipped_at: null`. Preserve the note and assess the raw-field concern, without counting its ambiguous policy sentence as a seventh explicit policy-identifier objection. |
| Unrequested prices | 020, 231 | Repeated price concern. 020 asks for status and dates; 231 replaces an identification request, so confirm applicability of the existing status-only boundary before assigning that mode. |
| No response | 230 | Repeated missing-response concern. Only a user message is captured; historical diagnostics report a 429 credit-balance error, not a current outage or an authorization decision. |
| No failure observed | 043, 055, 168, 202, 239 | Initial human review complete; do not infer every final mode is absent. |

Other details in the original notes remain open: 020 objects to “not recorded”
wording, although the order is `placed` with null shipping/delivery dates;
115 mentions excess information; 138 asks for a clearer next step. These do
not automatically create additional categories or overwrite existing boundaries.

The proposed grouping `unsolicited_internal_policy_identifiers` would concern
raw identifiers in customer-facing answers, not whether policy claims are
grounded. Proposed requirement: explain the applicable policy in plain
language, preserve source identifiers in internal trace evidence, and omit raw
identifiers from customer-facing answers unless requested. This conflicts with
the current visible-citation requirement in RESP-1 and needs explicit approval,
with PURPOSE-1 kept consistent. The proposal is saved in the checkpoint;
SPEC.md and the app taxonomy have not been changed or approved by implication.

The number of previously unseen consequential modes is **pending**, not zero
and not the number of concern notes. Related policy/technical-detail concerns
already existed in earlier annotations, including final-074 and final-120.
A newly proposed grouping does not itself prove a newly discovered failure
type. Reconcile those prior notes, the approved requirements and the final
batch before deciding whether further breadth review is required.

Current taxonomy remains three final modes and two candidates. There are
zero final binary decisions and 300 missing decisions for the existing three
final modes across 100 reviewed traces. Completing the required 5–8 final-mode
taxonomy still requires supported examples and boundaries; its full labeling
matrix will then require 500–800 explicit judgments, not new trace samples.
Reports, score synchronization/read-back, stable-taxonomy comparison and the
student's recording remain incomplete. Raindrop Workshop remains deferred,
not waived; full HW4 completion is not claimed.

Verification for this checkpoint: read the saved local app state and recorded
session evidence from its existing Langfuse-backed snapshot. No new live-model
run, Langfuse score write, annotation edit, taxonomy change or SPEC change was
performed. The course review-loop skill was used to organize human notes while
leaving requirement changes and final judgments with the student.

## Specification revision RESP-1: plain-language policy explanations

The student's subsequent **“approve”** explicitly accepted the proposed change:
explain policies in plain English, keep policy identifiers in internal trace
records, and omit them from customer-facing answers unless requested. Approval
`hw4-policy-identifier-spec-approval-08` is saved in
[review_clarifications.json](../state/review_clarifications.json).

RESP-1 now requires every policy claim to remain grounded in retrieved policy
documents, with its supporting identifiers preserved in internal trace records.
Customer-facing answers must explain the applicable policy in plain language
without raw policy identifiers unless explicitly requested. Internal support
responses retain their existing citation requirement. PURPOSE-1 was updated
to be consistent. No policy terms, authorization rules, refund thresholds,
human-approval requirements or kill switches changed.

The motivating human annotations are:

| Scenario | Stable trace ID | Annotation ID |
| --- | --- | --- |
| final-085 | `11ac4cc470cd4b49685a37852cecb3a9` | `522105d8-7fa3-462d-b9fb-25d2093ef03c` |
| final-092 | `88471324f51094691b7a3f59294a32a2` | `54cd7f12-ceb7-4680-a832-ce199b1642ef` |
| final-115 | `69e1feb092880ca9171f3c59a71f8675` | `c09d940a-2235-45da-8b8b-28c444ca330a` |
| final-138 | `2e67ef48c576d7708def5ef317c0faeb` | `85e93424-5837-4b13-94ac-fec2a86745a8` |
| final-149 | `f7ba8b8eb26607d50ed27556e87d2aa8` | `46f88b87-f69f-490d-a5f1-cf20fc2ba9c2` |
| final-249 | `be8f58e4ac6c021e8c7983aa493a89f4` | `ece5d42a-c269-48d8-bbeb-cb722575655d` |

This is an approved **specification change**, not evidence that the old agent
violated the rule in force when those traces were recorded. The old RESP-1
required visible identifiers. Any later evaluation of those traces against the
new desired behavior must name the revised requirement and retain that context.
The initial notes, earlier decisions and taxonomy-at-selection snapshot remain
unchanged. The final-batch checkpoint now records the requirement approval
separately from its original assessments.

The proposed `unsolicited_internal_policy_identifiers` category now has an
approved requirement source, but its exact boundary, example memberships,
close negatives and evaluator choice are not finalized by this approval.
Reconcile the earlier verbosity-mode citation exception under the new
requirement before applying final labels. This approval does not establish the
final-batch discovery count or waive the evidence requirements for other drafts.

Runtime implementation is deliberately unchanged: `agent/agent.py` still has
the old instruction to cite policy IDs, and SPEC.md is not read at runtime.
Updating the prompt and verifying future behavior is a separate implementation
step, not a result claimed here. No judge, live-model run, score write, or
automatic positive/negative decision was made. Raindrop remains deferred.

Offline verification: the updated JSON records parse; approval origins match
the saved annotations; prior clarification history, annotations, taxonomy,
suggestions, samples, label files and agent code are preserved. `git diff
--check` passes. Following the course error-analysis skill, the approved
requirement is recorded without converting approval into blanket judgments.

## Consolidated remaining-category review prepared

At the student's request for the next step, prepared
[remaining_taxonomy_review_packet.md](remaining_taxonomy_review_packet.md) and
its [evidence mirror](../state/remaining_taxonomy_review_packet.json).
The packet uses nine already-reviewed traces, with their saved human notes,
requests, complete recorded turn activity, and replies. All are single-turn
sessions in the current snapshot; stable trace links were verified.

Group A proposes policy-ID positives 085, 092 and 149, contrasted with internal
support answers 069, 072 and 075. The revised RESP-1 retains citations in
internal support-facing answers. This distinction follows the intended
audience, not the caller role alone: an explicitly requested customer-facing
draft must be judged as customer-facing. Definition, boundary, three positive
memberships, three close negatives and likely evaluator await human confirmation.

The policy-ID grouping was saved in the app as a **candidate**, revision
`7819a20a0472578e`, with six originating human observations and no confirmed
example memberships or binary labels. The app now has three final modes and
three candidates. Earlier modes and all notes, suggestions, sample selections
and labels were verified unchanged by API read-back.

Group B rechecks formatting concerns on 215, 111 and 140 in the app's intended
formatted display. The human must identify a remaining presentation defect or
say none, separately from verbosity, policy IDs, raw fields and source-mode
Markdown. No positive formatting judgment is proposed automatically. The
proposed precise formatting requirement is not yet approved. The previously
resolved formatting concerns on 069/075 remain resolved, not reopened.

A read-only lexical search scanned assistant messages in all 311 traces / 294
sessions of the app's existing Langfuse-backed snapshot for the existing
cause-speculation definition. Four traces matched the search expression.
Final-177 was the only strong match to the originating concern; signals on
166, 201 and 205 were unrelated refusal/search-planning language under the
proposed definition. These exclusions are assistant retrieval screening, not
human rejected suggestions. The search can miss paraphrases and does not prove
no additional examples exist. No new supporting examples were human-confirmed;
the cause draft remains provisional rather than acquiring invented evidence.

The course error-analysis skill guided grouping from the student's notes and
kept proposed matches separate from final decisions. The nine-case packet is
the next human review point; it does not complete HW4 or establish the final
new-mode count. Raindrop remains deferred. No live model, new sample, initial
review, final-mode decision or Langfuse score write was used. Offline JSON and
whitespace checks passed; local API reads/writes were limited to the recorded
trace snapshot and the one draft category.

## Policy-ID category confirmed; first six binary scores verified

The student reviewed A1–A6, confirming policy-ID failures on 085, 092 and 149,
and acceptable internal-support citations on 069 and 072. The student corrected
the typed 079 to 075, then explicitly answered “yes” when asked whether 075's
citations were acceptable for internal support. No judgment was assigned to 079.
Approval `hw4-policy-id-example-confirmation-09` preserves the conversation and
the category-specific scope. The sixth judgment is not inferred from mere ID
presence or a generic initial “no failure observed” note.

`unsolicited_internal_policy_identifiers` is now final, revision
`34fa9458870043f5`, with three confirmed positives and three close negatives.
Its requirement is the approved revised RESP-1. Historical traces predate this
revision and followed the previous visible-citation instruction. The likely
LLM-judge type remains a contextual recommendation, not a separately approved,
implemented or validated HW5 evaluator. No other mode or example membership
was changed.

Exactly six explicit binary judgments were saved: 1 for 085/092/149, and 0 for
069/072/075. Their local mirror is
[unsolicited_internal_policy_identifiers.jsonl](../state/labels/unsolicited_internal_policy_identifiers.jsonl).
All six scores were acknowledged and then independently read back from live
Langfuse with matching score IDs, values and remote names. The audit is
[policy_id_confirmation.json](../state/policy_id_confirmation.json).
Initial open-code annotations and all earlier decisions remain preserved.

The first writes exposed a review-tool compatibility bug: Langfuse limits
score-configuration names to 35 characters, but this canonical mode name has
39. A stable prefix/hash alias now satisfies the remote limit without renaming
the local category or changing label IDs, score IDs, timestamps or judgments.
The alias is `unsolicited_internal_p_dcf998ce82c3`; it is recorded in each row's
`langfuse_score_name`, with the full canonical mode in the remote configuration
description and score comment. Pending records were retried after gracefully
restarting the existing review server. An initial immediate read-back preceded
ingestion visibility; the later read-back verified all six scores.

Verification: three new synthetic regressions cover the 35-character boundary,
stable distinct aliases, matching configuration/score names, identity retention
and reuse of an existing alias config. The first focused run had 35 passes and
one sandbox socket-bind permission failure. The full explicitly offline suite
with loopback permission then passed: **172 passed, 13 skipped, 21 xfailed,
9 xpassed**. JSON validation and `git diff --check` passed. Live Langfuse was used
only for source reads, the score configuration, the six authorized score writes
and read-back. No live model was called.

Current progress: 100 reviewed traces; four final modes; two candidates; six
binary decisions; 394 missing decisions across the current four modes. The
completed six-case check is not the full labeling pass or a valid whole-sample
failure fraction. Next human task: formatting checks on **215, 111 and 140**.
Raindrop remains deferred, the final discovery count remains unresolved, and
HW4 is not yet complete. The course error-analysis skill was followed by
recording only the student's six category-specific judgments, with no defaults
for unjudged trace/mode pairs.

## Formatting recheck resolved; unsupported draft retired

The student answered the group B check with “215 none. 111 none 140 none all
good.” Record `hw4-formatting-recheck-confirmation-10` preserves that explicit
decision as **no remaining formatting/layout issue in the three current
rendered displays**. It does not approve every aspect of those traces or erase
independent policy-ID, price, raw-field or excess-detail concerns.

Three follow-up observations were saved beside the traces, leaving every
original annotation unchanged. The originating 215 concern and the two
additional proposed formatting examples no longer supply positive evidence
for `unreadable_response_format`. That draft was retired from the active
taxonomy, revision `8e1aa5d0533b4abd`, with its old definition and observations
preserved in revision history. This does not prove what caused the earlier
display concerns or assert that formatting problems cannot exist elsewhere.
No proposed formatting requirement was added to SPEC.md.

The nine-case review packet is complete: A supplied the confirmed policy-ID
category; B did not support a separate formatting category. Current counts
remain 100 reviewed traces, four final modes, six saved binary judgments and
394 missing judgments across the four final modes. The cause-speculation draft
still has only one strong lexical match; the retired formatting draft cannot
be used to satisfy the assignment's 5–8-mode minimum.

The student's existing final-136 note about raw `shipped_at` output is a
remaining requirement/boundary question, not an automatically finalized fifth
mode. If pursued, establish whether unwanted database-field syntax is distinct
from policy identifiers and excess detail, approve a precise requirement, and
confirm supporting positives/close negatives. The formatting-only acceptance
of final-140 cannot be treated as acceptance or rejection of a different mode.

Verification: local API read-back confirms the three follow-ups and retirement;
original annotations, other modes, suggestions, samples and all six existing
scores/labels are unchanged. JSON and whitespace checks passed. No new binary
scores, live-model runs or Workshop activity were performed. The course review
skill required keeping unsupported candidates out of the final taxonomy and
preserving the human's judgments rather than manufacturing a fifth mode.


## Specification revision: RESP-8 plain-language data fields

The student answered “yes” to: “Should customer-facing answers translate raw
fields such as `shipped_at: none` into plain English, unless technical details
were requested?” Approval `hw4-raw-field-spec-approval-11` is recorded in
`analysis/state/review_clarifications.json`.

The motivating human annotation is `ef9e6fa8-7aa6-4409-a8bf-47dfdb4f012e`,
final-136 / trace `b5f4aa3df97a7b05064492c6280647e3`. Its wording mentions
`shipped_at: null`; the observed reply says `shipped_at: none`. The original
note is preserved verbatim. RESP-8 now requires plain-language rendering of
unrequested raw database fields and technical values, preserving recorded
meaning and uncertainty. This is a new specification requirement, not a claim
that historical traces violated a rule in force at execution. SPEC.md is not
runtime input; the running agent and its prompt remain unchanged.

The candidate `unrequested_technical_fields` is saved with originating human
provenance and revision `9c46b7f631d5d06e`. The exact binary definition,
its split from policy identifiers and excess detail, and all six proposed
example memberships await human review. A short raw-field answer need not be
verbose or poorly formatted. Translating relevant database facts is a distinct
proposed correction from suppressing source-policy identifiers; this distinction
is not finalized merely to meet the five-mode minimum.

The corrected search read assistant text across all 311 locally loaded traces
and 294 sessions; 55 traces matched snake_case or technical-value tokens.
These are retrieval hits, not failures. Three already-reviewed shopper cases
(022, 136, 140) are proposed positives. Three already-reviewed contrasts
(141 plain-language shipment wording, 042 explicitly requested exact product
record, 210 explicitly requested internal refund flag) are proposed close
negatives. Six pending suggestions and full normalized session evidence are
saved in [the raw-field review packet](raw_field_review_packet.md). No sample
selection or initial human review was overwritten. The prior formatting-only
acceptance of 140 stays intact.

The course error-analysis skill requires stopping for confirmation of the
proposed category boundaries and examples. Current final count remains four;
this draft and cause speculation are candidates, and formatting remains
retired. Existing binary decisions remain six, with 394 missing across the
four final modes. No new score, evaluator, live-model run or Raindrop activity
was authorized or performed. Raindrop remains deferred, not waived.

Verification: local review API read-back confirms six new pending suggestions
and the candidate draft. Original annotations, existing modes/suggestions,
sample manifest and six label records are identical to the pre-change state.
All six evidence anchors match recorded assistant text. Local JSON validation
and git whitespace checks passed. No live model was used.

## Raw-field example review and requested-detail boundary

The student's latest review confirms raw-field failures on final-022, 136 and
140, and absence of this category on 141. Those four suggestions are accepted
as human observations and confirmed candidate memberships. The candidate now
has three positive examples and one close negative, revision
`c76f2a0ef40a13a3`. It remains non-final.

The student separately asks to remove policy information from 141, improve
042's reviewability, and remove unnecessary policy/flag discussion from 210.
Each concern is saved verbatim with its interpretation limits. Final-042 asks
for the exact product record, so its new formatting concern is not silently
converted into a raw-field label. Its original exact-record acceptance and
the unrelated retired-formatting decisions are preserved.

Final-210's support request explicitly asks to reconcile `refund_eligible`
with the delivery date and 30-day policy. The student rejects it as a clean
counterexample. Save that rejection without turning it automatically into a
positive: RESP-8 currently allows explicitly requested technical details, and
RESP-1 retains internal-support policy citations. Clarify whether the objection
is repetitive/excessive presentation or a desired change to the exception.
No requirement or earlier internal-support judgment is overwritten.

Clarification `hw4-raw-field-example-review-12` and the updated raw-field packet
preserve the exact statements and current status. Four final categories and
six existing binary scores remain; these four candidate memberships are not
yet final-mode scores. Local API read-back verifies seven added observations,
four accepted suggestions, one rejected suggestion and one unresolved suggestion.
All original annotations, unrelated modes/suggestions, samples and labels are
unchanged. No live model, runtime edit or Raindrop activity was performed.
The course review skill requires pausing finalization for this boundary decision,
not treating an unclear response as a pass or manufacturing missing negatives.

## RESP-8 audience clarification: internal staff only

The student clarified: “I want shorted answer... and I dont think the raw flags
should be delivred for merchant or User... only internal staff should get the
flags”. Record `hw4-raw-field-audience-clarification-13` preserves that statement
and the before/after requirement. RESP-8 now reserves raw fields/flags for
internal staff-facing answers; shoppers and merchants get plain-language data,
even when technical details are requested. The intended audience controls a
staff-authored customer-ready draft. Relevant data meaning and uncertainty must
be preserved. This is a SPEC-only change; runtime instructions are unchanged.
RESP-1's distinct policy-citation rule was not silently revised.

The raw-field candidate is renamed `raw_fields_to_external_audiences`,
revision `ebdcdad840ced256`. Its predecessor remains archived
with a supersession link, not counted as another failure mode. The three
confirmed shopper positives (022, 136, 140) and 141's raw-field absence are
retained. The clarification resolves 210 as raw-field absent for internal
support, while preserving the student's separate desire for a shorter answer.
That does not automatically mean the existing excess-detail definition is
satisfied, nor does it make the whole trace pass. The original rejected
suggestion remains historical evidence; a new follow-up explains the resolution.

The repeated search read all 311 traces in 294 local snapshot sessions after
the definition revision. There were 55 lexical hits, 26 with shopper/merchant
caller roles. These are retrieval signals, not labels; plain-English None and
ordinary reference expressions may be false positives, and staff-facing
versus externally drafted content still needs context. Full match provenance
is in the updated raw-field packet. No model was used or extra sample drawn.

Current candidate evidence: three confirmed positives, two confirmed close
negatives, and one remaining question on 042. Its support user requested an
exact product record, but the student's latest explicit note concerns formatting.
Confirm category-specific raw-field absence without treating that formatting
objection as withdrawn. The course review skill keeps the candidate provisional
until that confirmation, with no invented third close negative. Four modes
remain final; the six existing binary scores are unchanged.

Local API read-back verified preserved original annotations, prior suggestion
decisions, other categories, all labels and the sample manifest. One follow-up
was added; only 042's pending suggestion was moved to the renamed candidate,
with its previous mode reference saved. Raindrop remains deferred.

## Fifth category finalized; raw-field scores pending synchronization

The student answered “yes acceptable” to the explicit final-042 question:
its internal-staff-requested product fields are acceptable while the formatting
complaint remains separate. Confirmation `hw4-raw-field-final-confirmation-14`
completes the six category-specific examples: positives 022, 136, 140;
close negatives 141, 210, 042. The mode `raw_fields_to_external_audiences`
is now final, revision `5d6505da5cbc39ac`. It has a human origin,
approved RESP-8 audience boundary, distinct correction from policy-ID omission,
and likely contextual LLM-judge evaluator type. No judge was built or validated.

The course error-analysis skill was followed by preserving all original
observations and saving only the six explicit judgments, with no defaults for
unjudged pairs. The final-042 readability concern, 141 policy-information concern,
210 shorter-answer concern and 140 formatting acceptance remain separate.
There are now five final categories; no fabricated fifth mode or extra category
from the renamed predecessor is counted.

Local-app access was rejected by the tool approval service because its own
authentication failed. This is not evidence that Langfuse or its credentials
failed. No HTTP workaround or retry was used. Existing ReviewState suggestion
and finalization guards were executed in memory against saved trace evidence;
they passed. Authorized local file edits then persisted the accepted observation,
taxonomy revision and six pending JSONL labels with deterministic score IDs.
Remote synchronization and read-back were not attempted and remain pending.

Current local progress: 100 reviewed sample traces, five final modes, twelve
explicit binary decisions out of 500, and 488 missing judgments. The earlier
six policy-ID scores retain their verified remote status. The new six scores
are pending, not remotely verified. These partial labels cannot support
whole-sample category fractions or a claim that HW4 is complete.

Next: restore authorized local-service access and synchronize these six
judgments; complete the stable-taxonomy comparison and final-batch discovery
assessment, then finish the all-mode labeling pass and reports. Raindrop
remains deferred, not waived; the student's recording remains their task.
No live model or runtime behavior change was performed.

Offline post-write checks passed: valid JSON, current mode hashes, matching
positive/negative label sets, stable score IDs, unique trace/mode decisions,
100 reviewed sample IDs and 12 valid labels. Original annotations, other modes,
unrelated suggestions, the sample manifest and all six prior policy-ID label
records are unchanged. Only one accepted observation was added. Git whitespace
checks passed. The six raw-field scores remain pending; no remote read-back
or live-model verification is claimed.

## Authorized synchronization retry remains blocked

The student approved retrying the six pending raw-field score writes. The
read-only local-state check was again blocked by approval-service authentication
before the command executed. No sync POST, Langfuse write or remote read-back
occurred. The six local label records, deterministic score IDs and timestamps
were re-read offline and are unchanged; all remain pending. The retry audit is
`analysis/state/raw_field_sync_retry.json`. The existing user authorization is
recorded; another approval-only loop will not restore authentication. No access
workaround, credential change, model call or Raindrop action was attempted.

## Authorized raw-field synchronization retry completed

The student explicitly re-approved uploading the same six saved trace-linked
`raw_fields_to_external_audiences` judgments. Langfuse acknowledged all six
writes. Independent reads by stable score ID verified the expected trace ID,
score name and numeric value for each record: three failure-present values and
three failure-absent values. The local JSONL records now show `synced`; their
definitions, human judgments, evidence, score IDs and original timestamps are
unchanged. The retry audit and all six read-back results are preserved in
`analysis/state/raw_field_sync_retry.json`.

The full review server first attempted to reload the live trace collection but
Langfuse returned HTTP 422 before the server started. That source-loading issue
did not affect the six narrowly scoped score writes or score-ID read-backs.
No live model or Raindrop action was used. The homework remains incomplete:
there are still 488 missing trace-by-mode decisions, and the deferred Workshop,
stable-taxonomy/final-batch assessment, final reports and student recording
remain outstanding.

## Comparison with AgentDebug

The final Cartwheel taxonomy was compared with the published
[AgentErrorTaxonomy in AgentDebug](https://arxiv.org/abs/2509.25370). AgentDebug
organizes failures by the module in which a root cause appears: memory,
reflection, planning, action, or system. Its finer-grained types include
incomplete summaries, retrieval failures, progress or outcome
misinterpretation, constraint ignorance, inefficient planning,
planning-action disconnects, format and parameter errors, and several
system/tool limits.

The two taxonomies answer different questions. AgentDebug asks *where and why
the trajectory first went wrong*; the Cartwheel modes ask *which specific
user-facing product requirement the completed trace violates*. The nearest
relationships are:

| Cartwheel mode | Nearest AgentDebug concept | Important boundary |
| --- | --- | --- |
| `answer_obscured_by_excess_detail` | Memory over-simplification/incomplete summary or planning inefficiency | AgentDebug's summary error concerns lost information; this mode concerns irrelevant detail hiding an answer, regardless of the internal cause. |
| `missing_usable_final_response` | Action format error, system/tool execution error, or LLM limit | The Cartwheel mode is cause-neutral and requires the user-facing absence of an answer, clarification, refusal, escalation, or failure notice. |
| `unsolicited_status_price` | Planning constraint ignorance or planning-action disconnect | The Cartwheel rule is narrower: it concerns one unnecessary field in status-only answers. |
| `unsolicited_internal_policy_identifiers` | Planning constraint ignorance or planning-action disconnect | The decisive boundary is audience and whether the identifier was requested, not the agent's hidden module. |
| `raw_fields_to_external_audiences` | Planning constraint ignorance or planning-action disconnect | The decisive boundary is external versus internal audience and raw-field presentation. |

AgentDebug therefore identifies a possible omission in the Cartwheel analysis:
separate root-cause tags for retrieval, planning, tool, or environment failures.
No sixth final mode was added. The existing human observations support the five
product-facing rules above, but they do not support one stable, independently
defined upstream-cause mode with the required positives, close negatives, and
distinct product correction. In particular, provider or quota diagnostics in
traces associated with `missing_usable_final_response` remain context rather
than a silently inferred system-failure label.

The comparison also confirms that the Cartwheel names should remain specific.
Renaming the three audience/content-selection modes to a broad term such as
`constraint_ignorance` would collapse distinct fixes: omit an unrequested
price, translate an external raw field, and suppress an unrequested internal
policy identifier. The final names and boundaries are therefore unchanged.

## Explicit Workshop and video deferral

The student asked to proceed without Raindrop Workshop and without the video.
`analysis/report/workshop_notes.md` records that no Workshop runs were
inspected and no Workshop suggestion was treated as evidence. The recording
was not created. These are deliberate exclusions, not completed requirements.

## Final-batch stability assessment

The final uniform batch contained 15 traces: 10 with a saved first-failure note
and five with an explicit `no failure observed` note. After reconciling the
final taxonomy and its requirement revisions, **0 of the final 15 traces
produced a previously unseen consequential mode**.

The strongest apparent additions were not actually new to that batch.
Policy-identifier concerns had two related human observations before the final
batch, and the external raw-field concern had already appeared in an earlier
human note about exposing a flag to a consumer. The final batch sharpened those
boundaries and added evidence, but did not originate either concern. Remaining
notes mapped to already-known modes or did not mature into a supported final
mode. The taxonomy is therefore reasonably stable under the handout's final
batch check, and no additional stability batch is required.

This discovery count is separate from structured labeling: it does not turn
the 10 first-failure notes into mode-present labels or the five no-failure notes
into all-mode absences.

## Final results and handoff

The structured pass is complete: **100 distinct sampled traces × five final
modes = 500 current human-confirmed decisions**. The review app reports zero
missing or outdated judgments and zero pending synchronizations. Each mode has
100 current decisions at its final definition revision, and every current score
is acknowledged by Langfuse.

### Reviewed sample

| Selection batch | Reviewed traces |
| --- | ---: |
| Initial uniform sample | 15 |
| Cluster representatives | 15 |
| Product-dimension sample | 30 |
| Depth-search sample | 25 |
| Final uniform stability sample | 15 |
| **Total** | **100** |

The 100 trace IDs are distinct. Their role composition is 55 shopper, 24
merchant, and 21 support traces. Because clustering, dimension sampling, and
depth searches intentionally changed the sample composition, the results below
are **sample fractions**, not prevalence estimates.

### Per-mode counts and sample fractions

| Final failure mode | Present | Absent | Sample fraction present |
| --- | ---: | ---: | ---: |
| `unsolicited_status_price` | 6 | 94 | 6% |
| `answer_obscured_by_excess_detail` | 23 | 77 | 23% |
| `missing_usable_final_response` | 9 | 91 | 9% |
| `unsolicited_internal_policy_identifiers` | 28 | 72 | 28% |
| `raw_fields_to_external_audiences` | 8 | 92 | 8% |

A trace may contain more than one mode, so the present counts must not be added
and interpreted as a fraction of traces. The three modes with fewer than 15
failure-present examples—`unsolicited_status_price`,
`missing_usable_final_response`, and `raw_fields_to_external_audiences`—will
need targeted positive-label collection early in Homework 5 before an LLM
judge can meet the handout's class-balance guidance. All five modes already
have at least 30 absent labels.

### Stability and taxonomy revision

The final 15 uniformly sampled traces produced **0 previously unseen
consequential modes**. The taxonomy is therefore reasonably stable for this
assignment, and no additional stability batch is required.

One consequential revision split audience-specific technical leakage into two
different corrections. `unsolicited_internal_policy_identifiers` covers raw
internal policy IDs in customer-facing answers under revised RESP-1, while
`raw_fields_to_external_audiences` covers raw database fields or flags shown to
shoppers or merchants under revised RESP-8. They remain separate because
removing a source identifier and translating stored data into plain language
are different product changes. The original observations, intermediate names,
human confirmations, and rejected suggestions remain in the state history.

### Scope status

The interface, sampling, annotations, taxonomy, labels, specification
revisions, AgentDebug comparison, stability assessment, and written reports
are complete. Raindrop Workshop was not run and the video was not recorded at
the student's explicit request. Those two handout requirements are therefore
**deferred, not completed or waived**. Apart from those deliberate exclusions,
the HW4 repository work is ready for handoff.
