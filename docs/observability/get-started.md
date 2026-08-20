# Get started with tracing

Emit your first trace into the **central Langfuse** instance, then verify it in the UI.

Official: [Get started with tracing](https://langfuse.com/docs/observability/get-started). For concepts, see [data model](data-model.md). For structure quality, see [best practices](best-practices.md).

## Prerequisites

1. Complete [plug-in](../getting-started/plug-in.md) — you have host + API keys  
2. Install SDKs: `pip install langfuse openai`  
3. Set environment variables:

```bash
LANGFUSE_HOST=http://localhost:3000          # or your central URL
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_TRACING_ENVIRONMENT=dev             # see environments.md
OPENAI_API_KEY=sk-...
```

## Minimal example (manual nesting)

```python
from langfuse import get_client
from openai import OpenAI

langfuse = get_client()
openai = OpenAI()

with langfuse.start_as_current_observation(as_type="span", name="hello-langfuse") as root:
    root.update_trace(
        tags=["your-team", "your-service"],
        input={"user": "Say hello in one sentence."},
    )
    with langfuse.start_as_current_observation(
        as_type="generation",
        name="openai-chat",
        model="gpt-4o-mini",
    ) as generation:
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say hello in one sentence."}],
        )
        text = completion.choices[0].message.content
        usage = completion.usage
        generation.update(
            input={"messages": [{"role": "user", "content": "Say hello in one sentence."}]},
            output=text,
            usage_details={
                "input": usage.prompt_tokens if usage else None,
                "output": usage.completion_tokens if usage else None,
            },
        )
    root.update(output=text)
    print(text)

langfuse.flush()  # required for scripts / short-lived jobs
```

## Drop-in OpenAI client (less boilerplate)

```python
from langfuse import get_client
from langfuse.openai import OpenAI  # wraps OpenAI and records generations

langfuse = get_client()
openai = OpenAI()

with langfuse.start_as_current_observation(as_type="span", name="hello-langfuse") as root:
    root.update_trace(tags=["your-team", "your-service"])
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say hello in one sentence."}],
        name="openai-chat",
    )
    root.update(output=completion.choices[0].message.content)

langfuse.flush()
```

See [OpenAI integration](https://langfuse.com/docs/integrations/openai/get-started).

## Verify in the UI

1. Open the central Langfuse UI → **Traces**  
2. Find `hello-langfuse` (filter by tag `your-service` if needed)  
3. Confirm nested `openai-chat` generation with input, output, and usage  

If nothing appears: check keys/host, network access, and that you called `flush()` before the process exited.

## What good looks like

- One root span with clear input/output  
- Generation typed correctly with model + tokens  
- Environment `dev` and tags `team` / `service` set  

## Do / don’t

**Do** start from this pattern, then add nesting for tools ([instrumentation](instrumentation.md)).  
**Don’t** skip `flush()` in CLIs, notebooks that exit, or batch jobs.

## Next

- [Data model](data-model.md)  
- [Best practices](best-practices.md)  
- [Instrumentation](instrumentation.md)  
- [Environments](environments.md)  
