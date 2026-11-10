# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.

from __future__ import annotations

from typing import Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class DigestPublished(BaseModel):
    """
    data untuk digest.published v1. Penerbit: scheduler. Konsumen: notifier, api. Correlation membawa digest_id. Dokumen dibaca lewat scheduler /svc/v1/digests/{digest_id}/dokumen; event tidak memuat isi digest.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    jenis: Literal["harian"]
    periode_mulai: AwareDatetime
    periode_selesai: AwareDatetime
    sha256: str = Field(..., description="SHA-256 dokumen HTML digest.", pattern="^[0-9a-f]{64}$")
    mode_narasi: Literal["online", "lokal", "replay", "templat"]
    audit_head_hash: str | None = Field(
        None,
        description="Kepala rantai audit saat digest dibuat; opsional selama audit belum punya endpoint kepala rantai.",
        pattern="^[0-9a-f]{64}$",
    )
    terlambat: bool = Field(
        ..., description="Digest dijalankan setelah jadwalnya (mis. layanan sempat mati), masih dalam toleransi."
    )
