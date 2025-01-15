output "enabled_apis" {
  description = "Enabled APIs in the GCP project"
  value       = keys(google_project_service.enabled_apis)
}
