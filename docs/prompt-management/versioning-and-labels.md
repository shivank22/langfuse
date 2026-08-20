# Versioning and labels

## Versioning

Every save creates a new **version**. Versions are immutable; you promote by moving labels, not by editing history.

Official: [Prompt version control](https://langfuse.com/docs/prompt-management/features/prompt-version-control).

## Labels (org convention)

| Label | Meaning |
|-------|---------|
| `production` | What production apps must fetch |
| `staging` | Candidate for shared non-prod validation |
| `latest` | Optional; avoid as the only production selector |

Promotion flow:

1. Edit / create a new version in the UI (or SDK)  
2. Test in `staging` (apps in staging fetch `label="staging"`)  
3. Move `production` to that version when ready  

## Naming prompts

Use stable, descriptive names:

- `{domain}-{role}` → `support-system`, `support-classifier`  
- Avoid names tied to a single experiment (`test123`)  

## Linking to traces

When the app fetches a prompt and runs a generation, link the prompt to the trace so you can filter quality by version. Official: [Link prompts to traces](https://langfuse.com/docs/prompt-management/features/link-to-traces).

## Caching

SDKs cache prompts client-side. Expect near-memory latency after the first fetch; see [caching](https://langfuse.com/docs/prompt-management/features/caching). Plan for a short delay after label moves before all instances see the new version (cache TTL).

## Do / don’t

**Do** document who may move the `production` label for each prompt.  
**Don’t** delete old versions that still appear on historical traces you care about.
