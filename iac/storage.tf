resource "google_storage_bucket" "cloud_run_function_sources" {
  name     = "${var.project_id}-cloud-run-functions-sources"
  location = var.region
}
