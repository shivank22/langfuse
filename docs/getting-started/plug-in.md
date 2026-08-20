# Plug in to central Langfuse

Connect your application to the shared Langfuse instance. You do **not** deploy Langfuse yourself.

## Prerequisites

- Project API keys from the central platform team (public + secret)
- Base URL of the central instance (example: `https://langfuse.example.com` or `http://localhost:3000` for local)
- An OpenAI API key for your app’s LLM calls

## Environment variables

```bash
# Langfuse (required)
LANGFUSE_HOST=https://langfuse.example.com
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...

# OpenAI (app-side LLM calls)
OPENAI_API_KEY=sk-...
```

Optional but recommended:

```bash
LANGFUSE_TRACING_ENVIRONMENT=dev   # or staging / production
```

Install the Python SDK:

```bash
pip install langfuse openai
```

## Verify with one trace

```python
import os
from langfuse import get_client
from openai import OpenAI

# Reads LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST from env
langfuse = get_client()
openai = OpenAI()

with langfuse.start_as_current_observation(
    as_type="span",
    name="hello-langfuse",
    metadata={"team": "your-team", "service": "your-service"},
) as span:
    span.update_trace(
        user_id="verify-user",
        tags=["onboarding", "your-team"],
        metadata={"environment": os.getenv("LANGFUSE_TRACING_ENVIRONMENT", "dev")},
    )
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say hello in one sentence."}],
    )
    text = completion.choices[0].message.content
    span.update(output=text)
    print(text)

langfuse.flush()
```

## What good looks like

1. Open the Langfuse UI → **Traces**
2. Find a trace named `hello-langfuse`
3. Confirm input/output, tags, and timing appear

If nothing shows up: check keys, host URL (no trailing slash issues), network access to the central host, and that you called `flush()` before the process exits.

## Next steps

- [Observability instrumentation](../observability/instrumentation.md)  
- [Observability get started](../observability/get-started.md)
- [Evaluation overview](../evaluation/overview.md)
- [Prompt management in apps](../prompt-management/use-in-applications.md)
