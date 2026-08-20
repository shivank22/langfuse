# Prompt management guidelines

## What and why

**Prompt management** stores and versions prompts in Langfuse instead of hardcoding them in application deploys.

That separates prompt iteration (product / domain) from code deployment (engineering). Apps fetch the prompt by name and label; the SDK caches it client-side so retrieval stays low-latency.

Official overview: [Prompt management](https://langfuse.com/docs/prompt-management/overview).

## Why we require it for shared services

- One change in the UI can roll forward without a full release  
- Traces can be linked to prompt versions for performance analysis  
- Labels (`production`, `staging`) make promotions explicit  

## Core concepts

| Concept | Meaning |
|---------|---------|
| **Prompt** | Named text or chat message template |
| **Version** | Immutable revision of that prompt |
| **Label** | Pointer such as `production` or `staging` on a version |
| **Config** | Optional structured config alongside the prompt |

Data model: [prompt types, versioning, labels](https://langfuse.com/docs/prompt-management/data-model).

## Do / don’t

**Do**

- Keep production prompts in Langfuse; fetch by name + `production` label  
- Link prompt versions to traces when generating  
- Use `staging` (or similar) labels before promoting  

**Don’t**

- Ship new production prompt text only in git with no Langfuse version  
- Fetch “latest” unstructured tips without labels in production  
- Put secrets inside prompt templates  

## What good looks like

- Prompt library in the UI with clear names (`support-system`, `summarize-ticket`)  
- `production` label on the live version; older versions retained  
- Traces show which prompt version produced the output  

## Guides in this section

- [Versioning and labels](versioning-and-labels.md)
- [Use in applications](use-in-applications.md)
