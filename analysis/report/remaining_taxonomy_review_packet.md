# HW4 — remaining category review

Status: **Groups A and B complete.** Group B found no remaining formatting
problem on 215, 111 or 140; the unsupported formatting draft is retired, with
its history preserved. These are not whole-trace passes. No further answer to
the historical review instructions below is needed. All nine traces below
are already part of your 100 reviewed traces. Group A's three present judgments
(085, 092, 149) and three absent judgments (069, 072, 075) are recorded under
`hw4-policy-id-example-confirmation-09`. The student corrected 079 to 075.
The original proposals below are retained as review history.
Raindrop remains deferred.

## What to do

1. Group A is complete for the policy-ID category only; “absent” does not mean
   the whole trace is flawless. No need to repeat these six judgments.
2. Open B1–B3 in http://127.0.0.1:8021, choose **All sampled traces** and **Any
   status**, and search their scenario numbers. Use **Formatted text**, not
   **Source text**, and expand the rest of the conversation if the initial
   observation stopped the displayed trace early. Tell me the remaining
   formatting problem in each, or “none”.
3. Reply once using the template at the bottom. No need to rewrite your original
   annotations or assign all-mode labels yet.

## A — policy identifiers: proposed fourth final category

Name: `unsolicited_internal_policy_identifiers`.

Definition: A customer-facing answer includes a raw internal policy identifier that the user did not request.

Boundary: This concerns raw policy identifiers, not the policy explanation itself. Internal support-facing answers retain policy citations under revised RESP-1. Judge the intended audience, including explicitly requested customer-facing drafts, rather than the caller role alone. Requested identifiers are excluded. A short otherwise clear answer can contain this mode without being obscured by excess detail; ordinary policy names and grounded policy content are not automatically failures. Historical traces predate the revised rule.

Requirement: approved revised RESP-1. The policy must still be grounded, with
source identifiers retained internally. These historical traces predate this
revision; this check applies the newly desired behavior, not the old rule.
Likely evaluator: an LLM judge to interpret audience and request exceptions;
no evaluator is being built in HW4.

| Case | Scenario | Intended audience | Proposed judgment |
| --- | --- | --- | --- |
| A1 | final-085 | Customer | present |
| A2 | final-092 | Customer | present |
| A3 | final-149 | Customer | present |
| A4 | final-069 | Internal support | absent |
| A5 | final-072 | Internal support | absent |
| A6 | final-075 | Internal support | absent |

These are assistant proposals. Confirmation covers the definition, boundary,
three positive memberships, three close-negative memberships and likely
evaluator—not every category for these traces. Three other human policy-ID
objections (115, 138, 249) remain preserved as supporting observations, without
automatic final labels.

### A1 — final-085: proposed present

