---
name: skill-scope
description: "Decide where an agent skill should live or be installed: upstream, project-local, or user-global. Use before importing, adapting, or publishing skills."
---

# Choose skill scope

1. **Find the source.** Check for an existing skill and who maintains it.
   For third-party skills, track the upstream version and keep personal
   changes as a local patch when supported. Check rights before redistributing
   any copy, including examples and resources.
2. **Choose the narrowest useful scope.** Use project-local installation
   when the skill assumes a repository, stack, environment, or team policy.
   Use a user-global skill only for broadly applicable guidance. Keep a
   sensitive or experimental skill private and opt in only where needed.
3. **Keep one canonical copy.** Discover the harness's supported skill paths.
   If multiple tools need the same project skill, use a supported bridge to
   the canonical directory rather than maintaining duplicate instructions.
   Do not overwrite another skill with the same name; resolve the collision.
4. **Verify at the intended scope.** Check that the target harness can discover
   the skill and its bundled resources, and that a project-local skill does
   not leak into unrelated projects. Report source, scope, and any conflict.

Do not install or publish a skill just because a scope was recommended.
