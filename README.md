# clankerlib

A reusable library of **skills**, **instructions**, and **prompts** for AI agents. Every entry is a self-contained Markdown file, so you can copy it, symlink it, or pull it into any project.

## Contents

### Skills

Each skill lives in its own folder under `skills/`. The `SKILL.md` inside uses the [Claude Code skill format](https://docs.claude.com/en/docs/claude-code/skills).

| Name | Description | When to use |
|---|---|---|
| [code-review](skills/code-review/SKILL.md) | Review diffs/PRs for correctness, readability, maintainability | Asked to review code changes |
| [data-analysis](skills/data-analysis/SKILL.md) | Explore, clean, and summarize tabular data | Analyzing a CSV, spreadsheet, or dataset |
| [docx-handling](skills/docx-handling/SKILL.md) | Create, read, and edit Word documents | A `.docx` file is input or output |

### Instructions

Standing rules to include in an agent's context (e.g. `CLAUDE.md`, `AGENTS.md`, `.cursorrules`).

| Name | Description | When to use |
|---|---|---|
| [coding-standards](instructions/coding-standards.md) | Readability, naming, and structure rules | Any coding task |
| [commit-conventions](instructions/commit-conventions.md) | Commit message rules | Agent writes git commits |

### Prompts

Reusable prompt text, with `{{VARIABLES}}` for substitution.

| Name | Description | When to use |
|---|---|---|
| [general-assistant](prompts/system-prompts/general-assistant.md) | Baseline system prompt for a general-purpose agent | Starting point for a new agent |

`manifest.json` lists the same entries in machine-readable form for tooling.

## Repo layout

```
clankerlib/
├── skills/<name>/SKILL.md        # one folder per skill (plus optional supporting files)
├── instructions/<name>.md
├── prompts/system-prompts/<name>.md
├── manifest.json                 # machine-readable index
└── scripts/
    ├── validate.py               # frontmatter + manifest consistency checks
    └── install.sh                # copy/symlink skills into a project
```

Files and folders that start with `_` (e.g. `skills/_template/`) are templates. They are skipped by validation and install.

## Using it in a project

| Method | Command | Best for |
|---|---|---|
| Git submodule | `git submodule add https://github.com/caestrella1/clankerlib .agent-lib` | Version-locked, works well with CI |
| Git subtree | `git subtree add --prefix .agent-lib https://github.com/caestrella1/clankerlib main --squash` | Content lives in your repo's history, no separate clone step |
| degit | `npx degit caestrella1/clankerlib/skills/code-review .claude/skills/code-review` | One-time snapshot to customize |
| Symlink | `ln -s ~/src/clankerlib/skills/code-review .claude/skills/code-review` | Local dev across several projects |
| CI copy | `git clone --depth 1 https://github.com/caestrella1/clankerlib /tmp/lib && /tmp/lib/scripts/install.sh <skill>...` | Projects that need only a subset |

Pin a release by adding `#v0.1.0` (degit) or checking out the tag (submodule/subtree).

### Claude Code

Claude Code loads project skills from `.claude/skills/<name>/SKILL.md`. Install into that path with:

```bash
# from your project root
path/to/clankerlib/scripts/install.sh --list                 # show available skills
path/to/clankerlib/scripts/install.sh code-review            # copy one skill
path/to/clankerlib/scripts/install.sh --all                  # copy all skills
path/to/clankerlib/scripts/install.sh --symlink code-review  # symlink (stays in sync)
path/to/clankerlib/scripts/install.sh --dest ~/.claude/skills --all   # user-level install
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Run `python3 scripts/validate.py` before opening a PR.

## Versioning

Releases are tagged with [semver](https://semver.org) (`vMAJOR.MINOR.PATCH`), and the current version is in `manifest.json`. Renaming or removing an entry is a major change.

## License

[MIT](LICENSE)
