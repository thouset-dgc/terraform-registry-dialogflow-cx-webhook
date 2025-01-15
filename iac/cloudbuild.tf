
# resource "google_cloudbuild_trigger" "tf_plan" {

#   project         = var.project_id
#   name            = "${var.project_id}-plan"
#   location        = var.region
#   filename        = "cloudbuild.yaml"
#   service_account = google_service_account.service_account["cloud-build-deploy"].id

#   repository_event_config {
#     repository = google_cloudbuildv2_repository.github_repo.id
#     pull_request {
#       branch = (var.environment == "dv") ? "^(develop)$" : (var.environment == "qa") ? "^(preprod)$" : "^(prod)$"
#     }
#   }

#   substitutions = {
#     _APPLY_CHANGES = "false"
#     _ENV           = var.environment
#   }

# }


# resource "google_cloudbuild_trigger" "tf_apply" {

#   project         = var.project_id
#   name            = "${var.project_id}-apply"
#   location        = var.region
#   filename        = "cloudbuild.yaml"
#   service_account = google_service_account.service_account["cloud-build-deploy"].id

#   repository_event_config {
#     repository = google_cloudbuildv2_repository.github_repo.id
#     push {
#       branch = (var.environment == "dv") ? "^(develop)$" : (var.environment == "qa") ? "^(preprod)$" : "^(prod)$"
#       #branch = (var.environment == "pd") ? "^(prod)$" : "^(preprod)$"
#     }
#   }

#   substitutions = {
#     _APPLY_CHANGES = "true"
#     _ENV           = var.environment
#   }

# }
