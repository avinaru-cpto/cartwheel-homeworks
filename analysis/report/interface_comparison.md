# HW4 interface comparison

Status: custom interface implemented and used for the 100-trace review. The
Workshop comparison was deliberately deferred at the student's request. The
student requested an independent interface build before beginning the human
review. The build and its tests did not create homework annotations, modes,
sample selections, or Langfuse scores; those records came from the later
human-review workflow.

## Retained from the reference

Tool calls and results share a container, with colored role indicators and
expandable JSON. Evidence selection creates a temporary highlight before
focusing the note editor. Saved observations appear in the adjacent margin.
This keeps tool evidence close to the response the reviewer is assessing.

## Changed after inspecting the actual traces

The final HW3 collection contains **311 distinct trace IDs, 294 sessions, and
17 sessions with two turns**, verified against the export and the live source.
The custom interface groups by `cartwheel.session_id`, sorts turns by timestamp,
and preserves the original trace IDs for individual annotations and scores.
It does not merge retries merely because they share a scenario ID.

For example, opening follow-up trace `fac84563d0ebad9f9e788ac73230922a` also shows
earlier trace `e46175c4ea750399e9e1a3caaad05d0b`. Both have separate review state.
The supplied bulk normalizer merges by scenario; the custom adapter instead
uses only its single-record normalization function. It retains system context,
execution diagnostics, and a full raw-source view as well.

Additional live traces used to check the visual organization:

- `354d27074968be0c96490fb55ce788e9`: shopper order lookup.
- `8a90a74981157335e612ecdb6d1cb4b5`: merchant order lookup.
- `aa22bf74939b96f5f829f70303642482`: support order lookup.
- `f309372584db5e1e5e9d2192f693755d`: policy retrieval with multiple results.

These were inspected for trace structure and rendering, not assigned behavioral
labels. Merchant scope can be present on tool-span metadata even when absent
from root metadata, so the adapter reads those explicit attributes.

Separate taxonomy, structured-labeling, and progress views replace the
reference's combined progress workflow. Initial review distinguishes an explicit
“no failure observed” from an untouched trace. A final-mode definition change
invalidates older decisions for progress counting until the human rechecks them.
Suggestion rejections and note edits retain their histories.

The design-engineering skill influenced the restrained role colors, readable
line lengths, visible save feedback, keyboard-accessible step annotations, and
instant repeated navigation. There are no decorative navigation animations.

### Markdown display revision after human review

The student reported difficulty finding, sharing, and cataloguing traces and
understanding tool activity in the ordinary Langfuse view. After inspecting
the same trace in the custom interface, the student reported that the conversation
and tools were clear. This does not establish that sharing or cataloguing is solved.

During the first two review batches, the student repeatedly noted unreadable
formatting, including visible table pipes. The original custom interface showed
Markdown source literally to preserve evidence offsets. On 2026-09-24, the
student approved a UI-only formatting change, leaving the original trace text and
human observations unchanged.

| Before | After | Why |
| --- | --- | --- |
| Raw asterisks and table pipes in conversation prose | Rendered emphasis, lists, code, and tables by default | Separate the agent's writing from the review viewer's display limitation |
| Highlight positions followed displayed plain text | Rendered fragments map back to original source offsets | Preserve existing notes and permit selections across formatting and table cells |
| Original syntax was the only reading view | Per-message Source text / Formatted text switch | Keep the original evidence inspectable without making it the default reading experience |

The design-engineering guidance informed readable spacing and instant view
switches; no decorative animation was added. Existing formatting judgments remain
the student's observations and have not been changed automatically. The student
should revisit them in the formatted view before finalizing any failure category.

## Remaining limitations

The interface loads a snapshot of the trace collection at startup; restart the
server to fetch newly recorded traces. State updates from other tabs or the
coding agent are polled. Markdown rendering supports a common, source-mapped
subset rather than every CommonMark/GFM extension. Raw HTML is escaped and images
are not fetched; original syntax remains available using Source text. Sharing and
cataloguing usability have not yet been validated by the student.

Score persistence is tested with a simulated Langfuse bridge and includes
idempotency and outage recovery checks. All 500 human-confirmed judgments have
been written to Langfuse; the review workspace reports zero missing decisions
and zero pending synchronizations. The first twelve judgments also received
independent score-ID read-back checks. Live trace reading was verified; no live
model calls were made.

The map uses PCA and clustering of structural features; it is a navigation aid,
not a claim that a cluster corresponds to a failure category. Depth-search
candidates and Workshop hypotheses still come from the human/agent workflow.

## Offline fallback

Live Langfuse was reachable for the running interface, so no offline fallback
was used for homework review. Synthetic browser tests used a separate temporary
state directory and did not contact Langfuse. If a future review session uses
the HW3 export during an outage, record the date and actual reason here.

## Deferred items

- Workshop comparison remains explicitly deferred rather than represented as
  completed.
- The student recording remains explicitly deferred.
