# ADR 0008: Dependency - ruff

* **Status:** Proposed
* **Date:** 2026-02-26
* **Author:** Gemini Antigravity Agent
* **Deciders:** User

## Context and Problem Statement
We need a linter and formatter for Python code as mandated by `PYTHON_RULES.md`.

## Decision Drivers
* Ecosystem rules mandate `ruff` for all Python formatting/linting.
* Security (OpenSSF Score > 7.0 required, though exceptions can be made via ADR).

## Considered Options
1. **ruff (astral-sh)**: Extremely fast Rust-based Python linter. OpenSSF Score: 6.7.

## Decision Outcome
Chosen option: "ruff", because it is strictly mandated by `PYTHON_RULES.md`.

### Security Assessment
* **OpenSSF Score:** 6.7
* **Vulnerability Scan:** Clean
* **Install Scripts:** None

## Consequences
* **Good:** Meets ecosystem rules, extremely fast, replaces multiple older tools (flake8, black, isort).
* **Bad:** Score is slightly below 7.0, requiring this accepted exception.
