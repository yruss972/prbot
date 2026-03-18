# ADR-0001: Core Architecture - Cloudflare Provider Integrations

## Status
Accepted (Revised from Custom Webhook/GitHub App)

## Context
The project requires an automated PR review bot for personal projects developed by a solo developer.
* **Technical Constraints:** Must not require write access to the repository code. Cannot rely on GitHub Actions.
* **Business Drivers:** The solution must be completely free to operate.
* **New Insight:** We want to avoid reinventing the wheel with custom webhook handling if Cloudflare provides built-in integrations, and we want to leverage existing AI infrastructure (like AI Gateway).

## Decision
We will use **Cloudflare Pages with GitHub Integration** combined with a **Cloudflare Worker bound to Pages (or triggered by Deploy Hooks)** for event handling, and **Cloudflare AI Gateway** to route LLM requests. We will NOT build a custom GitHub App from scratch if we can leverage the native Cloudflare GitHub integration for commenting and status checks.

## Rationale
* **Technical Alignment:** Cloudflare Pages natively integrates with GitHub. When a PR is opened, Pages automatically deploys a preview and *can post a comment to the PR*. We can hook into this lifecycle (e.g., via a post-build script that triggers a Worker, or by using a Worker deployed alongside the Pages project) to execute the AI review.
* **Efficiency:** Eliminates the need to manually parse GitHub webhook signatures, manage a standalone GitHub App private key, and handle the OAuth/JWT lifecycle for simple comments.
* **Sustainability:** Relies on Cloudflare's maintained integration rather than custom code. AI Gateway provides observability, caching, and easy model swapping without changing core logic.

## Alternatives Considered
| Alternative | Pros | Cons |
| :--- | :--- | :--- |
| **Custom Webhook + GitHub App** (Original ADR) | Maximum control, zero reliance on "Pages" build times | High boilerplate for auth, signature validation, and payload parsing. Reinventing the wheel. |

## Consequences
* **Positive:** Less boilerplate code. Built-in observability via AI Gateway.
* **Negative:** We must reverse-engineer or carefully implement how to trigger the review *after* or *during* the Cloudflare Pages preview build, utilizing the tokens Cloudflare already possesses to comment on the PR.
* **Risks:** The native Cloudflare integration might not expose the specific permissions needed to post a *verbose code review* (vs just a "deploy preview" link), which might still necessitate a minimal custom GitHub Token (PAT).

## Implementation & Compliance
* **Migration:** Set up a dummy Cloudflare Pages project linked to the repo to observe the native webhook payloads.
* **Validation:** Verify we can intercept the PR event and post comments natively.
