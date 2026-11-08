# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, RootModel


class CheckStatus(RootModel[Literal["ok", "degraded", "down"]]):
    root: Literal["ok", "degraded", "down"]


class Check(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    status: CheckStatus
    detail: str | None = Field(None, max_length=500)


class Health(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    status: CheckStatus
    service: str
    version: str
    env: Literal["dev", "demo", "prod", "test"]
    checks: dict[str, Check]


class ErrorBody(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    code: str = Field(..., pattern="^[A-Z][A-Z0-9_]*$")
    message: str = Field(..., max_length=500)
    trace_id: str | None = None


class Error(BaseModel):
    """
    Bentuk galat seragam semua layanan.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    error: ErrorBody
