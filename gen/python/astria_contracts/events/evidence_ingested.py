# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class RecordRange(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    from_: int = Field(..., alias="from", ge=0)
    to: int = Field(..., ge=0)


class EvidenceIngested(BaseModel):
    """
    data untuk evidence.ingested v1. Penerbit: ingest. Konsumen: triage. Tidak memuat seluruh ID bukti; triage mengambilnya lewat API per rentang. file_sha256 dan batch_sha256 memungkinkan konsumen memeriksa keutuhan bukti.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    source_id: str = Field(..., max_length=64, min_length=1)
    count: int = Field(..., description="Jumlah record bukti dalam batch.", ge=0)
    record_range: RecordRange = Field(..., title="RecordRange")
    batch_ref: str = Field(..., description="Rujukan API baca bukti untuk batch ini.", max_length=256, min_length=1)
    alert_ids_count: int | None = Field(None, ge=0)
    file_sha256: str | None = Field(
        None,
        description="SHA-256 (hex huruf kecil) bytes mentah seluruh berkas sumber. Sama untuk semua batch dari berkas yang sama. Opsional demi kompatibilitas; ingest selalu mengisi.",
        pattern="^[0-9a-f]{64}$",
    )
    batch_sha256: str | None = Field(
        None,
        description="SHA-256 (hex huruf kecil) dari record_sha256 tiap bukti dalam record_range, diurutkan record_no, dipisah satu karakter baris baru (LF). Opsional demi kompatibilitas; ingest selalu mengisi.",
        pattern="^[0-9a-f]{64}$",
    )
