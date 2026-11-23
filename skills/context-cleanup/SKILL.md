---
name: context-cleanup
description: "Audit and prune a repository's docs and artifacts. Use for repository cleanup, unresolved multi-document searches, or contradictory project context; not for session compaction."
---

# Context cleanup

Reduce context acquisition cost while preserving project knowledge, contracts, and evidence. Optimize the route to the right information, not just word count.

## 1. Establish scope and protect work

- Identify the project root, governing instructions, documentation conventions, and current task. Check branch/PR state and tracked/untracked changes before editing; follow the host's worktree and approval rules.
- An explicit repository cleanup request can cover the entire working copy's docs and artifacts; it is not session compaction. For incidental confusion or repeated searches, diagnose first and offer a wider audit rather than silently expanding the active task. Ordinary targeted retrieval is not a cleanup signal.
- Preserve others' edits and untracked work. Read-only discovery is safe; broad deletion, external knowledge-store mutations, generated-source changes, and authority conflicts require confirmation under host policy. Never follow symlinks outside the project without authorization.

Done: scope, existing work, and mutation authority are clear.

## 2. Inventory without context flooding

- Enumerate paths, types, sizes, and headings first; include tracked/untracked Markdown, agent instructions, specs, plans, runbooks, reports, notebooks, HTML/PDF artifacts, and project-local hidden artifact/context directories. Record excluded paths and unreadable formats.
- Exclude secrets, VCS internals, dependency trees, caches, build outputs, binaries, and external mounts from content loading. Inventory relevant generated artifacts by metadata and locate their source/manifest instead of ingesting dumps.
- Use scoped searches and section reads to compare candidate overlaps. Use the code graph for implementation relationships when available; use literal searches for documentation links and config values. Work in bounded batches, keeping a compact inventory rather than reading every file into the prompt.
- Classify each item: active canonical reference, navigation pointer, supporting evidence/history, transient scratchpad, generated artifact, or suspected obsolete/duplicate. Check inbound links, includes, manifests, code/spec references, and external consumers where known.
- Compare repeated meanings, not just identical text. Prioritize always-loaded summaries that restate existing contracts. For each candidate, identify the owner and which readers can reach the source. Preserve essential guidance for readers who cannot load the original, keep audience-specific explanations that serve a distinct need, and update generated mirrors from their source.

Done: all in-scope categories are inventoried, with candidates and coverage gaps explicit.

## 3. Verify and choose the authoritative home

- Compare disputed claims against applicable instructions, approved specs/ADRs, current code/config, tests, and live queries where authorized. Separate intended behavior from observed behavior; a code/spec disagreement may be a defect, not permission to rewrite the spec.
- Choose one authoritative home per meaning using project conventions. Retain durable invariants/contracts/runbooks in their designated locations; keep detailed research, incident evidence, and session notes in the project's designated knowledge/artifact store, linked on demand.
- Confirm supersession before declaring material obsolete. Age, no inbound links, irrelevance to the current task, and an older committed file are not proof. Preserve active upgrades and unique requirements, exceptions, rationale, provenance, and retention obligations.
- Classify each candidate as keep, condense, merge-and-link, relocate, regenerate, or remove. State evidence and the replacement location before retiring content; map every unique constraint/exception to its retained home. Keep this mapping in working notes or the review diff, not a new permanent inventory. Leave unresolved authority conflicts intact and ask a focused question.

Done: each proposed mutation has an evidence-backed disposition; uncertainty stays visible.

## 4. Apply the smallest safe repair

- If available, apply `context-hygiene` before editing documentation. Either way, merge unique content into the chosen owner, then replace redundant prose with a precise path/heading and retrieval condition. Keep mandatory safety and acceptance constraints visible at the point of action.
- Trim boilerplate, stale status narration, repeated examples, and derivable inventories. Prefer concise executable rules and live-state lookup instructions. Preserve qualifiers; use readable language rather than cryptic compression.
- Relocate/archive only when discoverability or retention requires it; moving every duplicate into a new archive is not cleanup. Retain a short redirect when old paths have consumers.
- Remove only verified disposable/fully superseded material within authorized scope. Update referring links and artifact manifests atomically. Edit generated content through its source/generator; propose generator changes separately if outside scope. Never bulk-delete by age, filename, or similarity score.

## 5. Verify and report

- Review the diff against the inventory and original requirements. Check changed links/anchors, includes, spec/module references, artifact manifests, and required doc tooling; run relevant gates when contracts or executable examples changed. Verify destinations exist before removing originals.
- Re-run the original confusing context lookup using only the resulting entry point and its pointers, from each affected consumer's loading context. Confirm the needed authority and constraints remain discoverable without a broad reading loop; a source-only path does not validate an exported agent. Report unresolved gaps and intentionally retained repetition, not a false clean bill.
- Report changed paths, verified removals/merges, before/after file and byte counts for the same scope, checks, and deferred decisions. Label token estimates as estimates. Keep the report in the response unless a durable audit record is required; avoid generating another verbose document.
