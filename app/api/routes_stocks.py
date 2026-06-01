"""Stock CRUD + live data endpoints (ported from the Django stocks views)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.domain.models import Stock
from app.domain.schemas import StockIn, StockOut
from app.domain.scraper import StockScraper

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("", response_model=list[StockOut])
async def list_stocks(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Stock).order_by(Stock.symbol))
    return list(result.scalars())


@router.post("", response_model=StockOut, status_code=201)
async def create_stock(payload: StockIn, session: AsyncSession = Depends(get_session)):
    symbol = payload.symbol.strip().upper()
    exists = await session.scalar(select(Stock).where(Stock.symbol == symbol))
    if exists:
        raise HTTPException(status_code=409, detail="symbol already exists")
    stock = Stock(symbol=symbol, name=payload.name or symbol)
    session.add(stock)
    await session.commit()
    await session.refresh(stock)
    return stock


@router.get("/{symbol}/data")
async def stock_data(symbol: str):
    """Live scrape of Yahoo Finance fundamentals + recent OHLCV."""
    data = StockScraper(symbol.strip().upper()).scrape_stock_data()
    if len(data) <= 1:
        raise HTTPException(status_code=502, detail="could not scrape any data")
    return data
