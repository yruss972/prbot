# OSSF Recommendation: Disable GitHub Actions if unused to reduce attack surface
resource "github_actions_repository_permissions" "disable_actions" {
  repository      = github_repository.prbot.name
  enabled         = false
  allowed_actions = "local_only"
}
