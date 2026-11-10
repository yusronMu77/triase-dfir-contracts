# Dibangkitkan oleh scripts/generate.py dari kontrak. JANGAN DIEDIT.
"""Katalog event: jenis -> versi, subjek NATS, dan model data."""

from dataclasses import dataclass

from pydantic import BaseModel

from astria_contracts.events.audit_record import AuditRecord
from astria_contracts.events.card_skeleton_created import CardSkeletonCreated
from astria_contracts.events.card_verified import CardVerified
from astria_contracts.events.digest_published import DigestPublished
from astria_contracts.events.evidence_ingested import EvidenceIngested
from astria_contracts.events.narration_completed import NarrationCompleted
from astria_contracts.events.narration_retry_requested import NarrationRetryRequested


@dataclass(frozen=True)
class EventSpec:
    type: str
    version: int
    subject: str
    model: type[BaseModel]


STREAM_NAME = "ASTRIA"
STREAM_SUBJECTS = ["astria.>"]
DUPLICATE_WINDOW_SECONDS = 120

EVENTS: dict[str, EventSpec] = {
    "evidence.ingested": EventSpec("evidence.ingested", 1, "astria.evidence.ingested", EvidenceIngested),
    "card.skeleton.created": EventSpec("card.skeleton.created", 1, "astria.card.skeleton.created", CardSkeletonCreated),
    "narration.completed": EventSpec("narration.completed", 1, "astria.narration.completed", NarrationCompleted),
    "narration.retry_requested": EventSpec(
        "narration.retry_requested", 1, "astria.narration.retry_requested", NarrationRetryRequested
    ),
    "card.verified": EventSpec("card.verified", 1, "astria.card.verified", CardVerified),
    "digest.published": EventSpec("digest.published", 1, "astria.digest.published", DigestPublished),
    "audit.record": EventSpec("audit.record", 1, "astria.audit.record", AuditRecord),
}
