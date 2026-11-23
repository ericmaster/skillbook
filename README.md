# Skillbook

![An open field notebook with colorful tabs and sketches of a slide, notes, and a magnifying glass](assets/skillbook-hero.webp)

Portable playbooks for coding agents and their human collaborators.

## Available skills

| Skill | Description |
|---|---|
| [`architecture-model`](skills/architecture-model/SKILL.md) | Model a system with C4 and Structurizr DSL; validate the workspace and inspect the rendered views. |
| [`cleanup-stale-worktrees`](skills/cleanup-stale-worktrees/SKILL.md) | Audit and safely clean up completed Git worktrees and local branches while preserving active or unique work. |
| [`context-cleanup`](skills/context-cleanup/SKILL.md) | Audit and prune a repository’s docs and artifacts. Resolve stale or contradictory guidance without losing requirements or evidence. Not for chat compaction. |
| [`context-hygiene`](skills/context-hygiene/SKILL.md) | Write and revise concise specs, plans, runbooks, reports, and agent instructions. Keep rules in one place and verify readers can still find them. |
| [`datadog`](skills/datadog/SKILL.md) | Find and install just the official Datadog Labs skill needed for the current task. |
| [`opencode`](skills/opencode/SKILL.md) | Work with the OpenCode CLI, models, servers, and MCP; troubleshoot xAI authentication via an indexed reference. |
| [`presentation-design`](skills/presentation-design/SKILL.md) | Design or improve presentations, pitch decks, and executive slides. Shape the narrative, choose visuals, and verify the rendered slides and exported PDF. |
| [`root-session`](skills/root-session/SKILL.md) | Use `/root-session <task>` to hand off a task and its context to a new session you can follow. Use `/root-session` by itself to hand off the current task. |
| [`session-finder`](skills/session-finder/SKILL.md) | Find an existing Antigravity, Claude Code, Codex, or OpenCode session using its native picker or list, without searching transcript contents. |
| [`skill-scope`](skills/skill-scope/SKILL.md) | Decide whether a skill should be upstream-managed, project-local, or user-global before installing or sharing it. |
| [`skill-stocktake`](skills/skill-stocktake/SKILL.md) | Review a skill catalog for quality, overlap, broken dependencies, and publication risks. |
| [`spec-ir`](skills/spec-ir/SKILL.md) | Specify feature behavior in YAML and generate Mermaid flow, state, sequence, and entity-relationship diagrams. |

## Install

Copy each desired skill directory into a location your harness discovers. For an
agent that reads `.agents/skills/`, run from the project root:

```sh
mkdir -p .agents/skills
test ! -e .agents/skills/presentation-design &&
  cp -R /path/to/skillbook/skills/presentation-design .agents/skills/
```

Check for an existing skill with the same name before copying. Each skill can
be used independently. Installing both context skills covers writing new docs
and auditing what is already there. No specific model provider is required.
`root-session` uses native session creation where supported; otherwise it
prepares a brief you can paste into a new session.

## License

[MIT](LICENSE).
