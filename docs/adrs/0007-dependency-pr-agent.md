# ADR 0007: Dependency - pr-agent

* **Status:** Proposed
* **Date:** 2026-02-26
* **Author:** Gemini Antigravity Agent
* **Deciders:** User

## Context and Problem Statement
We need the core AI execution engine to perform the automated pull request reviews without writing all the diff-chunking and LLM-prompting logic from scratch.

## Decision Drivers
* Alignment with ADR-0004 (Execution Engine).
* Security (OpenSSF Score > 7.0 required, though exceptions can be made via ADR).

## Considered Options
1. **pr-agent (Codium-ai)**: Excellent specialized PR review logic. OpenSSF Score: 5.4.

## Decision Outcome
Chosen option: "pr-agent", because it's the core engine selected in ADR-0004. Its OpenSSF score (5.4) is below 7.0 (largely due to branch protection API read issues and missing packaging workflows), but its functionality is essential to the project and saves massive amounts of boilerplate.

### Security Assessment
* **OpenSSF Score:** 5.4
* **Vulnerability Scan:** 9 Known Vulnerabilities in Dependencies.
  * 8 relate to `aiohttp` (GHSA-54jq-c3m8-4m76, GHSA-69f9-5gxw-wvc2, GHSA-6jhg-hg63-jvvf, GHSA-6mq8-rvhq-8wgg, GHSA-fh55-r93g-j68g, GHSA-g84x-mcqj-x9qq, GHSA-jj3x-wxrx-4x23, GHSA-mqqc-3gqh-h2x8). These primarily involve Denial of Service (DoS) and path leaking. Since `prbot` will execute as an ephemeral, isolated process triggered by webhooks, a memory DoS in an underlying async HTTP library poses minimal risk to our infrastructure (it would just restart the container/process).
  * 1 relates to `google-cloud-aiplatform` (GHSA-wh2j-26j7-9728) involving predictable storage bucket naming. We are not utilizing Vertex AI Storage buckets, only interacting with LLM text endpoints, rendering this irrelevant to our attack surface.
* **Install Scripts:** None
## Consequences
* **Good:** Integrates complex PR review logic natively.
* **Bad:** Score is below 7.0, requiring this accepted exception.
