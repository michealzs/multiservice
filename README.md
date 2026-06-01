# Stock Intelligence Service

A FastAPI + LangChain/LangGraph service for stock research, converted from the
original Django `multiservice` project. The original app's Yahoo Finance
`StockScraper` and `Stock` model are preserved and re-exposed as an async API
with a retrieval-augmented agent on top.

## Stack

| Concern        | Technology |
|----------------|------------|
| API            | FastAPI + Uvicorn |
| Data           | SQLAlchemy (async) + Postgres |
| Vector store   | **pgvector** (primary), Weaviate & Pinecone adapters (optional) |
| LLM / agents   | LangChain + LangGraph (`create_react_agent`) |
| Observability  | Langfuse + LangSmith |
| IaC            | Terraform (pgvector container, optional Pinecone index / Weaviate) |

## What was ported

- `stocksapp/stocks.py` → `app/domain/scraper.py` (`StockScraper`, logic preserved, hardened).
- `stocksapp/models.py:Stock` → `app/domain/models.py` (SQLAlchemy).
- `HomeView` (list stocks + scrape) → `GET /stocks`, `GET /stocks/{symbol}/data`.

The Django project, templates, and static assets were removed.

## Endpoints

| Method | Path                    | Description |
|--------|-------------------------|-------------|
| GET    | `/healthz`, `/readyz`   | Liveness / readiness |
| GET    | `/stocks`               | List tracked stocks |
| POST   | `/stocks`               | Add a stock |
| GET    | `/stocks/{symbol}/data` | Live Yahoo Finance scrape |
| POST   | `/ingest/{symbol}`      | Scrape + embed fundamentals into the vector store |
| POST   | `/chat`                 | RAG agent (LangGraph) over scraped + ingested data |

## Run it

### Docker (recommended)
```bash
cp .env.example .env          # optionally add DEEPSEEK_API_KEY for full /chat
docker compose up -d --build
curl localhost:8000/healthz
curl -X POST localhost:8000/ingest/TSLA
curl -X POST localhost:8000/chat -H 'content-type: application/json' \
     -d '{"message": "How is TSLA doing?"}'
```

### Local
```bash
make install
make test                     # runs offline on sqlite + in-memory vectors
make run
```

## Keyless operation

The service runs **end-to-end with no API keys**: stock CRUD and live scraping
work as-is; embeddings fall back to a deterministic offline implementation and
the vector store falls back to an in-memory cosine index; `/chat` returns a
tool-only summary. Provide `DEEPSEEK_API_KEY` (or `OPENAI_API_KEY` / `ANTHROPIC_API_KEY`) to enable
full natural-language answers, and Langfuse/LangSmith keys to enable tracing.

## Vector backends

Set `VECTOR_BACKEND` to `pgvector` (default), `weaviate`, or `pinecone`. Each is
implemented behind the `app/vectorstores` interface; an unavailable backend
falls back to the in-memory store with a logged warning.

## Terraform

```bash
cd terraform
terraform init
terraform plan                                   # pgvector container only
terraform apply -var 'enable_pinecone=true'      # also create a Pinecone index
```
