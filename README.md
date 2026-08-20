# Central Langfuse Platform

Shared Langfuse for the organization — **central observability** and **agent evaluations** (plus prompt management), with a controlled self-hosted instance built from this source.

**Based on Langfuse 4.4.0** (see [`VERSION`](VERSION)). Upstream product README: [`README.langfuse.md`](README.langfuse.md).

**Product intent (read first):** [`docs/architecture/product-intent.md`](docs/architecture/product-intent.md)

## For application teams

You do **not** deploy Langfuse. Connect to the central instance and follow the golden path:

1. **[Plug in](docs/getting-started/plug-in.md)** — keys, env vars, verify one trace  
2. **[Observability](docs/observability/overview.md)** — [get started](docs/observability/get-started.md), data model, best practices, sessions, environments, instrumentation  
3. **[Evaluation](docs/evaluation/overview.md)** — scores, datasets, experiments, LLM-as-a-Judge · **[Agent evaluation](docs/evaluation/agent-evaluation.md)** · [Score catalog](docs/evaluation/score-catalog.md)  
4. **[Prompt management](docs/prompt-management/overview.md)** — versioning, labels, fetch in apps  

AI resource: **OpenAI** (`OPENAI_API_KEY` in your app). Docs index: [`docs/index.md`](docs/index.md).

Sample agentic apps are **out of scope** for this repo (coming later elsewhere).

## For central operators

Own and run the instance from **this** source (not only public Hub images):

```bash
cp .env.example .env   # standard local defaults — ready to run
./scripts/org/up.sh    # docker compose -f docker-compose.build.yml up -d --build
```

Local login after boot: `admin@example.com` / `e0e8a83af25fc3c29f4763b8` (user `admin`)  
Local API keys: `pk-lf-4a2c319df9fd1fec489d749f` / `sk-lf-166625364921565b786e34b3`

- Product intent: [`docs/architecture/product-intent.md`](docs/architecture/product-intent.md)  
- Components: [`docs/architecture/overview.md`](docs/architecture/overview.md)  
- Deploy / upgrade: [`docs/operations/deploy.md`](docs/operations/deploy.md)  

`docker-compose.yml` (Hub images) is for throwaway trials only. **Controlled environments use `docker-compose.build.yml`.**

## Consumer env contract

```bash
LANGFUSE_HOST=https://langfuse.example.com
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
OPENAI_API_KEY=sk-...
```

## License

Langfuse is MIT; see [`LICENSE`](LICENSE). Enterprise modules under [`ee/`](ee/) have a separate license.
