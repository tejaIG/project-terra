# Project Terra

Project Terra is a multi-agent AI framework for Indian mining equity intelligence.

## Apps

- `apps/command-center`: Next.js command interface (War Room).
- `apps/intelligence-core`: FastAPI + LangGraph orchestration runtime.

## Packages

- `packages/types`: Shared Zod schemas and TypeScript types.
- `packages/ui`: Shared UI primitives and utilities.
- `packages/database`: Supabase client and SQL migrations.

## Quick Start

1. Install dependencies: `pnpm install`
2. Frontend dev: `pnpm dev:fe`
3. Backend dev: `pnpm dev:be`

## Runtime Flow

1. `POST /runs` with `{ "ticker": "NMDC" }` to start a council run.
2. Connect `ws://localhost:8000/ws/council/{runId}` for real-time events.
3. Receive typed events: `run_started`, `agent_thought`, `price_tick`, `run_completed`, `error`.

## Environment

- Frontend: `NEXT_PUBLIC_WS_URL`, `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- Backend: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `LLM_PROVIDER`, `LLM_MODEL`, `OPENAI_API_KEY`, `KITE_API_KEY`, `KITE_ACCESS_TOKEN`
