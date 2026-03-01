import os

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("remote_tools", port=int(os.environ.get("PORT", 8001)), host=os.environ.get("HOST", "0.0.0.0"))


@mcp.tool()
def add(x: int, y: int) -> int:
    """Add two numbers"""
    return x + y


if __name__ == "__main__":
    mcp.run(transport="sse")
