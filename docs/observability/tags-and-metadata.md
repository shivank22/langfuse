# Tags and metadata

Label traces for filtering and dashboards (**tags**), and attach structured context (**metadata**), without putting secrets in either.

Official: [Tags](https://langfuse.com/docs/observability/features/tags), [Metadata](https://langfuse.com/docs/observability/features/metadata).

## Tags vs metadata vs scores

| Mechanism | What | When |
|-----------|------|------|
| **Tags** | Short, enumerable labels | Known at request start (team, service, channel) |
| **Metadata** | Key-value context | Request IDs, flags, raw payloads, eval helpers |
| **Scores** | Judgments after the fact | Eval results, user thumbs — see [score catalog](../evaluation/score-catalog.md) |

Tags are typically **immutable** once set at creation — do not use them for “failed_eval=true”; use scores instead.

## Org tag conventions

**Always set**

- `team` slug — e.g. `payments-team`  
- `service` name — e.g. `checkout-api`  

**Often useful**

- Feature: `feature-refunds`  
- Experiment / prompt variant: `experiment-prompt-v2`  
- Channel: `web`, `api`, `batch`  

Keep the set small and documented. Do not invent a new tag per request ID.

```python
from langfuse import get_client

langfuse = get_client()

with langfuse.start_as_current_observation(as_type="span", name="checkout-assist") as span:
    span.update_trace(
        tags=["payments-team", "checkout-api", "experiment-prompt-v2"],
        metadata={
            "request_id": "req-abc-123",
            "feature_flag_refund_v2": True,
        },
    )
```

## Metadata — what to store

Useful in practice:

- **Request context** — internal request ID, route, app version  
- **Experiment context** — variant IDs (if not using a tag)  
- **RAG context** — index name, chunk count (not entire corpora)  
- **Eval helpers** — expected behavior fields for judges (variable mapping)  
- **Raw payloads** — only when needed for debug; prefer not to duplicate huge blobs in input/output  

**Never** store API keys, passwords, or unconstrained PII.

## How to use in the UI

Filter traces by tag (`your-service`) and environment together. Use metadata filters when hunting a specific `request_id`. Breakdown dashboards by tag for latency/cost by service.

## What good looks like

- Every trace has `team` + `service` tags  
- Prod filter + service tag isolates one team’s live traffic  
- Experiment tags allow side-by-side comparison of two prompt versions  

## Do / don’t

**Do** reuse the same team/service tags across all services owned by that team.  
**Don’t** put dynamic unique values in tags (use metadata).  
**Don’t** use tags for post-hoc eval outcomes (use scores).

## Related

- [Environments](environments.md)  
- [Best practices](best-practices.md)  
- [Sessions](sessions.md)  
- [Agent evaluation](../evaluation/agent-evaluation.md)  
