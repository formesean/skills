# Repository guide

This repository distributes ten portable engineering skills and an opt-in local harness.

- Edit shared skills in `skills/<name>/SKILL.md`; keep `name` and `description` frontmatter,
  plus Rules, Method, and Output sections. Descriptions select tasks, not entire pipelines.
- Keep instructions concise, executable, and evidence-based. Preserve useful boundaries
  without adding confirmation gates to already authorized work.
- Read only relevant skills. For multi-session work, use `harness/PROTOCOL.md` and the
  bounded checkpoint helper. Do not put task logs or credentials in tracked files.
- Claude plugin roles live in `agents/`; Codex project roles in `.codex/agents/`. Keep
  role behavior aligned. These are optional workers, not a mandatory multi-agent loop.
- Bump both plugin manifest versions together for behavior changes. Update routing and
  README when skill names change. Do not assume host-specific installation is portable.
- Run `python harness/validate.py` and `python -m unittest discover -s tests -v`.
  Behavioral edits also need representative fresh-context evaluations from `evals/`.
  Validation syntax is not proof of model quality. Report platform tests not performed.
- Keep this guide and `CLAUDE.md` identical. Preserve unrelated changes and use explicit
  paths when staging. Never merge or deploy without the user's authorization.
