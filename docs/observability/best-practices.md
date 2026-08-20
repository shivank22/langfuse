# Best practices — what a good trace looks like

Trace structure is not cosmetic. Evaluators, dashboards, dataset experiments, and saved views all depend on stable names, nesting, and meaningful input/output.

Official: [What does a good trace look like?](https://langfuse.com/docs/observability/best-practices).

## Scope of one trace

A **trace** = one self-contained unit of work:

| Good trace scope | Group with sessions instead |
|------------------|-----------------------------|
| One chatbot **turn** | Whole conversation |
| One **agent run** | Several agent runs in a workflow |
| One pipeline execution | Multiple pipeline jobs over time |

For chat: **one trace per turn**, **one session per conversation**. That keeps traces small and the session view useful. See [sessions](sessions.md).

## Look at the trace tree

### Right steps and types

You should see LLM calls as **generations** (with model + tokens), tools as tool steps, and orchestration as spans. Wrong types break cost views and LLM-as-a-Judge targeting.

### Nesting

Tool calls nest under the agent/span that orchestrated them, as siblings of the generation that requested them — not dangling at the root.

```text
agent-run                    (span)
├── plan                     (span)
├── openai-decide            (generation)
├── tool-search-kb           (tool / span)
└── openai-final             (generation)
```

See [instrumentation](instrumentation.md).

### Reduce noise

Drop or filter HTTP/DB/framework internals that do not help you understand the LLM path. Official tip: [unwanted spans](https://langfuse.com/faq/all/unwanted-http-database-spans).

## Naming (treat like an API)

Names are referenced by evaluators, dashboards, and saved filters. Renaming silently breaks them.

**Do**

- Verb-first, stable names: `classify-intent`, `retrieve-context`, `generate-response`  
- Org patterns: root `{use-case}`, LLM `openai-{purpose}`, tools `tool-{name}`  

**Don’t**

- Put dynamic IDs in names (`process-order-8945`) — use metadata  
- Name by model (`gpt-4o`) — model is a generation attribute; models change  

## Meaningful input and output

- **Root observation**: set input/output to what a reviewer needs at a glance (user message → assistant answer). Raw blobs go in metadata.  
- **Generations**: messages / prompt in, completion out; include usage.  
- Empty I/O on “important” steps usually means the observation is noise or incomplete.

Root I/O feeds the tracing table, [dataset experiments](../evaluation/datasets-and-experiments.md), and many judges.

## Useful attributes

| Mechanism | Use for |
|-----------|---------|
| **Metadata** | Request IDs, feature flags, eval context, raw payloads |
| **Tags** | Business dimensions known upfront (`team`, `service`) — [tags](tags-and-metadata.md) |
| **Scores** | Post-hoc judgments (do not use tags for eval results) |
| **Environment** | `dev` / `staging` / `production` — [environments](environments.md) |
| **User ID** | Per-user cost and quality views |
| **Prompt link** | When using [prompt management](../prompt-management/overview.md), link prompts to generations |

### Tokens and cost on generations

For cost dashboards you need on each `generation`:

- Model name (matches Langfuse pricing table when possible)  
- Usage details (input/output tokens)  
- Optional explicit cost override  

OpenAI integrations often capture this automatically; manual code should set `usage_details` as in [get started](get-started.md).

## Agents and evaluation

Agent evals assume this structure. See [agent evaluation](../evaluation/agent-evaluation.md) and the [score catalog](../evaluation/score-catalog.md).

## What good looks like in the UI

- Trace tree reads like a story of the request  
- Filter `environment=production` + tag `your-service` returns only your traffic  
- Generations show model, tokens, and readable I/O  
- Multi-turn chats appear under one session with one trace per turn  

## Do / don’t

**Do** keep names stable once evaluators and dashboards depend on them.  
**Don’t** mix prod and non-prod in the same environment label.  
**Don’t** put secrets in input, output, tags, or metadata.

## Related

- [Data model](data-model.md)  
- [Instrumentation](instrumentation.md)  
- [Sessions](sessions.md)  
- [Environments](environments.md)  
- [Tags and metadata](tags-and-metadata.md)  
