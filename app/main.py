from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from fastmcp import FastMCP

api = FastAPI()
mcp = FastMCP.from_fastapi(api)
mcp_app = mcp.http_app(path="/mcp")


@api.get("/health")
async def health():
    return {"status": "ok"}


@api.get("/scalar", include_in_schema=False)
async def scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url)


app = FastAPI(
    title="Task App",
    routes=[
        *api.routes,
        *mcp_app.routes,
    ],
    lifespan=mcp_app.lifespan,
)
