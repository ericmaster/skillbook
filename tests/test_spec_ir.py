# Spec: skills/spec-ir/references/spec-ir.md
"""Black-box renderer tests, including source preservation on CLI errors."""

import subprocess
import sys
from pathlib import Path

import pytest


RENDER = Path(__file__).resolve().parents[1] / "skills/spec-ir/scripts/render_spec_ir.py"
START, END = "<!-- spec-ir:start -->", "<!-- spec-ir:end -->"
SPEC = '''```yaml spec-ir
id: sample
kind: flow
nodes:
  - {id: 'A-B', type: step, label: 'end', meta: {owner: QA}}
  - {id: 'A B', type: step, label: 'direction TB', meta: {}}
edges:
  - {from: A-B, to: A B, label: '":;|[]#<>&%%', meta: {sla: 30}}
```'''


# Spec: skills/spec-ir/references/spec-ir.md
def run(path):
    return subprocess.run([sys.executable, str(RENDER), str(path)], capture_output=True)


# Spec: skills/spec-ir/references/spec-ir.md
def test_all_kinds_and_refresh(tmp_path):
    path = tmp_path / "graph.md"
    kinds = ["flow", "state", "api", "data"]
    specs = [SPEC.replace("kind: flow", f"kind: {k}").replace("id: sample", f"id: {k}") for k in kinds]
    unrelated = f"````markdown\n{SPEC}\n````\n```mermaid\nunmanaged\n```\n"
    path.write_bytes((unrelated + "\n".join(specs)).replace("\n", "\r\n").encode())
    assert run(path).returncode == 0
    result = path.read_bytes()
    assert result.count(START.encode()) == len(kinds)
    assert result.startswith(unrelated.replace("\n", "\r\n").encode())
    assert result.endswith(END.encode())
    for head in ("flowchart TD", "stateDiagram-v2", "sequenceDiagram", "erDiagram"):
        assert f"{START}\r\n```mermaid\r\n{head}\r\n".encode() in result
    assert b'#34;#58;#59;#124;#91;#93;#35;#60;#62;#38;#37;#37;' in result
    assert b"N0->>N1:" in result
    assert run(path).returncode == 0 and path.read_bytes() == result
    path.write_bytes(result.replace(b"label: 'end'", b"label: 'Approved'"))
    assert run(path).returncode == 0
    assert b'["Approved"]' in path.read_bytes() and b'["end"]' not in path.read_bytes()


# Spec: skills/spec-ir/references/spec-ir.md
@pytest.mark.parametrize("bad", [
    SPEC.replace("kind: flow", "kind: ["), SPEC.replace("kind: flow", "kind: api\nkind: flow"),
    SPEC.replace("meta: {}", "meta: []"), SPEC.replace("meta: {}", "latency: 30"),
    SPEC.replace("id: 'A B'", "id: 'A-B'"), SPEC.replace("to: A B", "to: unknown"),
    SPEC.replace("id: sample", "id: 42"), SPEC.replace("kind: flow", "kind: jobs"),
    SPEC[:-3], SPEC + f"\n{START}\nordinary text\n{END}", SPEC + f"\n{END}",
    SPEC + "\n" + SPEC,
])
def test_invalid_later_block_preserves_whole_file(tmp_path, bad):
    path = tmp_path / "bad.md"
    original = (SPEC.replace("sample", "first") + "\n" + bad).encode()
    path.write_bytes(original)
    proc = run(path)
    assert proc.returncode != 0 and str(path).encode() in proc.stderr and b"line " in proc.stderr
    assert b"Traceback" not in proc.stderr and path.read_bytes() == original


# Spec: skills/spec-ir/references/spec-ir.md
def test_nested_fence_and_crlf(tmp_path):
    path = tmp_path / "quoted.md"
    source = "".join("> " + line + "\r\n" for line in SPEC.splitlines())
    path.write_bytes(source.encode())
    assert run(path).returncode == 0
    expected = path.read_bytes()
    assert expected.startswith((source + "> " + START + "\r\n> ```mermaid").encode())
    assert run(path).returncode == 0 and path.read_bytes() == expected


V2 = """```yaml spec-ir
version: 2
id: sample
kind: flow
lang: es
meta: {owner: QA, refs: ['./notes.md#scope']}
nodes:
  - id: reading
    type: step
    label: Leer
    rules:
      - {field: deadline, op: lte, value: 120, unit: s}
    meta: {owner: qa}
  - {id: answer, type: step, label: Responder}
edges:
  - from: reading
    to: answer
    label: Empezar
    when: {all: [{field: playback, op: eq, value: done}, {field: microphone, op: eq, value: true}]}
    meta: {refs: ['#example']}
```"""


