# Authoring feature specifications

Keep document navigation and unresolved questions outside the graph. Put all
specified behavior in fenced `yaml spec-ir` graphs. The YAML is authoritative;
Mermaid and the brief explanation are generated views.

## Version 2

````markdown
```yaml spec-ir
version: 2
id: invitation
kind: flow
nodes:
  - {id: pending, type: state, label: Pending}
  - id: expired
    type: state
    label: Expired
    rules:
      - {field: redeemable, op: eq, value: false}
edges:
  - from: pending
    to: expired
    label: Expire invitation
    when: {field: age, op: gte, value: 24, unit: h}
```
````

- Graph keys: `version: 2`, `id` (unique within the file), `kind` (`flow`,
  `state`, `api`, `data`), ordered `nodes` and `edges`, optional `lang`
  (`en` by default, or `es`) and `meta`.
- Node keys: `id` (unique within the graph), `type`, `label`, optional `rules`,
  `status` and `meta`. Put one testable, local assertion per `rules` entry.
  `status: proposed` on a node marks that step and its rules as proposed;
  the same status on an individual rule marks just that rule. Omit status
  for the specified baseline, which does not imply authorization to implement.
- Edge keys: `from`, `to` (existing node IDs), `label`, optional `when`,
  `er` and `meta`. Each `when` independently enables its edge; sequence,
  exclusivity, joins and fallbacks are not inferred from sibling edges or their
  order. Express requirements for taking an edge in its guard, not its label.
  `when` does not apply to `data`; use edge `er` for a Mermaid ER connector,
  e.g. `||--o{`. Without `er`, relationship constraints are unspecified.
- A guard or rule leaf is `{field, op, value}` with optional `unit` for
  numeric values. `eq`/`ne` accept booleans, finite numbers and identifiers;
  `lt`/`lte`/`gt`/`gte` accept numbers; `includes`/`excludes` specify membership
  of one identifier in a collection. Use `all`/`any` lists of two or more
  predicates (up to eight nesting levels) only in guards. A rule may also
  use `weighted_sum` with a mapping of at least two input identifiers to
  positive numeric weights summing to one. The rule's `field` is the result.
- Identifiers start with a lowercase ASCII letter, followed by lowercase
  letters, digits or underscores; dots separate segments. Quote identifiers
  that YAML would read as booleans or numbers. Labels are names, not rule
  containers: nonblank, one line, at most 100 characters.
- `meta` allows only `owner` (identifier up to 80 characters) and `refs` (a
  list of HTTPS links, relative `./`/`../` links or `#` anchors). No prose or
  arbitrary nested keys. Removing `meta` cannot change either generated view.
  Validation cannot catch omissions or discern all attempts to hide behavior
  in labels or identifiers; review the graph against the source.

## Generation and migration

Run the [renderer](../scripts/render_spec_ir.py) after editing the YAML. It
refreshes the Mermaid and **Description** (Spanish: **Descripción**) between `<!-- spec-ir:start -->` and
`<!-- spec-ir:end -->` immediately below each graph, including older
Mermaid-only regions and the former overview heading. The description narrates
up to two transitions (favoring baseline forks) and at most one baseline rule
(favoring numeric rules). It is intentionally not exhaustive. Invalid graphs or damaged regions
reject the file without changes. Unrelated Markdown is preserved and reruns
are byte-idempotent.

Unversioned v1 graphs still render Mermaid only: their nodes and edges require
`meta` mappings, and legacy data relations use `meta.er`. Do not strip these
mappings automatically. To migrate, trace each legacy behavioral clause to an
explicit v2 edge, guard or node rule, including `meta.er` → `er`. Keep open
questions open and proposals marked as such. Review in both directions before
rendering: no omitted rule and no new ungrounded behavior.
