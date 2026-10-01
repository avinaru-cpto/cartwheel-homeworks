# Homework 5: what it is and exactly what remains

This is the student-facing checklist for the official
[Homework 5 handout](../../homework/module-2/hw5.md). The handout is the source
of truth; this page translates it into the concrete Cartwheel work already in
this repository.

## The assignment in one minute

Homework 4 produced human labels for recurring agent failures. Homework 5 asks
whether an LLM can reproduce those human decisions reliably for **one** failure
mode.

The workflow is:

1. Choose one narrowly defined failure mode.
2. Collect at least 30 human Pass and 30 human Fail examples.
3. Lock the examples into training, development, and test sets.
4. Write an LLM-judge prompt using only training examples.
5. Run the judge on development examples, inspect every disagreement, and make
   at most two prompt revisions.
6. Freeze the chosen prompt and run it once on the untouched test set.
7. Report TPR, TNR, confidence intervals, and whether the judge is trustworthy
   enough for the intended use.
8. Commit the artifacts and record a video of no more than five minutes.

The point is not to prove that an LLM judge is perfect. The point is to measure
where it agrees and disagrees with a human, improve it without looking at the
test answers, and state honestly how much confidence the final evidence earns.

## Our selected judge

Mode: `unsolicited_internal_policy_identifiers`

Question: **Did the final answer expose a raw internal policy identifier to a
shopper or merchant who did not request it?**

- **Pass (1):** The failure is absent. External replies use plain language;
  explicitly requested identifiers are allowed; genuine internal-support
  replies may retain citations.
- **Fail (0):** The failure is present. An external-facing answer exposes an
  unrequested identifier such as `cw-cancellations`, `cw-returns`, or
  `store-cascade-audio-policy`.

This is more than a regular-expression check because the same identifier can
be correct in an internal support answer, incorrect in a customer answer, or
appropriate when the user explicitly requests the code. The judge must apply
the audience and request boundary.

## Current status

### Part A — choose the mode and collect labels: complete

- [x] Reused the HW4 labels instead of applying the reference patch.
- [x] Removed duplicate and close scenario variants.
- [x] Human-confirmed the final two Fail examples.
- [x] Saved 97 independent labels: **67 Pass / 30 Fail**.
- [x] Used the HW5 convention: **1 = Pass, 0 = Fail**.

### Part B — prepare inputs and split: complete

- [x] Saved 97 label-free judge inputs.
- [x] Included caller role, relevant policy context, conversation messages,
  tool calls, and tool results.
- [x] Kept human labels, review notes, and scenario metadata out of judge input.
- [x] Created the fixed seed-7 split once:

| Split | Pass | Fail | Total | Purpose |
| --- | ---: | ---: | ---: | --- |
| Training | 13 | 6 | 19 | Prompt examples only |
| Development | 27 | 12 | 39 | Prompt evaluation and revision |
| Test | 27 | 12 | 39 | One final held-out evaluation |

### Part C — write and refine the judge: complete

- [x] Drafted prompt v0 with Pass/Fail rules and structured JSON output.
- [x] Used four training-only examples: clear Pass, clear Fail, merchant Fail,
  and an internal-support boundary case.
- [x] Verified that none of the prompt examples are in development or test.
- [x] Approved and ran prompt v0 on the **39 development traces** using
  `gpt-4o-mini`.
- [x] Reviewed the single development disagreement.
- [x] Decided that the prompt was wrong and the human Fail label should remain
  unchanged.
- [x] Drafted prompt v1 with a mandatory final-reply identifier scan; the
  development disagreement was not added as a prompt example.
- [x] Approved and ran prompt v1 on the **39 development traces** using
  `gpt-4o-mini`.
- [x] Confirmed that v1 produced the same single false Pass and no new
  disagreements; no human labels changed.
- [x] Drafted prompt v2 as the second and final permitted revision.
- [x] Approved and ran prompt v2 on the **39 development traces** using
  `gpt-4o-mini`.
- [x] Reviewed all v2 disagreements: there were none.
- [x] Stopped after two revisions because v2 reached 39/39 development
  agreement and fixed the known false Pass without regressions.
