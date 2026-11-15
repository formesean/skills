# Project verification and QA handoff

Prefer an existing project runbook, smoke command, test fixture, or browser suite.
If the same feature repeatedly takes setup discovery, write one short project-local
recipe next to the existing checks. Start with the feature under review.

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
