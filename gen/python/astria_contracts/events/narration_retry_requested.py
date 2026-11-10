# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Kegagalan(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    klaim_no: int = Field(
        ...,
        description="Indeks klaim (mulai 0) menurut urutan pemeriksa: ringkasan, hipotesis_utama, tiap tandingan lalu pembantahnya, belum_diketahui.",
        ge=0,
    )
    kode: str = Field(..., pattern="^[A-Z][A-Z0-9_]*$")


class NarrationRetryRequested(BaseModel):
    """
    data untuk narration.retry_requested v1. Penerbit: verifier. Konsumen: narrative. Dikirim bila percobaan 1 punya klaim gagal; hanya kode kegagalan, tanpa teks klaim atau kutipan log.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    attempt: Literal[2] = Field(..., description="Nomor percobaan yang diminta; selalu 2.")
    kegagalan: list[Kegagalan] = Field(..., min_length=1)
