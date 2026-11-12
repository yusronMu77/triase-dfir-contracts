# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.

from __future__ import annotations

from typing import Any, Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, RootModel


class CatalogKind(
    RootModel[
        Literal[
            "alert_penjelasan",
            "pola_insiden",
            "temuan_korelasi",
            "langkah",
            "sla",
            "bobot_skor",
            "aturan_android",
            "aturan_peran",
            "aset",
        ]
    ]
):
    root: Literal[
        "alert_penjelasan",
        "pola_insiden",
        "temuan_korelasi",
        "langkah",
        "sla",
        "bobot_skor",
        "aturan_android",
        "aturan_peran",
        "aset",
    ]


class SettingSource(RootModel[Literal["bawaan", "berkas", "database", "env"]]):
    root: Literal["bawaan", "berkas", "database", "env"]


class SettingValue(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    key: str
    value: Any = Field(..., description="Nilai JSON sesuai tipe kunci pada registri")
    source: SettingSource
    version: int = Field(..., description="0 bila belum pernah diubah di database", ge=0)
    updated_by: str | None = None
    updated_at: AwareDatetime | None = None
    locked: bool | None = Field(None, description="true bila dikunci variabel lingkungan ASTRIA_*")


class SecretStatus(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    key: str
    terisi: bool
    version: int = Field(..., ge=0)
    updated_by: str | None = None
    updated_at: AwareDatetime | None = None


class SettingList(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    items: list[SettingValue | SecretStatus]


class PutSettingRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    value: Any = Field(..., description="Nilai JSON; divalidasi dengan tipe dan batas kunci")
    if_version: int = Field(..., ge=0)
    alasan: str | None = Field(None, max_length=500)


class PutSecretRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    value: str = Field(..., max_length=4096, min_length=1)


class SecretValue(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    key: str
    value: str


class ChannelPolicy(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    channel_id: str = Field(..., pattern="^[a-z][a-z0-9-]*$")
    active: bool
    max_detail: Literal["ringkas", "sedang", "penuh"]
    min_band: Literal["RENDAH", "SEDANG", "TINGGI", "KRITIS"] | None = Field(
        None, description="Ambang band terendah yang dikirim ke kanal"
    )
    version: int = Field(..., ge=0)
    updated_by: str | None = None
    updated_at: AwareDatetime | None = None


class ChannelPolicyList(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    items: list[ChannelPolicy]


class PutChannelPolicyRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    active: bool
    max_detail: Literal["ringkas", "sedang", "penuh"]
    min_band: Literal["RENDAH", "SEDANG", "TINGGI", "KRITIS"] | None = None
    if_version: int = Field(..., ge=0)


class EffectiveSettings(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    scope: str
    values: dict[str, Any] = Field(..., description="kunci lengkap (mis. chat.allow_t2) -> nilai")


class CatalogVersion(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    kind: CatalogKind
    version: int = Field(..., ge=1)
    status: Literal["draft", "ditinjau", "aktif", "arsip"]
    content_hash: str = Field(..., pattern="^sha256:[0-9a-f]{64}$")
    schema_version: str
    created_by: str
    reviewed_by: str | None = None
    activated_at: AwareDatetime | None = None


class CatalogVersionList(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    items: list[CatalogVersion]


class CreateCatalogDraftRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    content: dict[str, Any] = Field(
        ..., description="Dokumen utuh satu versi katalog; divalidasi dengan skema jenisnya"
    )
    schema_version: str | None = "1"


class CatalogCoverage(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    kind: CatalogKind
    catalog_version: int
    complete: bool
    issues: list[str]


class ActiveCatalog(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    catalog_version: int = Field(..., ge=1)
    content_hash: str = Field(..., pattern="^sha256:[0-9a-f]{64}$")
