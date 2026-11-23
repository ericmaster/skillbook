# Authoring feature specifications

Keep document frontmatter and navigation in Markdown. Write feature logic only in
fenced `yaml spec-ir` graphs. Each graph has **exactly** `id` (string), `kind`
(`flow`, `state`, `api`, `data`), `nodes` and `edges` (ordered lists).
Use precisely the node and edge keys below. Use nonblank strings for IDs, types
and labels; quote YAML-looking strings such as `"on"` or `"01"`. Node IDs are
unique within a graph; edge endpoints reference those IDs. Give each graph in
a file a distinct ID. Keep all domain-specific information inside the open
`meta` mappings: rules, payloads, owners, constraints, latency and error cases.
Use `{}` when none is known. The graph is authoritative; diagrams are projections.

````markdown
```yaml spec-ir
id: invitation
kind: flow
nodes:
  - {id: pending, type: state, label: Pending, meta: {}}
  - {id: expired, type: state, label: Expired, meta: {}}
edges:
  - from: pending
    to: expired
    label: Expire invitation
    meta: {when: "age >= 24h", redeemable: false}
```
````

Use `flow` for directed steps, `state` for transitions, `api` for participants
and messages (edges in time order), and `data` for entities and relationships.
For data edges with known multiplicity and identity, specify the Mermaid ER
connector in `meta.er` (e.g. `||--o{`). Otherwise the diagram uses an explicitly
unspecified relationship; do not infer cardinality from its placeholder glyphs.

## Generated diagrams

Run the [renderer](../scripts/render_spec_ir.py) after editing the source
graph. It renders `flow` as a flowchart, `state` as a state diagram, `api` as a
sequence diagram, and `data` as an entity-relationship diagram. Edit the YAML,
not the Mermaid block between `<!-- spec-ir:start -->` and
`<!-- spec-ir:end -->` immediately below it. Unrelated Markdown stays unchanged.
An invalid graph or malformed generated region rejects the entire file without
changes. Running the renderer again on unchanged input is byte-idempotent.
