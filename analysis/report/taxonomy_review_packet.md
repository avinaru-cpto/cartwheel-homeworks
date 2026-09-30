# HW4 — one-batch taxonomy review

Status: **A, B and C confirmed by the student and saved as three final modes.**
Approval: `hw4-taxonomy-packet-confirmation-06` in
[review_clarifications.json](../state/review_clarifications.json).
The student said: “Defer Raindrop workshop” and “confirm A, b and C”.
This confirms the listed positives and close negatives, including all four B
examples, and a likely LLM judge for each mode. The full labeling pass remains
pending. Raindrop remains deferred.

The text below preserves the packet **as presented before approval**. Its
“proposed”, “pending” and “candidate” wording is historical, superseded by this
confirmation; no new detailed rationale has been attributed to the student.
Prepared 2026-09-25 06:21:56 UTC from the saved Langfuse snapshot loaded
2026-09-18T08:19:54.101797+00:00.

You have reviewed **85 of the planned 100 traces**. All **25 depth suggestions are resolved** (8 accepted, 17 rejected); these are not final per-mode failure counts. There are still three candidate categories and no final binary labels. Raindrop remains deferred.

This packet organizes your existing decisions under the course's error-analysis workflow: you decide which examples fit; I preserve the evidence and boundaries. It adds no annotations, sample selections, final categories or labels. All 19 selected traces were already in your reviewed set. Traces with the same scenario number are distinguished by trace ID.

## One reply can cover this batch

- **A:** Confirm the three failure examples, three contrasting examples and a likely LLM judge, or name an exception. These reuse your explicit depth-review decisions.
- **B:** Read the four original replies below. Say which still fail because irrelevant detail makes the answer hard to find or understand, with a short reason. “None” is valid; do not choose three just to meet the homework minimum.
- **C:** Confirm the three incomplete/completed contrasts and a likely LLM judge for the full response requirement, or name an exception. This evaluator recommendation is a change from the saved, unapproved code-check proposal; no evaluator is being built now.

Suggested reply format: `A: confirm / changes; B: 108 …, 146 …, 182 …, 195 …; C: confirm / changes.`

A close negative means this particular failure is absent, not that the whole trace is perfect. Confirmation here concerns category evidence and evaluator planning; it does not authorize filling every mode-by-trace label.

## A — Unrequested prices in status-only answers

Definition: A status-only answer includes a price that the user did not request and that is not needed to answer the question.

Requirement: **RESP-6**, approved after these historical traces. Requested or necessary prices are excluded. A brief status answer can fail this rule without being confusing or verbose.

### Proposed failure examples — already accepted during depth review

