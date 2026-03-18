# ADR-0002: Language and Web Framework - TypeScript and Hono

## Status
Proposed

## Context
The webhook receiver must be written in a language and framework that runs natively and efficiently on Cloudflare Workers.
* **Technical Constraints:** Must compile/bundle to run on V8 isolates (Cloudflare Workers).
* **Business Drivers:** Rapid development, clear routing, and strong type safety.

## Decision
We will use **TypeScript** as the language and **Hono** as the web framework.

## Rationale
* **Technical Alignment:** Hono is an ultrafast, lightweight, edge-native web framework that has first-class support for Cloudflare Workers. TypeScript provides compile-time safety which is critical for parsing and handling complex webhook payloads from GitHub.
* **Efficiency:** Hono's minimal overhead ensures fast cold starts and execution times, crucial for staying within worker limits and responding to webhooks within GitHub's required timeframes.
* **Sustainability:** Hono has a strong community and is the standard choice for modern Cloudflare Workers applications.

## Alternatives Considered
| Alternative | Pros | Cons |
| :--- | :--- | :--- |
| **Standard Fetch API** | Zero dependencies | Routing and middleware (like signature validation) must be built from scratch. |
| **Express.js** | Ubiquitous Node framework | Not natively compatible with Edge environments without heavy polyfilling; slow cold starts. |

## Consequences
* **Positive:** Clean, readable routing. Easy implementation of middleware for webhook signature verification. Strong typing for GitHub webhook payloads.
* **Negative:** Introduces a dependency (Hono).
* **Risks:** Minimal risks given Hono's stability on Cloudflare.

## Implementation & Compliance
* **Migration:** Initialize the project using the standard Hono Cloudflare Workers template (`npm create hono@latest`).
* **Validation:** Write unit tests to ensure routes match expected GitHub webhook paths.
* **Tooling:** `pnpm` (per NODE_RULES.md) for package management, `wrangler` for deployment.
