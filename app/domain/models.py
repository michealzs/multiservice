"""SQLAlchemy models. Ported from the Django ``stocksapp.models.Stock``."""
from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Stock(Base):
    __tablename__ = "stocks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), default="")
    symbol: Mapped[str] = mapped_column(String(10), unique=True, index=True)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Stock {self.symbol}>"
