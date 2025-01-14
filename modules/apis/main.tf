variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "apis" {
  description = "List of APIs to be enabled"
  type        = list(string)
}

resource "google_project_service" "enabled_apis" {
  for_each = toset(var.apis)
  project  = var.project_id
  service  = each.key
}
