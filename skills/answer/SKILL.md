---
name: answer
description: Answer someone else's question about the system — QA, PM, support, a team lead — from the code, in their language, without turning it into a change. Use when a question arrives from outside engineering, and whenever the user says "answer this", "QA is asking", "PM wants to know", "how do I reply to this", "is this expected", or pastes a message asking whether something is correct, intended, or doable. To turn a confirmed bug into a fix use `debug`; to turn a confirmed new ask into criteria use `frame`.
---

# answer

Someone outside the code is asking about the code. They can't check your answer, which is
the whole reason they asked — and the whole reason a wrong one is expensive. It gets
repeated to a customer, written into a test plan, or used to close a ticket.

The deliverable is a reply they can act on, and the evidence you'd need if it's challenged.
Not a fix, not a plan, not a lecture about the architecture.

## Rules

- **Never answer from memory.** Not from the ticket, not from what the function is named,
  not from how you built it last month. Open the code that governs the case they asked
  about. An answer you didn't read is a guess with your credibility attached.
- **Separate what it does from whether that's right.** "The banner shows for expired
  trials" is a fact you can cite. "That's correct" is a product judgment, and it's usually
  the asker's to make, not yours. Give the fact first, then say which call is whose.
- **Don't fix it.** A question is not a work order. If the answer is "yes, that's a bug",
  say so and stop — the fix is a separate decision someone else gets to schedule. Handing
  back a diff answers a question nobody asked and commits their sprint for them.
- **Answer in their register.** No `file:line`, no function names, no "the reducer", unless
  they used that vocabulary first. Say what the system does in terms of what a user sees.
  The citations belong in the second block, for you.
- **Say "I don't know" when you don't.** Followed by what you'd have to read or run to find
  out, and how long. A confident wrong answer to someone who can't verify it is the single
  most expensive thing this skill can produce.
- **Answer what they asked, then the question behind it.** "Is this doable?" usually means
  "can I promise it Thursday" — so it's never a bare yes or no. Answer the literal
  question, then give what it touches, roughly what it costs, and what could go wrong. A
  bare "yes" gets quoted back to you as a commitment with a date on it.
- **Don't relitigate their premise.** If the question assumes something false, correct that
  in one line and answer the corrected question. A reply that only says "your question is
  wrong" is a round trip.
- **Never expose internals or secrets.** Not stack traces, not table names, not config
  values, not customer data you passed on the way. Replies get forwarded, pasted into
  tickets, and screenshotted to customers.

## Method

### 1. Pin the actual question

Restate it in one sentence before you read anything. Most outside questions are one of
four, and the shape decides the work:

- **"Is this the correct behavior?"** — a fact question plus a judgment question, wearing
  one sentence. Split them.
- **"Is this a bug?"** — does the code do this deliberately, and does anything depend on it.
- **"Is this doable?"** — scope, cost, and risk. Not a yes.
- **"Why did this happen?"** — a diagnosis, bounded to explaining, not repairing.

Can't tell which? Ask, and ask for the case: the account, the screen, the steps, the
timestamp. A question about "the export" is unanswerable until you know which export.

### 2. Read the code that governs their case

The path their example actually takes, end to end, not the file that sounds relevant. If
they gave a repro, follow it. If they gave a screenshot, find what renders it.

Read enough to state the rule, including the branches they didn't ask about — the edge case
is usually where the disagreement lives, and it's what they'll hit next.

### 3. Separate fact from judgment

Sort what you found into two piles, and keep them sorted in the reply:

- **Fact** — what the code does, which you can cite. This is yours to assert.
- **Judgment** — whether that's what it should do. This is theirs, or the PM's, or the
  author's. Name whose it is instead of quietly making it.

Where the code contradicts the spec they're holding, say both plainly and don't pick a
winner. That's the escalation, and it's the most valuable thing you can hand back.

### 4. Route what isn't an answer

If the answer is "that's a bug" → say so, stop, name `debug` as the next step.
If it's "that's not built" → say so, stop, name `frame` as the next step.
If it's "that's intended but they disagree" → that's a product conversation. Name who owns it.

Routing is a sentence, not a transition. Don't start the next skill inside this one.

### 5. Write it for them, and the evidence for you

Their block: plain language, short, states the answer first and the reasoning second. No
hedging stack, no architecture tour.

Your block: the citations, the caveats, and what you didn't check — so that when they reply
"but what about X", you know whether X was covered.

## Output

```
QUESTION: <what they actually asked, one sentence — and whose case>

REPLY:
  <the message to send them. Their vocabulary. Answer first.>

---
EVIDENCE:  <file:line for each fact asserted above>
JUDGMENT:  <which part of this is a call, and whose — omit if none>
UNCHECKED: <what you did not read or run, and what it would change>
NEXT:      <debug / frame / product conversation / nothing — omit if nothing>
```

Then stop. The `REPLY` block is what gets pasted; everything under the line is yours.

An answer with nothing `UNCHECKED` on a non-trivial question usually means you stopped
reading when the first file agreed with you.
