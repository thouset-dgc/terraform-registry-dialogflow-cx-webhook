resource "google_storage_bucket" "cloud_run_function_sources" {
  name     = "${var.project_id}-cloud-run-functions-sources"
  location = var.region
}

data "archive_file" "archive_webhook_function" {
  type        = "zip"
  source_dir  = "${path.module}/webhook_function_code/"
  output_path = "${path.module}/webhook_cloud_function.zip"

  depends_on = [
    google_storage_bucket.cloud_run_function_sources,
  ]
}

resource "google_storage_bucket_object" "webhook_function_zip" {
  name         = "${data.archive_file.archive_webhook_function.output_md5}.zip"
  content_type = "application/zip"

  bucket = google_storage_bucket.cloud_run_function_sources.name
  source = data.archive_file.archive_webhook_function.output_path

  depends_on = [
    data.archive_file.archive_webhook_function,
  ]
}


