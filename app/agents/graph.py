"""LangGraph ReAct agent for stock questions.

When an LLM provider is configured we build a real LangGraph ``create_react_agent``
wired to the domain tools, with Langfuse/LangSmith callbacks. When no provider
key is present we return a deterministic fallback that still exercises the
tools (RAG search + live scrape) so ``/chat`` is useful and tests pass offline.
"""
from __future__ import annotations

import json

from app.config import Settings, get_settings
from app.observability import configure_langsmith, get_callbacks

SYSTEM_PROMPT = (
    "You are a stock-intelligence assistant. Use the scrape_stock tool for live "
    "data and search_stock_knowledge for previously ingested context. Be concise "
    "and cite figures you used."
)


class StockAgent:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._graph = None
        if self.settings.llm_configured:
            try:
                self._graph = self._build_graph()
            except Exception:  # pragma: no cover - missing optional deps
                self._graph = None

    def _build_graph(self):
        from langgraph.prebuilt import create_react_agent

        from app.agents.tools import build_tools

        configure_langsmith(self.settings)
        return create_react_agent(self._llm(), build_tools())

    def _llm(self):
        if self.settings.llm_provider == "anthropic":
            from langchain_anthropic import ChatAnthropic

            return ChatAnthropic(
                model=self.settings.chat_model,
                api_key=self.settings.anthropic_api_key,
            )
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=self.settings.chat_model, api_key=self.settings.openai_api_key
        )

    def run(self, message: str) -> dict:
        if self._graph is None:
            return self._fallback(message)
        result = self._graph.invoke(
            {"messages": [("system", SYSTEM_PROMPT), ("user", message)]},
            config={"callbacks": get_callbacks(self.settings)},
        )
        messages = result.get("messages", [])
        reply = messages[-1].content if messages else ""
        used = [
            m.name
            for m in messages
            if getattr(m, "type", "") == "tool" and getattr(m, "name", None)
        ]
        return {"reply": reply, "used_tools": sorted(set(used)), "sources": []}

    def _fallback(self, message: str) -> dict:
        """No LLM key: do a best-effort tool-only answer so the route still works."""
        from app.agents.tools import scrape_stock_raw, search_knowledge_raw

        used: list[str] = []
        sources: list[str] = []
        parts = [
            "LLM provider not configured — returning a tool-only summary. "
            "Set OPENAI_API_KEY (or ANTHROPIC_API_KEY) for full natural-language answers."
        ]

        hits = search_knowledge_raw(message, k=3)
        if hits:
            used.append("search_stock_knowledge")
            sources = [h["metadata"].get("symbol", "") for h in hits]
            parts.append("Relevant ingested context:\n" + "\n".join(h["text"][:200] for h in hits))

        # Heuristic: if a token looks like a ticker, scrape it live.
        for token in message.replace("?", " ").split():
            if token.isupper() and 1 < len(token) <= 5:
                data = scrape_stock_raw(token)
                used.append("scrape_stock")
                parts.append(f"Live data for {token}: {json.dumps(data)[:400]}")
                break

        return {"reply": "\n\n".join(parts), "used_tools": sorted(set(used)), "sources": sources}


_agent: StockAgent | None = None


def get_agent() -> StockAgent:
    global _agent
    if _agent is None:
        _agent = StockAgent()
    return _agent


def reset_agent() -> None:
    global _agent
    _agent = None
