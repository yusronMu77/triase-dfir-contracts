<!-- astria-logo -->
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/astria-logo-reverse.svg">
    <img src=".github/assets/astria-logo.svg" alt="Astria" width="320">
  </picture>
</p>

# Astria contracts

Kontrak: snapshot OpenAPI, JSON Schema event, kartu v2, katalog event.

> Status: kerangka awal, belum ada kode. Repo ini adalah submodule dari workspace `triase-dfir` (folder `contracts/`). Rancangan: `notes/2026-11-06-triase-dfir-app-common-dan-infra.md` di repo root. Lajur developer: 3.

## Tech stack

JSON Schema, OpenAPI, datamodel-code-generator, openapi-typescript

## Isi

```text
openapi/        snapshot OpenAPI per layanan
events/         <type>.v1.schema.json, examples/, catalog.json
card/           card-v2.schema.json
```

Tambah field = tetap `v1` dan CHANGELOG bagian Added; hapus atau ubah arti field = event `v2` berdampingan dengan `v1`.

## Alur git

Branch `{type}/{yyyyMMdd}-{taskId}-{nama}`; commit `{type}({yyyyMMddHHmm}): [{taskId}] {pesan}`, satu baris, tanpa trailer. `main` hanya berubah lewat pull request (merge rebase); jangan push langsung ke `main` dan jangan `--no-verify`.
