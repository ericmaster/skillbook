---
name: skill-stocktake
description: "Audit an Agent Skills collection for missing or duplicate skills, stale instructions, broken references, and publication risks. Review a whole collection or the changes since a known revision."
---

# Skill stocktake

Review a skill collection without installing, invoking, or editing it. The idea
of reviewing a whole collection or just its changes was inspired by
[ECC's skill-stocktake](https://github.com/affaan-m/ECC/tree/main/skills/skill-stocktake).

1. **Set the boundary.** Resolve the collection root and its documented skill
   locations. Inventory `SKILL.md` entry points and bundled files, ignoring
   archives and dependency trees. Compare paths and names with the catalog or
   README index if one exists. Keep global installs and unrelated projects out
   of scope unless requested.
2. **Choose coverage.** For a full audit, review every entry. For a quick audit,
   compare with the last reviewed revision and check added, removed, and changed
   files, including scripts and references. Check dependents when a shared
   resource changes. If there is no reliable baseline, run a full audit.
3. **Evaluate.** Match each name to its directory. Check whether its description
   distinguishes the trigger from neighboring skills, and whether its steps,
   dependencies, links, and completion criteria work from an installed copy.
   Flag authority overreach, host-specific assumptions, and overlap. For a
   publication review, also identify private data and verify rights for every
   bundled file. No usage data is not evidence of disuse; unknown rights are
   not permission to redistribute.
4. **Return one actionable decision per skill.** Use **Keep**, **Fix**,
   **Consolidate**, **Retire**, or **Hold**. Include a path, the reason, and a
   concrete next step. For consolidation, name the surviving entry point and
   the unique behavior it must retain. Keep sensitive findings out of the
   collection, and apply changes only if the user requests them.
