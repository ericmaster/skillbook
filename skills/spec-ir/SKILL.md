---
name: spec-ir
description: "Write feature behavior as YAML graphs in Markdown and generate Mermaid diagrams and brief explanations. Use for flows, state transitions, API sequences, and entity relationships."
---

# Spec-IR

1. Use the [schema and example](references/spec-ir.md) to write or edit a
   `yaml spec-ir` version 2 block. Put routing conditions on edges as `when`
   and local requirements in node `rules`, one testable assertion per entry.
   Use `meta` only for ownership and references. The YAML is the contract.
2. Use Python 3 with the packages listed in [requirements.txt](requirements.txt).
   If they are missing, install them in an approved environment. From the
   skill's resolved directory, run the bundled renderer with the spec path:

   ```sh
   python3 scripts/render_spec_ir.py /path/to/spec.md
   ```

   Run it after each graph edit. Fix validation errors in the YAML and retry;
   do not edit the generated Mermaid or explanation manually. Review the graph and the rendered
   diff before committing.
3. Use `architecture-model` for the C4 view of systems and components. When
   both views are useful, link them instead of modeling the same rules twice.

For existing prose, preserve the original and verify the conversion against it
before rendering. Rendering validates the graph, not fidelity to the old spec.
