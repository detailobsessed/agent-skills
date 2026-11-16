# Scheduled backups

snapcap has no scheduler of its own: you run `snapcap backup` from cron or a systemd timer, and it reads its settings from `snapcap.toml`.

## Write the config file

Create `snapcap.toml` next to the directory you back up. These are all the settings snapcap understands:

| Key | Type | Default | Meaning |
| --- | --- | --- | --- |
| `repository` | path | none | repository to back up into |
| `exclude` | list of globs | `[]` | files to skip |
| `compression` | `zstd`, `none` | `zstd` | chunk compression |
| `compression_level` | integer 1 to 19 | `3` | zstd level; higher is smaller and slower |
| `retention.keep_last` | integer | `7` | snapshots kept by `prune` |
| `lock_timeout` | seconds | `60` | how long to wait for another snapcap run to release the repository |
| `verify_after_backup` | boolean | `false` | re-hash new chunks after writing them |
| `notify_command` | string | none | shell command run after each backup, with the exit status in `SNAPCAP_STATUS` |

A minimal file for a nightly job:

```toml
repository = "/mnt/backups/repo"
exclude = ["*.tmp", "node_modules"]
```

## Why incremental snapshots are cheap

Every snapshot after the first only writes chunks the repository has not seen. A nightly job on a mostly unchanged directory therefore writes very little, and the run time is dominated by reading and hashing files, not by writing. This is also why `verify_after_backup` is cheap to turn on: it only re-hashes the new chunks.

## Add the cron entry

Run `crontab -e` and add a line that runs the backup at 02:30 every night:

```text
30 2 * * * cd /home/me/projects && snapcap backup . >> /var/log/snapcap.log 2>&1
```

If two runs overlap, the second waits for `lock_timeout` seconds and then exits with status 75.

## Prune old snapshots

Add a weekly prune after the backup:

```text
0 4 * * 0 cd /home/me/projects && snapcap prune --keep-last 7
```
