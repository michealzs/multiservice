"""LangChain tools exposed to the stock-intelligence agent."""
from __future__ import annotations

import json

from app.config import get_settings
from app.domain.scraper import StockScraper
from app.vectorstores import get_vector_store


def scrape_stock_raw(symbol: str) -> dict:
    return StockScraper(symbol.strip().upper()).scrape_stock_data()


def search_knowledge_raw(query: str, k: int = 4) -> list[dict]:
    store = get_vector_store(get_settings())
    return [
        {"text": d.text, "metadata": d.metadata, "score": d.score}
        for d in store.similarity_search(query, k=k)
    ]


def build_tools() -> list:
    """Return StructuredTools. Imported lazily so the package works without
    langchain installed (the agent then uses its non-LLM fallback)."""
    from langchain_core.tools import tool

    @tool
    def scrape_stock(symbol: str) -> str:
        """Fetch live fundamentals and recent OHLCV for a ticker symbol (e.g. TSLA)."""
        return json.dumps(scrape_stock_raw(symbol))

    @tool
    def search_stock_knowledge(query: str) -> str:
        """Search previously ingested stock knowledge for context relevant to the query."""
        return json.dumps(search_knowledge_raw(query))

    return [scrape_stock, search_stock_knowledge]
