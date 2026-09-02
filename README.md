# Doc Extraction API

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Serving-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Storage-brightgreen.svg)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-Search-orange.svg)
![Azure](https://img.shields.io/badge/Azure-Document_Intelligence-blue.svg)
![Claude](https://img.shields.io/badge/Anthropic-Claude_API-purple.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

An end-to-end document intelligence pipeline that extracts structured data from invoice PDFs using Azure Document Intelligence and Claude API, stores results in MongoDB, and exposes full-text search through Elasticsearch — all served via FastAPI and orchestrated with Docker Compose.

## Overview

Most document processing stops at OCR. This pipeline goes further. The goal is to show that a raw PDF can be ingested, understood, stored, and queried through a production-grade API — combining classical document parsing with LLM-powered extraction.

Invoices are used as the demo case, but the architecture generalizes to any semi-structured document type: contracts, receipts, forms.

## How It Works

### Pipeline Steps

Each invoice upload triggers the following steps in order:

1. **Ingest** — FastAPI receives the PDF via a POST endpoint
2. **OCR** — Azure Document Intelligence parses the file, returning structured text and layout information
3. **Extraction** — Claude API interprets the parsed output and returns clean structured JSON: vendor, amount, date, line items
4. **Storage** — the raw OCR output and extracted JSON are persisted in MongoDB
5. **Indexing** — extracted fields are pushed to Elasticsearch for full-text and filtered search
6. **Query** — FastAPI exposes search and retrieval endpoints over the indexed data

### Why Two Databases?

MongoDB is the source of truth — flexible schema, stores the full document as-is. Elasticsearch is the search engine — optimized for querying by vendor, date range, amount, or free text. They serve different purposes and complement each other.

## Project Structure

```
doc-extraction-api/
│
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Loads environment variables
│   │
│   ├── api/
│   │   └── routes/
│   │       ├── ingest.py        # POST /invoices/upload
│   │       └── search.py        # GET /invoices/search, GET /invoices/{id}
│   │
│   ├── services/
│   │   ├── ocr.py               # Azure Document Intelligence calls
│   │   ├── extraction.py        # Claude API calls
│   │   ├── storage.py           # MongoDB logic
│   │   └── indexing.py          # Elasticsearch logic
│   │
│   ├── models/
│   │   └── invoice.py           # Pydantic models — data shapes and validation
│   │
│   └── db/
│       ├── mongo.py             # MongoDB connection
│       └── elastic.py           # Elasticsearch connection
│
├── tests/
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Running the Project

## Setup

### 1. Get your API keys

**Anthropic (Claude API)**
- Sign up at [console.anthropic.com](https://console.anthropic.com)
- Go to API Keys → Create Key
- Copy the key — you'll need it for `claude_api_key` in your `.env`

**Azure Document Intelligence**
- Sign up at [portal.azure.com](https://portal.azure.com) (free tier available: 500 pages/month)
- Create a resource → search "Document Intelligence" → select the **F0** free tier
- Once created, go to **Keys and Endpoint**
- Copy the endpoint URL and Key 1 — these are your `azure_url` and `azure_key`

### 2. Configure environment variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Fill in your credentials:

```env
mongo_uri=mongodb://admin:admin@mongo:27017/invoices?authSource=admin
elastic_src=http://elasticsearch:9200
claude_api_key=your_claude_api_key
azure_url=your_azure_endpoint
azure_key=your_azure_key
```

> `mongo_uri` and `elastic_src` are pre-configured for Docker Compose. Do not change them unless running the services manually.

### 3. Run with Docker Compose

```bash
docker-compose up --build
```

This starts three containers: the FastAPI app, MongoDB, and Elasticsearch.

Once running, the API is available at `http://localhost:8000`.
Interactive docs (Swagger UI) at `http://localhost:8000/docs`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/invoices/upload` | Upload a PDF invoice for processing |
| GET | `/invoices/search?q=` | Full-text search across indexed invoices |
| GET | `/invoices/{id}` | Retrieve a specific invoice by ID |

### Upload an invoice

```bash
curl -X POST http://localhost:8000/invoices/upload \
  -F "file=@invoice.pdf"
```

### Search invoices

```bash
curl "http://localhost:8000/invoices/search?q=vendor_name"
```

### Retrieve by ID

```bash
curl http://localhost:8000/invoices/{invoice_id}
```

## Running Tests

```bash
pytest tests/
```

All external dependencies (Azure, Claude, MongoDB, Elasticsearch) are mocked. 10/10 unit tests pass without any credentials.

## License

MIT
