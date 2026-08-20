# Observability guidelines

## Start here

1. **[Get started](get-started.md)** — emit your first trace to the central instance  
2. **[Data model](data-model.md)** — traces, observations, sessions  
3. **[Best practices](best-practices.md)** — what a good trace looks like  
4. **[Instrumentation](instrumentation.md)** — nested spans, OpenAI, agents, flush  

Then add [sessions](sessions.md), [environments](environments.md), and [tags and metadata](tags-and-metadata.md).

Official: [Observability overview](https://langfuse.com/docs/observability/overview).

## What and why

**Observability** means you can see what your LLM or agent app did on each request: prompts, model responses, tool calls, latency, and cost.

The core technique is **application tracing** — structured records of every request and its nested steps. Without it, debugging non-deterministic AI behavior is guesswork.

We use the **central Langfuse** instance so every team shares one place to inspect `dev`, `staging`, and `production` behavior. Good traces also power [evaluation](../evaluation/overview.md) and [agent evaluation](../evaluation/agent-evaluation.md).

## Build-time vs runtime

| Phase | Meaning | Our focus |
|-------|---------|-----------|
| **Build-time** | Offline datasets and experiments before you ship a change | Supported (datasets / experiments) |
| **Runtime** | Live traces and online scores while the agent runs | **Primary** — this is what Central Langfuse is for |

Agent failures (wrong tools, loops, goal drift) often appear only at runtime. Instrument production paths first; use offline experiments to gate changes before they reach production. See [product intent — agentic observability](../architecture/product-intent.md#3-agentic-observability-build-time-vs-runtime).

## Observability vs tracing

| Term | Meaning |
|------|---------|
| **Observability** | Broader ability to understand system state from outputs (traces, metrics, logs) |
| **Tracing** | Recording the flow of a request with causal links between steps |

For LLM apps, tracing is the primary observability tool because it captures prompts, responses, tools, and their relationships.

## Does Langfuse add latency?

No. SDKs queue events locally and flush in the background. Your request path is not blocked. Short-lived scripts must still call `flush()` before exit — see [get started](get-started.md) and [queuing and batching](https://langfuse.com/docs/observability/features/queuing-batching).

## If you want to…

| If you want to… | Go to |
|-----------------|--------|
| Emit the first OpenAI + Langfuse trace | [Get started](get-started.md) |
| Understand traces / observations / sessions | [Data model](data-model.md) |
| Structure traces for evals and dashboards | [Best practices](best-practices.md) |
| Nest agent tools and generations | [Instrumentation](instrumentation.md) |
| Multi-turn chat replay | [Sessions](sessions.md) |
| Separate prod from staging | [Environments](environments.md) |
| Filter by team / service | [Tags and metadata](tags-and-metadata.md) |
| Score agents on those traces | [Agent evaluation](../evaluation/agent-evaluation.md) |

## When to instrument

Instrument any path that:

- Calls an LLM (OpenAI or otherwise)  
- Runs agent / tool loops  
- Retrieves context for generation  
- Matters for cost, latency, quality review, or evaluation  

## Do / don’t

**Do**

- Always set environment (`dev` / `staging` / `production`)  
- Tag with `team` and `service`  
- Nest observations (parent → tools → generations)  
- Flush on short-lived jobs  

**Don’t**

- Log secrets or unnecessary PII  
- Flatten multi-step agents into one span  
- Mix `production` traffic into `dev`  

## Guides in this section

- [Get started](get-started.md)  
- [Data model](data-model.md)  
- [Best practices](best-practices.md)  
- [Instrumentation](instrumentation.md)  
- [Sessions](sessions.md)  
- [Environments](environments.md)  
- [Tags and metadata](tags-and-metadata.md)  
