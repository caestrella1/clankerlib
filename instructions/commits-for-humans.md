---
name: commits-for-humans
description: Rules for writing git commit messages.
applies-to: git
---

# Commits for humans

Commit messages based on [Conventional Commits](https://www.conventionalcommits.org). The goal is history that is easy to scan, search, and turn into a changelog.

## Rules

### Format

```
<type>(<optional scope>): <subject>

<optional body>

<optional footer>
```

### Type

| Type | Use for |
|---|---|
| `feat` | New user-facing functionality |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change with no behavior change |
| `test` | Adding or fixing tests |
| `perf` | Performance improvement |
| `build` / `ci` | Build system, dependencies, CI config |
| `chore` | Maintenance that doesn't fit above |

### Subject line
- Imperative mood: "add", not "added" or "adds".
- Lowercase after the colon, no trailing period.
- 72 characters max for the whole line, ideally ≤ 50.

### Body
- Separate from the subject with one blank line; wrap at 72 characters.
- Explain *why* the change was made and any trade-offs. The diff shows *what*.
- Omit the body for trivial changes.

### Footer
- Reference issues: `Fixes #123`, `Refs #456`.
- Breaking changes: `BREAKING CHANGE: <what breaks and how to migrate>`, or add `!` after the type: `feat!: ...`.

### Scope of a commit
- One logical change per commit. Don't mix a refactor with a bug fix.
- Every commit should build and pass tests.
- Never commit secrets, generated artifacts, or local config.

## Examples

**Do:**

```
fix(auth): reject expired refresh tokens

Tokens past their expiry were accepted if the access token was still
valid, letting sessions outlive the configured 30-day limit.

Fixes #412
```

```
feat(api)!: return ISO 8601 timestamps

BREAKING CHANGE: `created_at` is now a string ("2026-01-05T10:00:00Z")
instead of a Unix integer. Clients must parse the new format.
```

**Don't:**

```
Fixed stuff.
```

```
Update auth.py, add tests, refactor utils, bump deps
```
