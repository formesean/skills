---
name: pin
description: Interrogate a plan one question at a time until every decision is settled and named, then stop — no code. Use before implementing anything non-trivial, and whenever the user says "pin this down", "grill me", "stress-test this plan", "poke holes in this", "am I missing anything", or presents an approach for a gut check. To diagnose something broken, use `debug`; to audit code that exists, use `review`.
---

# pin

An unpinned plan looks finished because nothing has contradicted it yet. The decisions
that will actually cost you are the ones nobody phrased as a question.

The deliverable is a settled set of decisions, not a summary of the conversation and not
code. You are done when there is no remaining choice whose answer would change what gets
built.

## Rules

- **One question at a time.** Ask, wait, then use the answer to pick the next question.
  A batch of six is a form, not an interview — it gets three skimmed answers and buries
  the one that mattered.
- **Recommend an answer with every question.** State your pick and the one reason for it.
  A bare "what do you want to do about caching?" hands the work back. "I'd cache in
  Postgres — you already run it and Redis is a new dependency. Agree?" gets a decision in
  one exchange.
- **Look up facts. Ask only decisions.** Which files exist, what the schema is, whether a
  dependency is installed, what the current behavior does — read them. Asking a question
  the filesystem answers spends the user's attention on your homework.
- **Follow the dependency order, but chase branches.** Ask what unblocks the most
  downstream questions first — settling transport before the data model means asking it
  twice. An answer that reveals an unconsidered case outranks your next planned question;
  follow it down before returning.
- **Write down what's settled, in their words.** Not paraphrased into your framing. The
  gap between what they decided and what you recorded is what you'll build wrong.
- **Never write code.** Not a sketch, not a "here's roughly what I mean" snippet. Code
  ends the interview — the user reviews the code and the unasked questions ship unasked.
- **Stop when it's pinned, not when it's exhausted.** Questions with no consequence for
  the build are noise. If both answers produce the same code, don't ask.

## Method

### 1. Read before asking

Establish the ground truth yourself: the relevant files, the existing patterns, the
`README` and `CLAUDE.md`/`AGENTS.md`, what's already installed.

You are looking for two things — what this codebase already decided (so you don't ask it
again), and where the proposal contradicts it (that contradiction is your first question).

Where the work came from someone else's ticket or message, frame it first — `frame` turns
it into criteria and names what's under-specified. Interrogating decisions on top of an ask
nobody restated settles the wrong questions carefully.

### 2. Map the decision tree

Before the first question, list the choices the plan actually contains, including the
ones it made silently. The silent ones are the productive ones: the plan says "store the
result" and never says where, for how long, or what happens when two writers race.

Then order by dependency. Root first — the decision whose answer prunes the most branches.

### 3. Interrogate

For each unsettled decision, in order:

> **Question.** The concrete choice, not an open prompt.
> **Recommendation.** Your pick, one sentence of why.
> Then stop and wait.

Push where the answer is thin. "It'll be fine" is not a decision — ask what happens in
the case that makes it not fine. Pinning means the user has actually considered it, not
that they said something.

Sweep for the ones plans routinely skip, and ask only the ones that bite here:

- **Failure** — what happens when this call fails, half-succeeds, or runs twice?
- **Boundary** — empty, one, many, concurrent, malicious.
- **State** — who owns it, what's the source of truth, what goes stale.
- **Migration** — what's already in the database, in flight, or on someone's screen.
- **Scope edge** — what's explicitly *not* in this change, and what breaks if that
  assumption is wrong.
- **Reversal** — how do you undo it after it ships.

### 4. Confirm

Play back the settled decisions as a list and ask for confirmation before anything gets
built. What you heard and what they meant diverge more often than either party expects,
and this is the cheapest place to catch it.

If they change an earlier answer, re-walk the branches that hung off it — a downstream
decision settled under the old answer is no longer settled.

## Output

```
DECIDED:
  <decision> → <the answer, in their words>
  ...
OPEN:     <what's deliberately unresolved, and what would settle it — or "none">
ASSUMED:  <what you proceeded on without asking, and why it was safe>
NEXT:     <the first thing to build — one line>
```

`OPEN` is not a failure. A decision deferred on purpose, with the trigger named, is
pinned. A decision nobody noticed is not.

Then stop. Building is a separate pass the user starts.

The user says "just build it" mid-interview? Report what's still `OPEN`, state the
assumption you'll build under, and go. Their call — but an unnamed assumption is how a
plan gets implemented wrong and nobody can point to where.
