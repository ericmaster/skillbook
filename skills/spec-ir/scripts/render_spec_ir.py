#!/usr/bin/env python3
# Spec: skills/spec-ir/references/spec-ir.md
"""Regenerate Mermaid and brief explanations from Markdown Spec-IR fences."""

import argparse
import math
import re
from collections import Counter
from pathlib import Path

import yaml
from markdown_it import MarkdownIt


START, END = "<!-- spec-ir:start -->", "<!-- spec-ir:end -->"
HEAD = dict(flow="flowchart TD", state="stateDiagram-v2", api="sequenceDiagram", data="erDiagram")
SUMMARY = {"en": "**Generated overview.**", "es": "**Resumen generado.**"}
OPS = dict(eq="=", ne="≠", lt="<", lte="≤", gt=">", gte="≥", includes="∋", excludes="∌")
SYMBOL = r"[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*"
ER = r"(\|o|\|\||}o|}\|)(--|\.\.)(o\||\|\||o\{|\|\{)"


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
def shape(item, required, optional=""):
    keys = set(required.split())
    if not isinstance(item, dict) or not keys <= item.keys() <= keys | set(optional.split()):
        raise ValueError(f"expected keys {required!r}, optionally {optional!r}")


# Spec: skills/spec-ir/references/spec-ir.md
def matches(pattern, value):
    return isinstance(value, str) and re.fullmatch(pattern, value) is not None


# Spec: skills/spec-ir/references/spec-ir.md
def number(value):
    return type(value) is int or (type(value) is float and math.isfinite(value))


# Spec: skills/spec-ir/references/spec-ir.md
def annotation(item):
    meta = item.get("meta", {})
    shape(meta, "", "owner refs")
    if "owner" in meta and not matches(r"[A-Za-z0-9][A-Za-z0-9_.@/-]{0,79}", meta["owner"]):
        raise ValueError("meta.owner must be an identifier")
    if "refs" in meta and (not isinstance(meta["refs"], list) or not all(
        matches(r"(?:https://|#|\./|\.\./)[A-Za-z0-9_.:/?#@!$&'()*+,;=%~-]{1,300}", ref)
        for ref in meta["refs"]
    )):
        raise ValueError("meta.refs must be a list of links")


# Spec: skills/spec-ir/references/spec-ir.md
def predicate(item, *, rule=False, depth=0):
    if depth > 8:
        raise ValueError("when exceeds maximum nesting")
    if not rule and isinstance(item, dict) and set(item) in ({"all"}, {"any"}):
        terms = next(iter(item.values()))
        if not isinstance(terms, list) or len(terms) < 2:
            raise ValueError("all/any requires at least two predicates")
        for term in terms:
            predicate(term, depth=depth + 1)
        return
    shape(item, "field op value", "unit status" if rule else "unit")
    op, value = item["op"], item["value"]
    if not matches(SYMBOL, item["field"]):
        raise ValueError("predicate field must be an identifier")
    if "status" in item and item["status"] != "proposed":
        raise ValueError("status must be proposed")
    if rule and op == "weighted_sum":
        if (not isinstance(value, dict) or len(value) < 2
                or not all(matches(SYMBOL, k) and number(v) and 0 < v <= 1 for k, v in value.items())
                or not math.isclose(sum(value.values()), 1)):
            raise ValueError("weighted_sum requires at least two positive weights that sum to 1")
    elif (not isinstance(op, str) or op not in OPS
          or not (type(value) is bool or number(value) or matches(SYMBOL, value))
          or (op in ("lt", "lte", "gt", "gte") and not number(value))
          or (op in ("includes", "excludes") and not matches(SYMBOL, value))):
        raise ValueError("invalid operator or operand")
    if "unit" in item and (not matches(SYMBOL, item["unit"]) or not number(value)):
        raise ValueError("unit requires a numeric scalar")


