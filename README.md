# Skills For Shipping Someone Else's Ticket

My agent skills, for the part of engineering that isn't typing — reading an ask nobody
finished writing, settling the decisions it hid, and handing back something a reviewer can
trust.

Most agent workflows own the whole process: a pipeline you enter at one end and hope to
exit at the other. When the process breaks, you can't tell which stage broke it. These are
ten small skills instead — each with one job, each usable alone, each naming the next.
Take three and ignore the rest. Rewrite the ones you keep.

They fire on their own. Say "this is broken" and `debug` runs; finish a change and `ship`
writes the handoff. No invocation ceremony.

## Quickstart

Claude Code:

```sh
claude plugin marketplace add formesean/skills
claude plugin install skills@formesean
```

Codex:

```sh
codex plugin marketplace add formesean/skills
codex plugin add skills@formesean
```

Skills namespace as `skills:<name>`. There's no setup step and no per-repo config — every
skill derives what it needs from the repo it runs in.

## Why These Skills Exist

Each one exists because of a specific way work goes wrong. Not hypothetically.

### #1: Building The Wrong Thing, Correctly

> "The hardest single part of building a software system is deciding precisely what to build."
>
> Fred Brooks, [The Mythical Man-Month](https://www.amazon.com/Mythical-Man-Month-Software-Engineering-Anniversary/dp/0201835959)

**The Problem**: A ticket reads clearly, so the work starts. But the title was written by
someone who already knew the answer, and left out everything they considered obvious.
Nobody wrote down the gap. It surfaces in review, after the code exists.

**The Fix**: [`frame`](skills/frame/SKILL.md) turns the ask into numbered acceptance
criteria — and marks which ones you inferred rather than read. The marked ones are the
whole point. That's the list you send back before deciding anything.

### #2: Decisions Made Silently, Mid-Build

**The Problem**: The plan looked finished because nothing had contradicted it yet. Then a
choice nobody phrased as a question got answered by whoever happened to be typing at the
time. It's load-bearing now, and undocumented.

**The Fix**: [`pin`](skills/pin/SKILL.md) interrogates the plan one question at a time,
each with a recommendation attached, until no remaining choice would change what gets
built. One at a time matters — a wall of six questions gets answered as vibes.

[`plan`](skills/plan/SKILL.md) then turns settled decisions into the smallest build order
that works, each step ending in something you can actually run.

### #3: Fixing The Symptom, Refiling The Bug

> "Debugging is twice as hard as writing the code in the first place."
>
> Brian Kernighan, [The Elements of Programming Style](https://www.amazon.com/Elements-Programming-Style-2nd/dp/0070342075)

**The Problem**: A bug report names a symptom. The symptom is where it surfaced, not where
it broke. A patch at the call site closes the ticket and reopens it next month under a
different caller — and every sibling caller was broken the whole time.

**The Fix**: [`debug`](skills/debug/SKILL.md) refuses to edit until the cause is named in
one sentence, then fixes where the callers converge. The siblings nobody filed heal too.

### #4: "Done" Meaning "I Think It Works"

> "Testing shows the presence, not the absence of bugs."
>
> Edsger W. Dijkstra

**The Problem**: The summary is green because the person who wrote the code also wrote the
summary. Nobody ran anything. The gap between those two facts is where the incident lives.

**The Fix**: [`verify`](skills/verify/SKILL.md) runs the smallest gate that actually covers
the diff, pastes failures verbatim, and never reports green on a command it didn't run.
[`ship`](skills/ship/SKILL.md) then derives the branch name and commit message from what
the repo already does — and never pushes. The push stays yours.

### Summary

None of this is new. It's the discipline you'd apply if you weren't in a hurry, written
down so the agent applies it while you are.

## Reference

Don't know which one you need? **[which](skills/which/SKILL.md)** takes the situation and
names one skill. It routes and stops — it never does the work it points at.

The rest split on one axis — where they sit in the work. **The loop** runs in order, ticket
to handoff. **Entry points** are where real work actually starts, each routing into the loop
at the right place.

### The Loop

- **[frame](skills/frame/SKILL.md)** — Someone else's ask. Recover what "done" means as numbered criteria, mark what you inferred, name what's under-specified.
- **[pin](skills/pin/SKILL.md)** — Before building. Interrogate the plan one question at a time, each with a recommendation, until every decision is settled. No code.
- **[plan](skills/plan/SKILL.md)** — Decisions settled. Turn them into the smallest build order that works, in dependency order, each step checkable.
- **[implement](skills/implement/SKILL.md)** — Plan in hand. Build it step by step, check each one, and stop when reality contradicts the plan instead of improvising past it.
- **[verify](skills/verify/SKILL.md)** — Before calling it done. Smallest gate that covers the diff, residue check on the added lines, repro steps. Verifies, never fixes.
- **[ship](skills/ship/SKILL.md)** — Handoff. Branch name and Conventional Commit derived from the repo's own history, plus manual test steps. Never pushes.

### Entry Points

- **[answer](skills/answer/SKILL.md)** — A question from outside engineering. Reply from the code, in their language, with the evidence you'd need if it's challenged — without turning it into a change.
- **[debug](skills/debug/SKILL.md)** — Something is broken. Diagnose to root cause before editing, then fix once at the choke point where the callers converge.
- **[review](skills/review/SKILL.md)** — Audit a diff, branch, or repo. Evidence-backed findings, one line each, ranked by leverage. Reports, never repairs.

Each skill names its neighbors, so the handoff is automatic — `frame` routes open decisions
to `pin`, `debug` routes a confirmed new ask back to `frame`, `answer` refuses to fix and
points at whichever one owns it.

## Layout

```
.claude-plugin/     Claude Code manifests (plugin + self-marketplace)
.codex-plugin/      Codex manifest
skills/<name>/SKILL.md
```

Both platforms read the same `skills/` directory. One file per skill, one method, no
per-platform forks — the drift between duplicated copies is the thing this layout exists to
prevent.

## License

MIT. Fork it, cut what you don't use, rename the rest.
