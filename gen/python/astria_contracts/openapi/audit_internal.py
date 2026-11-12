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


class VerifyRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    from_seq: int | None = Field(None, ge=1)
    to_seq: int | None = Field(None, ge=1)


class VerifyResult(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    job_id: str | None = Field(None, pattern="^ver_[A-Za-z0-9]+$")
    status: Literal["berjalan", "selesai", "gagal"]
    from_seq: int
    to_seq: int | None = None
    checked: int
    ok: bool | None = Field(None, description="null selama berjalan atau bila tugas gagal")
    first_bad_seq: int | None = None
    reason: str | None = Field(
        None,
        description="nomor_urut_berlubang, prev_hash_tidak_cocok, payload_hash_tidak_cocok, entry_hash_tidak_cocok",
    )
    anchor_match: bool | None = Field(None, description="null bila tidak ada jangkar dalam rentang")
    started_at: AwareDatetime | None = None
    finished_at: AwareDatetime | None = None


class Anchor(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    anchor_id: int = Field(..., ge=1)
    seq: int = Field(..., ge=1)
    entry_hash: str = Field(..., pattern="^[0-9a-f]{64}$")
    created_at: AwareDatetime
    exported_to: str | None = None


class AnchorPage(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    items: list[Anchor]
