<!-- astria-logo -->
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/astria-logo-reverse.svg">
    <img src=".github/assets/astria-logo.svg" alt="Astria" width="320">
  </picture>
</p>

# Astria contracts

Kontrak antarlayanan Astria: JSON Schema event, OpenAPI internal, dan model Pydantic hasil generasi (`astria_contracts`).

> Status: Tahap 1, v0.3.0. Repo ini adalah submodule dari workspace `triase-dfir` (folder `contracts/`). Rancangan: `notes/2026-11-06-triase-dfir-app-common-dan-infra.md` bagian 3 di repo root. Lajur developer: 3; setiap perubahan butuh dua peninjau (pemilik dan konsumen).

## Isi

```text
events/envelope.schema.json        amplop semua event {id, type, version, occurred_at, trace_id, correlation, data}
events/<type>.schema.json          skema `data` per jenis event
events/examples/<type>.json        satu amplop valid per jenis (wajib; dipakai uji kontrak konsumen)
events/catalog.json                jenis -> versi, subjek NATS, penerbit, konsumen; nama stream dan jendela duplikat
openapi/common.yaml                /health, /ready, /metrics, bentuk galat seragam
openapi/identity-internal.yaml     token layanan EdDSA (HMAC) dan kunci publik (Tahap 0)
openapi/audit-internal.yaml        catat sinkron, baca bertahap, verifikasi rantai (Tahap 0)
gen/python/astria_contracts/       model hasil datamodel-code-generator 0.90.0 (di-commit, JANGAN diedit)
card/                              kartu v2 (Tahap 1)
```

| Event | Versi | Subjek | Penerbit | Konsumen |
|---|---|---|---|---|
| `evidence.ingested` | 1 | `astria.evidence.ingested` | ingest | triage |
| `card.skeleton.created` | 1 | `astria.card.skeleton.created` | triage | narrative |
| `narration.completed` | 1 | `astria.narration.completed` | narrative | verifier |
| `narration.retry_requested` | 1 | `astria.narration.retry_requested` | verifier | narrative |
| `card.verified` | 1 | `astria.card.verified` | verifier | ticket |
| `digest.published` | 1 | `astria.digest.published` | scheduler | notifier, api |
| `audit.record` | 1 | `astria.audit.record` | semua | audit |

## Aturan perubahan

- Tambah field opsional: versi tetap, catat di CHANGELOG bagian Added.
- Hapus field atau ubah arti field: jenis event baru (atau versi baru berdampingan), bukan mengubah yang lama.
- Setiap skema punya contoh di `events/examples/`; contoh wajib lolos skema dan model hasil generasi.
- Setelah mengubah skema: `uv run python scripts/generate.py`, lalu commit hasilnya. CI membangkitkan ulang dan gagal bila ada selisih.
- Rilis = tag git `vX.Y.Z` di `main`. Konsumen menaikkan tag di `[tool.uv.sources]`, lalu `uv lock`.

## Perintah

```text
uv sync
uv run python scripts/generate.py   # bangkitkan ulang gen/python
uv run pytest                       # skema valid, contoh lolos skema dan model
```

Dari kontainer dev: `pwsh ../devenv/scripts/dev.ps1 py uv run pytest` di folder ini.

## Pemakaian di layanan

```python
from astria_contracts import EVENTS, Envelope, example
from astria_contracts.events.evidence_ingested import EvidenceIngested

spec = EVENTS["evidence.ingested"]  # versi, subjek NATS, model data
EvidenceIngested.model_validate(example("evidence.ingested")["data"])
```

## Alur git

Branch `{type}/{yyyyMMdd}-{taskId}-{nama}`; commit `{type}({yyyyMMddHHmm}): [{taskId}] {pesan}`, satu baris, tanpa trailer. `main` hanya berubah lewat pull request (merge rebase); jangan push langsung ke `main` dan jangan `--no-verify`.