# Spec: skills/spec-ir/references/spec-ir.md
def semantic(graph):
    v2 = isinstance(graph, dict) and "version" in graph
    if v2:
        shape(graph, "version id kind nodes edges", "lang meta")
        if type(graph["version"]) is not int or graph["version"] != 2:
            raise ValueError("expected version: 2 (omit version for legacy graphs)")
        annotation(graph)
    else:
        fields(graph, "id kind nodes edges")
    kind, lang = graph["kind"], graph.get("lang", "en")
    if not isinstance(kind, str) or kind not in HEAD:
        raise ValueError("unknown kind")
    if not isinstance(lang, str) or lang not in SUMMARY:
        raise ValueError("lang must be en or es")
    if not isinstance(graph["id"], str) or not graph["id"].strip():
        raise ValueError("graph id must be a nonblank string")
    clean = dict(id=graph["id"], kind=kind, lang=lang, version=2 if v2 else 1)
    ids = set()
    for group, required, optional in (("nodes", "id type label", "rules status meta"),
                                      ("edges", "from to label", "when er meta")):
        if not isinstance(graph[group], list):
            raise ValueError(f"{group} must be a list")
        clean[group] = []
        for item in graph[group]:
            if v2:
                shape(item, required, optional)
                annotation(item)
                for key in required.split():
                    if key == "label":
                        if not matches(r"[^\r\n]{1,100}", item[key]) or not item[key].strip():
                            raise ValueError("label must be a nonblank single line of at most 100 characters")
                    elif not matches(SYMBOL, item[key]):
                        raise ValueError(f"{key} must be an identifier")
            else:
                fields(item, required + " meta")
            entry = {key: value for key, value in item.items() if key != "meta"}
            if group == "nodes":
                if item["id"] in ids:
                    raise ValueError(f"duplicate node: {item['id']}")
                ids.add(item["id"])
                if "status" in entry and entry["status"] != "proposed":
                    raise ValueError("status must be proposed")
                if "rules" in entry:
                    if not isinstance(entry["rules"], list):
                        raise ValueError("rules must be a list of atomic assertions")
                    for rule in entry["rules"]:
                        predicate(rule, rule=True)
            else:
                if item["from"] not in ids or item["to"] not in ids:
                    raise ValueError(f"unknown endpoint: {item['from']} -> {item['to']}")
                if not v2 and kind == "data" and "er" in item["meta"]:
                    entry["er"] = item["meta"]["er"]
                if "er" in entry and (kind != "data" or not matches(ER, entry["er"])):
                    raise ValueError("er must be a cardinality connector on a data edge")
                if "when" in entry:
                    if kind == "data":
                        raise ValueError("data edges cannot have guards")
                    predicate(entry["when"])
            clean[group].append(entry)
    return clean


# Spec: skills/spec-ir/references/spec-ir.md
def condition(item, lang):
    for key, words in (("all", (" and ", " y ")), ("any", (" or ", " o "))):
        if key in item:
            return "(" + words[lang == "es"].join(condition(term, lang) for term in item[key]) + ")"
    value, op = item["value"], item["op"]
    field = item["field"].replace("_", " ")
    if op == "weighted_sum":
        return field + " = " + " + ".join(f"{weight} × {k.replace('_', ' ')}"
                                          for k, weight in value.items())
    if type(value) is bool:
        value = ("sí" if value else "no") if lang == "es" else str(value).lower()
    text = f"{field} {OPS[op]} {str(value).replace('_', ' ')}"
    return text + (" " + item["unit"] if "unit" in item else "")


# Spec: skills/spec-ir/references/spec-ir.md
def node_title(node, lang):
    return node["label"] + (
        (" (propuesta)" if lang == "es" else " (proposed)") if "status" in node else ""
    )


# Spec: skills/spec-ir/references/spec-ir.md
def label(text):
    # Numeric Mermaid entities keep delimiters, directives and line breaks out of the grammar.
    text = " ".join(text.split())
    return "".join(c if c.isalnum() else f"#{ord(c)};" for c in text)


# Spec: skills/spec-ir/references/spec-ir.md
def diagram(graph):
    kind, lang = graph["kind"], graph["lang"]
    lines = [HEAD[kind]]
    ids = {}
    for node in graph["nodes"]:
        name = ids[node["id"]] = f"N{len(ids)}"
        text = label(node_title(node, lang))
        lines.append("    " + {
            "flow": f'{name}["{text}"]', "state": f'state "{text}" as {name}',
            "api": f"participant {name} as {text}", "data": f'{name}["{text}"]',
        }[kind])
    for edge in graph["edges"]:
        text = edge["label"]
        if "when" in edge:
            text += (" — si " if lang == "es" else " — if ") + condition(edge["when"], lang)
        a, b, text = ids[edge["from"]], ids[edge["to"]], label(text)
        if kind == "data":
            connector = edge.get("er", "}o..o{")
            if "er" not in edge:
                text += " (cardinalidad no especificada)" if lang == "es" else " (ER constraints unspecified)"
            line = f'{a} {connector} {b} : "{text}"'
        else:
            line = {"flow": f'{a} -->|"{text}"| {b}', "state": f"{a} --> {b} : {text}",
                    "api": f"{a}->>{b}: {text}"}[kind]
        lines.append("    " + line)
    return lines


