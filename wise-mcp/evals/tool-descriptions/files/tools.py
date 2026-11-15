from fastmcp import FastMCP

mcp = FastMCP("support")


@mcp.tool
def search(q: str, type: str = "all", n: int = 20) -> list[dict]:
    """Search."""
    # type is one of: ticket, article, customer, all. n is capped at 50 by the backend.
    ...


@mcp.tool
def get(id: str) -> dict:
    """Get an item."""
    # id is a ticket id like "T-1234"; customers and articles are not supported here.
    ...


@mcp.tool
def update(id: str, status: str, note: str = "") -> dict:
    """Update."""
    # status: open, pending, solved, closed. closed tickets cannot be reopened.
    ...


@mcp.tool
def assign(id: str, user: str) -> dict:
    """Assign ticket."""
    # user is an agent email; the backend wants the numeric agent id.
    ...


@mcp.tool
def export(start: str, end: str) -> str:
    """Export tickets as CSV."""
    # start/end are ISO dates; range is limited to 31 days; returns a download URL.
    ...


@mcp.tool
def stats(period: str) -> dict:
    """Stats."""
    # period: day, week, month. returns counts per status.
    ...
