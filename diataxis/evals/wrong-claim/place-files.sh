#!/usr/bin/env bash
# Copies the fixture project into a fresh git repo and commits it, so a run that edits, moves or
# deletes anything shows up in `git status`.
set -eu
cp -R "$(dirname "$0")/files/." .
git init -q
git add -A
git -c user.name=maintainer -c user.email=maintainer@example.com commit -qm "Add snapcap and its docs"
