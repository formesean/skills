# Behavioral evaluation

Static validation does not measure model behavior. `cases.json` contains scenario
prompts and separate grading criteria. Use disposable fixture repositories for cases
that require edits; do not run evaluations against a production checkout.

For each run:

1. Start a fresh session with the chosen skill and the prompt, plus only required raw
   fixture files. Do not expose `must`, previous outputs, the diagnosis, or the audit.
2. Keep model/version, effort, tools, host guidance, fixture commit, and permissions
   constant when comparing baseline and candidate. Record both exact revisions per run;
   `d3b07fb` is the original baseline, not the baseline for every future change.
3. Capture final output, tool trace, actual diff, commands/exits, duration, input/output
   tokens, cached tokens, retries, and user questions when the runtime exposes them.
   Use null for unavailable telemetry, never zero. Inspect actions, not just prose.
4. Grade each `must` independently with evidence. A forbidden side effect fails the
   case regardless of how polished the final answer looks. Human-check judge outputs.
5. Run multiple independent trials (start with 3 per case), then add held-out real
   tickets. Compare completion rate, false claims, scope violations, prompts for user
   input, and total/cached tokens. Do not accept token savings that lower task success.

No paid API runner or model credentials are required for repository checks. This suite
is an evaluation protocol, not an automated claim that every case passes. See
`results-2026-11-14.md` for the limited observations actually collected.

For a small workflow smoke pass, select `ticket-ambiguous`, `qa-chat-followup`,
`blocked-repro`, `checkpoint-stale-check`, `personal-idea`, `delegated-verification`,
and `compact-memory`. Supply the protocol only for cases that request it. Keep grading
criteria out of worker prompts. Record each case as PASS/FAIL/BLOCKED with evidence
for each requirement. Track missed requirements, unsupported claims, scope violations,
and unnecessary questions separately. Text-only cases measure response behavior;
they cannot establish tool execution, installation, or real-project success.

[Workflow smoke results](results-2026-11-16.md) record the seven single-trial response checks and their limitations.
