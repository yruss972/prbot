terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
  }
}

provider "github" {
  owner = var.github_owner
}

# The primary repository definition
resource "github_repository" "prbot" {
  name        = var.repository_name
  description = "Automated PR review bot using Cloudflare Pages and PR-Agent."
  visibility  = "public"

  has_issues   = true
  has_projects = false # OSSF Recommendation: Reduce attack surface
  has_wiki     = false # OSSF Recommendation: Reduce attack surface

  vulnerability_alerts = true # Dependabot alerts

  delete_branch_on_merge = true
  allow_auto_merge       = false
  allow_merge_commit     = false
  allow_rebase_merge     = false
  allow_squash_merge     = true
}
