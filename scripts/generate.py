"""Bangkitkan model Pydantic dari kontrak ke gen/python/astria_contracts.

Jalankan dari root repo: `uv run python scripts/generate.py`. Hasilnya di-commit dan tidak diedit tangan.
CI menjalankan ulang lalu `git diff --exit-code` untuk memastikan hasil generasi sama dengan sumber.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVENTS = ROOT / "events"
OPENAPI = ROOT / "openapi"
PKG = ROOT / "gen" / "python" / "astria_contracts"

HEADER = "# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.\n"

COMMON_FLAGS = [
    "--output-model-type",
    "pydantic_v2.BaseModel",
    "--target-python-version",
    "3.13",
    "--disable-timestamp",
    "--use-standard-collections",
    "--use-union-operator",
    "--use-schema-description",
    "--use-title-as-name",
    "--field-constraints",
    "--enum-field-as-literal",
    "all",
    "--use-double-quotes",
    "--extra-fields",
    "forbid",
    "--custom-file-header",
    HEADER.strip(),
    "--formatters",
    "ruff-format",
]


def module_name(stem: str) -> str:
    return stem.replace(".schema", "").replace(".", "_").replace("-", "_")


def codegen(src: Path, dst: Path, input_type: str) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        "-m",
        "datamodel_code_generator",
        "--input",
        str(src),
        "--input-file-type",
        input_type,
        "--output",
        str(dst),
        *COMMON_FLAGS,
    ]
    subprocess.run(cmd, check=True, cwd=ROOT)


def main() -> None:
    if PKG.exists():
        shutil.rmtree(PKG)
    (PKG / "events").mkdir(parents=True)
    (PKG / "openapi").mkdir(parents=True)

    catalog = json.loads((EVENTS / "catalog.json").read_text(encoding="utf-8"))
    registry_lines: list[str] = []

    codegen(EVENTS / "envelope.schema.json", PKG / "events" / "envelope.py", "jsonschema")
    for entry in catalog["events"]:
        schema = EVENTS / entry["schema"]
        mod = module_name(Path(entry["schema"]).stem)
        codegen(schema, PKG / "events" / f"{mod}.py", "jsonschema")
        title = json.loads(schema.read_text(encoding="utf-8"))["title"]
        registry_lines.append(f"from astria_contracts.events.{mod} import {title}")

    for spec in sorted(OPENAPI.glob("*.yaml")):
        codegen(spec, PKG / "openapi" / f"{module_name(spec.stem)}.py", "openapi")

    (PKG / "events" / "__init__.py").write_text(HEADER, encoding="utf-8")
    (PKG / "openapi" / "__init__.py").write_text(HEADER, encoding="utf-8")

    mapping = []
    for entry in catalog["events"]:
        title = json.loads((EVENTS / entry["schema"]).read_text(encoding="utf-8"))["title"]
        mapping.append(
            f'    "{entry["type"]}": EventSpec("{entry["type"]}", {entry["version"]}, "{entry["subject"]}", {title}),'
        )

    registry = (
        HEADER
        + '"""Katalog event: jenis -> versi, subjek NATS, dan model data."""\n\n'
        + "from dataclasses import dataclass\n\n"
        + "from pydantic import BaseModel\n\n"
        + "\n".join(sorted(registry_lines))
        + "\n\n\n@dataclass(frozen=True)\nclass EventSpec:\n"
        + "    type: str\n    version: int\n    subject: str\n    model: type[BaseModel]\n\n\n"
        + f'STREAM_NAME = "{catalog["stream"]["name"]}"\n'
        + f"STREAM_SUBJECTS = {catalog['stream']['subjects']!r}\n"
        + f"DUPLICATE_WINDOW_SECONDS = {catalog['stream']['duplicate_window_seconds']}\n\n"
        + "EVENTS: dict[str, EventSpec] = {\n"
        + "\n".join(mapping)
        + "\n}\n"
    )
    (PKG / "registry.py").write_text(registry, encoding="utf-8")

    init = (
        HEADER
        + '"""Model kontrak Astria hasil generasi dan pembantu memuat skema serta contoh."""\n\n'
        + "import json\nfrom importlib import resources\nfrom pathlib import Path\nfrom typing import Any\n\n"
        + "from astria_contracts.events.envelope import Correlation, Envelope\n"
        + "from astria_contracts.registry import DUPLICATE_WINDOW_SECONDS, EVENTS, STREAM_NAME, STREAM_SUBJECTS, EventSpec\n\n"
        + '__all__ = ["DUPLICATE_WINDOW_SECONDS", "EVENTS", "STREAM_NAME", "STREAM_SUBJECTS", "Correlation", "Envelope",'
        + ' "EventSpec", "example", "schema_dir"]\n\n\n'
        + "def schema_dir() -> Path:\n"
        + '    """Folder skema: di wheel ada di astria_contracts/schemas, di checkout ada di root repo."""\n'
        + '    packaged = Path(str(resources.files("astria_contracts"))) / "schemas"\n'
        + "    if packaged.is_dir():\n"
        + "        return packaged\n"
        + "    return Path(__file__).resolve().parents[3]\n\n\n"
        + "def example(event_type: str) -> dict[str, Any]:\n"
        + '    """Contoh amplop valid untuk satu jenis event (dipakai uji kontrak konsumen)."""\n'
        + '    path = schema_dir() / "events" / "examples" / f"{event_type}.json"\n'
        + '    return json.loads(path.read_text(encoding="utf-8"))\n'
    )
    (PKG / "__init__.py").write_text(init, encoding="utf-8")
    (PKG / "py.typed").write_text("", encoding="utf-8")

    subprocess.run([sys.executable, "-m", "ruff", "format", str(PKG)], check=True, cwd=ROOT)
    subprocess.run(
        [sys.executable, "-m", "ruff", "check", "--fix", "--select", "I,F401", str(PKG)], check=True, cwd=ROOT
    )
    subprocess.run([sys.executable, "-m", "ruff", "format", str(PKG)], check=True, cwd=ROOT)


if __name__ == "__main__":
    main()
