
locals {
  secret_id = [
    "github-token-secret",
    "cloud-sql-secret"
  ]
}

resource "google_secret_manager_secret" "secret" {
  for_each  = toset(local.secret_id)
  project   = var.project_id
  secret_id = each.value
  replication {
    auto {}
  }
}
