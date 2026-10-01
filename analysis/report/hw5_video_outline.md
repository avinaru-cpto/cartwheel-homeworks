# HW5 video outline — five minutes maximum

Use this as a speaking guide rather than reading every line.

## 0:00–0:45 — failure mode and boundary

- I built one LLM judge for `unsolicited_internal_policy_identifiers`.
- It returns Fail when a shopper- or merchant-facing final reply exposes a raw
  internal policy identifier that the user did not request.
- Internal-support citations, explicitly requested codes, and operational IDs
  such as order or ticket numbers remain Pass.
- I labeled 97 independent conversations: 67 Pass and 30 Fail.

## 0:45–1:20 — split and leakage protection

- I made one fixed 20/40/40 split: 19 training, 39 development, and 39 test.
- The prompt used four training-only examples.
- Development examples guided revisions; test examples stayed hidden until the
  final prompt was frozen.

## 1:20–2:20 — development disagreement

- Prompt v0 had TPR 100% and TNR 91.67%, with one false Pass.
- In trace `0646b764f649f3f87e62beeeb35b55af`, the merchant asked whether a
  refund would be denied, automatic, or queued.
- The final answer exposed `cw-refunds`, but the judge said no identifier was
  present. I confirmed the human Fail label.
- v1 added an inspection checklist but produced the same result.
- v2 shortened the prompt and required every critique to begin by copying
  candidate identifiers from the complete final assistant block.
- v2 reached 39/39 development agreement, so I froze it after the maximum two
  revisions.

## 2:20–3:30 — held-out test

- Recalculate from the saved confusion counts: TP 26, FN 1, TN 11, FP 1.
- TPR = 26 / (26 + 1) = 96.30%.
- TNR = 11 / (11 + 1) = 91.67%.
- The 95% Wilson intervals are 81.72%–99.34% for TPR and 64.61%–98.51% for
  TNR.
- Overall agreement is 37/39, or 94.87%.

## 3:30–4:25 — what failed

- The false Pass missed `cw-returns` in a merchant-facing final answer.
- The false Fail claimed `cw-returns` and `cw-cancellations` appeared in a
  shopper-facing final answer that contained neither.
- These are evidence-location failures: the decision boundary was clear, but
  the model did not always isolate the final reply reliably.

## 4:25–5:00 — use decision and learning

- I would use this judge for human-reviewed screening or prioritization.
- I would not use it as an autonomous enforcement gate.
- The main lesson is that structured critiques can still be confidently wrong,
  and a strong point estimate can hide wide uncertainty when the Fail sample is
  small.
- In production, I would test a hybrid design that deterministically extracts
  the final assistant reply before the LLM applies the contextual audience and
  request boundary.
