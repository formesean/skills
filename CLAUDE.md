# Repository guide

This repo is a **plugin marketplace** distributing an engineering method as ten skills for
Claude Code and Codex. It is not an app — there is no build, no dependencies, and no tests.

- The skills live in `skills/<name>/SKILL.md` — one file per skill, the single source of
  truth. Both harnesses read the same directory; there are no per-platform copies.
- Every skill holds the same three sections: `## Rules`, `## Method`, `## Output`. Rules
  run 6–9 bullets. Frontmatter is `name` + `description` only, so it works in both agents.
- `description` carries the trigger phrases *and* the routing to sibling skills — it is
  what makes a skill fire without being invoked. Edit it as carefully as the body.
- **Adding, renaming, or removing a skill touches four places**: the new `SKILL.md`, the
  routing table and disambiguation pairs in `skills/which/SKILL.md` (skill names appear
  ~27 times there), the four `description` fields across `.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json`, and `.codex-plugin/plugin.json`, and the README's
  Reference section plus its skill count in the opening paragraph.
- Claude manifests are `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`;
  the Codex manifest is `.codex-plugin/plugin.json` (`skills: "./skills/"`). Codex reads
  the Claude `marketplace.json`, so there is no separate Codex marketplace file.
- Bump `version` in both plugin manifests when skills change. Keep them in step.
- `AGENTS.md` is the Codex-facing copy of this file — update both together.

Skills are standing instructions, not narration: cut prose that defends a rule rather than
stating it. The quality gate here is reading the diff — a skill is prose, so the check is
whether a model could follow it without the conversation that produced it.
