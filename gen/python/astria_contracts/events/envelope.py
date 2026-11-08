# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.

from __future__ import annotations

from typing import Any

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class Correlation(BaseModel):
    """
    Kunci korelasi. Event tentang kartu membawa card_id dan version; urutan per card_id dijaga konsumen.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    card_id: str | None = Field(None, pattern="^IC-[0-9]{8}-[0-9]{3,}$")
    version: int | None = Field(None, description="Versi kartu (bukan versi skema).", ge=1)
    job_id: str | None = Field(None, max_length=64, min_length=1)
    source_id: str | None = Field(None, max_length=64, min_length=1)


class Envelope(BaseModel):
    """
    Amplop untuk semua event Astria. Isi event ada di `data`; skemanya di <type>.schema.json.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    id: str = Field(
        ...,
        description="ID unik event. Dipakai sebagai Nats-Msg-Id dan kunci idempoten konsumen. UUID disarankan.",
        max_length=64,
        min_length=1,
        pattern="^[A-Za-z0-9_-]+$",
    )
    type: str = Field(
        ...,
        description="Jenis event, mis. evidence.ingested. Subjek NATS = astria.<type>.",
        pattern="^[a-z][a-z0-9_]*(\\.[a-z][a-z0-9_]*)+$",
    )
    version: int = Field(
        ..., description="Versi skema `data` untuk jenis ini. Field opsional baru tidak menaikkan versi.", ge=1
    )
    occurred_at: AwareDatetime = Field(..., description="Waktu kejadian, UTC, RFC 3339.")
    trace_id: str = Field(
        ...,
        description="ID trace W3C (32 heksadesimal) untuk menyambung log dan trace lintas layanan.",
        pattern="^[0-9a-f]{32}$",
    )
    correlation: Correlation
    data: dict[str, Any] = Field(..., description="Isi event; divalidasi dengan skema per jenis.")
