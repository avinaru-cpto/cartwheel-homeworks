# Cartwheel HW4 review workspace

A custom local review tool for human open coding, taxonomy development, and
structured labeling. No model calls, automatic homework labels, or replayed
annotations run at startup. The supplied reference UI remains unchanged.

## Start

From the repository root, run:

```bash
uv run python -m analysis.review_app
```

This loads the existing `.env` without printing credentials, reads the live
Langfuse records for the final HW3 scenario IDs, and serves the interface at
**http://127.0.0.1:8021**. Allow the initial trace fetch to finish. The Cartwheel
application on port 8010 is not needed to review previously recorded traces.
Stop with Ctrl+C. Restart to refresh the trace collection; review state persists.

If live Langfuse is unavailable, use the unchanged HW3 export explicitly:

```bash
uv run python -m analysis.review_app \
  --source traces/support_traces.json \
  --offline-reason "Local Langfuse is temporarily unavailable"
```

Replace the reason with what actually happened. Offline mode displays a banner,
records the source in new batch manifests, and keeps binary judgments pending
until you restart with live Langfuse and choose **Progress → Retry pending scores**.
Add the actual outage reason to the interface comparison if you review offline.

## First session

1. Finish the handout's preliminary 5–10-trace Langfuse review and record your
   own interface observations. The overnight build does not satisfy that human step.
2. Inspect the workspace and request any layout adjustments.
3. Open **Progress → Select 15 traces** for the initial uniform batch. No sample
   is selected automatically, and inspecting a trace never marks it reviewed.
4. In **Review**, read until the first failure. Select text, write an observation,
   and press Enter. “Note on this step” is the keyboard-accessible alternative.
   Use “No failure observed” only after reviewing the trace without finding one.
5. After each batch, compare your notes and develop candidate modes in
   **Taxonomy**. The origin annotation IDs are available inside the mode editor.
6. Select later batches from **Progress**, following the handout. The displayed
   five sub-batches correspond to the handout's four grouped stages: 15+15,
   30, 25, and the final 15. Earlier sample IDs cannot be reused.
   The final uniform batch requires the first 85 sampled traces to be reviewed
   and an active draft taxonomy (candidate or final modes), not 5–8 finalized
   modes. It records the taxonomy at selection time so new-mode discovery can
   be assessed afterward. Sampling does not finalize modes or label traces;
   the assignment still requires 5–8 evidence-backed final modes for completion.
7. Finalize modes only after personally inspecting the supporting positives,
   close negatives, requirement, and boundary. Use **Labeling** for every
   reviewed trace × final mode decision, including absent decisions.

J / K moves between visible traces when focus is outside an editor. Enter saves
an inline note; Shift+Enter inserts a newline. The SPEC button opens the actual
repository specification. Each turn has a direct Langfuse link when available.

## Trace identity and evidence

- One score belongs to one original Langfuse trace ID. Sibling turns provide
  context but do not automatically count as reviewed or inherit another turn's label.
- Grouping uses `cartwheel.session_id`, with the recorded Langfuse session ID
  as a fallback. Missing sessions remain isolated. Scenario retries are separate.
- The supplied `normalize_trace` handles individual records. The bulk helper
  `normalize_traces` is deliberately not used because it merges scenario IDs.
- Merchant scope is recovered from explicit tool-span attributes when absent
  from the root record. An order's store field is never used as authorization scope.
- Tool calls and results share a container. Long results can be expanded in full.
  Unique system messages, recorded error diagnostics, and the complete raw JSON
  remain available. User and assistant prose renders common Markdown, including
  headings, emphasis, lists, quotes, fenced code, links, and tables. The
  **Source text / Formatted text** button switches each message independently.
- Evidence positions always refer to the original recorded string. Selecting
  formatted text, even across bold spans or table cells, saves an exact source
  substring; Markdown punctuation may therefore appear in the quoted evidence.
  Existing annotations require no migration. Tool arguments/results remain JSON.
