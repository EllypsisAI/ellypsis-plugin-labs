# Changelog

What changed in each release, and why it is better. This file ships inside the plugin and
is published, so it is written for people using mcp-eval — not for its authors. Internal
design notes and anything about who the tool was built with belong in the workshop, not here.

## 1.0.4 — 2026-09-01

Documentation pass. The changelog is written for people using mcp-eval, and an internal
design note that had been shipping inside the plugin directory is removed. No functional
changes.

Version bumped so `plugin update` re-copies; an install keeps whatever files it already has
until the version changes.

## 1.0.3 — 2026-09-01

**Fixtures and worked examples are fully synthetic.** The example account is
`Contoso Fabrication`, with invented contacts, ids, deal names, values and dates. A
recognised placeholder is deliberate over a plausible-sounding company name: a reader
should never have to wonder whether an example is real, and an eval tool that ships
realistic-looking business records teaches the wrong habit to whoever copies them.

Realism in these examples comes from how people phrase a question, not from whose account
is in it — an account name in a sales question is still how people talk, and that is all
the test plans needed.

All 72 tests pass, which is the check that matters: grading fixtures assert claims against
payload text, so an inconsistent substitution fails the suite.

Version bumped so `plugin update` re-copies; without it an existing install keeps the
fixtures it already has.

## 1.0.2 — 2026-08-28

**The test suite no longer ships to users.** A plugin install copies the plugin directory
verbatim, so `tests/` — 22 files, 164K of fixtures — was being written into every
installation of mcp-eval. Nobody installing an eval tool wants its fixtures on their disk.

Moved to `tests/mcp-eval/` at the repo root: still versioned, still in CI's reach, still
one command to run, but outside what gets packaged. The two path anchors were repointed
(both suites derived the plugin root from their own location), the `eval-report.html`
ignore rule moved to the root `.gitignore`, and the three run commands documented in the
suites' own docstrings were corrected — those are what a contributor actually types.

All 72 tests pass from the new location, and all three documented invocations work:
`pytest tests/`, `python3 tests/mcp-eval/test_report.py`, and
`python3 -m unittest discover -s tests/mcp-eval`.

Version bumped so `plugin update` re-copies; without it an existing install keeps the
files it already has.

## 1.0.1 — 2026-08-28

**Worked examples standardised across the guides and fixtures.** Every reference guide and
test fixture now uses one consistent placeholder account rather than a mix, so an example
read in `test-plan-guide.md` matches the payloads it is graded against.

Version bumped so `plugin update` actually re-copies — anyone on 1.0.0 has the old docs
cached.

## 1.0.0 — 2026-08-17

Full rewrite. Nothing of v0.2's architecture survives. Four files were salvaged as inputs
(metrics helpers, report visual style, assertion guidance, changelog lessons); the rest was
rebuilt from scratch.

### Why v0.2 died

Three failure modes, discovered when preparing it to meet real users:

1. **It measured the wrong client.** The primary mode (`run.py`) was a bespoke Python
   MCP client doing its own JSON-RPC handshake — it measured how the server behaves
   for a client that doesn't exist in production. The in-session path existed but was
   framed as a fallback and penalized (`duration_ms: null`). The doctrine was
   inverted: the entire point is evaluating the server *paired with the LLM* —
   discoverability, argument choice, payload survival, grounding. None of that is
   visible to a deterministic client.
2. **The grading lied.** Docs promised LLM grading; the code had none. Anything a
   regex couldn't match was marked `NEEDS_LLM_JUDGMENT` and then **defaulted to FAIL
   on disk**. Every semantic assertion in every v0.2 report failed closed.
3. **The most important input was homework.** After `/eval-init` the user was told to
   hand-edit `eval-tests.json` with realistic params and assertions. Nothing elicited
   them conversationally; most users never did it well, and bad cases produce
   meaningless evals.

### The v1 architecture

- **Claude Code is the harness.** An orchestrator (`/eval`) interviews the user,
  builds a plan, and spawns one sub-agent per case. Sub-agents make the real MCP
  calls; plugin hooks (Pre/PostToolUse, matched to `mcp__*` only) capture timing,
  arguments, and payload contents. Hooks are marker-gated: without an active eval
  marker they exit immediately, so they're inert in every normal session.
- **Payload containment is structural.** Tool payloads land in sub-agent contexts and
  die there; only structured summaries return. That, not a warning, is the main
  token-cost control (the warning exists too — preflight states a cost band and
  checks context headroom).
- **Information asymmetry replaces persona-acting.** Sub-agents aren't told to "act
  naive" — they genuinely receive only what a real user would say (L0 blind → L3
  spec). They're also never told they're in an eval: an agent that knows it's on a
  discovery test hunts through tools in a way no production agent does.
- **Sonnet is the test condition.** The test agency runs on Sonnet unless the user
  explicitly states Fable/Opus will operate the server in production. Cost, and
  design: an integration worth shipping should be operable by Sonnet. Every case
  records which model ran it.
- **Nothing defaults to FAIL — anywhere.** Assertions are `true | false | null`
  (null = ungradable, with reason). Grounding is trinary the same way: `false` means
  *fabricated* and nothing else; truncated evidence and declared own-knowledge claims
  are `null`, never counted as fabrications. The fabrication count is computable from
  the claim rows alone — no prose exceptions. This rule was re-derived three times
  during the build (assertion grading, grounding, truncation handling); treat any
  future field that "defaults to false" as a bug.
- **Grounding is payload-verified.** Hooks write full payload contents
  (`payloads/<tool_use_id>.txt`, 200 KB cap) plus a 500-char excerpt per telemetry
  line. Grading verifies each claimed excerpt against the captured payload — a cited
  call that doesn't exist in telemetry is the strongest fabrication signal. The
  sub-agent's own SOURCES report is the map, never the proof. (First contract draft
  recorded only payload *sizes*, which would have made grounding a self-report — a
  fabrication detector taking the suspect's word. Caught in build review.)
- **Write-capable tools are skipped by default** and run only on explicit per-tool
  approval with unambiguous vocabulary. The eval hits live business systems; a "test"
  must never corrupt a real pipeline.
- **The shared data model is a contract** (`references/workspace-contract.md`).
  Hooks, orchestrator, and report were built by three parallel builders against it;
  changes required sign-off. Keep it that way.
- **Skills-only surface.** Claude Code merged commands into skills (2.1.199); a
  `commands/` directory still works but is the legacy path. The first build shipped
  three commands plus a router skill — four overlapping trigger surfaces — and was
  restructured the same day into three skills (`eval`, `eval-rerun`, `eval-report`),
  the router merged into `eval` itself. The merge surfaced a real bug: `/eval-rerun`
  accepted a workspace argument while the hooks resolve a fixed `eval-workspace/`
  path, so a rerun against an archived workspace would have captured zero telemetry
  and read as a server failure. Rerun takes no workspace argument; restore the
  archive first.

### Carried forward from v0.2's own lessons

Server-agnostic forever (server knowledge lives in assertion text, not scripts); no
one-shot scripts with real data baked in; every stage's artifact independently
re-runnable; SKILL.md frontmatter stays minimal — `name` + `description` +
`argument-hint`, never an `arguments:` array (that form has silently broken frontmatter
parsing before); `author` is an object; validate with the `claude plugin validate` CLI,
not only the validator subagent.

### Distribution

v1.0.0 moves the plugin into the `ellypsis-plugin-labs` marketplace repo inline
(`plugins/mcp-eval/`). Install with
`/plugin marketplace add EllypsisAI/ellypsis-plugin-labs` then
`/plugin install mcp-eval@ellypsis-labs`.
