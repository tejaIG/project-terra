create table public.price_history (
  id bigint generated always as identity primary key,
  equity_id uuid not null references public.equities(id) on delete cascade,
  ts timestamptz not null,
  close_price numeric(18,4) not null,
  volume bigint not null,
  sentiment_score numeric(6,4),
  created_at timestamptz not null default now(),
  unique (equity_id, ts)
);

create index price_history_ts_brin on public.price_history using brin(ts);
