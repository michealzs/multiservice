import pytest


@pytest.mark.asyncio
async def test_create_and_list_stock(client):
    resp = await client.post("/stocks", json={"symbol": "tsla", "name": "Tesla"})
    assert resp.status_code == 201
    assert resp.json()["symbol"] == "TSLA"

    dup = await client.post("/stocks", json={"symbol": "TSLA"})
    assert dup.status_code == 409

    listing = await client.get("/stocks")
    assert listing.status_code == 200
    symbols = [s["symbol"] for s in listing.json()]
    assert "TSLA" in symbols


@pytest.mark.asyncio
async def test_ingest_then_search_offline(client, monkeypatch):
    """Ingest uses scraped data; patch the scraper so the test is offline."""
    from app.api import routes_ingest

    def fake_scrape(self, timeout: int = 15):
        return {"symbol": self.stock, "Revenue": "100B", "price": "250.00"}

    monkeypatch.setattr(
        "app.domain.scraper.StockScraper.scrape_stock_data", fake_scrape
    )

    resp = await client.post("/ingest/TSLA")
    assert resp.status_code == 200
    assert resp.json()["chunks_indexed"] >= 2
