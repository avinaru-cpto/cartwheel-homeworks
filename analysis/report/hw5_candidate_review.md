# HW5 candidate review: policy identifiers

Selected mode: `unsolicited_internal_policy_identifiers`

Decision rule:

- **Pass (1):** The failure is absent. A shopper/merchant reply omits raw
  internal policy identifiers unless the user explicitly asks for them; an
  internal support reply may retain identifiers.
- **Fail (0):** The failure is present. A shopper/merchant reply exposes a raw
  internal policy identifier that the user did not request.

HW5 currently has 67 independent Pass examples and 28 independent Fail
examples after removing duplicate/near-duplicate scenario runs. Two more
human-confirmed Fails are required before the fixed train/dev/test split.

## Candidate 1

- Trace: `8ca02cb34aa49e17e9e59f7489133fef`
- Scenario: `final-142`
- Audience: shopper
- User: “Do not change it yet: can order 2476 currently be cancelled under
  Cartwheel's shipment cutoff?”
- Final reply excerpt: “Cartwheel allows cancellation only before the store
  ships the order; once it has shipped, it can no longer be cancelled
  (**cw-cancellations**).”
- Proposed decision: **Fail (0)** because the shopper did not ask for the raw
  identifier `cw-cancellations`.

## Candidate 2

- Trace: `8a550cf05e7bde47d22523e440c98ca0`
- Scenario: `final-139`
- Audience: shopper
- User: “Do not change it yet: can order 3722 currently be cancelled under
  Cartwheel's shipment cutoff?”
- Final reply excerpt: “Cartwheel’s cancellation cutoff is shipment ... once
  shipped, it can no longer be cancelled ... (**cw-cancellations**).”
- Proposed decision: **Fail (0)** because the shopper did not ask for the raw
  identifier `cw-cancellations`.

Human checkpoint: review the two complete traces in the HW4 review interface
or source export, then explicitly confirm or correct the proposed decisions.
No HW5 labels have been written for these candidates yet.
