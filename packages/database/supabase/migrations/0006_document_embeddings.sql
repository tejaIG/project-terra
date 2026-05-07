create table public.document_embeddings (
  id uuid primary key default gen_random_uuid(),
  source text not null check (source in ('ministry_of_mines', 'nse_filing', 'bse_filing', 'broker_report', 'news')),
  source_url text,
  document_title text,
  chunk_index int not null,
  content text not null,
  embedding vector(1536) not null,
  metadata jsonb not null default '{}',
  created_at timestamptz not null default now()
);

create index document_embeddings_hnsw
  on public.document_embeddings using hnsw (embedding vector_cosine_ops);
