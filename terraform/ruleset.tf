# Define OSSF Compliant Branch Protections via Repository Rulesets
resource "github_repository_ruleset" "default_branch_protection" {
  name        = "default-branch-protection"
  repository  = github_repository.prbot.name
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["~DEFAULT_BRANCH"]
      exclude = []
    }
  }

  rules {
    # Block force pushes entirely
    non_fast_forward = true

    # Require linear history
    required_linear_history = true

    # Require PRs with 1 approval
    pull_request {
      required_approving_review_count = 1
      dismiss_stale_reviews_on_push   = true
      require_code_owner_review       = false
      require_last_push_approval      = true
    }

    # Require Signed Commits
    required_signatures = true
  }
}
