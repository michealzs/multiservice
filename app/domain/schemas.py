"""Pydantic request/response schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class StockIn(BaseModel):
    symbol: str = Field(..., examples=["TSLA"])
    name: str = ""


class StockOut(BaseModel):
    id: int
    symbol: str
    name: str

    model_config = {"from_attributes": True}


class ChatRequest(BaseModel):
    message: str = Field(..., examples=["How is TSLA doing today?"])
    session_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    used_tools: list[str] = []
    sources: list[str] = []


class IngestResponse(BaseModel):
    symbol: str
    chunks_indexed: int
