-- Executado pelo PostgreSQL somente na inicialização de um volume vazio.
-- Campos inseridos por salvar_execucao e consultados por buscar_cache.
CREATE TABLE IF NOT EXISTS executions (
    id UUID PRIMARY KEY,
    prompt_hash TEXT NOT NULL,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    temperature DOUBLE PRECISION NOT NULL,
    validation_version INTEGER NOT NULL,
    record JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS executions_cache_idx
    ON executions (prompt_hash, validation_version, model, provider, temperature, created_at DESC);
