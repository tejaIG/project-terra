alter table public.equities enable row level security;
alter table public.price_history enable row level security;
alter table public.agent_analyses enable row level security;
alter table public.user_trades enable row level security;

create policy "equities_select_authenticated"
on public.equities
for select
to authenticated
using (true);

create policy "price_history_select_authenticated"
on public.price_history
for select
to authenticated
using (true);

create policy "agent_analyses_select_authenticated"
on public.agent_analyses
for select
to authenticated
using (true);

create policy "user_trades_select_own"
on public.user_trades
for select
to authenticated
using (auth.uid() = user_id);

create policy "user_trades_insert_own"
on public.user_trades
for insert
to authenticated
with check (auth.uid() = user_id);
