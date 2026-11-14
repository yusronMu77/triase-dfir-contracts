# Changelog

## [Unreleased]

### Added

- OpenAPI `ingest-internal` 0.1.0 (baru): `POST /svc/v1/imports` (`adapter`, `path_ref`, `expected_sha256` opsional; 202 job baru, 200 berkas sudah diimpor) dan `GET /svc/v1/imports/{job_id}`, dengan daftar kode tolak. Menyelaraskan api dan ingest (api#12: api dulu memanggil `/svc/v1/ingest/jobs` yang tidak ada).

### Fixed

- `scripts/generate.py` di Windows menghasilkan CRLF sehingga cek CI "Hasil generasi sama dengan sumber kontrak" selalu gagal di CI lokal; ruff format kini dipaksa `line-ending = "lf"`.

## [0.5.0] - 2026-11-12

### Added

- OpenAPI `gateway-internal` 0.1.0 (baru): `POST /events` (termasuk `identity.revoked` sebagai kontrol dengan `channel_id` `*`), `PUT /secrets/{key}`, `POST /whatsapp/masuk`, `GET /status`; autentikasi HMAC per permintaan.
- `audit-internal` 0.3.0: parameter `recipient` (age, berulang) pada `GET /export`, respons `application/age`, dan galat 400 `EKSPOR_WAJIB_TERENKRIPSI` dan `PENERIMA_TIDAK_DIIZINKAN`. Aditif; ekspor polos tetap sah.

### Changed

- `config-internal` 0.2.0: `PUT /v1/secrets/gateway/{key}` mencantumkan 404 `GW_KUNCI_TIDAK_DIKENAL`, 409 `GW_DIKUNCI_ENV`, dan 422 `GW_EVENT_INVALID` yang diteruskan dari gateway.

## [0.4.0] - 2026-11-12

### Added

- Event `identity.revoked` v1 (subjek `astria.identity.revoked`, penerbit identity, konsumen notifier dan api): `user_id`, `reason` (`akun_nonaktif`, `peran_berubah`, `kata_sandi_diganti`, `sesi_dicabut`), `revoked_at`, dan `roles_after` opsional. Tanpa username, token, atau teks bebas.
- Event `config.changed` v1 (subjek `astria.config.changed`, penerbit config, konsumen api, triage, narrative, ticket, notifier, scheduler, ingest): `scope` (`setting`, `secret`, `catalog`, `channel_policy`) dengan `key`, `kind`, `value_version`, `catalog_version`, `content_hash` opsional. Tidak pernah memuat nilai pengaturan atau rahasia.
- OpenAPI `identity-internal` 0.2.0: login, logout, reauth, introspeksi sesi, pengguna (daftar, buat, ubah, peran, cabut sesi), kode pairing (terbit, klaim), rotasi kunci layanan. `Actor` (klaim `act`) mendapat `reauth_at` opsional yang diisi identity dari sesi.
- OpenAPI `audit-internal` 0.2.0: tugas verifikasi (`POST` dengan `wait_ms`, `GET /verify-jobs/{id}`), ekspor JSONL, jangkar (`/anchor/latest`, `/anchors`), filter `actor`, `action`, `target_type`, `target_id` pada baca bertahap. `VerifyResult` mendapat `job_id`, `anchor_match`, `started_at`, `finished_at`; `status` menjadi `berjalan`, `selesai`, atau `gagal`.
- OpenAPI `config-internal` 0.1.0 (baru): pengaturan efektif dan ubah, rahasia tulis-saja, teruskan rahasia kanal ke gateway, kebijakan kanal, katalog berversi (draf, tinjau, aktivasi, cakupan), dan jalur konsumen `/svc/v1` (pengaturan efektif, katalog aktif, kebijakan kanal, kunci API model).
- Kebutuhan dari identity#4 (identity, audit, config: versi penuh) dan daftar event api.

### Changed

- `audit-internal` `VerifyResult`: `ok` dan `to_seq` boleh `null` (selama berjalan atau gagal); `required` menjadi `status`, `from_seq`, `checked`. Pemanggil Tahap 0 yang membaca `ok` pada respons 200 tidak terpengaruh.

## [0.3.0] - 2026-11-10

### Added

- Event `digest.published` v1 (subjek `astria.digest.published`, penerbit scheduler, konsumen notifier dan api): `jenis`, periode, `sha256` dokumen, `mode_narasi`, `terlambat`, dan `audit_head_hash` opsional. Isi digest tidak ikut event. Mengikuti rancangan scheduler bagian 3.2.
- Correlation amplop: kunci opsional `digest_id` (`DG-yyyymmdd-HHMM`) dan `case_id` (`CS-yyyymmdd-nnn`) untuk scheduler dan dfir. Aditif, versi amplop tetap.

## [0.2.0] - 2026-11-10

### Added

- `evidence.ingested` v1: field opsional `file_sha256` (SHA-256 berkas sumber) dan `batch_sha256` (SHA-256 gabungan `record_sha256` dalam `record_range`), keduanya hex huruf kecil 64 karakter. Versi event tetap 1 (aditif). Contoh mendapat kedua field (nilai sintetis) dan `batch_ref` ke `/svc/v1/jobs/{job_id}/alerts`; nilai lain tidak berubah. Kebutuhan dari ingest#2.
- Event `narration.retry_requested` v1 (subjek `astria.narration.retry_requested`, penerbit verifier, konsumen narrative): `attempt` selalu 2 dan `kegagalan` berisi `klaim_no` serta kode gagal saja, tanpa teks klaim atau kutipan log. Mengikuti rancangan narrative bagian 3.3 dan verifier bagian 5.7.
- `card.skeleton.created`: field opsional `kode.teknik_attack` (`id` teknik ATT&CK dan `taktik`) dan `kode.temuan_korelasi` (`K-...`), dipakai verifier untuk pemeriksaan 6 (verifier bagian 5.6). Opsional, jadi versi event tetap 1.

## [0.1.0] - 2026-11-08

### Added

- Amplop event (`events/envelope.schema.json`) dan skema `data` untuk `evidence.ingested`, `card.skeleton.created`, `narration.completed`, `card.verified`, dan `audit.record` (v1), masing-masing dengan contoh di `events/examples/`.
- `events/catalog.json`: jenis event, subjek NATS, penerbit, konsumen, stream `ASTRIA` (`astria.>`), jendela duplikat 120 detik.
- OpenAPI 3.1: `common.yaml` (health, ready, metrics, galat seragam), `identity-internal.yaml` (token layanan, JWKS), `audit-internal.yaml` (catat, baca, verifikasi).
- Paket `astria_contracts`: model Pydantic hasil datamodel-code-generator 0.90.0, katalog `EVENTS`, pembantu `example()` dan `schema_dir()`; skema ikut dalam wheel.
- `scripts/generate.py` dan uji kontrak (skema Draft 2020-12 valid, contoh lolos skema dan model).
- CI: lint, uji, generasi ulang tanpa selisih, gitleaks; action dipin SHA.
- Logo Astria di kepala README (`.github/assets/`, dari kit logo di repo `triase-dfir-uiux`).
