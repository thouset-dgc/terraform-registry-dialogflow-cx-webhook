resource "google_cloudfunctions2_function" "dialogflow_cx_webhook" {
  name        = var.function_name
  location    = var.region
  description = "My GCP Cloud Function used as webhook for Dialogflow CX"

  build_config {
    runtime     = "python310"
    entry_point = var.function_entry_point

    source {
      storage_source {
        bucket = google_storage_bucket.cloud_run_function_sources.name
        object = google_storage_bucket_object.webhook_function_zip.name
      }
    }
  }

  service_config {
    min_instance_count = 1
    available_memory   = "256M"
    timeout_seconds    = 360
    ingress_settings   = "ALLOW_ALL"

    service_account_email = google_service_account.webhook_service_account.email

    environment_variables = {
      LOG_EXECUTION_ID           = true
      PROJECT_ID                 = var.project_id
      PROJECT_REGION             = var.region
      PROJECT_CLOUD_SQL_INSTANCE = "chatbot"
    }

    secret_environment_variables {
      key        = "CLOUD_SQL_SECRET"
      project_id = var.project_id
      secret     = google_secret_manager_secret.cloud_sql_secret.secret_id
      version    = "latest"
    }
  }

  depends_on = [
    google_storage_bucket_object.webhook_function_zip,
    google_service_account.webhook_service_account
  ]
}
