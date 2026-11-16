# Getting started

Install snapcap with pip. You need Python 3.11 or newer.

```sh
pip install snapcap
```

You can also install it with pipx or uv if you prefer to keep it isolated, or build it from source.

## Create a repository

A repository is a directory where snapcap keeps chunks and snapshot records. It can be on a local disk or a network share.

```sh
snapcap init /mnt/backups/repo
```

Repositories are content-addressed: every chunk is named by its SHA-256 hash. This is why two snapshots of the same data take almost no extra space, and why snapcap can check a repository for damage by re-hashing chunks. Content addressing was popularised by tools like git, and it has a few trade-offs: chunk size matters for how much deduplication you get, and deleting data needs a separate prune step because chunks are shared between snapshots.

## Take your first snapshot

```sh
snapcap backup ~/projects --tag first
```

You can add `--exclude` to skip files, for example `--exclude "*.tmp"`. Use `snapcap snapshots` to list what you have.
