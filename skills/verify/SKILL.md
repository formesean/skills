---
name: verify
description: Last gate before "done" — run the smallest quality gate that covers the diff, grep the added lines for residue, and write the manual test steps. Verifies, never fixes. Use before declaring any multi-file change complete, before proposing a commit, and whenever the user says "verify this", "is this ready", "preflight", or asks for repro steps. To audit code for findings use `review`; to diagnose a failure use `debug`.
---

# verify

The gate between "I think it works" and "it's done". Everything here is a check you can
run and a result you can paste — no judgment, no opinion about the design.

Verify, don't fix. The moment you start repairing, you stop verifying, and the failure
you were one command away from finding ships behind a green summary you wrote yourself.

## Rules

- **Failures verbatim.** Paste the command's actual output — the error, the file, the
  line. A summarized failure is a failure someone has to reproduce before they can act
  on it, and the detail you paraphrased away is usually the cause.
- **Never report green on a command you didn't run.** Not "should pass", not "tests look
  fine". Ran it and it passed, ran it and it failed, or couldn't run it and here's why.
- **One command at a time, sequentially.** Wait for each to exit before starting the next.
  Never parallel, never backgrounded — stacked runs exhaust memory and the failure you
  get back is the machine's, not the code's.
- **Scope to the diff — commands and greps both.** Pass the changed paths to the linter,
  typechecker, and test runner; grep `+` lines only. A whole-repo run buries your failure
  in unrelated ones, and flagging inherited residue bills this change for old debt.
- **Pre-existing failures are not this change's problem.** Name them, separate them, move
  on. But say them out loud — a failure you silently tolerated is one the next person
  assumes you caused.
- **Verify, don't fix.** Found a violation? Report it with `file:line`. Applying the fix
  is the next pass, and it needs its own gate run afterward anyway.
- **Never print a secret value.** Cite `file:line` and the credential type, recommend
  rotation. A verification report gets pasted into tickets and chat.

## Method

### 1. Establish the change set

```bash
git status
git diff                 # unstaged
git diff --staged        # staged
```

Clean worktree? The change is already committed — use `git diff <base>...HEAD` against the
branch point instead.

You need the actual added lines, not a description of the work. The diff is what ships;
the conversation about it is not.

### 2. Classify, then pick the gate

Read the diff and stop at the narrowest band that covers it. Each band adds to the one
above it; none of them replaces scoping with breadth.

- **Comments, docs, markdown, copy strings only** → lint the changed files. Stop there.
- **Types, interfaces, or signatures touched** → also typecheck.
- **Logic changed** → also tests, scoped to the affected files. Use the runner's
  related-tests flag where it has one (`jest --findRelatedTests <files>`,
  `vitest related <files>`, `pytest <path>`); no such flag → run the test files covering
  the changed modules.

Always pass the changed paths, and use the repo's own scripts — a command you invented is
a command that passes for reasons unrelated to whether the change is correct. Where a tool
only runs repo-wide (many typecheckers have no file-scoped mode), run it and report only
the errors in the changed files.

Whole-repo runs are an escalation, not a band. Reach for one only when the scoped run
structurally cannot see the risk — a widely-imported module where breakage lands two hops
past the direct importers, a change with no test file to scope to, or the user asked.
Then take the narrowest expansion that covers it, and say what forced it.

Say which band you chose and why, in one line. That sentence is what lets someone disagree
with the scope instead of just trusting it.

### 3. Grep the added lines

Over `+` lines only:

- **New configuration reaching outside the process** — a new env var, a new dependency, a
  new migration. Each needs explicit approval before it lands, so each is a finding here
  even when it's correct.
- **Residue** — debug prints and logging left behind, commented-out code, narrative
  comments explaining what the diff already says.
- **Hardcoded production values** — real emails, live URLs, account IDs reachable outside
  an environment branch.
- **Ungated writes** — a destructive or outbound operation the diff introduces with no
  dry-run path and no confirmation.
- **Sibling gaps** — the diff fixes one instance of a repeated pattern. `rg` the pattern
  and list every sibling still unfixed. This is the check that catches the bug getting
  refiled next month under a different caller.

### 4. Write the repro steps

Numbered, concrete, runnable by someone who didn't write the change: where to go, what
role or account to be in, the action, the expected result.

Include one negative check — the case that should fail, be rejected, or show an error.
A test plan that only walks the happy path verifies that the feature exists, not that it
works.

Anything only the user can run — a real device, a live email, a production flag, a
credential you don't have — goes under `manual-only` rather than being written as though
you'd done it.

## Output

```
VERIFY: PASS | FAIL
GATE:   <band chosen + why, one line — and if the run was widened past the band, what forced it>
        <command> → <result>
        <verbatim failure output, if any>
ADDED:  <violations with file:line — or "clean">
PRE-EXISTING: <failures already there before this change — omit if none>
STR:    1. <step> → <expected>
        2. ...
MANUAL-ONLY: <steps only the user can run — or "none">
```

`PASS` requires all three: the gate green, zero violations in added lines, and repro steps
written. Anything else is `FAIL` — and a `FAIL` leads with the shortest path back to green,
not with a list of everything wrong.

Couldn't run the gate at all — no test runner, missing credentials, a broken install? That
is `FAIL` with the reason named. An unverified change reported as verified is the exact
outcome this skill exists to prevent.

A `PASS` goes straight to `ship` — the branch name, commit message, and handoff. Don't wait
to be asked for it.
