# Configuration

snapcap reads `snapcap.toml` from the current directory, or the file passed with `--config`.

| Key | Type | Default | Meaning |
| --- | --- | --- | --- |
| `repository` | path | none | repository to back up into |
| `exclude` | list of globs | `[]` | files to skip |
| `compression` | `zstd`, `none` | `zstd` | chunk compression |
| `retention.keep_last` | integer | `7` | snapshots kept by `prune` |
