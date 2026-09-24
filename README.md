# clankerlib

A reusable, agent-agnostic library of **skills**, **instructions**, and **prompts** for AI agents. Every entry is plain Markdown with no vendor-specific syntax, so it works with any agent or model and can be copied, symlinked, or pulled into any project.

## Contents

### Skills

Each skill lives in its own folder under `skills/` and follows the open [Agent Skills specification](https://agentskills.io/specification) (`SKILL.md` with `name`/`description` frontmatter), which [many agents support](https://agentskills.io/clients).

| Name | Description | When to use |
|---|---|---|
| [data-analysis](skills/data-analysis/SKILL.md) | Explore, clean, and summarize tabular data | Analyzing a CSV, spreadsheet, or dataset |
| [declank](skills/declank/SKILL.md) | Rewrite text, comments, or docs to be shorter and plainer. Includes a checker script | Asked to shorten, simplify, or de-fluff writing |
| [docx-handling](skills/docx-handling/SKILL.md) | Create, read, and edit Word documents | A `.docx` file is input or output |
| [second-opinion](skills/second-opinion/SKILL.md) | Review diffs/PRs for correctness, readability, maintainability | Asked to review code changes |

### Instructions

Standing rules to include in whatever file your agent reads for project context (e.g. `AGENTS.md`), or paste into a system prompt.

| Name | Description | When to use |
|---|---|---|
| [coding-standards](instructions/coding-standards.md) | Readability, naming, and structure rules | Any coding task |
| [commits-for-humans](instructions/commits-for-humans.md) | Commit message rules | Agent writes git commits |
| [human-mode](instructions/human-mode.md) | Short, plain writing rules for responses, comments, and docs | Always; add it to every agent |

### Prompts

Reusable prompt text, with `{{VARIABLES}}` for substitution.

| Name | Description | When to use |
|---|---|---|
| [simple-clanker](prompts/system-prompts/simple-clanker.md) | Baseline system prompt for a general-purpose agent | Starting point for a new agent |

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
    └── install.sh                # copy/symlink skills into an agent's skills dir
```

Files and folders that start with `_` (e.g. `skills/_template/`) are templates. They are skipped by validation and install.

## Using it in a project

| Method | Command | Best for |
|---|---|---|
| Git submodule | `git submodule add https://github.com/caestrella1/clankerlib .agent-lib` | Version-locked, works well with CI |
| Git subtree | `git subtree add --prefix .agent-lib https://github.com/caestrella1/clankerlib main --squash` | Content lives in your repo's history, no separate clone step |
| degit | `npx degit caestrella1/clankerlib/skills/second-opinion <skills-dir>/second-opinion` | One-time snapshot to customize |
| Symlink | `ln -s ~/src/clankerlib/skills/second-opinion <skills-dir>/second-opinion` | Local dev across several projects |
| CI copy | `git clone --depth 1 https://github.com/caestrella1/clankerlib /tmp/lib && /tmp/lib/scripts/install.sh --dest <skills-dir> <skill>...` | Projects that need only a subset |

Pin a release by adding `#v0.1.0` (degit) or checking out the tag (submodule/subtree).

`<skills-dir>` is wherever your agent discovers skills. Check your agent's documentation for the path.

### Install script

```bash
path/to/clankerlib/scripts/install.sh --list                                # show available skills
path/to/clankerlib/scripts/install.sh --dest <skills-dir> second-opinion       # copy one skill
path/to/clankerlib/scripts/install.sh --dest <skills-dir> --all             # copy all skills
path/to/clankerlib/scripts/install.sh --dest <skills-dir> --symlink --all   # symlink (stays in sync)
```

### Apps without filesystem access

Some agent apps (web or mobile chat clients) don't read skills from disk and instead take an upload, often a zip of the skill folder. That upload format is set by each product and isn't part of the Agent Skills spec. To build one:

```bash
cd skills && zip -r ../second-opinion.zip second-opinion
```

For instructions and prompts, paste the Markdown body into the app's custom instructions or system prompt field.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Run `python3 scripts/validate.py` before opening a PR.

## Versioning

Releases are tagged with [semver](https://semver.org) (`vMAJOR.MINOR.PATCH`), and the current version is in `manifest.json`. Renaming or removing an entry is a major change.

## License

[MIT](LICENSE)