# Spec: skills/spec-ir/references/spec-ir.md
def test_v2_refresh_independence_and_idempotency(tmp_path):
    path = tmp_path / "graph.md"
    rest = "\n\nLeave **this** alone.\n"
    path.write_text(V2 + f"\n{START}\n```mermaid\nstale\n```\n{END}" + rest)
    assert run(path).returncode == 0
    text = path.read_text()
    assert text.endswith(rest) and "stale" not in text and text.count(START) == 1
    assert 'N0 -->|"Empezar — si (playback = done y microphone = sí)"| N1' in text
    assert ("**Descripción.** En el paso «Leer», se puede pasar a «Responder» "
            "cuando «playback» tiene el valor «done» y se cumple «microphone».") in text
    assert "deadline es como máximo 120 s" in text
    assert run(path).returncode == 0 and path.read_text() == text
    no_meta = "\n".join(line for line in V2.splitlines() if not line.lstrip().startswith("meta:"))
    path.write_text(no_meta + "\n" + text[text.index(START):])
    assert run(path).returncode == 0 and path.read_text().split(START)[1] == text.split(START)[1]
    path.write_text(text.replace("value: done", "value: failed"))
    assert run(path).returncode == 0
    assert "playback = failed" in path.read_text() and "«playback» tiene el valor «failed»" in path.read_text()


# Spec: skills/spec-ir/references/spec-ir.md
@pytest.mark.parametrize(("before", "after"), [
    ("owner: qa", "rules: 'never do this'"),
    ("owner: qa", "owner: 'review before opening'"),
    ("['#example']", "'see the notes'"),
    ("version: 2", "version: true"),
    ("value: 120", "value: 'use limited time'"),
    ("value: 120", "value: .inf"),
    ("op: lte", "op: [lte]"),
    ("value: 120", "value: 120, description: 'long prose'"),
    ("op: eq, value: done", "op: [eq], value: done"),
    ("op: eq, value: done", "op: eq, value: 'when the audio is done'"),
    ("label: Responder", "label: 'Responder', status: active"),
    ("kind: flow", "kind: data"),
])
def test_v2_rejects_freeform_or_invalid_semantics(tmp_path, before, after):
    path = tmp_path / "invalid.md"
    source = V2.replace(before, after)
    path.write_text(source)
    result = run(path)
    assert result.returncode != 0 and b"Traceback" not in result.stderr and path.read_text() == source


# Spec: skills/spec-ir/references/spec-ir.md
def test_v2_er_is_semantic_and_legacy_er_is_unchanged(tmp_path):
    path = tmp_path / "er.md"
    v2 = V2.replace("kind: flow", "kind: data")
    v2 = v2.replace(next(line for line in v2.splitlines() if "when:" in line), '    er: "||--o{"')
    path.write_text(v2)
    assert run(path).returncode == 0 and "N0 ||--o{ N1" in path.read_text()
    assert "cardinalidad: ||--o{" in path.read_text()
    legacy = SPEC.replace("kind: flow", "kind: data").replace("sla: 30", 'er: "||--o{"')
    path.write_text(legacy)
    assert run(path).returncode == 0 and "N0 ||--o{ N1" in path.read_text()
    assert "**Description.**" not in path.read_text()


# Spec: skills/spec-ir/references/spec-ir.md
def test_v2_weighted_sum_preserves_weights(tmp_path):
    path = tmp_path / "weights.md"
    path.write_text(V2.replace("deadline, op: lte, value: 120, unit: s",
                               "grade, op: weighted_sum, value: {first: 0.123456789, second: 0.876543211}"))
    assert run(path).returncode == 0
    result = path.read_text()
    assert "grade se calcula con un 12.3456789 % de first y un 87.6543211 % de second" in result
    assert run(path).returncode == 0 and path.read_text() == result


# Spec: skills/spec-ir/references/spec-ir.md
@pytest.mark.parametrize("heading", ["Generated overview", "Resumen generado"])
def test_v2_replaces_old_overview(tmp_path, heading):
    path = tmp_path / "old.md"
    path.write_text(V2 + f"\n{START}\n```mermaid\nold\n```\n\n**{heading}.** Old text.\n\n{END}\n")
    assert run(path).returncode == 0
    assert "**Descripción.**" in path.read_text() and "Old text." not in path.read_text()
