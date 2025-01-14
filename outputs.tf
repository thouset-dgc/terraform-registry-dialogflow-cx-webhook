output "project_id" {
  description = "ID of GCP project"
  value       = var.project_id
}

output "enabled_apis" {
  description = "Enabled APIs in the GCP project"
  value       = module.gcp_apis.enabled_apis
}

output "cloud_run_functions_url" {
  description = "Cloud Run Functions URL"
  value       = module.gcp_resources.webhook_cloud_run_functions_url
}

output "cloud_sql_secret_name" {
  description = "Secret name for Cloud SQL instance"
  value       = module.gcp_resources.cloud_sql_secret_name
  sensitive   = true
}
