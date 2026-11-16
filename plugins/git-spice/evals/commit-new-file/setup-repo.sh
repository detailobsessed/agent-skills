#!/usr/bin/env bash
# Builds a local repo tracked by git-spice: trunk main, branch feat-parser, an untracked parser.py and an edited README.md.
set -eu
git init -q -b main .
git config user.email eval@example.com
git config user.name eval
echo "# demo" > README.md
git add README.md
git commit -q -m "init"
git-spice repo init --trunk main --no-prompt >/dev/null 2>&1
git-spice branch create feat-parser --no-prompt --no-commit >/dev/null 2>&1
echo "def parse(): ..." > parser.py
echo "Parses the config." >> README.md
