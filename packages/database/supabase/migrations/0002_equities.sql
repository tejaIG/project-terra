create table public.equities (
  id uuid primary key default gen_random_uuid(),
  ticker text not null unique,
  name text not null,
  exchange text not null check (exchange in ('NSE', 'BSE')),
  sector text not null default 'Mining',
  commodity_focus text not null,
  created_at timestamptz not null default now()
);
