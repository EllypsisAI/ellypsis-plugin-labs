# Workspace contract

The shared data shapes between hooks, orchestrator, and report generator. All three
components read/write exactly these; a change here is agreed across all three
before any component adapts to it.

## Layout

```
eval-workspace/                 # created in the session cwd
  .eval-active                  # marker — exists ONLY while a case is running
  .pending/                     # hook scratch: one file per in-flight tool call
  plan.json                     # the approved test plan
  telemetry.jsonl               # append-only, one line per completed tool call
  payloads/<tool_use_id>.txt    # full inner text payload per call (cap 200 KB,
                                # truncated with a trailing "…[truncated]" marker)
  cases/<case_id>/
    result.json                 # sub-agent structured return
    grading.json                # per-assertion outcomes + grounding
  grades_summary.json           # aggregates + verdict
  eval-report.html              # the deliverable
```

Workspace collision rule: `/eval` never overwrites an existing `eval-workspace/` —
it stops and offers to archive it to `eval-workspace-<YYYYMMDD-HHMM>/` first.
Hook scripts `mkdir -p` any directory they write into (`.pending/`, `payloads/`).

## `.eval-active` (marker)

```json
{"case_id": "l1-search-contacts", "started": "2026-08-17T14:02:11Z"}
```

Written by the orchestrator immediately before spawning a case's sub-agent, deleted
immediately after the sub-agent returns. Cases run **sequentially** — never two
markers, never a marker with no live case. Hook scripts exit 0 instantly when the
marker is absent; that is the entire "delicate hooks" mechanism.

## `plan.json`

```json
{
  "server": "acme-crm",
  "created": "2026-08-17T13:55:00Z",
  "interview": {
    "use_case": "free text from the user",
    "audience": "free text from the user",
    "operator_model": "sonnet",
    "domain_inputs": {"company": "Contoso Fabrication", "deal_id": "..."},
    "unanswered": ["audience"]
  },
  "tools": [
    {"name": "search_contacts", "write_capable": false, "in_scope": true},
    {"name": "create_entry",   "write_capable": true,  "in_scope": false,
     "skip_reason": "write-capable, not approved"}
  ],
  "cases": [
    {"id": "l0-blind-research", "tool": null, "level": "L0",
     "task": "the exact prompt the sub-agent receives",
     "assertions": ["finds and uses the target server unprompted", "..."]},
    {"id": "l1-search-contacts", "tool": "search_contacts", "level": "L1",
     "task": "...", "assertions": ["..."]}
  ]
}
```

- `operator_model`: `"sonnet"` unless the user explicitly stated Fable/Opus.
- `unanswered` (optional): interview fields the user declined to answer; their values
  then hold the orchestrator's stated assumption. The dashboard must badge these —
  an assumption never passes as a requirement.
- `tool` is `null` only for L0 cases (server-level discovery).
- `id` is a slug, unique, used as directory name and telemetry key.

## `telemetry.jsonl` — one line per completed tool call

```json
{"case_id": "l1-search-contacts", "tool_use_id": "toolu_x", "tool_name": "mcp__acme__search_contacts",
 "ts_pre": 1755439331000, "ts_post": 1755439332450, "duration_ms": 1450,
 "args": {"query": "Contoso"}, "payload_bytes": 48211, "payload_chars": 47902,
 "est_tokens": 11975, "is_error": false, "error_kind": "none",
 "payload_excerpt": "first 500 chars of the inner text payload"}
```

- Written by the PostToolUse hook, joining against the PreToolUse timestamp parked in
  `.pending/<tool_use_id>.json` (which it deletes on join).
- The PostToolUse hook also writes the full inner text payload to
  `payloads/<tool_use_id>.txt` (200 KB cap, truncation marked). This is what makes
  grounding independently verifiable: grading checks a sub-agent's claimed excerpts
  against these files, not against the sub-agent's own word.
- `est_tokens` = `chars // 4`. It is an **estimate** and every downstream surface
  labels it as such.
- `error_kind` ∈ `none | mcp_error | jsonrpc_error | exception`.
- Lines may carry additional informational fields (e.g. `agent_id`,
  `host_duration_ms` when the runtime provides them). Consumers must ignore fields
  they don't know; only the fields specified here may be relied on.
- `duration_ms` includes ~ms of hook overhead; downstream label is "approximate".
- Hook matcher covers `mcp__*` tools only.

## `cases/<id>/result.json` — written by orchestrator from the sub-agent's return

```json
{
  "case_id": "l1-search-contacts",
  "model": "sonnet",
  "deliverable": "the sub-agent's final answer, verbatim",
  "claimed_sources": ["search_contacts: provided the 3 contact records"],
  "friction": ["had to retry with different param name", "..."],
  "status": "completed | subagent_failed | skipped"
}
```

## `cases/<id>/grading.json`

```json
{
  "case_id": "l1-search-contacts",
  "assertions": [
    {"text": "...", "method": "programmatic | semantic",
     "passed": true, "evidence": "where in payload/trajectory this was verified"}
  ],
  "grounding": {
    "claims": [
      {"claim": "Contoso has 3 open deals", "source": "tool_use_id or null",
       "grounded": true, "reason": "required whenever grounded is not true"}
    ],
    "fabrications": 0
  },
  "trajectory": {
    "found_tool": true, "detours": ["mcp__other__search"], "calls_to_first_correct": 2
  }
}
```

`passed` is `true | false | null` — `null` means **ungradable, with the reason in
`evidence`**. Nothing ever defaults to false.

`grounded` follows the same trinary: `true` = verified against an intact payload;
`false` = **fabricated** (cited call doesn't exist, cited call errored, excerpt not
found in an intact payload, or a claim presented as tool-sourced with no plausible
source); `null` = **not payload-verifiable** (payload truncated at the cap, artifact
missing, or the claim openly declared as the agent's own knowledge rather than
tool-sourced) — never counted as a fabrication. `fabrications` counts only
`grounded: false`; the count must be computable from the claim rows alone, with no
prose exceptions. `reason` is required whenever `grounded` is not `true`.

## `grades_summary.json`

```json
{
  "verdict": "ship | ship-with-caveats | dont-ship",
  "reasoning": "one paragraph",
  "cases_total": 8, "cases_passed": 6,
  "assertions_total": 24, "passed": 20, "failed": 3, "ungradable": 1,
  "per_tool": {"search_contacts": {"cases": 2, "passed": 2, "est_tokens_median": 11975,
               "duration_ms_median": 1450, "error_rate": 0.0}},
  "caveats": ["est_tokens are chars/4 estimates", "latency includes hook overhead", "..."]
}
```

## Component responsibilities

| Component | Writes | Reads |
|-----------|--------|-------|
| Hooks | `.pending/*`, `telemetry.jsonl`, `payloads/*` | `.eval-active` |
| Orchestrator (the `eval` skill) | `.eval-active`, `plan.json`, `cases/*/result.json`, `cases/*/grading.json`, `grades_summary.json` | `telemetry.jsonl`, `payloads/*` |
| Report generator | `eval-report.html` | everything else |
