"""Uji kontrak: setiap skema valid, setiap contoh lolos skema dan model hasil generasi."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

from astria_contracts import EVENTS, Envelope, example, schema_dir

ROOT = Path(__file__).resolve().parent.parent
CATALOG = json.loads((ROOT / "events" / "catalog.json").read_text(encoding="utf-8"))
ENVELOPE_SCHEMA = json.loads((ROOT / "events" / "envelope.schema.json").read_text(encoding="utf-8"))


def _load(rel: str) -> dict:
    return json.loads((ROOT / "events" / rel).read_text(encoding="utf-8"))


@pytest.mark.parametrize("path", sorted((ROOT / "events").glob("*.schema.json")), ids=lambda p: p.name)
def test_schema_is_valid_draft_2020_12(path: Path) -> None:
    Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))


@pytest.mark.parametrize("entry", CATALOG["events"], ids=lambda e: e["type"])
def test_example_matches_schema_and_model(entry: dict) -> None:
    envelope = _load(entry["example"])
    Draft202012Validator(ENVELOPE_SCHEMA).validate(envelope)
    Draft202012Validator(_load(entry["schema"])).validate(envelope["data"])

    assert envelope["type"] == entry["type"]
    assert envelope["version"] == entry["version"]
    assert entry["subject"] == f"astria.{entry['type']}"

    parsed = Envelope.model_validate(envelope)
    spec = EVENTS[entry["type"]]
    spec.model.model_validate(parsed.data)


def test_registry_covers_catalog() -> None:
    assert set(EVENTS) == {e["type"] for e in CATALOG["events"]}


def test_example_helper_reads_schema_dir() -> None:
    assert (schema_dir() / "events" / "catalog.json").is_file()
    assert example("evidence.ingested")["type"] == "evidence.ingested"


def test_envelope_rejects_unknown_field() -> None:
    bad = example("evidence.ingested") | {"extra": 1}
    with pytest.raises(Exception, match="extra"):
        Envelope.model_validate(bad)


def test_data_rejects_claim_without_evidence() -> None:
    env = example("narration.completed")
    env["data"]["narasi"]["ringkasan"][0]["bukti"] = []
    with pytest.raises(Exception, match="bukti"):
        EVENTS["narration.completed"].model.model_validate(env["data"])


@pytest.mark.parametrize("path", sorted((ROOT / "openapi").glob("*.yaml")), ids=lambda p: p.name)
def test_openapi_is_3_1(path: Path) -> None:
    spec = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert spec["openapi"].startswith("3.1")
    assert spec["paths"]
