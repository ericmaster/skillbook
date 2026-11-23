---
name: cleanup-stale-worktrees
description: "Audit Git worktrees and local branches for safe cleanup. Use when pruning stale registrations or removing completed worktrees without losing changes, commits, or active work."
---

# Clean up stale Git worktrees

Stay within the named repository. Keep the primary checkout on its default
integration branch. Leave default, protected, and remote branches alone. Do not integrate, stash,
reset, force-delete, or stop services as part of ordinary cleanup.

1. **Inventory without changing anything.** List worktrees with
   `git worktree list --porcelain`. Verify the primary path and the intended
   integration ref; do not assume the default is `main`. Check locked and
   missing entries, each candidate's tip and branch, and which sessions or
   processes use it. `git worktree prune --dry-run --verbose` previews missing
   registrations; it does not audit directories that still exist.
2. **Prove preservation.** Require task completion and check that the exact
   candidate tip is reachable from a verified retained ref with
   `git merge-base --is-ancestor <candidate-tip> <retained-tip>`. Confirm remote
   refs are current before relying on them. For existing directories, inspect
   tracked, untracked, and ignored files, plus submodule state where applicable.
   A clean Git status alone does not cover local databases, credentials, or
   evidence. Retain dirty, locked, unique, active, or uncertain work. Apply the
   project's age rule, or keep candidates less than 24 hours old or of unknown
   age. Commit timestamps alone do not establish worktree creation time.
3. **Recheck and remove eligible local work.** Apply only if cleanup was
   requested; an audit or dry run stops at the report. Check the tips and
   consumers again. Use `git worktree remove <path>` without force and then
   `git branch -d <branch>` where Git permits it and the branch has been
   independently checked for completion and preservation. For missing
   registrations, use `git worktree prune` only if every entry in its dry run
   qualifies. If a command refuses, retain the target and explain why.
4. **Report what changed.** Re-list worktrees and local branches and verify
   the primary checkout stayed on its integration branch. For retained items,
   give the concrete reason and, if appropriate, the decision still needed.
