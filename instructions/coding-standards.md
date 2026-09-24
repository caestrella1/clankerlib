---
name: coding-standards
description: General coding standards for readability, naming, and structure.
applies-to: all
---

# Coding standards

Language-agnostic rules for code an agent writes or edits. The goal is code a teammate can read, change, and trust. When a project has its own style guide, linter, or formatter, that takes precedence over these rules.

## Rules

### Match the codebase
- Follow the existing conventions in the file and repo (naming, formatting, error handling, comment density) before your own preferences.
- Run the project's formatter and linter on changed files before finishing.

### Naming
- Names describe *what*, not *how*: `unpaid_invoices`, not `filtered_list`.
- Booleans read as questions: `is_active`, `has_access`, `should_retry`.
- Functions start with a verb: `load_config()`, `send_email()`.
- No unexplained abbreviations. `customer_count`, not `cust_cnt`.

### Structure
- One function does one thing. If you need "and" to describe it, split it.
- Prefer early returns over nested conditionals.
- Keep functions short enough to read without scrolling (~40 lines is a smell, not a hard limit).
- No magic numbers. Name them: `MAX_RETRIES = 3`.

### Errors
- Never swallow exceptions silently. Handle, re-raise with context, or log.
- Validate input at system boundaries (API handlers, CLI args, file reads), not in every internal function.
- Error messages say what failed *and* what to do: `"config.yaml not found; run 'init' first"`.

### Comments
- Follow the code comment rules (C1 to C7) in [concise-writing](concise-writing.md): explain why, not what.
- `TODO` comments include a reason or ticket: `# TODO(#123): remove after v2 migration`.

### Scope
- Change only what the task needs. Don't refactor unrelated code in the same change.
- Don't add dependencies without saying why.
- Add or update tests for any behavior you change.

## Examples

**Do:**

```python
MAX_LOGIN_ATTEMPTS = 5

def is_locked_out(user):
    if user.is_admin:
        return False
    return user.failed_logins >= MAX_LOGIN_ATTEMPTS
```

**Don't:**

```python
def check(u):
    # check if user locked
    if not u.is_admin:
        if u.failed_logins >= 5:
            return True
        else:
            return False
    else:
        return False
```
