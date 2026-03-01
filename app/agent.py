import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

_agent = None


async def get_agent():
    global _agent

    if _agent is not None:
        return _agent

    client = MultiServerMCPClient(
        {
            "remote_tool": {
                "transport": "sse",
                "url": os.getenv("MCP_SERVER_URL"),
            }
        }
    )

    tools = await client.get_tools()

    _agent = create_agent(
        model="gpt-5-mini",
        tools=tools,
        system_prompt="You a helpful assistant who uses its tools to respond to users query",
    )

    return _agent
