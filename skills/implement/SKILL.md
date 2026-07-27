---
name: implement
description: Build a plan into working code, one step at a time, checking each before starting the next — and stopping when reality contradicts the plan instead of improvising past it. Use when a plan exists and it's time to write the code, and whenever the user says "implement this", "build it", "go ahead", or hands you a plan file or a numbered list of steps. To settle decisions first use `pin`, to write the build order use `plan`, when something breaks mid-build use `debug`.
---

# implement

The plan already made the decisions. Your job is to land them without quietly making new
ones — and to stop the moment the code contradicts what the plan assumed.

A build that deviates silently is worse than one that halts. The halt costs a question;
the silent deviation ships something nobody chose and gets discovered by a reviewer, or
by production, long after the reasoning is gone.

## Rules

- **One step at a time, checked before the next.** The check on step 2 is what tells you
  step 1 actually worked. Batching four steps and running one check at the end means a
  failure you can't localise and a diff you have to bisect by hand.
- **Deviations get surfaced, never absorbed.** The plan says a function exists and it
  doesn't; the shape it assumed is wrong; the check fails for a reason the plan didn't
  name. Say so, then take the smallest correction — or stop, if the correction is a
  decision rather than a detail.
- **Build what the step says.** Not the refactor you noticed, not the adjacent bug, not
  the test suite that should exist. Those go in the report as `NOTICED`. A diff carrying
  unrequested work hides the hunk that matters from whoever reviews it.
- **Match the surrounding code.** Its naming, its error handling, its layering, its
  comment density. New code that reads as foreign is a finding in the next review, even
  when it's correct.
- **Reuse before writing, and no scaffolding for later.** Something here already does it →
  call it. Stdlib or the platform → use it. Installed dependency → use it. Only then new
  code. Never add a dependency, env var, or migration without asking first, and never an
  interface with one implementation or a seam for a case that hasn't arrived.
- **Never report a step done on a check you didn't run.** "Should pass" is not a result.
  If you couldn't run it, say which one and why.
- **Leave no residue.** No debug prints, no commented-out code, no narrative comments
  explaining what the diff already says, no temporary assertions you added to bisect.
- **Never print a secret value.** Cite `file:line` and the credential type, recommend
  rotation, and keep going.

## Method

### 1. Load the plan

Read it fully before writing anything — including the `RISK`, `ASSUMED`, and `STOP IF`
lines. Those are the parts that tell you when to stop, and they are worthless read after
the fact.

No plan, and the change touches more than one file? Run `plan` first. A verbal "just add
X" for a multi-file change is a plan that exists only in the user's head, and the parts
you can't see are the parts you'll get wrong.

Then confirm the plan still describes the repo. It was written against a commit; files
move. Open the paths it names and verify they exist and look as described. A plan that
has drifted is caught here in one minute or discovered in step 4 with half a diff written.

### 2. Verify the gate before you need it

Find the repo's own commands — the `package.json` scripts, the `Makefile` targets — and
run the relevant one *before* changing anything.

You are establishing what a clean tree looks like. Walking into pre-existing failures and
attributing them to your diff wastes an hour; discovering them after four steps means you
can't tell which failures you caused.

Pre-existing failures? Name them now, in the report, and carry on. They are not yours to
fix in this pass.

### 3. Build one step

For each step, in order:

1. Read the code the step touches — the actual current state, not the plan's description
   of it. The plan is a map; the file is the territory.
2. Make the smallest edit that satisfies the step.
3. Run the step's check.
4. Say what happened in one line, then start the next step.

Failing check? Read the error before editing. If the cause is your last edit, fix it. If
the cause is something the plan didn't anticipate, that is a deviation — go to step 4.

Don't reach for the next step while the current check is red. A second edit on top of an
unexplained failure is how one small problem becomes two entangled ones.

### 4. Handle the deviation

The code will contradict the plan somewhere. What matters is which kind:

- **Detail** — the function is named differently, the import path moved, the type needs a
  cast the plan didn't mention. Take the smallest correction, note it, keep building.
- **Decision** — the plan's approach doesn't work here, a step needs a dependency, the
  shape assumed doesn't exist, two steps turn out to be one. Stop. Report what you found
  and what it costs. This is the user's call, and guessing at it converts their plan into
  yours without telling them.
- **`STOP IF` fired** — stop, whatever else is true. That line exists because someone
  predicted this exact moment and decided they wanted to hear about it.

Something is broken in a way the plan didn't cause — a pre-existing bug in a path you now
depend on? Switch to `debug`. Diagnosing to root cause inside an implementation pass
produces a diff that does two things badly.

### 5. Run the gate

Smallest gate that covers what you changed, using the repo's own scripts — one command at
a time, sequentially, never parallel or backgrounded. Pass the changed paths to every
command; a whole-repo run is an escalation you justify, not the default. `verify` owns the
full procedure: which band the diff falls in, the residue grep over added lines, and the
repro steps.

A red gate means the step isn't done. Fix it, or report it red — never report it green.

### 6. Confirm the goal

Re-read the plan's `GOAL` and check it against what the code now does, not against your
list of completed steps. Every step passing and the goal unmet is the normal way a build
fails, and only this reading catches it.

Then check the reverse: does the diff contain anything no step asked for? If yes, either
remove it or name it in the report.

## Output

```
BUILT:   <step> → <what landed, file:line> · <check> ✓
         ...
DEVIATED: <where the code contradicted the plan, and the correction — or "none">
GATE:     <command run> → <result>
GOAL:     <met | not met — measured against the plan's GOAL, not the step list>
NOTICED:  <what you saw and deliberately did not touch — omit if nothing>
```

Then the handoff, unprompted: branch name, Conventional Commit message, and numbered
manual test steps.

Stopped partway? Report the steps that landed, the exact one you stopped on, and what
decision would unblock it. A half-built change reported honestly is resumable; one
reported as done is a trap for whoever opens the file next.
