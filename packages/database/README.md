# @terra/database

Supabase-native data layer for Project Terra.

## Commands

- `pnpm --filter @terra/database run db:reset`
- `pnpm --filter @terra/database run gen:types`

## Notes

- SQL migrations define equities, agent debates, user HITL trades, embeddings, and time-series price history.
- `seed.sql` includes core mining equities for bootstrapping.
