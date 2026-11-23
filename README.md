# Skillbook

![An open field notebook with colorful tabs and sketches of a slide, notes, and a magnifying glass](assets/skillbook-hero.webp)

Portable playbooks for coding agents and their human collaborators.

## Available skills

| Skill | Description |
|---|---|
| [`context-cleanup`](skills/context-cleanup/SKILL.md) | Audit and prune a repository’s docs and artifacts. Resolve stale or contradictory guidance without losing requirements or evidence. Not for chat compaction. |
| [`context-hygiene`](skills/context-hygiene/SKILL.md) | Write and revise concise specs, plans, runbooks, reports, and agent instructions. Keep rules in one place and verify readers can still find them. |
| [`presentation-design`](skills/presentation-design/SKILL.md) | Design or improve presentations, pitch decks, and executive slides. Shape the narrative, choose visuals, and verify the rendered slides and exported PDF. |

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
and auditing what is already there. No provider or external service is required.
