import shutil
from pathlib import Path

from fastmcp import FastMCP

mcp = FastMCP("repos")
ROOT = Path("/srv/repos")


@mcp.tool
def list_repos() -> list[str]:
    """List repositories."""
    return sorted(p.name for p in ROOT.iterdir() if p.is_dir())


@mcp.tool
def delete_repo(name: str) -> str:
    """Delete a repository."""
    shutil.rmtree(ROOT / name)
    return f"deleted {name}"


if __name__ == "__main__":
    mcp.run()