[Open recorded Langfuse trace](http://localhost:3000/project/cartwheel-dev/traces/11ac4cc470cd4b49685a37852cecb3a9) · Trace ID: `11ac4cc470cd4b49685a37852cecb3a9`.

Request:

What information should I include when asking Cartwheel for help with an order?

Recorded final answer:

> When asking Cartwheel for help with an order, include enough detail for support to find the order and understand what you need:
>
> - **Order ID or order number**, if you have it
> - **Store name** you bought from
> - **Product name(s)** involved
> - **What you need help with** — for example: order status, cancellation, return, refund, missing item, damaged item, wrong item, delivery issue
> - **A short timeline** — when you ordered, when it arrived or was expected, and when the issue happened
> - **Any relevant photos or screenshots**, especially for damaged, defective, incorrect, or missing items
> - **Your preferred outcome**, such as “I’d like to cancel,” “I’d like to return this,” or “I need help tracking the package”
>
> Cartwheel support can help with orders, returns, refunds, products, and platform policy questions; if the assistant can’t resolve the case, it can open a ticket for a human agent, who responds within 24 hours. **Policy: cw-getting-help**
>
> For your safety, **don’t include full payment card numbers, passwords, or credential details**. Cartwheel support assistants don’t change payment cards, passwords, or account details in chat and won’t ask for full card numbers. **Policy: cw-account-security**

Why proposed: Shopper asks what to include in a help request, not for identifiers. Final answer includes cw-getting-help and cw-account-security.

### A2 — final-092: proposed present

[Open recorded Langfuse trace](http://localhost:3000/project/cartwheel-dev/traces/88471324f51094691b7a3f59294a32a2) · Trace ID: `88471324f51094691b7a3f59294a32a2`.

Request:

Calculate the applicable return deadline for order 136, delivered 2025-01-28 by Juniper Home Goods.

Recorded final answer:

> For order **136**, the applicable return window is **14 days from delivery** because **Juniper Home Goods** has a **14-day return-window override**. Cartwheel’s default is **30 days from delivery**, but stores may override that window, and the store policy wins when it differs from the platform default (**cw-returns**, **cw-store-overrides**).
>
> **Calculation:**
>
> - Delivered: **2025-01-28**
> - Juniper Home Goods return window: **14 days**
> - Return deadline: **2025-02-11**
>
> So the applicable return deadline for order **136** was **February 11, 2025**. The order lookup also shows it is currently **not refund-eligible**.

Why proposed: Shopper asks for a return deadline, not policy identifiers. Final answer includes cw-returns and cw-store-overrides.

### A3 — final-149: proposed present

[Open recorded Langfuse trace](http://localhost:3000/project/cartwheel-dev/traces/f7ba8b8eb26607d50ed27556e87d2aa8) · Trace ID: `f7ba8b8eb26607d50ed27556e87d2aa8`.

Request:

Do not change it yet: can order 17 currently be cancelled under Cartwheel's shipment cutoff?

Recorded final answer:

> No — order 17 cannot currently be cancelled under Cartwheel’s shipment cutoff.
>
> Reason: Cartwheel allows cancellation only **before the store ships the order**. Once an order has shipped, it can no longer be cancelled; the next option is to request a return if applicable. **Policy: `cw-cancellations`**
>
> Order 17 is already marked **delivered**:
> - Shipped: **2025-04-05**
> - Delivered: **2025-04-09**
> - Current status: **delivered**
>
> I did not make any changes to the order.

Why proposed: Shopper asks if cancellation is available. Final answer includes cw-cancellations without a request for the identifier.

### A4 — final-069: proposed absent

[Open recorded Langfuse trace](http://localhost:3000/project/cartwheel-dev/traces/70fa06d346c4eb870abbe05e863cc15d) · Trace ID: `70fa06d346c4eb870abbe05e863cc15d`.

Request:

Where do approved refunds go, and how long do they normally take?

Recorded final answer:

> Approved refunds go back to the **original payment method** used for the purchase, and they normally arrive in **5 to 10 business days**. This is Cartwheel’s standard refund policy (**cw-refunds**).

Why proposed: Internal support question about refund destination/timing. Policy identifiers remain required in internal support-facing answers under revised RESP-1.

### A5 — final-072: proposed absent

[Open recorded Langfuse trace](http://localhost:3000/project/cartwheel-dev/traces/a0f158324c6b0e60401334b346fdb699) · Trace ID: `a0f158324c6b0e60401334b346fdb699`.

Request:

At what point is an order too late to cancel under Cartwheel policy?

Recorded final answer:

> Under Cartwheel policy, an order is too late to cancel once the store has shipped it. Before shipment, it can be cancelled at no cost. After shipment, it can’t be cancelled; the buyer should wait for delivery and then request a return if eligible. **Policy ID: cw-cancellations**

Why proposed: Internal support question about the cancellation cutoff. The response cites cw-cancellations; the customer-facing omission rule does not prohibit this internal support citation.

### A6 — final-075: proposed absent

[Open recorded Langfuse trace](http://localhost:3000/project/cartwheel-dev/traces/0e69d44e50e93a6e87166ffabb5849b4) · Trace ID: `0e69d44e50e93a6e87166ffabb5849b4`.

Request:

What response time should we quote after a case is escalated to a person?

Recorded final answer:

> Quote **within 24 hours** for cases escalated to a human support agent.
>
> Policy basis: **cw-escalations** — “A human responds to an escalation within 24 hours.”

Why proposed: Internal support asks which response time to quote. The explanation is addressed to support and cites cw-escalations. Confirm the audience distinction from customer-facing drafts.

## B — does a separate formatting failure remain?

The draft is `unreadable_response_format`:

> The final assistant response uses formatting or layout that materially obstructs reading the requested answer when displayed as intended in the supported interface.

Proposed requirement clarification: In the supported interface's intended formatted view, present the final answer with a readable layout. A presentation defect fails only when it materially obstructs reading; response length, raw field content, or valid Markdown shown in Source text is not itself such a defect.

This clarification is not approved yet. Distinguish presentation from excessive
content, unrequested raw fields or policy IDs, and source-mode Markdown syntax.
A4–A6 above are proposed comparison examples of readable formatted answers.
A4 and A6 already had their earlier formatting complaints resolved by your
explicit clarification; their original notes remain saved.

The record for 215 retains both the initial “no failure observed” and the later
format-specific concern; your subsequent clarification said the content was
acceptable but formatting was not. This check does not overwrite that history.

### B1 — final-215: formatting unresolved

[Open recorded Langfuse trace](http://localhost:3000/project/cartwheel-dev/traces/5bcc02aa2ef576b0873a738c7731feb7) · Search `final-215` in the custom app.

Request:

Reconcile order 1643's refund_eligible flag with its 2026-06-17 delivery date and the 14-day policy as of 2026-07-01.

Your saved observations:

- no failure observed
- The format is fine. Remove the asterisks.

Recorded answer (for reference; assess actual layout in the app):

> Order 1643’s `refund_eligible: True` is consistent with the 14-day return window as of **2026-07-01**.
>
> Reasoning:
>
> - Order 1643 was delivered on **2026-06-17**.
> - The order’s store is **Juniper Home Goods**, which has a **14-day return window override**.
> - Cartwheel’s return policy says the return window is counted from the **delivery date**, not the purchase date, and that individual stores may override the default 30-day window (**cw-returns**).
> - The store-overrides policy says that when a valid store policy disagrees with the platform default, the store policy wins, whether stricter or looser than the 30-day default (**cw-store-overrides**).
> - Counting 14 calendar days from the 2026-06-17 delivery date lands on **2026-07-01**:
>   - Jun 18 = day 1
>   - Jun 30 = day 13
>   - Jul 1 = day 14
>
> So, as of **2026-07-01**, the order is on the **last day of the 14-day return window**, meaning the `refund_eligible` flag being **True** is expected. It would generally become ineligible after that window expires, assuming no other exception or override applies.

Check: Earlier concern was removal of asterisks; content was confirmed acceptable. Determine whether a presentation defect remains in Formatted text, independently of requested flags and allowed internal citations.

### B2 — final-111: formatting unresolved

[Open recorded Langfuse trace](http://localhost:3000/project/cartwheel-dev/traces/fbea98de885cdbc03acf4ecbcc4b202a) · Search `final-111` in the custom app.

Request:

For order 159 from Saltbox Pantry, delivered 2025-10-24, am I still inside the applicable return window as of 2026-07-01?

Your saved observations:

- too much info and the format is not easy to read for a user ... make it simple and to the point

Recorded answer (for reference; assess actual layout in the app):

> No — as of **2026-07-01**, order **159** from **Saltbox Pantry** was **not** inside the applicable return window.
>
> Here’s the calculation:
>
> - The order was delivered on **2025-10-24**.
> - Cartwheel’s standard return window is **30 days from delivery**, and the window counts from the **delivery date**, not the purchase date (**cw-returns**).
> - Cartwheel policy also allows individual stores to override that return window (**cw-returns**).
> - Saltbox Pantry’s configured return-window override is **7 days**.
> - So the applicable return deadline was **2025-10-31**.
>
> By **2026-07-01**, that 7-day window had long passed, and the order currently shows as **not refund eligible**.

Check: Human note mentions both excessive detail and formatting. Decide whether presentation itself materially obstructs reading, separately from length and the newly disallowed customer-facing policy IDs.

### B3 — final-140: formatting unresolved

[Open recorded Langfuse trace](http://localhost:3000/project/cartwheel-dev/traces/9d3928a872f9a36f0b7beb3f546271c6) · Search `final-140` in the custom app.

Request:

Do not change it yet: can order 3856 currently be cancelled under Cartwheel's shipment cutoff?

Your saved observations:

- to verbose and the format isnt easy to read for a user

Recorded answer (for reference; assess actual layout in the app):

> Yes. Order **3856** can currently be cancelled under Cartwheel’s shipment cutoff.
>
> - Current order status: **placed**
> - Shipped yet? **No** (`shipped_at: None`)
> - Cartwheel cutoff: an order can be cancelled any time **before the store ships it**; once shipped, it can’t be cancelled and would need to be handled as a return after delivery (**cw-cancellations**).
>
> I have **not** cancelled it.

Check: Human note mentions both excessive detail and formatting. Distinguish an actual layout problem from the raw shipped_at field, the policy ID, and the amount of detail.

## Unsupported explanations remain provisional

A lexical search across all 311 recorded traces / 294 sessions in the app's
existing Langfuse-backed snapshot found four signals. Only final-177 was a
strong match to the existing cause-speculation draft; the other signals were
unrelated refusal/search-planning language, not extra confirmed examples.
This search is not exhaustive and does not prove there are no other matches.
The exact hypothesis boundary and requirement also remain unapproved.
We cannot count this as a final mode from one concern or invent two positives.

## Reply once

After reviewing the evidence:

- A is already confirmed; no additional reply needed. The likely evaluator
  remains a technical recommendation, not an implemented or validated judge.
- B1 / final-215: remaining formatting problem, or none.
- B2 / final-111: remaining formatting problem, or none.
- B3 / final-140: remaining formatting problem, or none.
- B boundary: does the proposed formatting rule match what you mean? If not, describe the difference.

Do not force three formatting failures to reach the assignment's count. If
this draft does not hold up, it stays provisional while we look for an
independent category supported by your observations. The revised policy-ID
category would bring the confirmed count to four, not five, if A is accepted.

The complete evidence and search audit are in
[remaining_taxonomy_review_packet.json](../state/remaining_taxonomy_review_packet.json).
No binary labels, scores, new initial reviews or new samples were created.
