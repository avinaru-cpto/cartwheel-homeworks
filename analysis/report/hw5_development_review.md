# HW5 development review

Mode: `unsolicited_internal_policy_identifiers`

## Prompt v0

Judge: `unsolicited_internal_policy_identifiers-v0`

Model: `gpt-4o-mini`
Development class counts: 27 Pass / 12 Fail

| Metric | Result | 95% Wilson interval |
| --- | ---: | ---: |
| TPR | 27/27 = 1.0000 | 0.8754–1.0000 |
| TNR | 11/12 = 0.9167 | 0.6461–0.9851 |

Confusion counts: TP 27, FN 0, TN 11, FP 1. Overall agreement was 38/39
(0.9744).

### Reviewed disagreement

Trace `0646b764f649f3f87e62beeeb35b55af` was a false Pass: the human label was
Fail and the judge predicted Pass. The merchant asked whether a refund would be
denied, automatic, or queued. The final reply exposed `cw-refunds`, which the
merchant did not request. The judge critique incorrectly stated that no raw
identifier appeared.

Human checkpoint completed 2026-10-01: the student confirmed that the trace
remains **Fail**. The label was not changed.

### Revision decision

Prompt v1 keeps the criterion and all training-only examples unchanged. It adds
a mandatory sequence that makes the judge scan the entire final reply, quote
every candidate policy identifier, and then apply the audience/request
boundary. The reviewed development trace was not added as a few-shot example.

## Prompt v1

Prompt v1 produced the same development result as v0: TP 27, FN 0, TN 11, and
FP 1, for TPR 1.0000 and TNR 0.9167 with the same Wilson intervals. The same
trace was the only disagreement. Its critique again omitted `cw-refunds`, even
though v1 required a complete identifier scan. There were no new disagreements
and no human labels changed.

### Final revision decision

Prompt v2 is the second and final permitted revision. It shortens the rubric,
defines the final reply as the complete last `assistant:` block, and requires
the critique to begin by copying all candidate identifiers. The criterion and
training-only examples remain substantively unchanged, and no development or
test trace was added to the prompt.

## Prompt v2

Judge: `unsolicited_internal_policy_identifiers-v2`

Model: `gpt-4o-mini`

| Metric | Result | 95% Wilson interval |
| --- | ---: | ---: |
| TPR | 27/27 = 1.0000 | 0.8754–1.0000 |
| TNR | 12/12 = 1.0000 | 0.7575–1.0000 |

Confusion counts: TP 27, FN 0, TN 12, FP 0. Overall agreement was 39/39
(1.0000), with no disagreements.

The formerly missed trace was correctly classified as Fail. Its v2 critique
began `Candidates in final reply: cw-refunds` and correctly applied the merchant
audience and unrequested-code boundary. All 39 critiques followed the required
candidate-inventory format.

Development revision stops at v2 because this was the second and final allowed
revision, it resolved the known false Pass, and it introduced no development
regressions. Prompt v2 is the recommended version to freeze for the held-out
test. Perfect development agreement does not prove perfect generalization; the
Wilson intervals remain wide because development contains only 27 Pass and 12
Fail examples.
