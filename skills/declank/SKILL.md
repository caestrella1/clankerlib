---
name: declank
description: Rewrite text, code comments, or documentation to be shorter, plainer, and more direct. Use when asked to tighten, simplify, shorten, or de-fluff writing, or to clean up verbose comments or docs.
compatibility: The optional checker script needs Python 3.8+ (standard library only).
---

# Declank

Rewrite existing text so it says the same thing in fewer, plainer words. The rules are in [references/human-mode.md](references/human-mode.md).

## When to use

- "Make this shorter", "less wordy", "clean up these comments"
- Editing a README, doc, or PR description before it's published
- Reviewing a diff whose comments narrate the code

Don't use it to change meaning, or a tone the author chose on purpose.

## Steps

1. Run the checker for a first pass. It flags patterns by rule ID and misses things, so read the text too.
   ```bash
   python3 scripts/clank_detector.py README.md src/app.py   # code files: comments only
   echo "draft text" | python3 scripts/clank_detector.py -
   ```
2. Read the text against the rules. In code, touch only comments and docstrings.
3. Rewrite. Keep every fact, number, name, and instruction.
4. Compare with the original. Nothing factual lost, nothing added.
5. Run the checker again. Anything still flagged needs a reason to stay, such as a quoted string.
6. Report which files changed and anything you left on purpose.

## Examples

**Prose**
- Before: "In order to get started, it's worth noting that you'll need to leverage the CLI, which serves as the primary entry point for interacting with the system."
- After: "Install the CLI first. It's the main way to use the system."

**Comments**

Before:
```python
# Added retry logic
# Loop over each attempt and try to send the request
for attempt in range(MAX_RETRIES):
    # Send the request
    response = send(request)
```

After:
```python
# The upstream API drops ~1% of requests under load.
for attempt in range(MAX_RETRIES):
    response = send(request)
```
