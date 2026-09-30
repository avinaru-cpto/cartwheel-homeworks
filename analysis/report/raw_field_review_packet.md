# Raw-field review: six category-specific checks

Status: finalized with three positive examples (022, 136, 140) and three close negatives (141, 210, 042). All six explicit binary judgments are saved, synchronized to Langfuse and independently read back by stable score ID.

## Latest human review

- 022, 136, 140: the student confirms the unrequested shipment field is a failure.
- 141: raw-field failure absent. Preserve the separate request to remove policy information; it is not a whole-trace pass.
- 042: the student explicitly confirmed “yes acceptable” for the raw fields in this internal-staff exact-record request. Raw-field failure absent; the separate readability/formatting concern remains.
- 210: the student clarified that internal staff may receive raw flags, but the answer should be shorter. Record raw-field absence for this internal-support example and retain the separate brevity concern. The earlier rejection remains in history; it is not a current raw-field-positive label.

The table and recorded answers below preserve the original proposals. All six memberships are now confirmed. The original 210 rejection and subsequent clarification remain in history; 042 is accepted. Previous formatting decisions and the six earlier policy-ID scores are unchanged. See clarification records 12, 13 and `hw4-raw-field-final-confirmation-14`.

RESP-8 now reserves raw fields/flags for internal staff-facing answers. Shopper- and merchant-facing answers must use plain language, even when technical details are requested. The running agent has not been changed; all these traces predate the new requirement.

Final category: `raw_fields_to_external_audiences`, revision `5d6505da5cbc39ac`. The earlier `unrequested_technical_fields` draft is archived as its predecessor, not an extra category.

An answer intended for a shopper or merchant includes a raw database field name or technical null/boolean flag instead of expressing that data only in plain language.

## Review together

The original six-case packet is retained below for context; do not repeat these six confirmed judgments. Complete evidence, current decisions and remote read-back results are saved in [the JSON packet](../state/raw_field_review_packet.json).

