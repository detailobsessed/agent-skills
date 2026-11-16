# Usage

## Restoring

To restore a snapshot, find its ID with `snapcap snapshots`, then run:

```sh
snapcap restore 3f9a2c --target ~/restore
```

The target directory must exist and should be empty.

## Excluding files

Pass `--exclude` once per glob:

```sh
snapcap backup ~/projects --exclude "node_modules" --exclude "*.log"
```

## Pruning old snapshots

`snapcap prune --keep-last 7` keeps the seven newest snapshots and deletes the rest. Add `--dry-run` to see what would go.

## Commands

| Command | What it does |
| --- | --- |
| `init` | create a repository |
| `backup` | take a snapshot of a directory |
| `restore` | restore a snapshot |
| `prune` | delete old snapshots |
| `snapshots` | list snapshots |
