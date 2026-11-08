# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.

from __future__ import annotations

from typing import Any, Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class RecordReceipt(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    seq: int = Field(..., ge=0)
    entry_hash: str = Field(..., pattern="^[0-9a-f]{64}$")
    recorded_at: AwareDatetime
    duplicate: bool


class Entry(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    seq: int = Field(..., ge=0)
    occurred_at: AwareDatetime
    recorded_at: AwareDatetime
    actor: str
    actor_type: str
    action: str
    target_type: str
    target_id: str
    via: str
    idempotency_key: str
    payload: dict[str, Any]
    payload_hash: str = Field(..., pattern="^[0-9a-f]{64}$")
    prev_hash: str = Field(..., pattern="^[0-9a-f]{64}$")
    entry_hash: str = Field(..., pattern="^[0-9a-f]{64}$")


class RecordPage(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    items: list[Entry]
    next_from_seq: int | None


class VerifyResult(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    status: Literal["selesai"]
    from_seq: int
    to_seq: int | None
    checked: int
    ok: bool
    first_bad_seq: int | None = None
    reason: str | None = None
