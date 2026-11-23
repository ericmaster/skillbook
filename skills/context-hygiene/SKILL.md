---
name: context-hygiene
description: "Keep documentation concise without losing requirements or evidence. Use before writing or revising specs, plans, runbooks, reports, skills, or agent instructions."
---

# Context hygiene

Before writing or revising documentation, find its owner, write only what
changes, and verify readers can find the result. Apply this once per coherent
edit set; don't turn a small edit into a repository audit.

## 1. Find the owner

- Read applicable instructions and the nearest documentation index. Identify
  the reader, the decision the text enables, and what's new. If nothing
  changes, link to the existing source or leave it alone.
- Update the existing owner instead of adding another summary. Create a new
  document only for a distinct purpose, audience, or lifecycle; give it one
  useful discovery link. Keep related code and specifications in sync.
- Put durable contracts in versioned docs, temporary state in a scratchpad
  or handoff, and current operational facts behind live queries when available.

Done: the owner, reader, change, and destination are clear.

### Generated output

Choose destinations before running tools. Keep deliverables meant for version
control in Git. Put durable evidence in the project's approved store so it
survives removal of the working copy. Keep private logs access-controlled.
Link to retained evidence instead of copying it into reference docs. Check
tracked, untracked, and ignored outputs at completion; remove only verified
disposable task output. Confirm recipients can access the intended deliverable
before reporting it delivered.

## 2. Write only what changes

- Keep one authoritative home for each rule. Link to a precise section and
  explain when to read it. Keep mandatory instructions at the point of action
  if the consumer cannot load the source; a link alone is not enough for an
  exported skill or generated guide. Edit mirrors through their source.
- Lead with the action, prerequisites and completion checks. Keep exceptions
  next to the rule. Move branch-specific detail behind a short, explicit link.
- Preserve applicable requirements, security boundaries, acceptance criteria,
  terminology and rationale. Make exceptions testable; don't silently choose
  between disputed rules.
- Document what readers cannot discover cheaply. Keep essential test or build
  commands; link to authoritative configuration for derivable details. Keep
  examples that resolve ambiguity. Omit transcripts, routine progress, duplicate
  headings and speculation. Link to full diagnostics when summarizing failures.

Done: each addition changes behavior or supplies needed knowledge.

## 3. Verify before finishing

- Compare with the previous text and the authoritative source. Remove superseded
  statements instead of leaving conflicting versions. Flag unresolved conflicts
  for a decision.
- Check links, anchors, example commands and required documentation gates from
  the intended reader's environment, including any exported or installed copy.
  Verify consumers still reach any moved rules.
- Review the diff for duplication, unrelated changes and lost constraints.
  Report what changed and what was checked without writing an extra summary
  document. If repeated searches reveal systemic duplication, diagnose first;
  use `context-cleanup` if installed, or propose a bounded audit before expanding
  the scope.
