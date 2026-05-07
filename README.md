# Project Terra

building this for my self.


> **Autonomous Indian Mining Intelligence Nexus** — A multi-agent AI framework for commodity-driven equity investment on the NSE & BSE.

---

## Table of Contents

1. [Overview](#overview)
2. [The Problem Statement](#the-problem-statement)
3. [System Architecture](#system-architecture)
   - [The AI Council](#the-ai-council)
   - [LangGraph Orchestration](#langgraph-orchestration)
   - [WebSocket Real-Time Layer](#websocket-real-time-layer)
4. [Monorepo Structure](#monorepo-structure)
5. [Tech Stack](#tech-stack)
6. [Database Schema](#database-schema)
7. [API Reference](#api-reference)
8. [Environment Variables](#environment-variables)
9. [Getting Started](#getting-started)
10. [Development Scripts](#development-scripts)
11. [Risk Management & Governance](#risk-management--governance)
12. [Target Equities](#target-equities)
13. [Roadmap](#roadmap)

---

## Overview

India's mining sector sits at the intersection of rapid infrastructure expansion, energy transition, and state-owned enterprise (PSU) dynamics. Processing the firehose of global commodity prices, Ministry of Mines regulatory shifts, quarterly filings, and real-time NSE/BSE price action is beyond any single human analyst.

**Project Terra** solves this with an enterprise-grade, multi-agent AI system — an "AI Council" of four specialized agents that run in parallel, debate, and synthesize a final trade signal with a human-in-the-loop approval gate. It monitors equities like Coal India, NMDC, Hindalco, and Vedanta across four commodity pillars: **Coal, Iron Ore/Steel, Zinc/Base Metals, and Aluminium/Copper**.

---

## The Problem Statement

| Challenge | Impact |
|---|---|
| **PSU & Policy Premium** | Government mineral block auctions, export taxes, and divestment news are as impactful as global LME prices — and harder to track |
| **Information Asymmetry** | Alpha-generating insights are buried across Ministry of Mines PDFs, broker reports, and Moneycontrol headlines |
| **Domestic vs. Global Disconnect** | Hindustan Zinc's stock is tethered to LME zinc spot prices yet driven by domestic infrastructure budgets — both signals must be weighted simultaneously |
| **Human Processing Limits** | A single analyst cannot simultaneously run technical analysis, read every NSE/BSE filing, and monitor global commodity feeds in real time |

Project Terra replaces this bottleneck with autonomous, parallel AI processing.

---

## System Architecture

### The AI Council

Rather than a single model, Project Terra deploys four distinct AI personas that each analyze the same equity from a different lens, then hand off to a Lead Strategist who synthesizes their findings into a final signal.

```
POST /runs { ticker: "NMDC" }
         │
         ▼
┌─────────────────────────────────────────────────────┐
│                  LangGraph Council                  │
│                                                     │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │  Geologist  │  │    Quant     │  │  Oracle   │  │──▶ parallel execution
│  │ (Fundamentals)│  │  (Technicals)│  │(Sentiment)│  │
│  └──────┬──────┘  └──────┬───────┘  └─────┬─────┘  │
│         └────────────────┴────────────────┘         │
│                          │                          │
│                  ┌───────▼───────┐                  │
│                  │  Strategist   │                  │
│                  │(Lead Analyst) │                  │
│                  └───────┬───────┘                  │
└──────────────────────────┼──────────────────────────┘
                           │
                    TradeSignal (BUY/HOLD/SELL)
                    + confidence score
                    + plain-English thesis
                           │
                  Human Approval Gate
                  POST /trades (HITL)
```

#### The Geologist — Fundamental Analyst

- **Mandate:** Evaluate intrinsic value, operational health, and regulatory standing.
- **Data Sources:** NSE/BSE corporate filings, Ministry of Mines auction results, CAPEX plans, government royalty rates, and infrastructure budget allocations.
- **Key Tasks:** Production cost analysis, debt level assessment, NMDC-style capacity expansion tracking, and the impact of government export taxes.

#### The Quant — Quantitative Analyst

- **Mandate:** Identify optimal entry and exit points from market momentum and historical price action.
- **Data Sources:** Real-time NSE/BSE pricing, volume data, and global commodity spot prices (LME).
- **Key Tasks:** Moving averages, momentum indicators, correlation coefficients between a stock and its primary commodity (e.g., Vedanta vs. LME Zinc).

#### The Oracle — Sentiment Engine

- **Mandate:** Gauge the psychological state of the domestic and institutional market.
- **Data Sources:** Economic Times, Moneycontrol, broker upgrade/downgrade reports, retail investor forums.
- **Key Tasks:** Detecting irrational exuberance or extreme pessimism to provide a contrarian indicator to the Strategist.

#### The Strategist — Lead Portfolio Manager

- **Mandate:** Synthesize all three analyses into a final, actionable recommendation.
- **Key Tasks:** Weigh conflicting signals (e.g., "Technicals are bearish, but the government just announced a major infrastructure push benefiting Tata Steel"), then output a `BUY / HOLD / SELL` signal with a confidence score and a plain-English justification.

---

### LangGraph Orchestration

The council is built as a compiled **LangGraph `StateGraph`**. The three specialist agents (`parallel_agents` node) execute concurrently via `asyncio.gather`, and only once all three finish does the graph transition to the `strategist` node.

```python
# council.py — simplified graph topology
graph.add_node("parallel_agents", parallel_agents_node)  # Geologist + Quant + Oracle in parallel
graph.add_node("strategist", strategist_node)            # Lead Strategist synthesizes
graph.set_entry_point("parallel_agents")
graph.add_edge("parallel_agents", "strategist")
graph.add_edge("strategist", END)
```

`CouncilState` is a `TypedDict` threaded through the graph, accumulating `AgentAnalysis` objects from each agent before the `Strategist` emits the final `TradeSignal`.

---

### WebSocket Real-Time Layer

A WebSocket endpoint streams typed events to the Command Center frontend so the user can watch the AI Council "think" in real time.

**Connect:** `ws://localhost:8000/ws/council/{runId}`

| Event Type | Payload |
|---|---|
| `run_started` | `{ runId, ticker, timestamp }` |
| `agent_thought` | `{ agent, ticker, analysis, confidence }` |
| `price_tick` | `{ ticker, price, volume, timestamp }` |
| `run_completed` | `{ signal: TradeSignal \| null }` |
| `error` | `{ message }` |

The backend `EventBus` is an in-process pub/sub service. Each WebSocket connection subscribes to its `run_id` channel and receives only events for that run.

---

## Monorepo Structure

```
project-terra/
├── apps/
│   ├── command-center/          # Next.js 15 frontend — the "War Room" UI
│   │   └── src/
│   └── intelligence-core/       # FastAPI + LangGraph backend
│       └── src/
│           ├── agents/          # geologist.py, quant.py, oracle.py, strategist.py
│           ├── api/             # routes.py (REST), websocket.py (WS)
│           ├── services/        # event_bus, market_data, persistence, broker, tick_simulator
│           ├── tools/           # commodity_prices, mining_filings, news_sentiment
│           ├── council.py       # LangGraph StateGraph definition
│           ├── types.py         # Pydantic models: MarketData, AgentAnalysis, TradeSignal
│           └── main.py          # FastAPI app entry point
├── packages/
│   ├── types/                   # Shared Zod schemas + TypeScript types
│   ├── ui/                      # Shared React UI primitives
│   └── database/                # Supabase client + SQL migrations
│       └── supabase/migrations/
│           ├── 0001_init_extensions.sql
│           ├── 0002_equities.sql
│           ├── 0003_price_history.sql
│           ├── 0004_agent_analyses.sql
│           ├── 0005_user_trades.sql
│           ├── 0006_document_embeddings.sql
│           └── 0007_rls_policies.sql
├── package.json                 # pnpm workspace root
└── turbo.json                   # Turborepo pipeline config
```

---

## Tech Stack

### Frontend — `apps/command-center`

| Layer | Technology |
|---|---|
| Framework | [Next.js 15](https://nextjs.org/) (App Router) |
| Language | TypeScript 5 (strict mode) |
| UI | React 19 + Tailwind CSS 3 |
| Charts | [lightweight-charts](https://tradingview.github.io/lightweight-charts/) v4 |
| Utilities | `clsx`, `tailwind-merge` |
| Validation | Zod (via `@terra/types` package) |

### Backend — `apps/intelligence-core`

| Layer | Technology |
|---|---|
| Runtime | Python 3.11+ |
| Web Framework | [FastAPI](https://fastapi.tiangolo.com/) 0.115+ with Uvicorn |
| AI Orchestration | [LangGraph](https://langchain-ai.github.io/langgraph/) 0.2+ |
| LLM Integration | LangChain 0.3 + `langchain-openai` |
| Data Models | Pydantic v2 + `pydantic-settings` |
| HTTP Client | `httpx` |
| Data Processing | NumPy 2 + Pandas 2 |
| Scraping | BeautifulSoup4 |
| Package Manager | [uv](https://docs.astral.sh/uv/) |
| Testing | pytest 8 |

### Infrastructure

| Layer | Technology |
|---|---|
| Database | [Supabase](https://supabase.com/) (PostgreSQL + pgvector) |
| Auth | Supabase Auth (JWT bearer tokens) |
| Monorepo | [Turborepo](https://turbo.build/) + pnpm 9 workspaces |
| Broker Integration | Zerodha Kite Connect API |

---

## Database Schema

All tables live in the `public` schema with Row Level Security (RLS) enforced.

| Table | Description |
|---|---|
| `equities` | Master list of tracked NSE/BSE equities (ticker, name, exchange, commodity focus) |
| `price_history` | Time-series OHLCV price records per equity |
| `agent_analyses` | Persisted `AgentAnalysis` outputs from each council run |
| `user_trades` | Trade approvals submitted by the authenticated user (RLS: own rows only) |
| `document_embeddings` | pgvector embeddings for semantic search over filings and news |

RLS policies ensure that:
- `equities`, `price_history`, and `agent_analyses` are **readable by any authenticated user**.
- `user_trades` enforces **row-ownership**: a user can only `SELECT` and `INSERT` their own trade records.

---

## API Reference

### `POST /runs`

Triggers a full council analysis run asynchronously.

**Request body:**
```json
{ "ticker": "NMDC" }
```

**Response:**
```json
{ "runId": "550e8400-e29b-41d4-a716-446655440000" }
```

Connect to `ws://localhost:8000/ws/council/{runId}` immediately after to receive streamed events.

---

### `POST /trades`

Approves a trade signal generated by the council. Requires a valid Supabase JWT bearer token.

**Headers:**
```
Authorization: Bearer <supabase_access_token>
```

**Request body:**
```json
{
  "runId": "550e8400-...",
  "signal": {
    "ticker": "NMDC",
    "action": "BUY",
    "confidence": 0.82,
    "thesis": "NMDC's capacity expansion aligns with...",
    "suggestedPositionSize": 50000
  }
}
```

**Response:**
```json
{ "status": "approved" }
```

---

### `GET /health`

Returns `{ "status": "ok" }`. Used for liveness probes.

---

## Environment Variables

### Frontend (`apps/command-center/.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://<project-ref>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon-key>
```

### Backend (`apps/intelligence-core/.env`)

```env
# Supabase
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_SERVICE_ROLE_KEY=<service-role-key>

# LLM
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
OPENAI_API_KEY=sk-...

# Zerodha Kite Connect (broker integration)
KITE_API_KEY=<kite-api-key>
KITE_ACCESS_TOKEN=<kite-access-token>

# CORS (comma-separated origins)
CORS_ORIGINS=http://localhost:3000
```

> **Never commit secrets.** Load all credentials exclusively from environment variables. Use a `.env` file locally and a secrets manager in production.

---

## Getting Started

### Prerequisites

- **Node.js** >= 18
- **pnpm** 9 (`npm install -g pnpm@9`)
- **Python** >= 3.11
- **uv** (`pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- A **Supabase** project with the migrations applied

### 1. Clone & Install

```bash
git clone https://github.com/your-org/project-terra.git
cd project-terra
pnpm install
```

### 2. Configure Environment

Copy the example env files and fill in your credentials:

```bash
cp apps/command-center/.env.example apps/command-center/.env.local
cp apps/intelligence-core/.env.example apps/intelligence-core/.env
```

### 3. Apply Database Migrations

```bash
pnpm db:reset
```

This runs all migrations in `packages/database/supabase/migrations/` in order.

### 4. Generate TypeScript Types from Supabase

```bash
pnpm db:types
```

### 5. Start the Backend

```bash
pnpm dev:be
# FastAPI server starts at http://localhost:8000
# Docs available at http://localhost:8000/docs
```

### 6. Start the Frontend

```bash
pnpm dev:fe
# Next.js starts at http://localhost:3000
```

---

## Development Scripts

All scripts are run from the monorepo root.

| Script | Description |
|---|---|
| `pnpm dev:fe` | Start the Next.js Command Center on port 3000 |
| `pnpm dev:be` | Start the FastAPI Intelligence Core on port 8000 (with `--reload`) |
| `pnpm build` | Turborepo full build across all apps and packages |
| `pnpm lint` | Run ESLint + mypy across the workspace |
| `pnpm test` | Run pytest (backend) and any frontend tests |
| `pnpm format` | Prettier format all `.ts`, `.tsx`, `.md`, `.json`, `.yaml` files |
| `pnpm db:types` | Regenerate Supabase TypeScript types |
| `pnpm db:reset` | Re-apply all database migrations |

---

## Risk Management & Governance

Capital preservation is the foundational principle of Project Terra. The system enforces multiple layers of control:

| Control | Implementation |
|---|---|
| **Human-in-the-Loop (HITL)** | The system is **expressly forbidden** from executing live trades without cryptographic approval via `POST /trades` using a valid user JWT. |
| **Dynamic Stop-Losses** | The Quant agent continuously calculates volatility-adjusted stop-loss levels; the Strategist embeds them in every `TradeSignal`. |
| **Hard Exposure Limits** | The Strategist is constrained from recommending over-exposure to any single commodity or individual company. |
| **Confidence Scoring** | Every `TradeSignal` carries a `confidence` score (0–1). The Command Center UI visually degrades low-confidence signals to discourage impulsive approvals. |
| **Audit Trail** | All council runs, agent analyses, and approved trades are persisted in Supabase with timestamps for full post-trade accountability. |

---

## Target Equities

Project Terra is pre-configured for four commodity pillars of the Indian mining economy:

| Pillar | Equities | Drivers |
|---|---|---|
| **Coal** (Energy Backbone) | Coal India (CIL) | Thermal power demand, renewable energy transition, PSU dividend yield |
| **Iron Ore & Steel** (Infrastructure Anchor) | NMDC, Tata Steel, JSW Steel | India infrastructure budget, auto manufacturing, Chinese property sector |
| **Zinc & Base Metals** (Industrial Core) | Hindustan Zinc (HZL), Vedanta | Global supply deficits, domestic construction, operational cost efficiency |
| **Aluminium & Copper** (Electrification Play) | Hindalco, Hindustan Copper | EV manufacturing, power grid modernization, global green energy transition |

---

## Roadmap

- [ ] Live Zerodha Kite Connect trade execution (currently simulated)
- [ ] pgvector semantic search over Ministry of Mines filings via `document_embeddings`
- [ ] Expand to BSE500 mining constituents beyond the initial eight equities
- [ ] Backtesting harness against historical NSE/BSE price data
- [ ] Multi-user portfolio isolation with per-user exposure limits
- [ ] Slack / Telegram notification channel for high-confidence signals

---

> **Disclaimer:** Project Terra is a research and educational tool. It is not registered investment advice. Always consult a SEBI-registered financial advisor before making investment decisions.
