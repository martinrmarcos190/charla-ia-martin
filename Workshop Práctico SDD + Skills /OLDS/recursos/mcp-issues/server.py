import logging
import sys

import httpx
from mcp.server.fastmcp import FastMCP

# IMPORTANTE (stdio): nunca escribir a stdout, corrompe el JSON-RPC.
logging.basicConfig(level=logging.INFO, stream=sys.stderr)

mcp = FastMCP("issues-api")
API_BASE = "http://127.0.0.1:5000"


@mcp.tool()
async def list_issues() -> str:
    """Lista todos los issues de infraestructura registrados."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_BASE}/issues", timeout=30.0)
        r.raise_for_status()
        return str(r.json())


@mcp.tool()
async def get_issue(issue_id: int) -> str:
    """Devuelve un issue por id."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_BASE}/issues/{issue_id}", timeout=30.0)
        if r.status_code == 404:
            return f"No existe el issue {issue_id}."
        r.raise_for_status()
        return str(r.json())


@mcp.tool()
async def add_issue(
    title: str,
    service: str,
    severity: str,
    description: str = "",
    proposed_solution: str = "",
) -> str:
    """Crea un issue nuevo. severity: low/medium/high/critical."""
    payload = {
        "title": title,
        "service": service,
        "severity": severity,
        "description": description,
        "proposed_solution": proposed_solution,
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{API_BASE}/issues", json=payload, timeout=30.0)
        if r.status_code == 400:
            return f"La API rechazó el alta: {r.json().get('error')}"
        r.raise_for_status()
        return str(r.json())


@mcp.tool()
async def update_issue(
    issue_id: int,
    status: str | None = None,
    severity: str | None = None,
    description: str | None = None,
    proposed_solution: str | None = None,
) -> str:
    """Actualiza un issue: solo los campos provistos.
    status: open/investigating/resolved. severity: low/medium/high/critical."""
    payload = {
        k: v
        for k, v in {
            "status": status,
            "severity": severity,
            "description": description,
            "proposed_solution": proposed_solution,
        }.items()
        if v is not None
    }
    async with httpx.AsyncClient() as client:
        r = await client.put(f"{API_BASE}/issues/{issue_id}", json=payload, timeout=30.0)
        if r.status_code == 404:
            return f"No existe el issue {issue_id}."
        if r.status_code == 400:
            return f"La API rechazó la actualización: {r.json().get('error')}"
        r.raise_for_status()
        return str(r.json())


if __name__ == "__main__":
    mcp.run(transport="stdio")
