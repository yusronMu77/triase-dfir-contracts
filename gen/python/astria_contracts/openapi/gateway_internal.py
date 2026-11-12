# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.

from __future__ import annotations

from typing import Any

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, RootModel


class PayloadValue1(RootModel[str]):
    root: str = Field(
        ...,
        description="Skalar, atau daftar teks pendek (mis. `teknik` ATT&CK). Objek bersarang ditolak.",
        max_length=500,
    )


class PayloadValue2Item(RootModel[str]):
    root: str = Field(..., max_length=40)


class PayloadValue2(RootModel[list[PayloadValue2Item]]):
    root: list[PayloadValue2Item] = Field(
        ...,
        description="Skalar, atau daftar teks pendek (mis. `teknik` ATT&CK). Objek bersarang ditolak.",
        max_length=20,
    )


class PayloadValue(RootModel[PayloadValue1 | int | float | bool | PayloadValue2 | None]):
    root: PayloadValue1 | int | float | bool | PayloadValue2 | None = Field(
        ..., description="Skalar, atau daftar teks pendek (mis. `teknik` ATT&CK). Objek bersarang ditolak."
    )


class ChannelPayload(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    channel_id: str = Field(..., pattern="^(\\*|[a-z][a-z0-9_-]{0,63})$")
    payload: dict[str, PayloadValue | None] | None = Field(None, max_length=20)


class EventIn(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    event_id: str = Field(..., pattern="^[A-Za-z0-9._:-]{1,100}$")
    type: str = Field(..., max_length=64)
    occurred_at: AwareDatetime
    channels: list[ChannelPayload] | None = Field(None, max_length=20)


class EventAccepted(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    event_id: str
    identities: int | None = Field(None, description="Hanya untuk identity.revoked: jumlah ikatan yang dicabut", ge=0)


class SecretIn(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    value: str = Field(..., max_length=4096, min_length=1)


class WhatsAppIn(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    id: str = Field(..., pattern="^[A-Za-z0-9._:-]{1,128}$")
    dari: str = Field(..., pattern="^[0-9]{8,15}$")
    teks: str
    waktu: AwareDatetime


class Outbox(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    pending: int
    sending: int
    sent: int
    dead: int


class Whatsapp(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    enabled: bool | None = None


class Email(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    enabled: bool | None = None


class GatewayStatus(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    outbox: Outbox
    oldest_pending_at: AwareDatetime | None = None
    telegram: dict[str, Any]
    whatsapp: Whatsapp
    email: Email
    public_listener: bool
