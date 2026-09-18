# Portable Marketing Skills

This directory is the **generated distribution layer** for Agent Skills-compatible runtimes and the `npx skills` CLI.

The only canonical editable skill source remains:

```text
.agents/skills/
```

Do not hand-edit generated skill folders under `skills/`. Change the canonical skill in `.agents/skills/`, then rebuild:

```bash
python3 scripts/build-portable-skills.py
```

CI checks that the generated distribution has not drifted.

## Install in one command

Install Marketing Skills with the open Agent Skills CLI:

```bash
npx skills add vinceservidad/marketing-skills
```

List available skills first:

```bash
npx skills add vinceservidad/marketing-skills --list
```

Install specific skills:

```bash
npx skills add vinceservidad/marketing-skills \
  --skill google-ads \
  --skill meta-ads \
  --skill creative-strategy
```

Install all skills globally for Codex:

```bash
npx skills add vinceservidad/marketing-skills \
  --skill '*' \
  -g \
  -a codex \
  -y
```

Install all skills globally for Claude Code:

```bash
npx skills add vinceservidad/marketing-skills \
  --skill '*' \
  -g \
  -a claude-code \
  -y
```

The `skills` CLI also supports other compatible agents such as Cursor, Windsurf, GitHub Copilot, OpenCode, Gemini CLI, Cline, Roo, Warp, and others.

## Use one skill without installing

```bash
npx skills use vinceservidad/marketing-skills \
  --skill google-ads \
  --agent codex
```

## Why the generated bundles exist

Canonical Marketing Skills share operating contracts, frameworks, workflows, and templates. A user who installs only one skill still needs the dependencies that make that skill behave correctly.

Each generated portable bundle therefore contains:

```text
skills/<skill>/
  SKILL.md
  references/...
  _shared/
    AGENTS.md
    GLOSSARY.md
    KNOWLEDGE-TAXONOMY.md
    PLATFORM-CURRENCY.md
    CAPABILITY-REGISTRY.md
    ...only additional linked dependencies needed by that skill
```

This makes each installed skill self-contained without creating another editable source of truth.

## Full system or one skill?

For a focused task, install a single skill:

```bash
npx skills add vinceservidad/marketing-skills --skill google-ads
```

For the full operating system, install everything and use `$marketing-router` when you are not sure which specialist should own the request.

## Distribution contract

```text
.agents/skills/
      ↓
canonical governed source
      ↓
scripts/build-portable-skills.py
      ↓
skills/
      ↓
npx skills
      ↓
Codex / Claude Code / Cursor / Windsurf / Copilot / OpenCode / other compatible agents
```

The portable layer may contain repeated shared files by design. Those copies exist so individual skill installation works independently. They are generated and must never be maintained manually.

## Validation

Run:

```bash
python3 scripts/build-portable-skills.py --check
python3 -m unittest tests.test_portable_skills -v
```

The repository's normal CI also validates canonical architecture, generated distribution drift, installer safety, links, evaluations, and GPT knowledge exports.
