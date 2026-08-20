# Evaluation guidelines

## Start here for agents

**[Agent evaluation](agent-evaluation.md)** is the detailed golden path for multi-step / tool-using apps.  
**[Score catalog](score-catalog.md)** lists org-standard metric names — use them everywhere.

Official: [Evaluation overview](https://langfuse.com/docs/evaluation/overview), [core concepts](https://langfuse.com/docs/evaluation/core-concepts).

## What and why

**Evaluation** is how we judge quality of LLM or agent outputs — before and after shipping.

Langfuse stores judgments as **scores** attached to traces, observations, sessions, or dataset runs. You produce scores with humans, code, LLM-as-a-Judge, or the SDK/API.

We run evaluations against the **central** Langfuse project so datasets and experiment history stay shared and comparable.

## The evaluation loop

Maps to **build-time** (offline) vs **runtime** (online). We focus mainly on **runtime** scoring of live traces on Central Langfuse; build-time experiments gate changes before ship.

1. **Runtime (online)** — score live traces (LLM-as-a-Judge, code, user thumbs)  
2. **Build-time (offline)** — promote failures into a dataset; run experiments before deploy  
3. Ship if metrics pass; repeat  

That loop is how datasets grow from a few examples into a representative suite. See [product intent — agentic observability](../architecture/product-intent.md#3-agentic-observability-build-time-vs-runtime).

## Building blocks

| Object | Role |
|--------|------|
| **Score** | A named judgment (`NUMERIC`, `CATEGORICAL`, `BOOLEAN`, `TEXT`) |
| **Dataset / item** | Test cases (input + optional expected output) |
| **Experiment / run** | Execute your task over a dataset and score results |
| **Evaluation method** | How the score is produced (code, LLM judge, human, SDK) |

## If you want to… (feature map)

| If you want to… | Use |
|-----------------|-----|
| Evaluate an **agent** (tools + trajectory) | [Agent evaluation](agent-evaluation.md) |
| Pick stable metric names | [Score catalog](score-catalog.md) |
| Review / rate traces manually | [Annotation queues](https://langfuse.com/docs/evaluation/evaluation-methods/annotation-queues), [Scores via UI](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-ui) |
| Collect end-user feedback | `user_thumbs` via [SDK scores](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk) |
| Run deterministic checks | [Code evaluators](https://langfuse.com/docs/evaluation/evaluation-methods/code-evaluators) |
| Score subjective quality at scale | [LLM-as-a-Judge + OpenAI](llm-as-judge-and-openai.md) |
| Build reusable test cases | [Datasets and experiments](datasets-and-experiments.md) |
| Compare prompt / model / agent changes | [Experiments via SDK](https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk) / [UI](https://langfuse.com/docs/evaluation/experiments/experiments-via-ui) |
| Block deploys on regressions | [CI/CD experiments](https://langfuse.com/docs/evaluation/experiments/experiments-ci-cd) (pattern only in this repo) |
| Watch scores over time | [Score analytics](https://langfuse.com/docs/evaluation/scores/score-analytics) |

## Evaluation methods we use

| Method | When |
|--------|------|
| [Code evaluators](https://langfuse.com/docs/evaluation/evaluation-methods/code-evaluators) | Deterministic checks (JSON schema, required tools, max steps) |
| [LLM-as-a-Judge](llm-as-judge-and-openai.md) | Subjective criteria at scale — uses **OpenAI** on this platform |
| [Scores via SDK/API](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk) | Custom pipelines, user feedback |
| UI / annotation queues | Ground truth and spot checks |

## Do / don’t

**Do**

- Use [score catalog](score-catalog.md) names (`goal_achieved`, `faithfulness`, `tool_correctness`, …)  
- Keep datasets in Langfuse so you can compare experiment runs in the UI  
- Start with a small high-quality dataset; grow from production edge cases  
- For agents, score trajectory — not only the final message  

**Don’t**

- Treat a single LLM-judge score as absolute truth without spot-checking  
- Mix unrelated criteria into one vague score name  
- Run only online eval with no offline regression set  

## What good looks like

- Dataset of representative cases in the project  
- Experiment runs comparable in the UI after a prompt, model, or tool change  
- Live traces carrying the same score names you use offline  

## Guides in this section

- [Agent evaluation](agent-evaluation.md)  
- [Score catalog](score-catalog.md)  
- [Datasets and experiments](datasets-and-experiments.md)  
- [LLM-as-Judge and OpenAI](llm-as-judge-and-openai.md)  