# Spec: skills/spec-ir/references/spec-ir.md
def explanation(graph):
    lang = graph["lang"]
    titles = {node["id"]: node_title(node, lang) for node in graph["nodes"]}
    edges = graph["edges"]
    guards = [edge for edge in edges if "when" in edge]
    forks = Counter(edge["from"] for edge in guards)
    chosen = sorted(guards, key=lambda edge: -forks[edge["from"]])[:2] or edges[:2]
    if guards and guards[-1] not in chosen:
        chosen.append(guards[-1])
    parts = []
    for edge in chosen:
        text = f'{titles[edge["from"]]} → {titles[edge["to"]]}'
        if "when" in edge:
            text += (" si " if lang == "es" else " if ") + condition(edge["when"], lang)
        if graph["kind"] == "data":
            text += f' ({edge["label"]}: {edge["er"]})' if "er" in edge else f' ({edge["label"]})'
        parts.append(text)
    rules = [(node, rule) for node in graph["nodes"] for rule in node.get("rules", [])
             if "status" not in rule and "status" not in node]
    rules.sort(key=lambda pair: not (number(pair[1]["value"]) or pair[1]["op"] == "weighted_sum"))
    if rules:
        node, rule = rules[0]
        parts.append(f'{titles[node["id"]]}: {condition(rule, lang)}')
    if not parts:
        parts = list(titles.values())[:2] or (["Grafo vacío"] if lang == "es" else ["Empty graph"])
    prose = ". ".join(" ".join(part.split()) for part in parts) + "."
    # Author strings stay literal Markdown text, including links and HTML delimiters.
    prose = re.sub(r"[&<>\\`*_\[\]~]", lambda m: f"&#{ord(m[0])};", prose)
    return f"{SUMMARY[lang]} {prose}"


# Spec: skills/spec-ir/references/spec-ir.md
def generated_end(tokens, stop):
    if (len(tokens) < 3 or tokens[0].type != "html_block" or tokens[0].content.strip() != START
            or tokens[0].map != [stop, stop + 1] or tokens[1].type != "fence"
            or tokens[1].info.strip() != "mermaid" or tokens[1].map[0] != stop + 1):
        raise ValueError(f"line {stop + 1}: damaged generated region")
    end = tokens[2]
    offset = tokens[1].map[1]
    if (len(tokens) >= 6 and [t.type for t in tokens[2:5]] == ["paragraph_open", "inline", "paragraph_close"]
            and tokens[2].map == [offset + 1, offset + 2]
            and any(tokens[3].content.startswith(heading + " ") for heading in SUMMARY.values())):
        end, offset = tokens[5], offset + 3
    if end.type != "html_block" or end.content.strip() != END or end.map != [offset, offset + 1]:
        raise ValueError(f"line {stop + 1}: damaged generated region")
    return offset + 1


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
            graph = semantic(yaml.load(token.content, Loader=Loader))
            drawing = diagram(graph)
            if graph["id"] in seen:
                raise ValueError(f"duplicate graph: {graph['id']}")
            seen.add(graph["id"])
        except (yaml.YAMLError, ValueError, RecursionError) as exc:
            raise ValueError(f"line {start + 1} (Spec-IR): {exc}") from exc

        prefix, newline = closing[1], closing[3] or ("\r\n" if "\r\n" in source else "\n")
        end = stop
        if stop < len(lines) and lines[stop].rstrip("\r\n").strip() == (prefix + START).strip():
            end = generated_end(tokens[i + 1:i + 7], stop)
            claimed.update((stop, end - 1))
        block = [START, "```mermaid", *drawing, "```"]
        if graph["version"] == 2:
            block.extend(("", explanation(graph), ""))
        block.append(END)
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
