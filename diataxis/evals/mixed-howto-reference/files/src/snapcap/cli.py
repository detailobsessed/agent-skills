"""snapcap: snapshot backups of a directory into a content-addressed repository."""

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="snapcap")
    parser.add_argument("--config", default="snapcap.toml", help="path to the config file")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="create a repository")
    init.add_argument("repository")

    backup = sub.add_parser("backup", help="take a snapshot of a directory")
    backup.add_argument("path")
    backup.add_argument("--exclude", action="append", default=[], help="glob to skip; repeatable")
    backup.add_argument("--tag", help="label for the snapshot")

    restore = sub.add_parser("restore", help="restore a snapshot")
    restore.add_argument("snapshot")
    restore.add_argument("--target", required=True, help="directory to restore into")

    prune = sub.add_parser("prune", help="delete old snapshots")
    prune.add_argument("--keep-last", type=int, default=7, help="snapshots to keep")
    prune.add_argument("--dry-run", action="store_true")

    sub.add_parser("snapshots", help="list snapshots")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    print(f"snapcap {args.command}")
