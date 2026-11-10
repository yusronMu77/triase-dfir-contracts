# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, RootModel


class CatalogVersion(RootModel[int]):
    root: int = Field(..., ge=0)


class Sha256Ref(RootModel[str]):
    root: str = Field(..., pattern="^sha256:[0-9a-f]{64}$")


class EvidenceId(RootModel[str]):
    root: str = Field(..., pattern="^EV-[A-Za-z0-9_-]+$")


class Faktor(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    nama: str = Field(..., min_length=1)
    nilai: int
    alasan: str


class Entitas(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    jenis: str = Field(..., min_length=1)
    nilai: str = Field(..., min_length=1)
    peran: str = Field(..., min_length=1)
    bukti: list[EvidenceId] = Field(..., min_length=1)


class BuktiRef(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: EvidenceId
    sha256: str = Field(..., pattern="^[0-9a-f]{64}$")


class TemuanKorelasiItem(RootModel[str]):
    root: str = Field(..., pattern="^K-[A-Z0-9-]+$")


class TeknikAttack(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: str = Field(..., pattern="^T[0-9]{4}(\\.[0-9]{3})?$")
    taktik: str = Field(..., pattern="^[a-z]+(-[a-z]+)*$")


class Kode(BaseModel):
    """
    Bagian kartu yang dihitung deterministik oleh triage.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    judul: str = Field(..., max_length=200, min_length=1)
    pola: str = Field(..., pattern="^P-[A-Z0-9-]+$")
    skor: int = Field(..., ge=0, le=100)
    band: Literal["KRITIS", "TINGGI", "SEDANG", "RENDAH"]
    faktor: list[Faktor]
    entitas: list[Entitas]
    bukti: list[BuktiRef] = Field(..., min_length=1)
    teknik_attack: list[TeknikAttack] | None = Field(
        None,
        description="Teknik ATT&CK dari tag alert. Opsional (v0.2.0); verifier menolak klaim yang menyebut teknik di luar daftar ini.",
    )
    temuan_korelasi: list[TemuanKorelasiItem] | None = Field(
        None,
        description="Kode aturan korelasi yang terpicu (K-...). Opsional (v0.2.0); verifier menolak klaim yang menyebut temuan di luar daftar ini.",
    )


class CardSkeletonCreated(BaseModel):
    """
    data untuk card.skeleton.created v1. Penerbit: triage. Konsumen: narrative. Skor dan band hanya ditulis triage.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    paket_hash: Sha256Ref
    catalog_version: dict[str, CatalogVersion] = Field(
        ..., description="Versi tiap katalog yang dipakai saat menghitung."
    )
    algo_version: str = Field(..., max_length=64, min_length=1)
    kode: Kode