- The renderer is a source-mapped subset, not a full CommonMark/GFM implementation.
  It follows the common [GFM table syntax](https://github.github.io/gfm/#tables-extension-)
  while preserving extra cell content for inspection. Unsupported syntax remains
  available in Source text. Raw HTML is escaped, unsafe links are inert, and
  embedded images do not fetch external resources.
- Provider diagnostics and missing replies are visible evidence, not automatic
  behavioral failure labels. No examples or taxonomy are seeded from the real data.

## Saving and synchronization

State uses the required `analysis/state/` files. Starting or reading the app does
not change them. Sampling creates `sample_manifest.json`; notes preserve the
existing annotations envelope; taxonomy revisions retain their before/after
definitions; suggestions retain accepted/rejected dispositions and reasons.

One writer server is allowed per state directory. Browser saves include a state
revision; stale writes fail visibly instead of overwriting another tab. Note
edits and deletions preserve history. Binary label corrections append a new
record with `supersedes`, retaining previous rows. The course's label loader
uses the last current record per trace. Mode definition changes make older
decisions visibly outdated and require human rechecking.

Notes are free text saved locally. Accepting a suggestion for a candidate mode
saves a human-confirmed observation; its final binary decision remains missing.
For a final mode, explicit acceptance also writes a label with source
`accepted_suggestion`. Rejection never writes a negative binary judgment.

Accepted binary decisions save locally before synchronization. Langfuse score
configuration names are limited to 35 characters. Longer canonical mode names
use a stable readable-prefix/hash alias remotely; the full mode remains in the
local JSONL `mode`, the configuration description and score comment. Each synced
row records `langfuse_score_name` for matching remote read-back. Canonical mode
names, label IDs, stable score IDs and timestamps are not renamed by this mapping.
Langfuse writes
use numeric 0/1 score configs, the original trace ID, and a stable score ID and
timestamp to support retries and corrections across days. The synchronous
ingestion response is checked for per-event errors. A failure stays **pending**;
it does not appear as a successful sync. “Acknowledged” is not a read-back check:
verify the score in Langfuse before the assignment video. See the official
[score API documentation](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk).

The browser keeps an unsaved draft backup. **Progress → Recover browser draft**
shows it before an explicit retry. Avoid closing a page during a save. Existing
course demonstration labels are not counted unless their IDs are in the actual
loaded collection and their modes belong to your taxonomy.

## Local verification

Focused checks use synthetic records and temporary directories:

```bash
uv run pytest tests/test_review_app.py -q
node --test tests/test_review_markdown.cjs
```

Run the full suite explicitly offline so inherited Langfuse settings cannot
redirect older helper tests away from their committed fixtures:

```bash
LANGFUSE_PUBLIC_KEY='' LANGFUSE_SECRET_KEY='' LANGFUSE_HOST='' uv run pytest -q
```

Optional disposable browser QA, completely separate from homework state:

```bash
uv run python -m tests.review_app_fixture
```

It serves synthetic fixtures on port 8022, reads no credentials, and removes its
temporary state on normal exit. Labels created there are only test data.
Open **http://127.0.0.1:8022/markdown-checks** for automated DOM selection/source-map
checks. Synthetic fixture 9 includes a Markdown table and a pre-existing source
annotation for testing formatting switches, selection, saving, and reloading.

Verified on 2026-09-18: 25 focused tests passed. The final explicitly offline
full suite reported 161 passed, 13 skipped, 21 xfailed, and 9 xpassed. JavaScript
syntax was checked with Node. Chrome checks covered live session context and
retrieval results, synthetic inline selections, note persistence after reload,
the first-failure stopping view, explicit no-failure records, binary labeling,
pending sync status, rejection history, the map, and a 390px responsive layout
without horizontal overflow. No live model was called. Live score writes await
the student's first accepted judgment and read-back verification.

Markdown update verification on 2026-09-24: 14 Node renderer tests and 8 browser
DOM/source-map checks passed. Browser interaction checks also verified source
switching, legacy highlights, and saving/reloading a new cross-cell annotation
using only disposable fixture state. The 25 focused backend tests passed; the
explicitly offline full suite reported 161 passed, 13 skipped, 21 xfailed, and
9 xpassed. No live model or real annotation/score write was used for these checks.

## Scope and remaining homework

Final-batch gate correction verified on 2026-09-25: eight new sampling tests
passed, including a three-final/two-candidate taxonomy, deterministic disjoint
sampling, unchanged judgments, and preserved evidence/signoff requirements.
The explicitly offline Python suite reported 169 passed, 13 skipped, 21 xfailed
and 9 xpassed; all 14 Node renderer tests passed. No model was called.

This is a local, single-reviewer application, not a publicly hosted service.
Keep it bound to loopback. Requests require the local page's token and matching
origin; trace content is escaped before display.

Depth searches are performed with the coding agent, then 25 candidate IDs and
their search rationale are recorded in the interface. The app does not generate
AI suggestions itself. Populate `suggestions.json` with objects containing
`id`, `trace_id`, `mode`, `quote`, optional `idx`, and optional `label` (defaults
to failure present). Proposed evidence still requires human review.

The structured-labeling page also provides local accelerated triage. It loads
the complete selected trace and proposes present/absent decisions using saved
human examples, the original observation, and narrow mode-specific signals.
These proposals are not written to state or Langfuse. The reviewer must inspect
the trace, correct any proposal, explicitly confirm all five decisions, and
submit them; existing human labels always take precedence. “Save & next
unresolved” removes navigation overhead without weakening that confirmation.

Workshop installation/instrumentation and the recording remain separate from
the interface and were explicitly deferred by the student. The human review,
specification revisions, final-15 assessment, written comparisons, and reports
are recorded in `analysis/state/` and `analysis/report/`.
