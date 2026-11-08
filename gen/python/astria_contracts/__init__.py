# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.
"""Model kontrak Astria hasil generasi dan pembantu memuat skema serta contoh."""

import json
from importlib import resources
from pathlib import Path
from typing import Any

from astria_contracts.events.envelope import Correlation, Envelope
from astria_contracts.registry import DUPLICATE_WINDOW_SECONDS, EVENTS, STREAM_NAME, STREAM_SUBJECTS, EventSpec

__all__ = [
    "DUPLICATE_WINDOW_SECONDS",
    "EVENTS",
    "STREAM_NAME",
    "STREAM_SUBJECTS",
    "Correlation",
    "Envelope",
    "EventSpec",
    "example",
    "schema_dir",
]


def schema_dir() -> Path:
    """Folder skema: di wheel ada di astria_contracts/schemas, di checkout ada di root repo."""
    packaged = Path(str(resources.files("astria_contracts"))) / "schemas"
    if packaged.is_dir():
        return packaged
    return Path(__file__).resolve().parents[3]


def example(event_type: str) -> dict[str, Any]:
    """Contoh amplop valid untuk satu jenis event (dipakai uji kontrak konsumen)."""
    path = schema_dir() / "events" / "examples" / f"{event_type}.json"
    return json.loads(path.read_text(encoding="utf-8"))
