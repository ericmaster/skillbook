# Skillbook

Portable playbooks for coding agents and their human collaborators.

| Skill | Use it to |
|---|---|
| [`presentation-design`](skills/presentation-design/SKILL.md) | Design slide narratives and catch problems in rendered decks before delivery. |
| [`context-hygiene`](skills/context-hygiene/SKILL.md) | Keep agent-facing documentation concise without losing requirements or evidence. |
| [`context-cleanup`](skills/context-cleanup/SKILL.md) | Audit an existing repository for stale or duplicated documentation and artifacts. |

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
