
data "archive_file" "archive_function" {
  for_each    = var.cloud_run_functions_setting
  type        = "zip"
  source_dir  = each.value.source_dir
  output_path = "${each.value.output_path}.zip"

}

resource "google_storage_bucket_object" "function_zip" {
  for_each = var.cloud_run_functions_setting

  content_type = "application/zip"
  name         = "${data.archive_file.archive_function[each.key].output_md5}.zip"

  bucket = var.cloud_run_function_bucket_name
  source = data.archive_file.archive_function[each.key].output_path
}
