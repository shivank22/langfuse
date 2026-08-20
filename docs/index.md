# Central Langfuse — Team Guidelines

This repository runs a **shared Langfuse instance** for the organization and documents how application teams use it.

Based on **Langfuse 4.4.0**. Official product docs remain the deep reference; these pages are the **org golden path**.

## Start here

1. [**Product intent and architecture**](architecture/product-intent.md) — why this platform exists (central observability + agent evaluations)  
2. [Plug in to the central instance](getting-started/plug-in.md) — keys, env vars, verify one trace  
3. Pick the capability you need:

| Pillar | Guideline | Official reference |
|--------|-----------|-------------------|
| **Observability** | [Overview](observability/overview.md) · [Get started](observability/get-started.md) · [Best practices](observability/best-practices.md) | [Langfuse Observability](https://langfuse.com/docs/observability/overview) |
| **Evaluation** | [Overview](evaluation/overview.md) · **[Agent evaluation](evaluation/agent-evaluation.md)** · [Score catalog](evaluation/score-catalog.md) | [Evaluation overview](https://langfuse.com/docs/evaluation/overview) |
| **Prompt management** | [Overview](prompt-management/overview.md) | [Prompt management](https://langfuse.com/docs/prompt-management/overview) |

## Who this is for

| Role | Go to |
|------|--------|
| App / agent engineers | [Plug-in](getting-started/plug-in.md) → observability + [agent evaluation](evaluation/agent-evaluation.md) |
| Central platform / leads | [Product intent](architecture/product-intent.md) → [Deploy](operations/deploy.md) |

## AI resource

We use **OpenAI** as the LLM provider for application calls and for Langfuse features that need an LLM (for example LLM-as-a-Judge). See [LLM-as-Judge and OpenAI](evaluation/llm-as-judge-and-openai.md).

## Out of scope here

Sample agentic applications live in a separate repo later. These guidelines use short copy-pastable snippets only.
