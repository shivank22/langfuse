#!/usr/bin/env bash
# Start central Langfuse from local source (controlled build path).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.build.yml}"
ENV_FILE="${ENV_FILE:-.env}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE — copy the standard local defaults:"
  echo "  cp .env.example .env"
  exit 1
fi

echo "Building and starting Langfuse (compose: $COMPOSE_FILE)..."
docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d --build

echo "Waiting for langfuse-web health..."
ready=0
for i in $(seq 1 90); do
  if curl -sf "http://127.0.0.1:3000/api/public/health" >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 2
done

if [[ "$ready" -eq 1 ]]; then
  echo "Langfuse is up: http://localhost:3000"
  echo "Next: docs/getting-started/plug-in.md (app teams) · docs/operations/deploy.md (operators)"
else
  echo "Containers started but health check did not succeed yet. Check logs:"
  echo "  docker compose -f $COMPOSE_FILE --env-file $ENV_FILE logs -f langfuse-web"
  exit 1
fi
