---
name: debug
description: Diagnose a failure to its root cause before changing anything, then fix once where the callers converge. Use when something is broken, throwing, returning wrong values, failing in CI, or behaving differently than expected, and whenever the user says "debug", "why is this failing", "this is broken", or pastes a stack trace or error output. To audit code that isn't known-broken, use `review` instead; to answer someone asking whether something is a bug, use `answer` first.
---

# debug

A bug report names a symptom. The symptom is where it surfaced, not where it broke.
Find the break, not the surface.

A fix's value is whether the bug stays dead. A patch at the call site closes the ticket
and refiles it next month under a different caller; a fix at the choke point closes the
ones nobody filed yet.

## Rules

- **No edits until the cause is named.** A fix written before diagnosis is a guess with
  a diff attached. If you cannot state the cause in one sentence, keep reading.
- **Reproduce first, or say you couldn't.** An unreproduced bug is a hypothesis. Working
  from a trace alone is legitimate — pretending that's the same as reproducing is not.
- **Read the actual code.** Not what the function is named, not what the docstring
  claims, not what the variable implies — what it does with the input in question.
- **Never patch the reporting path alone.** The ticket names one caller; the bug lives
  where the callers converge. Fix there and the siblings heal with it.
- **Suspect your own last change first.** Recently touched code fails more than stable
  code. `git log` and `git diff` before theorizing about the framework.
- **Say what you ruled out.** A cause you eliminated is worth reporting — it's the map
  of where the next person shouldn't look.
- **Never print a secret value.** A trace or config carrying a credential gets cited by
  `file:line` and type, with rotation recommended. Pasting the value spreads it.

## Method

### 1. Reproduce

Get the failure in front of you: the failing test, the command, the exact input. Capture
the error verbatim — full stack trace, not a summary. The detail you paraphrase away is
the one that names the cause.

Pin down when it fires: every run, or one in fifty? One environment, or all of them?
An intermittent bug is a different animal from a deterministic one, and treating the
first like the second produces a fix that appears to work.

Can't reproduce? Say so explicitly and name what's missing — env, data, credentials,
device, timing. Then work from the trace alone and mark every conclusion unverified.

### 2. Locate the break

Read the trace bottom-up: the deepest frame in *your* code is the starting point, not
the top-level handler that caught it.

Narrow by bisection, not by reading everything:

- Where is the value still correct? Where is it already wrong? The break is between.
- `git log -S'<symbol>' -- <path>` and `git bisect` when it used to work.
- Add a temporary assertion or log at the midpoint; delete it before finishing.

The gap between "the value is wrong here" and "this line makes it wrong" is where
debugging actually happens. Don't close it by assuming — close it by reading the code
that runs between the two points.

State the cause in one sentence before continuing: *"`x` is undefined here because
`load()` returns early on empty input and the caller doesn't check."*

If you can't write that sentence, you have a suspicion, not a cause. Keep reading.

### 3. Find the choke point

Before editing, map who else hits this:

```bash
rg -n '<function name>' --type <lang>    # every caller
rg -n '<the buggy pattern>'              # every sibling instance
```

Then pick where to fix:

- Many callers, one broken assumption → fix inside the shared function. One guard beats
  N guards, and it covers the callers nobody filed a ticket about.
- The shared function is correct and one caller misuses it → fix that caller, then ask
  whether the API invites the mistake. If it does, that's a second finding worth naming.
- The same wrong pattern copy-pasted in several places → fix all of them now, or fix one
  and list the rest explicitly. Silently fixing one is how a bug gets refiled next month.

### 4. Fix

Smallest change that removes the cause. Not a workaround at the call site, not a
try/catch that swallows it, not a defensive check layered over a value that should never
have been wrong in the first place.

If the real fix is large and you're shipping a stopgap, say so plainly and name what the
proper fix is. An unlabelled stopgap becomes permanent.

Resist the cleanup you notice on the way. Unrelated tidying in a bugfix diff hides the
one hunk that matters from whoever reviews it — note it separately instead.

### 5. Prove it

Leave behind one check that **fails without the fix**. Verify that claim — revert the
fix (mentally or actually) and confirm the check would catch it. A test that passes both
ways proves nothing, and it's the most common way a bugfix ships broken.

Pin the cause, not the symptom: assert the behavior that was wrong, not the stack trace
that surfaced it. Prefer the repo's existing test setup. No test infrastructure and none
warranted? A runnable assertion or the exact command with expected output works.

Then run the smallest gate that covers the change: the affected test file, plus typecheck
if signatures moved. One command at a time.

## Output

```
CAUSE:  <one sentence — the actual mechanism, not the symptom>
WHERE:  <file:line — where it breaks, not where it surfaced>
BLAST:  <other callers or sibling instances affected, or "none — single caller">
FIX:    <what changed, and why there rather than at the call site>
PROOF:  <the check, and confirmation it fails without the fix>
RULED OUT: <plausible causes eliminated — omit if none were seriously considered>
```

Couldn't reproduce it? Say so in `CAUSE:` and mark the line `unverified`. A diagnosis
from a trace alone is useful; one dressed up as confirmed is not.

Unresolved? Report what you ruled out and the single next step that would settle it,
rather than a fix you can't defend. Handing back a narrowed problem beats handing back
a confident guess.
