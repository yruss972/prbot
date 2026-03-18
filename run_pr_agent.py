import os
import sys
import subprocess
import urllib.request
import json
from urllib.error import HTTPError

def load_env(filepath=".env"):
    """Trivial implementation to parse .env files natively to avoid extra dependencies"""
    if not os.path.exists(filepath):
        return

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            # Ignore comments and empty lines
            if not line or line.startswith("#"):
                continue

            # Split on the first '=' character
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                if key.startswith("export "):
                    key = key[7:].strip()
                value = value.strip().strip("'").strip('"')
                os.environ[key] = value


def get_pr_url_from_branch(branch: str, token: str) -> str:
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        try:
            remote_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).decode("utf-8").strip()
            if remote_url.startswith("https://"):
                repo = remote_url.split("github.com/")[-1].replace(".git", "")
            elif remote_url.startswith("git@"):
                repo = remote_url.split(":")[-1].replace(".git", "")
        except subprocess.CalledProcessError:
            pass

    if not repo:
        print("Error: Could not determine GITHUB_REPOSITORY from env or git remote.")
        return ""

    owner = repo.split('/')[0]
    api_url = f"https://api.github.com/repos/{repo}/pulls?state=open&head={owner}:{branch}"
    req = urllib.request.Request(api_url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "prbot"
    })

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            if data and len(data) > 0:
                return data[0].get("html_url", "")
    except HTTPError as e:
        print(f"GitHub API Error: {e.code} - {e.reason}")
    except Exception as e:
        print(f"Error fetching PR data: {e}")

    return ""


def main():
    load_env()

    # Ensure required secrets exist
    valid_llm_keys = ["OPENAI_KEY", "OPENAI__KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY", "ANTHROPIC_API_KEY"]
    if not any(os.environ.get(k) for k in valid_llm_keys):
        print(f"Error: At least one LLM API key must be set ({', '.join(valid_llm_keys)}).")
        sys.exit(1)

    if not os.environ.get("GITHUB_TOKEN"):
        print("Error: GITHUB_TOKEN environment variable must be set.")
        sys.exit(1)

    pr_url = None
    if len(sys.argv) >= 2:
        pr_url = sys.argv[1]
    else:
        branch = os.environ.get("CF_PAGES_BRANCH")
        if branch:
            if branch == "main":
                print("Skipping PR review for the 'main' branch.")
                sys.exit(0)
            print(f"Resolving PR URL for branch: {branch}")
            pr_url = get_pr_url_from_branch(branch, os.environ.get("GITHUB_TOKEN"))

    if not pr_url:
        print("Usage: uv run run_pr_agent.py <PR_URL>")
        print("Alternatively, ensure CF_PAGES_BRANCH is set and the branch has an open PR.")
        sys.exit(1)

    # We delay this import until after the environment variables are loaded
    # so pr-agent config initialization picks them up automatically.
    from pr_agent.cli import run_command  # type: ignore

    # Pr-agent expects arguments similarly to its CLI
    # `review` is the default action for a PR review
    print(f"Executing PR Agent review for: {pr_url}")
    run_command(pr_url=pr_url, command="review")


if __name__ == "__main__":
    main()
