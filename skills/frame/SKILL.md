---
name: frame
description: Turn a ticket, message, or verbal ask into a numbered list of acceptance criteria — including the implicit ones — and name what's under-specified before any decision gets made. Use at the start of any change that came from someone else, and whenever the user says "frame this", "what is this ticket actually asking", or hands over a ticket key, URL, screenshot, or pasted request. Fetch however the user says to. To settle open decisions use `pin`; to turn settled decisions into a build order use `plan`; if the ask is a question rather than a change, use `answer`.
---

# frame

A ticket is a description of a problem written by someone who already knows the answer.
Your job is to recover what "done" means before anyone starts deciding how to build it.

The expensive failure is not building it wrong. It's building the wrong thing correctly,
because the title read clearly and nobody wrote down what it left out.

The deliverable is a numbered list of acceptance criteria and an honest list of what the
source didn't say. Not a plan, not decisions, not code.

## Rules

- **Fetch however you're told.** A ticket key with a tracker tool available, a URL, a
  pasted body, a screenshot, a forwarded message, a sentence in chat. Use the method the
  user names. No tracker named and nothing pasted? Ask for the source — don't guess at a
  system or invent the contents.
- **Mark every criterion stated or inferred.** Implications count as criteria — a banner
  "on the old page" implies not on the new one — but an inferred requirement you didn't
  mark is indistinguishable from one the author wrote, and gets built with equal
  confidence. Never infer from the title, the component name, or what tickets like this
  usually want.
- **Restate before decomposing.** Two or three sentences in your own words. If you can't,
  you don't have the ask yet — that's the first thing to flag, not something to paper over
  by copying the description back.
- **Exact values are criteria.** Copy, dates, thresholds, recipients, roles, order. "Shows
  a warning" and "shows *this* warning text" are different acceptance criteria, and the
  gap between them is a round trip with whoever wrote the ticket.
- **Audit intent, not wording.** Sources are informal, abbreviated, mixed-language, or
  written in a hurry. Frame what they mean. Where meaning is genuinely ambiguous, that's
  an `UNCLEAR` line, not a coin flip.
- **Separate the ask from the context.** Background, history, and "while we're in there"
  asides are not criteria. Keep them out of the numbered list — but keep the ones that
  constrain the work under `CONTEXT`.
- **Read to test the ask, don't decide.** Enough code to see whether the ticket
  contradicts what's there, already exists, or names something that doesn't — not enough
  to design the change (`plan`) or resolve its ambiguity (`pin`). Framing that settles its
  own open questions skipped the conversation where the author gets a say.
- **Never print a secret value.** A ticket carrying a credential gets cited by source and
  type, with rotation recommended. Ticket bodies get pasted around freely.

## Method

### 0. Is this one ask, and is it worth framing?

Before framing, check three things and say so plainly when one holds:

- **Two asks wearing one title.** Frame them separately, or ask which one first. A single
  criteria list spanning two changes gets half-verified.
- **Already shipped.** The source describes behavior the code already has. Say so and stop
  — that's the answer, and it's cheaper than a frame nobody needed.
- **One obvious criterion.** A copy fix, a constant, a flag flip. Name the criterion in a
  line and go; a full frame on a one-line change costs more than the change.

None of these hold on most real asks. Don't stretch for one — the check is cheap because
it's fast, not because it usually fires.

### 1. Get the source

Retrieve it the way the user specified, then work from the actual text — the description,
the comments, the linked threads, the attached image. Comments routinely contain the real
requirement, added after someone asked the question you're about to ask.

Nothing retrievable — no access, no permission, a dead link? Say so plainly and ask for a
paste. Framing from a ticket key and a guess produces criteria that look authoritative and
match nothing.

### 2. Restate the ask

Two or three sentences: what changes, for whom, and what's true afterward that isn't now.

Then check it against the source. If your restatement is longer than the ticket, you're
padding. If it's confident where the ticket was vague, you've already invented something —
find that spot and mark it, because it's the first question worth asking.

### 3. Decompose into criteria

One numbered line per checkable behavior. The test for a criterion: could someone verify
it against the running system and get an unambiguous yes or no?

Split anything containing "and" that hides two behaviors. Sweep for the categories that
routinely go unwritten, and include only the ones this ask actually implies:

- **Visibility** — who sees it, who doesn't, in which state or role.
- **Exact content** — the copy, the number, the date, the recipient.
- **Negative space** — what should *stop* happening, or stay unchanged. The most commonly
  omitted criterion, and the one most likely to break something already working.
- **Boundary** — empty, one, many, expired, unauthorized.
- **Existing data** — what happens to records, sessions, or screens that predate this.

Mark each criterion's provenance: **stated** (the source says it) or **inferred** (you
concluded it). Inferred criteria are proposals — they need confirmation before they carry
the same weight, and mixing the two silently is how scope grows without anyone approving it.

### 4. Test the framing against the code

Now read enough of the repo to answer three questions:

- Does any criterion already hold? Say so — it may be the whole ticket, or it may mean
  you've misread the ask.
- Does any criterion contradict how the system works, or name something that doesn't
  exist? That's a blocker for the author, not a puzzle for you to solve.
- Does the source assume behavior the code doesn't have? That gap is the real work, and
  it's usually larger than the ticket implies.

### 5. Name what's missing

Everything the source left open goes in `UNCLEAR`, phrased as a question with the reason
it matters — what would be built differently depending on the answer.

Distinguish two kinds: what the **author** must answer (intent, copy, priority, scope) and
what the **user** can settle (approach, tradeoffs). The first blocks; the second routes to
`pin` and doesn't hold anything up.

A vague ticket with the vagueness named is workable. A vague ticket framed as clear is a
rewrite scheduled for after review.

## Output

```
SOURCE:  <what you framed, and how you got it>
ASK:     <two or three sentences, your words>

CRITERIA:
  1. [stated]   <checkable behavior>
  2. [inferred] <checkable behavior — from what>
  ...

CONTEXT:  <constraints from the source that aren't criteria — omit if none>
UNCLEAR:  <question — and what it changes · who answers it>
CONFLICT: <criterion vs. how the system actually works, file:line — omit if none>
ALREADY:  <criteria that already hold — omit if none>
SCOPE:    <what this explicitly does not cover>
```

Then stop. The criteria list is what gets verified at the end of the change — keep it as
the source of truth, and update it in place when an answer changes it rather than settling
the question in conversation and leaving the list stale.

Nothing `UNCLEAR` on a non-trivial ticket usually means you filled the gaps yourself
without noticing. Re-read the source for what it *didn't* say before reporting a clean
frame.
