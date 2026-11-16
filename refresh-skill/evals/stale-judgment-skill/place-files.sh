#!/usr/bin/env bash
# Unpacks the wise-mcp skill as it stood before its progressive-disclosure refresh (this repo's
# 05f6dc3^) into a fresh git repo, committed on the date it was last touched. Packed as a tarball
# so that neither the skills CLI nor the validators take the stale copy for a published skill.
set -eu
tar -xzf "$(dirname "$0")/files/skill.tar.gz"
git init -q
git add -A
GIT_AUTHOR_DATE="2026-08-05T22:51:05+02:00" GIT_COMMITTER_DATE="2026-08-05T22:51:05+02:00" \
  git -c user.name=maintainer -c user.email=maintainer@example.com commit -qm "Add the wise-mcp skill"
