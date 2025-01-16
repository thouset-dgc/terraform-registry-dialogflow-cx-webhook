
# resource "google_cloudbuildv2_connection" "github_connection" {
#   project  = var.project_id
#   name     = "github_connection"
#   location = var.region


#   github_config {
#     #app_installation_id = 56848194
#     authorizer_credential {
#       oauth_token_secret_version = "projects/${var.project_id}/secrets/${google_secret_manager_secret.github_token_secret.secret_id}/versions/latest"
#     }
#   }
# }



# resource "google_cloudbuildv2_repository" "github_repo" {
#   project           = var.project_id
#   location          = var.region
#   name              = var.repository_name
#   parent_connection = google_cloudbuildv2_connection.github_connection.id #"projects/${var.project_id}/locations/${var.region}/connections/${var.connection_name}"
#   remote_uri        = "https://github.com/${var.owner}/${var.repository_name}.git"
# }
