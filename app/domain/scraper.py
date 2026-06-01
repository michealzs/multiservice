"""Yahoo Finance stock scraper.

Ported from the original Django project's ``stocksapp/stocks.py``. The scraping
logic and the set of fundamentals it targets are preserved; it has been wrapped
with defensive error handling and a structured return type. Yahoo's markup
changes frequently, so selectors are best-effort and the method degrades to
whatever fields it could extract rather than raising.
"""
from __future__ import annotations

import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# Fundamentals targeted on the key-statistics page (preserved from the original).
TARGET_STATS = [
    "Beta (5Y Monthly)", "52-Week Change", "S&P500 52-Week Change",
    "52 Week High", "52 Week Low", "50-Day Moving Average",
    "200-Day Moving Average", "Avg Vol (3 month)", "Shares Outstanding",
    "Most Recent Quarter", "Profit Margin", "Operating Margin",
    "Return on Assets", "Return on Equity", "Revenue",
    "Revenue Per Share", "Gross Profit", "Total Cash",
    "Total Debt", "Book Value Per Share", "Operating Cash Flow",
]


class StockScraper:
    def __init__(self, stock: str) -> None:
        self.stock = stock
        self.hurl = f"https://finance.yahoo.com/quote/{stock}/history?p={stock}"
        self.url = f"https://finance.yahoo.com/quote/{stock}/key-statistics?p={stock}"
        self.headers = {
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 "
                "Edg/101.0.1210.47"
            )
        }
        self.temp: dict[str, str] = {}

    def scrape_stock_data(self, timeout: int = 15) -> dict[str, str]:
        """Scrape fundamentals + recent OHLCV. Returns a (possibly partial) dict."""
        self.temp = {"symbol": self.stock}
        try:
            self._scrape_statistics(timeout)
        except Exception as exc:  # best-effort: keep whatever we have
            logger.warning("Statistics scrape failed for %s: %s", self.stock, exc)
        try:
            self._scrape_history(timeout)
        except Exception as exc:
            logger.warning("History scrape failed for %s: %s", self.stock, exc)
        return self.temp

    def _scrape_statistics(self, timeout: int) -> None:
        page = requests.get(self.url, headers=self.headers, timeout=timeout)
        soup = BeautifulSoup(page.text, "html.parser")
        cells = soup.find_all("td")

        # Walk label/value cell pairs and capture targeted fundamentals.
        for i, cell in enumerate(cells[:-1]):
            label = cell.get_text(strip=True)
            if label in TARGET_STATS and label not in self.temp:
                self.temp[label] = cells[i + 1].get_text(strip=True)

        notice = soup.find("div", id="quote-market-notice")
        if notice and notice.string:
            self.temp["market time"] = notice.string

        streamers = soup.find_all("fin-streamer")
        if len(streamers) >= 5:
            self.temp["price"] = streamers[-5].get_text()
            self.temp["market_change"] = streamers[-4].get_text()
            self.temp["market_change_percent"] = streamers[-3].get_text()

        header = soup.find("div", id="quote-header-info")
        if header:
            for h in header.strings:
                self.temp["name"] = h
                break

    def _scrape_history(self, timeout: int) -> None:
        page = requests.get(self.hurl, headers=self.headers, timeout=timeout)
        soup = BeautifulSoup(page.text, "html.parser")
        td = soup.find_all("td")
        if len(td) >= 7:
            self.temp.update(
                day_date=td[0].get_text(), day_open=td[1].get_text(),
                day_high=td[2].get_text(), day_low=td[3].get_text(),
                day_close=td[4].get_text(), day_volume=td[6].get_text(),
            )
        if len(td) >= 14:
            self.temp.update(
                previous_date=td[7].get_text(), previous_open=td[8].get_text(),
                previous_high=td[9].get_text(), previous_low=td[10].get_text(),
                previous_close=td[11].get_text(), previous_volume=td[13].get_text(),
            )
