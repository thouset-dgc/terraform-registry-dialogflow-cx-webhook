
locals {
  sa_deploy_roles = [
    "roles/logging.logWriter",
    "roles/iam.serviceAccountUser",
    "roles/storage.objectUser",
    "roles/monitoring.admin",
    "roles/monitoring.notificationChannelEditor",
    "roles/cloudbuild.builds.builder",
    "roles/serviceusage.serviceUsageViewer",
    "roles/secretmanager.secretAccessor",
    "roles/resourcemanager.projectIamAdmin",
    "roles/viewer"
  ]

  sa_df_webhook_roles = [
    "roles/run.invoker",
    "roles/secretmanager.secretAccessor",
    "roles/cloudsql.client",
    "roles/bigquery.jobUser"
  ]

}

resource "google_project_iam_member" "cloudbuild_secretmanager_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:service-${var.project_number}@gcp-sa-cloudbuild.iam.gserviceaccount.com"
}

# resource "google_project_iam_member" "deploy_bindings" {
#   project  = var.project_id
#   for_each = toset(local.sa_deploy_roles)
#   role     = each.value
#   member   = "serviceAccount:${google_service_account.service_account["cloud-build-deploy"].email}"
# }

resource "google_project_iam_member" "df_webhook_bindings" {
  project  = var.project_id
  for_each = toset(local.sa_df_webhook_roles)
  role     = each.value
  member   = "serviceAccount:${google_service_account.service_account["df-webhook-${var.project_id}"].email}"
}

## You must create an instance of Dialogflow before applying this

# resource "google_project_iam_member" "dialogflow_run_invoker" {
#   project = var.project_id

#   member = "serviceAccount:service-${var.project_number}@gcp-sa-dialogflow.iam.gserviceaccount.com"
#   role   = "roles/run.invoker"
# }
