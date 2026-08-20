# Score catalog (org-standard metrics)

Stable **score names** for the central Langfuse project. Use these in code evaluators, LLM-as-a-Judge templates, SDK `create_score` calls, and dashboards. Do not invent synonyms (`goal_ok`, `achieved_goal`, …).

Official score types: [Scores](https://langfuse.com/docs/evaluation/scores/overview).

Agent usage: [Agent evaluation](agent-evaluation.md).

## How to read this catalog

| Field | Meaning |
|-------|---------|
| **Name** | Exact Langfuse score `name` |
| **Type** | `BOOLEAN` / `NUMERIC` / `CATEGORICAL` / `TEXT` |
| **Applies to** | Trace, observation, session, or dataset run |
| **Pass** | Org default threshold |
| **Method** | Preferred way to produce the score |
| **Owner** | Who defines criteria and monitors the metric |

---

## Outcome / quality

### `goal_achieved`

| | |
|--|--|
| **Type** | `BOOLEAN` (or `NUMERIC` 0–1 if you need soft scores) |
| **Definition** | Did the agent satisfy the user’s stated goal? |
| **Applies to** | Trace or dataset run |
| **Pass** | `true` (or `>= 0.7` if numeric) |
| **Method** | Code if checkable (keywords / expected fields); else LLM-as-a-Judge (OpenAI); humans for ground truth |
| **Owner** | App team |
| **When** | Offline experiments (required); online sample recommended |

### `answer_relevance`

| | |
|--|--|
| **Type** | `NUMERIC` 0–1 |
| **Definition** | Final answer addresses the user ask (not off-topic) |
| **Applies to** | Trace / final generation |
| **Pass** | `>= 0.7` |
| **Method** | LLM-as-a-Judge |
| **Owner** | App team |
| **When** | Offline + online sample |

### `faithfulness`

| | |
|--|--|
| **Type** | `NUMERIC` 0–1 |
| **Definition** | Claims in the answer are supported by tool results / retrieved context (groundedness) |
| **Applies to** | Trace / final generation |
| **Pass** | `>= 0.7` |
| **Method** | LLM-as-a-Judge with context + answer in the prompt |
| **Owner** | App team |
| **When** | Required for RAG and tool-using agents |

### `correctness`

| | |
|--|--|
| **Type** | `BOOLEAN` or `NUMERIC` 0–1 |
| **Definition** | Matches expected output when a reference answer exists |
| **Applies to** | Dataset run |
| **Pass** | `true` / `>= 0.8` |
| **Method** | Code (exact / contains); LLM-as-a-Judge vs reference for paraphrase |
| **Owner** | App team |
| **When** | Offline only (needs expected output) |

### `completeness`

| | |
|--|--|
| **Type** | `BOOLEAN` or `NUMERIC` 0–1 |
| **Definition** | Required fields, steps, or citations are present |
| **Applies to** | Trace / dataset run |
| **Pass** | `true` / `>= 0.8` |
| **Method** | Code evaluator preferred |
| **Owner** | App team |

---

## Agent / trajectory

### `tool_correctness`

| | |
|--|--|
| **Type** | `BOOLEAN` (or `NUMERIC` fraction of correct tools) |
| **Definition** | Agent called the expected tool(s) with acceptable arguments |
| **Applies to** | Trace / dataset run |
| **Pass** | `true` |
| **Method** | Code evaluator vs `expected_tools` on dataset items |
| **Owner** | App team |
| **When** | Offline (required for tool agents); optional online if you log tool names |

### `tool_success_rate`

| | |
|--|--|
| **Type** | `NUMERIC` 0–1 |
| **Definition** | Share of tool calls that returned without error |
| **Applies to** | Trace |
| **Pass** | `>= 0.95` (tune per service) |
| **Method** | Code / SDK from span status |
| **Owner** | App team |

### `trajectory_ok`

| | |
|--|--|
| **Type** | `BOOLEAN` |
| **Definition** | Path is acceptable: no useless loops, within max steps, order constraints met |
| **Applies to** | Trace / dataset run |
| **Pass** | `true` |
| **Method** | Code evaluator (max steps, duplicate detection); optional judge for soft path quality |
| **Owner** | App team |

### `step_efficiency`

| | |
|--|--|
| **Type** | `NUMERIC` (step count or inverse efficiency) |
| **Definition** | How many steps the agent used relative to a budget |
| **Applies to** | Trace |
| **Pass** | Steps `<=` budget (encode budget in metadata or evaluator config) |
| **Method** | Code |
| **Owner** | App team |

### `handoff_correct`

| | |
|--|--|
| **Type** | `BOOLEAN` |
| **Definition** | Multi-agent: correct specialist / handoff target selected |
| **Applies to** | Trace |
| **Pass** | `true` |
| **Method** | Code vs expected handoff; or LLM-as-a-Judge |
| **Owner** | App team |
| **When** | Only for multi-agent systems |

---

## Safety / policy

### `harmful_content`

| | |
|--|--|
| **Type** | `BOOLEAN` (`true` = failure / harmful) |
| **Definition** | Output violates safety policy (toxicity, disallowed advice, etc.) |
| **Applies to** | Trace / generation |
| **Pass** | `false` |
| **Method** | LLM-as-a-Judge and/or policy code filters |
| **Owner** | App team + central security/policy as applicable |
| **When** | Online sample on production; offline on safety dataset |

### `pii_leak`

| | |
|--|--|
| **Type** | `BOOLEAN` (`true` = leak detected) |
| **Definition** | Sensitive PII exposed inappropriately in the output |
| **Applies to** | Trace / generation |
| **Pass** | `false` |
| **Method** | Code / DLP libraries preferred; judge as supplement |
| **Owner** | App team + compliance |

### `policy_violation`

| | |
|--|--|
| **Type** | `BOOLEAN` or `CATEGORICAL` |
| **Definition** | Business or domain policy breach (e.g. unauthorized refund promise) |
| **Applies to** | Trace |
| **Pass** | `false` / category `none` |
| **Method** | Code or LLM-as-a-Judge with explicit policy text |
| **Owner** | App team |

---

## Ops / UX

### `latency_ms`

| | |
|--|--|
| **Type** | `NUMERIC` (milliseconds) |
| **Definition** | End-to-end agent latency |
| **Applies to** | Trace |
| **Pass** | Informational; pair with `latency_budget` |
| **Method** | From trace timings / SDK |
| **Owner** | App team |

### `latency_budget`

| | |
|--|--|
| **Type** | `BOOLEAN` |
| **Definition** | Latency within the service SLA |
| **Applies to** | Trace / dataset run |
| **Pass** | `true` |
| **Method** | Code evaluator |
| **Owner** | App team |

### `cost_budget`

| | |
|--|--|
| **Type** | `BOOLEAN` |
| **Definition** | Estimated token cost within budget for the run |
| **Applies to** | Trace |
| **Pass** | `true` |
| **Method** | Code from usage details |
| **Owner** | App team |

### `user_thumbs`

| | |
|--|--|
| **Type** | `BOOLEAN` (`1`/`true` = up) |
| **Definition** | Explicit end-user feedback |
| **Applies to** | Trace / session |
| **Pass** | N/A (signal, not a gate alone) |
| **Method** | Scores via SDK from the product UI |
| **Owner** | App team |
| **When** | Online only |

---

## Picking metrics by agent type

| Agent type | Minimum set |
|------------|-------------|
| Tool-using task agent | `goal_achieved`, `tool_correctness`, `trajectory_ok`, `faithfulness`, `latency_budget` |
| RAG / research | `goal_achieved`, `faithfulness`, `answer_relevance`, `completeness` |
| Support chatbot | `goal_achieved`, `answer_relevance`, `harmful_content`, `user_thumbs` |
| Multi-agent | above + `handoff_correct` |

---

## Naming and ownership rules

1. **Snake_case**, English, stable forever once published in this catalog  
2. Same name **online and offline** for a given concept  
3. App teams own use-case criteria; central platform owns this catalog document and shared judge connections  
4. Propose new names via PR to this file — do not silently introduce them in one service  

## Related

- [Agent evaluation](agent-evaluation.md)  
- [LLM-as-Judge and OpenAI](llm-as-judge-and-openai.md)  
- [Datasets and experiments](datasets-and-experiments.md)  
