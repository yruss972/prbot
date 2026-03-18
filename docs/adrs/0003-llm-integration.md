# ADR-0003: LLM Integration - Cloudflare AI Gateway + Premium Models

## Status
Accepted (Revised from direct Gemini API calls)

## Context
The bot requires an LLM to read the PR diff, analyze it, and formulate a review.
* **Technical Constraints:** Must process large context windows (diffs).
* **Business Drivers:** The solution should utilize existing subscriptions (Google AI Pro for Gemini 3.1 Pro or Opus 4.6 via Anthropic) rather than relying strictly on older, free-tier models (like Gemini 2.5 Flash), while utilizing Cloudflare's infrastructure.

## Decision
We will use **Cloudflare AI Gateway** to route requests to premium LLM providers (Google AI Studio for Gemini 3.1 Pro, or Anthropic for Claude 3.5/4.6 Opus).

## Rationale
* **Technical Alignment:** Cloudflare AI Gateway acts as a proxy, providing observability (logs, analytics), caching, and rate-limiting. It natively supports Google Vertex AI/AI Studio and Anthropic as providers.
* **Efficiency:** Caching identical PR diffs (if re-requested) saves costs and latency.
* **Sustainability:** We are decoupled from a specific provider's SDK. Switching from Gemini 3.1 to Opus 4.6 is a matter of changing a configuration string and API key in the Gateway settings, not rewriting the fetch logic in the worker.
* **Quality:** Gemini 3.1 Pro and Claude Opus represent the state-of-the-art for code reasoning, significantly outperforming older/free models. Since the user has a Google AI Pro subscription, we can utilize those API keys.

## Alternatives Considered
| Alternative | Pros | Cons |
| :--- | :--- | :--- |
| **Direct API Calls (Original ADR)** | Simpler setup | Lacks unified observability, harder to swap models, no built-in caching. |
| **Workers AI (Native LLMs)** | Completely free, runs on the edge | Models (like Llama 3 8B) lack the profound code reasoning and massive context windows of Gemini 1.5/3.1 Pro or Claude Opus. |

## Consequences
* **Positive:** Future-proof architecture. High-quality reviews. Built-in observability.
* **Negative:** Requires initial setup of AI Gateway in the Cloudflare dashboard. Requires managing API keys for the chosen provider (Google or Anthropic).
* **Risks:** If the PR diff exceeds the provider's token limit, the request will fail (though Gemini and Claude have massive 2M+ context windows, so this is unlikely).

## Implementation & Compliance
* **Migration:** Provision an AI Gateway in the Cloudflare Dashboard. Construct LLM requests using the Gateway's endpoint format rather than hitting `generativelanguage.googleapis.com` directly.
* **Validation:** Check AI Gateway logs in the Cloudflare dashboard to ensure requests are routed correctly and caching works.
