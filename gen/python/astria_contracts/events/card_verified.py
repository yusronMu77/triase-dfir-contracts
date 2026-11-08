# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, RootModel


class KodeGagalItem(RootModel[str]):
    root: str = Field(..., pattern="^[A-Z][A-Z0-9_]*$")


class KlaimDitolak(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    klaim_index: int = Field(..., ge=0)
    kode_gagal: list[KodeGagalItem] = Field(..., min_length=1)


class DokumenKartu(BaseModel):
    """
    Kartu lengkap setelah kebijakan: kode dari triage, model setelah klaim yang gagal dibuang. Bentuk rinci = kartu v2 (Tahap 1).
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    card_id: str = Field(..., pattern="^IC-[0-9]{8}-[0-9]{3,}$")
    version: int = Field(..., ge=1)
    kode: dict[str, Any]
    model: dict[str, Any]


class CardVerified(BaseModel):
    """
    data untuk card.verified v1. Penerbit: verifier. Konsumen: ticket. Status final pemeriksaan klaim terhadap bukti asli.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    status: Literal["LULUS", "SEBAGIAN", "TEMPLAT"]
    percobaan: int = Field(..., ge=1, le=2)
    klaim_total: int = Field(..., ge=0)
    klaim_lolos: int = Field(..., ge=0)
    ditolak: list[KlaimDitolak]
    policy_version: str = Field(..., max_length=64, min_length=1)
    checker_version: str = Field(..., max_length=64, min_length=1)
    model_terperiksa: str = Field(..., max_length=128, min_length=1)
    evidence_set_hash: str = Field(..., pattern="^sha256:[0-9a-f]{64}$")
    dokumen: DokumenKartu
