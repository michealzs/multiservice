"""Ingest stock fundamentals into the vector store for RAG."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.domain.schemas import IngestResponse
from app.domain.scraper import StockScraper
from app.vectorstores import get_vector_store

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/{symbol}", response_model=IngestResponse)
async def ingest_symbol(symbol: str):
    symbol = symbol.strip().upper()
    data = StockScraper(symbol).scrape_stock_data()
    if len(data) <= 1:
        raise HTTPException(status_code=502, detail="could not scrape any data")

    # One text chunk per fundamental keeps retrieval granular.
    texts = [f"{symbol} {key}: {value}" for key, value in data.items()]
    metadatas = [{"symbol": symbol, "field": key} for key in data]
    store = get_vector_store()
    store.add_texts(texts=texts, metadatas=metadatas)
    return IngestResponse(symbol=symbol, chunks_indexed=len(texts))
