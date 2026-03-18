# ADR 0006: Dependency - python-dotenv (Rejected)

* **Status:** Rejected
* **Date:** 2026-02-26
* **Author:** Gemini Antigravity Agent
* **Deciders:** User

## Context and Problem Statement
We need a way to load local environment variables from a `.env` file during local testing and execution of the `pr-agent` runner script.

## Decision Drivers
* Security (OpenSSF Score > 7.0 required).
* Minimizing external dependencies where standard library functionality suffices.

## Considered Options
1. **python-dotenv**: The standard third-party library for loading `.env` files. OpenSSF Score: 4.9.
2. **Native Python parsing**: Writing a trivial file parser using Python's built-in `os` and `pathlib`. OpenSSF Score: N/A (Standard Library).

## Decision Outcome
Chosen option: "Native Python parsing", because loading a `.env` file natively in Python is trivial (iterating lines and splitting on `=`). The `python-dotenv` library has an OpenSSF score of 4.9 (below our mandated 7.0) and introduces an unnecessary addition to the supply chain for functionality that can be achieved securely in ~5 lines of standard Python code.

### Security Assessment
* **OpenSSF Score:** N/A (Standard Library)
* **Vulnerability Scan:** N/A
* **Install Scripts:** N/A

## Consequences
* **Good:** Eliminates an unnecessary third-party dependency with a low score, reducing the attack surface.
* **Bad:** Requires writing and maintaining ~5 lines of custom `.env` parsing logic, which is a negligible trade-off.
