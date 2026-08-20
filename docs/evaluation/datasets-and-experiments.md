# Datasets and experiments

## Datasets

A **dataset** is a collection of items. Each item has an **input** (scenario) and optionally an **expected output**.

Create and manage datasets in the Langfuse UI or via SDK. Prefer managing them in Langfuse so you get in-UI comparison tables and can add items from production traces.

Official: [Datasets](https://langfuse.com/docs/evaluation/experiments/datasets).

### Org practice

1. One dataset per major use case (for example `support-bot-core` or `support-agent-core`)  
2. **Seed** with a small gold set by hand (UI or SDK): realistic inputs; expected outputs only when objectively checkable  
3. **Grow** when online eval or humans find a failure — open the live trace and **add it to the dataset** (promote failures)  
4. Use [score catalog](score-catalog.md) names when attaching evaluators  

How this fits agentic observability (build-time vs runtime): [product intent — How the dataset is created](../architecture/product-intent.md#how-the-dataset-is-created).

## Agent dataset item shape

For tool-using agents, put structured fields in `input` / `expected_output` so code evaluators can assert tools and outcomes. See [Agent evaluation](agent-evaluation.md).

```json
{
  "input": {
    "user_goal": "Cancel order 12345 and confirm refund timeline",
    "context": { "channel": "chat" }
  },
  "expected_output": {
    "expected_tools": ["get_order", "cancel_order"],
    "answer_contains": ["canceled", "refund"]
  }
}
```

Create the dataset once in the UI (`support-agent-core`), then add items from the UI or SDK. Promote production failures by copying the user goal (and optional tool expectations) into a new item.

## Experiments

An **experiment** runs your **task** (application code) on each dataset item, then scores the outputs.

Official: [Experiments via SDK](https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk), [via UI](https://langfuse.com/docs/evaluation/experiments/experiments-via-ui).

### Generic task + exact match

```python
from langfuse import get_client, Evaluation

langfuse = get_client()

def my_task(*, item, **kwargs):
    """Run your app / agent for one dataset item."""
    user_input = item.input
    # call your pipeline + OpenAI here
    return {"output": "..."}

def exact_match(*, input, output, expected_output, **kwargs):
    if expected_output is None:
        return Evaluation(name="has_expected", value=None, comment="no expected")
    ok = str(output.get("output", "")).strip() == str(expected_output).strip()
    return Evaluation(name="correctness", value=ok)

# Pseudocode — see current SDK docs for the exact experiment helper:
# https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk
#
# result = langfuse.run_experiment(
#     name="prompt-v2-vs-baseline",
#     data=langfuse.get_dataset("support-bot-core").items,
#     task=my_task,
#     evaluators=[exact_match],
# )
```

### Agent task pattern

```python
def agent_task(*, item, **kwargs):
    payload = item.input if isinstance(item.input, dict) else {"user_goal": item.input}
    user_goal = payload["user_goal"]
    answer = run_agent(user_goal)  # your nested-traced agent
    return {
        "output": answer,
        "tools_used": list(getattr(run_agent, "last_tools", [])),
    }

def tool_correctness(*, input, output, expected_output, **kwargs):
    expected = (expected_output or {}).get("expected_tools") or []
    if not expected:
        return Evaluation(name="tool_correctness", value=None, comment="no expected_tools")
    used = output.get("tools_used") or []
    return Evaluation(name="tool_correctness", value=list(used) == list(expected))
```

Use the **UI** for quick prompt-only iterations when the task is a Langfuse-managed prompt. Use the **SDK** when the task is your full agent or application.

### Interpreting agent experiment runs

In the experiment comparison UI, expect columns (or linked scores) for catalog metrics such as `goal_achieved`, `tool_correctness`, `trajectory_ok`, and `faithfulness`. Open a failing row and inspect the nested tool spans on the trace.

## Scoring from the app (online)

```python
from langfuse import get_client

langfuse = get_client()

with langfuse.start_as_current_observation(as_type="span", name="live-request") as span:
    # ... produce output ...
    span.update(output={"text": "..."})
    langfuse.create_score(
        name="user_thumbs",
        value=1,
        data_type="BOOLEAN",
        trace_id=span.trace_id,
    )
```

Confirm the exact `create_score` API for your SDK version in [scores via SDK](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk).

## What good looks like

- Experiment run table compares baseline vs candidate on the **same** dataset  
- Failed items are inspectable with full traces (for agents: tools + final generation)  
- Score names match the [score catalog](score-catalog.md)  

## Do / don’t

**Do** version experiment names meaningfully (`baseline-gpt4o-mini`, `agent-prompt-v3`).  
**Don’t** silently change dataset items mid-comparison without noting it.  
**Don’t** use free-form score names that are not in the catalog.

## Related

- [Agent evaluation](agent-evaluation.md)  
- [Score catalog](score-catalog.md)  
- [LLM-as-Judge and OpenAI](llm-as-judge-and-openai.md)  
