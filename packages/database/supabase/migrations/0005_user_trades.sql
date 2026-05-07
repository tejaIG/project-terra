create table public.user_trades (
  id uuid primary key default gen_random_uuid(),
  run_id uuid not null,
  equity_id uuid not null references public.equities(id) on delete cascade,
  user_id uuid not null,
  action text not null check (action in ('BUY', 'SELL')),
  rationale text not null,
  risk_params jsonb not null default '{}',
  approved boolean not null default false,
  created_at timestamptz not null default now()
);

create index user_trades_user_id_idx on public.user_trades(user_id);
