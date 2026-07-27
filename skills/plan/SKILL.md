---
name: plan
description: Turn settled decisions into a written build order — the smallest change that works, in dependency order, self-contained enough to hand off. Use before implementing anything that touches more than one file, and whenever the user says "plan this", "how would you build this", "write it up before you code", or asks for an implementation plan or roadmap. To settle the decisions first, use `pin`; to audit code that exists, use `review`.
---

# plan

A plan is not a description of the finished thing. It is the order you build it in, and
the shortest path through it that a reader who was not in this conversation can walk.

Most plans fail in one of two directions: they specify a system nobody asked for, or they
specify nothing checkable and get read as vibes. The fix for both is the same — write the
smallest change that satisfies the ask, and make every step end in something you can run.

## Rules

- **Read the code before planning against it.** Every file the change touches, the actual
  flow end to end. A plan written from the file names is a guess with headings on it, and
  it is the most expensive kind of wrong — the reader trusts it and builds it.
- **Plan only what was asked.** The migration you noticed, the tests that don't exist,
  the naming you'd change — those go in a `LATER` line, not into the build order. A plan
  that quietly triples the scope gets abandoned rather than argued with.
- **Take the smallest thing that works.** Something in this repo already does it → reuse
  it. Stdlib or the platform does it → use that. An installed dependency does it → use
  that. Only then write new code, and never add a dependency for what a few lines cover.
  No speculative structure either — no interface with one implementation, no config for a
  value that never changes, no seam "for when we need it." Later will know more than you.
- **Order by dependency, not by area.** Each step should compile, run, and be checkable
  on its own. If step 3 only makes sense once step 5 lands, the order is wrong.
- **Every step ends in a check.** The command to run and what it should say. A step whose
  completion is a matter of opinion is where the build silently goes off-plan.
- **Write for someone with no context.** No "as discussed", no "the pattern above". Paths,
  symbols, and the existing file to copy the convention from — named, in the step.
- **Name what you're not sure about.** An assumption you flag costs one question; an
  assumption you bury costs a rewrite.
- **No code beyond a signature.** A type, a function signature, a config key — fine.
  Writing the implementation into the plan means it gets reviewed as prose and shipped
  unread.
- **Never print a secret value.** Cite `file:line` and the credential type, and note
  rotation. Pasting the value into a document that gets shared spreads it.

## Method

### 1. Establish ground truth

Read before writing: the `README`, `CLAUDE.md`/`AGENTS.md`, the files the change touches,
their callers, the neighbouring code that already does something similar.

Collect the repo's own gates while you're here — the `package.json` scripts, the
`Makefile` targets, how tests are actually run. Those become the check line on every step.
A plan that invents its own verification commands gets ignored at the first one that fails.

You are looking for what already exists that you can use, and what convention the new code
has to match. Both go into the plan by name.

### 2. Settle the shape

State the approach in two or three sentences before decomposing it. If you can't, you
don't understand the change yet — go back to step 1.

Then take the smallest version that satisfies the ask. Walk it down deliberately: does
this piece need to exist at all, is it already here, does the stdlib or the platform cover
it, does something already installed cover it, can it be one line. Stop at the first
answer that holds.

Where a decision is still open, name it and pick a default. A plan blocked on a question
nobody asked is a plan that doesn't get built — recommend, mark it, and keep going.

If the decisions were never settled in the first place, stop and run `pin`. Planning on
top of unsettled decisions produces a build order that gets rewritten on the first answer.

### 3. Decompose

Break the change into steps that each land something real. The test is whether you could
stop after any step and the repo is still coherent.

Each step names:

- **What** — the concrete edit, by path. `src/auth/session.ts` — add `maxAge` to the
  cookie options, not "improve session handling."
- **Why here** — one clause, only when the location isn't obvious. Where callers converge,
  or which existing file it mirrors.
- **Check** — the command and the expected result.

Order them so each depends only on what came before. Where two steps are independent, say
so — that's where the work can split.

Three steps is a normal plan. Ten steps usually means the scope grew while you were
writing, or that steps are being split at boundaries the code doesn't have.

### 4. Find what bites

Before you call it done, walk the plan against the cases plans routinely skip. Include
only what actually applies here — a risk section listing everything is a risk section
nobody reads.

- **Blast radius** — `rg` the symbols you're changing. A signature that moves and leaves
  callers behind is the bug that ships.
- **Failure** — what happens when the new path fails, half-succeeds, or runs twice.
- **Migration** — what's already in the database, in flight, or on someone's screen.
- **Reversal** — how this gets undone after it ships.

Then name the escape hatch: the condition under which the builder should stop and come
back rather than improvise. *"If `load()` already handles empty input, skip step 2 and
say so"* is worth more than another paragraph of specification.

## Output

```
GOAL:  <what is true when this is done — one sentence, checkable>
SHAPE: <the approach in two or three sentences>

1. <path> — <the edit>
   check: <command> → <expected>
2. ...

RISK:    <the one or two things that actually bite here — or "none beyond the steps">
ASSUMED: <what you decided without asking, and what would change if wrong>
LATER:   <what you deliberately left out, and the trigger that brings it back>
STOP IF: <the condition that means come back rather than improvise>
```

Long or multi-session work, or a plan being handed to another agent? Write it to a file
with the same structure and record the commit SHA it was written against. A plan read a
week later has no conversation behind it — the file has to carry everything.

Then stop. Building is a separate pass the user starts — that's `implement`.
