---
name: session-finder
description: "Find an existing agent session by ID, title, project, or approximate time. Use native session pickers for Antigravity, Claude Code, Codex, and OpenCode. Resume only on request."
---

# Find an existing session

1. Identify the harness and project or worktree. Use the account, profile,
   and server that own the session. If those details are unclear, ask only
   for what would distinguish the candidates.
2. Use the harness's native session list or picker first. Confirm a match
   by ID or by title, project, and time. If several match, show a short list
   and let the user choose. Don't default to the newest unless asked.
3. Report the minimum metadata needed to identify the session. Do not open,
   grep, or export transcripts to find a match. Treat a hosted link and a
   local session ID as different until the harness confirms a mapping.
4. Resume only when the user requests it and the match is verified. For a
   lookup alone, give the picker or resume command without selecting or
   starting a session. If metadata is inaccessible, say so; do not create
   a replacement or switch accounts to make the lookup work.

## Harness references

- [Antigravity](references/antigravity.md)
- [Claude Code](references/claude.md)
- [Codex](references/codex.md)
- [OpenCode](references/opencode.md)

This skill finds existing sessions. Use `root-session`, if installed, to
start a new user-visible session with a handoff.
