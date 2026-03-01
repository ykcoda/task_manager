import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.messages import HumanMessage
from scalar_fastapi import get_scalar_api_reference
from sqlmodel import SQLModel

from .agent import get_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading agent...")
    await get_agent()
    logger.info("Agent loaded successfully.")
    yield


app = FastAPI(title="AI API", version="0.1.0", lifespan=lifespan)

origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8501").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)


class ChatRequest(SQLModel):
    message: str


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/chat")
async def chat(req: ChatRequest):
    logger.info("Received chat request.")
    agent = await get_agent()
    response = await agent.ainvoke({"messages": [HumanMessage(req.message)]})
    return response["messages"][-1].content


@app.get("/scalar")
async def scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url)