- [x] Confirmed v2 as the final prompt for freezing.

There is **no required numerical passing score** in the handout. We select the
final prompt from development evidence and report the uncertainty honestly.

### Part D — freeze and test: complete

- [x] Chose prompt v2 using development results only.
- [x] Froze prompt v2 before opening the test results.
- [x] Approved and ran the judge once on the **39 held-out test traces** using
  the same `gpt-4o-mini` model.
- [x] Saved confusion counts, TPR, TNR, and 95% Wilson intervals.
- [x] Decided to use the judge for human-reviewed screening, not autonomous
  enforcement.

Final held-out result:

| Metric | Result | 95% Wilson interval |
| --- | ---: | ---: |
| TPR | 26/27 = 0.9630 | 0.8172–0.9934 |
| TNR | 11/12 = 0.9167 | 0.6461–0.9851 |

Confusion counts: TP 26, FN 1, TN 11, FP 1. Overall agreement was 37/39
(0.9487). The false Pass missed `cw-returns` in the final reply; the false Fail
incorrectly attributed earlier trace identifiers to a final reply containing
none. The frozen prompt was not revised after seeing these results.

The test predictions stay hidden until the final prompt is frozen. A weak test
result is reported; it is not used to tune another version.

### Part E — submit and record: complete except video

- [x] Commit and push the preparation artifacts.
- [x] Package the development predictions, critiques, final judge,
  test metrics, and final summary.
- [ ] Record one continuous video of no more than five minutes.

The video must show:

1. The selected failure mode and decision boundary.
2. One development disagreement and what you did about it.
3. Final test TPR, TNR, and confidence intervals.
4. A live recalculation from saved predictions.
5. Whether you would use the judge, and why.

## What you personally need to do

The coding work and required human evaluation decisions are complete. The only
remaining personal task is to record the final video. Use
`analysis/report/hw5_video_outline.md` as the speaking guide.

## Metrics in plain English

- **TPR:** Of the replies humans marked Pass, how often did the judge also say
  Pass? Low TPR means the judge falsely flags acceptable replies.
- **TNR:** Of the replies humans marked Fail, how often did the judge also say
  Fail? Low TNR means the judge misses the failure we built it to detect.
- **95% confidence interval:** The plausible range around each rate. With only
  12 Fail examples in development and 12 in test, the TNR interval will remain
  fairly wide even when the point estimate looks strong.

Overall accuracy alone is not sufficient: a judge that mostly says Pass can
look accurate while missing the rare failures.

## Required repository artifacts

| Artifact | Location | Status |
| --- | --- | --- |
| Official assignment | `homework/module-2/hw5.md` | Current with course upstream |
| Human labels and evidence | `analysis/state/hw5_labels/unsolicited_internal_policy_identifiers.jsonl` | Complete |
| Fixed inputs | `analysis/state/hw5_trace_inputs.json` | Complete; freeze at first run |
| Fixed split | `analysis/state/splits.json` | Complete; do not reshuffle |
| Judge runner | `analysis/run_judges.py` | Complete |
| Prompt v0 | `analysis/prompts/unsolicited_internal_policy_identifiers-v0.txt` | Evaluated on development |
| Prompt v1 | `analysis/prompts/unsolicited_internal_policy_identifiers-v1.txt` | Evaluated on development |
| Prompt v2 | `analysis/prompts/unsolicited_internal_policy_identifiers-v2.txt` | Frozen final version |
| Development judge records and metrics | `analysis/state/judges/`, `analysis/report/dev-*.json` | Complete for v0, v1, and v2 |
| Final test metrics | `analysis/report/test-*.json` | Complete |
| Final review summary | `analysis/report/hw5_final_report.html` | Complete |
| Video | Student recording | Pending |

## Not required

- Building judges for all five HW4 modes. Only one judge is required.
- Raindrop Workshop.
- Estimating production prevalence.
- Hitting a specific minimum TPR or TNR.
- Inspecting test predictions during prompt development.

Additional judges and prevalence estimation are optional extensions. They
should not delay completing the required one-judge workflow.