| Case | Trace | Proposed judgment for raw fields only | Reason |
| --- | --- | --- | --- |
| R1 | [final-022](http://localhost:3000/project/cartwheel-dev/traces/9faa1565e19d7a30a7c909373e4cb8f0) | Present | `shipped_at: none` in an ordinary shopper status answer. |
| R2 | [final-136](http://localhost:3000/project/cartwheel-dev/traces/b5f4aa3df97a7b05064492c6280647e3) | Present | Originating human objection: raw shipment field in cancellation guidance. |
| R3 | [final-140](http://localhost:3000/project/cartwheel-dev/traces/9d3928a872f9a36f0b7beb3f546271c6) | Present | Same raw-field wording; prior formatting acceptance is a separate judgment. |
| R4 | [final-141](http://localhost:3000/project/cartwheel-dev/traces/cebc9a86476fc3e12830e622dcbb981c) | Absent | Cancellation answer uses ordinary shipment wording; policy IDs are a separate category. |
| R5 | [final-042](http://localhost:3000/project/cartwheel-dev/traces/601f0c898f4cbbba3919f39b9a8ba993) | Absent | The user explicitly requested the exact product record, so JSON fields are in scope. |
| R6 | [final-210](http://localhost:3000/project/cartwheel-dev/traces/57fd75858461ca06585e648ed7d5a119) | Absent | Internal support explicitly requested reconciliation of the named refund_eligible flag. |

No example question remains in this packet. Final-042's formatting concern, final-140's accepted formatting, final-141's policy-information objection and final-210's brevity concern are preserved. “Absent” here never means every other category passes.

## Final boundary and split

Current audience boundary: Audience, not merely caller role or explicit request, controls this mode: shoppers and merchants receive plain-language data, while relevant raw fields/flags are allowed in internal staff-facing answers. A staff request for a customer/merchant-ready draft still follows the external-audience rule. A request for technical details does not override the external-audience rule. Exclude internal tool results, stored trace records, ordinary order/product reference numbers, dates and plain-English words such as 'none'. Adding a plain-English paraphrase does not excuse a raw-field parenthesis. Preserve recorded meaning and uncertainty (RESP-3); a missing timestamp alone does not prove an event never happened. Distinct from raw policy identifiers (RESP-1), excessive detail and formatting: translating a data field, removing a source identifier, shortening an answer and changing its layout are separate corrections. Internal fields being allowed does not make an entire internal response acceptable.

The following paragraph preserves the superseded request-based proposal for comparison; it is no longer the active rule.

Assess customer-facing assistant text, including a customer-ready draft, not internal tool results or trace data. Explicit requests for technical fields, exact records or JSON are exceptions; internal-support technical investigations are outside the customer-facing scope. Ordinary order/product numbers, dates and plain-English words such as 'none' are not automatically failures. Adding a plain-English paraphrase does not excuse an unrequested raw-field parenthesis. Preserve recorded meaning and uncertainty (RESP-3); do not infer that an event did not occur solely from a missing timestamp. Separate from policy identifiers (RESP-1), which identify policy sources rather than expose database fields; separate from excess detail, since even a brief clear answer may retain a raw field; separate from layout, since reformatting alone does not remove it. The proposed split and example membership require human confirmation.

A database-field fix translates relevant data; the policy-ID fix removes unrequested source identifiers while preserving policy explanations. Merely shortening or reformatting an answer does not necessarily fix either. This is a proposed distinct mode, not a manufactured fifth category. Likely evaluator: contextual LLM judge, not implemented or validated.

## Evidence

### R1: final-022

User (shopper): Please check order 1935 for my Classic Poetry Collection. What is its current status?

Recorded final answer:

> Order **1935** for your **Classic Poetry Collection** from **Paper Lantern Press** is currently **placed**.
>
> It has **not shipped yet** (`shipped_at: none`) and has **not been delivered**.

Stable trace: `9faa1565e19d7a30a7c909373e4cb8f0`.

### R2: final-136

User (shopper): Do not change it yet: can order 3416 currently be cancelled under Cartwheel's shipment cutoff?

Recorded final answer:

> Yes — order **3416** can currently be cancelled under Cartwheel’s shipment cutoff.
>
> - The order status is **placed**.
> - It has **not shipped** (`shipped_at: none`).
> - Cartwheel’s cancellation policy says an order can be cancelled at no cost **any time before the store ships it**; once shipped, it can’t be cancelled and would need to go through returns instead. **Policy: `cw-cancellations`**
>
> I did **not** cancel it. If you want me to cancel order 3416, just confirm and I can do that.

Stable trace: `b5f4aa3df97a7b05064492c6280647e3`.

### R3: final-140

User (shopper): Do not change it yet: can order 3856 currently be cancelled under Cartwheel's shipment cutoff?

Recorded final answer:

> Yes. Order **3856** can currently be cancelled under Cartwheel’s shipment cutoff.
>
> - Current order status: **placed**
> - Shipped yet? **No** (`shipped_at: None`)
> - Cartwheel cutoff: an order can be cancelled any time **before the store ships it**; once shipped, it can’t be cancelled and would need to be handled as a return after delivery (**cw-cancellations**).
>
> I have **not** cancelled it.

Stable trace: `9d3928a872f9a36f0b7beb3f546271c6`.

### R4: final-141

User (shopper): Do not change it yet: can order 2221 currently be cancelled under Cartwheel's shipment cutoff?

Recorded final answer:

> No — order **2221** cannot currently be cancelled under Cartwheel’s shipment cutoff.
>
> Reason: Cartwheel’s cancellation cutoff is **before the store ships the order**. Once an order has shipped, it can no longer be cancelled; the buyer should wait for delivery and request a return if applicable (**cw-cancellations**).
>
> Order **2221** is already marked **shipped** on **2026-06-29**, so I did **not** cancel or change anything.

Stable trace: `cebc9a86476fc3e12830e622dcbb981c`.

### R5: final-042

User (support): Look up Modern Mug at Blue Heron Ceramics; return the exact product record, please.

Recorded final answer:

> Exact product record:
>
> ```json
> {
>   "product_id": 30,
>   "store_id": 1,
>   "title": "Modern Mug",
>   "price_usd": 163.75
> }
> ```

Stable trace: `601f0c898f4cbbba3919f39b9a8ba993`.

### R6: final-210

User (support): Reconcile order 161's refund_eligible flag with its 2026-06-01 delivery date and the 30-day policy as of 2026-07-01.

Recorded final answer:

> Order 161’s `refund_eligible: True` is consistent with the 30-day return window as of **2026-07-01**, based on the records I found.
>
> Details:
>
> - **Order 161**
>   - Status: **delivered**
>   - Delivered date: **2026-06-01**
>   - Store: **Copperline Tools**
>   - `refund_eligible`: **True**
>
> - **Applicable policy**
>   - Cartwheel’s return policy says items can be returned **within 30 days of delivery**, and that the window counts from the **delivery date**, not the purchase date. Policy: **cw-returns**
>   - Copperline Tools has **no return-window override**, so the standard Cartwheel 30-day window applies.
>
> - **Date reconciliation**
>   - From **2026-06-01** to **2026-07-01** is exactly **30 calendar days**.
>   - Because the system flag is still `True`, Cartwheel is treating the cutoff as inclusive through the 30th day after delivery.
>   - So, as of **2026-07-01**, the order is still eligible under the standard 30-day window. It would be expected to become ineligible after that cutoff, assuming no other exception applies.
>
> In short: **No mismatch found.** The `refund_eligible` flag being `True` on **2026-07-01** aligns with the standard 30-day delivery-based return policy (**cw-returns**) and the absence of a store override.

Stable trace: `57fd75858461ca06585e648ed7d5a119`.

## Search and status

After the audience revision, the full 311-trace / 294-session snapshot was searched again. It returned 55 lexical hits, including 26 shopper/merchant-role hits. These are retrieval counts, not failure labels. See the repeated-search evidence in the JSON packet. No extra samples, model calls or scores were created.

Searched 311 recorded traces across 294 sessions in the local Langfuse snapshot loaded 2026-09-25T22:06:57.373462+00:00. The corrected lexical search returned 55 possible matches. Most require contextual exclusions; this is not a failure count. Selected three shopper field examples and three contrasting cases, all already in the reviewed sample. No new sample batch, model call or binary score was created. Four categories remain final; this candidate and cause speculation remain provisional. Raindrop remains deferred.
