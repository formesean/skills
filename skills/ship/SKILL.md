---
name: ship
description: End-of-change handoff — derive the branch name from the repo's own conventions, write a Conventional Commit message, and list the manual test steps. Never pushes. Use when a change is complete, and whenever the user says "ship it", "branch name", "commit message", or asks how to hand this off. Emit it unprompted when work is done. To run the quality gate first use `verify`.
---

# ship

The handoff is the last place a change can still be cheap to fix. Everything after it —
review, merge, deploy — costs more.

Two things carry it: a branch name and commit message that match what this repo already
does, and test steps someone else can run without asking you a question.

Emit this unprompted when a change is done. Being asked for it means it fired late.

## Rules

- **Never push. By any vehicle.** Not `git push`, not a `--push` flag on another command,
  not a tool that pushes as a side effect. Hand over the command for the user to run.
  Publishing is theirs to trigger, always.
- **Derive the convention, don't assume it.** Read the repo's actual branches and actual
  commit log before naming anything. A prefix that's right in the last repo you touched is
  wrong here, and it's the most common way a handoff gets corrected.
- **The repo wins.** Where existing branches or commits contradict any rule below — house
  style, this file, what you did yesterday — follow the repo. Consistency inside one
  history beats correctness imported from outside it.
- **No handoff on a red gate.** Paste the failure verbatim instead. A commit message
  attached to failing code is a request for someone else to discover the failure.
- **Honest type over flattering type.** A tooling script is `chore`, a rename is `refactor`,
  a string change is `fix` or `docs`. Inflating to `feat` corrupts the changelog and the
  version bump downstream.
- **One logical change per commit.** Unrelated work in the tree gets proposed as separate
  commits with explicit `git add <paths>`. A commit whose subject needs "and" is two.
- **Never invent a ticket ID.** Use the one you were given. No ID in play? Leave it out —
  a wrong reference is worse than none, and it points reviewers at someone else's work.
- **Never print a secret value.** Found one in the diff or history? Stop the handoff, cite
  `file:line` and the type, and say rotate first. A secret in history is not fixed by a
  rewrite that leaves the key valid.

## Method

### 1. Derive the conventions

```bash
git branch -a | grep -v HEAD | tail -15   # the prefix actually in use
git log --oneline -15                     # the commit style actually in use
git status                                # what's staged, what's not, what's untracked
```

Read what's there before writing anything. You are answering three questions: does this
repo prefix branches (`<area>/<type>/<slug>`) or not (`<type>/<slug>`), does it put ticket
IDs in branches or subjects and in what case, and does it use Conventional Commits at all.

A repo with a scope convention, a ticket-ID position, or a subject style is telling you
the answer. Copy it. Where the log is inconsistent, follow the most recent dozen commits —
that's the convention in force, whatever the old ones did.

### 2. Confirm the gate is green

The change isn't shippable until the smallest gate covering it passes — `verify` owns
which commands those are and how to scope them.

Already run this session and nothing changed since? Say so and reuse the result. Not run?
Run it now. Red? Stop, paste the failure verbatim, and hand back the shortest path to
green instead of a handoff.

### 3. Name the branch

```
<type>/<kebab-slug>                   # no area convention in the repo
<area>/<type>/<kebab-slug>            # repo prefixes by area or product
<area>/<type>/<ticket-id>-<slug>      # repo carries ticket IDs, and you have one
```

`<type>` matches the commit type. `<slug>` is three to five words naming the change, not
the ticket title. Lowercase, hyphenated, no trailing ID unless the repo does that.

Already on a non-default branch that fits the change? Use it. Proposing a new branch for
work already committed somewhere sensible creates a migration nobody asked for.

### 4. Write the commit message

Conventional Commits:

```
<type>(<scope>)?: <subject>

<body>

<footer>
```

**Type** — `feat` new capability · `fix` corrected behavior · `docs` documentation ·
`style` formatting only, no code change · `refactor` neither fixes nor adds · `perf`
performance · `test` tests only · `build` build system or dependencies · `ci` pipeline
config · `chore` everything else, including tooling and scripts · `revert` undoes a commit.

**Scope** — optional, and only if the repo uses them. Take the value from the log, not
from the directory name.

**Subject** — imperative mood ("add", not "added" or "adds"), lowercase start, no trailing
period, and the whole header at or under 72 characters. It completes the sentence *"this
commit will…"*.

**Body** — only when the *why* isn't already in the subject. Wrap at 72. Explain the
reason and the constraint, not the diff — the diff is already in the commit.

**Footer** — `Refs: <id>` or the repo's own form for a ticket. A breaking change is
`!` after the type or scope *and* a `BREAKING CHANGE:` footer naming what breaks and what
replaces it.

### 5. Write the test steps

Numbered, runnable by someone who didn't write the change: where to go, what role or
account, the action, the expected result. Include one negative check — the case that
should be rejected or show an error.

Anything only the user can run — a real device, a live email, a production flag, a
credential you don't hold — goes under `manual-only`, not written as though you did it.

Going to a PM, client, or stakeholder as well? That's `answer` — same facts, their
register.

## Output

```
Branch:  <derived name>
Commit:  <type>(<scope>): <subject>

         <body, if the why isn't in the subject>

         <footer, if any>

Gate:    <command → result, or "verified this session, tree unchanged">

Run:     git checkout -b <branch>
         git add <paths>
         git commit -m "..."
         git push -u origin <branch>

STR:     1. <step> → <expected>
         2. ...
MANUAL-ONLY: <steps only you can run — or "none">
```

Include the push line as text for the user to run. Never run it.

Unrelated changes in the tree? Propose the split — one block per commit, each with its own
`git add <paths>` — rather than one commit that buries a real change inside incidental
edits.

Something still unresolved — a known limitation, a follow-up, a deliberate shortcut? Say it
in one line under the handoff. The moment before someone else reads this code is the last
cheap moment to mention it.
