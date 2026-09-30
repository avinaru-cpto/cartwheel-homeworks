# HW4 depth-review batch

Status: complete; all 25 initial human reviews and suggestion decisions saved.

The student approved preparing this batch and subsequently completed it. The
review workspace had 85 selected traces at depth-batch completion, all with initial reviews. This
batch added 25 distinct trace IDs outside the earlier samples and all previously
reviewed context traces. The final 15 uniform traces have now been reviewed:
100 distinct selected traces, all 100 reviewed. Five modes are final locally;
cause speculation remains a candidate, and the unsupported formatting draft is
retired. RESP-8 is approved. `raw_fields_to_external_audiences` has three confirmed
positives (022, 136, 140) and three close negatives (141, 210, 042).
Its six binary judgments are saved locally, awaiting Langfuse synchronization
after an approval-service authentication block. No trace re-review is needed
for these six decisions. See
[raw_field_review_packet.md](raw_field_review_packet.md).
The policy-identifier category has three confirmed
positive examples, three close negatives and six verified Langfuse scores.
Both groups are complete in
[remaining_taxonomy_review_packet.md](remaining_taxonomy_review_packet.md).
Completing this batch does not finalize candidates or assign binary labels.

## Review procedure used

1. Refresh http://127.0.0.1:8021.
2. Open **Progress → Depth searches → Open batch**.
3. Read each trace in session context. Save your own first-failure observation,
   or “no failure observed,” before responding to the AI suggestion.
4. Accept the failure suggestion only if its definition applies; otherwise
   reject it and briefly explain the boundary. A possible close negative is
   deliberately included for comparison, not a claim that it is a failure.

All 25 suggestions are resolved: 8 accepted and 17 rejected. The student's
follow-up clarifications and original decision history are preserved; see
[review_summary.md](review_summary.md). A rejection is not an automatic final
negative label, and an accepted candidate suggestion is not a final binary
score. Neither selection nor inspection alone marks a trace reviewed.

## Composition and search evidence

| Draft category | Possible matches | Possible close negatives | Total |
| --- | ---: | ---: | ---: |
| Unrequested status prices | 5 | 5 | 10 |
| Answer obscured by excess detail | 4 | 5 | 9 |
| Missing usable final response | 3 | 3 | 6 |
| Total | 12 | 13 | 25 |

Roles: 13 shopper, 7 merchant, 5 support. These are retrieval groups, not measured
failure counts.

The search inspected all 311 distinct traces in the app's existing Langfuse
snapshot, excluded 62 previously reviewed IDs (60 formal samples plus two
context traces), and selected from 249 eligible records. It used prompt/price
patterns, final-answer length and topic neighbors, final-message presence, and
recorded execution diagnostics. Purposeful selection added role and boundary
contrasts; no model was called. The snapshot was loaded on 2026-09-18, so this
does not claim to be an inventory freshly fetched from Langfuse today.

See [depth_search_plan.json](../state/depth_search_plan.json) for each selected
stable ID, request role, retrieval signals, evidence anchor, and rationale.
The prescribed batch is recorded in
[sample_manifest.json](../state/sample_manifest.json); suggestion decisions are in
[suggestions.json](../state/suggestions.json).

## Boundaries to test

- A price may be appropriate when explicitly requested or necessary.
- Requested technical records are not failures merely for containing technical
  details. At the time of these traces, RESP-1 required visible policy citations.
  The approved revision now omits unrequested raw policy identifiers from
  customer-facing answers while retaining internal source evidence; preserve
  the historical judgments and assess the new category separately.
- A longer answer may be warranted by a support investigation or procedure.
- A refusal or clarifying question can be a usable final response.
- Recorded quota/provider errors are execution evidence, not proof of a
  model-behavior error or a current provider problem.
- Three scenarios have both incomplete and completed attempts in this batch.
  Use the stable trace ID, not just the scenario number. The two final-229
  requests are worded differently, so they are not an identical-prompt retry.

## Remaining completion checklist

- [x] Review this 25-trace depth batch and resolve its suggestions; preserve
  genuine rejected suggestions and their reasons.
- [ ] Inspect 5–10 fresh or replayed Cartwheel runs in Raindrop Workshop and
  record identifiers, hypotheses, uncertainty, and the student's decisions.
  **Deferred at the student's request; continue taxonomy work first.**
- [x] Confirm 5–8 evidence-backed final categories, with at least three positive
  traces per mode and three close negatives when available, originating human
  annotations, requirement sources, boundaries, and likely evaluator types.
  Current status: five final categories; one cause-speculation candidate;
  one retired formatting draft and one archived raw-field predecessor. Groups A
  and B are complete. The student reports
  no remaining formatting problem on 215, 111 or 140. Cause speculation has
  one strong lexical match and remains provisional. The finalized raw-field mode
  has three confirmed positives and three confirmed close negatives, including
  042's explicit acceptance separate from formatting. The former request-based
  candidate is an archived alias, not an additional mode. The five-mode minimum
  is met; do not add unsupported categories merely to increase the count.
- [ ] Document a taxonomy revision, repeat a search after the revision, and
  compare the stable taxonomy with AgentDebug. Do not add unsupported modes.
- [x] Draw the final 15 uniform traces after drafting the taxonomy.
- [x] Review the final 15 uniform traces: 10 human concern notes and five
  explicit “no failure observed” notes, verified from saved state.
- [ ] Resolve the final-batch requirement/boundary questions, record how many
  previously unseen consequential modes appear, and review more if needed.
  See [final_batch_review.json](../state/final_batch_review.json). Six notes
  explicitly object to policy identifiers. The RESP-1 change and six policy-ID
  example judgments are now confirmed. RESP-8 and all six raw-field examples
  are confirmed. The final-batch discovery count/assessment remains pending.
- [ ] Apply every final mode to every reviewed trace. At 100 traces and 5–8
  modes, that is 500–800 explicit binary judgments, not 500–800 new traces.
  Preserve matching Langfuse scores and local JSONL; verify score read-back.
  Twelve explicit decisions are saved: six policy-ID scores remotely verified,
  and six raw-field scores pending synchronization. Across five final modes,
  488 of 500 decisions remain missing; do not infer them.
- [ ] Complete the reports and sample counts, check the required files, and
  prepare the submission commit.
- [ ] The student records the continuous screen demonstration, at most 5 minutes.

Verification: batch creation preserved annotations, taxonomy, and labels.
Subsequent human reviews and decisions were saved; later clarifications retained
the original notes and decision history. The last two suggestion closures were
read back through the review API. No final binary labels or Langfuse scores were
created by those closures, and no live model was called for this batch.
