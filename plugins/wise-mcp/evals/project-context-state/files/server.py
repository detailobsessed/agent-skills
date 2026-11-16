from fastmcp import FastMCP

mcp = FastMCP("tickets")
DB: dict[str, list[dict]] = {"web": [], "mobile": []}


@mcp.tool
def list_tickets(project_id: str, status: str = "open") -> list[dict]:
    """List tickets."""
    return [t for t in DB.get(project_id, []) if t["status"] == status]


@mcp.tool
def create_ticket(project_id: str, title: str, body: str = "") -> dict:
    """Create a ticket."""
    ticket = {"id": len(DB[project_id]) + 1, "title": title, "body": body, "status": "open"}
    DB[project_id].append(ticket)
    return ticket


if __name__ == "__main__":
    mcp.run()
