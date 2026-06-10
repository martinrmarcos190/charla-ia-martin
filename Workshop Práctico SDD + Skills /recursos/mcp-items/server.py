import logging
import sys

import httpx
from mcp.server.fastmcp import FastMCP

# IMPORTANTE (stdio): nunca escribir a stdout, corrompe el JSON-RPC.
logging.basicConfig(level=logging.INFO, stream=sys.stderr)

mcp = FastMCP("items-api")
API_BASE = "http://127.0.0.1:5000"


@mcp.tool()
async def list_models() -> str:
    """Lista todos los modelos del inventario local."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_BASE}/models", timeout=30.0)
        r.raise_for_status()
        return str(r.json())


@mcp.tool()
async def get_model(model_id: int) -> str:
    """Devuelve un modelo por id."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_BASE}/models/{model_id}", timeout=30.0)
        if r.status_code == 404:
            return f"No existe el modelo {model_id}."
        r.raise_for_status()
        return str(r.json())


@mcp.tool()
async def add_model(name: str, framework: str, accuracy: float) -> str:
    """Crea un modelo nuevo en el inventario."""
    payload = {"name": name, "framework": framework, "accuracy": accuracy}
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{API_BASE}/models", json=payload, timeout=30.0)
        r.raise_for_status()
        return str(r.json())


if __name__ == "__main__":
    mcp.run(transport="stdio")
