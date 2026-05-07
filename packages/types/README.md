# @terra/types

Shared Zod schemas and TypeScript types for Project Terra.

## Cross-language model sync

- TypeScript schemas in `src/*` are the canonical shape definitions.
- Python mirrors live in `apps/intelligence-core/src/types.py`.
- When a schema changes, update both sides in the same pull request.
- Keep field names stable (`camelCase`) to avoid frontend/backend drift.
