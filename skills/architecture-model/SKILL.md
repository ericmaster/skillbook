---
name: architecture-model
description: "Author or update a C4 architecture model in Structurizr DSL. Use for system context, container or component diagrams, or when implementation has drifted from workspace.dsl."
---

# Model architecture as code

Treat the [Structurizr DSL workspace](https://docs.structurizr.com/dsl) as the
source; images and exports are views of it, not separate models. Start from the
existing workspace, or ask where to store a new one if the project has no
convention. Skip views that do not answer a question.

Use `spec-ir` for a feature's behavioral contract, such as state transitions or
API sequences. C4 owns the system structure; link a behavioral spec rather than
copying its rules into the architecture model.

1. Name the audience and question. Use a system-context view for people,
   systems, and external dependencies. Add a container view to show applications,
   data stores, and how they communicate. Use a component view only when it
   clarifies the interior of a named container.
2. Verify elements and relationships against code, configuration, and approved
   decisions. Label direction and purpose on each relationship. Mark a proposed
   design separately from observed behavior. Link key elements to their source
   paths and relevant ADRs; do not model every file.
3. Edit the DSL and keep existing element identifiers and view keys stable
   unless a deliberately reviewed change requires otherwise. Prefer smaller
   views over squeezing extra elements into a diagram.
4. Use the project's verified Structurizr commands. The official
   [`validate`](https://docs.structurizr.com/validate) and
   [`inspect`](https://docs.structurizr.com/inspect) commands accept
   `-workspace <path>`. Render or export the changed views using the
   [official tooling](https://docs.structurizr.com/commands) and inspect
   labels, scope, and missing or misleading relationships. Keep a local
   viewer loopback-only; do not upload an internal model without approval.

Done: the edited workspace validates, the affected views have been checked,
and the handoff identifies any unverified relationship or missing tool.
