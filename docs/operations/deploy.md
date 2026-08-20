# Operations — deploy Langfuse

For **central platform operators**. Application teams use [plug-in](../getting-started/plug-in.md) instead.

This repo vendors Langfuse **4.4.0**. The controlled path **builds images from local Dockerfiles**.

## Prerequisites

- Docker and Docker Compose  
- Enough CPU/RAM for web + worker + Postgres + ClickHouse + Redis + MinIO (see upstream self-hosting guidance; prefer ≥ 4 vCPU / 16 GiB for shared use)

## Configure environment

```bash
cp .env.example .env
```

[`.env.example`](../../.env.example) already contains **working local defaults** (matching Postgres URL/password, MinIO keys, headless init admin user and API keys). No placeholders to invent.

For a shared or production host, replace secrets with generated values (`openssl rand -base64 32`, `openssl rand -hex 32` for `ENCRYPTION_KEY`) before exposing the instance.

Default local login after headless init: `admin@example.com` / `e0e8a83af25fc3c29f4763b8` (display name `admin`).  
Default local API keys: `pk-lf-4a2c319df9fd1fec489d749f` / `sk-lf-166625364921565b786e34b3`.

Configure OpenAI for in-product LLM features (LLM-as-a-Judge) via the Langfuse UI after boot. App teams keep their own `OPENAI_API_KEY` in their services.

## Start (build from source)

```bash
./scripts/org/up.sh
# or:
docker compose -f docker-compose.build.yml --env-file .env up -d --build
```

Wait until `langfuse-web` is healthy, then open `http://localhost:3000` (or your `NEXTAUTH_URL`).

## Quickstart only (not the control path)

`docker-compose.yml` pulls pre-built Hub images. Use it only for a throwaway trial. **Shared / controlled environments must use `docker-compose.build.yml`** so patches in this repo are what you run.

## Upgrade

1. Update source in this repo (or bump `VERSION` when rebasing upstream)  
2. Rebuild and recreate:

```bash
docker compose -f docker-compose.build.yml --env-file .env up -d --build
```

Follow upstream upgrade notes when crossing major versions: [Langfuse upgrade](https://langfuse.com/self-hosting/upgrade).

## Stop

```bash
docker compose -f docker-compose.build.yml --env-file .env down
# add -v only if you intend to delete data volumes
```

## Health checks

- Web: `GET /api/public/health` on port 3000  
- Worker: health endpoint on port 3030 (see compose healthchecks)

## CI

Pull requests validate that `docker-compose.build.yml` parses. See `.github/workflows/org-compose-validate.yml`.
