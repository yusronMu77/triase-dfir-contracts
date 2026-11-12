# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ConfigChanged(BaseModel):
    """
    data untuk config.changed v1. Penerbit: config. Konsumen: api, triage, narrative, ticket, notifier, scheduler, ingest. Event hanya memberi tahu bahwa sesuatu berubah; nilai efektif dan katalog dibaca konsumen lewat /svc/v1 config. Tidak pernah memuat nilai pengaturan atau rahasia. scope=setting memakai key dan value_version; scope=secret memakai key dan value_version; scope=catalog memakai kind, catalog_version, dan content_hash; scope=channel_policy memakai key (channel_id) dan value_version.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    scope: Literal["setting", "secret", "catalog", "channel_policy"]
    key: str | None = Field(
        None,
        description="Kunci pengaturan atau rahasia, atau channel_id untuk channel_policy.",
        max_length=200,
        min_length=1,
    )
    kind: str | None = Field(
        None, description="Jenis katalog (scope=catalog).", max_length=64, pattern="^[a-z][a-z0-9_]*$"
    )
    value_version: int | None = Field(None, ge=1)
    catalog_version: int | None = Field(None, ge=1)
    content_hash: str | None = Field(
        None, description="sha256 JSON kanonik katalog aktif, awalan sha256:.", pattern="^sha256:[0-9a-f]{64}$"
    )
