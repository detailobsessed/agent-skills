let skills = ["git-spice" "macos-expert" "wise-mcp"]

for skill in $skills {
  print $"== ($skill) =="
  uv run agentskills validate $skill
}
