# Instrumentation — traces and spans

How to create nested observations in application code for the central Langfuse instance. Assumes [plug-in](../getting-started/plug-in.md) and ideally [get started](get-started.md).

Official: [Get started](https://langfuse.com/docs/observability/get-started), [observation types](https://langfuse.com/docs/observability/features/observation-types). Structure rules: [best practices](best-practices.md). Concepts: [data model](data-model.md).

## Observation types

| `as_type` | Use when |
|-----------|----------|
| `span` | Orchestration, retrieval wrappers, generic steps |
| `generation` | LLM calls — set **model** and **usage_details** |
| tool step | External tools — name `tool-{name}` (use SDK tool type when available) |

Wrong types break cost views and LLM-as-a-Judge filters.

## Minimal OpenAI + Langfuse nesting

```python
from langfuse import get_client
from openai import OpenAI

langfuse = get_client()
openai = OpenAI()

with langfuse.start_as_current_observation(as_type="span", name="answer-question") as root:
    root.update_trace(
        tags=["your-team", "your-service"],
        metadata={"feature": "qa"},
        input={"user": "What is Langfuse?"},
    )

    with langfuse.start_as_current_observation(
        as_type="generation",
        name="openai-chat",
        model="gpt-4o-mini",
        input={"messages": [{"role": "user", "content": "What is Langfuse?"}]},
    ) as generation:
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "What is Langfuse?"}],
        )
        text = completion.choices[0].message.content
        usage = completion.usage
        generation.update(
            output=text,
            usage_details={
                "input": usage.prompt_tokens if usage else None,
                "output": usage.completion_tokens if usage else None,
            },
        )

    root.update(output=text)

langfuse.flush()
```

Prefer [`from langfuse.openai import OpenAI`](https://langfuse.com/docs/integrations/openai/get-started) when you want automatic generation capture with less boilerplate.

## Nested agent / tool pattern

Required for [agent evaluation](../evaluation/agent-evaluation.md): tools and generations nest under one `agent-run` root.

```python
from langfuse import get_client

langfuse = get_client()

def run_agent(user_message: str) -> str:
    with langfuse.start_as_current_observation(as_type="span", name="agent-run") as root:
        root.update_trace(
            tags=["your-team", "your-agent-service"],
            input=user_message,
        )

        with langfuse.start_as_current_observation(as_type="span", name="plan") as plan:
            plan.update(output={"steps": ["retrieve", "answer"]})

        with langfuse.start_as_current_observation(as_type="span", name="tool-retrieve") as tool:
            docs = ["doc-1", "doc-2"]
            tool.update(input={"query": user_message}, output=docs)

        with langfuse.start_as_current_observation(
            as_type="generation",
            name="openai-final",
            model="gpt-4o-mini",
        ) as gen:
            answer = "..."  # OpenAI call; set usage_details when available
            gen.update(output=answer)

        root.update(output=answer)
        return answer
```

## Naming conventions (org)

| Observation | Name pattern | Example |
|-------------|--------------|---------|
| Root / request | verb-first use case | `support-reply`, `agent-run` |
| LLM call | `openai-{purpose}` | `openai-summarize` |
| Tool | `tool-{name}` | `tool-search-kb` |

Keep names **stable** (no request IDs in the name). Put dynamic values in [metadata](tags-and-metadata.md).

## Environments, sessions, tags

Set these on every real service path:

- [Environments](environments.md) — `LANGFUSE_TRACING_ENVIRONMENT`  
- [Sessions](sessions.md) — `session_id` for multi-turn  
- [Tags and metadata](tags-and-metadata.md) — always `team` + `service`  

## Async and short-lived processes

Langfuse SDKs send data asynchronously. Always `langfuse.flush()` (or equivalent shutdown) before a script, notebook exit, or batch job finishes, or traces may be lost.

Official: [queuing and batching](https://langfuse.com/docs/observability/features/queuing-batching).

## What good looks like

- Trace tree: `agent-run` → `tool-*` → `openai-*`  
- Generations show model + tokens  
- Filters by environment + service tag return only your traffic  

## Do / don’t

**Do** nest tools under the orchestrating span; use `generation` for LLM calls.  
**Don’t** flatten multi-step agents into one span.  
**Don’t** skip `flush()` on short-lived processes.

## Related

- [Get started](get-started.md)  
- [Best practices](best-practices.md)  
- [Data model](data-model.md)  
- [Prompt management in applications](../prompt-management/use-in-applications.md)  
- [Agent evaluation](../evaluation/agent-evaluation.md)  
