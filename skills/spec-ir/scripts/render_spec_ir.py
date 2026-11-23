#!/usr/bin/env python3
# Spec: skills/spec-ir/references/spec-ir.md
"""Regenerate the Mermaid projections of Markdown Spec-IR fences."""

import argparse
import re
from pathlib import Path

import yaml
from markdown_it import MarkdownIt


START, END = "<!-- spec-ir:start -->", "<!-- spec-ir:end -->"
HEAD = dict(flow="flowchart TD", state="stateDiagram-v2", api="sequenceDiagram", data="erDiagram")


class Loader(yaml.SafeLoader):
    # Spec: skills/spec-ir/references/spec-ir.md
    def construct_mapping(self, node, deep=False):
        result = super().construct_mapping(node, deep)
        if len(result) != len(node.value):
            raise ValueError(f"duplicate mapping key near YAML line {node.start_mark.line + 1}")
        return result


# Spec: skills/spec-ir/references/spec-ir.md
def fields(item, keys):
    if not isinstance(item, dict) or set(item) != set(keys.split()):
        raise ValueError(f"expected exactly these keys: {keys}")
    for key in keys.split():
        value = item[key]
        if key == "meta":
            ok = isinstance(value, dict)
        elif key in ("nodes", "edges"):
            ok = isinstance(value, list)
        else:
            ok = isinstance(value, str) and value.strip()
        if not ok:
            raise ValueError(f"invalid {key!r}: expected a mapping, list or nonblank string per schema")


# Spec: skills/spec-ir/references/spec-ir.md
def label(text):
    # Numeric Mermaid entities keep delimiters, directives and line breaks out of the grammar.
    text = " ".join(text.split())
    return "".join(c if c.isalnum() else f"#{ord(c)};" for c in text)


# Spec: skills/spec-ir/references/spec-ir.md
def diagram(graph):
    fields(graph, "id kind nodes edges")
    kind = graph["kind"]
    if kind not in HEAD:
        raise ValueError(f"unknown kind: {kind}")
    lines = [HEAD[kind]]
    ids = {}
    for node in graph["nodes"]:
        fields(node, "id type label meta")
        if node["id"] in ids:
            raise ValueError(f"duplicate node: {node['id']}")
        name = ids[node["id"]] = f"N{len(ids)}"
        text = label(node["label"])
        lines.append("    " + {
            "flow": f'{name}["{text}"]', "state": f'state "{text}" as {name}',
            "api": f"participant {name} as {text}", "data": f'{name}["{text}"]',
        }[kind])
    for edge in graph["edges"]:
        fields(edge, "from to label meta")
        if edge["from"] not in ids or edge["to"] not in ids:
            raise ValueError(f"unknown endpoint: {edge['from']} -> {edge['to']}")
        a, b, text = ids[edge["from"]], ids[edge["to"]], label(edge["label"])
        if kind == "data":
            connector = edge["meta"].get("er", "}o..o{")
            if not isinstance(connector, str) or not re.fullmatch(
                r"(\|o|\|\||}o|}\|)(--|\.\.)(o\||\|\||o\{|\|\{)", connector
            ):
                raise ValueError("meta.er must be an ER cardinality connector")
            if "er" not in edge["meta"]:
                text += " (ER constraints unspecified)"
            line = f'{a} {connector} {b} : "{text}"'
        else:
            line = {"flow": f'{a} -->|"{text}"| {b}', "state": f"{a} --> {b} : {text}",
                    "api": f"{a}->>{b}: {text}"}[kind]
        lines.append("    " + line)
    return lines


# Spec: skills/spec-ir/references/spec-ir.md
def render(source):
    lines = re.findall(r"[^\r\n]*(?:\r\n|\r|\n)|[^\r\n]+$", source)
    tokens = MarkdownIt("commonmark").parse(source)
    edits, seen, claimed = [], set(), set()
    for i, token in enumerate(tokens):
        if token.type != "fence" or token.info.split() != ["yaml", "spec-ir"]:
            continue
        start, stop = token.map
        closing = re.fullmatch(r"([ \t>]*)(" + re.escape(token.markup[0]) +
                               r"{" + str(len(token.markup)) + r",})[ \t]*(\r\n|\r|\n)?", lines[stop - 1])
        if not closing or stop <= start + 1:
            raise ValueError(f"line {start + 1}: unclosed Spec-IR fence")
        try:
            graph = yaml.load(token.content, Loader=Loader)
            drawing = diagram(graph)
            if graph["id"] in seen:
                raise ValueError(f"duplicate graph: {graph['id']}")
            seen.add(graph["id"])
        except (yaml.YAMLError, ValueError, RecursionError) as exc:
            raise ValueError(f"line {start + 1} (Spec-IR): {exc}") from exc

        prefix, newline = closing[1], closing[3] or ("\r\n" if "\r\n" in source else "\n")
        end = stop
        if stop < len(lines) and lines[stop].rstrip("\r\n").strip() == (prefix + START).strip():
            region = tokens[i + 1:i + 4]
            if (len(region) != 3 or [t.type for t in region] != ["html_block", "fence", "html_block"]
                    or region[0].content.strip() != START or region[1].info.strip() != "mermaid"
                    or region[2].content.strip() != END or region[0].map != [stop, stop + 1]
                    or region[1].map != [stop + 1, region[2].map[0]]):
                raise ValueError(f"line {stop + 1}: damaged generated region")
            end = region[2].map[1]
            claimed.update((stop, region[2].map[0]))
        block = [START, "```mermaid", *drawing, "```", END]
        replacement = newline.join(prefix + line for line in block)
        if not closing[3]:
            replacement = newline + replacement
        if lines[end - 1].endswith(("\r", "\n")):
            replacement += newline
        edits.append((stop, end, replacement))
    for token in tokens:
        if token.type == "html_block" and token.content.strip() in (START, END) and token.map[0] not in claimed:
            raise ValueError(f"line {token.map[0] + 1}: orphan generated marker")
    for start, end, text in reversed(edits):
        lines[start:end] = [text]
    return "".join(lines)


# Spec: skills/spec-ir/references/spec-ir.md
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    path = parser.parse_args().file
    try:
        original = path.read_bytes()
        updated = render(original.decode("utf-8")).encode("utf-8")
        if updated != original:
            path.write_bytes(updated)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"{path}: {exc}\n")


if __name__ == "__main__":
    main()
