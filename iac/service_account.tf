locals {
  service_account = {
    # "cloud-build-deploy"           = "Cloud Build Deploy Service Account",
    "df-webhook-${var.project_id}" = "Service Account for Cloud Function used as Dialogflow CX webhook"
  }
}

resource "google_service_account" "service_account" {
  for_each     = local.service_account
  project      = var.project_id
  account_id   = each.key
  display_name = each.value
}
