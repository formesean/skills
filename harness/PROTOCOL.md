# Task orchestration and memory

This is an opt-in protocol for a human-operated Codex/Claude Code session, plus a
local checkpoint tool. It is not an autonomous model runner, security sandbox,
or a replacement for host compaction and permission controls.

## Execute

1. Define the requested outcome and authorization boundary. Pick only needed skills.
2. Retrieve relevant paths with search; read full governing functions and callers.
   Keep a source index (path/symbol/revision), not copies of whole files.
3. Implement and verify in coherent increments. Reuse unchanged observations. Stop
   repeating a failed approach after two attempts without new evidence; revise the
   hypothesis or report the blocker. Never retry non-idempotent writes blindly.
4. Before compaction, handoff, or a long pause, save the compact task state. On resume,
   read the checkpoint, check freshness, inspect the current diff and cited sources,
   then continue the next authorized action. Do not replay completed external writes.
5. Report observed results, uncertainty, and remaining work. Archive/delete completed
   local checkpoints when no longer needed; retain only useful accepted decisions.

## Context budget

Load one selected skill, then only needed references. Do not load all ten skills or
this entire repository into every task. Start with 100-200 lines around a search
hit; expand when control flow needs it. Summarize long tool output with exact short
error excerpts and source pointers. Do not truncate away the evidence for a claim.

The 16 KiB checkpoint cap is an engineering limit, not a model token measurement.
Save objective, stable criteria, accepted decisions, unresolved blockers, next action,
and check evidence. No transcripts, hidden reasoning, credentials, customer records,
or whole logs. Redact before saving; this tool is not a secret scanner.

Separate task state from long-lived knowledge. Promote a verified reusable decision
to the project's normal ADR/docs only when useful and within the user's scope. Include
source, rationale, review date, and an invalidation condition. Replace obsolete facts;
do not append contradicting memories indefinitely. Repository evidence outranks stale
notes. Do not create cross-project personal profiles from task data.

## Agents

The main session coordinates and owns requirements, integration, and the final answer.
Use the explorer for bounded investigation, reviewer for an independent read-only
pass, and verifier for relevant checks. Delegate only when supported and authorized
by the host. Default to one agent; add at most two independent workers initially.
More agents cost tokens and can overload small machines.

Send each worker: objective, source revision/paths, constraints, allowed actions,
expected evidence, and a stop condition. Do not send the whole conversation. For
independent evaluation, hide the diagnosis and expected answer. Assign one writer per
file; use isolated worktrees for independent edits. The parent checks cited evidence
and invalidates tests after integration changes. Workers must not recursively delegate,
publish, or promote memory without authorization. Prompt-only read-only roles are not
security controls; enforce capabilities with the host sandbox/tool permissions.

## Checkpoint CLI (Python 3.11+, Git, repository with a commit)

Run this tool from a checkout of this repository; plugin installation does not promise
to install its CLI. It stores state under the target repository's Git metadata, outside
tracked files. It executes fixed Git inspection commands only, never checkpoint commands.

```sh
python /path/to/skills/harness/state.py --repo /path/to/project save fix-banner \
  --expected-revision 0 < checkpoint.json
python /path/to/skills/harness/state.py --repo /path/to/project resume fix-banner
```

`checkpoint.json` has exactly these fields:

```json
{
  "objective": "Show the banner only for active accounts",
  "criteria": ["AC1: inactive accounts do not see the banner"],
  "decisions": ["Use the existing eligibility helper; source: src/eligibility.ts"],
  "next_action": "Add the inactive-account regression check",
  "blockers": [],
  "checks": [{"command": "pnpm test banner", "result": "NOT_RUN", "evidence": "Pending"}]
}
```

Use the last returned revision for subsequent saves. Concurrent/stale writers fail
instead of overwriting silently. A crashed writer can leave a `.lock`; verify no writer
is running before removing that specific lock. Saves replace state atomically. Checks
are caller-reported observations, not results certified by the tool.

`freshness` compares the current checkout with the snapshot taken at **save time**.
It covers HEAD, branch, Git-visible tracked and staged changes, and untracked
paths, file types, modes, and contents.
`STALE` calls for rereading changed sources and invalidating affected checks.

### Record what each check actually tested

Run this before and after a check whose result you want to reuse:

```sh
python /path/to/skills/harness/state.py --repo /path/to/project fingerprint
```

Record the shared value as the check's optional `source_fingerprint` only when the
two values match and the command actually tested that checkout. Omit it if the
source moved, the result predates fingerprinting, or the check targeted an
external build. Do not generate a fingerprint later to label an earlier result.
Keep temporary checkpoint input and generated evidence outside the checkout or
in an existing ignored location so those files do not alter the fingerprint.
Use the optional `environment` string for the actual setup, such as
`local seeded database` or `staging build abc123`. Preserve the observed result
and evidence in their original fields.

`resume` returns `check_source_freshness` in the same order as the checks:

- `MATCH` means the recorded check fingerprint matches the current checkout.
- `STALE` means the check fingerprint differs, even if the checkpoint itself matches.
- `UNKNOWN` means no check fingerprint was recorded. Old checkpoints remain readable.

The `git-v2:` format makes earlier snapshots and `git-v1:` check fingerprints
report `STALE`. Rerun affected checks and save fresh fingerprints to reuse their results.

These statuses compare Git state. Revalidate ignored config, dependencies,
submodules, environment, and remote services separately. A fingerprint is not a
transactional lock. An untracked file over 10 MiB aborts snapshotting. Exclude
build outputs appropriately. Use isolation for repositories you do not trust.
