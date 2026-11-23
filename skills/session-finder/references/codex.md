# Codex

Run `codex resume` from the intended project to open the interactive picker.
Use `codex resume --all` only if the directory is unknown or the user asks
for cross-project search; compare the working directory before selecting.

For an authorized resume, pass the verified ID to `codex resume "$session_id"`
or select the verified entry. Prefer the ID when names are duplicated. Use
`codex resume --last` only for an explicit most-recent request. On an attached
or remote client, verify the session's server before resuming.

Check `codex resume --help` and the
[Codex CLI reference](https://developers.openai.com/codex/cli/reference).
