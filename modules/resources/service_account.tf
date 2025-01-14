resource "google_service_account" "webhook_service_account" {
  account_id   = "df-webhook-${var.project_id}"
  display_name = "Service Account for Cloud Function used as Dialogflow CX webhook"
}

variable "dialoglow_service_account_roles" {
  description = "Service Account roles"
  type        = list(string)
  default = [
    "roles/run.invoker",
    "roles/secretmanager.secretAccessor",
    "roles/cloudsql.client",
    "roles/bigquery.jobUser"
  ]
}

resource "google_project_iam_member" "webhook_service_account_roles" {
  project = var.project_id
  member  = "serviceAccount:${google_service_account.webhook_service_account.email}"

  for_each = toset(var.dialoglow_service_account_roles)
  role     = each.value

  depends_on = [google_service_account.webhook_service_account]
}


#### Permission for Dialogflow Service Account 
## You must create an instance of Dialogflow before applying this
resource "google_project_iam_member" "dialogflow_service_account_roles" {
  project = var.project_id

  member = "serviceAccount:service-${var.project_number}@gcp-sa-dialogflow.iam.gserviceaccount.com"
  role   = "roles/run.invoker"

}
