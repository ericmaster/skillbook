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
