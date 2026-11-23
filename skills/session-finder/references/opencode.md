# OpenCode

Use the intended project or worktree and the same server as the existing
session. Prefer the host's native session list when available. Otherwise
check `opencode session list --help`, then use a bounded metadata list such
as `opencode session list --max-count 20`. On current versions the CLI lists
top-level sessions in the current project, newest first. If the match isn't
there, check the project, result limit, and native host before concluding
that the session is missing.

For an authorized interactive resume, verify the session exists, then use
`opencode --session "$session_id"` if supported. Recheck before passing an
ID; some versions create a session if the ID is unknown. Use OpenCode's
headless commands only when the user actually wants headless execution.

See the [OpenCode CLI reference](https://opencode.ai/docs/cli/). The
`opencode` skill covers CLI setup, execution, providers, and server behavior;
this reference covers finding the right session.
