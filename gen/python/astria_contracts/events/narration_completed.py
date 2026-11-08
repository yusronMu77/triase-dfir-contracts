# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, RootModel


class EvidenceId(RootModel[str]):
    root: str = Field(..., pattern="^EV-[A-Za-z0-9_-]+$")


class ModelInfo(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    backend: Literal["online", "lokal", "replay", "templat"]
    model_id: str = Field(..., max_length=128, min_length=1)
    cache_hit: bool
    prompt_versi: str = Field(..., max_length=64, min_length=1)


class Klaim(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    klaim: str = Field(..., max_length=1000, min_length=1)
    bukti: list[EvidenceId] = Field(..., min_length=1)
    nilai_dikutip: dict[str, str] | None = None


class Hipotesis(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    teks: str = Field(..., max_length=1000, min_length=1)
    bukti: list[EvidenceId] = Field(..., min_length=1)


class HipotesisTandingan(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    teks: str = Field(..., max_length=1000, min_length=1)
    pembantah: str = Field(..., max_length=1000)


class BelumDiketahuiItem(RootModel[str]):
    root: str = Field(..., max_length=500)


class Narasi(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    ringkasan: list[Klaim]
    hipotesis_utama: Hipotesis
    hipotesis_tandingan: list[HipotesisTandingan]
    belum_diketahui: list[BelumDiketahuiItem]


class NarrationCompleted(BaseModel):
    """
    data untuk narration.completed v1. Penerbit: narrative. Konsumen: verifier. Setiap klaim wajib menunjuk ID bukti.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    attempt: int = Field(..., ge=1, le=2)
    model: ModelInfo
    narasi: Narasi
    pemeriksa_siap: bool
