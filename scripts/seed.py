"""Seed a few well-known tickers into the database.

Usage: python -m scripts.seed
"""
from __future__ import annotations

import asyncio

from sqlalchemy import select

from app.db import SessionLocal, init_models
from app.domain.models import Stock

SYMBOLS = [("TSLA", "Tesla Inc"), ("AAPL", "Apple Inc"), ("MSFT", "Microsoft Corp")]


async def main() -> None:
    await init_models()
    async with SessionLocal() as session:
        for symbol, name in SYMBOLS:
            exists = await session.scalar(select(Stock).where(Stock.symbol == symbol))
            if not exists:
                session.add(Stock(symbol=symbol, name=name))
        await session.commit()
    print(f"Seeded {len(SYMBOLS)} stocks.")


if __name__ == "__main__":
    asyncio.run(main())
