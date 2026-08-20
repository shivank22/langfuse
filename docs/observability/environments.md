# Environments

Separate traces, observations, scores, and sessions by deployment stage so production data stays clean.

Official: [Environments](https://langfuse.com/docs/observability/features/environments).

## What and why

Use the same Langfuse **project** for all stages, but label every event with an **environment**:

| Value | Use for |
|-------|---------|
| `dev` | Local machines and developer testing |
| `staging` | Shared non-production |
| `production` | Live traffic |

This keeps dashboards, online evaluators, and filters from mixing test noise with prod.

## Naming rules

Environment strings must match: `^(?!langfuse)[a-z0-9-_]+$` and be at most **40** characters.

- Lowercase letters, numbers, hyphens, underscores only  
- Must not start with `langfuse`  
- Org standard: only `dev`, `staging`, `production` unless you have a documented exception (`qa`, `load-test`, …)  

## How to implement

### Recommended: process env var

```bash
export LANGFUSE_TRACING_ENVIRONMENT=production
```

All traces from that process inherit the environment (unless overridden).

### Client / request-scoped override

```python
import os
from langfuse import get_client, propagate_attributes

os.environ["LANGFUSE_TRACING_ENVIRONMENT"] = "staging"
langfuse = get_client()

# Or override per request (e.g. shared proxy serving multiple stages):
with langfuse.start_as_current_observation(as_type="span", name="proxy-request"):
    with propagate_attributes(environment="production"):
        pass  # child observations use production
```

If both env var and explicit parameter are set, follow SDK precedence (initialization / propagate usually wins over the bare default). When unset, Langfuse falls back to `default` — **always set an explicit org value**.

## How to use in the UI

Use the environment filter in the navigation bar; it applies across views. Compare latency or scores across `staging` vs `production` without separate projects.

Datasets and prompts can be reused across environments; filter traces when analyzing a stage.

## What good looks like

- Local runs show `dev`  
- CI / shared pre-prod shows `staging`  
- Live services show `production` only  
- Online LLM-as-a-Judge sampling targets `production` (plus tags)  

## Do / don’t

**Do** set `LANGFUSE_TRACING_ENVIRONMENT` in every deployment manifest.  
**Don’t** send load tests or notebook experiments as `production`.  
**Don’t** invent ad-hoc environment strings per PR.

## Related

- [Get started](get-started.md)  
- [Best practices](best-practices.md)  
- [Tags and metadata](tags-and-metadata.md)  
- [Managing different environments (FAQ)](https://langfuse.com/faq/all/managing-different-environments)  
