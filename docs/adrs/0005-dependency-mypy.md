# ADR 0005: Dependency - mypy

* **Status:** Proposed
* **Date:** 2026-02-26
* **Author:** Gemini Antigravity Agent
* **Deciders:** User

## Context and Problem Statement
We need a static type checker for the Python execution scripts (`run_pr_agent.py`) as mandated by the `PYTHON_RULES.md` ecosystem rules.

## Decision Drivers
* Security (OpenSSF Score > 7.0 required by our rules, though exceptions can be made via ADR).
* Ecosystem rules strictly mandate `mypy` for static type checking.

## Considered Options
1. **mypy**: The official standard, heavily supported, explicitly mandated by `PYTHON_RULES.md`. OpenSSF Score: 6.8.

## Decision Outcome
Chosen option: "mypy", because it is strictly mandated by the project's Python rules governing type checking, despite its score being slightly below the 7.0 threshold.

### Security Assessment
* **OpenSSF Score:** 6.8
* **Vulnerability Scan:** Clean (Trivy dependency scan).
* **Install Scripts:** None.

## Consequences
* **Good:** Strict type checking ensures robust scripts when interacting with GitHub webhooks and APIs.
* **Bad:** The OpenSSF score (6.8) is technically below the 7.0 threshold, primarily due to lacking pinned dependencies in some core build workflows, but as a foundational Python tool, the risk is accepted.
