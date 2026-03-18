# ADR-0004: Execution Engine - PR-Agent CLI on Cloudflare Pages

## Status
Proposed (Supersedes custom JS/Hono Webhook approach)

## Context
The user wants to leverage existing open-source tools (like Codium's `pr-agent`) instead of writing custom API integration code in JavaScript/Hono, pointing it at Cloudflare AI Gateway.
* **Technical Constraints:** Cloudflare Pages' build environment must execute the code. Cloudflare Pages does *not* natively expose the PR Number or PR URL as an environment variable to the build runner.
* **Business Drivers:** Maximize use of existing, battle-tested code review tools. Minimize custom boilerplate.

## Decision
We will use **Cloudflare Pages as the build/execution runner** to execute the **`pr-agent` CLI** tool (Python). We will write a small Python wrapper script that fetches the correct Pull Request URL using the GitHub API (based on the `CF_PAGES_BRANCH` environment variable) and then executes `pr-agent`.

## Rationale
* **Technical Alignment:** Cloudflare Pages defaults to Python 3.13 in its v3 build environment, fully supporting `pr-agent` (which requires >= Python 3.12).
* **Efficiency:** `pr-agent` is an industry-standard, well-maintained tool that handles the complex logic of parsing diffs, chunking, and formatting Markdown comments perfectly. Writing this from scratch in JS is "reinventing the wheel."
* **Sustainability:** By using `pr-agent`, we inherit all its future improvements (custom labels, chat commands, improved prompts) for free.

## Alternatives Considered
| Alternative | Pros | Cons |
| :--- | :--- | :--- |
| **Custom JavaScript Worker (Hono)** | Extremely fast, native edge execution | Requires writing custom logic for fetching diffs, constructing LLM prompts, parsing responses, and formatting GitHub comments. |
| **GitHub Actions** | Natively injects PR contexts and `GITHUB_TOKEN`. | Explicitly rejected by user constraints. |

## Consequences
* **Positive:** Zero custom ML/Prompt logic required. Highly robust output.
* **Negative:** We must provide a GitHub Personal Access Token (PAT) as an environment variable (`GITHUB_TOKEN`) to the Cloudflare Pages project, as the built-in Pages GitHub app token is not exposed/suitable for `pr-agent`.
* **Risks:** The Pages build timeout (20 mins free tier) is more than enough for a PR review, but we'll consume our 500 free Pages builds per month doing this. For a solo developer, 500 builds/month (roughly ~16 builds/day) is well within expected usage.

## Implementation & Compliance
* **Migration:** Create `build.sh` and `run_pr_agent.py` in the repository. Configure Cloudflare Pages to execute `bash build.sh` on deployment.
* **Validation:** Set environmental variables (`OPENAI__KEY`, `OPENAI__API_BASE` pointing to Cloudflare AI Gateway, and `GITHUB_TOKEN`) and trigger a PR to observe the CLI output in the Pages Build Logs.
