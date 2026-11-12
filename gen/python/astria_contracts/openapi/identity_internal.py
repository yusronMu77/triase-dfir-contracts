# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.

from __future__ import annotations

from typing import Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, RootModel


class Role(RootModel[Literal["analis", "dfir", "pimpinan", "admin"]]):
    root: Literal["analis", "dfir", "pimpinan", "admin"]


class Actor(BaseModel):
    """
    Pengguna yang memicu aksi (klaim `act`). Kosong untuk aksi sistem. `reauth_at` hanya diisi identity dari sesi
    `session_id`; nilai dari pemohon diabaikan.

    """

    model_config = ConfigDict(
        extra="forbid",
    )
    sub: str = Field(..., pattern="^usr_[A-Za-z0-9]+$")
    roles: list[str]
    session_id: str | None = None
    reauth_at: AwareDatetime | None = None


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


class ClientHashes(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    ip_hash: str | None = Field(None, pattern="^[0-9a-f]{64}$")
    user_agent_hash: str | None = Field(None, pattern="^[0-9a-f]{64}$")


class LoginRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    username: str = Field(..., max_length=128, min_length=1)
    password: str = Field(..., max_length=256, min_length=1)
    client: ClientHashes | None = None


class SessionUser(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    user_id: str = Field(..., pattern="^usr_[A-Za-z0-9]+$")
    username: str
    roles: list[Role]


class LoginResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    session_token: str = Field(..., description="32 byte acak, base64url tanpa padding", max_length=43, min_length=43)
    expires_at: AwareDatetime
    idle_expires_at: AwareDatetime
    user: SessionUser


class TokenRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    token: str = Field(..., max_length=128, min_length=1)


class ReauthRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    token: str = Field(..., max_length=128, min_length=1)
    password: str = Field(..., max_length=256, min_length=1)


class ReauthResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    reauth_at: AwareDatetime


class Introspection(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    active: bool
    user_id: str | None = None
    roles: list[Role] | None = None
    reauth_at: AwareDatetime | None = None
    session_id: str | None = None


class User(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    user_id: str = Field(..., pattern="^usr_[A-Za-z0-9]+$")
    username: str
    display_name: str
    active: bool
    roles: list[Role]
    created_at: AwareDatetime
    updated_at: AwareDatetime


class UserPage(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    items: list[User]
    next_cursor: str | None


class CreateUserRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    username: str = Field(..., pattern="^[A-Za-z0-9._-]{3,64}$")
    display_name: str = Field(..., max_length=128, min_length=1)
    password: str = Field(..., max_length=256, min_length=12)
    roles: list[Role] = Field(..., min_length=1)


class UpdateUserRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    display_name: str | None = Field(None, max_length=128, min_length=1)
    active: bool | None = None
    password: str | None = Field(None, max_length=256, min_length=12)


class SetRolesRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    roles: list[Role] = Field(..., min_length=1)


class PairingCodeRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    channel: str | None = Field(None, description="Kanal yang dituju; kosong = bebas.", pattern="^[a-z][a-z0-9-]*$")


class PairingCode(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    code: str = Field(..., description="8 karakter Crockford base32 huruf besar", pattern="^[0-9A-HJKMNP-TV-Z]{8}$")
    channel: str | None = None
    expires_at: AwareDatetime


class PairingClaim(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    channel: str = Field(..., pattern="^[a-z][a-z0-9-]*$")
    external_id_hash: str = Field(..., pattern="^[0-9a-f]{64}$")
    code: str = Field(..., max_length=16, min_length=8)


class PairingClaimResult(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    user_id: str = Field(..., pattern="^usr_[A-Za-z0-9]+$")
    claimed_at: AwareDatetime


class RotatedServiceKey(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    service: str
    key_id: str
    key: str = Field(..., description="32 byte hex; hanya tampil sekali", pattern="^[0-9a-f]{64}$")
    previous_key_id: str | None
    previous_not_after: AwareDatetime | None
