import os

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "remote_tools",
    port=int(os.environ.get("PORT", 8001)),
    host=os.environ.get("HOST", "0.0.0.0"),
)

FASTAPI_BASE_URL = os.environ.get("FASTAPI_BASE_URL", "http://localhost:8000")


@mcp.tool()
async def get_all_tasks() -> list:
    """Retrieve all available tasks from the task manager API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{FASTAPI_BASE_URL}/tasks")
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_task(title: str, status: str = "not_started") -> dict:
    """Create a new task via the task manager API.

    Args:
        title: The title of the task.
        status: The initial status of the task. Must be one of: not_started, in_progress, completed.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FASTAPI_BASE_URL}/tasks",
            json={"title": title, "status": status},
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run(transport="sse")
