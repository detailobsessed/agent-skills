# Command-line reference

snapcap requires Python 3.9 or newer.

All commands accept `--config PATH` to read a config file other than `snapcap.toml`.

## `snapcap init REPOSITORY`

Creates an empty repository at `REPOSITORY`.

## `snapcap backup PATH`

Takes a snapshot of `PATH`.

- `--exclude GLOB`: skip files matching `GLOB`. Repeatable.
- `--tag TAG`: label the snapshot.

## `snapcap restore SNAPSHOT --target DIR`

Restores `SNAPSHOT` into `DIR`.

If your laptop's disk died, here is how to get your projects back: mount the backup share, run `snapcap snapshots` to find the newest snapshot of your home directory, create an empty directory, and restore into it with `snapcap restore <id> --target ~/recovered`. Then copy what you need back into place and check a few files open before you delete the old disk image.

## `snapcap prune`

Deletes old snapshots.

- `--keep-days N`: delete snapshots older than `N` days. Default: 30.
- `--dry-run`: print what would be deleted, delete nothing.

## `snapcap snapshots`

Lists the snapshots in the repository, newest first.