| Trace | Evidence in this category | Saved human decision |
|---|---|---|
| [final-013](http://localhost:3000/project/cartwheel-dev/traces/a9499256610ffd92842699e742670e3e) | Status request; reply includes $23.50. You explicitly rejected the extra price. | Failure accepted — Shouldn't have the pricing there. |
| [final-014](http://localhost:3000/project/cartwheel-dev/traces/6f65ee6bb49301a524d3fe18fcbc3796) | Recorded status/dates request; reply includes $333.00. You explicitly rejected the extra price. | Failure accepted — You should not put the total of 333 on here. |
| [final-030](http://localhost:3000/project/cartwheel-dev/traces/a1797134c9f9c583f618d3faebf91758) | Brief status-summary request; reply includes $163.25. You explicitly rejected the extra price. | Failure accepted — Pricing should not be there. |

### Proposed close negatives — already rejected as failures

| Trace | Evidence in this category | Saved human decision |
|---|---|---|
| [final-232](http://localhost:3000/project/cartwheel-dev/traces/fdc9b6379302dc15c17d798c8942629e) | Status/dates answer omits price; your praise means failure absent for A. | Failure rejected — Is much better to read |
| [final-236](http://localhost:3000/project/cartwheel-dev/traces/b41fbdef0e06083dbe456aa076661299) | Status/dates answer omits price; your praise means failure absent for A. | Failure rejected — This is much better to read. |
| [final-062](http://localhost:3000/project/cartwheel-dev/traces/cf11613678bb1cf4a222c176c4feeb1d) | The user explicitly requests the product's price; price is appropriate. | Failure rejected — The user asked for the price, so we need to keep it. |

Likely evaluator: **LLM judge**, because price presence alone cannot tell whether the user requested it or whether it is necessary. Your saved decisions support this grouping; category/example/evaluator confirmation is still pending.

## B — The answer is obscured by excess detail

Definition: Irrelevant explanation makes the actual answer to the user's question difficult to find or understand.

Requirement: **RESP-5**, using your approved interpretation. Length alone, required policy citations, requested technical details, exact-record JSON and appropriate escalation are not automatic failures. A display-rendering issue must not be mistaken for a response-content failure.

All nine depth suggestions for this category were rejected. The four original concerns below therefore need re-review under the precise definition; they are not silently promoted to confirmed examples.

### final-108 — shopper

[Open trace](http://localhost:3000/project/cartwheel-dev/traces/f876e10fc7b07f1805983a7ef7c9c6e7); trace ID `f876e10fc7b07f1805983a7ef7c9c6e7`.

User request:

> Calculate the applicable return deadline for order 156, delivered 2026-04-25 by Northwind Books.

Your original note (preserved verbatim):

> Too verbose. Gives too much information and doesn't answer the customer's question clearly. The formatting is all wrong

Recorded final reply (complete):

> For order **156**, delivered on **2026-04-25** by **Northwind Books**:
>
> - Cartwheel’s default return window is **30 days from delivery**, not purchase date (**cw-returns**).
> - Northwind Books has a **45-day return window override**, and store overrides apply when they differ from the Cartwheel default (**cw-store-overrides**).
> - Calculation: **2026-04-25 + 45 days = 2026-06-09**
>
> **Applicable return deadline: 2026-06-09** — the return needed to be started by the end of that date.
>
> Since today is **2026-09-18**, that deadline has passed, and the order lookup shows order 156 is **not currently refund eligible**.

Review question: Does the policy explanation make the deadline hard to find, or is it useful support for the requested calculation? Required citations alone are not a failure. The final paragraph about current refund eligibility is distinct from the deadline calculation.

### final-146 — shopper

[Open trace](http://localhost:3000/project/cartwheel-dev/traces/549bbff44819c799c7efbf4fd338b997); trace ID `549bbff44819c799c7efbf4fd338b997`.

User request:

> Do not change it yet: can order 14 currently be cancelled under Cartwheel's shipment cutoff?

Your original note (preserved verbatim):

> Too long. It should just say it's ready for delivery, and because it's ready for delivery, I can't cancel it. You can do a return. That's it

Recorded final reply (complete):

> No — order 14 cannot currently be cancelled under Cartwheel’s shipment cutoff.
>
> I did **not** change or cancel anything. Order 14 is already marked **delivered**; it shipped on **2025-03-10** and was delivered on **2025-03-15**. Cartwheel’s cancellation policy says an order can be cancelled only **before the store ships it**; once it has shipped, it can no longer be cancelled and the buyer should use the return process instead if applicable (**cw-cancellations**).
>
> For this order, the system also shows it is **not refund eligible** at the moment.

Review question: The reply leads with “No.” Does any extra information still obscure the answer, or is your concern only length? The order record says delivered; the original note's “ready for delivery” wording is preserved as a note, not adopted as the order status.

### final-182 — support

[Open trace](http://localhost:3000/project/cartwheel-dev/traces/5555498a3839ebe716691feaff4090a7); trace ID `5555498a3839ebe716691feaff4090a7`.

User request:

> For order 8002, verify whether enough data exists to calculate a return deadline; escalate if the delivery timestamp is absent.

Your original note (preserved verbatim):

> Too verbose and doesn't really answer the question simply. It's only the last line, so it needs to be much clearer and simpler

Recorded final reply (complete):

> Order 8002 does **not** have enough data to calculate a return deadline.
>
> - Order status: **delivered**
> - Delivery timestamp: **absent** (`delivered_at = None`)
> - Return deadlines are calculated from the **delivery date**, not the purchase date, under Cartwheel’s return policy (**cw-returns**).
>
> Because the delivery timestamp is missing, I escalated this to a human support agent as requested.
>
> **Escalation ticket:** #161
> **Expected follow-up:** within 24 hours.

Review question: The first line answers whether enough data exists, and escalation was explicitly requested. Does the remaining detail obscure the answer? Your older “only the last line” note does not match the location of the answer in this saved reply.

### final-195 — support

[Open trace](http://localhost:3000/project/cartwheel-dev/traces/5c364ed5e487c833447d257b52528b9f); trace ID `5c364ed5e487c833447d257b52528b9f`.

User request:

> Compare Blue Heron products 1 and 2 without pretending the repeated title is unique.

Your original note (preserved verbatim):

> Overbose, and it doesn't clearly explain what it is actually doing here, so

Recorded final reply (complete):

> Here’s the comparison treating the repeated title as **not unique** and using the product IDs to distinguish the entries.
>
> | Field | Blue Heron product 1 | Blue Heron product 2 |
> |---|---:|---:|
> | Product ID | **1** | **2** |
> | Store ID | 1 | 1 |
> | Title | **Heavy-Duty Vase** | **Heavy-Duty Vase** |
> | Price | **$298.00** | **$9.00** |
>
> ### Key differences
>
> - They have the **same title**, so “Heavy-Duty Vase” is **not enough to identify the product**.
> - **Product ID 1** is much more expensive: **$298.00**.
> - **Product ID 2** is much cheaper: **$9.00**.
> - The price difference is **$289.00**.
> - Product 1 costs about **33.1×** as much as product 2.
> - Product 2 is about **97% cheaper** than product 1.
>
> ### Important note about the repeated title
>
> The catalog search also showed other products named **“Heavy-Duty Vase”** beyond IDs 1 and 2, including additional entries in the same store and another store. So any order, refund, or support request should refer to the **product ID**, not just the title.

Review question: IDs, repeated titles and prices help distinguish the products. Do the repeated price comparisons, ratio, percentage and catalog explanation make that comparison harder to understand?

### Proposed close negatives for B

| Trace | Evidence in this category | Saved human decision |
|---|---|---|
| [final-141](http://localhost:3000/project/cartwheel-dev/traces/cebc9a86476fc3e12830e622dcbb981c) | Leads with the cancellation answer, explains shipment cutoff, and cites policy; you approved its readability. | Failure rejected — Is much simpler to read |
| [final-178](http://localhost:3000/project/cartwheel-dev/traces/3b57a3446b3644107335cebe57a38b6e) | Confirms the requested escalation and says dates were not changed; you called it perfect. | Failure rejected — This is perfect. |
| [final-072](http://localhost:3000/project/cartwheel-dev/traces/a0f158324c6b0e60401334b346fdb699) | Short cancellation-policy explanation with citation; you liked its simple English. | Failure rejected — Tells it in really simple English. I like it. |

Likely evaluator: **LLM judge**, if this category survives review. It needs at least three confirmed positive examples before finalization. If the precise definition does not fit the notes, keep it pending or explicitly revise it and search again; do not redefine it silently. Full requests, tool results and session context are preserved in the accompanying evidence JSON.

## C — No usable response

Definition: The run ends without an answer, clarification, refusal, escalation, or clear failure notice, leaving silence or only an unfulfilled promise to act.

Requirement: **RESP-7**, approved after these historical traces. A clarification, appropriate refusal, escalation or clear user-facing failure notice counts as a response; task success is a separate question. Silence or only a promise does not count.

### Proposed failure examples — incomplete attempts

| Trace | Evidence in this category | Saved human decision |
|---|---|---|
| [final-229](http://localhost:3000/project/cartwheel-dev/traces/44862c87ab91d6a519e7d7f20a42cb3c) (incomplete; `44862c87`) | No assistant message recorded; provider rejection (400 cyber_policy). | Failure accepted — Yeah, this is a problem. Nothing showed up. |
| [final-238](http://localhost:3000/project/cartwheel-dev/traces/23d8c02949dfda9a3f1fc01352c861a6) (incomplete; `23d8c029`) | No assistant message recorded; quota exhaustion (429 credit_balance_exhausted). | Failure accepted — Correct. No response was delivered. |
| [final-242](http://localhost:3000/project/cartwheel-dev/traces/f8b252caf57871e2070d567411e0fe2e) (incomplete; `f8b252ca`) | No assistant message recorded; quota exhaustion (429 credit_balance_exhausted). | Failure accepted — Correct. No response was delivered. |

### Proposed close negatives — separate completed attempts

| Trace | Evidence in this category | Saved human decision |
|---|---|---|
| [final-229](http://localhost:3000/project/cartwheel-dev/traces/80290bc1947180f8d6513afd8ce4ec72) (completed; `80290bc1`) | Explains denied access; no other store's order details. | Failure rejected — This is correct. |
| [final-238](http://localhost:3000/project/cartwheel-dev/traces/b2d44f1891cba1343b973c261ddb90f9) (completed; `b2d44f18`) | Asks for identifying information instead of guessing. | Failure rejected — This is right, and it gave enough details. |
| [final-242](http://localhost:3000/project/cartwheel-dev/traces/263eb00c484d8fb7bea51ec3319c1fc9) (completed; `263eb00c`) | Refuses ineligible refund and confirms escalation; separate price objection remains. | Failure rejected — This works. |

Important boundaries:

- These three incomplete traces contain only the user message: no assistant message or tool activity is recorded. Old retrieval notes saying “after tool activity” are imprecise for these examples and are not adopted as evidence.
- Errors are historical execution diagnostics, not evidence of a current account problem or model reasoning failure. Group the observed lack of communication separately from its provider/quota causes. Both causes could be handled with a user-facing failure notice; do not split them just to increase the category count.
- The trace record establishes absence of a captured assistant response, not necessarily absence of an error notice displayed outside tracing. Your saved “no response” observations support the proposed examples; if you saw a separate clear failure notice, that changes their status under RESP-7.
- The completed final-229 uses a reworded prompt, so this is a boundary comparison, not a controlled identical-prompt rerun. The completed final-242 is only a negative for missing response; your separate price objection remains.
- For incomplete final-229, both your initial “no failure observed” note and later accepted “Nothing showed up” decision are retained. The later decision supplies the proposed positive evidence; the first note is not deleted.

Evaluator recommendation: **LLM judge for the full definition**. A code check is useful for finding empty assistant output, but cannot by itself reliably distinguish an answer, refusal or clear failure notice from only a promise. This is a new proposal for your approval, not a change to the saved pattern or an implemented/validated evaluator.

## Evidence and remaining work

The [machine-readable packet](../state/taxonomy_review_packet.json) includes all 19 selected requests, full normalized traces/tool results, companion traces in their sessions, diagnostics, original annotations, current suggestion decisions and their preserved histories. It also links each mode's originating human notes and specification requirement. Snapshot text is evidence, not a new run; dates and wording are not updated to today.

The handout requires **5–8 final evidence-backed categories**. Even if all three drafts are confirmed, more human-supported categories are still needed. We will not invent failures, split one fix into artificial categories, or reopen resolved requested-price/flag objections to reach that count. Unresolved concerns such as final-215 formatting still need evidence and a distinct boundary before becoming a mode.

After this review: gather any genuinely missing evidence/categories; repeat search after definition revisions; compare the stable taxonomy with AgentDebug; review the final 15 uniform traces and assess new-mode discovery; apply every final mode to every reviewed trace; sync accepted scores to Langfuse and verify them; finish reports and your recording. The Raindrop Workshop remains required but can be completed on the later day you requested. No workshop or model run is started by this packet.
