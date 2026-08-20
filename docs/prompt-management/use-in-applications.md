# Use prompts in applications

Fetch prompts from central Langfuse and use them with OpenAI. Assumes [plug-in](../getting-started/plug-in.md) is done.

Official get-started: [Add your first prompt](https://langfuse.com/docs/prompt-management/get-started).

## Fetch by name and label

```python
from langfuse import get_client
from openai import OpenAI

langfuse = get_client()
openai = OpenAI()

prompt = langfuse.get_prompt("support-system", label="production")
# For chat prompts, compile with variables:
messages = prompt.compile(user_name="Alex", issue="cannot login")

completion = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)
print(completion.choices[0].message.content)
```

For text prompts, use `prompt.compile(...)` to fill `{{variables}}`, then pass the resulting string into your OpenAI messages.

## Link prompt to the trace

```python
from langfuse import get_client
from langfuse.openai import OpenAI  # drop-in that can attach context

langfuse = get_client()
openai = OpenAI()

prompt = langfuse.get_prompt("support-system", label="production")
messages = prompt.compile(issue="cannot login")

with langfuse.start_as_current_observation(as_type="span", name="support-reply") as span:
    span.update_trace(tags=["support-team", "chatbot"])
    # Prefer SDK helpers that accept `langfuse_prompt=prompt` on generations
    # so the trace is linked to this prompt version — see:
    # https://langfuse.com/docs/prompt-management/features/link-to-traces
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        langfuse_prompt=prompt,
    )
    span.update(output=completion.choices[0].message.content)

langfuse.flush()
```

If your SDK version uses a different link parameter, follow the official link-to-traces page for the exact API.

## Environment-specific labels

```python
import os

label = "production" if os.getenv("APP_ENV") == "production" else "staging"
prompt = langfuse.get_prompt("support-system", label=label)
```

## Fallback for local development

Allowed for local spikes only: a checked-in default string if Langfuse is unreachable. **Production services must fail closed or use a last-known cached prompt** — do not silently ship an old hardcoded prompt as the long-term source of truth.

## What good looks like

- Changing the `production` label updates behavior without redeploying the app image  
- Traces in the UI show the prompt name and version  
- Staging apps exercise `staging` before promotion  

## Related

- [Versioning and labels](versioning-and-labels.md)  
- [Observability instrumentation](../observability/instrumentation.md)
