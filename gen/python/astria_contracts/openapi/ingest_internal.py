# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.

from __future__ import annotations

from typing import Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, RootModel


class ImportRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    adapter: Literal["hayabusa"]
    path_ref: str = Field(
        ...,
        description="Path relatif terhadap folder impor server, mis. `chains/svc-backup.jsonl`",
        max_length=1024,
        min_length=1,
    )
    expected_sha256: str | None = Field(
        None,
        description="Opsional. Bila berbeda dari SHA-256 isi berkas, impor ditolak 422 `SHA256_TIDAK_COCOK` tanpa job.",
        pattern="^[0-9a-f]{64}$",
    )


class JobStatus(RootModel[Literal["queued", "running", "completed", "completed_with_errors", "failed"]]):
    root: Literal["queued", "running", "completed", "completed_with_errors", "failed"]


class ErrorSample(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    record_no: int = Field(..., ge=1)
    code: str


class JobStats(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    total_lines: int | None = Field(None, ge=0)
    valid: int | None = Field(None, ge=0)
    blank: int | None = Field(None, ge=0)
    rejected: int | None = Field(None, ge=0)
    error_samples: list[ErrorSample] | None = Field(None, max_length=20)


class ImportResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    job_id: str = Field(..., pattern="^ING-[0-9]{8}-[0-9A-F]{8}$")
    source_id: str
    file_sha256: str = Field(..., pattern="^[0-9a-f]{64}$")
    status: JobStatus
    created: bool
    stats: JobStats


class JobResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    job_id: str = Field(..., pattern="^ING-[0-9]{8}-[0-9A-F]{8}$")
    source_id: str
    file_sha256: str = Field(..., pattern="^[0-9a-f]{64}$")
    status: JobStatus
    stats: JobStats
    last_record_no: int = Field(..., ge=0)
    error_code: str | None
    created_at: AwareDatetime | None
    started_at: AwareDatetime | None
    finished_at: AwareDatetime | None
