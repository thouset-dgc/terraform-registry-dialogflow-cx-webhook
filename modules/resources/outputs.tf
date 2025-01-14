output "webhook_cloud_run_functions_url" {
  description = "URL of cloud run functions used as webhook by Dialogflow CX"
  value       = google_cloudfunctions2_function.dialogflow_cx_webhook.url
  depends_on  = [google_cloudfunctions2_function.dialogflow_cx_webhook]
}

output "cloud_sql_secret_name" {
  description = "Cloud SQL Secret name"
  value       = google_secret_manager_secret.cloud_sql_secret.name
  sensitive   = true
}
