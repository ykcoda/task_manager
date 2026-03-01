from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from langchain.messages import HumanMessage
from agent import get_agent


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loaded agent....")
    await get_agent()
    yield


app = FastAPI(title="AI API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(SQLModel):
    message: str


@app.post("/chat")
async def chat(req: ChatRequest):
    agent = await get_agent()
    response = await agent.ainvoke({"messages": [HumanMessage(req.message)]})

    return response["messages"][-1].content


@app.get("/scalar")
async def scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url)
