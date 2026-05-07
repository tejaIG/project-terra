create table public.agent_analyses (
  id uuid primary key default gen_random_uuid(),
  run_id uuid not null,
  equity_id uuid not null references public.equities(id) on delete cascade,
  agent_id text not null check (agent_id in ('geologist', 'quant', 'oracle', 'strategist')),
  analysis text not null,
  sentiment_score numeric(6,4) not null,
  confidence numeric(6,4) not null,
  created_at timestamptz not null default now()
);

create index agent_analyses_run_id_idx on public.agent_analyses(run_id);
