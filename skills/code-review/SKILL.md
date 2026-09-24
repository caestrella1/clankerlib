---
name: code-review
description: Review a diff or pull request for correctness, readability, and maintainability issues. Use when asked to review code changes.
---

# Code review

## Purpose

Produce a prioritized list of actionable findings for a set of code changes. Focus on defects that would cause wrong behavior first, then on issues that make the code harder to maintain.

## When to use

- "Review this PR", "look over my changes", "any issues with this diff?"
- Before committing or merging, when the user asks for a second opinion
- When given a branch, commit range, PR number, or pasted diff

## When not to use

- Writing new code from scratch (no diff to review)
- Pure style or formatting passes. Use the project's formatter or linter instead.
- Security audits that need threat modeling beyond the diff

## Steps

1. **Get the diff.** Use `git diff <base>...HEAD` for a branch, or the PR diff. Note which files changed and how many lines.
2. **Understand intent.** Read the PR description, commit messages, and any linked issue. If intent is unclear, say so in the review instead of guessing.
3. **Read surrounding context.** For every changed function, open the full function and its callers. Most real bugs are in how new code interacts with existing code.
4. **Check correctness first.** Look for:
   - Off-by-one errors, wrong comparison operators, inverted conditions
   - Unhandled `null`/`undefined`/`None`, empty collections, zero, negative numbers
   - Error paths: swallowed exceptions, missing cleanup, partial writes
   - Concurrency: shared mutable state, missing awaits, race conditions
   - API contract changes that break existing callers
5. **Check tests.** Does a test cover the new behavior? Would it fail if the change were reverted?
6. **Check maintainability.** Look for duplicated logic, unclear names, functions doing too much, and dead code. Flag comments that narrate the code, restate names, or record history. They should explain why (concise-writing rules C1 to C3).
7. **Verify before reporting.** For each finding, confirm it against the actual code. Drop anything you cannot back up with a concrete scenario.
8. **Report** using the format below, most severe first. Keep each finding short: the problem, the scenario, the fix. No preamble or closing summary beyond the verdict.

## Output format

```markdown
### [severity] file.py:42 — short summary
**Problem:** What is wrong.
**Scenario:** Concrete input or state → wrong result.
**Fix:** Suggested change (code snippet if short).
```

| Severity | Meaning |
|---|---|
| `blocker` | Wrong behavior, data loss, security issue |
| `major` | Likely bug or missing test for new behavior |
| `minor` | Maintainability or clarity issue |
| `nit` | Optional polish |

End with a one-line verdict: **Approve**, **Approve with nits**, or **Request changes**.

## Examples

### Example 1

**Input:**

```diff
 def average(values):
-    return sum(values) / len(values)
+    total = 0
+    for i in range(1, len(values)):
+        total += values[i]
+    return total / len(values)
```

**Output:**

```markdown
### [blocker] stats.py:3 — loop skips the first element
**Problem:** `range(1, len(values))` starts at index 1, so `values[0]` is never added.
**Scenario:** `average([10, 20])` returns `10.0` instead of `15.0`.
**Fix:** Use `for v in values: total += v`, or keep the original `sum(values)`.

### [major] stats.py:6 — empty input raises ZeroDivisionError
**Problem:** Behavior on `[]` is unchanged but still unhandled, and there is no test.
**Scenario:** `average([])` → `ZeroDivisionError`.
**Fix:** Return `0.0` or raise a `ValueError` with a clear message, and add a test.

**Verdict:** Request changes
```
