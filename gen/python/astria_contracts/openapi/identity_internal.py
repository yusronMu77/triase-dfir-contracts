# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.

from __future__ import annotations

from typing import Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class Actor(BaseModel):
    """
    Pengguna yang memicu aksi (klaim `act`). Kosong untuk aksi sistem.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    sub: str = Field(..., pattern="^usr_[A-Za-z0-9]+$")
    roles: list[str]
    session_id: str | None = None


class ServiceTokenRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    audience: str = Field(..., pattern="^svc:[a-z][a-z0-9-]*$")
    act: Actor | None = None


class ServiceTokenResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    token: str
    token_type: Literal["Bearer"]
    expires_at: AwareDatetime


class Jwk(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    kty: Literal["OKP"]
    crv: Literal["Ed25519"]
    x: str
    kid: str
    alg: Literal["EdDSA"]
    use: Literal["sig"]


class Jwks(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    keys: list[Jwk]
