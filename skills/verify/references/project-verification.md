# Project verification and QA handoff

Prefer an existing project runbook, smoke command, test fixture, or browser suite.
If the same feature repeatedly takes setup discovery, write one short project-local
recipe next to the existing checks. Start with the feature under review. When creation
is authorized, use the compact template below; inspection-only work reports the gap
without writing files. Reuse existing fixtures and runners rather than adding a framework.

1. **Prepare** the intended build, isolated test data, required roles and feature
   flags. Confirm the application is ready to exercise with relevant dependencies.
2. **Exercise** the entry point the ticket describes. Include a positive path and
   the negative path that would catch the defect when both matter. Record expected
   and observed behavior and relevant side effects, such as a queued job, database
   transition, or badge count. Use existing fixtures or safe test modes for outbound
   effects and explain which effects were observed.
3. **Capture** the check command or steps, tested revision or build, environment,
   and shortest useful evidence. Local evidence applies to the local run. If a
   check depends on staging data or a deployed build you could not inspect, mark it
   blocked or unrun and name the exact staging check.
4. **Hand off** results by acceptance criterion. Give QA only the setup, actions,
   expected outcomes, and open checks they need. If a confirmed regression could
   recur, choose the existing test boundary that would catch it and run the check
   on the faulty and corrected versions when feasible.

| Criterion | Check and observed result | Source and environment | QA follow-up |
| --- | --- | --- | --- |
| AC1: eligible user sees a badge | Seeded browser journey: badge appears | Local build, revision recorded | Check staging only if deployment or staged data is in scope |
| AC2: basic strategy gets no step notification | Current path passes; legacy row case unrun | Local fixture omits legacy rows | Seed a legacy row and inspect dispatch and badge contribution |

For reusable local checkpoint evidence, capture the harness fingerprint around the
run as described in the harness protocol. On resume, check `check_source_freshness`
for the specific result. Treat a stale or unknown result as historical evidence,
even when the checkpoint itself matches.

## Reusable project recipe

Store this beside the project's existing tests/runbook, not in the shared skill pack.
Replace placeholders with inspected paths and commands; run them before calling the
recipe verified. If setup is unavailable, label it unrun and name what is missing.

```text
Target: <criterion IDs, entry point, supported local/test environment>
Prepare: <required dependencies, test roles/flags, isolated fixture/reset command>
Reproduce: <exact command or user actions, deterministic inputs>
Assert: <expected positive/negative outcomes and observable side effects>
Cleanup: <remove only this run's data/artifacts; safe repeat procedure>
Evidence: <command, exit/result, tested revision/build, environment, short observation>
Limits: <mocked effects, missing coverage, staging-only follow-up>
```

Check that reset/cleanup is scoped to disposable test data before executing it. Use
a test sink for messages/payments and never embed credentials or production records.
For a regression, demonstrate failure on the faulty version and success on the fix
when feasible; otherwise disclose the missing before-fix proof. Link the recipe from
the project runbook so later debug/verify sessions can find it.
