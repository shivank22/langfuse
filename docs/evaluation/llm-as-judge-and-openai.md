# LLM-as-a-Judge and OpenAI

## Role of OpenAI in this platform

We standardize on **OpenAI** as the AI resource for:

1. **Application LLM calls** (teams’ apps — via `OPENAI_API_KEY` in the app)  
2. **Langfuse LLM-as-a-Judge** and related in-product LLM features on the central instance  

Official: [LLM-as-a-Judge](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge).

## Configure the judge on the central instance

Central operators (or project admins) configure an LLM connection in the Langfuse UI for the shared project, using an org-managed OpenAI API key.

Typical steps:

1. Open the central Langfuse UI → project settings / LLM connections  
2. Add **OpenAI** with the org key and a default model (`gpt-4o-mini` for cheap judges; stronger models for critical safety/goal criteria)  
3. Create an evaluator / template (criteria, score type, variable mapping)  
4. Target **Live observations** (recommended for production) and/or **Experiments**  
5. Set **sampling** (e.g. 5–10% of matching traces) to control cost  

App teams do **not** need to embed the judge key in every service if judging runs inside Langfuse; they still need OpenAI keys for their own generation calls.

Use [score catalog](score-catalog.md) names for the score the judge writes (`faithfulness`, `goal_achieved`, `harmful_content`, …).

## When to use LLM-as-a-Judge

**Use when**

- Criteria are subjective (tone, helpfulness, groundedness narrative)  
- You need scale beyond human review  
- You are scoring agent **final answers** or summarizing **trajectories**  

**Prefer code evaluators when**

- Checks are deterministic (valid JSON, required tools, max steps, exact match)  
- You need fully reproducible CI gates without LLM variance  

## Judging agents (trajectory-aware)

Agents need more than “is this text nice?”. Configure separate judges (or rubrics) for:

| Catalog score | Judge focus | Inputs to map into the prompt |
|---------------|-------------|-------------------------------|
| `goal_achieved` | Did the final answer solve the user goal? | user goal + final answer |
| `faithfulness` | Is the answer supported by tool/context results? | tool outputs / retrieved context + final answer |
| `answer_relevance` | On-topic vs the ask? | user goal + final answer |
| `harmful_content` | Safety / policy | final answer (+ optional user goal) |

**Trajectory tip:** Prefer judging the **final generation observation** (or a compact summary of tool names + final answer) rather than dumping an entire huge trace into the judge prompt. For path correctness (`tool_correctness`, `trajectory_ok`), prefer [code evaluators](agent-evaluation.md) over judges.

### Example rubric snippets (customize in the UI)

**Faithfulness (numeric 0–1)** — reason first, then score:

```text
You evaluate whether the ASSISTANT_ANSWER is faithful to CONTEXT (tool results / retrieved docs).
User goal: {{user_goal}}
CONTEXT: {{context}}
ASSISTANT_ANSWER: {{answer}}

List any claims not supported by CONTEXT. Then return a faithfulness score from 0 to 1
(1 = fully supported, 0 = unsupported or contradicted).
```

**Goal achieved (boolean)** —

```text
User goal: {{user_goal}}
Assistant answer: {{answer}}

Did the assistant achieve the user goal? Answer true or false and briefly justify.
```

Map UI template variables to observation/trace fields (input, output, metadata) per Langfuse’s evaluator configuration.

## Org practice

- Name templates after the catalog score (`faithfulness-v1`, `goal_achieved-agent-v1`)  
- Spot-check a sample of judge scores when first rolling out; calibrate against human labels when stakes are high  
- Prefer the same score **names** online and offline  
- Sample production traffic; do not judge 100% of high-volume agents without a cost plan  

## Cost and safety

- Judges multiply OpenAI cost (every scored observation can call the model) — use filters (trace name, tags, environment) + sampling  
- Multi-step agent traces are large: send only what the rubric needs  
- Do not send unnecessary PII into judge prompts; follow org data policies  
- Prefer models that support **structured output** so scores parse reliably  

## Related

- [Agent evaluation](agent-evaluation.md)  
- [Score catalog](score-catalog.md)  
- [Evaluation overview](overview.md)  
- [Datasets and experiments](datasets-and-experiments.md)  
- [Operations — deploy](../operations/deploy.md)  
