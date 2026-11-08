# Changelog

## [Unreleased]

## [0.1.0] - 2026-11-08

### Added

- Amplop event (`events/envelope.schema.json`) dan skema `data` untuk `evidence.ingested`, `card.skeleton.created`, `narration.completed`, `card.verified`, dan `audit.record` (v1), masing-masing dengan contoh di `events/examples/`.
- `events/catalog.json`: jenis event, subjek NATS, penerbit, konsumen, stream `ASTRIA` (`astria.>`), jendela duplikat 120 detik.
- OpenAPI 3.1: `common.yaml` (health, ready, metrics, galat seragam), `identity-internal.yaml` (token layanan, JWKS), `audit-internal.yaml` (catat, baca, verifikasi).
- Paket `astria_contracts`: model Pydantic hasil datamodel-code-generator 0.90.0, katalog `EVENTS`, pembantu `example()` dan `schema_dir()`; skema ikut dalam wheel.
- `scripts/generate.py` dan uji kontrak (skema Draft 2020-12 valid, contoh lolos skema dan model).
- CI: lint, uji, generasi ulang tanpa selisih, gitleaks; action dipin SHA.
- Logo Astria di kepala README (`.github/assets/`, dari kit logo di repo `triase-dfir-uiux`).
