---
name: root-session
description: "Hand off a task with context to a new, user-visible root session on explicit request."
---

# Root session

Use `/root-session <task>` or `/root-session` to hand off the current task.
Only dispatch when the user explicitly invokes the skill or asks for a new
session. If the task or project is ambiguous, ask only for the missing decision.

1. **Prepare a short brief.** Resolve the project directory. Include the goal,
   acceptance criteria, relevant paths or links, verified state, decisions,
   what remains, and any limits on edits, branching, or deployment. Pass only
   what's needed; omit secrets and unrelated history.
2. **Create a user-visible session.** Use the host's native session creation
   tool, not a subagent or headless process. In OpenChamber, call
   `openchamber.session.create` with `directory`, a short `title`, and the
   brief as `prompt`. Use a worktree if requested or required by project
   rules; do not switch the primary checkout to a feature branch. Use the
   host's default agent and model unless the user specifies otherwise. If
   native session creation is unavailable, provide the brief for the user
   to paste into a new session instead.
3. **Hand over ownership.** In the brief, tell the recipient to execute the
   task and report to the user, not to invoke `/root-session` again. Return
   the session title and ID or link, then stop working the same task in the
   original session. If creation is uncertain, check for the session before
   retrying; avoid duplicate dispatch.
