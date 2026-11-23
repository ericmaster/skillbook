---
name: opencode
description: "Use when running or configuring OpenCode, diagnosing CLI or server mismatches, choosing models, managing MCP, or troubleshooting provider authentication."
---

# OpenCode

Before acting, check `opencode --version`, `opencode --help`, and the specific
subcommand's `--help`. Use the [CLI docs](https://opencode.ai/docs/cli/) and
[API reference](https://opencode.ai/docs/api/) for the installed release.
A local CLI version does not prove which server handles its requests.

1. **Choose the surface.** Use the interactive UI for work the user wants to
   follow. Use `opencode run "Explain this project"` for headless output when
   authorized. A headless run is not a user-visible handoff; use the host's
   session creation tool for that. Use a worktree for feature-branch work and
   leave the primary checkout on its integration branch.
2. **Verify the scope.** Confirm the intended project, server, and session before
   resuming or mutating anything. Keep the same server when troubleshooting a
   shared session. Use `--server <url>` or `--standalone` only if the installed
   CLI supports it and that mode is the intended one.
3. **Inspect before changing.** Use supported read-only commands to check
   model availability, authentication metadata, or integration status. Check
   the [providers](https://opencode.ai/docs/providers/),
   [config](https://opencode.ai/docs/config/), and
   [MCP](https://opencode.ai/docs/mcp-servers/) docs for the applicable schema.
   Keep existing defaults and permissions unless changing them is in scope.
4. **Verify the result.** Use the smallest check that exercises the same
   project or server path as the original request. Report what was verified;
   successful startup alone does not prove model access, credentials, or
   tool readiness. Redact any logs before sharing them.

For xAI refresh failures, follow [xAI OAuth recovery](references/xai-auth.md).
