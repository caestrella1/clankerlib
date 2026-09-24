# Contributing

## Adding an entry

| Type | Steps |
|---|---|
| Skill | `cp -R skills/_template skills/<name>` and fill in `SKILL.md` |
| Instruction | `cp instructions/_template.md instructions/<name>.md` |
| Prompt | `cp prompts/_template.md prompts/<category>/<name>.md` |

Then:

1. Set the frontmatter `name` (it must match the folder or file name) and `description`.
2. Add the entry to `manifest.json`, using the same `description`.
3. Add a row to the matching table in `README.md`.
4. Run `python3 scripts/validate.py`.

## Rules

- **Naming:** kebab-case (`code-review`, not `CodeReview` or `code_review`).
- **Self-contained:** a skill folder must work when copied on its own. Put supporting files inside the skill folder and reference them with relative paths.
- **Descriptions:** one sentence that says what the entry does *and* when to use it. Agents use this text to decide whether to load a skill.
- **Agent-agnostic:** no vendor-specific syntax, tool names, or paths. If an entry has environment requirements, state them in the `compatibility` frontmatter field.
- **No secrets:** never include credentials, internal hostnames, or private data.

## Skill structure

Every `SKILL.md` needs:

- YAML frontmatter with `name` and `description`
- **Purpose**: what it does
- **When to use**: the conditions that should trigger it
- **Steps**: numbered guidance
- **Examples**: at least one input/output pair

## Releases

Maintainers bump `version` in `manifest.json` and tag it: `git tag v0.2.0 && git push --tags`.
