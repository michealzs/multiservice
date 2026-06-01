import pytest


@pytest.mark.asyncio
async def test_chat_offline_fallback(client):
    """With no LLM key, /chat returns the tool-only fallback message."""
    resp = await client.post("/chat", json={"message": "tell me about stocks"})
    assert resp.status_code == 200
    body = resp.json()
    assert "LLM provider not configured" in body["reply"]
    assert isinstance(body["used_tools"], list)
