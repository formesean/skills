---
name: which
description: Name the one skill that fits the situation, and where it hands off next. Use when the user asks "which skill", "what should I use here", "where do I start with this", "what do I run next", or describes a situation without naming a skill and the right entry point isn't obvious. Routes only — it never does the work it routes to.
---

# which

Nine skills that cross-reference each other have no front door. Someone holding a ticket,
a stack trace, or a half-finished branch has to already know the set to pick from it.

The deliverable is one name and one line of why. Not a tour of the catalogue, and not the
work itself.

## Rules

- **Name one skill.** The whole value is collapsing nine options to one. "You could use
  `frame` or `pin`" hands the choice back with extra steps — pick, and say what would
  change your pick.
- **Route, never execute.** Naming `debug` and then diagnosing the bug defeats the point:
  the user asked which door, and you walked them through it before they chose. Stop at
  the name.
- **Route from the situation, not the vocabulary.** "Review this" from someone holding a
  bug report means `debug`, not `review`. What they have in hand beats what they called it.
- **Ask when the situation is genuinely ambiguous.** One question, not a form. "Is this
  broken now, or are you checking whether it's right?" separates `debug` from `review` in
  one exchange.
- **Say when the answer is no skill.** A one-line change, a question you can answer
  directly, a task none of these cover — say so. Routing into a skill that then reports
  "this didn't need framing" wastes a full pass.
- **Name the handoff, not the whole loop.** One skill and what comes after it. Reciting
  all six loop stages to someone who asked where to start buries the answer.

## Method

### 1. Establish what they're holding

The artifact decides the route, so identify it first — and ask if it isn't clear:

- Someone else's ticket, message, or screenshot → `frame`
- A failure: stack trace, wrong output, red CI → `debug`
- A question from outside engineering → `answer`
- An approach or plan not yet built → `pin`
- Settled decisions, nothing written → `plan`
- A written plan → `implement`
- A finished diff → `verify`
- A green gate → `ship`
- Existing code, nothing known broken → `review`

### 2. Check the two pairs that get confused

Most mis-routes are one of these:

- **`debug` vs `review`** — is something known-broken, or are you auditing? Broken is
  `debug`. Not-known-broken is `review`, even when you suspect there's a bug in there.
- **`frame` vs `pin`** — is the ask unclear, or are the decisions unsettled? Not knowing
  what "done" means is `frame`. Knowing what done means but not how to build it is `pin`.

A third, less often: **`verify` vs `review`**. Verify runs commands and reports pass/fail.
Review reads code and reports findings. "Is this ready to ship" is `verify`.

### 3. Route

Name the skill, one line of why, and what it hands to next.

Where the situation spans several — a ticket that's also broken, a plan that's also
unclear — name the one that comes first in the work, not the one that covers the most.
The skills route to each other on their own from there.

## Output

```
USE:   <skill>
WHY:   <one line — what you're holding, and what that skill turns it into>
THEN:  <the skill it hands to next — omit if it's terminal>
```

Ambiguous? Ask the one question that separates the candidates, then route. Don't emit a
`USE:` line you're not confident in — a wrong route costs a whole pass before anyone
notices.

No skill fits? Say so plainly and answer the underlying question directly if you can.
