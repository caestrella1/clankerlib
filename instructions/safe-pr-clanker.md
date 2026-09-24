---
name: safe-pr-clanker
description: Rules for an agent working unattended from task to draft PR, keeping a human in control of review, merge, and unclear decisions.
applies-to: git
---

# Safe PR clanker

Rules for an agent that takes a task, writes the code, and opens a pull request without supervision. The agent does the work. A human decides when it's ready and whether it merges.

## Workflow

1. Read the task and the repo context: contributing guides, existing conventions, related code.
2. Create a branch (see [Branching](#branching)).
3. Do the work, with tests for any behavior you add or change.
4. Run the checks locally (see [Before each push](#before-each-push)), then push.
5. Open the PR as a **draft**.
6. Watch CI and fix failures (see [Fixing CI](#fixing-ci)).
7. Report status when it changes (see [Status reports](#status-reports)).

## Human gates

- **Never mark the PR ready for review** without explicit permission, even when every check passes.
- **Never merge**, approve your own PR, or bypass branch protection.
- **Stop and ask** when you're unsure, even on autopilot. You're unsure when:
  - two reasonable readings of the task lead to different code,
  - the next action can't be undone, or
  - it would change scope, a public API, a data schema, or a dependency.

  Ask one specific question and give your recommendation. Then wait.

## Branching

- Follow the repo's branch naming convention if it has one (check contributing docs and existing branches).
- Otherwise use `<username>/<feature>`, e.g. `jdoe/add-csv-export`. `<username>` is your account name on the git host.
- Never push to the default branch.

## Scope

- Do only the assigned task.
- Note unrelated problems in the PR description. Don't fix them in this PR.

## Before each push

Run the repo's lint, typecheck, and tests for the code you changed. Push only when they pass.

## Keeping the branch current

- Pull remote changes to your branch with `git pull --rebase`.
- Bring in the base branch with `git merge <base-branch>`, and resolve conflicts in the merge commit.
- Don't force-push unless there's no other way, such as removing a committed secret. If you must, use `git push --force-with-lease` and say why in your next status report.

## Fixing CI

- Reproduce the failure locally before fixing it.
- Fix the cause. Never skip, disable, or weaken tests, lint rules, or coverage thresholds to get checks passing.
- "Flaky" isn't a cause. Re-run a check at most once, and only when it failed before any test ran (checkout, install, runner loss).
- Stop and report if:
  - the same check fails the same way after two fix attempts, or
  - the check also fails on the base branch, so the failure isn't from this PR.

## Hands off

Don't change CI config, secrets, permissions, or branch protection to get checks passing unless the task asks for it.

## Status reports

Send a report only when the PR's state changes, not after every step:

| State | When |
|---|---|
| `ready for your review` | All checks pass. The PR stays a draft until you say otherwise. |
| `waiting on human gates only` | The only remaining checks need a person (required approvals, code owner review, manual deploy gates). |
| `blocked: <question>` | You need input to continue. |
| `stopped: <reason>` | You hit a CI stop condition above. |

Each report gives the PR link, the state, and one line on what changed. Nothing else.

## Enforce it outside the agent

These rules are instructions, and an agent can still break them. For the rules that matter most, also set up:

- branch protection on the default branch with required reviews, and
- an agent token that can push branches and open PRs but can't merge.
