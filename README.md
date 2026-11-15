# Skills for engineering work

Ten portable skills for understanding tickets, making decisions, implementing changes,
and handing back evidence. Use one or combine only the stages the task needs. Simple
edits do not need an interview or a full pipeline. Skills guide model behavior; they
cannot guarantee invocation, persistent memory, or sandbox enforcement.

## Install

Claude Code:

```sh
claude plugin marketplace add formesean/skills
claude plugin install skills@formesean
```

Codex (plugin-capable releases):

```sh
codex plugin marketplace add formesean/skills
codex plugin add skills@formesean
```

Codex command syntax was checked against local CLI `0.167.0-alpha.4`; complete plugin
installation was not exercised in this review. Claude Code was unavailable locally.
Check your installed CLI help when commands differ. The two platforms share `skills/`;
platform-specific agent configuration is separate. Installation from the default branch
does not include an unmerged PR.

## Choose the smallest useful workflow

| Skill | Deliverable |
| --- | --- |
| [which](skills/which/SKILL.md) | Select a skill; no forced pipeline |
| [answer](skills/answer/SKILL.md) | Stakeholder reply backed by current evidence |
| [frame](skills/frame/SKILL.md) | Criteria, provenance, and consequential ambiguity |
| [pin](skills/pin/SKILL.md) | Resolve consequential decisions without routine reapproval |
| [plan](skills/plan/SKILL.md) | Small, checkable implementation sequence |
| [implement](skills/implement/SKILL.md) | Requested change and relevant validation |
| [debug](skills/debug/SKILL.md) | Evidence-backed cause, authorized fix, regression evidence |
| [review](skills/review/SKILL.md) | Ranked findings with concrete failure scenarios |
| [verify](skills/verify/SKILL.md) | PASS / FAIL / BLOCKED with observed evidence |
| [ship](skills/ship/SKILL.md) | Handoff or explicitly authorized publication |

Examples: “Diagnose only” remains read-only. “Review and fix” completes the review and
then repairs within the same task. “Write a commit message” does not authorize a push.
“Open a draft PR” authorizes that action, not merging or deployment.

## Optional agents and local harness

[The harness protocol](harness/PROTOCOL.md) describes bounded retrieval, checkpointing,
freshness checks, recovery, and agent handoffs. `harness/state.py` saves compact local
task state under the target repository's Git metadata. Optional per-check fingerprints
flag evidence from a different checkout state, even when the checkpoint itself matches.
The CLI is opt-in and uses the checkout of this repo.

Three worker definitions are provided:

- `agents/*.md`: Claude plugin explorer, reviewer, and verifier. Explorer/reviewer
  allow only Read/Grep/Glob; verifier also has Bash, governed by host permissions.
- `.codex/agents/*.toml`: project-scoped Codex counterparts. They are available in this
  checkout on supported clients. Copy selected files into another project's
  `.codex/agents/` only if desired; do not overwrite existing roles. These are behavioral
  instructions and inherit the host security boundary. Do not assume installing this
  plugin globally registers its project-scoped Codex agents.

Start with one coordinating session. Use bounded independent workers when useful; do
not start three agents for every ticket. Keep memory local and redacted. A checkpoint
matching Git state still needs environment and external-service revalidation.

## Development and checks

Python 3.11+ and Git; no third-party Python dependency is needed for the harness:

```sh
python harness/validate.py
python -m unittest discover -s tests -v
```

[Behavioral scenarios](evals/README.md) cover workflow boundaries, stale memory,
injection, and false verification claims. [Initial results](evals/results-2026-11-14.md)
state what was and was not tested. The [audit](docs/audit-2026-11-14.md) records findings,
changes, measured prompt size, tradeoffs, and sources.

## License

[MIT](LICENSE).
