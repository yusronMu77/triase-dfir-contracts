# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.

from __future__ import annotations

from typing import Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class IdentityRevoked(BaseModel):
    """
    data untuk identity.revoked v1. Penerbit: identity. Konsumen: notifier (meneruskan ke gateway untuk menghapus ikatan kanal) dan api (membuang cache sesi dan menutup SSE). Terbit saat akun dinonaktifkan, peran diganti atau dicabut, kata sandi diganti oleh admin, atau semua sesi dicabut. Tidak memuat username, token, atau alasan bebas.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    user_id: str = Field(..., pattern="^usr_[A-Za-z0-9]+$")
    reason: Literal["akun_nonaktif", "peran_berubah", "kata_sandi_diganti", "sesi_dicabut"]
    revoked_at: AwareDatetime
    roles_after: list[Literal["analis", "dfir", "pimpinan", "admin"]] | None = Field(
        None,
        description="Peran pengguna sesudah perubahan; kosong bila akun nonaktif. Hanya diisi untuk reason peran_berubah.",
    )
