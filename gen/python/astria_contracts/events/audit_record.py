# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.

from __future__ import annotations

from typing import Any, Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class AuditRecord(BaseModel):
    """
    data untuk audit.record v1 (jalur asinkron) dan isi POST /internal/v1/records (jalur sinkron). Penerbit: semua layanan. Konsumen: audit. Payload maks 4 KiB, tanpa angka pecahan, tanpa nilai rahasia.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    idempotency_key: str = Field(..., max_length=200, min_length=1)
    occurred_at: AwareDatetime
    actor: str = Field(
        ..., description="usr_... untuk pengguna, svc:<nama> untuk layanan.", max_length=64, min_length=1
    )
    actor_type: Literal["user", "service", "system"]
    action: str = Field(..., max_length=100, pattern="^[a-z][a-z0-9_]*(\\.[a-z][a-z0-9_]*)+$")
    target_type: str = Field(..., max_length=64, min_length=1)
    target_id: str = Field(..., max_length=200, min_length=1)
    via: Literal["ui", "api", "bot", "cli", "system"]
    payload: dict[str, Any]
